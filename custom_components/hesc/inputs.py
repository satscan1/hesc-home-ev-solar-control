"""Read HESC inputs from Home Assistant states, exactly as v2.0.0 does.

Ported from the "Evaluate HESC" function node (reference/v2.0.0/hesc_flow.json):
the helpers st/attr/num/txt/on/low/list/pw, the C (configuration) and L (live values)
blocks and the `missing` list. Only reading; nothing here changes anything in HA.

Known differences with v2, on purpose (see docs/dev/integration.md):
- v2 reads its configuration from input_text/input_number helpers; v3 from the config entry.
- v2 prefers its own template sensor `sensor.hesc_ev_soc` (battery level with fallbacks)
  when it holds a number; v3 has no such template yet and reads the chosen SoC sensor.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from homeassistant.core import State

from .const import (
    BAD_STATES,
    CONF_CHARGER_ECO_VALUES,
    CONF_CHARGER_MODE,
    CONF_CHARGER_SOLAR_SWITCH,
    CONF_EV_CONNECTED,
    CONF_EV_DISCONNECTED_VALUES,
    CONF_EV_GREEN_ENERGY,
    CONF_EV_POWER,
    CONF_EV_SOC,
    CONF_FORECAST_30M,
    CONF_FORECAST_ATTRIBUTE,
    CONF_FORECAST_NOW,
    CONF_GRID_EXPORT_POSITIVE,
    CONF_GRID_POWER,
    CONF_HPVC_ENABLED,
    CONF_HPVC_LIMITED,
    CONF_IRRADIANCE,
    CONF_PV_POWER,
    CONF_STANDALONE,
    CONF_USE_HPVC_SOURCES,
    CONF_USE_IRRADIANCE,
    DEFAULT_DISCONNECTED_VALUES,
    DEFAULT_ECO_VALUES,
    DEFAULT_HPVC_ENABLED,
    DEFAULT_HPVC_LIMITED,
    HPVC_GRID_HELPER,
    HPVC_PV_HELPER,
)

StateGetter = Callable[[str], State | None]

_BINARY_DOMAINS = re.compile(r"^(binary_sensor|switch|input_boolean)\.")
# JavaScript parseFloat: leading whitespace, then the longest numeric prefix.
_JS_FLOAT = re.compile(r"^\s*([+-]?(?:Infinity|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?))", re.ASCII)


def js_parse_float(value: Any) -> float | None:
    """JavaScript parseFloat(), returning None where JS returns NaN."""
    if value is None:
        return None
    if isinstance(value, bool):
        return None  # parseFloat(true) is NaN
    if isinstance(value, (int, float)):
        return None if isinstance(value, float) and math.isnan(value) else float(value)
    m = _JS_FLOAT.match(_js_string(value))
    if not m:
        return None
    return float(m.group(1).replace("Infinity", "inf"))


def low(value: Any) -> str:
    """v2 low(): trimmed, lower-case text; None becomes ''."""
    return "" if value is None else _js_string(value).strip().lower()


def as_list(value: Any) -> list[str]:
    """v2 list(): comma separated, trimmed, lower-case, empty parts dropped."""
    return [x for x in (low(p) for p in str(value or "").split(",")) if x]


def _js_string(value: Any) -> str:
    """JavaScript String(): enough of it for state and attribute values."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer() and abs(value) < 1e21:
        return str(int(value))
    if isinstance(value, (list, tuple)):
        return ",".join("" if v is None else _js_string(v) for v in value)
    if isinstance(value, dict):
        return "[object Object]"
    return str(value)


@dataclass
class Inputs:
    """The live values v2 calls L, plus what v2 needs to judge them."""

    fc_now: float | None = None
    fc_30m: float | None = None
    fc_median: float | None = None
    irradiance: float | None = None
    pv_w: float | None = None
    grid_w: float | None = None
    ev_connected: bool = False
    ev_power_w: float | None = None
    ev_green: float | None = None
    ev_soc: float | None = None
    charger_mode: str | None = None
    solar_switch_on: bool = True
    hpvc_on: bool = False
    hpvc_limited: bool = False
    in_solar_mode: bool = False
    irradiance_used: bool = False
    missing: list[str] = field(default_factory=list)
    forecast_source: str = "solcast"  # forecast.py kind; set by the coordinator

    @property
    def valid(self) -> bool:
        return not self.missing


class _Reader:
    """The v2 helper functions, on top of a state getter."""

    def __init__(self, get: StateGetter) -> None:
        self._get = get

    def st(self, entity_id: str | None) -> str | None:
        if not entity_id:
            return None
        s = self._get(entity_id)
        return s.state if s is not None else None

    def attr(self, entity_id: str | None, name: str) -> Any:
        if not entity_id:
            return None
        s = self._get(entity_id)
        return s.attributes.get(name) if s is not None else None

    def num(self, value: Any) -> float | None:
        return js_parse_float(value)

    def on(self, entity_id: str | None) -> bool:
        return self.st(entity_id) == "on"

    def pw(self, entity_id: str | None) -> float | None:
        """Power in W; a "kW" unit is multiplied by 1000 and "mW" (any case) divided by 1000, as in v2."""
        v = self.num(self.st(entity_id))
        if v is None:
            return None
        unit = low(self.attr(entity_id, "unit_of_measurement"))
        if unit == "kw":
            return v * 1000
        if unit == "mw":
            return v / 1000
        return v


def _txt(cfg: Mapping[str, Any], key: str) -> str:
    """v2 txt() on a configuration field: BAD values become '', the rest is trimmed."""
    v = cfg.get(key)
    if v is None:
        return ""
    v = str(v)
    return "" if v in BAD_STATES else v.strip()


def _helper(r: _Reader, entity_id: str) -> str:
    """The text in a helper, '' when empty, unknown or unavailable (v2 automation rule)."""
    v = (r.st(entity_id) or "").strip()
    return "" if v in ("", "unknown", "unavailable") else v


def read_inputs(get: StateGetter, cfg: Mapping[str, Any]) -> Inputs:
    """Read every input the v2 decision round reads, with the same parsing."""
    r = _Reader(get)

    fc_now_id = _txt(cfg, CONF_FORECAST_NOW)
    fc_30_id = _txt(cfg, CONF_FORECAST_30M)
    fc_attr = _txt(cfg, CONF_FORECAST_ATTRIBUTE)
    irr_id = _txt(cfg, CONF_IRRADIANCE)
    use_irr = bool(cfg.get(CONF_USE_IRRADIANCE, False))
    ev_conn_id = _txt(cfg, CONF_EV_CONNECTED)
    mode_id = _txt(cfg, CONF_CHARGER_MODE)
    eco_vals = as_list(_txt(cfg, CONF_CHARGER_ECO_VALUES) or DEFAULT_ECO_VALUES)
    solar_sw = _txt(cfg, CONF_CHARGER_SOLAR_SWITCH)
    off_vals = as_list(_txt(cfg, CONF_EV_DISCONNECTED_VALUES) or DEFAULT_DISCONNECTED_VALUES)
    hpvc_en = _txt(cfg, CONF_HPVC_ENABLED) or DEFAULT_HPVC_ENABLED
    hpvc_lim = _txt(cfg, CONF_HPVC_LIMITED) or DEFAULT_HPVC_LIMITED
    ev_green_id = _txt(cfg, CONF_EV_GREEN_ENERGY)
    ev_soc_id = _txt(cfg, CONF_EV_SOC)
    standalone = bool(cfg.get(CONF_STANDALONE, False))

    def fc_val(entity_id: str) -> float | None:
        if not entity_id:
            return None
        return r.num(r.attr(entity_id, fc_attr)) if fc_attr else r.num(r.st(entity_id))

    # v2 "use HPVC sources" (hesc_sync_sources_from_hpvc): HPVC's PV and grid sensors replace
    # the own choice whenever HPVC has one filled in. v3 reads them live instead of copying.
    pv_id = _txt(cfg, CONF_PV_POWER)
    grid_id = _txt(cfg, CONF_GRID_POWER)
    if cfg.get(CONF_USE_HPVC_SOURCES, False):
        pv_id = _helper(r, HPVC_PV_HELPER) or pv_id
        grid_id = _helper(r, HPVC_GRID_HELPER) or grid_id

    grid = r.pw(grid_id)
    if grid is not None and cfg.get(CONF_GRID_EXPORT_POSITIVE, False):
        grid = -grid  # v1.5: HESC works with import positive

    if _BINARY_DOMAINS.match(ev_conn_id):
        ev_connected = r.on(ev_conn_id)
    else:
        conn_state = r.st(ev_conn_id)
        ev_connected = (
            bool(ev_conn_id)
            and conn_state not in (*BAD_STATES, None)
            and low(conn_state) not in off_vals
        )

    mode_state = r.st(mode_id)
    inp = Inputs(
        fc_now=fc_val(fc_now_id),
        fc_30m=fc_val(fc_30_id),
        fc_median=r.num(r.st(fc_now_id)),
        irradiance=r.num(r.st(irr_id)) if (use_irr and irr_id) else None,
        pv_w=r.pw(pv_id),
        grid_w=grid,
        ev_connected=ev_connected,
        ev_power_w=r.pw(_txt(cfg, CONF_EV_POWER)),
        ev_green=r.num(r.st(ev_green_id)) if ev_green_id else None,
        ev_soc=r.num(r.st(ev_soc_id)) if ev_soc_id else None,
        charger_mode=mode_state,
        solar_switch_on=(not solar_sw) or r.on(solar_sw),
        hpvc_on=r.on(hpvc_en),
        hpvc_limited=r.on(hpvc_lim),
    )

    missing = inp.missing
    if inp.fc_now is None:
        missing.append("forecast now")
    if inp.fc_30m is None:
        missing.append("forecast +30m")
    if inp.pv_w is None:
        missing.append("PV power")
    if inp.ev_power_w is None:
        missing.append("EV power")
    if not ev_conn_id or r.st(ev_conn_id) in (*BAD_STATES, None):
        missing.append("EV connected")
    if not mode_id or mode_state in (*BAD_STATES, None):
        missing.append("charger mode")
    if not standalone and r.st(hpvc_en) in (*BAD_STATES, None):
        missing.append("HPVC enabled")

    inp.irradiance_used = use_irr and bool(irr_id) and inp.irradiance is not None
    inp.in_solar_mode = low(mode_state) in eco_vals and inp.solar_switch_on
    return inp
