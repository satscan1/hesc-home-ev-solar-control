# 05 · Chargers and sources

*Nederlands: [05-chargers-and-sources.nl.md](05-chargers-and-sources.nl.md)*

**In short**
- HESC never talks to your charger, car or forecast service directly. It only works through Home
  Assistant: it reads and controls the entities that the integrations of your charger, car and
  forecast create there.
- Pick your charger type in the setup screen; HESC then looks up the matching entities by itself.
- Every charger needs a certain amount of sun before it starts on sun. HESC knows this
  per brand and never advises a lower start level.
- The car's battery level, a solar forecast and energy prices let HESC plan more accurately, but are not
  required.

## Your charger

### What HESC needs from it

| What | Why | Example |
|---|---|---|
| **Is a car connected?** | Nothing to do without a car | a connected sensor, or a status such as `Ready` / `Charging` |
| **Charging power** | To see whether the car really charges | in W or kW |
| **The setting for charging on sun** | In that setting the charger starts by itself when there is enough sun | Wallbox *Eco*, Alfen *Green*, Zappi *Eco+* |
| **Start/stop** (for the charge plan) | To charge from the grid at the cheapest quarters | a pause/resume switch, or a "charge now" mode |
| **Charging current** (optional) | To fit the charging to the sun | Wallbox *Maximum charging current* |

A paused charger counts as 0 W, whatever power it still reports: some chargers (the Wallbox
for one) keep showing their last power for minutes after a pause. Paused means: the start/stop
switch is off, or the charger's status says *paused*.

### Charger types

Choose the type in the setup screen (step **Charger**) or later on the *Settings* page. HESC then
looks up your charger's entities in Home Assistant and fills them in. For every brand HESC knows
which setting of the charger means "charge on sun" (on a Wallbox for example *Eco*) and which
status means that no car is connected.

- If HESC finds exactly one matching entity, it fills it in. If it finds more, it leaves the
  field empty and you choose.
- HESC never overwrites what you filled in yourself.
- The search also works when your Home Assistant uses names in another language (German or
  Dutch).

| Charger | Setting for charging on sun | Note |
|---|---|---|
| **Wallbox** (Pulsar Plus, Copper) | `eco_mode`, `full_solar` | tested in practice |
| **Alfen Eve** | `Green` | needs a meter on the Alfen load balancing |
| **Peblar** | `pure_solar` | |
| **myenergi Zappi** | `Eco+` | pick the Zappi internal-load power sensor yourself |
| **go-e Charger** | `4` (Eco) | needs grid/PV data (go-e Controller or sent from Home Assistant) |
| **Fronius Wattpilot** | `Eco` | uses the Fronius meter |
| **SMA EV Charger** | `optimized_charging` | via Sunny Home Manager |
| **Ohme** | `on` (Solar Boost) | only partly: Home Pro with its own clamp |
| **Easee** | `on` | only with an Easee Equalizer; pick its surplus-charging switch yourself |
| **evcc** (any charger) | `pv`, `smart` | choose the entities of the evcc loadpoint, not those of the charger itself |
| **Other (manual)** | your choice | fill in the fields yourself |

Chargers without a setting of their own for charging on sun (for example Zaptec, Tesla Wall Connector or plain
OCPP) can be used through evcc.

Only the Wallbox has been tested in practice. With another charger: keep shadow mode on for a few
sunny days, check that the *Live* card shows all values, and that the charger returns to its
charging on sun after a grid charge.

**One planner per charger.** Switch off charging schedules in the charger's own app or in other
integrations while HESC plans the charging.

### How much sun a charger needs to start

A charger that charges on sun starts only when there is enough surplus. The standard minimum for
every charger is 6 A per phase: about **1.4 kW on one phase** and **4.1 kW on three phases**.
Some brands start lower:

| Charger · mode | 1 phase | 3 phases |
|---|---|---|
| Wallbox · Eco | ± 460 W | ± 1.4 kW, at least 480 W on **every** phase |
| Wallbox · Full Green | 1.4 kW | 4.1 kW |
| Alfen · Green | 1.4 kW | 4.2 kW |
| Zappi · Eco+ | 1.4 kW | 4.2 kW |
| Ohme · Solar Boost | 0.72 kW (+ 0.72 kW from the grid) | 4.1 kW |
| Easee | 1.4 kW | 4.1 kW, 6 A on **every** phase |
| Other brands | 1.4 kW | 4.1 kW (standard) |

HESC uses this as a floor: the start threshold advice never goes below what your charger needs.

### One phase or three?

You do not set this, and HESC does not choose it. The number of phases is the smallest of what
your house connection, your charger and your car can do. A car with a single-phase charger
always charges on one phase, also on a three-phase charger. HESC measures it while the car
charges.

**Phase advice.** If your grid meter shows power per phase (most smart meters do), HESC counts how
the sun is spread over the phases. On chargers that need sun on every phase (Wallbox Eco,
Easee), one weak phase can keep the charger from starting. The advice on the *Settings* page
goes through three stages:
1. **measuring** — not enough sunny days yet;
2. **provisional** — after about two weeks;
3. **confirmed** — after enough days in the sunniest period of the year at your location.

It is information only; HESC changes nothing by itself.

### Charging current

If your charger lets HESC set the charging current (Wallbox: *Maximum charging current*), HESC
lowers the current while the charge plan charges from the grid, so that more of the energy comes
from the sun — as long as the car is still full in time. Afterwards the current goes back to what
it was. This is normal behaviour; there is no switch for it. If you did not fill in a charging
current, HESC never changes the current.

## Your car's battery level

Not required, but the charge plan and "car is full" work much more accurately with it. Any battery-level
sensor in % works, usually from the integration of your car brand. No sensor yet? The setup
screen tells you where to find one for your car.

**Regular updates work best.** A value that is refreshed every few minutes gives the best
planning. Many car integrations update less often to spare the car's 12 V battery; that is fine.

**Where HESC gets the battery level.** HESC takes the first of these sources that has a value. If
the first one drops out, it moves on to the next:
1. the battery-level sensor you chose;
2. a second battery sensor of the same car, if HESC finds one;
3. the last known level of this charging session, plus what was charged since;
4. the usual level at plug-in over the last 14 days.

The dashboard shows which source is used.

**Known behaviour:** some car integrations send a wrong value for a short while right after a
Home Assistant restart (for example 99.9 %), until their next update. HESC then thinks for a few
minutes that the car is full and may postpone charging. With the next correct value everything is
recalculated; nothing stays wrong.

## Solar forecast

| What you have | What HESC does |
|---|---|
| **Solcast** | Best choice. HESC uses the cautious estimate to decide and the normal estimate to compare with what really happens. Tip: in Solcast add `attr_brk_halfhourly` under *Attribute breakdown* for 30-minute blocks. |
| **Open-Meteo Solar Forecast** or **Forecast.Solar** | Works the same way; HESC converts it by itself. |
| **No forecast** | HESC charges on measured solar power and plans grid charging as if no sun comes (never late). The kickstart is off. A notice under *Settings → Repairs* explains how to add a forecast. |

**Weather station (optional).** A local irradiance sensor (W/m²) or lux meter can be used as an
extra check. Switch on *Use local weather station* in the setup screen. Start with low thresholds;
after a few weeks the report shows how well it matches your solar power.

## Energy prices

Only needed for the charge plan, cheap chances and the Costs page, and only useful with a
**dynamic** contract (a price per quarter or hour). Set the price source on *Settings → Advanced → Plan and notifications*.

| Price source | Sources |
|---|---|
| *Price list in sensor* | Nord Pool (HACS), ENTSO-E, Energi Data Service, EPEX Spot, Frank Energie, Zonneplan, Octopus Energy (Agile), Amber Electric, PVPC (Spain) |
| *EnergyZero / ANWB Energie*, *EasyEnergy*, *Tibber*, *Nord Pool (official)* | pick any sensor of that integration; HESC fetches the prices itself every 30 minutes |

- HESC always plans in quarters; hourly and half-hourly prices are split into quarters.
- Currencies: EUR, SEK, DKK, NOK, GBP and AUD. *Automatic* takes the currency from the price
  sensor.
- Public holidays for the price forecast come from the **Workday** integration of your country.
- Grid tariffs that change during the day are not modelled; use *all-in* prices from your source
  if you have them.

## Home battery (optional)

For the kickstart, HESC reads the level (%) and power (W) of your home batteries and their total
size. A positive power means the battery is charging. See the *Settings* page, *Home battery and
EV*.
