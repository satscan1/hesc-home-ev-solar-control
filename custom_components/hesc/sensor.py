"""Diagnostic sensors: the inputs as HESC v3 reads them (same parsing as v2)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity
from .inputs import Inputs
from . import texts
from .phone import summary


@dataclass(frozen=True, kw_only=True)
class HescSensorDescription(SensorEntityDescription):
    value: Callable[[Inputs], Any]


def _power(key: str, fn: Callable[[Inputs], Any]) -> HescSensorDescription:
    return HescSensorDescription(
        key=key,
        translation_key=key,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value=fn,
    )


SENSORS: tuple[HescSensorDescription, ...] = (
    _power("pv_power", lambda i: i.pv_w),
    _power("grid_power", lambda i: i.grid_w),
    _power("ev_power", lambda i: i.ev_power_w),
    # forecast and irradiance keep the unit of their source (v2 does not convert them)
    HescSensorDescription(
        key="forecast_now", translation_key="forecast_now",
        state_class=SensorStateClass.MEASUREMENT, entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.fc_now,
    ),
    HescSensorDescription(
        key="forecast_30m", translation_key="forecast_30m",
        state_class=SensorStateClass.MEASUREMENT, entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.fc_30m,
    ),
    HescSensorDescription(
        key="irradiance", translation_key="irradiance",
        state_class=SensorStateClass.MEASUREMENT, entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.irradiance,
    ),
    HescSensorDescription(
        key="ev_soc", translation_key="ev_soc",
        device_class=SensorDeviceClass.BATTERY, state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE, entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.ev_soc,
    ),
    HescSensorDescription(
        key="charger_mode", translation_key="charger_mode", entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: i.charger_mode,
    ),
    HescSensorDescription(
        key="missing_inputs", translation_key="missing_inputs", entity_category=EntityCategory.DIAGNOSTIC,
        value=lambda i: ", ".join(i.missing),
    ),
    # HESC also works with another forecast or without one
    HescSensorDescription(
        key="forecast_source", translation_key="forecast_source", entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.ENUM, options=["solcast", "series", "sensors", "none"],
        value=lambda i: i.forecast_source,
    ),
)


# What the ported v2 logic publishes (v2 wrote these to its own input_text helpers).
STATUS_SENSORS: tuple[tuple[str, str], ...] = (
    ("state", "input_text.hesc_state"),
    ("reason", "input_text.hesc_reason"),
    ("last_action", "input_text.hesc_last_action"),
    ("insight_today", "input_text.hesc_insight_1"),
    ("insight_accuracy", "input_text.hesc_insight_2"),
    ("insight_now", "input_text.hesc_insight_3"),
    ("plan_status", "input_text.hesc_plan_status"),
    ("kick_status", "input_text.hesc_kick_status"),
    ("current_status", "input_text.hesc_current_status"),
    ("costs_export_info", "input_text.hesc_costs_export_info"),
    ("settings_backup_info", "input_text.hesc_settings_backup_info"),
    ("advice", "input_text.hesc_advice"),
    ("advice_updated", "input_text.hesc_advice_updated"),
    ("report_generated", "input_text.hesc_report_generated"),
)

# 3.1.0: status texts people read; they get the attributes `nl` and `de` (texts.py)
TRANSLATED = frozenset({
    "input_text.hesc_state", "input_text.hesc_reason", "input_text.hesc_last_action", "input_text.hesc_plan_status",
    "input_text.hesc_kick_status", "input_text.hesc_current_status",
})

# Sensors v2 made with templates or Node-RED that v3 computes itself.
# key, v2 entity it replaces
COMPUTED: tuple[tuple[str, str], ...] = (
    ("prices", "sensor.hesc_prices"),
    ("charge_plan", "sensor.hesc_charge_plan"),
    ("price_forecast", "sensor.hesc_price_forecast"),
    ("expected_charge_cost", "sensor.hesc_expected_charge_cost"),
    ("holidays", "sensor.hesc_holidays"),
    ("ev_battery_level", "sensor.hesc_ev_soc"),  # battery level with fallbacks
    ("notice", "sensor.hesc_notice"),
    ("charging_costs", "sensor.hesc_charging_costs"),
    # v2's dashboard template sensors
    ("solar_still_to_come_today", "sensor.hesc_solar_still_to_come_today"),
    ("notification_phones", "sensor.hesc_notification_phones"),
    ("charger_profile", "sensor.hesc_charger_profile"),
    ("setup", "sensor.hesc_setup"),
    ("compare", "sensor.hesc_compare"),  # v3 only: differences with v2 today
    ("advice_threshold", "sensor.hesc_advice_threshold"),
    ("phase_advice", "sensor.hesc_phase_advice"),  # rc3: phase advice (v3 only)
    ("diag_pv_power", "sensor.hesc_diag_pv_power"),
    ("diag_ev_power", "sensor.hesc_diag_ev_power"),
    ("diag_forecast_power", "sensor.hesc_diag_forecast_power"),
    ("diag_forecast_cautious", "sensor.hesc_diag_forecast_cautious"),
    ("diag_irradiance", "sensor.hesc_diag_irradiance"),
)
_W = ("W", SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT)
# key -> (unit, device class, state class) as in v2's template
_NUMERIC: dict[str, tuple[str | None, SensorDeviceClass | None, SensorStateClass | None]] = {
    "ev_battery_level": (PERCENTAGE, SensorDeviceClass.BATTERY, None),
    "charging_costs": ("kWh", None, None),
    "solar_still_to_come_today": ("kWh", None, None),
    "diag_pv_power": _W, "diag_ev_power": _W, "diag_forecast_power": _W, "diag_forecast_cautious": _W,
    "diag_irradiance": ("W/m²", None, SensorStateClass.MEASUREMENT),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    coordinator = entry.runtime_data
    async_add_entities([
        *(HescSensor(coordinator, d) for d in SENSORS),
        *(StatusSensor(coordinator, key, helper) for key, helper in STATUS_SENSORS),
        *(ComputedSensor(coordinator, key, v2_id) for key, v2_id in COMPUTED),
        SummarySensor(coordinator),
    ])


class ComputedSensor(HescEntity, SensorEntity):
    """A v2 template/Node-RED sensor, computed by v3 (same state and attributes as v2's)."""

    # large lists that change often: shown, not stored in the recorder
    _unrecorded_attributes = frozenset({"raw_today", "raw_tomorrow", "plan", "forecast", "dates", "days", "months", "phones", "profile", "last_difference"})

    def __init__(self, coordinator: HescCoordinator, key: str, v2_id: str) -> None:
        super().__init__(coordinator, key)
        self._v2_id = v2_id
        self._timestamp = key == "charge_plan"
        if self._timestamp:
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._key = key
        self._numeric = key in _NUMERIC
        if self._numeric:
            unit, dclass, sclass = _NUMERIC[key]
            self._attr_native_unit_of_measurement = unit
            if dclass is not None:
                self._attr_device_class = dclass
            if sclass is not None:
                self._attr_state_class = sclass
        if key == "phase_advice":  # rc3: translated stages
            from .phase_advice import STAGES

            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = list(STAGES)
        if key.startswith("diag_") or key in ("notification_phones", "charger_profile", "setup"):
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        st = self.coordinator.computed.get(self._v2_id)
        return super().available and not (st is not None and st["state"] == "unavailable")

    @property
    def native_value(self) -> Any:
        st = self.coordinator.computed.get(self._v2_id)
        if st is None or st["state"] in ("", "unknown"):
            return None
        if self._timestamp:
            from homeassistant.util import dt as dt_util

            return dt_util.parse_datetime(st["state"])
        if self._numeric or self.native_unit_of_measurement:
            # v2 shows a whole number as text ("40"); a numeric sensor would show "40.0"
            try:
                v = float(st["state"])
            except ValueError:
                return None
            if self._key == "solar_still_to_come_today":
                return v  # v2 rounds to 1 decimal and shows "0.0"
            return int(v) if v.is_integer() else v
        return st["state"]

    @property
    def native_unit_of_measurement(self) -> str | None:
        if self._numeric:
            return self._attr_native_unit_of_measurement
        # v2's advised start threshold has "W" only while there is an advice (else "collecting")
        st = self.coordinator.computed.get(self._v2_id)
        if self._key == "advice_threshold" and st is not None:
            return st["attributes"].get("unit_of_measurement")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        st = self.coordinator.computed.get(self._v2_id)
        if st is None:
            return None
        out = {k: v for k, v in st["attributes"].items() if k not in ("friendly_name", "icon", "unit_of_measurement")}
        if self._key == "notice":  # 3.1.0: the notice line in Dutch and German too
            out.update(texts.translated(st["state"] if st["state"] != "none" else None))
        return out


class StatusSensor(HescEntity, RestoreEntity, SensorEntity):
    """A status text of the v2 logic, as v3 computes it (never written to v2's helpers).

    Restored after a restart, like v2's input_text helpers, so the logic finds its last
    action again (v2 10-10-2026: do not log it again with a new time).
    """

    def __init__(self, coordinator: HescCoordinator, key: str, helper: str) -> None:
        super().__init__(coordinator, key)
        self._helper = helper

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state not in ("unknown", "unavailable") and self._helper not in self.coordinator.published:
            self.coordinator.published[self._helper] = last.state

    @property
    def native_value(self) -> str | None:
        return self.coordinator.published.get(self._helper)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        out: dict[str, Any] = {}
        if self._helper == "input_text.hesc_state":
            ctx = self.coordinator.context or {}
            out["release_state"] = ctx.get("state")
        if self._helper in TRANSLATED:
            # 3.1.0: the same text in Dutch and German for the dashboard in that language
            out.update(texts.translated(self.native_value))
        return out or None


class HescSensor(HescEntity, SensorEntity):
    entity_description: HescSensorDescription

    def __init__(self, coordinator: HescCoordinator, description: HescSensorDescription) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        return self.entity_description.value(self.coordinator.data)


class SummarySensor(HescEntity, SensorEntity):
    """Since 3.0.0: one line for a phone widget or the Apple Watch (see summary())."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "summary")

    def _calc(self) -> tuple[str | None, dict[str, Any]]:
        c = self.coordinator
        soc = (c.computed.get("sensor.hesc_ev_soc") or {}).get("state")
        plan_raw = ((c.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
        return summary(soc, plan_raw, c.published.get("input_text.hesc_state"), dt_util.utcnow(),
                       plan_status=c.published.get("input_text.hesc_plan_status"),
                       plugged_in=c.data.ev_connected if c.data is not None else None)

    @property
    def native_value(self) -> str | None:
        # 3.1.0: a phone widget shows this line as it is, so it comes in Home Assistant's language
        return texts.translate(self._calc()[0], self.hass.config.language if self.hass else None)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._calc()[1]
