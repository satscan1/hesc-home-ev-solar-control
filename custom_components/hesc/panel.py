"""The HESC dashboard, delivered by the integration itself.

HESC registers its own dashboard in the sidebar, so a user does not create a dashboard or paste
YAML, and an update of HESC brings the matching dashboard along.

The dashboard is `dashboard/hesc_v3_dashboard.yaml` in this folder, written with the entity ids
HESC gets on a fresh install (`sensor.hesc_v3_…`) and the default source entities (Solcast, HPVC).
Before it is served, every id that is different in this Home Assistant is replaced:
- HESC's own entities: found in the entity registry by platform and translation key (the key
  HESC's unique ids are built from), so a renamed entity keeps working;
- the sources: the entities chosen in HESC's setup (solar forecast today/tomorrow, HPVC limited).

The dashboard is registered in `async_setup`, before the config entry is set up, at the same
moment as the dashboards a user made. It stays registered while the entry reloads (an options
save reloads it) and goes away only when HESC is removed. A config entry that does not exist yet
(first install) registers it once the entry is set up.

Home Assistant has no public API for an integration-provided dashboard. HESC uses the same route
as a YAML dashboard from configuration.yaml (the lovelace component's dashboard table and panel
registration). If that route changes in a future Home Assistant, only the dashboard is missing;
HESC itself keeps working, and the error is logged.

When the address is already taken (for instance by a dashboard the user created by hand at
/hesc-v3), HESC leaves it alone and shows a repair notice.

Since 3.0.0 the same dashboard is also a dashboard strategy (`strategy: type: custom:hesc`, in
frontend/hesc-cards.js): *Settings → Dashboards → Add dashboard* lists it, and a user can make an
own copy at any address with one click, or take control of it to change it. The strategy asks
HESC for the config over the websocket (`hesc/dashboard`), with the links set to its own address.

Since 3.0.0 the dashboard also comes in other languages (`hesc_v3_dashboard.<lang>.yaml`, made from the
English one by tools/dashboard_translate.py; only the texts differ). Since 3.1.0 the sidebar dashboard
follows the language each user chose in the profile, like the one-click dashboard (before: the language
of Home Assistant, Settings → System → General, which is still the fallback). A language without its own
file gets the English dashboard.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback, valid_entity_id
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir
from homeassistant.util import slugify
from homeassistant.util.hass_dict import HassKey
from homeassistant.util.yaml import parse_yaml

from .const import (
    CONF_HPVC_LIMITED,
    CONF_SOLAR_TODAY,
    CONF_SOLAR_TOMORROW,
    DOMAIN,
    FIRST_INSTALL_DEFAULTS,
    NAME,
)

_LOGGER = logging.getLogger(__name__)

DASHBOARD_URL = "hesc-v3"
DASHBOARD_TITLE = "HESC"
DASHBOARD_ICON = "hesc:ev-zon"
DASHBOARD_FILE = Path(__file__).parent / "dashboard" / "hesc_v3_dashboard.yaml"
TRANSLATIONS_FILE = Path(__file__).parent / "translations" / "en.json"
ISSUE_URL_TAKEN = "dashboard_url_taken"
DATA_DASHBOARD: HassKey[HescDashboard] = HassKey(f"{DOMAIN}_dashboard")

# Source entities the dashboard names directly, with the setup field that holds the user's choice.
SOURCE_FIELDS = (CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW, CONF_HPVC_LIMITED)

_ID_CHARS = "A-Za-z0-9_"


def default_entity_ids(names: dict[str, dict[str, dict[str, Any]]]) -> dict[str, str]:
    """{"<platform>:<translation key>": entity id on a fresh install}.

    A fresh install names an entity "<device name> <entity name>" (has_entity_name) with the English
    name, as HESC ships only English entity names."""
    out: dict[str, str] = {}
    for platform, items in names.items():
        for key, item in items.items():
            name = (item or {}).get("name")
            if name:
                out[f"{platform}:{key}"] = f"{platform}.{slugify(f'{NAME} {name}')}"
    return out


def replace_ids(text: str, mapping: dict[str, str]) -> str:
    """Replace whole entity ids only: `sensor.hesc_v3_advice` never touches `sensor.hesc_v3_advice_x`."""
    pairs = {old: new for old, new in mapping.items() if old and new and old != new}
    if not pairs:
        return text
    pattern = re.compile(
        rf"(?<![{_ID_CHARS}])("
        + "|".join(re.escape(o) for o in sorted(pairs, key=len, reverse=True))
        + rf")(?![{_ID_CHARS}])"
    )
    return pattern.sub(lambda m: pairs[m.group(1)], text)


def id_mapping(hass: HomeAssistant, entry_id: str | None, defaults: dict[str, str], settings: dict[str, Any]) -> dict[str, str]:
    """{id in the shipped dashboard: id in this Home Assistant}, only for ids that differ."""
    mapping: dict[str, str] = {}
    if entry_id:
        reg = er.async_get(hass)
        for ent in er.async_entries_for_config_entry(reg, entry_id):
            if ent.platform != DOMAIN or not ent.translation_key:
                continue
            default = defaults.get(f"{ent.domain}:{ent.translation_key}")
            if default and default != ent.entity_id:
                mapping[default] = ent.entity_id
    for field in SOURCE_FIELDS:
        default = str(FIRST_INSTALL_DEFAULTS.get(field) or "")
        chosen = str(settings.get(field) or "").strip()
        # only a real entity id goes into the YAML text (values can come from v2's text helpers)
        if default and chosen and chosen != default and valid_entity_id(chosen):
            mapping[default] = chosen
    return mapping


def build_config(raw: str, mapping: dict[str, str]) -> dict[str, Any]:
    """The dashboard as Home Assistant serves it: ids replaced, then parsed."""
    config = parse_yaml(replace_ids(raw, mapping))
    if not isinstance(config, dict) or not isinstance(config.get("views"), list):
        raise HomeAssistantError("HESC dashboard file has no views")
    return config


class HescDashboard:
    """Registers, serves and removes HESC's own dashboard."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._raw = ""  # the English dashboard
        self._raw_lang: dict[str, str] = {}  # the other languages
        self._defaults: dict[str, str] = {}
        self._mapping: dict[str, str] | None = None
        self._config: dict[str, Any] | None = None  # in the language of Home Assistant
        self._config_lang = "en"
        self._json: Any = None
        self._lang_configs: dict[str, dict[str, Any]] = {}  # other languages (per user, and the strategy)
        self._lang_json: dict[str, Any] = {}
        self._lovelace: Any = None
        self.panel_registered = False
        self._unsub: Any = None

    # ---- the config entry, looked up when needed (it may reload or not exist yet) -------------
    def _entry(self) -> Any:
        entries = self.hass.config_entries.async_entries(DOMAIN)
        return entries[0] if entries else None

    def current_mapping(self) -> dict[str, str]:
        entry = self._entry()
        settings = dict(entry.options or entry.data) if entry else {}
        return id_mapping(self.hass, entry.entry_id if entry else None, self._defaults, settings)

    # ---- files and serving --------------------------------------------------------------------
    async def async_load_files(self) -> None:
        def _read() -> tuple[str, dict[str, str], dict[str, str]]:
            raw = DASHBOARD_FILE.read_text(encoding="utf-8")
            other = {
                f.name.split(".")[1]: f.read_text(encoding="utf-8")
                for f in DASHBOARD_FILE.parent.glob(DASHBOARD_FILE.stem + ".*.yaml")
            }
            names = json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8")).get("entity", {})
            return raw, other, default_entity_ids(names)

        self._raw, self._raw_lang, self._defaults = await self.hass.async_add_executor_job(_read)

    def language(self, lang: str | None = None) -> str:
        """The dashboard language for `lang` (default: Home Assistant's): its own file, or English."""
        code = (lang or self.hass.config.language or "en").replace("_", "-").split("-")[0].lower()
        return code if code in self._raw_lang else "en"

    def _source(self, lang: str) -> str:
        return self._raw_lang.get(lang, self._raw)

    async def async_config(self, force: bool = False) -> tuple[dict[str, Any], Any]:
        """The dashboard config, rebuilt only when an id changed (rename, other source)."""
        from homeassistant.helpers.json import cached_json_fragment

        mapping = self.current_mapping()
        lang = self.language()
        if force or self._config is None or mapping != self._mapping or lang != self._config_lang:
            config = await self._build(lang, mapping)
            self._config, self._mapping, self._config_lang = config, mapping, lang
            self._json = cached_json_fragment(config)
            self._lang_configs = {}
            self._lang_json = {}
        return self._config, self._json

    async def _build(self, lang: str, mapping: dict[str, str]) -> dict[str, Any]:
        raw = self._source(lang)
        try:
            return await self.hass.async_add_executor_job(build_config, raw, mapping)
        except Exception:
            _LOGGER.exception("HESC dashboard: filling in entity ids failed; serving the standard ids")
            return await self.hass.async_add_executor_job(build_config, raw, {})

    async def async_config_for(self, lang: str | None) -> dict[str, Any]:
        """The dashboard config in a user's language (the one-click dashboard)."""
        config, _ = await self.async_config()
        code = self.language(lang)
        if code == self._config_lang:
            return config
        if code not in self._lang_configs:
            self._lang_configs[code] = await self._build(code, self._mapping or {})
        return self._lang_configs[code]

    async def async_json_for(self, lang: str | None, force: bool = False) -> Any:
        """The sidebar dashboard as JSON in `lang` (3.1.0: each user's own language)."""
        from homeassistant.helpers.json import cached_json_fragment

        _, data = await self.async_config(force)
        code = self.language(lang)
        if code == self._config_lang:
            return data
        if code not in self._lang_json:
            self._lang_json[code] = cached_json_fragment(await self.async_config_for(code))
        return self._lang_json[code]

    async def async_user_language(self) -> str | None:
        """The language the user who asks has chosen in the profile, or None (then: Home Assistant's).

        The lovelace websocket command runs inside the asking connection, so the user is known.
        The frontend keeps the profile language in the user's frontend data (key "language").
        Anything unexpected gives None: the dashboard then follows Home Assistant's language,
        as in 3.0.0."""
        try:
            from homeassistant.components.frontend.storage import async_user_store
            from homeassistant.components.websocket_api import current_connection

            conn = current_connection.get()
            user = getattr(conn, "user", None)
            if user is None:
                return None
            data = (await async_user_store(self.hass, user.id)).data.get("language")
            lang = data.get("language") if isinstance(data, dict) else None
            return lang if isinstance(lang, str) and lang else None
        except Exception:  # noqa: BLE001 - never let this cost the dashboard
            return None

    # ---- registration -------------------------------------------------------------------------
    def _make_lovelace(self) -> Any:
        """A read-only YAML-mode dashboard whose config comes from HESC instead of a file."""
        from homeassistant.components.lovelace.dashboard import LovelaceConfig

        owner = self

        class _HescLovelace(LovelaceConfig):
            @property
            def mode(self) -> str:
                return "yaml"

            async def async_get_info(self) -> dict[str, Any]:
                try:
                    config, _ = await owner.async_config()
                except Exception as err:  # noqa: BLE001 - system health must not fail on HESC
                    return {"mode": self.mode, "error": str(err)}
                return {"mode": self.mode, "views": len(config.get("views", []))}

            async def async_load(self, force: bool) -> dict[str, Any]:
                lang = await owner.async_user_language()
                config, _ = await owner.async_config(force)
                return await owner.async_config_for(lang) if lang else config

            async def async_json(self, force: bool) -> Any:
                return await owner.async_json_for(await owner.async_user_language(), force)

            def changed(self) -> None:
                self._config_updated()

        return _HescLovelace(
            self.hass,
            DASHBOARD_URL,
            {"mode": "yaml", "title": DASHBOARD_TITLE, "icon": DASHBOARD_ICON,
             "show_in_sidebar": True, "require_admin": False},
        )

    def _address_taken(self, data: Any) -> bool:
        from homeassistant.components import frontend

        existing = data.dashboards.get(DASHBOARD_URL)
        if existing is not None and existing is not self._lovelace:
            return True
        return not self.panel_registered and frontend.async_panel_exists(self.hass, DASHBOARD_URL)

    async def async_register(self) -> None:
        """Register the dashboard once, or raise a repair notice when the address is taken."""
        if self.panel_registered:
            return
        if "lovelace" not in self.hass.config.components or "frontend" not in self.hass.config.components:
            return  # e.g. in tests without a frontend
        from homeassistant.components import frontend
        from homeassistant.components.lovelace.const import LOVELACE_DATA

        data = self.hass.data.get(LOVELACE_DATA)
        if data is None:
            return
        if self._address_taken(data):
            self._raise_taken()
            return
        if not self._raw:
            await self.async_load_files()
        await self.async_config(force=True)  # a broken file fails here, not in the frontend
        # checked again: the awaits above gave other code a chance to take the address
        if self._address_taken(data):
            self._raise_taken()
            return
        self._lovelace = self._lovelace or self._make_lovelace()
        data.dashboards[DASHBOARD_URL] = self._lovelace
        try:
            frontend.async_register_built_in_panel(
                self.hass, "lovelace", frontend_url_path=DASHBOARD_URL, require_admin=False,
                show_in_sidebar=True, sidebar_title=DASHBOARD_TITLE, sidebar_icon=DASHBOARD_ICON,
                config={"mode": "yaml"}, update=False,
            )
        except Exception:
            if data.dashboards.get(DASHBOARD_URL) is self._lovelace:
                data.dashboards.pop(DASHBOARD_URL)
            raise
        self.panel_registered = True
        ir.async_delete_issue(self.hass, DOMAIN, ISSUE_URL_TAKEN)
        self._unsub = self.hass.bus.async_listen(
            er.EVENT_ENTITY_REGISTRY_UPDATED, self._registry_updated, event_filter=self._is_rename
        )

    def _raise_taken(self) -> None:
        _LOGGER.info("Address /%s is already in use: HESC does not add its own dashboard", DASHBOARD_URL)
        ir.async_create_issue(
            self.hass, DOMAIN, ISSUE_URL_TAKEN, is_fixable=False, is_persistent=False,
            severity=ir.IssueSeverity.WARNING, translation_key=ISSUE_URL_TAKEN,
            translation_placeholders={"url": f"/{DASHBOARD_URL}"},
        )

    @staticmethod
    @callback
    def _is_rename(event_data: Any) -> bool:
        return event_data.get("action") == "update" and "old_entity_id" in event_data

    @callback
    def _registry_updated(self, event: Event) -> None:
        """An entity got another id: tell open dashboards to load the config again."""
        if self._lovelace is not None and self._mapping is not None and self.current_mapping() != self._mapping:
            self._lovelace.changed()

    @callback
    def async_unregister(self) -> None:
        """Remove the dashboard (HESC removed). The repair notice goes with it."""
        if self._unsub is not None:
            self._unsub()
            self._unsub = None
        ir.async_delete_issue(self.hass, DOMAIN, ISSUE_URL_TAKEN)
        from homeassistant.components import frontend
        from homeassistant.components.lovelace.const import LOVELACE_DATA

        if self.panel_registered:
            frontend.async_remove_panel(self.hass, DASHBOARD_URL, warn_if_unknown=False)
            self.panel_registered = False
        data = self.hass.data.get(LOVELACE_DATA)
        if data is not None and self._lovelace is not None and data.dashboards.get(DASHBOARD_URL) is self._lovelace:
            data.dashboards.pop(DASHBOARD_URL)


async def async_setup_dashboard(hass: HomeAssistant) -> None:
    """Register HESC's dashboard if HESC is configured (also called after a first setup).

    A failure costs only the dashboard: it is logged and HESC keeps running."""
    dash = hass.data.get(DATA_DASHBOARD)
    if dash is None:
        dash = hass.data[DATA_DASHBOARD] = HescDashboard(hass)
    if dash.panel_registered or not hass.config_entries.async_entries(DOMAIN):
        return
    try:
        await dash.async_register()
    except Exception:
        _LOGGER.exception("HESC could not add its dashboard")


@callback
def async_remove_dashboard(hass: HomeAssistant) -> None:
    dash = hass.data.pop(DATA_DASHBOARD, None)
    if dash is not None:
        dash.async_unregister()


_HESC_PATH = re.compile(r"/" + re.escape(DASHBOARD_URL) + r"(?=[/\"'?#\s]|$)")


def at_address(config: dict[str, Any], url_path: str | None) -> dict[str, Any]:
    """The config with its links to HESC's pages pointing at another dashboard address."""
    if not url_path or url_path == DASHBOARD_URL or not re.fullmatch(r"[a-z0-9_-]+", url_path):
        return config
    return json.loads(_HESC_PATH.sub("/" + url_path, json.dumps(config)))


@callback
def async_setup_websocket(hass: HomeAssistant) -> None:
    """`hesc/dashboard`: the dashboard config for the strategy (one-click dashboard)."""
    import voluptuous as vol
    from homeassistant.components import websocket_api

    @websocket_api.websocket_command(
        {vol.Required("type"): "hesc/dashboard", vol.Optional("url_path"): str, vol.Optional("language"): str}
    )
    @websocket_api.async_response
    async def ws_dashboard(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        dash = hass.data.get(DATA_DASHBOARD)
        if dash is None:
            dash = hass.data[DATA_DASHBOARD] = HescDashboard(hass)
        if not dash._raw:
            await dash.async_load_files()
        config = await dash.async_config_for(msg.get("language"))
        connection.send_result(msg["id"], at_address(config, msg.get("url_path")))

    websocket_api.async_register_command(hass, ws_dashboard)
