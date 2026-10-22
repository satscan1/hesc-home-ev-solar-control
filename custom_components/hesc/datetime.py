"""One-off plan ready-by time, replacing v2's input_datetime.hesc_plan_deadline."""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.datetime import DateTimeEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .coordinator import HescConfigEntry, HescCoordinator
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(PlanDateTime(entry.runtime_data, s) for s in SETTINGS if s.kind == "datetime")


class PlanDateTime(PlanSettingEntity, DateTimeEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_native_value = None
        coordinator.datetime_entities[spec.key] = self

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._attr_native_value = dt_util.parse_datetime(last.state)
        self.coordinator.plan[self._spec.key] = self._attr_native_value

    async def async_set_value(self, value: datetime) -> None:
        self.set_from_logic(value)

    def set_from_logic(self, value: datetime | None) -> None:
        self._attr_native_value = value
        self.coordinator.plan[self._spec.key] = value
        self.async_write_ha_state()
