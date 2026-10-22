# 09 · Fehlerbehebung

*English: [09-troubleshooting.md](09-troubleshooting.md) · Nederlands: [09-troubleshooting.nl.md](09-troubleshooting.nl.md)*

**Kurz gesagt**
- Die meisten Meldungen auf dem Dashboard sind normal: HESC sagt dir, worauf es wartet.
- Direkt nach einem Neustart von Home Assistant sind manche Karten etwa eine Minute leer. Das
  erledigt sich von selbst.
- Stimmt wirklich etwas nicht? Schau dir die Prüfung der Einrichtung auf der Seite *Einstellungen*
  und die Karte *Live* auf der *Übersicht* an, und drücke **Bericht erstellen**.

## Nach einem Neustart von Home Assistant

| Was du siehst | Was es bedeutet |
|---|---|
| Die Karte *Status* oder andere Karten sind leer oder zeigen kurz einen Fehler | Normal. HESC füllt das Dashboard etwa eine Minute nach dem Start. |
| Der Ladestand des Autos ist ein paar Minuten falsch (zum Beispiel 99,9 %) | Manche Auto-Integrationen schicken bis zu ihrem nächsten Update einen falschen Wert. HESC rechnet neu, sobald der richtige Wert kommt. Siehe [05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#der-ladestand-deines-autos). |
| Ein Feld in der Einrichtung ist leer | Die Integration deiner Wallbox oder deines Zählers war noch nicht bereit. HESC sucht erneut, sobald Home Assistant gestartet ist. Immer noch leer? Fülle es unter *Einstellungen → Geräte & Dienste → HESC v3 → Konfigurieren* aus. |
| Die Prüfung der Einrichtung auf *Einstellungen* zeigt ein rotes ❌ | Warte ein paar Minuten. Nach 15 Minuten immer noch rot? Dann fehlt wirklich etwas; die Prüfung sagt dir, was. |

## Installation und Dashboard

| Problem | Prüfe |
|---|---|
| Tasten zwischen den Seiten des Dashboards tun nichts | Die Adresse des Dashboards muss genau `hesc-v3` sein. Siehe [01 · Installation](01-installation.de.md#3-das-dashboard-hinzufügen). |
| Grafiken, der Balken *Erwartetes Solarladen* oder die Kacheln auf der Seite Kosten fehlen, oder eine Karte sagt *Custom element doesn't exist: hesc-…* | Die eigenen Karten von HESC laden mit der Integration: Starte Home Assistant nach der Installation oder einem Update von HESC neu und lade dann den Browser neu (auf einem Telefon: App schließen und wieder öffnen). Karten aus HACS sind nicht nötig. |
| Die Symbole von HESC fehlen | Lade den Browser neu (auf einem Telefon: App schließen und wieder öffnen). |
| HESC findet meine Wallbox nicht | Wähle den Wallbox-Typ auf *Einstellungen* erneut und drücke **Erneut suchen**. Nicht in der Liste? Wähle *Other (manual)* und fülle die Felder selbst aus. |

## Laden mit Sonne

| Meldung | Was sie bedeutet |
|---|---|
| `Waiting for inputs: …` | Die genannte Quelle ist leer oder nicht verfügbar. Prüfe sie auf der Karte *Live* und in der Einrichtung. |
| `HPVC is not limiting PV — nothing to release` | Normal: HPVC begrenzt deine Solarpaneele nicht, also kann die Wallbox die Sonne schon nutzen. |
| `Waiting for HPVC to confirm the release (x/5 min, …)` | Kurz normal: HPVC erledigt zuerst etwas mit höherer Priorität. |
| `HPVC has no external release interface (needs HPVC 1.5.1 or newer)` | Aktualisiere HPVC. |
| `EV already full, no release needed` | Das Auto steht bei *Auto gilt als voll bei*. |
| `Charger not in solar mode` | Die Wallbox ist nicht in ihrer Einstellung für Laden mit Sonne (zum Beispiel Eco), oder der zusätzliche Solarschalter ist aus. |
| `Forecast too low` | Die vorsichtige Prognose liegt unter der Startschwelle. |
| `Cooldown until …` | Eine Freigabe ist gerade zu Ende gegangen; HESC wartet, bevor es es erneut versucht. |
| `Maximum release attempts reached today` | Heute sind zu viele Freigaben fehlgeschlagen. Beginnt um Mitternacht neu. |
| Der Phasenhinweis bleibt auf *wird gemessen* | In den ersten Wochen normal: Er braucht genug sonnige Tage. Er braucht die Netzleistung pro Phase in der Einrichtung. |

**Die Wallbox startet nicht, obwohl HESC fragt, oder startet, wenn sie nicht soll.** Prüfe, ob in
der eigenen App der Wallbox oder in einer anderen Integration ein Ladeplan eingestellt ist, und
schalte ihn aus. Nach einem Update der App oder der Firmware der Wallbox kann ein Ladeplan von
selbst auftauchen.

## Ladeplan

| Meldung | Was sie bedeutet |
|---|---|
| `Grid charging not set up …` | Fülle den Start/Stopp-Schalter oder den Lademoduswert für "jetzt laden" unter *Einstellungen → Erweitert → Ladeplan und Meldungen* aus. |
| `No active plan` | Schalte den Plan *ein fester Tag pro Woche* oder die Wochenplanung ein. Ohne Plan lädt HESC nur mit Sonne und bei günstigen Gelegenheiten. |
| `Waiting for the next planned quarter` | Normal. Die geplanten Viertelstunden stehen in der Preisgrafik. |
| `Final check: below goal, charging to goal` | Normal in der letzten Stunde vor der Fertig-Zeit, wenn das Auto noch unter seinem Ziel liegt. HESC lädt bis zum Ziel, egal zu welchem Preis. |
| `EV already charging, left alone` | Das Auto lud schon (zum Beispiel mit Sonne). HESC übernimmt es nicht. |
| `Finished, charger stopped by itself` | Die Wallbox hat ein paar Minuten keinen Strom gezogen (Auto voll oder eigenes Limit). |
| `Cheap chance skipped: enough sun today (…)` | Normal: Die Sonne deckt den Bedarf voraussichtlich später am Tag. |
| *Preise nicht verfügbar* | Der Preissensor liefert gerade keine Preise. Prüfe *Preisquelle* und *Preissensor* unter *Einstellungen → Erweitert → Ladeplan und Meldungen* und die Preisintegration selbst. |
| Falsche Währung oder kleine Einheit | *Währung* → *Automatic* nimmt sie aus dem Preissensor; wähle deine Währung, wenn der Sensor sie nicht angibt. |
| Preise nur bis heute Abend bekannt | Normal, bevor die Preise des nächsten Tages veröffentlicht werden (gegen 13:00). Der Plan nutzt dann erwartete Preise und wird später genauer. |
| Der Wochenplan tut nichts | Prüfe **Urlaubsmodus** unter dem Wochenplan. |
| Benachrichtigung *Charger fault* | HESC hat 3 Mal versucht, die Wallbox wieder einzuschalten. Prüfe die Wallbox und ihre Cloud-Verbindung. |

## Hausspeicher und Auto (Kickstart)

Wird auf der *Übersicht* unter *Aktueller Stand* angezeigt, solange das Auto angesteckt ist.

| Meldung | Was sie bedeutet |
|---|---|
| `Not set up: …` | Fülle den Start/Stopp-Schalter, *Zurück in den Solarmodus* und die Felder für den Hausspeicher unter *Einstellungen → Hausspeicher und Auto* aus. |
| `Waiting: home batteries not taking the sun` | Normal: Der Hausspeicher lädt nicht, also sieht die Wallbox den Überschuss schon. |
| `Home batteries first for the rest of today` | Nicht genug Sonne für beide übrig; der Hausspeicher bekommt sie. |
| `Kickstart: charger started …` → `Kickstart: charger paused …` → `Kickstart: waiting for the charger …` | Ein Kickstart läuft: Die Wallbox startet, die Hausspeicher-Steuerung sieht das Auto und hört auf, die Speicher zu laden, die Wallbox wartet wieder auf Sonne. |
| `Charge plan has the charger` | Normal: Der Kickstart wartet auf den Ladeplan. |
| `Done for today (…)` | Die höchste Zahl an Kickstarts ist erreicht, oder der Hausspeicher hat Vorrang bekommen. Beginnt morgen neu. |

## Hinweise und Benachrichtigungen

Die Zeile neben dem Logo auf der *Übersicht* zeigt *✓ Keine Hinweise* oder den wichtigsten
Hinweis. Tippe darauf, um dorthin zu gehen, wo du handeln kannst.

| Hinweis | Bedeutung |
|---|---|
| **P1** (rot, auch auf deinem Telefon) | Das Ladeziel wurde verfehlt oder lässt sich nicht bestätigen, oder ein echter Fehler. Bleibt 12 Stunden. |
| **P2** (orange) | Ein Sensor fehlt, aber HESC arbeitet weiter (zum Beispiel ist der Ladestand geschätzt). |
| **P3** (grau) | Nur zur Info. Zwei Stunden. |

**Keine Benachrichtigungen auf dem Telefon?** Füge auf *Einstellungen* unter *Benachrichtigungen
aufs Telefon* dein Telefon hinzu und sende eine Testbenachrichtigung. Nur P1 und P2 gehen ans
Telefon.

## Kosten

| Problem | Prüfe |
|---|---|
| Keine Taste *Kosten* auf der *Übersicht* | Schalte die Seite Kosten auf *Einstellungen* ein. |
| Kosten zu hoch oder zu niedrig | Prüfe *Endpreis* oder Aufschlag und MwSt. auf *Einstellungen*. Änderst du sie, wird der ganze Verlauf neu berechnet. |
| Eine Warnung über Netzenergie ohne Preis | Es wurde aus dem Netz geladen, während kein Preis bekannt war. Das wird getrennt gezählt. |
