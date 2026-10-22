# 05 · Wallboxen und Quellen

*English: [05-chargers-and-sources.md](05-chargers-and-sources.md) · Nederlands: [05-chargers-and-sources.nl.md](05-chargers-and-sources.nl.md)*

**Kurz gesagt**
- HESC spricht nie direkt mit deiner Wallbox, deinem Auto oder deinem Prognosedienst. Es arbeitet
  nur über Home Assistant: Es liest und steuert die Entitäten, die die Integrationen deiner Wallbox,
  deines Autos und deiner Prognose dort anlegen.
- Wähle deinen Wallbox-Typ in der Einrichtung; HESC sucht dann selbst die passenden Entitäten.
- Jede Wallbox braucht eine bestimmte Menge Sonne, bevor sie mit Sonne startet. HESC kennt das pro
  Marke und empfiehlt nie ein niedrigeres Startniveau.
- Der Ladestand des Autos, eine Solarprognose und Strompreise lassen HESC genauer planen, sind aber
  nicht nötig.

## Deine Wallbox

### Was HESC von ihr braucht

| Was | Warum | Beispiel |
|---|---|---|
| **Ist ein Auto angeschlossen?** | Ohne Auto gibt es nichts zu tun | ein Sensor "angeschlossen" oder ein Status wie `Ready` / `Charging` |
| **Ladeleistung** | Um zu sehen, ob das Auto wirklich lädt | in W oder kW |
| **Die Einstellung für Laden mit Sonne** | In dieser Einstellung startet die Wallbox von selbst, wenn genug Sonne da ist | Wallbox *Eco*, Alfen *Green*, Zappi *Eco+* |
| **Start/Stopp** (für den Ladeplan) | Um in den günstigsten Viertelstunden aus dem Netz zu laden | ein Schalter für Pause/Fortsetzen oder ein Modus "jetzt laden" |
| **Ladestrom** (optional) | Um das Laden an die Sonne anzupassen | Wallbox *Maximum charging current* |

Eine pausierte Wallbox zählt als 0 W, egal welche Leistung sie noch meldet: Manche Wallboxen (zum
Beispiel die Wallbox) zeigen nach einer Pause noch minutenlang ihre letzte Leistung. Pausiert
heißt: Der Start/Stopp-Schalter ist aus, oder der Status der Wallbox sagt *paused*.

### Wallbox-Typen

Wähle den Typ in der Einrichtung (Schritt **Wallbox**) oder später auf der Seite *Einstellungen*.
HESC sucht dann die Entitäten deiner Wallbox in Home Assistant und füllt sie aus. Für jede Marke
weiß HESC, welche Einstellung der Wallbox "mit Sonne laden" bedeutet (bei einer Wallbox der Marke
Wallbox zum Beispiel *Eco*) und welcher Status bedeutet, dass kein Auto angeschlossen ist.

- Findet HESC genau eine passende Entität, füllt es sie aus. Findet es mehrere, lässt es das Feld
  leer, und du wählst.
- HESC überschreibt nie, was du selbst ausgefüllt hast.
- Die Suche funktioniert auch, wenn dein Home Assistant Namen in einer anderen Sprache verwendet
  (Deutsch oder Niederländisch).

| Wallbox | Einstellung für Laden mit Sonne | Hinweis |
|---|---|---|
| **Wallbox** (Pulsar Plus, Copper) | `eco_mode`, `full_solar` | in der Praxis getestet |
| **Alfen Eve** | `Green` | braucht einen Zähler am Lastmanagement der Alfen |
| **Peblar** | `pure_solar` | |
| **myenergi Zappi** | `Eco+` | wähle den Leistungssensor "internal load" der Zappi selbst |
| **go-e Charger** | `4` (Eco) | braucht Netz-/Solardaten (go-e Controller oder aus Home Assistant geschickt) |
| **Fronius Wattpilot** | `Eco` | verwendet den Fronius-Zähler |
| **SMA EV Charger** | `optimized_charging` | über den Sunny Home Manager |
| **Ohme** | `on` (Solar Boost) | nur teilweise: Home Pro mit eigener Messzange |
| **Easee** | `on` | nur mit einem Easee Equalizer; wähle seinen Schalter für Überschussladen selbst |
| **evcc** (any charger) | `pv`, `smart` | wähle die Entitäten des evcc-Ladepunkts, nicht die der Wallbox selbst |
| **Other (manual)** | deine Wahl | fülle die Felder selbst aus |

Wallboxen ohne eigene Einstellung für Laden mit Sonne (zum Beispiel Zaptec, Tesla Wall Connector oder einfaches
OCPP) lassen sich über evcc verwenden.

Nur die Wallbox wurde in der Praxis getestet. Mit einer anderen Wallbox: Lass den Schattenmodus ein
paar sonnige Tage an, prüfe, ob die Karte *Live* alle Werte zeigt und ob die Wallbox nach dem
Netzladen zu ihrem Laden mit Sonne zurückkehrt.

**Ein Planer pro Wallbox.** Schalte Ladepläne in der eigenen App der Wallbox oder in anderen
Integrationen aus, solange HESC das Laden plant.

### Wie viel Sonne eine Wallbox zum Starten braucht

Eine Wallbox, die mit Sonne lädt, startet erst, wenn genug Überschuss da ist. Das übliche Minimum
für jede Wallbox ist 6 A pro Phase: etwa **1,4 kW auf einer Phase** und **4,1 kW auf drei Phasen**.
Manche Marken starten niedriger:

| Wallbox · Modus | 1 Phase | 3 Phasen |
|---|---|---|
| Wallbox · Eco | ± 460 W | ± 1,4 kW, mindestens 480 W auf **jeder** Phase |
| Wallbox · Full Green | 1,4 kW | 4,1 kW |
| Alfen · Green | 1,4 kW | 4,2 kW |
| Zappi · Eco+ | 1,4 kW | 4,2 kW |
| Ohme · Solar Boost | 0,72 kW (+ 0,72 kW aus dem Netz) | 4,1 kW |
| Easee | 1,4 kW | 4,1 kW, 6 A auf **jeder** Phase |
| Andere Marken | 1,4 kW | 4,1 kW (Standard) |

HESC verwendet das als Untergrenze: Die Empfehlung zur Startschwelle geht nie unter das, was deine
Wallbox braucht.

### Eine Phase oder drei?

Das stellst du nicht ein, und HESC wählt es nicht. Die Zahl der Phasen ist das Kleinste von dem,
was dein Hausanschluss, deine Wallbox und dein Auto können. Ein Auto mit einem einphasigen
Ladegerät lädt immer auf einer Phase, auch an einer dreiphasigen Wallbox. HESC misst es, während
das Auto lädt.

**Phasenhinweis.** Zeigt dein Zähler die Leistung pro Phase (die meisten Smart Meter tun das),
zählt HESC, wie die Sonne über die Phasen verteilt ist. Bei Wallboxen, die Sonne auf jeder Phase
brauchen (Wallbox Eco, Easee), kann eine schwache Phase die Wallbox am Starten hindern. Der Hinweis
auf der Seite *Einstellungen* durchläuft drei Stufen:
1. **wird gemessen** — noch nicht genug sonnige Tage;
2. **vorläufig** — nach etwa zwei Wochen;
3. **bestätigt** — nach genug Tagen in der sonnigsten Zeit des Jahres an deinem Standort.

Er ist nur zur Info; HESC ändert nichts von selbst.

### Ladestrom

Lässt deine Wallbox HESC den Ladestrom einstellen (Wallbox: *Maximum charging current*), senkt
HESC den Strom, während der Ladeplan aus dem Netz lädt, damit mehr von der Energie von der Sonne
kommt — solange das Auto trotzdem rechtzeitig voll ist. Danach geht der Strom zurück auf den
vorigen Wert. Das ist normales Verhalten; es gibt keinen Schalter dafür. Hast du keinen Ladestrom
ausgefüllt, ändert HESC den Strom nie.

## Der Ladestand deines Autos

Nicht nötig, aber der Ladeplan und "Auto ist voll" arbeiten damit viel genauer. Jeder Sensor für
den Ladestand in % funktioniert, meist aus der Integration deiner Automarke. Noch kein Sensor? Die
Einrichtung sagt dir, wo du einen für dein Auto findest.

**Regelmäßige Updates funktionieren am besten.** Ein Wert, der alle paar Minuten aktualisiert
wird, gibt die beste Planung. Viele Auto-Integrationen aktualisieren seltener, um die
12-V-Batterie des Autos zu schonen; das ist in Ordnung.

**Woher HESC den Ladestand nimmt.** HESC nimmt die erste dieser Quellen, die einen Wert hat. Fällt
die erste aus, geht es zur nächsten:
1. der Sensor für den Ladestand, den du gewählt hast;
2. ein zweiter Akkusensor desselben Autos, wenn HESC einen findet;
3. der letzte bekannte Ladestand dieser Ladesitzung, plus das, was seitdem geladen wurde;
4. der übliche Ladestand beim Anschließen in den letzten 14 Tagen.

Das Dashboard zeigt, welche Quelle verwendet wird.

**Bekanntes Verhalten:** Manche Auto-Integrationen schicken direkt nach einem Neustart von Home
Assistant kurz einen falschen Wert (zum Beispiel 99,9 %), bis zu ihrem nächsten Update. HESC denkt
dann ein paar Minuten, das Auto sei voll, und verschiebt vielleicht das Laden. Mit dem nächsten
richtigen Wert wird alles neu berechnet; nichts bleibt falsch.

## Solarprognose

| Was du hast | Was HESC tut |
|---|---|
| **Solcast** | Beste Wahl. HESC verwendet die vorsichtige Schätzung zum Entscheiden und die normale Schätzung zum Vergleich mit dem, was wirklich passiert. Tipp: Füge in Solcast unter *Attribute breakdown* `attr_brk_halfhourly` hinzu, für Blöcke von 30 Minuten. |
| **Open-Meteo Solar Forecast** oder **Forecast.Solar** | Funktioniert genauso; HESC rechnet es selbst um. |
| **Keine Prognose** | HESC lädt mit gemessener Solarleistung und plant das Netzladen so, als käme keine Sonne (nie zu spät). Der Kickstart ist aus. Ein Hinweis unter *Einstellungen → Reparaturen* erklärt, wie du eine Prognose hinzufügst. |

**Wetterstation (optional).** Ein eigener Einstrahlungssensor (W/m²) oder ein Luxmeter kann als
zusätzliche Prüfung dienen. Schalte *Eigene Wetterstation verwenden* in der Einrichtung ein.
Beginne mit niedrigen Schwellen; nach ein paar Wochen zeigt der Bericht, wie gut sie zu deiner
Solarleistung passt.

## Strompreise

Nur nötig für den Ladeplan, günstige Gelegenheiten und die Seite Kosten, und nur sinnvoll mit einem
**dynamischen** Vertrag (ein Preis pro Viertelstunde oder Stunde). Stelle die Preisquelle unter
*Einstellungen → Erweitert → Ladeplan und Meldungen* ein.

| Preisquelle | Quellen |
|---|---|
| *Price list in sensor* | Nord Pool (HACS), ENTSO-E, Energi Data Service, EPEX Spot, Frank Energie, Zonneplan, Octopus Energy (Agile), Amber Electric, PVPC (Spanien) |
| *EnergyZero / ANWB Energie*, *EasyEnergy*, *Tibber*, *Nord Pool (official)* | wähle einen beliebigen Sensor dieser Integration; HESC holt die Preise alle 30 Minuten selbst |

- HESC plant immer in Viertelstunden; Preise pro Stunde und pro halbe Stunde werden in
  Viertelstunden aufgeteilt.
- Währungen: EUR, SEK, DKK, NOK, GBP und AUD. *Automatic* nimmt die Währung aus dem Preissensor.
- Feiertage für die Preisprognose kommen aus der Integration **Workday** deines Landes.
- Netzentgelte, die sich im Laufe des Tages ändern, werden nicht abgebildet; verwende
  *Endpreise* aus deiner Quelle, wenn du sie hast.

## Hausspeicher (optional)

Für den Kickstart liest HESC den Ladestand (%) und die Leistung (W) deiner Hausspeicher und ihre
Gesamtgröße. Eine positive Leistung bedeutet, dass der Speicher lädt. Siehe die Seite
*Einstellungen*, *Hausspeicher und Auto*.
