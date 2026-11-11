"""Diagnostic binary sensors: inputs valid, EV connected, charger in solar mode, HPVC limiting."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity, per_car
from .inputs import Inputs


@dataclass(frozen=True, kw_only=True)
class HescBinaryDescription(BinarySensorEntityDescription):
    value: Callable[[Inputs], bool]


BINARY_SENSORS: tuple[HescBinaryDescription, ...] = (
    HescBinaryDescription(
        key="inputs_valid", translation_key="inputs_valid", entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.valid,
    ),
    HescBinaryDescription(
        key="ev_connected", translation_key="ev_connected", device_class=BinarySensorDeviceClass.PLUG,
        entity_category=EntityCategory.DIAGNOSTIC, value=lambda i: i.ev_connected,
    ),
    HescBinaryDescription(
        key="charger_solar_mode", translation_key="charger_solar_mode", entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.in_solar_mode,
    ),
    HescBinaryDescription(
        key="hpvc_limiting", translation_key="hpvc_limiting", entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.hpvc_on and i.hpvc_limited,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    coordinator = entry.runtime_data
    c = coordinator
    async_add_entities([*(HescBinarySensor(c, d, ev) for d in BINARY_SENSORS for ev in per_car(c, d.key)),
                        *(ComputedBinarySensor(c, k, v2, ev) for k, v2 in COMPUTED_BINARY for ev in per_car(c, k)),
                        ReportReadyBinarySensor(coordinator), KickHandBackBinarySensor(coordinator),
                        FirstStartDoneBinarySensor(coordinator)])


class HescBinarySensor(HescEntity, BinarySensorEntity):
    entity_description: HescBinaryDescription

    def __init__(self, coordinator: HescCoordinator, description: HescBinaryDescription, ev: str = "ev1") -> None:
        super().__init__(coordinator, description.key, ev)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        inputs = self.coordinator.car_inputs(self._ev)  # v4: what this car's charger reports
        return None if inputs is None else self.entity_description.value(inputs)


# v2's dashboard template binary sensors, computed by v3 (key -> v2 entity id)
COMPUTED_BINARY: tuple[tuple[str, str], ...] = (
    ("diag_ev_connected", "binary_sensor.hesc_diag_ev_connected"),
    ("diag_charger_solar_mode", "binary_sensor.hesc_diag_charger_solar_mode"),
    ("diag_release_active", "binary_sensor.hesc_diag_release_active"),
    ("configuration_valid", "binary_sensor.hesc_configuration_valid"),
    ("prices_available", "binary_sensor.hesc_prices_available"),
    ("check_charger", "binary_sensor.hesc_check_charger"),
    ("check_sources", "binary_sensor.hesc_check_sources"),
    ("check_weather_station", "binary_sensor.hesc_check_weather_station"),
    ("check_charge_plan", "binary_sensor.hesc_check_charge_plan"),
    ("check_home_battery_and_ev", "binary_sensor.hesc_check_home_battery_and_ev"),
    # setup-screen switches the dashboard shows or hides sections on (mirrors of v2's input_booleans)
    ("setup_standalone", "input_boolean.hesc_standalone"),
    ("setup_use_hpvc_sources", "input_boolean.hesc_use_hpvc_sources"),
    ("setup_use_irradiance", "input_boolean.hesc_use_irradiance"),
)


class ComputedBinarySensor(HescEntity, BinarySensorEntity):
    """A v2 template binary sensor, computed by v3 (same state and attributes as v2's)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: HescCoordinator, key: str, v2_id: str, ev: str = "ev1") -> None:
        super().__init__(coordinator, key, ev)
        self._v2_id = v2_id

    def _st(self) -> dict | None:
        with self._car():
            return self.coordinator.computed.get(self._v2_id)

    @property
    def is_on(self) -> bool | None:
        st = self._st()
        return None if st is None else st["state"] == "on"

    @property
    def extra_state_attributes(self) -> dict | None:
        st = self._st()
        return dict(st["attributes"]) if st and st["attributes"] else None


class ReportReadyBinarySensor(HescEntity, RestoreEntity, BinarySensorEntity):
    """v2's input_boolean.hesc_report_ready: on once a report is written, off while a new one
    is built and when the report is opened. Restored after a restart, like v2's helper."""

    _HELPER = "input_boolean.hesc_report_ready"

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "report_ready")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state in ("on", "off") and self._HELPER not in self.coordinator.published:
            self.coordinator.published[self._HELPER] = last.state

    @property
    def is_on(self) -> bool:
        return self.coordinator.published.get(self._HELPER) == "on"


class FirstStartDoneBinarySensor(HescEntity, BinarySensorEntity):
    """v4: on once the first start in the panel is done (opmaakchat 02-11 11:35, round 2 nr 1): the
    dashboard shows its other sections only then, the first start card only while it is off."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "first_start_done")

    @property
    def is_on(self) -> bool:
        from .setup_wizard import setup_done

        e = self.coordinator.config_entry
        return setup_done(e.options or e.data)


class KickHandBackBinarySensor(HescEntity, BinarySensorEntity):
    """Since 3.0.0: on while a kickstart hands the charger back to its solar mode (paused, then
    waiting for the charger to start on sun). For a home battery control: hold the home batteries
    meanwhile, also when the charger briefly shows 0 W (practice test 19-10-2026)."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "kick_hand_back")

    @property
    def is_on(self) -> bool:
        return self.coordinator.kick_hand_back
