"""Setting advice from the recent history (the Advisor).

Line-by-line port of v2.0.0's Node-RED function node "HESC Advisor" (daily, and before every
report). It reads the history file (only the last `window` days) and turns it into plain-language
advice on the start/hold threshold (from all solar sessions of the current way of working:
standalone or with HPVC), the wait for the charger to start, failed real releases, how good the
forecast is and, when switched on, the weather-station thresholds. It only advises: it never
changes a setting. It notes when the start threshold advice moves by 200 W or more (shown for a
week) and publishes a one-line summary to input_text.hesc_advice only when that line changes.
Proven identical to the original node on random multi-tick runs
(`tests/integration/test_advisor_parity.py`).
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .inputs import js_parse_float
from .jscompat import UNDEFINED, iso, js_number_str, js_round
from .price_forecast import date_parse

LASTING = 20  # an Eco session counts as "lasting" from 20 minutes
MINDAYS = 7  # advice on the start threshold only after sessions on this many different days
TARGET = 0.6  # a start threshold is good when at least 60% of the sessions it lets start keep charging 20 min
DAY_MS = 86400000

# String.prototype.trim(): ECMAScript WhiteSpace and LineTerminator characters.
_JS_WS = "\t\n\v\f\r \u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
_JS_DEC = re.compile(r"^[+-]?(Infinity|(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?)$", re.ASCII)
_JS_RADIX = re.compile(r"^0([xX][0-9a-fA-F]+|[oO][0-7]+|[bB][01]+)$", re.ASCII)


@dataclass
class Result:
    advice: dict[str, Any]  # global hescAdvice / msg.advice
    out1_passes: bool  # out1 is the msg (+ msg.advice) to the report builder; False for topic 'advice'
    out2: list[dict[str, Any]] = field(default_factory=list)  # HA actions (only when the line changed)
    flow: dict[str, Any] = field(default_factory=dict)  # the node's flow context after this run
    status: str = ""  # node.status text


# ---- JavaScript semantics the node relies on ----

def _is_num(v: Any) -> bool:
    """typeof v === 'number'"""
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _truthy(v: Any) -> bool:
    if v is None or v is False or v is UNDEFINED:
        return False
    if _is_num(v):
        return not (v == 0 or math.isnan(v))
    if isinstance(v, str):
        return v != ""
    return True


def _s(v: Any) -> str:
    """String(v)"""
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    if isinstance(v, bool):
        return "true" if v else "false"
    if _is_num(v):
        return js_number_str(v)
    if isinstance(v, list):
        return ",".join("" if x is None or x is UNDEFINED else _s(x) for x in v)
    if isinstance(v, dict):
        return "[object Object]"
    return str(v)


def _num(v: Any) -> float:
    """ToNumber(v), as used by the relational operators and arithmetic."""
    if v is UNDEFINED:
        return math.nan
    if v is None or v is False:
        return 0.0
    if v is True:
        return 1.0
    if _is_num(v):
        return float(v)
    if isinstance(v, dict):
        return math.nan
    s = _s(v).strip(_JS_WS)
    if s == "":
        return 0.0
    m = _JS_RADIX.match(s)
    if m:
        return float(int(m.group(1)[1:], {"x": 16, "o": 8, "b": 2}[m.group(1)[0].lower()]))
    if not _JS_DEC.match(s):
        return math.nan
    return float(s.replace("Infinity", "inf"))


def _get(o: Any, k: str) -> Any:
    """o[k] for a parsed JSON value that is known not to be null/undefined."""
    return o.get(k, UNDEFINED) if isinstance(o, dict) else UNDEFINED


def _round(x: float) -> Any:
    """Math.round, keeping JavaScript's -0 for -0.5 <= x < 0."""
    r = js_round(x)
    if r == 0 and (x < 0 or (x == 0 and math.copysign(1.0, x) < 0)):
        return -0.0
    return r


def _ceil(x: float) -> Any:
    """Math.ceil (null counts as 0)."""
    if x is None:
        return 0
    if not math.isfinite(x):
        return x
    r = math.ceil(x)
    return -0.0 if r == 0 and x < 0 else r


def _r100(v: float) -> Any:
    return _round(v / 100) * 100


def _fmt_w(v: float) -> str:
    """Math.round(v).toLocaleString('en-US') + ' W'"""
    r = _round(v)
    if isinstance(r, float):
        if math.isnan(r):
            return "NaN W"
        if math.isinf(r):
            return ("∞" if r > 0 else "-∞") + " W"
        if r == 0:
            return ("-0" if math.copysign(1.0, r) < 0 else "0") + " W"
        r = int(r)
    return f"{r:,} W"


def _qn(a: list[Any], p: float) -> Any:
    s = sorted(x for x in a if _is_num(x) and math.isfinite(x))
    if not s:
        return None
    return s[min(len(s) - 1, max(0, js_round(p * (len(s) - 1))))]


def _date_parse(v: Any) -> float:
    """Date.parse(v) for the ISO texts the history holds (other values: NaN)."""
    if isinstance(v, str):
        return date_parse(v)
    return math.nan


def _nl_date(ms: float, tz: str) -> str:
    """new Date(ms).toLocaleDateString('nl-NL', {timeZone})"""
    if math.isnan(ms) or abs(ms) > 8.64e15:
        return "Invalid Date"
    d = datetime.fromtimestamp(ms / 1000, ZoneInfo(tz))
    return f"{d.day}-{d.month}-{d.year}"


def _nl_day_month_time(ms: float, tz: str) -> str:
    """new Date(ms).toLocaleString('nl-NL', {timeZone, day, month, hour, minute: '2-digit'})"""
    return datetime.fromtimestamp(ms / 1000, ZoneInfo(tz)).strftime("%d-%m, %H:%M")


def _slice16(s: str, n: int) -> str:
    """s.slice(0, n): JavaScript counts UTF-16 code units."""
    if all(ord(c) < 0x10000 for c in s):
        return s[:n]
    return s.encode("utf-16-le", "surrogatepass")[: 2 * n].decode("utf-16-le", "surrogatepass")


def _no_constant(name: str) -> Any:
    raise ValueError(name)  # JSON.parse has no NaN / Infinity


def _parse_line(line: str) -> Any:
    return json.loads(line, parse_int=float, parse_constant=_no_constant)


def run(S: dict[str, Any], history_text: str, topic: str | None, flow: dict[str, Any], now_ms: int,
        limited_only: bool = False) -> Result:
    """One run of the node. S: states in Node-RED form; history_text: msg.payload; topic: msg.topic.
    Since 3.0.0: ``limited_only`` = the start threshold item only learns from solar sessions that
    started while HPVC limited the panels (the only ones the threshold decided); no threshold
    advice without HPVC. False = v2 behaviour (parity tests)."""
    flow = dict(flow)
    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    tz = pa.get("tz") if _truthy(pa.get("tz")) else "Europe/Amsterdam"

    def st(i: str) -> Any:
        return S[i].get("state", UNDEFINED) if _truthy(S.get(i, UNDEFINED)) else UNDEFINED

    def num(i: str, d: float) -> float:
        v = js_parse_float(st(i)) if st(i) is not UNDEFINED else None
        return d if v is None else v

    now = now_ms
    WINDOW = max(7, num("input_number.hesc_advice_window_days", 30))
    MINRUNS = max(3, num("input_number.hesc_advice_min_runs", 8))
    cur = {"pStart": num("input_number.hesc_p_start", 2000), "pHold": num("input_number.hesc_p_hold", 1500),
           "tStart": num("input_number.hesc_t_start", 10),
           "irrStart": num("input_number.hesc_irr_start", 220), "irrHold": num("input_number.hesc_irr_hold", 160)}
    irr_sensor = st("input_text.hesc_irradiance_sensor")
    use_irr = (st("input_boolean.hesc_use_irradiance") == "on" and _truthy(irr_sensor)
               and irr_sensor not in ("unknown", "unavailable", ""))
    since = now - WINDOW * DAY_MS

    # ---- parse (only the window: the advice follows the season) ----
    rows: list[dict[str, Any]] = []
    for line in _s(history_text if _truthy(history_text) else "").split("\n"):
        if not line.strip(_JS_WS):
            continue
        try:
            r = _parse_line(line)
        except (ValueError, RecursionError):
            continue
        if r is None:
            continue  # r.start throws: skipped
        if not isinstance(r, dict):
            continue  # Date.parse(undefined) is NaN
        v = r.get("start", UNDEFINED)
        if not _truthy(v):
            v = r.get("slot_start", UNDEFINED)
        if not _truthy(v):
            v = r.get("ts", UNDEFINED)
        if _date_parse(v) >= since:
            rows.append(r)

    def ctx(r: dict[str, Any]) -> Any:
        return r.get("start_ctx", UNDEFINED)

    def has_fc(r: dict[str, Any]) -> bool:
        c = ctx(r)
        return _truthy(c) and _is_num(_get(c, "fc_now"))

    def is_forced(r: dict[str, Any]) -> bool:
        if r.get("forced_start", UNDEFINED) is True:
            return True
        if r.get("forced_start", UNDEFINED) is not UNDEFINED or not has_fc(r):
            return False
        c = r["start_ctx"]
        return _is_num(_get(c, "pv")) and c["fc_now"] < cur["pHold"] and c["pv"] < cur["pHold"]

    def minutes(r: dict[str, Any]) -> float:
        return _num(r.get("minutes", UNDEFINED))

    eco = [r for r in rows if r.get("type") == "eco_charge" and not is_forced(r)]
    lasting = [r for r in eco if minutes(r) >= LASTING and has_fc(r)]
    live = [r for r in rows if r.get("type") == "release" and not _truthy(r.get("shadow", UNDEFINED)) and r.get("reason") != "EV full"]
    live_ok = [r for r in live if _truthy(r.get("ev_started", UNDEFINED))]
    acc_rows = [r for r in rows if r.get("type") == "accuracy"
                and _num(r.get("hpvc_limited_share") if _truthy(r.get("hpvc_limited_share", UNDEFINED)) else 0) < 0.1
                and _num(r.get("fc_w", UNDEFINED)) > 50]

    items: list[dict[str, Any]] = []
    summary = ""

    # 1. start / hold threshold — from ALL solar sessions of the current way of working
    standalone_now = st("input_boolean.hesc_standalone") == "on"

    def mode_of(r: dict[str, Any]) -> bool:
        c = ctx(r)
        if _truthy(c) and isinstance(_get(c, "standalone"), bool):
            return c["standalone"]
        return not (_truthy(c) and _truthy(_get(c, "hpvc_on")))

    mode_label = "standalone" if standalone_now else "with HPVC"
    mode_rows = [r for r in eco if has_fc(r) and mode_of(r) == standalone_now]
    if limited_only:
        mode_label = "started while HPVC limited"
        mode_rows = [] if standalone_now else [r for r in mode_rows if _truthy(_get(r["start_ctx"], "hpvc_limited"))]

    def day_key(r: dict[str, Any]) -> str:
        v = r.get("start", UNDEFINED)
        if not _truthy(v):
            v = r.get("ts", UNDEFINED)
        return _nl_date(_date_parse(v), tz)

    n_days = len({day_key(r) for r in mode_rows})

    def push_threshold(p: float, measured: str, basis: str) -> bool:
        h = _r100(p * 0.8)
        same = abs(p - cur["pStart"]) < 200
        items.append({"key": "p_start", "title": "Start and hold threshold", "status": "ok" if same else "advice", "basis": basis,
                      "measured": measured,
                      "advice": ("Keep the start threshold at " + _fmt_w(cur["pStart"]) + "." if same else
                                 "Set the start threshold to " + _fmt_w(p) + " and the hold threshold to " + _fmt_w(h)
                                 + " (now " + _fmt_w(cur["pStart"]) + " / " + _fmt_w(cur["pHold"]) + ")."),
                      "value": {"p_start": p, "p_hold": h}})
        return same

    n_mode = len(mode_rows)
    if limited_only and standalone_now:
        items.append({"key": "p_start", "title": "Start and hold threshold", "status": "ok",
                      "measured": "Standalone (no HPVC).",
                      "advice": "No advice without HPVC: the start threshold only decides when HPVC limits your panels."})
        summary = "No start threshold advice without HPVC"
    elif n_mode >= MINRUNS and n_days >= MINDAYS:
        def at(p: float) -> dict[str, Any]:
            a = [r for r in mode_rows if r["start_ctx"]["fc_now"] >= p]
            lc = len([r for r in a if minutes(r) >= LASTING])
            return {"n": len(a), "l": lc, "share": lc / len(a) if a else 0}

        now0 = at(cur["pStart"])
        p: Any = cur["pStart"]
        if now0["n"] and now0["share"] < 0.5:
            cands: list[Any] = []
            for r in mode_rows:
                c = _r100(r["start_ctx"]["fc_now"]) + 0  # a Set stores -0 as +0
                if c not in cands:
                    cands.append(c)
            for c in sorted(x for x in cands if x > cur["pStart"]):
                x = at(c)
                if x["n"] >= 3 and x["share"] >= TARGET:
                    p = min(8000, c)
                    break
        lost_good = len([r for r in mode_rows if minutes(r) >= LASTING and r["start_ctx"]["fc_now"] < p])
        avoided_short = len([r for r in mode_rows if minutes(r) < LASTING and r["start_ctx"]["fc_now"] < p])
        same = push_threshold(p, _s(n_mode) + " solar sessions on " + _s(n_days) + " days (" + mode_label + "). " + _s(now0["l"]) + " of "
                              + _s(now0["n"]) + " kept charging for " + _s(LASTING) + " minutes or more."
                              + (" At " + _fmt_w(p) + ", " + _s(avoided_short) + " short sessions would not have started, but also "
                                 + _s(lost_good) + " good ones." if p != cur["pStart"] else ""), "sessions")
        summary = (("Start threshold fits (" + _fmt_w(cur["pStart"]) + ")") if same else
                   ("Start " + _fmt_w(p) + " (now " + _fmt_w(cur["pStart"]) + ")")) + ": " + _s(now0["l"]) + " of " + _s(now0["n"]) + " sessions kept charging"
    else:
        runs_txt = (_s(n_mode) + " solar sessions (enough)") if n_mode >= MINRUNS else (_s(n_mode) + " of " + _s(MINRUNS) + " solar sessions")
        items.append({"key": "p_start", "title": "Start and hold threshold", "status": "waiting",
                      "measured": runs_txt + ", on " + _s(n_days) + " of " + _s(MINDAYS) + " days (" + mode_label + ").",
                      "advice": ("No advice yet. HESC learns from the solar sessions that started while HPVC limited your panels, because only then does the start threshold decide anything; advice appears once enough of them, on enough different days, are collected."
                                 if limited_only else
                                 "No advice yet. HESC learns from the solar sessions of the way you work now; advice appears once enough of them, on enough different days, are collected.")})
        summary = "Collecting data: " + (_s(n_mode) + " solar sessions" if n_mode >= MINRUNS else _s(n_mode) + " of " + _s(MINRUNS) + " solar sessions") + ", " + _s(n_days) + " of " + _s(MINDAYS) + " days"

    # 2. wait for the charger — only real (non-shadow) releases show the charger's start delay
    delays = [v for v in (r.get("start_delay_min", UNDEFINED) for r in live_ok) if _is_num(v)]
    if len(delays) >= max(3, js_round(MINRUNS / 2)):
        q90 = _ceil(_qn(delays, 0.9))
        t = min(30, max(3, q90 + 2))
        same = abs(t - cur["tStart"]) <= 1
        items.append({"key": "t_start", "title": "Wait for the charger to start", "status": "ok" if same else "advice",
                      "measured": "After " + _s(len(delays)) + " releases the charger started within " + _s(q90) + " minutes in 9 of 10 cases.",
                      "advice": "Keep " + _s(cur["tStart"]) + " minutes." if same else "Set the wait time to " + _s(t) + " minutes (now " + _s(cur["tStart"]) + ").",
                      "value": {"t_start": t}})
    else:
        items.append({"key": "t_start", "title": "Wait for the charger to start", "status": "waiting",
                      "measured": _s(len(delays)) + " releases with a measured start so far." if live else "Only measurable with shadow mode off (real releases).",
                      "advice": "No advice yet."})

    # 3. failed real releases — the start threshold is too low if many releases do not lead to charging
    if len(live) >= max(3, js_round(MINRUNS / 2)):
        share = len(live_ok) / len(live)
        if share < 0.5:
            items.append({"key": "fails", "title": "Releases without charging", "status": "advice",
                          "measured": "Only " + _s(len(live_ok)) + " of " + _s(len(live)) + " releases led to charging.",
                          "advice": "Raise the start threshold to " + _fmt_w(_r100(cur["pStart"] * 1.15)) + ".",
                          "value": {"p_start": _r100(cur["pStart"] * 1.15)}})
        else:
            items.append({"key": "fails", "title": "Releases without charging", "status": "ok",
                          "measured": _s(len(live_ok)) + " of " + _s(len(live)) + " releases led to charging.", "advice": "No change needed."})

    # 4. forecast reliability (all daylight intervals, not curtailed)
    if len(acc_rows) >= MINRUNS * 12:
        ratio = _qn([100 * _num(r.get("pv_w", UNDEFINED)) / _num(r["fc_w"]) for r in acc_rows], 0.5)
        rv = 0 if ratio is None else ratio  # null counts as 0
        status, adv = "ok", "The forecast fits well. No change needed."
        if rv < 85:
            status, adv = "info", "The forecast is on the optimistic side here. Keep deciding on the cautious estimate (estimate10); the threshold advice above is already based on it."
        elif rv > 115:
            status, adv = "info", "The forecast is on the pessimistic side here. The threshold advice above already takes this into account."
        items.append({"key": "forecast", "title": "How good is the forecast?", "status": status,
                      "measured": "Actual solar power was on average " + _s(_round(rv)) + "% of the forecast (" + _s(_round(len(acc_rows) / 4)) + " hours of daylight measured).",
                      "advice": adv})
    else:
        items.append({"key": "forecast", "title": "How good is the forecast?", "status": "waiting",
                      "measured": _s(_round(len(acc_rows) / 4)) + " of " + _s(_round(MINRUNS * 3)) + " hours of daylight measured.", "advice": "No advice yet."})

    # 5. weather station (only when switched on)
    if use_irr:
        li = [r for r in lasting if _is_num(_get(r["start_ctx"], "irr"))]
        if len(li) >= MINRUNS:
            q = _qn([r["start_ctx"]["irr"] for r in li], 0.25)
            i = _round((0 if q is None else q) / 10) * 10
            same = abs(i - cur["irrStart"]) < 30
            ih = _round(i * 0.75 / 10) * 10
            items.append({"key": "irr", "title": "Weather station thresholds", "status": "ok" if same else "advice",
                          "measured": "Most lasting solar sessions started with " + _s(i) + " W/m² or more.",
                          "advice": "Keep " + _s(cur["irrStart"]) + " W/m²." if same else "Set irradiance to start to " + _s(i) + " W/m² and to hold to "
                          + _s(ih) + " W/m² (now " + _s(cur["irrStart"]) + " / " + _s(cur["irrHold"]) + ").",
                          "value": {"irr_start": i, "irr_hold": ih}})
        else:
            items.append({"key": "irr", "title": "Weather station thresholds", "status": "waiting",
                          "measured": _s(len(li)) + " of " + _s(MINRUNS) + " solar sessions with irradiance collected.", "advice": "No advice yet."})

    # ---- change tracking: the advice follows the season, so note when it moves ----
    prev = flow.get("hescAdvicePrev")
    if not _truthy(prev):
        prev = {}
    p_now = next((x["value"] for x in items if x["key"] == "p_start" and "value" in x), None)
    prev_p = _get(prev, "p_start")
    if p_now and _truthy(prev_p) and abs(p_now["p_start"] - _num(prev_p)) >= 200:
        flow["hescAdviceChange"] = {"text": "The start threshold advice moved from " + _fmt_w(_num(prev_p)) + " to " + _fmt_w(p_now["p_start"]) + " on "
                                    + _nl_date(now, tz) + ". This is normal when the season changes.", "at": now}
    if p_now and (not _truthy(prev_p) or abs(p_now["p_start"] - _num(prev_p)) >= 200):
        flow["hescAdvicePrev"] = {"p_start": p_now["p_start"], "at": now}
    chg = flow.get("hescAdviceChange")
    changed = _get(chg, "text") if (_truthy(chg) and now - _num(_get(chg, "at")) < 7 * DAY_MS) else None  # shown for a week
    advice = {"generated": iso(now), "window_days": WINDOW, "min_runs": MINRUNS, "items": items, "summary": summary, "changed": changed,
              "counts": {"eco": len(eco), "lasting": len(lasting), "live": len(live), "accuracy_hours": _round(len(acc_rows) / 4)}}

    # ---- publish (only on change) ----
    out2: list[dict[str, Any]] = []
    line = _slice16(summary + " · last " + _s(WINDOW) + " days", 255)
    last = flow.get("hescAdviceLine", UNDEFINED)
    if _truthy(S.get("input_text.hesc_advice", UNDEFINED)) and last != line:
        flow["hescAdviceLine"] = line
        out2.append({"payload": {"action": "input_text.set_value", "target": {"entity_id": ["input_text.hesc_advice"]}, "data": {"value": line}}})
        if _truthy(S.get("input_text.hesc_advice_updated", UNDEFINED)):
            out2.append({"payload": {"action": "input_text.set_value", "target": {"entity_id": ["input_text.hesc_advice_updated"]},
                                     "data": {"value": _nl_day_month_time(now, tz)}}})
    return Result(advice=advice, out1_passes=topic != "advice", out2=out2, flow=flow, status=_slice16(summary, 60))
