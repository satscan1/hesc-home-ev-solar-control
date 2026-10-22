# 08 · Een dag met HESC

*English: [08-a-day-with-hesc.md](08-a-day-with-hesc.md)*

**In het kort**
- Eén gewone voorjaarsdag in een bedacht huis, van het aansluiten van de auto tot een volle auto
  de volgende ochtend.
- 's Ochtends pakken de thuisbatterijen de zon; een kickstart geeft de auto zijn beurt.
- Overdag laadt de auto op zon; de laadpaal bepaalt zelf wanneer hij start en pauzeert.
- 's Nachts vult het laadplan de rest aan in de goedkoopste kwartieren, op tijd voor de ochtend.

Deze dag is een voorbeeld: het huis, de tijden en de getallen zijn bedacht, maar elke stap is wat
HESC echt doet.

## Het huis

- **Zonnepanelen** van ongeveer 5 kWp. Solcast verwacht vandaag **18 kWh**.
- **Thuisbatterijen** van samen 10 kWh, 's ochtends op 30 %, met hun eigen batterijregeling.
- **Een Wallbox** op drie fases, op *Eco* (laden op zon).
- **Een auto** met een accu van 60 kWh, op **40 %** als hij wordt aangesloten.
- **Een laadplan:** 80 % om 07:30 morgenochtend.
- **Dynamische energieprijzen**, per kwartier.
- Instellingen: startdrempel **1.500 W**, doorlaaddrempel **1.100 W**.

## 07:45 · Aangesloten

De auto wordt aangesloten op 40 %. HESC rekent uit wat er nodig is: 40 % → 80 % is ongeveer
24 kWh.

Op *Overzicht* zie je het plan voor vandaag:
- **Verwachting laadmogelijkheden op zon:** groene staven van ongeveer 10:30 tot 15:30. Groen betekent: genoeg
  zon om de laadpaal te laten starten. Oranje betekent: genoeg om door te laden, niet om te
  starten. Boven de grafiek staan de twee drempels.
- **Verwacht laden op zon:** vandaag ongeveer 5 uur laden op zon.
- **Live:** *Accustand auto 40 % · vol bij 80 %*, *Zon die vandaag nog komt 18 kWh*.

Het laadplan reserveert vannacht al een paar goedkope kwartieren, maar laat ruimte voor de zon die
nog komt.

## 08:30 – 10:00 · De thuisbatterijen eten eerst

De zon komt op. De thuisbatterijen staan op 30 % en nemen elke watt die over is. Er gaat niets
naar het net, dus de Wallbox ziet geen overschot en wacht.

Op de kaart *Live*: *Net 0 W*, *Thuisbatterijen 1800 W · 42 %*. HESC kijkt mee en wacht.

## 10:15 · Kickstart

De voorzichtige verwachting is nu 2.300 W, boven de startdrempel. De thuisbatterijen laden al een
tijdje rustig. En er is vandaag genoeg zon over voor allebei: nog ongeveer 14 kWh, de
thuisbatterijen hebben nog ongeveer 6 kWh nodig.

Dus geeft HESC de auto een **kickstart**. Onder *Huidige stand* toont *Thuisbatterij en auto*:
1. *Kickstart: charger started* — de laadpaal start even.
2. De batterijregeling ziet dat de auto laadt en stopt met het laden van de thuisbatterijen.
3. *Kickstart: charger paused* — HESC pauzeert de laadpaal weer.
4. *Kickstart: waiting for the charger to start on sun* — de laadpaal staat weer op *Eco*. Nu gaat
   de zon die over is naar het net, en dat ziet de Wallbox.

## 10:20 – 10:35 · Genoeg zon, maar niet op elke fase

Er is in totaal 2,0 kW over. Een Wallbox op *Eco* heeft op drie fases ongeveer 1,4 kW nodig, maar
ook **minstens ongeveer 480 W op elke fase**. Fase 3 heeft maar 350 W, dus de Wallbox wacht.

Om 10:35 staat de zon hoger, alle drie de fases zitten boven 480 W, en de Wallbox start vanzelf. De
auto laadt op zon.

Toont je meter het vermogen per fase, dan telt HESC hoe vaak dit gebeurt. Je ziet het op de pagina
*Instellingen* in de regel *Fasen*: eerst *aan het meten*, na een paar weken *voorlopig*, en in
de zonnigste periode van het jaar *bevestigd*. Elke laadpaal heeft zijn eigen startniveau; zie
[05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#hoeveel-zon-een-laadpaal-nodig-heeft-om-te-starten).

## 12:00 · Een goedkoop kwartier, maar genoeg zon

Rond het middaguur zakt de prijs naar bijna niets. Een goedkope kans — maar de zon dekt naar
verwachting wat de auto vandaag nog nodig heeft. *Status* toont:

> *Cheap chance skipped: enough sun today (…)*

De auto laadt gewoon door op zon.

**Heb je HPVC** en begrenst die op dit moment je panelen (terugleveren levert niets op), dan ziet de
Wallbox geen overschot. Dan vraagt HESC aan HPVC om de zon door te laten voor de auto, zolang de
verwachting boven de startdrempel ligt. HPVC beslist; HESC wacht op het antwoord en geeft de
panelen terug zodra de auto stopt of de zon onder de doorlaaddrempel zakt.

## 14:30 – 16:00 · Wolken

Er komen wolken en ze gaan weer. De Wallbox pauzeert als de zon te laag is en start vanzelf weer
als hij terugkomt. HESC grijpt niet in: de laadpaal beslist op zijn eigen zon.

Op *Overzicht* laat *Zonverwachting en realisatie · auto* zien hoe de oranje lijn (de echte zonnestroom) onder
het paarse vlak (de verwachting) zakt, en hoe de cyaan lijn (de auto) daarmee aan en uit gaat.

## 16:15 · Een gepland kwartier, en de stroom gaat omlaag

Het laadplan heeft 16:15 – 16:30 gekozen: de prijs is daar laag. De auto laadt van het net. Er is
nog ongeveer 2,5 kW zon.

Omdat deze Wallbox HESC de laadstroom laat instellen, zet HESC die terug naar 6 A per fase. De auto
neemt dan ongeveer 4,1 kW, en meer dan de helft daarvan komt uit de zon in plaats van van het net.
HESC doet dit alleen zolang de auto op tijd vol is. Na het kwartier gaat de stroom terug naar wat
hij was.

## 17:15 · De zon is weg

De Wallbox stopt; de auto heeft vandaag ongeveer 10 kWh zon gekregen en staat op **58 %**. De
thuisbatterijen zijn vol.

Het laadplan rekent de rest uit: 58 % → 80 % is ongeveer 13 kWh. Het kiest de goedkoopste
kwartieren van de nacht.

## 02:00 – 03:15 · De rest van het net

Tussen 02:00 en 03:15, de goedkoopste kwartieren van de nacht, laadt het plan van het net. Om 03:15
staat de auto op **80 %**, ruim vier uur vóór de klaar-tijd. *Status* toont *Goal reached (80%)*.

## De dag in getallen

| | |
|---|---|
| Zonverwachting (Solcast) | 18 kWh |
| Opgewekte zonnestroom | ongeveer 19 kWh |
| Naar de thuisbatterijen | ongeveer 7 kWh (30 % → vol) |
| Naar de auto uit de zon | ongeveer 10,5 kWh |
| Naar de auto van het net | ongeveer 13,5 kWh |
| Auto | 40 % → 80 % (ongeveer 24 kWh) |
| Aandeel zon in de auto | ongeveer 44 % |
| Kosten netstroom voor de auto | ongeveer € 2,80 (13,5 kWh tegen ongeveer € 0,21 all-in) |

## Wat je hieruit meeneemt

- **Iedereen doet zijn eigen werk.** De batterijregeling stuurt de thuisbatterijen, de laadpaal
  bepaalt wanneer hij op zon start, HPVC beslist over de panelen. HESC kijkt mee, vraagt en plant.
- **De kickstart zorgt dat de auto 's ochtends op gang komt.** Zonder kickstart zou de auto wachten
  tot de thuisbatterijen vol zijn.
- **Niet elke watt telt even zwaar.** Op drie fases heeft een laadpaal zoals de Wallbox op *Eco*
  zon nodig op elke fase. Dat is de eigen regel van de laadpaal; het fase-advies laat zien hoe vaak
  je daardoor wordt tegengehouden.
- **Het laadplan vult alleen aan wat de zon laat liggen.** Het neemt de goedkoopste kwartieren en
  zorgt dat de auto op tijd vol is.

Meer over de logica hierachter: [04 · Hoe het werkt](04-how-it-works.nl.md) en
[07 · Slim laden uitgelegd](07-smart-charging-explained.nl.md). Wat elke kaart op het dashboard
laat zien: [06 · Dashboard](06-dashboard.nl.md).
