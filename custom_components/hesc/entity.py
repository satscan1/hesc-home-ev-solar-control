"""Base entity: every HESC v3 entity hangs under one device "HESC v3"."""

from __future__ import annotations

import json
from pathlib import Path

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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


def device_info(entry_id: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=NAME,
        manufacturer="HESC",
        model="Home EV Solar Control",
        sw_version=f"{VERSION} · {BUILD_DATE}",  # shown under the logo on Main
        entry_type=DeviceEntryType.SERVICE,
    )


class HescEntity(CoordinatorEntity[HescCoordinator]):
    """An entity that shows something the coordinator read."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: HescCoordinator, key: str) -> None:
        super().__init__(coordinator)
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = device_info(entry_id)

    @property
    def suggested_object_id(self) -> str | None:
        """A new entity gets its id from the English name, in every language (since 3.0.0, which adds
        translations). Home Assistant would otherwise take it from the translated name (Dutch, German,
        ...), while the dashboard, the guide and other integrations (e.g. HBC) use the English ids.
        Ids that already exist never change; only the name shown follows the language."""
        platform = getattr(getattr(self, "platform", None), "domain", None)
        name = ENGLISH_NAMES.get(f"{platform}:{self.translation_key}")
        return name if name else super().suggested_object_id
