"""Buttons: export the charging costs as CSV; settings back-up, restore and standard values; test
notification; generate the report; take over settings and history from v2; search the
charger entities again. Since 3.0.0 also one-tap buttons for phones and watches (Android quick-settings
tiles and Wear OS can press a button but cannot start an action with data)."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import HescConfigEntry, HescCoordinator
from .entity import HescEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: HescConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities([CostsExportButton(c), *(SettingsButton(c, w) for w in ("backup", "restore", "reset")), NotifyTestButton(c), GenerateReportButton(c),
                        TakeOverButton(c), ChargerSearchButton(c),
                        *(PhoneButton(c, key, action) for key, action in PHONE_BUTTONS.items())])


# key -> the HESC action it runs (services.py); the goal of "charge now" is the charge plan's goal
PHONE_BUTTONS = {
    "charge_now_plan_goal": "charge_now",
    "charge_now_stop": "charge_now_off",
    "skip_next_day": "skip_plan_day",
    "undo_skip_day": "undo_skip_plan_day",
    "plan_off": "charge_plan_off",
}


def plan_goal(coordinator: HescCoordinator) -> int:
    """The goal of the charge plan HESC works with (one-off or weekly), on a 5 % step, 50-100."""
    import json

    raw = ((coordinator.computed.get("sensor.hesc_charge_plan") or {}).get("attributes") or {}).get("plan")
    try:
        p = json.loads(raw) if isinstance(raw, str) else (raw or {})
        g = float(p.get("goal"))
    except (TypeError, ValueError, AttributeError):
        g = float(str(coordinator.plan.get("plan_goal") or "80").rstrip("%") or 80)
    return int(min(100, max(50, round(g / 5) * 5)))


class PhoneButton(HescEntity, ButtonEntity):
    """Since 3.0.0: one tap for a phone widget, quick-settings tile or watch; runs a HESC action."""

    def __init__(self, coordinator: HescCoordinator, key: str, action: str) -> None:
        super().__init__(coordinator, key)
        self._action = action

    async def async_press(self) -> None:
        data = {"goal": plan_goal(self.coordinator)} if self._action == "charge_now" else {}
        await self.hass.services.async_call(DOMAIN, self._action, data, blocking=True)


class CostsExportButton(HescEntity, ButtonEntity):
    """Writes charging_costs_days.csv and charging_costs_months.csv to v3's own folder."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "costs_export")

    async def async_press(self) -> None:
        await self.coordinator.async_export_costs()


class SettingsButton(HescEntity, ButtonEntity):
    """v2: input_button.hesc_settings_backup / _restore / _reset, on v3's own settings."""

    def __init__(self, coordinator: HescCoordinator, which: str) -> None:
        super().__init__(coordinator, f"settings_{which}")
        self._which = which

    async def async_press(self) -> None:
        await self.coordinator.async_settings_button(self._which)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Restore shows which back-up it will use before it is pressed."""
        if self._which != "restore":
            return None
        return dict(self.coordinator.backup_meta) or {"backup_created": None}


class NotifyTestButton(HescEntity, ButtonEntity):
    """v2's input_button.hesc_notify_test. In shadow mode v3 sends no notifications (the press says so)."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "notify_test")

    async def async_press(self) -> None:
        await self.coordinator.async_notify_test()


class GenerateReportButton(HescEntity, ButtonEntity):
    """v2's input_button.hesc_generate_report: builds the report in /config/www/hesc_v3/."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "generate_report")

    async def async_press(self) -> None:
        await self.coordinator.async_generate_report()


class TakeOverButton(HescEntity, ButtonEntity):
    """Fill v3's own settings once with v2's values and take over v2's history.
    Only while shadow mode is on."""

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "take_over_v2")
        self._attr_entity_category = EntityCategory.CONFIG

    async def async_press(self) -> None:
        await self.coordinator.async_take_over_from_v2()


class ChargerSearchButton(HescEntity, ButtonEntity):
    """v2's input_button.hesc_charger_search: fill empty charger fields that have exactly one
    candidate for the chosen charger type. Filled-in fields are never changed."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator) -> None:
        super().__init__(coordinator, "charger_search")

    async def async_press(self) -> None:
        from .config_flow import apply_charger_type
        from .const import CONF_CHARGER_TYPE
        from .select import store_setup

        current = self.coordinator.settings
        charger_type = current.get(CONF_CHARGER_TYPE)
        if charger_type:
            store_setup(self.coordinator, apply_charger_type(self.hass, current, charger_type, charger_type))
