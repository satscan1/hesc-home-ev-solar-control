# Changelog

## 4.0.0-rc.1 · 11-11-2026

First release candidate of HESC v4, the successor of the HESC v3 series. Manual: [README.md](README.md) · Dutch: [README.nl.md](README.nl.md) · German: [README.de.md](README.de.md).

### Switching from v3, and back
- Taking over from HESC v3 uses the values v3 uses now (its helpers).
- After taking over, HESC v4 pauses HESC v3 (nothing is removed), so only one of them controls the charger.
- Expert › Notifications: "Back to v3" turns v3 on again and pauses v4.
- Expert › Notifications: "Run the first start again"; planning, costs and history are kept.

### First start
- Solar sensors listed best first with HESC's suggestion ticked; HPVC control sensors and unavailable sensors left out.
- With HPVC installed: a plain question which meter counts all your panels (HESC's own suggestion ticked).
- After the first start the home battery setup opens by itself in a pop-up.

### Step by step
- Home battery: batteries found by HESC, live values to check, size typed directly, the kickstart explained (the home battery is filled first).
- Sun and grid, Cheap chances and Notifications can be set up step by step too: one question per screen, a summary before saving.
- Home battery lists without totals, plans, house use, forecasts, air conditioners, demo sensors and capacity or health measurements.
- The tile is called Home battery (Thuisbatterij(en) in Dutch, Hausakku in German).

### Planning
- On a phone: month and rhythm as pages, a holiday in two taps, optionally open HESC on the month (per device).
- Calendar: double-tap a day for its own time and battery goal.
- No plug-in reminder when the car's level is known within the last hour and already reaches the goal.

### Prices
- Pick the country first (sets the currency), then only that country's price sources.
- New price sources: EPEX Spot, PVPC, OMIE, Energi Data Service, Octopus Energy, Amber Electric, Zonneplan and ENTSO-e; Grid Clock in every European country.
- Sources are shown when installed; missing ones of your country are named. Nord Pool (HACS) by name, own sensor with a price list last.

### Sun and phases
- Sun and grid: the yield split over the phases in percent, now (live) and the measured average; only with 3 phases.
- Expert › Advice › Phase overview: per phase whether it gets the minimum the charger needs, advice in plain words, option to show the split on Standard.
- Sun chart: filled areas and colours as in v3.
- A day forecast with half-hour rows is preferred.
- Sensor values rounded for reading (14.9 kWh instead of 14.8537 kWh).

### Back-up
- The full back-up in its own folder (/config/hesc_backup), kept when HESC is removed; an older back-up is still found.

### Languages
- Every setting name, (i) text and step-by-step screen in English, Dutch and German.

### Under the hood
- Sub devices link to the main device by its registry id (no deprecation warning in the log).

## 4.0.0-beta.1 · 08-11-2026

First beta of HESC v4, the successor of HESC v3. Manual: [README.md](README.md) · Dutch: [README.nl.md](README.nl.md) · German short version: [README.de.md](README.de.md).

### Install and first start
- HESC v4 is its own integration (`hesc_v4`) with its own panel in the sidebar; it runs next to HESC v3 without touching it.
- One question when adding the integration; with HESC v3 installed you can take over its settings and history.
- The first start asks how you charge at home: one car, two cars on one charger, or two cars each on their own charger.
- It asks about your house: connection (1 or 3 phases, amps per phase), load balancer, solar panels and dynamic prices.
- Then the charger brand and the car (name, colour, battery capacity only when the car does not report it).
- After that only what HESC did not find itself; with a Wallbox and one car about 9 taps.
- HESC starts in shadow mode: it calculates and shows what it would do, but switches nothing.

### Two cars, one or two chargers
- Two cars on one charger: HESC plans both, the first before the cable swap, the second after.
- Fixed time to move the cable per shared charger, with a reminder on your phone at that time.
- Two cars on two chargers, same brand or different.
- Sharing the grid between two cars: ready first goes first; a car never loses its running quarter.
- Sharing the sun between two cars: one car takes the sun first; the second joins when there is enough sun left over for it.
- Add a car or charger 2, and remove car 2 or charger 2: HESC first shows what goes; costs and history are kept.
- HESC on or off per car; the other car carries on.

### House connection and comfort guard
- With the house connection set and no load balancer that takes the house into account, HESC keeps house plus cars under the connection minus 10 %.
- It only lowers the normal charging current, in whole amperes, never below 6 A, and raises it again when there is room.
- This is comfort, not protection: the charger, the load balancer and the installer stay responsible.

### Planning per car
- Rhythm: a standard ready time and goal, per weekday on or off, or with its own time or goal.
- Only this time: skip the next time, or another time or goal.
- Calendar: single days off, extra days, and a vacation from a first to a last day.
- Reminder on your phone when the car is not plugged in in the evening, at a time per car.
- Charge now only after Start and a confirmation; stopping is always possible.
- The plan leads: between planned quarters the charger stays paused, also after a Home Assistant restart, and HESC says so on your phone.
- Switching the charger on by hand (in Home Assistant or in the charger's own app) is respected until the next planned quarter.

### Smarter charging
- HESC learns the charging power per car from its own grid charging sessions (can be switched off per car).
- A car without a battery-level sensor: HESC charges until the car stops by itself, or you type the battery level on your phone.
- New price source Grid Clock, next to EnergyZero/ANWB, EasyEnergy, Tibber and Nord Pool.

### Panel
- Today and tomorrow: a short letter per car and one chart with forecast, price and the charging moments per car.
- Coming week: per car the next seven days; tap a car or a day to open its planning.
- Settings in three tabs, Basic, Standard and Expert; Standard and Expert as tiles with ✓ or ⚠ that open in a pop-up.
- An (i) with one or two sentences of explanation at every setting.
- Picking a sensor from a short list with HESC's suggestion on top; home battery sensors and charger modes with tick boxes.
- Costs per car per day, week, month and year, from sun and grid, also as a CSV download.
- Report window: the charging report, and keep or share in three forms (full back-up, anonymous to share, short for a bug report).
- The panel follows the language of your Home Assistant profile: Dutch, German, and English for every other language. HESC's own status, advice and export lines follow too.

### Known limits of this beta
- Some English and German texts may still need polishing.
- The planning is not yet part of the settings back-up.
- The start-threshold advice and the phase advice still work for car 1 only.

## 3.1.1 · 25-10-2026

- The expected cost in the charge plan card shows the right amount at once. Before, it could
  show the previous amount (for example *€ 0,00*) for one update after a restart or a plan change.
- German: shorter column titles in the charge plan card (*ERW. KOSTEN*, *GÜNSTIG*), so the card
  no longer wraps.
- Manual: new pictures of the charge plan page, now in English, Dutch and German, and the plan
  card and price chart described as they are since 3.1.0.

## 3.1.0 · 25-10-2026

**Charge plan card**
- No active plan: the card only says *No charging plan active*. The old ready-by time, charging
  time, price and the word *preview* are gone, so a quick look no longer suggests the car is
  being charged.
- Active plan: the expected cost now stands next to the energy price. With cheap chances on,
  the cheap-chance price limit is shown next to it in purple (the same colour as in the chart).
  HESC shows no amount for cheap chances: a negative market price does not mean you get paid.
- A plan that is switched off (or paused by holiday mode) before its ready-by time leaves nothing
  behind: no goal check and no *EV goal missed* notification at that time any more, and the
  morning summary says *No charge plan* instead of the old time with *(off)*.

**Price chart**
- Where the sun can start charging, the sun wins over a cheap chance: those quarters are green
  only (the sun is cheaper, and it is what HESC really does).
- Expected prices (not yet published) have an almost empty area, so they read differently from
  the real prices at a glance.

**Languages**
- The HESC dashboard in the sidebar follows the language each user chose in the profile (before:
  the language of Home Assistant, which is still used when a user has not chosen one). All titles
  follow, also the price chart title.
- The texts HESC makes itself (state, reason, last action, charge plan, home battery and EV,
  charging current, notices) are shown in Dutch and German on the dashboard in that language.
  Notifications, the morning summary and the phone and watch summary come in the language of
  Home Assistant. Inside, HESC keeps working with the English texts, so your own automations
  that read them keep working.
- Still in English: the values in drop-down lists (for example *Today*, *Tomorrow*). Translating
  those would change the values your own automations use; that waits for a later version.

**README**
- A row of badges under the logo (release, HACS, stars, Ko-fi) and a *Support this project*
  section with the Ko-fi button.

## 3.0.0 · 22-10-2026

The first release of HESC as a Home Assistant integration. It can do everything HESC v2 can,
without Node-RED and without a YAML package. HESC v2 stays available; see
[Upgrading from v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.md).

**New compared with v2**
- One integration with a setup screen. HESC finds your charger, car and meter by itself, also
  when Home Assistant uses entity names in another language.
- Battery-level finder: if no battery-level sensor is found, the setup screen tells you where to
  get one for your car.
- Works with Solcast, Open-Meteo or Forecast.Solar, or without any solar forecast.
- Charging current control on chargers that allow it, so more of a grid charge comes from the sun.
- Start level per charger: the start threshold advice never goes below what your charger needs to
  start on sun.
- Phase advice when your meter shows power per phase.
- Start threshold advice only learns from solar sessions that started while HPVC limited your
  panels: only then does the threshold decide anything. No threshold advice without HPVC.
- Kickstart: start, let the home battery control see the car, pause, back to charging on sun.
- Take over settings and history from v2 with one button.
- The dashboard comes with HESC: *HESC* in the sidebar, nothing to paste, updated with every
  HESC update. HESC fills in its own entity names and your chosen Solcast and HPVC sensors, so
  renaming them keeps the dashboard working. Already pasted a dashboard at `/hesc-v3` (testers)?
  HESC leaves it alone and explains under *Settings → Repairs* how to switch.
- Plug & play: HESC brings its own dashboard cards (charts, *Expected solar charging*, Costs,
  Kiosk). No apexcharts-card, button-card, card-mod or kiosk-mode needed any more; the cards are
  in the card picker (search for *HESC*).
- Your own copy of the dashboard with one click: *Settings → Dashboards → Add dashboard →
  Community dashboards → HESC*, or two lines in the raw configuration editor.
- Kiosk page: the Home Assistant menu and top bar are hidden by HESC itself.
- In Dutch and German: the setup screen, the names of HESC's entities, the dashboard, HESC's cards
  and the guide page (*Uitleg*, *Anleitung*) follow the language of Home Assistant (the one-click
  dashboard and the cards: your own profile language). Entity ids stay the same in every language,
  so the guide and other automations keep working. The support report follows the language of Home
  Assistant too. Still in English: the messages HESC writes itself (state, reason, advice, phone
  notifications) and the values in drop-down lists.
- Switch *Use HPVC* (off by default): on when you work with HPVC.
- A paused charger counts as 0 W, also when it still reports its last power (Wallbox).
- Kickstart hands back to charging on sun 15 s after the charger's pause shows in Home Assistant,
  and a sensor *Kickstart hand-back in progress* tells your home battery control to hold the home
  battery meanwhile.
- Kickstart waits up to 6 minutes for a cloud charger to show that it started (was 4).
- On your phone and watch: actions *Set charge plan* and *Charge plan off* (for Siri, Shortcuts
  and the Apple Watch) and a one-line *Summary for phone and watch* sensor for a widget.
- *Charge now to* a goal (select and action): grid charging at once, back to solar at the goal.
- *Skip one day* of the weekly plan (a day off) without changing the plan (date and action).
- Lock-screen widgets on the iPhone follow at once: HESC sends a silent refresh to the phones in its
  phone list when the summary changes, at most once every 20 minutes.
- One-tap buttons for phones and watches (also Android quick-settings tiles and Wear OS): charge
  now to the plan goal, stop charge now, skip the next day of the weekly plan, undo, charge plan off.
- Link your home battery control to HESC: use *EV charging power* (0 W as soon as the charger is
  paused) and *Kickstart hand-back in progress* (see How it works). With a home battery the
  charger can stay paused in its solar mode; HESC starts it with a kickstart.
- Charge plan goals in steps of 5 % (v2: 10 %).
- Dashboard: house-style icons and logo, a *Live* card, a kiosk page for a wall
  tablet, and on/off switches for the sources.
- User manual in English, Dutch and German, with screenshots.
