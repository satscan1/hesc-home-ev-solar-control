# 01 · Installation

*English: [01-installation.md](01-installation.md) · Nederlands: [01-installation.nl.md](01-installation.nl.md)*

**Kurz gesagt**
- Installiere die Integration, füge sie in Home Assistant hinzu und fülle die Einrichtung aus. HESC
  füllt das meiste selbst aus.
- Das Dashboard und seine Karten kommen mit HESC: sonst ist nichts zu installieren.
- HESC startet im Schattenmodus: Es schaut zu und zeigt, was es tun würde, schaltet aber nichts.
  Schalte den Schattenmodus aus, wenn du dem vertraust, was du siehst.
- Kommst du von HESC v2? Lies auch [02 · Umstieg von v2](02-upgrade-from-v2.de.md).

## 0. Bevor du anfängst

- **Home Assistant 2026.10.1 oder neuer.**
- **HACS**, um HESC zu installieren (siehe Schritt 1). HESC braucht keine anderen Karten aus HACS.
- **Deine Wallbox** in Home Assistant, über ihre eigene Integration. HESC muss sehen können, ob ein
  Auto angeschlossen ist, wie viel Leistung ins Auto geht, und die Einstellung, mit der die Wallbox
  mit Sonne lädt (zum Beispiel Eco bei einer Wallbox der Marke Wallbox).
- **Ein Planer pro Wallbox.** Schalte Ladepläne in der App deiner Wallbox oder in anderen
  Integrationen aus, solange HESC dein Laden plant. Zwei Planer an einer Wallbox kommen sich in
  die Quere. Prüfe nach einem Update der App oder der Firmware der Wallbox, dass nicht von selbst
  ein Ladeplan aufgetaucht ist.
- **Der Ladestand deines Autos** (empfohlen). Meist über die Integration deiner Automarke. HESC
  funktioniert auch ohne, aber der Ladeplan ist damit genauer. Ein Wert, der sich regelmäßig
  aktualisiert (alle paar Minuten), funktioniert am besten. Kommt kein neuer Wert, rechnet HESC mit
  dem letzten bekannten Ladestand plus dem, was seitdem geladen wurde.
- **Optional:**
  - eine **Solarprognose** — [Solcast](https://github.com/BJReplay/ha-solcast-solar) funktioniert
    am besten; Open-Meteo und Forecast.Solar gehen auch. Ohne Prognose lädt HESC trotzdem mit
    gemessener Solarleistung und plant das Netzladen so, als käme keine Sonne;
  - **dynamische Strompreise**, für den Ladeplan, günstige Gelegenheiten und die Seite Kosten;
  - ein **Hausspeicher**, für den Kickstart;
  - [Home PV Control (HPVC)](https://github.com/BioPC/home-pv-control) **1.5.1 oder neuer**, wenn
    deine Solarpaneele für die Einspeisung begrenzt werden. Ohne HPVC läuft HESC für sich allein
    (eigenständig).

## 1. Die Integration installieren

**Mit HACS**
1. HACS → ⋮ → **Custom repositories** → füge `https://github.com/satscan1/hesc-home-ev-solar-control` hinzu, Typ
   **Integration**.
2. Suche **HESC - Home EV Solar Control** in HACS und klicke auf **Download**.
3. Starte Home Assistant neu.

**Von Hand**
1. Kopiere den Ordner `custom_components/hesc` aus diesem Repository nach
   `/config/custom_components/hesc` auf deinem Home Assistant.
2. Starte Home Assistant neu.

## 2. HESC hinzufügen und die Einrichtung ausfüllen

*Einstellungen → Geräte & Dienste → Integration hinzufügen → **HESC v3***. Die Einrichtung hat fünf
Schritte. HESC durchsucht dein Home Assistant und füllt selbst aus, was es findet. Prüfe es und
klicke auf **OK**.

| Schritt | Was du wählst |
|---|---|
| **Wallbox** | Deinen Wallbox-Typ: Wallbox, Alfen Eve, Peblar, myenergi Zappi, go-e Charger, Fronius Wattpilot, SMA EV Charger, Ohme, Easee, evcc (any charger) oder *Other (manual)*. HESC sucht danach selbst die Entitäten deiner Wallbox. |
| **Quellen** | Woher HESC deine Solarleistung, deine Netzleistung und die Solarprognose bekommt. Hast du HPVC, kann HESC die Sensoren von HPVC verwenden (*Solar- und Netzleistung aus HPVC*). Zeigt dein Zähler die Leistung **pro Phase**, füllt HESC auch die drei Phasensensoren aus; die sind für den Phasenhinweis. |
| **Elektroauto** | Wie HESC sieht, ob das Auto angeschlossen ist, wie viel Leistung hineingeht und wie voll der Akku ist. Kein Sensor für den Ladestand? Der Bildschirm sagt dir, wo du einen für dein Auto findest. |
| **Entitäten der Wallbox** | Mit welcher Einstellung die Wallbox mit Sonne lädt, wie HESC sie startet und stoppt, und den Ladestrom (wenn deine Wallbox HESC ihn einstellen lässt). |
| **HPVC** | Mit HPVC zusammenarbeiten oder *Ohne HPVC (eigenständig)*. Ohne HPVC steht das von selbst auf eigenständig. |

Konnte HESC ein Feld noch nicht ausfüllen, zum Beispiel weil die Integration der Wallbox noch
startete? Dann sucht es erneut, sobald Home Assistant ganz gestartet ist. Du kannst später alles
ändern: *Einstellungen → Geräte & Dienste → HESC v3 → Konfigurieren*.

<p><img src="images/setup-charger.png" width="49%" alt="Setup screen: charger"> <img src="images/setup-sources.png" width="49%" alt="Setup screen: sources"></p>

## 3. Das Dashboard hinzufügen

**Das Dashboard kommt mit HESC.** Sobald HESC eingerichtet ist, steht **HESC** in der Seitenleiste
(Adresse `/hesc-v3`). Du musst nichts anlegen oder einfügen, und jedes Update von HESC bringt das
passende Dashboard mit. HESC trägt die Namen seiner eigenen Entitäten und die Solcast- und
HPVC-Sensoren ein, die du in der Einrichtung gewählt hast. Benennst du sie um, funktioniert das
Dashboard trotzdem weiter.

**Keine Karten aus HACS nötig (seit 3.0.0).** Die Grafiken, der Balken *Erwartetes Solarladen*,
die Seite Kosten und die Seite Kiosk verwenden die eigenen Karten von HESC. Sie kommen mit der
Integration und stehen nach einem Neustart in der Kartenauswahl (suche nach *HESC*). Hast du für
HESC früher apexcharts-card, button-card, card-mod oder kiosk-mode installiert? HESC verwendet sie
nicht mehr; behalte sie, wenn andere Dashboards sie brauchen.

**Deine eigene Kopie, mit einem Klick.** Das Dashboard von HESC kannst du im Dashboard-Editor
nicht ändern. Willst du eine eigene Version (andere Seiten, andere Karten)?

1. *Einstellungen → Dashboards → Dashboard hinzufügen*.
2. Wähle unter *Community dashboards* **HESC · Home EV Solar Control**, gib ihm einen Namen und
   klicke auf *Erstellen*.
3. Deine Kopie hat dieselben Seiten; die Tasten zwischen den Seiten führen zu deiner Kopie.
   Solange du sie nicht änderst, folgt sie jedem Update von HESC. Zum Ändern: der Stift oben
   rechts (*Dashboard bearbeiten*) *→ ⋮ → Kontrolle übernehmen*. Ab dann gehört sie dir und folgt
   HESC nicht mehr.

Nicht in der Liste? Erstelle ein neues leeres Dashboard (*Neues Dashboard von Grund auf*), öffne
es, tippe auf den Stift oben rechts und wähle *⋮ → Raw-Konfigurationseditor*. Ersetze alles durch
diese zwei Zeilen und speichere:

```yaml
strategy:
  type: custom:hesc
```

- **Du hast schon ein Dashboard unter `/hesc-v3`** (eines, das du selbst eingefügt hast, zum
  Beispiel als Tester)? Dann lässt HESC es in Ruhe und zeigt einen Hinweis unter
  *Einstellungen → Reparaturen*. Um zum Dashboard zu wechseln, das mit HESC kommt: lösche dein
  eigenes unter *Einstellungen → Dashboards* und lade danach HESC neu (*Einstellungen → Geräte &
  Dienste → HESC v3 → ⋮ → Neu laden*) oder starte Home Assistant neu.

Die Symbole und das Logo von HESC kommen mit der Integration; du musst nichts installieren.

**Nutzt du Solcast?** Die Grafiken verwenden Blöcke von 30 Minuten. In Solcast: *Konfigurieren →
Attribute breakdown → `attr_brk_halfhourly` hinzufügen*. Ohne das verwendet HESC die Prognose
pro Stunde.

<p><img src="images/add-dashboard.png" width="32%" alt="Add dashboard"> <img src="images/one-click-dashboard.png" width="32%" alt="Your own copy with one click"> <img src="images/card-picker.png" width="32%" alt="HESC cards in the card picker"></p>

## 4. Erst zusehen, dann live

Nach der Installation ist HESC im **Schattenmodus**: Es liest alles und zeigt auf dem Dashboard,
was es tun würde, steuert aber weder deine Wallbox noch HPVC.

1. Lass es ein paar Ladetage laufen. Schau auf die *Übersicht* und drücke ab und zu auf
   **Bericht erstellen** (unter Status).
2. Prüfe, ob die Momente, in denen HESC mit Sonne starten würde, Sinn ergeben, und ob der
   Ladeplan die Viertelstunden wählt, die du erwartest.
3. Schalte dann **Schattenmodus (nur zusehen)** auf der *Übersicht* aus. Ab diesem Moment steuert
   HESC deine Wallbox wirklich.

## Wo HESC seine Dateien ablegt

HESC legt seinen Verlauf, den Preisverlauf für die Preisprognose, den Ladestand beim Anschließen,
die Phasenmessungen und die Sicherung der Einstellungen in `/config/hesc_v3/` ab. Diese Dateien
bleiben, wenn du HESC aktualisierst.

## Aktualisieren

**HACS:** lade das Update herunter und starte Home Assistant neu. **Von Hand:** ersetze den Ordner
`custom_components/hesc` und starte neu. Deine Einstellungen und dein Verlauf bleiben.

## Entfernen

*Einstellungen → Geräte & Dienste → HESC v3 → ⋮ → Löschen*, entferne danach die Integration in
HACS (oder den Ordner `custom_components/hesc`) und starte neu. Der Ordner `/config/hesc_v3/` mit
deinem Verlauf bleibt; lösche ihn selbst, wenn du ihn nicht mehr brauchst. Das Dashboard, das mit
HESC kommt, verschwindet mit.
