"""Charging costs: sun / grid into the EV, grid priced per quarter, plus the CSV export.

Line-by-line ports of v2.0.0's Node-RED function nodes "Charging costs (sun / grid)" (every
input round), "Load charging costs" / "Start with empty charging costs" (at start) and "Export
charging costs (CSV)" (button). Day totals per local day: [sun kWh, grid kWh, grid cost (raw),
grid kWh without price]. Proven identical to the original nodes on random runs
(`tests/integration/test_costs_parity.py`).
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .inputs import js_parse_float
from .jscompat import UNDEFINED, iso, js_json, js_number_str, js_to_fixed

BAD = ("unknown", "unavailable", "none", "")
DAY = 86400000
COLUMNS = ["date", "sun_kwh", "grid_kwh", "grid_cost_raw", "grid_kwh_without_price"]


def _s(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return js_number_str(v)
    return str(v)


def _truthy(v: Any) -> bool:
    """JavaScript truthiness (objects and arrays are always true)."""
    if v is None or v is False or v is UNDEFINED:
        return False
    if isinstance(v, (int, float)):
        return not (v == 0 or math.isnan(v))
    if isinstance(v, str):
        return v != ""
    return True


def _r(v: Any, d: int) -> float:
    """+Number(v || 0).toFixed(d)"""
    x = v if isinstance(v, (int, float)) and not isinstance(v, bool) and v and not math.isnan(v) else 0
    return float(js_to_fixed(x, d))


def _money(pa: dict[str, Any]) -> tuple[str, str, str, bool]:
    sym = pa.get("symbol") or "€"
    cur = pa.get("currency") or "EUR"
    after = _s(pa.get("symbol_after")) == "true" if pa.get("symbol_after") is not None else False
    dec = "." if pa.get("decimal") == "." else ","
    return sym, cur, dec, after


def load(text: str | None) -> dict[str, Any]:
    """v2 "Load charging costs" (file read) or "Start with empty charging costs" (no file: text None)."""
    if text is None:
        return {"version": 1, "days": {}}
    try:
        c = json.loads(text)
    except ValueError:
        c = None
    if not isinstance(c, dict) or not _truthy(c.get("days")):
        c = {"version": 1, "days": {}}
    return c


@dataclass
class Result:
    save: str | None = None  # charging_costs.json (None = not written)
    publish: dict[str, Any] | None = None  # sensor.hesc_charging_costs {"state", "attributes"}
    costs: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    status: str = ""
    ran: bool = True


def run(S: dict[str, Any], costs: dict[str, Any] | None, context: dict[str, Any], now: int, tz: str) -> Result:
    """One run of "Charging costs (sun / grid)". costs: flow hescCosts (None = not loaded yet);
    tz: the time zone Node-RED runs in (HA's)."""
    res = Result()
    ctx = dict(context)
    if costs is None:
        res.ran, res.context = False, ctx
        return res

    def st(i: Any) -> Any:
        return S[i].get("state") if i and i in S else UNDEFINED

    def attr(i: Any, a: str) -> Any:
        if i and i in S and S[i].get("attributes") is not None:
            return S[i]["attributes"].get(a, UNDEFINED)
        return UNDEFINED

    def num(v: Any) -> float | None:
        return js_parse_float(v)

    def txt(i: str) -> str:
        v = st(i)
        return "" if (v is UNDEFINED or v is None or v in BAD) else _s(v).strip()

    def low(v: Any) -> str:
        return ("" if (v is None or v is UNDEFINED or v == "" or v is False or v == 0) else _s(v)).lower()

    def pw(i: str) -> float | None:
        v = num(st(i))
        if v is None:
            return None
        u = low(attr(i, "unit_of_measurement"))
        return v * 1000 if u == "kw" else (v * 1e6 if u == "mw" else v)

    zone = ZoneInfo(tz)

    def day_key(t: float) -> str:
        return datetime.fromtimestamp(t / 1000, zone).strftime("%Y-%m-%d")

    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    sym, _cur, dec, after = _money(pa)

    def amt(v: float, d: int = 2) -> str:
        s = js_to_fixed(v, d).replace(".", dec, 1)
        return s + " " + sym if after else sym + ("" if dec == "." else " ") + s

    C = json.loads(js_json(costs)) if costs else {"version": 1, "days": {}}
    last = ctx.get("lastTs") or 0
    ctx["lastTs"] = now
    dt = (now - last) / 1000 if last else 0
    if dt <= 0 or dt > 120:
        dt = 0

    ev_id = txt("input_text.hesc_ev_power_sensor")
    grid_id = txt("input_text.hesc_grid_power_sensor")
    ev_min = num(st("input_number.hesc_ev_active_w")) or 400
    ev = max(0, pw(ev_id) or 0)
    grid_raw = pw(grid_id)
    grid = None if grid_raw is None else (-grid_raw if st("input_boolean.hesc_grid_export_positive") == "on" else grid_raw)
    price = num(st("sensor.hesc_prices"))
    k = day_key(now)
    days = C.setdefault("days", {})
    if not _truthy(days.get(k)):
        days[k] = [0, 0, 0, 0]
    if ev >= ev_min and dt > 0:
        g_w = ev if grid is None else min(ev, max(grid, 0))
        s_w = ev - g_w
        gk, sk = g_w * dt / 3.6e6, s_w * dt / 3.6e6
        d = days[k]
        d[0] += sk
        d[1] += gk
        if price is not None:
            d[2] += gk * price
        else:
            d[3] += gk
        ctx["dirty"] = True
    res.costs = C

    last_pub = ctx.get("lastPub") or 0
    last_day = ctx.get("lastDay") or ""
    if not (now - last_pub >= 300000 or last_day != k):
        res.context = ctx
        return res
    ctx["lastPub"], ctx["lastDay"] = now, k

    cutoff = day_key(now - 1100 * DAY)
    for key in sorted(days):
        if key < cutoff:
            del days[key]
    kept = sorted(days)
    since100 = day_key(now - 100 * DAY)
    recent = [[x] + [_r(v, 3) for v in days[x]] for x in kept if x >= since100]
    months: dict[str, list[float]] = {}
    for x in kept:
        m = x[:7]
        months.setdefault(m, [0, 0, 0, 0])
        for i in range(4):
            months[m][i] += days[x][i]
    month_list = [[m] + [_r(v, 3) for v in months[m]] for m in sorted(months)]
    t = days[k]
    if ctx.get("dirty"):
        res.save = js_json(C)
    ctx["dirty"] = False
    res.publish = {"state": _s(_r(t[0] + t[1], 2)), "attributes": {
        "friendly_name": "HESC charging costs", "unit_of_measurement": "kWh", "icon": "mdi:cash-multiple",
        "since": kept[0] if kept else k, "updated": iso(now),
        "today": [k] + [_r(v, 3) for v in t],
        "days": recent, "months": month_list, "columns": list(COLUMNS)}}
    res.status = k + " · sun " + _s(_r(t[0], 1)) + " · grid " + _s(_r(t[1], 1)) + " kWh · " + amt(_r(t[2], 2), 2)
    res.context = ctx
    return res


def export(S: dict[str, Any], costs: dict[str, Any] | None, now: int, folder: str) -> tuple[list[tuple[str, str]], str]:
    """v2 "Export charging costs (CSV)": ([(file name, text)], info text). Files go to `folder`."""
    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    tz = pa.get("tz") or "Europe/Amsterdam"
    _sym, cur, dec_mark, _after = _money(pa)

    def num(i: str, d: float) -> float:
        s = S.get(i)
        v = js_parse_float(s.get("state")) if s else None
        return v if v is not None and math.isfinite(v) else d

    stamp = datetime.fromtimestamp(now / 1000, ZoneInfo(tz)).strftime("%d-%m %H:%M")
    if not costs or not costs.get("days"):
        return [], ("Export " + stamp + " · no charging costs counted yet")[:250]
    all_in = (S.get("input_boolean.hesc_costs_all_in") or {}).get("state") == "on"
    markup, vat, feed_in = num("input_number.hesc_costs_markup", 0), num("input_number.hesc_costs_vat", 0), num("input_number.hesc_feed_in_price", 0)

    def dec(v: float, n: int) -> str:
        return js_to_fixed(v, n).replace(".", dec_mark, 1)

    sep = ";" if dec_mark == "," else ","

    def row(label: str, d: list[float]) -> str:
        grid = d[2] if all_in else (d[2] + markup * d[1]) * (1 + vat / 100)
        sun = d[0] * feed_in
        return sep.join([label, dec(d[0], 2), dec(d[1], 2), dec(d[3], 2), dec(grid, 2), dec(sun, 2), dec(grid + sun, 2)])

    head = ["Sun kWh", "Grid kWh", "Grid kWh without price", "Grid cost " + cur, "Sun value " + cur, "Total " + cur]
    days = costs["days"]
    keys = sorted(days)
    months: dict[str, list[float]] = {}
    tot = [0.0, 0.0, 0.0, 0.0]

    def nz(v: Any) -> float:
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v and not math.isnan(v) else 0

    for k in keys:
        d, m = days[k], k[:7]
        months.setdefault(m, [0, 0, 0, 0])
        for i in range(4):
            x = nz(d[i] if i < len(d) else 0)
            months[m][i] += x
            tot[i] += x
    note = "price from the source is all-in" if all_in else "mark-up " + dec(markup, 4) + " " + cur + "/kWh · VAT " + dec(vat, 1) + " %"
    foot = ["", "# HESC charging costs · exported " + stamp + " · " + note + " · sun valued at " + dec(feed_in, 4) + " " + cur + "/kWh"]
    day_txt = "\r\n".join(["Date" + sep + sep.join(head)] + [row(k, days[k]) for k in keys] + [row("Total", tot)] + foot) + "\r\n"
    mk = sorted(months)
    mon_txt = "\r\n".join(["Month" + sep + sep.join(head)] + [row(m, months[m]) for m in mk] + [row("Total", tot)] + foot) + "\r\n"
    bom = "﻿"
    info = ("Export " + stamp + " · " + _s(len(keys)) + " days, " + _s(len(mk)) + (" month" if len(mk) == 1 else " months")
            + " · in " + folder + ": charging_costs_days.csv and charging_costs_months.csv")
    return [("charging_costs_days.csv", bom + day_txt), ("charging_costs_months.csv", bom + mon_txt)], info[:250]
