"""Tuning numbers (thresholds and times), replacing v2's input_number helpers."""

from __future__ import annotations

from homeassistant.components.number import NumberMode, RestoreNumber
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity, per_car
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting
from .tuning import NUMBERS, NumberSpec


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([
        *(TuningNumber(c, spec, ev) for spec in NUMBERS for ev in per_car(c, spec.key)),
        *(PlanNumber(c, s, ev) for s in SETTINGS if s.kind == "number" for ev in per_car(c, s.key)),
    ])


class TuningNumber(HescEntity, RestoreNumber):
    """One v2 tuning value; the default is v2's first-install value."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: HescCoordinator, spec: NumberSpec, ev: str = "ev1") -> None:
        super().__init__(coordinator, spec.key, ev)
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
        with self._car():
            self.coordinator.tuning[self._spec.key] = float(self._attr_native_value)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        with self._car():
            self.coordinator.tuning[self._spec.key] = float(value)
        self.async_write_ha_state()


class PlanNumber(PlanSettingEntity, RestoreNumber):
    """An own charge plan number (battery size, charging power, opportunity price, ...)."""

    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: HescCoordinator, spec: Setting, ev: str = "ev1") -> None:
        super().__init__(coordinator, spec, ev)
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
        self._restored(float(self._attr_native_value))
        if self._spec.key == "soc_entered":  # v4 step 4E: cleared by the logic at unplug
            with self._car():
                self.coordinator.soc_entity = self

    async def async_set_native_value(self, value: float) -> None:
        self.set_from_logic(value)

    def set_from_logic(self, value: float) -> None:
        self._attr_native_value = value
        self._store(float(value))
        self.async_write_ha_state()
