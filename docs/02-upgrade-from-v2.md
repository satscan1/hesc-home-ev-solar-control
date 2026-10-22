# 02 · Upgrading from HESC v2

*Nederlands: [02-upgrade-from-v2.nl.md](02-upgrade-from-v2.nl.md)*

**In short**
- Install v3 next to v2. Both run; v3 only watches (shadow mode).
- One button copies your v2 settings and history into v3.
- At a quiet moment you put v2 in shadow mode and v3 live.
- When v3 has run well for a few days, you remove v2's Node-RED flow and package.
- Changed your mind? You can go back at any moment until you remove v2.

## How v2 and v3 live next to each other

- v3 has its own entities (`…hesc_v3_…`) and its own dashboard (`/hesc-v3`). Nothing of v2 is
  changed by installing v3.
- v3 never writes v2's settings. It only reads them, and only when you press *Take over*.
- Whichever of the two has shadow mode **off** is the one that acts. Never have both live.

## Step 1 · Install v3 and let it watch

Follow [01 · Installation](01-installation.md). Leave v3's shadow mode **on**. Let both run for
a few days and compare the two dashboards: v3 should come to the same decisions as v2. The sensor
*Differences with v2 today* counts the moments where v3 would decide differently.

## Step 2 · Take over settings and history

1. *Settings → Devices & services → HESC v3 → device* → press **Take over settings and history
   from v2**.
2. v3 first saves a back-up of its own settings (to undo: **Settings restore**). Then every v3
   setting gets v2's value, and v2's charging history becomes v3's history (v2's file is only
   read, never changed).
3. Check the settings on v3's *Settings* and *Charge plan* pages.

## Step 3 · Switch over at a quiet moment

Pick a moment when nothing is going on: no grid charging by the plan and no solar release
running.

1. **v2:** switch shadow mode **on** (v2 dashboard, *Main*).
2. **v2:** empty v2's list of phones for notifications (v2 also sends notifications in shadow
   mode).
3. **v3:** press **Take over settings and history from v2** once more, so the last hours are in.
4. **v3:** switch **Shadow mode (evaluate only)** **off** on *Main*. v3 is live now.
5. **v3:** check that your phone is in v3's list for notifications (*Settings* page).

## Step 4 · Remove v2 (after a few good days)

Only when v3 has run well for some days. After this step there is no way back to v2 without
installing it again.

1. **Node-RED:** delete the four tabs whose name starts with **HESC** (*HESC Inputs*, *HESC Engine*,
   *HESC Outputs*, *HESC Reports*, each with a version number) and deploy. Leave the flows of other projects (for example HPVC or Home Battery
   Control) alone. If nothing else uses Node-RED, you may remove the add-on too.
2. **Package:** remove `/config/packages/hesc_config.yaml`, run a configuration check and
   restart Home Assistant.
3. **Dashboard:** delete the v2 dashboard under *Settings → Dashboards*.
4. v2's history in `/config/hesc-data/` stays where it is; v3 has its own copy. Delete it
   yourself if you no longer need it.

## Going back to v2 (before step 4)

1. **v3:** switch shadow mode **on**.
2. **v2:** switch shadow mode **off** and put your phone back in v2's list for notifications.
