"""Charge plan texts (price sensor, 'charge now' value, notify services), replacing v2's input_text helpers."""
from __future__ import annotations

from homeassistant.components.text import TextEntity
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import model
from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity, per_car
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(PlanText(c, s, ev) for s in SETTINGS if s.kind == "text" for ev in per_car(c, s.key))
    async_add_entities([EvNameText(c, ev) for ev in c.ev_ids()])  # v4: one per car


class PlanText(PlanSettingEntity, TextEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting, ev: str = model.EV1) -> None:
        super().__init__(coordinator, spec, ev)
        self._attr_native_max = spec.max_len
        self._attr_native_min = 0
        self._attr_native_value = str(spec.default)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            self._attr_native_value = last.state
        self._restored(self._attr_native_value)

    async def async_set_value(self, value: str) -> None:
        self._attr_native_value = value
        self._store(value)
        self.async_write_ha_state()


class EvNameText(HescEntity, TextEntity):
    """v4: the car's shown name (decision 9: EV1 starts as the car's name in HA, can be changed).
    Kept in the config entry with the car (model.EV_NAME); the entity id keeps ev1 (text.hesc_v4_ev1_car_name)."""

    _attr_native_min = 1
    _attr_native_max = 40

    def __init__(self, coordinator: HescCoordinator, ev: str = model.EV1) -> None:
        super().__init__(coordinator, "ev_name", ev)

    @property
    def native_value(self) -> str:
        entry = self.coordinator.config_entry
        return model.ev_name(model.ensure_nested(entry.options or entry.data), self._ev)

    async def async_set_value(self, value: str) -> None:
        self.coordinator.store_ev(self._ev, {model.EV_NAME: value.strip() or self._ev.upper()})
        self.async_write_ha_state()
