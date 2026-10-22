# 06 · Dashboard

*English: [06-dashboard.md](06-dashboard.md) · Nederlands: [06-dashboard.nl.md](06-dashboard.nl.md)*

**Kurz gesagt**
- Das Dashboard hat drei Seiten: *Übersicht* (was jetzt passiert), *Ladeplan* (wann das Auto fertig
  sein muss) und *Einstellungen*. Daneben: die Seite *Kosten*, die *Anleitung* und eine Seite
  *Kiosk* für ein Tablet an der Wand.
- Das meiste liest du nur. Ändern kannst du etwas auf *Ladeplan* und *Einstellungen* und in der
  Einrichtung.
- Das Dashboard kommt mit HESC (Seitenleiste: **HESC**). Die Karten, die es braucht:
  [01 · Installation](01-installation.de.md#3-das-dashboard-hinzufügen).

## Übersicht

![Main](images/main.png)

### Oben

- **Version:** die laufende Version von HESC, neben dem Logo.
- **Hinweiszeile:** *✓ Keine Hinweise* oder der wichtigste Hinweis mit seiner Uhrzeit. Rot = das
  Ladeziel ist in Gefahr (wird auch an dein Telefon geschickt), orange = ein Sensor fehlt, aber
  HESC arbeitet weiter, grau = nur zur Info. Tippe darauf, um dorthin zu gehen, wo du handeln
  kannst.
- **Anzeigen:**
  - *HESC-Status*, *Auto* (angesteckt?), *Solarmodus* (ist die Wallbox auf Laden mit Sonne
    eingestellt?) und *HPVC begrenzt*;
  - *Freigabe*, nur solange HESC HPVC gebeten hat, die Sonne durchzulassen;
  - *Erwartete Ladekosten*: was der aktive Plan aus dem Netz voraussichtlich kostet;
  - *Kosten*: öffnet die Seite Kosten (nur, wenn sie in *Einstellungen* eingeschaltet ist);
  - *Anleitung*: öffnet die Anleitung. Gedrückt halten für die niederländische Version.

### EV Solar Master Control

- **HESC an:** der Hauptschalter. Aus heißt, HESC bewertet gar nichts.
- **Schattenmodus (nur zusehen):** HESC bewertet und zeigt alles, schaltet aber nichts. Fang immer
  hier an.
- **HPVC hat die Paneele freigegeben:** erscheint, solange HPVC die Sonne für das Auto durchlässt.

### Status

- **Zustand:** was HESC gerade tut, und warum.
- **Letzte Aktion:** das Letzte, was HESC getan hat.
- **Heute:** die Zahl der Sitzungen mit Sonne und der HPVC-Freigaben heute.
- **Empfehlung:** die Startschwelle, die HESC aus deinen eigenen Sitzungen empfiehlt, die
  starteten, während HPVC deine Paneele begrenzte, neben der aktuellen Schwelle. Tippe darauf, um zu
  *Einstellungen* zu gehen.
- **Bericht erstellen** darunter erstellt einen Bericht mit allem, was HESC gemessen und
  entschieden hat. Ist er fertig, wird die Taste zu **Bericht ansehen**.

### Live

Die Werte von genau jetzt:

| Zeile | Was sie zeigt |
|---|---|
| **Netz** | wie viel du ins Netz einspeist oder daraus beziehst |
| **Hausspeicher** | ihre Leistung (positiv = laden) und ihr durchschnittlicher Ladestand; nur, wenn *Hausspeicher und Auto* ausgefüllt ist |
| **Ladestand Auto** | der Ladestand des Autos, *Auto gilt als voll bei* und woher der Wert kommt |
| **Strompreis jetzt** | der Endpreis und der Marktpreis; nur, wenn Strompreise eingerichtet sind |
| **Sonne, die heute noch kommt** | wie viele kWh die Sonne heute voraussichtlich noch bringt |
| **Beste Zeit zum Anschließen** | der nächste Zeitraum mit genug Sonne, um mit Sonne zu starten (das Grün in den Grafiken), zum Beispiel *Sonne morgen 11:00–17:30*; wird keine solche Sonne erwartet, stattdessen die günstigste Netzstunde der bekannten Preise |

### Aktueller Stand

Ob das Auto angesteckt ist, die Wallbox auf Laden mit Sonne eingestellt ist, HPVC deine Paneele
begrenzt und eine Freigabe läuft, mit einem Zeitstrahl der letzten 12 Stunden darunter. Ist
*Hausspeicher und Auto* eingeschaltet und das Auto angesteckt, zeigt eine zusätzliche Zeile, was der
Kickstart gerade tut.

### Solarprognose und Ist · Auto

Die letzten 12 Stunden. Oben: Solarleistung, Prognose und Ladeleistung des Autos jetzt.

- lila: die Prognose;
- orange: was deine Paneele wirklich erzeugt haben;
- blau, unter der Nulllinie: was ins Auto ging;
- die gestrichelte Linie: die Startschwelle.

### Erwartete Lademöglichkeiten mit Sonne

Die erwartete Sonne für heute und morgen, pro halbe Stunde. Oben: die **Startschwelle** und die
**Weiterladeschwelle**. Grüne Balken = genug Sonne, um das Laden zu starten, orange = genug zum
Weiterladen, aber nicht zum Starten, grau = zu wenig. *Jetzt* markiert den aktuellen Moment.

### Erwartetes Solarladen

Wann das Auto heute und morgen voraussichtlich mit Sonne lädt, zwischen Sonnenaufgang und
Sonnenuntergang, und wie viele Stunden.

## Ladeplan

![Charge plan](images/charge-plan.png)

- **Ladeplan · ein fester Tag pro Woche:** ein Tag, eine Uhrzeit und ein Ladeziel, zum Beispiel
  100 % am Freitag um 08:00. Er kommt jede Woche wieder. *Aktiv* schaltet ihn ein oder aus.
- **Ladeplan · Wochenplanung:** hake die Tage an (*Mo* … *So*), wähle eine Uhrzeit und ein
  Ladeziel, zum Beispiel 80 % an Werktagen um 07:00. Sind beide Pläne aktiv, gewinnt der frühere.
- **Urlaubsmodus:** Der Wochenplan ruht, solange du weg bist; der Plan für einen Tag und das Laden
  mit Sonne laufen weiter. *Urlaub bis (optional)*: am Tag nach diesem Datum schaltet er sich von
  selbst aus.
- **Einen Tag überspringen (freier Tag):** Wähle ein Datum, und der Wochenplan tut an diesem Tag
  nichts; stattdessen zählt der nächste Tag des Plans. Der Plan selbst bleibt, wie er ist. Wird
  angezeigt, solange der Wochenplan an ist.
- **Jetzt laden bis:** lädt sofort aus dem Netz, bis das Auto den gewählten Ladestand erreicht;
  danach geht die Wallbox zurück in ihren eigenen Solarmodus. Es hört von selbst auf, wenn das Ziel
  erreicht ist, das Auto abgesteckt wird oder nach der erwarteten Ladezeit × 1,5 plus eine Stunde.
  Es braucht eingerichtetes Netzladen (*Einstellungen → Ladeplan und Meldungen*) und den
  Ladestand des Autos; nicht innerhalb von 3 % unter dem Ziel, nicht im Schattenmodus.
- **Ladeeinstellungen:**
  - *Günstige Gelegenheiten nutzen* und *Günstig unter* — auch ohne Plan laden, wenn der Preis sehr
    niedrig ist;
  - *Nutzbare Akkukapazität* und *Ladeleistung aus dem Netz* — was dein Auto wirklich fasst und was
    deine Wallbox aus dem Netz liefert.
- **Status Ladeplan:** was HESC für welchen Plan und bis wann tut: Ladezeit, durchschnittlicher
  Strompreis, Ladestand jetzt, Ziel, was noch nötig ist, und der Status.
- **Preisgrafik:** der Preis für heute und morgen als glatte Linie: hellgrau = der Preis, dunkelgrau
  = ein erwarteter Preis (die echten Preise für morgen sind noch nicht bekannt). Farbige Flächen
  unter der Linie zeigen, wann es sich lohnt, das Auto angeschlossen zu haben: grün = genug Sonne
  erwartet, um mit Sonne zu starten (*Sonne: starten*), bernsteinfarben = genug Sonne zum
  Weiterladen, kein neuer Start (*Sonne: weiterladen*), blau = Netzplan, lila gestreift = eine
  günstige Gelegenheit. Fällt eine günstige Gelegenheit in eine sonnige Zeit, siehst du das Grün
  durch die lila Streifen.

## Einstellungen

![Settings](images/settings.png)

Drei Spalten: **1 · Deine Wallbox**, **2 · Quellen** und **3 · Erweitert**. Die meisten Felder
kommen aus der Einrichtung; die Taste *Quellen und Wallbox ändern* öffnet sie.

**1 · Deine Wallbox**
- *Wallbox-Typ* und *Erneut suchen* — HESC sucht die Entitäten deiner Wallbox.
- *Felder Wallbox* — was HESC verwendet; sie öffnen sich von selbst, wenn etwas fehlt.
- **Prüfung der Einrichtung** — eine Zeile pro Teil mit einem Haken. Ein Teil, der nicht stimmt,
  öffnet sich und sagt, was fehlt.
- **Empfehlung** — die aktuelle Startschwelle und die Empfehlung. Darunter die Zeile *Phasen* mit
  dem Phasenhinweis, wenn du die Netzleistung pro Phase gewählt hast. *Empfehlung automatisch
  anwenden* lässt HESC die Schwelle in kleinen Schritten in Richtung der Empfehlung bewegen. Ohne
  HPVC gibt es keine Empfehlung zur Schwelle, deshalb zeigt diese Karte dann nur die aktuelle
  Schwelle, und der Schalter ist ausgeblendet.
- **Deine Einstellungen** — deine Schwellen, Auto, Zeiten, Ladeplan und Empfehlung auf einen Blick.
- *Sichern*, *Sicherung wiederherstellen*, *Standardwerte*.
- **Ladekosten** — *An* zeigt die Seite Kosten; *Optionen* zeigt den Wert einer Solar-kWh,
  *Endpreis* oder Aufschlag und MwSt.

**2 · Quellen**
- *HPVC verwenden* — einschalten, wenn du HPVC verwendest (standardmäßig aus).
- *Solar und Netz aus HPVC* — die Sensoren von HPVC für Solar und Netz übernehmen. Nur, wenn HPVC
  alle deine Paneele sieht. Aus bringt deine eigenen Sensoren zurück.
- *Quellen ändern* — zeigt die Sensoren für Solar, Netz und Prognose und die Entitäten von HPVC.
- *Weitere Felder zeigen* — zum Beispiel *Auto gilt als voll bei* und die Werte, die "kein Auto"
  bedeuten.
- **Eigene Wetterstation** — *An* und *Optionen* (Einstrahlungssensor und seine Schwellen, und
  welche Solarprognose HESC verwendet).

**3 · Erweitert — nur bei Bedarf**
- *Ladeschwellen* — die Start- und Weiterladeschwelle, *Startschwelle nach Jahreszeit* und *Auto
  gilt als ladend über*.
- *Zeiten* — wie lange HESC bei jedem Schritt einer Freigabe wartet.
- *Empfehlung* — über wie viele Tage und ab wie vielen Sitzungen.
- *Ladeplan und Meldungen* — Start/Stopp-Schalter, *Zurück in den Solarmodus*, der Wert
  für "jetzt laden", Preisquelle, Preissensor, *Preise pro*, Währung, die letzte Prüfung, Telefone
  für Benachrichtigungen (mit einer Testtaste) und die Morgenübersicht.
- **Mindestladung** — *An* und *Optionen*: das Auto mindestens auf einem Ladestand halten, in den
  günstigsten Viertelstunden.
- **Hausspeicher und Auto** — *An* und *Optionen*: Ladestand- und Leistungssensoren der
  Hausspeicher, ihre Größe, *Kickstarts pro Tag* und *Minimale Restsonne für das Auto*.

Mehr zu jeder Einstellung: [03 · Einstellungen](03-settings.de.md).

## Kosten

![Costs](images/costs.png)

Wird mit der Anzeige *Kosten* auf der *Übersicht* geöffnet, wenn die Seite Kosten in
*Einstellungen* eingeschaltet ist.

- **Zeitraum:** *Tage*, *Wochen*, *Monate*, *Quartale* oder *Jahr*.
- **Summen:** wie viele kWh ins Auto gingen, von der Sonne und aus dem Netz, was der Netzanteil
  gekostet hat, und der Wert der Solar-kWh.
- **Kacheln:** eine pro Tag (oder Woche, Monat …), mit den kWh von der Sonne (grün) und aus dem Netz
  (grau) und den Kosten.
- **In Tabelle exportieren (CSV):** schreibt zwei Dateien, pro Tag und pro Monat, die sich in Excel
  öffnen lassen.

## Anleitung, Guide und Uitleg

Die Anleitung, die ins Dashboard eingebaut ist: auf Deutsch (*Anleitung*), Englisch (*Guide*) und
Niederländisch (*Uitleg*). Derselbe Text wie
[07 · Intelligentes Laden erklärt](07-smart-charging-explained.de.md). Das ⓘ neben einer
Überschrift öffnet sie auch.

## Kiosk

![Kiosk](images/kiosk.png)

Eine Seite für ein Tablet an der Wand: beide Pläne und die Planeinstellungen, was HESC gerade tut,
der Status des Plans und die Live-Werte. Öffne `/hesc-v3/kiosk` auf dem Tablet. Das Menü und die
obere Leiste von Home Assistant sind auf dieser Seite ausgeblendet; hänge `?disable_km` an die
Adresse, um sie zu behalten. Keine zusätzliche Karte nötig (seit 3.0.0). Nach einem Neustart von
Home Assistant lädt sich die Seite selbst neu.

Siehe auch: [05 · Wallboxen und Quellen](05-chargers-and-sources.de.md) ·
[09 · Fehlerbehebung](09-troubleshooting.de.md)

## Auf Telefon und Uhr

<img src="images/main-phone.png" width="300" alt="HESC on a phone">

HESC funktioniert mit der Home-Assistant-App auf einem iPhone oder einem Android-Telefon, auch
unterwegs. Was du tun kannst, ist auf beiden gleich; nur die Tasten auf dem Telefon unterscheiden
sich.

**Was HESC bietet (beide Telefone)**

- Der Sensor *Zusammenfassung für Telefon und Uhr*: eine Zeile, zum Beispiel *EV 72% → 80% by Sat 24-10 07:00 ·
  Charging on sun · grid Fri 02:00* oder *EV 91% · not plugged in*. Seine Attribute enthalten die
  einzelnen Werte (Ladestand, Ziel, fertig um, nächste Netz-Viertelstunde, angesteckt, jetzt laden)
  für deine eigenen Templates.
- Aktionen:
  - **HESC: Ladeplan festlegen** (`hesc.set_charge_plan`: Tag, Uhrzeit, Ziel — alle optional; die
    Uhrzeit ist eine volle oder halbe Stunde). Einen Plan festlegen schaltet ihn ein.
  - **HESC: Ladeplan aus** (`hesc.charge_plan_off`).
  - **HESC: Jetzt laden** (`hesc.charge_now`: Ziel) und **HESC: Jetzt laden beenden**
    (`hesc.charge_now_off`).
  - **HESC: Einen Tag des Wochenplans überspringen** (`hesc.skip_plan_day`: Datum, optional —
    weggelassen: der nächste Tag des Wochenplans) und **HESC: Überspringen eines Tages rückgängig
    machen** (`hesc.undo_skip_plan_day`).
- Fertige Tasten für einen Tipp: *Jetzt bis zum Ladeziel des Plans laden*, *Jetzt laden beenden*,
  *Nächsten Tag des Wochenplans überspringen*, *Überspringen eines Tages rückgängig machen* und
  *Ladeplan aus*.
- **Benachrichtigungen:** wähle dein Telefon auf der Seite *Einstellungen*.

Ein Widget auf dem Telefon, eine Schnelleinstellungskachel oder eine Uhr kann eine dieser Tasten
drücken oder ein *Skript* starten. Für alles andere (ein anderes Ziel, eine andere Uhrzeit) packst
du die Aktion in ein eigenes Skript (*Einstellungen → Automationen & Szenen → Skripte*). Zum
Beispiel in YAML:

```yaml
hesc_charge_tomorrow_0700_95:
  alias: "HESC: charge for tomorrow 07:00 to 95 %"
  sequence:
    - action: hesc.set_charge_plan
      data: {day: Tomorrow, time: "07:00", goal: 95}
hesc_charge_now_to:
  alias: "HESC: charge now to"
  fields:
    goal:
      default: 80
      selector: {number: {min: 50, max: 100, step: 5, unit_of_measurement: "%"}}
  sequence:
    - action: hesc.charge_now
      data: {goal: "{{ goal | int(80) }}"}
hesc_skip_next_day:
  alias: "HESC: skip the next day of the weekly plan"
  sequence:
    - action: hesc.skip_plan_day
```

**iPhone und Apple Watch**

- **Widget oder Uhr:** füge *Zusammenfassung für Telefon und Uhr* in der Home-Assistant-App als
  Widget oder als Komplikation auf der Uhr hinzu.
- **Siri oder Kurzbefehle:** erstelle einen Kurzbefehl mit der Home-Assistant-Aktion *Aktion
  ausführen* (eine der HESC-Aktionen oben) oder *Skript ausführen*. Sag dann zum Beispiel *Hey Siri,
  lade das Auto für morgen*.
- **Sperrbildschirm:** Die Widgets *Details* und *Gauge* aktualisieren sich, wenn sie eine stille
  Benachrichtigung bekommen. HESC schickt eine an die iPhones und iPads in seiner Telefonliste, wenn
  sich etwas in der Zusammenfassung ändert (angesteckt, Plan, Ziel, Laden, Ladestand pro 10 %),
  höchstens alle 20 Minuten, damit das Tagesbudget, das iOS diesen Aktualisierungen gibt, nie
  aufgebraucht wird. Widgets auf dem Homescreen aktualisieren sich etwa alle 15 Minuten; das
  entscheidet iOS. Nicht im Schattenmodus.

**Android-Telefon und Wear-OS-Uhr**

- **Widget:** das Widget *Entity state* mit *Zusammenfassung für Telefon und Uhr* oder das Widget
  *Template* für deinen eigenen Text. Android-Widgets aktualisieren sich von selbst: alle 30 Minuten,
  solange der Bildschirm an ist, oder sofort, wenn du die Home-Assistant-App Benachrichtigungen lesen
  lässt, mit *Real-time* an (Android-Einstellungen; braucht etwas mehr Akku). HESC schickt
  Android-Telefonen keine Aktualisierungsbenachrichtigung; das ist ein iOS-Befehl und würde als
  Nachricht erscheinen.
- **Ein Tipp:** das Widget *Action button* oder eine *Schnelleinstellungskachel* (in der App:
  *Einstellungen → Companion-App → Manage tiles*), die jeweils eine der HESC-Tasten drückt oder eines
  deiner HESC-Skripte ausführt.
- **Sprache:** Stelle die Home-Assistant-App als Assistenten des Telefons ein und bitte Assist, ein
  HESC-Skript auszuführen.
- **Wear-OS-Uhr:** eine Kachel *Shortcuts* mit den HESC-Tasten oder deinen HESC-Skripten und eine
  Komplikation *Entity state* mit *Zusammenfassung für Telefon und Uhr*.

Der Android-Teil folgt der Dokumentation der Home Assistant Companion-App; er wurde noch nicht auf
einem Android-Telefon ausprobiert.
