"""Phase advice (since rc3).

Some chargers need enough surplus on EVERY phase before they start (Wallbox Eco: 480 W per phase,
rule from practice; Easee: 6 A per phase). When the sun is spread unevenly over the phases
(for example 45/34/21 %), the weakest phase decides when the car can charge on the sun. This advice shows that,
from the house's own meter per phase, and only says what it has seen:

* It starts with the spread of the surplus over the phases (works anywhere, any season).
* Whether the weakest phase really stops the charger follows from the measurements.
* The sunniest period is not taken from months (Dutch "March-June" means nothing elsewhere) but
  from the height of the sun at noon at the location of Home Assistant: days when the sun gets
  within TOP_MARGIN_DEG of its highest point of the year. Southern hemisphere: automatically
  around December; near the equator: almost the whole year.

Stages: ``not_available`` (no meter per phase, or the car charges on 1 phase) -> ``measuring``
(fewer than NEED_DAYS days with usable sun) -> ``provisional`` (spread known, sunniest period not
seen yet) -> ``confirmed`` (NEED_TOP_DAYS usable days in the sunniest period seen).
Information only: it never switches anything.

Measured per 30-second round, only while the car is NOT charging (then the meter shows what the
charger would see): surplus per phase = minus the grid power of that phase (import positive).
"""

from __future__ import annotations

import math
from functools import lru_cache
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from .charger_specs import StartSpec

USEFUL_W = 1000.0        # a round "has usable sun" when the total surplus is at least this
USEFUL_DAY_MIN = 30.0    # a day counts when it had at least this many minutes of usable sun
NEED_DAYS = 14
NEED_TOP_DAYS = 10
TOP_MARGIN_DEG = 10.0
KEEP_DAYS = 400
ROUND_S = 30.0

STAGES = ("not_available", "measuring", "provisional", "confirmed")


# ---- where the sun is ---------------------------------------------------------------------------

def declination_deg(d: date) -> float:
    """Declination of the sun (Cooper's formula), degrees."""
    n = d.timetuple().tm_yday
    return 23.44 * math.sin(math.radians(360.0 / 365.0 * (284 + n)))


def noon_elevation_deg(latitude: float, d: date) -> float:
    return 90.0 - abs(latitude - declination_deg(d))


@lru_cache(maxsize=16)
def max_noon_elevation_deg(latitude: float, year: int) -> float:
    d0 = date(year, 1, 1)
    return max(noon_elevation_deg(latitude, d0 + timedelta(days=i)) for i in range(366 if year % 4 == 0 else 365))


def is_top_day(latitude: float, d: date) -> bool:
    return noon_elevation_deg(latitude, d) >= max_noon_elevation_deg(latitude, d.year) - TOP_MARGIN_DEG


@lru_cache(maxsize=16)
def top_period(latitude: float, year: int) -> tuple[date, date] | None:
    """First and last day of the sunniest period of `year` (for the text; around new year on the
    southern hemisphere the period wraps: then the part starting in the second half is given)."""
    d0 = date(year, 1, 1)
    days = [d0 + timedelta(days=i) for i in range(366 if year % 4 == 0 else 365)]
    top = [d for d in days if is_top_day(latitude, d)]
    if not top:
        return None
    if top[0] == days[0] and top[-1] == days[-1] and len(top) < len(days):  # wraps around new year
        start = next(d for d in reversed(days) if not is_top_day(latitude, d)) + timedelta(days=1)
        end = next(d for d in days if not is_top_day(latitude, d)) - timedelta(days=1)
        return start, end.replace(year=year + 1)
    return top[0], top[-1]


@lru_cache(maxsize=8)
def next_top_block(latitude: float, today: date) -> tuple[date, date] | None:
    """The sunniest period that is running now or comes next (from `today`, at most a year ahead):
    first and last day of that block. Near the equator there are two peaks: the next one is given."""
    d = today
    for _ in range(370):
        if is_top_day(latitude, d):
            break
        d += timedelta(days=1)
    else:
        return None
    start, end = d, d
    while is_top_day(latitude, end + timedelta(days=1)) and (end - start).days < 370:
        end += timedelta(days=1)
    if start == today:  # running now: find where it began
        while is_top_day(latitude, start - timedelta(days=1)) and (end - start).days < 370:
            start -= timedelta(days=1)
    return start, end


# ---- counting ---------------------------------------------------------------------------------

@dataclass
class Day:
    date: str
    sun_min: float = 0.0
    surplus_wh: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    blocked_min: float = 0.0   # total enough for a start, but one phase below the per-phase need
    ok_min: float = 0.0        # every phase at or above the per-phase need
    top: bool = False

    def to_json(self) -> dict[str, Any]:
        return {"date": self.date, "sun_min": round(self.sun_min, 1), "surplus_wh": [round(x, 1) for x in self.surplus_wh],
                "blocked_min": round(self.blocked_min, 1), "ok_min": round(self.ok_min, 1), "top": self.top}

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "Day":
        wh = ([float(x) for x in d.get("surplus_wh", [])] + [0.0, 0.0, 0.0])[:3]
        return cls(str(d["date"]), float(d.get("sun_min", 0)), wh,
                   float(d.get("blocked_min", 0)), float(d.get("ok_min", 0)), bool(d.get("top", False)))

    @property
    def usable(self) -> bool:
        return self.sun_min >= USEFUL_DAY_MIN


@dataclass
class PhaseStats:
    days: dict[str, Day] = field(default_factory=dict)

    def round(self, today: date, latitude: float, surplus_w: list[float], spec: StartSpec,
              dt_s: float = ROUND_S) -> None:
        """One round with the surplus per phase (W, export positive) while the car does not charge."""
        key = today.isoformat()
        day = self.days.get(key)
        if day is None:
            day = self.days[key] = Day(key, top=is_top_day(latitude, today))
            self._trim(today)
        total = sum(surplus_w)
        m = dt_s / 60.0
        if total >= USEFUL_W:
            day.sun_min += m
            for i in range(3):
                day.surplus_wh[i] += max(0.0, surplus_w[i]) * dt_s / 3600.0
        need = spec.per_phase
        if need is not None:
            if min(surplus_w) >= need:
                day.ok_min += m
            elif total >= max(3 * need, spec.start_3p):
                day.blocked_min += m

    def _trim(self, today: date) -> None:
        cut = (today - timedelta(days=KEEP_DAYS)).isoformat()
        for k in [k for k in self.days if k < cut]:
            del self.days[k]

    def to_json(self) -> dict[str, Any]:
        return {"version": 1, "days": [d.to_json() for d in sorted(self.days.values(), key=lambda d: d.date)]}

    @classmethod
    def from_json(cls, data: Any) -> "PhaseStats":
        out = cls()
        for d in (data or {}).get("days", []) if isinstance(data, dict) else []:
            try:
                day = Day.from_json(d)
            except (KeyError, TypeError, ValueError):
                continue
            out.days[day.date] = day
        return out


# ---- the advice ---------------------------------------------------------------------------------

def _pct(xs: list[float]) -> list[int]:
    s = sum(xs)
    return [round(100 * x / s) for x in xs] if s > 0 else [0, 0, 0]


def advice(stats: PhaseStats, today: date, latitude: float, spec: StartSpec, *,
           sensors_ok: bool, phases: int | None) -> tuple[str, dict[str, Any]]:
    """State (stage) and attributes of sensor.hesc_phase_advice."""
    period = next_top_block(latitude, today)
    attrs: dict[str, Any] = {
        "friendly_name": "HESC phase advice", "icon": "mdi:sine-wave",
        "need_days": NEED_DAYS, "need_top_days": NEED_TOP_DAYS,
        "top_period": None if period is None else f"{period[0].strftime('%d-%m')} – {period[1].strftime('%d-%m')}",
        "per_phase_need_w": spec.per_phase, "charger_source": spec.source,
    }
    if not sensors_ok:
        attrs["text"] = ("No phase advice: HESC needs the grid power of each phase (choose them under sources). "
                         "With a 1-phase connection there is nothing to spread.")
        return "not_available", attrs
    if phases == 1:
        attrs["text"] = "No phase advice: your car charges on 1 phase, so the spread over the phases does not matter."
        return "not_available", attrs

    usable = [d for d in stats.days.values() if d.usable]
    top = [d for d in usable if d.top]
    sums = [sum(d.surplus_wh[i] for d in usable) for i in range(3)]
    share = _pct(sums)
    weakest = min(range(3), key=lambda i: sums[i]) + 1 if usable else None
    attrs.update({"usable_days": len(usable), "top_days": len(top),
                  "share_phase_1": share[0], "share_phase_2": share[1], "share_phase_3": share[2],
                  "weakest_phase": weakest})

    def per_day(ds: list[Day], key: str) -> float | None:
        return round(sum(getattr(d, key) for d in ds) / len(ds) / 60.0, 1) if ds else None

    if spec.per_phase is not None:
        attrs.update({"blocked_hours_per_day": per_day(usable, "blocked_min"),
                      "blocked_hours_per_day_top": per_day(top, "blocked_min"),
                      "blocked_days_top": sum(1 for d in top if d.blocked_min >= 15)})
    spread = f"{share[0]} / {share[1]} / {share[2]} %"

    if len(usable) < NEED_DAYS:
        lead = f" So far phase {weakest} gets the least ({spread})." if usable else ""
        attrs["text"] = f"Measuring the phases: {len(usable)} of {NEED_DAYS} days with enough sun.{lead}"
        return "measuring", attrs

    if spec.per_phase is None:
        attrs["text"] = (f"Phase {weakest} gets the least of your surplus ({spread}). Your charger looks at the total "
                         f"of the three phases, so this spread does not stop it.")
        return ("confirmed" if len(top) >= NEED_TOP_DAYS else "provisional"), attrs

    need = f"{spec.per_phase:.0f} W on every phase"
    if len(top) < NEED_TOP_DAYS:
        when = ""
        if period:
            when = (f" now (sunniest period until {period[1].strftime('%d-%m')})" if period[0] <= today
                    else f" from {period[0].strftime('%d-%m')}")
        so_far = attrs["blocked_hours_per_day"]
        attrs["text"] = (f"Phase {weakest} gets the least of your surplus ({spread}). Your charger needs {need}. "
                         f"So far that kept it from starting {so_far} h per day. Whether it matters in the sunniest "
                         f"period shows{when} (calculated for your location; {len(top)} of {NEED_TOP_DAYS} days seen).")
        return "provisional", attrs

    b = attrs["blocked_hours_per_day_top"] or 0.0
    if b < 0.1:
        attrs["text"] = (f"Phase {weakest} gets the least of your surplus ({spread}), but in the sunniest period it did "
                         f"not stop your charger ({need}). No change needed.")
    else:
        attrs["text"] = (f"Phase {weakest} gets the least of your surplus ({spread}). In the sunniest period it kept your "
                         f"charger ({need}) from starting on {attrs['blocked_days_top']} days, {b} h per day on average. "
                         f"A more even spread (for example an inverter or panels moved to phase {weakest}) gives up to "
                         f"that much more charging on the sun.")
    return "confirmed", attrs
