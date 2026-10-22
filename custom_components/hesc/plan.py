"""Charge plan: when must the EV be ready, and which quarters charge from the grid.

Line-by-line port of v2.0.0's template sensor "HESC charge plan" (`sensor.hesc_charge_plan`:
state = ready-by time, attribute `plan` = the plan as JSON) and of "HESC expected charge
cost" (`sensor.hesc_planned_cost`). Runs on Home Assistant's own date helpers, so the
result is the same as v2's template. Proven against the original templates on random
inputs (`tests/integration/test_plan_parity.py`).
"""
from __future__ import annotations

import json
import math
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from homeassistant.util import dt as dt_util

from .templatecompat import as_datetime, as_timestamp, forgiving_float, jinja_round, sort_by

Getter = Callable[[str], "tuple[str, dict[str, Any]] | None"]
WDS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_BAD = ("", "unknown", "unavailable")

def _tojson(v: Any) -> str:
    """Jinja's built-in `tojson` (sorted keys, HTML-safe), which v2's template uses."""
    from jinja2.utils import htmlsafe_json_dumps

    return str(htmlsafe_json_dumps(v, sort_keys=True))


def _states(get: Getter, entity_id: str) -> str:
    st = get(entity_id) if entity_id else None
    return "unknown" if st is None else st[0]


def _attr(get: Getter, entity_id: str, name: str) -> Any:
    st = get(entity_id) if entity_id else None
    return None if st is None else st[1].get(name)


def _is_on(get: Getter, entity_id: str) -> bool:
    return _states(get, entity_id) == "on"


def _is_number(v: Any) -> bool:
    try:
        f = float(v)
    except (ValueError, TypeError):
        return False
    return math.isfinite(f)


def _today_at(hhmm: str) -> datetime:
    today = dt_util.start_of_local_day()
    if not hhmm:
        return today
    t = dt_util.parse_time(hhmm)
    if t is None:
        raise ValueError(f"could not convert str to datetime: '{hhmm}'")
    return datetime.combine(today, t, today.tzinfo)


# since 3.0.0 (skip one day of the plan, e.g. a day off): one date on
# which the repeating plan does nothing; the plan itself stays as it is. Not in v2.
SKIP_HELPER = "input_datetime.hesc_rep_skip"


def next_repeating(get: Getter, now: datetime, skip: str = "") -> datetime | None:
    """The next ready-by time of the repeating plan after `now` (its days and time only), leaving out
    the day `skip` (YYYY-MM-DD). v2 looks 8 days ahead; with a skipped day 15 are needed, which gives
    the same result whenever nothing is skipped."""
    rb = _today_at(_states(get, "input_select.hesc_rep_time"))
    for i in range(15):
        d = rb + timedelta(days=i)
        if d > now and _is_on(get, "input_boolean.hesc_rep_" + WDS[d.weekday()].lower()) and d.date().isoformat() != skip:
            return d
    return None


def deadline(get: Getter) -> tuple[datetime, str, str, bool, bool]:
    """(ready-by time, source, chosen goal, one-off active, repeating active). Raises like the template."""
    now = dt_util.now()
    day = _states(get, "input_select.hesc_plan_day")
    base = _today_at(_states(get, "input_select.hesc_plan_time"))
    if day == "Today":
        off = 0
    elif day == "Tomorrow":
        off = 1
    elif day in WDS:
        off = (WDS.index(day) - now.weekday()) % 7
        if off == 0 and base <= now:
            off = 7
    else:
        off = 1
    fx_ts = forgiving_float(_attr(get, "input_datetime.hesc_plan_deadline", "timestamp"), 0)
    if fx_ts > (now.timestamp() - 400 * 86400):
        one_dl0 = dt_util.as_local(as_datetime(fx_ts))  # type: ignore[arg-type]
    else:
        one_dl0 = base + timedelta(days=off)
    if one_dl0 <= now:
        wk = int(jinja_round((now.timestamp() - as_timestamp(one_dl0)) / 604800, 0, "floor")) + 1  # type: ignore[operator]
    else:
        wk = 0
    one_dl = one_dl0 + timedelta(days=7 * wk)
    rp = next_repeating(get, now, skip=_states(get, SKIP_HELPER)[:10])
    one_on = _is_on(get, "input_boolean.hesc_plan_enabled") and one_dl > now
    rep_on = _is_on(get, "input_boolean.hesc_rep_enabled") and not _is_on(get, "input_boolean.hesc_vacation") and rp is not None
    if rep_on and (not one_on or rp < one_dl):  # type: ignore[operator]
        return rp, "repeating", _states(get, "input_select.hesc_rep_goal"), one_on, rep_on  # type: ignore[return-value]
    return one_dl, "one-off", _states(get, "input_select.hesc_plan_goal"), one_on, rep_on


def state(get: Getter) -> str:
    """State of sensor.hesc_charge_plan ('unknown' when the template fails)."""
    try:
        return deadline(get)[0].isoformat()
    except Exception:  # noqa: BLE001 - the template renders nothing then
        return "unknown"


def compute(get: Getter) -> dict[str, Any]:
    """The plan (attribute `plan`, as a dict). Raises where the template fails."""
    now = dt_util.now()
    dl, src, goal_sel, one_on, rep_on = deadline(get)
    soc_txt = _states(get, "input_text.hesc_ev_soc_sensor").strip()
    soc_e = "sensor.hesc_ev_soc" if (soc_txt not in _BAD and _is_number(_states(get, "sensor.hesc_ev_soc"))) else soc_txt
    soc = forgiving_float(_states(get, soc_e), -1) if soc_e not in _BAD else -1
    goal = forgiving_float(goal_sel.replace("%", ""), 80)
    cap = forgiving_float(_states(get, "input_number.hesc_ev_battery_kwh"), 0)
    kw = forgiving_float(_states(get, "input_number.hesc_plan_charge_kw"), 11)
    need_kwh = max(goal - soc, 0) / 100 * cap if (soc >= 0 and cap > 10) else 0
    pstart = forgiving_float(_states(get, "input_number.hesc_p_start"), 2000)
    phold = forgiving_float(_states(get, "input_number.hesc_p_hold"), 1500)
    kwh = 0.0
    phase = ""
    for se in (_states(get, "input_text.hesc_solar_today_sensor").strip(), _states(get, "input_text.hesc_solar_tomorrow_sensor").strip()):
        if se in _BAD:
            continue
        for r in (_attr(get, se, "detailedForecast") or []):
            t = as_datetime(r["period_start"])
            e = t + timedelta(minutes=30)  # type: ignore[operator]
            v = forgiving_float(r.get("pv_estimate10"), 0) * 1000
            if v >= pstart:
                phase = "go"
            elif v >= phold and phase:
                phase = "hold"
            else:
                phase = ""
            if phase and e > now and t < dl:  # type: ignore[operator]
                s0 = t if t > now else now  # type: ignore[operator]
                e0 = e if e < dl else dl
                frac = max((e0 - s0).total_seconds() / 1800, 0)
                kwh = kwh + min(max(v / 1000 - 0.4, 0), kw) * 0.5 * frac
    solar_kwh = min(kwh, need_kwh)
    grid_kwh = max(need_kwh - solar_kwh, 0)
    n = int(jinja_round(grid_kwh / (kw * 0.25), 0, "ceil")) if kw > 0 else 0
    a = _attr(get, "sensor.hesc_prices", "raw_today") or []
    b = _attr(get, "sensor.hesc_prices", "raw_tomorrow") or []
    items: list[dict[str, Any]] = []
    last = None
    for p in list(a) + list(b):
        last = p["end"]
        pe = as_datetime(p["end"])
        if pe > now and pe <= dl:  # type: ignore[operator]
            items.append({"start": p["start"], "end": p["end"], "value": p["value"], "sort": p["value"], "fc": False})
    fcs = _attr(get, "sensor.hesc_price_forecast", "forecast") or []
    pen = forgiving_float(_attr(get, "sensor.hesc_price_forecast", "penalty"), 0.02)
    fc_last = None
    for p in fcs:
        pe = as_datetime(p["end"])
        if (last is None or as_datetime(p["start"]) >= as_datetime(last)) and pe > now and pe <= dl:  # type: ignore[operator]
            items.append({"start": p["start"], "end": p["end"], "value": p["value"], "sort": p["value"] + pen, "fc": True})
            fc_last = p["end"]
    pick = sort_by(sort_by(items, "sort")[:n], "start")
    pf = [as_datetime(p["start"]).isoformat() for p in pick if p["fc"]]  # type: ignore[union-attr]
    pl = [as_datetime(p["start"]).isoformat() for p in pick]  # type: ignore[union-attr]
    avg = jinja_round(sum(p["value"] for p in pick) / len(pick) * 100, 1) if pick else None
    fit_kwh = min(grid_kwh, len(pick) * kw * 0.25)
    hrs = fit_kwh / kw if kw > 0 else 0
    return {
        "soc": jinja_round(soc, 1) if soc >= 0 else None, "goal": int(goal), "need_kwh": jinja_round(need_kwh, 1),
        "solar_kwh": jinja_round(solar_kwh, 1), "grid_kwh": jinja_round(fit_kwh, 1), "grid_kwh_needed": jinja_round(grid_kwh, 1),
        "quarters": len(pick), "quarters_needed": n, "short_of_time": n > len(pick),
        "charge_time": "%d:%02d" % (int(hrs), int(hrs * 60) % 60), "kw": kw, "avg_price_ct": avg,
        "planned": pl, "prices_complete": (last is not None and as_datetime(last) >= dl),  # type: ignore[operator]
        "prices_until": as_datetime(last).isoformat() if last is not None else None,  # type: ignore[union-attr]
        "planned_forecast": pf,
        "forecast_until": as_datetime(fc_last).isoformat() if fc_last is not None else None,  # type: ignore[union-attr]
        "deadline": dl.isoformat(), "source": src, "active": one_on or rep_on, "deadline_text": dl.strftime("%a %d-%m %H:%M"),
    }


def sensor(get: Getter) -> tuple[str, dict[str, Any]]:
    """State and attributes of v2's sensor.hesc_charge_plan (attribute `plan` is JSON text, as in v2)."""
    try:
        plan_txt: Any = _tojson(compute(get))
    except Exception:  # noqa: BLE001 - the template renders nothing then
        plan_txt = None
    return state(get), {"plan": plan_txt}


def _plan_dict(get: Getter) -> dict[str, Any]:
    raw = _attr(get, "sensor.hesc_charge_plan", "plan")
    p = json.loads(raw) if isinstance(raw, str) else raw
    return p or {}


def planned_cost(get: Getter, prev_state: str | None) -> tuple[str, dict[str, Any]]:
    """State and attributes of v2's sensor.hesc_planned_cost ("HESC expected charge cost").

    prev_state: this sensor's state before the update (v2's `display` uses `this.state`).
    """
    p = _plan_dict(get)
    if p.get("active") and not _states(get, "input_text.hesc_plan_status").startswith("EV already charging"):
        allin = _is_on(get, "input_boolean.hesc_costs_all_in")
        mk = 0 if allin else forgiving_float(_states(get, "input_number.hesc_costs_markup"), 0)
        vat = 0 if allin else forgiving_float(_states(get, "input_number.hesc_costs_vat"), 0)
        g = forgiving_float(p.get("grid_kwh"), 0)
        st = str(jinja_round((g * forgiving_float(p.get("avg_price_ct"), 0) / 100 + g * mk) * (1 + vat / 100), 2))
    else:
        st = "0"
    dc = _attr(get, "sensor.hesc_prices", "decimal") or ","
    aft = _attr(get, "sensor.hesc_prices", "symbol_after")
    amt = ("%.2f" % forgiving_float(prev_state if prev_state is not None else "unknown", 0)).replace(".", dc)
    sym = _attr(get, "sensor.hesc_prices", "symbol") or "€"
    display = (amt + " " + sym) if aft else (sym + ("" if dc == "." else " ") + amt)
    attrs = {
        "display": display,
        "grid_kwh": jinja_round(forgiving_float(p.get("grid_kwh"), 0), 1),
        "avg_price_ct": p.get("avg_price_ct"),
        "ready_by": p.get("deadline_text") if p.get("active") else "no active plan",
        "partly_expected_prices": len(p.get("planned_forecast") or []) > 0,
    }
    return st, attrs


def fixed_deadline(day: str, time_str: str) -> datetime:
    """v2 automation "Fix one-off charge plan deadline": the ready-by time for a chosen day and time.

    Raises ValueError for an unusable time, like the template.
    """
    now = dt_util.now()
    base = _today_at(time_str)
    if day == "Today":
        off = 0
    elif day == "Tomorrow":
        off = 1
    elif day in WDS:
        off = (WDS.index(day) - now.weekday()) % 7
        if off == 0 and base <= now:
            off = 7
    else:
        off = 1
    # v2 stores it in an input_datetime (whole seconds, local time)
    return (base + timedelta(days=off)).replace(microsecond=0)
