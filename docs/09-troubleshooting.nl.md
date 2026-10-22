# 09 · Problemen oplossen

*English: [09-troubleshooting.md](09-troubleshooting.md)*

**In het kort**
- De meeste meldingen op het dashboard zijn normaal: HESC vertelt waar hij op wacht.
- Vlak na een herstart van Home Assistant zijn sommige kaarten ongeveer een minuut leeg. Dat
  herstelt zich vanzelf.
- Is er echt iets mis? Kijk naar de controle op de pagina *Instellingen* en de kaart *Live* op
  *Overzicht*, en druk op **Rapport maken**.

## Na een herstart van Home Assistant

| Wat je ziet | Wat het betekent |
|---|---|
| De kaart *Status* of andere kaarten zijn even leeg of tonen een fout | Normaal. HESC vult het dashboard ongeveer een minuut na de start. |
| De accustand van de auto klopt een paar minuten niet (bijvoorbeeld 99,9 %) | Sommige auto-integraties sturen een verkeerde waarde tot hun volgende update. HESC rekent opnieuw zodra de juiste waarde binnenkomt. Zie [05 · Laadpalen en bronnen](05-chargers-and-sources.nl.md#de-accustand-van-je-auto). |
| Een veld in het instelscherm is leeg | De integratie van je laadpaal of meter was nog niet klaar. HESC zoekt opnieuw zodra Home Assistant is opgestart. Nog steeds leeg? Vul het in onder *Instellingen → Apparaten & diensten → HESC v3 → Configureren*. |
| De controle op *Instellingen* toont een rood ❌ | Wacht een paar minuten. Na 15 minuten nog rood? Dan ontbreekt er echt iets; de controle vertelt wat. |

## Installatie en dashboard

| Probleem | Controleer |
|---|---|
| Knoppen tussen de dashboardpagina's doen niets | Het adres van het dashboard moet precies `hesc-v3` zijn. Zie [01 · Installatie](01-installation.nl.md#3-het-dashboard-toevoegen). |
| Grafieken, de balk *Verwacht laden op zon* of de kostentegels ontbreken, of een kaart meldt *Custom element doesn't exist: hesc-…* | De eigen kaarten van HESC laden met de integratie: herstart Home Assistant na het installeren of bijwerken van HESC en ververs daarna de browser (op de telefoon: app sluiten en opnieuw openen). Kaarten uit HACS zijn niet nodig. |
| De HESC-iconen ontbreken | Ververs de browser (op de telefoon: app sluiten en opnieuw openen). |
| HESC vindt mijn laadpaal niet | Kies het type laadpaal opnieuw op *Instellingen* en druk op **Opnieuw zoeken**. Staat hij er niet tussen? Kies *Other (manual)* en vul de velden zelf in. |

## Laden op zon

| Melding | Wat het betekent |
|---|---|
| `Waiting for inputs: …` | De genoemde bron is leeg of niet beschikbaar. Kijk op de kaart *Live* en in het instelscherm. |
| `HPVC is not limiting PV — nothing to release` | Normaal: HPVC begrenst je zonnepanelen niet, dus de laadpaal kan de zon al gebruiken. |
| `Waiting for HPVC to confirm the release (x/5 min, …)` | Even normaal: HPVC maakt eerst iets met een hogere voorrang af. |
| `HPVC has no external release interface (needs HPVC 1.5.1 or newer)` | Werk HPVC bij. |
| `EV already full, no release needed` | De auto staat op *Auto telt als vol bij*. |
| `Charger not in solar mode` | De laadpaal staat niet in de stand voor laden op zon (bijvoorbeeld Eco), of de extra zonneschakelaar staat uit. |
| `Forecast too low` | De voorzichtige verwachting ligt onder de startdrempel. |
| `Cooldown until …` | Er is net een vrijgave afgelopen; HESC wacht even voordat hij het opnieuw probeert. |
| `Maximum release attempts reached today` | Vandaag zijn te veel vrijgaves mislukt. Om middernacht begint het opnieuw. |
| Het fase-advies blijft op *aan het meten* | De eerste weken normaal: het heeft genoeg zonnige dagen nodig. Het heeft ook het netvermogen per fase nodig in het instelscherm. |

**De laadpaal start niet als HESC het vraagt, of start als het niet moet.** Kijk of er een
laadschema staat in de app van de laadpaal of in een andere integratie, en zet het uit. Na een
update van de app of de firmware kan er vanzelf een schema bijkomen.

## Laadplan

| Melding | Wat het betekent |
|---|---|
| `Grid charging not set up …` | Vul de start/stop-schakelaar of de modus "nu laden" in op *Instellingen → Geavanceerd → Laadplan en meldingen*. |
| `No active plan` | Zet het plan *één vaste dag per week* of het weekplan aan. Zonder plan laadt HESC alleen op zon en bij goedkope kansen. |
| `Waiting for the next planned quarter` | Normaal. De geplande kwartieren staan in de prijsgrafiek. |
| `Final check: below goal, charging to goal` | Normaal in het laatste uur vóór de klaar-tijd als de auto nog onder zijn doel zit. HESC laadt dan naar het doel, wat de prijs ook is. |
| `EV already charging, left alone` | De auto laadde al (bijvoorbeeld op zon). HESC neemt het niet over. |
| `Finished, charger stopped by itself` | De laadpaal nam een paar minuten geen vermogen af (auto vol of eigen grens). |
| `Cheap chance skipped: enough sun today (…)` | Normaal: de zon dekt naar verwachting later vandaag wat nodig is. |
| *Prijzen niet beschikbaar* | De prijssensor geeft nu geen prijzen. Kijk bij *Prijsbron* en *Prijssensor* op *Instellingen → Geavanceerd → Laadplan en meldingen*, en naar de prijsintegratie zelf. |
| Verkeerde valuta of kleine eenheid | *Valuta* → *Automatic* haalt hem uit de prijssensor; kies je valuta zelf als de sensor het niet zegt. |
| Prijzen alleen tot vanavond bekend | Normaal voordat de prijzen van morgen bekend zijn (rond 13:00). Het plan rekent dan met verwachte prijzen en wordt later vaster. |
| Het weekplan doet niets | Kijk bij **Vakantiemodus** onder het weekplan. |
| Melding *Charger fault* | HESC heeft 3 keer geprobeerd de laadpaal weer aan te zetten. Controleer de laadpaal en de cloudverbinding. |

## Thuisbatterij en auto (kickstart)

Staat op *Overzicht* onder *Huidige stand* zolang de auto is aangesloten.

| Melding | Wat het betekent |
|---|---|
| `Not set up: …` | Vul de start/stop-schakelaar, *Terug naar zonnestand* en de velden van de thuisbatterij in op *Instellingen → Thuisbatterij en auto*. |
| `Waiting: home batteries not taking the sun` | Normaal: de thuisbatterij laadt niet, dus de laadpaal ziet het overschot al. |
| `Home batteries first for the rest of today` | Niet genoeg zon meer voor allebei; de thuisbatterij krijgt hem. |
| `Kickstart: charger started …` → `Kickstart: charger paused …` → `Kickstart: waiting for the charger …` | Een kickstart is bezig: de laadpaal start, de regeling van de thuisbatterij ziet de auto en stopt met batterijen laden, de laadpaal gaat terug naar wachten op zon. |
| `Charge plan has the charger` | Normaal: de kickstart wacht op het laadplan. |
| `Done for today (…)` | Het maximale aantal kickstarts is bereikt, of de thuisbatterij kreeg voorrang. Morgen weer. |

## Meldingen

De regel naast het logo op *Overzicht* toont *✓ Geen meldingen*, of de belangrijkste melding. Tik erop om
naar de plek te gaan waar je iets kunt doen.

| Melding | Betekenis |
|---|---|
| **P1** (rood, ook op je telefoon) | Het laaddoel is gemist of kan niet bevestigd worden, of er is een echte storing. Blijft 12 uur staan. |
| **P2** (oranje) | Er ontbreekt een sensor, maar HESC werkt door (bijvoorbeeld een geschatte accustand). |
| **P3** (grijs) | Ter info. Twee uur. |

**Geen meldingen op je telefoon?** Voeg op *Instellingen*, onder *Meldingen naar je telefoon*, je
telefoon toe en stuur een testmelding. Alleen P1 en P2 gaan naar de telefoon.

## Kosten

| Probleem | Controleer |
|---|---|
| Geen knop *Kosten* op *Overzicht* | Zet de kostenpagina aan op *Instellingen*. |
| Kosten te hoog of te laag | Controleer *all-in*, of de opslag en btw, op *Instellingen*. Een wijziging rekent de hele geschiedenis opnieuw. |
| Een waarschuwing over netstroom zonder prijs | Er is van het net geladen terwijl er geen prijs bekend was. Dat wordt apart geteld. |
