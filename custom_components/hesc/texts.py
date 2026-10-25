"""Dutch and German for the texts HESC makes itself (since 3.1.0).

HESC's logic keeps working in English: the status sensors, the history and every comparison in
HESC and in a user's own automations stay exactly as they were. Only what a person reads is
translated:

- the status sensors get the attributes ``nl`` and ``de`` (the dashboard in that language shows them);
- notifications, the morning summary and the one-line phone summary follow the language of Home
  Assistant (`translate(text, hass.config.language)`).

A text is cut into parts at " · " and every part is looked up in RULES (a whole-part match).
A part without a rule stays English, so a new or unknown text is never lost, only untranslated
(tests/test_texts.py lists every text the scenarios produce and checks each has a translation).
Day names before a date or time ("Sat 31-10", "Tue 07:00") and decimal points follow the language.
"""
from __future__ import annotations

import re
from collections.abc import Callable

LANGS = ("nl", "de")
SEP = " · "

# Part of a text (whole match) -> Dutch, German. In a translation {1}, {2}, ... are the matched
# groups as they are; {t1}, {t2}, ... are the groups translated as a part themselves.
_R: list[tuple[str, str, str]] = [
    # ---- solar charging and the HPVC release (state, reason, last action) ----
    (r"Idle", "Rust", "Ruhe"),
    (r"Disabled", "Uit", "Aus"),
    (r"Release requested, waiting for HPVC", "Vrijgave gevraagd, wacht op HPVC", "Freigabe angefragt, warte auf HPVC"),
    (r"Release — waiting for EV", "Vrijgave — wacht op de auto", "Freigabe — warte auf das Auto"),
    (r"Release — EV charging", "Vrijgave — auto laadt", "Freigabe — Auto lädt"),
    (r"Release ended: (.+)", "Vrijgave beëindigd: {t1}", "Freigabe beendet: {t1}"),
    (r"HESC disabled", "HESC staat uit", "HESC ist aus"),
    (r"standalone mode switched on", "zelfstandige stand aangezet", "Standalone-Modus eingeschaltet"),
    (r"inputs unavailable", "gegevens niet beschikbaar", "Eingangswerte nicht verfügbar"),
    (r"EV disconnected or charger not in solar mode", "auto losgekoppeld of laadpaal niet in zonnestand",
     "Auto abgesteckt oder Wallbox nicht im Solarmodus"),
    (r"sunset", "zonsondergang", "Sonnenuntergang"),
    (r"HPVC busy \((.*)\), no release confirmation within (\S+) min, request withdrawn",
     "HPVC bezig ({1}), geen bevestiging binnen {2} min, verzoek ingetrokken",
     "HPVC beschäftigt ({1}), keine Bestätigung innerhalb von {2} Min, Anfrage zurückgezogen"),
    (r"EV full", "auto vol", "Auto voll"),
    (r"EV did not start within (\S+) min", "auto startte niet binnen {1} min", "Auto hat nicht innerhalb von {1} Min gestartet"),
    (r"EV stopped charging", "auto stopte met laden", "Auto hat aufgehört zu laden"),
    (r"solar below hold threshold", "zon onder de doorlaadgrens", "Sonne unter der Halteschwelle"),
    (r"maximum release duration", "maximale duur van de vrijgave", "maximale Freigabedauer"),
    (r"Release requested: HESC asked HPVC for full PV, waiting for HPVC to confirm",
     "Vrijgave gevraagd: HESC vroeg HPVC om volle zonnestroom, wacht op bevestiging van HPVC",
     "Freigabe angefragt: HESC hat HPVC um volle PV-Leistung gebeten, warte auf die Bestätigung von HPVC"),
    (r"Release requested: HESC would ask HPVC for full PV, waiting for HPVC to confirm",
     "Vrijgave gevraagd: HESC zou HPVC om volle zonnestroom vragen, wacht op bevestiging van HPVC",
     "Freigabe angefragt: HESC würde HPVC um volle PV-Leistung bitten, warte auf die Bestätigung von HPVC"),
    (r"Conditions met, confirming \((\S+)/(\S+) min\)", "Voorwaarden in orde, even bevestigen ({1}/{2} min)",
     "Bedingungen erfüllt, kurz bestätigen ({1}/{2} Min)"),
    (r"Waiting for inputs: (.+)", "Wacht op gegevens: {t1}", "Warte auf Eingangswerte: {t1}"),
    (r"forecast now", "verwachting nu", "Prognose jetzt"),
    (r"forecast \+30m", "verwachting +30 min", "Prognose +30 Min"),
    (r"PV power", "zonnestroom", "PV-Leistung"),
    (r"EV power", "laadvermogen auto", "Ladeleistung Auto"),
    (r"EV connected", "auto aangesloten", "Auto angeschlossen"),
    (r"charger mode", "stand laadpaal", "Modus der Wallbox"),
    (r"HPVC enabled", "HPVC aan", "HPVC an"),
    (r"Night", "Nacht", "Nacht"),
    (r"No EV connected", "Geen auto aangesloten", "Kein Auto angeschlossen"),
    (r"Charger not in solar mode", "Laadpaal niet in zonnestand", "Wallbox nicht im Solarmodus"),
    (r"EV is charging", "Auto laadt", "Auto lädt"),
    (r"Standalone \(no HPVC\): the charger starts on solar by itself",
     "Zelfstandig (zonder HPVC): de laadpaal start zelf op zon", "Standalone (ohne HPVC): die Wallbox startet selbst mit Sonne"),
    (r"HPVC is not limiting PV — nothing to release", "HPVC begrenst de panelen niet — niets vrij te geven",
     "HPVC begrenzt die Paneele nicht — nichts freizugeben"),
    (r"HPVC has no external release interface \(needs HPVC 1\.5\.1 or newer\)",
     "HPVC heeft geen koppeling voor vrijgave (HPVC 1.5.1 of nieuwer nodig)",
     "HPVC hat keine Schnittstelle für die Freigabe (HPVC 1.5.1 oder neuer nötig)"),
    (r"EV already full, no release needed", "Auto al vol, geen vrijgave nodig", "Auto schon voll, keine Freigabe nötig"),
    (r"Forecast too low \(< (\S+) W\)", "Verwachting te laag (< {1} W)", "Prognose zu niedrig (< {1} W)"),
    (r"Irradiance too low \(< (\S+) W/m²\)", "Zonlicht te zwak (< {1} W/m²)", "Einstrahlung zu niedrig (< {1} W/m²)"),
    (r"Cooldown until (\S+)", "Pauze tot {1}", "Pause bis {1}"),
    (r"Maximum release attempts reached today", "Maximaal aantal vrijgaves voor vandaag bereikt",
     "Maximale Zahl an Freigaben für heute erreicht"),
    (r"Release: HPVC confirmed full PV, the charger can start in solar mode",
     "Vrijgave: HPVC bevestigde volle zonnestroom, de laadpaal kan starten in zijn zonnestand",
     "Freigabe: HPVC hat volle PV-Leistung bestätigt, die Wallbox kann im Solarmodus starten"),
    (r"Release: HPVC would confirm full PV, the charger can start in solar mode",
     "Vrijgave: HPVC zou volle zonnestroom bevestigen, de laadpaal kan starten in zijn zonnestand",
     "Freigabe: HPVC würde volle PV-Leistung bestätigen, die Wallbox kann im Solarmodus starten"),
    (r"Waiting for HPVC to confirm the release \((\S+)/(\S+) min, HPVC: (.*)\)",
     "Wacht op bevestiging van de vrijgave door HPVC ({1}/{2} min, HPVC: {3})",
     "Warte auf die Bestätigung der Freigabe durch HPVC ({1}/{2} Min, HPVC: {3})"),
    (r"EV started charging on solar", "Auto begon te laden op zon", "Auto hat mit Sonne zu laden begonnen"),
    (r"Waiting for the charger to start in solar mode \((\S+)/(\S+) min\)",
     "Wacht tot de laadpaal start in zijn zonnestand ({1}/{2} min)", "Warte, bis die Wallbox im Solarmodus startet ({1}/{2} Min)"),
    (r"Release active — EV charging on solar", "Vrijgave actief — auto laadt op zon", "Freigabe aktiv — Auto lädt mit Sonne"),
    # ---- charge plan ----
    (r"Grid charging", "Laden van het net", "Laden aus dem Netz"),
    (r"Grid charging not set up \(Settings → Charge plan\)", "Laden van het net niet ingesteld (Instellingen → Laadplan)",
     "Laden aus dem Netz nicht eingerichtet (Einstellungen → Ladeplan)"),
    (r"Nothing to charge", "Niets te laden", "Nichts zu laden"),
    (r"No active plan", "Geen actief plan", "Kein aktiver Plan"),
    (r"Within (\S+)% of goal \((\S+)%, charges below (\S+)%\)", "Binnen {1}% van het doel ({2}%, laadt onder {3}%)",
     "Innerhalb von {1}% vom Ziel ({2}%, lädt unter {3}%)"),
    (r"Goal reached \((\S+)%\)", "Doel bereikt ({1}%)", "Ziel erreicht ({1}%)"),
    (r"Planned quarter", "Gepland kwartier", "Geplante Viertelstunde"),
    (r"Safety net: only just enough time left", "Vangnet: nog net genoeg tijd", "Sicherheitsnetz: gerade noch genug Zeit"),
    (r"Final check: below goal, charging to goal", "Eindcontrole: onder het doel, laadt tot het doel",
     "Schlusskontrolle: unter dem Ziel, lädt bis zum Ziel"),
    (r"Cheap chance skipped: enough sun today \(~(\S+) kWh for (\S+) kWh\)",
     "Goedkope kans overgeslagen: genoeg zon vandaag (~{1} kWh voor {2} kWh)",
     "Günstige Gelegenheit ausgelassen: genug Sonne heute (~{1} kWh für {2} kWh)"),
    (r"Cheap chance \((\S+) (\S+) ≤ (\S+) (\S+)\)", "Goedkope kans ({1} {2} ≤ {3} {4})", "Günstige Gelegenheit ({1} {2} ≤ {3} {4})"),
    (r"Waiting for the next planned quarter", "Wacht op het volgende geplande kwartier", "Warte auf die nächste geplante Viertelstunde"),
    (r"Minimum charge: below (\S+)%, charging \(ready by (\S+)\)", "Minimumlading: onder {1}%, laadt (klaar om {2})",
     "Mindestladung: unter {1}%, lädt (fertig um {2})"),
    (r"Minimum charge: below (\S+)%, waiting for the cheapest quarter \((\S+)\), ready by (\S+)",
     "Minimumlading: onder {1}%, wacht op het goedkoopste kwartier ({2}), klaar om {3}",
     "Mindestladung: unter {1}%, warte auf die günstigste Viertelstunde ({2}), fertig um {3}"),
    (r"Minimum charge: below (\S+)%, waiting for the cheapest quarter, ready by (\S+)",
     "Minimumlading: onder {1}%, wacht op het goedkoopste kwartier, klaar om {2}",
     "Mindestladung: unter {1}%, warte auf die günstigste Viertelstunde, fertig um {2}"),
    (r"Finished, charger stopped by itself", "Klaar, laadpaal stopte zelf", "Fertig, die Wallbox hat selbst gestoppt"),
    (r"Charger refused to start (\S+) times, no more starts for this plan",
     "Laadpaal weigerde {1} keer te starten, geen nieuwe pogingen voor dit plan",
     "Wallbox hat {1}-mal den Start verweigert, keine weiteren Versuche für diesen Plan"),
    (r"Final check: one more try after refused starts", "Eindcontrole: nog één poging na geweigerde starts",
     "Schlusskontrolle: noch ein Versuch nach verweigerten Starts"),
    (r"EV already charging, left alone", "Auto laadt al, HESC laat hem met rust", "Auto lädt schon, HESC lässt es in Ruhe"),
    (r"charger back in its own solar mode \(grid top-up below (\S+)%\)",
     "laadpaal terug in zijn eigen zonnestand (bijladen van het net onder {1}%)",
     "Wallbox zurück in ihrem eigenen Solarmodus (Nachladen aus dem Netz unter {1}%)"),
    (r"pause refused 3x \(charger stays as it is\)", "pauzeren 3x geweigerd (laadpaal blijft zoals hij is)",
     "Pause 3x verweigert (Wallbox bleibt, wie sie ist)"),
    (r"charger paused by HESC \(on again with sun, below (\S+)% or a plan\)",
     "laadpaal gepauzeerd door HESC (weer aan bij zon, onder {1}% of bij een plan)",
     "Wallbox von HESC pausiert (wieder an bei Sonne, unter {1}% oder bei einem Plan)"),
    (r"Planned: waiting for the first planned quarter", "Gepland: wacht op het eerste geplande kwartier",
     "Geplant: warte auf die erste geplante Viertelstunde"),
    # ---- home battery and EV (kickstart) ----
    (r"Kickstart: charger started, waiting until the home battery control sees the EV",
     "Kickstart: laadpaal gestart, wacht tot de batterijregeling de auto ziet",
     "Kickstart: Wallbox gestartet, warte, bis die Speichersteuerung das Auto sieht"),
    (r"Kickstart: charger paused, back to solar mode in a moment", "Kickstart: laadpaal gepauzeerd, zo terug naar de zonnestand",
     "Kickstart: Wallbox pausiert, gleich zurück in den Solarmodus"),
    (r"Kickstart: waiting for the charger to start on sun", "Kickstart: wacht tot de laadpaal start op zon",
     "Kickstart: warte, bis die Wallbox mit Sonne startet"),
    (r"Kickstart: charger started", "Kickstart: laadpaal gestart", "Kickstart: Wallbox gestartet"),
    (r"Home batteries first: EV paused, charger back to waiting for sun",
     "Eerst de thuisbatterijen: auto gepauzeerd, laadpaal wacht weer op zon",
     "Erst die Hausspeicher: Auto pausiert, Wallbox wartet wieder auf Sonne"),
    (r"Home batteries first: EV paused", "Eerst de thuisbatterijen: auto gepauzeerd", "Erst die Hausspeicher: Auto pausiert"),
    (r"Home batteries first for the rest of today", "Eerst de thuisbatterijen, de rest van vandaag",
     "Erst die Hausspeicher, für den Rest des Tages"),
    (r"Off", "Uit", "Aus"),
    (r"Off: needs a solar forecast \(sun left today\)", "Uit: heeft een zonverwachting nodig (zon over vandaag)",
     "Aus: braucht eine Solarprognose (Sonne übrig heute)"),
    (r"Not set up: start/stop switch and back-to-solar entity needed",
     "Niet ingesteld: start/stop-schakelaar en terug-naar-zon-entiteit nodig",
     "Nicht eingerichtet: Start/Stopp-Schalter und Zurück-zu-Solar-Entität nötig"),
    (r"Not set up: home battery size and level sensors needed", "Niet ingesteld: grootte en laadstand van de thuisbatterij nodig",
     "Nicht eingerichtet: Größe und Ladestand des Hausspeichers nötig"),
    (r"Charge plan has the charger", "Het laadplan heeft de laadpaal", "Der Ladeplan hat die Wallbox"),
    (r"HPVC release running", "HPVC-vrijgave loopt", "HPVC-Freigabe läuft"),
    (r"Sun down", "Zon onder", "Sonne untergegangen"),
    (r"EV charging", "Auto laadt", "Auto lädt"),
    (r"sun left (\S+) kWh, home batteries need (\S+) kWh", "zon over {1} kWh, thuisbatterijen hebben {2} kWh nodig",
     "Sonne übrig {1} kWh, Hausspeicher brauchen {2} kWh"),
    (r"sun left (\S+) kWh, home batteries need (\S+) kWh \(plan needs the EV charge\)",
     "zon over {1} kWh, thuisbatterijen hebben {2} kWh nodig (het plan heeft de lading nodig)",
     "Sonne übrig {1} kWh, Hausspeicher brauchen {2} kWh (der Plan braucht die Ladung)"),
    (r"EV full \((\S+)%\)", "Auto vol ({1}%)", "Auto voll ({1}%)"),
    (r"Sun left today for the home batteries \((\S+) kWh left, (\S+) kWh needed\)",
     "De zon van vandaag is voor de thuisbatterijen ({1} kWh over, {2} kWh nodig)",
     "Die Sonne von heute ist für die Hausspeicher ({1} kWh übrig, {2} kWh nötig)"),
    (r"Waiting: forecast now (\S+) W, start at (\S+) W", "Wacht: verwachting nu {1} W, start bij {2} W",
     "Warte: Prognose jetzt {1} W, Start bei {2} W"),
    (r"Waiting: home batteries not taking the sun", "Wacht: thuisbatterijen nemen de zon niet",
     "Warte: Hausspeicher nehmen die Sonne nicht"),
    (r"Waiting: home batteries charging, check again in (\S+) min", "Wacht: thuisbatterijen laden, opnieuw kijken over {1} min",
     "Warte: Hausspeicher laden, erneut prüfen in {1} Min"),
    (r"Waiting until (\S+) \(30 min between kickstarts\)", "Wacht tot {1} (30 min tussen kickstarts)",
     "Warte bis {1} (30 Min zwischen Kickstarts)"),
    (r"Waiting", "Wacht", "Warte"),
    (r"today (\S+) of (\S+)", "vandaag {1} van {2}", "heute {1} von {2}"),
    # ---- charging current ----
    (r"Off: the charger does not let HESC set its current", "Uit: de laadpaal laat HESC zijn laadstroom niet instellen",
     "Aus: die Wallbox lässt HESC den Ladestrom nicht einstellen"),
    (r"Measuring the charger's phases", "Meet de fasen van de laadpaal", "Misst die Phasen der Wallbox"),
    (r"Waiting: only while the charge plan charges from the grid", "Wacht: alleen als het laadplan van het net laadt",
     "Warte: nur, wenn der Ladeplan aus dem Netz lädt"),
    (r"Waiting: car not charging", "Wacht: auto laadt niet", "Warte: Auto lädt nicht"),
    (r"Waiting for inputs \(grid power, charging current\)", "Wacht op gegevens (netvermogen, laadstroom)",
     "Warte auf Eingangswerte (Netzleistung, Ladestrom)"),
    (r"(\S+) A", "{1} A", "{1} A"),
    (r"following the sun", "volgt de zon", "folgt der Sonne"),
    (r"full current: (.+)", "volle stroom: {t1}", "voller Strom: {t1}"),
    (r"no plan deadline", "geen klaar-tijdstip", "keine Fertig-Zeit"),
    (r"plan is short of time", "het plan heeft te weinig tijd", "der Plan hat zu wenig Zeit"),
    (r"time tight \((\S+) min left, (\S+) min needed at full power\)", "krap in de tijd ({1} min over, {2} min nodig op vol vermogen)",
     "knapp in der Zeit ({1} Min übrig, {2} Min nötig bei voller Leistung)"),
    (r"back to the current from before", "terug naar de stroom van daarvoor", "zurück zum Strom von vorher"),
    (r"next change after (\S+) s", "volgende wijziging na {1} s", "nächste Änderung nach {1} s"),
    (r"putting back HESC's own change", "zet de eigen wijziging van HESC terug", "nimmt die eigene Änderung von HESC zurück"),
    (r"would set (\S+) A", "zou {1} A instellen", "würde {1} A einstellen"),
    # ---- notices, notifications ----
    (r"Battery level from (.+) \((.+) missing\)", "Accustand van {1} ({2} ontbreekt)", "Akkustand von {1} ({2} fehlt)"),
    (r"Battery level estimated \(no sensor value\)", "Accustand geschat (geen sensorwaarde)", "Akkustand geschätzt (kein Sensorwert)"),
    (r"Battery level estimated from usual level \(no sensor value\)", "Accustand geschat uit de gebruikelijke stand (geen sensorwaarde)",
     "Akkustand aus dem üblichen Stand geschätzt (kein Sensorwert)"),
    (r"Battery level unknown: plan waits", "Accustand onbekend: het plan wacht", "Akkustand unbekannt: der Plan wartet"),
    (r"Start threshold (.+) → (.+) \(from your history\)", "Startdrempel {1} → {2} (uit je geschiedenis)",
     "Startschwelle {1} → {2} (aus deinem Verlauf)"),
    (r"(EV goal not confirmed|EV goal missed|Charger refuses to start|Charger fault): (.+)", "{t1}: {t2}", "{t1}: {t2}"),
    (r"(\S+ \S+): battery level unknown, (\S+)% not confirmed\. Check the car\.",
     "{1}: accustand onbekend, {2}% niet bevestigd. Kijk even bij de auto.",
     "{1}: Akkustand unbekannt, {2}% nicht bestätigt. Schau bitte nach dem Auto."),
    (r"(\S+ \S+): (\S+)% instead of (\S+)%\. Check the car\.", "{1}: {2}% in plaats van {3}%. Kijk even bij de auto.",
     "{1}: {2}% statt {3}%. Schau bitte nach dem Auto."),
    (r"The charger did not start 3 times\. HESC stops trying for this plan\. Check the car and the charger\.",
     "De laadpaal startte 3 keer niet. HESC probeert het niet meer voor dit plan. Kijk bij de auto en de laadpaal.",
     "Die Wallbox hat 3-mal nicht gestartet. HESC versucht es für diesen Plan nicht mehr. Schau nach dem Auto und der Wallbox."),
    (r"HESC could not switch the charger back on after 3 attempts \((.*)\)\. The EV may not charge as planned\. "
     r"Please check the charger\.",
     "HESC kon de laadpaal na 3 pogingen niet weer aanzetten ({1}). De auto laadt misschien niet zoals gepland. "
     "Kijk even bij de laadpaal.",
     "HESC konnte die Wallbox nach 3 Versuchen nicht wieder einschalten ({1}). Das Auto lädt vielleicht nicht wie geplant. "
     "Schau bitte nach der Wallbox."),
    (r"HESC P(\d) · (EV goal not confirmed|EV goal missed|Charger refuses to start|Charger fault)", "HESC P{1} · {t2}",
     "HESC P{1} · {t2}"),
    (r"EV goal not confirmed", "Doel niet bevestigd", "Ziel nicht bestätigt"),
    (r"EV goal missed", "Doel niet gehaald", "Ziel verfehlt"),
    (r"Charger refuses to start", "Laadpaal weigert te starten", "Wallbox verweigert den Start"),
    (r"Charger fault", "Storing laadpaal", "Störung der Wallbox"),
    (r"HESC P2 · EV battery level", "HESC P2 · Accustand auto", "HESC P2 · Akkustand Auto"),
    (r"HESC test", "HESC-test", "HESC-Test"),
    (r"No phone chosen yet: HESC notifications only appear inside Home Assistant\.",
     "Nog geen telefoon gekozen: meldingen van HESC verschijnen alleen in Home Assistant.",
     "Noch kein Telefon gewählt: Meldungen von HESC erscheinen nur in Home Assistant."),
    (r"This phone gets the notifications from Home EV Solar Control\.",
     "Deze telefoon krijgt de meldingen van Home EV Solar Control.",
     "Dieses Telefon bekommt die Meldungen von Home EV Solar Control."),
    # ---- morning summary ----
    (r"HESC · Morning summary", "HESC · Ochtendoverzicht", "HESC · Morgenübersicht"),
    (r"EV level unknown", "Auto: accustand onbekend", "Auto: Akkustand unbekannt"),
    (r"EV (\S+) %", "Auto {1} %", "Auto {1} %"),
    (r"EV (\S+) % \(estimated\)", "Auto {1} % (geschat)", "Auto {1} % (geschätzt)"),
    (r"plugged in", "aangesloten", "angeschlossen"),
    (r"not plugged in", "niet aangesloten", "nicht angeschlossen"),
    (r"Plan (\S+ \S+ \S+) → (\S+) %", "Plan {1} → {2} %", "Plan {1} → {2} %"),
    (r"needs (\S+) kWh, (\S+) from grid", "nog {1} kWh nodig, {2} van het net", "braucht {1} kWh, {2} aus dem Netz"),
    (r"needs (\S+) kWh, all from sun", "nog {1} kWh nodig, alles van de zon", "braucht {1} kWh, alles aus der Sonne"),
    (r"already reached", "al bereikt", "schon erreicht"),
    (r"No charge plan", "Geen laadplan", "Kein Ladeplan"),
    (r"Holiday mode on", "Vakantiestand aan", "Urlaubsmodus an"),
    (r"week plan paused", "weekplan gepauzeerd", "Wochenplan pausiert"),
    (r"week plan paused until (\S+)", "weekplan gepauzeerd tot {1}", "Wochenplan pausiert bis {1}"),
    (r"Sun today ± (\S+) kWh", "Zon vandaag ± {1} kWh", "Sonne heute ± {1} kWh"),
    (r"Yesterday (\S+) kWh", "Gisteren {1} kWh", "Gestern {1} kWh"),
    (r"(\S+) % sun", "{1} % zon", "{1} % Sonne"),
    (r"Yesterday not charged", "Gisteren niet geladen", "Gestern nicht geladen"),
    (r"Goal yesterday reached \((\S+) % of (\S+) %\)", "Doel gisteren gehaald ({1} % van {2} %)", "Ziel gestern erreicht ({1} % von {2} %)"),
    (r"Goal yesterday missed \((\S+) % of (\S+) %\)", "Doel gisteren niet gehaald ({1} % van {2} %)",
     "Ziel gestern verfehlt ({1} % von {2} %)"),
    (r"Goal yesterday not confirmed \(no battery level\)", "Doel gisteren niet bevestigd (geen accustand)",
     "Ziel gestern nicht bestätigt (kein Akkustand)"),
    # ---- phone summary (widget, Apple Watch) ----
    (r"EV (\S+)%", "Auto {1}%", "Auto {1}%"),
    (r"EV (\S+)% → (\S+)%", "Auto {1}% → {2}%", "Auto {1}% → {2}%"),
    (r"EV (\S+)% → (\S+)% now", "Auto {1}% → {2}% nu", "Auto {1}% → {2}% jetzt"),
    (r"EV (\S+)% → (\S+)% by (\S+ \S+ \S+)", "Auto {1}% → {2}% om {3}", "Auto {1}% → {2}% bis {3}"),
    (r"grid (\S+ \S+)", "net {1}", "Netz {1}"),
    (r"Charging on sun", "Laadt op zon", "Lädt mit Sonne"),
]

_DAYS = {"nl": dict(zip(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), ("ma", "di", "wo", "do", "vr", "za", "zo"))),
         "de": dict(zip(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")))}
_DAY_RE = re.compile(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?= \d)")
_DEC_RE = re.compile(r"(?<![\d.])(-?\d+)\.(\d+)(?![\d.])")
_SHADOW = {"nl": "[schaduw] ", "de": "[Schatten] "}
_HHMM = re.compile(r"^(\d{1,2}:\d{2}) (.+)$", re.S)
_GROUP = re.compile(r"\{(t?)(\d)\}")

RULES: list[tuple[re.Pattern[str], dict[str, str]]] = [
    (re.compile(en + r"\Z", re.S), {"nl": nl, "de": de}) for en, nl, de in _R
]


def lang_of(code: str | None) -> str | None:
    """'nl' or 'de' for a language code HESC translates to ('nl-NL', 'de_AT', ...), else None."""
    c = (code or "").replace("_", "-").split("-")[0].lower()
    return c if c in LANGS else None


def _part(text: str, lang: str) -> str | None:
    for rx, tr in RULES:
        m = rx.match(text)
        if m is None:
            continue
        groups = m.groups()

        def fill(g: re.Match[str], groups: tuple[str | None, ...] = groups) -> str:
            v = groups[int(g.group(2)) - 1] or ""
            return _translate(v, lang) if g.group(1) else v
        return _GROUP.sub(fill, tr[lang])
    return None


def _translate(text: str, lang: str) -> str:
    whole = _part(text, lang)  # a whole text first (some contain " · " themselves)
    if whole is not None:
        return whole
    parts = text.split(SEP)
    if len(parts) > 1:
        return SEP.join(_translate(p, lang) for p in parts)
    items = text.split(", ")  # a list such as "forecast now, forecast +30m"
    if len(items) > 1 and all(_part(x, lang) is not None for x in items):
        return ", ".join(_part(x, lang) or x for x in items)
    return text


def translate(text: str | None, lang: str | None) -> str | None:
    """`text` in `lang` ('nl', 'de' or a code like 'nl-NL'); English and unknown languages unchanged."""
    code = lang_of(lang)
    if not text or code is None:
        return text
    out_lines = []
    for line in str(text).split("\n"):
        shadow = line.startswith("[shadow] ")
        body = line[len("[shadow] "):] if shadow else line
        m = _HHMM.match(body)
        if m and _part(m.group(2), code) is not None or (m and SEP in m.group(2)):
            body = m.group(1) + " " + _translate(m.group(2), code)
        else:
            body = _translate(body, code)
        body = _DAY_RE.sub(lambda d: _DAYS[code][d.group(1)], body)
        body = _DEC_RE.sub(r"\1,\2", body)
        out_lines.append((_SHADOW[code] if shadow else "") + body)
    return "\n".join(out_lines)


def translated(text: str | None) -> dict[str, str | None]:
    """The attributes `nl` and `de` for a status text."""
    return {lang: translate(text, lang) for lang in LANGS}


def is_translated(text: str, lang: str) -> bool:
    """True when every part of `text` has a rule (for the tests)."""
    def ok(t: str) -> bool:
        if _part(t, lang) is not None:
            return True
        parts = t.split(SEP)
        if len(parts) > 1:
            return all(ok(p) for p in parts)
        items = t.split(", ")
        return len(items) > 1 and all(_part(x, lang) is not None for x in items)
    for line in text.split("\n"):
        body = line[len("[shadow] "):] if line.startswith("[shadow] ") else line
        m = _HHMM.match(body)
        if not (ok(body) or (m is not None and ok(m.group(2)))):
            return False
    return True


TranslateFn = Callable[[str | None], str | None]
