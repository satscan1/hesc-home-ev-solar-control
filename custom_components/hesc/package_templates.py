"""Two v2.0.0 package template sensors the battery-level and kickstart parts read, as Python.

- "HESC EV battery backup sensor" (`sensor.hesc_ev_battery_backup_sensor`): another battery sensor
  (%, device class battery) on a device with the same car name as the device of the battery-level
  sensor from the settings. Every 10 minutes and at start.
- "HESC solar still to come today" (`sensor.hesc_solar_still_to_come_today`): the cautious forecast
  from now to the end of the day, in kWh.

Proven identical to the original templates rendered by Home Assistant
(`tests/integration/test_package_templates.py`).
"""
from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from datetime import datetime, timedelta
from typing import Any

from .templatecompat import as_datetime, forgiving_float, jinja_round, jinja_str

_KEYS = {"estimate": "pv_estimate", "estimate10": "pv_estimate10", "estimate90": "pv_estimate90"}


def _norm(name: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", jinja_str(name).lower())


def backup_sensor(
    main_id: str,
    battery_sensors: Iterable[str],
    device_id: Callable[[str], str | None],
    device_name: Callable[[str | None], Any],
) -> str:
    """State of the template: the first other battery sensor on a device of the same car, or 'none'.

    battery_sensors: entity ids of `sensor.*` states with device class battery and unit %, sorted by
    entity id (as `states.sensor` iterates). device_name(d): name_by_user or name (None when missing).
    """
    m = (main_id or "").strip()
    md = device_id(m) if m not in ("", "unknown", "unavailable") else None
    car = _norm((device_name(md) if md else "") or "")
    if len(car) < 3:
        return "none"
    for ent in battery_sensors:
        d = device_id(ent)
        if d and d != md:
            n = _norm(device_name(d) or "")
            if len(n) >= 3 and (car in n or n in car):
                return ent
    return "none"


def backup_device(prev_state: str | None, device_id: Callable[[str], str | None], device_name: Callable[[str | None], Any]) -> str:
    """Attribute `device`: the device name of the sensor found at the previous evaluation (`this.state`)."""
    b = prev_state if prev_state is not None else "none"
    d = device_id(b) if b.startswith("sensor.") else None
    if not d:
        return ""
    name = device_name(d)
    return "" if name is None else jinja_str(name)


def solar_remaining(get: Callable[[str], Any], now: datetime) -> str:
    """State of "HESC solar still to come today" ('unavailable' when the forecast has no detailedForecast).

    get(entity_id) -> (state, attributes) or None.
    """
    def states(e: str) -> str:
        s = get(e)
        return "unknown" if s is None else s[0]

    def state_attr(e: str, a: str) -> Any:
        s = get(e)
        return None if s is None else s[1].get(a)

    src = states("input_text.hesc_solar_today_sensor")
    rows = state_attr(src, "detailedForecast")
    if rows is None:
        return "unavailable"
    key = _KEYS.get(states("input_text.hesc_forecast_attribute"), "pv_estimate10")
    k = 0.0
    for p in rows or []:
        ps = p.get("period_start") if isinstance(p, dict) else None
        s = as_datetime(ps) if isinstance(ps, str) else ps
        e = s + timedelta(minutes=30)
        if e > now:
            frac = min((e - max(s, now)).total_seconds() / 1800, 1)
            k = k + forgiving_float(p.get(key) if isinstance(p, dict) else None, 0) * 0.5 * frac
    return jinja_str(jinja_round(k, 1))
