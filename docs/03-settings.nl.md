# 03 · Instellingen

*English: [03-settings.md](03-settings.md)*

**In het kort**
- **Wat HESC leest** (laadpaal, auto, zonnestroom, verwachting, HPVC) stel je in in het
  instelscherm: *Instellingen → Apparaten & diensten → HESC v3 → Configureren*.
- **Hoe HESC zich gedraagt** (drempels, laadplan, kosten, meldingen) stel je in op de pagina
  *Instellingen* van het HESC-dashboard, en de plannen zelf op de pagina *Laadplan*.
- De standaardwaarden werken voor de meeste huizen. Verander alleen iets als het advies of het
  rapport daar aanleiding toe geeft.
- Blokken die in orde zijn blijven dicht. Een blok waar iets ontbreekt gaat vanzelf open.

## Twee plekken

| Waar | Wat je daar instelt |
|---|---|
| **Instelscherm** (*Configureren*) | Type laadpaal en de entiteiten daarvan, zonnestroom en netvermogen, zonverwachting, auto (aangesloten, laadvermogen, accustand), HPVC of standalone, netvermogen per fase. Zie [01 · Installatie](01-installation.nl.md#2-hesc-toevoegen-en-het-instelscherm-invullen). |
| **Dashboard, pagina *Instellingen*** | Alles over hoe HESC zich gedraagt: drempels, tijden, advies, netladen, prijzen, meldingen, minimumlading, thuisbatterij, kosten. |
| **Dashboard, pagina *Laadplan*** | Wanneer de auto klaar moet zijn en hoe vol, vakantiemodus, goedkope kansen. |
| **Dashboard, pagina *Overzicht*** | *HESC aan* en *Schaduwmodus (alleen kijken)*. |

Op de pagina *Instellingen* staan de entiteiten uit het instelscherm alleen ter inzage. De regel
*Bronnen en laadpaal wijzigen* opent het instelscherm.

## Bovenaan de pagina Instellingen

- **Controle.** Eén kaart zegt *Instellingen gecontroleerd · alles in orde*, of hoeveel onderdelen aandacht nodig
  hebben. Per onderdeel (laadpaal, bronnen, weerstation, laadplan, thuisbatterij en auto) zie je
  de waarden van nu; bij een onderdeel dat niet klopt staat wat er ontbreekt. Onderdelen die je
  niet gebruikt staan op één regel, *Niet gebruikt*.
- **Advies.** De startdrempel waar je eigen geschiedenis op wijst, de drempel van nu, op hoeveel
  sessies het rust, en de schakelaar *Advies automatisch toepassen*. De regel **Fasen** toont het
  fase-advies. Hoe het advies werkt: [04 · Hoe het werkt](04-how-it-works.nl.md#startdrempel-en-advies).
- **Je instellingen.** Je drempels, auto, tijden, laadplan en advies in één oogopslag.
- **Back-up maken · Back-up terugzetten · Standaardwaarden.** *Back-up maken* bewaart al je
  HESC-instellingen in `/config/hesc_v3/` (plus een kopie met datum en tijd). *Back-up terugzetten*
  zet ze terug; de knop laat zien welke back-up hij gebruikt. *Standaardwaarden* maakt eerst een
  back-up en zet daarna alleen de afstelling terug (drempels, tijden, advies, eindcontrole);
  sensoren, doelen, prijzen en kosten blijven zoals ze zijn.

## 1 · Je laadpaal — verplicht

*Type laadpaal* en **Opnieuw zoeken** (zoekt de entiteiten van de laadpaal opnieuw op). De velden
van de laadpaal blijven dicht zolang de controle groen is; *Velden laadpaal* laat ze zien. Zie
[05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#je-laadpaal).

## 2 · Bronnen

| Schakelaar | Betekenis |
|---|---|
| *HPVC gebruiken* | Aan als je Home PV Control gebruikt; uit (de standaard) als je dat niet doet. Zonder HPVC slaat HESC de vrijgave over: er wordt niets begrensd, dus de laadpaal start vanzelf op zon. Een nieuwe installatie zet dit alleen zelf aan als hij HPVC vindt. |
| *Zonnestroom en net uit HPVC* | Aan = HESC gebruikt de sensoren van HPVC voor zonnestroom en netvermogen. Uit = je eigen sensoren uit het instelscherm. |
| *Bronnen wijzigen* | Laat de velden voor zonnestroom, netvermogen, verwachting en HPVC zien. Die gaan ook vanzelf open als er iets ontbreekt. |

## Extra

Zichtbaar met *Extra velden tonen*.

| Veld | Wanneer je het nodig hebt |
|---|---|
| *Statuswaarden die "geen auto" betekenen* | Alleen als *Auto aangesloten* een statussensor is. |
| *Extra zonneschakelaar* | Laadpalen die een extra schakelaar nodig hebben om op zon te laden (go-e, Wattpilot). |
| *Teller zonne-energie* | De teller van de laadpaal voor energie uit de zon, voor het rapport. |
| *Accustand auto* + *Auto telt als vol bij* | De accustand van de auto en de stand die als vol telt (standaard 80 %; 100 % bij LFP-accu's). Gebruikt voor "de auto is vol", het laadplan en goedkope kansen. |

**Eigen weerstation.** *Aan* zet het weerstation aan of uit; *Opties* toont de
zonlichtsensor en de start- en vasthouddrempel (standaard 220 / 160 W/m²). Zonder
weerstation werkt HESC alleen op de verwachting.

## 3 · Geavanceerd — alleen als het nodig is

Elk blok heeft een eigen schakelaar om het te tonen.

| Blok | Instellingen | Standaard |
|---|---|---|
| *Laaddrempels* | *Startdrempel per seizoen*, *Verwacht vermogen om te starten* / *om door te laden*, *Auto telt als ladend boven* | uit · 2 000 / 1 500 W · 400 W |
| *Tijden* | stabiel vóór vrijgave, wachten op de laadpaal, toegestane zondip, laadpaal gestopt vóór terugzetten, maximale duur vrijgave, afkoeltijd, mislukte vrijgaves per dag | 5, 10, 5, 5, 240, 30 min · 3 |
| *Advies* | advies over de laatste, minimum aantal sessies voor advies | 30 dagen · 8 sessies |
| *Laadplan en meldingen* | start/stop-schakelaar **of** de modus "nu laden", *Terug naar zonnestand*, prijsbron, prijssensor, prijzen per, valuta, zonverwachting vandaag / morgen, eindcontrole, telefoons voor meldingen, ochtendoverzicht | geen netladen · *Price list in sensor* · *Automatic* · *Automatic* · 60 min · uit |

**Netladen.** Vul **één** van de eerste twee in: een start/stop-schakelaar (gaat aan in een
gepland kwartier), of de modus-waarde die "nu laden" betekent. *Terug naar zonnestand* (naar keuze,
bij een start/stop-schakelaar) is een knop of script die de laadpaal na het netladen terugzet
naar laden op zon, bijvoorbeeld Wallbox *Resume schedule*. Bij type *Wallbox* vult HESC deze zelf
in als hij er precies één vindt. Niets ingevuld = geen netladen.

**Prijzen.** Zie [05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#energieprijzen).

**Meldingen.** *Telefoon toevoegen of weghalen* toont elk apparaat met de Home Assistant-app; ✓ = krijgt
meldingen. *Testmelding sturen* probeert het uit. *Ochtendoverzicht elke dag* stuurt één
bericht per dag (accustand, volgende plan, zon vandaag, gisteren).

## Minimumlading

*Aan* + *Opties*. Wordt de auto aangesloten onder de *Minimale accustand* (standaard 20 %),
dan laadt HESC hem tot dat niveau binnen *Halen binnen* (standaard 3 uur), in de goedkoopste
kwartieren van die periode. Handig als je bijna leeg thuiskomt en de auto snel weer nodig kunt
hebben.

## Thuisbatterij en auto

*Aan* + *Opties*, alleen met een thuisbatterij. Vul de sensor(en) voor de stand en het
vermogen van je thuisbatterijen in (meerdere met komma's ertussen; een positief vermogen
betekent laden), hun totale grootte, het maximale aantal kickstarts per dag en hoeveel zon er
minstens over moet blijven voor de auto. Heeft de start/stop-schakelaar en *Terug naar zonnestand*
uit het blok *Laadplan en meldingen* nodig. Hoe het werkt:
[04 · Hoe het werkt](04-how-it-works.nl.md#thuisbatterij-en-auto-kickstart); je
thuisbatterijregeling aan HESC koppelen:
[04 · Thuisbatterijregeling koppelen](04-how-it-works.nl.md#je-thuisbatterijregeling-aan-hesc-koppelen).

## Laadkosten

*Aan* toont de knop *Kosten* op *Overzicht* en de kostenpagina; *Opties* toont de velden. HESC telt
de kosten ook als de pagina niet zichtbaar is.

| Veld | Betekenis | Standaard |
|---|---|---|
| *Waarde van een kWh zon* | de terugleververgoeding die je misloopt door de auto te laden; 0 = gratis | 0 |
| *Prijs uit de prijsbron is al all-in* | de prijs bevat al belasting, opslag van de leverancier en btw | uit |
| *Opslag per kWh* | energiebelasting en leverancier, alleen als het niet all-in is | 0 |
| *Btw over prijs + opslag* | in %, alleen als het niet all-in is | 0 |

Een wijziging rekent de hele geschiedenis opnieuw.

## Pagina Laadplan

| Instelling | Betekenis |
|---|---|
| *Laadplan · één vaste dag per week* | Dag, tijd, doel, *Actief*. Komt elke week terug; zet *Actief* uit als je het maar één keer nodig hebt. |
| *Laadplan · weekplanning* | Dagen, tijd, doel, *Actief*. |
| *Vakantiemodus* + *Vakantie tot* | Het weekplan doet niets; het plan voor één dag en laden op zon gaan door. Gaat de dag na *Vakantie tot* vanzelf uit. |
| *Goedkope kansen pakken* + *Goedkoop onder* | Laad ook als de prijs op of onder deze prijs ligt (per kWh, in de valuta van je prijzen), tenzij de zon het later die dag dekt. |
| *Bruikbare accucapaciteit* · *Laadvermogen van het net* | Om uit te rekenen hoeveel energie nodig is en hoeveel kwartieren dat kost (standaard 60 kWh · 11 kW). |

## Pagina Overzicht

| Schakelaar | Betekenis |
|---|---|
| *HESC aan* | Hoofdschakelaar. Uit = HESC doet niets. |
| *Schaduwmodus (alleen kijken)* | Aan = HESC beslist en laat zien wat hij zou doen, maar schakelt niets. Staat aan na het installeren. |
