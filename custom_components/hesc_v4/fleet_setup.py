"""Removing a car or a charger, from the panel (decision 08-11-2026 08:43 / 08:50).

Only the second car (EV2) and the second charger can be removed: the entity ids keep EV1/EV2 and
charger1/charger2 (decision 30-10 20:31), so EV1 stays EV1 and nothing is renumbered.

- Remove EV2: its settings, its entities and its HESC device go; its own charger (charger 2, when no other
  car is on it) goes with it. Its files (planning, charging costs, history, learned charging power) are
  NOT deleted: they are renamed to `removed_<date>_<name>` in HESC's folder, so nothing is lost.
- Remove charger 2: the car on it moves to charger 1 (the two cars share charger 1 then).

`check_only` gives the consequences without changing anything (the panel shows them first; removing
stays SatScan's decision). Afterwards HESC reloads and the entities that no longer belong to a car or
charger are removed from Home Assistant's entity registry.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.util import dt as dt_util

from . import cars, model
from .const import DOMAIN

# the files a car keeps in HESC's folder (coordinator._car_paths)
CAR_FILES = ("own_flags.json", "current_control.json", "history.jsonl", "ev_soc_plugins.json",
             "charging_costs.json", "planning.json", "charge_power.json")


def _nested(e: Any) -> dict[str, Any]:
    return model.ensure_nested(e.options or e.data)


def _owners(nested: dict[str, Any]) -> set[str]:
    """The cars and chargers set up, and per charger whether two cars share it."""
    out = set(model.ev_ids(nested))
    out |= {model.charger_of(nested, ev) for ev in model.ev_ids(nested)}
    return out


def _orphans(hass: HomeAssistant, e: Any, nested: dict[str, Any]) -> list[er.RegistryEntry]:
    """Entities of this entry whose car or charger is gone, and the sharing entities of a charger that is
    no longer shared."""
    owners = _owners(nested)
    shared: dict[str, int] = {}
    for ev in model.ev_ids(nested):
        shared[model.charger_of(nested, ev)] = shared.get(model.charger_of(nested, ev), 0) + 1
    out = []
    for ent in er.async_entries_for_config_entry(er.async_get(hass), e.entry_id):
        rest = ent.unique_id[len(e.entry_id) + 1:] if ent.unique_id.startswith(e.entry_id + "_") else ""
        part = next((p for p in (*model.EVS, *model.CHARGERS) if rest.startswith(p + "_")), None)
        if part is None:
            continue
        key = rest[len(part) + 1:]
        if part not in owners:
            out.append(ent)
        elif key in model.SHARED_ONLY:
            ch = part if part in model.CHARGERS else model.charger_of(nested, part)
            if shared.get(ch, 0) < 2:
                out.append(ent)
    return out


async def async_clean_entities(hass: HomeAssistant, e: Any) -> list[str]:
    """Remove the entities (and HESC devices) that no longer belong to a car or charger."""
    nested = _nested(e)
    reg, devs = er.async_get(hass), dr.async_get(hass)
    gone = []
    for ent in _orphans(hass, e, nested):
        reg.async_remove(ent.entity_id)
        gone.append(ent.entity_id)
    owners = _owners(nested)
    for dev in dr.async_entries_for_config_entry(devs, e.entry_id):
        ident = next((i[1] for i in dev.identifiers if i[0] == DOMAIN), "")
        part = ident[len(e.entry_id) + 1:] if ident.startswith(e.entry_id + "_") else ""
        if part in (*model.EVS, *model.CHARGERS) and part not in owners:
            devs.async_remove_device(dev.id)
    return gone


def _files(hass: HomeAssistant, ev: str) -> list[Path]:
    base = Path(hass.config.path(DOMAIN))
    out = [base / cars.file_name(n, ev) for n in CAR_FILES]
    out.append(base / cars.file_name("charging_costs_days.csv", ev))
    out.append(base / cars.file_name("charging_costs_months.csv", ev))
    return [p for p in out if p.exists()]


async def async_remove_car(hass: HomeAssistant, e: Any, car: str, check_only: bool) -> dict[str, Any]:
    from .setup_wizard import async_store

    nested = _nested(e)
    if car != model.EV2 or car not in model.ev_ids(nested):
        return {"ok": False, "error": "only_ev2" if car in model.ev_ids(nested) else "unknown_car"}
    ch = model.charger_of(nested, car)
    others_on = [ev for ev in model.ev_ids(nested) if ev != car and model.charger_of(nested, ev) == ch]
    new = model.ensure_nested(nested)
    new["evs"].pop(car, None)
    if not others_on:
        new["chargers"].pop(ch, None)
    files = await hass.async_add_executor_job(_files, hass, car)
    entities = sorted(x.entity_id for x in _orphans(hass, e, new))
    out = {"ok": True, "car": car, "name": model.ev_name(nested, car),
           "charger_removed": None if others_on else ch, "entities": entities,
           "files_kept": [p.name for p in files]}
    if check_only:
        return out
    stamp = dt_util.now().strftime("%Y%m%d-%H%M")

    def rename() -> list[str]:
        kept = []
        for p in files:
            target = p.with_name(f"removed_{stamp}_{p.name}")
            p.rename(target)
            kept.append(target.name)
        return kept

    out["files_kept"] = await hass.async_add_executor_job(rename)
    await async_store(hass, e, new)
    out["entities"] = await async_clean_entities(hass, e)
    return out


async def async_remove_charger(hass: HomeAssistant, e: Any, charger: str, check_only: bool) -> dict[str, Any]:
    from .setup_wizard import async_store

    nested = _nested(e)
    if charger != model.CHARGER2 or charger not in (nested.get("chargers") or {}):
        return {"ok": False, "error": "only_charger2" if charger in (nested.get("chargers") or {}) else "unknown_charger"}
    moved = [ev for ev in model.ev_ids(nested) if model.charger_of(nested, ev) == charger]
    new = model.ensure_nested(nested)
    new["chargers"].pop(charger, None)
    for ev in moved:
        new["evs"][ev][model.EV_CHARGER] = model.CHARGER1
    out = {"ok": True, "charger": charger, "cars_moved_to_charger1": moved,
           "entities": sorted(x.entity_id for x in _orphans(hass, e, new))}
    if check_only:
        return out
    await async_store(hass, e, new)
    out["entities"] = await async_clean_entities(hass, e)
    return out
