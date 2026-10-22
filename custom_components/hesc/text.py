"""Charge plan texts (price sensor, 'charge now' value, notify services), replacing v2's input_text helpers."""
from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HescConfigEntry, HescCoordinator
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(PlanText(entry.runtime_data, s) for s in SETTINGS if s.kind == "text")


class PlanText(PlanSettingEntity, TextEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_native_max = spec.max_len
        self._attr_native_min = 0
        self._attr_native_value = str(spec.default)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._attr_native_value = last.state
        self.coordinator.plan[self._spec.key] = self._attr_native_value

    async def async_set_value(self, value: str) -> None:
        self._attr_native_value = value
        self._store(value)
        self.async_write_ha_state()
