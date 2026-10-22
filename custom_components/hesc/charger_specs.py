"""What a charger needs before it starts in its solar mode (since rc3).

Sources: official manufacturer documentation, ElaadNL/NAL and evcc documentation, plus a rule
from practice for the Wallbox.

The number of phases is not chosen by HESC or by the charger: it is the smallest of what the
house connection, the charger and the car's on-board charger can do. HESC
measures it while the car charges (current.py) or from the highest charging power it has seen.

Per brand and solar mode value:
  start_1p   surplus (W) needed to start on 1 phase
  start_3p   surplus (W) needed to start on 3 phases, summed over the phases
  per_phase  surplus (W) needed on EVERY phase on 3 phases, or None when the charger only looks
             at the total (then the spread of the sun over the phases does not stop it)
  source     where the numbers come from (shown in the advice attributes)

6 A per phase (1.38 kW / 4.14 kW) is the lowest charging current of the standard (NAL
requirement 1-9, IEC 61851-1) and the fallback for brands without own documentation.
"""

from __future__ import annotations

from dataclasses import dataclass

VOLT = 230.0
MIN_A = 6.0
STD_1P = round(MIN_A * VOLT)          # 1380 W
STD_3P = round(3 * MIN_A * VOLT)      # 4140 W


@dataclass(frozen=True)
class StartSpec:
    start_1p: float
    start_3p: float
    per_phase: float | None
    source: str

    def start(self, phases: int | None) -> float:
        """Surplus needed to start; unknown phases -> the 1-phase value (the lowest, never too high).
        On 3 phases at least the per-phase need on every phase (Wallbox Eco: 3 x 480 = 1440 W)."""
        if phases == 3:
            return max(self.start_3p, 3 * self.per_phase if self.per_phase else 0.0)
        return self.start_1p


STANDARD = StartSpec(STD_1P, STD_3P, None, "standard: 6 A per phase (NAL 1-9 / IEC 61851-1)")

# (brand, solar mode value) -> spec; brand alone (value "*") for every solar value of that brand.
SPECS: dict[tuple[str, str], StartSpec] = {
    ("Wallbox", "eco_mode"): StartSpec(
        460, 1380, 480,
        "Wallbox Eco-Smart guide: Eco 1 phase 2 A (~460 W), 3 phases 2 A per phase / 6 A total; "
        "rule from practice: at least 480 W on every phase"),
    ("Wallbox", "full_solar"): StartSpec(
        STD_1P, STD_3P, None, "Wallbox Eco-Smart guide: Full Green 6 A (1 phase) / 3x6 A (~4140 W), total L1+L2+L3"),
    ("Alfen Eve", "*"): StartSpec(1400, 4200, None, "Alfen KA-01197: Green >= 1.4 kW (1 phase) / 4.2 kW (3 phases)"),
    ("Peblar", "*"): StartSpec(STD_1P, STD_3P, None, "Peblar support: pure solar >= 6 A (1.38 kW) per phase"),
    ("myenergi Zappi", "*"): StartSpec(1400, 4200, None, "myenergi support: Eco+ 6 A, ~1.4 kW / ~4.2 kW (Min Green Level 100 %)"),
    ("Ohme", "*"): StartSpec(720, STD_3P, None, "Ohme: Solar Boost starts at 0.72 kW sun (+0.72 kW grid); 3 phases: standard 6 A"),
    ("Easee", "*"): StartSpec(STD_1P, STD_3P, STD_1P, "Easee support: at least 6 A surplus on each phase for ~10 min"),
}


def spec_for(charger_type: str | None, solar_values: str | None, active_mode: str | None = None) -> StartSpec:
    """The start spec for the configured charger type and its solar mode: the mode the charger is in
    now when that is one of the solar values (Wallbox "eco_mode, full_solar"), else the first value."""
    t = str(charger_type or "")
    vals = [x.strip() for x in str(solar_values or "").split(",") if x.strip()]
    v = active_mode if active_mode in vals else (vals[0] if vals else "")
    return SPECS.get((t, v)) or SPECS.get((t, "*")) or STANDARD


ONE_PHASE_MAX_W = 32 * VOLT  # 7.36 kW: the most a single phase carries (32 A)
PLAUSIBLE_MAX_W = 25000.0    # above this a reading is a glitch (unit error), not a charger


def phases_from_power(max_charge_w: float | None) -> int | None:
    """Phases from the highest charging power seen recently: above what one phase can carry
    (32 A ~ 7.4 kW, plus margin) it must be 3 phases. Below that it is unknown (a 1-phase 32 A
    charger, or 3 phases at a low current): then None and the advice keeps the lowest floor."""
    if max_charge_w is not None and ONE_PHASE_MAX_W * 1.05 < max_charge_w <= PLAUSIBLE_MAX_W:
        return 3
    return None
