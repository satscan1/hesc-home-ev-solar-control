"""Price forecast: expected quarter prices after the last known price.

Line-by-line port of v2.0.0's Node-RED function node "Price forecast" (every 15 minutes).
Keeps an own price history (hourly averages per day + the day's solar forecast) and predicts
the quarters from the last known price until 24 h later. Proven identical to the original
node on random histories (`tests/integration/test_forecast_parity.py`).
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from zoneinfo import ZoneInfo

from .jscompat import iso, js_json, js_to_fixed

DEF = [
    [-1.5, -1.8, -2.1, -2.5, -2.6, -2.4, -1.7, -0.6, 0.9, 1.4, 1.2, 0.8, 0.4, 0.3, 0.5, 1, 1.8, 2.8, 2.6, 1.7, 0.7, 0, -0.1, -0.8],
    [-0.2, -0.7, -1.2, -1.4, -1.5, -1, 0.3, 1.7, 2.2, 1, -0.4, -1.9, -2.6, -3, -2.7, -1.4, -0.1, 2.1, 3.3, 3.5, 2.4, 1.3, 0.6, -0.3],
    [0.6, 0, -0.6, -1, -1, -0.5, 1, 2.2, 1.9, 0, -2, -3.4, -4.3, -4.6, -4.3, -3.4, -1.8, 0.8, 3.7, 5.7, 4.8, 3.2, 2.3, 0.8],
    [1.6, 0.9, 0.4, 0.2, 0.3, 0.8, 2, 2.5, 1.6, -0.8, -3, -4.9, -6.1, -6.8, -6.6, -5.6, -3.6, -0.6, 2.7, 5.6, 6.6, 5.5, 4.4, 2.9],
    [1.8, 1.2, 0.8, 0.7, 0.7, 1.2, 2.6, 3.2, 2.1, -0.6, -3.5, -5.8, -7.5, -8.5, -8.1, -6.3, -3.7, 0, 3.3, 6, 7.3, 6.3, 4.3, 2.5],
]
BINS = [0, 0.2, 0.4, 0.6, 0.8]
WEEKEND_DAYS = 8
PRIOR_DAYS, BASE_DAYS, KEEP_DAYS, SOLAR_WEIGHT = 30, 14, 90, 0.5
DAY_MS = 86400000
Q_MS = 15 * 60000


def js_num(v: Any) -> float | None:
    """v2's num(): parseFloat, null when NaN."""
    from .inputs import js_parse_float

    return js_parse_float(v)


def date_parse(s: Any) -> float:
    """Date.parse for the ISO strings v2 stores (with offset or Z). NaN when unparsable."""
    if not isinstance(s, str):
        s = "" if s is None else str(s)
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        return math.nan
    if d.tzinfo is None:
        d = d.replace(tzinfo=UTC) if len(s) <= 10 else d.replace(tzinfo=UTC)
    return d.timestamp() * 1000


def js_truthy(v: Any) -> bool:
    """JavaScript truthiness (objects and arrays are always true)."""
    if v is None or v is False:
        return False
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return not (v == 0 or math.isnan(v))
    if isinstance(v, str):
        return v != ""
    return True


def _fixed(x: float, n: int) -> float:
    """+(x).toFixed(n)."""
    return float(js_to_fixed(x, n))


@dataclass
class ForecastResult:
    history: dict[str, Any]
    save: str | None  # JSON text for the history file (None = unchanged)
    state: str
    attributes: dict[str, Any]
    status: str


def run(S: dict[str, Any], H: Any, now: float) -> ForecastResult:
    """One run of the node. S: states in Node-RED form; H: the stored price history; now: ms."""
    def st(i):
        return S[i].get("state") if i and i in S else None

    def attr(i, a):
        return (S[i].get("attributes") or {}).get(a) if i and i in S else None

    def txt(i):
        v = st(i)
        return str(v if v else "").strip()

    pa = (S.get("sensor.hesc_prices") or {}).get("attributes") or {}
    tzname = pa.get("tz") or "Europe/Amsterdam"
    tz = ZoneInfo(tzname)
    fx = js_num(pa.get("fx_vs_eur")) or 1
    penalty = _fixed(0.02 * fx, 4)

    def day_key(t: float) -> str:
        return datetime.fromtimestamp(t / 1000, tz).strftime("%Y-%m-%d")

    def hour_of(t: float) -> int:
        return datetime.fromtimestamp(t / 1000, tz).hour % 24

    def mean(a):
        s = 0
        for x in a:
            s = s + x
        return s / len(a) if a else math.nan

    def cls(n):
        c = 0
        for i, b in enumerate(BINS):
            if n >= b:
                c = i
        return c

    H = copy.deepcopy(H) if isinstance(H, dict) and js_truthy(H.get("days")) else {"version": 1, "days": {}}
    changed = False

    rows = list(attr("sensor.hesc_prices", "raw_today") or []) + list(attr("sensor.hesc_prices", "raw_tomorrow") or [])
    sol_today = js_num(st(txt("input_text.hesc_solar_today_sensor")))
    sol_tomorrow = js_num(st(txt("input_text.hesc_solar_tomorrow_sensor")))
    today, tomorrow = day_key(now), day_key(now + DAY_MS)
    by_day: dict[str, dict[str, list]] = {}
    known_end = 0.0
    for r in rows:
        a, b, v = date_parse(r.get("start")), date_parse(r.get("end")), js_num(r.get("value"))
        if math.isnan(a) or math.isnan(b) or v is None:
            continue
        known_end = max(known_end, b)
        d, h = day_key(a), hour_of(a)
        if d not in by_day:
            by_day[d] = {"s": [0] * 24, "n": [0] * 24}
        by_day[d]["s"][h] += v
        by_day[d]["n"][h] += 1
    for d, b in by_day.items():
        if len([x for x in b["n"] if x > 0]) < 23:
            continue
        p = [_fixed(s / b["n"][h], 5) if b["n"][h] else None for h, s in enumerate(b["s"])]
        sol = sol_today if d == today else (sol_tomorrow if d == tomorrow else None)
        old = H["days"].get(d) or {}
        if sol is not None:
            solar = _fixed(max(sol, old.get("solar") or 0), 2)
        else:
            solar = old.get("solar") if "solar" in old else None
        p_changed = "p" not in old or js_json(old["p"]) != js_json(p)
        s_changed = "solar" not in old or old["solar"] != solar or type(old["solar"]) is bool
        if p_changed or s_changed:
            H["days"][d] = {"solar": solar, "p": p}
            changed = True
    keys = sorted(H["days"].keys())
    while len(keys) > KEEP_DAYS:
        del H["days"][keys.pop(0)]
        changed = True

    sol_vals = [H["days"][k].get("solar") for k in keys[-30:]]
    sol_vals = [x for x in sol_vals if x is not None and x > 0] + [x for x in (sol_today, sol_tomorrow) if x is not None and x > 0]
    srt = sorted(sol_vals)
    p90 = srt[math.floor(0.9 * (len(srt) - 1))] if srt else None

    def norm(x):
        if x is None or not p90:
            return None
        return min(1.2, x / max(1, p90))

    def full_day(k):
        dd = H["days"][k]
        p = dd.get("p")
        return bool(p) and all(x is not None for x in p) and bool(dd.get("solar"))

    full = [k for k in keys if full_day(k)]
    iu = H.get("index_updated")
    age = (now - date_parse(iu)) / DAY_MS if iu else 999
    if not isinstance(H.get("index"), list) or age >= 7:
        tot = [[0.0] * 24 for _ in DEF]
        cnt = [0] * len(DEF)
        for k in full:
            n = norm(H["days"][k]["solar"])
            if n is None:
                continue
            c = cls(n)
            m = mean(H["days"][k]["p"])
            for h, v in enumerate(H["days"][k]["p"]):
                tot[c][h] += (v - m) * 100
            cnt[c] += 1
        H["index"] = [[_fixed((v * fx * PRIOR_DAYS + tot[c][h]) / (PRIOR_DAYS + cnt[c]), 2) for h, v in enumerate(r)] for c, r in enumerate(DEF)]
        H["index_days"] = len(full)
        H["index_updated"] = iso(now)
        changed = True
    idx = H["index"]

    fc: list[dict[str, Any]] = []
    basis = 0
    if known_end > 0:
        hol_a = (S.get("sensor.hesc_holidays") or {}).get("attributes", {}).get("dates") if "sensor.hesc_holidays" in S else None
        hol = hol_a if isinstance(hol_a, list) else []

        def is_we(k: str) -> bool:
            try:
                g = datetime.fromisoformat(k + "T12:00:00+00:00").isoweekday() % 7
            except ValueError:
                return k in hol
            return g in (0, 6) or k in hol

        before = [k for k in full if k < day_key(known_end)]
        mixed = before[-BASE_DAYS:]
        fallback = [k for k in keys if H["days"][k].get("p") and all(x is not None for x in H["days"][k]["p"])][-1:]

        def pick(we: bool):
            same = [k for k in before if is_we(k) == we]
            same = same[-(WEEKEND_DAYS if we else BASE_DAYS):]
            return same if len(same) >= 3 else (mixed if len(mixed) >= 3 else fallback)

        def model(bd):
            if not bd:
                return None
            prof = [mean([H["days"][k]["p"][h] for k in bd]) for h in range(24)]
            base_idx = []
            for h in range(24):
                v = []
                for k in bd:
                    n = norm(H["days"][k].get("solar"))
                    v.append(None if n is None else idx[cls(n)][h])
                v = [x for x in v if x is not None]
                base_idx.append(mean(v) if v else None)
            return {"prof": prof, "baseIdx": base_idx, "n": len(bd)}

        M = {"wd": model(pick(False)), "we": model(pick(True))}
        basis = max(M["wd"]["n"] if M["wd"] else 0, M["we"]["n"] if M["we"] else 0)
        if basis > 0:
            t = known_end
            while t < known_end + DAY_MS:
                d, h = day_key(t), hour_of(t)
                m = M["we"] if is_we(d) else M["wd"]
                if m:
                    sol = sol_today if d == today else (sol_tomorrow if d == tomorrow else None)
                    n = norm(sol)
                    adj = 0 if (n is None or m["baseIdx"][h] is None) else SOLAR_WEIGHT * (idx[cls(n)][h] - m["baseIdx"][h]) / 100
                    fc.append({"start": iso(t), "end": iso(t + Q_MS), "value": _fixed(m["prof"][h] + adj, 4)})
                t += Q_MS

    attrs = {
        "friendly_name": "HESC price forecast", "icon": "mdi:crystal-ball", "unit_of_measurement": "quarters",
        "forecast": fc, "from": fc[0]["start"] if fc else None, "until": fc[-1]["end"] if fc else None,
        "basis_days": basis, "history_days": len(keys), "index_days": H.get("index_days") or 0,
        "index_updated": H.get("index_updated") or None, "solar_p90": p90, "solar_today": sol_today,
        "solar_tomorrow": sol_tomorrow, "penalty": penalty, "updated": iso(now),
    }
    status = f"{len(fc)} quarters · {basis} days · index {H.get('index_days') or 0} d"
    return ForecastResult(H, js_json(H) if changed else None, str(len(fc)), attrs, status)
