# 09 · Troubleshooting

*Nederlands: [09-troubleshooting.nl.md](09-troubleshooting.nl.md)*

**In short**
- Most messages on the dashboard are normal: HESC tells you what it is waiting for.
- Right after a Home Assistant restart some cards are empty for about a minute. That fixes
  itself.
- Something really wrong? Check the setup check on the *Settings* page and the *Live* card on
  *Main*, and press **Generate report**.

## After a Home Assistant restart

| What you see | What it means |
|---|---|
| The *Status* card or other cards are empty, or show an error for a moment | Normal. HESC fills the dashboard about a minute after the start. |
| The battery level of the car is wrong for a few minutes (for example 99.9 %) | Some car integrations send a wrong value until their next update. HESC recalculates as soon as the right value comes in. See [05 · Chargers and sources](05-chargers-and-sources.md#your-cars-battery-level). |
| A field in the setup screen is empty | The integration of your charger or meter was not ready yet. HESC searches again once Home Assistant has started. Still empty? Fill it in under *Settings → Devices & services → HESC v3 → Configure*. |
| The setup check on *Settings* shows a red ❌ | Wait a few minutes. Still red after 15 minutes? Then something is really missing; the check tells you what. |

## Installation and dashboard

| Problem | Check |
|---|---|
| Buttons between the dashboard pages do nothing | The dashboard URL must be exactly `hesc-v3`. See [01 · Installation](01-installation.md#3-add-the-dashboard). |
| Charts, the *Expected solar charging* bar or the Costs tiles are missing, or a card says *Custom element doesn't exist: hesc-…* | HESC's own cards load with the integration: restart Home Assistant after installing or updating HESC, then refresh the browser (on a phone: close and reopen the app). No cards from HACS are needed. |
| HESC icons are missing | Refresh the browser (on a phone: close and reopen the app). |
| HESC does not find my charger | Choose the charger type again on *Settings* and press **Search again**. Not in the list? Choose *Other (manual)* and fill in the fields yourself. |

## Charging on sun

| Message | What it means |
|---|---|
| `Waiting for inputs: …` | The source named is empty or unavailable. Check it on the *Live* card and in the setup screen. |
| `HPVC is not limiting PV — nothing to release` | Normal: HPVC is not limiting your solar panels, so the charger can already use the sun. |
| `Waiting for HPVC to confirm the release (x/5 min, …)` | Normal for a short while: HPVC first finishes something with a higher priority. |
| `HPVC has no external release interface (needs HPVC 1.5.1 or newer)` | Update HPVC. |
| `EV already full, no release needed` | The car is at *EV counts as full at*. |
| `Charger not in solar mode` | The charger is not in its setting for charging on sun (for example Eco), or the extra solar switch is off. |
| `Forecast too low` | The cautious forecast is below the start threshold. |
| `Cooldown until …` | A release ended a moment ago; HESC waits before it tries again. |
| `Maximum release attempts reached today` | Too many releases failed today. Starts again at midnight. |
| The phase advice stays on *measuring* | Normal for the first weeks: it needs enough sunny days. It needs the grid power per phase in the setup screen. |

**The charger does not start although HESC asks, or starts when it shouldn't.** Check whether a
charging schedule is set in the charger's own app or in another integration, and switch it off.
After an update of the charger app or firmware a schedule can appear by itself.

## Charge plan

| Message | What it means |
|---|---|
| `Grid charging not set up …` | Fill in the start/stop switch or the "charge now" mode value on *Settings → Advanced → Plan and notifications*. |
| `No active plan` | Switch on the *one fixed day per week* plan or the weekly schedule. Without a plan HESC only charges on sun and for cheap chances. |
| `Waiting for the next planned quarter` | Normal. The planned quarters are shown in the price chart. |
| `Final check: below goal, charging to goal` | Normal in the last hour before the ready-by time when the car is still below its goal. HESC charges to the goal whatever the price. |
| `EV already charging, left alone` | The car was already charging (for example on sun). HESC does not take it over. |
| `Finished, charger stopped by itself` | The charger drew no power for a few minutes (car full or its own limit). |
| `Cheap chance skipped: enough sun today (…)` | Normal: the sun is expected to cover the need later today. |
| *Prices not available* | The price sensor gives no prices right now. Check *Price source* and *Price sensor* on *Settings → Advanced → Plan and notifications*, and the price integration itself. |
| Wrong currency or small unit | *Currency* → *Automatic* takes it from the price sensor; choose your currency if the sensor does not say. |
| Prices known only until tonight | Normal before the next day's prices are published (around 13:00). The plan then uses expected prices and firms up later. |
| The weekly plan does nothing | Check **Holiday mode** under the weekly plan. |
| Notification *Charger fault* | HESC tried 3 times to switch the charger back on. Check the charger and its cloud connection. |

## Home battery and EV (kickstart)

Shown on *Main* under *Current state* while the car is plugged in.

| Message | What it means |
|---|---|
| `Not set up: …` | Fill in the start/stop switch, *Back to solar mode*, and the home battery fields on *Settings → Home battery and EV*. |
| `Waiting: home batteries not taking the sun` | Normal: the home battery is not charging, so the charger already sees the surplus. |
| `Home batteries first for the rest of today` | Not enough sun left for both; the home battery gets it. |
| `Kickstart: charger started …` → `Kickstart: charger paused …` → `Kickstart: waiting for the charger …` | A kickstart in progress: the charger starts, the home battery control sees the car and stops charging the batteries, the charger goes back to waiting for sun. |
| `Charge plan has the charger` | Normal: the kickstart waits for the charge plan. |
| `Done for today (…)` | The maximum number of kickstarts was reached, or the home battery got priority. Starts again tomorrow. |

## Notices and notifications

The line next to the logo on *Main* shows *✓ No notices*, or the most important notice. Tap it to
go where you can act.

| Notice | Meaning |
|---|---|
| **P1** (red, also on your phone) | The charge goal was missed or cannot be confirmed, or a real fault. Stays for 12 hours. |
| **P2** (orange) | A sensor is missing, but HESC keeps working (for example the battery level is estimated). |
| **P3** (grey) | Just so you know. Two hours. |

**No notifications on your phone?** On *Settings*, under *Notifications to your phone*, add your
phone and send a test notification. Only P1 and P2 go to the phone.

## Costs

| Problem | Check |
|---|---|
| No *Costs* button on *Main* | Switch on the costs page on *Settings*. |
| Costs too high or too low | Check *all-in*, or the mark-up and VAT, on *Settings*. Changing them recalculates the whole history. |
| A warning about grid energy without a price | Some grid charging happened while no price was known. It is counted separately. |
