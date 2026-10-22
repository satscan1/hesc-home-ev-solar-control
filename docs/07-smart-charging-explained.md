# 07 · Smart charging explained

*Nederlands: [07-smart-charging-explained.nl.md](07-smart-charging-explained.nl.md)*

**In short**
- Plug the car in when you get home, and make sure your plan matches when you leave. HESC does
  the rest.
- HESC uses free sun first, then the cheapest quarters from the grid, and always keeps a safety
  net so the car is ready on time.
- After about two weeks HESC knows your prices well enough to look ahead.
- The same text is built into the dashboard: the *Guide* badge on *Main* (hold it for Dutch).

## The short version

After about two weeks HESC runs almost on its own. Your part is small:

1. **Plug the car in** when you get home.
2. **Make sure your plan matches when you leave.** A weekly plan for your usual days (for example
   *80 % on weekdays at 07:30*), and the *one fixed day per week* plan for one extra day (*100 % on
   Saturdays at 09:00*).

Between the moment you plug in and the moment you leave, HESC looks for the cheapest way to get
the car where you want it.

## Why the first two weeks matter

Most things work from the first day: charging on sun, the charge plan, the safety net and the
goal check.

One thing gets better with time: **looking ahead at prices.** Prices for tomorrow are published
around 13:00. Before that, nobody knows them. HESC fills that gap with an expected price, based
on what prices did in your own last 14 days and on how sunny tomorrow will be (sunny days are
usually cheap around midday and expensive in the evening).

- **The first day:** no expected prices yet. HESC plans with the prices that are known. The
  safety net still gets the car ready.
- **After one full day:** a rough expectation, simply yesterday's pattern. Expected prices appear
  as grey bars in the price chart and the plan can use them.
- **From day 3:** the average of all full days so far.
- **From day 14:** two full weeks of your own prices.
- **Every week after that:** HESC refines how sun and price relate on your market.

A known price always wins over an expected one, unless the expected one is clearly cheaper
(2 cents per kWh or more). As soon as the real prices arrive, the plan uses those.

## The order HESC follows

Every 30 seconds HESC looks at the car, the sun, the prices and your plan, and asks the same
questions in the same order:

| # | Question | What happens |
|---|---|---|
| 1 | **Is there sun?** | Your charger charges on sun in its own setting for it (for example Eco), as it always did. With HPVC, HESC first asks HPVC to let the sun through. HESC counts the sun in the plan, so it does not buy energy the sun will deliver anyway. |
| 2 | **Is it one of the planned cheapest quarters?** | HESC starts the charger from the grid for that quarter. |
| 3 | **Is time running out?** | **Safety net:** when the time left is only just enough to reach the goal, HESC starts charging, whatever the price. |
| 4 | **Is it the last hour before you leave and is the car still short?** | **Final check:** HESC charges to your goal, whatever the price. |
| 5 | **Is the price very low right now?** | **Cheap chance:** HESC charges now, even without a plan, *unless* enough sun is expected later today. |
| 6 | **Is the car below the minimum you set?** | **Minimum charge** (optional, off by default): the car gets at least that level within a few hours, in the cheapest quarters. |
| 7 | Nothing of the above | HESC waits. The dashboard tells you why, for example *Waiting for the next planned quarter*. |

A few rules apply to all of these:

- **3 % margin.** HESC only charges from the grid when the car is more than 3 % below the goal.
  A car at 78 % with a goal of 80 % is left alone; at 76.9 % it charges.
- **Which goal?** With an active plan: the goal of that plan. Without one: *EV counts as full at*
  (default 80 %). A cheap chance never fills a car that already counts as full.
- **HESC only undoes what it started.** If you start charging yourself, or the car is already
  charging on sun, HESC leaves it alone.
- **After grid charging the charger is not left on.** Otherwise the car could quietly top itself
  up from the grid in the evening peak. With *Back to solar mode* filled in (Wallbox: *Resume
  schedule*, filled in for you), HESC pauses the charger, checks that the pause really took effect
  (cloud chargers react about a minute late), and then puts it back to charging on sun. Without
  that field the charger stays paused until there is enough sun, the car drops more than 3 % below
  the goal, a plan starts, or you unplug.

## How the plan picks the cheapest hours

Say you plug in at 18:00 with the car at 40 %, and your weekly plan says *80 % at 07:30*.

1. **How much is needed?** 40 % of a 60 kWh battery = 24 kWh.
2. **How much comes from the sun before 07:30?** None, it is night. (On a Saturday plan for
   14:00 the morning sun would count.)
3. **How long does that take from the grid?** At 11 kW: a bit over 2 hours, so 9 quarters.
4. **Which 9 quarters?** The cheapest ones between now and 07:30. Usually somewhere in the night.

The planned quarters show in **amber** in the price chart on the *Charge plan* tab. When the plan
is not active, the chart shows what it *would* do, marked *preview*.

## Cheap chances and the sun

*Take cheap chances* charges whenever the price drops below *Cheap when below*, even without a
plan. These moments show in **blue-green** in the price chart.

A cheap moment in the morning is no bargain when the afternoon sun would have filled the car for
free. So HESC first looks at the solar forecast for the rest of the day. If the sun is expected to
cover what the car still needs, with 20 % to spare, the cheap chance is skipped: *Cheap chance
skipped: enough sun today*.

## How much sun your charger needs

A charger that charges on sun only starts when there is enough sun to spare. That amount differs
per brand: from about 0.5 kW on one phase (Wallbox Eco) to about 4 kW on three phases (the
standard minimum of 6 A per phase). HESC knows this per brand, and the start threshold advice
never goes below what your charger needs. The table is in [05 · Chargers and
sources](05-chargers-and-sources.md#how-much-sun-a-charger-needs-to-start).

**Grid charging and the sun at the same time.** If your charger lets HESC set the charging
current (Wallbox: *Maximum charging current*, which needs an admin account), HESC turns the
charger down while it charges from the grid and the sun is shining. More of the charge then comes
from your panels and less from the grid. This is normal; there is nothing to switch on. HESC only
does it while the car will still be full on time, and afterwards it puts the current back.
Whether your charger uses 1 or 3 phases, HESC works out by itself.

**Phase advice.** Some chargers only start when every phase has enough sun to spare (a Wallbox on
Eco about 480 W per phase, an Easee 6 A per phase). If your panels are spread unevenly over the
phases, the weakest phase then decides when your car can charge on sun. With the grid power per
phase filled in, HESC measures this on sunny days and tells you what it saw: first the spread over
the phases, later how often the weakest phase held your charger back. It is advice only; HESC
changes nothing.

## Without a solar forecast

HESC also works without a forecast. It then charges on the solar power it measures, and the plan
counts no sun at all, so the car is never late. The kickstart is off, because it needs to know how
much sun is still to come. See [05 · Chargers and sources](05-chargers-and-sources.md#solar-forecast).

## Home battery and EV

*Optional, off by default. Only for homes with a home battery.*

On a sunny morning the home battery usually takes all the spare sun first. The charger then sees
no surplus and waits, sometimes until the home battery is full in the afternoon. On a day with
less sun the car may get nothing.

With **Home battery and EV** switched on, HESC helps the car get its turn:

1. **Kickstart.** The car is plugged in and waiting for sun, the home battery has been charging for
   a few minutes, and the cautious forecast says there is enough sun now. HESC checks the rest of
   the day: is there clearly more sun left than the home battery still needs (with 20 % to spare,
   and at least *Minimum sun left for the EV*)? Then:
   1. HESC starts the charger;
   2. your home battery control sees the car charging and stops filling the home battery;
   3. HESC pauses the charger and waits until the pause has really taken effect;
   4. HESC puts the charger back to charging on sun, which now gets the sun that came free.
2. **Back to the home battery.** Later in the day, when the sun left is only just enough to fill
   the home battery, HESC puts the charger back to waiting, so the home battery is full by the
   evening. There is no new kickstart that day after that.

During the short start the home battery may deliver a little power to the car. That is expected.

HESC never controls the home battery itself. It does nothing while a charge plan is charging,
during an HPVC release or after sunset, and at most a few times a day (*Kickstarts per day*,
default 3, at least 30 minutes apart).

What you fill in (*Settings*, *Home battery and EV* → *Settings*): the level sensor(s) of your
home battery, its power sensor(s) (positive = charging) and its total size in kWh. It also needs
the charger's start/stop switch and *Back to solar mode*; for a Wallbox both are filled in for
you.

## What will it cost?

The **Expected charge cost** badge on *Main* shows what the active plan is expected to cost from
the grid: the price of each planned quarter, plus your mark-up and VAT (or the all-in price). It
only counts grid charging that will really happen; without an active plan, with the car at its
goal, or while the car charges on sun, it shows 0.00.

**What did it cost?** Tap the **Costs** badge. Per day, week, month, quarter or year you see how
much went into the car, how much came from the sun (green) and the grid (grey), and what the grid
part cost. Set your mark-up, VAT and the value of a solar kWh once under *Settings → Charging
costs*; the whole history follows. **Export to spreadsheet (CSV)** writes two files for Excel.

## Situations

### "I drive to work every weekday"

Make a **weekly plan**: tick the days, set the time you leave and the level you want. Leave it
active. Plug in when you get home. That is all.

### "I'm going on a trip on Saturday"

Use **one fixed day per week**: pick *Saturday*, the time you leave and for example 100 %, and
switch it on. When both plans are active, the earliest one wins; your weekly plan simply
continues. Only need it once? Switch *Active* off after the trip.

### "The car stays at home for a few days"

No plan needed. The car charges on sun, takes cheap chances, and otherwise the charger stays
paused. Only when the car drops more than 3 % below *EV counts as full at* does HESC top it up.

### "I came home with an almost empty battery and might need the car tonight"

Switch on **Minimum charge** (*Settings*, *Use*). Default: at least 20 % within 3 hours, in the
cheapest quarters of those 3 hours, or straight away if no prices are known.

### "I have a home battery and the car never gets any sun"

Switch on **Home battery and EV** and fill in your home battery. See [Home battery and
EV](#home-battery-and-ev) above.

### "I need the car now, forget the plan"

Start charging yourself (app, charger button or the charger's own setting). HESC sees the car is
already charging and leaves it alone.

### "I plugged in late; is there still time?"

HESC checks this all the time. If the time left is only just enough, the safety net starts
charging straight away. Is the goal still missed? Then you get a notification at the time you
wanted to leave: *EV goal missed*, with the level it reached.

### "Tomorrow is going to be sunny"

The plan counts the sun in advance (cautious forecast, minus a little for the house), so it buys
less from the grid. Cheap chances the sun makes unnecessary are skipped.

### "Tomorrow's prices aren't known yet"

Normal before about 13:00. After the first days the plan uses expected prices (grey bars) and
firms up when the real prices arrive.

### "My car stops at 80 % by itself"

Many cars have their own charge limit. If it is lower than your goal, the charger stops by itself
and HESC shows *Finished, charger stopped by itself*. Set your goal at or below the car's limit,
or raise the limit in the car.

### "The charger did not respond"

Cloud chargers sometimes ignore a command. HESC checks and tries again: a refused start or resume
after 5 minutes, a refused pause after 30 minutes, each at most 3 times.

### "Home Assistant restarted during charging"

HESC keeps using the last valid plan for up to 10 minutes, so a running charge does not stop.
Right after a restart some cards are empty for about a minute, and the car's battery level can be
wrong for a few minutes. See [09 · Troubleshooting](09-troubleshooting.md#after-a-home-assistant-restart).

### "I'm on holiday"

Switch on **Holiday mode** under the weekly plan. The weekly plan rests; your one-day plan stays
active, so the car can be full on the day you come back. Charging on sun carries on. Set
**Holiday until** if you like: the day after that date, holiday mode switches itself off.

## What you set once

| Setting | Where | Default | Tip |
|---|---|---|---|
| *Usable battery capacity* | *Charge plan* | 60 kWh | What your car can really use |
| *Grid charging power* | *Charge plan* | 11 kW | A little below what your charger really delivers gives some margin |
| *Take cheap chances* / *Cheap when below* | *Charge plan* | your choice / 0.05 per kWh | In the currency of your prices |
| *EV counts as full at* | *Settings*, optional fields | 80 % | The level kept without a plan |
| Final check | *Settings*, *Plan and notifications* | 60 min | How long before you leave HESC charges whatever the price |
| *Minimum charge* | *Settings* | off (20 %, 3 h) | *Use* + *Settings* |
| *Home battery and EV* | *Settings* | off (3 per day) | Only with a home battery |
| *Back to solar mode* | *Settings*, *Plan and notifications* | filled in for Wallbox | Puts the charger back to charging on sun after grid charging |
| Phones for notifications | *Settings*, *Plan and notifications* | none | Test with *Send a test notification* |
| Morning summary | *Settings*, *Plan and notifications* | off (06:00) | One message a day: battery level, next plan, sun today, yesterday |
| Charging costs | *Settings*, *Charging costs* | mark-up 0, VAT 0, solar kWh free | Or *all-in* when your price sensor has the full price |

## Where to look

- **Status** on *Main*: what HESC does now and why.
- **Price chart** (*Charge plan*): amber = planned, blue-green = cheap chance, grey = expected price.
- **Notice line** next to the logo: *✓ No notices*, or what needs attention. Tap it to go where
  you can act.
- **Expected charge cost** and **Costs** badges on *Main*.
- **Setup check** on *Settings*: when something is wrong, that part opens by itself.
- **Report** (*Generate report* under Status): everything HESC measured and decided.

See also: [04 · How it works](04-how-it-works.md) · [06 · Dashboard](06-dashboard.md) ·
[08 · A day with HESC](08-a-day-with-hesc.md)
