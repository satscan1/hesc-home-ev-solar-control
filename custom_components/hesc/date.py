"""Holiday mode end date, replacing v2's input_datetime.hesc_vacation_until."""
from __future__ import annotations

from datetime import date

from homeassistant.components.date import DateEntity
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
    async_add_entities(PlanDate(entry.runtime_data, s) for s in SETTINGS if s.kind == "date")


class PlanDate(PlanSettingEntity, DateEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._attr_native_value = dt_util.parse_date(last.state)
        self.coordinator.plan[self._spec.key] = self._attr_native_value
        self.coordinator.date_entities[self._spec.key] = self

    def clear(self) -> None:
        """Since 3.0.0 (hesc.undo_skip_plan_day): back to no date."""
        self._attr_native_value = None
        self._store(None)
        self.async_write_ha_state()

    async def async_set_value(self, value: date) -> None:
        self._attr_native_value = value
        self._store(value)
        self.async_write_ha_state()
