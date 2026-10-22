"""Small JavaScript-compatible helpers, so v3 produces exactly the texts and numbers v2 produced.

v2 is a Node-RED (JavaScript) flow. Where its output depends on JavaScript behaviour
(Math.round, toFixed, number-to-text, JSON.stringify, Date formatting), v3 uses these.
"""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any
from zoneinfo import ZoneInfo


class _Undefined:
    """JavaScript `undefined`: dropped by JSON.stringify inside objects."""

    _instance: _Undefined | None = None

    def __new__(cls) -> _Undefined:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "undefined"

    def __bool__(self) -> bool:
        return False


UNDEFINED: Any = _Undefined()


def js_round(x: float) -> Any:
    """Math.round: halves go up (towards +infinity); Infinity and NaN stay as they are."""
    if isinstance(x, float) and not math.isfinite(x):
        return x
    return math.floor(x + 0.5)


def js_number_str(x: float | int) -> str:
    """String(number) for finite numbers as v2 meets them."""
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if math.isnan(x):
        return "NaN"
    if math.isinf(x):
        return "Infinity" if x > 0 else "-Infinity"
    if x == int(x) and abs(x) < 1e21:
        return str(int(x))
    r = repr(x)
    if "e" in r:
        mant, exp = r.split("e")
        e = int(exp)
        if -7 < e < 21:
            return format(Decimal(r), "f")
        return f"{mant}e{'+' if e > 0 else '-'}{abs(e)}"
    return r


def js_to_fixed(x: float, digits: int) -> str:
    """Number.prototype.toFixed: exact value, halves away from zero for positive values."""
    q = Decimal(1).scaleb(-digits)
    if x == 0:
        x = 0  # (-0).toFixed(n) has no minus sign; (-0.001).toFixed(2) keeps it ("-0.00")
    return str(Decimal(x).quantize(q, rounding=ROUND_HALF_UP))


def _encode(v: Any) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, (int, float)):
        if isinstance(v, float) and not math.isfinite(v):
            return "null"
        return js_number_str(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        parts = [f"{json.dumps(str(k), ensure_ascii=False)}:{_encode(val)}" for k, val in v.items() if val is not UNDEFINED]
        return "{" + ",".join(parts) + "}"
    if isinstance(v, (list, tuple)):
        return "[" + ",".join("null" if x is UNDEFINED else _encode(x) for x in v) + "]"
    raise TypeError(f"cannot encode {type(v)}")


def js_json(v: Any) -> str:
    """JSON.stringify(v) without spacing."""
    return _encode(v)


def iso(ms: float) -> str:
    """new Date(ms).toISOString()."""
    dt = datetime.fromtimestamp(math.floor(ms) / 1000, UTC)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(math.floor(ms)) % 1000:03d}Z"


def local_date(ms: float, tz: str) -> str:
    """new Date(ms).toLocaleDateString('sv-SE', {timeZone}) → YYYY-MM-DD."""
    return datetime.fromtimestamp(ms / 1000, ZoneInfo(tz)).strftime("%Y-%m-%d")


def local_hhmm(ms: float, tz: str) -> str:
    """toLocaleTimeString('nl-NL', {timeZone, hour: '2-digit', minute: '2-digit'})."""
    return datetime.fromtimestamp(ms / 1000, ZoneInfo(tz)).strftime("%H:%M")
