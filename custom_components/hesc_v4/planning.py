"""The v4 planning model per car (step 4, decision 12): rhythm, only this time, calendar.

* **Rhythm**: v3's repeating plan (its days, time and goal), with an own time and goal per weekday
  (step 4A, `plan.next_repeating` / `plan.repeating_goal`).
* **Only this time** (`once`, step 4B): for one day, skip it, or charge with another time and/or goal;
  also on a day the rhythm does not charge. It is bound to that day and replaces the rhythm on it; it
  goes when the day is over, so the car goes back to the rhythm by itself. Replaces v3's "plan for one day" and
  "skip one day".
* **Calendar** (step 4C): days off, extra days (with the standard time and goal) and a vacation as a
  period from-to (`to` empty: until it is stopped). Replaces v3's holiday switch and "holiday until".
  Decision 10-11-2026: an extra day can have its own time and/or goal (`own`: {date: {time, goal}}),
  set by double-tapping a day in the calendar.

HESC keeps this per car itself (decision 31-10-2026 17:25) and the dashboard changes it through
HESC actions. The plan (`plan.deadline`) reads it from the car's view as the attribute `planning` of
`ENTITY`; without it (the simulator's v3 days) the plan works exactly as v3.

Pure functions on a plain dict, so the simulator and the integration share them.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime, timedelta
from typing import Any, Final

from homeassistant.util import dt as dt_util

ENTITY: Final = "sensor.hesc_v4_internal_planning"
HORIZON_DAYS: Final = 15  # as v3's repeating plan with a skipped day
WEEK: Final = 7
WDS: Final = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
STANDARD: Final = "Standard"

# what a day of the coming week is
RHYTHM: Final = "rhythm"
ONCE: Final = "once"
EXTRA: Final = "extra"
SKIPPED: Final = "skipped"
OFF: Final = "off"
VACATION: Final = "vacation"
NONE: Final = "none"

Getter = Callable[[str], "tuple[str, dict[str, Any]] | None"]


def empty() -> dict[str, Any]:
    return {"once": None, "off": [], "extra": [], "own": {}, "vacation": None}


def clean(raw: Any) -> dict[str, Any]:
    """A planning dict with every key, from whatever was stored (unknown keys dropped)."""
    out = empty()
    if not isinstance(raw, dict):
        return out
    once = raw.get("once")
    if isinstance(once, dict) and _date(once.get("date")):
        goal = once.get("goal")
        out["once"] = {"date": str(once["date"])[:10], "skip": bool(once.get("skip")),
                       "time": _hhmm(once.get("time")), "goal": int(goal) if _is_int(goal) else None}
    for key in ("off", "extra"):
        out[key] = sorted({str(d)[:10] for d in (raw.get(key) or []) if _date(d)})
    own = raw.get("own")
    if isinstance(own, dict):
        for d, v in own.items():
            if _date(d) and isinstance(v, dict) and str(d)[:10] in out["extra"]:
                goal = v.get("goal")
                x = {"time": _hhmm(v.get("time")), "goal": int(goal) if _is_int(goal) else None}
                if x["time"] or x["goal"] is not None:
                    out["own"][str(d)[:10]] = x
    vac = raw.get("vacation")
    if isinstance(vac, dict) and _date(vac.get("from")):
        out["vacation"] = {"from": str(vac["from"])[:10], "to": str(vac["to"])[:10] if _date(vac.get("to")) else None}
    return out


def is_empty(p: dict[str, Any]) -> bool:
    return p.get("once") is None and not p.get("off") and not p.get("extra") and not p.get("own") and p.get("vacation") is None


# ---- reading the rhythm from the car's view ---------------------------------------------------------
def _st(get: Getter, eid: str) -> str:
    s = get(eid)
    return "unknown" if s is None else str(s[0])


def _rhythm_on(get: Getter) -> bool:
    return _st(get, "input_boolean.hesc_rep_enabled") == "on"


def _weekday_on(get: Getter, day: date) -> bool:
    return _st(get, f"input_boolean.hesc_rep_{WDS[day.weekday()].lower()}") == "on"


def day_time(get: Getter, day: date) -> str:
    own = _st(get, f"input_select.hesc_rep_{WDS[day.weekday()].lower()}_time")
    return own if _hhmm(own) else _st(get, "input_select.hesc_rep_time")


def day_goal(get: Getter, day: date) -> str:
    own = _st(get, f"input_select.hesc_rep_{WDS[day.weekday()].lower()}_goal")
    return own if own.endswith("%") else _st(get, "input_select.hesc_rep_goal")


def _own_day(get: Getter, day: date) -> bool:
    """The weekday has its own time or goal (not "Standard")."""
    wd = WDS[day.weekday()].lower()
    return bool(_hhmm(_st(get, f"input_select.hesc_rep_{wd}_time"))) or _st(get, f"input_select.hesc_rep_{wd}_goal").endswith("%")


def _at(day: date, hhmm: str) -> datetime | None:
    t = dt_util.parse_time(hhmm) if _hhmm(hhmm) else None
    if t is None:
        return None
    return datetime.combine(day, t, dt_util.get_default_time_zone())


# ---- what one day is ------------------------------------------------------------------------------
def on_vacation(p: dict[str, Any], day: date) -> bool:
    v = p.get("vacation")
    if not v:
        return False
    start = _date(v.get("from"))
    end = _date(v.get("to"))
    return start is not None and start <= day and (end is None or day <= end)


def day_plan(p: dict[str, Any], get: Getter, day: date) -> tuple[str, datetime | None, str]:
    """(kind, ready-by time, goal) of one day. Kind is one of RHYTHM, ONCE, EXTRA, SKIPPED, OFF,
    VACATION, NONE; the time is None when the day does not charge."""
    once = p.get("once")
    if once and once.get("date") == day.isoformat():
        if once.get("skip"):
            return SKIPPED, None, ""
        t = _at(day, once.get("time") or day_time(get, day))
        goal = f"{once['goal']}%" if once.get("goal") is not None else day_goal(get, day)
        return ONCE, t, goal
    if on_vacation(p, day):
        return VACATION, None, ""
    iso = day.isoformat()
    if iso in (p.get("off") or []):
        return OFF, None, ""
    if iso in (p.get("extra") or []):
        own = (p.get("own") or {}).get(iso) or {}
        goal = f"{own['goal']}%" if own.get("goal") is not None else day_goal(get, day)
        return EXTRA, _at(day, own.get("time") or day_time(get, day)), goal
    if _rhythm_on(get) and _weekday_on(get, day):
        return RHYTHM, _at(day, day_time(get, day)), day_goal(get, day)
    return NONE, None, ""


def next_moment(p: dict[str, Any], get: Getter, now: datetime) -> tuple[datetime, str, str] | None:
    """The next ready-by time after `now`: (time, goal, plan source "one-off" or "repeating").

    While on vacation the week plan does not plan at all, also not for a day after the vacation
    (as v3's holiday mode); only this time still counts."""
    today = dt_util.as_local(now).date()
    away = on_vacation(p, today)
    for i in range(HORIZON_DAYS):
        day = today + timedelta(days=i)
        kind, t, goal = day_plan(p, get, day)
        if away and kind != ONCE:
            continue
        if t is not None and t > now:
            return t, goal, "one-off" if kind == ONCE else "repeating"
    return None


def coming_week(p: dict[str, Any], get: Getter, now: datetime) -> list[dict[str, Any]]:
    """Today and the six days after (decision 13: "Komende week"), for the dashboard."""
    today = dt_util.as_local(now).date()
    out = []
    for i in range(WEEK):
        day = today + timedelta(days=i)
        kind, t, goal = day_plan(p, get, day)
        out.append({"date": day.isoformat(), "weekday": WDS[day.weekday()], "kind": kind,
                    "time": t.strftime("%H:%M") if t else None, "goal": int(goal.rstrip("%")) if goal else None,
                    "passed": bool(t and t <= now),
                    # 07-11 (opmaakchat, "Komende week"): a rhythm day with its own time and/or goal
                    "own": (kind == RHYTHM and _own_day(get, day)) or (kind == EXTRA and day.isoformat() in (p.get("own") or {}))})
    return out


def expire(p: dict[str, Any], now: datetime) -> dict[str, Any]:
    """Drop what is over: "only this time" once its day is over (back to the rhythm), past days off and
    extra days, and a vacation that ended."""
    p = clean(p)
    today = dt_util.as_local(now).date()
    once = p["once"]
    # kept until its day is over: it replaces that day's rhythm moment, also after its own time passed
    if once and ((_date(once["date"]) or today) < today):
        p["once"] = None
    for key in ("off", "extra"):
        p[key] = [d for d in p[key] if (_date(d) or today) >= today]
    p["own"] = {d: v for d, v in p["own"].items() if d in p["extra"]}
    v = p["vacation"]
    if v and v.get("to") and (_date(v["to"]) or today) < today:
        p["vacation"] = None
    return p


# ---- changing it (the HESC actions) -----------------------------------------------------------------
def set_once(p: dict[str, Any], day: date, *, skip: bool = False, time: str | None = None,
             goal: int | None = None) -> dict[str, Any]:
    p = clean(p)
    p["once"] = {"date": day.isoformat(), "skip": skip, "time": _hhmm(time), "goal": goal}
    return p


def clear_once(p: dict[str, Any]) -> dict[str, Any]:
    p = clean(p)
    p["once"] = None
    return p


def set_day(p: dict[str, Any], day: date, what: str, time: str | None = None,
            goal: int | None = None) -> dict[str, Any]:
    """Calendar: `what` is "off" (no charging), "extra" (charge; with the standard, or with its own `time`
    and/or `goal`, decision 10-11-2026) or "rhythm" (back to what the rhythm says)."""
    p = clean(p)
    iso = day.isoformat()
    p["off"] = [d for d in p["off"] if d != iso]
    p["extra"] = [d for d in p["extra"] if d != iso]
    p["own"].pop(iso, None)
    if what in ("off", "extra"):
        p[what] = sorted({*p[what], iso})
    if what == "extra" and (_hhmm(time) or goal is not None):
        p["own"][iso] = {"time": _hhmm(time), "goal": goal}
    return p


def set_vacation(p: dict[str, Any], start: date, end: date | None) -> dict[str, Any]:
    p = clean(p)
    p["vacation"] = {"from": start.isoformat(), "to": end.isoformat() if end else None}
    return p


def clear_vacation(p: dict[str, Any]) -> dict[str, Any]:
    p = clean(p)
    p["vacation"] = None
    return p


def from_v3(get: Getter, now: datetime, one_off_deadline: datetime | None) -> dict[str, Any]:
    """What v3's own fields hold, in the v4 model (decision 2, 17:25): an active "plan for one day" →
    only this time on its day; "skip one day" → a day off; holiday mode (until) → a vacation from today."""
    p = empty()
    today = dt_util.as_local(now).date()
    if _st(get, "input_boolean.hesc_plan_enabled") == "on" and one_off_deadline is not None and one_off_deadline > now:
        local = dt_util.as_local(one_off_deadline)
        goal = _st(get, "input_select.hesc_plan_goal").rstrip("%")
        p["once"] = {"date": local.date().isoformat(), "skip": False, "time": local.strftime("%H:%M"),
                     "goal": int(goal) if _is_int(goal) else None}
    skip = _date(_st(get, "input_datetime.hesc_rep_skip")[:10])
    if skip is not None and skip >= today:
        p["off"] = [skip.isoformat()]
    if _st(get, "input_boolean.hesc_vacation") == "on":
        until = _date(_st(get, "input_datetime.hesc_vacation_until")[:10])
        p["vacation"] = {"from": today.isoformat(), "to": until.isoformat() if until else None}
    return p


# ---- helpers ------------------------------------------------------------------------------------
def _date(v: Any) -> date | None:
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    try:
        return date.fromisoformat(str(v)[:10])
    except (TypeError, ValueError):
        return None


def _hhmm(v: Any) -> str | None:
    s = str(v or "").strip()[:5]
    try:
        h, m = (int(x) for x in s.split(":"))
    except ValueError:
        return None
    return f"{h:02d}:{m:02d}" if 0 <= h < 24 and 0 <= m < 60 else None


def _is_int(v: Any) -> bool:
    try:
        int(str(v))
    except (TypeError, ValueError):
        return False
    return True
