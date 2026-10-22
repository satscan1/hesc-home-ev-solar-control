# 02 · Overstappen van HESC v2

*English: [02-upgrade-from-v2.md](02-upgrade-from-v2.md)*

**In het kort**
- Installeer v3 naast v2. Ze draaien allebei; v3 kijkt alleen mee (schaduwmodus).
- Met één knop neemt v3 je instellingen en geschiedenis van v2 over.
- Op een rustig moment zet je v2 in schaduwmodus en v3 live.
- Draait v3 een paar dagen goed, dan haal je de Node-RED-flow en het package van v2 weg.
- Toch terug? Dat kan op elk moment, zolang je v2 nog niet hebt weggehaald.

## Hoe v2 en v3 naast elkaar bestaan

- v3 heeft eigen entiteiten (`…hesc_v3_…`) en een eigen dashboard (`/hesc-v3`). Door v3 te
  installeren verandert er niets aan v2.
- v3 schrijft nooit in de instellingen van v2. Hij leest ze alleen, en alleen als je op *Instellingen
  en geschiedenis van v2 overnemen* drukt.
- Wie van de twee de schaduwmodus **uit** heeft, is degene die schakelt. Zet ze nooit allebei
  live.

## Stap 1 · v3 installeren en laten meekijken

Volg [01 · Installatie](01-installation.nl.md). Laat de schaduwmodus van v3 **aan**. Laat ze
allebei een paar dagen draaien en vergelijk de twee dashboards: v3 hoort tot dezelfde
beslissingen te komen als v2. De sensor *Verschillen met v2 vandaag* telt de momenten waarop v3
anders zou beslissen.

## Stap 2 · Instellingen en geschiedenis overnemen

1. *Instellingen → Apparaten & diensten → HESC v3 → apparaat* → druk op **Instellingen en geschiedenis
   van v2 overnemen**.
2. v3 maakt eerst een back-up van zijn eigen instellingen (terugdraaien: **Instellingen terugzetten**).
   Daarna krijgt elke v3-instelling de waarde van v2, en wordt de laadgeschiedenis van v2 de
   geschiedenis van v3 (het bestand van v2 wordt alleen gelezen, nooit veranderd).
3. Controleer de instellingen op de pagina's *Instellingen* en *Laadplan* van v3.

## Stap 3 · Overstappen op een rustig moment

Kies een moment waarop er niets gebeurt: geen netladen volgens het plan en geen zonnevrijgave
bezig.

1. **v2:** zet de schaduwmodus **aan** (dashboard van v2, *Main*).
2. **v2:** maak de lijst met telefoons voor meldingen van v2 leeg (v2 stuurt ook in schaduwmodus
   meldingen).
3. **v3:** druk nog één keer op **Instellingen en geschiedenis van v2 overnemen**, zodat de laatste uren
   er ook in zitten.
4. **v3:** zet **Schaduwmodus (alleen kijken)** **uit** op *Overzicht*. v3 is nu live.
5. **v3:** controleer of je telefoon in de meldingenlijst van v3 staat (pagina *Instellingen*).

## Stap 4 · v2 weghalen (na een paar goede dagen)

Pas als v3 een paar dagen goed heeft gedraaid. Na deze stap kun je niet meer terug naar v2 zonder
hem opnieuw te installeren.

1. **Node-RED:** verwijder de vier tabbladen waarvan de naam begint met **HESC** (*HESC Inputs*,
   *HESC Engine*, *HESC Outputs*, *HESC Reports*, elk met een versienummer) en klik op Deploy. Laat de flows van andere projecten (bijvoorbeeld HPVC of
   Home Battery Control) staan. Gebruikt niets anders Node-RED, dan mag de add-on ook weg.
2. **Package:** verwijder `/config/packages/hesc_config.yaml`, doe een configuratiecontrole en
   start Home Assistant opnieuw.
3. **Dashboard:** verwijder het v2-dashboard onder *Instellingen → Dashboards*.
4. De geschiedenis van v2 in `/config/hesc-data/` blijft staan; v3 heeft een eigen kopie.
   Verwijder hem zelf als je hem niet meer nodig hebt.

## Terug naar v2 (vóór stap 4)

1. **v3:** zet de schaduwmodus **aan**.
2. **v2:** zet de schaduwmodus **uit** en zet je telefoon terug in de meldingenlijst van v2.
