"""HESC actions for phones, Siri, the Apple Watch (since 3.0.0) and the v4 dashboard.

v4 step 4 (planning.py, decision 31-10-2026 17:25): the actions change the car's planning, which
HESC keeps itself. Every action takes an optional `car` (ev1, ev2; default ev1).

* `set_charge_plan` (day, time, goal) and `only_this_time` (date, skip, time, goal): only this time, for
  one day; `charge_plan_off` / `only_this_time_clear` take it back.
* `skip_plan_day` (date, default: the next day the car would charge for) / `undo_skip_plan_day`.
* `calendar_day` (date, off / extra / rhythm), `vacation` (start, end) and `vacation_stop`.
* `battery_level` (level): the battery level now, entered by hand, for a car without a sensor.
* `export` (form: full / anonymous / bug) and `restore_backup`: the report and back-up (export.py).
* `charge_now` charges from the grid now up to a goal (charge_now.py); `charge_now_off` stops that.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.util import dt as dt_util

from . import charge_now, model, plan, planning
from .const import DOMAIN
from .plan_settings import SETTINGS

SERVICE_SET_PLAN = "set_charge_plan"
SERVICE_PLAN_OFF = "charge_plan_off"
SERVICE_SKIP = "skip_plan_day"
SERVICE_UNDO_SKIP = "undo_skip_plan_day"
SERVICE_CHARGE_NOW = "charge_now"
SERVICE_CHARGE_NOW_OFF = "charge_now_off"
SERVICE_ONCE = "only_this_time"
SERVICE_ONCE_CLEAR = "only_this_time_clear"
SERVICE_DAY = "calendar_day"
SERVICE_VACATION = "vacation"
SERVICE_VACATION_STOP = "vacation_stop"
SERVICE_BATTERY_LEVEL = "battery_level"
SERVICE_EXPORT = "export"
SERVICE_RESTORE = "restore_backup"

_OPTIONS = {s.key: s.options for s in SETTINGS if s.kind == "select"}
DAYS = ("Today", "Tomorrow", *planning.WDS)
TIMES = _OPTIONS["rep_time"]  # every quarter (v4, decision 15)
GOALS = tuple(int(g.rstrip("%")) for g in _OPTIONS["rep_goal"])  # from 15 % (v4, decision 21)
CAR = vol.Optional("car", default=model.EV1)
CARS = vol.In((model.EV1, model.EV2))

SET_PLAN_SCHEMA = vol.Schema({
    CAR: CARS,
    vol.Optional("day"): vol.In(DAYS),
    vol.Optional("time"): cv.string,
    vol.Optional("goal"): vol.All(vol.Coerce(int), vol.In(GOALS)),
})
ONCE_SCHEMA = vol.Schema({
    CAR: CARS,
    vol.Optional("date"): cv.date,
    vol.Optional("skip", default=False): cv.boolean,
    vol.Optional("time"): cv.string,
    vol.Optional("goal"): vol.All(vol.Coerce(int), vol.In(GOALS)),
})
CAR_SCHEMA = vol.Schema({CAR: CARS})
SKIP_SCHEMA = vol.Schema({CAR: CARS, vol.Optional("date"): cv.date})
DAY_SCHEMA = vol.Schema({CAR: CARS, vol.Required("date"): cv.date, vol.Required("what"): vol.In(("off", "extra", "rhythm")),
                         # decision 10-11-2026: an extra day with its own time and/or goal
                         vol.Optional("time"): cv.string, vol.Optional("goal"): vol.All(vol.Coerce(int), vol.Range(min=10, max=100))})
VACATION_SCHEMA = vol.Schema({CAR: CARS, vol.Required("start"): cv.date, vol.Optional("end"): cv.date})
LEVEL_SCHEMA = vol.Schema({CAR: CARS, vol.Required("level"): vol.All(vol.Coerce(float), vol.Range(min=1, max=100))})
EXPORT_SCHEMA = vol.Schema({vol.Required("form"): vol.In(("full", "anonymous", "bug"))})
CHARGE_NOW_SCHEMA = vol.Schema({CAR: CARS, vol.Required("goal"): vol.All(vol.Coerce(int), vol.In(charge_now.GOALS))})


def _time_option(value: str) -> str:
    """'7:00', '07:00' or '07:00:00' -> '07:00'; only whole quarters, like the plan's own setting."""
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


def _car(hass: HomeAssistant, call: ServiceCall) -> tuple[Any, str]:
    c = _coordinator(hass)
    ev = call.data.get("car", model.EV1)
    if ev not in c.ev_ids():
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="no_such_car",
                                     translation_placeholders={"car": str(ev).upper()})
    return c, ev


def _not_past(day: date) -> None:
    if day < dt_util.now().date():
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="skip_in_past",
                                     translation_placeholders={"date": day.isoformat()})


def _next_day(c: Any, ev: str) -> date:
    """The day of the car's next ready-by time (its planning, only-this-time included)."""
    with c.as_car(ev):
        p = c.planning or planning.empty()
        nxt = planning.next_moment(p, c._getter(c._view()), dt_util.now())
    if nxt is None:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="no_repeating_day")
    return dt_util.as_local(nxt[0]).date()


async def _apply(c: Any, ev: str, fn: Any, *args: Any, **kw: Any) -> None:
    c.change_planning(ev, fn, *args, **kw)
    await c.async_request_refresh()


async def _set_plan(call: ServiceCall) -> None:
    """v3's one-off plan (day, time, goal) as only this time on that day (v4 step 4B)."""
    c, ev = _car(call.hass, call)
    data: dict[str, Any] = call.data
    with c.as_car(ev):
        before = (c.planning or {}).get("once") or {}
    if before.get("skip"):
        before = {}
    # what is not given stays as it was (as v3's plan for one day)
    time = _time_option(data["time"]) if "time" in data else before.get("time")
    goal = data.get("goal", before.get("goal"))
    if "day" in data:
        day = plan.fixed_deadline(data["day"], time or "00:00").date()
    elif before.get("date") and "time" not in data:
        day = date.fromisoformat(before["date"])
    else:  # the next such time: today if still to come, else tomorrow
        day_name = "Today" if time and plan.fixed_deadline("Today", time) > dt_util.now() else "Tomorrow"
        day = plan.fixed_deadline(day_name, time or "00:00").date()
    await _apply(c, ev, planning.set_once, day, time=time, goal=goal)


async def _once(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    data: dict[str, Any] = call.data
    day = data.get("date") or _next_day(c, ev)
    _not_past(day)
    time = _time_option(data["time"]) if "time" in data else None
    await _apply(c, ev, planning.set_once, day, skip=bool(data.get("skip")), time=time, goal=data.get("goal"))


async def _once_clear(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    await _apply(c, ev, planning.clear_once)


async def _skip(call: ServiceCall) -> None:
    """Skip one day: the given date, else the next day the car would charge for (only this time: skip)."""
    c, ev = _car(call.hass, call)
    day: date | None = call.data.get("date")
    if day is None:
        day = _next_day(c, ev)
    _not_past(day)
    await _apply(c, ev, planning.set_once, day, skip=True)


async def _undo_skip(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    with c.as_car(ev):
        once = (c.planning or {}).get("once")
    if once and once.get("skip"):
        await _apply(c, ev, planning.clear_once)


async def _calendar_day(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    _not_past(call.data["date"])
    time = _time_option(call.data["time"]) if call.data.get("time") else None
    await _apply(c, ev, planning.set_day, call.data["date"], call.data["what"], time, call.data.get("goal"))


async def _vacation(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    start, end = call.data["start"], call.data.get("end")
    if end is not None and end < start:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="vacation_end_before_start")
    await _apply(c, ev, planning.set_vacation, start, end)


async def _vacation_stop(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    await _apply(c, ev, planning.clear_vacation)


async def _battery_level(call: ServiceCall) -> None:
    """v4 step 4E (decision 31-10 18:55): the battery level now, entered by hand (a car without a
    battery-level sensor); counts for this plug-in."""
    c, ev = _car(call.hass, call)
    with c.as_car(ev):
        ent = c.soc_entity
        if ent is None or ent.hass is None:
            raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")
        ent.set_from_logic(float(call.data["level"]))
    await c.async_request_refresh()


async def _export(call: ServiceCall) -> ServiceResponse:
    """v4 step 8: the report in one of three forms (full back-up, anonymous to share, short for a bug)."""
    return await _coordinator(call.hass).async_export(call.data["form"])


async def _restore(call: ServiceCall) -> ServiceResponse:
    """v4 step 8: put back the full back-up (settings, planning, learned charging power per car)."""
    return await _coordinator(call.hass).async_restore_backup()


async def _charge_now(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    with c.as_car(ev):  # v4: per car
        c.start_charge_now(int(call.data["goal"]))


async def _charge_now_off(call: ServiceCall) -> None:
    c, ev = _car(call.hass, call)
    with c.as_car(ev):
        c.end_charge_now("switched off")
    await c.async_request_refresh()


def async_setup_services(hass: HomeAssistant) -> None:
    hass.services.async_register(DOMAIN, SERVICE_SET_PLAN, _set_plan, schema=SET_PLAN_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_PLAN_OFF, _once_clear, schema=CAR_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_SKIP, _skip, schema=SKIP_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_UNDO_SKIP, _undo_skip, schema=CAR_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ONCE, _once, schema=ONCE_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_ONCE_CLEAR, _once_clear, schema=CAR_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_DAY, _calendar_day, schema=DAY_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_VACATION, _vacation, schema=VACATION_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_VACATION_STOP, _vacation_stop, schema=CAR_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_BATTERY_LEVEL, _battery_level, schema=LEVEL_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_EXPORT, _export, schema=EXPORT_SCHEMA,
                                 supports_response=SupportsResponse.OPTIONAL)
    hass.services.async_register(DOMAIN, SERVICE_RESTORE, _restore, schema=vol.Schema({}),
                                 supports_response=SupportsResponse.OPTIONAL)
    hass.services.async_register(DOMAIN, SERVICE_CHARGE_NOW, _charge_now, schema=CHARGE_NOW_SCHEMA)
    hass.services.async_register(DOMAIN, SERVICE_CHARGE_NOW_OFF, _charge_now_off, schema=CAR_SCHEMA)
