# 04 · How it works

*Nederlands: [04-how-it-works.nl.md](04-how-it-works.nl.md)*

**In short**
- Every 30 seconds HESC reads your sources and decides what the charger should do.
- On sun: HESC lets the charger start in its own setting for charging on sun. With HPVC, HESC
  first asks HPVC to stop limiting your solar panels for a while.
- From the grid: the charge plan picks the cheapest quarters before your ready-by time and
  counts on the sun that is still to come.
- With a home battery, a kickstart makes sure the car gets its turn on a sunny day.
- In shadow mode HESC makes all the same decisions, but switches nothing.

## Every 30 seconds

HESC reads about twenty values from Home Assistant: solar power, grid power, forecast, the
charger, the car, prices, the home battery. It works out what to do and writes the result to its
own entities (status, reason, plan). Times and day boundaries follow the time zone of Home
Assistant. Parts that need not run that often have their own pace, for example the price
forecast every 15 minutes.

**Shadow mode** (*Shadow mode (evaluate only)* on *Main*) is on after installing. HESC then
decides exactly as when it is live and shows it, but sends no command to the charger or HPVC.
**Enable HESC** off means HESC does nothing at all.

## Charging on sun

**Without HPVC (standalone).** Nothing limits your solar panels, so the charger starts on sun by
itself as soon as there is enough surplus. HESC follows every session, records how it went and
gives advice on the start threshold.

**With HPVC.** HPVC keeps your export near zero, so the charger never sees enough surplus to
start. HESC therefore asks HPVC for a release:

| Step | What happens |
|---|---|
| Idle | HESC waits until all start conditions hold for *Conditions stable before release* (5 min). |
| Release requested | HESC asks HPVC (HPVC 1.5.1 or newer). HPVC first finishes anything with a higher priority, then lets the panels produce freely. No answer within 5 minutes → HESC tries later. |
| Waiting for the car | HPVC confirmed. The charger has *Wait for charger to start* (10 min) to start. |
| Charging | The car charges on sun. |
| Release ended | The car stopped, the sun stayed below the hold threshold for longer than *Allowed solar dip*, the car was unplugged, sunset, or *Maximum release duration*. HPVC takes over again and a cooldown starts. |

Start conditions: the car is connected, not charging, not full and the charger is set to charge
on sun; HPVC is limiting; the cautious forecast (now and in 30 minutes) is at or above the start
threshold; the weather station agrees (if used); no cooldown; not too many failed releases today;
the sun is up. HESC never switches HPVC off itself; it only asks.

## Solar forecast

| What you have | How HESC uses it |
|---|---|
| **Solcast** | The cautious estimate to decide, the normal estimate to compare with what really happened. |
| **Open-Meteo** or **Forecast.Solar** | Converted by HESC to the same form; works the same way. |
| **No forecast** | HESC uses measured solar power (or the weather station) instead. The charge plan counts no sun, so it is never late. The kickstart is off. |

## Start threshold and advice

The start threshold is about the **forecast**. It decides three things:

- when HESC asks HPVC to lift the limit on your panels (only while HPVC limits them);
- when the kickstart may start;
- which half hours the charge plan counts as "sun is coming".

It does **not** decide when your charger charges on sun: in its solar mode the charger starts on
surplus by itself, whatever the threshold. The right value differs per home, so HESC works it
out from your own sessions:

- It only looks at the charging sessions on sun that **started while HPVC limited your panels**,
  of the last 30 days (up to 60 days in winter, when there are few). Only for those did the
  threshold decide anything. Starts by hand or by a schedule are left out.
- In the dark months HPVC rarely limits, so the advice often keeps collecting. That is fine: the
  threshold then matters little. Without HPVC (standalone) there is no advice; *Start threshold
  per season* is the simple choice then.
- **Advice:** the lowest start forecast from which the next 8 sessions together got at least 70 %
  of their energy from the sun. Rounded to 50 W, between 1 000 and 3 500 W. Hold = 75 % of start.
- **Never below your charger.** The advice never goes below the sun your charger needs to start
  (see [05 · Chargers and sources](05-chargers-and-sources.md#how-much-sun-a-charger-needs-to-start)).
  The advice then says so.
- **Apply advice automatically** (off by default): HESC moves the start threshold towards the
  advice by itself, in small steps: at most 200 W per step and one step per 7 days, only for a
  difference of at least 100 W and when the advice rests on enough sessions on different days.
  Every change shows as a grey notice on *Main*.
- **Start threshold per season** (off by default): every night HESC sets the start threshold for
  the month: June–July 2 500 W, April–May and August–September 2 000 W, March and October
  1 500 W, November–February 1 200 W; hold 75 %. Never below your charger's start level. It
  cannot be on together with *Apply advice automatically*.

The advice is worked out every evening and when HESC starts.

## Phase advice

Only with grid power per phase in the setup screen. While the car is not charging, HESC looks at
how much surplus each phase has. Chargers that need sun on **every** phase (Wallbox Eco, Easee)
are held back by the weakest phase. The advice goes through three stages:

1. **measuring** — fewer than 14 days with usable sun;
2. **provisional** — the spread over the phases is known;
3. **confirmed** — enough days in the sunniest period of the year seen.

The sunniest period is worked out from the height of the sun at your location, so it is right
anywhere in the world (in the southern hemisphere around December). The phase advice is
information only; HESC changes nothing by itself.

## Charge plan

The plan takes the active plan (the one-day plan or the weekly plan; the earliest wins), the goal
and the ready-by time. It works out the energy needed, subtracts the sun that is expected before
the deadline, and picks the cheapest quarters for the rest. After the day's prices it also uses
expected prices, but only waits for one when it is clearly cheaper.

**Sun in the plan.** Every half hour before the deadline with a cautious forecast high enough for
the charger to start counts as (forecast − 0.4 kW for the house) × 0.5 h, at most the grid
charging power.

| Reason on the dashboard | What happens |
|---|---|
| *Planned quarter* | Charging from the grid. |
| *Safety net: only just enough time left* | Charging, because the time left is just enough. |
| *Final check: below goal, charging to goal* | In the last hour (*Final check*) below the goal: charging, whatever the price. |
| *Cheap chance (…)* | The price is at or below *Cheap when below*: charging. |
| *Cheap chance skipped: enough sun today (…)* | The sun later today covers the need with 20 % to spare. |
| *Within 3 % of goal* | Grid charging only starts more than 3 % below the goal. |
| *Goal reached* | Charger paused or back to its previous mode. |
| *EV already charging, left alone* | HESC never takes over a charge it did not start. |

**Afterwards.** With *Back to solar mode* filled in, HESC pauses the charger after grid charging,
checks that the pause has really arrived (cloud chargers are often a minute late) and then puts
the charger back in charging on sun. Without it, the charger stays paused so the car cannot top
itself up from the grid; HESC switches it on again for sun, a new plan, or when you unplug.

**Goal check.** At the ready-by time HESC compares the battery level with the goal. More than 3 %
below: a red notice *EV goal missed* (also on your phone).

**Minimum charge** (optional): below the minimum level the car is charged to it within the set
time, in the cheapest quarters of that window.

## Charging current

If HESC may set the charging current, it lowers it while the charge plan charges from the grid:
the car then takes about what the sun gives, never below 6 A. Only while the car is still full in
time with 30 minutes to spare; otherwise full current. Afterwards the current goes back to what it
was, also after a restart. HESC measures the number of phases itself and acts only once it knows
them. At most one change per minute; nothing in shadow mode.

## Home battery and EV (kickstart)

On a sunny morning the home battery takes all the spare sun, so the charger sees no surplus and
the car waits. HESC never controls the home battery; it only starts the charger.

**Kickstart** when all of these hold: the car is plugged in, waiting to charge on sun and not
full; the home batteries have been charging above 500 W for a few minutes; the cautious forecast
is at or above the start threshold; the sun left today is clearly more than the home batteries
still need (1.2 × what they need, plus *Minimum sun left for the EV*); no charge plan and no
release busy; fewer than *Kickstarts per day* today, at least 30 minutes after the last one.

The order:
1. HESC starts the charger.
2. Your home battery control sees the car charging and stops filling the home battery.
3. HESC pauses the charger and waits until the pause has really arrived.
4. HESC puts the charger back in charging on sun. It now sees the surplus and charges on sun.

Step 4 must come while your home battery control still holds the home battery. HESC therefore
hands back 15 seconds after the charger's start/stop switch turned off (the moment Home Assistant
saw it, even when a cloud charger shows the pause late). For your home battery control there is a
sensor *Kickstart hand-back in progress*: it is on from step 3 until the charger charges on sun
again. Hold the home battery while it is on, also when the charger briefly shows 0 W.

**Back to the home battery.** When the car has charged on sun for 10 minutes or more and the sun
left today is only just enough for the home batteries, HESC pauses the charger and puts it back
to waiting for sun, so the home battery is full by the evening.

### Link your home battery control to HESC

Does your home battery control decide by itself when the car is charging (for example to stop
filling the home battery, as in step 2)? Give it these two HESC entities:

| Entity | Use it for |
|---|---|
| **EV charging power** (`sensor.hesc_v3_ev_charging_power`) | The car's charging power. Use it instead of your charger's own power sensor: it shows 0 W as soon as the charger is paused, also when the charger still reports its last power for minutes (Wallbox). |
| **Kickstart hand-back in progress** (`binary_sensor.hesc_v3_kickstart_hand_back_in_progress`) | Hold the home battery while it is on. |

Both work with every charger whose start/stop or pause switch HESC knows, or whose status says it
is paused. They are only as quick as your charger reports: a cloud charger can be a minute or more
behind, and HESC updates every 30 seconds. Only a separate kWh meter in the charger's group is
truly instant.

With a home battery you can leave the charger paused in its solar mode; HESC starts it with a
kickstart when enough sun is left. **Without a home battery there is no kickstart:** then do not
leave the charger paused, or the car never charges on sun.

## Car battery level

All parts of HESC use one battery level. HESC takes the first of these that has a value:
1. the battery-level sensor from the setup screen;
2. a second battery-level sensor of the same car, which HESC finds by itself;
3. the last level of this charging session, plus 90 % of the kWh charged since;
4. the usual level at plug-in over the last 14 days (from 5 plug-ins).

An estimated or unknown level gives an orange notice. No sensor at all? The setup screen helps
you find one for your car.

## Prices, costs and notifications

- **Prices:** all parts read one price list per quarter; see
  [05 · Chargers and sources](05-chargers-and-sources.md#energy-prices). The **price forecast**
  learns your market from your own price history and fills the quarters after the last known
  price.
- **Costs:** while the car charges, the part that comes from the grid is priced at the price of
  that quarter; the rest counts as sun (also energy from a home battery).
- **Notifications:** P1 (red, also on your phone): the goal was missed or a real fault. P2
  (orange, also on your phone): a sensor is missing, HESC keeps working. P3 (grey, *Main* only):
  just so you know.

## History and report

HESC writes one line per event and session to its history in `/config/hesc_v3/`, about 50 lines
on a sunny day. **Generate report** (on *Main*, under *Status*) turns it into a page with your
sessions, the advice and how reliable your sources are.
