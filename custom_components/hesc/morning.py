"""Morning summary to the chosen phones.

Line-by-line ports of v2.0.0's Node-RED function nodes "Morning summary: when" (every minute) and
"Morning summary (phone)" (with the history file as input). Proven identical to the original
nodes on random cases (`tests/integration/test_morning_parity.py`).
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .jscompat import UNDEFINED, js_number_str, js_round, js_to_fixed
from .price_forecast import date_parse

BAD = ("unknown", "unavailable", "none", "")
_TIME = re.compile(r"^([0-9]{1,2}):([0-9]{2})$")
_JS_NUM = re.compile(r"^[+-]?(Infinity|(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?)$", re.ASCII)


def _s(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return js_number_str(v)
    if v is None:
        return "null"
    if v is UNDEFINED:
        return "undefined"
    return str(v)


def _truthy(v: Any) -> bool:
    if v is None or v is False or v is UNDEFINED:
        return False
    if isinstance(v, (int, float)):
        return not (v == 0 or math.isnan(v))
    if isinstance(v, str):
        return v != ""
    return True


def _js_number(v: Any) -> float:
    """JavaScript Number() for a state text."""
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return 0.0
    if v is UNDEFINED:
        return math.nan
    s = str(v).strip()
    if s == "":
        return 0.0
    if not _JS_NUM.match(s):
        return math.nan
    return float(s.replace("Infinity", "inf"))


def _round_s(v: float) -> str:
    """String(Math.round(v)), NaN included."""
    return "NaN" if math.isnan(v) else _s(js_round(v))


def _tz(S: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    return (pa.get("tz") or "Europe/Amsterdam"), pa


def due(S: dict[str, Any], context: dict[str, Any], now: int) -> tuple[bool, dict[str, Any]]:
    """v2 "Morning summary: when": (send now?, node context)."""
    ctx = dict(context)

    def st(i: str) -> Any:
        return S[i].get("state") if i in S else UNDEFINED

    if st("input_boolean.hesc_morning_summary") != "on":
        return False, ctx
    t = st("input_select.hesc_morning_summary_time")
    t = "" if not _truthy(t) else _s(t)
    m = _TIME.match(t)
    if not m:
        return False, ctx
    tz, _ = _tz(S)
    loc = datetime.fromtimestamp(now / 1000, ZoneInfo(tz))
    mins, at = loc.hour * 60 + loc.minute, int(m.group(1)) * 60 + int(m.group(2))
    today = loc.strftime("%Y-%m-%d")
    if mins < at or mins > at + 60:
        return False, ctx
    if ctx.get("sent") == today:
        return False, ctx
    ctx["sent"] = today
    return True, ctx


def summary(S: dict[str, Any], history: str, now: int) -> tuple[list[str], str | None]:  # noqa: C901
    """v2 "Morning summary (phone)": (notify services, message); message None = no phones chosen."""
    def st(i: str) -> Any:
        return S[i].get("state") if i in S else UNDEFINED

    def at(i: str, a: str) -> Any:
        if i in S and S[i].get("attributes") is not None:
            return S[i]["attributes"].get(a, UNDEFINED)
        return UNDEFINED

    def num(i: str, d: Any) -> Any:
        v = st(i)
        from .inputs import js_parse_float

        x = js_parse_float(v)
        return x if x is not None and math.isfinite(x) else d

    def n1(v: float) -> str:
        return js_to_fixed(js_round(v * 10) / 10, 1)

    tz, pa = _tz(S)
    sym = pa.get("symbol") or "€"
    after = _s(pa.get("symbol_after")) == "true" if pa.get("symbol_after") is not None else False
    dec = "." if pa.get("decimal") == "." else ","

    def eur(v: float) -> str:
        s = js_to_fixed(v, 2).replace(".", dec, 1)
        return s + " " + sym if after else sym + ("" if dec == "." else " ") + s

    raw = st("input_text.hesc_notify_services")
    services = [x.strip() for x in ("" if not _truthy(raw) else _s(raw)).split(",")]
    services = [s for s in services if re.match(r"^notify\.", s)]
    if not services:
        return [], None
    zone = ZoneInfo(tz)

    def day_str(ms: float) -> str:
        if math.isnan(ms):
            raise ValueError("Invalid time value")  # JS RangeError
        return datetime.fromtimestamp(ms / 1000, zone).strftime("%Y-%m-%d")

    yesterday = day_str(now - 86400000)
    lines: list[str] = []
    soc = st("sensor.hesc_ev_soc")
    conn = at("sensor.hesc_ev_soc", "connected")
    est = at("sensor.hesc_ev_soc", "estimated")
    if soc is UNDEFINED or soc is None or soc in BAD:
        level = "level unknown"
    else:
        level = _round_s(_js_number(soc)) + " %" + (" (estimated)" if _truthy(est) else "")
    lines.append("EV " + level + " · " + ("plugged in" if _truthy(conn) else "not plugged in"))

    plan: Any = None
    p = at("sensor.hesc_charge_plan", "plan")
    try:
        plan = json.loads(p) if isinstance(p, str) else p
    except ValueError:
        pass
    if isinstance(plan, dict) and _truthy(plan.get("deadline_text")):
        line = "Plan " + _s(plan["deadline_text"]) + " → " + _s(plan.get("goal", UNDEFINED)) + " %"
        need, grid = plan.get("need_kwh"), plan.get("grid_kwh_needed")
        if not _truthy(plan.get("active")):
            line += " (off)"
        elif isinstance(need, (int, float)) and not isinstance(need, bool) and need > 0:
            line += " · needs " + n1(need) + " kWh" + (", " + n1(grid) + " from grid"
                                                      if isinstance(grid, (int, float)) and not isinstance(grid, bool) and grid > 0 else ", all from sun")
        else:
            line += " · already reached"
        lines.append(line)
    else:
        lines.append("No charge plan")

    if st("input_boolean.hesc_vacation") == "on":
        u = st("input_datetime.hesc_vacation_until")
        vs = S.get("input_boolean.hesc_vacation")
        lc = vs.get("last_changed") if vs else None
        since = day_str(lc.timestamp() * 1000 if isinstance(lc, datetime) else date_parse(lc)) if vs else ""
        until = ""
        if _truthy(u) and isinstance(u, str) and u > since:
            until = " until " + "-".join(list(reversed(u.split("-")))[:2])
        lines.append("Holiday mode on · week plan paused" + until)

    sun = num("sensor.hesc_solar_still_to_come_today", None)
    if sun is not None:
        lines.append("Sun today ± " + n1(sun) + " kWh")

    days = at("sensor.hesc_charging_costs", "days")
    days = days if isinstance(days, list) else []
    y = next((d for d in days if isinstance(d, list) and d and d[0] == yesterday), None)
    if y and (y[1] + y[2]) > 0.05:
        all_in = st("input_boolean.hesc_costs_all_in") == "on"
        mk = 0 if all_in else num("input_number.hesc_costs_markup", 0)
        vat = 0 if all_in else num("input_number.hesc_costs_vat", 0)
        grid_c = ((y[3] if _truthy(y[3]) else 0) + y[2] * mk) * (1 + vat / 100)
        sunv = y[1] * num("input_number.hesc_feed_in_price", 0)
        tot = y[1] + y[2]
        lines.append("Yesterday " + n1(tot) + " kWh · " + _round_s(100 * y[1] / tot) + " % sun · " + eur(grid_c + sunv))
    else:
        lines.append("Yesterday not charged")

    g = None
    for ln in (history or "").split("\n"):
        if '"charge_plan"' not in ln or '"goal_' not in ln:
            continue
        try:
            r = json.loads(ln)
            if _truthy(r.get("deadline")) and day_str(date_parse(r["deadline"]) if isinstance(r["deadline"], str)
                                                       else _js_number(r["deadline"])) == yesterday:
                g = r
        except (ValueError, AttributeError, TypeError, OverflowError, OSError):
            pass
    if g:
        ev = g.get("event")
        if ev == "goal_check" and _truthy(g.get("ok")):
            lines.append("Goal yesterday reached (" + _round_s(_js_number(g.get("soc", UNDEFINED))) + " % of " + _s(g.get("goal", UNDEFINED)) + " %)")
        elif ev in ("goal_missed", "goal_check"):
            soc_g = g.get("soc", UNDEFINED)
            lines.append("Goal yesterday missed (" + ("?" if soc_g is None else _round_s(_js_number(soc_g))) + " % of " + _s(g.get("goal", UNDEFINED)) + " %)")
        elif ev == "goal_unknown":
            lines.append("Goal yesterday not confirmed (no battery level)")
    return services, "\n".join(lines)


def messages(services: list[str], message: str) -> list[dict[str, Any]]:
    """The HA API posts v2 sends (one per phone)."""
    return [{"payload": {"protocol": "http", "method": "post", "path": "/api/services/notify/" + s[7:],
                         "data": {"title": "HESC · Morning summary", "message": message}}} for s in services]
