"""Solar forecast source: HESC works with Solcast, with another forecast, or without one.

Design:

* **Solcast** (level A): the ported v2 logic reads Solcast's own format
  (``detailedForecast`` with ``pv_estimate10``); nothing changes.
* **Another forecast** (level B): Open-Meteo Solar Forecast (attribute ``watts`` on its
  day sensors) and Forecast.Solar (action ``forecast_solar.get_forecast``) give a power
  series. It is converted here to Solcast's format, on stand-in entities, so the four
  parts that read a forecast (solar charging, charge plan, kickstart, "solar still to
  come") need no change of their own.
* **No forecast** (level C): HESC is a price planner plus solar charging on measured
  sun. "Forecast now/+30 min" become the measured PV power, or — when an irradiance
  sensor or a lux meter is used — the irradiance thresholds decide alone. The charge
  plan counts no sun (never late), the kickstart is off (it needs the sun left today).

A chosen source that becomes unavailable is *not* "no forecast": HESC then reports the
missing input as before. Only an empty choice is level C.

Everything here only reads a states mapping (entity id -> {"state", "attributes"}) and
returns overrides for it; the same function runs in Home Assistant and in the simulator.
"""
from __future__ import annotations

from bisect import bisect_right
from collections.abc import Mapping
from datetime import datetime, timedelta
from typing import Any

from homeassistant.util import dt as dt_util

from .inputs import js_parse_float

# stand-in entities (never created in HA; they only exist in the logic's view of the states)
SYN_NOW = "sensor.hesc_v3_internal_forecast_now"
SYN_30 = "sensor.hesc_v3_internal_forecast_30m"
SYN_TODAY = "sensor.hesc_v3_internal_forecast_today"
SYN_TOMORROW = "sensor.hesc_v3_internal_forecast_tomorrow"
SYN_IRR = "sensor.hesc_v3_internal_irradiance"
SOURCE = "sensor.hesc_v3_internal_forecast_source"

H_NOW = "input_text.hesc_forecast_now_sensor"
H_30 = "input_text.hesc_forecast_30m_sensor"
H_ATTR = "input_text.hesc_forecast_attribute"
H_TODAY = "input_text.hesc_solar_today_sensor"
H_TOMORROW = "input_text.hesc_solar_tomorrow_sensor"
H_IRR = "input_text.hesc_irradiance_sensor"
H_USE_IRR = "input_boolean.hesc_use_irradiance"
H_PV = "input_text.hesc_pv_power_sensor"
H_PSTART = "input_number.hesc_p_start"

KIND_SOLCAST = "solcast"
KIND_SERIES = "series"
KIND_SENSORS = "sensors"
KIND_NONE = "none"

# Sunlight gives roughly 120 lux per W/m² (ASSUMPTION, to be checked against a real lux meter).
LUX_PER_WM2 = 120.0
_BAD = ("", "unknown", "unavailable", "none", "null")


def _txt(states: Mapping[str, Any], eid: str) -> str:
    v = (states.get(eid) or {}).get("state")
    v = "" if v is None else str(v).strip()
    return "" if v.lower() in _BAD else v


def _attrs(states: Mapping[str, Any], eid: str) -> Mapping[str, Any]:
    if not eid:
        return {}
    return (states.get(eid) or {}).get("attributes") or {}


def _num(v: Any) -> float | None:
    return js_parse_float(v)


def _put(over: dict[str, Any], eid: str, state: Any, attributes: dict[str, Any] | None = None) -> None:
    over[eid] = {"state": "" if state is None else str(state), "attributes": attributes or {}}


def parse_series(*maps: Any) -> dict[datetime, float]:
    """{ISO time: W} maps (Open-Meteo ``watts`` attribute, Forecast.Solar action) -> {datetime: W}."""
    out: dict[datetime, float] = {}
    for m in maps:
        if not isinstance(m, Mapping):
            continue
        for k, v in m.items():
            t = dt_util.parse_datetime(str(k))
            w = _num(v)
            if t is None or w is None:
                continue
            if t.tzinfo is None:
                t = t.replace(tzinfo=dt_util.get_default_time_zone())
            out[t] = w
    return dict(sorted(out.items()))


def power_at(series: Mapping[datetime, float], t: datetime) -> float | None:
    """Power (W) at time t, linear between the points; 0 outside the series (night)."""
    if not series:
        return None
    keys = list(series)
    if t < keys[0] or t > keys[-1]:
        return 0.0
    i = bisect_right(keys, t)
    if i >= len(keys):
        return float(series[keys[-1]])
    a, b = keys[i - 1], keys[i]
    span = (b - a).total_seconds()
    f = (t - a).total_seconds() / span if span else 0.0
    return series[a] + (series[b] - series[a]) * f


_DETAILED_CACHE: dict[tuple[Any, ...], tuple[list[dict[str, Any]], float]] = {}


def detailed(series: Mapping[datetime, float], day: datetime) -> tuple[list[dict[str, Any]], float]:
    """Solcast-style ``detailedForecast`` rows (30 min, kW) for the local day of ``day``, and the day total (kWh).

    The power per half hour is the mean of the start, middle and end of that half hour. The
    other sources have no spread, so pv_estimate10/90 equal pv_estimate.
    """
    start = dt_util.as_local(day).replace(hour=0, minute=0, second=0, microsecond=0)
    key = (start, len(series), next(iter(series), None), next(reversed(series), None), sum(series.values()))
    if key in _DETAILED_CACHE:
        return _DETAILED_CACHE[key]
    rows: list[dict[str, Any]] = []
    total = 0.0
    t = start
    while t.date() == start.date():
        pts = [power_at(series, t + timedelta(minutes=m)) or 0.0 for m in (0, 15, 30)]
        kw = round(sum(pts) / 3 / 1000, 4)
        rows.append({"period_start": t.isoformat(), "pv_estimate": kw, "pv_estimate10": kw, "pv_estimate90": kw})
        total += kw * 0.5
        t = dt_util.as_local(t + timedelta(minutes=30))
    if len(_DETAILED_CACHE) > 64:
        _DETAILED_CACHE.clear()
    _DETAILED_CACHE[key] = (rows, round(total, 2))
    return _DETAILED_CACHE[key]


def _pv_watts(states: Mapping[str, Any]) -> float | None:
    pv = _txt(states, H_PV)
    s = states.get(pv) if pv else None
    if not s:
        return None
    v = _num(s.get("state"))
    if v is None:
        return None
    unit = str((s.get("attributes") or {}).get("unit_of_measurement") or "").lower()
    return v * 1000 if unit == "kw" else (v / 1000 if unit == "mw" else v)


def kind(states: Mapping[str, Any], extra_series: Mapping[datetime, float] | None = None,
         forecast_solar: bool = False) -> str:
    """Which forecast HESC has (by what is chosen in the setup, not by what is available now).

    ``forecast_solar``: the chosen sensors belong to Forecast.Solar; until its series has been
    fetched HESC uses its plain sensors (never mistaken for Solcast)."""
    if forecast_solar:
        return KIND_SERIES if extra_series else KIND_SENSORS
    today = _txt(states, H_TODAY)
    if today and "detailedForecast" in _attrs(states, today):
        return KIND_SOLCAST
    if today and "watts" in _attrs(states, today):
        return KIND_SERIES
    if extra_series:
        return KIND_SERIES
    if today or _txt(states, H_NOW):
        return KIND_SOLCAST if today else KIND_SENSORS
    return KIND_NONE


def overrides(states: Mapping[str, Any], now: datetime,
              extra_series: Mapping[datetime, float] | None = None,
              forecast_solar: bool = False) -> dict[str, dict[str, Any]]:
    """Overrides for the logic's view of the states (empty for Solcast and plain sensors)."""
    over: dict[str, dict[str, Any]] = {}
    k = kind(states, extra_series, forecast_solar)
    _put(over, SOURCE, k)

    # a lux meter in the irradiance field: convert to W/m² (works for every level)
    irr = _txt(states, H_IRR)
    if irr:
        unit = str(_attrs(states, irr).get("unit_of_measurement") or "").lower()
        if unit in ("lx", "lux"):
            lux = _num((states.get(irr) or {}).get("state"))
            _put(over, SYN_IRR, "" if lux is None else round(lux / LUX_PER_WM2, 1), {"unit_of_measurement": "W/m²"})
            _put(over, H_IRR, SYN_IRR)

    if k == KIND_SERIES:
        today, tomorrow = _txt(states, H_TODAY), _txt(states, H_TOMORROW)
        series = dict(extra_series or {}) or parse_series(_attrs(states, today).get("watts"),
                                                          _attrs(states, tomorrow).get("watts"))
        rows_t, kwh_t = detailed(series, now)
        rows_m, kwh_m = detailed(series, now + timedelta(days=1))
        p_now, p_30 = power_at(series, now), power_at(series, now + timedelta(minutes=30))
        _put(over, SYN_TODAY, kwh_t, {"detailedForecast": rows_t, "unit_of_measurement": "kWh"})
        _put(over, SYN_TOMORROW, kwh_m, {"detailedForecast": rows_m, "unit_of_measurement": "kWh"})
        _put(over, SYN_NOW, "" if p_now is None else round(p_now), {"unit_of_measurement": "W"})
        _put(over, SYN_30, "" if p_30 is None else round(p_30), {"unit_of_measurement": "W"})
        for helper, syn in ((H_TODAY, SYN_TODAY), (H_TOMORROW, SYN_TOMORROW), (H_NOW, SYN_NOW), (H_30, SYN_30)):
            _put(over, helper, syn)
        _put(over, H_ATTR, "")
    elif k == KIND_SENSORS:
        if not _txt(states, H_30):
            _put(over, H_30, _txt(states, H_NOW))  # no "+30 min" sensor: use "now" for both
        if forecast_solar:  # its day sensors have no series: the plan and kickstart see none (yet)
            _put(over, H_TODAY, "")
            _put(over, H_TOMORROW, "")
    elif k == KIND_NONE:
        use_irr = (states.get(H_USE_IRR) or {}).get("state") == "on"
        irr_now = _num((over.get(SYN_IRR) or states.get(_txt(states, H_IRR)) or {}).get("state")) if irr else None
        if use_irr and irr_now is not None:
            # the irradiance thresholds decide alone: the forecast test always passes
            value: float | None = _num((states.get(H_PSTART) or {}).get("state")) or 2000
        else:
            value = _pv_watts(states)
        _put(over, SYN_NOW, "" if value is None else round(value), {"unit_of_measurement": "W"})
        _put(over, SYN_30, "" if value is None else round(value), {"unit_of_measurement": "W"})
        _put(over, H_NOW, SYN_NOW)
        _put(over, H_30, SYN_30)
        _put(over, H_ATTR, "")
    return over
