"""Charge plan choices (day, time, goal, price source ...), replacing v2's input_select helpers."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from . import charge_now
from .config_flow import CHARGER_TYPES, apply_charger_type
from .const import CHARGER_NOT_CHOSEN, CONF_CHARGER_TYPE
from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity
from .plan_entities import PlanSettingEntity
from .plan_settings import SETTINGS, Setting


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([*(PlanSelect(c, s) for s in SETTINGS if s.kind == "select"), NotifyPick(c), ChargerType(c), ChargeNow(c)])


class PlanSelect(PlanSettingEntity, SelectEntity):
    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec)
        self._attr_options = list(spec.options)
        self._attr_current_option = str(spec.default)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last is not None and last.state in self._attr_options:
            self._attr_current_option = last.state
        self.coordinator.plan[self._spec.key] = self._attr_current_option

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self._store(option)
        self.async_write_ha_state()


CHOOSE = "Choose a phone"


class NotifyPick(HescEntity, SelectEntity):
    """v2's input_select.hesc_notify_pick and its two automations: the list shows the phones
    (✓ = chosen); picking one adds or removes it from v3's own notify services."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_current_option = CHOOSE

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "notify_pick")

    def _own(self) -> list[str]:
        return [x.strip() for x in str(self.coordinator.plan.get("notify_services") or "").split(",") if x.strip()]

    def _phones(self) -> list[dict]:
        """The phones, ✓ = in v3's own list (the list this picker changes, also in shadow mode)."""
        st = self.coordinator.computed.get("sensor.hesc_notification_phones")
        own = self._own()
        return [{**p, "chosen": p.get("service") in own} for p in (st or {}).get("attributes", {}).get("phones") or []]

    @property
    def options(self) -> list[str]:
        return [CHOOSE, *(("✓ " if p.get("chosen") else "") + str(p.get("name")) for p in self._phones())]

    async def async_select_option(self, option: str) -> None:
        if option == CHOOSE:
            return
        picked = option.replace("✓ ", "")
        phone = next((p.get("service") for p in self._phones() if p.get("name") == picked), "") or ""
        current = self._own()
        if phone == "":
            new = current
        elif phone in current:
            new = [x for x in current if x != phone]
        else:
            new = [*current, phone]
        await self.coordinator.async_set_own_text("notify_services", ", ".join(new))
        self._attr_current_option = CHOOSE
        self.async_write_ha_state()


def store_setup(coordinator: HescCoordinator, updated: dict) -> None:
    """Write changed setup choices back to the config entry (options hold the complete set
    once the options flow has run; before that, the first setup's data). No reload is needed:
    the coordinator reads the setup choices every round."""
    entry = coordinator.config_entry
    if updated == coordinator.settings:
        return
    if entry.options:
        coordinator.hass.config_entries.async_update_entry(entry, options=updated)
    else:
        coordinator.hass.config_entries.async_update_entry(entry, data=updated)


class ChargerType(HescEntity, SelectEntity):
    """v2's input_select.hesc_charger_type on the Settings page, as in
    v2. Choosing a type does what v2's hesc_apply_charger_type does, the same as the first step of
    the setup screen: brand values when the brand changes, empty charger fields with exactly one
    candidate filled in."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = [CHARGER_NOT_CHOSEN, *CHARGER_TYPES]

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "charger_type")

    @property
    def current_option(self) -> str:
        return str(self.coordinator.settings.get(CONF_CHARGER_TYPE) or CHARGER_NOT_CHOSEN)

    async def async_select_option(self, option: str) -> None:
        current = self.coordinator.settings
        store_setup(self.coordinator, apply_charger_type(self.hass, current, current.get(CONF_CHARGER_TYPE), option))
        self.async_write_ha_state()


class ChargeNow(HescEntity, RestoreEntity, SelectEntity):
    """Since 3.0.0: "Charge now to" Off / 50 % .. 100 % (charge_now.py). Ends by itself at the goal,
    when the EV is unplugged or at its give-up time (attribute `until`). Kept over a restart."""

    _attr_options = list(charge_now.OPTIONS)
    _attr_current_option = charge_now.OFF

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "charge_now")
        self._until: datetime | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.coordinator.charge_now_entity = self
        last = await self.async_get_last_state()
        until = dt_util.parse_datetime(str(last.attributes.get("until"))) if last is not None else None
        if (last is not None and last.state in self._attr_options and last.state != charge_now.OFF
                and until is not None and until > dt_util.now()):
            self._attr_current_option, self._until = last.state, until
            self.coordinator.charge_now = {"goal": int(last.state.rstrip("%")), "until": until}

    async def async_will_remove_from_hass(self) -> None:
        if self.coordinator.charge_now_entity is self:
            self.coordinator.charge_now_entity = None
        await super().async_will_remove_from_hass()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"until": self._until.isoformat() if self._until is not None else None}

    def set_from_logic(self, option: str, until: datetime | None) -> None:
        self._attr_current_option, self._until = option, until
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        if option == charge_now.OFF:
            self.coordinator.end_charge_now("switched off")
            self.coordinator.config_entry.async_create_task(self.hass, self.coordinator.async_request_refresh(), "hesc charge now")
        else:
            self.coordinator.start_charge_now(int(option.rstrip("%")))
