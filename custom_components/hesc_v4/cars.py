"""Each car its own round (HESC v4 step 2, part B).

The decision logic of v3 keeps everything of "the car" on the coordinator itself (its plan flow,
battery-level log, release context, costs, status texts, ...). In v4 every car gets its own copy of
those, kept in a slot, and the coordinator switches to a car for that car's round
(`HescCoordinator.as_car`). EV1 is the car the coordinator holds at rest, so with one car nothing
changes: v4 with one car does exactly what v3 does (meetlat tests/baseline_v3).

Three kinds of state:

* WHOLE: belongs to one car completely and is swapped as a whole (contexts, flows, files).
* SPLIT: one dict with shared, car and charger keys (setting values and the setting entities). The
  coordinator holds the dict of EV1 (shared + EV1 + EV1's charger); another car sees the shared keys
  of that dict, its own keys and those of its own charger. Keys of a car or charger that has not set a
  value yet get the default, never EV1's value.
* Per-car keys of `published` (status texts) and `computed` (the car's sensors); the rest of those
  two dicts is shared.
"""

from __future__ import annotations

from typing import Any, Final

# swapped as a whole
WHOLE: Final = (
    "context",          # solar release context (v2 flow context "hesc")
    "own_flags",        # input_boolean.hesc_plan_owns_charging
    "plan_flow",        # charge plan control
    "soc_context", "soc_flow", "soc_blocked",  # battery level with fallbacks
    "kick_flow",        # kickstart
    "costs", "costs_context",  # charging costs, per car (decision 30-10 20:31)
    "morning_context",  # morning summary, per car (decision 31-10 06:51)
    "current_ctx",      # charging current control
    "charge_now", "charge_now_entity", "charge_now_wish",
    "last_result", "_round_inputs", "ev_max_days",
    "flags_path", "current_path", "history_path", "soc_path", "costs_path",
    "planning", "planning_path",  # v4 step 4: only this time and the calendar (planning.py)
    "learn", "learn_path", "plan_kw",  # v4 step 4D: the charging power learned (learn.py)
    "fill", "soc_entry", "soc_entity", "no_soc_over",  # v4 step 4E: a car without a battery-level sensor
    "plug_told",  # v4 step 6: the day the "plug in the car" reminder went out
    "widget_push",  # the phone widget refresh, to the car's own phones (phone.py)
)

# dicts with shared, car and charger keys
SPLIT: Final = ("plan", "tuning", "switches", "switch_entities", "date_entities", "datetime_entities")

# status texts of one car
PUBLISHED: Final = frozenset({
    "input_text.hesc_state", "input_text.hesc_reason", "input_text.hesc_last_action",
    "input_text.hesc_insight_1", "input_text.hesc_insight_2", "input_text.hesc_insight_3",
    "input_text.hesc_plan_status", "input_text.hesc_kick_status", "input_text.hesc_current_status",
    "input_text.hesc_costs_export_info",
})

# computed sensors of one car
COMPUTED: Final = frozenset({
    "sensor.hesc_charge_plan", "sensor.hesc_expected_charge_cost", "sensor.hesc_ev_soc",
    "sensor.hesc_notice", "sensor.hesc_charging_costs", "sensor.hesc_ev_battery_backup_sensor",
    "binary_sensor.hesc_diag_ev_connected",
    "sensor.hesc_coming_week",  # v4 step 4: the coming week of the car's planning (decision 13)
    "sensor.hesc_charge_power",  # v4 step 4D: the charging power the plan reckons with (learn.py)
})


def file_name(name: str, ev: str) -> str:
    """EV1 keeps v3's file names; another car gets its own: history.jsonl -> history_ev2.jsonl."""
    if ev == "ev1":
        return name
    stem, dot, ext = name.rpartition(".")
    return f"{stem}_{ev}.{ext}" if dot else f"{name}_{ev}"


def fresh(ev: str, paths: dict[str, Any], own_flags: dict[str, bool]) -> dict[str, Any]:
    """The WHOLE state of a car that has not had a round yet (as at a first start)."""
    return {
        "context": None, "own_flags": dict.fromkeys(own_flags, False), "plan_flow": {},
        "soc_context": {}, "soc_flow": {}, "soc_blocked": False, "kick_flow": {},
        "costs": None, "costs_context": {}, "morning_context": {}, "current_ctx": {},
        "charge_now": None, "charge_now_entity": None, "charge_now_wish": None, "last_result": None, "_round_inputs": None,
        "ev_max_days": {}, "planning": None, "learn": None, "plan_kw": None,
        "fill": None, "soc_entry": None, "soc_entity": None, "no_soc_over": {},
        "plug_told": None, "widget_push": None, **paths,
    }
