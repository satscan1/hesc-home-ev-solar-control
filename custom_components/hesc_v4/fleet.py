"""Two cars on two chargers: who charges from the grid when (HESC v4 step 2, part C).

Pure functions, used by the coordinator (each car its own round, cars.py) and by the windtunnel
(sim/hescsim/fleet.py). Decisions (project notes "HESC v4 — ..."):

* 4: with a plan, the car that must be ready first goes first; same time -> the car that needs the
  most kWh; sun without a plan -> most kWh; same time and kWh -> EV1.
* 5: switching from one car to the other only on a quarter boundary.
* 7 + 30-10 22:40: grid charging together or one after the other, chosen at EV2. Together never
  more than one charger on its own (the default), unless the user raises that number.
* 31-10 07:45: one charger is one cable; a double charger with two cables counts as two chargers.

How the cars share the grid:

* **Automatic** (the default, decision 31-10 07:49: "wat het goedkoopst is en op tijd geladen"):
  HESC works out both ways below and takes the cheaper one in which both cars are ready in time.
  It changes its choice only on a quarter boundary (decision 5).
* **One after the other**: the cars plan in priority order.
  A car's charge plan does not use the quarters the cars before it planned, nor a quarter another car
  is charging in right now (so a car never loses its running quarter: decision 5).
* **Together**: both plan as usual but each with at most an equal share of the "together" maximum,
  and the charging current of each charger is held to that share. Only when HESC can set the charging
  current of every charger involved; otherwise one after the other.

What a car's round needs is put in its view under ``ENTITY`` (state = the way of sharing,
attributes ``blocked`` = quarter starts this car may not plan, ``max_w`` = most this car may take
from the grid). Without that entity (one car) plan.py and current.py do exactly what v3 does.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Final

ENTITY: Final = "sensor.hesc_v4_internal_fleet"
AUTO: Final = "automatic"
AFTER: Final = "one_after_the_other"
TOGETHER: Final = "together"
MODES: Final = (AUTO, AFTER, TOGETHER)
DEFAULT_MODE: Final = AUTO  # decision 31-10-2026 07:49


@dataclass
class Car:
    """What the division needs to know about one car (from its last round)."""

    key: str                        # ev1 / ev2
    index: int                      # 0 = EV1: the last tie-break (decision 4)
    connected: bool = False
    plan: dict[str, Any] = field(default_factory=dict)  # the car's charge plan (plan.compute)
    can_set_current: bool = False   # its charger lets HESC set the charging current
    grid_now: bool = False          # it charges from the grid right now (planned or not, e.g. by itself)
    grid_this_quarter: bool = False  # it charged from the grid at some moment in the current quarter
    outside_plan: bool = False      # it charges from the grid by itself (not HESC's plan, not "charge now")
    can_pause: bool = False         # HESC can pause its charger (a pause switch is set)

    @property
    def has_plan(self) -> bool:
        return bool(self.plan.get("active")) and _num(self.plan.get("need_kwh")) > 0

    @property
    def deadline(self) -> datetime | None:
        try:
            return datetime.fromisoformat(str(self.plan.get("deadline")))
        except ValueError:
            return None

    @property
    def need_kwh(self) -> float:
        return _num(self.plan.get("need_kwh"))

    @property
    def planned(self) -> list[str]:
        return [str(p) for p in (self.plan.get("planned") or [])]


def _num(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def parse_plan(raw: Any) -> dict[str, Any]:
    """The `plan` attribute of a car's charge plan sensor (JSON text, as in v2) as a dict."""
    if isinstance(raw, dict):
        return raw
    try:
        p = json.loads(raw) if isinstance(raw, str) else None
    except ValueError:
        return {}
    return p if isinstance(p, dict) else {}


def priority(cars: list[Car]) -> list[str]:
    """The order the cars plan in (decision 4). Connected cars first; among them the cars with an
    active plan by ready-by time, then most kWh, then EV1; then the cars without a plan by most kWh,
    then EV1. Cars that are not connected come last, in the same order."""
    def key(c: Car) -> tuple[Any, ...]:
        dl = c.deadline if c.has_plan else None
        return (0 if c.connected else 1, 0 if dl is not None else 1,
                dl.timestamp() if dl is not None else 0.0, -round(c.need_kwh, 1), c.index)
    return [c.key for c in sorted(cars, key=key)]


def running_quarter(plan: dict[str, Any], now: datetime) -> str | None:
    """The planned slot this car is in right now (its start as in `planned`), if any."""
    for start in plan.get("planned") or []:
        try:
            t = datetime.fromisoformat(str(start))
        except ValueError:
            continue
        if t <= now and (now - t).total_seconds() < 15 * 60:
            return str(start)
    return None


def together_possible(cars: list[Car]) -> bool:
    """Together only when HESC can hold every charger with a plan to its share."""
    sharing = [c for c in cars if c.connected and c.has_plan]
    return len(sharing) > 1 and all(c.can_set_current for c in sharing)


def default_together_w(cars: list[Car]) -> float:
    """Decision 22:40: together never more than one charger on its own. HESC knows a car's charging
    power (the plan's kW, per car), not the installer's value of the charger: the highest of them."""
    # the car's own kW: `kw` is already held to the share when the cars charge together (`kw_car` is
    # what the car can do), else the limit would shrink round after round
    kws = [_num(c.plan.get("kw_car") or c.plan.get("kw")) for c in cars]
    kws = [k for k in kws if k > 0]
    return (max(kws) if kws else 11.0) * 1000


def view_for(key: str, cars: list[Car], mode: str, together_w: float | None,
             planned_now: dict[str, list[str]], now: datetime,
             pausing: set[str] | frozenset[str] = frozenset()) -> dict[str, Any]:
    """The state `ENTITY` has in the round of car `key`.

    planned_now: the planned quarters of the cars that had their round already in this round (the
    cars before this one in the priority order). pausing: cars HESC pauses this round
    (outside_plan_pause), whose grid charging does not block the quarter."""
    order = priority(cars)
    limit = together_w if together_w and together_w > 0 else default_together_w(cars)
    if mode == TOGETHER:
        sharing = [c for c in cars if c.connected and c.has_plan]
        mine = next((c for c in sharing if c.key == key), None)
        # whole amperes on 3 phases (current.py counts 3 until it measured the phases): what the
        # charger really gives, so the plan reckons with that
        share = (math.floor(limit / len(sharing) / 690) * 690) if mine is not None else None
        return {"state": TOGETHER, "attributes": {"blocked": [], "max_w": share, "order": order,
                                                   "limit_w": limit}}
    blocked: list[str] = []
    for other in order:
        if other == key:
            break
        blocked += planned_now.get(other, [])
    # Decision 5: no switch within a quarter. After the first round of a quarter, the quarter a car has
    # in its plan stays that car's (also when it stops early); when both have it, the order decides.
    # At the start of a quarter the order alone decides. A car that charges from the grid outside its
    # plan (e.g. left alone after plugging in while charging) always keeps the quarter: the grid sees
    # it whatever HESC planned.
    quarter = now.replace(minute=now.minute - now.minute % 15, second=0, microsecond=0)
    boundary = (now - quarter).total_seconds() < 30
    locks = {c.key: running_quarter(c.plan, now) for c in cars}
    for c in cars:
        if c.key == key:
            continue
        q = locks.get(c.key)
        if q and not boundary:
            if not (locks.get(key) == q and order.index(key) < order.index(c.key)):
                blocked.append(q)
        if c.grid_now and not q and c.key not in pausing:  # a car HESC pauses now gives its quarter free
            blocked.append(quarter.isoformat())
        elif c.grid_this_quarter and not boundary and c.key not in pausing:
            # it charged in this quarter and its plan dropped the quarter (a cheaper one came up):
            # the rest of the quarter stays unused rather than switching within it
            blocked.append(quarter.isoformat())
    blocked = sorted(set(blocked))
    # A car with another car after it plans one quarter extra: a charger needs a little longer than the
    # plan counts (starting up), and at the end the other car has the quarters the single-car safety
    # net would use. Unused, the quarter goes back to the other car at the next quarter.
    after_me = [c for c in order[order.index(key) + 1:] if any(x.key == c and x.connected and x.has_plan for x in cars)] \
        if key in order else []
    extra = 1 if after_me else 0
    return {"state": AFTER, "attributes": {"blocked": blocked, "max_w": None, "order": order, "limit_w": limit,
                                           "extra_quarters": extra}}


# ---- automatic: the cheapest way in which both cars are ready in time ----------------------------
def _slots(prices: list[dict[str, Any]], now: datetime, deadline: datetime) -> list[tuple[str, float]]:
    out = []
    for p in prices:
        try:
            start, end = datetime.fromisoformat(str(p["start"])), datetime.fromisoformat(str(p["end"]))
            value = float(p["value"])
        except (KeyError, TypeError, ValueError):
            continue
        if end > now and end <= deadline:
            out.append((start.isoformat(), value))
    return out


def estimate(cars: list[Car], prices: list[dict[str, Any]], now: datetime, mode: str,
             together_w: float | None) -> tuple[float, float]:
    """(grid cost, kWh short of the goals) of the cars with a plan when they share the grid this way.
    A rough count of the plan's own sums (cheapest quarters before the ready-by time)."""
    planning = [c for c in cars if c.connected and c.has_plan and c.deadline is not None]
    order = [k for k in priority(cars) if any(c.key == k for c in planning)]
    by_key = {c.key: c for c in planning}
    limit = together_w if together_w and together_w > 0 else default_together_w(cars)
    cost = short = 0.0
    taken: set[str] = set()
    for key in order:
        c = by_key[key]
        kwh = _num(c.plan.get("grid_kwh_needed"))
        kw = _num(c.plan.get("kw_car") or c.plan.get("kw")) or 11.0
        if mode == TOGETHER:
            kw = min(kw, limit / 1000 / len(planning))
        free = sorted((v, s) for s, v in _slots(prices, now, c.deadline) if mode == TOGETHER or s not in taken)  # type: ignore[arg-type]
        n = int(-(-kwh // (kw * 0.25))) if kw > 0 and kwh > 0 else 0
        pick = free[:n]
        got = min(kwh, len(pick) * kw * 0.25)
        cost += sum(v for v, _ in pick) * kw * 0.25 if pick else 0.0
        short += max(kwh - got, 0.0)
        taken.update(s for _, s in pick)
    return cost, short


def choose_mode(setting: str, cars: list[Car], prices: list[dict[str, Any]], now: datetime,
                together_w: float | None, prev: str | None, may_change: bool) -> str:
    """The way of sharing for this round. A fixed choice of the user is kept (together falls back to
    one after the other when HESC cannot hold the chargers to their share). Automatic: the cheaper
    way in which both are ready in time; it only changes when `may_change` (a quarter boundary)."""
    if prev in (AFTER, TOGETHER) and not may_change:
        return prev  # decision 5: the way of sharing changes on a quarter boundary only
    if setting == TOGETHER:
        return TOGETHER if together_possible(cars) else AFTER
    if setting == AFTER or not together_possible(cars):
        return AFTER
    a_cost, a_short = estimate(cars, prices, now, AFTER, together_w)
    t_cost, t_short = estimate(cars, prices, now, TOGETHER, together_w)
    if round(a_short, 2) != round(t_short, 2):
        return AFTER if a_short < t_short else TOGETHER
    if t_cost < a_cost * 0.99:  # at least 1 % cheaper, else keep it simple: one after the other
        return TOGETHER
    return AFTER


def extra_quarters(get: Any) -> int:
    """For plan.py: quarters this car plans on top of what it needs (margin for the car after it)."""
    st = get(ENTITY) if get is not None else None
    return int(_num((st[1] or {}).get("extra_quarters"))) if st else 0


def blocked_set(get: Any) -> tuple[set[str], float | None]:
    """For plan.py: the quarter starts this car may not plan and the most it may take (kW), from
    `ENTITY` in its view. (set(), None) without the entity."""
    st = get(ENTITY) if get is not None else None
    if not st:
        return set(), None
    attrs = st[1] or {}
    out = set()
    for q in attrs.get("blocked") or []:
        try:
            out.add(datetime.fromisoformat(str(q)).isoformat())
        except ValueError:
            continue
    mw = attrs.get("max_w")
    return out, (_num(mw) / 1000 if mw else None)


# ---- the sun for two cars (decision 6) ----------------------------------------------------------
# "Eerst krijgt één auto zijn volle stroom; de rest gaat naar de tweede auto als dat genoeg is om diens
# laadpaal te laten starten (startniveau per laadpaal)." The chargers follow the sun themselves (Eco);
# two of them watching one meter start together and then both take too little sun (the grid makes up
# the difference). HESC's lever is the one v3 already uses after grid charging: pause the charger and
# send it back to its own solar mode. HESC pauses only a charger it may pause (a pause switch and a
# "back to solar" entity are set) and only releases what it paused itself.
QUARTER_S: Final = 15 * 60
NEVER_RAN_W: Final = 4300.0  # above every charger's start level (3 x 6 A = 4.14 kW, Alfen/Zappi 4.2 kW)


@dataclass
class SunCar:
    """What the sun division needs of one car."""

    key: str
    index: int
    connected: bool = False
    solar: bool = False          # its charger is in its own solar mode and HESC's plan does not grid charge
    power_w: float = 0.0         # what it draws now
    soc: float | None = None
    full_soc: float = 80.0       # "EV full at battery level"
    battery_kwh: float = 0.0
    start_w: float = 1380.0      # the start level of its charger in its solar mode (charger_specs.py)
    active_w: float = 400.0      # "EV charging threshold"
    can_hold: bool = False       # HESC can pause it and send it back to solar

    @property
    def need_kwh(self) -> float:
        if self.soc is None:
            return 0.0
        return max(self.full_soc - self.soc, 0.0) / 100 * self.battery_kwh

    @property
    def full(self) -> bool:
        return self.soc is not None and self.soc >= self.full_soc


@dataclass
class SunState:
    """Kept between rounds."""

    leader: str | None = None
    held: set[str] = field(default_factory=set)   # cars HESC holds (paused) now
    done: set[str] = field(default_factory=set)   # leaders that are full or do not take the sun
    idle_since: datetime | None = None            # the leader draws nothing while there is sun for it
    ran_w: dict[str, float] = field(default_factory=dict)  # lowest power a car charged at on the sun


def _at_boundary(now: datetime) -> bool:
    return now.minute % 15 == 0 and now.second < 30


def sun_division(cars: list[SunCar], grid_w: float | None, now: datetime, state: SunState,
                 pv_w: float | None = None) -> SunState:
    """Which cars HESC holds back from the sun this round (decision 6, with 4 and 5).

    * The leader takes the sun first. It is chosen among the cars on the sun by most kWh needed, then
      EV1 (decision 4), and stays the leader until it is full, does not take the sun for a quarter
      while there is clearly enough for it, or is unplugged (no swapping back and forth).
    * A follower that draws nothing is held while the leader does not charge yet, and while the sun
      the leader leaves (export) is below the follower charger's start level: that changes nothing on
      the grid and keeps two chargers from starting on the same sun. It is let go on a quarter
      boundary once the leader charges and the export reaches the follower's start level (decision 5).
    * A follower that charges while the house takes power from the grid is held again on a quarter
      boundary: the leader keeps its sun, the follower would only charge from the grid.
    * Without sun to share (``pv_w`` below every start level: night, dusk) nobody is held.

    The caller pauses the cars that became held and sends a car back to solar only when it was let go
    while it is still on the sun (not when HESC's plan took it over or it was unplugged).
    """
    s = SunState(leader=state.leader, held=set(state.held), done=set(state.done), idle_since=state.idle_since,
                 ran_w=dict(state.ran_w))
    by_key = {c.key: c for c in cars}
    for c in cars:
        if not c.connected:
            s.ran_w.pop(c.key, None)
        elif c.solar and c.power_w > c.active_w and c.key not in s.held:
            s.ran_w[c.key] = min(s.ran_w.get(c.key, c.power_w), c.power_w)
    s.done = {k for k in s.done if k in by_key and by_key[k].connected and by_key[k].solar}
    for c in cars:
        if c.full and c.connected:
            s.done.add(c.key)
    sun = [c for c in cars if c.connected and c.solar and c.key not in s.done]
    s.held &= {c.key for c in sun}  # a car that left the sun (plan, unplugged, full) is not HESC's to hold
    if sun and pv_w is not None and pv_w < min(c.start_w for c in sun):
        # no sun to share (night, dusk): nothing to hold back, and the leader is chosen afresh tomorrow
        return SunState(leader=None, held=set(), done=s.done, idle_since=None, ran_w=s.ran_w)
    if len(sun) < 2 or grid_w is None:
        # one car (or none) wants the sun: nobody is held back. A car HESC held is let go on the next
        # quarter boundary (decision 5); one that is no longer on the sun at once (nothing to hold).
        s.held = {k for k in s.held if k in by_key and by_key[k].connected and by_key[k].solar
                  and k not in s.done and not _at_boundary(now)}
        s.leader = sun[0].key if sun else None
        s.idle_since = None
        return s
    if s.leader not in {c.key for c in sun}:
        s.leader = sorted(sun, key=lambda c: (-round(c.need_kwh, 1), c.index))[0].key
        s.idle_since = None
    leader = by_key[s.leader]
    s.held.discard(leader.key)
    export = max(-grid_w, 0.0)
    # The leader does not take the sun that is clearly there for it (its car is full at its own limit,
    # or it refuses): more export than it charged at before (or than any charger needs to start, when
    # it did not charge yet) for a quarter.
    if leader.power_w <= leader.active_w and export >= max(s.ran_w.get(leader.key, NEVER_RAN_W), leader.start_w):
        s.idle_since = s.idle_since or now
        if (now - s.idle_since).total_seconds() >= QUARTER_S:
            s.done.add(leader.key)
            return sun_division(cars, grid_w, now, SunState(None, s.held, s.done, None, s.ran_w))
    else:
        s.idle_since = None
    for f in sun:
        if f.key == leader.key or not f.can_hold:
            s.held.discard(f.key)
            continue
        leader_runs = leader.power_w > leader.active_w
        if f.key in s.held:
            if leader_runs and export >= f.start_w and _at_boundary(now):
                s.held.discard(f.key)
        elif f.power_w <= f.active_w:
            # before the leader charges: at once (two chargers must not start on the same sun);
            # otherwise on a quarter boundary, so a passing cloud gives at most one command a quarter
            if not leader_runs or (export < f.start_w and _at_boundary(now)):
                s.held.add(f.key)
        elif grid_w > f.active_w and _at_boundary(now):
            s.held.add(f.key)
    return s


# ---- comfort guard for the house connection (part D) --------------------------------------------
# Decisions 31-10-2026 09:56-10:10: the first start asks the house connection and whether a load
# balancer takes the house into account. Without one ("No" or "Don't know") HESC keeps house + cars
# under the connection by lowering only the normal charging current (hard rule 30-10 21:54 stays).
# 09:59: "het is een comfortbewaking, meer niet ... de gebruiker blijft te allen tijde
# verantwoordelijk dat er geen overbelasting komt." HESC promises nothing; protection stays with the
# charger, the load balancer and the installer. Also with one car (there is no second car to wait).
GUARD: Final = "sensor.hesc_v4_internal_house_guard"
GUARD_MARGIN: Final = 0.10   # proposal 31-10 (not decided yet): 10 % below the connection
GUARD_ROOM_W: Final = 300.0  # raise again only with this much room left (no up and down)
VOLT: Final = 230.0


def parse_connection(value: Any) -> tuple[int, float] | None:
    """'3x25 A' -> (3, 25.0); 'Not set' or anything else -> None."""
    import re

    m = re.fullmatch(r"\s*([13])\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*A?\s*", str(value or ""))
    return (int(m.group(1)), float(m.group(2).replace(",", "."))) if m else None


def house_limit_w(connection: Any) -> float | None:
    p = parse_connection(connection)
    return p[0] * p[1] * VOLT * (1 - GUARD_MARGIN) if p else None


@dataclass
class GuardCar:
    key: str
    power_w: float = 0.0
    current_a: float | None = None   # the charging current set on the charger now
    phases: int = 3                  # measured, else the house connection's (decision 22:02 a)
    can_set_current: bool = False
    min_a: float = 6.0
    max_a: float = 16.0              # the charger integration's maximum


@dataclass
class GuardState:
    caps: dict[str, float] = field(default_factory=dict)  # car -> most current HESC allows now (A)


def guard_kw(get: Any) -> float | None:
    """For plan.py: the most this car charges with while the comfort guard holds it (kW), else None."""
    st = get(GUARD) if get is not None else None
    mw = _num((st[1] or {}).get("max_w")) if st else 0.0
    return mw / 1000 if mw > 0 else None


def comfort_guard(cars: list[GuardCar], grid_w: float | None, connection: Any, load_balancer: Any,
                  state: GuardState) -> GuardState:
    """The most current each car may charge with, so house + cars stay under the connection.

    ``cars`` in priority order (decision 4): the last one is lowered first and raised last. Only cars
    whose charging current HESC can set; never below the charger's minimum (6 A) - HESC does not
    pause for this (only the normal charging current, decision 09:58)."""
    limit = house_limit_w(connection)
    if limit is None or str(load_balancer or "") == "Yes" or grid_w is None:
        return GuardState()
    by_key = {c.key: c for c in cars}
    caps = {k: v for k, v in state.caps.items() if k in by_key and by_key[k].can_set_current}
    over = grid_w - limit
    if over > 0:
        for c in reversed(cars):
            if over <= 0:
                break
            if not c.can_set_current or c.current_a is None or c.power_w <= 0:
                continue
            step = c.phases * VOLT
            now_a = min(caps.get(c.key, c.max_a), c.current_a)
            if c.key in caps and caps[c.key] < c.current_a:
                over -= (c.current_a - caps[c.key]) * step  # lowered already, the charger did not follow yet
                if over <= 0:
                    break
                now_a = caps[c.key]
            new = max(c.min_a, now_a - math.ceil(over / step))
            if new < now_a:
                caps[c.key] = float(new)
                over -= (now_a - new) * step
    else:
        room = -over - GUARD_ROOM_W
        for c in cars:
            if c.key not in caps:
                continue
            step = c.phases * VOLT
            up = math.floor(room / step)
            if up <= 0:
                break
            new = caps[c.key] + up
            if new >= c.max_a:
                room -= (c.max_a - caps[c.key]) * step
                del caps[c.key]
            else:
                caps[c.key] = float(new)
                room -= up * step
    return GuardState(caps=caps)


# ---- a car that charges by itself while the other car needs the grid (decision 31-10 13:55) -----
# v3 leaves a car alone that was already charging when it was plugged in ("EV already charging, left
# alone"). With two cars that car takes the quarters the other car needs. Decision 31-10-2026
# 13:55 ("1 ja", on the advice of 13:45): only with two cars, on a quarter boundary, only when the other
# car would otherwise not be in time, never for HESC's own "charge now".
@dataclass
class OutsideState:
    paused: dict[str, str] = field(default_factory=dict)  # car HESC paused -> the car it gave way to
    since: dict[str, datetime] = field(default_factory=dict)  # when HESC paused it


PAUSE_SETTLE_S: Final = 180  # a cloud charger may show its old power for a while after a pause


def outside_plan_pause(cars: list[Car], now: datetime, state: OutsideState) -> OutsideState:
    """Which cars HESC keeps paused because another car needs the grid. A paused car is let go
    (back on) when the car it gave way to no longer needs it: unplugged, no plan, goal reached or
    ready-by time passed. A paused car that is unplugged is simply forgotten."""
    by_key = {c.key: c for c in cars}
    paused: dict[str, str] = {}
    since: dict[str, datetime] = {}
    for a, b in state.paused.items():
        ca, cb = by_key.get(a), by_key.get(b)
        if ca is None or not ca.connected:
            continue  # unplugged: nothing to give back
        at = state.since.get(a, now)
        if ca.grid_now and (now - at).total_seconds() > PAUSE_SETTLE_S:
            continue  # charging again (its own plan, or someone switched it on): no longer HESC's pause
        done = cb is None or not cb.connected or not cb.has_plan or (cb.deadline is not None and now >= cb.deadline)
        if done and _at_boundary(now):
            continue  # the other car is done: let this one go, on a quarter boundary (decision 5)
        paused[a] = b
        since[a] = at
    if _at_boundary(now):
        for a in cars:
            if a.key in paused or not (a.outside_plan and a.can_pause and a.connected and a.grid_now):
                continue
            for b in cars:
                if b.key != a.key and b.connected and b.has_plan and bool(b.plan.get("short_of_time")):
                    paused[a.key] = b.key
                    since[a.key] = now
                    break
    return OutsideState(paused=paused, since=since)


def outside_released(before: OutsideState, after: OutsideState, cars: list[Car]) -> list[str]:
    """The cars HESC switches back on: let go while still paused (not the ones charging again)."""
    by_key = {c.key: c for c in cars}
    return sorted(k for k in before.paused if k not in after.paused and k in by_key
                  and by_key[k].connected and not by_key[k].grid_now)


# ---- two cars on one charger, taking turns (step 3, decisions 26 and 30-32) ----------------------
# 31: one cable swap time ("kabel omzetten uiterlijk om ..."); the first car charges before it, the
# second after it. The car on the charger before that time is ready by it (its own ready-by time
# when that is earlier); the car that is not on the charger sees the charger as not connected.
DEFAULT_SWAP: Final = "22:30"  # proposal 31-10 14:35 ("tussen 10 en 11 uur", decision 30-10 23:56)


def next_swap(now: datetime, hhmm: Any) -> datetime | None:
    """The next cable swap moment at or after `now` (today, or tomorrow when it has passed)."""
    try:
        h, m = (int(x) for x in str(hhmm or "").strip().split(":")[:2])
        t = now.replace(hour=h, minute=m, second=0, microsecond=0)
    except ValueError:
        return None
    return t if t > now else t + timedelta(days=1)


SWAP_MARGIN: Final = timedelta(minutes=30)  # decision 31-10-2026 15:09


def swap_ready_by(now: datetime, hhmm: Any) -> datetime | None:
    """When the car on a shared charger must be ready: half an hour before the cable swap time, because
    people often move the cable before "at the latest" (windtunnel 22:07). Within that half hour the
    swap time itself, so the car does not fall back to its own (later) ready-by."""
    sw = next_swap(now, hhmm)
    if sw is None:
        return None
    return sw - SWAP_MARGIN if now < sw - SWAP_MARGIN else sw


def ready_by(get: Any) -> datetime | None:
    """For plan.py: the cable swap time this car must be ready by, from `ENTITY` in its view."""
    st = get(ENTITY) if get is not None else None
    raw = (st[1] or {}).get("ready_by") if st else None
    try:
        return datetime.fromisoformat(str(raw)) if raw else None
    except ValueError:
        return None


def cable_moved(before: str | None, now: str | None, before_plan_charging: bool) -> bool:
    """True when the cable went from one car to the other while HESC's plan charged the first car from
    the grid: that charging is not the new car's, so the charger goes back to its own mode and the new
    car's own plan decides (otherwise the new car would be "already charging, left alone")."""
    return bool(before and now and before != now and before_plan_charging)
