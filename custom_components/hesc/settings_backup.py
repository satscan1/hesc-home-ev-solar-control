"""Settings back-up / restore / back to standard values.

Port of v2.0.0's Node-RED function node "Settings back-up / restore / reset", working on a
states view of v3's own settings under v2's helper ids (so the file has v2's format).
Three v3 buttons that do the same for v3's own settings. The
choice of actions is proven identical to the original node (`tests/integration/test_settings_backup_parity.py`).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.util import dt as dt_util

from .inputs import js_parse_float
from .jscompat import iso, js_number_str

DENY = re.compile(r"(\.hesc_state$|_reason$|_status$|insight|\.hesc_last_|owns_|report_ready|defaults_|\.hesc_show_|\.hesc_edit_|backup)")
_ID = re.compile(r"^input_(number|text|select|boolean|datetime)\.hesc_")
DEFAULTS: dict[str, float] = {
    "input_number.hesc_p_start": 2000, "input_number.hesc_p_hold": 1500, "input_number.hesc_irr_start": 220,
    "input_number.hesc_irr_hold": 160, "input_number.hesc_t_stable": 5, "input_number.hesc_t_start": 10,
    "input_number.hesc_t_dip": 5, "input_number.hesc_t_stop": 5, "input_number.hesc_t_max": 240,
    "input_number.hesc_cooldown": 30, "input_number.hesc_max_attempts": 3, "input_number.hesc_ev_active_w": 400,
    "input_number.hesc_advice_window_days": 30, "input_number.hesc_advice_min_runs": 8,
    "input_number.hesc_plan_final_check_min": 60,
}
INFO = "input_text.hesc_settings_backup_info"


def _js_number(v: Any) -> float:
    """JavaScript Number() for a state text (NaN when it is not a number)."""
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s == "":
        return 0.0
    x = js_parse_float(s)
    if x is None or not re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?|[+-]?Infinity", s):
        return float("nan")
    return x


def _s(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return js_number_str(v)
    if v is None:
        return "null"
    return str(v)


def _stamps(now: int, tz: str) -> tuple[str, str]:
    d = datetime.fromtimestamp(now / 1000, dt_util.get_time_zone(tz) or ZoneInfo(tz))
    return d.strftime("%Y%m%d-%H%M"), d.strftime("%d-%m %H:%M")


def _info(text: str) -> dict[str, Any]:
    return {"payload": {"action": "input_text.set_value", "target": {"entity_id": INFO}, "data": {"value": text[:250]}}}


def collect(S: dict[str, Any]) -> dict[str, Any]:
    items: dict[str, Any] = {}
    for i in S:
        if not _ID.match(i) or DENY.search(i):
            continue
        v = S[i].get("state")
        if v is None or v in ("unknown", "unavailable"):
            continue
        items[i] = v
    return items


def set_action(S: dict[str, Any], i: str, value: Any) -> dict[str, Any] | None:
    dom = i.split(".")[0]
    cur = S.get(i)
    if not cur or _s(cur.get("state")) == _s(value):
        return None
    if dom == "input_number" and _js_number(cur.get("state")) == _js_number(value):
        return None
    if dom == "input_number":
        return {"payload": {"action": "input_number.set_value", "target": {"entity_id": i}, "data": {"value": _js_number(value)}}}
    if dom == "input_text":
        return {"payload": {"action": "input_text.set_value", "target": {"entity_id": i}, "data": {"value": _s(value)}}}
    if dom == "input_boolean":
        return {"payload": {"action": "input_boolean.turn_on" if value == "on" else "input_boolean.turn_off", "target": {"entity_id": i}, "data": {}}}
    if dom == "input_select":
        opts = (cur.get("attributes") or {}).get("options") or []
        return {"payload": {"action": "input_select.select_option", "target": {"entity_id": i}, "data": {"option": value}}} if value in opts else None
    if dom == "input_datetime":
        return {"payload": {"action": "input_datetime.set_datetime", "target": {"entity_id": i}, "data": {"datetime": _s(value)}}}
    return None


def backup(S: dict[str, Any], reason: str, now: int, tz: str) -> tuple[list[tuple[str, str]], int]:
    """Files (name, text) of a back-up: the latest and a dated copy."""
    stamp, _ = _stamps(now, tz)
    items = collect(S)
    body = json.dumps({"version": 1, "created": iso(now), "reason": reason, "count": len(items), "items": items},
                      indent=1, ensure_ascii=False)
    return [("settings_backup.json", body), ("settings_backup_" + stamp + ".json", body)], len(items)


def press_backup(S: dict[str, Any], now: int, tz: str) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    _, nice = _stamps(now, tz)
    files, count = backup(S, "manual", now, tz)
    return files, [_info("Back-up " + nice + " · " + _s(count) + " settings")]


def restore(S: dict[str, Any], text: str | None, now: int, tz: str) -> list[dict[str, Any]]:
    """Restore from the file text; None = no back-up file yet."""
    _, nice = _stamps(now, tz)
    if text is None:
        return [_info("Restore not possible: no back-up yet (" + nice + ")")]
    try:
        b = json.loads(text)
    except ValueError:
        b = None
    items = b.get("items") if isinstance(b, dict) else None
    if items is None or items is False or items == "" or (isinstance(items, (int, float)) and not items):
        return [_info("Restore failed: back-up file unreadable (" + nice + ")")]
    keys = list(items.items()) if isinstance(items, dict) else ([(str(k), v) for k, v in enumerate(items)] if isinstance(items, list) else [])
    acts = [a for a in (set_action(S, i, v) for i, v in keys) if a]
    created = b.get("created") or ""
    created = _s(created) if created else ""
    acts.append(_info("Restored " + nice + " from back-up of " + created[:16].replace("T", " ", 1) + " UTC · "
                      + _s(len(acts)) + " settings changed"))
    return acts


def reset(S: dict[str, Any], now: int, tz: str) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    """Back-up first, then the tuning values back to the HESC standard values."""
    _, nice = _stamps(now, tz)
    files, _count = backup(S, "before reset to standard values", now, tz)
    acts = [a for a in (set_action(S, i, v) for i, v in DEFAULTS.items()) if a]
    acts.append(_info("Standard values " + nice + " · " + _s(len(acts)) + " changed · back-up made first"))
    return files, acts
