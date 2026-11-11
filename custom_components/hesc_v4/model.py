"""HESC v4 data model: two cars, each on its own charger or sharing one, with one shared dashboard.

Decisions (project notes, "HESC v4 — ..." files):
- 27-10 (decision 9): v3 settings become EV1 + the shared settings; EV1's name is the car's name in HA.
- 27-10 (decision 8): with one car there is no EV2.
- 28-10 (decision 25): every setting is one of three kinds: only this car / charger / shared.
- 30-10 20:31: start thresholds and timing per charger; kickstart "minimum kWh for the car" per car;
  cheap chance + price limit shared; vacation per car; fixed ids EV1/EV2 in entity ids.

Storage (config entry VERSION 2) - the setup choices of the config entry, nested:

    {"shared":   {<shared keys>},
     "evs":      {"ev1": {"name": "...", "charger": "charger1", <car keys>}, "ev2": {...}},
     "chargers": {"charger1": {<charger keys>}, "charger2": {...}}}

The same scope table decides which device and unique id an entity setting gets (entity.py), so the
values kept by entities follow the same three kinds.

The decision logic still reads one flat dict for one car (`flatten`): the shared settings, the car's
own settings and those of the charger it is on. With one car this is exactly v3's dict, so v4 with one
car does what v3 does (meetlat: tests/baseline_v3).
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import Any, Final

from . import const as c
from .plan_settings import DAYS


class Scope(StrEnum):
    SHARED = "shared"
    EV = "ev"
    CHARGER = "charger"


EV1: Final = "ev1"
EV2: Final = "ev2"
EVS: Final = (EV1, EV2)
CHARGER1: Final = "charger1"
CHARGER2: Final = "charger2"
CHARGERS: Final = (CHARGER1, CHARGER2)

# keys of a car that only exist in v4
EV_NAME: Final = "name"  # shown name; the entity ids keep ev1/ev2 (decision 30-10 20:31)
EV_CHARGER: Final = "charger"  # which charger the car is on (two cars may share one)

ENTRY_VERSION: Final = 2  # 1 = v3's flat dict

# ---- the scope of every setting ------------------------------------------------------------------
# Car: the car's battery, its own sensor and its own planning (rhythm, this time only, vacation).
EV_KEYS: Final[frozenset[str]] = frozenset({
    EV_NAME, EV_CHARGER,
    "ev_name",  # the text entity that shows and changes EV_NAME
    c.CONF_EV_SOC,
    "ev_full_soc",  # tuning: "full at %"
    "ev_battery_kwh",
    "car_setup",  # v4 08-11: sensor.hesc_v4_evN_setup, the sources of the car and its charger
    "car_controlled",  # v4 08-11: HESC controls this car (and its own charger) on/off
    "colour",  # v4 first start: the car's colour on the cards (opmaakchat 02-11 nr 7)
    "car_plug_sensor",  # v4 step 3: the car's own "plugged in" sensor (decision 30)
    "min_charge_enabled", "min_charge_soc", "min_charge_hours",
    "plan_final_check_min",
    "rep_enabled", "rep_time", "rep_goal", *(f"rep_{d}" for d in DAYS),
    *(f"rep_{d}_time" for d in DAYS), *(f"rep_{d}_goal" for d in DAYS),
    "kick_min_ev_kwh",  # decision 30-10 20:31: per car
    # Charging power the plan reckons with. Provisional: per car, because the car's onboard charger
    # decides the phases (decision 17-10). To be confirmed by SatScan.
    "plan_charge_kw", "plan_charge_kw_learn", "no_soc_kwh", "soc_entered",
    "plug_reminder", "plug_reminder_time",  # v4 step 6 (decision 33: per car)
    "charge_now",  # the "charge now to ...%" choice
    # morning summary per car, each to its own phones (decision 31-10-2026 06:51: "beide apart
    # en dus in te stellen op 2 phone"); the phones are the car's notification phones
    "morning_summary", "morning_summary_time", "notify_services",
})

# Entities that show one car (not settings): status texts, the car's plan, battery level, costs and
# what its charger reports (step 2, part B: each car its own round and its own sensors).
EV_ENTITY_KEYS: Final[frozenset[str]] = frozenset({
    "state", "reason", "last_action", "insight_today", "insight_accuracy", "insight_now",
    "plan_status", "kick_status", "current_status",
    "charge_plan", "expected_charge_cost", "ev_battery_level", "notice", "charging_costs", "coming_week", "charge_power",
    "ev_power", "ev_soc", "charger_mode", "missing_inputs", "summary",
    "inputs_valid", "ev_connected", "charger_solar_mode", "diag_ev_connected",
    "notify_pick",
    # decision 31-10-2026 20:34 ("3 Akkoord"): phone buttons and the costs export per car too
    "costs_export", "costs_export_info",
    "charge_now_plan_goal", "charge_now_stop", "skip_next_day", "undo_skip_day", "plan_off",
})

# Charger: what the charger is, its sensors and controls, and when it starts and stops.
CHARGER_KEYS: Final[frozenset[str]] = frozenset({
    c.CONF_CHARGER_TYPE, c.CONF_CHARGER_MODE, c.CONF_CHARGER_ECO_VALUES, c.CONF_CHARGER_SOLAR_SWITCH,
    c.CONF_CHARGER_START_STOP, c.CONF_CHARGER_RESUME, c.CONF_CHARGER_CURRENT,
    # read from the charger, not from the car (v3 names them ev_*)
    c.CONF_EV_CONNECTED, c.CONF_EV_DISCONNECTED_VALUES, c.CONF_EV_POWER, c.CONF_EV_GREEN_ENERGY,
    "charger_grid_mode_value",
    # start thresholds and timing: per charger (decision 30-10 20:31)
    "p_start", "p_hold", "irr_start", "irr_hold",
    "t_stable", "t_start", "t_dip", "t_stop", "t_max", "cooldown", "max_attempts", "ev_active_w",
    "charger_max_a",  # v4 part D: the installer's maximum (decision 31-10 09:58, question 3)
    "swap_time",  # v4 step 3: cable swap time when two cars share this charger (decision 31)
    "charger_car",  # v4 step 3: which car is on this charger, chosen yourself (decision 30)
    "swap_reminder",  # v4 first start: the cable swap reminder on/off (decision 32)
})

# Everything else is shared: sun, grid, prices and cheap chance, home battery and kickstart, HPVC,
# costs settings, notifications, advice, live/shadow mode and the dashboard switches.


def scope_of(key: str) -> Scope:
    if key in EV_KEYS or key in EV_ENTITY_KEYS:
        return Scope.EV
    if key in CHARGER_KEYS:
        return Scope.CHARGER
    return Scope.SHARED


# ---- nested <-> flat -------------------------------------------------------------------------------
def is_nested(settings: Mapping[str, Any]) -> bool:
    return isinstance(settings.get("evs"), Mapping) and isinstance(settings.get("shared"), Mapping)


def nest(flat: Mapping[str, Any], *, name: str | None = None) -> dict[str, Any]:
    """v3's flat dict -> v4: EV1 on charger 1 plus the shared settings (decision 9)."""
    out: dict[str, Any] = {"shared": {}, "evs": {EV1: {EV_NAME: name or "EV1", EV_CHARGER: CHARGER1}},
                           "chargers": {CHARGER1: {}}}
    for key, value in flat.items():
        part = scope_of(key)
        if part is Scope.EV:
            out["evs"][EV1][key] = value
        elif part is Scope.CHARGER:
            out["chargers"][CHARGER1][key] = value
        else:
            out["shared"][key] = value
    return out


def ensure_nested(settings: Mapping[str, Any]) -> dict[str, Any]:
    return _copy(settings) if is_nested(settings) else nest(settings)


def ev_ids(nested: Mapping[str, Any]) -> list[str]:
    """The cars set up, EV1 first. With one car there is no EV2 (decision 8)."""
    evs = nested.get("evs") or {}
    return [e for e in EVS if e in evs]


# Settings that only mean something when two cars share one charger (step 3, decisions 30-31)
SHARED_ONLY: Final = frozenset({"swap_time", "charger_car", "car_plug_sensor", "swap_reminder"})


def entity_cars(nested: Mapping[str, Any], key: str) -> list[str]:
    """For which cars an entity with this key exists: one per car for a car's key, one per charger
    (made for the first car on it) for a charger's key, else only one (EV1, shared)."""
    evs = ev_ids(nested) or [EV1]
    part = scope_of(key)
    if key in SHARED_ONLY:  # step 3: only where two cars share one charger
        on: dict[str, list[str]] = {}
        for ev in evs:
            on.setdefault(charger_of(nested, ev), []).append(ev)
        evs = [ev for ev in evs if len(on[charger_of(nested, ev)]) > 1]
    if part is Scope.EV:
        return evs
    if part is Scope.CHARGER:
        firsts: dict[str, str] = {}
        for ev in evs:
            firsts.setdefault(charger_of(nested, ev), ev)
        return list(firsts.values())
    return [EV1]


def charger_of(nested: Mapping[str, Any], ev: str = EV1) -> str:
    car = (nested.get("evs") or {}).get(ev) or {}
    return str(car.get(EV_CHARGER) or CHARGER1)


def ev_name(nested: Mapping[str, Any], ev: str = EV1) -> str:
    car = (nested.get("evs") or {}).get(ev) or {}
    return str(car.get(EV_NAME) or ev.upper())


def flatten(settings: Mapping[str, Any], ev: str = EV1) -> dict[str, Any]:
    """What the decision logic of one car reads: shared + this car + the charger it is on.
    A flat (v3) dict comes back as it is."""
    if not is_nested(settings):
        return dict(settings)
    out = dict(settings.get("shared") or {})
    out.update((settings.get("chargers") or {}).get(charger_of(settings, ev)) or {})
    car = dict((settings.get("evs") or {}).get(ev) or {})
    car.pop(EV_NAME, None)
    car.pop(EV_CHARGER, None)
    out.update(car)
    return out


def apply(settings: Mapping[str, Any], changes: Mapping[str, Any], ev: str = EV1) -> dict[str, Any]:
    """Put flat changes for one car in the right place: car keys at the car, charger keys at the
    charger the car is on, the rest in shared. Other cars and chargers stay as they are."""
    out = ensure_nested(settings)
    out["evs"].setdefault(ev, {EV_NAME: ev.upper(), EV_CHARGER: CHARGER1})
    charger = charger_of(out, ev)
    out.setdefault("chargers", {}).setdefault(charger, {})
    for key, value in changes.items():
        part = scope_of(key)
        if part is Scope.EV:
            out["evs"][ev][key] = value
        elif part is Scope.CHARGER:
            out["chargers"][charger][key] = value
        else:
            out["shared"][key] = value
    return out


def replace_flat(settings: Mapping[str, Any], flat: Mapping[str, Any], ev: str = EV1) -> dict[str, Any]:
    """The options flow hands back the complete flat set of one car: a field emptied there stays empty
    (v3 rule). The shared part, this car's keys and its charger's keys are replaced; another car and
    another charger stay as they are."""
    out = ensure_nested(settings)
    charger = charger_of(out, ev)
    car = out["evs"].setdefault(ev, {EV_NAME: ev.upper(), EV_CHARGER: CHARGER1})
    out["evs"][ev] = {EV_NAME: car.get(EV_NAME, ev.upper()), EV_CHARGER: car.get(EV_CHARGER, CHARGER1)}
    out["shared"] = {}
    out.setdefault("chargers", {})[charger] = {}
    return apply(out, flat, ev)


def _copy(nested: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "shared": dict(nested.get("shared") or {}),
        "evs": {k: dict(v) for k, v in (nested.get("evs") or {}).items()},
        "chargers": {k: dict(v) for k, v in (nested.get("chargers") or {}).items()},
    }


# ---- unique ids and devices of entity settings ------------------------------------------------------
def owner(key: str, ev: str = EV1, charger: str = CHARGER1) -> str | None:
    """The car or charger an entity belongs to; None for shared entities."""
    part = scope_of(key)
    if part is Scope.EV:
        return ev
    if part is Scope.CHARGER:
        return charger
    return None


# ---- the car's name in Home Assistant ---------------------------------------------------------------
def car_name(hass: Any, soc_entity: str | None) -> str | None:
    """Decision 9: EV1 is named after the car in HA. Taken from the device of the car's battery-level
    sensor (e.g. "BYD Atto3"); None when there is no such sensor or device (then "EV1")."""
    if not soc_entity:
        return None
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    ent = er.async_get(hass).async_get(str(soc_entity))
    if ent is None or not ent.device_id:
        return None
    dev = dr.async_get(hass).async_get(ent.device_id)
    if dev is None:
        return None
    return (dev.name_by_user or dev.name or "").strip() or None


def unique_id(entry_id: str, key: str, ev: str = EV1, charger: str = CHARGER1) -> str:
    """Unique id of an entity setting: `<entry>_<key>` when shared, `<entry>_ev1_<key>` for a car,
    `<entry>_charger1_<key>` for a charger. The entity ids follow from the device name:
    `hesc_v4_<name>`, `hesc_v4_ev1_<name>`, `hesc_v4_charger1_<name>` (fixed ids, decision 30-10 20:31)."""
    part = owner(key, ev, charger)
    return f"{entry_id}_{part}_{key}" if part else f"{entry_id}_{key}"


OWNER_LABEL: Final = {EV1: "EV1", EV2: "EV2", CHARGER1: "Charger1", CHARGER2: "Charger2"}
