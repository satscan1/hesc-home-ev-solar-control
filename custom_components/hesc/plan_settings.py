"""Charge plan, kickstart, cost and morning-summary settings (v2's helpers) as entities of the integration.

Options, ranges and steps are those of the v2 helpers; defaults are what a v2 first install
ends up with (the helper's own default, or the value v2's first-install automations set).

Design choice: while shadow mode is on, v3 follows v2's own plan helpers (one place
to set them, a fair comparison). These own settings start to count when shadow mode goes off;
at the switch-over they are first filled once with what v2 has at that moment.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

_TIMES = tuple(f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30))
# since 3.0.0 every 5 % (v2: every 10 %), so goals like 95 % are possible
_GOALS = tuple(f"{g}%" for g in range(50, 101, 5))
DAYS: Final = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


@dataclass(frozen=True)
class Setting:
    key: str
    helper: str  # the v2 helper it replaces
    kind: str  # select | switch | number | text | datetime | date
    default: object = None
    options: tuple[str, ...] = ()
    minimum: float = 0
    maximum: float = 0
    step: float = 1
    unit: str | None = None
    max_len: int = 255
    extra: dict = field(default_factory=dict)


SETTINGS: Final[tuple[Setting, ...]] = (
    Setting("plan_enabled", "input_boolean.hesc_plan_enabled", "switch", False),
    Setting("plan_day", "input_select.hesc_plan_day", "select", "Today",
            options=("Today", "Tomorrow", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")),
    Setting("plan_time", "input_select.hesc_plan_time", "select", "00:00", options=_TIMES),
    Setting("plan_goal", "input_select.hesc_plan_goal", "select", "50%", options=_GOALS),
    Setting("plan_deadline", "input_datetime.hesc_plan_deadline", "datetime", None),
    Setting("rep_enabled", "input_boolean.hesc_rep_enabled", "switch", False),
    Setting("rep_time", "input_select.hesc_rep_time", "select", "00:00", options=_TIMES),
    Setting("rep_goal", "input_select.hesc_rep_goal", "select", "50%", options=_GOALS),
    *(Setting(f"rep_{d}", f"input_boolean.hesc_rep_{d}", "switch", False) for d in DAYS),
    Setting("vacation", "input_boolean.hesc_vacation", "switch", False),
    Setting("vacation_until", "input_datetime.hesc_vacation_until", "date", None),
    # since 3.0.0, not in v2: one day on which the repeating plan does nothing (plan.SKIP_HELPER)
    Setting("rep_skip", "input_datetime.hesc_rep_skip", "date", None),
    Setting("plan_opportunity", "input_boolean.hesc_plan_opportunity", "switch", False),
    Setting("plan_opportunity_price", "input_number.hesc_plan_opportunity_price", "number", 0.05,
            minimum=-5, maximum=10, step=0.01, unit="per kWh"),
    Setting("min_charge_enabled", "input_boolean.hesc_min_charge_enabled", "switch", False),
    Setting("min_charge_soc", "input_number.hesc_min_charge_soc", "number", 20, minimum=5, maximum=80, step=5, unit="%"),
    Setting("min_charge_hours", "input_number.hesc_min_charge_hours", "number", 3, minimum=0.5, maximum=12, step=0.5, unit="h"),
    Setting("plan_final_check_min", "input_number.hesc_plan_final_check_min", "number", 60, minimum=0, maximum=180, step=15, unit="min"),
    Setting("ev_battery_kwh", "input_number.hesc_ev_battery_kwh", "number", 60, minimum=10, maximum=150, step=0.5, unit="kWh"),
    Setting("plan_charge_kw", "input_number.hesc_plan_charge_kw", "number", 11, minimum=1.4, maximum=22, step=0.5, unit="kW"),
    Setting("price_source", "input_select.hesc_price_source", "select", "Price list in sensor",
            options=("Price list in sensor", "EnergyZero / ANWB Energie", "EasyEnergy", "Tibber", "Nord Pool (official)")),
    Setting("price_sensor", "input_text.hesc_price_sensor", "text", ""),
    Setting("currency", "input_select.hesc_currency", "select", "Automatic",
            options=("Automatic", "EUR", "SEK", "DKK", "NOK", "GBP", "AUD")),
    Setting("price_resolution", "input_select.hesc_price_resolution", "select", "Automatic",
            options=("Automatic", "Per quarter", "Per hour")),
    Setting("charger_grid_mode_value", "input_text.hesc_charger_grid_mode_value", "text", "", max_len=100),
    Setting("notify_services", "input_text.hesc_notify_services", "text", ""),
    # The same rule for kickstart, costs and the morning summary.
    # No first-install automation sets these in v2, so the defaults are the helpers' own (minimum / off /
    # first option / empty).
    Setting("kick_enabled", "input_boolean.hesc_kick_enabled", "switch", False),
    Setting("home_battery_soc_sensors", "input_text.hesc_home_battery_soc_sensors", "text", ""),
    Setting("home_battery_power_sensors", "input_text.hesc_home_battery_power_sensors", "text", ""),
    Setting("home_battery_kwh", "input_number.hesc_home_battery_kwh", "number", 0, minimum=0, maximum=100, step=0.01, unit="kWh"),
    Setting("kick_max_per_day", "input_number.hesc_kick_max_per_day", "number", 1, minimum=1, maximum=10, step=1),
    Setting("kick_min_ev_kwh", "input_number.hesc_kick_min_ev_kwh", "number", 0.5, minimum=0.5, maximum=20, step=0.5, unit="kWh"),
    Setting("costs_all_in", "input_boolean.hesc_costs_all_in", "switch", False),
    Setting("costs_markup", "input_number.hesc_costs_markup", "number", 0, minimum=0, maximum=10, step=0.0001, unit="per kWh"),
    Setting("costs_vat", "input_number.hesc_costs_vat", "number", 0, minimum=0, maximum=30, step=0.5, unit="%"),
    Setting("feed_in_price", "input_number.hesc_feed_in_price", "number", 0, minimum=0, maximum=10, step=0.005, unit="per kWh"),
    Setting("morning_summary", "input_boolean.hesc_morning_summary", "switch", False),
    Setting("morning_summary_time", "input_select.hesc_morning_summary_time", "select", "06:00",
            options=("06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00")),
    # v2's dashboard helpers (show/hide sections, costs page and period). Off / first option by default.
    *(Setting(f"show_{k}", f"input_boolean.hesc_show_{k}", "switch", False)
      for k in ("advice", "charger_fields", "costs_settings", "kick_settings", "min_charge_settings", "optional",
                "plan_settings", "thresholds", "timing", "weather_settings")),
    Setting("edit_sources", "input_boolean.hesc_edit_sources", "switch", False),
    Setting("costs_enabled", "input_boolean.hesc_costs_enabled", "switch", False),
    # Advice applied automatically / seasonal start threshold (helpers' default: off)
    Setting("advice_auto", "input_boolean.hesc_advice_auto", "switch", False),
    Setting("seasonal_threshold", "input_boolean.hesc_seasonal_threshold", "switch", False),
    Setting("costs_period", "input_select.hesc_costs_period", "select", "Days",
            options=("Days", "Weeks", "Months", "Quarters", "Year")),
)
BY_KEY: Final = {s.key: s for s in SETTINGS}
