"""Price fetch (action-only price sources) and holidays, ported from v2.0.0's package.

- `fetch_plan` / `fetch_rows`: v2's trigger template "HESC price fetch" (every 30 minutes):
  which action to call for EnergyZero / ANWB Energie, EasyEnergy, Tibber and Nord Pool
  (official), with which data, and how the two answers become one list of rows.
- `holiday_calendar` / `holidays`: v2's trigger template "HESC holidays" (every 6 hours):
  a Monday-Friday that is not in the Workday calendar counts as a holiday.
Proven against the original templates (`tests/integration/test_pricefetch_parity.py`).
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import timedelta
from typing import Any

from homeassistant.util import dt as dt_util

ACTION_SOURCES = {
    "EnergyZero / ANWB Energie": "energyzero.get_energy_prices",
    "EasyEnergy": "easyenergy.get_energy_usage_prices",
    "Tibber": "tibber.get_prices",
    "Nord Pool (official)": "nordpool.get_prices_for_date",
}


def fetch_plan(src: str, entry: str) -> tuple[str, dict[str, Any], dict[str, Any]] | None:
    """(action, data for today, data for tomorrow), or None when the source needs no action.

    entry: the config entry id of the price sensor ('' when unknown).
    """
    if src not in ACTION_SOURCES:
        return None
    t0 = dt_util.start_of_local_day()
    t0s, t2s = t0.isoformat(), (t0 + timedelta(days=2)).isoformat()
    now = dt_util.now()
    d0, d1 = str(now.date()), str((now + timedelta(days=1)).date())
    if src == "Tibber":
        dat1: dict[str, Any] = {"start": t0s, "end": t2s}
    elif src == "Nord Pool (official)":
        dat1 = {"config_entry": entry, "date": d0}
    else:
        dat1 = {"config_entry": entry, "incl_vat": True, "start": t0s, "end": t2s}
    dat2 = {"config_entry": entry, "date": d1} if src == "Nord Pool (official)" else dat1
    return ACTION_SOURCES[src], dat1, dat2


def fetch_rows(r1: Any, r2: Any) -> list[Any]:
    """Attribute `rows`: the price lists of both answers, whatever their wrapping."""
    out: list[Any] = []
    for r in (r1 if r1 is not None else {}, r2 if r2 is not None else {}):
        x = r
        if isinstance(x, dict) and x.get("prices") is not None:
            x = x.get("prices")
        if isinstance(x, dict):
            x = list(x.values())[0] if len(x) > 0 else []
        if _iterable(x):
            out = out + list(x)
    return out


def fetch_div(src: str) -> int:
    return 1000 if src == "Nord Pool (official)" else 1


def _iterable(x: Any) -> bool:
    if isinstance(x, str) or x is None:
        return False
    try:
        iter(x)
    except TypeError:
        return False
    return True


def holiday_calendar(workday_entities: Iterable[str], calendar_ids: Iterable[str]) -> str:
    """The Workday calendar v2 uses: '' when there is none."""
    cands = [e for e in workday_entities if re.match("calendar", e)] + [e for e in calendar_ids if re.search("workday", e)]
    return cands[0] if cands else ""


def holidays(cal: str, events: Any) -> tuple[int, list[str], str]:
    """(state, attribute dates, attribute source) from the calendar answer `events`
    (the response of calendar.get_events, or None when the call failed)."""
    if cal and isinstance(events, dict) and events.get(cal):
        wd = [e.get("start") for e in (events[cal].get("events") or [])]
        dates = []
        now = dt_util.now()
        for i in range(-100, 31):
            day = (now + timedelta(days=i)).date()
            if day.weekday() < 5 and day.isoformat() not in wd:
                dates.append(day.isoformat())
        return len(dates), dates, cal
    return 0, [], cal or "none"
