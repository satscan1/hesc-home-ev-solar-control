"""What the first start finds by itself (decisions 30-10-2026 nr 37 and 01-11-2026 10:17-10:42).

The same searches as the first-start sketch on the proefbord (opmaakchat, `suFind`): the charger brand via
its integration, the solar power and grid power now, the solar forecast, the price sources and the number
of phases of the grid meter. Only reading: nothing is changed. A search returns candidates, best first;
the setup screen fills a field in only when there is exactly one (v2 rule), else it asks.
"""
from __future__ import annotations

import re
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

# charger integrations -> HESC's charger type (charger_table.py)
CHARGER_PLATFORMS = {
    "wallbox": "Wallbox", "alfen_wallbox": "Alfen Eve", "peblar": "Peblar", "myenergi": "myenergi Zappi",
    "goecharger": "go-e Charger", "goecharger_api2": "go-e Charger", "go_echarger": "go-e Charger",
    "wattpilot": "Fronius Wattpilot", "fronius_wattpilot": "Fronius Wattpilot", "smaev": "SMA EV Charger",
    "sma_ev_charger": "SMA EV Charger", "evcc_intg": "evcc (any charger)", "evcc": "evcc (any charger)",
    "ohme": "Ohme", "easee": "Easee",
}
# price integrations -> HESC's price source (plan_settings "price_source")
GRID_CLOCK = "Grid Clock"
LIST_IN_SENSOR = "Price list in sensor"
PRICE_ACTIONS = {"energyzero": "EnergyZero / ANWB Energie", "anwb_energie": "EnergyZero / ANWB Energie",
                 "easyenergy": "EasyEnergy", "tibber": "Tibber"}
# 11-11-2026: integrations with a price list in one sensor (prices.py reads them as "Price list in sensor"):
# platform -> (name shown, attributes that hold the list)
LIST_PLATFORMS = {
    "epex_spot": ("EPEX Spot", ("data",)),
    "pvpc_hourly_pricing": ("PVPC (ESIOS)", ("price_00h",)),
    "omie": ("OMIE", ("today_hours",)),
    "energidataservice": ("Energi Data Service", ("raw_today",)),
    "amber_electric": ("Amber Electric", ("forecasts",)),
    "zonneplan_one": ("Zonneplan", ("forecast",)),
}
_GRID_CLOCK = re.compile(r"^sensor\.grid_clock_(.+)_prices$")
_SKIP = re.compile(r"hesc_v3|hesc_v4|^sensor\.hesc_")
_PV = re.compile(r"pv|solar|zon|omvormer|inverter", re.I)
_NOT_PV = re.compile(r"forecast|verwacht|predict|solcast"
                     # 08-11 (decision 09:27): not a battery, the house, the grid or a car ("HPVC Total HBC Charging
                     # Power" stood on top: "hpvc" contains "pv")
                     r"|hbc|charging|charge|battery|batter|accu|akku|consum|verbruik|load|house|huis|grid|export|import"
                     r"|wallbox|\bev\b|_ev_|car\b|auto\b"
                     # 10-11 (more plug and play): control figures of HPVC and the like are no solar power
                     r"|error|_mae|_rms|limit|setpoint|diag", re.I)
_GRID_PLATFORMS = re.compile(r"dsmr|homewizard|p1_monitor|slimmelezer")
_GRID = re.compile(r"grid|\bnet\b|p1|netvermogen|power_consumption|active_power", re.I)
_NOT_GRID = re.compile(r"pv|solar|zon|car|ev_|wallbox|charger|laad", re.I)
_PHASE = re.compile(r"^(sensor\..*?(?:phase|fase)_?l?)([123])$")
_NOT_NET = re.compile(r"(production|consumption|levering|teruglevering|returned|delivered|export|import)")


def _sensors(hass: HomeAssistant) -> list[tuple[str, Any, er.RegistryEntry | None, str]]:
    """(entity id, state, registry entry, "id name device") of every sensor that is not HESC's own."""
    reg, devs = er.async_get(hass), dr.async_get(hass)
    out = []
    for st in hass.states.async_all("sensor"):
        if _SKIP.search(st.entity_id):
            continue
        ent = reg.async_get(st.entity_id)
        dev = devs.async_get(ent.device_id) if ent and ent.device_id else None
        txt = " ".join(str(x) for x in (st.entity_id, st.attributes.get("friendly_name"),
                                         dev and (dev.name_by_user or dev.name)) if x)
        out.append((st.entity_id, st, ent, txt))
    return out


def _power(st: Any) -> bool:
    return st.attributes.get("device_class") == "power" or str(st.attributes.get("unit_of_measurement") or "") in ("W", "kW")


def _charger_entity(ent: er.RegistryEntry | None) -> bool:
    """A sensor of a charger integration is never the house's solar or grid meter."""
    return bool(ent and ent.platform in CHARGER_PLATFORMS)


def pv_candidates(hass: HomeAssistant) -> list[str]:
    """Solar power now: a power sensor named pv/solar/zon/inverter that is not a forecast; "total" first."""
    found = [(2 if re.search(r"total|totaal|som", t, re.I) else 0, e) for e, st, ent, t in _sensors(hass)
             if _power(st) and _PV.search(t) and not _NOT_PV.search(t) and not _charger_entity(ent)]
    return [e for _s, e in sorted(found, key=lambda x: (-x[0], x[1]))]


_METER_PLATFORMS = ("dsmr", "dsmr_reader", "homewizard", "p1_monitor", "slimmelezer")
_DERIVED = re.compile(r"max|piek|peak|(?<![a-z0-9])1_?m(?:in)?(?![a-z])|gemiddeld|average|avg|mean|minimum", re.I)
_SOCKET = re.compile(r"socket|stekker|plug|kwh.?meter|hwe-skt|hwe-kwh", re.I)
_INVERTER = re.compile(r"inverter|omvormer|wechselrichter", re.I)
_EXPORT = re.compile(r"production|productie|teruglever|returned|export|injection", re.I)
_IMPORT = re.compile(r"consumption|verbruik|afname|import|delivered|geleverd", re.I)


def _meter(hass: HomeAssistant, ent: er.RegistryEntry | None) -> bool:
    """A sensor of the smart meter (decision 02-11 11:10 nr 8): DSMR, DSMR Reader, P1 monitor,
    SlimmeLezer, HomeWizard only its P1 meter (not an Energy Socket or kWh meter)."""
    if ent is None:
        return False
    plat = ent.platform
    dev = dr.async_get(hass).async_get(ent.device_id) if ent.device_id else None
    dev_txt = " ".join(str(x) for x in (dev and dev.model, dev and dev.name, dev and dev.name_by_user) if x)
    if plat == "esphome":  # a SlimmeLezer runs ESPHome
        return bool(re.search(r"slimme ?lezer|p1", dev_txt, re.I))
    if plat not in _METER_PLATFORMS:
        return False
    if plat == "homewizard":
        return bool(re.search(r"p1", dev_txt or ent.entity_id, re.I)) and not _SOCKET.search(dev_txt)
    return True


def grid_choices(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Grid power now, best first (decision 02-11 11:10 nr 8). Only the smart meter's power sensors
    (no plugs/sockets, nothing unavailable, nothing derived such as max/peak/1m/average, no inverter, no
    phase sensor). One sensor with + and - (import positive) comes first. When the meter only has a
    separate import and export sensor: one choice "import + export" ({"entity_id": import,
    "export_entity_id": export}); HESC then computes import - export itself.
    When no smart meter sensor is found at all: sensors named grid/net/p1 (as before), with the same
    exclusions, so a meter read via MQTT or a template still turns up."""
    signed, imp, exp, named = [], [], [], []
    for e, st, ent, t in _sensors(hass):
        if not _power(st) or st.state in ("unavailable", "unknown") or _PHASE.match(e) or _charger_entity(ent):
            continue
        if _DERIVED.search(e) or _SOCKET.search(t) or _INVERTER.search(t):
            continue
        if _meter(hass, ent):
            (exp if _EXPORT.search(e) else imp if _IMPORT.search(e) else signed).append(e)
        elif _GRID.search(t) and not _NOT_GRID.search(t) and not _EXPORT.search(e) and not _IMPORT.search(e):
            named.append(e)
    out: list[dict[str, Any]] = [{"entity_id": e} for e in sorted(signed)]
    if not signed and imp and exp:
        out.append({"entity_id": sorted(imp)[0], "export_entity_id": sorted(exp)[0]})
    if not out:
        out = [{"entity_id": e} for e in sorted(named, key=lambda x: (not re.search(r"p1|grid|net", x), x))]
    for i, c in enumerate(out):
        c["recommended"] = i == 0
    return out


def grid_candidates(hass: HomeAssistant) -> list[str]:
    """The entity ids of grid_choices (an "import + export" choice by its import sensor)."""
    return [c["entity_id"] for c in grid_choices(hass)]


def meter_phases(hass: HomeAssistant) -> str | None:
    """Decision 01-11 10:42 nr 2: power per phase L1/L2/L3 on the grid meter -> "3"; only L1 -> "1"."""
    groups: dict[str, set[int]] = {}
    for st in hass.states.async_all("sensor"):
        m = _PHASE.match(st.entity_id)
        if m and not _NOT_NET.search(st.entity_id) and _power(st):
            groups.setdefault(m.group(1), set()).add(int(m.group(2)))
    if any(g == {1, 2, 3} for g in groups.values()):
        return "3"
    if groups and all(g == {1} for g in groups.values()):
        return "1"
    return None


def chargers_found(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Charger types whose integration is in this Home Assistant, per type the number of chargers
    (devices) and their names: [{"brand", "count", "devices"}] (opmaakchat 02-11, nr 6)."""
    reg, devs = er.async_get(hass), dr.async_get(hass)
    devices: dict[str, str] = {}
    for ent in reg.entities.values():
        brand = CHARGER_PLATFORMS.get(ent.platform)
        if brand and not ent.disabled_by:
            devices.setdefault(ent.device_id or ent.platform, brand)
    out: dict[str, dict[str, Any]] = {}
    for dev_id, brand in devices.items():
        dev = devs.async_get(dev_id)
        item = out.setdefault(brand, {"brand": brand, "count": 0, "devices": [], "device_ids": []})
        item["count"] += 1
        item["devices"].append((dev and (dev.name_by_user or dev.name)) or brand)
        item["device_ids"].append(dev_id)  # 07-11: for `hesc_v4/setup/charger` {device}
    return list(out.values())


def charger_brands(hass: HomeAssistant) -> list[str]:
    """Charger types found, one per charger device."""
    return [c["brand"] for c in chargers_found(hass) for _ in range(c["count"])]


def action_source_sensor(hass: HomeAssistant, source: str) -> str | None:
    """A sensor of the integration behind an action-only price source (EnergyZero, EasyEnergy, Tibber,
    Nord Pool official). HESC needs one: the price fetch finds the integration's config entry through it
    (v2: "price sensor"). The price of now first. None when the integration is not there."""
    platforms = [p for p, src in {**PRICE_ACTIONS, "nordpool": "Nord Pool (official)"}.items() if src == source]
    reg = er.async_get(hass)
    found = [e.entity_id for e in reg.entities.values()
             if e.platform in platforms and e.domain == "sensor" and not e.disabled_by and hass.states.get(e.entity_id)]
    found.sort(key=lambda x: (not re.search(r"current_hour_price|current_price|price_now|current_electricity", x), x))
    return found[0] if found else None


def price_sources(hass: HomeAssistant) -> list[dict[str, Any]]:
    """The price sources found: {"source", "sensor" (or None), "zone", "now"}; Grid Clock first."""
    reg = er.async_get(hass)
    out: list[dict[str, Any]] = []
    for st in sorted(hass.states.async_all("sensor"), key=lambda s: s.entity_id):
        m = _GRID_CLOCK.match(st.entity_id)
        if m:
            cur = hass.states.get(f"sensor.grid_clock_{m.group(1)}_current_price")
            out.append({"source": GRID_CLOCK, "sensor": st.entity_id,
                        "zone": str(st.attributes.get("zone") or m.group(1)).upper(), "now": cur.state if cur else None})
    seen = set()
    for ent in sorted(reg.entities.values(), key=lambda e: e.entity_id):
        if ent.disabled_by or ent.domain not in ("sensor", "event"):
            continue
        if ent.domain == "event":  # Octopus Energy keeps its rates in an event entity per day
            if ent.platform == "octopus_energy" and ent.entity_id.endswith("_current_day_rates") and "Octopus Energy" not in seen \
                    and ent.entity_id.startswith("event.octopus_energy_electricity_"):
                seen.add("Octopus Energy")
                out.append({"source": LIST_IN_SENSOR, "label": "Octopus Energy", "sensor": ent.entity_id, "zone": None, "now": None})
            continue
        if ent.platform in PRICE_ACTIONS and PRICE_ACTIONS[ent.platform] not in seen:
            src = PRICE_ACTIONS[ent.platform]
            seen.add(src)
            # fix 06-11-2026: the sensor is needed, else the price fetch has no config entry (no prices)
            sensor = action_source_sensor(hass, src)
            st = hass.states.get(sensor) if sensor else None
            out.append({"source": src, "sensor": sensor, "zone": None, "now": st.state if st else None})
        elif ent.platform in LIST_PLATFORMS:
            # 11-11-2026: price sources per country - integrations that give a price list in one sensor
            st = hass.states.get(ent.entity_id)
            attrs = st.attributes if st else {}
            label, keys = LIST_PLATFORMS[ent.platform]
            if label not in seen and any(k in attrs for k in keys):
                seen.add(label)
                out.append({"source": LIST_IN_SENSOR, "label": label, "sensor": ent.entity_id,
                            "zone": attrs.get("market_area") or attrs.get("area"), "now": st.state if st else None})
        elif ent.platform in ("nordpool", "entsoe"):
            st = hass.states.get(ent.entity_id)
            attrs = st.attributes if st else {}
            if any(k in attrs for k in ("raw_today", "prices_today", "prices")):
                # 10-11-2026: show the integration's own name, not "Prijslijst in een sensor" (unclear for a Nord Pool user)
                out.append({"source": LIST_IN_SENSOR, "label": "Nord Pool (HACS)" if ent.platform == "nordpool" else "ENTSO-e",
                            "sensor": ent.entity_id, "zone": attrs.get("region") or attrs.get("area"),
                            "now": st.state if st else None})
            elif ent.platform == "nordpool" and "Nord Pool (official)" not in seen:
                seen.add("Nord Pool (official)")
                sensor = action_source_sensor(hass, "Nord Pool (official)")
                out.append({"source": "Nord Pool (official)", "sensor": sensor, "zone": None, "now": None})
    return out


def forecast_found(values: dict[str, Any], hass: HomeAssistant, now_key: str) -> bool:
    eid = str(values.get(now_key) or "")
    return bool(eid) and hass.states.get(eid) is not None


_CAPACITY = re.compile(r"capacit|capaciteit|kapazit|battery_size|battery_kwh|accu_?grootte|akkugr", re.I)
_NOT_CAPACITY = re.compile(r"charged|geladen|added|consum|verbruik|energy_today|session|remaining|resterend", re.I)


def car_capacity(hass: HomeAssistant, soc_entity: str | None) -> float | None:
    """The battery capacity the car's own integration reports (decision 01-11-2026 11:50: no model
    table, "heb je integratie in HA dan lezen we die eerst uit"): a kWh sensor named capacity on the same
    device as the car's battery-level sensor. None when there is none; then the user fills it in."""
    reg = er.async_get(hass)
    ent = reg.async_get(str(soc_entity or "")) if soc_entity else None
    if ent is None or not ent.device_id:
        return None
    for other in er.async_entries_for_device(reg, ent.device_id):
        if other.domain != "sensor" or other.disabled_by:
            continue
        st = hass.states.get(other.entity_id)
        if st is None:
            continue
        unit = str(st.attributes.get("unit_of_measurement") or "")
        txt = f"{other.entity_id} {other.original_name or ''} {st.attributes.get('friendly_name') or ''}"
        if unit not in ("kWh", "Wh") or not _CAPACITY.search(txt) or _NOT_CAPACITY.search(txt):
            continue
        if st.attributes.get("state_class") == "total_increasing":
            continue
        try:
            kwh = float(st.state) / (1000 if unit == "Wh" else 1)
        except ValueError:
            continue
        if 10 <= kwh <= 150:
            return round(kwh, 1)
    return None
