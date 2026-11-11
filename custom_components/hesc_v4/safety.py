"""Hard rule (decision 30-10-2026 21:54: "HARD NOOIT"): HESC never writes installer or house settings.

HESC only sets the normal charging current (never above the maximum the charger reports) and the
charger's own mode/switch controls chosen in the setup screen. Settings that belong to the installer
or the house connection are never written, whatever the logic or a setup choice asks:
Wallbox "Power Boost" / ICP max current, go-e absolute maximum (ama), Easee circuit/charger maximum,
Zaptec installation maximum, Zappi supply grid limit, fuse/breaker/main-connection values.
Background: desk study of charging power and charger limits (30-10-2026).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Final

# Entity ids that hold an installer or house-connection setting (all languages HESC ships).
_INSTALLER: Final = re.compile(
    r"(icp_max|_icp\b|power_boost|powerboost|absolute_max|_ama\b|max_charger_limit|charger_max_current"
    r"|circuit|installation|installer|grid_limit|supply_limit|main_fuse|fuse|breaker"
    r"|hoofdzekering|zekering|aansluitwaarde|installateur|hauptsicherung|sicherung)",
    re.IGNORECASE,
)


def is_installer_setting(entity_id: str) -> bool:
    """True for an entity id that holds an installer or house setting HESC must never write."""
    return bool(_INSTALLER.search(entity_id or ""))


def allowed_targets(domain: str, entity_ids: Iterable[str], current_entities: Iterable[str]) -> tuple[list[str], list[str]]:
    """Split a command's targets into (allowed, refused).

    Refused: every installer/house setting, and every `number` that is not a chosen charging-current
    control or one of HESC's own numbers (a charger number HESC was not set up to change)."""
    current = {e for e in current_entities if e}
    ok: list[str] = []
    refused: list[str] = []
    for eid in entity_ids:
        if is_installer_setting(eid):
            refused.append(eid)
        elif domain == "number" and eid not in current and not eid.startswith("number.hesc_v4_"):
            refused.append(eid)
        else:
            ok.append(eid)
    return ok, refused
