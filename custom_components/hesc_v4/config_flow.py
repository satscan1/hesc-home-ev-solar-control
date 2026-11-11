"""Setup screen (config flow) and options flow for HESC v4.

v4 first start (opmaakchat 31-10-2026 21:45, decision 21:38 "Akkoord"): how many cars -> how many
chargers (two cars) -> per charger its brand and entities -> per car its name, battery and battery-level
sensor -> two cars on one charger: taking turns -> house connection and load balancer -> solar (yes: the
sources and HPVC; no: only the grid meter) -> prices -> summary. HESC v3 installed: "take over" first.
Options: change the sources and charger (as v3), or add a second car.

The v3 steps (still used by the options flow "change"): charger type -> sources -> EV -> charger -> HPVC. The fields start with what v2
fills in on a first install (automations hesc_apply_defaults_on_first_install and
hesc_apply_defaults_v120), and the charger type fills brand values and entities like
v2's hesc_apply_charger_type. Tuning (thresholds, times) is not part of this flow;
it becomes number/select entities of the integration itself.
"""

from __future__ import annotations

import re

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from . import model, safety
from .plan_settings import BY_KEY as SETTING
from .charger_table import CHARGER_TABLE
from .const import (
    BAD_STATES,
    CHARGER_NOT_CHOSEN,
    CHARGER_OTHER,
    CONF_CHARGER_CURRENT,
    CONF_CHARGER_ECO_VALUES,
    CONF_CHARGER_MODE,
    CONF_CHARGER_RESUME,
    CONF_CHARGER_SOLAR_SWITCH,
    CONF_CHARGER_START_STOP,
    CONF_CHARGER_TYPE,
    CONF_EV_CONNECTED,
    CONF_EV_DISCONNECTED_VALUES,
    CONF_EV_GREEN_ENERGY,
    CONF_EV_POWER,
    CONF_EV_SOC,
    CONF_FORECAST_30M,
    CONF_FORECAST_ATTRIBUTE,
    CONF_FORECAST_NOW,
    CONF_GRID_EXPORT_POSITIVE,
    CONF_GRID_POWER_L1,
    CONF_GRID_POWER_L2,
    CONF_GRID_POWER_L3,
    CONF_GRID_POWER_PHASES,
    CONF_GRID_POWER,
    CONF_HPVC_ENABLED,
    CONF_HPVC_LIMITED,
    CONF_IRRADIANCE,
    CONF_NO_SOLAR,
    CONF_PV_POWER,
    CONF_SOLAR_TODAY,
    CONF_SOLAR_TOMORROW,
    CONF_STANDALONE,
    CONF_USE_HPVC_SOURCES,
    CONF_USE_IRRADIANCE,
    DEFAULT_ECO_VALUES,
    DEFAULT_HPVC_ENABLED,
    DOMAIN,
    FIRST_INSTALL_DEFAULTS,
    HPVC_GRID_HELPER,
    HPVC_PV_HELPER,
    NAME,
)
from .ev_soc_finder import find_ev_soc_candidates
from .profile import charger_profile

CHARGER_TYPES = [*CHARGER_TABLE, CHARGER_OTHER]

# v2 stores entity ids as free text, so any entity is accepted (no domain filter).
_ENTITY = selector.EntitySelector()
_TEXT = selector.TextSelector()
_BOOL = selector.BooleanSelector()

STEPS = ("sources", "ev", "charger", "hpvc")


def _field(key: str, values: dict[str, Any], required: bool = False) -> vol.Marker:
    """A form field showing the current value, without forcing it."""
    current = values.get(key)
    marker = vol.Required if required else vol.Optional
    if current in (None, ""):
        return marker(key)
    return marker(key, description={"suggested_value": current})


def _bool(key: str, values: dict[str, Any]) -> vol.Marker:
    """A switch field: off unless sent, showing the current value."""
    return vol.Optional(key, default=False, description={"suggested_value": bool(values.get(key, False))})


_PHASE_POWER = selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor", device_class="power"))


def schema_sources(v: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            _bool(CONF_USE_HPVC_SOURCES, v): _BOOL,
            _field(CONF_PV_POWER, v): _ENTITY,
            _field(CONF_GRID_POWER, v): _ENTITY,
            _bool(CONF_GRID_EXPORT_POSITIVE, v): _BOOL,
            _field(CONF_GRID_POWER_L1, v): _PHASE_POWER,  # rc3: phase advice (optional)
            _field(CONF_GRID_POWER_L2, v): _PHASE_POWER,
            _field(CONF_GRID_POWER_L3, v): _PHASE_POWER,
            _field(CONF_FORECAST_NOW, v): _ENTITY,  # optional since 16-10 (no forecast = level C)
            _field(CONF_FORECAST_30M, v): _ENTITY,
            _field(CONF_FORECAST_ATTRIBUTE, v): _TEXT,
            _field(CONF_SOLAR_TODAY, v): _ENTITY,
            _field(CONF_SOLAR_TOMORROW, v): _ENTITY,
            _bool(CONF_USE_IRRADIANCE, v): _BOOL,
            _field(CONF_IRRADIANCE, v): _ENTITY,
        }
    )


def schema_ev(v: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            _field(CONF_EV_CONNECTED, v, True): _ENTITY,
            _field(CONF_EV_DISCONNECTED_VALUES, v): _TEXT,
            _field(CONF_EV_POWER, v, True): _ENTITY,
            _field(CONF_EV_SOC, v): _ENTITY,
            _field(CONF_EV_GREEN_ENERGY, v): _ENTITY,
        }
    )


def schema_charger(v: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            _field(CONF_CHARGER_MODE, v, True): _ENTITY,
            _field(CONF_CHARGER_ECO_VALUES, v, True): _TEXT,
            _field(CONF_CHARGER_SOLAR_SWITCH, v): _ENTITY,
            _field(CONF_CHARGER_START_STOP, v): _ENTITY,
            _field(CONF_CHARGER_RESUME, v): _ENTITY,
            _field(CONF_CHARGER_CURRENT, v): selector.EntitySelector(selector.EntitySelectorConfig(domain="number")),
        }
    )


def schema_hpvc(v: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            _bool(CONF_STANDALONE, v): _BOOL,
            _field(CONF_HPVC_ENABLED, v): _ENTITY,
            _field(CONF_HPVC_LIMITED, v): _ENTITY,
        }
    )


def schema_charger_type(v: dict[str, Any]) -> vol.Schema:
    current = v.get(CONF_CHARGER_TYPE)
    marker = vol.Required(CONF_CHARGER_TYPE, description={"suggested_value": current} if current else None)
    return vol.Schema(
        {
            marker: selector.SelectSelector(
                selector.SelectSelectorConfig(options=CHARGER_TYPES, mode=selector.SelectSelectorMode.DROPDOWN)
            )
        }
    )


SCHEMAS = {"sources": schema_sources, "ev": schema_ev, "charger": schema_charger, "hpvc": schema_hpvc}


def ev_soc_hint(hass: HomeAssistant, values: dict[str, Any]) -> tuple[str | None, str]:
    """Suggestion and explanation for the EV battery-level field (new in v3).

    Returns (entity to pre-fill or None, text for the step description). A field that is
    already filled in is left alone and gets no text.
    """
    if str(values.get(CONF_EV_SOC) or "").strip():
        return None, ""
    return soc_hint(find_ev_soc_candidates(hass))


def soc_hint(found: list[str]) -> tuple[str | None, str]:
    """(entity to pre-fill or None, explanation) from the battery-level sensors found."""
    if len(found) == 1:
        return found[0], f"HESC found the battery level of your car: {found[0]}. Check it and continue."
    if found:
        return None, (
            "HESC found more than one possible battery level of a car: "
            + ", ".join(found)
            + ". Pick the one of your car."
        )
    return None, (
        "HESC found no battery level of a car in Home Assistant. Ways to get one:\n"
        "1. The Home Assistant integration of your car brand (Settings > Devices & services, or HACS).\n"
        "2. An OBD2 plug-in module in the car that sends the battery level to Home Assistant "
        "(for example over MQTT).\n"
        "Without a battery level HESC still works: it charges until the car stops by itself and learns how much "
        "a charge needs (v4)."
    )


def _helper_text(hass: HomeAssistant, entity_id: str) -> str:
    s = hass.states.get(entity_id)
    return "" if s is None or s.state in BAD_STATES else s.state.strip()


def validate(hass: HomeAssistant, step: str, user_input: dict[str, Any]) -> dict[str, str]:
    """Errors per field for one step (empty = fine)."""
    errors: dict[str, str] = {}
    if step == "sources":
        hpvc_pv = user_input.get(CONF_USE_HPVC_SOURCES) and _helper_text(hass, HPVC_PV_HELPER)
        if not user_input.get(CONF_PV_POWER) and not hpvc_pv:
            errors[CONF_PV_POWER] = "pv_required"
        if user_input.get(CONF_USE_IRRADIANCE) and not user_input.get(CONF_IRRADIANCE):
            errors[CONF_IRRADIANCE] = "irradiance_required"
        # rc3: grid power per phase: all three (different sensors) or none
        phases = [str(user_input.get(k) or "").strip() for k in CONF_GRID_POWER_PHASES]
        filled = [p for p in phases if p]
        if filled and (len(filled) != 3 or len(set(filled)) != 3):
            for k, p in zip(CONF_GRID_POWER_PHASES, phases):
                if not p or phases.count(p) > 1:
                    errors[k] = "phases_all_or_none"
    if step == "charger_entities":
        step = "charger"  # v4 first start: the same rules as v3's charger step
    current = str(user_input.get(CONF_CHARGER_CURRENT) or "")
    if step == "charger" and current and safety.is_installer_setting(current):
        errors[CONF_CHARGER_CURRENT] = "installer_setting"  # hard rule 30-10-2026 (safety.py)
    if step == "charger" and not str(user_input.get(CONF_CHARGER_ECO_VALUES, "")).strip():
        errors[CONF_CHARGER_ECO_VALUES] = "eco_values_required"
    if step == "hpvc" and not user_input.get(CONF_STANDALONE):
        for key in (CONF_HPVC_ENABLED, CONF_HPVC_LIMITED):
            if not user_input.get(key):
                errors[key] = "hpvc_required"
    return errors


def _clean(step: str, values: dict[str, Any], user_input: dict[str, Any]) -> dict[str, Any]:
    """Store this step's answers; a field left empty is removed (v2: empty input_text)."""
    out = dict(values)
    for key in SCHEMAS[step]({}).schema:
        out.pop(str(key), None)
    for key, val in user_input.items():
        if isinstance(val, str):
            val = val.strip()
        if val not in (None, ""):
            out[key] = val
    return out


# Other solar forecasts HESC recognises: integration -> sensor key
# (end of the entity's unique id) per setup field.
_FORECAST_KEYS: dict[str, dict[str, str]] = {
    "open_meteo_solar_forecast": {
        CONF_FORECAST_NOW: "power_production_now",
        CONF_FORECAST_30M: "power_production_next_30minutes",
        CONF_SOLAR_TODAY: "energy_production_today",
        CONF_SOLAR_TOMORROW: "energy_production_tomorrow",
    },
    "forecast_solar": {
        CONF_FORECAST_NOW: "power_production_now",
        CONF_FORECAST_30M: "power_production_next_hour",
        CONF_SOLAR_TODAY: "energy_production_today",
        CONF_SOLAR_TOMORROW: "energy_production_tomorrow",
    },
}
_FORECAST_FIELDS = (CONF_FORECAST_NOW, CONF_FORECAST_30M, CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW)


def forecast_suggestions(hass: HomeAssistant) -> dict[str, str]:
    """The forecast fields for a new install: Solcast as in v2 when it is there, else Open-Meteo or
    Forecast.Solar when one of them is installed, else empty (HESC works without a forecast)."""
    if hass.states.get(str(FIRST_INSTALL_DEFAULTS[CONF_FORECAST_NOW])) is not None:
        return {k: str(FIRST_INSTALL_DEFAULTS[k]) for k in (*_FORECAST_FIELDS, CONF_FORECAST_ATTRIBUTE)}
    from homeassistant.helpers import entity_registry as er

    reg = er.async_get(hass)
    for platform, keys in _FORECAST_KEYS.items():
        ents = [e for e in reg.entities.values() if e.platform == platform and e.domain == "sensor" and not e.disabled]
        found: dict[str, str] = {}
        for field_key, key in keys.items():
            match = sorted(e.entity_id for e in ents if str(e.unique_id).endswith(key))
            if match:
                found[field_key] = match[0]
        if CONF_FORECAST_NOW in found:
            return {**found, CONF_FORECAST_ATTRIBUTE: ""}
    return {}


_PHASE_RX = re.compile(r"^(sensor\..*?(?:phase|fase)_?l?)([123])$")
_NOT_NET = re.compile(r"(production|consumption|levering|teruglevering|returned|delivered|export|import)")


def phase_power_suggestions(hass: HomeAssistant) -> dict[str, str]:
    """rc3: one complete set of grid power sensors per phase (net, W or kW; e.g. HomeWizard
    ``..._power_phase_1``, a P1 meter ``..._vermogen_fase_1``), only when exactly one set exists.
    Meters that split import and export per phase (two sensors per phase) are not offered."""
    groups: dict[str, dict[int, str]] = {}
    for s in hass.states.async_all("sensor"):
        m = _PHASE_RX.match(s.entity_id)
        if not m or _NOT_NET.search(s.entity_id) or s.attributes.get("device_class") != "power":
            continue
        groups.setdefault(m.group(1), {})[int(m.group(2))] = s.entity_id
    full = [g for g in groups.values() if set(g) == {1, 2, 3}]
    if len(full) != 1:
        return {}
    return dict(zip(CONF_GRID_POWER_PHASES, (full[0][1], full[0][2], full[0][3])))


def first_install_values(hass: HomeAssistant) -> dict[str, Any]:
    """What v2 fills in once on a new install (only text fields and switches that HESC reads)."""
    values: dict[str, Any] = {k: v for k, v in FIRST_INSTALL_DEFAULTS.items()
                              if k not in (*_FORECAST_FIELDS, CONF_FORECAST_ATTRIBUTE)}
    values.update(forecast_suggestions(hass))
    values.update(phase_power_suggestions(hass))
    # "No HPVC found on a new install: start in standalone mode"
    hpvc = hass.states.get(DEFAULT_HPVC_ENABLED)
    if hpvc is None or (hpvc.state in ("unknown", "unavailable") and "friendly_name" not in hpvc.attributes):
        values[CONF_STANDALONE] = True
    return values


def apply_charger_type(hass: HomeAssistant, values: dict[str, Any], old_type: str | None, new_type: str) -> dict[str, Any]:
    """v2 hesc_apply_charger_type: brand values and entities with exactly one candidate.

    Brand values are only replaced when the charger type changes from one brand to another
    (or the field is empty); entity fields are only filled when empty.

    v2.0.1 fix (`first_choice` in hesc_apply_charger_type): when the first brand is
    chosen (previous type "Not chosen") and the solar mode value still holds the first-install
    default "eco_mode", the brand's own value is filled in. It does not apply at start, on a
    later change or "search again". v2.0.1 dev4 adds `stale_default` (see below), which does.
    """
    out = dict(values)
    out[CONF_CHARGER_TYPE] = new_type
    prof = charger_profile(hass, new_type)
    if not prof.known:
        return out
    brand_changed = (
        old_type is not None and old_type != new_type and old_type not in (CHARGER_NOT_CHOSEN, CHARGER_OTHER)
    )

    def empty(key: str) -> bool:
        return str(out.get(key) or "").strip() in ("", "unknown", "unavailable")

    first_choice = (
        old_type == CHARGER_NOT_CHOSEN
        and new_type != old_type
        and str(out.get(CONF_CHARGER_ECO_VALUES) or "") == DEFAULT_ECO_VALUES
    )
    # v2.0.1 dev4 (`stale_default`): the field still holds exactly "eco_mode" while the brand's
    # own values do not contain it -> repaired at the next start/search (never for Wallbox).
    stale_default = (
        str(out.get(CONF_CHARGER_ECO_VALUES) or "").strip() == DEFAULT_ECO_VALUES
        and DEFAULT_ECO_VALUES not in prof.values
    )
    if brand_changed or first_choice or stale_default or empty(CONF_CHARGER_ECO_VALUES):
        out[CONF_CHARGER_ECO_VALUES] = prof.values
    if prof.not_connected and (brand_changed or empty(CONF_EV_DISCONNECTED_VALUES)):
        out[CONF_EV_DISCONNECTED_VALUES] = prof.not_connected
    for conf, key in (
        (CONF_CHARGER_MODE, "mode"),
        (CONF_EV_CONNECTED, "connected"),
        (CONF_EV_POWER, "power"),
        (CONF_CHARGER_SOLAR_SWITCH, "switch"),
        (CONF_CHARGER_START_STOP, "startstop"),
        (CONF_CHARGER_RESUME, "resume"),
        (CONF_CHARGER_CURRENT, "current"),
    ):
        found = prof.single(key)
        if found and empty(conf):
            out[conf] = found
    return out


class _Steps:
    """The four shared steps; subclasses decide what happens at the end."""

    hass: HomeAssistant
    _values: dict[str, Any]

    def _finish(self) -> ConfigFlowResult:
        raise NotImplementedError

    async def _step(self, step: str, user_input: dict[str, Any] | None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = validate(self.hass, step, user_input)
            if not errors:
                self._values = _clean(step, self._values, user_input)
                nxt = STEPS.index(step) + 1
                if nxt < len(STEPS):
                    return await getattr(self, f"async_step_{STEPS[nxt]}")()
                return self._finish()
        shown = {**self._values, **(user_input or {})}
        placeholders: dict[str, str] = {}
        if step == "ev":
            suggestion, hint = ev_soc_hint(self.hass, shown)
            if suggestion and user_input is None:
                shown[CONF_EV_SOC] = suggestion
            placeholders["soc_hint"] = hint
        return self.async_show_form(  # type: ignore[attr-defined]
            step_id=step,
            data_schema=SCHEMAS[step](shown),
            errors=errors,
            description_placeholders=placeholders or None,
        )

    async def async_step_sources(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        return await self._step("sources", user_input)

    async def async_step_ev(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        return await self._step("ev", user_input)

    async def async_step_charger(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        return await self._step("charger", user_input)

    async def async_step_hpvc(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        return await self._step("hpvc", user_input)


PREV_DOMAIN = "hesc"  # HESC v3, installed next to the v4 alpha

# ---- v4 first start ---------------------------------------------------------------------------------
# Setting values the first start asks for that live in HESC's own entities (house connection, battery,
# the charger's maximum, taking turns, prices). They are kept in the entry under FIRST_VALUES per owner
# ("shared", "ev1", "charger1", ...) and set on those entities at the first start (__init__.py).
FIRST_VALUES = "first_values"
CHARGER_FIELDS = (CONF_EV_CONNECTED, CONF_EV_DISCONNECTED_VALUES, CONF_EV_POWER, CONF_CHARGER_MODE,
                  CONF_CHARGER_ECO_VALUES, CONF_CHARGER_SOLAR_SWITCH, CONF_CHARGER_START_STOP,
                  CONF_CHARGER_RESUME, CONF_CHARGER_CURRENT, CONF_EV_GREEN_ENERGY)
_ENTITY_KEYS = ("mode", "connected", "power", "switch", "startstop", "resume", "current")
_KEY_FIELD = {"mode": CONF_CHARGER_MODE, "connected": CONF_EV_CONNECTED, "power": CONF_EV_POWER,
              "switch": CONF_CHARGER_SOLAR_SWITCH, "startstop": CONF_CHARGER_START_STOP,
              "resume": CONF_CHARGER_RESUME, "current": CONF_CHARGER_CURRENT}
MAX_A, MIN_A, DEFAULT_A = 32, 6, 16


def _select(options: list[str] | tuple[str, ...], key: str | None = None) -> selector.SelectSelector:
    extra = {"translation_key": key} if key else {}
    return selector.SelectSelector(selector.SelectSelectorConfig(
        options=list(options), mode=selector.SelectSelectorMode.DROPDOWN, **extra))


def _number(lo: float, hi: float, step: float, unit: str) -> selector.NumberSelector:
    return selector.NumberSelector(selector.NumberSelectorConfig(
        min=lo, max=hi, step=step, unit_of_measurement=unit, mode=selector.NumberSelectorMode.BOX))


def split_defaults(values: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """first_install_values -> (shared part, the part every charger starts with)."""
    shared = {k: v for k, v in values.items() if model.scope_of(k) is model.Scope.SHARED}
    charger = {k: v for k, v in values.items() if model.scope_of(k) is model.Scope.CHARGER}
    return shared, charger


def second_charger(hass: HomeAssistant, values: dict[str, Any], charger_type: str, used: dict[str, Any]) -> dict[str, Any]:
    """A second charger of a brand: an entity of the first charger is not offered again, and where the
    brand has exactly two candidates the other one is filled in."""
    out = dict(values)
    prof = charger_profile(hass, charger_type)
    for key, conf in _KEY_FIELD.items():
        mine = str(used.get(conf) or "")
        if mine and out.get(conf) == mine:
            out.pop(conf)
        found = [e for e in (getattr(prof, key, []) if prof.known else []) if e != mine]
        if not str(out.get(conf) or "").strip() and len(found) == 1 and mine:
            out[conf] = found[0]
    return out


def installer_max(hass: HomeAssistant, current_entity: Any) -> int:
    """The installer's maximum when the charger lets HESC read it (the `max` of its charging-current
    entity, decision 31-10-2026 09:58 question 3), else 16 A."""
    st = hass.states.get(str(current_entity or "")) if current_entity else None
    try:
        hi = float((st.attributes or {}).get("max")) if st is not None else None
    except (TypeError, ValueError):
        hi = None
    return int(hi) if hi is not None and MIN_A <= hi <= MAX_A else DEFAULT_A


def ev_soc_candidates(hass: HomeAssistant, used: list[str]) -> list[str]:
    return [e for e in find_ev_soc_candidates(hass) if e not in used]


def car_device(hass: HomeAssistant, entity_id: str | None) -> tuple[str | None, str | None, str | None]:
    """(name, manufacturer, model) of the device of a car's battery-level sensor."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    ent = er.async_get(hass).async_get(str(entity_id or "")) if entity_id else None
    dev = dr.async_get(hass).async_get(ent.device_id) if ent and ent.device_id else None
    if dev is None:
        return None, None, None
    return (dev.name_by_user or dev.name or None), dev.manufacturer, dev.model


_PROFILE_KEY = {v: k for k, v in _KEY_FIELD.items()}
CHARGER_REQUIRED = (CONF_EV_CONNECTED, CONF_EV_POWER, CONF_CHARGER_MODE, CONF_CHARGER_ECO_VALUES)


class HescConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up HESC v4 (one per Home Assistant). Decision 01-11-2026 12:44 ("B"): the HA window only
    asks "Install HESC v4?" (with v3 present first: take over v3's settings); the first start itself runs
    in HESC's own panel (setup_wizard.py). The entry starts in shadow mode, the first start not finished."""

    VERSION = model.ENTRY_VERSION  # 2: settings nested as shared / per car / per charger (model.py)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is None and self.hass.config_entries.async_entries(PREV_DOMAIN):
            return await self.async_step_from_v3()
        if user_input is not None:
            return self._create_new()
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    def _create_new(self) -> ConfigFlowResult:
        """An entry with the first-install defaults, EV1 on charger 1, the first start not finished."""
        from .setup_wizard import SETUP_DONE

        shared, charger = split_defaults(first_install_values(self.hass))
        nested = {"shared": {**shared, SETUP_DONE: False},
                  "evs": {model.EV1: {model.EV_NAME: "EV1", model.EV_CHARGER: model.CHARGER1}},
                  "chargers": {model.CHARGER1: charger}}
        return self.async_create_entry(title=NAME, data=nested)

    async def async_step_from_v3(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """v4 alpha next to v3 (decision 30-10-2026): take over v3's settings (v3 is only read). v3's setup
        choices become EV1 + charger 1 + shared right away; v3's own setting values and history follow
        at the first start (coordinator.async_take_over_from_v3). Taken over = the first start is done;
        not taken over: the first start in the panel."""
        if user_input is None:
            return self.async_show_form(step_id="from_v3", data_schema=vol.Schema({vol.Required("take_over", default=True): bool}))
        if not user_input.get("take_over"):
            return self._create_new()
        v3 = self.hass.config_entries.async_entries(PREV_DOMAIN)[0]
        values = {**v3_live_values(self.hass, dict(v3.options or v3.data)), "take_over_v3_pending": True}
        name = model.car_name(self.hass, values.get(CONF_EV_SOC))
        return self.async_create_entry(title=NAME, data=model.nest(values, name=name))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> HescOptionsFlow:
        return HescOptionsFlow()


def v3_live_values(hass: HomeAssistant, setup: dict[str, Any]) -> dict[str, Any]:
    """v3's setup choices with what v3 uses now (decision 09-11-2026, bug in beta.1): a source changed in v3
    after its install lives in v3's own helper (`input_text.hesc_<key>`, `input_boolean.hesc_<key>`, ...),
    not in its config entry. A helper with a usable value wins; an empty or unknown helper keeps the setup choice."""
    out = dict(setup)
    for key, old in setup.items():
        for dom in ("input_text", "input_select", "input_boolean", "input_number"):
            st = hass.states.get(f"{dom}.hesc_{key}")
            if st is None or st.state in ("", "unknown", "unavailable"):
                continue
            if dom == "input_boolean":
                out[key] = st.state == "on"
            elif dom == "input_number":
                try:
                    out[key] = type(old)(float(st.state)) if isinstance(old, (int, float)) and not isinstance(old, bool) else float(st.state)
                except ValueError:
                    continue
            else:
                out[key] = st.state
            break
    return out


class HescOptionsFlow(_Steps, OptionsFlowWithReload):
    """Change EV1's sources and charger later (v3: charger type + 'search again'). A second car is added
    in HESC's own panel (decision 01-11-2026 12:44)."""

    def __init__(self) -> None:
        self._values: dict[str, Any] = {}

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        current = model.flatten(self.config_entry.options or self.config_entry.data)  # EV1
        if user_input is not None:
            self._values = apply_charger_type(
                self.hass, current, current.get(CONF_CHARGER_TYPE), user_input[CONF_CHARGER_TYPE]
            )
            return await self.async_step_sources()
        return self.async_show_form(step_id="init", data_schema=schema_charger_type(current))

    def _finish(self) -> ConfigFlowResult:
        # Options hold the complete set, so a field emptied here stays empty.
        return self.async_create_entry(data=model.replace_flat(self.config_entry.options or self.config_entry.data, self._values))
