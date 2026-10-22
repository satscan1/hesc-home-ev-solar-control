"""Tuning numbers (thresholds and times), replacing v2's input_number helpers."""

from __future__ import annotations

from homeassistant.components.number import NumberMode, RestoreNumber
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting
from .tuning import NUMBERS, NumberSpec


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities([
        *(TuningNumber(entry.runtime_data, spec) for spec in NUMBERS),
        *(PlanNumber(entry.runtime_data, s) for s in SETTINGS if s.kind == "number"),
    ])


class TuningNumber(HescEntity, RestoreNumber):
    """One v2 tuning value; the default is v2's first-install value."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: HescCoordinator, spec: NumberSpec) -> None:
        super().__init__(coordinator, spec.key)
        self._spec = spec
        self._attr_native_min_value = spec.minimum
        self._attr_native_max_value = spec.maximum
        self._attr_native_step = spec.step
        self._attr_native_unit_of_measurement = spec.unit
        self._attr_native_value = float(spec.default)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_number_data()
        if last is not None and last.native_value is not None:
            self._attr_native_value = min(max(last.native_value, self._spec.minimum), self._spec.maximum)
        self.coordinator.tuning[self._spec.key] = float(self._attr_native_value)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.coordinator.tuning[self._spec.key] = float(value)
        self.async_write_ha_state()


class PlanNumber(PlanSettingEntity, RestoreNumber):
    """An own charge plan number (battery size, charging power, opportunity price, ...)."""

    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_native_min_value = spec.minimum
        self._attr_native_max_value = spec.maximum
        self._attr_native_step = spec.step
        self._attr_native_unit_of_measurement = spec.unit
        self._attr_native_value = float(spec.default)  # type: ignore[arg-type]

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_number_data()
        if last is not None and last.native_value is not None:
            self._attr_native_value = min(max(last.native_value, self._spec.minimum), self._spec.maximum)
        self.coordinator.plan[self._spec.key] = float(self._attr_native_value)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self._store(float(value))
        self.async_write_ha_state()
