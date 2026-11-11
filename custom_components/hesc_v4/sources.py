"""One source at a time, from the panel (opmaakchat 06-11-2026 13:45).

The settings window of the panel shows the sensors HESC reads (solar power, grid power, irradiance, the
forecast, the car's battery level, the charger's sensors ...). Until now only the options flow could
change them. `hesc_v4/setup/source` sets one, `hesc_v4/setup/find` lists suggestions per source
(`sources`), best first, like `pv` and `grid`.

Only which entity HESC *reads* (or, for the charger, which entity HESC uses for the normal charging
current and modes) is changed here: never an installer or house setting (hard rule 30-10-2026,
safety.py) - a charging-current entity that is an installer setting is refused.
"""
from __future__ import annotations

import re
from typing import Any, Final

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from . import current, model, safety
from .const import (
    CONF_CHARGER_CURRENT,
    CONF_CHARGER_ECO_VALUES,
    CONF_EV_DISCONNECTED_VALUES,
    CONF_CHARGER_MODE,
    CONF_CHARGER_RESUME,
    CONF_CHARGER_SOLAR_SWITCH,
    CONF_CHARGER_START_STOP,
    CONF_EV_CONNECTED,
    CONF_EV_GREEN_ENERGY,
    CONF_EV_POWER,
    CONF_EV_SOC,
    CONF_FORECAST_30M,
    CONF_FORECAST_NOW,
    CONF_GRID_EXPORT_SENSOR,
    CONF_GRID_POWER,
    CONF_GRID_POWER_L1,
    CONF_GRID_POWER_L2,
    CONF_GRID_POWER_L3,
    CONF_HPVC_ENABLED,
    CONF_HPVC_LIMITED,
    CONF_IRRADIANCE,
    CONF_PV_POWER,
    CONF_SOLAR_TODAY,
    CONF_SOLAR_TOMORROW,
)

# source key -> the entity domains it may be
KEYS: Final[dict[str, tuple[str, ...]]] = {
    CONF_PV_POWER: ("sensor",),
    CONF_GRID_POWER: ("sensor",),
    CONF_GRID_EXPORT_SENSOR: ("sensor",),
    CONF_GRID_POWER_L1: ("sensor",),
    CONF_GRID_POWER_L2: ("sensor",),
    CONF_GRID_POWER_L3: ("sensor",),
    CONF_FORECAST_NOW: ("sensor",),
    CONF_FORECAST_30M: ("sensor",),
    CONF_SOLAR_TODAY: ("sensor",),
    CONF_SOLAR_TOMORROW: ("sensor",),
    CONF_IRRADIANCE: ("sensor",),
    CONF_EV_SOC: ("sensor",),
    CONF_EV_CONNECTED: ("sensor", "binary_sensor"),
    CONF_EV_POWER: ("sensor",),
    CONF_EV_GREEN_ENERGY: ("sensor",),
    CONF_CHARGER_MODE: ("select", "input_select"),
    CONF_CHARGER_SOLAR_SWITCH: ("switch", "input_boolean"),
    CONF_CHARGER_START_STOP: ("switch", "input_boolean", "button"),
    CONF_CHARGER_RESUME: ("button", "switch", "input_button", "input_boolean"),
    CONF_CHARGER_CURRENT: ("number", "input_number"),
    CONF_HPVC_ENABLED: ("switch", "input_boolean", "binary_sensor"),
    CONF_HPVC_LIMITED: ("binary_sensor", "input_boolean", "switch"),
}
# the name as `sensor.hesc_v4_setup` shows it (v2's helper object id) -> source key
HELPER_NAMES: Final[dict[str, str]] = {
    **{f"hesc_{k}": k for k in KEYS if k != CONF_CHARGER_CURRENT},
    current.ENTITY_HELPER.split(".", 1)[1]: CONF_CHARGER_CURRENT,
    # 10-11-2026: the names `sensor.hesc_v4_setup` shows for the grid power per phase (Zon en net, phase advice)
    "hesc_grid_power_phase_1": CONF_GRID_POWER_L1, "hesc_grid_power_phase_2": CONF_GRID_POWER_L2,
    "hesc_grid_power_phase_3": CONF_GRID_POWER_L3,
}

_IRRADIANCE = re.compile(r"irradiance|zonlicht|zoninstraling|instraling|solar_?rad|globalstrahlung|strahlung|lux", re.I)
_FORECAST = re.compile(r"forecast|solcast|verwacht|voorspel|prognose|predict", re.I)
_TODAY = re.compile(r"today|vandaag|heute", re.I)
_TOMORROW = re.compile(r"tomorrow|morgen", re.I)
_NOW = re.compile(r"now|nu|jetzt|current|power_production_now|power_now", re.I)
_30M = re.compile(r"30|next_hour|volgend|next", re.I)
_SOC = re.compile(r"battery_level|soc|state_of_charge|accu|batterij|ladestand", re.I)
_CHARGER_WORDS: Final[dict[str, re.Pattern[str]]] = {
    CONF_EV_CONNECTED: re.compile(r"status|plug|connected|aangesloten|cable|kabel", re.I),
    CONF_EV_POWER: re.compile(r"charging_power|charge_power|laadvermogen|power", re.I),
    CONF_EV_GREEN_ENERGY: re.compile(r"green|groen|solar|zon", re.I),
    CONF_CHARGER_MODE: re.compile(r"solar|mode|stand|eco", re.I),
    CONF_CHARGER_SOLAR_SWITCH: re.compile(r"solar|eco|zon", re.I),
    CONF_CHARGER_START_STOP: re.compile(r"pause|resume|start|stop|charging|laden", re.I),
    CONF_CHARGER_RESUME: re.compile(r"resume|hervat|start", re.I),
    CONF_CHARGER_CURRENT: re.compile(r"current|stroom|ampere|amps|max_charging", re.I),
}


def key_of(name: str) -> str | None:
    """The source key for a key or a helper name ("irradiance_sensor" or "hesc_irradiance_sensor")."""
    if name in KEYS:
        return name
    return HELPER_NAMES.get(name.split(".", 1)[-1])


def _st(hass: HomeAssistant, eid: str) -> dict[str, Any]:
    st = hass.states.get(eid)
    a = st.attributes if st else {}
    return {"entity_id": eid, "name": a.get("friendly_name") or eid, "state": st.state if st else None,
            "unit": a.get("unit_of_measurement")}


def _usable(st: Any) -> bool:
    return st.state not in ("unavailable", "unknown") and not st.entity_id.startswith(("sensor.hesc_", "select.hesc_"))


def _unit(st: Any) -> str:
    return str(st.attributes.get("unit_of_measurement") or "")


def candidates(hass: HomeAssistant, key: str) -> list[str]:
    """Suggestions for one source, best first (empty when HESC has none to offer)."""
    from .config_flow import ev_soc_candidates
    from .finders import CHARGER_PLATFORMS, grid_choices, pv_candidates

    if key == CONF_PV_POWER:
        return pv_candidates(hass)
    if key == CONF_GRID_POWER:
        return [c["entity_id"] for c in grid_choices(hass)]
    if key == CONF_GRID_EXPORT_SENSOR:
        return [c["export_entity_id"] for c in grid_choices(hass) if c.get("export_entity_id")]
    if key in (CONF_GRID_POWER_L1, CONF_GRID_POWER_L2, CONF_GRID_POWER_L3):
        n = {CONF_GRID_POWER_L1: "1", CONF_GRID_POWER_L2: "2", CONF_GRID_POWER_L3: "3"}[key]
        rx = re.compile(rf"^sensor\..*(?:phase|fase)_?l?{n}$")
        return sorted(s.entity_id for s in hass.states.async_all("sensor")
                      if rx.match(s.entity_id) and s.attributes.get("device_class") == "power" and _usable(s)
                      and not re.search(r"production|consumption|levering|returned|delivered|export|import", s.entity_id))
    if key == CONF_EV_SOC:
        return ev_soc_candidates(hass, [])
    if key == CONF_IRRADIANCE:
        found = [s for s in hass.states.async_all("sensor") if _usable(s) and (
            s.attributes.get("device_class") == "irradiance" or _unit(s).replace("²", "2") in ("W/m2", "lx")
            or _IRRADIANCE.search(s.entity_id))]
        return [s.entity_id for s in sorted(found, key=lambda s: (
            s.attributes.get("device_class") != "irradiance", not _IRRADIANCE.search(s.entity_id), s.entity_id))]
    if key in (CONF_FORECAST_NOW, CONF_FORECAST_30M, CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW):
        power = key in (CONF_FORECAST_NOW, CONF_FORECAST_30M)
        word = {CONF_FORECAST_NOW: _NOW, CONF_FORECAST_30M: _30M, CONF_SOLAR_TODAY: _TODAY,
                CONF_SOLAR_TOMORROW: _TOMORROW}[key]
        found = [s for s in hass.states.async_all("sensor") if _usable(s) and _FORECAST.search(
            f"{s.entity_id} {s.attributes.get('friendly_name') or ''}") and (
            _unit(s) in ("W", "kW") if power else _unit(s) in ("kWh", "Wh"))]
        return [s.entity_id for s in sorted(found, key=lambda s: (not word.search(s.entity_id), s.entity_id))]
    if key in (CONF_HPVC_ENABLED, CONF_HPVC_LIMITED):
        word = "enabled|aan|on" if key == CONF_HPVC_ENABLED else "limit|begrens"
        return sorted(e for d in KEYS[key] for e in hass.states.async_entity_ids(d)
                      if "hpvc" in e and re.search(word, e))
    # the charger's entities: those of a charger integration first, the words of the field first
    reg = er.async_get(hass)
    words = _CHARGER_WORDS.get(key)
    own = [e.entity_id for e in reg.entities.values()
           if e.platform in CHARGER_PLATFORMS and e.domain in KEYS[key] and not e.disabled_by]
    if key == CONF_CHARGER_CURRENT:  # hard rule: never an installer setting
        own = [e for e in own if not safety.is_installer_setting(e)]
    if key in (CONF_EV_POWER, CONF_EV_GREEN_ENERGY):
        own = [e for e in own if (st := hass.states.get(e)) is not None
               and _unit(st) in (("W", "kW") if key == CONF_EV_POWER else ("kWh", "Wh"))]
    return sorted(own, key=lambda e: (not (words and words.search(e)), e))


_INVERTER_PLATFORMS = re.compile(r"solaredge|enphase|envoy|fronius|sma|growatt|huawei|goodwe|solis|apsystems|hoymiles|"
                                 r"solax|sungrow|victron|deye|sofar|foxess|omnik|zeversolar|kostal|solarman|ahoy|opendtu",
                                 re.I)
_TOTAL = re.compile(r"total|totaal|som|sum|gesamt", re.I)
_BAT_NAME = re.compile(r"battery|batterij|accu|akku|marstek|venus|zendure|anker|ecoflow|powerwall|home_bat", re.I)
_NOT_HOME_BAT = re.compile(r"phone|telefoon|iphone|ipad|tablet|watch|remote|afstandsbediening|sensor_battery|"
                           r"_ev_|\bev\b|car|auto|byd|tesla|wallbox|charger|laadpaal|mobile"
                           # 10-11-2026: plans, house use and demo sensors are no home battery
                           r"|batterijplan|batteryplan|huisverbruik|verbruik|consumption|demo"
                           # 11-11-2026: capacity/health measurements about a battery (e.g. marstek_capacity_monitor)
                           r"|capaciteit|capacity|specificatie|health|gezondheid|beschikbaar|cycli|cycles|marge", re.I)


def _num(st: Any) -> float | None:
    try:
        return float(st.state)
    except (TypeError, ValueError):
        return None


def ranked(hass: HomeAssistant, key: str) -> list[dict[str, Any]]:
    """The candidates of one source, best first, each with `why` (reason codes the panel translates) and
    `suggested` (true for the best one only, and only when HESC is sure enough; 08-11, decision 09:27).

    Reason codes: power, energy, name_pv, name_total, inverter, follows_sun, smart_meter, signed,
    import_export, irradiance, forecast, word_match, charger_device, car_device, only_one."""
    reg = er.async_get(hass)
    out: list[dict[str, Any]] = []

    def add(eid: str, score: float, why: list[str]) -> None:
        out.append({"entity_id": eid, "score": score, "why": why})

    if key == CONF_GRID_POWER:
        from .finders import grid_choices

        for c in grid_choices(hass):
            why = ["smart_meter", "power"] + (["import_export"] if c.get("export_entity_id") else ["signed"])
            add(c["entity_id"], 10 if c["recommended"] else 5, why)
    elif key == CONF_PV_POWER:
        sun_up = (hass.states.get("sun.sun") or type("S", (), {"state": ""})()).state == "above_horizon"
        for eid in candidates(hass, key):
            st, ent = hass.states.get(eid), reg.async_get(eid)
            txt = f"{eid} {st.attributes.get('friendly_name') or ''}" if st else eid
            score, why = 3.0, ["power", "name_pv"]
            if _TOTAL.search(txt):
                score, why = score + 2, why + ["name_total"]
            if ent and _INVERTER_PLATFORMS.search(ent.platform):
                score, why = score + 2, why + ["inverter"]
            v = _num(st) if st else None
            if v is not None and ((sun_up and v > 0) or (not sun_up and abs(v) < 50)):
                score, why = score + 1, why + ["follows_sun"]
            add(eid, score, why)
    else:
        found = candidates(hass, key)
        for i, eid in enumerate(found):
            why: list[str] = []
            st = hass.states.get(eid)
            if key == CONF_IRRADIANCE and st and st.attributes.get("device_class") == "irradiance":
                why = ["irradiance"]
            elif key in (CONF_FORECAST_NOW, CONF_FORECAST_30M, CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW):
                why = ["forecast"] + (["word_match"] if i == 0 else [])
                # decision 10-11-2026 (more plug and play): a day forecast with the half-hour rows
                # (detailedForecast) beats a sensor with only the day total - HESC draws and plans with the rows
                if key in (CONF_SOLAR_TODAY, CONF_SOLAR_TOMORROW) and st and st.attributes.get("detailedForecast"):
                    why += ["half_hours"]
            elif key == CONF_EV_SOC:
                why = ["car_device"]
            elif key in _CHARGER_WORDS:
                ent = reg.async_get(eid)
                why = (["charger_device"] if ent and ent.device_id else []) + (
                    ["word_match"] if _CHARGER_WORDS[key].search(eid) else [])
            add(eid, len(why) * 2 + (1 if i == 0 else 0) + (2 if "half_hours" in why else 0), why)
    out.sort(key=lambda c: -c["score"])
    for c in out:
        c["suggested"] = False
    # sure enough: a clear first (a better score than the second), with a real reason
    if out and out[0]["why"] and (len(out) == 1 or out[0]["score"] > out[1]["score"]):
        out[0]["suggested"] = True
        if len(out) == 1:
            out[0]["why"].append("only_one")
    return out


def home_battery(hass: HomeAssistant) -> dict[str, Any]:
    """Suggestions for the home battery fields (several may be chosen; 08-11, decision 09:27): level sensors
    (%) and power sensors (W; HESC expects + = the battery charges). A "total" power sensor is suggested
    alone; else every per-battery sensor. `sign_note` when the total has the opposite sign of the sum of the
    per-battery sensors: one of them counts the other way round (+ = discharging), check which."""
    def ok(st: Any) -> bool:
        txt = f"{st.entity_id} {st.attributes.get('friendly_name') or ''}"
        return _usable(st) and bool(_BAT_NAME.search(txt)) and not _NOT_HOME_BAT.search(txt)

    sts = [s for s in hass.states.async_all("sensor") if ok(s)]
    level = sorted((s for s in sts if _unit(s) == "%" and s.attributes.get("device_class") in ("battery", None)),
                   key=lambda s: s.entity_id)
    power = sorted((s for s in sts if s.attributes.get("device_class") == "power" or _unit(s) in ("W", "kW")),
                   key=lambda s: (not _TOTAL.search(s.entity_id), s.entity_id))
    totals = [s for s in power if _TOTAL.search(s.entity_id)]
    singles = [s for s in power if not _TOTAL.search(s.entity_id)]
    note = None
    if totals and singles:
        t, parts = _num(totals[0]), [v for v in (_num(s) for s in singles) if v is not None]
        if t is not None and parts and abs(sum(parts)) > 5 and abs(t + sum(parts)) < abs(t - sum(parts)):
            note = "total_opposite_to_parts"
    pick = {totals[0].entity_id} if totals else {s.entity_id for s in singles}
    lv_totals = [s for s in level if _TOTAL.search(s.entity_id)]
    lv_pick = {lv_totals[0].entity_id} if lv_totals else {s.entity_id for s in level}
    return {
        "home_battery_soc_sensors": {"multi": True, "candidates": [
            {**_st(hass, s.entity_id), "suggested": s.entity_id in lv_pick} for s in level][:25]},
        "home_battery_power_sensors": {"multi": True, "sign": "plus_is_charging", "sign_note": note, "candidates": [
            {**_st(hass, s.entity_id), "suggested": s.entity_id in pick} for s in power][:25]},
    }


def suggestions(hass: HomeAssistant) -> dict[str, Any]:
    """For `find`: per source key its candidates ({entity_id, name, state, unit, score, why, suggested}),
    best first; its place (shared · ev · charger) and the helper name `sensor.hesc_v4_setup` shows it under.
    Plus the home battery fields (multi)."""
    out: dict[str, Any] = {}
    for key in KEYS:
        out[key] = {"candidates": [{**_st(hass, c["entity_id"]), **{k: c[k] for k in ("score", "why", "suggested")}}
                                   for c in ranked(hass, key)[:25]],
                    "scope": model.scope_of(key).value,
                    "helper": next(h for h, k in HELPER_NAMES.items() if k == key)}
    out.update(home_battery(hass))
    return out


def check(hass: HomeAssistant, key: str | None, entity_id: str) -> str | None:
    """The error code for setting `key` to `entity_id` ("" = empty it), None when fine."""
    if key is None:
        return "unknown_source"
    if not entity_id:
        return None
    if entity_id.split(".", 1)[0] not in KEYS[key]:
        return "wrong_kind"
    if hass.states.get(entity_id) is None:
        return "not_found"
    if key == CONF_CHARGER_CURRENT and safety.is_installer_setting(entity_id):
        return "installer_setting"
    return None


# 08-11 (opmaakchat 10:40): value lists of a charger, set with `hesc_v4/setup/value`
VALUE_KEYS: Final = (CONF_CHARGER_ECO_VALUES, CONF_EV_DISCONNECTED_VALUES)


def value_key_of(name: str) -> str | None:
    """`charger_eco_values` / `ev_disconnected_values`, also by the name `sensor.hesc_v4_setup` shows
    (`hesc_charger_eco_value`, `hesc_ev_disconnected_values`)."""
    n = name.split(".", 1)[-1]
    n = n[len("hesc_"):] if n.startswith("hesc_") else n
    n = {"charger_eco_value": CONF_CHARGER_ECO_VALUES}.get(n, n)  # v2's helper name
    return n if n in VALUE_KEYS else None


async def async_values_seen(hass: HomeAssistant, entity_id: str, days: int) -> dict[str, Any]:
    """The distinct states of an entity in the recorder (most recent first), its `options` and the
    "no car" values the charger table knows."""
    from datetime import timedelta

    from homeassistant.util import dt as dt_util

    from .charger_table import CHARGER_TABLE

    st = hass.states.get(entity_id)
    seen: list[str] = []
    try:
        from homeassistant.components.recorder import get_instance, history

        end = dt_util.utcnow()
        changes = await get_instance(hass).async_add_executor_job(
            history.state_changes_during_period, hass, end - timedelta(days=days), end, entity_id, True)
        for s in reversed(changes.get(entity_id, [])):
            if s.state not in seen and s.state not in ("unknown", "unavailable"):
                seen.append(s.state)
    except Exception:  # noqa: BLE001 - no recorder (or not this entity): only the state of now
        pass
    if st is not None and st.state not in seen and st.state not in ("unknown", "unavailable"):
        seen.insert(0, st.state)
    known = sorted({v.strip() for p in CHARGER_TABLE.values() for v in str(p.get("nc") or "").split(",") if v.strip()})
    return {"entity_id": entity_id, "seen": seen[:30], "options": list((st.attributes.get("options") if st else None) or []),
            "known_not_connected": known}
