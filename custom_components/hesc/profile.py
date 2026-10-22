"""Charger profile: suggestions for the charger entities, ported from v2.0.0.

Same search as the v2 template sensor `sensor.hesc_charger_profile` (hesc_config.yaml):
1. mode entity: entities whose `options` contain one of the brand's solar values;
   if none, entities whose id matches the brand's mode pattern (first 5);
2. only when exactly one mode entity is found, look on its device for
   power (sensor, device_class power), connected (binary_sensor with device_class plug,
   else the brand's pattern, else a status-like sensor), solar switch, start/stop and resume.
Like v2, a field is only filled in when exactly one candidate was found.

Since rc3 (tested against real charger integrations): a solar value such as "on" (Ohme,
Easee) or "4" (go-e) also appears in other select/switch entities in the house, so several mode
candidates are found and none is suggested. When the brand has a mode pattern, only the candidates
that also match it are kept (if any do). Likewise for power: a charger with several power sensors
(Alfen, go-e, Zappi, evcc) keeps only those that match the brand's power pattern.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .charger_table import CHARGER_TABLE


@dataclass
class ChargerProfile:
    """What v2's charger profile sensor reports for one charger type."""

    type: str
    known: bool
    values: str = ""
    not_connected: str = ""
    tested: bool = False
    note: str = ""
    mode: list[str] = field(default_factory=list)
    connected: list[str] = field(default_factory=list)
    power: list[str] = field(default_factory=list)
    switch: list[str] = field(default_factory=list)
    startstop: list[str] = field(default_factory=list)
    resume: list[str] = field(default_factory=list)
    current: list[str] = field(default_factory=list)  # charging current (number), 16-10

    def single(self, key: str) -> str | None:
        """The candidate for a field, only when there is exactly one (v2 rule)."""
        found: list[str] = getattr(self, key)
        return found[0] if len(found) == 1 else None


def _attr_is(hass: HomeAssistant, entity_id: str, name: str, value: Any) -> bool:
    s = hass.states.get(entity_id)
    return s is not None and s.attributes.get(name) == value


def charger_profile(hass: HomeAssistant, charger_type: str) -> ChargerProfile:
    """Run the v2 charger search for `charger_type` on the current states."""
    p = CHARGER_TABLE.get(charger_type)
    if p is None:
        return ChargerProfile(type=charger_type, known=False)

    values = [v.strip() for v in str(p["values"]).split(",")]
    # Jinja's `states` iterates in the state machine's own order (insertion order).
    states = hass.states.async_all()
    modes: list[str] = []
    for s in states:
        opts = s.attributes.get("options")
        if opts is None or isinstance(opts, str) or not hasattr(opts, "__iter__"):
            continue
        opt_str = [str(o) for o in opts]
        if any(v in opt_str for v in values):
            modes.append(s.entity_id)
    if not modes and p["mode"]:
        rx = re.compile(str(p["mode"]))
        modes = [s.entity_id for s in states if rx.match(s.entity_id)]
    elif len(modes) > 1 and p["mode"]:
        rx = re.compile(str(p["mode"]))
        def fits(s: Any) -> bool:  # no options (a switch) or its options hold one of the solar values
            opts = s.attributes.get("options")
            return opts is None or any(v in [str(o) for o in opts] for v in values)

        named = [e for e in modes if rx.match(e)] or [s.entity_id for s in states if rx.match(s.entity_id) and fits(s)]
        if named:
            modes = named
    modes = modes[:5]

    near: list[str] = []
    if len(modes) == 1:
        ent_reg = er.async_get(hass)
        entry = ent_reg.async_get(modes[0])
        if entry is not None and entry.device_id:
            near = [e.entity_id for e in er.async_entries_for_device(ent_reg, entry.device_id)]

    power = [e for e in near if e.startswith("sensor.") and _attr_is(hass, e, "device_class", "power")]
    if len(power) > 1 and p.get("power"):
        rx = re.compile(str(p["power"]))
        named = [e for e in power if rx.search(e)]
        if named:
            power = named
    conn = [e for e in near if e.startswith("binary_sensor.") and _attr_is(hass, e, "device_class", "plug")]
    if not conn and p["conn"]:
        rx = re.compile(str(p["conn"]))
        conn = [e for e in near if rx.search(e)]
    if not conn:
        status_rx = re.compile("(status|state|plug|car|connect)")
        reject_rx = re.compile("(power|energy|current|voltage)")
        conn = [
            e
            for e in near
            if e.startswith("sensor.")
            and status_rx.search(e)
            and not reject_rx.search(e)
            and not _attr_is(hass, e, "state_class", "measurement")
        ]

    def by_pattern(key: str) -> list[str]:
        pattern = p.get(key)
        if not pattern:
            return []
        rx = re.compile(str(pattern))
        return [e for e in near if rx.search(e)][:5]

    return ChargerProfile(
        type=charger_type,
        known=True,
        values=str(p["values"]),
        not_connected=str(p["nc"]),
        tested=bool(p["tested"]),
        note=str(p["note"]),
        mode=modes,
        connected=conn[:5],
        power=power[:5],
        switch=by_pattern("switch"),
        startstop=by_pattern("startstop"),
        resume=by_pattern("resume"),
        current=by_pattern("current"),
    )
