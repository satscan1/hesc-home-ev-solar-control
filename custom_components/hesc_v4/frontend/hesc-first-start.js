/* HESC v4 · First start in HESC's own panel (decision 01-11-2026 12:44 "B").
 *
 * custom:hesc-v4-first-start — shown at the top of the HESC v4 dashboard while the first start is not done
 * (sensor.hesc_v4_setup, attribute setup_done). Part 1 asks what a user knows without looking anything up,
 * part 2 only shows what HESC could not find, then "Klaar" saves everything in one go.
 * Talks to the integration over the websocket: hesc_v4/setup/find, hesc_v4/setup/charger, hesc_v4/setup/save
 * (setup_wizard.py; answers format in docs/dev/v4-first-start.md). Texts NL/EN/DE, house style as the proefbord.
 * Decisions in the texts: 01-11 10:17-10:42, 11:50, 12:49 (order), 12:55 (amps per phase), 12:58 (Klaar).
 */

const FS_TXT = {
  nl: {
    step: (i, n) => `Eerste start · stap ${i} van ${n}`, next: "Volgende ›", back: "‹ Terug", done: "Klaar", saving: "Opslaan…",
    shadow: "HESC v4 start in schaduwmodus: het kijkt mee en schakelt niets.",
    how: "Hoe laad je thuis?", one: "Eén auto", twoShared: "Twee auto's, één laadpaal", twoSharedSub: "om de beurt, jij zet de kabel om", twoOwn: "Twee auto's, elk een eigen laadpaal",
    house: "Je huis", phases: "hoofdaansluiting: aantal fasen", ph1: "1 fase", ph3: "3 fasen", dk: "Weet ik niet", amps: "ampère per fase", own: "zelf",
    lb: "heb je een load balancer die het huisverbruik meeneemt?", lbSub: "Bijvoorbeeld Wallbox Power Boost, of een laadpaal die via de slimme meter meekijkt.",
    yes: "Ja", no: "Nee", solar: "heb je zonnepanelen?", dynamic: "heb je dynamische energieprijzen?",
    resp: "HESC houdt hiermee het laden binnen de aansluiting als comfort. Jij blijft verantwoordelijk dat je elektrische installatie niet overbelast raakt; dat regelen laadpaal, load balancer en installateur.",
    charger: (n) => n === 2 ? "Je laadpalen" : "Je laadpaal", chargerSub: "Het merk, en wat de installateur als maximum heeft ingesteld.", chargerN: (j) => `laadpaal ${j}`,
    other: "Anders", maxA: "maximum dat de installateur heeft ingesteld", maxASub: "Weet je het niet, laat dan 16 A staan. Bij Easee, Peblar en Wallbox leest HESC dit straks zelf uit de laadpaal.",
    car: (n) => n === 2 ? "Je auto's" : "Je auto", carSub: "De naam komt uit Home Assistant; pas hem aan als je wilt.", carN: (j) => `Auto ${j}`,
    name: "naam", capacity: "accucapaciteit", capSub: "Staat in de specificaties van je auto.", atCharger: "aan laadpaal",
    sharing: "Om de beurt", sharingSub: "Beide auto's laden aan dezelfde laadpaal. De auto die 's avonds aan de paal hangt laadt eerst; de andere nadat jij de kabel hebt omgezet.",
    swap: "kabel omzetten uiterlijk om", remind: "Herinnering op je telefoon als het tijd is om de kabel om te zetten",
    missingCharger: (b) => `Laadpaal: ${b}`, missingSub: "Dit kon HESC niet vinden. Kies het zelf:",
    soc: (c) => `Accustand van ${c}`, socSub: "Welke sensor geeft het accu-% van deze auto?", socNone: "Geen: HESC schat het zelf. Je kunt de accustand ook zelf invullen op de startpagina of je telefoon.",
    sources: "Zon en net", pv: "Zonnestroom nu", pvHpvc: "Je hebt ook HPVC. HESC vond daarom twee meters voor je zonnepanelen: die van HPVC en een eigen meter. De meter van HPVC telt soms maar een deel van je panelen. HESC heeft de meter gekozen die al je panelen samen telt. Klopt dat? Dan hoef je niets te doen.", grid: "Netvermogen nu", fcNow: "Zonverwachting nu", fc30: "Zonverwachting over 30 minuten",
    hpvc: "HPVC gevonden", hpvcSub: "HPVC regelt je zonnepanelen bij negatieve prijzen. Zal HESC daarmee samenwerken?", hpvcNo: "Nee, HESC werkt op zichzelf",
    price: "Waar komen je prijzen vandaan?", priceSub: "Een ✓ betekent dat HESC die bron in Home Assistant vond.", gridClock: "Grid Clock (heel Europa, 41 zones)",
    gcNote: "Grid Clock geeft de kale beursprijs. Vul opslag en btw in bij Kosten.", gcEuro: "Grid Clock levert altijd in euro.", now: "nu",
    ready: "Klaar! HESC v4 gaat aan de slag.", readySub: "HESC start in schaduwmodus: het kijkt mee en schakelt niets. Zet hem aan op de startpagina als je zover bent. Alles kun je later wijzigen bij Instellingen.",
    recommended: "aanbevolen", others: "Andere sensoren", gridHelp: "Het vermogen van je hele huis aan de elektriciteitsmeter (P1). Positief = afname, negatief = teruglevering.",
    confirm: "Ik begrijp dat ik zelf verantwoordelijk blijf voor mijn elektrische installatie.", found: "✓ = gevonden in je Home Assistant", device: "Welke laadpaal is het? Je hebt er meer van dit merk.",
    otherNote: "Je kiest straks zelf 4 sensoren of schakelaars van je laadpaal.", colour: "kleur", chargerShort: "Laadpaal",
    sumLoad: "Laden", sumHouse: "Huis", sumSun: "Zon", sumPrice: "Prijzen", unknownConn: "aansluiting onbekend", lbShort: "load balancer", fixed: "vast", none: "geen",
    choose: "— kies —", errors: { required: "verplicht", amps_invalid: "ampère tussen 6 en 250", capacity_invalid: "accucapaciteit tussen 10 en 150 kWh", installer_setting: "maximum tussen 6 en 32 A", unknown_charger: "onbekende laadpaal", two_cars_already: "er zijn al twee auto's" },
    failed: "Opslaan lukte niet:", ws: "HESC v4 antwoordt niet. Herstart Home Assistant als je HESC v4 net hebt geïnstalleerd.",
    fields: { ev_connected_sensor: "Auto aangesloten", ev_disconnected_values: "Waarden voor 'geen auto'", ev_power_sensor: "Laadvermogen", charger_mode_entity: "Stand van de laadpaal", charger_eco_values: "Waarde(n) voor zonneladen", charger_solar_switch_entity: "Schakelaar zonneladen", charger_start_stop_entity: "Start/stop", charger_resume_entity: "Hervatten", charger_current_entity: "Laadstroom", ev_green_energy_sensor: "Groene energie" },
  },
  en: {
    step: (i, n) => `First start · step ${i} of ${n}`, next: "Next ›", back: "‹ Back", done: "Done", saving: "Saving…",
    shadow: "HESC v4 starts in shadow mode: it watches and switches nothing.",
    how: "How do you charge at home?", one: "One car", twoShared: "Two cars, one charger", twoSharedSub: "taking turns, you move the cable", twoOwn: "Two cars, each its own charger",
    house: "Your house", phases: "main connection: number of phases", ph1: "1 phase", ph3: "3 phases", dk: "Don't know", amps: "amps per phase", own: "other",
    lb: "do you have a load balancer that takes the house into account?", lbSub: "For example Wallbox Power Boost, or a charger that reads the smart meter.",
    yes: "Yes", no: "No", solar: "do you have solar panels?", dynamic: "do you have dynamic energy prices?",
    resp: "HESC uses this to keep charging within the connection, as a comfort. You stay responsible for not overloading your electrical installation; charger, load balancer and installer take care of that.",
    charger: (n) => n === 2 ? "Your chargers" : "Your charger", chargerSub: "The brand, and the maximum the installer set.", chargerN: (j) => `charger ${j}`,
    other: "Other", maxA: "maximum set by the installer", maxASub: "Don't know? Leave it at 16 A. For Easee, Peblar and Wallbox HESC reads it from the charger.",
    car: (n) => n === 2 ? "Your cars" : "Your car", carSub: "The name comes from Home Assistant; change it if you like.", carN: (j) => `Car ${j}`,
    name: "name", capacity: "battery capacity", capSub: "In your car's specifications.", atCharger: "on charger",
    sharing: "Taking turns", sharingSub: "Both cars charge on the same charger. The car on the charger in the evening goes first; the other after you move the cable.",
    swap: "move the cable at the latest at", remind: "Reminder on your phone when it is time to move the cable",
    missingCharger: (b) => `Charger: ${b}`, missingSub: "HESC could not find this. Pick it yourself:",
    soc: (c) => `Battery level of ${c}`, socSub: "Which sensor gives this car's battery %?", socNone: "None: HESC estimates it. You can also enter the battery level on the start page or your phone.",
    sources: "Sun and grid", pv: "Solar power now", pvHpvc: "You also have HPVC, so HESC found two meters for your solar panels: the HPVC one and another one. The HPVC meter sometimes counts only part of your panels. HESC picked the meter that counts all your panels together. Is that right? Then you don't need to do anything.", grid: "Grid power now", fcNow: "Solar forecast now", fc30: "Solar forecast in 30 minutes",
    hpvc: "HPVC found", hpvcSub: "HPVC controls your solar panels at negative prices. Should HESC work with it?", hpvcNo: "No, HESC works on its own",
    price: "Where do your prices come from?", priceSub: "A ✓ means HESC found that source in Home Assistant.", gridClock: "Grid Clock (all of Europe, 41 zones)",
    gcNote: "Grid Clock gives the bare market price. Enter mark-up and VAT under Costs.", gcEuro: "Grid Clock always delivers in euro.", now: "now",
    ready: "Done! HESC v4 gets to work.", readySub: "HESC starts in shadow mode: it watches and switches nothing. Switch it on on the start page when you are ready. You can change everything later under Settings.",
    recommended: "recommended", others: "Other sensors", gridHelp: "The power of your whole house at the electricity meter (P1). Positive = import, negative = export.",
    confirm: "I understand that I stay responsible for my electrical installation.", found: "✓ = found in your Home Assistant", device: "Which charger is it? You have more than one of this brand.",
    otherNote: "You will pick 4 sensors or switches of your charger yourself.", colour: "colour", chargerShort: "Charger",
    sumLoad: "Charging", sumHouse: "House", sumSun: "Sun", sumPrice: "Prices", unknownConn: "connection unknown", lbShort: "load balancer", fixed: "fixed", none: "none",
    choose: "— choose —", errors: { required: "required", amps_invalid: "amps between 6 and 250", capacity_invalid: "capacity between 10 and 150 kWh", installer_setting: "maximum between 6 and 32 A", unknown_charger: "unknown charger", two_cars_already: "there are already two cars" },
    failed: "Saving failed:", ws: "HESC v4 does not answer. Restart Home Assistant if you just installed HESC v4.",
    fields: { ev_connected_sensor: "Car connected", ev_disconnected_values: "Values meaning 'no car'", ev_power_sensor: "Charging power", charger_mode_entity: "Charger mode", charger_eco_values: "Value(s) for solar charging", charger_solar_switch_entity: "Solar charging switch", charger_start_stop_entity: "Start/stop", charger_resume_entity: "Resume", charger_current_entity: "Charging current", ev_green_energy_sensor: "Green energy" },
  },
  de: {
    step: (i, n) => `Erster Start · Schritt ${i} von ${n}`, next: "Weiter ›", back: "‹ Zurück", done: "Fertig", saving: "Speichern…",
    shadow: "HESC v4 startet im Schattenmodus: es schaut zu und schaltet nichts.",
    how: "Wie lädst du zu Hause?", one: "Ein Auto", twoShared: "Zwei Autos, eine Wallbox", twoSharedSub: "abwechselnd, du steckst das Kabel um", twoOwn: "Zwei Autos, jedes eine eigene Wallbox",
    house: "Dein Haus", phases: "Hauptanschluss: Anzahl Phasen", ph1: "1 Phase", ph3: "3 Phasen", dk: "Weiß nicht", amps: "Ampere pro Phase", own: "andere",
    lb: "hast du ein Lastmanagement, das den Hausverbrauch berücksichtigt?", lbSub: "Zum Beispiel Wallbox Power Boost oder eine Wallbox, die den Smart Meter mitliest.",
    yes: "Ja", no: "Nein", solar: "hast du eine PV-Anlage?", dynamic: "hast du dynamische Strompreise?",
    resp: "HESC hält damit das Laden als Komfort innerhalb des Anschlusses. Du bleibst verantwortlich, dass deine Elektroinstallation nicht überlastet wird; dafür sorgen Wallbox, Lastmanagement und Installateur.",
    charger: (n) => n === 2 ? "Deine Wallboxen" : "Deine Wallbox", chargerSub: "Die Marke und das vom Installateur eingestellte Maximum.", chargerN: (j) => `Wallbox ${j}`,
    other: "Andere", maxA: "vom Installateur eingestelltes Maximum", maxASub: "Weißt du es nicht, lass 16 A stehen. Bei Easee, Peblar und Wallbox liest HESC es aus der Wallbox.",
    car: (n) => n === 2 ? "Deine Autos" : "Dein Auto", carSub: "Der Name kommt aus Home Assistant; ändere ihn, wenn du willst.", carN: (j) => `Auto ${j}`,
    name: "Name", capacity: "Akkukapazität", capSub: "Steht in den technischen Daten deines Autos.", atCharger: "an Wallbox",
    sharing: "Abwechselnd", sharingSub: "Beide Autos laden an derselben Wallbox. Das Auto, das abends angesteckt ist, lädt zuerst; das andere, nachdem du das Kabel umgesteckt hast.",
    swap: "Kabel spätestens umstecken um", remind: "Erinnerung auf dem Handy, wenn das Kabel umgesteckt werden soll",
    missingCharger: (b) => `Wallbox: ${b}`, missingSub: "Das hat HESC nicht gefunden. Wähle es selbst:",
    soc: (c) => `Ladestand von ${c}`, socSub: "Welcher Sensor gibt den Akku-% dieses Autos?", socNone: "Keiner: HESC schätzt ihn. Du kannst den Ladestand auch auf der Startseite oder dem Handy eingeben.",
    sources: "Sonne und Netz", pv: "PV-Leistung jetzt", pvHpvc: "Du hast auch HPVC. Darum hat HESC zwei Zähler für deine Solarmodule gefunden: den von HPVC und einen anderen. Der HPVC-Zähler zählt manchmal nur einen Teil deiner Module. HESC hat den Zähler gewählt, der alle Module zusammen zählt. Stimmt das? Dann musst du nichts tun.", grid: "Netzleistung jetzt", fcNow: "PV-Prognose jetzt", fc30: "PV-Prognose in 30 Minuten",
    hpvc: "HPVC gefunden", hpvcSub: "HPVC regelt deine PV-Anlage bei negativen Preisen. Soll HESC damit zusammenarbeiten?", hpvcNo: "Nein, HESC arbeitet allein",
    price: "Woher kommen deine Preise?", priceSub: "Ein ✓ heißt: HESC hat diese Quelle in Home Assistant gefunden.", gridClock: "Grid Clock (ganz Europa, 41 Zonen)",
    gcNote: "Grid Clock liefert den reinen Börsenpreis. Aufschlag und MwSt. unter Kosten eintragen.", gcEuro: "Grid Clock liefert immer in Euro.", now: "jetzt",
    ready: "Fertig! HESC v4 legt los.", readySub: "HESC startet im Schattenmodus: es schaut zu und schaltet nichts. Schalte es auf der Startseite ein, wenn du so weit bist. Alles kannst du später unter Einstellungen ändern.",
    recommended: "empfohlen", others: "Andere Sensoren", gridHelp: "Die Leistung deines ganzen Hauses am Stromzähler (P1). Positiv = Bezug, negativ = Einspeisung.",
    confirm: "Ich verstehe, dass ich selbst für meine Elektroinstallation verantwortlich bleibe.", found: "✓ = in deinem Home Assistant gefunden", device: "Welche Wallbox ist es? Du hast mehrere dieser Marke.",
    otherNote: "Du wählst gleich selbst 4 Sensoren oder Schalter deiner Wallbox.", colour: "Farbe", chargerShort: "Wallbox",
    sumLoad: "Laden", sumHouse: "Haus", sumSun: "Sonne", sumPrice: "Preise", unknownConn: "Anschluss unbekannt", lbShort: "Lastmanagement", fixed: "fest", none: "keine",
    choose: "— wählen —", errors: { required: "Pflichtfeld", amps_invalid: "Ampere zwischen 6 und 250", capacity_invalid: "Kapazität zwischen 10 und 150 kWh", installer_setting: "Maximum zwischen 6 und 32 A", unknown_charger: "unbekannte Wallbox", two_cars_already: "es gibt schon zwei Autos" },
    failed: "Speichern fehlgeschlagen:", ws: "HESC v4 antwortet nicht. Starte Home Assistant neu, wenn du HESC v4 gerade installiert hast.",
    fields: { ev_connected_sensor: "Auto angesteckt", ev_disconnected_values: "Werte für 'kein Auto'", ev_power_sensor: "Ladeleistung", charger_mode_entity: "Modus der Wallbox", charger_eco_values: "Wert(e) für PV-Laden", charger_solar_switch_entity: "Schalter PV-Laden", charger_start_stop_entity: "Start/Stopp", charger_resume_entity: "Fortsetzen", charger_current_entity: "Ladestrom", ev_green_energy_sensor: "Grüne Energie" },
  },
};
// "Auto toevoegen" (decision 06-11-2026 19:25): the same card in add mode adds a second car
Object.assign(FS_TXT.nl, { addHow: "Waar laadt de tweede auto?", addSame: "Aan dezelfde laadpaal", addSameSub: "om de beurt met de eerste auto", addOwn: "Aan een eigen laadpaal", addTitle: "Auto toevoegen", addDone: "Toevoegen", addFull: "Je hebt al twee auto's. Meer kan HESC niet.", addReadySub: "HESC voegt de tweede auto toe en herlaadt. De schaduwmodus blijft zoals hij is." });
Object.assign(FS_TXT.en, { addHow: "Where does the second car charge?", addSame: "At the same charger", addSameSub: "taking turns with the first car", addOwn: "At its own charger", addTitle: "Add a car", addDone: "Add", addFull: "You already have two cars. HESC handles no more.", addReadySub: "HESC adds the second car and reloads. Shadow mode stays as it is." });
Object.assign(FS_TXT.de, { addHow: "Wo lädt das zweite Auto?", addSame: "An derselben Wallbox", addSameSub: "abwechselnd mit dem ersten Auto", addOwn: "An einer eigenen Wallbox", addTitle: "Auto hinzufügen", addDone: "Hinzufügen", addFull: "Du hast schon zwei Autos. Mehr kann HESC nicht.", addReadySub: "HESC fügt das zweite Auto hinzu und lädt neu. Der Schattenmodus bleibt, wie er ist." });
const FS_BRANDS = ["Wallbox", "Alfen Eve", "Peblar", "myenergi Zappi", "go-e Charger", "Fronius Wattpilot", "SMA EV Charger", "evcc (any charger)", "Ohme", "Easee", "Other (manual)"];
const FS_COLORS = ["#3fc8f4", "#ff8a65"];
// decision 02-11 10:59: four car colours that mean nothing else on the dashboard
const FS_PALETTE = [["light_blue", "#3fc8f4"], ["salmon", "#ff8a65"], ["pink", "#f06292"], ["copper", "#b87333"]];
const FS_REQUIRED = ["ev_connected_sensor", "ev_power_sensor", "charger_mode_entity", "charger_eco_values"]; // config_flow.CHARGER_REQUIRED
const FS_CSS = `
:host{--line:var(--divider-color,#30333c);--muted:var(--secondary-text-color,#9aa0aa);--card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));--dot:#ff9800;--c:var(--primary-color)}
ha-card{padding:18px 20px;display:grid;gap:16px;max-width:760px;margin:0 auto}
.prog{display:flex;gap:6px}.prog i{flex:1;height:4px;border-radius:2px;background:var(--card2)}.prog i.on{background:var(--c)}
.step{font-size:12px;color:var(--muted)}
h3{margin:0;font-size:20px;font-weight:500;line-height:1.3}h4{margin:0;font-size:15px;font-weight:500;display:flex;gap:8px;align-items:center}h4 i{width:10px;height:10px;border-radius:50%}
.sub{margin:0;color:var(--muted);font-size:14px;line-height:1.45}.note{color:var(--dot)}
.big{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.opt{font:inherit;border-radius:14px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:14px 12px;cursor:pointer;text-align:left;display:grid;gap:4px;align-content:start}
.opt b{font-size:17px}.opt span{font-size:12px;color:var(--muted)}.opt.on{border-color:var(--c);background:color-mix(in srgb,var(--c) 22%,transparent)}
.chips{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.chip{font:inherit;font-size:14px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:8px 14px;cursor:pointer}
.chip.on{border-color:var(--c);background:color-mix(in srgb,var(--c) 25%,transparent);font-weight:600}
.box{display:grid;gap:12px;border:1.5px solid var(--line);border-radius:14px;padding:14px}
.row{display:flex;gap:10px;align-items:center;background:var(--card2);border-radius:12px;padding:10px 14px;font-size:14px}
.row small{display:block;color:var(--muted);font-size:12px}
.name,select{font:inherit;font-size:15px;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:8px 12px;width:100%;box-sizing:border-box}
.name:focus,select:focus{outline:none;border-color:var(--c)}.name.amp{width:90px}.name.cap{width:120px}
.lbl{font-size:12px;color:var(--muted);margin-bottom:4px}.err{color:#ef5350;font-size:12px;margin-top:4px}
.nav{display:flex;gap:10px;align-items:center}
.btn{font:inherit;font-size:14px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:9px 18px;cursor:pointer}
.btn.pri{background:var(--c);border-color:var(--c);color:var(--text-primary-color,#fff);font-weight:600}.btn[disabled]{opacity:.4;cursor:default}
.stp2{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:var(--card2);height:40px;flex:none}
.stp2 button{width:40px;height:40px;border:0;background:none;color:var(--primary-text-color);font-size:20px;cursor:pointer;border-radius:50%}
.stp2 b{min-width:62px;text-align:center;font-size:18px;font-weight:600}
.tg{width:48px;height:28px;border-radius:999px;border:0;background:var(--card2);box-shadow:inset 0 0 0 1.5px var(--line);position:relative;cursor:pointer;flex:none}
.tg::after{content:"";position:absolute;top:4px;left:4px;width:20px;height:20px;border-radius:50%;background:var(--muted);transition:left .15s}
.tg.on{background:var(--c);box-shadow:none}.tg.on::after{left:24px;background:#fff}
.ok{color:#66bb6a;font-weight:700}
.pickrow{display:block;width:100%;text-align:left;font:inherit;font-size:14px;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:9px 12px;margin-top:6px;cursor:pointer}
.pickrow.on{border-color:var(--c);background:color-mix(in srgb,var(--c) 22%,transparent)}
details summary{cursor:pointer;margin-top:8px}
.dotc{width:34px;height:34px;border-radius:50%;border:3px solid transparent;background:var(--dc);background-clip:padding-box;box-shadow:0 0 0 1.5px var(--line);cursor:pointer;padding:0}
.dotc.on{box-shadow:0 0 0 3px var(--primary-text-color,#fff)}.dotc[disabled]{opacity:.25;cursor:default}
.cdot{display:inline-block;width:12px;height:12px;border-radius:50%}
dl{display:grid;grid-template-columns:auto 1fr;gap:8px 18px;margin:0;font-size:15px}dt{color:var(--muted)}dd{margin:0;font-weight:500}
`;
const fsStep = (t, d) => { const [h, m] = t.split(":").map(Number); let x = (h * 60 + m + d * 15 + 1440) % 1440; return `${String(Math.floor(x / 60)).padStart(2, "0")}:${String(x % 60).padStart(2, "0")}`; };
const fsEsc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

class HescV4FirstStart extends HTMLElement {
  setConfig(config) { this._config = config || {}; }
  getCardSize() { return 8; }
  getGridOptions() { return { columns: "full", rows: "auto" }; }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    const st = hass.states["sensor.hesc_v4_setup"];
    // the sensor is a hint (it can still be "unknown" right after installing); hesc_v4/setup/find has the truth
    const done = !st || st.attributes.setup_done === true || (this._find && this._find.setup_done === true);
    if (this._config && (this._config.add || this._config.redo)) this._force = true; // redo: 11-11-2026, run the first start again
    if (done && !this._force) { if (this.style.display !== "none") { this.style.display = "none"; if (this.shadowRoot) this.shadowRoot.innerHTML = ""; } return; }
    this.style.display = "";
    if (first || !this._find) this._load();
  }

  get t() { const l = (this._hass && (this._hass.locale?.language || this._hass.language) || "en").slice(0, 2); return FS_TXT[l] || FS_TXT.en; }

  async _load() {
    if (this._loading) return;
    this._loading = true;
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    try {
      this._find = await this._hass.callWS({ type: "hesc_v4/setup/find" });
    } catch (e) {
      this.shadowRoot.innerHTML = `<style>${FS_CSS}</style><ha-card><p class="sub note">${this.t.ws}</p></ha-card>`;
      this._loading = false; return;
    }
    if (this._find.setup_done && !this._add() && !(this._config && this._config.redo)) { this._loading = false; this.style.display = "none"; this.shadowRoot.innerHTML = ""; return; }
    const f = this._find, one = (l) => (l && l.length === 1 ? l[0] : null);
    const brands = (f.chargers || []).flatMap((c) => (c && c.brand ? Array(c.count || 1).fill(c.brand) : [c])); // [{brand, count, devices}] or names
    this._a = { // answers, pre-filled (decision 10:42)
      how: "one", phases: f.phases === "1" || f.phases === "3" ? f.phases : "", amps: "", lb: "",
      solar: f.solar, dynamic: f.dynamic, brand: [brands[0] || "", brands[1] || brands[0] || ""], max_a: [16, 16],
      cars: [0, 1].map((j) => { const c = (f.cars || [])[j] || {}; return { name: c.car_name || "", capacity: c.capacity || "", soc: c.entity_id, colour: FS_PALETTE[j][0] }; }),
      confirm: false,
      soc: [undefined, undefined], swap: "22:30", remind: true, ent: [{}, {}], src: {}, hpvc: true,
      price: (f.prices || [])[0] || null,
    };
    if (one(f.cars)) this._a.soc[0] = undefined; // the one found is taken by HESC itself
    if (this._add()) { // second car: ev1 keeps its colour, ev2 gets the first free one; the car found that is not ev1's comes first
      this._a.brand[1] = ""; // a second charger never starts as the first one's brand
      const c1 = ((this._hass.states["select.hesc_v4_ev1_colour"] || {}).state) || FS_PALETTE[0][0];
      this._a.cars[0].colour = c1; this._a.cars[1].colour = (FS_PALETTE.find((p) => p[0] !== c1) || FS_PALETTE[1])[0];
      this._a.how = "add_same"; this._a.add = "same";
      const ev1soc = ((this._hass.states["sensor.hesc_v4_setup"] || {}).attributes || {}).hesc_ev_soc_sensor;
      const other = (f.cars || []).find((c) => c.entity_id !== ev1soc); if (other) { this._a.cars[1].name = other.car_name || ""; this._a.cars[1].capacity = other.capacity || ""; this._a.soc[1] = other.entity_id; }
      this._full = !this._addC() && !!this._hass.states["sensor.hesc_v4_ev2_charge_plan"];
    }
    this._i = 0; this._err = {}; this._chg = [null, null];
    this._loading = false;
    this._render();
  }

  _add() { return !!(this._config && this._config.add); }
  _addC() { return !!(this._config && this._config.add === "charger"); } // 08-11: a second charger for EV2, that shares charger 1
  _carIdx() { return this._add() ? [1] : Array.from({ length: this._n() }, (_, j) => j); }
  _chIdx() { return this._add() ? (this._a.add === "own" ? [1] : []) : Array.from({ length: this._nCh() }, (_, j) => j); }
  _n() { return this._a.how === "one" ? 1 : 2; }
  _hex(k) { return (FS_PALETTE.find((p) => p[0] === k) || FS_PALETTE[0])[1]; }
  _found(brand) { // decision 02-11 10:55: one green tick per charger found (find may list a brand once per charger device)
    return (this._find.chargers || []).reduce((n, c) => n + ((c && c.brand ? c.brand : c) === brand ? (c && c.count) || 1 : 0), 0);
  }
  _kw(amps) { // decision 02-11 10:54: 16 A = 11 kW, 32 A = 22 kW (3 phases); 1 phase 3.7 / 7.4 kW
    const ph = this._a.phases === "1" ? 1 : 3, kw = (amps * 230 * ph) / 1000;
    return `${(ph === 3 ? Math.round(kw) : Math.round(kw * 10) / 10).toString().replace(".", this.t === FS_TXT.en ? "." : ",")} kW`;
  }
  _nCh() { return this._a.how === "two_own" || this._a.add === "own" ? 2 : 1; }

  _steps() {
    const a = this._a, f = this._find, st = ["how", "house", "charger", "car"];
    if (this._addC()) {
      a.add = "own"; const s3 = ["charger"];
      if (this._chg[1] && this._chg[1].missing.length) s3.push("missing1");
      s3.push("done"); return s3;
    }
    if (this._add()) {
      const s2 = ["addhow"]; if (a.add === "own") s2.push("charger"); s2.push("car");
      if (a.add === "own" && this._chg[1] && this._chg[1].missing.length) s2.push("missing1");
      s2.push("soc1", "done"); return s2;
    }
    if (a.how === "two_shared") st.push("sharing");
    for (let j = 0; j < this._nCh(); j++) if (this._chg[j] && this._chg[j].missing.length) st.push(`missing${j}`);
    for (let j = 0; j < this._n(); j++) if ((f.cars || []).length !== 1) st.push(`soc${j}`);
    if (this._srcAsk().length) st.push("sources");
    if (f.hpvc) st.push("hpvc");
    if (a.dynamic && (f.prices || []).length !== 1) st.push("price");
    st.push("done");
    return st;
  }

  _srcAsk() { // only what is missing (decision 10:28)
    const f = this._find, a = this._a, ask = [];
    // 11-11-2026: HESC's own suggestion beats HPVC's solar sensor (HPVC may measure only part of the panels)
    if (a.solar && ((f.pv || []).length !== 1 && !f.pv_from_hpvc || (f.pv_suggested && f.pv_from_hpvc && f.pv_suggested !== f.pv_from_hpvc))) ask.push("pv_power_sensor");
    if ((f.grid || []).length !== 1 && !f.grid_from_hpvc) ask.push("grid_power_sensor"); // 02-11 #9: taken from HPVC
    if (a.solar && !(f.forecast && f.forecast.forecast_now_sensor)) ask.push("forecast_now_sensor", "forecast_30m_sensor");
    return ask;
  }

  _ok(id) {
    const a = this._a;
    if (id === "house") return !!a.phases && (a.phases === "dk" || +a.amps >= 6) && !!a.lb && a.solar != null && a.dynamic != null && a.confirm;
    if (id === "charger") return this._chIdx().every((j) => a.brand[j]);
    if (id === "car") return this._carIdx().every((j) => +a.cars[j].capacity >= 10 && +a.cars[j].capacity <= 150);
    if (id && id.startsWith("missing")) { const j = +id.slice(7); return this._chg[j].missing.filter((k) => FS_REQUIRED.includes(k)).every((k) => a.ent[j][k] || (k === "charger_eco_values" && this._chg[j].values[k] && String(this._chg[j].values[k]).length)); }
    if (id === "sources") return ["pv_power_sensor", "grid_power_sensor"].filter((k) => this._srcAsk().includes(k)).every((k) => a.src[k]);
    return true;
  }

  _pickEnt(key, val, list, domains, none) { // a select of the candidates, else all entities of the domains
    const all = list && list.length ? list.map((c) => (typeof c === "string" ? { entity_id: c } : c))
      : Object.keys(this._hass.states).filter((id) => domains.some((d) => id.startsWith(`${d}.`))).sort().map((id) => ({ entity_id: id }));
    const lab = (c) => `${fsEsc(c.name || this._hass.states[c.entity_id]?.attributes.friendly_name || c.entity_id)}${c.state != null ? ` — ${this.t.now} ${fsEsc(c.state)} ${fsEsc(c.unit || "")}` : ""}`;
    return `<select data-ent="${key}"><option value="">${none || this.t.choose}</option>${all.map((c) => `<option value="${fsEsc(c.entity_id)}"${c.entity_id === val ? " selected" : ""}>${lab(c)}</option>`).join("")}</select>`;
  }

  _gridPick() { // 02-11 #8: only smart-meter sensors, the recommended one on top, the rest folded away
    const t = this.t, a = this._a, g = this._find.grid || [], cur = a.src.grid_power_sensor;
    const lab = (c) => c.combined ? `${fsEsc(c.name)} + ${fsEsc(c.export_name)} — ${t.now} ${fsEsc(c.state)} / ${fsEsc(c.export_state)} ${fsEsc(c.unit || "")}` : `${fsEsc(c.name)} — ${t.now} ${fsEsc(c.state)} ${fsEsc(c.unit || "")}`;
    const btn = (c, k) => `<button class="pickrow${cur === c.entity_id ? " on" : ""}" data-grid="${k}">${c.recommended ? `<span class="ok">✓ ${t.recommended}</span> ` : ""}${lab(c)}</button>`;
    const rec = g.filter((c) => c.recommended), rest = g.filter((c) => !c.recommended);
    return `<p class="sub">${t.gridHelp}</p>${rec.map((c) => btn(c, g.indexOf(c))).join("")}${rest.length ? `<details${rest.some((c) => c.entity_id === cur) ? " open" : ""}><summary class="sub">${t.others} (${rest.length})</summary>${rest.map((c) => btn(c, g.indexOf(c))).join("")}</details>` : ""}`;
  }

  _render() {
    const t = this.t, a = this._a, f = this._find, steps = this._steps();
    this._i = Math.max(0, Math.min(this._i, steps.length - 1));
    const id = steps[this._i], last = id === "done", e = (k) => (this._err[k] ? `<div class="err">${t.errors[this._err[k]] || this._err[k]}</div>` : "");
    const opt = (k, v, title, sub) => `<button class="opt${a[k] === v ? " on" : ""}" data-k="${k}" data-v="${v}"><b>${title}</b>${sub ? `<span>${sub}</span>` : ""}</button>`;
    const ch = (k, v, label) => `<button class="chip${a[k] === v ? " on" : ""}" data-k="${k}" data-v="${v}">${label}</button>`;
    const yn = (k) => `<button class="chip${a[k] === true ? " on" : ""}" data-k="${k}" data-b="1">${t.yes}</button><button class="chip${a[k] === false ? " on" : ""}" data-k="${k}" data-b="0">${t.no}</button>`;
    let body = "";
    if (this._add() && this._full) {
      body = `<h3>${t.addTitle}</h3><p class="sub">${t.addFull}</p>`;
    } else if (id === "addhow") {
      body = `<h3>${t.addHow}</h3><div class="big">${opt("add", "same", t.addSame, t.addSameSub)}${opt("add", "own", t.addOwn)}</div>`;
    } else if (this._addC() && id === "done") {
      const errs = Object.keys(this._err).length ? `<p class="sub note">${t.failed} ${Object.entries(this._err).map(([k, v]) => `${fsEsc(k)}: ${t.errors[v] || fsEsc(v)}`).join(" · ")}</p>` : "";
      const n2 = fsEsc(((this._hass.states["text.hesc_v4_ev2_car_name"] || {}).state) || t.carN(2));
      body = `<h3>${t.ready}</h3><dl><dt>${t.chargerShort} 2</dt><dd>${a.brand[1] === "Other (manual)" ? t.other : fsEsc(a.brand[1])}, max. ${a.max_a[1]} A</dd><dt>${t.carN(2)}</dt><dd>${n2}</dd></dl>${errs}`;
    } else if (this._add() && id === "done") {
      const c = a.cars[1], nl = (v) => (this.t === FS_TXT.en ? String(v) : String(v).replace(".", ","));
      const errs = Object.keys(this._err).length ? `<p class="sub note">${t.failed} ${Object.entries(this._err).map(([k, v]) => `${fsEsc(k)}: ${t.errors[v] || fsEsc(v)}`).join(" · ")}</p>` : "";
      body = `<h3>${t.ready}</h3><p class="sub">${t.addReadySub}</p><dl><dt>${t.carN(2)}</dt><dd><i class="cdot" style="background:${this._hex(c.colour)}"></i> ${fsEsc(c.name || t.carN(2))} · ${nl(c.capacity)} kWh</dd>
        <dt>${t.chargerShort}</dt><dd>${a.add === "own" ? `${a.brand[1] === "Other (manual)" ? t.other : fsEsc(a.brand[1])}, max. ${a.max_a[1]} A` : t.addSame}</dd></dl>${errs}`;
    } else if (id === "how") {
      body = `<h3>${t.how}</h3><p class="sub">${t.shadow}</p><div class="big">${opt("how", "one", t.one)}${opt("how", "two_shared", t.twoShared, t.twoSharedSub)}${opt("how", "two_own", t.twoOwn)}</div>`;
    } else if (id === "house") {
      const list = a.phases === "1" || a.phases === "3" ? (f.amps || {})[a.phases] || [] : [];
      body = `<h3>${t.house}</h3>
        <div><div class="lbl">${t.phases}</div><div class="chips">${ch("phases", "1", t.ph1)}${ch("phases", "3", t.ph3)}${ch("phases", "dk", t.dk)}</div></div>
        ${list.length ? `<div><div class="lbl">${t.amps}</div><div class="chips">${list.map((v) => ch("amps", String(v), `${v} A`)).join("")}<input class="name amp" data-amps type="number" min="6" max="250" placeholder="${t.own}" value="${list.map(String).includes(String(a.amps)) ? "" : fsEsc(a.amps)}"></div>${e("house.amps")}</div>` : ""}
        <div><div class="lbl">${t.lb}</div><div class="chips">${ch("lb", "Yes", t.yes)}${ch("lb", "No", t.no)}${ch("lb", "Don't know", t.dk)}</div><p class="sub">${t.lbSub}</p></div>
        <div><div class="lbl">${t.solar}</div><div class="chips">${yn("solar")}</div></div>
        <div><div class="lbl">${t.dynamic}</div><div class="chips">${yn("dynamic")}</div></div>
        <p class="sub"><span class="note">${t.resp}</span></p>
        <label class="row" style="cursor:pointer"><input type="checkbox" data-confirm${a.confirm ? " checked" : ""} style="width:20px;height:20px;accent-color:var(--c)"><span>${t.confirm}</span></label>`;
    } else if (id === "charger") {
      body = `<h3>${t.charger(this._nCh())}</h3><p class="sub">${t.chargerSub}</p>` + this._chIdx().map((j) => `<div class="box">
        ${this._nCh() === 2 ? `<h4>${t.chargerN(j + 1)}</h4>` : ""}
        <div class="chips">${FS_BRANDS.map((b) => { const n = this._found(b); return `<button class="chip${a.brand[j] === b ? " on" : ""}" data-brand="${j}" data-v="${fsEsc(b)}">${n ? `<span class="ok">${"✓".repeat(n)}</span> ` : ""}${b === "Other (manual)" ? t.other : b.replace(" (any charger)", "")}</button>`; }).join("")}</div>
        ${this._chg[j] && this._chg[j].device_choice && (this._chg[j].devices || []).length > 1 ? `<p class="sub">${t.device}</p><div class="chips">${this._chg[j].devices.map((d) => `<button class="chip${(this._chg[j].device || "") === d.id ? " on" : ""}" data-dev="${j}" data-v="${fsEsc(d.id)}">${fsEsc(d.name)}</button>`).join("")}</div>` : ""}
        ${(f.chargers || []).length ? `<p class="sub">${t.found}</p>` : ""}${a.brand[j] === "Other (manual)" ? `<p class="sub note">${t.otherNote}</p>` : ""}
        <div class="row"><span style="flex:1">${t.maxA}<small>${t.maxASub}</small></span><div class="stp2"><button data-max="${j}" data-d="-1">−</button><b>${a.max_a[j]} A · ${this._kw(a.max_a[j])}</b><button data-max="${j}" data-d="1">+</button></div></div>${e(`chargers.charger${j + 1}.max_a`)}</div>`).join("");
    } else if (id === "car") {
      body = `<h3>${t.car(this._n())}</h3><p class="sub">${t.carSub}</p>` + this._carIdx().map((j) => `<div class="box">
        <h4><i style="background:${this._hex(a.cars[j].colour)}"></i>${t.carN(j + 1)}</h4>
        <div><div class="lbl">${t.name}</div><input class="name" data-name="${j}" value="${fsEsc(a.cars[j].name)}"></div>
        <div><div class="lbl">${t.capacity}</div><div class="chips"><input class="name cap" data-cap="${j}" type="number" min="10" max="150" step="0.1" value="${fsEsc(a.cars[j].capacity)}"> kWh</div><p class="sub">${t.capSub}</p>${e(`cars.ev${j + 1}.capacity`)}</div>
        <div><div class="lbl">${t.colour}</div><div class="chips">${FS_PALETTE.map(([k, hex]) => { const taken = (this._add() || this._n() === 2) && a.cars[1 - j].colour === k; return `<button class="dotc${a.cars[j].colour === k ? " on" : ""}" data-colour="${j}" data-v="${k}" style="--dc:${hex}"${taken ? " disabled" : ""} aria-label="${k}"></button>`; }).join("")}</div></div>
        ${this._nCh() === 2 ? `<div class="lbl">${t.atCharger} ${j + 1}</div>` : ""}</div>`).join("");
    } else if (id === "sharing") {
      body = `<h3>${t.sharing}</h3><p class="sub">${t.sharingSub}</p>
        <div><div class="lbl">${t.swap}</div><div class="stp2"><button data-swap="-1">−</button><b>${a.swap}</b><button data-swap="1">+</button></div></div>
        <div class="row"><span style="flex:1">${t.remind}</span><button class="tg${a.remind ? " on" : ""}" data-remind role="switch" aria-checked="${a.remind}"></button></div>`;
    } else if (id.startsWith("missing")) {
      const j = +id.slice(7), c = this._chg[j];
      body = `<h3>${t.missingCharger(a.brand[j] === "Other (manual)" ? t.other : a.brand[j])}</h3><p class="sub">${t.missingSub}</p>` + c.missing.map((k) => `<div><div class="lbl">${t.fields[k] || k}</div>${
        /values$/.test(k) ? `<input class="name" data-txt="c${j}.${k}" value="${fsEsc(a.ent[j][k] ?? (Array.isArray(c.values[k]) ? c.values[k].join(", ") : c.values[k] || ""))}">`
          : this._pickEnt(`c${j}.${k}`, a.ent[j][k], (c.candidates || {})[k], ["sensor", "binary_sensor", "select", "switch", "button", "number", "input_select", "input_boolean"])}${e(`chargers.charger${j + 1}.entities.${k}`)}</div>`).join("");
    } else if (id.startsWith("soc")) {
      const j = +id.slice(3);
      body = `<h3>${t.soc(fsEsc(a.cars[j].name || t.carN(j + 1)))}</h3><p class="sub">${t.socSub}</p>${this._pickEnt(`soc.${j}`, a.soc[j], f.cars || [], ["sensor"], t.socNone)}`;
    } else if (id === "sources") {
      if (!a.src.pv_power_sensor && f.pv_suggested) a.src.pv_power_sensor = f.pv_suggested; // 10-11: HESC's suggestion ready
      const lab = { pv_power_sensor: t.pv, grid_power_sensor: t.grid, forecast_now_sensor: t.fcNow, forecast_30m_sensor: t.fc30 };
      const cand = { pv_power_sensor: f.pv, grid_power_sensor: f.grid };
      const hp = f.pv_suggested && f.pv_from_hpvc && f.pv_suggested !== f.pv_from_hpvc;
      body = `<h3>${t.sources}</h3><p class="sub">${hp ? t.pvHpvc : t.missingSub}</p>` + this._srcAsk().map((k) => `<div><div class="lbl">${lab[k]}</div>${k === "grid_power_sensor" && (f.grid || []).length ? this._gridPick() : this._pickEnt(`src.${k}`, a.src[k], cand[k], ["sensor"])}${e(`sources.${k}`)}</div>`).join("");
    } else if (id === "hpvc") {
      body = `<h3>${t.hpvc}</h3><p class="sub">${t.hpvcSub}</p><div class="chips"><button class="chip${a.hpvc ? " on" : ""}" data-hpvc="1">${t.yes}</button><button class="chip${!a.hpvc ? " on" : ""}" data-hpvc="0">${t.hpvcNo}</button></div>`;
    } else if (id === "price") {
      const ps = f.prices || [], cur = a.price;
      body = `<h3>${t.price}</h3><p class="sub">${t.priceSub}</p><div class="chips">${ps.map((p, k) => `<button class="chip${cur && cur.sensor === p.sensor ? " on" : ""}" data-price="${k}">✓ ${p.source === "Grid Clock" ? t.gridClock : fsEsc(p.label || p.source)}${p.zone ? ` · ${fsEsc(p.zone)}` : ""}${p.now != null ? ` · ${t.now} ${fsEsc(p.now)} ct` : ""}</button>`).join("")}</div>
        ${cur && cur.source === "Grid Clock" ? `<p class="sub">${t.gcNote}${this._hass.config.currency && this._hass.config.currency !== "EUR" ? ` ${t.gcEuro}` : ""}</p>` : ""}${e("price")}`;
    } else {
      const nl = (v) => (this.t === FS_TXT.en ? String(v) : String(v).replace(".", ","));
      const chgOf = (j) => { const k = this._nCh() === 2 ? j : 0, b = a.brand[k]; return `${b === "Other (manual)" ? t.other : b.replace(" (any charger)", "")}, max. ${a.max_a[k]} A · ${this._kw(a.max_a[k])}`; };
      const carRows = a.cars.slice(0, this._n()).map((c, j) => `<dt>${this._n() === 2 ? t.carN(j + 1) : t.carN("").trim()}</dt><dd><i class="cdot" style="background:${this._hex(c.colour)}"></i> ${fsEsc(c.name || t.carN(j + 1))} · ${nl(c.capacity)} kWh${this._nCh() === 2 ? ` · ${chgOf(j)}` : ""}</dd>`).join("");
      const chgRow = this._nCh() === 1 ? `<dt>${t.chargerShort}</dt><dd>${chgOf(0)}${a.how === "two_shared" ? ` · ${t.twoSharedSub}` : ""}</dd>` : "";
      const conn = a.phases === "dk" || !a.phases ? t.unknownConn : `${a.phases}×${a.amps} A`;
      const errs = Object.keys(this._err).length ? `<p class="sub note">${t.failed} ${Object.entries(this._err).map(([k, v]) => `${fsEsc(k)}: ${t.errors[v] || fsEsc(v)}`).join(" · ")}</p>` : "";
      body = `<h3>${t.ready}</h3><p class="sub">${t.readySub}</p>
        <dl>${carRows}${chgRow}
        <dt>${t.sumHouse}</dt><dd>${conn} · ${t.lbShort}: ${a.lb === "Yes" ? t.yes : a.lb === "No" ? t.no : t.dk}</dd>
        <dt>${t.sumSun}</dt><dd>${a.solar ? t.yes : t.no}${f.hpvc && a.solar ? ` · HPVC: ${a.hpvc ? t.yes : t.no}` : ""}</dd>
        <dt>${t.sumPrice}</dt><dd>${a.dynamic ? fsEsc(a.price ? `${a.price.label || a.price.source}${a.price.zone ? ` ${a.price.zone}` : ""}` : "?") : t.fixed}</dd></dl>${errs}`;
    }
    this.shadowRoot.innerHTML = `<style>${FS_CSS}</style><ha-card>
      <div class="prog">${steps.map((_, k) => `<i class="${k <= this._i ? "on" : ""}"></i>`).join("")}</div>
      <div class="step">${t.step(this._i + 1, steps.length)}</div>${body}
      <div class="nav"${this._add() && this._full ? " hidden" : ""}>${this._i > 0 ? `<button class="btn" id="prev">${t.back}</button>` : ""}<span style="flex:1"></span>
        ${last ? `<button class="btn pri" id="save"${this._busy ? " disabled" : ""}>${this._busy ? t.saving : this._add() ? t.addDone : t.done}</button>` : `<button class="btn pri" id="next"${this._ok(id) ? "" : " disabled"}>${t.next}</button>`}</div>
    </ha-card>`;
    this._wire(id);
  }

  _wire(id) {
    const r = this.shadowRoot, a = this._a, re = () => this._render();
    r.querySelectorAll("[data-k]").forEach((b) => b.addEventListener("click", () => {
      const k = b.dataset.k; a[k] = b.dataset.b != null ? b.dataset.b === "1" : b.dataset.v;
      if (k === "phases") a.amps = ""; re();
    }));
    r.querySelectorAll("[data-amps]").forEach((i) => i.addEventListener("change", () => { a.amps = i.value ? String(Math.round(+i.value)) : ""; re(); }));
    r.querySelectorAll("[data-brand]").forEach((b) => b.addEventListener("click", () => { const j = +b.dataset.brand; a.brand[j] = b.dataset.v; (a.device = a.device || [])[j] = undefined; this._chg[j] = null; re(); this._loadChargers().then(re); }));
    r.querySelectorAll("[data-dev]").forEach((b) => b.addEventListener("click", () => { const j = +b.dataset.dev; (a.device = a.device || [])[j] = b.dataset.v; this._chg[j] = null; a.ent[j] = {}; this._loadChargers().then(re); }));
    r.querySelectorAll("[data-max]").forEach((b) => b.addEventListener("click", () => { const j = +b.dataset.max; a.max_a[j] = Math.max(6, Math.min(32, a.max_a[j] + +b.dataset.d)); re(); }));
    r.querySelectorAll("[data-name]").forEach((i) => i.addEventListener("change", () => { a.cars[+i.dataset.name].name = i.value.trim(); }));
    r.querySelectorAll("[data-cap]").forEach((i) => i.addEventListener("input", () => { a.cars[+i.dataset.cap].capacity = i.value; const n = r.getElementById("next"); if (n) n.disabled = !this._ok("car"); }));
    r.querySelectorAll("[data-grid]").forEach((b) => b.addEventListener("click", () => { const c = this._find.grid[+b.dataset.grid]; a.src.grid_power_sensor = c.entity_id; a.src.grid_export_sensor = c.combined ? c.export_entity_id : ""; re(); }));
    r.querySelectorAll("[data-confirm]").forEach((c) => c.addEventListener("change", () => { a.confirm = c.checked; a.confirmAt = c.checked ? new Date().toISOString() : null; re(); }));
    r.querySelectorAll("[data-colour]").forEach((b) => b.addEventListener("click", () => { a.cars[+b.dataset.colour].colour = b.dataset.v; re(); }));
    r.querySelectorAll("[data-swap]").forEach((b) => b.addEventListener("click", () => { a.swap = fsStep(a.swap, +b.dataset.swap); re(); }));
    r.querySelectorAll("[data-remind]").forEach((b) => b.addEventListener("click", () => { a.remind = !a.remind; re(); }));
    r.querySelectorAll("[data-hpvc]").forEach((b) => b.addEventListener("click", () => { a.hpvc = b.dataset.hpvc === "1"; re(); }));
    r.querySelectorAll("[data-price]").forEach((b) => b.addEventListener("click", () => { a.price = this._find.prices[+b.dataset.price]; re(); }));
    const upd = () => { const n = r.getElementById("next"); if (n) n.disabled = !this._ok(id); };
    r.querySelectorAll("[data-ent]").forEach((s) => s.addEventListener("change", () => { this._setEnt(s.dataset.ent, s.value); upd(); }));
    r.querySelectorAll("[data-txt]").forEach((s) => s.addEventListener("input", () => { this._setEnt(s.dataset.txt, s.value); upd(); }));
    const go = async (d) => {
      if (d > 0 && id === "charger") await this._loadChargers(); // part 2 needs to know what is missing per charger
      this._i += d; re();
    };
    if (r.getElementById("next")) r.getElementById("next").addEventListener("click", () => go(1));
    if (r.getElementById("prev")) r.getElementById("prev").addEventListener("click", () => go(-1));
    if (r.getElementById("save")) r.getElementById("save").addEventListener("click", () => this._save());
  }

  _setEnt(key, v) {
    const a = this._a, [grp, k] = key.split(/\.(.+)/);
    if (grp === "soc") a.soc[+k] = v;
    else if (grp === "src") a.src[k] = v;
    else a.ent[+grp.slice(1)][k] = v;
  }

  async _loadChargers() {
    for (const j of this._chIdx()) {
      const dev = (this._a.device || [])[j];
      if (this._chg[j] && this._chg[j].brand === this._a.brand[j] && (!dev || this._chg[j].device === dev)) continue;
      try {
        // per charger only the entities of that one device (two of the same brand; rekenchat caf95a0)
        const other = j && !this._add() ? (this._a.device || [])[0] || (this._chg[0] || {}).device : undefined;
        this._chg[j] = await this._hass.callWS({ type: "hesc_v4/setup/charger", brand: this._a.brand[j], ...(j ? { charger: "charger2" } : {}),
          ...(dev ? { device: dev } : {}), ...(other ? { other_device: other } : {}) });
        if (this._a.max_a[j] === 16 && this._chg[j].max_a) this._a.max_a[j] = this._chg[j].max_a; // read from the charger
      } catch (e) { this._chg[j] = { brand: this._a.brand[j], missing: [], values: {}, candidates: {} }; }
    }
  }

  _addAnswers() {
    const a = this._a, f = this._find, c = a.cars[1], car = { name: c.name, capacity: +c.capacity };
    if ((f.features || []).includes("car_colour")) car.colour = c.colour;
    if (a.soc[1] !== undefined) car.soc = a.soc[1];
    const ans = { add: a.add, cars: { ev2: car } };
    if (a.add === "own") {
      const ent = {}; Object.entries(a.ent[1]).forEach(([k, v]) => { if (v !== "" && v != null) ent[k] = /values$/.test(k) ? v.split(",").map((x) => x.trim()).filter(Boolean) : v; });
      ans.chargers = { charger2: { brand: a.brand[1], max_a: a.max_a[1], entities: ent, ...((this._chg[1] || {}).device ? { device: this._chg[1].device } : {}) } }; car.charger = "charger2";
    }
    return ans;
  }

  _answers() {
    const a = this._a, f = this._find, n = this._n(), nCh = this._nCh();
    const ans = {
      how: a.how,
      house: { phases: a.phases === "dk" || !a.phases ? "Don't know" : a.phases, ...(a.phases === "1" || a.phases === "3" ? { amps: +a.amps } : {}),
        load_balancer: a.lb, solar: !!a.solar, dynamic: !!a.dynamic,
        ...((f.features || []).includes("responsibility") ? { responsibility_ok: !!a.confirm, responsibility_at: a.confirmAt } : {}) },
      chargers: {}, cars: {},
    };
    for (let j = 0; j < nCh; j++) {
      const ent = {};
      Object.entries(a.ent[j]).forEach(([k, v]) => { if (v !== "" && v != null) ent[k] = /values$/.test(k) ? v.split(",").map((x) => x.trim()).filter(Boolean) : v; });
      ans.chargers[`charger${j + 1}`] = { brand: a.brand[j], max_a: a.max_a[j], entities: ent, ...((this._chg[j] || {}).device ? { device: this._chg[j].device } : {}) };
    }
    for (let j = 0; j < n; j++) {
      const c = a.cars[j], car = { name: c.name, capacity: +c.capacity };
      if ((f.features || []).includes("car_colour")) car.colour = c.colour;
      if ((f.cars || []).length !== 1 && a.soc[j] !== undefined) car.soc = a.soc[j];
      if (a.how === "two_own") car.charger = `charger${j + 1}`;
      ans.cars[`ev${j + 1}`] = car;
    }
    if (a.how === "two_shared") ans.sharing = { swap_time: a.swap, swap_reminder: a.remind };
    const src = {}; this._srcAsk().forEach((k) => { src[k] = a.src[k] || ""; }); if (a.src.grid_export_sensor) src.grid_export_sensor = a.src.grid_export_sensor; if (Object.keys(src).length) ans.sources = src;
    if (f.hpvc) ans.hpvc = a.hpvc;
    if (a.dynamic && a.price) ans.price = { source: a.price.source, sensor: a.price.sensor };
    return ans;
  }

  async _save() {
    this._busy = true; this._err = {}; this._render();
    let res;
    try { res = await this._hass.callWS(this._addC() ? { type: "hesc_v4/setup/save", answers: { chargers: this._addAnswers().chargers, cars: { ev2: { charger: "charger2" } } }, add_charger: true } : this._add() ? { type: "hesc_v4/setup/save", answers: this._addAnswers(), add_car: true } : { type: "hesc_v4/setup/save", answers: this._answers() }); }
    catch (e) { res = { ok: false, errors: { save: e.message || String(e) } }; }
    this._busy = false;
    if (res && res.ok && this._add()) { this._find = null; this.shadowRoot.innerHTML = `<style>${FS_CSS}</style><ha-card><h3>✓ ${this.t.ready}</h3><p class="sub">${this.t.addReadySub}</p></ha-card>`; window.dispatchEvent(new CustomEvent("hesc-v4-close")); return; }
    if (res && res.ok) {
      this._force = false; this._find = null; this.style.display = "none"; this.shadowRoot.innerHTML = "";
      // decision 11-11-2026: after the first start, the home battery step by step (same menu as in the tile)
      if (window.hv4OpenBatWizPopup) window.hv4OpenBatWizPopup();
      return;
    } // the integration reloads; setup_done turns true
    this._err = res.errors || {}; this._render();
  }
}

if (!customElements.get("hesc-v4-first-start")) customElements.define("hesc-v4-first-start", HescV4FirstStart);
window.customCards = window.customCards || [];
window.customCards.push({ type: "hesc-v4-first-start", name: "HESC v4 · Eerste start", description: "The first start of HESC v4 (shown until it is done)." });
