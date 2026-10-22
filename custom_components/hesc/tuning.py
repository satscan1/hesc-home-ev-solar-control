"""Tuning settings (v2's input_number / input_boolean helpers), as entities of the integration.

Defaults are what v2.0.0 sets on a first install (hesc_apply_defaults_on_first_install);
ranges and steps are those of the v2 helpers. Each maps to the v2 helper it replaces, so
the ported v2 logic reads them under the same name.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class NumberSpec:
    key: str
    helper: str  # v2 helper this replaces
    default: float
    minimum: float
    maximum: float
    step: float
    unit: str | None


NUMBERS: Final[tuple[NumberSpec, ...]] = (
    NumberSpec("p_start", "input_number.hesc_p_start", 2000, 500, 10000, 50, "W"),
    NumberSpec("p_hold", "input_number.hesc_p_hold", 1500, 500, 10000, 50, "W"),
    NumberSpec("irr_start", "input_number.hesc_irr_start", 220, 0, 1200, 10, "W/m²"),
    NumberSpec("irr_hold", "input_number.hesc_irr_hold", 160, 0, 1200, 10, "W/m²"),
    NumberSpec("t_stable", "input_number.hesc_t_stable", 5, 1, 30, 1, "min"),
    NumberSpec("t_start", "input_number.hesc_t_start", 10, 2, 30, 1, "min"),
    NumberSpec("t_dip", "input_number.hesc_t_dip", 5, 1, 30, 1, "min"),
    NumberSpec("t_stop", "input_number.hesc_t_stop", 5, 1, 30, 1, "min"),
    NumberSpec("t_max", "input_number.hesc_t_max", 240, 30, 600, 10, "min"),
    NumberSpec("cooldown", "input_number.hesc_cooldown", 30, 0, 180, 5, "min"),
    NumberSpec("max_attempts", "input_number.hesc_max_attempts", 3, 1, 10, 1, None),
    NumberSpec("ev_active_w", "input_number.hesc_ev_active_w", 400, 100, 3000, 50, "W"),
    NumberSpec("advice_window_days", "input_number.hesc_advice_window_days", 30, 7, 90, 1, "days"),
    NumberSpec("advice_min_runs", "input_number.hesc_advice_min_runs", 8, 3, 50, 1, None),
    NumberSpec("ev_full_soc", "input_number.hesc_ev_full_soc", 80, 50, 100, 1, "%"),
)


@dataclass(frozen=True)
class SwitchSpec:
    key: str
    helper: str
    default: bool


# Shadow mode is a switch too (switch.py) but has its own rules: on by default, project rule.
SWITCHES: Final[tuple[SwitchSpec, ...]] = (
    SwitchSpec("enabled", "input_boolean.hesc_enabled", True),
)
