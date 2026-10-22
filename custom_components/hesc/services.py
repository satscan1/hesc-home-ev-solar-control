"""HESC actions for phones, Siri and the Apple Watch (since 3.0.0).

`hesc.set_charge_plan` sets the one-off charge plan (ready-by day and time, goal) and switches
it on; `hesc.charge_plan_off` switches it off. `hesc.skip_plan_day` lets the repeating plan skip one
day (a day off) without changing the plan; `hesc.undo_skip_plan_day` takes that back.
`hesc.charge_now` charges from the grid now up to a goal (charge_now.py); `hesc.charge_now_off`
stops that. They go through the plan's own entities, so the
result is exactly what setting those entities by hand gives (the deadline is worked out the same
way, the dashboard shows it at once). One call is easier for a Siri shortcut, a notification button
or a Watch action than four separate settings.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util

from . import charge_now, plan
from .const import DOMAIN
from .plan_settings import SETTINGS

SERVICE_SET_PLAN = "set_charge_plan"
SERVICE_PLAN_OFF = "charge_plan_off"
SERVICE_SKIP = "skip_plan_day"
SERVICE_UNDO_SKIP = "undo_skip_plan_day"
SERVICE_CHARGE_NOW = "charge_now"
SERVICE_CHARGE_NOW_OFF = "charge_now_off"

_OPTIONS = {s.key: s.options for s in SETTINGS if s.kind == "select"}
DAYS = _OPTIONS["plan_day"]  # Today, Tomorrow, Mon .. Sun
TIMES = _OPTIONS["plan_time"]  # every half hour
GOALS = tuple(int(g.rstrip("%")) for g in _OPTIONS["plan_goal"])

SET_PLAN_SCHEMA = vol.Schema({
    vol.Optional("day"): vol.In(DAYS),
    vol.Optional("time"): cv.string,
    vol.Optional("goal"): vol.All(vol.Coerce(int), vol.In(GOALS)),
})

SKIP_SCHEMA = vol.Schema({vol.Optional("date"): cv.date})
CHARGE_NOW_SCHEMA = vol.Schema({vol.Required("goal"): vol.All(vol.Coerce(int), vol.In(charge_now.GOALS))})


def _time_option(value: str) -> str:
    """'7:00', '07:00' or '07:00:00' -> '07:00'; only whole and half hours, like the plan's own setting."""
    parts = str(value).strip().split(":")
    try:
        h, m = int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
    except ValueError:
        h, m = -1, -1
    option = f"{h:02d}:{m:02d}"
    if option not in TIMES:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="bad_plan_time",
                                     translation_placeholders={"time": str(value)})
    return option


def _coordinator(hass: HomeAssistant) -> Any:
    entries = hass.config_entries.async_loaded_entries(DOMAIN)
    if not entries:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")
    return entries[0].runtime_data


def _entity(hass: HomeAssistant, domain: str, key: str) -> str:
    entries = hass.config_entries.async_loaded_entries(DOMAIN)
    if not entries:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")
    eid = er.async_get(hass).async_get_entity_id(domain, DOMAIN, f"{entries[0].entry_id}_{key}")
    if eid is None:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")
    return eid


async def _set_plan(call: ServiceCall) -> None:
    hass = call.hass
    data: dict[str, Any] = call.data
    steps: list[tuple[str, str, dict[str, Any]]] = []
    if "day" in data:
        steps.append(("select", "select_option", {"entity_id": _entity(hass, "select", "plan_day"), "option": data["day"]}))
    if "time" in data:
        steps.append(("select", "select_option", {"entity_id": _entity(hass, "select", "plan_time"),
                                                  "option": _time_option(data["time"])}))
    if "goal" in data:
        steps.append(("select", "select_option", {"entity_id": _entity(hass, "select", "plan_goal"),
                                                  "option": f"{data['goal']}%"}))
    steps.append(("switch", "turn_on", {"entity_id": _entity(hass, "switch", "plan_enabled")}))
    for domain, service, service_data in steps:
        await hass.services.async_call(domain, service, service_data, blocking=True)


async def _plan_off(call: ServiceCall) -> None:
    await call.hass.services.async_call("switch", "turn_off", {"entity_id": _entity(call.hass, "switch", "plan_enabled")},
                                        blocking=True)


async def _skip(call: ServiceCall) -> None:
    """Skip one day of the repeating plan: the given date, else the next day the plan would charge for."""
    hass = call.hass
    c = _coordinator(hass)
    day: date | None = call.data.get("date")
    if day is None:
        get = c._getter(c._view())
        try:
            on = (get("input_boolean.hesc_rep_enabled") or ("off",))[0] == "on"
            nxt = plan.next_repeating(get, dt_util.now()) if on else None
        except ValueError:  # no repeating time set
            nxt = None
        if nxt is None:
            raise ServiceValidationError(translation_domain=DOMAIN, translation_key="no_repeating_day")
        day = nxt.date()
    elif day < dt_util.now().date():
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="skip_in_past",
                                     translation_placeholders={"date": day.isoformat()})
    await hass.services.async_call("date", "set_value", {"entity_id": _entity(hass, "date", "rep_skip"),
                                                         "date": day.isoformat()}, blocking=True)
    await c.async_request_refresh()


async def _undo_skip(call: ServiceCall) -> None:
    c = _coordinator(call.hass)
    _entity(call.hass, "date", "rep_skip")
    ent = c.date_entities.get("rep_skip")
    if ent is not None and ent.hass is not None:
        ent.clear()
    await c.async_request_refresh()


async def _charge_now(call: ServiceCall) -> None:
    _coordinator(call.hass).start_charge_now(int(call.data["goal"]))


async def _charge_now_off(call: ServiceCall) -> None:
    c = _coordinator(call.hass)
    c.end_charge_now("switched off")
    await c.async_request_refresh()


def async_setup_services(hass: HomeAssistant) -> None:
    hass.services.async_register(DOMAIN, SERVICE_SET_PLAN, _set_plan, schema=SET_PLAN_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_PLAN_OFF, _plan_off, schema=vol.Schema({}))
    hass.services.async_register(DOMAIN, SERVICE_SKIP, _skip, schema=SKIP_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_UNDO_SKIP, _undo_skip, schema=vol.Schema({}))
    hass.services.async_register(DOMAIN, SERVICE_CHARGE_NOW, _charge_now, schema=CHARGE_NOW_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_CHARGE_NOW_OFF, _charge_now_off, schema=vol.Schema({}))
