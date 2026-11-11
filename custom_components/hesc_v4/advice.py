"""Start threshold advice from the own history (+ apply automatically), and the seasonal start threshold.

Line-by-line ports of v2.0.0's Node-RED function nodes "Advice: when to run" (gate: 90 s after
start, daily after 21:35, when the auto switch changes, and when the published sensor is gone)
and "Start threshold advice (+ auto apply)" (method A: sun share; method B: lasting sessions;
auto: one step of at most 200 W per 7 days), plus v2's package automations "HESC - Seasonal
start threshold" and "HESC - Auto advice and seasonal threshold exclude each other".
The two nodes are proven identical to the originals on random runs
(`tests/integration/test_advice_parity.py`); the seasonal values against HA's own template
engine (`tests/integration/test_advice_seasonal.py`).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .advisor import (
    _date_parse,
    _fmt_w,
    _get,
    _is_num,
    _parse_line,
    _round,
    _s,
    _truthy,
)
from .inputs import js_parse_float
from .jscompat import UNDEFINED, iso, js_json, js_round

DAY = 86400000
WINDOW, LASTING, MERGE_MIN, NEED_SESS, NEED_DAYS = 30, 20, 5, 8, 5
MIN_W, MAX_W, STEP, MIN_DIFF, WAIT_DAYS, HOLD_PCT = 1000, 3500, 200, 100, 7, 0.75
WINDOW_MAX, WINDOW_MIN_SESS = 60, 15
SUN_TARGET, SUN_WINDOW, SUN_NEED = 0.70, 8, 15
SENSOR = "sensor.hesc_advice_threshold"
_DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec")  # ICU en-GB


# ---- "Advice: when to run" ---------------------------------------------------------

def gate(S: dict[str, Any], context: dict[str, Any], now: int, tz: str) -> tuple[str | None, dict[str, Any]]:
    """One tick of the gate (v2 runs it with every input round). Returns (topic or None, node context).
    tz: the time zone Node-RED runs in (Home Assistant's)."""
    auto = (S.get("input_boolean.hesc_advice_auto") or {}).get("state") == "on"
    d = datetime.fromtimestamp(now / 1000, ZoneInfo(tz))
    today = d.strftime("%Y-%m-%d")
    after = d.hour * 60 + d.minute >= 21 * 60 + 35
    G = dict(context.get("G") or {"day": "", "auto": None, "startup": now, "ran": False})
    why = ""
    if G.get("auto") is not None and auto != G.get("auto"):
        why = "switch"
    if not G.get("ran") and now - G["startup"] > 90000:
        why = why or "start"
    if after and G.get("day") != today:
        why = why or "daily"
        G["day"] = today
    if not why and not S.get(SENSOR) and now - (G.get("missingAt") or 0) > 600000 and now - G["startup"] > 90000:
        why = "missing"
        G["missingAt"] = now
    G["auto"] = auto
    if why:
        G["ran"] = True
    return (why or None), {**context, "G": G}


# ---- "Start threshold advice (+ auto apply)" ---------------------------------------

@dataclass
class Result:
    out1: dict[str, Any] | None = None  # history line {payload: JSON text} (advice_applied)
    msgs: list[dict[str, Any]] = field(default_factory=list)  # out2: HA API calls (set_value + sensor)
    flow: dict[str, Any] = field(default_factory=dict)  # flow context after (hescNoticeP3)

    def sensor(self) -> dict[str, Any]:
        """The published sensor.hesc_advice_threshold as a state object."""
        data = self.msgs[-1]["payload"]["data"]
        return {"state": data["state"], "attributes": dict(data["attributes"])}

    def set_values(self) -> list[tuple[str, float]]:
        return [(m["payload"]["data"]["entity_id"], m["payload"]["data"]["value"]) for m in self.msgs
                if m["payload"]["path"] == "/api/services/input_number/set_value"]


def _r50(v: float) -> Any:
    return _round(v / 50) * 50


def _clamp(v: float) -> float:
    return min(MAX_W, max(MIN_W, v))


def _en_gb_day(ms: float, tz: str) -> str:
    """new Date(t).toLocaleDateString('en-GB', {timeZone, weekday: 'short', day: 'numeric', month: 'short'})"""
    if math.isnan(ms) or abs(ms) > 8.64e15:
        return "Invalid Date"
    d = datetime.fromtimestamp(ms / 1000, ZoneInfo(tz))
    return f"{_DAYS[d.weekday()]} {d.day} {_MONTHS[d.month - 1]}"


def _time(v: Any) -> float:
    """new Date(v).getTime() for a value from the history (string, number or other)."""
    if _is_num(v):
        return float(v) if abs(v) <= 8.64e15 else math.nan
    return _date_parse(v)


def _slice10(v: Any) -> str:
    if not isinstance(v, str):
        raise TypeError("start.slice is not a function")  # the node throws here
    return v[:10]


def _share(arr: list[dict[str, float]]) -> float | None:
    e = 0.0
    for x in arr:
        e += x["ev"]
    if not e > 0:
        return None
    s = 0.0
    for x in arr:
        s += x["sun"]
    return s / e


def _sort_by(rows: list[Any], key) -> list[Any]:
    """Array.prototype.sort with (a, b) => key(a) - key(b): stable; NaN differences count as equal."""
    from functools import cmp_to_key

    def cmp(a: Any, b: Any) -> int:
        d = key(a) - key(b)
        return 0 if math.isnan(d) else (-1 if d < 0 else (1 if d > 0 else 0))
    return sorted(rows, key=cmp_to_key(cmp))


def run(S: dict[str, Any], history_text: Any, topic: str | None, flow: dict[str, Any], now: int,
        floor_w: float | None = None, limited_only: bool = False) -> Result:
    """Since rc3: ``floor_w`` = the charger's start level (charger_specs.py).
    The advice never goes below it: a lower threshold only gives releases the charger cannot use.
    None = no floor (v2 behaviour, used by the parity tests).

    Since 3.0.0: ``limited_only`` = only learn from solar sessions that started while HPVC limited
    the panels. Only then did the start threshold decide anything (the release request); sessions
    the charger started on surplus by itself say nothing about the threshold. Without HPVC
    (standalone) there is no advice. False = v2 behaviour (all sessions, parity tests)."""
    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    tz = pa.get("tz") if _truthy(pa.get("tz")) else "Europe/Amsterdam"

    def st(i: str) -> Any:
        return S[i].get("state", UNDEFINED) if S.get(i) else UNDEFINED

    def num(i: str, d: float) -> float:
        v = js_parse_float(st(i)) if st(i) is not UNDEFINED else None
        return d if v is None else v

    def fmt(v: float) -> str:
        return _fmt_w(v)

    flow = dict(flow)
    rows: list[Any] = []
    for line in _s("" if history_text is None or history_text is UNDEFINED else history_text).split("\n"):
        if not line.strip():
            continue
        try:
            rows.append(_parse_line(line))
        except ValueError:
            pass

    def typ(r: Any) -> Any:
        if r is None:
            raise TypeError("Cannot read properties of null")  # the node throws here
        return _get(r, "type")

    def pick(w: int) -> tuple[list[Any], list[dict[str, Any]]]:
        since = now - w * DAY
        eco = []
        for r in rows:
            if typ(r) != "eco_charge":
                continue
            start, ctx = _get(r, "start"), _get(r, "start_ctx")
            if not _truthy(start) or not _truthy(ctx) or _get(r, "forced_start") is True or not _is_num(_get(r, "minutes")):
                continue
            if limited_only and not _truthy(_get(ctx, "hpvc_limited")):
                continue
            if _time(start) > since:
                eco.append(r)
        eco = _sort_by(eco, lambda r: _time(r["start"]))
        merged: list[dict[str, Any]] = []
        for r in eco:
            s0 = _time(r["start"])
            e0 = s0 + r["minutes"] * 60000
            last = merged[-1] if merged else None
            if last and s0 - last["end"] <= MERGE_MIN * 60000:
                last["end"] = max(last["end"], e0)
                last["minutes"] = (last["end"] - last["start"]) / 60000
            else:
                merged.append({"start": s0, "end": e0, "minutes": r["minutes"], "fc": _get(r["start_ctx"], "fc_now"),
                               "day": _slice10(r["start"])})
        return eco, merged

    win = WINDOW
    eco, merged = pick(win)
    if len(merged) < WINDOW_MIN_SESS:
        win = WINDOW_MAX
        eco, merged = pick(win)
    good = [m for m in merged if m["minutes"] >= LASTING and _is_num(m["fc"]) and math.isfinite(m["fc"])]
    fcs = sorted(m["fc"] for m in good)
    days = len({m["day"] for m in good})
    enough = len(good) >= NEED_SESS and days >= NEED_DAYS
    q25 = fcs[math.floor((len(fcs) - 1) * 0.25)] if fcs else None
    sun_rows = []
    for r in eco:
        ev, green, fc = _get(r, "ev_wh"), _get(r, "ev_green_kwh"), _get(r["start_ctx"], "fc_now")
        if _is_num(ev) and ev > 200 and _is_num(green) and _is_num(fc):
            sun_rows.append({"fc": fc, "ev": ev / 1000, "sun": min(green, ev / 1000), "day": _slice10(r["start"])})
    sun_rows = _sort_by(sun_rows, lambda x: x["fc"])
    sun_days = len({x["day"] for x in sun_rows})
    sun_adv = None
    if len(sun_rows) >= SUN_NEED and sun_days >= NEED_DAYS:
        for k in range(len(sun_rows) - SUN_WINDOW + 1):
            sh = _share(sun_rows[k:k + SUN_WINDOW])
            if sh is not None and sh >= SUN_TARGET:
                sun_adv = sun_rows[k]["fc"]
                break
        if sun_adv is None:
            sun_adv = MAX_W
    method = "sun_share" if sun_adv is not None else "lasting"
    adv_raw = sun_adv if sun_adv is not None else (q25 if enough else None)
    adv_start = None if adv_raw is None else _clamp(math.floor(adv_raw / 50) * 50)
    floor = None if floor_w is None else math.ceil(floor_w / 50) * 50
    floored = adv_start is not None and floor is not None and adv_start < floor
    if floored:
        adv_start = floor
    sun_above = None if adv_start is None else _share([x for x in sun_rows if x["fc"] >= adv_start])
    sun_below = None if adv_start is None else _share([x for x in sun_rows if x["fc"] < adv_start])
    adv_hold = None if adv_start is None else _r50(adv_start * HOLD_PCT)
    if limited_only and st("input_boolean.hesc_standalone") == "on":  # no HPVC: the threshold steers no start
        adv_start = adv_hold = sun_above = sun_below = None
        floored = False

    cur_start, cur_hold = num("input_number.hesc_p_start", 2000), num("input_number.hesc_p_hold", 1500)
    auto = st("input_boolean.hesc_advice_auto") == "on"
    seasonal = st("input_boolean.hesc_seasonal_threshold") == "on"
    applied = _sort_by([r for r in rows if typ(r) == "advice_applied"], lambda r: -_time(_get(r, "ts")))
    last_change = applied[0] if applied else None
    next_allowed = _time(_get(last_change, "ts")) + WAIT_DAYS * DAY if last_change is not None else 0
    diff = 0 if adv_start is None else adv_start - cur_start

    res = Result(flow=flow)
    new_start = new_hold = None
    msgs: list[dict[str, Any]] = []

    def step() -> Any:
        v = _r50(cur_start + math.copysign(1, diff) * min(STEP, abs(diff)))
        return v if floor is None else max(floor, v)  # rc3: the floor holds for every step too

    enough_any = adv_start is not None
    standalone = limited_only and st("input_boolean.hesc_standalone") == "on"
    if standalone:
        status = "No advice without HPVC: the start threshold only decides when HPVC limits your panels."
    elif not enough_any and limited_only:
        status = (f"Collecting: {len(good)} of {NEED_SESS} good solar sessions that started while HPVC limited your panels,"
                  f" on {days} of {NEED_DAYS} days. Only those say something about the start threshold.")
    elif not enough_any:
        status = f"Collecting: {len(good)} of {NEED_SESS} good solar sessions, on {days} of {NEED_DAYS} days."
    elif abs(diff) < MIN_DIFF:
        status = "Your start threshold fits your own history."
    elif not auto:
        status = f"Advice: {'raise' if diff > 0 else 'lower'} the start threshold to {fmt(adv_start)}. You decide (auto is off)."
        if floored:
            status += f" Not lower: your charger only starts from {fmt(floor)}."
    elif now < next_allowed:
        status = f"Next step ({fmt(cur_start)} → {fmt(step())}) from {_en_gb_day(next_allowed, tz)}."
    else:
        new_start = _clamp(step()) if floor is None else max(floor, _clamp(step()))  # floor may lie above MAX_W
        new_hold = _r50(new_start * HOLD_PCT)
        status = f"Changed now: {fmt(cur_start)} → {fmt(new_start)} (hold {fmt(new_hold)})."
        for eid, v in (("input_number.hesc_p_start", new_start), ("input_number.hesc_p_hold", new_hold)):
            msgs.append({"payload": {"protocol": "http", "method": "post", "path": "/api/services/input_number/set_value",
                                     "data": {"entity_id": eid, "value": v}}})
        res.out1 = {"payload": js_json({"ts": iso(now), "type": "advice_applied", "from": {"start": cur_start, "hold": cur_hold},
                                        "to": {"start": new_start, "hold": new_hold}, "advised": adv_start,
                                        "sessions": len(good), "days": days})}
        flow["hescNoticeP3"] = {"text": f"Start threshold {fmt(cur_start)} → {fmt(new_start)} (from your history)", "at": now, "prio": 3}
    if last_change is not None:
        frm, to = _get(last_change, "from"), _get(last_change, "to")
        lc = f"{_en_gb_day(_time(_get(last_change, 'ts')), tz)}: {fmt(_get(frm, 'start'))} → {fmt(_get(to, 'start'))}"
    else:
        lc = "today" if new_start is not None else None
    attrs: dict[str, Any] = {"friendly_name": "HESC advised start threshold", "icon": "mdi:auto-fix"}
    if adv_start is not None:
        attrs["unit_of_measurement"] = "W"
    attrs.update({
        "status_text": status, "advised_start": adv_start, "advised_hold": adv_hold,
        "current_start": new_start if new_start is not None else cur_start,
        "current_hold": new_hold if new_hold is not None else cur_hold,
        "good_sessions": len(good), "all_sessions": len(merged), "days": days, "need_sessions": NEED_SESS, "need_days": NEED_DAYS,
        "window_days": win, "lowest_good_forecast": fcs[0] if fcs else None,
        "median_good_forecast": fcs[math.floor((len(fcs) - 1) / 2)] if fcs else None,
        "auto": auto, "seasonal": seasonal, "method": method, "sun_sessions": len(sun_rows),
        "sun_share_above": None if sun_above is None else js_round(sun_above * 100),
        "sun_share_below": None if sun_below is None else js_round(sun_below * 100),
        "sun_target": js_round(SUN_TARGET * 100), "last_change": lc,
        "next_step_from": iso(next_allowed) if (auto and enough_any and abs(diff) >= MIN_DIFF and new_start is None
                                                 and now < next_allowed) else None,
        "run": topic if _truthy(topic) else None, "updated": iso(now),
    })
    if floor is not None:
        attrs["charger_start_floor"] = floor
    msgs.append({"payload": {"protocol": "http", "method": "post", "path": "/api/states/" + SENSOR,
                             "data": {"state": "collecting" if adv_start is None else _s(adv_start), "attributes": attrs}}})
    res.msgs = msgs
    return res


# ---- package automations -----------------------------------------------------------

def seasonal_thresholds(month: int) -> tuple[int, int]:
    """'HESC - Seasonal start threshold': start per month, hold = 75 % rounded to 50 W.
    Jinja's round() is Python's round() (half to even), as in Home Assistant."""
    p_start = 2500 if month in (6, 7) else 2000 if month in (4, 5, 8, 9) else 1500 if month in (3, 10) else 1200
    return p_start, int(round(p_start * 0.75 / 50, 0) * 50)


def seasonal_actions(S: dict[str, Any], month: int, floor_w: float | None = None) -> list[tuple[str, float]]:
    """The set_value calls of the automation (only when switched on and the value differs)."""
    if (S.get("input_boolean.hesc_seasonal_threshold") or {}).get("state") != "on":
        return []
    out = []
    start, hold = seasonal_thresholds(month)
    if floor_w is not None and start < floor_w:  # rc3: never below the charger's start level
        start = int(math.ceil(floor_w / 50) * 50)
        hold = int(round(start * 0.75 / 50, 0) * 50)
    for eid, v in zip(("input_number.hesc_p_start", "input_number.hesc_p_hold"), (start, hold)):
        cur = js_parse_float((S.get(eid) or {}).get("state"))
        if (0.0 if cur is None or not math.isfinite(cur) else cur) != float(v):
            out.append((eid, float(v)))
    return out


# 'HESC - Auto advice and seasonal threshold exclude each other': switching one on turns the other off.
EXCLUSIVE = {"advice_auto": "seasonal_threshold", "seasonal_threshold": "advice_auto"}
