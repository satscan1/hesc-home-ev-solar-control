"""Find the car's battery-level sensor for the setup screen (new in v3, not in v2).

When the setup screen shows the EV step and no battery-level sensor
is chosen yet, HESC looks in Home Assistant for one:
1. a battery-level sensor of a car is already there -> HESC suggests it (when there is exactly
   one, it is pre-filled; with several, they are listed to choose from);
2. none found -> the step explains the ways to get one: the car brand's own Home Assistant
   integration, A Better Route Planner (ABRP, live data via Enode) with its Home Assistant
   integration, or an OBD2 plug-in module in the car.
HESC itself never talks to a car cloud, ABRP or Enode; it only reads sensors.

A candidate is a `sensor.*` with unit % that looks like a battery level (device class battery,
or "soc"/"battery"/"state of charge" in its id or name), on a device that belongs to a car:
the device's manufacturer, model or name names a car brand, a car data service (ABRP, Enode,
Smartcar) or an OBD module. Phones, tablets and home batteries are skipped.
"""

from __future__ import annotations

import re

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN

# Car brands, car data services and OBD modules, matched as whole words on the device's
# manufacturer, model and name (case insensitive). Brands that are also everyday words for
# battery devices (Smart, Mini, Ora) are left out on purpose: "Smart Lock", "mini switch".
_CAR = re.compile(
    r"\b("
    r"tesla|byd|kia|hyundai|genesis|volkswagen|vw|skoda|škoda|audi|cupra|seat|porsche|bmw|"
    r"mercedes(-benz)?|polestar|volvo|renault|dacia|alpine|nissan|peugeot|citro[eë]n|opel|"
    r"vauxhall|ds automobiles|fiat|jeep|ford|toyota|lexus|mazda|honda|subaru|mg|saic|xpeng|nio|"
    r"zeekr|lynk|jaguar|land rover|rivian|lucid|leapmotor|lotus|aiways|gwm|"
    r"abrp|a better route planner|iternio|enode|evlink(ha)?|smartcar|obd|obd2|obd-ii|elm327"
    r")\b",
    re.IGNORECASE,
)
# Battery-like devices that are not a car, even when made by a car brand.
_NOT_CAR = re.compile(r"powerwall|wall connector|gateway|home battery|thuisbatterij|hausspeicher|heimspeicher|phone|tablet", re.IGNORECASE)
_SOC_WORDS = re.compile(r"soc|battery|state.of.charge|elec_percent|accu|charge.level|akku|batterie|ladezustand", re.IGNORECASE)
# Integrations whose battery sensors are never the car.
_SKIP_PLATFORMS = {DOMAIN, "mobile_app"}


def _is_car_device(device: dr.DeviceEntry | None) -> bool:
    if device is None:
        return False
    text = " ".join(
        str(x) for x in (device.manufacturer, device.model, device.name_by_user, device.name) if x
    )
    return bool(_CAR.search(text)) and not _NOT_CAR.search(text)


def find_ev_soc_candidates(hass: HomeAssistant) -> list[str]:
    """Entity ids of battery-level sensors that belong to a car, sorted by entity id."""
    ent_reg = er.async_get(hass)
    dev_reg = dr.async_get(hass)
    found: list[str] = []
    for entry in ent_reg.entities.values():
        if entry.domain != "sensor" or entry.platform in _SKIP_PLATFORMS or entry.disabled_by:
            continue
        state = hass.states.get(entry.entity_id)
        if state is None or state.attributes.get("unit_of_measurement") != "%":
            continue
        name = " ".join(
            str(x) for x in (entry.entity_id, entry.original_name, state.attributes.get("friendly_name")) if x
        )
        if state.attributes.get("device_class") != "battery" and not _SOC_WORDS.search(name):
            continue
        device = dev_reg.async_get(entry.device_id) if entry.device_id else None
        if _is_car_device(device):
            found.append(entry.entity_id)
    return sorted(found)
