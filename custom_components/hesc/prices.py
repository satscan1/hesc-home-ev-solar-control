"""Price adapter: any supported price source -> one list of quarters.

Line-by-line port of v2.0.0's template sensor "HESC prices" (`sensor.hesc_prices`,
`hesc_config.yaml`, variable `p` and the sensor's state and attributes). It runs on
Home Assistant's own date helpers, so dates, time zones and rounding come out the
same as in v2's template. Proven against the original template on random inputs
(`tests/integration/test_prices_parity.py`).
"""
from __future__ import annotations

import math
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from homeassistant.util import dt as dt_util

from .templatecompat import (
    as_datetime,
    forgiving_float,
    jinja_round,
    jinja_str,
    sort_by,
)

# get(entity_id) -> (state, attributes) or None
Getter = Callable[[str], "tuple[str, dict[str, Any]] | None"]

ACTION_SOURCES = ("EnergyZero / ANWB Energie", "EasyEnergy", "Tibber", "Nord Pool (official)")
LIST_SOURCES = ("Price list in sensor", "unknown", "unavailable", "")
CURRENCIES = ("EUR", "SEK", "DKK", "NOK", "GBP", "AUD")
SYMBOL = {"EUR": "€", "SEK": "kr", "DKK": "kr", "NOK": "kr", "GBP": "£", "AUD": "$"}
MINOR = {"EUR": "ct", "SEK": "öre", "DKK": "øre", "NOK": "øre", "GBP": "p", "AUD": "c"}
FX_VS_EUR = {"EUR": 1, "SEK": 11.5, "DKK": 7.46, "NOK": 11.7, "GBP": 0.86, "AUD": 1.75}
_EURO_AFTER = (
    "Berlin", "Busingen", "Madrid", "Canary", "Ceuta", "Paris", "Monaco", "Rome", "Vatican",
    "San_Marino", "Lisbon", "Madeira", "Azores", "Helsinki", "Mariehamn", "Luxembourg", "Athens",
    "Bratislava", "Ljubljana", "Tallinn", "Riga", "Vilnius", "Zagreb", "Andorra",
)
_POINT_DECIMAL = ("London", "Dublin", "Belfast", "Isle_of_Man", "Jersey", "Guernsey", "Gibraltar", "Malta", "Zurich")
_LIST_ATTRS = (
    ("raw_today", "raw_tomorrow"), ("prices_today", "prices_tomorrow"), ("prices", "tomorrow_prices"),
    ("data",), ("forecast",), ("rates",), ("forecasts",),
)
_START_KEYS = ("start", "start_time", "time", "hour", "from", "timestamp", "start_date", "startsAt")
_END_KEYS = ("end", "end_time", "till")
_VALUE_KEYS = ("value", "price", "price_per_kwh", "value_inc_vat", "total", "electricity_price", "per_kwh")


def _states(get: Getter, entity_id: str) -> str:
    st = get(entity_id)
    return "unknown" if st is None else st[0]


def _attr(get: Getter, entity_id: str, name: str) -> Any:
    st = get(entity_id)
    return None if st is None else st[1].get(name)


def _is_list(v: Any) -> bool:
    """Jinja: `v is iterable and v is not string and v is not mapping`."""
    if v is None or isinstance(v, (str, dict)):
        return False
    try:
        iter(v)
    except TypeError:
        return False
    return True


def _first(r: dict, keys: tuple[str, ...]) -> Any:
    """Jinja `a or b or c`: the first truthy value, else the last one."""
    v = None
    for k in keys:
        v = r.get(k)
        if v:
            return v
    return v


def adapt(get: Getter, fetch_rows: Any, fetch_div: Any) -> dict[str, Any]:
    """Variable `p` of the template: now, today, tomorrow, step_min, items_in, cur.

    fetch_rows / fetch_div: the attributes `rows` and `div` of v2's "HESC price fetch"
    (prices from an action-only source).
    """
    src = _states(get, "input_select.hesc_price_source")
    ent = _states(get, "input_text.hesc_price_sensor").strip()
    resmode = _states(get, "input_select.hesc_price_resolution")
    rows: list[Any] = []
    div: float = 1
    if src in LIST_SOURCES:
        u = jinja_str(_attr(get, ent, "unit_of_measurement") or "").lower()
        div = 1000 if "mwh" in u else 1
        for pair in _LIST_ATTRS:
            if not rows:
                for a in pair:
                    v = _attr(get, ent, a)
                    if _is_list(v):
                        rows = rows + list(v)
        # PVPC (Spain): one attribute per hour
        if not rows and _attr(get, ent, "price_00h") is not None:
            t0 = _today_at("00:00")
            for dd0 in (0, 1):
                for h in range(24):
                    v = _attr(get, ent, ("price_" if dd0 == 0 else "price_next_day_") + f"{h:02d}" + "h")
                    if v is not None:
                        ts = t0 + timedelta(days=dd0, hours=h)
                        rows = rows + [{"start": ts.isoformat(), "end": (ts + timedelta(hours=1)).isoformat(), "value": v}]
    else:
        rows = fetch_rows or []
        div = forgiving_float(fetch_div, 1)

    # 1. read every item, whatever its field names
    items: list[dict[str, Any]] = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        s = _first(r, _START_KEYS)
        e = _first(r, _END_KEYS)
        v = None
        for k in _VALUE_KEYS:
            if r.get(k) is not None:
                v = r.get(k)
                break
        else:
            v = r.get("price_tax_included")
        if isinstance(v, dict):
            v = v.get("amount")
        sd = s if isinstance(s, datetime) else as_datetime(jinja_str(s))
        ed = None if e is None else (e if isinstance(e, datetime) else as_datetime(jinja_str(e)))
        if sd is not None and v is not None and jinja_str(v) not in ("", "None"):
            f = forgiving_float(v, 0)
            f = f / 10000000 if abs(f) > 1000 else f / div
            items.append({"s": dt_util.as_local(sd), "e": (dt_util.as_local(ed) if ed is not None else None), "v": f})

    # 2. sort, drop duplicates, fill missing ends
    srt = sort_by(items, "s")
    lst: list[dict[str, Any]] = []
    last = None
    step: float = 3600
    for x in srt:
        if last is None or x["s"] != last:
            lst.append(x)
            last = x["s"]
    for i in range(1, len(lst)):
        d = (lst[i]["s"] - lst[i - 1]["s"]).total_seconds()
        if 0 < d < step:
            step = d

    # 3. cut into quarters (an hour price becomes four equal quarters)
    q: list[dict[str, Any]] = []
    for x in lst:
        en = x["e"] if x["e"] is not None else x["s"] + timedelta(seconds=step)
        k = int(jinja_round((en - x["s"]).total_seconds() / 900, 0))
        for j in range(max(k, 1)):
            q.append({"s": x["s"] + timedelta(minutes=15 * j), "v": x["v"]})

    # 4. "Per hour": every quarter gets the average of its hour
    today: list[dict[str, Any]] = []
    tomorrow: list[dict[str, Any]] = []
    now_val = None
    now = dt_util.now()
    d0 = now.date()
    for x in q:
        if resmode == "Per hour":
            hk = x["s"].replace(minute=0)
            grp = [y["v"] for y in q if y["s"] >= hk and y["s"] < hk + timedelta(hours=1)]
            val = sum(grp) / len(grp)
        else:
            val = x["v"]
        row = {"start": x["s"].isoformat(), "end": (x["s"] + timedelta(minutes=15)).isoformat(), "value": jinja_round(val, 5)}
        if x["s"].date() == d0:
            today.append(row)
        elif x["s"].date() == d0 + timedelta(days=1):
            tomorrow.append(row)
        if x["s"] <= now < x["s"] + timedelta(minutes=15):
            now_val = jinja_round(val, 5)

    # 5. currency
    cs = _states(get, "input_select.hesc_currency")
    cur = cs if cs in CURRENCIES else ""
    if cur == "":
        if src in LIST_SOURCES:
            hint = (jinja_str(_attr(get, ent, "currency") or "") + " " + jinja_str(_attr(get, ent, "unit_of_measurement") or "")).upper()
        else:
            hint = ""
        cur = ("SEK" if "SEK" in hint else "DKK" if "DKK" in hint else "NOK" if "NOK" in hint
               else "GBP" if ("GBP" in hint or "£" in hint) else "AUD" if ("AUD" in hint or "$" in hint) else "EUR")
    return {"now": now_val, "today": today, "tomorrow": tomorrow, "step_min": int(step / 60), "items_in": len(lst), "cur": cur}


def _today_at(hhmm: str) -> datetime:
    today = dt_util.start_of_local_day()
    if not hhmm:
        return today
    t = dt_util.parse_time(hhmm)
    return datetime.combine(today, t, today.tzinfo)  # type: ignore[arg-type]


def survives_template(p: dict[str, Any]) -> bool:
    """v2 passes `p` through `tojson` and back. JSON `null` (no price for now) or a
    non-finite number is not a Python literal, so `p` then stays a plain string and
    every `p.<field>` in the sensor renders empty (v2.0.0 behaviour, kept)."""
    if p["now"] is None:
        return False

    def finite(v: Any) -> bool:
        return not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))

    if not finite(p["now"]):
        return False
    return all(finite(r["value"]) for r in p["today"] + p["tomorrow"])


def sensor(get: Getter, p: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """State and attributes of v2's `sensor.hesc_prices` for adapter result `p`."""
    ok = survives_template(p)
    tz = jinja_str(dt_util.now().tzinfo)
    cur = p["cur"] if ok else "EUR"
    zone_last = tz.split("/")[-1]
    attrs: dict[str, Any] = {
        "raw_today": p["today"] if ok else "",
        "raw_tomorrow": p["tomorrow"] if ok else "",
        "tomorrow_valid": (len(p["tomorrow"]) > 0) if ok else False,
        "source_interval_min": p["step_min"] if ok else "",
        "source": _states(get, "input_select.hesc_price_source"),
        "resolution": _states(get, "input_select.hesc_price_resolution"),
        "currency": cur,
        "symbol": SYMBOL.get(cur, "€"),
        "minor": MINOR.get(cur, "ct"),
        "symbol_after": cur in ("SEK", "DKK", "NOK") or (cur == "EUR" and zone_last in _EURO_AFTER),
        "decimal": "," if ((tz.startswith("Europe/") or tz in ("Atlantic/Canary", "Atlantic/Madeira", "Atlantic/Azores"))
                           and zone_last not in _POINT_DECIMAL) else ".",
        "fx_vs_eur": FX_VS_EUR.get(cur, 1),
        "tz": tz,
    }
    if ok:
        state = jinja_str(p["now"])
    else:
        state = ""
    return state, attrs
