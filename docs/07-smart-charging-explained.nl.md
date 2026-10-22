# 07 · Slim laden uitgelegd

*English: [07-smart-charging-explained.md](07-smart-charging-explained.md)*

**In het kort**
- Stekker erin als je thuiskomt, en zorg dat je plan klopt met je vertrektijd. De rest doet HESC.
- HESC gebruikt eerst gratis zon, dan de goedkoopste kwartieren van het net, en houdt altijd een
  vangnet zodat de auto op tijd klaar is.
- Na ongeveer twee weken kent HESC je prijzen goed genoeg om vooruit te kijken.
- Dezelfde tekst zit in het dashboard: het knopje *Uitleg* op *Overzicht*.

## Jouw deel

Na ongeveer twee weken werkt HESC bijna helemaal vanzelf. Jouw deel is klein:

1. **Stekker erin** als je thuiskomt.
2. **Zorg dat je plan klopt met je vertrektijd.** Een weekplan voor je vaste dagen (bijvoorbeeld
   *80 % op werkdagen om 07:30*), en het plan *één vaste dag per week* voor één extra dag (*100 % op
   zaterdag om 09:00*).

Tussen het moment dat je aansluit en het moment dat je vertrekt, zoekt HESC de goedkoopste manier
om de auto op het gewenste niveau te krijgen.

## Waarom de eerste twee weken ertoe doen

Het meeste werkt vanaf de eerste dag: laden op zon, het laadplan, het vangnet en de controle van
je doel.

Eén ding wordt beter met de tijd: **vooruitkijken naar prijzen.** De prijzen voor morgen komen
rond 13:00 uit. Daarvoor weet niemand ze. HESC vult dat gat met een verwachte prijs, op basis van
wat de prijzen de afgelopen 14 dagen bij jou deden en hoe zonnig het morgen wordt (zonnige dagen
zijn meestal goedkoop rond het middaguur en duur in de avond).

- **De eerste dag:** nog geen verwachte prijzen. HESC plant met de prijzen die bekend zijn. Het
  vangnet zorgt dat de auto toch klaar is.
- **Na één volle dag:** een ruwe verwachting, gewoon het patroon van gisteren. Verwachte prijzen
  verschijnen als grijze staven in de prijsgrafiek en het plan mag ze gebruiken.
- **Vanaf dag 3:** het gemiddelde van alle volle dagen tot nu toe.
- **Vanaf dag 14:** twee volle weken van je eigen prijzen.
- **Daarna elke week:** HESC stelt bij hoe zon en prijs op jouw markt samenhangen.

Een bekende prijs gaat altijd voor op een verwachte, tenzij de verwachte duidelijk goedkoper is
(2 cent per kWh of meer). Zodra de echte prijzen er zijn, gebruikt het plan die.

## De volgorde die HESC aanhoudt

Elke 30 seconden kijkt HESC naar de auto, de zon, de prijzen en je plan, en stelt steeds dezelfde
vragen in dezelfde volgorde:

| # | Vraag | Wat er gebeurt |
|---|---|---|
| 1 | **Is er zon?** | Je laadpaal laadt op zon in zijn eigen stand daarvoor (bijvoorbeeld Eco), zoals altijd. Met HPVC vraagt HESC eerst aan HPVC om de zon door te laten. HESC rekent de zon mee in het plan, zodat het geen stroom koopt die de zon toch levert. |
| 2 | **Is het een van de geplande goedkoopste kwartieren?** | HESC zet de laadpaal dat kwartier aan op netstroom. |
| 3 | **Raakt de tijd op?** | **Vangnet:** is de resterende tijd nog maar net genoeg om het doel te halen, dan start HESC het laden, wat de prijs ook is. |
| 4 | **Is het het laatste uur voor vertrek en zit de auto nog onder het doel?** | **Eindcontrole:** HESC laadt tot je doel, wat de prijs ook is. |
| 5 | **Is de prijs nu erg laag?** | **Goedkope kans:** HESC laadt nu, ook zonder plan, *tenzij* er later vandaag genoeg zon verwacht wordt. |
| 6 | **Zit de auto onder het minimum dat je hebt ingesteld?** | **Minimumlading** (optioneel, standaard uit): de auto krijgt binnen een paar uur minstens dat niveau, in de goedkoopste kwartieren. |
| 7 | Niets van dit alles | HESC wacht. Het dashboard zegt waarom, bijvoorbeeld *Waiting for the next planned quarter*. |

Voor alles hierboven gelden een paar regels:

- **3 % marge.** HESC laadt pas van het net als de auto meer dan 3 % onder het doel zit. Een auto
  op 78 % met een doel van 80 % blijft met rust; op 76,9 % wordt er geladen.
- **Welk doel?** Met een actief plan: het doel van dat plan. Zonder plan: *Auto telt als vol bij*
  (standaard 80 %). Een goedkope kans vult nooit een auto die al als vol telt.
- **HESC maakt alleen ongedaan wat het zelf startte.** Start je zelf met laden, of laadt de auto
  al op zon, dan laat HESC het met rust.
- **Na het laden van het net blijft de laadpaal niet aan staan.** Anders kan de auto stilletjes in
  de dure avondpiek bijladen van het net. Is *Terug naar zonnestand* ingevuld (Wallbox: *Resume
  schedule*, wordt voor je ingevuld), dan zet HESC de laadpaal op pauze, controleert dat de pauze
  echt is doorgekomen (laadpalen via de cloud reageren ongeveer een minuut later) en zet hem
  daarna terug op laden op zon. Zonder dat veld blijft de laadpaal op pauze tot er genoeg zon is,
  de auto meer dan 3 % onder het doel zakt, een plan start of je de stekker eruit haalt.

## Hoe het plan de goedkoopste uren kiest

Stel: je sluit om 18:00 aan met de auto op 40 %, en je weekplan zegt *80 % om 07:30*.

1. **Hoeveel is er nodig?** 40 % van een accu van 60 kWh = 24 kWh.
2. **Hoeveel komt er van de zon vóór 07:30?** Niets, het is nacht. (Bij een plan voor zaterdag
   14:00 zou de ochtendzon wel meetellen.)
3. **Hoe lang duurt dat van het net?** Bij 11 kW: iets meer dan 2 uur, dus 9 kwartieren.
4. **Welke 9 kwartieren?** De goedkoopste tussen nu en 07:30. Meestal ergens in de nacht.

De geplande kwartieren zie je **amber** in de prijsgrafiek op het tabblad *Laadplan*. Staat
het plan niet aan, dan laat de grafiek zien wat het *zou* doen, met het woord *voorbeeld*.

## Goedkope kansen en de zon

*Goedkope kansen pakken* laadt zodra de prijs onder *Goedkoop onder* zakt, ook zonder plan. Die
momenten zie je **blauwgroen** in de prijsgrafiek.

Een goedkoop moment in de ochtend is geen koopje als de middagzon de auto gratis had kunnen
vullen. Daarom kijkt HESC eerst naar de zonverwachting voor de rest van de dag. Dekt de zon naar
verwachting wat de auto nog nodig heeft, met 20 % over, dan wordt de goedkope kans overgeslagen:
*Cheap chance skipped: enough sun today*.

## Hoeveel zon je laadpaal nodig heeft

Een laadpaal die op zon laadt, start pas als er genoeg zon over is. Hoeveel verschilt per merk:
van ongeveer 0,5 kW op één fase (Wallbox Eco) tot ongeveer 4 kW op drie fases (het
standaardminimum van 6 A per fase). HESC weet dat per merk, en het advies voor de startdrempel
komt nooit lager uit dan wat je laadpaal nodig heeft. De tabel staat in [05 · Laadpalen en
bronnen](05-chargers-and-sources.nl.md#hoeveel-zon-een-laadpaal-nodig-heeft-om-te-starten).

**Netladen en zon tegelijk.** Laat je laadpaal HESC de laadstroom instellen (Wallbox: *Maximum
charging current*, daarvoor is een beheerdersaccount nodig), dan zet HESC de laadpaal zachter
zolang hij van het net laadt en de zon schijnt. Er komt dan meer uit je panelen en minder uit het
net. Dit is normaal; je hoeft niets aan te zetten. HESC doet het alleen zolang de auto op tijd
vol is, en zet de stroom daarna terug. Of je laadpaal op 1 of 3 fases laadt, ziet HESC zelf.

**Fase-advies.** Sommige laadpalen starten pas als er op elke fase genoeg zon over is (een Wallbox
op Eco ongeveer 480 W per fase, een Easee 6 A per fase). Liggen je panelen ongelijk over de fases,
dan bepaalt de zwakste fase wanneer je auto op zon kan laden. Heb je het netvermogen per fase
ingevuld, dan meet HESC dit op zonnige dagen en vertelt wat hij zag: eerst de verdeling over de
fases, later hoe vaak de zwakste fase je laadpaal tegenhield. Het is alleen advies; HESC
verandert er niets mee.

## Zonder zonverwachting

HESC werkt ook zonder verwachting. Hij laadt dan op de zonnestroom die hij meet, en het plan
rekent helemaal geen zon mee, zodat de auto nooit te laat is. De kickstart staat uit, want die
moet weten hoeveel zon er nog komt. Zie [05 · Laadpalen en
bronnen](05-chargers-and-sources.nl.md#zonverwachting).

## Thuisbatterij en auto

*Naar keuze, standaard uit. Alleen voor huizen met een thuisbatterij.*

Op een zonnige ochtend pakt de thuisbatterij meestal eerst alle zon die over is. De laadpaal ziet
dan geen overschot en wacht, soms tot de thuisbatterij 's middags vol is. Op een dag met minder
zon kan de auto dan niets krijgen.

Met **Thuisbatterij en auto** aan helpt HESC de auto aan de beurt te komen:

1. **Kickstart.** De auto hangt aan de laadpaal en wacht op zon, de thuisbatterij laadt al een
   paar minuten, en de voorzichtige verwachting zegt dat er nu genoeg zon is. HESC kijkt naar de
   rest van de dag: is er duidelijk meer zon over dan de thuisbatterij nog nodig heeft (met 20 %
   over, en minstens *Minimale zon over voor de auto*)? Dan:
   1. start HESC de laadpaal;
   2. ziet de regeling van je thuisbatterij de auto laden en stopt die met de thuisbatterij vullen;
   3. zet HESC de laadpaal op pauze en wacht tot de pauze echt is doorgekomen;
   4. zet HESC de laadpaal terug op laden op zon, en die krijgt nu de zon die vrijkwam.
2. **Terug naar de thuisbatterij.** Later op de dag, als de resterende zon nog maar net genoeg is
   om de thuisbatterij te vullen, zet HESC de laadpaal weer op wachten, zodat de thuisbatterij 's
   avonds vol is. Daarna volgt die dag geen nieuwe kickstart.

Tijdens de korte start kan de thuisbatterij heel even wat stroom aan de auto leveren. Dat is
normaal.

HESC stuurt de thuisbatterij nooit zelf. Hij doet niets terwijl een laadplan laadt, tijdens een
vrijgave van HPVC of na zonsondergang, en hoogstens een paar keer per dag (*Kickstarts per dag*,
standaard 3, minstens 30 minuten ertussen).

Wat je invult (*Instellingen*, *Thuisbatterij en auto* → *Opties*): de standsensor(en) van je
thuisbatterij, de vermogenssensor(en) (positief = laden) en de totale grootte in kWh. Het heeft
ook de start/stop-schakelaar van de laadpaal en *Terug naar zonnestand* nodig; bij een Wallbox worden
die voor je ingevuld.

## Wat gaat het kosten?

Het knopje **Verwachte laadkosten** op *Overzicht* toont wat het actieve plan naar verwachting van het
net kost: de prijs van elk gepland kwartier, plus je opslag en btw (of de all-in-prijs). Het telt
alleen netladen dat echt gaat gebeuren; zonder actief plan, als de auto zijn doel al heeft, of
terwijl de auto op zon laadt, staat er 0,00.

**Wat heeft het gekost?** Tik op het knopje **Kosten**. Per dag, week, maand, kwartaal of jaar zie
je hoeveel er in de auto ging, hoeveel van de zon kwam (groen) en van het net (grijs), en wat het
netdeel kostte. Je opslag, btw en de waarde van een zonne-kWh stel je één keer in onder *Instellingen
→ Laadkosten*; de hele geschiedenis rekent mee. **Exporteren naar spreadsheet (CSV)** maakt twee
bestanden voor Excel.

## Situaties

### "Ik rijd elke werkdag naar mijn werk"

Maak een **weekplan**: vink de dagen aan, zet je vertrektijd en het niveau dat je wilt. Laat het
aan staan. Stekker erin als je thuiskomt. Klaar.

### "Ik ga zaterdag op reis"

Gebruik **één vaste dag per week**: kies *Saturday*, je vertrektijd en bijvoorbeeld 100 %, en zet
het aan. Staan beide plannen aan, dan wint de vroegste; je weekplan gaat gewoon door. Heb je het
maar één keer nodig? Zet *Actief* na de reis weer uit.

### "De auto blijft een paar dagen thuis"

Geen plan nodig. De auto laadt op zon, pakt goedkope kansen, en verder blijft de laadpaal op
pauze. Pas als de auto meer dan 3 % onder *Auto telt als vol bij* zakt, laadt HESC hem bij.

### "Ik kom thuis met een bijna lege accu en heb de auto vanavond misschien nog nodig"

Zet **Minimumlading** aan (*Instellingen*, *Aan*). Standaard: minstens 20 % binnen 3 uur, in de
goedkoopste kwartieren van die 3 uur, of meteen als er geen prijzen bekend zijn.

### "Ik heb een thuisbatterij en de auto krijgt nooit zon"

Zet **Thuisbatterij en auto** aan en vul je thuisbatterij in. Zie [Thuisbatterij en
auto](#thuisbatterij-en-auto) hierboven.

### "Ik heb de auto nu nodig, laat het plan maar"

Start zelf met laden (app, knop op de laadpaal of de eigen stand van de laadpaal). HESC ziet dat
de auto al laadt en laat hem met rust.

### "Ik heb laat aangesloten; is er nog tijd?"

HESC houdt dat steeds in de gaten. Is de resterende tijd nog maar net genoeg, dan start het
vangnet meteen. Wordt het doel toch niet gehaald, dan krijg je op je vertrektijd een melding:
*EV goal missed*, met de stand die gehaald is.

### "Morgen wordt het zonnig"

Het plan rekent de zon vooraf mee (voorzichtige verwachting, min een beetje voor het huis), dus
het koopt minder van het net. Goedkope kansen die de zon overbodig maakt, worden overgeslagen.

### "De prijzen voor morgen zijn nog niet bekend"

Normaal vóór ongeveer 13:00. Na de eerste dagen gebruikt het plan verwachte prijzen (grijze
staven) en wordt het vaster zodra de echte prijzen er zijn.

### "Mijn auto stopt zelf bij 80 %"

Veel auto's hebben een eigen laadgrens. Ligt die lager dan je doel, dan stopt de laadpaal vanzelf
en toont HESC *Finished, charger stopped by itself*. Zet je doel op of onder de grens van de auto,
of verhoog die grens in de auto.

### "De laadpaal reageerde niet"

Laadpalen via de cloud negeren soms een opdracht. HESC controleert en probeert opnieuw: een
geweigerde start of hervatting na 5 minuten, een geweigerde pauze na 30 minuten, elk hoogstens
3 keer.

### "Home Assistant is tijdens het laden herstart"

HESC gebruikt het laatste geldige plan nog tot 10 minuten, zodat een lopende lading niet stopt.
Vlak na een herstart zijn sommige kaarten ongeveer een minuut leeg, en kan de accustand van de
auto een paar minuten niet kloppen. Zie [09 · Problemen
oplossen](09-troubleshooting.nl.md#na-een-herstart-van-home-assistant).

### "Ik ga op vakantie"

Zet **Vakantiemodus** aan, onder het weekplan. Het weekplan rust; je dagplan blijft actief, zodat
de auto vol kan zijn op de dag dat je terugkomt. Laden op zon gaat gewoon door. Vul eventueel
**Vakantie tot** in: de dag na die datum gaat de vakantiemodus vanzelf uit.

## Wat je één keer instelt

| Instelling | Waar | Standaard | Tip |
|---|---|---|---|
| *Bruikbare accucapaciteit* | *Laadplan* | 60 kWh | Wat je auto echt kan gebruiken |
| *Laadvermogen van het net* | *Laadplan* | 11 kW | Iets onder wat je laadpaal echt levert geeft wat marge |
| *Goedkope kansen pakken* / *Goedkoop onder* | *Laadplan* | eigen keuze / 0,05 per kWh | In de munt van je prijzen |
| *Auto telt als vol bij* | *Instellingen*, blok *Extra* | 80 % | Het niveau dat zonder plan wordt vastgehouden |
| Eindcontrole | *Instellingen*, *Laadplan en meldingen* | 60 min | Hoe lang voor vertrek HESC laadt, wat de prijs ook is |
| *Minimumlading* | *Instellingen* | uit (20 %, 3 uur) | *Aan* + *Opties* |
| *Thuisbatterij en auto* | *Instellingen* | uit (3 per dag) | Alleen met een thuisbatterij |
| *Terug naar zonnestand* | *Instellingen*, *Laadplan en meldingen* | ingevuld bij Wallbox | Zet de laadpaal na netladen terug op laden op zon |
| Telefoons voor meldingen | *Instellingen*, *Laadplan en meldingen* | geen | Test met *Testmelding sturen* |
| Ochtendoverzicht | *Instellingen*, *Laadplan en meldingen* | uit (06:00) | Eén bericht per dag: accustand, volgend plan, zon vandaag, gisteren |
| Laadkosten | *Instellingen*, *Laadkosten* | opslag 0, btw 0, zonne-kWh gratis | Of *all-in* als je prijssensor de volledige prijs geeft |

## Waar je kijkt

- **Status** op *Overzicht*: wat HESC nu doet en waarom.
- **Prijsgrafiek** (*Laadplan*): amber = gepland, blauwgroen = goedkope kans, grijs = verwachte
  prijs.
- **Meldingenregel** naast het logo: *✓ Geen meldingen*, of wat aandacht nodig heeft. Tik erop om naar
  de plek te gaan waar je iets kunt doen.
- De knopjes **Verwachte laadkosten** en **Kosten** op *Overzicht*.
- **Controle** op *Instellingen*: klopt er iets niet, dan gaat dat onderdeel vanzelf open.
- **Rapport** (*Rapport maken* onder Status): alles wat HESC gemeten en besloten heeft.

Zie ook: [04 · Hoe het werkt](04-how-it-works.nl.md) · [06 · Dashboard](06-dashboard.nl.md) ·
[08 · Een dag met HESC](08-a-day-with-hesc.nl.md)
