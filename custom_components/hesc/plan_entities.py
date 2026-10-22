"""Shared base for the charge plan setting entities (plan_settings.py)."""
from __future__ import annotations

from homeassistant.const import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity

from .coordinator import HescCoordinator
from .entity import HescEntity
from .plan_settings import Setting


class PlanSettingEntity(HescEntity, RestoreEntity):
    """One own charge plan setting. Restored after a restart, like v2's helpers."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: HescCoordinator, spec: Setting) -> None:
        super().__init__(coordinator, spec.key)
        self._spec = spec

    def _store(self, value: object) -> None:
        self.coordinator.set_plan_setting(self._spec.key, value)
