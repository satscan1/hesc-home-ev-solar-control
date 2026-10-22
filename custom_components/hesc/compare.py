"""Differences log with v2.

While v3 runs in shadow next to v2, it compares every 30-second round what v2 really shows
with what v3 would show, per part: solar charging / release (state text), charge plan control
(status text), the planned quarters, kickstart (status text), EV battery level (value and
source) and the notice line. v3's own "[shadow] " prefix is ignored. A difference is logged
when it lasts at least two rounds (one minute; the two run on their own 30-second clocks),
once, with both values and both reasons; when the two agree again that is logged too. Each
day gets one summary line (rounds compared, decisions of v2 = changes of its values,
differences), also with 0 differences. Only reads v2; switches nothing.
File: /config/hesc_v3/compare_log.jsonl (about 30 days).

Since rc3: the sensor's counters (rounds, decisions) changed every round, so Home
Assistant stored a new history row every 30 s (about 2,880 a day). The sensor now shows the
counters as of the last refresh: at most every PUBLISH_ROUNDS rounds (15 min), and at once when
the number of differences, the last difference or the day changes. The log file is unchanged.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

SHADOW = "[shadow] "
KEEP_DAYS = 30
PUBLISH_ROUNDS = 30  # 30 rounds of 30 s = 15 min


def norm(v: Any) -> str:
    s = "" if v is None else str(v)
    return s[len(SHADOW):] if s.startswith(SHADOW) else s


@dataclass
class Part:
    v2: str = ""
    v3: str = ""
    rounds_diff: int = 0
    open: bool = False  # a logged difference that has not ended yet


@dataclass
class CompareLog:
    day: str = ""
    parts: dict[str, Part] = field(default_factory=dict)
    rounds: int = 0
    decisions: int = 0
    differences: int = 0
    last: dict[str, Any] | None = None
    shown: dict[str, Any] | None = None  # what the sensor shows (rc3: refreshed at most every 15 min)

    def round(self, ts: str, day: str, values: dict[str, tuple[Any, Any, Any, Any]]) -> list[dict[str, Any]]:
        """values: part -> (v2 value, v3 value, v2 reason, v3 reason); None for v2 = not available.
        Returns the new log lines."""
        out: list[dict[str, Any]] = []
        if self.day and day != self.day:
            out.append(self.summary())
            self.rounds = self.decisions = self.differences = 0
        self.day = day
        self.rounds += 1
        for name, (a, b, ra, rb) in values.items():
            if a is None:
                continue
            p = self.parts.setdefault(name, Part())
            a2, b2 = norm(a), norm(b)
            if p.v2 and a2 != p.v2:
                self.decisions += 1
            p.v2, p.v3 = a2, b2
            if a2 != b2:
                p.rounds_diff += 1
                if p.rounds_diff == 2 and not p.open:
                    p.open = True
                    self.differences += 1
                    line = {"ts": ts, "type": "difference", "part": name, "v2": a2, "v3": b2,
                            "v2_reason": norm(ra), "v3_reason": norm(rb)}
                    self.last = line
                    out.append(line)
            else:
                if p.open:
                    out.append({"ts": ts, "type": "same_again", "part": name, "value": a2})
                p.rounds_diff, p.open = 0, False
        return out

    def summary(self) -> dict[str, Any]:
        return {"type": "day", "date": self.day, "rounds": self.rounds, "decisions": self.decisions,
                "differences": self.differences}

    def sensor(self) -> tuple[str, dict[str, Any]]:
        now = {"date": self.day, "rounds": self.rounds, "decisions": self.decisions, "last_difference": self.last}
        old = self.shown
        if (old is None or old["date"] != self.day or old["last_difference"] != self.last
                or self.rounds - old["rounds"] >= PUBLISH_ROUNDS or self.rounds < old["rounds"]):
            self.shown = now
        return str(self.differences), dict(self.shown)


def trim(lines: list[str], today: str) -> list[str]:
    """Keep about KEEP_DAYS days (by the date in each line)."""
    from datetime import date, timedelta

    cut = (date.fromisoformat(today) - timedelta(days=KEEP_DAYS)).isoformat()
    keep = []
    for ln in lines:
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        day = d.get("date") or str(d.get("ts", ""))[:10]
        if day >= cut:
            keep.append(ln)
    return keep


def plan_key(plan_attr: Any) -> str | None:
    """The planned quarters of a charge plan attribute (v2's JSON text), for comparing."""
    if plan_attr is None:
        return None
    try:
        p = json.loads(plan_attr) if isinstance(plan_attr, str) else plan_attr
    except ValueError:
        return str(plan_attr)
    if not isinstance(p, dict):
        return ""
    return json.dumps({"active": p.get("active"), "planned": p.get("planned"), "goal": p.get("goal"),
                       "deadline": p.get("deadline")}, sort_keys=True)
