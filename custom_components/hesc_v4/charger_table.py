"""Charger table, ported unchanged from HESC v2.0.0 (hesc_config.yaml, charger brand table).

Each entry gives the suggestions the setup screen offers for one brand:
  values     comma separated mode values that mean "solar/eco mode"
  nc         comma separated states of the connected-sensor that mean "no car"
  mode/conn/power/switch/startstop/resume  regular expressions to find the entities
  tested     whether the brand was tested with v2

Since rc3 (manufacturer documentation and the
Dutch translations shipped with Home Assistant 2026.10.1): Home Assistant in Dutch creates Dutch
entity ids, so the Wallbox and Peblar patterns also match the Dutch names (e.g.
`number.<charger>_maximale_laadstroom`); Wallbox "Locked" means no car; Peblar start/stop and
charging current; evcc 0.316+ calls its solar mode "smart" (old name "pv" kept).
Since 3.0.0 (German release): the German names from HA 2026.10.1's de.json for Wallbox, Peblar
and Ohme as well (e.g. `select.<charger>_pv_aufladung`, `number.<charger>_maximaler_ladestrom`).
"""

from __future__ import annotations

from typing import Final

CHARGER_TABLE: Final[dict[str, dict[str, str | bool]]] = {
    "Wallbox": {
        "values": "eco_mode, full_solar",
        "nc": "Ready, Disconnected, Locked",
        "mode": "^select\\..*(_solar_charging|_pv_aufladung)$",
        "conn": "(_status_description|_statusbeschrijving|_statusbeschreibung)$",
        "power": "(_charging_power|_laadvermogen|_ladeleistung)$",
        "switch": "",
        "startstop": "^switch\\.",
        "resume": "^button\\..*(_resume_schedule|_zeitplan_fortsetzen)$",
        "current": "^number\\..*(_maximum_charging_current|_maximale_laadstroom|_maximaler_ladestrom)$",
        "tested": True,
        "note": "Official Wallbox integration. Tested with a Pulsar Plus."
    },
    "Alfen Eve": {
        "values": "Green",
        "nc": "Available",
        "mode": "^select\\..*_solar_charging_mode$",
        "conn": "_status_code_socket_1$",
        "power": "_active_power_total_socket_1$",
        "switch": "",
        "tested": False,
        "note": "Needs a meter on the Alfen load balancing."
    },
    "Peblar": {
        "values": "pure_solar",
        "nc": "no_ev_connected",
        "mode": "^select\\..*(_smart_charging|_slim_laden|_intelligentes_laden)$",
        "conn": "(_state|_status|_zustand)$",
        "power": "_power$",
        "switch": "",
        "startstop": "^switch\\..*(_charge|_opladen|_aufladung)$",
        "current": "^number\\..*(_charge_limit|_laadlimiet|_ladestrombegrenzung)$",
        "tested": False,
        "note": ""
    },
    "myenergi Zappi": {
        "values": "Eco+",
        "nc": "EV Disconnected",
        "mode": "^select\\.myenergi_.*_charge_mode$",
        "conn": "_plug_status$",
        "power": "",
        "switch": "",
        "tested": False,
        "note": "Charging power: pick the Zappi internal-load CT power sensor yourself."
    },
    "go-e Charger": {
        "values": "4",
        "nc": "",
        "mode": "^select\\.goe_.*_lmo$",
        "conn": "_car_0$",
        "power": "_nrg_11$",
        "switch": "_fup$",
        "tested": False,
        "note": "Needs grid/PV data (go-e Controller or pushed from Home Assistant)."
    },
    "Fronius Wattpilot": {
        "values": "Eco",
        "nc": "no car",
        "mode": "^select\\..*_charging_mode$",
        "conn": "_car_connected$",
        "power": "_charging_power$",
        "switch": "_pv_surplus$",
        "tested": False,
        "note": "Uses the Fronius meter."
    },
    "SMA EV Charger": {
        "values": "optimized_charging",
        "nc": "not_connected",
        "mode": "^select\\..*_operating_mode_of_charge_session$",
        "conn": "_charging_session_status$",
        "power": "_charging_station_power$",
        "switch": "",
        "tested": False,
        "note": "Via Sunny Home Manager."
    },
    "evcc (any charger)": {
        "values": "pv, smart",
        "nc": "",
        "mode": "^select\\.evcc_.*_mode$",
        "conn": "_connected$",
        "power": "_chargepower$",
        "switch": "",
        "tested": False,
        "note": "Read the evcc loadpoint, not the charger itself."
    },
    "Ohme": {
        "values": "on",
        "nc": "unplugged",
        "mode": "^switch\\..*(_solar_boost|_pv_boost)$",
        "conn": "_status$",
        "power": "_power$",
        "switch": "",
        "tested": False,
        "note": "Only partly: Home Pro with its own clamp."
    },
    "Easee": {
        "values": "on",
        "nc": "disconnected",
        "mode": "",
        "conn": "_status$",
        "power": "_power$",
        "switch": "",
        "tested": False,
        "note": "Only with an Easee Equalizer; pick its surplus-charging switch as mode entity yourself."
    }
}
