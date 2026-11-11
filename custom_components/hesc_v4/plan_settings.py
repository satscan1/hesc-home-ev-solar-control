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

# v4 (decision 15, 27-10): times in quarter steps (v3: every half hour; a superset, defaults unchanged)
_TIMES = tuple(f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 15, 30, 45))
# since 3.0.0 every 5 % (v2: every 10 %), so goals like 95 % are possible; v4 (decision 21, 28-10):
# from 15 % (below about 10 % a car no longer charges its 12 V battery; v3 starts at 50 %)
_GOALS = tuple(f"{g}%" for g in range(15, 101, 5))
DAYS: Final = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
# v4 step 4A (decision 12): a weekday of the rhythm can have its own time and goal; "Standard" = the
# rhythm's own time and goal
STANDARD: Final = "Standard"


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


# v4 step 4 (decision 31-10-2026 17:25): v3's "plan for one day" (plan_enabled, plan_day, plan_time,
# plan_goal, plan_deadline), "skip one day" (rep_skip) and holiday mode (vacation, vacation_until) are
# gone; only this time and the calendar (planning.py) replace them. Their v3 values are taken over.
GONE: Final = ("plan_enabled", "plan_day", "plan_time", "plan_goal", "plan_deadline", "vacation",
               "vacation_until", "rep_skip")

SETTINGS: Final[tuple[Setting, ...]] = (
    Setting("rep_enabled", "input_boolean.hesc_rep_enabled", "switch", False),
    Setting("rep_time", "input_select.hesc_rep_time", "select", "00:00", options=_TIMES),
    Setting("rep_goal", "input_select.hesc_rep_goal", "select", "50%", options=_GOALS),
    *(Setting(f"rep_{d}", f"input_boolean.hesc_rep_{d}", "switch", False) for d in DAYS),
    *(Setting(f"rep_{d}_time", f"input_select.hesc_rep_{d}_time", "select", STANDARD,
              options=(STANDARD, *_TIMES)) for d in DAYS),
    *(Setting(f"rep_{d}_goal", f"input_select.hesc_rep_{d}_goal", "select", STANDARD,
              options=(STANDARD, *_GOALS)) for d in DAYS),
    Setting("plan_opportunity", "input_boolean.hesc_plan_opportunity", "switch", False),
    Setting("plan_opportunity_price", "input_number.hesc_plan_opportunity_price", "number", 0.05,
            minimum=-5, maximum=10, step=0.01, unit="per kWh"),
    Setting("min_charge_enabled", "input_boolean.hesc_min_charge_enabled", "switch", False),
    Setting("min_charge_soc", "input_number.hesc_min_charge_soc", "number", 20, minimum=5, maximum=80, step=5, unit="%"),
    Setting("min_charge_hours", "input_number.hesc_min_charge_hours", "number", 3, minimum=0.5, maximum=12, step=0.5, unit="h"),
    Setting("plan_final_check_min", "input_number.hesc_plan_final_check_min", "number", 60, minimum=0, maximum=180, step=15, unit="min"),
    Setting("ev_battery_kwh", "input_number.hesc_ev_battery_kwh", "number", 60, minimum=10, maximum=150, step=0.5, unit="kWh"),
    Setting("plan_charge_kw", "input_number.hesc_plan_charge_kw", "number", 11, minimum=1.4, maximum=22, step=0.5, unit="kW"),
    # v4 step 4D (decision 30-10 21:52, 31-10 17:25): learn the charging power; off = the number above
    # as set by hand (taken over from v3: off, the v3 value counts as set by hand)
    Setting("plan_charge_kw_learn", "input_boolean.hesc_plan_charge_kw_learn", "switch", True),
    # v4 step 4E, a car without a battery-level sensor (decision 31-10 01:10): kWh one charge needs, by
    # hand (Expert; 0 = learned from earlier charges, the first time half the battery) ...
    Setting("no_soc_kwh", "input_number.hesc_no_soc_kwh", "number", 0, minimum=0, maximum=150, step=1, unit="kWh"),
    # ... and the battery level now, entered on the phone (decision 31-10 18:55); 0 = not entered.
    # Counts for this plug-in only (cleared when the car is unplugged).
    Setting("soc_entered", "input_number.hesc_soc_entered", "number", 0, minimum=0, maximum=100, step=1, unit="%",
            extra={"control": True}),
    # v4 step 6 (decisions 27, 33; wish 14): per car a reminder when a charge plan is active and the car is
    # not plugged in at a time of your own (default on, 22:00 - SatScan can change the default)
    Setting("plug_reminder", "input_boolean.hesc_plug_reminder", "switch", True),
    Setting("plug_reminder_time", "input_select.hesc_plug_reminder_time", "select", "22:00", options=_TIMES),
    Setting("price_source", "input_select.hesc_price_source", "select", "Price list in sensor",
            options=("Price list in sensor", "EnergyZero / ANWB Energie", "EasyEnergy", "Tibber", "Nord Pool (official)",
                     "Grid Clock")),  # v4 step 5: Grid Clock (decision 30-10-2026 19:23)
    Setting("price_sensor", "input_text.hesc_price_sensor", "text", ""),
    # decision 11-11-2026: first the country, then only the price sources of that country; the country also sets
    # the currency. "Automatic" = the country of Home Assistant. The countries follow the currencies below.
    Setting("price_country", "input_select.hesc_price_country", "select", "Automatic",
            options=("Automatic", "Netherlands", "Belgium", "Germany", "Austria", "France", "Spain", "Finland",
                     "Sweden", "Norway", "Denmark", "United Kingdom", "Australia", "Other")),
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
    # v4, two cars on two chargers (fleet.py): how they share the grid (decision 7; default "automatic":
    # the cheapest way with both in time, decision 31-10-2026 07:49) and the most both may take together
    # from the grid (0 = one charger on its own, decision 30-10 22:40). Shown at EV2.
    Setting("fleet_grid_mode", "input_select.hesc_fleet_grid_mode", "select", "Automatic",
            options=("Automatic", "One after the other", "Together")),
    Setting("fleet_together_kw", "input_number.hesc_fleet_together_kw", "number", 0,
            minimum=0, maximum=44, step=0.5, unit="kW"),
    # v4 step 2 part D (decisions 31-10-2026 09:56-10:10), asked in the first start. Used for a
    # comfort guard only: the user stays responsible that the installation is not overloaded (09:59).
    # 01-11 (decision, opmaakchat 10:21 + rekenchat 10:50): the house connection as two settings, the
    # number of phases and the amps per phase; the amps from a list or typed in (e.g. 1x60 A)
    Setting("house_phases", "input_select.hesc_house_phases", "select", "Don't know", options=("Don't know", "1", "3")),
    Setting("house_amps", "input_number.hesc_house_amps", "number", 25, minimum=6, maximum=250, step=1, unit="A"),
    Setting("house_load_balancer", "input_select.hesc_house_load_balancer", "select", "Don't know",
            options=("Yes", "No", "Don't know")),
    # per charger: the most it may charge with, as the installer set it (16 A when not known)
    Setting("charger_max_a", "input_number.hesc_charger_max_a", "number", 16,
            minimum=6, maximum=32, step=1, unit="A"),
    # v4 step 3 (decision 31): two cars on one charger - "move the cable at the latest at ...", per
    # charger, in quarter steps (decision 15). Default 22:30: proposal 31-10 14:35.
    Setting("swap_time", "input_select.hesc_swap_time", "select", "22:30",
            options=tuple(f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 15, 30, 45))),
    # decision 30: which car is on the charger - automatic (the car's own "plugged in" sensor, else
    # the car whose battery level rises), choosing it yourself is the reserve (per charger)
    Setting("charger_car", "input_select.hesc_charger_car", "select", "Automatic",
            options=("Automatic", "EV1", "EV2")),
    # decision 32 + first start (opmaakchat 31-10 21:45 question 5, SatScan "Akkoord" 21:38): the cable swap
    # reminder can be switched off, per charger (default on)
    Setting("swap_reminder", "input_boolean.hesc_swap_reminder", "switch", True),
    # per car: HESC controls this car and its own charger (decision 08-11-2026 08:43). Off = HESC leaves the car and
    # its charger alone, like shadow mode for that car only: no pause/resume, no current, no mode
    Setting("car_controlled", "input_boolean.hesc_car_controlled", "switch", True),
    # per car: its colour on the cards (opmaakchat 02-11 nr 7; EV1 light blue, EV2 salmon, set in the first
    # start; the hex is in setup_wizard.COLOURS and the select's attribute "hex")
    Setting("colour", "input_select.hesc_colour", "select", "light_blue",
            options=("light_blue", "salmon", "pink", "copper")),
    # per car, optional: the car's own "plugged in" / "charging" sensor (from the car's integration)
    Setting("car_plug_sensor", "input_text.hesc_car_plug_sensor", "text", ""),
)
BY_KEY: Final = {s.key: s for s in SETTINGS}
