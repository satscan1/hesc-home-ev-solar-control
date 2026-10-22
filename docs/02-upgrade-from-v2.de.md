# 02 · Umstieg von HESC v2

*English: [02-upgrade-from-v2.md](02-upgrade-from-v2.md) · Nederlands: [02-upgrade-from-v2.nl.md](02-upgrade-from-v2.nl.md)*

**Kurz gesagt**
- Installiere v3 neben v2. Beide laufen; v3 schaut nur zu (Schattenmodus).
- Eine Taste kopiert deine Einstellungen und deinen Verlauf von v2 nach v3.
- In einem ruhigen Moment setzt du v2 in den Schattenmodus und schaltest v3 live.
- Wenn v3 ein paar Tage gut gelaufen ist, entfernst du den Node-RED-Flow und das Package von v2.
- Doch anders entschieden? Bis du v2 entfernst, kannst du jederzeit zurück.

## Wie v2 und v3 nebeneinander leben

- v3 hat eigene Entitäten (`…hesc_v3_…`) und ein eigenes Dashboard (`/hesc-v3`). Durch die
  Installation von v3 wird an v2 nichts geändert.
- v3 schreibt nie die Einstellungen von v2. Es liest sie nur, und nur, wenn du auf *Übernehmen*
  drückst.
- Wer von beiden den Schattenmodus **aus** hat, ist der, der handelt. Schalte nie beide live.

## Schritt 1 · v3 installieren und zusehen lassen

Folge [01 · Installation](01-installation.de.md). Lass den Schattenmodus von v3 **an**. Lass
beide ein paar Tage laufen und vergleiche die zwei Dashboards: v3 sollte zu denselben
Entscheidungen kommen wie v2. Der Sensor *Unterschiede zu v2 heute* zählt die Momente, in denen
v3 anders entscheiden würde.

## Schritt 2 · Einstellungen und Verlauf übernehmen

1. *Einstellungen → Geräte & Dienste → HESC v3 → Gerät* → drücke **Einstellungen und Verlauf von
   v2 übernehmen**.
2. v3 sichert zuerst seine eigenen Einstellungen (zum Rückgängigmachen: **Einstellungen
   wiederherstellen**). Danach bekommt jede Einstellung von v3 den Wert aus v2, und der
   Ladeverlauf von v2 wird zum Verlauf von v3 (die Datei von v2 wird nur gelesen, nie geändert).
3. Prüfe die Einstellungen auf den Seiten *Einstellungen* und *Ladeplan* von v3.

## Schritt 3 · In einem ruhigen Moment umschalten

Wähle einen Moment, in dem nichts los ist: kein Netzladen durch den Plan und keine laufende
Freigabe für Sonne.

1. **v2:** schalte den Schattenmodus **an** (Dashboard von v2, *Main*).
2. **v2:** leere die Liste der Telefone für Benachrichtigungen in v2 (v2 schickt auch im
   Schattenmodus Benachrichtigungen).
3. **v3:** drücke noch einmal **Einstellungen und Verlauf von v2 übernehmen**, damit auch die
   letzten Stunden dabei sind.
4. **v3:** schalte **Schattenmodus (nur zusehen)** auf der *Übersicht* **aus**. v3 ist jetzt live.
5. **v3:** prüfe, ob dein Telefon in der Liste für Benachrichtigungen von v3 steht (Seite
   *Einstellungen*).

## Schritt 4 · v2 entfernen (nach ein paar guten Tagen)

Erst, wenn v3 einige Tage gut gelaufen ist. Nach diesem Schritt gibt es keinen Weg zurück zu v2,
ohne es neu zu installieren.

1. **Node-RED:** lösche die vier Tabs, deren Name mit **HESC** beginnt (*HESC Inputs*, *HESC Engine*,
   *HESC Outputs*, *HESC Reports*, jeweils mit einer Versionsnummer), und klicke auf Deploy. Lass die Flows anderer Projekte (zum Beispiel HPVC oder Home Battery
   Control) in Ruhe. Verwendet sonst nichts Node-RED, kannst du auch das Add-on entfernen.
2. **Package:** entferne `/config/packages/hesc_config.yaml`, prüfe die Konfiguration und starte
   Home Assistant neu.
3. **Dashboard:** lösche das Dashboard von v2 unter *Einstellungen → Dashboards*.
4. Der Verlauf von v2 in `/config/hesc-data/` bleibt, wo er ist; v3 hat eine eigene Kopie. Lösche
   ihn selbst, wenn du ihn nicht mehr brauchst.

## Zurück zu v2 (vor Schritt 4)

1. **v3:** schalte den Schattenmodus **an**.
2. **v2:** schalte den Schattenmodus **aus** und trage dein Telefon wieder in die Liste für
   Benachrichtigungen von v2 ein.
