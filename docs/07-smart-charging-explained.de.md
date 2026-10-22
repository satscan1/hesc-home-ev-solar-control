# 07 · Intelligentes Laden erklärt

*English: [07-smart-charging-explained.md](07-smart-charging-explained.md) · Nederlands: [07-smart-charging-explained.nl.md](07-smart-charging-explained.nl.md)*

**Kurz gesagt**
- Steck das Auto an, wenn du nach Hause kommst, und sorge dafür, dass dein Plan zu deiner Abfahrt
  passt. Den Rest erledigt HESC.
- HESC nutzt zuerst kostenlose Sonne, dann die günstigsten Viertelstunden aus dem Netz, und behält
  immer ein Sicherheitsnetz, damit das Auto rechtzeitig fertig ist.
- Nach etwa zwei Wochen kennt HESC deine Preise gut genug, um vorauszuschauen.
- Derselbe Text ist ins Dashboard eingebaut: die Anzeige *Anleitung* auf der *Übersicht* (gedrückt
  halten für Niederländisch).

## Die Kurzfassung

Nach etwa zwei Wochen läuft HESC fast von allein. Dein Teil ist klein:

1. **Steck das Auto an**, wenn du nach Hause kommst.
2. **Sorge dafür, dass dein Plan zu deiner Abfahrt passt.** Ein Wochenplan für deine üblichen Tage
   (zum Beispiel *80 % an Werktagen um 07:30*) und der Plan *ein fester Tag pro Woche* für einen
   zusätzlichen Tag (*100 % samstags um 09:00*).

Zwischen dem Anstecken und der Abfahrt sucht HESC den günstigsten Weg, das Auto dorthin zu
bringen, wo du es haben willst.

## Warum die ersten zwei Wochen zählen

Das meiste funktioniert vom ersten Tag an: Laden mit Sonne, der Ladeplan, das Sicherheitsnetz und
die Zielprüfung.

Eines wird mit der Zeit besser: **der Blick auf die Preise von morgen.** Die Preise für morgen
werden gegen 13:00 veröffentlicht. Vorher kennt sie niemand. HESC füllt diese Lücke mit einem
erwarteten Preis, auf Basis der Preise deiner eigenen letzten 14 Tage und davon, wie sonnig es
morgen wird (an sonnigen Tagen ist es mittags meist günstig und abends teuer).

- **Der erste Tag:** noch keine erwarteten Preise. HESC plant mit den bekannten Preisen. Das
  Sicherheitsnetz macht das Auto trotzdem fertig.
- **Nach einem vollen Tag:** eine grobe Erwartung, einfach das Muster von gestern. Erwartete Preise
  erscheinen als graue Balken in der Preisgrafik, und der Plan kann sie nutzen.
- **Ab Tag 3:** der Durchschnitt aller vollen Tage bis dahin.
- **Ab Tag 14:** zwei volle Wochen deiner eigenen Preise.
- **Danach jede Woche:** HESC verfeinert, wie Sonne und Preis auf deinem Markt zusammenhängen.

Ein bekannter Preis gewinnt immer gegen einen erwarteten, es sei denn, der erwartete ist deutlich
günstiger (2 Cent pro kWh oder mehr). Sobald die echten Preise da sind, nutzt der Plan diese.

## Die Reihenfolge, der HESC folgt

Alle 30 Sekunden schaut HESC auf das Auto, die Sonne, die Preise und deinen Plan und stellt sich
dieselben Fragen in derselben Reihenfolge:

| # | Frage | Was passiert |
|---|---|---|
| 1 | **Scheint die Sonne?** | Deine Wallbox lädt mit Sonne in ihrer eigenen Einstellung dafür (zum Beispiel Eco), wie sie es immer getan hat. Mit HPVC bittet HESC zuerst HPVC, die Sonne durchzulassen. HESC rechnet die Sonne in den Plan ein, damit es keine Energie kauft, die die Sonne ohnehin liefert. |
| 2 | **Ist es eine der geplanten günstigsten Viertelstunden?** | HESC startet die Wallbox für diese Viertelstunde aus dem Netz. |
| 3 | **Wird die Zeit knapp?** | **Sicherheitsnetz:** Reicht die verbleibende Zeit gerade noch für das Ziel, startet HESC das Laden, egal zu welchem Preis. |
| 4 | **Ist es die letzte Stunde vor der Abfahrt und fehlt dem Auto noch etwas?** | **Letzte Prüfung:** HESC lädt bis zu deinem Ziel, egal zu welchem Preis. |
| 5 | **Ist der Preis gerade sehr niedrig?** | **Günstige Gelegenheit:** HESC lädt jetzt, auch ohne Plan, *außer* es wird später am Tag genug Sonne erwartet. |
| 6 | **Liegt das Auto unter dem Minimum, das du eingestellt hast?** | **Mindestladung** (optional, standardmäßig aus): Das Auto bekommt innerhalb weniger Stunden mindestens diesen Ladestand, in den günstigsten Viertelstunden. |
| 7 | Nichts davon | HESC wartet. Das Dashboard sagt dir, warum, zum Beispiel *Waiting for the next planned quarter*. |

Für all das gelten ein paar Regeln:

- **3 % Spielraum.** HESC lädt nur dann aus dem Netz, wenn das Auto mehr als 3 % unter dem Ziel
  liegt. Ein Auto bei 78 % mit Ziel 80 % bleibt in Ruhe; bei 76,9 % lädt es.
- **Welches Ziel?** Mit einem aktiven Plan: das Ziel dieses Plans. Ohne Plan: *Auto gilt als voll
  bei* (Standard 80 %). Eine günstige Gelegenheit füllt nie ein Auto, das schon als voll gilt.
- **HESC macht nur rückgängig, was es selbst begonnen hat.** Startest du das Laden selbst, oder lädt
  das Auto schon mit Sonne, lässt HESC es in Ruhe.
- **Nach dem Netzladen bleibt die Wallbox nicht an.** Sonst könnte das Auto sich abends in der
  Spitzenzeit still aus dem Netz nachladen. Ist *Zurück in den Solarmodus* ausgefüllt (Wallbox:
  *Resume schedule*, wird für dich ausgefüllt), pausiert HESC die Wallbox, prüft, ob die Pause
  wirklich angekommen ist (Wallboxen über die Cloud reagieren etwa eine Minute später), und setzt
  sie dann zurück auf Laden mit Sonne. Ohne dieses Feld bleibt die Wallbox pausiert, bis genug Sonne
  da ist, das Auto mehr als 3 % unter das Ziel fällt, ein Plan startet oder du absteckst.

## Wie der Plan die günstigsten Stunden wählt

Angenommen, du steckst um 18:00 an, das Auto steht bei 40 %, und dein Wochenplan sagt
*80 % um 07:30*.

1. **Wie viel wird gebraucht?** 40 % eines 60-kWh-Akkus = 24 kWh.
2. **Wie viel kommt vor 07:30 von der Sonne?** Nichts, es ist Nacht. (Bei einem Samstagsplan für
   14:00 würde die Morgensonne mitzählen.)
3. **Wie lange dauert das aus dem Netz?** Bei 11 kW: etwas über 2 Stunden, also 9 Viertelstunden.
4. **Welche 9 Viertelstunden?** Die günstigsten zwischen jetzt und 07:30. Meist irgendwo in der
   Nacht.

Die geplanten Viertelstunden erscheinen **bernsteinfarben** in der Preisgrafik auf der Seite
*Ladeplan*. Ist der Plan nicht aktiv, zeigt die Grafik, was er tun *würde*, markiert als *Vorschau*.

## Günstige Gelegenheiten und die Sonne

*Günstige Gelegenheiten nutzen* lädt immer dann, wenn der Preis unter *Günstig unter* fällt, auch
ohne Plan. Diese Momente erscheinen **blaugrün** in der Preisgrafik.

Ein günstiger Moment am Morgen ist aber kein Schnäppchen, wenn die Nachmittagssonne das Auto
kostenlos gefüllt hätte. Deshalb schaut HESC zuerst auf die Solarprognose für den Rest des Tages.
Deckt die erwartete Sonne das, was das Auto noch braucht, mit 20 % Reserve, wird die günstige
Gelegenheit ausgelassen: *Cheap chance skipped: enough sun today*.

## Wie viel Sonne deine Wallbox braucht

Eine Wallbox, die mit Sonne lädt, startet erst, wenn genug Sonne übrig ist. Wie viel, ist je nach
Marke verschieden: von etwa 0,5 kW auf einer Phase (Wallbox Eco) bis etwa 4 kW auf drei Phasen (das
übliche Minimum von 6 A pro Phase). HESC kennt das pro Marke, und die Empfehlung zur Startschwelle
geht nie unter das, was deine Wallbox braucht. Die Tabelle steht in
[05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#wie-viel-sonne-eine-wallbox-zum-starten-braucht).

**Netzladen und Sonne gleichzeitig.** Lässt deine Wallbox HESC den Ladestrom einstellen (Wallbox:
*Maximum charging current*, dafür ist ein Administratorkonto nötig), regelt HESC die Wallbox
herunter, während sie aus dem Netz lädt und die Sonne scheint. Dann kommt mehr von der Ladung von
deinen Paneelen und weniger aus dem Netz. Das ist normal; du musst nichts einschalten. HESC tut es
nur, solange das Auto trotzdem rechtzeitig voll ist, und stellt den Strom danach wieder zurück. Ob
deine Wallbox 1 oder 3 Phasen nutzt, ermittelt HESC selbst.

**Phasenhinweis.** Manche Wallboxen starten erst, wenn jede Phase genug Sonne übrig hat (eine
Wallbox im Eco-Modus etwa 480 W pro Phase, ein Easee 6 A pro Phase). Sind deine Paneele ungleich
auf die Phasen verteilt, entscheidet dann die schwächste Phase, wann dein Auto mit Sonne laden
kann. Ist die Netzleistung pro Phase ausgefüllt, misst HESC das an sonnigen Tagen und sagt dir, was
es gesehen hat: zuerst die Verteilung über die Phasen, später, wie oft die schwächste Phase deine
Wallbox gebremst hat. Es ist nur ein Hinweis; HESC ändert nichts.

## Ohne Solarprognose

HESC funktioniert auch ohne Prognose. Es lädt dann mit der Solarleistung, die es misst, und der
Plan rechnet mit gar keiner Sonne, damit das Auto nie zu spät fertig ist. Der Kickstart ist aus,
weil er wissen muss, wie viel Sonne noch kommt. Siehe
[05 · Wallboxen und Quellen](05-chargers-and-sources.de.md#solarprognose).

## Hausspeicher und Auto

*Optional, standardmäßig aus. Nur für Häuser mit einem Hausspeicher.*

An einem sonnigen Morgen nimmt meist der Hausspeicher zuerst die ganze überschüssige Sonne. Die
Wallbox sieht dann keinen Überschuss und wartet, manchmal bis der Hausspeicher am Nachmittag voll
ist. An einem Tag mit weniger Sonne bekommt das Auto vielleicht nichts.

Mit **Hausspeicher und Auto** eingeschaltet hilft HESC dem Auto, an die Reihe zu kommen:

1. **Kickstart.** Das Auto ist angesteckt und wartet auf Sonne, der Hausspeicher lädt seit ein
   paar Minuten, und die vorsichtige Prognose sagt, dass jetzt genug Sonne da ist. HESC prüft den
   Rest des Tages: Ist deutlich mehr Sonne übrig, als der Hausspeicher noch braucht (mit 20 %
   Reserve und mindestens *Minimale Restsonne für das Auto*)? Dann:
   1. HESC startet die Wallbox;
   2. deine Hausspeicher-Steuerung sieht, dass das Auto lädt, und hört auf, den Hausspeicher zu
      füllen;
   3. HESC pausiert die Wallbox und wartet, bis die Pause wirklich angekommen ist;
   4. HESC setzt die Wallbox zurück auf Laden mit Sonne, die jetzt die frei gewordene Sonne
      bekommt.
2. **Zurück zum Hausspeicher.** Später am Tag, wenn die restliche Sonne gerade noch reicht, um den
   Hausspeicher zu füllen, lässt HESC die Wallbox wieder warten, damit der Hausspeicher bis zum
   Abend voll ist. Danach gibt es an diesem Tag keinen neuen Kickstart.

Während des kurzen Starts kann der Hausspeicher etwas Leistung an das Auto abgeben. Das ist
erwartet.

HESC steuert den Hausspeicher nie selbst. Es tut nichts, während ein Ladeplan lädt, während einer
HPVC-Freigabe oder nach Sonnenuntergang, und höchstens ein paar Mal am Tag (*Kickstarts pro Tag*,
Standard 3, mit mindestens 30 Minuten dazwischen).

Was du ausfüllst (*Einstellungen*, *Hausspeicher und Auto* → *Optionen*): den oder die
Ladestandsensoren deines Hausspeichers, den oder die Leistungssensoren (positiv = laden) und seine
Gesamtgröße in kWh. Außerdem braucht es den Start/Stopp-Schalter der Wallbox und *Zurück in den
Solarmodus*; bei einer Wallbox der Marke Wallbox ist beides schon für dich ausgefüllt.

## Was wird es kosten?

Die Anzeige **Erwartete Ladekosten** auf der *Übersicht* zeigt, was der aktive Plan aus dem Netz
voraussichtlich kostet: der Preis jeder geplanten Viertelstunde, plus dein Aufschlag und die MwSt.
(oder der Endpreis). Sie zählt nur Netzladen, das wirklich stattfindet; ohne aktiven Plan, wenn
das Auto sein Ziel erreicht hat, oder während das Auto mit Sonne lädt, zeigt sie 0,00.

**Was hat es gekostet?** Tippe auf die Anzeige **Kosten**. Pro Tag, Woche, Monat, Quartal oder Jahr
siehst du, wie viel ins Auto ging, wie viel davon von der Sonne (grün) und aus dem Netz (grau) kam,
und was der Netzanteil gekostet hat. Aufschlag, MwSt. und den Wert einer Solar-kWh stellst du einmal
unter *Einstellungen → Ladekosten* ein; der ganze Verlauf wird angepasst. **In Tabelle exportieren
(CSV)** schreibt zwei Dateien für Excel.

## Situationen

### "Ich fahre jeden Werktag zur Arbeit"

Erstelle einen **Wochenplan**: hake die Tage an, stelle die Abfahrtszeit und den gewünschten
Ladestand ein. Lass ihn aktiv. Steck an, wenn du nach Hause kommst. Das ist alles.

### "Am Samstag mache ich einen Ausflug"

Nutze **ein fester Tag pro Woche**: wähle *Samstag*, die Abfahrtszeit und zum Beispiel 100 %, und
schalte ihn ein. Sind beide Pläne aktiv, gewinnt der frühere; dein Wochenplan läuft einfach weiter.
Brauchst du ihn nur einmal? Schalte *Aktiv* nach dem Ausflug aus.

### "Das Auto bleibt ein paar Tage zu Hause"

Kein Plan nötig. Das Auto lädt mit Sonne, nutzt günstige Gelegenheiten, und sonst bleibt die
Wallbox pausiert. Erst wenn das Auto mehr als 3 % unter *Auto gilt als voll bei* fällt, lädt HESC
nach.

### "Ich bin mit fast leerem Akku heimgekommen und brauche das Auto vielleicht heute Abend"

Schalte **Mindestladung** ein (*Einstellungen*, *An*). Standard: mindestens 20 % innerhalb von 3
Stunden, in den günstigsten Viertelstunden dieser 3 Stunden, oder sofort, wenn keine Preise bekannt
sind.

### "Ich habe einen Hausspeicher und das Auto bekommt nie Sonne"

Schalte **Hausspeicher und Auto** ein und trage deinen Hausspeicher ein. Siehe
[Hausspeicher und Auto](#hausspeicher-und-auto) oben.

### "Ich brauche das Auto jetzt, vergiss den Plan"

Starte das Laden selbst (App, Taste an der Wallbox oder die eigene Einstellung der Wallbox). HESC
sieht, dass das Auto schon lädt, und lässt es in Ruhe.

### "Ich habe spät angesteckt; reicht die Zeit noch?"

HESC prüft das ständig. Reicht die verbleibende Zeit gerade noch, startet das Sicherheitsnetz
sofort. Wird das Ziel trotzdem verfehlt? Dann bekommst du zu deiner Abfahrtszeit eine
Benachrichtigung: *EV goal missed*, mit dem erreichten Ladestand.

### "Morgen wird es sonnig"

Der Plan rechnet die Sonne vorab ein (vorsichtige Prognose, minus etwas für das Haus) und kauft
deshalb weniger aus dem Netz. Günstige Gelegenheiten, die die Sonne überflüssig macht, werden
ausgelassen.

### "Die Preise von morgen sind noch nicht bekannt"

Normal vor etwa 13:00. Nach den ersten Tagen nutzt der Plan erwartete Preise (graue Balken) und
wird genauer, sobald die echten Preise da sind.

### "Mein Auto hört bei 80 % von selbst auf"

Viele Autos haben ein eigenes Ladelimit. Liegt es unter deinem Ziel, stoppt die Wallbox von selbst,
und HESC zeigt *Finished, charger stopped by itself*. Setze dein Ziel auf oder unter das Limit des
Autos, oder erhöhe das Limit im Auto.

### "Die Wallbox hat nicht reagiert"

Wallboxen über die Cloud ignorieren manchmal einen Befehl. HESC prüft und versucht es erneut: einen
abgelehnten Start oder ein abgelehntes Fortsetzen nach 5 Minuten, eine abgelehnte Pause nach 30
Minuten, jeweils höchstens 3 Mal.

### "Home Assistant wurde während des Ladens neu gestartet"

HESC nutzt den letzten gültigen Plan bis zu 10 Minuten weiter, damit ein laufendes Laden nicht
stoppt. Direkt nach einem Neustart sind manche Karten etwa eine Minute leer, und der Ladestand des
Autos kann ein paar Minuten falsch sein. Siehe
[09 · Fehlerbehebung](09-troubleshooting.de.md#nach-einem-neustart-von-home-assistant).

### "Ich bin im Urlaub"

Schalte **Urlaubsmodus** unter dem Wochenplan ein. Der Wochenplan ruht; dein Plan für einen Tag
bleibt aktiv, sodass das Auto am Tag deiner Rückkehr voll sein kann. Laden mit Sonne läuft weiter.
Stelle bei Bedarf **Urlaub bis** ein: am Tag nach diesem Datum schaltet sich der Urlaubsmodus von
selbst aus.

## Was du einmal einstellst

| Einstellung | Wo | Standard | Tipp |
|---|---|---|---|
| *Nutzbare Akkukapazität* | *Ladeplan* | 60 kWh | Was dein Auto wirklich nutzen kann |
| *Ladeleistung aus dem Netz* | *Ladeplan* | 11 kW | Etwas unter dem, was deine Wallbox wirklich liefert, gibt etwas Reserve |
| *Günstige Gelegenheiten nutzen* / *Günstig unter* | *Ladeplan* | deine Wahl / 0,05 pro kWh | In der Währung deiner Preise |
| *Auto gilt als voll bei* | *Einstellungen*, weitere Felder | 80 % | Der Ladestand, der ohne Plan gehalten wird |
| Letzte Prüfung | *Einstellungen*, *Ladeplan und Meldungen* | 60 min | Wie lange vor der Abfahrt HESC lädt, egal zu welchem Preis |
| *Mindestladung* | *Einstellungen* | aus (20 %, 3 h) | *An* + *Optionen* |
| *Hausspeicher und Auto* | *Einstellungen* | aus (3 pro Tag) | Nur mit Hausspeicher |
| *Zurück in den Solarmodus* | *Einstellungen*, *Ladeplan und Meldungen* | für Wallbox ausgefüllt | Setzt die Wallbox nach dem Netzladen zurück auf Laden mit Sonne |
| Telefone für Benachrichtigungen | *Einstellungen*, *Ladeplan und Meldungen* | keine | Mit *Testbenachrichtigung senden* testen |
| Morgenübersicht | *Einstellungen*, *Ladeplan und Meldungen* | aus (06:00) | Eine Nachricht am Tag: Ladestand, nächster Plan, Sonne heute, gestern |
| Ladekosten | *Einstellungen*, *Ladekosten* | Aufschlag 0, MwSt. 0, Solar-kWh gratis | Oder *Endpreis*, wenn dein Preissensor schon den vollen Preis hat |

## Wo du nachschaust

- **Status** auf der *Übersicht*: was HESC gerade tut und warum.
- **Preisgrafik** (*Ladeplan*): bernsteinfarben = geplant, blaugrün = günstige Gelegenheit, grau =
  erwarteter Preis.
- **Hinweiszeile** neben dem Logo: *✓ Keine Hinweise* oder was Aufmerksamkeit braucht. Tippe darauf,
  um dorthin zu gehen, wo du handeln kannst.
- Die Anzeigen **Erwartete Ladekosten** und **Kosten** auf der *Übersicht*.
- **Prüfung der Einrichtung** auf *Einstellungen*: Stimmt etwas nicht, öffnet sich dieser Teil von
  selbst.
- **Bericht** (*Bericht erstellen* unter Status): alles, was HESC gemessen und entschieden hat.

Siehe auch: [04 · So funktioniert es](04-how-it-works.de.md) · [06 · Dashboard](06-dashboard.de.md) ·
[08 · Ein Tag mit HESC](08-a-day-with-hesc.de.md)
