# 04 · Hoe het werkt

*English: [04-how-it-works.md](04-how-it-works.md)*

**In het kort**
- Elke 30 seconden leest HESC je bronnen en beslist wat de laadpaal moet doen.
- Op zon: HESC laat de laadpaal starten in zijn eigen stand voor laden op zon. Met HPVC vraagt
  HESC eerst aan HPVC om je zonnepanelen een tijdje niet te begrenzen.
- Van het net: het laadplan kiest de goedkoopste kwartieren vóór je klaar-tijd en rekent op de
  zon die nog komt.
- Met een thuisbatterij zorgt een kickstart dat de auto op een zonnige dag aan de beurt komt.
- In schaduwmodus neemt HESC precies dezelfde beslissingen, maar schakelt hij niets.

## Elke 30 seconden

HESC leest zo'n twintig waarden uit Home Assistant: zonnestroom, netvermogen, verwachting, de
laadpaal, de auto, prijzen, de thuisbatterij. Hij rekent uit wat er moet gebeuren en schrijft
de uitkomst naar zijn eigen entiteiten (status, reden, plan). Tijden en daggrenzen volgen de
tijdzone van Home Assistant. Onderdelen die niet zo vaak hoeven, hebben een eigen tempo,
bijvoorbeeld de prijsvoorspelling elke 15 minuten.

**Schaduwmodus** (*Schaduwmodus (alleen kijken)* op *Overzicht*) staat aan na het installeren. HESC
beslist dan precies zoals wanneer hij live is en laat dat zien, maar stuurt geen opdracht naar de
laadpaal of HPVC. Staat **HESC aan** uit, dan doet HESC helemaal niets.

## Laden op zon

**Zonder HPVC (standalone).** Niets begrenst je zonnepanelen, dus de laadpaal start vanzelf op
zon zodra er genoeg overschot is. HESC volgt elke sessie, legt vast hoe die ging en geeft advies
over de startdrempel.

**Met HPVC.** HPVC houdt je teruglevering rond nul, dus de laadpaal ziet nooit genoeg overschot
om te starten. Daarom vraagt HESC aan HPVC om een vrijgave:

| Stap | Wat er gebeurt |
|---|---|
| Rust | HESC wacht tot alle startvoorwaarden *Omstandigheden stabiel voor vrijgave* lang (5 min) kloppen. |
| Vrijgave gevraagd | HESC vraagt het aan HPVC (HPVC 1.5.1 of nieuwer). HPVC maakt eerst af wat voorrang heeft en laat de panelen dan vrij produceren. Geen antwoord binnen 5 minuten → HESC probeert het later. |
| Wachten op de auto | HPVC heeft bevestigd. De laadpaal heeft *Wachten tot de laadpaal start* (10 min) om te starten. |
| Laden | De auto laadt op zon. |
| Vrijgave voorbij | De auto stopte, de zon bleef langer dan *Toegestane zondip* onder de vasthouddrempel, de auto werd losgekoppeld, de zon ging onder, of *Langste vrijgave*. HPVC neemt het weer over en er begint een afkoeltijd. |

Startvoorwaarden: de auto is aangesloten, laadt niet, is niet vol en de laadpaal staat op laden
op zon; HPVC begrenst; de voorzichtige verwachting (nu en over 30 minuten) ligt op of boven de
startdrempel; het weerstation is het ermee eens (als je het gebruikt); geen afkoeltijd; niet te
veel mislukte vrijgaves vandaag; de zon is op. HESC zet HPVC nooit zelf uit; hij vraagt het
alleen.

## Zonverwachting

| Wat je hebt | Hoe HESC het gebruikt |
|---|---|
| **Solcast** | De voorzichtige schatting om te beslissen, de gewone schatting om te vergelijken met wat er echt gebeurde. |
| **Open-Meteo** of **Forecast.Solar** | HESC zet het om naar dezelfde vorm; werkt op dezelfde manier. |
| **Geen verwachting** | HESC gebruikt in plaats daarvan de gemeten zonnestroom (of het weerstation). Het laadplan rekent geen zon, dus het is nooit te laat. De kickstart staat uit. |

## Startdrempel en advies

De startdrempel gaat over de **verwachting**. Hij bepaalt drie dingen:

- wanneer HESC HPVC vraagt de begrenzing van je panelen op te heffen (alleen als HPVC begrenst);
- wanneer de kickstart mag starten;
- welke halve uren het laadplan meetelt als "er komt zon".

Hij bepaalt **niet** wanneer je laadpaal op zon laadt: in de zonnestand start de laadpaal zelf
op overschot, wat de drempel ook is. De juiste waarde verschilt per huis, dus HESC berekent hem
uit je eigen sessies:

- Hij kijkt alleen naar de laadsessies op zon die **startten terwijl HPVC je panelen begrensde**,
  van de laatste 30 dagen (in de winter tot 60 dagen, als het er weinig zijn). Alleen bij die
  sessies deed de drempel ertoe. Starts met de hand of door een schema tellen niet mee.
- In de donkere maanden begrenst HPVC zelden, dus het advies blijft dan vaak verzamelen. Dat is
  niet erg: de drempel doet dan weinig. Zonder HPVC (standalone) is er geen advies; *Startdrempel
  per seizoen* is dan de eenvoudige keuze.
- **Advies:** de laagste startverwachting vanaf waar de volgende 8 sessies samen minstens 70 %
  van hun energie uit de zon haalden. Afgerond op 50 W, tussen 1 000 en 3 500 W. Vasthouden =
  75 % van start.
- **Nooit onder je laadpaal.** Het advies komt nooit lager uit dan de zon die je laadpaal nodig
  heeft om te starten (zie [05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#hoeveel-zon-een-laadpaal-nodig-heeft-om-te-starten)).
  Het advies zegt dat er dan bij.
- **Advies automatisch toepassen** (standaard uit): HESC schuift de startdrempel zelf richting het
  advies, in kleine stappen: hooguit 200 W per stap en één stap per 7 dagen, alleen bij een
  verschil van minstens 100 W en als het advies op genoeg sessies op verschillende dagen rust.
  Elke wijziging verschijnt als grijze melding op *Overzicht*.
- **Startdrempel per seizoen** (standaard uit): elke nacht zet HESC de startdrempel voor de
  maand: juni–juli 2 500 W, april–mei en augustus–september 2 000 W, maart en oktober 1 500 W,
  november–februari 1 200 W; vasthouden 75 %. Nooit onder het startniveau van je laadpaal. Kan
  niet tegelijk aan staan met *Advies automatisch toepassen*.

Het advies wordt elke avond berekend en als HESC opstart.

## Fase-advies

Alleen met netvermogen per fase in het instelscherm. Zolang de auto niet laadt, kijkt HESC
hoeveel overschot elke fase heeft. Laadpalen die op **elke** fase zon nodig hebben (Wallbox Eco,
Easee) worden tegengehouden door de zwakste fase. Het advies gaat door drie stadia:

1. **meten** — minder dan 14 dagen met bruikbare zon;
2. **voorlopig** — de verdeling over de fases is bekend;
3. **bevestigd** — genoeg dagen in de zonnigste periode van het jaar gezien.

De zonnigste periode berekent HESC uit de stand van de zon op jouw plek, dus het klopt overal ter
wereld (op het zuidelijk halfrond rond december). Het fase-advies is alleen informatie; HESC
verandert er zelf niets mee.

## Laadplan

Het plan neemt het actieve plan (het plan voor één dag of het weekplan; het vroegste wint), het
doel en de klaar-tijd. Het rekent uit hoeveel energie nodig is, trekt de zon af die vóór de
klaar-tijd verwacht wordt, en kiest voor de rest de goedkoopste kwartieren. Na de prijzen van de
dag gebruikt het ook verwachte prijzen, maar het wacht alleen op zo'n prijs als die duidelijk
goedkoper is.

**Zon in het plan.** Elk half uur vóór de klaar-tijd met een voorzichtige verwachting die hoog
genoeg is om de laadpaal te laten starten, telt als (verwachting − 0,4 kW voor het huis) × 0,5
uur, hooguit het netlaadvermogen.

| Reden op het dashboard | Wat er gebeurt |
|---|---|
| *Planned quarter* | Laden van het net. |
| *Safety net: only just enough time left* | Laden, omdat de resterende tijd net genoeg is. |
| *Final check: below goal, charging to goal* | In het laatste uur (*Eindcontrole voor de klaar-tijd*) onder het doel: laden, wat de prijs ook is. |
| *Cheap chance (…)* | De prijs ligt op of onder *Goedkoop onder*: laden. |
| *Cheap chance skipped: enough sun today (…)* | De zon later vandaag dekt wat nodig is, met 20 % over. |
| *Within 3 % of goal* | Netladen start pas als de auto meer dan 3 % onder het doel zit. |
| *Goal reached* | Laadpaal gepauzeerd of terug naar de vorige modus. |
| *EV already charging, left alone* | HESC neemt nooit een laadbeurt over die hij niet zelf startte. |

**Daarna.** Met *Terug naar zonnestand* ingevuld pauzeert HESC de laadpaal na het netladen, kijkt of
de pauze echt is aangekomen (laadpalen via de cloud zijn vaak een minuut te laat) en zet de
laadpaal daarna terug naar laden op zon. Zonder dat veld blijft de laadpaal gepauzeerd, zodat de
auto zich niet zelf van het net bijlaadt; HESC zet hem weer aan voor zon, een nieuw plan, of als
je de stekker eruit haalt.

**Controle van het doel.** Op de klaar-tijd vergelijkt HESC de accustand met het doel. Meer dan
3 % eronder: een rode melding *EV goal missed* (ook op je telefoon).

**Minimumlading** (naar keuze): onder het minimumniveau wordt de auto binnen de ingestelde tijd
tot dat niveau geladen, in de goedkoopste kwartieren van die periode.

## Laadstroom

Mag HESC de laadstroom instellen, dan verlaagt hij die terwijl het laadplan van het net laadt:
de auto neemt dan ongeveer wat de zon geeft, nooit minder dan 6 A. Alleen zolang de auto op tijd
vol is met 30 minuten speling; anders volle stroom. Daarna gaat de stroom terug naar wat hij was,
ook na een herstart. HESC meet zelf het aantal fases en doet pas iets als hij dat weet. Hooguit
één wijziging per minuut; niets in schaduwmodus.

## Thuisbatterij en auto (kickstart)

Op een zonnige ochtend pakt de thuisbatterij alle zon die over is, dus de laadpaal ziet geen
overschot en de auto wacht. HESC regelt de thuisbatterij nooit zelf; hij start alleen de
laadpaal.

**Kickstart** als dit allemaal klopt: de auto is aangesloten, wacht op laden op zon en is niet
vol; de thuisbatterijen laden al een paar minuten met meer dan 500 W; de voorzichtige
verwachting ligt op of boven de startdrempel; de zon die vandaag nog komt is duidelijk meer dan
de thuisbatterijen nog nodig hebben (1,2 × wat ze nodig hebben, plus *Minimale zon over voor de
auto*); geen laadplan en geen vrijgave bezig; minder dan *Kickstarts per dag* vandaag, en minstens
30 minuten na de vorige.

De volgorde:
1. HESC start de laadpaal.
2. De regeling van je thuisbatterij ziet de auto laden en stopt met de thuisbatterij vullen.
3. HESC pauzeert de laadpaal en wacht tot de pauze echt is aangekomen.
4. HESC zet de laadpaal terug naar laden op zon. Die ziet nu het overschot en laadt op zon.

Stap 4 moet komen terwijl de regeling van je thuisbatterij die nog vasthoudt. HESC geeft daarom
terug 15 seconden nadat de start/stop-schakelaar van de laadpaal uit ging (het moment dat Home
Assistant dat zag, ook als een cloud-laadpaal de pauze laat doorgeeft). Voor de regeling van je
thuisbatterij is er een sensor *Kickstart: overdracht bezig*: die staat aan van stap 3 tot de
laadpaal weer op zon laadt. Houd de thuisbatterij vast zolang hij aan staat, ook als de laadpaal
even 0 W laat zien.

**Terug naar de thuisbatterij.** Laadt de auto 10 minuten of langer op zon en is de zon die
vandaag nog komt maar net genoeg voor de thuisbatterijen, dan pauzeert HESC de laadpaal en zet
hem terug op wachten op zon, zodat de thuisbatterij 's avonds vol is.

### Je thuisbatterijregeling aan HESC koppelen

Bepaalt de regeling van je thuisbatterij zelf wanneer de auto laadt (bijvoorbeeld om te stoppen
met de thuisbatterij vullen, zoals in stap 2)? Geef haar dan deze twee entiteiten van HESC:

| Entiteit | Gebruik hem voor |
|---|---|
| **Laadvermogen auto** (`sensor.hesc_v3_ev_charging_power`) | Het laadvermogen van de auto. Gebruik hem in plaats van de vermogenssensor van je laadpaal: hij staat op 0 W zodra de laadpaal gepauzeerd is, ook als de laadpaal nog minutenlang zijn laatste vermogen meldt (Wallbox). |
| **Kickstart: overdracht bezig** (`binary_sensor.hesc_v3_kickstart_hand_back_in_progress`) | Houd de thuisbatterij vast zolang hij aan staat. |

Beide werken met elke laadpaal waarvan HESC de start/stop- of pauzeschakelaar kent, of waarvan de
status zegt dat hij gepauzeerd is. Ze zijn zo snel als je laadpaal meldt: een cloud-laadpaal kan
een minuut of meer achterlopen, en HESC werkt elke 30 seconden bij. Alleen een eigen kWh-meter in
de groep van de laadpaal is echt direct.

Met een thuisbatterij kun je de laadpaal in de zonnestand gepauzeerd laten staan; HESC start hem
met een kickstart als er genoeg zon over is. **Zonder thuisbatterij is er geen kickstart:** laat de
laadpaal dan niet gepauzeerd staan, anders laadt de auto nooit op zon.

## Accustand van de auto

Alle onderdelen van HESC gebruiken één accustand. HESC neemt de eerste van deze die een waarde
heeft:
1. de accustand-sensor uit het instelscherm;
2. een tweede accustand-sensor van dezelfde auto, die HESC zelf vindt;
3. de laatste stand van deze laadsessie, plus 90 % van de kWh die sindsdien geladen is;
4. de gebruikelijke stand bij het aansluiten over de laatste 14 dagen (vanaf 5 keer aansluiten).

Een geschatte of onbekende stand geeft een oranje melding. Helemaal geen sensor? Het
instelscherm helpt je er een voor jouw auto te vinden.

## Prijzen, kosten en meldingen

- **Prijzen:** alle onderdelen lezen één prijslijst per kwartier; zie
  [05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#energieprijzen). De
  **prijsvoorspelling** leert je markt kennen uit je eigen prijsgeschiedenis en vult de
  kwartieren na de laatste bekende prijs.
- **Kosten:** terwijl de auto laadt, krijgt het deel dat van het net komt de prijs van dat
  kwartier; de rest telt als zon (ook energie uit een thuisbatterij).
- **Meldingen:** P1 (rood, ook op je telefoon): het doel is gemist of er is een echte storing. P2
  (oranje, ook op je telefoon): er ontbreekt een sensor, HESC werkt door. P3 (grijs, alleen op
  *Overzicht*): ter info.

## Geschiedenis en rapport

HESC schrijft per gebeurtenis en sessie één regel in zijn geschiedenis in `/config/hesc_v3/`,
zo'n 50 regels op een zonnige dag. **Rapport maken** (op *Overzicht*, onder *Status*) maakt daar een
pagina van met je sessies, het advies en hoe betrouwbaar je bronnen zijn.
