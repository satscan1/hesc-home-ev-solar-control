# 03 · Settings

*Nederlands: [03-settings.nl.md](03-settings.nl.md)*

**In short**
- **What HESC reads** (charger, car, solar power, forecast, HPVC) is set in the setup screen:
  *Settings → Devices & services → HESC v3 → Configure*.
- **How HESC behaves** (thresholds, charge plan, costs, notifications) is set on the *Settings*
  page of the HESC dashboard, and the plans themselves on the *Charge plan* page.
- The defaults work for most homes. Change something only when the advice or the report points
  to it.
- Blocks that are fine stay closed. A block that misses something opens by itself.

## Two places

| Where | What you set there |
|---|---|
| **Setup screen** (*Configure*) | Charger type and its entities, solar power and grid power, solar forecast, car (connected, charging power, battery level), HPVC or standalone, grid power per phase. See [01 · Installation](01-installation.md#2-add-hesc-and-fill-in-the-setup-screen). |
| **Dashboard, *Settings* page** | Everything about how HESC behaves: thresholds, timing, advice, grid charging, prices, notifications, minimum charge, home battery, costs. |
| **Dashboard, *Charge plan* page** | When the car must be ready and how full, holiday mode, cheap chances. |
| **Dashboard, *Main* page** | *Enable HESC* and *Shadow mode (evaluate only)*. |

On the *Settings* page the entities from the setup screen are shown read-only. The row *Change
sources and charger* opens the setup screen.

## The top of the Settings page

- **Setup check.** One card says *Setup verified · all OK*, or how many parts need attention.
  Per part (charger, sources, weather station, charge plan, home battery and EV) you see the
  values of now; a part that is wrong shows what is missing. Parts you do not use are on one
  line, *Not used*.
- **Advice.** The start threshold your own history points to, the threshold of now, how many
  sessions it is based on, and the switch *Apply advice automatically*. The line **Phases**
  shows the phase advice. How the advice works: [04 · How it works](04-how-it-works.md#start-threshold-and-advice).
- **Your settings.** Your thresholds, car, timing, charge plan and advice at a glance.
- **Back up settings · Restore back-up · Standard values.** *Back up settings* saves all your
  HESC settings in `/config/hesc_v3/` (plus a copy with date and time). *Restore back-up* puts
  them back; the button shows which back-up it will use. *Standard values* first makes a
  back-up and then resets only the tuning (thresholds, timing, advice, final check); sensors,
  goals, prices and costs stay as they are.

## 1 · Your charger — required

*Charger type* and **Search again** (looks up the charger's entities again). The charger fields
stay closed while the check is green; *Charger fields* shows them. See
[05 · Chargers and sources](05-chargers-and-sources.md#your-charger).

## 2 · Sources

| Switch | Meaning |
|---|---|
| *Use HPVC* | On when you use Home PV Control; off (the default) when you do not. Without HPVC, HESC skips the release step: nothing is limited, so the charger starts on sun by itself. A new install switches this on by itself only when it finds HPVC. |
| *PV & grid from HPVC* | On = HESC uses HPVC's solar power and grid power sensors. Off = your own sensors from the setup screen. |
| *Change sources* | Shows the solar power, grid power, forecast and HPVC fields. They also open by themselves when something is missing. |

## Optional

Shown with *Show optional fields*.

| Field | When you need it |
|---|---|
| *Status values meaning "no car"* | Only when *EV connected* is a status sensor. |
| *Extra solar switch* | Chargers that need an extra switch for charging on sun (go-e, Wattpilot). |
| *Solar energy counter* | The charger's counter of energy from the sun, for the report. |
| *EV battery level* + *EV counts as full at* | The car's battery level and the level that counts as full (default 80 %; 100 % for LFP batteries). Used for "car is full", the charge plan and cheap chances. |

**Local weather station.** *Use* switches it on or off; *Settings* shows the irradiance sensor and
its start and hold thresholds (default 220 / 160 W/m²). Without a weather station HESC works on
the forecast alone.

## 3 · Advanced — only if needed

Each block has its own switch to show it.

| Block | Settings | Defaults |
|---|---|---|
| *Charging thresholds* | *Start threshold per season*, *Forecast power to start* / *to hold*, *EV counts as charging above* | off · 2 000 / 1 500 W · 400 W |
| *Timing* | stable before release, wait for charger, allowed solar dip, charger stopped before restore, maximum release duration, cooldown, failed releases per day | 5, 10, 5, 5, 240, 30 min · 3 |
| *Advice* | advice based on last, minimum sessions before advice | 30 days · 8 sessions |
| *Plan and notifications* | start/stop switch **or** "charge now" mode value, *Back to solar mode*, price source, price sensor, prices per, currency, solar forecast today / tomorrow, final check, phones for notifications, morning summary | no grid charging · *Price list in sensor* · *Automatic* · *Automatic* · 60 min · off |

**Grid charging.** Fill in **one** of the first two: a start/stop switch (switched on in a planned
quarter), or the mode value that means "charge now". *Back to solar mode* (optional, with a
start/stop switch) is a button or script that puts the charger back in charging on sun after
grid charging, for example Wallbox *Resume schedule*. With charger type *Wallbox* HESC fills
these in itself when it finds exactly one. Nothing filled in = no grid charging.

**Prices.** See [05 · Chargers and sources](05-chargers-and-sources.md#energy-prices).

**Notifications.** *Add or remove a phone* lists every device with the Home Assistant app; ✓ =
gets notifications. *Send a test notification* tries it. *Morning summary every day* sends one
message a day (battery level, next plan, sun today, yesterday).

## Minimum charge

*Use* + *Settings*. When the car is plugged in below the *Minimum battery level* (default 20 %),
HESC charges it to that level within *Reach it within* (default 3 h), in the cheapest quarters
of that window. Handy when you come home almost empty and may need the car again soon.

## Home battery and EV

*Use* + *Settings*, only with a home battery. Fill in the level sensor(s) and power sensor(s) of
your home batteries (several, comma separated; a positive power means charging), their total
size, the maximum number of kickstarts per day and the minimum sun that must be left for the
car. Needs the start/stop switch and *Back to solar mode* from the block *Plan and notifications*. How it
works: [04 · How it works](04-how-it-works.md#home-battery-and-ev-kickstart); linking your home
battery control to HESC: [04 · Link your home battery control](04-how-it-works.md#link-your-home-battery-control-to-hesc).

## Charging costs

*Use* shows the *Costs* button on *Main* and the Costs page; *Settings* shows the fields. HESC
counts the costs whether the page is shown or not.

| Field | Meaning | Default |
|---|---|---|
| *Value of a solar kWh* | the feed-in compensation you miss by charging the car; 0 = free | 0 |
| *Price from the price source is already all-in* | the price already includes tax, supplier mark-up and VAT | off |
| *Mark-up per kWh* | energy tax and supplier, only when not all-in | 0 |
| *VAT over price + mark-up* | in %, only when not all-in | 0 |

Changing these recalculates the whole history.

## Charge plan page

| Setting | Meaning |
|---|---|
| *Charging plan · one fixed day per week* | Day, time, goal, *Active*. Comes back every week; switch *Active* off when you only need it once. |
| *Charging plan · weekly schedule* | Days, time, goal, *Active*. |
| *Holiday mode* + *Holiday until* | The weekly plan does nothing; the one-day plan and charging on sun carry on. Switches itself off the day after *Holiday until*. |
| *Take cheap chances* + *Cheap when below* | Also charge when the price is at or below this price (per kWh, in the currency of your prices), unless the sun covers it later that day. |
| *Usable battery capacity* · *Grid charging power* | To work out how much energy is needed and how many quarters that takes (default 60 kWh · 11 kW). |

## Main page

| Switch | Meaning |
|---|---|
| *Enable HESC* | Master switch. Off = HESC does nothing. |
| *Shadow mode (evaluate only)* | On = HESC decides and shows what it would do, but switches nothing. On after installing. |
