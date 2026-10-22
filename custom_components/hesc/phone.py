"""Phones, Siri and the Apple Watch (since 3.0.0): the one-line summary and the widget refresh.

`summary()` gives sensor "Summary for phone and watch". iOS refreshes its home-screen widgets only
every 15 minutes or so; the lock-screen (Details / Gauge) widgets of the Companion app refresh at once
on a silent notification with message "update_widgets". `WidgetPush` decides when HESC sends one to
the phones in its phone list: when something that matters in the summary changes (plugged in, plan,
goal, charging or not, the battery level per 10 %), at most once every 20 minutes, so
the daily budget iOS gives these updates is never used up. Only to iPhones and iPads with the
Companion app: "update_widgets" is an iOS command; Android and any other notify service would show
the word as a message (Android widgets refresh by themselves).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

from homeassistant.util import dt as dt_util

from . import charge_now

MIN_GAP = timedelta(minutes=20)
MESSAGE = "update_widgets"


def summary(soc: Any, plan_raw: Any, state: Any, now: datetime, plan_status: Any = None,
            plugged_in: bool | None = None) -> tuple[str | None, dict[str, Any]]:
    """One line for a phone widget or the Apple Watch, from values HESC already has (since 3.0.0).

    "EV 72% → 80% by Sat 24-10 07:00 · Charging on sun · grid Fri 02:00" (plan active), "EV 91% · Idle"."""
    try:
        soc_v = round(float(soc)) if soc not in (None, "", "unknown", "unavailable") else None
    except (TypeError, ValueError):
        soc_v = None
    plan: dict[str, Any] = {}
    if isinstance(plan_raw, dict):
        plan = plan_raw
    elif isinstance(plan_raw, str) and plan_raw.strip().startswith("{"):
        try:
            plan = json.loads(plan_raw)
        except ValueError:
            plan = {}
    active = bool(plan.get("active"))
    if active and plan_status not in (None, "", "unknown", "No active plan"):
        state = plan_status  # while a plan runs its own status says more than the release status ("Idle")
    goal = plan.get("goal") if active else None
    deadline_text = plan.get("deadline_text") if active else None
    nxt = None
    if active:
        for q in plan.get("planned") or []:
            t = dt_util.parse_datetime(str(q))
            if t is not None and t > now:
                nxt = t if nxt is None or t < nxt else nxt
    ev = "EV " + (f"{soc_v}%" if soc_v is not None else "?")
    now_charge = active and plan.get("source") == charge_now.SOURCE
    if goal is not None and now_charge:
        ev += f" \u2192 {goal}% now"  # charge now: the end time is only a give-up time
    elif goal is not None:
        ev += f" \u2192 {goal}%" + (f" by {deadline_text}" if deadline_text else "")
    parts = [ev]
    if plugged_in is False:
        parts.append("not plugged in")  # shown in the widget too
    elif state not in (None, "", "unknown"):
        parts.append(str(state))
    if nxt is not None and not now_charge:
        parts.append("grid " + dt_util.as_local(nxt).strftime("%a %H:%M"))
    attrs = {"ev_battery": soc_v, "plan_active": active, "goal": goal, "ready_by": plan.get("deadline") if active else None,
             "next_grid_quarter": nxt.isoformat() if nxt is not None else None, "doing": state,
             "plugged_in": plugged_in, "charge_now": now_charge}
    return " \u00b7 ".join(parts)[:255], attrs


def widget_key(text: str | None, attrs: dict[str, Any]) -> tuple:
    """What has to change before the phones are asked to refresh their widgets."""
    soc = attrs.get("ev_battery")
    doing = str(attrs.get("doing") or "").lower()
    charging = "charging" in doing and "not charging" not in doing
    return (attrs.get("plugged_in"), attrs.get("plan_active"), attrs.get("goal"), attrs.get("ready_by"),
            attrs.get("charge_now"), charging, None if soc is None else int(soc) // 10)


def phones(notify_services: Any, apple: set[str] | None = None) -> list[str]:
    """The Companion app phones in HESC's phone list (notify.mobile_app_*); with `apple`, only those."""
    out = [x.strip() for x in str(notify_services or "").split(",")]
    return [x for x in out if x.startswith("notify.mobile_app_") and (apple is None or x in apple)]


def apple_devices(hass: Any) -> set[str]:
    """notify.mobile_app_<name> of every Companion app device that runs iOS or iPadOS."""
    from homeassistant.util import slugify

    out = set()
    for entry in hass.config_entries.async_entries("mobile_app"):
        d = entry.data or {}
        os_name = str(d.get("os_name") or "").lower()
        if os_name in ("ios", "ipados") or str(d.get("manufacturer") or "").lower() == "apple":
            out.add("notify.mobile_app_" + slugify(str(d.get("device_name") or "")))
    return out


class WidgetPush:
    """At most one "update_widgets" every MIN_GAP; a change within the gap is sent when the gap ends."""

    def __init__(self) -> None:
        self.key: tuple | None = None
        self.sent_key: tuple | None = None
        self.last: datetime | None = None

    def due(self, key: tuple, now: datetime) -> bool:
        """True when a refresh should go out now (the caller sends it)."""
        if self.key is None and self.sent_key is None:
            self.key = self.sent_key = key  # first round after a start: nothing has changed yet
            return False
        self.key = key
        if key == self.sent_key:
            return False
        if self.last is not None and now - self.last < MIN_GAP:
            return False  # checked again every round; goes out once the gap is over
        self.sent_key, self.last = key, now
        return True
