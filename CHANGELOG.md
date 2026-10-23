# Changelog

## 3.0.0 · 22-10-2026 

The first release of HESC as a Home Assistant integration. It can do everything HESC v2 can,
without Node-RED and without a YAML package. HESC v2 stays available; see
[Upgrading from v2](docs/02-upgrade-from-v2.md).

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
