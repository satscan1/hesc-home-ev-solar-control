"""Charging current control: while HESC charges from the grid, let the current follow the sun.

Design (replaces the earlier idea "charge plan at 6 A"): where the charger lets HESC set its charging current, HESC may lower it to
get more sun into the car — also during a planned grid-charging quarter — as long as the car is
still full in time. First Wallbox only. No switch and no phase setting — it is
part of the default behaviour whenever the charger lets HESC set its current, and the number of
phases follows from the charger itself.

When it acts: a current entity is known, the charge plan has
the charger (v2's flag ``hesc_plan_owns_charging``) and the car is charging. The current is then
set so the car takes about what the sun gives (charging power minus grid import), never below the
charger's minimum (6 A) and never above its maximum. When the plan no longer needs the charger,
or time gets tight, the current goes back to what it was before.

Phases: measured, never asked. While the car charges at the current before HESC changed anything,
charging power / (current × 230 V) gives 1, 2 or 3 phases; HESC acts only once it knows them.

"In time": the plan must not be short of time and, at full power, the remaining energy must still
fit before the deadline with ``MARGIN_MIN`` to spare. Otherwise full current.

Nothing is switched in shadow mode; the status then says what HESC would do. One exception (rc3):
when HESC itself lowered the current while live and shadow mode went on since, it still puts its
own change back (repair of its own action, not a new decision). At most one change
per ``GAP_S`` (cloud chargers are slow) and only for a difference of at least 1 A.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from homeassistant.util import dt as dt_util

from .inputs import js_parse_float

ENTITY_HELPER = "input_text.hesc_charger_current_entity"
VOLT = 230.0
MIN_A = 6.0
MARGIN_MIN = 30.0
GAP_S = 60.0
_BAD = ("", "unknown", "unavailable", "none")


@dataclass
class Result:
    actions: list[dict[str, Any]] = field(default_factory=list)
    status: str = ""
    context: dict[str, Any] = field(default_factory=dict)


def _st(S: Any, eid: str) -> Any:
    return (S.get(eid) or {}).get("state") if eid else None


def _attr(S: Any, eid: str, name: str) -> Any:
    return ((S.get(eid) or {}).get("attributes") or {}).get(name) if eid else None


def _num(v: Any) -> float | None:
    return js_parse_float(v)


def _txt(S: Any, eid: str) -> str:
    v = _st(S, eid)
    v = "" if v is None else str(v).strip()
    return "" if v.lower() in _BAD else v


def _pw(S: Any, eid: str) -> float | None:
    v = _num(_st(S, eid))
    if v is None:
        return None
    unit = str(_attr(S, eid, "unit_of_measurement") or "").lower()
    return v * 1000 if unit == "kw" else (v / 1000 if unit == "mw" else v)


def _in_time(S: Any, now: datetime) -> tuple[bool, str]:
    raw = _attr(S, "sensor.hesc_charge_plan", "plan")
    try:
        plan = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except ValueError:
        plan = {}
    deadline = dt_util.parse_datetime(str(_st(S, "sensor.hesc_charge_plan") or ""))
    if not isinstance(plan, dict) or deadline is None:
        return False, "no plan deadline"
    if plan.get("short_of_time"):
        return False, "plan is short of time"
    need = _num(plan.get("need_kwh")) or 0.0
    kw = _num(plan.get("kw")) or 0.0
    left_min = (deadline - now).total_seconds() / 60
    need_min = need / kw * 60 if kw > 0 else float("inf")
    if left_min < need_min + MARGIN_MIN:
        return False, f"time tight ({left_min:.0f} min left, {need_min:.0f} min needed at full power)"
    return True, ""


def run(S: Any, context: dict[str, Any] | None, now_ms: float) -> Result:
    """One round. ``S``: the logic's view of the states; ``context``: kept between rounds."""
    ctx = dict(context or {})
    res = Result(context=ctx)
    now = dt_util.utc_from_timestamp(now_ms / 1000)
    ent = _txt(S, ENTITY_HELPER)
    shadow = _st(S, "input_boolean.hesc_shadow_mode") != "off"
    cur = _num(_st(S, ent)) if ent else None
    if not ent:
        res.status = "Off: the charger does not let HESC set its current"
        return res
    lo = max(MIN_A, _num(_attr(S, ent, "min")) or MIN_A)
    hi = _num(_attr(S, ent, "max")) or 16.0
    ev_pow = _pw(S, _txt(S, "input_text.hesc_ev_power_sensor"))
    grid = _pw(S, _txt(S, "input_text.hesc_grid_power_sensor"))
    if grid is not None and _st(S, "input_boolean.hesc_grid_export_positive") == "on":
        grid = -grid  # HESC works with import positive
    active_w = _num(_st(S, "input_number.hesc_ev_active_w")) or 400
    plan_owns = _st(S, "input_boolean.hesc_plan_owns_charging") == "on"
    charging = ev_pow is not None and ev_pow > active_w

    # phases follow from the charger: measured while it charges at a current HESC did not change.
    # Only while the charge plan charges from the grid, or when the charger is not in its solar mode:
    # charging on sun, the charger lowers the current by itself (for example Wallbox Eco down to 2 A
    # per phase), so power / set current would give too few phases. (A Wallbox keeps showing Eco
    # while the plan charges through its pause/resume switch, hence "plan owns" counts too.)
    mode_ent = _txt(S, "input_text.hesc_charger_mode_entity")
    solar_vals = [v.strip().lower() for v in (_txt(S, "input_text.hesc_charger_eco_value") or "").split(",") if v.strip()]
    in_solar = bool(mode_ent) and str(_st(S, mode_ent) or "").strip().lower() in solar_vals
    if charging and cur and cur >= lo and ctx.get("saved") is None and (plan_owns or not in_solar):
        est = ev_pow / (cur * VOLT)
        if 0.6 <= est <= 3.4 and abs(est - round(est)) <= 0.3:
            ctx["phases"] = float(min(3, max(1, round(est))))
    phases = ctx.get("phases")

    target: float | None = None
    why = ""
    if plan_owns and charging and grid is not None and cur is not None:
        ok, tight = _in_time(S, now)
        if ok and not phases:
            res.status = "Measuring the charger's phases"
            return res
        if ok:
            sun_w = ev_pow - grid  # what the car takes now minus what comes from the grid
            target = min(hi, max(lo, round(sun_w / (phases * VOLT))))
            if not shadow:  # rc3 review: "saved" only when HESC really changes it (live), never in shadow
                ctx.setdefault("saved", cur)
            why = "following the sun"  # no kW in the text: every status change is an HA write
        elif ctx.get("saved") is not None:
            target, why = ctx["saved"], f"full current: {tight}"
    elif ctx.get("saved") is not None:
        target, why = ctx["saved"], "back to the current from before"

    if target is None:
        if not plan_owns:
            res.status = "Waiting: only while the charge plan charges from the grid"
        elif not charging:
            res.status = "Waiting: car not charging"
        else:
            res.status = "Waiting for inputs (grid power, charging current)"
        return res

    restoring = ctx.get("saved") is not None and target == ctx["saved"] and not why.startswith("following")
    if cur is not None and abs(target - cur) < 1:
        if restoring:
            ctx.pop("saved", None)
        res.status = f"{target:.0f} A · {why}"
        return res
    if now_ms - float(ctx.get("lastAt") or 0) < GAP_S * 1000:
        res.status = ("-" if cur is None else f"{cur:.0f}") + f" A · next change after {GAP_S:.0f} s"
        return res
    if shadow and not restoring:
        res.status = f"[shadow] would set {target:.0f} A · {why}"
        return res
    payload = {"action": "number.set_value", "target": {"entity_id": [ent]}, "data": {"value": target}}
    if shadow:
        # since rc3: HESC lowered the current while live and shadow mode
        # went on since. Putting its own change back is repair, not a new action: allowed in shadow mode.
        payload["restore_own_change"] = True
        why = "putting back HESC's own change"
    res.actions.append({"payload": payload})
    ctx["lastAt"] = now_ms
    if restoring:
        ctx.pop("saved", None)
    res.status = ("[shadow] " if shadow else "") + f"{target:.0f} A · {why}"
    return res
