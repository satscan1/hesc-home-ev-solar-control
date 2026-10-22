"""Charge now to a goal (since 3.0.0).

Not in v2. "Charge now to 90 %" is a short charge plan that starts at once: every quarter from
now until the end is a planned quarter, the goal is the chosen one. The ported charge plan
control (charge_plan.py) then does what it does for any plan: start grid charging, stop at the
goal (or at the end), and put the charger back in its own solar mode. Nothing else changes, so
the dashboard, the cost estimate, the history and the notifications all work as for a plan.

It ends by itself when the goal is reached, the EV is unplugged or the end time has passed.
The end time is set when it starts: the expected charge time x 1.5 plus one hour, so a slow
charge still reaches the goal and a car that will not take power is not kept waiting forever.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any

from homeassistant.util import dt as dt_util

SOURCE = "charge now"
OFF = "Off"
GOALS = tuple(range(50, 101, 5))
OPTIONS = (OFF, *(f"{g}%" for g in GOALS))
MARGIN = 3  # charge_plan.MARGIN: below goal minus this the plan control starts


def end_time(now: datetime, soc: float, goal: int, cap_kwh: float, kw: float) -> datetime:
    """When charge-now gives up: expected charge time x 1.5 plus one hour, on a quarter."""
    need_h = max(goal - soc, 0) / 100 * cap_kwh / kw if kw > 0 else 4
    end = dt_util.as_utc(now) + timedelta(hours=need_h * 1.5 + 1)  # UTC: right over a clock change
    return dt_util.as_local(_quarter(end) + (timedelta(minutes=15) if end != _quarter(end) else timedelta(0)))


def _quarter(t: datetime) -> datetime:
    """Start of the quarter (on UTC times: every offset in use is a whole quarter)."""
    return t.replace(minute=t.minute - t.minute % 15, second=0, microsecond=0)


def override(p: dict[str, Any], goal: int, until: datetime, now: datetime, cap_kwh: float,
             prices: list[dict[str, Any]]) -> dict[str, Any]:
    """The plan (as plan.compute returns it) with charge-now in its place."""
    soc = p.get("soc")
    kw = float(p.get("kw") or 11)
    need = max(goal - float(soc), 0) / 100 * cap_kwh if isinstance(soc, (int, float)) and cap_kwh > 10 else 0
    loc_until = dt_util.as_local(until)
    quarters: list[datetime] = []
    # step in UTC, so the repeated hour when the clocks go back (and the skipped one in spring) is
    # counted as the real time it is; shown in local time
    t, end = _quarter(dt_util.as_utc(now)), dt_util.as_utc(until)
    while t < end:
        quarters.append(dt_util.as_local(t))
        t = t + timedelta(minutes=15)
    n = math.ceil(need / (kw * 0.25)) if kw > 0 else 0
    vals = []
    for q in quarters[:n]:
        for r in prices:
            a, b = dt_util.parse_datetime(str(r.get("start"))), dt_util.parse_datetime(str(r.get("end")))
            if a is not None and b is not None and a <= q < b and isinstance(r.get("value"), (int, float)):
                vals.append(float(r["value"]))
                break
    hrs = min(need, len(quarters) * kw * 0.25) / kw if kw > 0 else 0
    out = dict(p)
    out.update({
        "goal": int(goal), "need_kwh": round(need, 1), "solar_kwh": 0, "grid_kwh": round(need, 1),
        "grid_kwh_needed": round(need, 1), "quarters": len(quarters), "quarters_needed": n,
        "short_of_time": n > len(quarters), "charge_time": f"{int(hrs)}:{int(hrs * 60) % 60:02d}",
        "avg_price_ct": round(sum(vals) / len(vals) * 100, 1) if vals and len(vals) == min(n, len(quarters)) else None,
        "planned": [q.isoformat() for q in quarters], "planned_forecast": [],
        "deadline": loc_until.isoformat(), "deadline_text": loc_until.strftime("%a %d-%m %H:%M"),
        "source": SOURCE, "active": True,
    })
    return out


def finished(goal: int, soc: Any, ev_connected: bool | None, until: datetime, now: datetime) -> str | None:
    """Why charge-now ends now (None: it goes on)."""
    if ev_connected is False:
        return "EV unplugged"
    if now >= until:
        return "end time passed"
    if isinstance(soc, (int, float)) and soc >= goal - 0.5:
        return "goal reached"
    return None
