# 03 · Einstellungen

*English: [03-settings.md](03-settings.md) · Nederlands: [03-settings.nl.md](03-settings.nl.md)*

**Kurz gesagt**
- **Was HESC liest** (Wallbox, Auto, Solarleistung, Prognose, HPVC), stellst du in der Einrichtung
  ein: *Einstellungen → Geräte & Dienste → HESC v3 → Konfigurieren*.
- **Wie HESC sich verhält** (Schwellen, Ladeplan, Kosten, Benachrichtigungen), stellst du auf der
  Seite *Einstellungen* des HESC-Dashboards ein, und die Pläne selbst auf der Seite *Ladeplan*.
- Die Standardwerte passen für die meisten Häuser. Ändere etwas nur, wenn die Empfehlung oder der
  Bericht darauf hinweist.
- Blöcke, die in Ordnung sind, bleiben zu. Ein Block, dem etwas fehlt, öffnet sich von selbst.

## Zwei Orte

| Wo | Was du dort einstellst |
|---|---|
| **Einrichtung** (*Konfigurieren*) | Wallbox-Typ und seine Entitäten, Solarleistung und Netzleistung, Solarprognose, Auto (angeschlossen, Ladeleistung, Ladestand), HPVC oder eigenständig, Netzleistung pro Phase. Siehe [01 · Installation](01-installation.de.md#2-hesc-hinzufügen-und-die-einrichtung-ausfüllen). |
| **Dashboard, Seite *Einstellungen*** | Alles darüber, wie HESC sich verhält: Schwellen, Zeiten, Empfehlung, Netzladen, Preise, Benachrichtigungen, Mindestladung, Hausspeicher, Kosten. |
| **Dashboard, Seite *Ladeplan*** | Wann das Auto fertig sein muss und wie voll, Urlaubsmodus, günstige Gelegenheiten. |
| **Dashboard, Seite *Übersicht*** | *HESC an* und *Schattenmodus (nur zusehen)*. |

Auf der Seite *Einstellungen* werden die Entitäten aus der Einrichtung nur angezeigt. Die Zeile
*Quellen und Wallbox ändern* öffnet die Einrichtung.

## Oben auf der Seite Einstellungen

- **Prüfung der Einrichtung.** Eine Karte sagt *Einrichtung geprüft · alles in Ordnung* oder wie
  viele Teile Aufmerksamkeit brauchen. Pro Teil (Wallbox, Quellen, Wetterstation, Ladeplan,
  Hausspeicher und Auto) siehst du die aktuellen Werte; ein Teil, der nicht stimmt, zeigt, was
  fehlt. Teile, die du nicht verwendest, stehen in einer Zeile, *Nicht verwendet*.
- **Empfehlung.** Die Startschwelle, auf die dein eigener Verlauf hinweist, die aktuelle Schwelle,
  auf wie vielen Sitzungen sie beruht, und der Schalter *Empfehlung automatisch anwenden*. Die
  Zeile **Phasen** zeigt den Phasenhinweis. Wie die Empfehlung funktioniert:
  [04 · So funktioniert es](04-how-it-works.de.md#startschwelle-und-empfehlung).
- **Deine Einstellungen.** Deine Schwellen, Auto, Zeiten, Ladeplan und Empfehlung auf einen Blick.
- **Sichern · Sicherung wiederherstellen · Standardwerte.** *Sichern* speichert alle deine
  Einstellungen von HESC in `/config/hesc_v3/` (plus eine Kopie mit Datum und Uhrzeit).
  *Sicherung wiederherstellen* holt sie zurück; die Taste zeigt, welche Sicherung sie verwendet.
  *Standardwerte* erstellt zuerst eine Sicherung und setzt dann nur die Feinabstimmung zurück
  (Schwellen, Zeiten, Empfehlung, letzte Prüfung); Sensoren, Ziele, Preise und Kosten bleiben,
  wie sie sind.

## 1 · Deine Wallbox — erforderlich

*Wallbox-Typ* und **Erneut suchen** (sucht die Entitäten der Wallbox erneut). Die Felder der
Wallbox bleiben zu, solange die Prüfung grün ist; *Felder Wallbox* zeigt sie. Siehe
[05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#deine-wallbox).

## 2 · Quellen

| Schalter | Bedeutung |
|---|---|
| *HPVC verwenden* | An, wenn du Home PV Control verwendest; aus (Standard), wenn nicht. Ohne HPVC lässt HESC die Freigabe weg: nichts wird begrenzt, also startet die Wallbox von selbst mit Sonne. Eine neue Installation schaltet das nur dann selbst ein, wenn sie HPVC findet. |
| *Solar und Netz aus HPVC* | An = HESC verwendet die Sensoren von HPVC für Solarleistung und Netzleistung. Aus = deine eigenen Sensoren aus der Einrichtung. |
| *Quellen ändern* | Zeigt die Felder für Solarleistung, Netzleistung, Prognose und HPVC. Sie öffnen sich auch von selbst, wenn etwas fehlt. |

## Weiteres

Wird mit *Weitere Felder zeigen* angezeigt.

| Feld | Wann du es brauchst |
|---|---|
| *Statuswerte, die "kein Auto" bedeuten* | Nur, wenn *Auto angeschlossen* ein Statussensor ist. |
| *Zusätzlicher Solarschalter* | Wallboxen, die zum Laden mit Sonne einen zusätzlichen Schalter brauchen (go-e, Wattpilot). |
| *Zähler Solarenergie* | Der Zähler der Wallbox für Energie aus der Sonne, für den Bericht. |
| *Ladestand Auto* + *Auto gilt als voll bei* | Der Ladestand des Autos und der Ladestand, der als voll gilt (Standard 80 %; 100 % für LFP-Akkus). Verwendet für "Auto ist voll", den Ladeplan und günstige Gelegenheiten. |

**Eigene Wetterstation.** *An* schaltet sie ein oder aus; *Optionen* zeigt den Einstrahlungssensor
und seine Schwellen zum Starten und Weiterladen (Standard 220 / 160 W/m²). Ohne Wetterstation
arbeitet HESC nur mit der Prognose.

## 3 · Erweitert — nur bei Bedarf

Jeder Block hat einen eigenen Schalter, um ihn zu zeigen.

| Block | Einstellungen | Standardwerte |
|---|---|---|
| *Ladeschwellen* | *Startschwelle nach Jahreszeit*, *Prognoseleistung zum Starten* / *zum Weiterladen*, *Auto gilt als ladend über* | aus · 2 000 / 1 500 W · 400 W |
| *Zeiten* | stabil vor Freigabe, warten, bis die Wallbox startet, erlaubter Sonneneinbruch, Wallbox gestoppt vor Wiederherstellung, längste Freigabe, Pause nach Freigabe, fehlgeschlagene Freigaben pro Tag | 5, 10, 5, 5, 240, 30 min · 3 |
| *Empfehlung* | Empfehlung auf Basis der letzten, Mindestanzahl Sitzungen vor Empfehlung | 30 Tage · 8 Sitzungen |
| *Ladeplan und Meldungen* | Start/Stopp-Schalter **oder** Lademoduswert für "jetzt laden", *Zurück in den Solarmodus*, Preisquelle, Preissensor, Preise pro, Währung, Solarprognose heute / morgen, letzte Prüfung, Telefone für Benachrichtigungen, Morgenübersicht | kein Netzladen · *Price list in sensor* · *Automatic* · *Automatic* · 60 min · aus |

**Netzladen.** Fülle **eines** der ersten beiden aus: einen Start/Stopp-Schalter (wird in einer
geplanten Viertelstunde eingeschaltet) oder den Lademoduswert, der "jetzt laden" bedeutet.
*Zurück in den Solarmodus* (optional, mit einem Start/Stopp-Schalter) ist eine Taste oder ein
Skript, das die Wallbox nach dem Netzladen zurück auf Laden mit Sonne setzt, zum Beispiel bei einer
Wallbox der Marke Wallbox *Resume schedule*. Beim Wallbox-Typ *Wallbox* füllt HESC das selbst aus,
wenn es genau eine findet. Nichts ausgefüllt = kein Netzladen.

**Preise.** Siehe [05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#strompreise).

**Benachrichtigungen.** *Telefon hinzufügen oder entfernen* listet jedes Gerät mit der
Home-Assistant-App; ✓ = bekommt Benachrichtigungen. *Testbenachrichtigung senden* probiert es aus.
*Morgenübersicht jeden Tag* schickt eine Nachricht am Tag (Ladestand, nächster Plan, Sonne heute,
gestern).

## Mindestladung

*An* + *Optionen*. Wird das Auto unter dem *Mindestladestand* (Standard 20 %) angeschlossen, lädt
HESC es innerhalb von *Erreichen innerhalb (Stunden)* (Standard 3 h) auf diesen Ladestand, in den
günstigsten Viertelstunden dieses Zeitfensters. Praktisch, wenn du fast leer heimkommst und das
Auto vielleicht bald wieder brauchst.

## Hausspeicher und Auto

*An* + *Optionen*, nur mit einem Hausspeicher. Trage den oder die Ladestandsensoren und den oder
die Leistungssensoren deiner Hausspeicher ein (mehrere, durch Kommas getrennt; eine positive
Leistung bedeutet laden), ihre Gesamtgröße, die höchste Zahl an Kickstarts pro Tag und die
minimale Sonne, die für das Auto übrig bleiben muss. Braucht den Start/Stopp-Schalter und
*Zurück in den Solarmodus* aus dem Block *Ladeplan und Meldungen*. Wie es funktioniert:
[04 · So funktioniert es](04-how-it-works.de.md#hausspeicher-und-auto-kickstart); deine
Hausspeicher-Steuerung mit HESC verbinden:
[04 · Deine Hausspeicher-Steuerung verbinden](04-how-it-works.de.md#deine-hausspeicher-steuerung-mit-hesc-verbinden).

## Ladekosten

*An* zeigt die Anzeige *Kosten* auf der *Übersicht* und die Seite Kosten; *Optionen* zeigt die
Felder. HESC zählt die Kosten, ob die Seite angezeigt wird oder nicht.

| Feld | Bedeutung | Standard |
|---|---|---|
| *Wert einer Solar-kWh* | die Einspeisevergütung, die dir entgeht, wenn du das Auto lädst; 0 = gratis | 0 |
| *Preis aus der Preisquelle ist schon der Endpreis* | der Preis enthält schon Steuer, Aufschlag des Anbieters und MwSt. | aus |
| *Aufschlag pro kWh* | Energiesteuer und Anbieter, nur wenn nicht Endpreis | 0 |
| *MwSt. auf Preis + Aufschlag* | in %, nur wenn nicht Endpreis | 0 |

Änderst du diese Werte, wird der ganze Verlauf neu berechnet.

## Seite Ladeplan

| Einstellung | Bedeutung |
|---|---|
| *Ladeplan · ein fester Tag pro Woche* | Tag, Uhrzeit, Ladeziel, *Aktiv*. Kommt jede Woche wieder; schalte *Aktiv* aus, wenn du ihn nur einmal brauchst. |
| *Ladeplan · Wochenplanung* | Tage, Uhrzeit, Ladeziel, *Aktiv*. |
| *Urlaubsmodus* + *Urlaub bis* | Der Wochenplan tut nichts; der Plan für einen Tag und das Laden mit Sonne laufen weiter. Schaltet sich am Tag nach *Urlaub bis* von selbst aus. |
| *Günstige Gelegenheiten nutzen* + *Günstig unter* | Auch laden, wenn der Preis bei oder unter diesem Preis liegt (pro kWh, in der Währung deiner Preise), außer die Sonne deckt es später am Tag. |
| *Nutzbare Akkukapazität* · *Ladeleistung aus dem Netz* | Um auszurechnen, wie viel Energie nötig ist und wie viele Viertelstunden das dauert (Standard 60 kWh · 11 kW). |

## Seite Übersicht

| Schalter | Bedeutung |
|---|---|
| *HESC an* | Hauptschalter. Aus = HESC tut nichts. |
| *Schattenmodus (nur zusehen)* | An = HESC entscheidet und zeigt, was es tun würde, schaltet aber nichts. Nach der Installation an. |
