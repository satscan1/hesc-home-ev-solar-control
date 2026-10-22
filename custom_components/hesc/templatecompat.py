"""Small helpers that behave like the Jinja filters and functions v2's templates use.

Each one copies Home Assistant's own implementation (HA 2026.10, `helpers/template/
extensions/`), so ported template code gives the same answers as the template did.
"""
from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from homeassistant.util import dt as dt_util


def jinja_str(v: Any) -> str:
    """Jinja `| string` and `{{ v }}` output."""
    return str(v)


def forgiving_float(value: Any, default: Any) -> Any:
    """HA `| float(default)`."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def jinja_round(value: Any, precision: int = 0, method: str = "common") -> Any:
    """HA `| round(precision, method)` (forgiving_round)."""
    import math

    multiplier = float(10**precision)
    if method == "ceil":
        value = math.ceil(float(value) * multiplier) / multiplier
    elif method == "floor":
        value = math.floor(float(value) * multiplier) / multiplier
    elif method == "half":
        value = round(float(value) * 2) / 2
    else:
        value = round(float(value), precision)
    return int(value) if precision == 0 else value


def as_datetime(value: Any) -> datetime | None:
    """HA `as_datetime(value)` without default (None for an unparsable string)."""
    if type(value) is datetime:
        return value
    if type(value) is date:
        return datetime.combine(value, time(0, 0, 0))
    try:
        return dt_util.utc_from_timestamp(float(value))
    except (ValueError, TypeError):
        try:
            return dt_util.parse_datetime(value, raise_on_error=True)
        except (ValueError, TypeError):
            if isinstance(value, str):
                return None
            raise


def as_timestamp(value: Any) -> float | None:
    """HA `as_timestamp(value)` for datetimes and ISO strings (None when unparsable)."""
    if isinstance(value, datetime):
        return value.timestamp()
    try:
        return dt_util.as_timestamp(value)
    except (ValueError, TypeError):
        return None


def sort_by(items: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    """Jinja `| sort(attribute=key)`: stable, strings compared case-insensitively."""
    def k(x: dict[str, Any]) -> Any:
        v = x.get(key)
        return v.lower() if isinstance(v, str) else v

    return sorted(items, key=k)
