# 08 · Ein Tag mit HESC

*English: [08-a-day-with-hesc.md](08-a-day-with-hesc.md) · Nederlands: [08-a-day-with-hesc.nl.md](08-a-day-with-hesc.nl.md)*

**Kurz gesagt**
- Ein gewöhnlicher Frühlingstag in einem ausgedachten Haus, vom Anstecken des Autos bis zum vollen
  Auto am nächsten Morgen.
- Am Morgen nehmen die Hausspeicher die Sonne; ein Kickstart bringt das Auto an die Reihe.
- Tagsüber lädt das Auto mit Sonne; die Wallbox entscheidet, wann sie startet und pausiert.
- In der Nacht lädt der Ladeplan den Rest in den günstigsten Viertelstunden nach, rechtzeitig für
  den Morgen.

Dieser Tag ist ein Beispiel: Das Haus, die Uhrzeiten und die Zahlen sind ausgedacht, aber jeder
Schritt ist das, was HESC wirklich tut.

## Das Haus

- **Solarpaneele** mit etwa 5 kWp. Solcast erwartet heute **18 kWh**.
- **Hausspeicher** mit insgesamt 10 kWh, morgens bei 30 %, gesteuert von ihrer eigenen
  Speichersteuerung.
- **Eine Wallbox** (Marke Wallbox) auf drei Phasen, in *Eco* (Laden mit Sonne).
- **Ein Auto** mit einem 60-kWh-Akku, bei **40 %**, wenn es angesteckt wird.
- **Ein Ladeplan:** 80 % bis morgen früh um 07:30.
- **Dynamische Strompreise**, pro Viertelstunde.
- Einstellungen: Startschwelle **1 500 W**, Weiterladeschwelle **1 100 W**.

## 07:45 · Angesteckt

Das Auto wird bei 40 % angesteckt. HESC rechnet aus, was nötig ist: 40 % → 80 % sind etwa 24 kWh.

Auf der *Übersicht* siehst du den Plan für heute:
- **Erwartete Lademöglichkeiten mit Sonne:** grüne Balken von etwa 10:30 bis 15:30. Grün heißt:
  genug Sonne, damit die Wallbox startet. Orange heißt: genug zum Weiterladen, nicht zum Starten.
  Die zwei Schwellen stehen über der Grafik.
- **Erwartetes Solarladen:** heute etwa 5 Stunden Laden mit Sonne.
- **Live:** *Ladestand Auto 40 % · voll bei 80 %*, *Sonne, die heute noch kommt 18 kWh*.

Der Ladeplan reserviert schon ein paar günstige Viertelstunden heute Nacht, lässt aber Platz für
die Sonne, die noch kommt.

## 08:30 – 10:00 · Die Hausspeicher essen zuerst

Die Sonne geht auf. Die Hausspeicher stehen bei 30 % und nehmen jedes Watt, das übrig ist. Nichts
geht ins Netz, deshalb sieht die Wallbox keinen Überschuss und wartet.

Auf der Karte *Live*: *Netz 0 W*, *Hausspeicher 1800 W · 42 %*. HESC schaut zu und wartet.

## 10:15 · Kickstart

Die vorsichtige Prognose liegt jetzt bei 2 300 W, über der Startschwelle. Die Hausspeicher laden
schon eine Weile gleichmäßig. Und heute ist genug Sonne für beide übrig: etwa 14 kWh kommen noch,
die Hausspeicher brauchen noch etwa 6 kWh.

Also gibt HESC dem Auto einen **Kickstart**. Unter *Aktueller Stand* zeigt *Hausspeicher und
Auto*:
1. *Kickstart: charger started* — die Wallbox startet für einen Moment.
2. Die Speichersteuerung sieht, dass das Auto lädt, und hört auf, die Hausspeicher zu laden.
3. *Kickstart: charger paused* — HESC pausiert die Wallbox wieder.
4. *Kickstart: waiting for the charger to start on sun* — die Wallbox ist zurück in *Eco*. Jetzt
   geht die überschüssige Sonne ins Netz, und die Wallbox sieht sie.

## 10:20 – 10:35 · Genug Sonne, aber nicht auf jeder Phase

Insgesamt sind 2,0 kW übrig. Eine Wallbox in *Eco* braucht auf drei Phasen etwa 1,4 kW, aber auch
**mindestens etwa 480 W auf jeder Phase**. Phase 3 hat nur 350 W, deshalb wartet die Wallbox.

Um 10:35 steht die Sonne höher, alle drei Phasen liegen über 480 W, und die Wallbox startet von
selbst. Das Auto lädt mit Sonne.

Zeigt dein Zähler die Leistung pro Phase, zählt HESC, wie oft das passiert. Du siehst es auf der
Seite *Einstellungen* in der Zeile *Phasen*: zuerst *wird gemessen*, nach einigen Wochen
*vorläufig* und in der sonnigsten Zeit des Jahres *bestätigt*. Jede Wallbox hat ihr eigenes
Startniveau; siehe
[05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#wie-viel-sonne-eine-wallbox-zum-starten-braucht).

## 12:00 · Eine günstige Viertelstunde, aber genug Sonne

Mittags fällt der Preis auf fast nichts. Eine günstige Gelegenheit — aber die Sonne deckt
voraussichtlich, was das Auto heute noch braucht. *Status* zeigt:

> *Cheap chance skipped: enough sun today (…)*

Das Auto lädt weiter mit Sonne.

**Wenn du HPVC hast** und es deine Paneele in diesem Moment begrenzt (Einspeisen bringt nichts),
würde die Wallbox keinen Überschuss sehen. Dann bittet HESC HPVC, die Sonne für das Auto
durchzulassen, solange die Prognose über der Startschwelle liegt. HPVC entscheidet; HESC wartet auf
seine Antwort und gibt die Paneele zurück, sobald das Auto stoppt oder die Sonne unter die
Weiterladeschwelle fällt.

## 14:30 – 16:00 · Wolken

Wolken kommen und gehen. Die Wallbox pausiert, wenn die Sonne zu schwach ist, und startet von
selbst wieder, wenn sie zurückkommt. HESC mischt sich nicht ein: Die Wallbox entscheidet mit ihrer
eigenen Sonne.

Auf der *Übersicht* zeigt *Solarprognose und Ist · Auto*, wie die orange Linie (echte
Solarleistung) unter die lila Fläche (die Prognose) taucht und die cyanfarbene Linie (das Auto)
mit ihr an- und ausgeht.

## 16:15 · Eine geplante Viertelstunde, und der Strom geht runter

Der Ladeplan hat 16:15 – 16:30 gewählt: Der Preis ist dort niedrig. Das Auto lädt aus dem Netz. Es
gibt noch etwa 2,5 kW Sonne.

Weil diese Wallbox HESC den Ladestrom einstellen lässt, senkt HESC ihn auf 6 A pro Phase. Das Auto
nimmt dann etwa 4,1 kW, und mehr als die Hälfte davon kommt von der Sonne statt aus dem Netz. HESC
tut das nur, solange das Auto trotzdem rechtzeitig voll ist. Nach der Viertelstunde geht der Strom
zurück auf den vorigen Wert.

## 17:15 · Die Sonne ist weg

Die Wallbox stoppt; das Auto hat heute etwa 10 kWh Sonne genommen und steht bei **58 %**. Die
Hausspeicher sind voll.

Der Ladeplan rechnet den Rest aus: 58 % → 80 % sind etwa 13 kWh. Er wählt die günstigsten
Viertelstunden der Nacht.

## 02:00 – 03:15 · Der Rest aus dem Netz

Zwischen 02:00 und 03:15, den günstigsten Viertelstunden der Nacht, lädt der Plan aus dem Netz. Um
03:15 steht das Auto bei **80 %**, mehr als vier Stunden vor der Fertig-Zeit. *Status* zeigt
*Goal reached (80%)*.

## Der Tag in Zahlen

| | |
|---|---|
| Solarprognose (Solcast) | 18 kWh |
| Erzeugte Solarleistung | etwa 19 kWh |
| In die Hausspeicher | etwa 7 kWh (30 % → voll) |
| Ins Auto von der Sonne | etwa 10,5 kWh |
| Ins Auto aus dem Netz | etwa 13,5 kWh |
| Auto | 40 % → 80 % (etwa 24 kWh) |
| Sonnenanteil im Auto | etwa 44 % |
| Netzkosten für das Auto | etwa € 2,80 (13,5 kWh zu etwa € 0,21 Endpreis) |

## Was du daraus mitnimmst

- **Jeder macht seine eigene Arbeit.** Die Speichersteuerung steuert die Hausspeicher, die Wallbox
  entscheidet, wann sie mit Sonne startet, HPVC entscheidet über die Paneele. HESC schaut zu, fragt
  und plant.
- **Der Kickstart bringt das Auto am Morgen in Gang.** Ohne ihn würde das Auto warten, bis die
  Hausspeicher voll sind.
- **Nicht jedes Watt zählt gleich.** Auf drei Phasen braucht eine Wallbox wie die Wallbox in *Eco*
  Sonne auf jeder Phase. Das ist die eigene Regel der Wallbox; der Phasenhinweis zeigt, wie oft sie
  dich bremst.
- **Der Ladeplan füllt nur auf, was die Sonne übrig lässt.** Er nimmt die günstigsten
  Viertelstunden und sorgt dafür, dass das Auto rechtzeitig voll ist.

Mehr über die Logik dahinter: [04 · So funktioniert es](04-how-it-works.de.md) und
[07 · Intelligentes Laden erklärt](07-smart-charging-explained.de.md). Was jede Karte auf dem
Dashboard zeigt: [06 · Dashboard](06-dashboard.de.md).
