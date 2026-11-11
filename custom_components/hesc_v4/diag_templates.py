"""v2.0.0's small dashboard template sensors (diagnostics, configuration valid, prices available).

Each function is a line-by-line port of one template from v2's package and gives the state HA
renders (binary sensors: 'on'/'off'; 'unavailable' when the template's availability is false).
`get(entity_id)` returns (state, attributes) or None, as everywhere in v3. Proven identical to the
templates rendered by Home Assistant (`tests/integration/test_diag_templates.py`).
"""
from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

from .templatecompat import forgiving_float, jinja_round, jinja_str

Getter = Callable[[str], Any]
BAD = ("", "unknown", "unavailable")


def _states(get: Getter, e: Any) -> str:
    s = get(e) if isinstance(e, str) and e else None
    return "unknown" if s is None else s[0]


def _attr(get: Getter, e: Any, a: Any) -> Any:
    s = get(e) if isinstance(e, str) and e else None
    if s is None or not isinstance(a, str):
        return None
    return s[1].get(a)


def is_number(value: Any) -> bool:
    """HA `| is_number`."""
    if not isinstance(value, (str, int, float)):
        return False
    try:
        f = float(value)
    except (ValueError, TypeError):
        return False
    return math.isfinite(f)


def _onoff(v: bool) -> str:
    return "on" if v else "off"


def _power(get: Getter, helper: str) -> str:
    e = _states(get, helper)
    if not is_number(_states(get, e)):
        return "unavailable"
    k = 1000 if jinja_str(_attr(get, e, "unit_of_measurement")).lower() == "kw" else 1
    return jinja_str(jinja_round(forgiving_float(_states(get, e), 0) * k, 0))


def diag_pv_power(get: Getter) -> str:
    return _power(get, "input_text.hesc_pv_power_sensor")


def diag_ev_power(get: Getter) -> str:
    return _power(get, "input_text.hesc_ev_power_sensor")


def diag_forecast_power(get: Getter) -> str:
    e = _states(get, "input_text.hesc_forecast_now_sensor")
    if not is_number(_states(get, e)):
        return "unavailable"
    return jinja_str(jinja_round(forgiving_float(_states(get, e), 0), 0))


def diag_forecast_cautious(get: Getter) -> str:
    e = _states(get, "input_text.hesc_forecast_now_sensor")
    a = _states(get, "input_text.hesc_forecast_attribute")
    v = _attr(get, e, a) if a not in BAD else _states(get, e)
    if not is_number(v):
        return "unavailable"
    return jinja_str(jinja_round(forgiving_float(v, 0), 0))


def diag_irradiance(get: Getter) -> str:
    e = _states(get, "input_text.hesc_irradiance_sensor")
    if not (_states(get, "input_boolean.hesc_use_irradiance") == "on" and is_number(_states(get, e))):
        return "unavailable"
    return jinja_str(jinja_round(forgiving_float(_states(get, e), 0), 0))


def diag_charger_solar_mode(get: Getter) -> str:
    m = jinja_str(_states(get, _states(get, "input_text.hesc_charger_mode_entity"))).lower()
    ev = _states(get, "input_text.hesc_charger_eco_value")
    vals = [x.strip() for x in (ev if ev not in BAD else "eco_mode").lower().split(",")]
    sw = _states(get, "input_text.hesc_charger_solar_switch_entity")
    return _onoff(m in vals and (sw in BAD or _states(get, sw) == "on"))


def diag_release_active(get: Getter) -> str:
    return _onoff("Release" in _states(get, "input_text.hesc_state"))


def configuration_valid(get: Getter) -> str:
    ok = True
    fields = ["hesc_ev_connected_sensor", "hesc_ev_power_sensor", "hesc_charger_mode_entity", "hesc_pv_power_sensor", "hesc_forecast_now_sensor"]
    if _states(get, "input_boolean.hesc_standalone") != "on":
        fields += ["hesc_hpvc_enabled_entity", "hesc_hpvc_limited_entity"]
    for f in fields:
        e = _states(get, "input_text." + f).strip()
        if e in BAD or (_states(get, e) == "unknown" and _attr(get, e, "friendly_name") is None):
            ok = False
    return _onoff(ok and _states(get, "input_text.hesc_charger_eco_value").strip() not in BAD)


def prices_available(get: Getter) -> str:
    e = _states(get, "input_text.hesc_price_sensor").strip()
    raw = _attr(get, "sensor.hesc_prices", "raw_today") or []
    return _onoff(e not in BAD and _states(get, e) not in ("unknown", "unavailable") and len(raw) > 0)


# v2 entity id -> function (all read the v2 helper ids, which v3 provides in its states view)
DIAG: dict[str, Callable[[Getter], str]] = {
    "sensor.hesc_diag_pv_power": diag_pv_power,
    "sensor.hesc_diag_ev_power": diag_ev_power,
    "sensor.hesc_diag_forecast_power": diag_forecast_power,
    "sensor.hesc_diag_forecast_cautious": diag_forecast_cautious,
    "sensor.hesc_diag_irradiance": diag_irradiance,
    "binary_sensor.hesc_diag_charger_solar_mode": diag_charger_solar_mode,
    "binary_sensor.hesc_diag_release_active": diag_release_active,
    "binary_sensor.hesc_configuration_valid": configuration_valid,
    "binary_sensor.hesc_prices_available": prices_available,
}


# ---- "check" templates (Settings page): (state, {"missing": text}) --------------------------
def _bad(get: Getter, e: str) -> bool:
    return e in BAD or _attr(get, e, "friendly_name") is None or _states(get, e) == "unavailable"


def check_charger(get: Getter) -> tuple[str, dict[str, Any]]:
    m: list[str] = []
    for t, label in (("input_text.hesc_ev_connected_sensor", "EV connected sensor"),
                     ("input_text.hesc_ev_power_sensor", "charging power sensor"),
                     ("input_text.hesc_charger_mode_entity", "charger mode entity")):
        if _bad(get, _states(get, t).strip()):
            m.append(label)
    if _states(get, "input_text.hesc_charger_eco_value").strip() in BAD:
        m.append("solar mode value")
    return _onoff(not m), {"missing": ", ".join(m)}


def check_sources(get: Getter) -> tuple[str, dict[str, Any]]:
    m: list[str] = []
    if _bad(get, _states(get, "input_text.hesc_pv_power_sensor").strip()):
        m.append("PV power sensor")
    g = _states(get, "input_text.hesc_grid_power_sensor").strip()
    if g not in ("", "unknown") and _bad(get, g):
        m.append("grid power sensor")
    fc = _states(get, "input_text.hesc_forecast_now_sensor").strip()
    fa = _states(get, "input_text.hesc_forecast_attribute").strip()
    if _bad(get, fc) or (fa not in BAD and _attr(get, fc, fa) is None):
        m.append("solar forecast")
    if _states(get, "input_boolean.hesc_standalone") == "off":
        for t in ("input_text.hesc_hpvc_enabled_entity", "input_text.hesc_hpvc_limited_entity"):
            if _bad(get, _states(get, t).strip()) and "HPVC entities" not in m:
                m.append("HPVC entities")
    return _onoff(not m), {"missing": ", ".join(m)}


def check_weather_station(get: Getter) -> tuple[str, dict[str, Any]]:
    m: list[str] = []
    if _states(get, "input_boolean.hesc_use_irradiance") == "on":
        e = _states(get, "input_text.hesc_irradiance_sensor").strip()
        if _bad(get, e) or forgiving_float(_states(get, e), None) is None:
            m.append("irradiance sensor")
    return _onoff(not m), {"missing": ", ".join(m)}


def _gone(get: Getter, e: str) -> bool:
    return e in BAD or _attr(get, e, "friendly_name") is None


def check_charge_plan(get: Getter) -> tuple[str, dict[str, Any]]:
    m: list[str] = []
    ss = _states(get, "input_text.hesc_charger_start_stop_entity").strip()
    gm = _states(get, "input_text.hesc_charger_grid_mode_value").strip()
    if _gone(get, ss) and gm in BAD:
        m.append("start/stop switch or charge-now value")
    rs = _states(get, "input_text.hesc_charger_resume_entity").strip()
    if rs not in ("", "unknown") and _gone(get, rs):
        m.append("back-to-solar entity")
    p = _states(get, "input_text.hesc_price_sensor").strip()
    if _bad(get, p) or len(_attr(get, "sensor.hesc_prices", "raw_today") or []) == 0:
        m.append("price sensor")
    if _bad(get, _states(get, "input_text.hesc_solar_today_sensor").strip()):
        m.append("solar forecast today")
    return _onoff(not m), {"missing": ", ".join(m)}


def check_home_battery_and_ev(get: Getter) -> tuple[str, dict[str, Any]]:
    m: list[str] = []
    if _states(get, "input_boolean.hesc_kick_enabled") == "on":
        def ids(helper: str) -> list[str]:
            return [x.strip() for x in _states(get, helper).strip().split(",") if x.strip() not in BAD]

        def broken(lst: list[str]) -> bool:
            return (not lst or any(_states(get, e) == "unavailable" for e in lst)
                    or any(_attr(get, e, "friendly_name") is None for e in lst))

        if broken(ids("input_text.hesc_home_battery_soc_sensors")):
            m.append("home battery level sensors")
        if broken(ids("input_text.hesc_home_battery_power_sensors")):
            m.append("home battery power sensors")
        if forgiving_float(_states(get, "input_number.hesc_home_battery_kwh"), 0) <= 0:
            m.append("home battery size")
        ss = _states(get, "input_text.hesc_charger_start_stop_entity").strip()
        if _gone(get, ss) or ss.startswith("button."):
            m.append("start/stop switch (Charge plan)")
        if _gone(get, _states(get, "input_text.hesc_charger_resume_entity").strip()):
            m.append("back-to-solar entity (Charge plan)")
    return _onoff(not m), {"missing": ", ".join(m)}


CHECKS: dict[str, Callable[[Getter], tuple[str, dict[str, Any]]]] = {
    "binary_sensor.hesc_check_charger": check_charger,
    "binary_sensor.hesc_check_sources": check_sources,
    "binary_sensor.hesc_check_weather_station": check_weather_station,
    "binary_sensor.hesc_check_charge_plan": check_charge_plan,
    "binary_sensor.hesc_check_home_battery_and_ev": check_home_battery_and_ev,
}


# ---- "HESC notification phones" -----------------------------------------------------------------
def mobile_app_devices(hass: Any) -> list[tuple[Any, Any]]:
    """(name, name_by_user) per device of `integration_entities('mobile_app') | map('device_id') |
    reject('none') | unique`, in HA's own order (copy of HA's integration_entities)."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er
    from homeassistant.helpers.entity import entity_sources

    ent_reg, dev_reg = er.async_get(hass), dr.async_get(hass)
    entities: list[str] = []
    for entry in hass.config_entries.async_entries():
        if entry.title == "mobile_app":
            entities.extend(e.entity_id for e in er.async_entries_for_config_entry(ent_reg, entry.entry_id))
    if not entities:
        entities = [eid for eid, info in entity_sources(hass).items() if info["domain"] == "mobile_app"]
    out: list[tuple[Any, Any]] = []
    seen: set[str] = set()
    for eid in entities:
        ent = ent_reg.async_get(eid)
        d = ent.device_id if ent else None
        if d is None or d in seen:
            continue
        seen.add(d)
        dev = dev_reg.async_get(d)
        out.append((dev.name if dev else None, dev.name_by_user if dev else None))
    return out


def notification_phones(get: Getter, devices: list[tuple[Any, Any]]) -> tuple[str, dict[str, Any]]:
    from homeassistant.util import slugify

    chosen = [x.strip() for x in _states(get, "input_text.hesc_notify_services").split(",")]
    chosen = [x for x in chosen if x != ""]
    names: list[Any] = []
    phones: list[dict[str, Any]] = []
    for name, by_user in devices:
        sv = "notify.mobile_app_" + slugify(str(name))
        shown = by_user or name
        if sv in chosen:
            names.append(shown)
        phones.append({"name": shown, "service": sv, "chosen": sv in chosen})
    other = [c for c in chosen if not c.startswith("notify.mobile_app_")]
    every = names + other
    state = ", ".join(jinja_str(x) for x in every) if every else "none (only inside Home Assistant)"
    return state, {"phones": phones}
