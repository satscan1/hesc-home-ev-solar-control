"""The first start in HESC's own panel (decision 01-11-2026 12:44, "B").

The HA setup window only asks "Install HESC v4?" (and with v3 present: take over v3's settings). The
entry is then made in shadow mode with the first start not finished (`SETUP_DONE` false). The first start
itself runs in the panel "HESC v4" in the house style; this module gives the panel what it needs over the
websocket (names in `async_setup_websocket`):

* `hesc_v4/setup/find`: what HESC finds by itself (finders.py): charger integrations, the grid meter's
  phases, solar power, grid power, the solar forecast, price sources, battery-level sensors with the
  car's name and capacity, HPVC; plus the amps lists per phase count and whether the first start is done.
* `hesc_v4/setup/charger`: for one charger brand, what HESC finds of its entities and what is missing.
* `hesc_v4/setup/save`: the answers of the first start (or of "add a second car"); checked per field,
  then stored in the entry like the HA setup window did (the values that live in HESC's own entities as
  `first_values`, set at the next start) and the integration is reloaded.

The questions, order and texts are those of the postbus aanvulling 01-11 "besluiten eerste start" and
"eerste start in eigen paneel"; the panel itself is built by the opmaakchat.
"""
from __future__ import annotations

from typing import Any, Final

from homeassistant.core import HomeAssistant

from . import fleet_setup, model, sources
from .const import (
    CHARGER_NOT_CHOSEN,
    CHARGER_OTHER,
    CONF_CHARGER_CURRENT,
    CONF_CHARGER_ECO_VALUES,
    CONF_CHARGER_TYPE,
    CONF_EV_SOC,
    CONF_FORECAST_30M,
    CONF_FORECAST_ATTRIBUTE,
    CONF_FORECAST_NOW,
    CONF_GRID_EXPORT_SENSOR,
    CONF_GRID_POWER,
    CONF_IRRADIANCE,
    CONF_NO_SOLAR,
    CONF_PV_POWER,
    CONF_STANDALONE,
    CONF_USE_HPVC_SOURCES,
    CONF_USE_IRRADIANCE,
    DOMAIN,
    HPVC_GRID_HELPER,
    HPVC_PV_HELPER,
)

SETUP_DONE: Final = "setup_done"  # shared key; missing (entries made before 01-11) counts as done
FIRST_VALUES: Final = "first_values"
HOW: Final = ("one", "two_shared", "two_own")  # order: decision 01-11 12:49
# the amps lists depend on the phases (decision 01-11 12:55); another value can always be typed (6-250 A)
AMPS: Final = {"1": (25, 35, 40, 50, 63), "3": (16, 20, 25, 35, 40, 63)}
AMPS_MIN, AMPS_MAX = 6, 250
PHASES: Final = ("Don't know", "1", "3")
LOAD_BALANCER: Final = ("Yes", "No", "Don't know")
# the user confirms being responsible that the installation is not overloaded (decision 31-10 09:59,
# asked in the first start: opmaakchat 02-11 nr 3); stored as the time of the confirmation
RESPONSIBILITY: Final = "responsibility_confirmed"
# a colour per car for the cards (opmaakchat 02-11 nr 7); the panel shows the hex
COLOURS: Final = {"light_blue": "#3fc8f4", "salmon": "#ff8a65", "pink": "#f06292", "copper": "#b87333"}
COLOUR_DEFAULT: Final = {"ev1": "light_blue", "ev2": "salmon"}
FEATURES: Final = ("responsibility", "car_colour", "charger_count", "grid_combined", "grid_from_hpvc", "set_source",
                   "charger_device", "car_controlled", "remove_car", "remove_charger", "add_charger", "set_value",
                   "values_seen", "car_setup")


def setup_done(settings: Any) -> bool:
    return bool(model.flatten(settings or {}).get(SETUP_DONE, True))


# ---- what HESC finds ----------------------------------------------------------------------------------
def _state(hass: HomeAssistant, eid: str) -> dict[str, Any]:
    st = hass.states.get(eid)
    return {"entity_id": eid, "name": (st.attributes.get("friendly_name") if st else None) or eid,
            "state": st.state if st else None, "unit": st.attributes.get("unit_of_measurement") if st else None}


def find(hass: HomeAssistant) -> dict[str, Any]:
    """Everything the first start can fill in or offer, read-only (finders.py, config_flow helpers)."""
    from .config_flow import PREV_DOMAIN, _helper_text, car_device, ev_soc_candidates, first_install_values
    from .finders import car_capacity, chargers_found, grid_choices, meter_phases, price_sources, pv_candidates

    shared, _charger = _split(first_install_values(hass))
    from .sources import ranked

    # decision 10-11-2026 (more plug and play): the solar list best first, without sensors that are
    # unavailable now, and HESC's suggestion ready to confirm
    pv_rank = [c for c in ranked(hass, CONF_PV_POWER)
               if (st := hass.states.get(c["entity_id"])) and st.state not in ("unavailable", "unknown")]
    pv = [c["entity_id"] for c in pv_rank] or pv_candidates(hass)
    pv_best = next((c["entity_id"] for c in pv_rank if c["suggested"]), None)
    grid = grid_choices(hass)
    hpvc_pv = _helper_text(hass, HPVC_PV_HELPER) if shared.get(CONF_USE_HPVC_SOURCES) else ""
    hpvc_grid = _helper_text(hass, HPVC_GRID_HELPER) if shared.get(CONF_USE_HPVC_SOURCES) else ""
    fc = {k: shared.get(k) for k in (CONF_FORECAST_NOW, CONF_FORECAST_30M) if shared.get(k)}
    fc_found = bool(fc.get(CONF_FORECAST_NOW) and hass.states.get(str(fc[CONF_FORECAST_NOW])))
    prices = price_sources(hass)
    cars = []
    for eid in ev_soc_candidates(hass, []):
        cars.append({**_state(hass, eid), "car_name": car_device(hass, eid)[0], "capacity": car_capacity(hass, eid)})
    return {
        "v3": bool(hass.config_entries.async_entries(PREV_DOMAIN)),
        "how": list(HOW), "phases": meter_phases(hass), "amps": {k: list(v) for k, v in AMPS.items()},
        "chargers": chargers_found(hass),
        "pv": [_state(hass, e) for e in pv], "pv_suggested": pv_best, "pv_from_hpvc": hpvc_pv or None,
        "grid": [_grid_choice(hass, c) for c in grid], "grid_from_hpvc": hpvc_grid or None,
        "colours": dict(COLOURS),
        # what save understands, so the panel only sends it then (opmaakchat 02-11 11:35)
        "features": list(FEATURES),
        # 06-11: suggestions per source for the settings window (sources.py, `hesc_v4/setup/source`)
        "sources": sources.suggestions(hass),
        "forecast": fc if fc_found else {},
        "solar": bool(pv or hpvc_pv or fc_found), "dynamic": bool(prices),
        "prices": prices, "cars": cars,
        "hpvc": not shared.get(CONF_STANDALONE, False),
    }


def _grid_choice(hass: HomeAssistant, c: dict[str, Any]) -> dict[str, Any]:
    out = {**_state(hass, c["entity_id"]), "recommended": c["recommended"]}
    if c.get("export_entity_id"):
        exp = _state(hass, c["export_entity_id"])
        out.update(export_entity_id=exp["entity_id"], export_name=exp["name"], export_state=exp["state"],
                   export_unit=exp["unit"], combined=True)
    return out


def charger(hass: HomeAssistant, brand: str, other: dict[str, Any] | None = None, device: str | None = None,
            other_device: str | None = None) -> dict[str, Any]:
    """For one charger of this brand: the fields HESC fills in, the ones it misses (only those are asked,
    decision 01-11 10:28) and the candidates per missing field; the installer's maximum it can read.

    07-11 (decision 22:59, two chargers of the same brand): `device` = which charger (HA device) this is; only
    its entities are filled in or offered, never those of another charger nor any entity of `other` (the
    other charger's settings) or of `other_device`. Without `device` HESC takes the first of this brand
    that is not the other charger's (`devices` lists them all, `device_choice` true when there are more)."""
    from .config_flow import _PROFILE_KEY, first_install_values, installer_max

    _shared, template = _split(first_install_values(hass))
    devices = charger_devices(hass, brand)
    taken = {d for d in (other_device, _device_of_values(hass, other)) if d}
    if device is None:
        device = next((d["id"] for d in devices if d["id"] not in taken), None)
    vals, prof = _apply_brand(hass, template, brand, other, device, taken)
    missing = charger_missing(hass, vals, prof)
    cands = {}
    for key in missing:
        pk = _PROFILE_KEY.get(key)
        if pk and prof.known:
            cands[key] = list(getattr(prof, pk, []))
    return {"brand": brand, "values": vals, "missing": missing, "candidates": cands,
            "max_a": installer_max(hass, vals.get(CONF_CHARGER_CURRENT)),
            "device": device, "devices": devices, "device_choice": len(devices) > 1}


def charger_devices(hass: HomeAssistant, brand: str) -> list[dict[str, Any]]:
    """The chargers (HA devices) of this brand: [{"id", "name"}], in a fixed order."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    from .finders import CHARGER_PLATFORMS

    reg, devs = er.async_get(hass), dr.async_get(hass)
    ids = sorted({e.device_id for e in reg.entities.values()
                  if e.device_id and not e.disabled_by and CHARGER_PLATFORMS.get(e.platform) == brand})
    out = []
    for i in ids:
        d = devs.async_get(i)
        out.append({"id": i, "name": (d and (d.name_by_user or d.name)) or brand})
    return sorted(out, key=lambda d: (str(d["name"]).lower(), d["id"]))


def _all_charger_devices(hass: HomeAssistant) -> set[str]:
    from homeassistant.helpers import entity_registry as er

    from .finders import CHARGER_PLATFORMS

    return {e.device_id for e in er.async_get(hass).entities.values() if e.device_id and e.platform in CHARGER_PLATFORMS}


def _device_of(hass: HomeAssistant, entity_id: str) -> str | None:
    from homeassistant.helpers import entity_registry as er

    ent = er.async_get(hass).async_get(entity_id) if entity_id else None
    return ent.device_id if ent else None


def _entities_of(values: dict[str, Any] | None) -> set[str]:
    """The entities a charger's settings use (sensors, switches, selects, number)."""
    from .config_flow import _KEY_FIELD

    return {str(values.get(c)).strip() for c in _KEY_FIELD.values() if values and str(values.get(c) or "").strip()}


def _device_of_values(hass: HomeAssistant, values: dict[str, Any] | None) -> str | None:
    """The charger device of a charger's settings (the first of its entities on a charger device)."""
    chargers = _all_charger_devices(hass)
    return next((d for e in sorted(_entities_of(values)) if (d := _device_of(hass, e)) in chargers), None)


def _split(values: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    from .config_flow import split_defaults

    return split_defaults(values)


def _apply_brand(hass: HomeAssistant, template: dict[str, Any], brand: str, other: dict[str, Any] | None,
                 device: str | None = None, taken: set[str] | None = None) -> tuple[dict[str, Any], Any]:
    """The brand's values and the entities of this charger only: (values, the profile limited to it).

    An entity of another charger device, or one the other charger uses, is never filled in nor offered
    (decision 07-11 22:59: "laadpaal 1 en 2 nooit door elkaar")."""
    import dataclasses

    from .config_flow import _KEY_FIELD, apply_charger_type
    from .profile import charger_profile

    vals = apply_charger_type(hass, dict(template), CHARGER_NOT_CHOSEN, brand)
    prof = charger_profile(hass, brand, device) if device else charger_profile(hass, brand)
    used = _entities_of(other)
    others = _all_charger_devices(hass) - ({device} if device else set())
    if not device:
        others = {d for d in others if d in (taken or set())}

    def mine(eid: str) -> bool:
        return eid not in used and _device_of(hass, eid) not in others

    if prof.known:
        prof = dataclasses.replace(prof, **{k: [e for e in getattr(prof, k) if mine(e)] for k in _KEY_FIELD})
    for key, conf in _KEY_FIELD.items():
        cur = str(vals.get(conf) or "").strip()
        if cur and not mine(cur):
            vals.pop(conf)
        found = getattr(prof, key, []) if prof.known else []
        if not str(vals.get(conf) or "").strip() and len(found) == 1:
            vals[conf] = found[0]
    return vals, prof


def charger_missing(hass: HomeAssistant, vals: dict[str, Any], prof: Any = None) -> list[str]:
    """The charger fields to ask: required ones not found; with several candidates the optional ones too;
    "Other": every empty field and the first-install solar value "eco_mode" (a guess)."""
    from .config_flow import _PROFILE_KEY, CHARGER_FIELDS, CHARGER_REQUIRED
    from .profile import charger_profile

    if prof is None:
        prof = charger_profile(hass, str(vals.get(CONF_CHARGER_TYPE) or CHARGER_OTHER))
    out = []
    for key in CHARGER_FIELDS:
        if key == CONF_CHARGER_ECO_VALUES and not prof.known:
            out.append(key)
            continue
        if str(vals.get(key) or "").strip():
            continue
        if key in CHARGER_REQUIRED or not prof.known:
            out.append(key)
        elif key in _PROFILE_KEY and len(getattr(prof, _PROFILE_KEY[key], [])) > 1:
            out.append(key)
    return out


# ---- the answers --------------------------------------------------------------------------------------
def build(hass: HomeAssistant, answers: dict[str, Any], current: Any = None,
          colours: dict[str, str] | None = None) -> tuple[dict[str, Any], dict[str, str]]:
    """The answers of the first start -> (the entry's settings, errors per field "path": code).

    `current` given: "add a second car" (answers hold `add`: "own" | "same", one car and maybe one charger;
    the house questions are not asked again; `colours`: the colours of the cars already set up). Error
    codes: required, confirm_required, amps_invalid, capacity_invalid, colour_taken, installer_setting,
    unknown_charger."""
    from .config_flow import CHARGER_REQUIRED, first_install_values, installer_max
    from .finders import price_sources
    from . import safety

    errors: dict[str, str] = {}
    shared_d, template = _split(first_install_values(hass))
    first: dict[str, dict[str, Any]] = {}
    add = current is not None
    if add:
        nested = model.ensure_nested(current)
        shared = dict(nested["shared"])
        chargers = {k: dict(v) for k, v in nested["chargers"].items()}
        cars = {k: dict(v) for k, v in nested["evs"].items()}
        own = answers.get("add") in ("own", "charger")
        new_chargers = [model.CHARGER2] if own else []
        if answers.get("add") == "charger":
            # 08-11 (decision 08:50): EV2 shares charger 1 and gets its own charger 2; no new car
            if model.EV2 not in cars or model.CHARGER2 in chargers:
                errors["add"] = "no_shared_car"
            new_cars = []
            cars.setdefault(model.EV2, {})[model.EV_CHARGER] = model.CHARGER2
        else:
            new_cars = [model.EV2]
            cars[model.EV2] = {model.EV_CHARGER: model.CHARGER2 if own else model.CHARGER1}
        sharing_on = None if own else model.CHARGER1
    else:
        how = answers.get("how")
        if how not in HOW:
            errors["how"] = "required"
            how = "one"
        shared, chargers, cars = dict(shared_d), {}, {}
        own = how == "two_own"
        new_chargers = list(model.CHARGERS[: 2 if own else 1])
        new_cars = list(model.EVS[: 1 if how == "one" else 2])
        for i, ev in enumerate(new_cars):
            cars[ev] = {model.EV_CHARGER: model.CHARGERS[i] if own else model.CHARGER1}
        sharing_on = model.CHARGER1 if how == "two_shared" else None
        _house(answers.get("house") or {}, shared, first, errors)
        if (answers.get("house") or {}).get("responsibility_ok") is not True:
            errors["house.responsibility_ok"] = "confirm_required"
        else:
            from homeassistant.util import dt as dt_util

            shared[RESPONSIBILITY] = dt_util.now().isoformat(timespec="seconds")

    # chargers
    for ch in new_chargers:
        a = (answers.get("chargers") or {}).get(ch) or {}
        brand = str(a.get("brand") or "")
        from .config_flow import CHARGER_TYPES

        if brand not in CHARGER_TYPES:
            errors[f"chargers.{ch}.brand"] = "unknown_charger" if brand else "required"
            continue
        others = [v for k, v in chargers.items() if k != ch]
        other = others[0] if others else None
        devices = [d["id"] for d in charger_devices(hass, brand)]
        device = a.get("device") or None
        other_device = _device_of_values(hass, other)
        if device is not None and device not in devices:
            errors[f"chargers.{ch}.device"] = "unknown_device"
            device = None
        elif device is not None and device == other_device:
            errors[f"chargers.{ch}.device"] = "same_device"
        if device is None:
            device = next((d for d in devices if d != other_device), None)
        vals, _prof = _apply_brand(hass, template, brand, other, device, {other_device} if other_device else set())
        for key, val in (a.get("entities") or {}).items():
            if isinstance(val, str):
                val = val.strip()
            if val not in (None, ""):
                vals[key] = val
        # never one entity for both chargers (decision 07-11 22:59)
        from .config_flow import _KEY_FIELD

        for conf in _KEY_FIELD.values():
            if str(vals.get(conf) or "").strip() and str(vals.get(conf)).strip() in _entities_of(other):
                errors[f"chargers.{ch}.{conf}"] = "charger_entity_taken"
        for key in CHARGER_REQUIRED:
            if not str(vals.get(key) or "").strip():
                errors[f"chargers.{ch}.{key}"] = "required"
        cur = str(vals.get(CONF_CHARGER_CURRENT) or "")
        if cur and safety.is_installer_setting(cur):
            errors[f"chargers.{ch}.{CONF_CHARGER_CURRENT}"] = "installer_setting"  # hard rule 30-10
        chargers[ch] = vals
        mx = _int(a.get("max_a"), 16)
        if not 6 <= mx <= 32:
            errors[f"chargers.{ch}.max_a"] = "required"
        if mx == 16:  # "weet ik niet": read from the charger when it reports its maximum
            mx = installer_max(hass, vals.get(CONF_CHARGER_CURRENT))
        first.setdefault(ch, {})["charger_max_a"] = mx

    # cars
    used: list[str] = [str(c.get(CONF_EV_SOC)) for k, c in cars.items() if k not in new_cars and c.get(CONF_EV_SOC)]
    taken: list[str] = [str(colour) for ev in cars if ev not in new_cars and (colour := (colours or {}).get(ev))]
    for ev in new_cars:
        a = (answers.get("cars") or {}).get(ev) or {}
        car = cars[ev]
        if "soc" in a:
            soc = str(a.get("soc") or "").strip()  # given; empty = none, HESC estimates it
        else:  # the panel skipped the screen: exactly one found is taken (decision 01-11 nr 7)
            from .config_flow import ev_soc_candidates

            left = ev_soc_candidates(hass, used)
            soc = left[0] if len(left) == 1 else ""
        if soc and soc in used:
            errors[f"cars.{ev}.soc"] = "required"
        used.append(soc)
        if soc:
            car[CONF_EV_SOC] = soc
        from .config_flow import car_device

        car[model.EV_NAME] = str(a.get("name") or "").strip() or car_device(hass, soc)[0] or model.car_name(hass, soc) or ev.upper()
        if own and not add and a.get("charger") in model.CHARGERS:
            car[model.EV_CHARGER] = a["charger"]
        colour = str(a.get("colour") or "") or (COLOUR_DEFAULT[ev] if COLOUR_DEFAULT[ev] not in taken else
                                                 next(c for c in COLOURS if c not in taken))
        if colour not in COLOURS:
            errors[f"cars.{ev}.colour"] = "required"
        elif colour in taken:
            errors[f"cars.{ev}.colour"] = "colour_taken"
        taken.append(colour)
        first.setdefault(ev, {})["colour"] = colour
        cap = _float(a.get("capacity"))
        if cap is None or not 10 <= cap <= 150:
            errors[f"cars.{ev}.capacity"] = "capacity_invalid"  # 01-11 11:50: the user fills it in
        else:
            first.setdefault(ev, {})["ev_battery_kwh"] = cap

    if sharing_on:
        s = answers.get("sharing") or {}
        first.setdefault(sharing_on, {}).update({"swap_time": str(s.get("swap_time") or "22:30"),
                                                  "swap_reminder": bool(s.get("swap_reminder", True))})

    if not add:
        _sources(hass, answers, shared, errors)
        _price(hass, answers, first, errors, price_sources)
        shared.pop("_dynamic", None)
        shared[SETUP_DONE] = True
    shared[FIRST_VALUES] = first
    return {"shared": shared, "evs": cars, "chargers": chargers}, errors


def _house(h: dict[str, Any], shared: dict[str, Any], first: dict[str, dict[str, Any]], errors: dict[str, str]) -> None:
    phases = str(h.get("phases") or "Don't know")
    if phases not in PHASES:
        errors["house.phases"] = "required"
    amps = _float(h.get("amps"))
    if amps is None or not AMPS_MIN <= amps <= AMPS_MAX:
        errors["house.amps"] = "amps_invalid"
        amps = 25
    lb = str(h.get("load_balancer") or "Don't know")
    if lb not in LOAD_BALANCER:
        errors["house.load_balancer"] = "required"
    first.setdefault("shared", {}).update(house_phases=phases, house_amps=amps, house_load_balancer=lb)
    shared["_solar"], shared["_dynamic"] = bool(h.get("solar", True)), bool(h.get("dynamic", False))


def _sources(hass: HomeAssistant, answers: dict[str, Any], shared: dict[str, Any], errors: dict[str, str]) -> None:
    from .config_flow import _helper_text
    from .finders import grid_choices, pv_candidates

    solar = shared.pop("_solar", True)
    src = answers.get("sources") or {}
    if not solar:
        for key in (CONF_USE_HPVC_SOURCES, CONF_PV_POWER, CONF_FORECAST_NOW, CONF_FORECAST_30M, CONF_FORECAST_ATTRIBUTE,
                    "solar_today_sensor", "solar_tomorrow_sensor", CONF_USE_IRRADIANCE, CONF_IRRADIANCE):
            shared.pop(key, None)
        shared.update({CONF_NO_SOLAR: True, CONF_STANDALONE: True})
    else:
        pv = pv_candidates(hass)
        given = str(src.get(CONF_PV_POWER) or "").strip()
        if given:
            shared[CONF_PV_POWER] = given
            # 11-11-2026: a solar sensor chosen here wins over HPVC's (HPVC may see only part of the panels);
            # HPVC's sources only stay when HESC would otherwise miss the grid power
            if str(src.get(CONF_GRID_POWER) or "").strip() or len(grid_choices(hass)) == 1:
                shared[CONF_USE_HPVC_SOURCES] = False
        elif len(pv) == 1:
            shared[CONF_PV_POWER] = pv[0]
        elif not (shared.get(CONF_USE_HPVC_SOURCES) and _helper_text(hass, HPVC_PV_HELPER)):
            errors[f"sources.{CONF_PV_POWER}"] = "required"
        for key in (CONF_FORECAST_NOW, CONF_FORECAST_30M):
            val = str(src.get(key) or "").strip()
            if val:
                shared[key] = val
        fc = shared.get(CONF_FORECAST_NOW)
        if fc and hass.states.get(str(fc)) is None:  # a suggestion that is not there: no forecast (level C)
            for key in (CONF_FORECAST_NOW, CONF_FORECAST_30M):
                shared.pop(key, None)
        # HPVC: only asked when found (decision 01-11 nr 9); its entities are filled in by HESC
        if not shared.get(CONF_STANDALONE):
            shared[CONF_STANDALONE] = not bool(answers.get("hpvc", True))
    given = str(src.get(CONF_GRID_POWER) or "").strip()
    export = str(src.get(CONF_GRID_EXPORT_SENSOR) or "").strip()
    grid = grid_choices(hass)
    shared.pop(CONF_GRID_EXPORT_SENSOR, None)
    if given:
        shared[CONF_GRID_POWER] = given
        if export:  # the choice "import + export": HESC uses import - export
            shared[CONF_GRID_EXPORT_SENSOR] = export
    elif len(grid) == 1:
        shared[CONF_GRID_POWER] = grid[0]["entity_id"]
        if grid[0].get("export_entity_id"):
            shared[CONF_GRID_EXPORT_SENSOR] = grid[0]["export_entity_id"]
    # nothing given and not exactly one found: HPVC's grid sensor when HESC takes it (grid_from_hpvc),
    # else the grid power stays empty and shows as missing, as before


def _price(hass: HomeAssistant, answers: dict[str, Any], first: dict[str, dict[str, Any]], errors: dict[str, str],
           price_sources: Any) -> None:
    from .plan_settings import BY_KEY

    shared_first = first.setdefault("shared", {})
    if not answers.get("house", {}).get("dynamic", False):
        return
    p = answers.get("price") or {}
    source, sensor = str(p.get("source") or ""), str(p.get("sensor") or "").strip()
    if not source:
        found = price_sources(hass)
        if len(found) == 1:
            source, sensor = found[0]["source"], found[0]["sensor"] or ""
    if source not in BY_KEY["price_source"].options:
        errors["price.source"] = "required"
        return
    shared_first["price_source"] = source
    if sensor:
        shared_first["price_sensor"] = sensor


def _int(v: Any, default: int) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def _float(v: Any) -> float | None:
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None


# ---- websocket ------------------------------------------------------------------------------------------
def async_setup_websocket(hass: HomeAssistant) -> None:
    import voluptuous as vol
    from homeassistant.components import websocket_api

    def entry() -> Any:
        found = hass.config_entries.async_entries(DOMAIN)
        return found[0] if found else None

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/find"})
    @websocket_api.async_response
    async def ws_find(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        e = entry()
        out = find(hass)
        out["setup_done"] = setup_done(e.options or e.data) if e else False
        out["cars_set_up"] = model.ev_ids(model.ensure_nested(e.options or e.data)) if e else []
        connection.send_result(msg["id"], out)

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/charger", vol.Required("brand"): str,
                                      vol.Optional("charger"): str, vol.Optional("device"): vol.Any(str, None),
                                      vol.Optional("other_device"): vol.Any(str, None)})
    @websocket_api.async_response
    async def ws_charger(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        e = entry()
        other = None
        if e is not None and msg.get("charger") == model.CHARGER2:
            other = (model.ensure_nested(e.options or e.data)["chargers"].get(model.CHARGER1)) or None
        connection.send_result(msg["id"], charger(hass, msg["brand"], other, msg.get("device"), msg.get("other_device")))

    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/save", vol.Required("answers"): dict,
                                      vol.Optional("add_car", default=False): bool,
                                      vol.Optional("add_charger", default=False): bool})
    @websocket_api.async_response
    async def ws_save(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        e = entry()
        if e is None:
            connection.send_error(msg["id"], "not_set_up", "HESC v4 is not installed")
            return
        current = e.options or e.data
        if msg["add_car"] and len(model.ev_ids(model.ensure_nested(current))) >= 2:
            connection.send_result(msg["id"], {"ok": False, "errors": {"add": "two_cars_already"}})
            return
        answers = dict(msg["answers"])
        if msg["add_charger"]:  # 08-11: charger 2 for EV2, that shares charger 1 now
            answers["add"] = "charger"
        adding = msg["add_car"] or msg["add_charger"]
        nested, errors = build(hass, answers, current if adding else None, _colours(hass, e))
        if errors:
            connection.send_result(msg["id"], {"ok": False, "errors": errors})
            return
        await async_store(hass, e, nested)
        if msg["add_charger"]:
            await fleet_setup.async_clean_entities(hass, e)
        connection.send_result(msg["id"], {"ok": True})

    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/source", vol.Required("key"): str,
                                      vol.Required("entity_id"): vol.Any(str, None),
                                      vol.Optional("car", default=model.EV1): vol.In(model.EVS)})
    @websocket_api.async_response
    async def ws_source(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        """Set one source (opmaakchat 06-11 13:45): {key, entity_id ("" or null = empty), car?}. Result
        {"ok": true} or {"ok": false, "error": unknown_source | wrong_kind | not_found | installer_setting |
        unknown_car}. A car or charger source is set for `car` (its charger). HESC reloads."""
        e = entry()
        if e is None:
            connection.send_error(msg["id"], "not_set_up", "HESC v4 is not installed")
            return
        key, eid = sources.key_of(msg["key"]), str(msg["entity_id"] or "").strip()
        current = model.ensure_nested(e.options or e.data)
        error = sources.check(hass, key, eid)
        if error is None and msg["car"] not in model.ev_ids(current):
            error = "unknown_car"
        if error is not None:
            connection.send_result(msg["id"], {"ok": False, "error": error})
            return
        # 08-11 (opmaakchat 10:40): no reload - the logic reads its settings from the entry every round
        await async_store_live(hass, e, model.apply(current, {key: eid}, msg["car"]))
        connection.send_result(msg["id"], {"ok": True, "key": key})

    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/value", vol.Required("key"): str,
                                      vol.Required("value"): vol.Any(str, [str]),
                                      vol.Optional("car", default=model.EV1): vol.In(model.EVS)})
    @websocket_api.async_response
    async def ws_value(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        """08-11 (opmaakchat 10:40): a charger's value list: `charger_eco_value` (the modes that charge on
        the sun) or `ev_disconnected_values` (the states of the status sensor that mean "no car"). `value`:
        a list or a comma-separated text. Result {"ok": true, "key", "value"} or {"ok": false, "error":
        unknown_value | empty | unknown_car}. No reload."""
        e = entry()
        if e is None:
            connection.send_error(msg["id"], "not_set_up", "HESC v4 is not installed")
            return
        current = model.ensure_nested(e.options or e.data)
        key = sources.value_key_of(msg["key"])
        vals = msg["value"] if isinstance(msg["value"], list) else str(msg["value"]).split(",")
        text = ", ".join(v.strip() for v in vals if str(v).strip())
        error = ("unknown_value" if key is None else "empty" if not text
                 else "unknown_car" if msg["car"] not in model.ev_ids(current) else None)
        if error:
            connection.send_result(msg["id"], {"ok": False, "error": error})
            return
        await async_store_live(hass, e, model.apply(current, {key: text}, msg["car"]))
        connection.send_result(msg["id"], {"ok": True, "key": key, "value": text})

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/values_seen", vol.Required("entity_id"): str,
                                      vol.Optional("days", default=14): vol.All(int, vol.Range(min=1, max=60))})
    @websocket_api.async_response
    async def ws_values_seen(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        """08-11 (opmaakchat 10:40): the states an entity had (the recorder, last `days` days, most recent
        first) plus its `options` and the values the charger table knows, for the "no car" ticks."""
        connection.send_result(msg["id"], await sources.async_values_seen(hass, msg["entity_id"], msg["days"]))

    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/remove_car", vol.Required("car"): str,
                                      vol.Optional("check_only", default=False): bool})
    @websocket_api.async_response
    async def ws_remove_car(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        """08-11: remove a car (only EV2) and its own charger. `check_only`: only the consequences."""
        e = entry()
        if e is None:
            connection.send_error(msg["id"], "not_set_up", "HESC v4 is not installed")
            return
        connection.send_result(msg["id"], await fleet_setup.async_remove_car(hass, e, msg["car"], msg["check_only"]))

    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/remove_charger", vol.Required("charger"): str,
                                      vol.Optional("check_only", default=False): bool})
    @websocket_api.async_response
    async def ws_remove_charger(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        """08-11: remove a charger (only charger 2); its car moves to charger 1 (they share it)."""
        e = entry()
        if e is None:
            connection.send_error(msg["id"], "not_set_up", "HESC v4 is not installed")
            return
        connection.send_result(msg["id"], await fleet_setup.async_remove_charger(hass, e, msg["charger"],
                                                                                 msg["check_only"]))

    for cmd in (ws_find, ws_charger, ws_save, ws_source, ws_remove_car, ws_remove_charger, ws_value, ws_values_seen):
        websocket_api.async_register_command(hass, cmd)


def _colours(hass: HomeAssistant, e: Any) -> dict[str, str]:
    """The colour of every car set up now (its select `select.hesc_v4_evN_colour`)."""
    from homeassistant.helpers import entity_registry as er

    reg, out = er.async_get(hass), {}
    for ev in model.ev_ids(model.ensure_nested(e.options or e.data)):
        eid = reg.async_get_entity_id("select", DOMAIN, model.unique_id(e.entry_id, "colour", ev))
        st = hass.states.get(eid) if eid else None
        out[ev] = st.state if st and st.state in COLOURS else COLOUR_DEFAULT[ev]
    return out


async def async_store_live(hass: HomeAssistant, e: Any, nested: dict[str, Any]) -> None:
    """Store a changed source or value without reloading: the logic reads the entry every round; one
    round now so the setup sensors show the change at once."""
    if e.options:
        hass.config_entries.async_update_entry(e, options=nested)
    else:
        hass.config_entries.async_update_entry(e, data=nested)
    co = getattr(e, "runtime_data", None)
    if co is not None:
        co._last_run.pop("dashboard templates", None)  # the setup sensors show the change in this round
        await co.async_refresh()


async def async_store(hass: HomeAssistant, e: Any, nested: dict[str, Any]) -> None:
    """Store the settings (options once they exist, else data) and reload: the entities get the values of
    `first_values` at the start (HescCoordinator.async_apply_first_values)."""
    if e.options:
        hass.config_entries.async_update_entry(e, options=nested)
    else:
        hass.config_entries.async_update_entry(e, data=nested)
    if e.state.recoverable:
        await hass.config_entries.async_reload(e.entry_id)
