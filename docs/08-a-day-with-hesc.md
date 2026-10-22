# 08 · A day with HESC

*Nederlands: [08-a-day-with-hesc.nl.md](08-a-day-with-hesc.nl.md)*

**In short**
- One ordinary spring day in an invented house, from plugging in the car to a full car the next
  morning.
- In the morning the home batteries take the sun; a kickstart gives the car its turn.
- During the day the car charges on sun; the charger decides when it starts and pauses.
- At night the charge plan adds the rest in the cheapest quarters, in time for the morning.

This day is an example: the house, the times and the numbers are made up, but every step is what
HESC really does.

## The house

- **Solar panels** of about 5 kWp. Solcast expects **18 kWh** today.
- **Home batteries** of 10 kWh in total, at 30 % in the morning, run by their own battery control.
- **A Wallbox** on three phases, in *Eco* (charging on sun).
- **A car** with a 60 kWh battery, at **40 %** when it is plugged in.
- **A charge plan:** 80 % by 07:30 tomorrow morning.
- **Dynamic energy prices**, per quarter.
- Settings: start threshold **1,500 W**, keep-charging threshold **1,100 W**.

## 07:45 · Plugged in

The car is plugged in at 40 %. HESC works out what is needed: 40 % → 80 % is about 24 kWh.

On *Main* you see the plan for today:
- **Expected solar charging opportunities:** green bars from about 10:30 to 15:30. Green means: enough sun for
  the charger to start. Orange means: enough to keep charging, not to start. The two thresholds
  are shown above the chart.
- **Expected solar charging:** today about 5 hours of charging on sun.
- **Live:** *EV battery level 40 % · full at 80 %*, *Solar still to come today 18 kWh*.

The charge plan already reserves a few cheap quarters tonight, but leaves room for the sun that
is still to come.

## 08:30 – 10:00 · The home batteries eat first

The sun comes up. The home batteries are at 30 % and take every watt that is left over. Nothing
goes to the grid, so the Wallbox sees no surplus and waits.

On the *Live* card: *Grid 0 W*, *Home batteries 1800 W · 42 %*. HESC watches and waits.

## 10:15 · Kickstart

The cautious forecast is now 2,300 W, above the start threshold. The home batteries have been
charging steadily for a while. And there is enough sun left today for both: about 14 kWh to come,
the home batteries still need about 6 kWh.

So HESC gives the car a **kickstart**. Under *Current state*, *Home battery and EV* shows:
1. *Kickstart: charger started* — the charger starts for a moment.
2. The battery control sees that the car is charging and stops charging the home batteries.
3. *Kickstart: charger paused* — HESC pauses the charger again.
4. *Kickstart: waiting for the charger to start on sun* — the charger is back in *Eco*. Now the
   spare sun goes to the grid, and the Wallbox sees it.

## 10:20 – 10:35 · Enough sun, but not on every phase

There is 2.0 kW spare in total. A Wallbox on *Eco* needs about 1.4 kW on three phases, but also
**at least about 480 W on every phase**. Phase 3 has only 350 W, so the Wallbox waits.

At 10:35 the sun is higher, all three phases are above 480 W, and the Wallbox starts by itself.
The car charges on sun.

If your meter shows power per phase, HESC counts how often this happens. You see it on the
*Settings* page in the line *Phases*: first *measuring*, after some weeks *provisional*, and in the
sunniest period of the year *confirmed*. Every charger has its own start level; see
[05 · Chargers and sources](05-chargers-and-sources.md#how-much-sun-a-charger-needs-to-start).

## 12:00 · A cheap quarter, but enough sun

At noon the price drops to almost nothing. A cheap chance — but the sun is expected to cover what
the car still needs today. *Status* shows:

> *Cheap chance skipped: enough sun today (…)*

The car keeps charging on sun.

**If you have HPVC** and it limits your panels at this moment (sending power back earns nothing),
the Wallbox would see no surplus. Then HESC asks HPVC to let the sun through for the car, as long
as the forecast is above the start threshold. HPVC decides; HESC waits for its answer and gives
the panels back as soon as the car stops or the sun drops below the keep-charging threshold.

## 14:30 – 16:00 · Clouds

Clouds come and go. The Wallbox pauses when the sun is too low and starts again by itself when it
comes back. HESC does not interfere: the charger decides on its own sun.

On *Main*, *Solar forecast vs actual · EV* shows the orange line (real solar power) dipping under
the purple area (the forecast), and the cyan line (the car) going on and off with it.

## 16:15 · A planned quarter, and the current goes down

The charge plan has picked 16:15 – 16:30: the price is low there. The car charges from the grid.
There is still about 2.5 kW of sun.

Because this Wallbox lets HESC set the charging current, HESC lowers it to 6 A per phase. The car
then takes about 4.1 kW, and more than half of it comes from the sun instead of the grid. HESC only
does this while the car is still full in time. After the quarter the current goes back to what it
was.

## 17:15 · The sun is gone

The Wallbox stops; the car has taken about 10 kWh of sun today and is at **58 %**. The home
batteries are full.

The charge plan works out the rest: 58 % → 80 % is about 13 kWh. It picks the cheapest quarters of
the night.

## 02:00 – 03:15 · The rest from the grid

Between 02:00 and 03:15, the cheapest quarters of the night, the plan charges from the grid. At
03:15 the car is at **80 %**, more than four hours before the ready-by time. *Status* shows
*Goal reached (80%)*.

## The day in numbers

| | |
|---|---|
| Solar forecast (Solcast) | 18 kWh |
| Solar power made | about 19 kWh |
| To the home batteries | about 7 kWh (30 % → full) |
| To the car from the sun | about 10.5 kWh |
| To the car from the grid | about 13.5 kWh |
| Car | 40 % → 80 % (about 24 kWh) |
| Share of sun in the car | about 44 % |
| Grid cost for the car | about € 2.80 (13.5 kWh at about € 0.21 all-in) |

## What to take from this

- **Everyone does their own job.** The battery control runs the home batteries, the charger
  decides when it starts on sun, HPVC decides about the panels. HESC watches, asks and plans.
- **The kickstart is what gets the car going in the morning.** Without it, the car would wait
  until the home batteries were full.
- **Not every watt counts the same.** On three phases a charger like the Wallbox on *Eco* needs sun
  on every phase. That is the charger's own rule; the phase advice shows how often it holds you
  back.
- **The charge plan only fills in what the sun leaves.** It takes the cheapest quarters and makes
  sure the car is full in time.

More about the logic behind this: [04 · How it works](04-how-it-works.md) and
[07 · Smart charging explained](07-smart-charging-explained.md). What every card on the dashboard
shows: [06 · Dashboard](06-dashboard.md).
