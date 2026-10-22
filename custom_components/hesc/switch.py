"""Switches: shadow mode (on by default: HESC v3 switches nothing), HESC enabled, weather station on/off,
own charge plan settings."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_OFF, STATE_ON, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    CONF_HPVC_ENABLED,
    CONF_HPVC_LIMITED,
    CONF_IRRADIANCE,
    CONF_STANDALONE,
    CONF_USE_HPVC_SOURCES,
    CONF_USE_IRRADIANCE,
)
from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting
from .tuning import SWITCHES, SwitchSpec


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    coordinator = entry.runtime_data
    migrate_standalone_switch(hass, entry.entry_id)
    async_add_entities([
        ShadowModeSwitch(coordinator),
        WeatherStationSwitch(coordinator),
        UseHpvcSwitch(coordinator),
        HpvcSourcesSwitch(coordinator),
        *(TuningSwitch(coordinator, s) for s in SWITCHES),
        *(PlanSwitch(coordinator, s) for s in SETTINGS if s.kind == "switch"),
    ])


class ShadowModeSwitch(HescEntity, RestoreEntity, SwitchEntity):
    """Like v2's input_boolean.hesc_shadow_mode: anything but an explicit 'off' counts as on."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "shadow_mode")
        self._attr_is_on = True

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        self._attr_is_on = not (last is not None and last.state == STATE_OFF)
        self.coordinator.shadow = self._attr_is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._attr_is_on = True
        self.coordinator.shadow = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._attr_is_on = False
        self.coordinator.shadow = False
        self.async_write_ha_state()


class WeatherStationSwitch(HescEntity, SwitchEntity):
    """v2's input_boolean.hesc_use_irradiance as a dashboard toggle. It is the same choice as "Use local
    weather station" in the setup screen: both read and write the integration's stored setup."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "use_weather_station")

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.settings.get(CONF_USE_IRRADIANCE))

    def _store(self, value: bool) -> None:
        entry = self.coordinator.config_entry
        current = dict(entry.options or entry.data)
        current[CONF_USE_IRRADIANCE] = value
        if entry.options:
            self.hass.config_entries.async_update_entry(entry, options=current)
        else:
            self.hass.config_entries.async_update_entry(entry, data=current)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        if not self.coordinator.settings.get(CONF_IRRADIANCE):  # same rule as the setup screen
            raise ServiceValidationError("Choose the irradiance sensor first (setup screen, sources)")
        self._store(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._store(False)


class TuningSwitch(HescEntity, RestoreEntity, SwitchEntity):
    """A v2 on/off setting (HESC enabled); default as on a v2 first install."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator, spec: SwitchSpec) -> None:
        super().__init__(coordinator, spec.key)
        self._spec = spec
        self._attr_is_on = spec.default

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state in (STATE_ON, STATE_OFF):
            self._attr_is_on = last.state == STATE_ON
        self.coordinator.switches[self._spec.key] = bool(self._attr_is_on)

    async def _set(self, value: bool) -> None:
        self._attr_is_on = value
        self.coordinator.switches[self._spec.key] = value
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._set(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._set(False)


class PlanSwitch(PlanSettingEntity, SwitchEntity):
    """An own charge plan on/off setting (plan, weekly plan days, holiday mode, ...)."""

    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_is_on = bool(spec.default)
        coordinator.switch_entities[spec.key] = self

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state in (STATE_ON, STATE_OFF):
            self._attr_is_on = last.state == STATE_ON
        self.coordinator.plan[self._spec.key] = bool(self._attr_is_on)

    def set_from_logic(self, value: bool) -> None:
        self._attr_is_on = value
        self._store(value)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.set_from_logic(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.set_from_logic(False)


class SetupChoiceSwitch(HescEntity, SwitchEntity):
    """A setup-screen on/off choice as a dashboard toggle, like v2's input_booleans (since rc3).
    Reads and writes the integration's stored setup, same as the setup screen."""

    _attr_entity_category = EntityCategory.CONFIG
    _conf: str = ""

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.settings.get(self._conf))

    def _check(self, value: bool) -> None:
        """Same rules as the setup screen; raise when the choice cannot be made."""

    def _store(self, value: bool) -> None:
        self._check(value)
        entry = self.coordinator.config_entry
        current = dict(entry.options or entry.data)
        current[self._conf] = value
        if entry.options:
            self.hass.config_entries.async_update_entry(entry, options=current)
        else:
            self.hass.config_entries.async_update_entry(entry, data=current)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._store(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._store(False)


class UseHpvcSwitch(SetupChoiceSwitch):
    """"Use HPVC": on = work together with HPVC, off = without HPVC (standalone, the default).
    The opposite of v2's input_boolean.hesc_standalone; stored as the same setup choice.
    Since 3.0.0 (replaces the switch "No HPVC (standalone)", see migrate_standalone_switch)."""

    _conf = CONF_STANDALONE

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "use_hpvc")

    @property
    def is_on(self) -> bool:
        return not self.coordinator.settings.get(CONF_STANDALONE)

    def _check(self, value: bool) -> None:
        s = self.coordinator.settings
        if not value and not (s.get(CONF_HPVC_ENABLED) and s.get(CONF_HPVC_LIMITED)):
            raise ServiceValidationError("Choose the HPVC entities first (setup screen, HPVC step)")

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._store(False)  # with HPVC = not standalone

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._store(True)


def migrate_standalone_switch(hass: HomeAssistant, entry_id: str) -> None:
    """The switch "No HPVC (standalone)" became "Use HPVC" (the opposite) in 3.0.0. Move its registry
    entry to the new key and entity id, so no orphan "No HPVC" entity is left behind."""
    reg = er.async_get(hass)
    old = reg.async_get_entity_id("switch", DOMAIN, f"{entry_id}_standalone")
    if old is None or reg.async_get_entity_id("switch", DOMAIN, f"{entry_id}_use_hpvc"):
        return
    new_id = "switch.hesc_v3_use_hpvc"
    kwargs: dict[str, Any] = {"new_unique_id": f"{entry_id}_use_hpvc"}
    if reg.async_get(new_id) is None:
        kwargs["new_entity_id"] = new_id
    reg.async_update_entity(old, **kwargs)


class HpvcSourcesSwitch(SetupChoiceSwitch):
    """v2's input_boolean.hesc_use_hpvc_sources ("PV & grid from HPVC"). Switching it off puts the own
    PV and grid sensors back: v3 keeps the own choice and only swaps in HPVC's while this is on."""

    _conf = CONF_USE_HPVC_SOURCES

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "pv_and_grid_from_hpvc")
