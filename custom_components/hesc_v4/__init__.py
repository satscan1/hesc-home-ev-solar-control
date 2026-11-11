"""HESC v4: Home EV Solar Control as a Home Assistant integration.

Reads all inputs like v2 and runs the ported v2 logic. In shadow mode (the default) it switches
nothing and sends nothing; with shadow mode off it gives v2's commands itself.
"""

from __future__ import annotations

import hashlib
from datetime import timedelta
from pathlib import Path

from homeassistant.components import webhook
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import (
    async_call_later,
    async_track_state_change_event,
    async_track_time_change,
    async_track_time_interval,
)
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.typing import ConfigType

from .config_flow import apply_charger_type
from . import model
from .const import CONF_CHARGER_START_STOP, CONF_CHARGER_TYPE, CONF_EV_SOC, DOMAIN
from .coordinator import REPORT_WEBHOOK, HescConfigEntry, HescCoordinator
from .entity import ENGLISH_NAMES, load_english_names
from .panel import async_remove_dashboard, async_setup_dashboard, async_setup_websocket
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# The house-style icons as the icon set "hesc" (`icon: hesc:zon`), loaded in the frontend for every
# user without a dashboard resource. Built by tools/icons/build_iconset.py.
ICONS_DIR = Path(__file__).parent / "frontend"
ICONS_URL = "/hesc_v4_frontend"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """HESC's dashboard (panel.py) and the icon set on every page of the frontend."""
    # the dashboard first, together with the user's own dashboards: it then exists before the
    # entry is set up, and the kiosk page finds it right after an HA restart
    await async_setup_dashboard(hass)
    if "websocket_api" in hass.config.components:
        async_setup_websocket(hass)  # since 3.0.0: the one-click dashboard (strategy) asks HESC for its config
    from .setup_wizard import async_setup_websocket as setup_ws

    from .switch_v3 import async_setup_websocket as switch_ws

    switch_ws(hass)  # RC1 (11-11): back to v3 from Expert
    setup_ws(hass)  # v4 (01-11): the first start in HESC's own panel (registered also before the websocket loads)
    async_setup_services(hass)  # since 3.0.0: set_charge_plan / charge_plan_off (phones, Siri, Watch)
    # frontend and http are after-dependencies: loaded first when present (always in a normal HA);
    # without them (e.g. in tests) HESC runs without the icon set.
    if getattr(hass, "http", None) is not None:
        from .downloads import async_register

        async_register(hass)  # 08-11: the charging-costs CSV as a download (signed-in users only)
    if "frontend" not in hass.config.components or getattr(hass, "http", None) is None:
        return True
    from homeassistant.components.frontend import add_extra_js_url
    from homeassistant.components.http import StaticPathConfig

    js = ICONS_DIR / "hesc-icons.js"
    version = await hass.async_add_executor_job(lambda: hashlib.sha256(js.read_bytes()).hexdigest()[:8])
    await hass.http.async_register_static_paths([StaticPathConfig(ICONS_URL, str(ICONS_DIR), True)])
    add_extra_js_url(hass, f"{ICONS_URL}/hesc-icons.js?v={version}")
    # Kiosk screen: reload once after an HA restart so the icons are there again.
    kiosk_js = ICONS_DIR / "hesc-kiosk-reload.js"
    kiosk_version = await hass.async_add_executor_job(lambda: hashlib.sha256(kiosk_js.read_bytes()).hexdigest()[:8])
    add_extra_js_url(hass, f"{ICONS_URL}/hesc-kiosk-reload.js?v={kiosk_version}")
    # Since 3.0.0: HESC's own dashboard cards and the one-click dashboard (no HACS cards needed).
    cards_js = ICONS_DIR / "hesc-cards.js"
    cards_version = await hass.async_add_executor_job(lambda: hashlib.sha256(cards_js.read_bytes()).hexdigest()[:8])
    add_extra_js_url(hass, f"{ICONS_URL}/hesc-cards.js?v={cards_version}")
    # v4 (decision 01-11-2026 12:44 "B"): the first start in HESC's own panel
    fs_js = ICONS_DIR / "hesc-first-start.js"
    fs_version = await hass.async_add_executor_job(lambda: hashlib.sha256(fs_js.read_bytes()).hexdigest()[:8])
    add_extra_js_url(hass, f"{ICONS_URL}/hesc-first-start.js?v={fs_version}")
    # v4 (decision 02-11-2026 12:48): the proefbord layout as HESC's own panel (button row + windows)
    panel_js = ICONS_DIR / "hesc-v4-panel.js"
    panel_version = await hass.async_add_executor_job(lambda: hashlib.sha256(panel_js.read_bytes()).hexdigest()[:8])
    add_extra_js_url(hass, f"{ICONS_URL}/hesc-v4-panel.js?v={panel_version}")
    return True


PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR, Platform.BUTTON, Platform.DATE, Platform.DATETIME, Platform.NUMBER, Platform.SELECT,
    Platform.SENSOR, Platform.SWITCH, Platform.TEXT,
]


def _remove_gone_entities(hass: HomeAssistant, entry: HescConfigEntry, coordinator: HescCoordinator) -> None:
    """v4 step 4 (decision 2, 31-10 17:25): the entities of v3's plan for one day, skip one day and
    holiday mode are gone (plan_settings.GONE); their values went to the planning (take over from v3)."""
    from homeassistant.helpers import entity_registry as er

    from . import model
    from .plan_settings import GONE

    reg = er.async_get(hass)
    for ev in coordinator.ev_ids():
        for key in GONE:
            uid = model.unique_id(entry.entry_id, key, ev, model.charger_of(coordinator.nested, ev))
            for domain in ("switch", "select", "date", "datetime"):
                eid = reg.async_get_entity_id(domain, DOMAIN, uid)
                if eid is not None:
                    reg.async_remove(eid)


async def async_setup_entry(hass: HomeAssistant, entry: HescConfigEntry) -> bool:
    _search_empty_charger_fields(hass, entry)
    coordinator = HescCoordinator(hass, entry)
    _remove_gone_entities(hass, entry, coordinator)
    for ev in coordinator.ev_ids():  # v4: each car its own files (cars.py)
        await coordinator.async_load_flags(ev)
        await coordinator.async_load_current(ev)
        await coordinator.async_load_planning(ev)
        await coordinator.async_load_learn(ev)
    await coordinator.async_load_phase_stats()
    await coordinator.async_refresh_backup_meta()
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    if not ENGLISH_NAMES:  # new entities get their id from the English name (entity.py)
        await hass.async_add_executor_job(load_english_names)
    # the main device first: the devices of the cars and chargers point to it (via_device)
    from homeassistant.helpers import device_registry as dr

    from .entity import device_info

    main = device_info(entry.entry_id)
    from .entity import MAIN_DEVICE_IDS

    MAIN_DEVICE_IDS[entry.entry_id] = dr.async_get(hass).async_get_or_create(config_entry_id=entry.entry_id, **main).id
    await _migrate_car_entities(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # tuning entities have restored their values now (HA waits for them): start the decision logic
    coordinator.logic_ready = True
    # v4 first start / a second car added: the answers that live in HESC's own entities
    await coordinator.async_apply_first_values()
    _schedule(hass, entry, coordinator)
    if model.flatten(entry.options or entry.data).get("take_over_v3_pending"):
        # set up "take over from v3": v3's own setting values and history follow now (v3 is only read)
        async def _take_over() -> None:
            try:
                await coordinator.async_take_over_from_v3()
            finally:
                coordinator.store_settings({"take_over_v3_pending": False})
            # RC1 (11-11-2026): only one HESC may steer the charger; v3 is paused, not removed
            from .switch_v3 import async_pause_v3

            await async_pause_v3(hass)

        entry.async_create_background_task(hass, _take_over(), "hesc take over v3")
    # first install: the dashboard could not be registered in async_setup yet
    await async_setup_dashboard(hass)
    return True


async def async_migrate_entry(hass: HomeAssistant, entry: HescConfigEntry) -> bool:
    """Version 1 (v3: one flat dict) -> 2 (v4: shared / EV1 / charger 1, model.py). Decision 9: the v3
    settings become EV1 plus the shared settings, EV1 named after the car in HA."""
    if entry.version > model.ENTRY_VERSION:
        return False
    if entry.version == 1:
        flat = dict(entry.options or entry.data)
        name = model.car_name(hass, flat.get(CONF_EV_SOC))
        data = model.nest(entry.data, name=name)
        options = model.nest(entry.options, name=name) if entry.options else {}
        hass.config_entries.async_update_entry(entry, data=data, options=options, version=model.ENTRY_VERSION)
        from homeassistant.helpers import entity_registry as er

        prefix = f"{entry.entry_id}_"

        @callback
        def _move(ent: er.RegistryEntry) -> dict[str, str] | None:
            key = ent.unique_id.removeprefix(prefix)
            if not ent.unique_id.startswith(prefix) or model.owner(key) is None:
                return None
            return {"new_unique_id": model.unique_id(entry.entry_id, key)}

        await er.async_migrate_entries(hass, entry.entry_id, _move)
    return True


async def _migrate_car_entities(hass: HomeAssistant, entry: HescConfigEntry) -> None:
    """Step 2 part B: some entities became a car's (status, plan, battery level, costs, morning summary
    and phones; model.EV_ENTITY_KEYS / EV_KEYS). Move EV1's existing ones to their new unique id and
    to `..._hesc_v4_ev1_...`, so no orphan is left and EV1 keeps its history."""
    from homeassistant.helpers import entity_registry as er

    reg = er.async_get(hass)
    prefix = f"{entry.entry_id}_"

    @callback
    def _move(ent: er.RegistryEntry) -> dict[str, str] | None:
        if not ent.unique_id.startswith(prefix):
            return None
        key = ent.unique_id.removeprefix(prefix)
        if model.owner(key) != model.EV1:
            return None
        new_uid = model.unique_id(entry.entry_id, key)
        if reg.async_get_entity_id(ent.domain, DOMAIN, new_uid) is not None:
            return None
        out = {"new_unique_id": new_uid}
        domain, obj = ent.entity_id.split(".", 1)
        if obj.startswith("hesc_v4_") and not obj.startswith("hesc_v4_ev1_"):
            new_id = f"{domain}.hesc_v4_ev1_{obj.removeprefix('hesc_v4_')}"
            if reg.async_get(new_id) is None:
                out["new_entity_id"] = new_id
        return out

    await er.async_migrate_entries(hass, entry.entry_id, _move)


def _schedule(hass: HomeAssistant, entry: HescConfigEntry, c: HescCoordinator) -> None:
    """v2's timers: price forecast every 15 min (first after 60 s), holidays every 6 h at :07,
    price fetch every 30 min, holiday mode end at 00:01; the last three also at start."""
    on = entry.async_on_unload
    entry.async_create_background_task(hass, c.async_load_price_history(), "hesc price history")

    # v2 "EV battery level: load at start (30 s)"
    async def _load_soc(_now: object) -> None:
        for ev in c.ev_ids():
            await c.async_load_soc_plugins(ev)

    on(async_call_later(hass, 30, _load_soc))

    # v2 "Charging costs: load at start (35 s)"
    async def _load_costs(_now: object) -> None:
        for ev in c.ev_ids():
            await c.async_load_costs(ev)

    on(async_call_later(hass, 35, _load_costs))

    async def _stopping(_event: object) -> None:
        for ev in c.ev_ids():
            await c.async_save_costs(ev)
        await c.async_save_phase_stats()

    on(hass.bus.async_listen(EVENT_HOMEASSISTANT_STOP, _stopping))
    on(async_track_time_change(hass, c.update_backup_sensor, minute=list(range(0, 60, 10)), second=0))
    # v2 "Morning summary": every minute
    on(async_track_time_interval(hass, c.async_morning_summary, timedelta(minutes=1)))

    # since 3.0.0: the kickstart hands back to solar mode 15 s after the charger's start/stop switch
    # turned off; run a round right then instead of waiting for the next one (up to 30 s later)
    start_stop = [str(model.flatten(c.nested, ev).get(CONF_CHARGER_START_STOP) or "").strip() for ev in c.ev_ids()]
    start_stop = sorted({e for e in start_stop if e})  # v4: every charger's switch
    if start_stop:

        @callback
        def _start_stop_changed(event: Event) -> None:
            new = event.data.get("new_state")
            if new is None or new.state != "off":
                return

            async def _round(_now: object) -> None:
                await c.async_request_refresh()

            on(async_call_later(hass, 16, _round))

        on(async_track_state_change_event(hass, start_stop, _start_stop_changed))

    # like v2's "homeassistant start" triggers: once HA has started (other integrations loaded)
    async def _started(_hass: HomeAssistant) -> None:
        # since rc3: at boot HESC is set up before the charger and the meter have their
        # entities, so the search for empty fields finds nothing. Search again once HA has started.
        _search_empty_charger_fields(hass, entry)
        c.update_backup_sensor()
        c.update_charger_profile()
        await c.async_update_holidays()
        await c.async_fetch_prices()
        await c.async_fetch_forecast_solar()
        c.update_forecast_issue()

    on(async_at_started(hass, _started))
    # Forecast.Solar has no series in its sensors: fetch it with its action
    on(async_track_time_interval(hass, c.async_fetch_forecast_solar, timedelta(minutes=15)))
    on(async_call_later(hass, 60, c.async_run_price_forecast))
    on(async_track_time_interval(hass, c.async_run_price_forecast, timedelta(minutes=15)))
    on(async_track_time_change(hass, c.async_update_holidays, hour=[0, 6, 12, 18], minute=7, second=0))
    on(async_track_time_change(hass, c.async_fetch_prices, minute=[0, 30], second=0))

    # v2 "Daily advice 21:30 (+ at start)" and the seasonal start threshold (00:05 and at start)
    on(async_call_later(hass, 90, c.async_daily_advisor))
    on(async_track_time_change(hass, c.async_daily_advisor, hour=21, minute=30, second=0))
    on(async_track_time_change(hass, c.async_seasonal, hour=0, minute=5, second=0))

    async def _seasonal_at_start(_hass: HomeAssistant) -> None:
        await c.async_seasonal()

    on(async_at_started(hass, _seasonal_at_start))

    # v2 automation "Reset report after viewing": the report calls this webhook when it is opened
    async def _viewed(_hass: HomeAssistant, _webhook_id: str, _request: object) -> None:
        c.report_viewed()

    webhook.async_register(hass, DOMAIN, "HESC v4 report viewed", REPORT_WEBHOOK, _viewed,
                           allowed_methods=["POST"], local_only=False)
    on(lambda: webhook.async_unregister(hass, REPORT_WEBHOOK))


async def async_remove_entry(hass: HomeAssistant, entry: HescConfigEntry) -> None:
    """HESC removed: its dashboard goes too (a reload keeps it)."""
    async_remove_dashboard(hass)


async def async_unload_entry(hass: HomeAssistant, entry: HescConfigEntry) -> bool:
    from homeassistant.helpers import issue_registry as ir

    for ev in entry.runtime_data.ev_ids():
        await entry.runtime_data.async_save_costs(ev)
        await entry.runtime_data.async_restore_current(ev)
    await entry.runtime_data.async_save_phase_stats()
    ir.async_delete_issue(hass, DOMAIN, "no_solar_forecast")
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def _search_empty_charger_fields(hass: HomeAssistant, entry: HescConfigEntry) -> None:
    """v2 runs hesc_apply_charger_type at every start: empty charger fields with exactly one
    candidate get filled in. Nothing that is filled in is changed."""
    stored = entry.options or entry.data
    current = model.flatten(stored)
    charger_type = current.get(CONF_CHARGER_TYPE)
    if not charger_type:
        return
    updated = apply_charger_type(hass, current, charger_type, charger_type)
    # rc3: the grid power per phase (phase advice), only when all three are empty and one set is found
    from .config_flow import phase_power_suggestions
    from .const import CONF_GRID_POWER_PHASES

    # offered once: a user who empties the fields later keeps them empty (review rc3)
    if not updated.get("phase_fields_offered") and not any(str(updated.get(k) or "").strip() for k in CONF_GRID_POWER_PHASES):
        found = phase_power_suggestions(hass)
        if found:
            updated.update(found)
            updated["phase_fields_offered"] = True
    if updated == current:
        return
    changes = {k: v for k, v in updated.items() if current.get(k) != v}
    if entry.options:
        hass.config_entries.async_update_entry(entry, options=model.apply(stored, changes))
    else:
        hass.config_entries.async_update_entry(entry, data=model.apply(stored, changes))
