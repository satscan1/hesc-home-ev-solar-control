"""Shared base for the charge plan setting entities (plan_settings.py)."""
from __future__ import annotations

from homeassistant.const import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity

from . import model
from .coordinator import HescCoordinator
from .entity import HescEntity
from .plan_settings import Setting


class PlanSettingEntity(HescEntity, RestoreEntity):
    """One own charge plan setting. Restored after a restart, like v2's helpers."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator, spec: Setting, ev: str = model.EV1) -> None:
        super().__init__(coordinator, spec.key, ev)
        self._spec = spec
        if spec.extra.get("control"):  # v4: a control for every day (on the phone), not a setting
            self._attr_entity_category = None

    def _store(self, value: object) -> None:
        with self._car():
            self.coordinator.set_plan_setting(self._spec.key, value)

    def _restored(self, value: object) -> None:
        """The value after a restart, into this car's plan settings."""
        with self._car():
            self.coordinator.plan[self._spec.key] = value
