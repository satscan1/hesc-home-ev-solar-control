<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/custom_components/hesc/frontend/hesc-logo.png" width="160" alt="HESC"></p>

# HESC — Home EV Solar Control

*English: [README.md](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/README.md) · Nederlands: [README.nl.md](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/README.nl.md)*

HESC lädt dein Elektroauto so viel wie möglich mit deinem eigenen Solarstrom, und aus dem Netz zu
den günstigsten Zeiten, wenn die Sonne nicht reicht. Es läuft in Home Assistant.

<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/docs/images/infographic-de.png" width="100%" alt="HESC v3 auf einen Blick"></p>

<p align="center"><img src="https://raw.githubusercontent.com/satscan1/hesc-home-ev-solar-control/main/docs/images/main.png" width="90%" alt="HESC dashboard"></p>

## Was HESC tut

- **Lädt mit Sonne.** HESC verfolgt deine Solarprognose und deine Solarleistung und lässt deine
  Wallbox im richtigen Moment mit Sonne starten.
- **Plant das Netzladen.** Sag HESC, wann das Auto fertig sein muss und wie voll. HESC wählt mit
  dynamischen Preisen die günstigsten Viertelstunden und lässt Platz für die Sonne, die noch kommt.
- **Arbeitet mit deinem Hausspeicher zusammen.** Würden die Hausspeicher die ganze Sonne nehmen,
  gibt HESC dem Auto einen Kickstart. So kommt das Auto an die Reihe, statt zu warten, bis die
  Speicher voll sind. HESC steuert den Hausspeicher nie selbst: Das funktioniert mit einem Speicher,
  der darauf reagiert, was das Haus verbraucht (siehe
  [So funktioniert es](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.de.md#hausspeicher-und-auto-kickstart)).
- **Zeigt, was passiert.** Ein Dashboard mit heute, der Prognose, Kosten und Empfehlungen; und ein
  Bericht, den du jederzeit öffnen kannst.

## Neu in v3

HESC v3 ist eine Home-Assistant-Integration. Es kann alles, was HESC v2 kann, und dazu:

- **Kein Node-RED und kein YAML-Package mehr.** Du installierst eine Integration und füllst eine
  Einrichtung aus.
- **Findet deine Wallbox und dein Auto selbst**, auch wenn Home Assistant deutsche oder niederländische
  Entitätsnamen verwendet.
- **Funktioniert ohne Solarprognose**, wenn du keine hast (Solcast, Open-Meteo und Forecast.Solar
  werden unterstützt).
- **Passt den Ladestrom an** bei Wallboxen, die das erlauben, damit mehr Sonne ins Auto geht.
- **Kennt das Startniveau deiner Wallbox.** Die Empfehlung geht nie unter das, was deine Wallbox
  braucht, um mit Sonne zu starten.
- **Phasenhinweis**, wenn dein Zähler die Leistung pro Phase zeigt: Er sagt dir, ob eine Phase
  deine Wallbox bremst.
- **Das Dashboard kommt mit HESC**: *HESC* in der Seitenleiste, nichts einzufügen.
- **Jetzt laden** bis zu einem Ladestand, den du wählst, aus dem Netz, danach von selbst zurück zur
  Sonne.
- **Einen Tag überspringen** im Wochenplan (ein freier Tag), ohne den Plan zu ändern.
- **Auf Telefon und Uhr** (iPhone, Apple Watch, Android, Wear OS): eine Zusammenfassung in einer
  Zeile für ein Widget, Aktionen für Siri und Kurzbefehle und Tasten für einen Tipp. Siehe
  [Dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.de.md#auf-telefon-und-uhr).

HESC v2 bleibt verfügbar. Du kannst v3 neben v2 laufen lassen und umsteigen, wenn du bereit bist;
siehe [Umstieg von v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.de.md).

## Wie HESC getestet wird

Jede Version wird vor dem Release in einem Simulator getestet, der ganze Tage in Sekunden abspielt:
feste Szenarien (sonniger Sommertag, bewölkter Wintertag, negative Preise, eine Wallbox, die nicht
starten will, ein Neustart mitten in einem Plan, …) und echte, aufgezeichnete Tage, für jede
unterstützte Wallbox. Eine neue Version muss genauso entscheiden wie die vorige, außer die Änderung
ist so gewollt.

## Was du brauchst

- Home Assistant **2026.10.1** oder neuer.
- Deine **Wallbox** in Home Assistant, über ihre eigene Integration.
- Den **Ladestand deines Autos** in Home Assistant (empfohlen). HESC funktioniert auch ohne, plant
  damit aber genauer.
- Optional: eine **Solarprognose**, **dynamische Strompreise**, einen **Hausspeicher** und
  [Home PV Control (HPVC)](https://github.com/BioPC/home-pv-control) 1.5.1 oder neuer.

## Installation in drei Schritten

1. Installiere die Integration (HACS oder von Hand).
2. Füge **HESC v3** unter *Einstellungen → Geräte & Dienste* hinzu und fülle die Einrichtung aus.
3. Öffne **HESC** in der Seitenleiste: Das Dashboard und seine Karten kommen mit HESC, sonst ist
   nichts zu installieren.

HESC startet im **Schattenmodus**: Es schaut zu und zeigt, was es tun würde, schaltet aber nichts,
bis du den Schattenmodus ausschaltest. Schritt für Schritt: [Installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.de.md).

## Anleitung

| | English | Deutsch |
|---|---|---|
| Installation | [01-installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.md) | [01-installation](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/01-installation.de.md) |
| Umstieg von v2 | [02-upgrade-from-v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.md) | [02-umstieg-von-v2](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/02-upgrade-from-v2.de.md) |
| Einstellungen | [03-settings](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/03-settings.md) | [03-einstellungen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/03-settings.de.md) |
| So funktioniert es | [04-how-it-works](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.md) | [04-so-funktioniert-es](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/04-how-it-works.de.md) |
| Wallboxen und Quellen | [05-chargers-and-sources](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/05-chargers-and-sources.md) | [05-wallboxen-und-quellen](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/05-chargers-and-sources.de.md) |
| Dashboard | [06-dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.md) | [06-dashboard](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/06-dashboard.de.md) |
| Intelligentes Laden erklärt | [07-smart-charging-explained](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/07-smart-charging-explained.md) | [07-intelligentes-laden-erklärt](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/07-smart-charging-explained.de.md) |
| Ein Tag mit HESC | [08-a-day-with-hesc](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/08-a-day-with-hesc.md) | [08-ein-tag-mit-hesc](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/08-a-day-with-hesc.de.md) |
| Fehlerbehebung | [09-troubleshooting](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/09-troubleshooting.md) | [09-fehlerbehebung](https://github.com/satscan1/hesc-home-ev-solar-control/blob/main/docs/09-troubleshooting.de.md) |

