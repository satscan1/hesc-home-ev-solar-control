"""Switch between HESC v3 and v4 without losing anything (decision 11-11-2026, RC1).

HACS installs v4 next to v3 (other domain, other folder), so both could run and both could steer the
charger. Only one may be active:
* after "take over from v3" v4 pauses v3 (its config entry disabled by the user; nothing removed);
* `hesc_v4/setup/back_to_v3` (Expert) turns v3 on again and pauses v4. In HACS the user then picks a
  v3.x version if v3's files are gone.
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntryDisabler
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PREV_DOMAIN = "hesc"  # HESC v3


async def async_pause_v3(hass: HomeAssistant) -> int:
    """Pause every active v3 entry. Returns how many were paused."""
    n = 0
    for e in hass.config_entries.async_entries(PREV_DOMAIN):
        if e.disabled_by is None:
            await hass.config_entries.async_set_disabled_by(e.entry_id, ConfigEntryDisabler.USER)
            n += 1
    return n


async def async_back_to_v3(hass: HomeAssistant) -> dict[str, Any]:
    """Turn v3 on again and pause v4. Without a v3 entry nothing changes (v4 keeps running)."""
    v3 = hass.config_entries.async_entries(PREV_DOMAIN)
    if not v3:
        return {"v3": False}
    for e in v3:
        if e.disabled_by is not None:
            await hass.config_entries.async_set_disabled_by(e.entry_id, None)
    for e in hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(hass.config_entries.async_set_disabled_by(e.entry_id, ConfigEntryDisabler.USER))
    return {"v3": True}


def async_setup_websocket(hass: HomeAssistant) -> None:
    @websocket_api.require_admin
    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/setup/back_to_v3"})
    @websocket_api.async_response
    async def ws_back_to_v3(hass: HomeAssistant, connection: Any, msg: dict[str, Any]) -> None:
        connection.send_result(msg["id"], await async_back_to_v3(hass))

    websocket_api.async_register_command(hass, ws_back_to_v3)
