# 05 · Laadpalen en bronnen

*English: [05-chargers-and-sources.md](05-chargers-and-sources.md)*

**In het kort**
- HESC praat nooit rechtstreeks met je laadpaal, auto of verwachtingsdienst. Hij werkt alleen via
  Home Assistant: hij leest en bedient de entiteiten die de integraties van je laadpaal, auto en
  verwachting daar maken.
- Kies je type laadpaal in het instelscherm; HESC zoekt dan zelf de bijbehorende entiteiten op.
- Elke laadpaal heeft een bepaalde hoeveelheid zon nodig voordat hij op zon start.
  HESC weet dat per merk en adviseert nooit een lager startniveau.
- De accustand van de auto, een zonverwachting en energieprijzen laten HESC nauwkeuriger plannen, maar zijn
  niet verplicht.

## Je laadpaal

### Wat HESC ervan nodig heeft

| Wat | Waarom | Voorbeeld |
|---|---|---|
| **Is er een auto aangesloten?** | Zonder auto valt er niets te doen | een sensor "aangesloten", of een status zoals `Ready` / `Charging` |
| **Laadvermogen** | Om te zien of de auto echt laadt | in W of kW |
| **De stand voor laden op zon** | In die stand start de laadpaal zelf als er genoeg zon is | Wallbox *Eco*, Alfen *Green*, Zappi *Eco+* |
| **Start/stop** (voor het laadplan) | Om in de goedkoopste kwartieren van het net te laden | een pauze/hervat-schakelaar, of een modus "nu laden" |
| **Laadstroom** (naar keuze) | Om het laden aan de zon aan te passen | Wallbox *Maximale laadstroom* |

Een gepauzeerde laadpaal telt als 0 W, wat hij ook nog meldt: sommige laadpalen (bijvoorbeeld de
Wallbox) laten na een pauze minutenlang hun laatste vermogen zien. Gepauzeerd betekent: de
start/stop-schakelaar staat uit, of de status van de laadpaal zegt *gepauzeerd* (*paused*).

### Soorten laadpalen

Kies het type in het instelscherm (stap **Laadpaal**) of later op de pagina *Instellingen*. HESC
zoekt dan zelf in je Home Assistant de entiteiten van je laadpaal op en vult ze in. HESC weet per
merk welke stand van de laadpaal "laden op zon" is (bij een Wallbox bijvoorbeeld *Eco*) en
welke status betekent dat er geen auto aan hangt.

- Vindt HESC precies één passende entiteit, dan vult hij die in. Vindt hij er meer, dan laat hij
  het veld leeg en kies je zelf.
- Wat je zelf hebt ingevuld, overschrijft HESC nooit.
- Het zoeken werkt ook als je Home Assistant Nederlandse of Duitse namen gebruikt.

| Laadpaal | Stand voor laden op zon | Opmerking |
|---|---|---|
| **Wallbox** (Pulsar Plus, Copper) | `eco_mode`, `full_solar` | in de praktijk getest |
| **Alfen Eve** | `Green` | heeft een meter op de Alfen-loadbalancing nodig |
| **Peblar** | `pure_solar` | |
| **myenergi Zappi** | `Eco+` | kies zelf de vermogenssensor van de interne Zappi-stroomtang |
| **go-e Charger** | `4` (Eco) | heeft net- en zondata nodig (go-e Controller of vanuit Home Assistant) |
| **Fronius Wattpilot** | `Eco` | gebruikt de Fronius-meter |
| **SMA EV Charger** | `optimized_charging` | via de Sunny Home Manager |
| **Ohme** | `on` (Solar Boost) | maar deels: Home Pro met eigen stroomtang |
| **Easee** | `on` | alleen met een Easee Equalizer; kies zelf de schakelaar voor laden op overschot |
| **evcc** (elke laadpaal) | `pv`, `smart` | kies de entiteiten van het evcc-laadpunt, niet die van de laadpaal zelf |
| **Other (manual)** | eigen keuze | vul de velden zelf in |

Laadpalen zonder eigen stand voor laden op zon (bijvoorbeeld Zaptec, Tesla Wall Connector of gewoon OCPP)
kun je gebruiken via evcc.

Alleen de Wallbox is in de praktijk getest. Heb je een andere laadpaal: laat de schaduwmodus een
paar zonnige dagen aan, kijk of de kaart *Live* alle waarden toont, en of de laadpaal na het
netladen terugkeert naar laden op zon.

**Eén planner per laadpaal.** Zet laadschema's in de app van de laadpaal of in andere
integraties uit zolang HESC het laden plant.

### Hoeveel zon een laadpaal nodig heeft om te starten

Een laadpaal die op zon laadt, start pas als er genoeg overschot is. Het standaardminimum voor
elke laadpaal is 6 A per fase: ongeveer **1,4 kW op één fase** en **4,1 kW op drie fases**.
Sommige merken starten lager:

| Laadpaal · modus | 1 fase | 3 fases |
|---|---|---|
| Wallbox · Eco | ± 460 W | ± 1,4 kW, minstens 480 W op **elke** fase |
| Wallbox · Full Green | 1,4 kW | 4,1 kW |
| Alfen · Green | 1,4 kW | 4,2 kW |
| Zappi · Eco+ | 1,4 kW | 4,2 kW |
| Ohme · Solar Boost | 0,72 kW (+ 0,72 kW van het net) | 4,1 kW |
| Easee | 1,4 kW | 4,1 kW, 6 A op **elke** fase |
| Andere merken | 1,4 kW | 4,1 kW (standaard) |

HESC gebruikt dit als ondergrens: het advies voor de startdrempel komt nooit lager uit dan wat je
laadpaal nodig heeft.

### Eén fase of drie?

Dat stel je niet in, en HESC kiest het ook niet. Het aantal fases is het kleinste van wat je
huisaansluiting, je laadpaal en je auto aankunnen. Een auto met een eenfase-lader laadt altijd
op één fase, ook aan een driefase-laadpaal. HESC meet het terwijl de auto laadt.

**Fase-advies.** Toont je meter het vermogen per fase (de meeste slimme meters doen dat), dan
telt HESC hoe de zon over de fases verdeeld is. Bij laadpalen die op elke fase zon nodig hebben
(Wallbox Eco, Easee) kan één zwakke fase de laadpaal tegenhouden. Het advies op de pagina
*Instellingen* gaat door drie stadia:
1. **meten** — nog niet genoeg zonnige dagen;
2. **voorlopig** — na ongeveer twee weken;
3. **bevestigd** — na genoeg dagen in de zonnigste periode van het jaar op jouw plek.

Het is alleen informatie; HESC verandert er zelf niets mee.

### Laadstroom

Laat je laadpaal HESC de laadstroom instellen (Wallbox: *Maximale laadstroom*), dan verlaagt
HESC de stroom terwijl het laadplan van het net laadt, zodat meer van de energie uit de zon komt
— zolang de auto op tijd vol is. Daarna gaat de stroom terug naar wat hij was. Dit is normaal
gedrag; er is geen schakelaar voor. Heb je geen laadstroom ingevuld, dan verandert HESC de stroom
nooit.

## De accustand van je auto

Niet verplicht, maar het laadplan en "de auto is vol" werken er veel nauwkeuriger mee. Elke
accustand-sensor in % werkt, meestal van de integratie van je automerk. Nog geen sensor? Het
instelscherm vertelt waar je er een voor jouw auto vindt.

**Regelmatige updates werken het best.** Een waarde die om de paar minuten wordt bijgewerkt geeft
de beste planning. Veel auto-integraties werken minder vaak bij om de 12V-accu van de auto te
sparen; dat is prima.

**Waar HESC de accustand vandaan haalt.** HESC neemt de eerste van deze bronnen die een waarde
heeft. Valt de eerste weg, dan gaat hij door naar de volgende:
1. de accustand-sensor die je hebt gekozen;
2. een tweede accustand-sensor van dezelfde auto, als HESC die vindt;
3. de laatst bekende stand van deze laadsessie, plus wat er sindsdien geladen is;
4. de gebruikelijke stand bij het aansluiten over de laatste 14 dagen.

Het dashboard laat zien welke bron gebruikt wordt.

**Bekend gedrag:** sommige auto-integraties sturen vlak na een herstart van Home Assistant even
een verkeerde waarde (bijvoorbeeld 99,9 %), tot hun volgende update. HESC denkt dan een paar
minuten dat de auto vol is en kan het laden uitstellen. Bij de volgende juiste waarde rekent alles
opnieuw; er blijft niets verkeerd staan.

## Zonverwachting

| Wat je hebt | Wat HESC doet |
|---|---|
| **Solcast** | Beste keus. HESC beslist met de voorzichtige schatting en vergelijkt met de gewone schatting wat er echt gebeurt. Tip: voeg in Solcast `attr_brk_halfhourly` toe onder *Attribute breakdown* voor blokken van 30 minuten. |
| **Open-Meteo Solar Forecast** of **Forecast.Solar** | Werkt op dezelfde manier; HESC zet het zelf om. |
| **Geen verwachting** | HESC laadt op gemeten zonnestroom en plant het netladen alsof er geen zon komt (nooit te laat). De kickstart staat uit. Een melding onder *Instellingen → Reparaties* legt uit hoe je een verwachting toevoegt. |

**Weerstation (naar keuze).** Een eigen zonlichtsensor (W/m²) of luxmeter kan als extra
controle dienen. Zet *Eigen weerstation gebruiken* aan in het instelscherm. Begin met lage
drempels; na een paar weken laat het rapport zien hoe goed hij bij je zonnestroom past.

## Energieprijzen

Alleen nodig voor het laadplan, goedkope kansen en de kostenpagina, en alleen zinvol met een
**dynamisch** contract (een prijs per kwartier of uur). De prijsbron stel je in op *Instellingen → Geavanceerd →
Laadplan en meldingen*.

| Prijsbron | Bronnen |
|---|---|
| *Price list in sensor* | Nord Pool (HACS), ENTSO-E, Energi Data Service, EPEX Spot, Frank Energie, Zonneplan, Octopus Energy (Agile), Amber Electric, PVPC (Spanje) |
| *EnergyZero / ANWB Energie*, *EasyEnergy*, *Tibber*, *Nord Pool (official)* | kies een sensor van die integratie; HESC haalt de prijzen zelf elke 30 minuten op |

- HESC plant altijd in kwartieren; prijzen per uur of half uur worden in kwartieren verdeeld.
- Valuta: EUR, SEK, DKK, NOK, GBP en AUD. *Automatic* haalt de valuta uit de prijssensor.
- Feestdagen voor de prijsvoorspelling komen uit de integratie **Workday** voor je land.
- Nettarieven die over de dag veranderen worden niet meegerekend; gebruik *all-in*-prijzen van je
  bron als je die hebt.

## Thuisbatterij (naar keuze)

Voor de kickstart leest HESC de stand (%) en het vermogen (W) van je thuisbatterijen en hun totale
grootte. Een positief vermogen betekent dat de batterij laadt. Zie de pagina *Instellingen*, *Thuisbatterij
en auto*.
