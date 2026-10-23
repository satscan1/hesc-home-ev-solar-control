<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/custom_components/hesc/frontend/hesc-logo.png" width="160" alt="HESC"></p>

# HESC — Home EV Solar Control

*Nederlands: [README.nl.md](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/README.nl.md) · Deutsch: [README.de.md](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/README.de.md)*

HESC charges your electric car as much as possible on your own solar power, and from the grid
at the cheapest moments when the sun is not enough. It runs inside Home Assistant.

<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/docs/images/infographic-en.png" width="100%" alt="HESC v3 at a glance"></p>

<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/docs/images/main.png" width="90%" alt="HESC dashboard"></p>

## What HESC does

- **Charges on sun.** HESC watches your solar forecast and your solar power, and lets your
  charger start on sun at the right moment.
- **Plans grid charging.** Tell HESC when the car must be ready and how full. HESC picks the
  cheapest quarters with dynamic prices, and leaves room for the sun that is still to come.
- **Works with your home battery.** When the home batteries would take all the sun, HESC gives
  the car a kickstart, so it gets its turn instead of waiting until the batteries are full. HESC
  never controls the home battery itself: this works with a battery that reacts to what the house
  uses (see [How it works](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.md#home-battery-and-ev-kickstart)).
- **Shows what happens.** A dashboard with today, the forecast, costs and advice; and a report
  you can open at any time.

## New in v3

HESC v3 is a Home Assistant integration. It can do everything HESC v2 can, plus:

- **No Node-RED and no YAML package any more.** You install one integration and fill in one
  setup screen.
- **Finds your charger and car by itself**, also when Home Assistant uses Dutch or German entity names.
- **Works without a solar forecast** if you have none (Solcast, Open-Meteo and Forecast.Solar
  are supported).
- **Adjusts the charging current** on chargers that allow it, to get more sun into the car.
- **Knows your charger's start level.** The advice never goes below what your charger needs to
  start on sun.
- **Phase advice** if your grid meter shows power per phase: it tells you if one phase holds
  your charger back.
- **The dashboard comes with HESC**: *HESC* in the sidebar, nothing to paste.
- **Charge now** to a level you choose, from the grid, then back to sun by itself.
- **Skip one day** of the weekly plan (a day off) without changing the plan.
- **On your phone and watch** (iPhone, Apple Watch, Android, Wear OS): a one-line summary for a
  widget, actions for Siri and Shortcuts, and one-tap buttons. See
  [Dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.md#on-your-phone-and-watch).

HESC v2 stays available. You can run v3 next to v2 and switch over when you are ready; see
[Upgrading from v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.md).

## How HESC is tested

Every version is tested before release in a simulator that plays whole days in seconds: fixed
scenarios (sunny summer day, cloudy winter day, negative prices, a charger that refuses to start,
a restart in the middle of a plan, …) and real recorded days, for every supported charger. A new
version must decide the same as the previous one, unless the change is intended.

## What you need

- Home Assistant **2026.10.1** or newer.
- Your **charger** in Home Assistant, through its own integration.
- Your **car's battery level** in Home Assistant (recommended). HESC also works without it, but
  plans more accurately with it.
- Optional: a **solar forecast**, **dynamic energy prices**, a **home battery**, and
  [Home PV Control (HPVC)](https://github.com/BioPC/home-pv-control) 1.5.1 or newer.

## Install in three steps

1. Install the integration (HACS or by hand).
2. Add **HESC v3** under *Settings → Devices & services* and fill in the setup screen.
3. Open **HESC** in the sidebar: the dashboard and its cards come with HESC, nothing else to install.

HESC starts in **shadow mode**: it watches and shows what it would do, but switches nothing until
you turn shadow mode off. Step by step: [Installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.md).

## Documentation

| | English | Nederlands | Deutsch |
|---|---|---|---|
| Installation | [01-installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.md) | [01-installatie](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.nl.md) | [01-installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.de.md) |
| Upgrading from v2 | [02-upgrade-from-v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.md) | [02-overstappen-van-v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.nl.md) | [02-umstieg-von-v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.de.md) |
| Settings | [03-settings](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/03-settings.md) | [03-instellingen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/03-settings.nl.md) | [03-einstellungen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/03-settings.de.md) |
| How it works | [04-how-it-works](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.md) | [04-hoe-het-werkt](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.nl.md) | [04-so-funktioniert-es](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.de.md) |
| Chargers and sources | [05-chargers-and-sources](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/05-chargers-and-sources.md) | [05-laadpalen-en-bronnen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/05-chargers-and-sources.nl.md) | [05-wallboxen-und-quellen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/05-chargers-and-sources.de.md) |
| Dashboard | [06-dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.md) | [06-dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.nl.md) | [06-dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.de.md) |
| Smart charging explained | [07-smart-charging-explained](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/07-smart-charging-explained.md) | [07-slim-laden-uitgelegd](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/07-smart-charging-explained.nl.md) | [07-intelligentes-laden-erklärt](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/07-smart-charging-explained.de.md) |
| A day with HESC | [08-a-day-with-hesc](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/08-a-day-with-hesc.md) | [08-een-dag-met-hesc](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/08-a-day-with-hesc.nl.md) | [08-ein-tag-mit-hesc](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/08-a-day-with-hesc.de.md) |
| Troubleshooting | [09-troubleshooting](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/09-troubleshooting.md) | [09-problemen-oplossen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/09-troubleshooting.nl.md) | [09-fehlerbehebung](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/09-troubleshooting.de.md) |

