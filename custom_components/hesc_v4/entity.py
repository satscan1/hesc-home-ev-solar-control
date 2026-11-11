"""Base entity: shared entities hang under the device "HESC v4", a car's under "HESC v4 EV1", a
charger's under "HESC v4 Charger1" (model.py)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import model
from .const import BUILD_DATE, DOMAIN, NAME, VERSION
from .coordinator import HescCoordinator


# "<platform>:<translation key>" -> English entity name; filled once by load_english_names()
ENGLISH_NAMES: dict[str, str] = {}


def load_english_names() -> None:
    """Read the English entity names (blocking: run it in the executor). See suggested_object_id."""
    data = json.loads((Path(__file__).parent / "translations" / "en.json").read_text(encoding="utf-8"))
    ENGLISH_NAMES.update({
        f"{platform}:{key}": item["name"]
        for platform, items in data.get("entity", {}).items()
        for key, item in items.items()
        if (item or {}).get("name")
    })


# 11-11-2026: HA 2027.8 drops `via_device` (identifiers); the sub devices point to the main device by its
# registry id. __init__ creates the main device first and puts its id here.
MAIN_DEVICE_IDS: dict[str, str] = {}


def device_info(entry_id: str, part: str | None = None) -> DeviceInfo:
    """One device "HESC v4" for the shared entities; since v4 also one per car ("HESC v4 EV1") and per
    charger ("HESC v4 Charger1"), linked to the main device. The device name gives the entity ids
    their ev1_/charger1_ part (model.unique_id)."""
    if part:
        info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{part}")},
            name=f"{NAME} {model.OWNER_LABEL.get(part, part)}",
            manufacturer="HESC",
            model="Home EV Solar Control",
            sw_version=f"{VERSION} · {BUILD_DATE}",
            entry_type=DeviceEntryType.SERVICE,
        )
        if entry_id in MAIN_DEVICE_IDS:
            info["via_device_id"] = MAIN_DEVICE_IDS[entry_id]
        return info
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=NAME,
        manufacturer="HESC",
        model="Home EV Solar Control",
        sw_version=f"{VERSION} · {BUILD_DATE}",  # shown under the logo on Main
        entry_type=DeviceEntryType.SERVICE,
    )


def per_car(coordinator: HescCoordinator, key: str) -> list[str]:
    """The cars an entity with this key is made for (model.entity_cars)."""
    return model.entity_cars(coordinator.nested, key)


class HescEntity(CoordinatorEntity[HescCoordinator]):
    """An entity that shows something the coordinator read."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: HescCoordinator, key: str, ev: str = model.EV1) -> None:
        super().__init__(coordinator)
        entry_id = coordinator.config_entry.entry_id
        # v4: the car this entity works for (its own key, or the first car on its charger); EV1 for shared
        self._ev = ev
        charger = model.charger_of(coordinator.nested, ev)
        self._attr_unique_id = model.unique_id(entry_id, key, ev, charger)
        self._attr_translation_key = key
        self._attr_device_info = device_info(entry_id, model.owner(key, ev, charger))

    def _car(self) -> Any:
        """Work on the coordinator as this entity's car (cars.py); nothing moves for EV1."""
        return self.coordinator.as_car(self._ev)

    @property
    def suggested_object_id(self) -> str | None:
        """A new entity gets its id from the English name, in every language (since 3.0.0, which adds
        translations). Home Assistant would otherwise take it from the translated name (Dutch, German,
        ...), while the dashboard, the guide and other integrations (e.g. HBC) use the English ids.
        Ids that already exist never change; only the name shown follows the language."""
        platform = getattr(getattr(self, "platform", None), "domain", None)
        name = ENGLISH_NAMES.get(f"{platform}:{self.translation_key}")
        return name if name else super().suggested_object_id
