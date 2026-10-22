# 01 · Installatie

*English: [01-installation.md](01-installation.md)*

**In het kort**
- Installeer de integratie, voeg hem toe in Home Assistant en vul het instelscherm in. HESC
  vult het meeste zelf in.
- Het dashboard en de kaarten komen met HESC mee: verder niets te installeren.
- HESC begint in schaduwmodus: hij kijkt mee en laat zien wat hij zou doen, maar schakelt niets.
  Zet de schaduwmodus uit als je vertrouwt wat je ziet.
- Kom je van HESC v2? Lees dan ook [02 · Overstappen van v2](02-upgrade-from-v2.nl.md).

## 0. Voordat je begint

- **Home Assistant 2026.10.1 of nieuwer.**
- **HACS**, om HESC te installeren (zie stap 1). HESC heeft geen andere kaarten uit HACS nodig.
- **Je laadpaal** in Home Assistant, via de eigen integratie van de laadpaal. HESC moet kunnen
  zien of er een auto aan hangt, hoeveel vermogen er in de auto gaat, en de instelling waarmee de
  laadpaal op zon laadt (bijvoorbeeld Eco bij een Wallbox).
- **Eén planner per laadpaal.** Zet laadschema's in de app van je laadpaal of in andere
  integraties uit zolang HESC het laden plant. Twee planners op één laadpaal zitten elkaar in de
  weg. Kijk na een update van de app of de firmware van de laadpaal of er niet vanzelf een schema
  is bijgekomen.
- **De accustand van je auto** (aanbevolen). Meestal via de integratie van je automerk. HESC
  werkt ook zonder, maar het laadplan is nauwkeuriger mét. Een waarde die regelmatig wordt bijgewerkt
  (om de paar minuten) werkt het best. Komt er geen nieuwe waarde binnen, dan rekent HESC verder
  met de laatst bekende stand plus wat er sindsdien geladen is.
- **Naar keuze:**
  - een **zonverwachting** — [Solcast](https://github.com/BJReplay/ha-solcast-solar) werkt het
    best; Open-Meteo en Forecast.Solar werken ook. Zonder verwachting laadt HESC nog steeds op
    gemeten zonnestroom en plant het netladen alsof er geen zon komt;
  - **dynamische energieprijzen**, voor het laadplan, goedkope kansen en de kostenpagina;
  - een **thuisbatterij**, voor de kickstart;
  - [Home PV Control (HPVC)](https://github.com/BioPC/home-pv-control) **1.5.1 of nieuwer**, als
    je zonnepanelen worden begrensd voor teruglevering. Zonder HPVC werkt HESC op zichzelf
    (standalone).

## 1. De integratie installeren

**Met HACS**
1. HACS → ⋮ → **Custom repositories** → voeg `https://github.com/satscan1/hesc-home-ev-solar-control` toe, type
   **Integration**.
2. Zoek **HESC - Home EV Solar Control** in HACS en klik op **Download**.
3. Start Home Assistant opnieuw.

**Met de hand**
1. Kopieer de map `custom_components/hesc` uit deze repository naar
   `/config/custom_components/hesc` op je Home Assistant.
2. Start Home Assistant opnieuw.

## 2. HESC toevoegen en het instelscherm invullen

*Instellingen → Apparaten & diensten → Integratie toevoegen → **HESC v3***. Het instelscherm heeft
vijf stappen. HESC zoekt in je Home Assistant en vult zelf in wat hij vindt. Controleer het en
klik op **Verzenden**.

| Stap | Wat je kiest |
|---|---|
| **Laadpaal** | Je type laadpaal: Wallbox, Alfen Eve, Peblar, myenergi Zappi, go-e Charger, Fronius Wattpilot, SMA EV Charger, Ohme, Easee, evcc (elke laadpaal), of *Other (manual)*. HESC zoekt daarna zelf de entiteiten van je laadpaal op. |
| **Bronnen** | Waar HESC je zonnestroom, je netvermogen en de zonverwachting vandaan haalt. Heb je HPVC, dan kan HESC de sensoren van HPVC gebruiken (*Zonnestroom en netvermogen uit HPVC*). Toont je meter het vermogen **per fase**, dan vult HESC ook de drie fasesensoren in; die zijn voor het fase-advies. |
| **Elektrische auto** | Hoe HESC ziet of de auto is aangesloten, hoeveel vermogen erin gaat en hoe vol de accu is. Geen accustand-sensor? Het scherm vertelt waar je er een voor jouw auto vindt. |
| **Entiteiten van de laadpaal** | Met welke instelling de laadpaal op zon laadt, waarmee HESC hem start en stopt, en de laadstroom (als je laadpaal HESC die laat instellen). |
| **HPVC** | Samenwerken met HPVC, of *Zonder HPVC (standalone)*. Heb je geen HPVC, dan staat dit vanzelf op standalone. |

Kon HESC een veld nog niet invullen, bijvoorbeeld omdat de integratie van de laadpaal nog aan het
opstarten was? Dan zoekt hij opnieuw zodra Home Assistant helemaal is opgestart. Alles kun je later
wijzigen: *Instellingen → Apparaten & diensten → HESC v3 → Configureren*.

<p><img src="images/setup-charger.png" width="49%" alt="Setup screen: charger"> <img src="images/setup-sources.png" width="49%" alt="Setup screen: sources"></p>

## 3. Het dashboard toevoegen

**Het dashboard komt met HESC mee.** Zodra HESC is ingesteld, staat **HESC** in de zijbalk (adres
`/hesc-v3`). Je hoeft niets aan te maken of te plakken, en bij elke update van HESC komt het
bijpassende dashboard mee. HESC vult zelf de namen van zijn eigen entiteiten in en de Solcast- en
HPVC-sensoren die je in het instelscherm koos. Hernoem je die, dan blijft het dashboard werken.

**Geen kaarten uit HACS nodig (sinds 3.0.0).** De grafieken, de balk *Verwacht laden op zon*,
de kostenpagina en de Kiosk-pagina gebruiken de eigen kaarten van HESC. Die zitten in de integratie
en staan na een herstart in de kaartkiezer (zoek op *HESC*). Had je voor HESC eerder
apexcharts-card, button-card, card-mod of kiosk-mode geïnstalleerd? HESC gebruikt ze niet meer;
laat ze staan als andere dashboards ze nodig hebben.

**Een eigen kopie, met één klik.** Het dashboard van HESC kun je niet wijzigen in de
dashboard-editor. Wil je een eigen versie (andere pagina's, andere kaarten)?

1. *Instellingen → Dashboards → Dashboard toevoegen*.
2. Kies onder *Community-dashboards* voor **HESC · Home EV Solar Control**, geef het een naam en
   kies *Maak aan*.
3. Je kopie heeft dezelfde pagina's; de knoppen tussen de pagina's gaan naar je kopie. Zolang je
   niets wijzigt, gaat hij mee met elke update van HESC. Wijzigen: het potlood rechtsboven
   (*Dashboard bewerken*) *→ ⋮ → Controle nemen*. Vanaf dan is hij van jou en gaat hij niet meer
   mee met HESC.

Staat hij niet in de lijst? Maak dan een leeg dashboard (*Leeg nieuw dashboard*), open het, tik op
het potlood rechtsboven en kies *⋮ → Ruwe configuratie-editor*, vervang alles door deze twee regels en
sla op:

```yaml
strategy:
  type: custom:hesc
```

- **Heb je al een dashboard op `/hesc-v3`** (zelf geplakt, bijvoorbeeld als tester)? Dan laat
  HESC dat staan en zet een melding onder *Instellingen → Reparaties*. Overstappen op het
  dashboard dat met HESC meekomt: verwijder je eigen dashboard onder *Instellingen → Dashboards*
  en herlaad daarna HESC (*Instellingen → Apparaten & diensten → HESC v3 → ⋮ → Herladen*) of
  herstart Home Assistant.

De iconen en het logo van HESC zitten in de integratie; daarvoor hoef je niets te installeren.

**Gebruik je Solcast?** De grafieken werken met blokken van 30 minuten. In Solcast:
*Configureren → Attribute breakdown → voeg `attr_brk_halfhourly` toe*. Zonder dat gebruikt HESC
de verwachting per uur.

<p><img src="images/add-dashboard.png" width="32%" alt="Add dashboard"> <img src="images/one-click-dashboard.png" width="32%" alt="Your own copy with one click"> <img src="images/card-picker.png" width="32%" alt="HESC cards in the card picker"></p>

## 4. Eerst kijken, dan live

Na het installeren staat HESC in **schaduwmodus**: hij leest alles en laat op het dashboard zien
wat hij zou doen, maar hij stuurt je laadpaal en HPVC niet aan.

1. Laat hem een paar laaddagen meedraaien. Kijk op *Overzicht* en druk af en toe op **Rapport
   maken** (onder Status).
2. Kijk of de momenten waarop HESC op zon zou starten kloppen, en of het laadplan de kwartieren
   kiest die je verwacht.
3. Zet daarna **Schaduwmodus (alleen kijken)** uit op *Overzicht*. Vanaf dat moment stuurt HESC je laadpaal echt aan.

## Waar HESC zijn bestanden bewaart

HESC bewaart zijn geschiedenis, de prijsgeschiedenis voor de prijsvoorspelling, de accustand bij
het aansluiten, de fasemetingen en de back-up van de instellingen in `/config/hesc_v3/`. Die
bestanden blijven staan als je HESC bijwerkt.

## Bijwerken

**HACS:** download de update en start Home Assistant opnieuw. **Met de hand:** vervang de map
`custom_components/hesc` en start opnieuw. Je instellingen en geschiedenis blijven.

## Verwijderen

*Instellingen → Apparaten & diensten → HESC v3 → ⋮ → Verwijderen*, haal daarna de integratie weg
in HACS (of de map `custom_components/hesc`) en start opnieuw. De map `/config/hesc_v3/` met je
geschiedenis blijft staan; verwijder die zelf als je hem niet meer nodig hebt. Het dashboard dat
met HESC meekomt, verdwijnt vanzelf mee.
