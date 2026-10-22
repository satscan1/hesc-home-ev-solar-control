# 04 · So funktioniert es

*English: [04-how-it-works.md](04-how-it-works.md) · Nederlands: [04-how-it-works.nl.md](04-how-it-works.nl.md)*

**Kurz gesagt**
- Alle 30 Sekunden liest HESC deine Quellen und entscheidet, was die Wallbox tun soll.
- Mit Sonne: HESC lässt die Wallbox in ihrer eigenen Einstellung für Laden mit Sonne starten. Mit
  HPVC bittet HESC zuerst HPVC, deine Solarpaneele eine Weile nicht mehr zu begrenzen.
- Aus dem Netz: Der Ladeplan wählt die günstigsten Viertelstunden vor deiner Fertig-Zeit und
  rechnet mit der Sonne, die noch kommt.
- Mit einem Hausspeicher sorgt ein Kickstart dafür, dass das Auto an einem sonnigen Tag an die
  Reihe kommt.
- Im Schattenmodus trifft HESC alle Entscheidungen genauso, schaltet aber nichts.

## Alle 30 Sekunden

HESC liest etwa zwanzig Werte aus Home Assistant: Solarleistung, Netzleistung, Prognose, die
Wallbox, das Auto, Preise, den Hausspeicher. Es rechnet aus, was zu tun ist, und schreibt das
Ergebnis in seine eigenen Entitäten (Zustand, Grund, Plan). Uhrzeiten und Tagesgrenzen folgen der
Zeitzone von Home Assistant. Teile, die nicht so oft laufen müssen, haben ihren eigenen Takt, zum
Beispiel die Preisprognose alle 15 Minuten.

Der **Schattenmodus** (*Schattenmodus (nur zusehen)* auf der *Übersicht*) ist nach der Installation
an. HESC entscheidet dann genau wie im Live-Betrieb und zeigt es, schickt aber keinen Befehl an die
Wallbox oder an HPVC. **HESC an** aus heißt: HESC tut gar nichts.

## Laden mit Sonne

**Ohne HPVC (eigenständig).** Nichts begrenzt deine Solarpaneele, also startet die Wallbox von
selbst mit Sonne, sobald genug Überschuss da ist. HESC verfolgt jede Sitzung, hält fest, wie sie
lief, und gibt eine Empfehlung zur Startschwelle.

**Mit HPVC.** HPVC hält deine Einspeisung nahe null, deshalb sieht die Wallbox nie genug
Überschuss zum Starten. HESC bittet HPVC deshalb um eine Freigabe:

| Schritt | Was passiert |
|---|---|
| Ruhe | HESC wartet, bis alle Startbedingungen während *Bedingungen stabil vor Freigabe* (5 min) erfüllt sind. |
| Freigabe angefragt | HESC fragt HPVC (HPVC 1.5.1 oder neuer). HPVC erledigt zuerst alles mit höherer Priorität und lässt die Paneele dann frei produzieren. Keine Antwort innerhalb von 5 Minuten → HESC versucht es später. |
| Warten auf das Auto | HPVC hat bestätigt. Die Wallbox hat *Warten, bis die Wallbox startet* (10 min) Zeit zum Starten. |
| Laden | Das Auto lädt mit Sonne. |
| Freigabe beendet | Das Auto hat gestoppt, die Sonne blieb länger als *Erlaubter Sonneneinbruch* unter der Weiterladeschwelle, das Auto wurde abgesteckt, Sonnenuntergang, oder *Längste Freigabe*. HPVC übernimmt wieder, und eine Pause beginnt. |

Startbedingungen: Das Auto ist angeschlossen, lädt nicht, ist nicht voll, und die Wallbox ist auf
Laden mit Sonne eingestellt; HPVC begrenzt; die vorsichtige Prognose (jetzt und in 30 Minuten)
liegt bei oder über der Startschwelle; die Wetterstation stimmt zu (wenn verwendet); keine Pause;
heute nicht zu viele fehlgeschlagene Freigaben; die Sonne ist aufgegangen. HESC schaltet HPVC nie
selbst aus; es fragt nur.

## Solarprognose

| Was du hast | Wie HESC es nutzt |
|---|---|
| **Solcast** | Die vorsichtige Schätzung zum Entscheiden, die normale Schätzung zum Vergleich mit dem, was wirklich passiert ist. |
| **Open-Meteo** oder **Forecast.Solar** | Von HESC in dieselbe Form umgerechnet; funktioniert genauso. |
| **Keine Prognose** | HESC verwendet stattdessen die gemessene Solarleistung (oder die Wetterstation). Der Ladeplan rechnet mit keiner Sonne, damit er nie zu spät ist. Der Kickstart ist aus. |

## Startschwelle und Empfehlung

Die Startschwelle bezieht sich auf die **Prognose**. Sie entscheidet drei Dinge:

- wann HESC HPVC bittet, die Begrenzung deiner Paneele aufzuheben (nur, solange HPVC sie begrenzt);
- wann der Kickstart starten darf;
- welche halben Stunden der Ladeplan als "Sonne kommt" zählt.

Sie entscheidet **nicht**, wann deine Wallbox mit Sonne lädt: In ihrem Solarmodus startet die
Wallbox von selbst bei Überschuss, egal wie die Schwelle steht. Der richtige Wert ist in jedem Haus
anders, deshalb rechnet HESC ihn aus deinen eigenen Sitzungen aus:

- Es schaut nur auf die Ladesitzungen mit Sonne, die **starteten, während HPVC deine Paneele
  begrenzte**, aus den letzten 30 Tagen (im Winter, wenn es wenige gibt, bis zu 60 Tage). Nur bei
  denen hat die Schwelle etwas entschieden. Starts von Hand oder nach Zeitplan bleiben außen vor.
- In den dunklen Monaten begrenzt HPVC selten, deshalb sammelt die Empfehlung oft weiter. Das ist in
  Ordnung: Die Schwelle spielt dann kaum eine Rolle. Ohne HPVC (eigenständig) gibt es keine
  Empfehlung; *Startschwelle nach Jahreszeit* ist dann die einfache Wahl.
- **Empfehlung:** die niedrigste Startprognose, ab der die nächsten 8 Sitzungen zusammen mindestens
  70 % ihrer Energie von der Sonne bekamen. Gerundet auf 50 W, zwischen 1 000 und 3 500 W.
  Weiterladen = 75 % von Starten.
- **Nie unter deiner Wallbox.** Die Empfehlung geht nie unter die Sonne, die deine Wallbox zum
  Starten braucht (siehe [05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#wie-viel-sonne-eine-wallbox-zum-starten-braucht)).
  Die Empfehlung sagt das dann auch.
- **Empfehlung automatisch anwenden** (standardmäßig aus): HESC bewegt die Startschwelle von selbst
  in Richtung der Empfehlung, in kleinen Schritten: höchstens 200 W pro Schritt und ein Schritt pro
  7 Tage, nur bei einem Unterschied von mindestens 100 W und wenn die Empfehlung auf genug
  Sitzungen an verschiedenen Tagen beruht. Jede Änderung erscheint als grauer Hinweis auf der
  *Übersicht*.
- **Startschwelle nach Jahreszeit** (standardmäßig aus): Jede Nacht setzt HESC die Startschwelle
  für den Monat: Juni–Juli 2 500 W, April–Mai und August–September 2 000 W, März und Oktober
  1 500 W, November–Februar 1 200 W; Weiterladen 75 %. Nie unter dem Startniveau deiner Wallbox.
  Kann nicht zusammen mit *Empfehlung automatisch anwenden* an sein.

Die Empfehlung wird jeden Abend und beim Start von HESC ausgerechnet.

## Phasenhinweis

Nur mit Netzleistung pro Phase in der Einrichtung. Solange das Auto nicht lädt, schaut HESC, wie
viel Überschuss jede Phase hat. Wallboxen, die Sonne auf **jeder** Phase brauchen (Wallbox Eco,
Easee), werden von der schwächsten Phase gebremst. Der Hinweis durchläuft drei Stufen:

1. **wird gemessen** — weniger als 14 Tage mit brauchbarer Sonne;
2. **vorläufig** — die Verteilung über die Phasen ist bekannt;
3. **bestätigt** — genug Tage in der sonnigsten Zeit des Jahres gesehen.

Die sonnigste Zeit wird aus dem Sonnenstand an deinem Standort berechnet, deshalb stimmt sie überall
auf der Welt (auf der Südhalbkugel um Dezember herum). Der Phasenhinweis ist nur zur Info; HESC
ändert nichts von selbst.

## Ladeplan

Der Plan nimmt den aktiven Plan (den Plan für einen Tag oder den Wochenplan; der frühere gewinnt),
das Ladeziel und die Fertig-Zeit. Er rechnet die nötige Energie aus, zieht die Sonne ab, die vor
der Frist erwartet wird, und wählt für den Rest die günstigsten Viertelstunden. Nach den Preisen des
Tages nutzt er auch erwartete Preise, wartet aber nur dann auf einen, wenn er deutlich günstiger ist.

**Sonne im Plan.** Jede halbe Stunde vor der Frist, in der die vorsichtige Prognose hoch genug ist,
damit die Wallbox startet, zählt als (Prognose − 0,4 kW für das Haus) × 0,5 h, höchstens die
Ladeleistung aus dem Netz.

| Grund auf dem Dashboard | Was passiert |
|---|---|
| *Planned quarter* | Laden aus dem Netz. |
| *Safety net: only just enough time left* | Laden, weil die verbleibende Zeit gerade noch reicht. |
| *Final check: below goal, charging to goal* | In der letzten Stunde (*letzte Prüfung*) unter dem Ladeziel: Laden, egal zu welchem Preis. |
| *Cheap chance (…)* | Der Preis liegt bei oder unter *Günstig unter*: Laden. |
| *Cheap chance skipped: enough sun today (…)* | Die Sonne später am Tag deckt den Bedarf mit 20 % Reserve. |
| *Within 3 % of goal* | Netzladen startet erst mehr als 3 % unter dem Ladeziel. |
| *Goal reached* | Wallbox pausiert oder zurück in ihrem vorigen Modus. |
| *EV already charging, left alone* | HESC übernimmt nie eine Ladung, die es nicht selbst begonnen hat. |

**Danach.** Ist *Zurück in den Solarmodus* ausgefüllt, pausiert HESC die Wallbox nach dem
Netzladen, prüft, ob die Pause wirklich angekommen ist (Wallboxen über die Cloud sind oft eine
Minute zu spät), und setzt die Wallbox dann zurück auf Laden mit Sonne. Ohne dieses Feld bleibt die
Wallbox pausiert, damit das Auto sich nicht aus dem Netz nachladen kann; HESC schaltet sie wieder
ein für Sonne, für einen neuen Plan oder wenn du absteckst.

**Zielprüfung.** Zur Fertig-Zeit vergleicht HESC den Ladestand mit dem Ladeziel. Mehr als 3 %
darunter: ein roter Hinweis *EV goal missed* (auch auf deinem Telefon).

**Mindestladung** (optional): Unter dem Mindestladestand wird das Auto innerhalb der eingestellten
Zeit darauf geladen, in den günstigsten Viertelstunden dieses Zeitfensters.

## Ladestrom

Darf HESC den Ladestrom einstellen, senkt es ihn, während der Ladeplan aus dem Netz lädt: Das Auto
nimmt dann etwa das, was die Sonne liefert, nie unter 6 A. Nur, solange das Auto mit 30 Minuten
Reserve trotzdem rechtzeitig voll ist; sonst voller Strom. Danach geht der Strom zurück auf den
vorigen Wert, auch nach einem Neustart. HESC misst die Zahl der Phasen selbst und handelt erst,
wenn es sie kennt. Höchstens eine Änderung pro Minute; nichts im Schattenmodus.

## Hausspeicher und Auto (Kickstart)

An einem sonnigen Morgen nimmt der Hausspeicher die ganze überschüssige Sonne, deshalb sieht die
Wallbox keinen Überschuss, und das Auto wartet. HESC steuert den Hausspeicher nie; es startet nur
die Wallbox.

**Kickstart**, wenn all das zutrifft: Das Auto ist angesteckt, wartet auf Laden mit Sonne und ist
nicht voll; die Hausspeicher laden seit ein paar Minuten mit über 500 W; die vorsichtige Prognose
liegt bei oder über der Startschwelle; die restliche Sonne heute ist deutlich mehr, als die
Hausspeicher noch brauchen (1,2 × ihr Bedarf, plus *Minimale Restsonne für das Auto*); kein
Ladeplan und keine Freigabe aktiv; heute weniger als *Kickstarts pro Tag*, mindestens 30 Minuten
nach dem letzten.

Die Reihenfolge:
1. HESC startet die Wallbox.
2. Deine Hausspeicher-Steuerung sieht, dass das Auto lädt, und hört auf, den Hausspeicher zu füllen.
3. HESC pausiert die Wallbox und wartet, bis die Pause wirklich angekommen ist.
4. HESC setzt die Wallbox zurück auf Laden mit Sonne. Sie sieht jetzt den Überschuss und lädt mit
   Sonne.

Schritt 4 muss kommen, solange deine Hausspeicher-Steuerung den Hausspeicher noch festhält. HESC gibt
deshalb 15 Sekunden, nachdem der Start/Stopp-Schalter der Wallbox ausging, zurück (der Moment, in
dem Home Assistant es gesehen hat, auch wenn eine Wallbox über die Cloud die Pause erst spät zeigt).
Für deine Hausspeicher-Steuerung gibt es einen Sensor *Kickstart: Übergabe läuft*: Er ist von
Schritt 3 an, bis die Wallbox wieder mit Sonne lädt. Halte den Hausspeicher fest, solange er an
ist, auch wenn die Wallbox kurz 0 W zeigt.

**Zurück zum Hausspeicher.** Hat das Auto 10 Minuten oder länger mit Sonne geladen und reicht die
restliche Sonne heute gerade noch für die Hausspeicher, pausiert HESC die Wallbox und lässt sie
wieder auf Sonne warten, damit der Hausspeicher bis zum Abend voll ist.

### Deine Hausspeicher-Steuerung mit HESC verbinden

Entscheidet deine Hausspeicher-Steuerung selbst, wann das Auto lädt (zum Beispiel, um aufzuhören,
den Hausspeicher zu füllen, wie in Schritt 2)? Gib ihr diese zwei Entitäten von HESC:

| Entität | Verwende sie für |
|---|---|
| **Ladeleistung Auto** (`sensor.hesc_v3_ev_charging_power`) | Die Ladeleistung des Autos. Verwende sie statt des eigenen Leistungssensors deiner Wallbox: Sie zeigt 0 W, sobald die Wallbox pausiert ist, auch wenn die Wallbox noch minutenlang ihre letzte Leistung meldet (Wallbox). |
| **Kickstart: Übergabe läuft** (`binary_sensor.hesc_v3_kickstart_hand_back_in_progress`) | Halte den Hausspeicher fest, solange er an ist. |

Beide funktionieren mit jeder Wallbox, deren Start/Stopp- oder Pausenschalter HESC kennt oder
deren Status sagt, dass sie pausiert ist. Sie sind nur so schnell, wie deine Wallbox meldet: Eine
Wallbox über die Cloud kann eine Minute oder mehr hinterher sein, und HESC aktualisiert alle 30
Sekunden. Nur ein eigener kWh-Zähler in der Gruppe der Wallbox ist wirklich sofort.

Mit einem Hausspeicher kannst du die Wallbox pausiert in ihrem Solarmodus lassen; HESC startet sie
mit einem Kickstart, wenn genug Sonne übrig ist. **Ohne Hausspeicher gibt es keinen Kickstart:**
Lass die Wallbox dann nicht pausiert, sonst lädt das Auto nie mit Sonne.

## Ladestand des Autos

Alle Teile von HESC verwenden einen Ladestand. HESC nimmt den ersten davon, der einen Wert hat:
1. den Sensor für den Ladestand aus der Einrichtung;
2. einen zweiten Sensor für den Ladestand desselben Autos, den HESC selbst findet;
3. den letzten Ladestand dieser Ladesitzung, plus 90 % der seitdem geladenen kWh;
4. den üblichen Ladestand beim Anschließen in den letzten 14 Tagen (ab 5 Anschlüssen).

Ein geschätzter oder unbekannter Ladestand gibt einen orangen Hinweis. Gar kein Sensor? Die
Einrichtung hilft dir, einen für dein Auto zu finden.

## Preise, Kosten und Benachrichtigungen

- **Preise:** Alle Teile lesen eine Preisliste pro Viertelstunde; siehe
  [05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#strompreise). Die **Preisprognose**
  lernt deinen Markt aus deinem eigenen Preisverlauf und füllt die Viertelstunden nach dem letzten
  bekannten Preis.
- **Kosten:** Während das Auto lädt, wird der Teil aus dem Netz zum Preis der jeweiligen
  Viertelstunde berechnet; der Rest zählt als Sonne (auch Energie aus einem Hausspeicher).
- **Benachrichtigungen:** P1 (rot, auch auf deinem Telefon): Das Ladeziel wurde verfehlt oder ein
  echter Fehler. P2 (orange, auch auf deinem Telefon): Ein Sensor fehlt, HESC arbeitet weiter. P3
  (grau, nur auf der *Übersicht*): nur zur Info.

## Verlauf und Bericht

HESC schreibt eine Zeile pro Ereignis und Sitzung in seinen Verlauf in `/config/hesc_v3/`, etwa 50
Zeilen an einem sonnigen Tag. **Bericht erstellen** (auf der *Übersicht*, unter *Status*) macht
daraus eine Seite mit deinen Sitzungen, der Empfehlung und wie zuverlässig deine Quellen sind.
