"""Learn the charging power per car (v4 step 4D).

Decision 30-10-2026 21:52 ("ik zou ook leren doen, optie 2") and 31-10 17:25 (points 3 and 4):
the power the plan reckons with is not asked but learned. HESC starts with a safe estimate and replaces
it with what it measures while charging from the grid; in Expert it can be set by hand. The number is
only an estimate of the charging time (when the plan starts), never a safety limit.

* A **session** is a stretch of grid charging by HESC (its plan or "charge now") in which the current
  was not held down (comfort guard, "together" share). It counts when it lasted at least a quarter.
* The **learned power** is the median of the last 5 sessions, so one odd session (a cold battery,
  nearly full) does not pull it off. A session still running counts once it lasted a quarter, so the
  plan can already adjust the same night.
* The **first estimate**, before any session, comes from the house connection and the charger's
  maximum (decision 30-10 22:02 a): phases x the lowest of 16 A, the charger's maximum and the
  connection's current x 230 V. Without a house connection: none (the plan keeps its setting, as v3).

Pure functions on a plain dict, shared by the simulator and the integration.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from statistics import median
from typing import Any, Final

SESSIONS_KEPT: Final = 5
MIN_SESSION: Final = timedelta(minutes=15)
CAR_MAX_A: Final = 16.0  # most cars charge with at most 16 A per phase
VOLT: Final = 230.0


def empty() -> dict[str, Any]:
    return {"sessions": [], "run": None}


def clean(raw: Any) -> dict[str, Any]:
    out = empty()
    if not isinstance(raw, dict):
        return out
    out["sessions"] = [round(float(v), 2) for v in (raw.get("sessions") or []) if _num(v) and float(v) > 0][-SESSIONS_KEPT:]
    run = raw.get("run")
    if isinstance(run, dict) and _when(run.get("since")) and _num(run.get("sum_w")) and _num(run.get("n")):
        out["run"] = {"since": str(run["since"]), "sum_w": float(run["sum_w"]), "n": int(run["n"])}
    return out


def first_estimate(connection: Any, charger_max_a: Any) -> float | None:
    """kW from the house connection ("3x25 A") and the charger's maximum current; None without one."""
    from .fleet import parse_connection

    conn = parse_connection(connection)
    if conn is None:
        return None
    phases, house_a = conn
    amps = min(CAR_MAX_A, house_a, float(charger_max_a) if _num(charger_max_a) and float(charger_max_a) > 0 else CAR_MAX_A)
    return round(phases * amps * VOLT / 1000, 1)


def step(state: dict[str, Any], now: datetime, power_w: float | None, grid_charging: bool, held_down: bool,
         active_w: float) -> dict[str, Any]:
    """One round: add the measured power to the running session, or close it."""
    s = clean(state)
    run = s["run"]
    measuring = grid_charging and not held_down and power_w is not None and power_w >= active_w
    if measuring:
        if run is None:
            run = {"since": now.isoformat(), "sum_w": 0.0, "n": 0}
        run["sum_w"] += float(power_w)
        run["n"] += 1
        s["run"] = run
        return s
    if run is not None:
        since = _when(run["since"])
        if since is not None and now - since >= MIN_SESSION and run["n"] > 0:
            s["sessions"] = [*s["sessions"], round(run["sum_w"] / run["n"] / 1000, 2)][-SESSIONS_KEPT:]
        s["run"] = None
    return s


def learned_kw(state: dict[str, Any], now: datetime) -> float | None:
    """The median of the last 5 sessions (a running one counts after a quarter); None before any."""
    s = clean(state)
    values = list(s["sessions"])
    run = s["run"]
    if run is not None and run["n"] > 0:
        since = _when(run["since"])
        if since is not None and now - since >= MIN_SESSION:
            values = [*values, run["sum_w"] / run["n"] / 1000][-SESSIONS_KEPT:]
    return round(median(values), 1) if values else None


def plan_kw(state: dict[str, Any], now: datetime, learn: bool, set_kw: float, connection: Any,
            charger_max_a: Any) -> tuple[float, str]:
    """(kW, where it comes from: "set by hand", "learned", "estimate" or "setting") for the plan."""
    if not learn:
        return set_kw, "set by hand"
    kw = learned_kw(state, now)
    if kw is not None:
        return kw, "learned"
    est = first_estimate(connection, charger_max_a)
    if est is not None:
        return est, "estimate"
    return set_kw, "setting"


def _num(v: Any) -> bool:
    try:
        float(v)
    except (TypeError, ValueError):
        return False
    return True


def _when(v: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(v))
    except (TypeError, ValueError):
        return None


# ---- v4 step 4E: a car without a battery-level sensor (decision 31-10-2026 01:10) -------------
# HESC lets it charge until the car stops by itself and estimates how much it needs from earlier
# charges: the kWh of the last 5 plug-ins that ended with the car full (it stopped by itself while
# HESC charged it). Expert: "kWh per charge" by hand. The very first time, with nothing learned and
# nothing set: half the battery (decision 31-10-2026 ± 18:30, "Halve accu").
NO_SOC_ENTITY: Final = "sensor.hesc_v4_internal_no_soc"  # what the plan still has to charge (need_kwh)
SOC_ENTERED_ENTITY: Final = "sensor.hesc_v4_internal_soc_entered"  # the battery level entered by hand, + since
EFF: Final = 0.9  # charging losses, as ev_soc.py
FULL_AFTER: Final = timedelta(minutes=5)  # no power for this long while HESC charges = the car is full
MAX_STEP: Final = timedelta(minutes=2)    # a longer gap between rounds counts as this long


def fill_step(state: dict[str, Any], now: datetime, connected: bool, power_w: float | None, hesc_charges: bool,
              active_w: float) -> dict[str, Any]:
    """One round of the plug-in: count the energy, and see whether the car stopped by itself."""
    s = dict(state or {})
    fills = [round(float(v), 1) for v in (s.get("fills") or []) if _num(v)][-SESSIONS_KEPT:]
    plug = dict(s["plug"]) if isinstance(s.get("plug"), dict) else None
    if not connected:
        if plug is not None and plug.get("full") and float(plug.get("kwh") or 0) > 1:
            fills = [*fills, round(float(plug["kwh"]), 1)][-SESSIONS_KEPT:]
        s.update(fills=fills, plug=None)
        return s
    if plug is None:
        plug = {"kwh": 0.0, "full": False, "charged": False, "last": now.isoformat(), "low_since": None}
    last = _when(plug.get("last")) or now
    dt = min(max(now - last, timedelta(0)), MAX_STEP)
    w = float(power_w or 0)
    plug["kwh"] = float(plug.get("kwh") or 0) + w * dt.total_seconds() / 3_600_000
    plug["last"] = now.isoformat()
    if w >= active_w:
        plug["charged"], plug["low_since"] = True, None
    elif hesc_charges and plug.get("charged") and not plug.get("full"):
        since = _when(plug.get("low_since"))
        if since is None:
            plug["low_since"] = now.isoformat()
        elif now - since >= FULL_AFTER:
            plug["full"] = True
    s.update(fills=fills, plug=plug)
    return s


def fill_kwh(state: dict[str, Any], set_kwh: Any, battery_kwh: Any) -> tuple[float, str]:
    """(kWh one charge needs, where it comes from: "set by hand", "learned" or "half the battery")."""
    if _num(set_kwh) and float(set_kwh) > 0:
        return float(set_kwh), "set by hand"
    fills = [float(v) for v in ((state or {}).get("fills") or []) if _num(v)]
    if fills:
        return round(median(fills), 1), "learned"
    cap = float(battery_kwh) if _num(battery_kwh) else 0.0
    return round(cap / 2, 1), "half the battery"


def no_soc_need(state: dict[str, Any], set_kwh: Any, battery_kwh: Any) -> tuple[float, str]:
    """(kWh still to charge in this plug-in, source): what one charge needs minus what it got; 0 once
    the car stopped by itself."""
    kwh, src = fill_kwh(state, set_kwh, battery_kwh)
    plug = (state or {}).get("plug") or {}
    if plug.get("full"):
        return 0.0, src
    return round(max(kwh - float(plug.get("kwh") or 0), 0.0), 2), src


def entered_soc(entry: dict[str, Any] | None, plug_kwh: float, battery_kwh: Any) -> float | None:
    """The battery level entered by hand at kWh `entry["kwh"]` of this plug-in, plus what was charged
    since (decision 31-10-2026 18:53/18:55: "accustand nu" on the phone, for a car without a sensor)."""
    if not entry or not _num(entry.get("soc")) or not _num(battery_kwh) or float(battery_kwh) <= 0:
        return None
    added = max(float(plug_kwh) - float(entry.get("kwh") or 0), 0.0) * EFF / float(battery_kwh) * 100
    return round(min(100.0, float(entry["soc"]) + added), 1)
