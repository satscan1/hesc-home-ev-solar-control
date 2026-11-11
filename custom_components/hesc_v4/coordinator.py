"""The 30-second round (the v2 decision round pace): read inputs, run the ported v2 logic.

The solar/HPVC-release logic (solar.py) runs here on the live states. Its status
texts go to HESC v4's own sensors and its history lines to /config/hesc_v4/history.jsonl.

Commands: the ported logic gives the same commands as v2 (HPVC release request,
charger, notifications). In shadow mode v3 sends none of them, not even the notifications
v2 sends in shadow mode; they are only kept in `would_do`. With shadow mode off v3 sends them,
like v2's output nodes. v2's own helpers are never written: the one v2 helper the logic sets
(`input_boolean.hesc_plan_owns_charging`) is kept by v3 itself (`own_flags`, saved in
/config/hesc_v4/own_flags.json so it survives a restart, like v2's input_boolean).

Prices (prices.py), the charge plan (plan.py), its expected cost, the price forecast
(price_forecast.py, every 15 minutes, own history file) and the charge plan control
(charge_plan.py) run here too, on v3's own computed sensors. Price fetch for action-only
sources and the holiday calendar ask Home Assistant for data (read-only actions with a
response). Charge plan settings: while shadow mode is on v3 reads v2's own plan helpers where
they exist (its own plan setting entities where they do not, e.g. without v2); with shadow off
it uses its own plan setting entities.

Like v2's Node-RED flow context, the release context lives in memory only: it starts fresh
after an HA restart and also after a reload of the integration (e.g. saving its options).
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util
from homeassistant.util.file import write_utf8_file

from . import (
    advice,
    advisor,
    charge_now,
    charge_plan,
    charger_specs,
    compare,
    costs,
    current,
    diag_templates,
    ev_soc,
    forecast,
    kickstart,
    morning,
    package_templates,
    phase_advice,
    phone,
    plan,
    price_forecast,
    pricefetch,
    prices,
    report,
    settings_backup,
    texts,
)
from .const import (
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
    CONF_GRID_POWER,
    CONF_GRID_POWER_PHASES,
    CONF_HPVC_ENABLED,
    CONF_HPVC_LIMITED,
    CONF_IRRADIANCE,
    CONF_PV_POWER,
    CONF_SOLAR_TODAY,
    CONF_SOLAR_TOMORROW,
    CONF_STANDALONE,
    CONF_USE_HPVC_SOURCES,
    CONF_USE_IRRADIANCE,
    DOMAIN,
    HPVC_GRID_HELPER,
    HPVC_PV_HELPER,
    UPDATE_INTERVAL,
    VERSION,
)
from . import cars, export, fleet, learn, model, planning, safety
from .inputs import Inputs, _Reader, read_inputs
from .jscompat import iso, js_json
from .phase_advice import PhaseStats
from .plan_settings import BY_KEY, SETTINGS
from .solar import REQ as HPVC_REQUEST, Result, evaluate
from .tuning import NUMBERS, SWITCHES

_LOGGER = logging.getLogger(__name__)

type HescConfigEntry = ConfigEntry[HescCoordinator]

# v2 status helpers that v3 publishes to its own sensors instead (restored after a restart,
# like v2's input_text helpers)
PUBLISHED = (
    "input_text.hesc_state",
    "input_text.hesc_reason",
    "input_text.hesc_insight_1",
    "input_text.hesc_insight_2",
    "input_text.hesc_insight_3",
    "input_text.hesc_last_action",
    "input_text.hesc_plan_status",
    "input_text.hesc_kick_status",
    "input_text.hesc_current_status",  # v3 only: current control (16-10)
    "input_text.hesc_costs_export_info",
    "input_text.hesc_settings_backup_info",
    # advice and report
    "input_text.hesc_advice",
    "input_text.hesc_advice_updated",
    "input_text.hesc_report_generated",
    "input_boolean.hesc_report_ready",
)
# v2 sensors v3 computes itself; the ported logic reads v3's values under v2's names
COMPUTED = ("sensor.hesc_prices", "sensor.hesc_charge_plan", "sensor.hesc_price_forecast",
            "sensor.hesc_expected_charge_cost", "sensor.hesc_holidays", "sensor.hesc_price_fetch",
            "sensor.hesc_ev_soc", "sensor.hesc_notice", "binary_sensor.hesc_diag_ev_connected",
            "sensor.hesc_charging_costs", "sensor.hesc_ev_battery_backup_sensor",
            "sensor.hesc_solar_still_to_come_today", advice.SENSOR)
# v4 alpha runs next to HESC v3 (decision 30-10-2026: "v3 stays untouched"). Where v3 read v2's
# files once, v4 reads v3's files (read only, never written): /config/hesc_v3/.
PREV_DIR = "hesc_v3"
PREV_DOMAIN = "hesc"  # HESC v3's integration
V2_PRICE_HISTORY = (PREV_DIR, "price_history.json")
V2_SOC_PLUGINS = (PREV_DIR, "ev_soc_plugins.json")
V2_COSTS = (PREV_DIR, "charging_costs.json")
V2_HISTORY = (PREV_DIR, "history.jsonl")
REPORT_DIR = ("www", DOMAIN)  # served as /local/hesc_v4/
REPORT_WEBHOOK = DOMAIN + "_report_viewed"
# v2 helpers the logic switches itself; v3 keeps them (live mode only)
OWN_FLAGS = ("input_boolean.hesc_plan_owns_charging",)
COMMAND_TIMEOUT = 30  # seconds per action (one round)
_V2_HELPER = re.compile(r"^input_[a-z]+\.hesc_")

# setup choice -> v2 text helper that holds it
_TEXT_HELPERS = {
    CONF_FORECAST_NOW: "input_text.hesc_forecast_now_sensor",
    CONF_FORECAST_30M: "input_text.hesc_forecast_30m_sensor",
    CONF_FORECAST_ATTRIBUTE: "input_text.hesc_forecast_attribute",
    CONF_IRRADIANCE: "input_text.hesc_irradiance_sensor",
    CONF_EV_CONNECTED: "input_text.hesc_ev_connected_sensor",
    CONF_EV_POWER: "input_text.hesc_ev_power_sensor",
    CONF_EV_GREEN_ENERGY: "input_text.hesc_ev_green_energy_sensor",
    CONF_EV_SOC: "input_text.hesc_ev_soc_sensor",
    CONF_CHARGER_MODE: "input_text.hesc_charger_mode_entity",
    CONF_CHARGER_ECO_VALUES: "input_text.hesc_charger_eco_value",
    CONF_CHARGER_SOLAR_SWITCH: "input_text.hesc_charger_solar_switch_entity",
    CONF_EV_DISCONNECTED_VALUES: "input_text.hesc_ev_disconnected_values",
    CONF_HPVC_ENABLED: "input_text.hesc_hpvc_enabled_entity",
    CONF_HPVC_LIMITED: "input_text.hesc_hpvc_limited_entity",
    CONF_SOLAR_TODAY: "input_text.hesc_solar_today_sensor",
    CONF_CHARGER_CURRENT: current.ENTITY_HELPER,
    CONF_SOLAR_TOMORROW: "input_text.hesc_solar_tomorrow_sensor",
    CONF_CHARGER_START_STOP: "input_text.hesc_charger_start_stop_entity",
    CONF_CHARGER_RESUME: "input_text.hesc_charger_resume_entity",
}
_BOOL_HELPERS = {
    CONF_USE_IRRADIANCE: "input_boolean.hesc_use_irradiance",
    CONF_GRID_EXPORT_POSITIVE: "input_boolean.hesc_grid_export_positive",
    CONF_STANDALONE: "input_boolean.hesc_standalone",
}


def _float(v: Any, default: float) -> float:
    """A state text as a finite number, else `default`."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return default
    return f if math.isfinite(f) else default


def _js_state(state: Any) -> dict[str, Any]:
    # as Node-RED's home-assistant states: with last_changed / last_updated as ISO text
    return {"state": state.state, "attributes": state.attributes,
            "last_changed": state.last_changed.isoformat(), "last_updated": state.last_updated.isoformat()}


class _SynState:
    """A stand-in entity (forecast.py) as read_inputs reads a State."""

    def __init__(self, v: Mapping[str, Any]) -> None:
        self.state = v["state"]
        self.attributes = v.get("attributes") or {}


# Since 3.0.0: words in the charger's status that mean "paused" (Wallbox "Paused"; Dutch, German).
_PAUSED_WORDS = ("paused", "pause", "gepauzeerd", "pausiert", "suspended")


def paused_power_state(get: Any, cfg: Mapping[str, Any]) -> dict[str, Any] | None:
    """The EV power sensor as 0 W while the charger says it is paused, else None.

    Practice test 19-10-2026 (Wallbox Pulsar Plus): after a pause the charger kept reporting its old
    power (5.7 kW, then 870 W with status "Paused") for minutes while the car took nothing (the grid
    meter showed export), so HESC counted the car as charging. Paused means: the charger's start/stop
    switch is off, or its status sensor reads paused. Only a clear "off" or a paused status counts;
    unknown or unavailable leaves the power as it is.
    """
    pw_id = str(cfg.get(CONF_EV_POWER) or "").strip()
    pw = get(pw_id) if pw_id else None
    if pw is None:
        return None
    paused = False
    sw_id = str(cfg.get(CONF_CHARGER_START_STOP) or "").strip()
    if sw_id.split(".")[0] in ("switch", "input_boolean"):
        sw = get(sw_id)
        paused = sw is not None and str(sw.state).lower() == "off"
    st_id = str(cfg.get(CONF_EV_CONNECTED) or "").strip()
    if not paused and st_id:
        st = get(st_id)
        text = str(st.state).lower() if st is not None else ""
        paused = any(w in text for w in _PAUSED_WORDS)
    if not paused:
        return None
    return {"state": "0", "attributes": dict(pw.attributes),
            "last_changed": pw.last_changed.isoformat(), "last_updated": pw.last_updated.isoformat()}


class StatesView(Mapping[str, Mapping[str, Any]]):
    """All HA states as the v2 logic sees them, with v2's own helpers replaced by v3's settings.

    States are converted only when the logic reads them.
    """

    def __init__(self, hass: HomeAssistant, overrides: dict[str, dict[str, Any]]) -> None:
        self._hass = hass
        self._over = overrides

    def __getitem__(self, key: str) -> Mapping[str, Any]:
        if key in self._over:
            return self._over[key]
        s = self._hass.states.get(key)
        if s is None:
            raise KeyError(key)
        return _js_state(s)

    def __contains__(self, key: object) -> bool:
        return key in self._over or (isinstance(key, str) and self._hass.states.get(key) is not None)

    def __iter__(self) -> Iterator[str]:
        yield from self._over
        for s in self._hass.states.async_all():
            if s.entity_id not in self._over:
                yield s.entity_id

    def __len__(self) -> int:
        return len(list(iter(self)))


class HescCoordinator(DataUpdateCoordinator[Inputs]):
    """Reads the inputs like v2 and runs the ported v2 decision logic on them."""

    config_entry: HescConfigEntry

    def __init__(self, hass: HomeAssistant, entry: HescConfigEntry) -> None:
        super().__init__(hass, _LOGGER, config_entry=entry, name=DOMAIN, update_interval=UPDATE_INTERVAL)
        self.tuning: dict[str, float] = {n.key: float(n.default) for n in NUMBERS}
        self.switches: dict[str, bool] = {s.key: s.default for s in SWITCHES}
        self.shadow = True
        # Logic runs only once the tuning entities have restored their values.
        self.logic_ready = False
        self.context: dict[str, Any] | None = None  # v2: flow context "hesc" (memory only, like Node-RED)
        self.published: dict[str, str] = {}
        self.would_do: list[dict[str, Any]] = []  # the last commands (sent only with shadow mode off)
        self.own_flags: dict[str, bool] = dict.fromkeys(OWN_FLAGS, False)
        self.flags_path = Path(hass.config.path(DOMAIN, "own_flags.json"))
        # v4 step 4: only this time and the calendar of the car (planning.py); None = not loaded or
        # not made yet (made from v3's own fields at the first round, decision 2 of 31-10 17:25)
        self.planning: dict[str, Any] | None = None
        self.planning_path = Path(hass.config.path(DOMAIN, "planning.json"))
        # v4 step 4D: the charging power learned (learn.py) and what the plan reckons with (kW, source)
        self.learn: dict[str, Any] | None = None
        self.learn_path = Path(hass.config.path(DOMAIN, "charge_power.json"))
        self.plan_kw: tuple[float, str] | None = None
        self._gc_found: list[dict[str, Any]] | None = None  # v4 step 5: Grid Clock sensors (every minute)
        # fix 06-11: (price source, a sensor of its integration) for an action-only source (every minute)
        self._action_found: tuple[str, str | None] | None = None
        self.plug_told: str | None = None  # v4 step 6: the day the "plug in the car" reminder went out
        self.exports: dict[str, dict[str, Any]] = {}  # v4 step 8: the latest report per form
        # v4 step 4E: a car without a battery-level sensor (learn.fill_step), the level entered by hand
        self.fill: dict[str, Any] | None = None
        self.soc_entry: dict[str, Any] | None = None
        self.soc_entity: Any = None
        self.no_soc_over: dict[str, dict[str, Any]] = {}
        self.current_path = Path(hass.config.path(DOMAIN, "current_control.json"))
        self._commands: list[tuple[str, str, dict[str, Any], dict[str, Any] | None]] = []
        self._sending = False
        self.last_result: Result | None = None
        self.history_path = Path(hass.config.path(DOMAIN, "history.jsonl"))
        # prices and charge plan
        self.plan: dict[str, Any] = {s.key: s.default for s in SETTINGS}  # own charge plan settings
        self.switch_entities: dict[str, Any] = {}
        self.date_entities: dict[str, Any] = {}
        self.datetime_entities: dict[str, Any] = {}
        self.computed: dict[str, dict[str, Any]] = {}  # v2 sensor id -> {"state", "attributes"}
        self.plan_flow: dict[str, Any] = {}  # v2: flow context of the "Charge plan" node (memory only)
        # v4 08-11 (decision 09:32): after a Home Assistant start, once per car a notification that HESC
        # controls the car according to its plan again
        self._restart_note: set[str] = set() if hass.is_running else {"pending"}
        self.price_hist: Any = None
        self.price_hist_loaded = False
        self.price_hist_path = Path(hass.config.path(DOMAIN, "price_history.json"))
        self.fetch_rows: Any = None
        self.fetch_div: Any = None
        self._fetch_key: tuple[str, str] | None = None
        # battery level with fallbacks (v2 node context and its flow keys, memory only)
        self.soc_context: dict[str, Any] = {}
        self.soc_flow: dict[str, Any] = {}
        self.kick_flow: dict[str, Any] = {}  # v2: flow key hescKick (memory only)
        self.costs: dict[str, Any] | None = None  # v2: flow key hescCosts (None until loaded)
        self.costs_context: dict[str, Any] = {}
        self.morning_context: dict[str, Any] = {}
        self.compare = compare.CompareLog()  # differences with v2
        self.data_dir = Path(hass.config.path(DOMAIN))
        # decision 11-11-2026: the full back-up in its own folder, so it stays when HESC (and its folder) is removed
        self.backup_path = Path(hass.config.path("hesc_backup", export.FILE_NAMES["full"]))
        self.backup_meta: dict[str, Any] = {}
        # solar forecast source: overrides for the logic's view, and the
        # Forecast.Solar series fetched with its action (empty for other sources)
        self.current_ctx: dict[str, Any] = {}
        self.fc_over: dict[str, dict[str, Any]] = {}
        self.fs_series: dict[Any, float] = {}
        self.fc_kind = ""  # set in the first round
        self.soc_blocked = False  # own battery-level file could not be read: do not overwrite it
        self.soc_path = Path(hass.config.path(DOMAIN, "ev_soc_plugins.json"))
        # advice and report (v2 node and flow contexts, memory only)
        self.advice_gate_ctx: dict[str, Any] = {}
        self.advisor_flow: dict[str, Any] = {}
        self.advice_global: dict[str, Any] | None = None  # v2: global hescAdvice
        self.report_flow: dict[str, Any] = {}
        self._seasonal_on: bool | None = None
        self._standalone_seen: bool | None = None  # advice runs again when HPVC is switched on or off
        # since rc3: phase advice and the charger's start level as advice floor
        self.phase_stats = PhaseStats()
        self.phase_path = Path(hass.config.path(DOMAIN, "phase_stats.json"))
        self.phase_sign: float | None = None   # +1: phase sensors import positive, -1: export positive
        self.phase_votes: list[int] = []        # last sign checks (majority decides, review rc3)
        self.ev_max_days: dict[str, float] = {}  # highest charging power per day, last 30 days
        self._phase_saved_at = 0
        self._round_inputs: Inputs | None = None
        # since 3.0.0: "charge now to a goal" ({"goal": int, "until": datetime}) and its select entity;
        # the phone widget refresh (phone.py)
        self.charge_now: dict[str, Any] | None = None
        # decision 06-11-2026 13:23: "charge now to" is kept also without the EV plugged in; it
        # starts once the EV is plugged in and below the goal (the goal, else None)
        self.charge_now_wish: int | None = None
        self.charge_now_entity: Any = None
        self.widget_push = phone.WidgetPush()
        self._last_run: dict[str, int] = {}  # rc3: own pace per part (_due)
        self._phase_key: tuple[Any, ...] | None = None
        self.costs_path = self.data_dir / "charging_costs.json"
        # v4: each car its own round (cars.py). EV1 is held at rest; another car waits in a slot.
        self._active: str = model.EV1
        self._slots: dict[str, dict[str, Any]] = {}
        self._extra: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in cars.SPLIT}
        self._hpvc_want: dict[str, bool] = {}  # per car: does its round ask HPVC for a release
        # v4, part C: how two cars share the grid (fleet.py); the view of the car whose round it is
        self._fleet_over: dict[str, Any] | None = None
        self.fleet_mode: str | None = None       # the way chosen (automatic: changes on a quarter)
        self.fleet_sun = fleet.SunState()        # decision 6: which car gets the sun first, who is held
        self.fleet_outside = fleet.OutsideState()  # 31-10 13:55: a car charging by itself that gives way
        self.house_guard = fleet.GuardState()    # part D: most current per car near the house connection
        # step 3: two cars on one charger - which car is on it, battery levels when charging began,
        # and the day the cable swap reminder went out
        self.attached: dict[str, str] = {}
        self._soc_start: dict[str, dict[str, float]] = {}
        self._swap_told: dict[str, str] = {}
        self._fleet_last_grid: dict[str, Any] = {}  # per car: when it last charged from the grid

    @property
    def settings(self) -> dict:
        """Setup choices: the options flow stores the complete set, so it replaces the first setup."""
        return model.flatten(self.config_entry.options or self.config_entry.data, self._active)

    # ---- v4: each car its own round (cars.py) -------------------------------------------
    @property
    def nested(self) -> dict[str, Any]:
        return model.ensure_nested(self.config_entry.options or self.config_entry.data)

    def ev_ids(self) -> list[str]:
        """The cars set up, EV1 first (with one car only EV1, decision 8)."""
        return model.ev_ids(self.nested) or [model.EV1]

    @property
    def active_ev(self) -> str:
        """The car whose round (or entity) the coordinator is working for right now."""
        return self._active

    def owner_of(self, key: str, ev: str) -> str | None:
        """Car, charger or None (shared) a setting key belongs to, seen from car `ev`."""
        return model.owner(key, ev, model.charger_of(self.nested, ev))

    def _home(self, owner: str | None) -> bool:
        """Values of this owner live in the coordinator's own dicts: shared, EV1 and EV1's charger."""
        return owner is None or owner == model.EV1 or owner == model.charger_of(self.nested, model.EV1)

    @contextmanager
    def as_car(self, ev: str) -> Iterator[None]:
        """Work for car `ev`: its round, or one of its entities. With EV1 (and with one car) nothing moves."""
        if ev == self._active:
            yield
            return
        prev = self._active
        self._switch(prev, ev)
        try:
            yield
        finally:
            self._switch(ev, prev)

    def _switch(self, a: str, b: str) -> None:
        if a != model.EV1 and b != model.EV1:
            self._switch(a, model.EV1)
            self._switch(model.EV1, b)
            return
        if a == b:
            return
        # the state of car a goes to its slot
        slot = self._slots.setdefault(a, {})
        for name in cars.WHOLE:
            slot[name] = getattr(self, name)
        slot["published"] = {k: self.published.pop(k) for k in cars.PUBLISHED if k in self.published}
        slot["computed"] = {k: self.computed.pop(k) for k in cars.COMPUTED if k in self.computed}
        if a == model.EV1:
            slot["split"] = {name: getattr(self, name) for name in cars.SPLIT}
        else:
            home = self._slots[model.EV1]["split"]
            for name in cars.SPLIT:
                for key, value in getattr(self, name).items():
                    owner = self.owner_of(key, a)
                    if self._home(owner):
                        home[name][key] = value
                    else:
                        self._extra[name].setdefault(str(owner), {})[key] = value
        # car b comes out of its slot
        new = self._slots.get(b)
        if new is None:
            new = self._slots[b] = cars.fresh(b, self._car_paths(b), self.own_flags)
        for name in cars.WHOLE:
            setattr(self, name, new[name])
        self.published.update(new.get("published") or {})
        self.computed.update(new.get("computed") or {})
        if b == model.EV1:
            for name in cars.SPLIT:
                setattr(self, name, new["split"][name])
        else:
            home = self._slots[model.EV1]["split"]
            for name in cars.SPLIT:
                setattr(self, name, self._merged(name, home[name], b))
        self._active = b

    def _merged(self, name: str, home: dict[str, Any], ev: str) -> dict[str, Any]:
        """What car `ev` sees: the shared keys from home, its own and its charger's from their extra
        dicts, else the default (never EV1's value)."""
        out = {k: v for k, v in home.items() if self._home(self.owner_of(k, ev))}
        defaults: dict[str, Any] = {}
        if name == "plan":
            defaults = {s.key: s.default for s in SETTINGS}
        elif name == "tuning":
            defaults = {n.key: float(n.default) for n in NUMBERS}
        elif name == "switches":
            defaults = {w.key: w.default for w in SWITCHES}
        for key, value in defaults.items():
            if not self._home(self.owner_of(key, ev)):
                out[key] = value
        for owner in (ev, model.charger_of(self.nested, ev)):
            if not self._home(owner):
                out.update(self._extra[name].get(owner, {}))
        return out

    def _car_paths(self, ev: str) -> dict[str, Path]:
        d = self.data_dir
        return {"flags_path": d / cars.file_name("own_flags.json", ev),
                "current_path": d / cars.file_name("current_control.json", ev),
                "history_path": d / cars.file_name("history.jsonl", ev),
                "soc_path": d / cars.file_name("ev_soc_plugins.json", ev),
                "costs_path": d / cars.file_name("charging_costs.json", ev),
                "planning_path": d / cars.file_name("planning.json", ev),
                "learn_path": d / cars.file_name("charge_power.json", ev)}

    def store_ev(self, ev: str, values: dict[str, Any]) -> None:
        """v4: a car's own fields that are not settings of the logic (its name, its charger)."""
        entry = self.config_entry
        updated = model.ensure_nested(entry.options or entry.data)
        updated["evs"].setdefault(ev, {}).update(values)
        if entry.options:
            self.hass.config_entries.async_update_entry(entry, options=updated)
        else:
            self.hass.config_entries.async_update_entry(entry, data=updated)

    def store_settings(self, changes: dict[str, Any], ev: str = model.EV1) -> None:
        """Write changed setup choices back to the config entry, each at its own place (shared, the car,
        its charger; model.apply). Options hold the complete set once the options flow has run; before
        that, the first setup's data. No reload is needed: the coordinator reads them every round."""
        entry = self.config_entry
        current = entry.options or entry.data
        if all(model.flatten(current, ev).get(k) == v for k, v in changes.items()):
            return
        updated = model.apply(current, changes, ev)
        if entry.options:
            self.hass.config_entries.async_update_entry(entry, options=updated)
        else:
            self.hass.config_entries.async_update_entry(entry, data=updated)

    def house_connection(self) -> str | None:
        """The house connection as "3x25 A" from the two settings (phases, amps per phase); None while the
        phases are not known (then no comfort guard and no first estimate, as v3)."""
        ph, amps = str(self.plan.get("house_phases") or ""), _float(self.plan.get("house_amps"), 0)
        return f"{ph}x{amps:g} A" if ph in ("1", "3") and amps > 0 else None

    # ---- own charge plan settings --------------------------------------------------
    def set_plan_setting(self, key: str, value: Any) -> None:
        old = self.plan.get(key)
        self.plan[key] = value
        if key == "soc_entered":  # v4 step 4E: the battery level now, entered by hand (phone)
            plug = (self.fill or {}).get("plug") or {}
            self.soc_entry = {"soc": float(value), "kwh": float(plug.get("kwh") or 0)} if value else None
        # v2 automation "Auto advice and seasonal threshold exclude each other" (own switches)
        other = advice.EXCLUSIVE.get(key)
        if other and value and not old:
            sw = self.switch_entities.get(other)
            if sw is not None and sw.hass is not None:
                sw.set_from_logic(False)
            else:
                self.plan[other] = False

    def _own_plan_overrides(self) -> dict[str, dict[str, Any]]:
        over: dict[str, dict[str, Any]] = {}
        for spec in SETTINGS:
            v = self.plan.get(spec.key)
            attrs: dict[str, Any] = {}
            if spec.kind == "switch":
                state = "on" if v else "off"
            elif spec.kind == "number":
                state = str(float(v)) if v is not None else "unknown"
            elif spec.kind == "datetime":
                if v is None:
                    state = "unknown"
                else:
                    loc = dt_util.as_local(v)
                    state = loc.strftime("%Y-%m-%d %H:%M:%S")
                    attrs = {"has_date": True, "has_time": True, "timestamp": loc.timestamp()}
            elif spec.kind == "date":
                state = v.isoformat() if v is not None else "unknown"
                attrs = {"has_date": True, "has_time": False}
            else:
                state = "" if v is None else str(v)
            over[spec.helper] = {"state": state, "attributes": attrs}
        return over

    # ---- what the ported v2 logic sees -----------------------------------------------
    def _overrides(self) -> dict[str, dict[str, Any]]:
        cfg = self.settings
        over: dict[str, dict[str, Any]] = {}

        def put(eid: str, state: Any) -> None:
            over[eid] = {"state": str(state), "attributes": {}}

        for key, helper in _TEXT_HELPERS.items():
            put(helper, cfg.get(key, ""))
        for key, helper in _BOOL_HELPERS.items():
            put(helper, "on" if cfg.get(key) else "off")
        pv, grid = cfg.get(CONF_PV_POWER, ""), cfg.get(CONF_GRID_POWER, "")
        if cfg.get(CONF_USE_HPVC_SOURCES):
            for helper, cur in ((HPVC_PV_HELPER, "pv"), (HPVC_GRID_HELPER, "grid")):
                s = self.hass.states.get(helper)
                v = s.state.strip() if s is not None else ""
                if v not in ("", "unknown", "unavailable"):
                    if cur == "pv":
                        pv = v
                    else:
                        grid = v
        put("input_text.hesc_pv_power_sensor", pv)
        put("input_text.hesc_grid_power_sensor", grid)
        for spec in NUMBERS:
            put(spec.helper, self.tuning[spec.key])
        for sw in SWITCHES:
            put(sw.helper, "on" if self.switches[sw.key] else "off")
        # v4 08-11: a car HESC does not control works as in shadow mode (it reads and plans, sends nothing)
        put("input_boolean.hesc_shadow_mode", "on" if self.shadow or not self.car_controlled() else "off")
        put("input_boolean.hesc_charger_on_by_hand", "on" if self._charger_by_hand() else "off")
        put("input_boolean.hesc_plan_leads", "on")  # v4 08-11 (decision 09:32): the plan leads (charge_plan.py)
        # v3 never owns HPVC-off (plan B is not in v3); the grid-charging flag is v3's own
        put("input_boolean.hesc_owns_hpvc_off", "off")
        for eid in OWN_FLAGS:  # like v2's input_boolean: also visible in shadow mode
            put(eid, "on" if self.own_flags[eid] else "off")
        for eid in PUBLISHED:
            put(eid, self.published.get(eid, ""))
        own_plan = self._own_plan_overrides()
        if self.shadow:
            # 3.0.0: in shadow mode v3 reads v2's plan helpers, but only where they exist. Without v2
            # (every new user) it uses its own plan settings; before, prices and plans stayed empty.
            own_plan = {eid: v for eid, v in own_plan.items() if self.hass.states.get(eid) is None}
        over.update(own_plan)
        for eid in COMPUTED:
            if eid in self.computed:
                over[eid] = self.computed[eid]
            else:
                # not computed yet: as if v2's sensor did not exist
                over[eid] = {"state": "unknown", "attributes": {}}
        if "sensor.hesc_prices" not in self.computed:
            over["sensor.hesc_prices"] = {"state": "", "attributes": {"tz": self.hass.config.time_zone}}
        over.update(self.fc_over)
        if self._fleet_over is not None:  # v4, two cars: how this car shares the grid (fleet.py)
            over[fleet.ENTITY] = self._fleet_over
        if (self.plan.get("price_source") == prices.GRID_CLOCK and not str(self.plan.get("price_sensor") or "").strip()):
            if self._gc_found is None:
                self._gc_found = prices.grid_clock_candidates(self.hass.states.async_all("sensor"))
            found = self._gc_found
            if len(found) == 1:  # v4 step 5: one Grid Clock zone found - use it (decision 30-10 19:23, point 2)
                over["input_text.hesc_price_sensor"] = {"state": found[0]["entity_id"], "attributes": {}}
        if (self.plan.get("price_source") in pricefetch.ACTION_SOURCES
                and not str(self.plan.get("price_sensor") or "").strip()):
            # fix 06-11-2026 (EnergyZero gave no prices): an action-only source needs a sensor of its
            # integration to find the config entry; when none is set, take one of that integration
            from .finders import action_source_sensor

            if self._action_found is None or self._action_found[0] != self.plan.get("price_source"):
                src = str(self.plan.get("price_source"))
                self._action_found = (src, action_source_sensor(self.hass, src))
            if self._action_found[1]:
                over["input_text.hesc_price_sensor"] = {"state": self._action_found[1], "attributes": {}}
        if self.plan_kw is not None and self.plan_kw[1] in ("learned", "estimate"):  # v4 step 4D (learn.py)
            over["input_number.hesc_plan_charge_kw"] = {"state": str(float(self.plan_kw[0])), "attributes": {}}
        if self.planning is not None:  # v4 step 4: only this time and the calendar (planning.py)
            over[planning.ENTITY] = {"state": "on", "attributes": {"planning": self.planning}}
            # for the parts ported from v2 (morning summary): v2's holiday helpers from the vacation
            on_vac = planning.on_vacation(self.planning, dt_util.now().date())
            vac = self.planning.get("vacation") or {}
            over["input_boolean.hesc_vacation"] = {"state": "on" if on_vac else "off", "attributes": {}}
            over["input_datetime.hesc_vacation_until"] = {
                "state": str(vac.get("to") or "unknown") if on_vac else "unknown", "attributes": {}}
        cap = self.house_guard.caps.get(self._active)
        if cap is not None:  # v4 part D: the house is close to its connection (fleet.comfort_guard)
            ph = int(self.charger_phases() or (fleet.parse_connection(self.house_connection()) or (3,))[0])
            over[fleet.GUARD] = {"state": "on", "attributes": {"max_a": cap, "max_w": cap * ph * fleet.VOLT}}
        paused = paused_power_state(self.hass.states.get, cfg)
        if paused is not None:
            over[str(cfg.get(CONF_EV_POWER)).strip()] = paused
        over.update(self.no_soc_over)  # v4 step 4E
        over.update(self._away_states())
        return over

    def _refresh_forecast(self) -> None:
        """Work out the forecast source and its stand-ins for this round (forecast.py)."""
        self.fc_over = {}
        try:
            self.fc_over = forecast.overrides(self._view(), dt_util.now(), self.fs_series,
                                              forecast_solar=self.forecast_solar_entry() is not None)
        except Exception:
            _LOGGER.exception("HESC v4 could not read the solar forecast this round")
        kind = (self.fc_over.get(forecast.SOURCE) or {}).get("state") or forecast.KIND_SOLCAST
        changed = kind != self.fc_kind
        self.fc_kind = kind
        if changed:
            self.update_forecast_issue()

    @callback
    def update_forecast_issue(self) -> None:
        """Without a solar forecast: one note under Settings → Repairs on how to add one."""
        from homeassistant.helpers import issue_registry as ir

        if self.fc_kind == forecast.KIND_NONE:
            ir.async_create_issue(
                self.hass, DOMAIN, "no_solar_forecast", is_fixable=False, is_persistent=False,
                severity=ir.IssueSeverity.WARNING, translation_key="no_solar_forecast",
                learn_more_url="https://github.com/BJReplay/ha-solcast-solar",
            )
        else:
            ir.async_delete_issue(self.hass, DOMAIN, "no_solar_forecast")

    def _inputs_cfg_and_getter(self) -> tuple[dict[str, Any], Any]:
        """Setup choices and state getter for read_inputs, with the forecast stand-ins applied."""
        cfg = dict(self.settings)
        for key, helper in _TEXT_HELPERS.items():
            if helper in self.fc_over:
                cfg[key] = self.fc_over[helper]["state"]
        syn = {e: v for e, v in self.fc_over.items() if e.startswith("sensor.hesc_v4_internal_")}
        paused = paused_power_state(self.hass.states.get, cfg)
        if paused is not None:
            syn[str(cfg.get(CONF_EV_POWER)).strip()] = paused
        syn.update(self._away_states())

        def get(entity_id: str) -> Any:
            if entity_id in syn:
                return _SynState(syn[entity_id])
            return self.hass.states.get(entity_id)

        return cfg, get

    def forecast_solar_entry(self) -> str | None:
        """Config entry of Forecast.Solar when one of the chosen forecast sensors is one of its sensors."""
        from homeassistant.helpers import entity_registry as er

        reg = er.async_get(self.hass)
        for key in (CONF_FORECAST_NOW, CONF_FORECAST_30M, CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW):
            ent = reg.async_get(str(self.settings.get(key) or ""))
            if ent is not None and ent.platform == "forecast_solar" and ent.config_entry_id:
                return ent.config_entry_id
        return None

    async def async_fetch_forecast_solar(self, _now: Any = None) -> None:
        """Forecast.Solar has no series in its sensors: ask its action for one (every 15 min)."""
        entry_id = self.forecast_solar_entry()
        if entry_id is None or not self.hass.services.has_service("forecast_solar", "get_forecast"):
            self.fs_series = {}
            return
        try:
            resp = await self.hass.services.async_call(
                "forecast_solar", "get_forecast", {"config_entry": entry_id}, blocking=True, return_response=True)
        except Exception as err:  # noqa: BLE001 - also schema errors; then no series (not an old one)
            _LOGGER.warning("HESC v4 could not get the Forecast.Solar series: %s", err)
            self.fs_series = {}
            return
        self.fs_series = forecast.parse_series((resp or {}).get("watts"))

    def _now_ms(self) -> int:
        return int(dt_util.utcnow().timestamp() * 1000)

    async def _async_update_data(self) -> Inputs:
        self._refresh_forecast()
        if self.shared_chargers():
            self._part("which car is on the charger", self._detect_attached)
        cfg, get = self._inputs_cfg_and_getter()
        inputs = read_inputs(get, cfg)
        inputs.forecast_source = self.fc_kind
        self._round_inputs = inputs
        if self.logic_ready:
            try:
                self._run_logic()
            except Exception:
                _LOGGER.exception("HESC v4 decision round failed; inputs and settings stay available")
        return inputs

    def _view(self) -> StatesView:
        return StatesView(self.hass, self._overrides())

    @staticmethod
    def _getter(view: StatesView):
        def get(entity_id: str):
            if not entity_id or entity_id not in view:
                return None
            v = view[entity_id]
            return v["state"], v["attributes"]
        return get

    @callback
    def update_backup_sensor(self, _now: Any = None) -> None:
        """v2 template "HESC EV battery backup sensor" (every 10 minutes and at start), per car."""
        for ev in self.ev_ids():
            with self.as_car(ev):
                self._update_backup_sensor()

    def _update_backup_sensor(self) -> None:
        from homeassistant.helpers import device_registry as dr
        from homeassistant.helpers import entity_registry as er

        devreg, entreg = dr.async_get(self.hass), er.async_get(self.hass)

        def device_id(e: str) -> str | None:
            ent = entreg.async_get(e) if e else None
            return ent.device_id if ent else None

        def device_name(d: str | None) -> Any:
            dev = devreg.async_get(d) if d else None
            return (dev.name_by_user or dev.name) if dev else None

        bats = sorted(s.entity_id for s in self.hass.states.async_all("sensor")
                      if s.attributes.get("device_class") == "battery" and s.attributes.get("unit_of_measurement") == "%")
        main = str(self.settings.get(CONF_EV_SOC, "") or "")
        prev = self.computed.get("sensor.hesc_ev_battery_backup_sensor", {}).get("state")
        state = package_templates.backup_sensor(main, bats, device_id, device_name)
        device = package_templates.backup_device(prev, device_id, device_name)
        self.computed["sensor.hesc_ev_battery_backup_sensor"] = {"state": state, "attributes": {"device": device}}

    def _part(self, name: str, fn: Any, *args: Any) -> None:
        """Run one ported part; like a Node-RED node, a fault in it does not stop the others."""
        try:
            fn(*args)
        except Exception:
            _LOGGER.exception("HESC v4 part %s failed this round", name)

    def _solar_remaining(self) -> None:
        get = self._getter(self._view())
        try:
            state = package_templates.solar_remaining(get, dt_util.now())
        except (TypeError, ValueError, AttributeError):
            state = "unavailable"  # HA: the template fails to render
        self.computed["sensor.hesc_solar_still_to_come_today"] = {"state": state, "attributes": {"unit_of_measurement": "kWh"}}

    def _due(self, name: str, seconds: float) -> bool:
        """Since rc3: parts that need not run every 30 s get their own pace."""
        now = self._now_ms()
        last = self._last_run.get(name)
        if last is not None and now - last < seconds * 1000 - 1000:
            return False
        self._last_run[name] = now
        return True

    def _run_logic(self) -> None:
        if self._due("solar still to come", 300):  # the forecast itself changes every 15-30 min
            self._part("solar still to come", self._solar_remaining)
        # v4: each car its own round (cars.py); with two cars in the order of decision 4 (fleet.py), so
        # a car's plan knows the quarters of the cars before it. With one car this is v3's round.
        evs = self.ev_ids()
        self._part("house connection guard", lambda: self._house_guard(evs))
        if len(evs) == 1:
            with self.as_car(evs[0]):
                self._car_round()
        else:
            self._fleet_rounds(evs)
        if self._due("dashboard templates", 60):  # dashboard only
            self._part("dashboard templates", self._run_dashboard_templates)
        self._part("advice: when to run", self._run_advice_gate)
        self._part("seasonal start threshold", self._check_seasonal_switch)
        self._part("differences with v2", self._run_compare)
        self._part("phase advice", self._run_phase_advice)
        for ev in evs:  # each car its own widget refresh, to its own phones (decision 31-10 20:34)
            with self.as_car(ev):
                self._part("phone widgets", self._phone_widgets)

    def _house_guard(self, evs: list[str]) -> None:
        """v4 part D: comfort guard for the house connection (fleet.comfort_guard), also with one car.
        Without a house connection, or with a load balancer, it does nothing (v3 behaviour)."""
        conn, lb = self.house_connection(), self.plan.get("house_load_balancer")
        if fleet.house_limit_w(conn) is None or str(lb or "") == "Yes":
            self.house_guard = fleet.GuardState()
            return
        house = fleet.parse_connection(conn)
        order = fleet.priority(self._fleet_cars(evs)) if len(evs) > 1 else list(evs)
        cars = []
        for ev in order:
            with self.as_car(ev):
                inp = self._round_inputs
                ent = str(self.settings.get(CONF_CHARGER_CURRENT) or "").strip()
                st = self.hass.states.get(ent) if ent else None
                cur = _float(st.state, -1) if st is not None else -1
                hi = _float((st.attributes or {}).get("max"), 16) if st is not None else 16
                cars.append(fleet.GuardCar(
                    key=ev, power_w=float((inp.ev_power_w or 0.0) if inp else 0.0),
                    current_a=cur if cur >= 0 else None,
                    phases=int(self.charger_phases() or (house[0] if house else 3)),
                    can_set_current=bool(ent), max_a=hi))
        grid = self.data.grid_w if self.data is not None else None
        self.house_guard = fleet.comfort_guard(cars, grid, conn, lb, self.house_guard)

    def _fleet_rounds(self, evs: list[str]) -> None:
        cars_now = self._fleet_cars(evs)
        now = dt_util.now()
        setting = {"Automatic": fleet.AUTO, "One after the other": fleet.AFTER, "Together": fleet.TOGETHER}.get(
            str(self.plan.get("fleet_grid_mode") or ""), fleet.DEFAULT_MODE)
        together_w = _float(self.plan.get("fleet_together_kw"), 0) * 1000 or None
        may_change = self.fleet_mode is None or (now.minute % 15 == 0 and now.second < 30)  # decision 5
        pr = (self.computed.get("sensor.hesc_prices") or {}).get("attributes") or {}
        prices = list(pr.get("raw_today") or []) + list(pr.get("raw_tomorrow") or [])
        self.fleet_mode = fleet.choose_mode(setting, cars_now, prices, now, together_w, self.fleet_mode, may_change)
        self._fleet_sun(evs, now)
        self._fleet_outside(cars_now, now)
        self._swap_reminder(now)
        pausing = set(self.fleet_outside.paused)
        planned_now: dict[str, list[str]] = {}
        for ev in fleet.priority(cars_now):
            with self.as_car(ev):
                self._fleet_over = fleet.view_for(ev, cars_now, self.fleet_mode, together_w, planned_now, now,
                                                  pausing)
                ch = model.charger_of(self.nested, ev)
                if ch in self.shared_chargers() and self.attached.get(ch) == ev:
                    # step 3 (decision 31, margin 15:09): the car on the charger is ready half an hour before the swap time
                    sw = fleet.swap_ready_by(now, self.plan.get("swap_time") or fleet.DEFAULT_SWAP)
                    if sw is not None:
                        self._fleet_over["attributes"]["ready_by"] = sw.isoformat()
                try:
                    self._car_round()
                finally:
                    self._fleet_over = None
                raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
                planned_now[ev] = fleet.Car(ev, 0, plan=fleet.parse_plan(raw)).planned

    # ---- step 3: two cars on one charger, taking turns (decisions 26, 30-32) ---------------------
    def shared_chargers(self) -> dict[str, list[str]]:
        """Chargers with more than one car: charger -> its cars (EV1 first)."""
        out: dict[str, list[str]] = {}
        for ev in self.ev_ids():
            out.setdefault(model.charger_of(self.nested, ev), []).append(ev)
        return {ch: evs for ch, evs in out.items() if len(evs) > 1}

    def _num_state(self, eid: str) -> float | None:
        st = self.hass.states.get(eid) if eid else None
        if st is None:
            return None
        try:
            v = float(st.state)
        except (TypeError, ValueError):
            return None
        unit = str((st.attributes or {}).get("unit_of_measurement") or "").lower()
        return v * 1000 if unit == "kw" else v

    def _which_car(self, ch: str, evs: list[str]) -> str:
        """Decision 30: chosen yourself, else the car's own plugged-in sensor, else the car whose battery
        level rises while the charger charges, else the car known before (EV1 at the very start)."""
        with self.as_car(evs[0]):
            chosen = {"EV1": model.EV1, "EV2": model.EV2}.get(str(self.plan.get("charger_car") or ""))
            power = self._num_state(str(self.settings.get(CONF_EV_POWER) or "").strip())
            active = _float(self.tuning.get("ev_active_w"), 400)
        if chosen in evs:
            return chosen
        plugged, socs = [], {}
        for ev in evs:
            with self.as_car(ev):
                st = self.hass.states.get(str(self.plan.get("car_plug_sensor") or "").strip())
                if st is not None and str(st.state).strip().lower() in ("on", "true", "plugged", "plugged in",
                                                                         "connected", "charging", "yes"):
                    plugged.append(ev)
                soc = self._num_state(str(self.settings.get(CONF_EV_SOC) or "").strip())
                if soc is not None:
                    socs[ev] = soc
        if len(plugged) == 1:
            return plugged[0]
        if power is not None and power > active:
            start = self._soc_start.setdefault(ch, dict(socs))
            rising = [ev for ev in evs if ev in socs and ev in start and socs[ev] - start[ev] >= 1.0]
            if len(rising) == 1:
                return rising[0]
        else:
            self._soc_start.pop(ch, None)
        return self.attached.get(ch) or evs[0]

    def _detect_attached(self) -> None:
        for ch, evs in self.shared_chargers().items():
            prev, now_ev = self.attached.get(ch), self._which_car(ch, evs)
            if prev and prev != now_ev:
                with self.as_car(prev):
                    owned = bool(self.own_flags.get(OWN_FLAGS[0]))
                if fleet.cable_moved(prev, now_ev, owned):
                    # HESC's grid charging was for the other car: back to the charger's own mode, the
                    # new car's own plan decides
                    with self.as_car(now_ev):
                        back = str(self.settings.get(CONF_CHARGER_RESUME) or "").strip()
                        pause = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
                        if back:
                            action = "button.press" if back.startswith("button.") else back.split(".")[0] + ".turn_on"
                            self._command({"action": action, "target": {"entity_id": [back]}, "data": {}})
                        elif pause:
                            self._command({"action": pause.split(".")[0] + ".turn_off",
                                           "target": {"entity_id": [pause]}, "data": {}})
            self.attached[ch] = now_ev

    def _away_states(self) -> dict[str, dict[str, Any]]:
        """For the car that is not on its (shared) charger: the charger shows "not connected" and 0 W,
        so its round neither plans on it nor sends it anything."""
        ch = model.charger_of(self.nested, self._active)
        att = self.attached.get(ch)
        if att is None or att == self._active or ch not in self.shared_chargers():
            return {}
        cfg = self.settings
        out: dict[str, dict[str, Any]] = {}
        conn = str(cfg.get(CONF_EV_CONNECTED) or "").strip()
        if conn:
            if conn.split(".")[0] in ("binary_sensor", "switch", "input_boolean"):
                off = "off"
            else:
                vals = [v.strip() for v in str(cfg.get(CONF_EV_DISCONNECTED_VALUES) or "").split(",") if v.strip()]
                off = vals[0] if vals else "Disconnected"
            out[conn] = {"state": off, "attributes": {}}
        pw = str(cfg.get(CONF_EV_POWER) or "").strip()
        if pw:
            out[pw] = {"state": "0", "attributes": {"unit_of_measurement": "W"}}
        return out

    def _charger_by_hand(self) -> bool:
        """v4: "de user kan de laadpaal altijd een zetje geven" (decision 08-11 09:32 / 15:45).

        By hand = the charger's start/stop switch went from off to on while HESC did not just switch it
        itself (no HESC command to the charger in the 3 minutes before): from Home Assistant or from the
        charger's own app alike. Charging by itself (Eco) does not switch it on - while the plan holds
        the switch is off - and after a restart HESC sees no switching, only "on": neither counts.
        Kept until the next planned quarter starts (then the plan takes over again), until the switch
        is off again, or until the car is unplugged."""
        sw = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
        st = self.hass.states.get(sw) if sw else None
        inp = self._round_inputs
        flow = self.plan_flow
        now = dt_util.now().timestamp()
        cur = st.state if st is not None else None
        prev = flow.get("hescSwPrev")
        if cur in ("on", "off"):
            flow["hescSwPrev"] = cur
        if inp is not None and not inp.ev_connected or cur == "off":
            flow.pop("hescByHand", None)
        elif prev == "off" and cur == "on" and now - float(flow.get("hescOwnCmd") or 0) > 180:
            flow["hescByHand"] = now
        since = flow.get("hescByHand")
        if since is not None:
            raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
            for t in fleet.parse_plan(raw).get("planned") or []:
                ts = dt_util.parse_datetime(str(t))
                if ts is not None and since < ts.timestamp() <= now:
                    flow.pop("hescByHand", None)  # the next planned quarter has started: the plan leads
                    break
        return "hescByHand" in flow

    def _restart_notice(self) -> None:
        """v4 08-11: after a Home Assistant start, once per car: "Home Assistant restarted · HESC controls
        <car> according to the plan again (next charging moment ...)" - when the car is plugged in, has an
        active plan and HESC controls it."""
        if "pending" not in self._restart_note or self._active in self._restart_note or self.data is None:
            return
        self._restart_note.add(self._active)
        inp = self._round_inputs
        raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
        p = fleet.parse_plan(raw)
        if self.shadow or not self.car_controlled() or inp is None or not inp.ev_connected or not p.get("active"):
            return
        now = dt_util.now()
        nxt = sorted(t for t in (dt_util.parse_datetime(str(x)) for x in (p.get("planned") or [])) if t and t > now - timedelta(minutes=15))
        when = f"{dt_util.as_local(nxt[0]):%H:%M}" if nxt else "none planned"
        name = model.ev_name(self.nested, self._active)
        msg = f"Home Assistant restarted · HESC controls {name} according to the plan again (next charging moment {when})."
        for target in [x.strip() for x in str(self.plan.get("notify_services") or "").split(",") if x.strip().startswith("notify.")]:
            self._command({"action": target, "data": {"title": "HESC controls the charger again", "message": msg}})

    def _plug_reminder(self) -> None:
        """v4 step 6 (decisions 27, 33): within 10 minutes after the car's own time, once a day, a
        notification to the car's phones when it has an active charge plan and is not plugged in. A car
        that waits for the cable on a shared charger gets the cable swap reminder instead."""
        if not self.plan.get("plug_reminder", True):
            return
        now = dt_util.now()
        sw = fleet.next_swap(now - timedelta(minutes=10), self.plan.get("plug_reminder_time") or "22:00")
        if sw is None or not sw <= now < sw + timedelta(minutes=10) or self.plug_told == now.date().isoformat():
            return
        inp = self._round_inputs
        if inp is None or inp.ev_connected:
            return
        ch = model.charger_of(self.nested, self._active)
        if ch in self.shared_chargers() and self.attached.get(ch) not in (None, self._active):
            return
        raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
        p = fleet.parse_plan(raw)
        dl = fleet.Car(self._active, 0, plan=p).deadline
        if not p.get("active") or dl is None or dl <= now:
            return
        if self._soc_enough(p, now):
            return
        self.plug_told = now.date().isoformat()
        name = model.ev_name(self.nested, self._active)
        local = dt_util.as_local(dl)
        msg = f"Don't forget to plug in {name}: there is a charge plan for {local:%H:%M} on {local:%d-%m}."
        for target in [x.strip() for x in str(self.plan.get("notify_services") or "").split(",")
                       if x.strip().startswith("notify.")]:
            self._command({"action": target, "data": {"title": "Plug in the car", "message": msg}})

    def _soc_enough(self, p: dict[str, Any], now: datetime) -> bool:
        """Decision 11-11-2026: no plug-in reminder when the car already has enough for its next goal.
        Only when the battery level is known and fresh: reported within the last 60 minutes. Unknown or
        older: the reminder goes as before."""
        try:
            goal = float(str(p.get("goal")).rstrip("%"))
        except (TypeError, ValueError):
            return False
        st = self.hass.states.get(str(self.settings.get(CONF_EV_SOC) or "").strip())
        if st is None:
            return False
        try:
            soc = float(st.state)
        except (TypeError, ValueError):
            return False
        seen = max(t for t in (st.last_updated, getattr(st, "last_reported", None)) if t is not None)
        return now - seen <= timedelta(minutes=60) and soc >= goal

    def _swap_reminder(self, now: datetime) -> None:
        """Decision 32: at the cable swap time a notification, when the first car is still on the charger
        and the other car has an active plan; to the phones of both cars, once a day."""
        for ch, evs in self.shared_chargers().items():
            att = self.attached.get(ch)
            with self.as_car(evs[0]):
                hhmm = str(self.plan.get("swap_time") or fleet.DEFAULT_SWAP)
                if self.plan.get("swap_reminder") is False:
                    continue  # switched off for this charger
            sw = fleet.next_swap(now - timedelta(minutes=10), hhmm)
            if sw is None or not sw <= now < sw + timedelta(minutes=10) \
                    or self._swap_told.get(ch) == now.date().isoformat():
                continue  # within 10 minutes after the swap time, once a day
            others = [ev for ev in evs if ev != att]
            waiting = []
            for ev in others:
                with self.as_car(ev):
                    raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
                    if fleet.Car(ev, 0, plan=fleet.parse_plan(raw)).has_plan:
                        waiting.append(ev)
            if not waiting:
                continue
            self._swap_told[ch] = now.date().isoformat()
            name = model.ev_name(self.nested, waiting[0]) or waiting[0].upper()
            phones: list[str] = []
            for ev in evs:
                with self.as_car(ev):
                    phones += [x.strip() for x in str(self.plan.get("notify_services") or "").split(",")
                               if x.strip().startswith("notify.")]  # like the plan's own notifications
            for target in dict.fromkeys(phones):
                self._command({"action": target, "data": {"title": "Move the cable",
                                                          "message": f"Time to move the cable to {name}."}})

    def _fleet_outside(self, cars: list[fleet.Car], now: datetime) -> None:
        """Decision 31-10 13:55: a car that charges by itself gives way (paused on the quarter) when the
        other car would otherwise not be in time; back on when that car no longer needs it."""
        before = self.fleet_outside
        self.fleet_outside = fleet.outside_plan_pause(cars, now, before)
        for ev, action in [(k, "turn_off") for k in sorted(set(self.fleet_outside.paused) - set(before.paused))] + \
                [(k, "turn_on") for k in fleet.outside_released(before, self.fleet_outside, cars)]:
            with self.as_car(ev):
                pause = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
                if pause:
                    self._command({"action": pause.split(".")[0] + "." + action, "target": {"entity_id": [pause]},
                                   "data": {}})

    def _fleet_sun(self, evs: list[str], now: datetime) -> None:
        """Decision 6: one car gets the sun first, the other only what is left when that starts its
        charger. HESC pauses the other car's charger and sends it back to its solar mode (fleet.py)."""
        cars = []
        for i, ev in enumerate(evs):
            with self.as_car(ev):
                inp = self._round_inputs  # EV1: this round's; another car: its last round's
                pause = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
                back = str(self.settings.get(CONF_CHARGER_RESUME) or "").strip()
                cars.append(fleet.SunCar(
                    key=ev, index=i, connected=bool(inp and inp.ev_connected),
                    solar=bool(inp and inp.in_solar_mode and not self.own_flags.get(OWN_FLAGS[0])),
                    power_w=float((inp.ev_power_w or 0.0) if inp else 0.0),
                    soc=inp.ev_soc if inp else None,
                    full_soc=_float(self.tuning.get("ev_full_soc"), 80),
                    battery_kwh=_float(self.plan.get("ev_battery_kwh"), 60),
                    start_w=self.advice_floor_w(),
                    active_w=_float(self.tuning.get("ev_active_w"), 400),
                    can_hold=bool(pause and back and pause.split(".")[0] in ("switch", "input_boolean"))))
        grid = self.data.grid_w if self.data is not None else None
        pv = self.data.pv_w if self.data is not None else None
        before = set(self.fleet_sun.held)
        self.fleet_sun = fleet.sun_division(cars, grid, now, self.fleet_sun, pv)
        on_sun = {x.key for x in cars if x.connected and x.solar}
        for ev in sorted(self.fleet_sun.held - before):
            with self.as_car(ev):
                pause = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
                self._command({"action": pause.split(".")[0] + ".turn_off", "target": {"entity_id": [pause]}, "data": {}})
        for ev in sorted((before - self.fleet_sun.held) & on_sun):
            with self.as_car(ev):
                back = str(self.settings.get(CONF_CHARGER_RESUME) or "").strip()
                if back:
                    action = "button.press" if back.startswith("button.") else back.split(".")[0] + ".turn_on"
                    self._command({"action": action, "target": {"entity_id": [back]}, "data": {}})

    def _fleet_cars(self, evs: list[str]) -> list[fleet.Car]:
        """What the division needs of every car, from its last round."""
        out = []
        for i, ev in enumerate(evs):
            with self.as_car(ev):
                raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
                inputs = self._round_inputs  # EV1: this round's; another car: its last round's
                active_w = _float(self.tuning.get("ev_active_w"), 400)
                grid_now = bool(inputs and inputs.ev_connected and (inputs.ev_power_w or 0) > active_w
                                and (self.own_flags.get(OWN_FLAGS[0]) or not inputs.in_solar_mode))
                now = dt_util.now()
                quarter = now.replace(minute=now.minute - now.minute % 15, second=0, microsecond=0)
                if grid_now:
                    self._fleet_last_grid[ev] = now
                last = self._fleet_last_grid.get(ev)
                pause = str(self.settings.get(CONF_CHARGER_START_STOP) or "").strip()
                out.append(fleet.Car(key=ev, index=i, connected=bool(inputs and inputs.ev_connected),
                                     plan=fleet.parse_plan(raw), grid_now=grid_now,
                                     grid_this_quarter=last is not None and last >= quarter,
                                     can_set_current=bool(str(self.settings.get(CONF_CHARGER_CURRENT) or "").strip()),
                                     outside_plan=grid_now and not self.own_flags.get(OWN_FLAGS[0])
                                     and self.charge_now is None,
                                     can_pause=pause.split(".")[0] in ("switch", "input_boolean")))
        return out

    def _car_round(self) -> None:
        """The parts of the round that belong to one car (the coordinator works for that car now)."""
        if self._active != model.EV1:  # EV1's inputs were read at the start of the round
            self._part("inputs", self._read_car_inputs)
        self._part("planning", self._run_planning)
        self._part("learn the charging power", self._run_learn)
        self._part("car without a battery-level sensor", self._run_no_soc)
        self._part("price and plan templates", self._run_plan_templates)
        view = self._view()
        self._part("charge plan", self._run_charge_plan, view)
        res = evaluate(view, self.context, self._now_ms())
        self._apply_solar(res)
        self._part("kickstart", self._run_kickstart)
        self._part("current control", self._run_current)
        self._part("charging costs", self._run_costs)
        self._part("plug-in reminder", self._plug_reminder)
        self._part("restart notice", self._restart_notice)
        if not self.soc_blocked:
            self._part("battery level", self._run_ev_soc)

    # ---- v4 step 4: only this time and the calendar (planning.py) ------------------------------
    def _run_planning(self) -> None:
        """Drop what is over in the car's planning, and show the coming week."""
        now = dt_util.now()
        if self.planning is None:
            self.planning = planning.empty()
            self._save_planning()
        p = planning.expire(self.planning, now)
        if p != self.planning:
            self.planning = p
            self._save_planning()
        get = self._getter(self._view())
        nxt = planning.next_moment(self.planning, get, now)
        self.computed["sensor.hesc_coming_week"] = {
            "state": nxt[0].isoformat() if nxt else "none",
            "attributes": {"days": planning.coming_week(self.planning, get, now), "planning": self.planning,
                           "goal": int(nxt[1].rstrip("%")) if nxt and nxt[1].rstrip("%").isdigit() else None}}

    # v3's own fields that v4 replaced by the planning (plan_settings.GONE): helper -> (platform, key, kind)
    _V3_PLANNING: Final = {
        "input_boolean.hesc_plan_enabled": ("switch", "plan_enabled", "switch"),
        "input_select.hesc_plan_day": ("select", "plan_day", "select"),
        "input_select.hesc_plan_time": ("select", "plan_time", "select"),
        "input_select.hesc_plan_goal": ("select", "plan_goal", "select"),
        "input_datetime.hesc_plan_deadline": ("datetime", "plan_deadline", "datetime"),
        "input_boolean.hesc_vacation": ("switch", "vacation", "switch"),
        "input_datetime.hesc_vacation_until": ("date", "vacation_until", "date"),
        "input_datetime.hesc_rep_skip": ("date", "rep_skip", "date"),
    }

    def _take_over_v3_planning(self) -> None:
        """Decision 2 (31-10 17:25): v3's plan for one day, skipped day and holiday become EV1's planning."""
        v3 = self._v3_states(self._V3_PLANNING)
        now = dt_util.now()
        with self.as_car(model.EV1):
            base = self._getter(self._view())

            def get(eid: str) -> Any:
                v = v3.get(eid)
                return (v["state"], v["attributes"]) if v is not None else base(eid)

            dl = None
            if (v3.get("input_boolean.hesc_plan_enabled") or {}).get("state") == "on":
                dl = dt_util.parse_datetime(str((v3.get("input_datetime.hesc_plan_deadline") or {}).get("state")))
                if dl is None:
                    try:
                        dl = plan.fixed_deadline(str(get("input_select.hesc_plan_day")[0]),
                                                 str(get("input_select.hesc_plan_time")[0]))
                    except (TypeError, ValueError):
                        dl = None
                if dl is not None and dl.tzinfo is None:
                    dl = dl.replace(tzinfo=dt_util.get_default_time_zone())
            self.planning = planning.from_v3(get, now, dl)
            self._save_planning()

    # ---- v4 step 4D: learn the charging power (learn.py) ---------------------------------------
    def _run_learn(self) -> None:
        now = dt_util.now()
        inp = self._round_inputs
        before = self.learn or learn.empty()
        held = self.house_guard.caps.get(self._active) is not None or bool(
            ((self._fleet_over or {}).get("attributes") or {}).get("max_w"))
        grid = bool(self.own_flags.get(OWN_FLAGS[0])) or self.charge_now is not None
        self.learn = learn.step(before, now, inp.ev_power_w if inp is not None else None, grid, held,
                                _float(self.tuning.get("ev_active_w"), 400))
        if self.learn["sessions"] != before.get("sessions"):
            self._save_learn()
        set_kw = _float(self.plan.get("plan_charge_kw"), 11)
        self.plan_kw = learn.plan_kw(self.learn, now, bool(self.plan.get("plan_charge_kw_learn", True)), set_kw,
                                     self.house_connection(), self.plan.get("charger_max_a"))
        self.computed["sensor.hesc_charge_power"] = {
            "state": str(self.plan_kw[0]),
            "attributes": {"source": self.plan_kw[1], "sessions": list(self.learn["sessions"]),
                           "learned": learn.learned_kw(self.learn, now), "set_by_hand": set_kw,
                           "first_estimate": learn.first_estimate(self.house_connection(),
                                                                  self.plan.get("charger_max_a"))}}

    def _run_no_soc(self) -> None:
        """v4 step 4E: a car without a battery-level sensor. With a level entered by hand that level
        plus what was charged since is its battery level; else the plan charges what one charge needs
        (learned, set by hand, the first time half the battery) until the car stops by itself."""
        self.no_soc_over = {}
        if str(self.settings.get(CONF_EV_SOC) or "").strip():
            self.fill, self.soc_entry = None, None
            return
        now = dt_util.now()
        inp = self._round_inputs
        conn = bool(inp is not None and inp.ev_connected)
        before = self.fill or {}
        self.fill = learn.fill_step(before, now, conn, inp.ev_power_w if inp is not None else None,
                                    bool(self.own_flags.get(OWN_FLAGS[0])) or self.charge_now is not None,
                                    _float(self.tuning.get("ev_active_w"), 400))
        if self.fill.get("fills") != before.get("fills"):
            self._save_learn()
        if not conn and (self.soc_entry is not None or self.plan.get("soc_entered")):
            self.soc_entry = None  # counts for one plug-in
            if self.soc_entity is not None and self.soc_entity.hass is not None:
                self.soc_entity.set_from_logic(0)
            else:
                self.plan["soc_entered"] = 0
        plug_kwh = float((self.fill.get("plug") or {}).get("kwh") or 0)
        soc = learn.entered_soc(self.soc_entry, plug_kwh, self.plan.get("ev_battery_kwh")) if conn else None
        info: dict[str, Any]
        if soc is not None:
            self.no_soc_over = {
                learn.SOC_ENTERED_ENTITY: {"state": str(soc), "attributes": {"unit_of_measurement": "%"}},
                "input_text.hesc_ev_soc_sensor": {"state": learn.SOC_ENTERED_ENTITY, "attributes": {}}}
            info = {"battery_level": soc, "source": "entered by hand"}
        else:
            need, src = learn.no_soc_need(self.fill, self.plan.get("no_soc_kwh"), self.plan.get("ev_battery_kwh"))
            self.no_soc_over = {learn.NO_SOC_ENTITY: {"state": "on", "attributes": {"need_kwh": need, "source": src}}}
            info = {"need_kwh": need, "source": src, "full": bool((self.fill.get("plug") or {}).get("full"))}
        cp = self.computed.get("sensor.hesc_charge_power")
        if cp is not None:
            cp["attributes"]["no_battery_sensor"] = {**info, "charged_kwh": round(plug_kwh, 2),
                                                     "fills": list(self.fill.get("fills") or [])}

    def _save_learn(self) -> None:
        text = json.dumps({"sessions": (self.learn or learn.empty())["sessions"],
                           "fills": list((self.fill or {}).get("fills") or [])})
        path = self.learn_path

        async def save() -> None:
            await self.hass.async_add_executor_job(self._write_file, path, text)

        self.config_entry.async_create_task(self.hass, save(), "hesc charge power")

    async def async_load_learn(self, ev: str = model.EV1) -> None:
        with self.as_car(ev):
            path = self.learn_path

        def read() -> Any:
            try:
                return json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                return None

        saved = await self.hass.async_add_executor_job(read)
        if isinstance(saved, dict):
            with self.as_car(ev):
                self.learn = learn.clean(saved)
                self.fill = {"fills": [v for v in (saved.get("fills") or []) if isinstance(v, (int, float))][-5:],
                             "plug": None}

    def change_planning(self, ev: str, fn: Any, *args: Any, **kw: Any) -> None:
        """A HESC action on the car's planning: apply it, save it and run a round."""
        with self.as_car(ev):
            self.planning = fn(self.planning or planning.empty(), *args, **kw)
            self._save_planning()

    def _save_planning(self) -> None:
        text = json.dumps(self.planning)
        path = self.planning_path

        async def save() -> None:
            await self.hass.async_add_executor_job(self._write_file, path, text)

        self.config_entry.async_create_task(self.hass, save(), "hesc planning")

    async def async_load_planning(self, ev: str = model.EV1) -> None:
        with self.as_car(ev):
            path = self.planning_path

        def read() -> Any:
            try:
                return json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                return None

        saved = await self.hass.async_add_executor_job(read)
        if isinstance(saved, dict):
            with self.as_car(ev):
                self.planning = planning.clean(saved)

    def _read_car_inputs(self) -> None:
        cfg, get = self._inputs_cfg_and_getter()
        inputs = read_inputs(get, cfg)
        inputs.forecast_source = self.fc_kind
        self._round_inputs = inputs

    def car_inputs(self, ev: str) -> Inputs | None:
        """The inputs of car `ev` as its last round read them (EV1: the coordinator's data)."""
        if ev == model.EV1:
            return self.data
        with self.as_car(ev):
            return self._round_inputs

    # ---- rc3: charger start level and phase advice -------------------------------------------
    def charger_spec(self) -> charger_specs.StartSpec:
        mode = self._round_inputs.charger_mode if self._round_inputs is not None else None
        return charger_specs.spec_for(self.settings.get(CONF_CHARGER_TYPE), self.settings.get(CONF_CHARGER_ECO_VALUES), mode)

    @property
    def max_ev_w(self) -> float | None:
        return max(self.ev_max_days.values()) if self.ev_max_days else None

    def charger_phases(self) -> int | None:
        """Phases the car charges on: measured by the current control, else from the highest
        charging power seen (never asked)."""
        ph = self.current_ctx.get("phases")
        by_power = charger_specs.phases_from_power(self.max_ev_w)
        if ph:
            measured = int(round(float(ph)))
            return max(measured, by_power or 0)  # more power than one phase can carry means 3 phases
        return by_power

    def advice_floor_w(self) -> float:
        """The lowest start threshold the advice may give: the charger's start level (rc3)."""
        return float(self.charger_spec().start(self.charger_phases()))

    def _run_phase_advice(self) -> None:
        inp = self._round_inputs
        if inp is None:
            return
        ev = inp.ev_power_w
        now = dt_util.now()
        today = now.date().isoformat()
        if ev is not None and 0 < ev <= charger_specs.PLAUSIBLE_MAX_W and ev > self.ev_max_days.get(today, 0.0):
            self.ev_max_days[today] = ev
            cut = (now.date() - timedelta(days=30)).isoformat()
            self.ev_max_days = {k: v for k, v in self.ev_max_days.items() if k >= cut}
        ids = [str(self.settings.get(k) or "").strip() for k in CONF_GRID_POWER_PHASES]
        reader = _Reader(self.hass.states.get)  # real HA states (the phase sensors are the user's own)
        vals = [reader.pw(e) if e else None for e in ids]
        sensors_ok = all(e for e in ids) and all(v is not None for v in vals)
        if sensors_ok and inp.grid_w is not None and abs(inp.grid_w) >= 300:
            # The three phases must add up to the grid power (one way or the other): that also rules
            # out a set of inverter sensors. Majority over the last 20 checks, so a round where the
            # sensors update at different moments cannot flip the sign (review rc3).
            total = sum(vals)  # type: ignore[arg-type]
            for sign in (1, -1):
                if abs(sign * total - inp.grid_w) <= 0.25 * abs(inp.grid_w) + 150:
                    self.phase_votes = (self.phase_votes + [sign])[-20:]
                    break
            else:
                self.phase_votes = (self.phase_votes + [0])[-20:]
            if len(self.phase_votes) >= 5:
                pos, neg = self.phase_votes.count(1), self.phase_votes.count(-1)
                best = 1.0 if pos >= neg else -1.0
                self.phase_sign = best if max(pos, neg) >= 0.7 * len(self.phase_votes) else None
        active = float(self.tuning.get("ev_active_w", 400) or 400)
        charging = ev is None or ev > active  # unknown car power: do not count (review rc3)
        if sensors_ok and self.phase_sign is not None and not charging:
            surplus = [-self.phase_sign * float(v) for v in vals]  # type: ignore[arg-type]
            self.phase_stats.round(now.date(), self.hass.config.latitude, surplus, self.charger_spec())
        # the text only changes with the day (finished days only) or the situation: work it out then
        spec, phases = self.charger_spec(), self.charger_phases()
        key = (today, sensors_ok, phases, spec, len(self.phase_stats.days))
        if key != self._phase_key:
            self._phase_key = key
            done = PhaseStats(days={k: d for k, d in self.phase_stats.days.items() if k < today})
            st, attrs = phase_advice.advice(done, now.date(), self.hass.config.latitude, spec,
                                            sensors_ok=sensors_ok, phases=phases)
            self.computed["sensor.hesc_phase_advice"] = {"state": st, "attributes": attrs}
        # 11-11-2026: the panel also shows the split right now (live), so it needs the sensors and their sign
        pa = self.computed.get("sensor.hesc_phase_advice")
        if pa is not None:
            pa["attributes"]["phase_sensors"] = ids if sensors_ok else []
            pa["attributes"]["phase_sign"] = self.phase_sign
        if self._now_ms() - self._phase_saved_at >= 15 * 60000:
            self._phase_saved_at = self._now_ms()
            self.hass.async_add_executor_job(self._write_file, self.phase_path, self._phase_json())

    def _phase_json(self) -> str:
        data = self.phase_stats.to_json()
        data["ev_max_days"] = self.ev_max_days
        data["phase_votes"] = self.phase_votes
        data["phase_sign"] = self.phase_sign
        return json.dumps(data)

    async def async_save_phase_stats(self) -> None:
        """On unload / HA stop: keep the last minutes of the phase advice (review rc3)."""
        await self.hass.async_add_executor_job(self._write_file, self.phase_path, self._phase_json())

    async def async_load_phase_stats(self) -> None:
        def read() -> Any:
            try:
                return json.loads(self.phase_path.read_text("utf-8"))
            except (OSError, ValueError):
                return None

        data = await self.hass.async_add_executor_job(read)
        self.phase_stats = PhaseStats.from_json(data)
        if isinstance(data, dict):
            days = data.get("ev_max_days")
            if isinstance(days, dict):
                self.ev_max_days = {str(k): float(v) for k, v in days.items() if isinstance(v, (int, float))}
            votes = data.get("phase_votes")
            if isinstance(votes, list):
                self.phase_votes = [int(v) for v in votes if v in (-1, 0, 1)][-20:]
            if data.get("phase_sign") in (1, -1, 1.0, -1.0):
                self.phase_sign = float(data["phase_sign"])
        self._phase_saved_at = self._now_ms()

    def _run_compare(self) -> None:
        """What v2 really shows next to what v3 would show; only reads v2."""
        def v2(eid: str, attr: str | None = None) -> Any:
            s = self.hass.states.get(eid)
            if s is None or s.state in ("unavailable",):
                return None
            return s.attributes.get(attr) if attr else s.state

        def v3c(eid: str, attr: str | None = None) -> Any:
            st = self.computed.get(eid) or {}
            return (st.get("attributes") or {}).get(attr) if attr else st.get("state")

        pub = self.published.get
        soc2 = v2("sensor.hesc_ev_soc")
        values = {
            "solar": (v2("input_text.hesc_state"), pub("input_text.hesc_state", ""),
                      v2("input_text.hesc_reason"), pub("input_text.hesc_reason", "")),
            "charge_plan": (v2("input_text.hesc_plan_status"), pub("input_text.hesc_plan_status", ""), None, None),
            "plan_quarters": (compare.plan_key(v2("sensor.hesc_charge_plan", "plan")) if v2("sensor.hesc_charge_plan") is not None else None,
                              compare.plan_key(v3c("sensor.hesc_charge_plan", "plan")), None, None),
            "kickstart": (v2("input_text.hesc_kick_status"), pub("input_text.hesc_kick_status", ""), None, None),
            "battery_level": (None if soc2 is None else f"{soc2} ({v2('sensor.hesc_ev_soc', 'source')})",
                              f"{v3c('sensor.hesc_ev_soc')} ({v3c('sensor.hesc_ev_soc', 'source')})", None, None),
            "notice": (v2("sensor.hesc_notice"), v3c("sensor.hesc_notice"), None, None),
        }
        now = dt_util.now()
        lines = self.compare.round(now.isoformat(timespec="seconds"), now.date().isoformat(), values)
        st, attrs = self.compare.sensor()
        self.computed["sensor.hesc_compare"] = {"state": st, "attributes": attrs}
        if lines:
            text = "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lines)
            new_day = any(x.get("type") == "day" for x in lines)
            self.hass.async_add_executor_job(self._append_compare, text, now.date().isoformat() if new_day else None)

    def _append_compare(self, text: str, trim_for: str | None) -> None:
        path = self.data_dir / "compare_log.jsonl"
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as f:
                f.write(text)
            if trim_for:  # once a day: keep about 30 days
                kept = compare.trim(path.read_text(encoding="utf-8").splitlines(), trim_for)
                self._write_file(path, "".join(ln + "\n" for ln in kept))
        except OSError as err:
            _LOGGER.warning("HESC v4 could not write %s: %s", path, err)

    def setup_values(self) -> dict[str, str]:
        """The setup-screen choices under v2's helper names (object id -> state text), for the dashboard."""
        over = self._overrides()
        helpers = [*_TEXT_HELPERS.values(), *_BOOL_HELPERS.values(), "input_text.hesc_pv_power_sensor",
                   "input_text.hesc_grid_power_sensor"]
        out = {h.split(".", 1)[1]: over[h]["state"] for h in helpers if h in over}
        out["hesc_charger_type"] = str(self.settings.get(CONF_CHARGER_TYPE) or "Not chosen")
        out["hesc_use_hpvc_sources"] = "on" if self.settings.get(CONF_USE_HPVC_SOURCES) else "off"
        # since rc3: grid power per phase for the Live card (empty when not chosen)
        for i, key in enumerate(CONF_GRID_POWER_PHASES, 1):
            out[f"hesc_grid_power_phase_{i}"] = str(self.settings.get(key) or "")
        return out

    @callback
    def update_charger_profile(self, _now: Any = None) -> None:
        """v2 template "HESC charger profile" (at start; v3 changes the charger type in its setup screen)."""
        import dataclasses

        from .profile import charger_profile

        ctype = str(self.settings.get(CONF_CHARGER_TYPE) or "Not chosen")
        p = charger_profile(self.hass, ctype)
        prof = dataclasses.asdict(p) if p.known else {"type": p.type, "known": False}
        self.computed["sensor.hesc_charger_profile"] = {"state": ctype, "attributes": {"profile": prof}}
        self.async_update_listeners()

    def _run_dashboard_templates(self) -> None:
        """v2's dashboard template sensors: diagnostics, checks, notification phones."""
        setup = self.setup_values()
        # v4 step 5: Grid Clock sensors found, for the first start (zone and the price of now)
        found = self._gc_found = prices.grid_clock_candidates(self.hass.states.async_all("sensor"))
        self._action_found = None
        for c in found:
            st = self.hass.states.get(c["current_price_entity"])
            c["now_ct_kwh"] = st.state if st is not None else None
        from .setup_wizard import setup_done

        entry = self.config_entry
        setup = {**setup, "grid_clock_sensors": found, "exports": dict(self.exports),
                 "setup_done": setup_done(entry.options or entry.data)}  # 01-11: the first start in the panel
        self.computed["sensor.hesc_setup"] = {"state": "ok", "attributes": setup}
        # v4 08-11 (opmaakchat 10:08): per car the same names, read as that car (EV2's own charger)
        self.computed["sensor.hesc_car_setup"] = {"state": "ok", "attributes": dict(setup)}
        for ev in self.ev_ids():
            if ev != self._active:
                with self.as_car(ev):
                    self.computed["sensor.hesc_car_setup"] = {"state": "ok", "attributes": self.setup_values()}
        for h in ("hesc_standalone", "hesc_use_hpvc_sources", "hesc_use_irradiance"):
            # mirrors for the dashboard only (the logic reads its own overrides, not these)
            self.computed["input_boolean." + h] = {"state": setup[h], "attributes": {}}
        get = self._getter(self._view())
        for eid, fn in diag_templates.DIAG.items():
            self.computed[eid] = {"state": fn(get), "attributes": {}}
        for eid, cfn in diag_templates.CHECKS.items():
            st, attrs = cfn(get)
            self.computed[eid] = {"state": st, "attributes": attrs}
        st, attrs = diag_templates.notification_phones(get, diag_templates.mobile_app_devices(self.hass))
        self.computed["sensor.hesc_notification_phones"] = {"state": st, "attributes": attrs}

    def _apply_solar(self, res: Result) -> None:
        self.context = res.context
        self.last_result = res
        for msg in res.status:
            p = msg["payload"]
            for eid in p["target"]["entity_id"]:
                self.published[eid] = p["data"].get("value", "")
        for msg in res.hpvc + res.ownership:
            self._command(msg["payload"])
        del self.would_do[:-20]
        if res.history:
            self._history(res.history)

    # ---- commands (v2's output nodes) ------------------------------------------------
    def car_controlled(self) -> bool:
        """v4 08-11 (decision 08:43): HESC controls the car it works for now, and its charger. A shared charger
        follows the car on it: a car that is off leaves the charger alone while it is plugged in."""
        return self.plan.get("car_controlled", True) is not False

    def _command(self, p: dict[str, Any]) -> None:
        """One command of the ported logic: an action message (v2 "HA actions", "Ownership flag",
        "Publish status" for notifications) or an HA API post (v2 "notify" via the API node).
        Kept in would_do; sent only with shadow mode off, one after the other in the given order."""
        self.would_do.append(p)
        own = {str(self.settings.get(k) or "").strip() for k in (CONF_CHARGER_START_STOP, CONF_CHARGER_RESUME)}
        if own & set(((p.get("target") or {}).get("entity_id")) or []):
            self.plan_flow["hescOwnCmd"] = dt_util.now().timestamp()  # v4 08-11: HESC switched the charger itself
        if (self.shadow or not self.car_controlled()) and not p.get("restore_own_change"):
            return  # rc3: only "put HESC's own change back" (current.py) passes in shadow mode
        if "path" in p:  # {"protocol": "http", "method": "post", "path": "/api/services/<d>/<s>", "data": ...}
            path = str(p.get("path") or "")
            if not (p.get("method") == "post" and path.startswith("/api/services/") and path.count("/") == 4):
                return
            dom, svc = path[len("/api/services/"):].split("/")
            target = None
        else:
            action = str(p.get("action") or "")
            if "." not in action:
                return
            dom, svc = action.split(".", 1)
            target = p.get("target")
        data = dict(p.get("data") or {})
        if dom == "persistent_notification" and data.get("notification_id") == "hesc_charge_plan":
            # v2 in shadow mode still writes its own: v3 gets its own id
            data["notification_id"] = "hesc_v4_charge_plan"
        if dom in ("notify", "persistent_notification"):
            # 3.1.0: what a person reads comes in Home Assistant's language (the logic stays English)
            for k in ("title", "message"):
                if isinstance(data.get(k), str):
                    data[k] = texts.translate(data[k], self.hass.config.language)
        if target is not None and (not isinstance(target, dict) or set(target) - {"entity_id"}):
            _LOGGER.warning("HESC v4 skipped %s.%s: target %s is not a list of entities", dom, svc, target)
            return

        def entities(v: Any) -> list[str]:
            return [v] if isinstance(v, str) else list(v or [])

        ids = entities((target or {}).get("entity_id")) + entities(data.pop("entity_id", None))
        for eid in ids:
            if eid in self.own_flags and svc in ("turn_on", "turn_off"):
                on = svc == "turn_on"
                if self.own_flags[eid] != on:
                    self.own_flags[eid] = on
                    self._save_flags()
        # never v2's own helpers (v2 is left alone); the own flags are kept above
        kept = [e for e in ids if not _V2_HELPER.match(e)]
        if ids and not kept:
            return
        # hard rule (decision 30-10-2026): never an installer or house setting (safety.py)
        currents = [str((ch or {}).get(CONF_CHARGER_CURRENT) or "")
                    for ch in (model.ensure_nested(self.config_entry.options or self.config_entry.data)["chargers"] or {}).values()]
        kept, refused = safety.allowed_targets(dom, kept, currents)
        if refused:
            _LOGGER.warning("HESC v4 never writes installer or house settings: %s.%s on %s refused", dom, svc, ", ".join(refused))
            if not kept:
                return
        if HPVC_REQUEST in kept and svc in ("turn_on", "turn_off"):
            # v4: one HPVC for the house. With two cars its release lasts while one of them asks for it.
            self._hpvc_want[self._active] = svc == "turn_on"
            if svc == "turn_off" and any(w for e, w in self._hpvc_want.items() if e != self._active):
                kept = [e for e in kept if e != HPVC_REQUEST]
                if not kept:
                    return
        self._commands.append((dom, svc, data, {"entity_id": kept} if kept else None))
        if not self._sending:
            self._sending = True
            self.config_entry.async_create_task(self.hass, self._send_all(), "hesc commands")

    async def _send_all(self) -> None:
        """Send the queued commands one by one, in order. A failing or hanging action is logged and
        the next one goes on (like a Node-RED action node)."""
        try:
            while self._commands:
                dom, svc, data, target = self._commands.pop(0)
                try:
                    async with asyncio.timeout(COMMAND_TIMEOUT):
                        await self.hass.services.async_call(dom, svc, data, blocking=True, target=target)
                except Exception as err:  # noqa: BLE001
                    _LOGGER.warning("HESC v4 could not call %s.%s %s: %s", dom, svc, target or "", err or type(err).__name__)
        finally:
            self._sending = False

    def _save_flags(self) -> None:
        text = json.dumps(self.own_flags)
        path = self.flags_path

        async def save() -> None:
            await self.hass.async_add_executor_job(self._write_file, path, text)

        self.config_entry.async_create_task(self.hass, save(), "hesc own flags")

    async def async_load_current(self, ev: str = model.EV1) -> None:
        """The charging current from before HESC lowered it (survives a restart)."""
        with self.as_car(ev):
            path = self.current_path

        def read() -> dict[str, Any]:
            try:
                d = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                return {}
            return d if isinstance(d, dict) else {}

        data = await self.hass.async_add_executor_job(read)
        with self.as_car(ev):
            if data.get("saved") is not None:
                self.current_ctx["saved"] = data["saved"]
            # phases measured before 3.0.0 may be too low (measured while charging on sun): only keep v2 measurements
            if data.get("phases") is not None and data.get("phases_v") == 2:
                self.current_ctx["phases"] = data["phases"]

    async def async_restore_current(self, ev: str = model.EV1) -> None:
        """On unload: put the charging current back (rc3: also in shadow mode, it is HESC's own change)."""
        with self.as_car(ev):
            saved = self.current_ctx.get("saved")
            ent = str(self.settings.get(CONF_CHARGER_CURRENT) or "")
            path = self.current_path
        if saved is None or not ent:  # rc3: HESC's own change is put back in shadow mode too
            return
        try:
            await self.hass.services.async_call("number", "set_value", {"entity_id": ent, "value": saved}, blocking=True)
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("HESC v4 could not put the charging current back to %s A: %s", saved, err)
            return
        with self.as_car(ev):
            self.current_ctx.pop("saved", None)
            text = json.dumps({"saved": None, "phases": self.current_ctx.get("phases"), "phases_v": 2})
        await self.hass.async_add_executor_job(self._write_file, path, text)

    async def async_load_flags(self, ev: str = model.EV1) -> None:
        with self.as_car(ev):
            path = self.flags_path

        def read() -> dict[str, Any]:
            try:
                return json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                return {}

        saved = await self.hass.async_add_executor_job(read)
        with self.as_car(ev):
            for eid in OWN_FLAGS:
                if isinstance(saved, dict) and isinstance(saved.get(eid), bool):
                    self.own_flags[eid] = saved[eid]

    def _history(self, msgs: list[dict[str, Any]]) -> None:
        lines = "".join(m["payload"] + "\n" for m in msgs)
        self.hass.async_add_executor_job(self._append_history, lines, self.history_path)

    # ---- prices, plan, cost (v2 template sensors) ------------------------------------
    def _run_plan_templates(self) -> None:
        get = self._getter(self._view())
        self._maybe_fetch(get)
        p = prices.adapt(get, self.fetch_rows, self.fetch_div)
        st, attrs = prices.sensor(get, p)
        self.computed["sensor.hesc_prices"] = {"state": st, "attributes": attrs}
        get = self._getter(self._view())
        st, attrs = plan.sensor(get)
        if self.charge_now is None and self.charge_now_wish is not None:
            self._start_waiting_charge_now()
        if self.charge_now is not None:
            st, attrs = self._apply_charge_now(get, st, attrs)
        self.computed["sensor.hesc_charge_plan"] = {"state": st, "attributes": attrs}
        get = self._getter(self._view())
        # 3.1.0: v2's "display" showed the previous amount (this.state) and lagged one update behind;
        # the plan card now shows it next to the price, so it shows the amount just worked out
        st, _ = plan.planned_cost(get, None)
        st, attrs = plan.planned_cost(get, st)
        self.computed["sensor.hesc_expected_charge_cost"] = {"state": st, "attributes": attrs}

    # ---- since 3.0.0: charge now to a goal (charge_now.py) ----------------------------
    def _apply_charge_now(self, get: Any, st: str, attrs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        cn = self.charge_now
        raw = attrs.get("plan")
        try:
            p = json.loads(raw) if isinstance(raw, str) else None
        except ValueError:
            p = None
        now = dt_util.now()
        if self.shadow:
            self.end_charge_now("shadow mode on")
            return st, attrs
        why = charge_now.finished(cn["goal"], (p or {}).get("soc"), self._ev_plug_reported(get), cn["until"], now)
        if why is not None:
            self.end_charge_now(why)
            return st, attrs
        if not isinstance(p, dict):
            return st, attrs
        pr = (self.computed.get("sensor.hesc_prices") or {}).get("attributes") or {}
        rows = list(pr.get("raw_today") or []) + list(pr.get("raw_tomorrow") or [])
        cap = _float((get("input_number.hesc_ev_battery_kwh") or ("",))[0], 0)
        newp = charge_now.override(p, cn["goal"], cn["until"], now, cap, rows)
        return newp["deadline"], {"plan": plan._tojson(newp)}

    def _ev_plug_reported(self, get: Any) -> bool | None:
        """Plugged in as the connection sensor reports it; None while the sensor is unavailable or
        missing (a cloud charger dropping out, or just after a restart): that is no unplug."""
        eid = str((get("input_text.hesc_ev_connected_sensor") or ("",))[0] or "").strip()
        st = self.hass.states.get(eid) if eid else None
        if st is None or st.state in ("unavailable", "unknown", ""):
            return None
        return self._round_inputs.ev_connected if self._round_inputs is not None else None

    def _grid_charging_set_up(self, get: Any) -> bool:
        """charge_plan's method is not "Off": a start/stop switch, or a mode entity with a grid value."""
        def txt(e: str) -> str:
            return str((get(e) or ("",))[0] or "").strip()
        return bool(txt("input_text.hesc_charger_start_stop_entity")
                    or (txt("input_text.hesc_charger_grid_mode_value") and txt("input_text.hesc_charger_mode_entity")))

    def start_charge_now(self, goal: int) -> None:
        """Choose "charge now to `goal` %". Decision 06-11-2026 13:23: the choice is kept, with or
        without the EV plugged in; charging starts as soon as the EV is plugged in, its battery level is
        known and it is more than 3 % below the goal (until then the select shows the goal, attribute
        `waiting`). Refused (ServiceValidationError) only in shadow mode or when grid charging is not set up."""
        from homeassistant.exceptions import ServiceValidationError

        def refuse(key: str, **ph: Any) -> ServiceValidationError:
            return ServiceValidationError(translation_domain=DOMAIN, translation_key=key,
                                          translation_placeholders={k: str(v) for k, v in ph.items()} or None)

        if self.shadow:
            raise refuse("charge_now_shadow")
        now_state = self._charge_now_state()  # before the view: building it can swap the car state
        if not self._grid_charging_set_up(self._getter(self._view())):
            raise refuse("grid_not_set_up")
        self.end_charge_now("new goal chosen", show_off=False)
        self.charge_now_wish = int(goal)
        if not self._start_waiting_charge_now(now_state):
            _LOGGER.info("HESC v4 charge now to %s%%: waiting until the EV is plugged in and below it", goal)
            if self.charge_now_entity is not None and self.charge_now_entity.hass is not None:
                self.charge_now_entity.set_from_logic(f"{int(goal)}%", None, waiting=True)
        self.config_entry.async_create_task(self.hass, self.async_request_refresh(), "hesc charge now")

    def _charge_now_state(self) -> tuple[bool, float]:
        """(EV plugged in, battery level or NaN) of this car's last round."""
        connected = self._round_inputs is not None and bool(self._round_inputs.ev_connected)
        return connected, _float((self.computed.get("sensor.hesc_ev_soc") or {}).get("state"), math.nan)

    def _start_waiting_charge_now(self, now_state: tuple[bool, float] | None = None) -> bool:
        """Start the chosen "charge now" when it can: EV plugged in, battery level known, below the goal."""
        goal = self.charge_now_wish
        connected, soc = now_state or self._charge_now_state()
        if goal is None or self.shadow or not connected:
            return False
        if math.isnan(soc) or soc >= goal - charge_now.MARGIN:
            return False
        get = self._getter(self._view())
        cap = _float((get("input_number.hesc_ev_battery_kwh") or ("",))[0], 60)
        kw = _float((get("input_number.hesc_plan_charge_kw") or ("",))[0], 11)
        until = charge_now.end_time(dt_util.now(), soc, goal, cap, kw)
        self.charge_now = {"goal": int(goal), "until": until}
        self.charge_now_wish = None
        _LOGGER.info("HESC v4 charge now to %s%% (gives up at %s)", goal, until)
        if self.charge_now_entity is not None and self.charge_now_entity.hass is not None:
            self.charge_now_entity.set_from_logic(f"{int(goal)}%", until)
        return True

    def end_charge_now(self, why: str, show_off: bool = True) -> None:
        if why == "switched off":
            self.charge_now_wish = None  # a waiting choice is switched off too
            if self.charge_now is None and show_off and self.charge_now_entity is not None \
                    and self.charge_now_entity.hass is not None:
                self.charge_now_entity.set_from_logic(charge_now.OFF, None)
        if self.charge_now is None:
            return
        until_ms = self.charge_now["until"].timestamp() * 1000
        self.charge_now = None
        # ended early: the goal check the plan control set for the give-up time is not wanted any more
        # (else "EV goal missed" for a goal nobody asked for, once that time comes)
        x = self.plan_flow.get("hescPlan")
        if why != "end time passed" and isinstance(x, dict) and isinstance(x.get("checkDl"), (int, float)) \
                and abs(x["checkDl"] - until_ms) < 1000:
            x["checkDone"] = True
        _LOGGER.info("HESC v4 charge now ended: %s", why)
        if show_off and self.charge_now_entity is not None and self.charge_now_entity.hass is not None:
            self.charge_now_entity.set_from_logic(charge_now.OFF, None)

    # ---- since 3.0.0: phone widgets refresh (phone.py) --------------------------------
    def _phone_widgets(self) -> None:
        soc = (self.computed.get("sensor.hesc_ev_soc") or {}).get("state")
        plan_raw = ((self.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
        conn = self._round_inputs.ev_connected if self._round_inputs is not None else None
        text, attrs = phone.summary(soc, plan_raw, self.published.get("input_text.hesc_state"), dt_util.utcnow(),
                                    plan_status=self.published.get("input_text.hesc_plan_status"), plugged_in=conn)
        if self.widget_push is None:
            self.widget_push = phone.WidgetPush()
        if not self.widget_push.due(phone.widget_key(text, attrs), dt_util.utcnow()):
            return
        for target in phone.phones(self.plan.get("notify_services"), phone.apple_devices(self.hass)):
            self._command({"action": target, "data": {"message": phone.MESSAGE}})

    def _run_charge_plan(self, view: StatesView) -> None:
        r = charge_plan.run(view, self.plan_flow, self._now_ms())
        self.plan_flow = r.flow
        for msg in r.status:
            p = msg["payload"]
            if p.get("action") == "input_text.set_value":
                for eid in p["target"]["entity_id"]:
                    self.published[eid] = p["data"].get("value", "")
            else:
                self._command(p)  # ownership flag and notifications
        for msg in r.actions:
            self._command(msg["payload"])
        del self.would_do[:-20]
        if r.history:
            self._history(r.history)

    # ---- EV battery level with fallbacks --------------------------------------------
    async def async_load_soc_plugins(self, ev: str = model.EV1) -> None:
        """v2 "Load plug-in battery levels" (30 s after start): own file, else v3's file (EV1 only)."""
        import json

        with self.as_car(ev):
            own = self.soc_path
        paths = (own, Path(self.hass.config.path(*V2_SOC_PLUGINS))) if ev == model.EV1 else (own,)
        for path in paths:
            try:
                text = await self.hass.async_add_executor_job(path.read_text, "utf-8")
            except FileNotFoundError:
                continue
            except OSError as err:
                # not "no file": keep the battery level off, so the file is never overwritten with an empty log
                _LOGGER.error("HESC v4 could not read %s, own battery level is off: %s", path, err)
                with self.as_car(ev):
                    self.soc_blocked = True
                return
            log, state = [], None
            try:
                j = json.loads(text or "{}")
                if isinstance(j, dict) and isinstance(j.get("plugins"), list):
                    log = j["plugins"]
                if isinstance(j, dict) and isinstance(j.get("state"), dict):
                    state = j["state"]
            except ValueError:
                _LOGGER.warning("HESC v4: %s unreadable, starting empty", path)
            with self.as_car(ev):
                self.soc_flow["hescSocState"] = state
                self.soc_flow["hescSocLog"] = log
            return

    async def async_load_costs(self, ev: str = model.EV1) -> None:
        """v2 "Load charging costs" (35 s after start): own file, else v3's file (read only, EV1 only),
        else empty."""
        text = None
        with self.as_car(ev):
            own = self.costs_path
        paths = (own, Path(self.hass.config.path(*V2_COSTS))) if ev == model.EV1 else (own,)
        for path in paths:
            try:
                text = await self.hass.async_add_executor_job(path.read_text, "utf-8")
                break
            except FileNotFoundError:
                continue
            except OSError as err:
                # not "no file": keep counting off, so the file is never overwritten with an empty history
                _LOGGER.error("HESC v4 could not read %s, charging costs are not counted: %s", path, err)
                return
        with self.as_car(ev):
            self.costs = costs.load(text)

    def _run_costs(self) -> None:
        r = costs.run(self._view(), self.costs, self.costs_context, self._now_ms(), self.hass.config.time_zone)
        self.costs_context = r.context
        if not r.ran:
            return
        self.costs = r.costs
        if r.publish is not None:
            self.computed["sensor.hesc_charging_costs"] = r.publish
        if r.save is not None:
            self.hass.async_add_executor_job(self._write_file, self.costs_path, r.save)

    async def async_export_costs(self, ev: str = model.EV1) -> None:
        """v2 "Export charging costs (CSV)": two CSV files in v3's own folder. v4: per car; EV1 keeps
        v3's file names, EV2 gets charging_costs_days_ev2.csv (decision 31-10-2026 20:34)."""
        with self.as_car(ev):
            files, info = costs.export(self._view(), self.costs, self._now_ms(), folder=DOMAIN)
        for name, text in files:
            own = cars.file_name(name, ev)
            info = info.replace(name, own)
            if not await self.hass.async_add_executor_job(self._write_file, self.data_dir / own, text):
                raise HomeAssistantError(f"Could not write {self.data_dir / own}")
        with self.as_car(ev):
            self.published["input_text.hesc_costs_export_info"] = info
        self.async_update_listeners()

    async def async_morning_summary(self, _now: Any = None) -> None:
        """v2 "Morning summary" (every minute): at the chosen time, the summary for the phones.
        Sent only with shadow mode off (v2 sends it in shadow mode too; v3 never does).
        v4: one summary per car, at that car's time, to that car's phones (decision 31-10 06:51)."""
        for ev in self.ev_ids():
            await self._morning_summary(ev)

    async def _morning_summary(self, ev: str) -> None:
        try:
            with self.as_car(ev):
                view = self._view()
                fire, self.morning_context = morning.due(view, self.morning_context, self._now_ms())
                path = self.history_path
            if not fire:
                return
            try:
                text = await self.hass.async_add_executor_job(path.read_text, "utf-8")
            except OSError:
                return  # no history file yet: v2's "Read history" fails and nothing is sent
            with self.as_car(ev):
                services, message = morning.summary(self._view(), text, self._now_ms())
        except Exception:
            _LOGGER.exception("HESC v4 morning summary failed")
            return
        if message is not None:
            with self.as_car(ev):
                for msg in morning.messages(services, message):
                    self._command(msg["payload"])
            del self.would_do[:-20]

    # ---- settings back-up / restore / standard values -------------------------------
    def _own_settings_view(self) -> tuple[dict[str, dict[str, Any]], dict[str, tuple[str, str, str]]]:
        """v3's own settings under v2's helper ids, and helper id -> (platform, key, kind)."""
        view: dict[str, dict[str, Any]] = {}
        where: dict[str, tuple[str, str, str]] = {}
        for spec in NUMBERS:
            view[spec.helper] = {"state": str(float(self.tuning[spec.key])), "attributes": {}}
            where[spec.helper] = ("number", spec.key, "number")
        for sw in SWITCHES:
            view[sw.helper] = {"state": "on" if self.switches[sw.key] else "off", "attributes": {}}
            where[sw.helper] = ("switch", sw.key, "switch")
        own = self._own_plan_overrides()
        for spec in SETTINGS:
            st = dict(own[spec.helper])
            if spec.kind == "select":
                st["attributes"] = {"options": list(spec.options)}
            view[spec.helper] = st
            where[spec.helper] = ({"switch": "switch", "number": "number", "select": "select", "text": "text",
                                   "datetime": "datetime", "date": "date"}[spec.kind], spec.key, spec.kind)
        return view, where

    async def async_apply_first_values(self) -> None:
        """v4 first start (config_flow.FIRST_VALUES): the answers that live in HESC's own entities (house
        connection, battery, the charger's maximum, taking turns, prices) are set on those entities once,
        then removed from the entry. Per owner: "shared", a car ("ev2") or a charger ("charger2"); a
        charger's entities belong to the first car on it."""
        from homeassistant.helpers import entity_registry as er

        from .config_flow import FIRST_VALUES

        entry = self.config_entry
        current = model.ensure_nested(entry.options or entry.data)
        pending = current["shared"].get(FIRST_VALUES)
        if not isinstance(pending, dict) or not pending:
            return
        reg = er.async_get(self.hass)
        evs = self.ev_ids()
        for owner, values in pending.items():
            if owner in model.EVS:
                ev = owner
            elif owner in model.CHARGERS:
                ev = next((e for e in evs if model.charger_of(self.nested, e) == owner), model.EV1)
            else:
                ev = model.EV1
            for key, value in (values or {}).items():
                spec = BY_KEY.get(key)
                if spec is None:
                    continue
                platform = spec.kind
                eid = reg.async_get_entity_id(platform, DOMAIN, model.unique_id(
                    entry.entry_id, key, ev, model.charger_of(self.nested, ev)))
                if eid is None:
                    _LOGGER.warning("HESC v4 first start: no entity for %s (%s)", key, owner)
                    continue
                data: dict[str, Any] = {"entity_id": eid}
                if platform == "switch":
                    service = "turn_on" if value else "turn_off"
                elif platform == "select":
                    service, data["option"] = "select_option", str(value)
                elif platform in ("number", "text"):
                    service, data["value"] = "set_value", value
                else:
                    continue
                try:
                    await self.hass.services.async_call(platform, service, data, blocking=True)
                except (HomeAssistantError, ValueError) as err:
                    _LOGGER.warning("HESC v4 first start: could not set %s: %s", eid, err)
        current = model.ensure_nested(entry.options or entry.data)
        current["shared"].pop(FIRST_VALUES, None)
        if entry.options:
            self.hass.config_entries.async_update_entry(entry, options=current)
        else:
            self.hass.config_entries.async_update_entry(entry, data=current)
        self.async_update_listeners()

    async def _apply_setting_actions(self, acts: list[dict[str, Any]], where: dict[str, tuple[str, str, str]]) -> None:
        from homeassistant.helpers import entity_registry as er

        entreg = er.async_get(self.hass)
        for a in acts:
            p = a["payload"]
            target = p["target"]["entity_id"]
            if target == settings_backup.INFO:
                self.published[target] = p["data"]["value"]
                continue
            platform, key, kind = where[target]
            eid = entreg.async_get_entity_id(platform, DOMAIN, model.unique_id(
                self.config_entry.entry_id, key, self._active, model.charger_of(self.nested, self._active)))
            if eid is None:
                continue
            action = p["action"].split(".")[1]
            data: dict[str, Any] = {"entity_id": eid}
            if kind == "number":
                v = p["data"]["value"]
                if not (isinstance(v, (int, float)) and math.isfinite(v)):
                    _LOGGER.warning("HESC v4 restore: %s skipped, %r is not a number", eid, v)
                    continue
                service, data["value"] = "set_value", v
            elif kind == "text":
                service, data["value"] = "set_value", p["data"]["value"]
            elif kind == "switch":
                service = action
            elif kind == "select":
                service, data["option"] = "select_option", p["data"]["option"]
            elif kind == "datetime":
                dt = dt_util.parse_datetime(p["data"]["datetime"])
                if dt is None:
                    continue
                service, data["datetime"] = "set_value", dt if dt.tzinfo else dt.replace(tzinfo=dt_util.get_default_time_zone())
            else:  # date
                service, data["date"] = "set_value", str(p["data"]["datetime"])[:10]
            try:
                await self.hass.services.async_call(platform, service, data, blocking=True)
            except (HomeAssistantError, ValueError) as err:
                _LOGGER.warning("HESC v4 could not restore %s: %s", eid, err)
        self.async_update_listeners()

    async def async_set_own_text(self, key: str, value: str, ev: str = model.EV1) -> None:
        """Set one of v3's own text settings through its entity (so the entity shows it at once).
        v4: the entity of car `ev` when it is a car's setting (e.g. its phones)."""
        from homeassistant.helpers import entity_registry as er

        uid = model.unique_id(self.config_entry.entry_id, key, ev, model.charger_of(self.nested, ev))
        eid = er.async_get(self.hass).async_get_entity_id("text", DOMAIN, uid)
        if eid is None:
            with self.as_car(ev):
                self.plan[key] = value
            return
        await self.hass.services.async_call("text", "set_value", {"entity_id": eid, "value": value}, blocking=True)

    async def async_notify_test(self) -> None:
        """v2 automation "Notification phones: send a test", on v3's own phone list."""
        if self.shadow:
            raise HomeAssistantError("Shadow mode is on: HESC v4 sends no notifications")
        targets = [x.strip() for x in str(self.plan.get("notify_services") or "").split(",")]
        targets = [x for x in targets if x.startswith("notify.")]
        if not targets:
            lang = self.hass.config.language
            await self.hass.services.async_call("persistent_notification", "create", {
                "title": texts.translate("HESC test", lang),
                "message": texts.translate("No phone chosen yet: HESC notifications only appear inside Home Assistant.", lang)})
            return
        for t in targets:
            try:
                lang = self.hass.config.language
                await self.hass.services.async_call("notify", t.split(".", 1)[1], {
                    "title": texts.translate("HESC test", lang),
                    "message": texts.translate("This phone gets the notifications from Home EV Solar Control.", lang)})
            except Exception as err:  # noqa: BLE001 - continue_on_error, like v2
                _LOGGER.warning("HESC v4 test notification to %s failed: %s", t, err)

    async def async_settings_button(self, which: str) -> None:
        """v2 "Settings back-up / restore / reset" on v3's own settings (files in /config/hesc_v4)."""
        view, where = self._own_settings_view()
        now, tz = self._now_ms(), self.hass.config.time_zone
        if which == "backup":
            files, acts = settings_backup.press_backup(view, now, tz)
        elif which == "reset":
            files, acts = settings_backup.reset(view, now, tz)
        else:
            files = []
            path = self.data_dir / "settings_backup.json"
            try:
                text = await self.hass.async_add_executor_job(path.read_text, "utf-8")
            except FileNotFoundError:
                text = None
            except OSError as err:
                raise HomeAssistantError(f"Could not read {path}: {err}") from err
            acts = settings_backup.restore(view, text, now, tz)
        for name, text in files:
            if not await self.hass.async_add_executor_job(self._write_file, self.data_dir / name, text):
                raise HomeAssistantError(f"Could not write {self.data_dir / name}")
        if files:
            await self.async_refresh_backup_meta()
        await self._apply_setting_actions(acts, where)

    # ---- v4 step 8: report and back-up in three forms (export.py) ----------------------------------
    async def _share_ids(self) -> dict[str, str]:
        """A fixed random code per car for the shared forms (never derived from a name or an id)."""
        import secrets

        path = self.data_dir / "share_ids.json"

        def read() -> dict[str, str]:
            try:
                d = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                d = {}
            return d if isinstance(d, dict) else {}

        ids = await self.hass.async_add_executor_job(read)
        changed = False
        for ev in self.ev_ids():
            if not ids.get(ev):
                ids[ev] = "CAR-" + secrets.token_hex(3).upper()
                changed = True
        if changed:
            await self.hass.async_add_executor_job(self._write_file, path, json.dumps(ids))
        return ids

    async def _export_data(self) -> dict[str, Any]:
        from homeassistant.const import __version__ as ha_version

        data: dict[str, Any] = {k: {} for k in ("setup", "settings", "planning", "learn", "status", "decisions",
                                                "missing", "names")}
        paths = {}
        for ev in self.ev_ids():
            with self.as_car(ev):
                flat = model.flatten(self.config_entry.options or self.config_entry.data, ev)
                data["setup"][ev] = {k: v for k, v in flat.items() if isinstance(v, (str, int, float, bool)) or v is None}
                view, _where = self._own_settings_view()
                data["settings"][ev] = settings_backup.collect(view)
                data["planning"][ev] = self.planning
                data["learn"][ev] = {"sessions": list((self.learn or {}).get("sessions") or []),
                                     "fills": list((self.fill or {}).get("fills") or [])}
                inp = self._round_inputs
                cw = self.computed.get("sensor.hesc_coming_week") or {}
                data["status"][ev] = {
                    "state": self.published.get("input_text.hesc_state"), "reason": self.published.get("input_text.hesc_reason"),
                    "plan_status": self.published.get("input_text.hesc_plan_status"),
                    "connected": inp.ev_connected if inp is not None else None,
                    "next_ready_by": cw.get("state"), "charging_power_kw": (self.plan_kw or (None,))[0]}
                data["missing"][ev] = list(getattr(inp, "missing", []) or []) if inp is not None else []
                data["names"][ev] = model.ev_name(self.nested, ev)
                paths[ev] = self.history_path

        def tail() -> dict[str, list[str]]:
            out = {}
            for ev, path in paths.items():
                try:
                    lines = path.read_text("utf-8").splitlines()[-200:]
                except OSError:
                    lines = []
                rows = []
                for ln in lines:
                    try:
                        d = json.loads(ln)
                    except ValueError:
                        continue
                    if not isinstance(d, dict):
                        continue
                    what = d.get("event") or d.get("type") or ""
                    rows.append(f"{str(d.get('ts') or d.get('t') or '')[:16]} {what}: {d.get('reason') or ''}".strip())
                out[ev] = rows
            return out

        data["decisions"] = await self.hass.async_add_executor_job(tail)
        shared = self.shared_chargers()
        data["fleet"] = {"cars": len(self.ev_ids()), "chargers": len({model.charger_of(self.nested, ev) for ev in self.ev_ids()}),
                         "one_charger_for_two_cars": bool(shared), "grid_division": self.plan.get("fleet_grid_mode"),
                         "house_connection": self.house_connection(),
                         "load_balancer": self.plan.get("house_load_balancer"), "price_source": self.plan.get("price_source"),
                         "shadow_mode": self.shadow,
                         # first start: when the user confirmed being responsible for the installation
                         "responsibility_confirmed": model.flatten(self.config_entry.options or self.config_entry.data)
                         .get("responsibility_confirmed")}
        data["share_ids"] = await self._share_ids()
        data["meta"] = {"created": dt_util.now().isoformat(timespec="seconds"), "hesc_version": VERSION,
                        "ha_version": ha_version, "language": self.hass.config.language}
        return data

    async def async_export(self, variant: str) -> dict[str, Any]:
        """Make the report in one of three forms. The full back-up (names, phones) goes to /config/hesc_backup
        (not served, and kept when HESC is removed); the anonymous and short forms go to /config/www/hesc_v4 so they can be opened."""
        ex = export.build(variant, await self._export_data())
        html = export.page(ex, self.hass.config.language)
        name = export.FILE_NAMES[variant]
        path = self.backup_path if variant == "full" else Path(self.hass.config.path("www", "hesc_v4", name))

        def write() -> bool:
            path.parent.mkdir(parents=True, exist_ok=True)
            return self._write_file(path, html)

        if not await self.hass.async_add_executor_job(write):
            raise HomeAssistantError(f"Could not write {path}")
        url = None if variant == "full" else f"/local/hesc_v4/{name}?v={int(dt_util.utcnow().timestamp())}"
        self.exports[variant] = {"created": ex["created"], "file": str(path), "url": url}
        self.async_update_listeners()
        out = {"file": str(path), "url": url}
        if variant == "bug":
            out["text"] = ex["text"]
        return out

    async def async_restore_backup(self) -> dict[str, Any]:
        """Put back the settings, the planning and the learned charging power of every car from the full
        back-up (/config/hesc_backup/hesc_backup.html; an older one in HESC's own folder). Cars that are not there are skipped."""
        path = self.backup_path
        if not await self.hass.async_add_executor_job(path.exists):
            path = self.data_dir / export.FILE_NAMES["full"]  # a back-up made before 11-11-2026
        try:
            text = await self.hass.async_add_executor_job(path.read_text, "utf-8")
        except OSError as err:
            raise HomeAssistantError(f"No full back-up found ({path})") from err
        try:
            ex = export.parse(text)
        except export.ExportError as err:
            raise HomeAssistantError(f"Back-up not usable: {err}") from err
        if ex.get("variant") != "full":
            raise HomeAssistantError("Only a full back-up can be put back")
        done = []
        now, tz = self._now_ms(), self.hass.config.time_zone
        for ev in self.ev_ids():
            if ev not in (ex.get("settings") or {}):
                continue
            with self.as_car(ev):
                view, where = self._own_settings_view()
                acts = settings_backup.restore(view, json.dumps({"items": ex["settings"][ev]}), now, tz)
                await self._apply_setting_actions(acts, where)
                if isinstance((ex.get("planning") or {}).get(ev), dict):
                    self.planning = planning.clean(ex["planning"][ev])
                    self._save_planning()
                lr = (ex.get("learn") or {}).get(ev) or {}
                self.learn = learn.clean({"sessions": lr.get("sessions") or []})
                self.fill = {"fills": list(lr.get("fills") or []), "plug": None}
                self._save_learn()
            done.append(ev)
        await self.async_request_refresh()
        return {"restored": done, "created": ex.get("created")}

    async def async_refresh_backup_meta(self) -> None:
        """Date, reason and count of settings_backup.json, shown on the restore button."""
        path = self.data_dir / "settings_backup.json"

        def read() -> dict[str, Any]:
            try:
                b = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                return {}
            if not isinstance(b, dict):
                return {}
            created = str(b.get("created") or "")
            local = dt_util.parse_datetime(created) if created else None
            return {"backup_created": dt_util.as_local(local).strftime("%Y-%m-%d %H:%M") if local else None,
                    "backup_reason": b.get("reason"), "backup_count": b.get("count")}

        self.backup_meta = await self.hass.async_add_executor_job(read)
        self.async_update_listeners()

    # ---- take over from v3 ------------------------------------------------------------
    def v3_entry(self) -> Any:
        """HESC v3's config entry (domain "hesc"), when v3 is installed next to v4."""
        entries = self.hass.config_entries.async_entries(PREV_DOMAIN)
        return entries[0] if entries else None

    def _v3_states(self, where: dict[str, tuple[str, str, str]]) -> dict[str, Any]:
        """v3's current setting values under the helper names the takeover uses (read only):
        v3's entity for the same key (unique id `<v3 entry>_<key>`, platform "hesc")."""
        from homeassistant.helpers import entity_registry as er

        entry = self.v3_entry()
        out: dict[str, Any] = {}
        if entry is None:
            return out
        reg = er.async_get(self.hass)
        for helper, (platform, key, _kind) in where.items():
            eid = reg.async_get_entity_id(platform, PREV_DOMAIN, f"{entry.entry_id}_{key}")
            st = self.hass.states.get(eid) if eid else None
            if st is not None:
                out[helper] = {"state": st.state, "attributes": dict(st.attributes)}
        return out

    def _take_over_v3_setup(self) -> int:
        """v3's setup choices (sources, charger, car sensor) become EV1 + charger 1 + shared (decision 9).
        Returns the number of fields that changed. v3's entry is only read."""
        entry = self.v3_entry()
        if entry is None:
            return 0
        v3 = dict(entry.options or entry.data)
        mine = self.config_entry.options or self.config_entry.data
        before = model.flatten(mine)
        keep = {k: v for k, v in before.items() if k == "take_over_v3_pending"}
        updated = model.replace_flat(mine, {**v3, **keep})
        if model.ev_name(updated) == "EV1":
            name = model.car_name(self.hass, v3.get(CONF_EV_SOC))
            if name:
                updated["evs"][model.EV1][model.EV_NAME] = name
        if self.config_entry.options:
            self.hass.config_entries.async_update_entry(self.config_entry, options=updated)
        else:
            self.hass.config_entries.async_update_entry(self.config_entry, data=updated)
        after = model.flatten(updated)
        return sum(1 for k in set(before) | set(after) if before.get(k) != after.get(k))

    async def async_take_over_from_v3(self) -> None:
        """v4 alpha next to v3 (decision 30-10-2026: "v3 stays untouched"): fill v4's settings with v3's
        current values and take over v3's history, so v4 goes on where v3 stops. v3 is only read.
        Only in shadow mode; meant
        to be pressed right before shadow mode goes off (may be pressed again to refresh).
        Back-ups (so a restore never brings back stale defaults): a dated copy of v3's own settings
        before taking over (the undo point), and right after taking over a fresh back-up that
        becomes settings_backup.json, so "Settings restore" brings back the taken-over values and
        not the standard values from before. v3's own shadow history is kept as
        history_shadow_<date-time>.jsonl; nothing is deleted. v2 is only read."""
        if not self.shadow:
            raise HomeAssistantError("Shadow mode is off: take over from v3 only before HESC v4 takes over")
        if self.v3_entry() is None:
            raise HomeAssistantError("HESC v3 is not installed: there is nothing to take over")
        src = Path(self.hass.config.path(*V2_HISTORY))
        marker = self.data_dir / "taken_over_v3.json"

        def read_v2() -> tuple[str | None, bool]:
            try:
                return src.read_text("utf-8"), marker.exists()
            except FileNotFoundError:
                return None, marker.exists()

        try:
            v2_text, _again = await self.hass.async_add_executor_job(read_v2)
        except (OSError, ValueError) as err:
            raise HomeAssistantError(f"Could not read v3's history {src}: {err}") from err
        setup_changed = self._take_over_v3_setup()
        view, where = self._own_settings_view()
        now, tz = self._now_ms(), self.hass.config.time_zone
        stamp, nice = settings_backup._stamps(now, tz)
        files, _ = settings_backup.backup(view, "before taking over v3's settings", now, tz)
        files = [f for f in files if f[0] != "settings_backup.json"]  # dated undo point only
        v3 = self._v3_states(where)
        items = settings_backup.collect(v3)
        acts = [a for a in (settings_backup.set_action(view, i, v) for i, v in items.items()) if a]
        changed = len(acts) + setup_changed

        def unique(name: str, ext: str = ".json") -> Path:
            path, n = self.data_dir / f"{name}{ext}", 1
            while path.exists():
                n += 1
                path = self.data_dir / f"{name}_{n}{ext}"
            return path

        def write_all() -> None:
            for name, text in files:
                path = self.data_dir / name if name == "settings_backup.json" else unique(name[:-5])
                if not self._write_file(path, text):
                    raise HomeAssistantError(f"Could not write {path}")
            if v2_text is not None:
                if self.history_path.exists():
                    self.history_path.replace(unique(f"history_shadow_{stamp}", ".jsonl"))
                if not self._write_file(self.history_path, v2_text):
                    raise HomeAssistantError(f"Could not write {self.history_path}")
            self._write_file(marker, json.dumps({"taken_over": iso(now)}))

        try:
            await self.hass.async_add_executor_job(write_all)
        except OSError as err:
            raise HomeAssistantError(f"Could not take over v3's history: {err}") from err
        hist = "no v3 history" if v2_text is None else f"history {sum(1 for ln in v2_text.split(chr(10)) if ln.strip())} lines"
        await self._apply_setting_actions(acts, where)
        self._take_over_v3_planning()
        # decision 3 (31-10 17:25): the charging power taken over from v3 counts as set by hand
        with self.as_car(model.EV1):
            sw = self.switch_entities.get("plan_charge_kw_learn")
            if sw is not None and sw.hass is not None:
                sw.set_from_logic(False)
            else:
                self.plan["plan_charge_kw_learn"] = False
        # the fresh back-up right after taking over becomes the one "Settings restore" uses
        after, _ = self._own_settings_view()
        files2, _ = settings_backup.backup(after, "after taking over v3's settings", now, tz)

        def write_after() -> None:
            for name, text in files2:
                path = self.data_dir / name if name == "settings_backup.json" else unique(name[:-5])
                if not self._write_file(path, text):
                    raise HomeAssistantError(f"Could not write {path}")

        try:
            await self.hass.async_add_executor_job(write_after)
        except OSError as err:
            raise HomeAssistantError(f"Could not write the back-up after taking over: {err}") from err
        await self.async_refresh_backup_meta()
        await self._apply_setting_actions(
            [settings_backup._info(f"Taken over from v3 {nice} · {changed} settings changed · {hist} · back-up made")], where)

    def _run_current(self) -> None:
        """Charging current follows the sun while the plan charges from the grid (current.py)."""
        before = (self.current_ctx.get("saved"), self.current_ctx.get("phases"))
        r = current.run(self._view(), self.current_ctx, self._now_ms())
        self.current_ctx = r.context
        if (r.context.get("saved"), r.context.get("phases")) != before:
            # kept on disk: after a restart HESC still puts the current back and knows the phases
            text = json.dumps({"saved": r.context.get("saved"), "phases": r.context.get("phases"), "phases_v": 2})
            path = self.current_path

            async def save() -> None:
                await self.hass.async_add_executor_job(self._write_file, path, text)

            self.config_entry.async_create_task(self.hass, save(), "hesc current")
        self.published["input_text.hesc_current_status"] = r.status
        for msg in r.actions:
            self._command(msg["payload"])

    @property
    def kick_hand_back(self) -> bool:
        """Since 3.0.0: a kickstart is handing the charger back to its solar mode (paused, or waiting
        for the charger to start on sun). Meant for a home battery control: hold the home batteries
        meanwhile, also when the charger briefly shows 0 W, so the charger finds the surplus."""
        seq = (self.kick_flow.get("hescKick") or {}).get("seq") or {}
        return seq.get("phase") in ("pause", "watch") and bool(seq.get("kickPause"))

    def _run_kickstart(self) -> None:
        flow = dict(self.kick_flow)
        if "hescPlan" in self.plan_flow:
            flow["hescPlan"] = self.plan_flow["hescPlan"]
        r = kickstart.run(self._view(), flow, self._now_ms())
        self.kick_flow = r.flow
        for msg in r.status:
            p = msg["payload"]
            for eid in p["target"]["entity_id"]:
                self.published[eid] = p["data"].get("value", "")
        for msg in r.actions:
            self._command(msg["payload"])
        del self.would_do[:-20]
        if r.history:
            self._history(r.history)

    def _run_ev_soc(self) -> None:
        view = self._view()
        self.computed["binary_sensor.hesc_diag_ev_connected"] = {"state": ev_soc.diag_ev_connected(view), "attributes": {}}
        view = self._view()
        flow = dict(self.soc_flow)
        for k in ("hescNoticeP1",):
            if k in self.plan_flow:
                flow[k] = self.plan_flow[k]
        r = ev_soc.run(view, flow, self.soc_context, self._now_ms())
        self.soc_context = r.context
        if not r.ran:
            return
        if "hescNoticeP1" in r.flow:
            self.plan_flow["hescNoticeP1"] = r.flow.pop("hescNoticeP1")
        self.soc_flow = r.flow
        for msg in r.api:
            path = msg["payload"]["path"]
            if path.startswith("/api/states/"):
                d = msg["payload"]["data"]
                self.computed[path[len("/api/states/"):]] = {"state": d["state"], "attributes": d["attributes"]}
            else:
                self._command(msg["payload"])  # phone notification
        del self.would_do[:-20]
        if r.save is not None:
            self.hass.async_add_executor_job(self._write_file, self.soc_path, r.save)

    # ---- advice and report -----------------------------------------------------------
    def _history_paths(self) -> tuple[Path, ...]:
        """The history the advice and the report read. In shadow mode v4 reads v3's history (read only):
        v4 switches nothing then, so its own history does not show what really happened."""
        if self.shadow:
            return (Path(self.hass.config.path(*V2_HISTORY)),)
        return (self.history_path,)

    def _read_history_sync(self, own_steps: bool) -> str | None:
        """The history text, or None when the file is missing or unreadable (v2's "file in" fails).
        own_steps: in shadow mode add v3's own "advice_applied" lines, so the one-step-per-week
        brake also sees the steps v3 made on its own thresholds."""
        path = self._history_paths()[0]
        try:
            text = path.read_text("utf-8")
        except OSError as err:
            if not isinstance(err, FileNotFoundError):
                _LOGGER.warning("HESC v4 could not read %s: %s", path, err)
            return None
        if own_steps and self.shadow:
            try:
                own = self.history_path.read_text("utf-8")
            except OSError:
                own = ""
            extra = "".join(ln + "\n" for ln in own.split("\n") if '"type":"advice_applied"' in ln)
            if extra:
                text = text + ("" if text.endswith("\n") or not text else "\n") + extra
        return text

    def _snapshot(self) -> dict[str, dict[str, Any]]:
        """All states as the ported logic sees them, as plain data (safe to use in a worker thread)."""
        view = self._view()
        return {k: view[k] for k in view}

    def _run_advice_gate(self) -> None:
        """v2 "Advice: when to run" (every input round)."""
        st = self._view().get("input_boolean.hesc_advice_auto") or {}
        S: dict[str, Any] = {"input_boolean.hesc_advice_auto": {"state": st.get("state")}}
        if advice.SENSOR in self.computed:
            S[advice.SENSOR] = self.computed[advice.SENSOR]
        topic, self.advice_gate_ctx = advice.gate(S, self.advice_gate_ctx, self._now_ms(), self.hass.config.time_zone)
        if topic:
            self.config_entry.async_create_task(self.hass, self.async_run_advice(topic), "hesc advice")
        # since 3.0.0: the advice depends on HPVC (no threshold advice without it), so with or
        # without HPVC switched over, the advice and the report line are worked out again at once
        sa = (self._view().get("input_boolean.hesc_standalone") or {}).get("state") == "on"
        was, self._standalone_seen = self._standalone_seen, sa
        if was is not None and sa != was:
            if not topic:
                self.config_entry.async_create_task(self.hass, self.async_run_advice("standalone"), "hesc advice")
            self.config_entry.async_create_task(self.hass, self.async_daily_advisor(), "hesc advisor")

    async def async_run_advice(self, topic: str) -> None:
        """v2 "Read history (advice)" -> "Start threshold advice (+ auto apply)" -> HA."""
        S, now = self._snapshot(), self._now_ms()
        floor = self.advice_floor_w()

        def work() -> advice.Result | None:
            text = self._read_history_sync(own_steps=True)
            return None if text is None else advice.run(S, text, topic, {}, now, floor_w=floor, limited_only=True)

        try:
            r = await self.hass.async_add_executor_job(work)
        except Exception:
            _LOGGER.exception("HESC v4 start threshold advice failed")
            return
        if r is None:
            return
        if r.out1 is not None:  # the step is recorded before it is made
            await self.hass.async_add_executor_job(self._append_history, r.out1["payload"] + "\n")
        self.computed[advice.SENSOR] = r.sensor()
        if "hescNoticeP3" in r.flow:
            self.soc_flow["hescNoticeP3"] = r.flow["hescNoticeP3"]
        for helper, value in r.set_values():
            await self.async_set_tuning(helper, value)
        self.async_update_listeners()

    async def async_set_tuning(self, helper: str, value: float) -> None:
        """Set one of v3's own tuning values (under v2's helper name) through its entity."""
        from homeassistant.helpers import entity_registry as er

        spec = next(n for n in NUMBERS if n.helper == helper)
        eid = er.async_get(self.hass).async_get_entity_id("number", DOMAIN, model.unique_id(self.config_entry.entry_id, spec.key))
        if eid is None:
            self.tuning[spec.key] = float(value)
            return
        try:
            await self.hass.services.async_call("number", "set_value", {"entity_id": eid, "value": value}, blocking=True)
        except (HomeAssistantError, ValueError) as err:
            _LOGGER.warning("HESC v4 could not set %s to %s: %s", eid, value, err)

    def _check_seasonal_switch(self) -> None:
        """v2 automation "Seasonal start threshold", trigger "switched on"."""
        on = (self._view().get("input_boolean.hesc_seasonal_threshold") or {}).get("state") == "on"
        was, self._seasonal_on = self._seasonal_on, on
        if on and was is False:
            self.config_entry.async_create_task(self.hass, self.async_seasonal(), "hesc seasonal threshold")

    async def async_seasonal(self, _now: Any = None) -> None:
        """v2 automation "Seasonal start threshold" (00:05, at start, when switched on)."""
        for helper, value in advice.seasonal_actions(self._view(), dt_util.now().month, floor_w=self.advice_floor_w()):
            await self.async_set_tuning(helper, value)

    async def async_daily_advisor(self, _now: Any = None) -> None:
        """v2 "Daily advice 21:30 (+ at start)" -> "Read HESC history (advice)" -> "HESC Advisor"."""
        S, now, flow = self._snapshot(), self._now_ms(), self.advisor_flow

        def work() -> advisor.Result | None:
            text = self._read_history_sync(own_steps=False)
            return None if text is None else advisor.run(S, text, "advice", flow, now, limited_only=True)

        try:
            r = await self.hass.async_add_executor_job(work)
        except Exception:
            _LOGGER.exception("HESC v4 advisor failed")
            return
        if r is not None:
            self._apply_advisor(r)

    def _apply_advisor(self, r: advisor.Result) -> None:
        self.advisor_flow = r.flow
        self.advice_global = r.advice
        self._publish(r.out2)

    def _publish(self, acts: list[dict[str, Any]] | None) -> None:
        for a in acts or []:
            p = a["payload"]
            for eid in p["target"]["entity_id"]:
                if p["action"].startswith("input_boolean."):
                    self.published[eid] = "on" if p["action"].endswith("turn_on") else "off"
                else:
                    self.published[eid] = p["data"].get("value", "")
        self.async_update_listeners()

    async def async_generate_report(self) -> None:
        """v2 "Generate report requested" -> Mark generating -> history -> Advisor -> report -> Mark ready."""
        out1, proceed, self.report_flow, _status = report.mark_generating(self.report_flow, self._now_ms())
        if out1 is not None:
            self._publish([out1])
        if not proceed:
            return
        S, now, flow, glob = self._snapshot(), self._now_ms(), self.advisor_flow, self.advice_global
        runtime = self.last_result.runtime if self.last_result is not None else None
        hist_path = str(self._history_paths()[0])
        lang = self.hass.config.language  # the report follows Home Assistant's language (nl, de; else English)

        def work() -> tuple[advisor.Result, str, str]:
            text = self._read_history_sync(own_steps=False)
            if text is None:
                text = ""  # v2 "History missing" -> "Empty history"
            r = advisor.run(S, text, None, flow, now, limited_only=True)
            html, open_html, _ = report.build(S, runtime, r.advice, text, now, global_advice=glob, version="v" + VERSION,
                                              history_path=hist_path, webhook_id=REPORT_WEBHOOK, lang=lang)
            return r, html, open_html

        try:
            r, html, open_html = await self.hass.async_add_executor_job(work)
        except Exception as err:
            _LOGGER.exception("HESC v4 report failed")
            raise HomeAssistantError(f"HESC v4 could not build the report: {err}") from err
        self._apply_advisor(r)
        folder = Path(self.hass.config.path(*REPORT_DIR))
        for name, body, is_open in (("open.html", open_html, True), ("report.html", html, False)):
            if not await self.hass.async_add_executor_job(self._write_file, folder / name, body):
                raise HomeAssistantError(f"Could not write {folder / name}")
            acts, self.report_flow, _ = report.mark_ready(self.report_flow, self._view(), self._now_ms(), is_open)
            self._publish(acts)

    def report_viewed(self) -> None:
        """v2 automation "Reset report after viewing" (webhook)."""
        self.published[report.READY_ENTITY] = "off"
        self.async_update_listeners()

    def _write_file(self, path: Path, text: str) -> bool:
        """Write atomically (a crash never leaves half a file)."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            write_utf8_file(str(path), text)
        except (OSError, HomeAssistantError) as err:
            _LOGGER.warning("HESC v4 could not write %s: %s", path, err)
            return False
        return True

    async def async_save_costs(self, ev: str = model.EV1) -> None:
        """On unload: keep what was counted since the last 5-minute save."""
        with self.as_car(ev):
            data, path = self.costs, self.costs_path
        if data is not None:
            await self.hass.async_add_executor_job(self._write_file, path, js_json(data))

    # ---- price forecast (every 15 minutes, own history file) -------------------------
    async def async_load_price_history(self) -> None:
        self.price_hist = await self.hass.async_add_executor_job(self._read_price_history)
        self.price_hist_loaded = True

    def _read_price_history(self) -> Any:
        import json

        for path in (self.price_hist_path, Path(self.hass.config.path(*V2_PRICE_HISTORY))):
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                continue
            except (OSError, ValueError) as err:
                _LOGGER.warning("HESC v4 could not read price history %s: %s", path, err)
                return None
        return None

    async def async_run_price_forecast(self, _now: Any = None) -> None:
        if not self.price_hist_loaded:
            return
        try:
            r = price_forecast.run(self._view(), self.price_hist, self._now_ms())
        except Exception:
            _LOGGER.exception("HESC v4 price forecast failed")
            return
        self.price_hist = r.history
        self.computed["sensor.hesc_price_forecast"] = {"state": r.state, "attributes": r.attributes}
        if r.save is not None:
            await self.hass.async_add_executor_job(self._write_price_history, r.save)
        self.async_update_listeners()

    def _write_price_history(self, text: str) -> None:
        try:
            self.price_hist_path.parent.mkdir(parents=True, exist_ok=True)
            self.price_hist_path.write_text(text, encoding="utf-8")
        except OSError as err:
            _LOGGER.warning("HESC v4 could not write price history %s: %s", self.price_hist_path, err)

    # ---- holidays and price fetch (read-only actions with a response) --------------
    async def async_update_holidays(self, _now: Any = None) -> None:
        from homeassistant.helpers import entity_registry as er

        reg = er.async_get(self.hass)
        workday = [e.entity_id for e in reg.entities.values() if e.platform == "workday"]
        cal = pricefetch.holiday_calendar(workday, self.hass.states.async_entity_ids("calendar"))
        events = None
        if cal:
            start = dt_util.now() - timedelta(days=100)
            end = dt_util.now() + timedelta(days=31)
            try:
                events = await self.hass.services.async_call(
                    "calendar", "get_events",
                    {"entity_id": cal, "start_date_time": start.strftime("%Y-%m-%d 00:00:00"),
                     "end_date_time": end.strftime("%Y-%m-%d 00:00:00")},
                    blocking=True, return_response=True)
            except Exception as err:  # noqa: BLE001 - v2: continue_on_error
                _LOGGER.debug("HESC v4 holiday calendar not read: %s", err)
        n, dates, source = pricefetch.holidays(cal, events)
        self.computed["sensor.hesc_holidays"] = {"state": str(n), "attributes": {"dates": dates, "source": source}}
        self.async_update_listeners()

    def _maybe_fetch(self, get) -> None:
        src = (get("input_select.hesc_price_source") or ("unknown",))[0]
        ent = (get("input_text.hesc_price_sensor") or ("unknown",))[0].strip()
        if src in pricefetch.ACTION_SOURCES and (src, ent) != self._fetch_key:
            self._fetch_key = (src, ent)
            self.config_entry.async_create_background_task(self.hass, self.async_fetch_prices(), "hesc price fetch")

    async def async_fetch_prices(self, _now: Any = None) -> None:
        from homeassistant.helpers import entity_registry as er

        get = self._getter(self._view())
        src = (get("input_select.hesc_price_source") or ("unknown",))[0]
        ent = (get("input_text.hesc_price_sensor") or ("unknown",))[0].strip()
        if src not in pricefetch.ACTION_SOURCES:
            return
        self._fetch_key = (src, ent)
        entry = ""
        if ent not in ("", "unknown"):
            e = er.async_get(self.hass).async_get(ent)
            entry = (e.config_entry_id if e else "") or ""
        action, dat1, dat2 = pricefetch.fetch_plan(src, entry)  # type: ignore[misc]
        domain, service = action.split(".", 1)
        answers = []
        for data in (dat1, dat2):
            try:
                answers.append(await self.hass.services.async_call(domain, service, data, blocking=True, return_response=True))
            except Exception as err:  # noqa: BLE001 - v2: continue_on_error
                _LOGGER.debug("HESC v4 price fetch %s failed: %s", action, err)
                answers.append(None)
        self.fetch_rows = pricefetch.fetch_rows(answers[0], answers[1])
        self.fetch_div = pricefetch.fetch_div(src)
        self.computed["sensor.hesc_price_fetch"] = {
            "state": dt_util.now().isoformat(), "attributes": {"source": src, "div": self.fetch_div, "rows": self.fetch_rows}}
        self.async_update_listeners()

    def _append_history(self, lines: str, path: Path | None = None) -> None:
        path = path or self.history_path
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as f:
                f.write(lines)
        except OSError as err:
            _LOGGER.warning("HESC v4 could not write its history file %s: %s", path, err)
