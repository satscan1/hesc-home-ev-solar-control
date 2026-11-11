"""Holiday mode end date, replacing v2's input_datetime.hesc_vacation_until."""
from __future__ import annotations

from datetime import date

from homeassistant.components.date import DateEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .coordinator import HescConfigEntry, HescCoordinator
from .entity import per_car
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(PlanDate(c, s, ev) for s in SETTINGS if s.kind == "date" for ev in per_car(c, s.key))


class PlanDate(PlanSettingEntity, DateEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting, ev: str = "ev1") -> None:
        super().__init__(coordinator, spec, ev)
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._attr_native_value = dt_util.parse_date(last.state)
        self._restored(self._attr_native_value)
        with self._car():
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
