/* HESC v4 panel cards: the proefbord cards (branch v4/proefbord) as HESC's own panel. Made by
 * tools/panel/make_panel_js.py; element names hesc-v4p-* so the proefbord resource can stay loaded. */
/* ---------- HESC v4 panel in other languages (decision 08-11-2026 16:29: "taal van je Home Assistant-profiel") ----------
 * The panel is written in Dutch. In another profile language the texts in the panel's own elements (hesc-v4*) are
 * translated: the cards' config when the card gets it, and whatever the cards render, as it appears: a whole text
 * (exact), a text with markup (exact on the element's inner HTML), or pieces of a longer text (fragments: whole words,
 * longest first). The table is tools/panel/i18n/panel_texts.yaml (Dutch | English | German per line);
 * make_panel_js.py puts it in HV4_I18N. Dutch profile = nothing changes.
 * German profile = German; every other language = English. For testing: localStorage "hesc-v4-lang" = nl | en | de.
 * Texts that still look Dutch are kept in window.__hv4Miss, so a missing translation is easy to find. */
const HV4_I18N = {"en": {"exact": {"Fasen-overzicht": "Phase overview", "Hoe je zonnestroom over de drie fasen verdeeld is, of elke fase genoeg zon krijgt om je laadpaal te laten starten, en wat je eraan kunt doen.": "How your solar power is spread over the three phases, whether every phase gets enough sun to let your charger start, and what you can do about it.", "Alleen met een thuisbatterij: zo zitten je thuisbatterij(en) en je auto elkaar niet in de weg.": "Only with a home battery: this way your home battery and your car don't get in each other's way.", "Thuisbatterij(en)": "Home battery", "Land": "Country", "Het land van je stroomcontract. Daarna zie je alleen de prijsbronnen van dat land, en de valuta gaat vanzelf goed. Automatisch = het land van Home Assistant.": "The country of your electricity contract. Then you only see the price sources of that country, and the currency is set by itself. Automatic = the country of Home Assistant.", "Waar HESC de stroomprijzen vandaan haalt. Een bron die HESC bij jou vindt staat erbij; bij Eigen sensor met prijslijst kies je de sensor hieronder.": "Where HESC gets the electricity prices. A source HESC finds here is listed; with Own sensor with a price list you pick the sensor below.", "Alleen bij Eigen sensor met prijslijst: de sensor met de prijzen van vandaag en morgen.": "Only with Own sensor with a price list: the sensor with today's and tomorrow's prices.", "De munt van je prijzen. Gaat vanzelf goed als je een land kiest; Automatisch = die van Home Assistant.": "The currency of your prices. Set by itself when you pick a country; Automatic = the one of Home Assistant.", "Nederland": "Netherlands", "België": "Belgium", "Duitsland": "Germany", "Oostenrijk": "Austria", "Frankrijk": "France", "Spanje": "Spain", "Zweden": "Sweden", "Noorwegen": "Norway", "Denemarken": "Denmark", "Verenigd Koninkrijk": "United Kingdom", "Australië": "Australia", "Ander land": "Other country", "Eigen sensor met prijslijst": "Own sensor with a price list", "Hoe je zonnestroom over de drie fasen verdeeld is. Sommige laadpalen starten pas als er op elke fase genoeg zon is; de zwakste fase bepaalt dan wanneer je auto op zon kan laden.": "How your solar power is spread over the three phases. Some chargers only start when every phase has enough sun; the weakest phase then decides when your car can charge on sun.", "Netvermogen fase 1": "Grid power phase 1", "Netvermogen fase 2": "Grid power phase 2", "Netvermogen fase 3": "Grid power phase 3", "Alleen bij 3 fasen. Met het netvermogen per fase meet HESC hoe je zonnestroom over de fasen verdeeld is.": "3 phases only. With the grid power per phase HESC measures how your solar power is spread over the phases.", "alleen deze dag": "this day only", "Opslaan": "Save", "Deze dag uit": "This day off", "Terug naar ritme": "Back to the rhythm", "+ Vakantie": "+ Holiday", "✕ annuleren": "✕ cancel", "Tik de eerste dag van de vakantie": "Tap the first day of the holiday", "Tik nu de laatste dag van de vakantie": "Now tap the last day of the holiday", "Op dit toestel HESC hier openen": "Open HESC here on this device", "Maand": "Month", "Ritme en deze keer": "Rhythm and this time", "Nu": "Now", "Om": "At", "aan": "on", "een": "a", "uit": "off", "van": "from", "zon": "sun", "Auto": "Car", "Jaar": "Year", "accu": "battery", "auto": "car", "geen": "none", "naar": "to", "week": "week", "Dagen": "Days", "Klaar": "Done", "Laadt": "Charges", "Weken": "Weeks", "klaar": "ready", "laadt": "charges", "laden": "charge", "net ±": "grid ±", "stand": "mode", "wacht": "waits", "+ Auto": "+ Car", "Advies": "Advice", "Auto's": "Cars", "Kosten": "Costs", "Morgen": "Tomorrow", "Uitleg": "Guide", "accu %": "battery %", "auto 1": "car 1", "auto 2": "car 2", "bezig…": "busy…", "morgen": "tomorrow", "op zon": "on sun", "stuurt": "controls", "Accu nu": "Battery now", "Je auto": "Your car", "Je huis": "Your house", "Maanden": "Months", "Melding": "Notification", "Per uur": "Per hour", "Prijzen": "Prices", "Rapport": "Report", "Vandaag": "Today", "Vol bij": "Full at", "laadt ·": "charging ·", "nu, tot": "now, to", "vandaag": "today", "· accu": "· battery", ": ik zie": ": I see", "Eén auto": "One car", "Laadpaal": "Charger", "Prijs nu": "Price now", "Vakantie": "Holiday", "klaar om": "ready at", "laadpaal": "charger", "vakantie": "holiday", "vannacht": "tonight", "volgende": "next", "— geen —": "— none —", "⏻ uit ·": "⏻ off ·", "· klaar": "· ready", "<br>accu": "<br>battery", "Annuleren": "Cancel", "Je auto's": "Your cars", "Kan niet:": "Not possible:", "Kwartalen": "Quarters", "Meldingen": "Notifications", "Ontbreekt": "Missing", "Standaard": "Standard", "Thuisaccu": "Home battery", "Uitvoeren": "Run", "alleen nu": "only now", "deze auto": "this car", "deze keer": "this time", "gaat voor": "goes first", "ontbreekt": "missing", "standaard": "standard", "staat aan": "is on", "staat uit": "is off", "+ Laadpaal": "+ Charger", "1 laadpaal": "1 charger", "Alleen zon": "Sun only", "Laadpaal 1": "Charger 1", "Laadpaal 2": "Charger 2", "Laadpaal ·": "Charger ·", "Zon en net": "Sun and grid", "auto laadt": "car charging", "laadpaal 1": "charger 1", "laadpaal 2": "charger 2", "prijs (ct)": "price (ct)", "· klaar om": "· ready at", "Je laadpaal": "Your charger", "Om de beurt": "Taking turns", "Verwijderen": "Remove", "Weerstation": "Weather station", "herinnering": "reminder", "je laadpaal": "your charger", "n ontbreekt": "missing", "net ± 3 kWh": "grid ± 3 kWh", "nog ± 3 kWh": "still ± 3 kWh", "van het net": "from the grid", "weerstation": "weather station", "· deze keer": "· this time", "· geen auto": "· no car", "Instellingen": "Settings", "Je laadpalen": "Your chargers", "Komende week": "Coming week", "Niet gekozen": "Not chosen", "Niet gelukt:": "Failed:", "Nu laden tot": "Charge now to", "Vorige maand": "Previous month", "Weet ik niet": "I don't know", "Zon verwacht": "Expected sun", "alleen {ev1}": "only {ev1}", "alleen {ev2}": "only {ev2}", "laden op zon": "charging on sun", "net ± 13 kWh": "grid ± 13 kWh", "niet gekozen": "not chosen", "nog ± 26 kWh": "still ± 26 kWh", "zon ± 10 kWh": "sun ± 10 kWh", "Accustand van": "Battery level of", "Ja, uitvoeren": "Yes, run", "Laatste actie": "Last action", "Uitleg openen": "Open the guide", "de meeste kWh": "the most kWh", "een stand van": "a mode of", "} verwijderen": "} remove", "· om de beurt": "· taking turns", "Accu nu → doel": "Battery now → goal", "Laatste export": "Last export", "Netvermogen nu": "Grid power now", "Volgende maand": "Next month", "Zon · goedkoop": "Sun · cheap", "Zonnestroom nu": "Solar power now", "morgen ± 7 kWh": "tomorrow ± 7 kWh", "niet gevonden:": "not found:", "Andere laadpaal": "Other charger", "Eco (zon + net)": "Eco (sun + grid)", "Laatste back-up": "Last back-up", "Thuisaccu en EV": "Home battery and EV", "Tik om te typen": "Tap to type", "wacht op schema": "waiting for schedule", "zon verwachting": "solar forecast", "kWh van het net": "kWh from the grid", "+ Auto toevoegen": "+ Add car", "15 minuten later": "15 minutes later", "Accustand-sensor": "Battery level sensor", "Auto laadt vanaf": "Car charges from", "Bewaren of delen": "Keep or share", "De accu gaat van": "The battery goes from", "Langste vrijgave": "Longest release", "Verwachte kosten": "Expected cost", "niet aangesloten": "not plugged in", "15 minuten eerder": "15 minutes earlier", "Advies bijgewerkt": "Advice updated", "Ik weet het zeker": "I'm sure", "Kies een telefoon": "Choose a phone", "Vandaag en morgen": "Today and tomorrow", "laden van het net": "charging from the grid", "vandaag en morgen": "today and tomorrow", "· met herinnering": "· with reminder", "(alleen deze keer)": "(this time only)", "Herinnering sturen": "Send reminder", "Hoe laad je thuis?": "How do you charge at home?", "Kickstarts per dag": "Kickstarts per day", "Rapport en back-up": "Report and back-up", "Start bij zonlicht": "Start at sunlight", "Tijden en vrijgave": "Times and release", "Tik om te wijzigen": "Tap to change", "op zijn vroegst om": "at the earliest at", "○ niet aangesloten": "○ not plugged in", "✕ terug naar ritme": "✕ back to rhythm", "✕ vakantie stoppen": "✕ stop holiday", "· wacht op de auto": "· waiting for the car", "Anoniem om te delen": "Anonymous to share", "Auto's en laadpalen": "Cars and chargers", "HESC aanzetten voor": "Switch HESC on for", "HESC laadt opnieuw…": "HESC reloads…", "HESC uitzetten voor": "Switch HESC off for", "Hij is aangesloten.": "It is plugged in.", "Ja, ik wil nu laden": "Yes, I want to charge now", "Meldingen gaan naar": "Notifications go to", "Wachten op laadpaal": "Waiting for charger", "geen lading gepland": "no charge planned", "installeer eerst de": "first install the", "ja, met verwachting": "yes, with forecast", "· vandaag en morgen": "· today and tomorrow", "— kies een sensor —": "— choose a sensor —", "<b>Echt</b> · 1 auto": "<b>Real</b> · 1 car", "Afkoelen na vrijgave": "Cool-down after release", "Gemiddelde laadprijs": "Average charging price", "HESC stuurt laadpaal": "HESC controls charger", "Verwacht vermogen nu": "Expected power now", "Verwachte laadkosten": "Expected charging cost", "evcc (elke laadpaal)": "evcc (any charger)", "geen netblok gepland": "no grid block planned", "heb je zonnepanelen?": "do you have solar panels?", "tik om aan te zetten": "tap to switch on", "tik om uit te zetten": "tap to switch off", "= wat HESC zou kiezen": "= what HESC would choose", "Aan/uit in de grafiek": "On/off in the chart", "Stabiel vóór vrijgave": "Stable before release", "Start bij verwachting": "Start at forecast", "Zonverwachting morgen": "Solar forecast tomorrow", "geen netladen gepland": "no grid charging planned", "laadt op zon · 3,7 kW": "charging on sun · 3.7 kW", "<b>Demo</b> · 2 auto's": "<b>Demo</b> · 2 cars", "Advies over de laatste": "Advice over the last", "Doorladen bij zonlicht": "Keep charging at sunlight", "Laadvermogen (W of kW)": "Charging power (W or kW)", ", de rest gratis op zon": ", the rest free on sun", "HPVC aan/uit-schakelaar": "HPVC on/off switch", "geldt voor beide auto's": "applies to both cars", "gestreept = van het net": "striped = from the grid", "· daarna weer het ritme": "· then back to the rhythm", "Hij is niet aangesloten.": "It is not plugged in.", "Ja, ik wil dit aanzetten": "Yes, I want to switch this on", "Ja, ik wil dit uitzetten": "Yes, I want to switch this off", "Kort voor een bugmelding": "Short, for a bug report", "Laadvermogen van het net": "Charging power from the grid", "Min. sessies voor advies": "Min. sessions for advice", "Prijslijst in een sensor": "Price list in a sensor", "kies het doel, dan Start": "choose the goal, then Start", "laadt nu van het net tot": "charging from the grid now to", "wacht op zon (Eco-Smart)": "waiting for sun (Eco-Smart)", "Deze auto kent HESC niet.": "HESC does not know this car.", "Doorladen bij verwachting": "Keep charging at forecast", "Geadviseerde startdrempel": "Advised start threshold", "Melding: niet aangesloten": "Notification: not plugged in", "Twee auto's, één laadpaal": "Two cars, one charger", "Zon: starten en doorladen": "Sun: start and keep charging", ": integratie niet gevonden": ": integration not found", "Er is geen laden gepland.": "No charging planned.", "Min. zon over voor de auto": "Min. sun left for the car", "Mislukte vrijgaven per dag": "Failed releases per day", "Verwachte laadkosten samen": "Expected charging cost together", "leeg · tik om in te vullen": "empty · tap to fill in", "Nee, HESC werkt op zichzelf": "No, HESC works on its own", "kabel omzetten uiterlijk om": "swap the cable at the latest at", "kandidaten, kies degene die": "candidates, choose the one that", "typ de waarde, bijv. 0,1116": "type the value, e.g. 0.1116", "1,9 kW overschot · gaat naar": "1.9 kW surplus · goes to", "Eerstvolgende keer overslaan": "Skip next time", "Eindcontrole vóór klaar-tijd": "Final check before ready time", "Wat wil je bewaren of delen?": "What do you want to keep or share?", "geen zonverwachting gevonden": "no solar forecast found", "Deze laadpaal kent HESC niet.": "HESC does not know this charger.", "nog niets van het net gepland": "nothing planned from the grid yet", "Vol vermogen (geen zonnestand)": "Full power (no solar mode)", "Waar komen je prijzen vandaan?": "Where do your prices come from?", "aangesloten, auto vraagt niets": "plugged in, car asks for nothing", "het accu-% van deze auto geeft": "gives this car's battery %", "waar komen je prijzen vandaan?": "where do your prices come from?", "De aan/uit-schakelaar van HPVC.": "HPVC's on/off switch.", "HESC kijkt wat er weg zou gaan…": "HESC checks what would go…", "Instelscherm van Home Assistant": "Home Assistant settings screen", "Klaar! HESC v4 gaat aan de slag.": "Done! HESC v4 gets to work.", "Laden als de stroom goedkoop is.": "Charge when power is cheap.", "om de beurt, jij zet de kabel om": "taking turns, you swap the cable", "04:00–04:45 van het net (± 3 kWh)": "04:00–04:45 from the grid (± 3 kWh)", "Geen geschikte sensoren gevonden.": "No suitable sensors found.", "heb je dynamische energieprijzen?": "do you have dynamic energy prices?", "Je andere auto merkt er niets van.": "Your other car won't notice.", "taal van je Home Assistant-profiel": "language of your Home Assistant profile", "De uitleg van HESC, in gewone taal.": "HESC's guide, in plain language.", "Eerstvolgende keer andere tijd of %": "Other time or % next time", "Niet nodig: er laadt maar één auto.": "Not needed: only one car charges.", "Twee auto's, elk een eigen laadpaal": "Two cars, each with its own charger", "Vink per thuisaccu één sensor aan ·": "Tick one sensor per home battery ·", "Zonverwachting en realisatie · auto": "Solar forecast and actual · car", "Hoeveel je zonnepanelen nu opwekken.": "How much your solar panels produce now.", "Verwachting laadmogelijkheden op zon": "Expected charging on sun", "Verwijderd. HESC laadt zich opnieuw.": "Removed. HESC reloads.", "Alleen auto 2 kan weg; auto 1 blijft.": "Only car 2 can go; car 1 stays.", "Verwachting-attribuut (leeg = waarde)": "Forecast attribute (empty = value)", "Zonverwachting vandaag (per half uur)": "Solar forecast today (per half hour)", "HESC houdt auto 1 en laadpaal 1 altijd": "HESC always keeps car 1 and charger 1", "Hoe lang een vrijgave hoogstens duurt.": "How long a release lasts at most.", "Netvermogen (negatief = teruglevering)": "Grid power (negative = export)", "Staat in de specificaties van je auto.": "It's in your car's specifications.", "de prijzen van vandaag en morgen heeft": "has today's and tomorrow's prices", "heeft panelen vrijgegeven voor de auto": "has released panels for the car", "· voorbeeld, er wordt niets opgeslagen": "· example, nothing is saved", "Alleen als je Home PV Control gebruikt.": "Only if you use Home PV Control.", "Schaduwmodus (rekent mee, stuurt niets)": "Shadow mode (calculates along, controls nothing)", "geen sensor voor zonnevermogen gevonden": "no sensor for solar power found", "De startdrempel die het advies aanraadt.": "The start threshold the advice recommends.", "Deze HESC-versie kan nog niets weghalen.": "This HESC version cannot remove anything yet.", "Planning, laadkosten en instellingen van": "Planning, charging costs and settings of", "Waar HESC zon, net en verwachting leest.": "Where HESC reads sun, grid and forecast.", "het totale vermogen van je panelen geeft": "gives the total power of your panels", "krijg je een herinnering op je telefoon.": "you get a reminder on your phone.", "Hoeveel de laadpaal nu laadt, in W of kW.": "How much the charger is charging now, in W or kW.", "Dashboardpatroon — knoppenrij met vensters": "Dashboard pattern — row of buttons with windows", "De zonverwachting van morgen per half uur.": "Tomorrow's solar forecast per half hour.", "Auto aangesloten (aan/uit- of statussensor)": "Car plugged in (on/off or status sensor)", "Boven dit vermogen telt de auto als ladend.": "Above this power the car counts as charging.", "maximum dat de installateur heeft ingesteld": "maximum set by the installer", "s laden aan dezelfde laadpaal. De auto die": "s charging at the same charger. The car that", "Het verwachte zonvermogen over een half uur.": "The expected solar power in half an hour.", "Je HESC-instellingen bewaren en terugzetten.": "Keep and restore your HESC settings.", "Start/stop-schakelaar laadpaal (aan = laden)": "Charger start/stop switch (on = charging)", "Alleen laadpaal 2 kan weg; laadpaal 1 blijft.": "Only charger 2 can go; charger 1 stays.", "Waarde(n) voor laden op zon, komma-gescheiden": "Value(s) for charging on sun, comma-separated", "afname en teruglevering van het hele huis meet": "measures the whole house's import and export", "gaat voor: beide moeten wo 07:30 klaar zijn en": "goes first: both must be ready Wed 07:30 and", "zon genoeg · prijs onder je goedkope-kansprijs": "enough sun · price below your cheap-chance price", "Hoeveel kWh je thuisaccu’s samen kunnen opslaan.": "How many kWh your home batteries can store together.", "Je hebt in dit venster nog geen back-up gemaakt.": "You haven't made a back-up in this window yet.", "Zonne-energieteller (kWh van zon in het rapport)": "Solar energy meter (kWh from sun in the report)", "de verwachting geeft (Solcast of Forecast.Solar)": "gives the forecast (Solcast or Forecast.Solar)", "Pas na zoveel zonnesessies geeft HESC een advies.": "HESC only gives advice after this many solar sessions.", "Terug naar zonnestand (Wallbox: schema hervatten)": "Back to solar mode (Wallbox: resume schedule)", "Wanneer het advies voor het laatst is bijgewerkt.": "When the advice was last updated.", "Zet de instellingen uit de laatste back-up terug.": "Restore the settings from the last back-up.", "Zonder namen en codes. Bovenaan staat wat je deelt.": "Without names and codes. What you share is at the top.", "Hoe lang HESC na een vrijgave wacht voor een nieuwe.": "How long HESC waits after a release before a new one.", "Hij is nog niet aangesloten: steek de kabel erin vóór": "It is not plugged in yet: plug it in before", "geen netmeter gevonden (bijv. P1 / DSMR / HomeWizard)": "no grid meter found (e.g. P1 / DSMR / HomeWizard)", "wordt opgeslagen · HESC laadt opnieuw (± half minuut)": "being saved · HESC reloads (± half a minute)", "Aan als je Home PV Control gebruikt. Zonder HPVC: uit.": "On if you use Home PV Control. Without HPVC: off.", "heb je een load balancer die het huisverbruik meeneemt?": "do you have a load balancer that includes the house's use?", "Alles, ook namen. Om zelf te bewaren of terug te zetten.": "Everything, names too. To keep yourself or to restore.", "Een ✓ betekent dat HESC die bron in Home Assistant vond.": "A ✓ means HESC found that source in Home Assistant.", "Wat je slimme meter nu meet. Negatief = je levert terug.": "What your smart meter measures now. Negative = you export.", "Weet je het zeker? Dit kan niet ongedaan worden gemaakt.": "Are you sure? This cannot be undone.", "kies straks bij Instellingen de sensor met de prijslijst": "choose the sensor with the price list in Settings later", "· HESC zoekt laadvermogen, aangesloten en laadstand zelf": "· HESC finds charging power, plugged in and charging mode itself", "€ 0,231 /kWh · goedkoopst vannacht 02:15–04:00 (€ 0,171)": "€ 0.231 /kWh · cheapest tonight 02:15–04:00 (€ 0.171)", "<b>Komt in v4: het rapport maakt de v4-integratie.</b> ·": "<b>Coming in v4: the v4 integration makes the report.</b> ·", "De naam komt uit Home Assistant; pas hem aan als je wilt.": "The name comes from Home Assistant; change it if you like.", "Geen prijzen ontvangen: HESC kan nu niet plannen op prijs.": "No prices received: HESC cannot plan on price now.", "Binnen hoeveel uur de minimale accustand bereikt moet zijn.": "Within how many hours the minimum battery level must be reached.", "Het verwachte zonvermogen van nu, bijvoorbeeld van Solcast.": "The expected solar power right now, e.g. from Solcast.", "Welke laadstand(en) van je laadpaal laden op zon betekenen.": "Which mode(s) of your charger mean charging on sun.", "dan weer laden op zon en goedkope uren volgens de planning.": "then charging on sun and cheap hours again as planned.", "Boven dit verwachte zonvermogen begint HESC op zon te laden.": "Above this expected solar power HESC starts charging on sun.", "De sensor van HPVC die zegt of hij de zonnepanelen begrenst.": "HPVC's sensor that says whether it limits the solar panels.", "Statuswaarden voor \"geen auto\" (alleen bij een statussensor)": "Status values for \"no car\" (status sensor only)", "✓ Alles gevonden. Dit scherm wordt in het echt overgeslagen.": "✓ Everything found. In real life this screen is skipped.", "De munt van je prijzen. Automatisch = die van Home Assistant.": "The currency of your prices. Automatic = Home Assistant's.", "Het merk, en wat de installateur als maximum heeft ingesteld.": "The brand, and the maximum the installer has set.", "Hoe lang de laadpaal gestopt moet zijn voordat HESC terugzet.": "How long the charger must be stopped before HESC switches back.", "Hoe vaak per dag HESC de laadpaal hoogstens een duwtje geeft.": "How often a day HESC gives the charger a nudge at most.", "Aan: HESC neemt het advies zelf over. Uit: je ziet het alleen.": "On: HESC adopts the advice itself. Off: you only see it.", "dan met rust: geen planning, niet pauzeren of hervatten. Heeft": "then alone: no planning, no pausing or resuming. If", "HESC v4 start in schaduwmodus: het kijkt mee en schakelt niets.": "HESC v4 starts in shadow mode: it watches and switches nothing.", "Hoe lang HESC wacht tot de laadpaal na de vrijgave echt begint.": "How long HESC waits for the charger to really start after the release.", "Over hoeveel dagen HESC je laadsessies bekijkt voor het advies.": "Over how many days HESC looks at your charging sessions for the advice.", "Wanneer de laatste back-up van je HESC-instellingen is gemaakt.": "When the last back-up of your HESC settings was made.", "Wat het advies nu zegt, of hoeveel sessies het nog nodig heeft.": "What the advice says now, or how many sessions it still needs.", "Kabel wisselen is niet nodig: elke auto heeft een eigen laadpaal.": "No need to swap the cable: each car has its own charger.", "Samenvatting in het Engels, om in een issue op GitHub te plakken.": "Summary in English, to paste in an issue on GitHub.", "12:30–16:30 op zon (± 10 kWh) · 02:15–04:00 van het net (± 13 kWh)": "12:30–16:30 on sun (± 10 kWh) · 02:15–04:00 from the grid (± 13 kWh)", "Of HESC op 1 of 3 fasen zou moeten laden, als je laadpaal dat kan.": "Whether HESC should charge on 1 or 3 phases, if your charger can.", "Herinnering op je telefoon als het tijd is om de kabel om te zetten": "Reminder on your phone when it's time to swap the cable", "Op of onder deze prijs per kWh telt een kwartier als goedkope kans.": "At or below this price per kWh a quarter counts as a cheap chance.", "De teller van de laadpaal voor energie uit de zon, voor het rapport.": "The charger's meter for energy from the sun, for the report.", "HESC maakt eerst zelf een back-up; die kun je hierboven terugzetten.": "HESC first makes a back-up itself; you can restore it above.", "Hoe lang de zon even mag wegvallen (een wolk) zonder dat HESC stopt.": "How long the sun may drop out (a cloud) without HESC stopping.", "Onder dit zonlicht stopt HESC weer (alleen met het weerstation aan).": "Below this sunlight HESC stops again (only with the weather station on).", "HESC gaat dan weer laden op zon en goedkope uren volgens je planning.": "HESC then charges on sun and cheap hours again as planned.", "Hoe geduldig HESC is. De standaardwaarden werken voor de meeste huizen.": "How patient HESC is. The defaults work for most homes.", "Dit kon HESC niet (zeker) vinden. Kies het zelf; de rest is al ingevuld.": "HESC couldn't find this (for sure). Choose it yourself; the rest is filled in.", "Onder dit % laadt HESC de auto meteen bij, in de goedkoopste kwartieren.": "Below this % HESC tops up the car right away, in the cheapest quarters.", "Boven dit zonlicht begint HESC te laden (alleen met het weerstation aan).": "Above this sunlight HESC starts charging (only with the weather station on).", "De bestanden van deze auto blijven bewaard (hernoemd), niets wordt gewist.": "This car's files are kept (renamed), nothing is deleted.", "HESC vraagt straks zelf naar het laadvermogen, aangesloten en de laadstand": "HESC will ask for the charging power, plugged in and the charging mode itself", "HESC kijkt naar je eigen laadsessies en stelt een betere startdrempel voor.": "HESC looks at your own charging sessions and suggests a better start threshold.", "Netsensor: teruglevering positief (uit = afname positief, de meeste meters)": "Grid sensor: export positive (off = import positive, most meters)", "Prijzen per uur of per kwartier. Automatisch = zoals je prijsbron ze geeft.": "Prices per hour or per quarter. Automatic = as your price source gives them.", "Bewaart al je HESC-instellingen in Home Assistant, plus een kopie met datum.": "Saves all your HESC settings in Home Assistant, plus a dated copy.", "De sensor waaruit HESC het % van je auto leest. Tik om een andere te kiezen.": "The sensor HESC reads your car's % from. Tap to choose another.", "Hoe lang de zon stabiel genoeg moet zijn voordat HESC de laadpaal vrijgeeft.": "How long the sun must be stable enough before HESC releases the charger.", "Na zoveel mislukte vrijgaven op een dag probeert HESC het die dag niet meer.": "After this many failed releases in a day HESC stops trying that day.", "Voorbeeld: de auto's en laadtijden zijn verzonnen, prijzen en zon zijn echt.": "Example: the cars and charging times are invented, prices and sun are real.", "Tot hoeveel % HESC de auto als vol rekent. Vaak 80 %; bij een LFP-accu 100 %.": "Up to what % HESC counts the car as full. Often 80 %; with an LFP battery 100 %.", "De stand (%) van je thuisaccu(s). Per accu één sensor, of één voor alle samen.": "The level (%) of your home battery(s). One sensor per battery, or one for all together.", "De zonverwachting van vandaag per half uur. HESC plant daarmee het laden op zon.": "Today's solar forecast per half hour. HESC uses it to plan charging on sun.", "Aan: HESC leest zonnestroom en netvermogen uit HPVC in plaats van uit Zon en net.": "On: HESC reads solar power and grid power from HPVC instead of from Sun and grid.", "Alleen met een thuisaccu: zo zitten je thuisaccu en je auto elkaar niet in de weg.": "Only with a home battery: so your home battery and your car don't get in each other's way.", "Bijvoorbeeld Wallbox Power Boost, of een laadpaal die via de slimme meter meekijkt.": "For example Wallbox Power Boost, or a charger that watches via the smart meter.", "Alleen bij Prijslijst in een sensor: de sensor met de prijzen van vandaag en morgen.": "Only with Price list in a sensor: the sensor with today's and tomorrow's prices.", "vannacht van 01:45 tot 02:00, van 03:00 tot 03:15 en van 04:45 tot 05:00 van het net": "tonight from 01:45 to 02:00, from 03:00 to 03:15 and from 04:45 to 05:00 from the grid", "Zon verwacht tegen werkelijk, en wanneer de auto met behulp van zonne-energie kan laden.": "Expected sun against actual, and when the car can charge with solar energy.", "De sensor van je weerstation die het zonlicht meet, in W/m². Tik om een andere te kiezen.": "Your weather station's sensor that measures sunlight, in W/m². Tap to choose another.", "Voor laadpalen die iets extra nodig hebben. Bij de meeste laadpalen vult HESC dit zelf in.": "For chargers that need something extra. For most chargers HESC fills this in itself.", "Maakt het laadrapport opnieuw met de gegevens van nu. Daarna verschijnt Laadrapport openen.": "Makes the charging report again with today's data. Then Open charging report appears.", "De schakelaar waarmee HESC de laadpaal laat laden of pauzeren. Nodig om van het net te laden.": "The switch HESC uses to let the charger charge or pause. Needed to charge from the grid.", "Een extra schakelaar die sommige laadpalen nodig hebben om op zon te laden (go-e, Wattpilot).": "An extra switch some chargers need to charge on sun (go-e, Wattpilot).", "Telt je meter teruglevering als positief? Zet dit dan aan. De meeste meters doen het andersom.": "Does your meter count export as positive? Then switch this on. Most meters do the opposite.", "HPVC gevonden. HPVC regelt je zonnepanelen bij negatieve prijzen. Zal HESC daarmee samenwerken?": "HPVC found. HPVC controls your solar panels at negative prices. Should HESC work with it?", "Hoeveel zon er vandaag minstens over moet blijven voor de auto voordat HESC een kickstart doet.": "How much sun must at least be left for the car today before HESC does a kickstart.", "Het merk van je laadpaal. Daarmee zoekt HESC zelf de schakelaars en sensoren van de laadpaal op.": "Your charger's brand. HESC uses it to find the charger's switches and sensors itself.", "Zet de instellingen uit de back-up terug. Welke back-up hij gebruikt, staat bij Laatste back-up.": "Restore the settings from the back-up. Which back-up it uses is shown at Last back-up.", "Aan: de startdrempel past zich aan de tijd van het jaar aan (in de winter lager dan in de zomer).": "On: the start threshold follows the time of year (lower in winter than in summer).", "Met hoeveel kW HESC rekent als hij van het net laadt. Bepaalt hoeveel kwartieren hij nodig heeft.": "How many kW HESC uses when it charges from the grid. Sets how many quarters it needs.", "Waar de zonverwachting vandaan komt, bijvoorbeeld Solcast of Forecast.Solar. HESC kiest dit zelf.": "Where the solar forecast comes from, e.g. Solcast or Forecast.Solar. HESC chooses this itself.", "Bewaart al je HESC-instellingen in Home Assistant (map hesc_v3), plus een kopie met datum en tijd.": "Saves all your HESC settings in Home Assistant (folder hesc_v3), plus a copy with date and time.", "De laadstand van je laadpaal (bijvoorbeeld zon, eco of direct). HESC zet hem op zon en weer terug.": "Your charger's charging mode (e.g. sun, eco or direct). HESC switches it to sun and back.", "Welke statuswaarden betekenen dat er geen auto aan de laadpaal hangt. Alleen bij een statussensor.": "Which status values mean no car is connected to the charger. Status sensor only.", "De knop die de laadpaal na het netladen terugzet naar laden op zon (bij Wallbox: schema hervatten).": "The button that sets the charger back to charging on sun after grid charging (Wallbox: resume schedule).", "Geen: HESC schat het zelf. Je kunt de accustand ook zelf invullen op de startpagina of je telefoon.": "None: HESC estimates it itself. You can also enter the battery level yourself on the start page or your phone.", "Waaruit HESC ziet of de auto aan de laadpaal hangt: een aan/uit-sensor of de status van de laadpaal.": "How HESC sees whether the car is connected: an on/off sensor or the charger's status.", "Aan: vindt HESC een betere sensor dan de gekozen, dan neemt hij die zelf. Uit: je keuze blijft staan.": "On: if HESC finds a better sensor than the chosen one, it takes it. Off: your choice stays.", "Het vermogen van je thuisaccu(s). + = laden. Per accu één sensor, of één totaal-sensor; niet allebei.": "Your home battery(s) power. + = charging. One sensor per battery, or one total sensor; not both.", "Aan: HESC laadt ook buiten je planning als de stroom goedkoop is, tenzij de zon het later die dag dekt.": "On: HESC also charges outside your planning when power is cheap, unless the sun covers it later that day.", "Let op: de totaal-sensor telt andersom dan de losse accu's. HESC rekent met + = laden; kijk welke klopt.": "Note: the total sensor counts the other way round from the single batteries. HESC uses + = charging; check which is right.", "Zoveel minuten voor de klaar-tijd kijkt HESC nog één keer of de auto het doel haalt, en laadt anders bij.": "This many minutes before the ready time HESC checks once more whether the car reaches its goal, and tops up if not.", "Standaard: wat je af en toe wilt bijstellen, zoals meldingen, goedkope kansen, de thuisaccu en de back-up.": "Standard: what you want to adjust now and then, like notifications, cheap chances, the home battery and the back-up.", "Aan: komt de auto thuis met minder dan de minimale accustand, dan laadt HESC hem eerst snel tot dat niveau.": "On: if the car comes home below the minimum battery level, HESC first charges it quickly to that level.", "Hoeveel kWh je auto echt kan laden (staat in de handleiding). HESC leest het uit de auto als die het meldt.": "How many kWh your car can really charge (see the manual). HESC reads it from the car if the car reports it.", "De stand van je laadpaal die nu laden betekent. Alleen nodig als je laadpaal geen start/stop-schakelaar heeft.": "The charger mode that means charging now. Only needed if your charger has no start/stop switch.", "HESC stuurt dan niets meer aan: de laadpaal laadt zoals hij zelf staat ingesteld, zonder zon- of prijsplanning.": "HESC then controls nothing: the charger charges as it is set itself, without sun or price planning.", "Weet je het niet, laat dan 16 A staan. Bij Easee, Peblar en Wallbox leest HESC dit straks zelf uit de laadpaal.": "If you don't know, leave it at 16 A. With Easee, Peblar and Wallbox HESC will read it from the charger itself.", "Zet de afstelling terug: drempels, tijden, advies en eindcontrole. Sensoren, doelen, prijzen en kosten blijven.": "Restore the tuning: thresholds, times, advice and final check. Sensors, goals, prices and costs stay.", "Expert: laadregels, HPVC, weerstation, advies en kickstart. Zelden nodig; wie het simpel houdt, komt hier nooit.": "Expert: charging rules, HPVC, weather station, advice and kickstart. Rarely needed; keep it simple and you never come here.", "Onder dit verwachte zonvermogen stopt HESC weer. Iets lager dan de start, zodat hij niet steeds aan en uit gaat.": "Below this expected solar power HESC stops again. A bit lower than the start, so it doesn't keep switching on and off.", "Zoekt de sensoren en schakelaars van je laadpaal opnieuw op, bijvoorbeeld na een update van de laadpaal-integratie.": "Finds your charger's sensors and switches again, e.g. after an update of the charger integration.", "Alleen nodig als de verwachting in een attribuut van de sensor staat (bijvoorbeeld estimate10). Leeg = de waarde zelf.": "Only needed if the forecast is in an attribute of the sensor (e.g. estimate10). Empty = the value itself.", "Aan: HESC zorgt dat je thuisaccu en je auto elkaar niet in de weg zitten (kickstart en pauze). Alleen met een thuisaccu.": "On: HESC makes sure your home battery and your car don't get in each other's way (kickstart and pause). Only with a home battery.", "Welke sensoren en schakelaars van je laadpaal HESC gebruikt. Meestal vindt HESC ze zelf; voorstel is wat HESC het best vindt.": "Which sensors and switches of your charger HESC uses. Usually HESC finds them itself; suggestion is what HESC thinks is best.", "een eigen laadpaal, dan laat HESC die ook met rust. Een andere auto gaat gewoon door, ook als die dezelfde laadpaal gebruikt.": "its own charger, HESC leaves that alone too. Another car just carries on, even if it uses the same charger.", "Het rapport opent in een nieuw tabblad. Met \"Rapport downloaden\" bewaar je het als één bestand; daarin zitten ook de gegevens.": "The report opens in a new tab. With \"Download report\" you keep it as one file; it contains the data too.", "Kies de maand of het jaar. Bij twee auto's zie je het totaal en per auto een regel; de balkjes per dag in de kleur van de auto.": "Choose the month or the year. With two cars you see the total and a line per car; the bars per day in the car's colour.", ": het kijkt mee en schakelt niets. Zet hem aan op de startpagina als je zover bent. Alles kun je later wijzigen bij Instellingen.": ": it watches and switches nothing. Switch it on on the start page when you're ready. You can change everything later in Settings.", "Maakt eerst een back-up en zet dan alleen de afstelling terug (drempels, tijden, advies). Sensoren, doelen, prijzen en kosten blijven.": "First makes a back-up, then restores only the tuning (thresholds, times, advice). Sensors, goals, prices and costs stay.", "Waar HESC de stroomprijzen vandaan haalt. De meeste bronnen vindt HESC zelf; bij Prijslijst in een sensor kies je de sensor hieronder.": "Where HESC gets the power prices. HESC finds most sources itself; with Price list in a sensor you choose the sensor below.", "Je auto: hoe groot de accu is, wanneer hij vol is en of hij een minimumlading krijgt. Het labeltje ⏻ zet HESC voor deze auto aan of uit.": "Your car: how big the battery is, when it's full and whether it gets a minimum charge. The ⏻ tag switches HESC on or off for this car.", "Beide auto's laden aan dezelfde laadpaal. De auto die 's avonds aan de paal hangt laadt eerst; de andere nadat jij de kabel hebt omgezet.": "Both cars charge at the same charger. The car on the charger in the evening charges first; the other after you have swapped the cable.", "Een export van je HESC zelf: instellingen, planning en wat HESC geleerd heeft. Om te bewaren, te delen op een forum of bij een foutmelding.": "An export of your HESC itself: settings, planning and what HESC has learned. To keep, to share on a forum or with a bug report.", "Basis: wat elke installatie nodig heeft: je laadpaal, je auto('s), de prijzen en HESC aan/uit. Meestal vult de eerste start dit al voor je in.": "Basis: what every installation needs: your charger, your car(s), the prices and HESC on/off. The first start usually fills this in for you.", "Wanneer HESC op zon begint en blijft laden: op de verwachting, en als je wilt ook op je eigen weerstation. Het advies kan deze drempels voor je bijstellen.": "When HESC starts and keeps charging on sun: on the forecast, and if you like on your own weather station too. The advice can adjust these thresholds for you.", "HESC laadt de auto dan meteen van het net, ook als stroom nu duur is of er geen zon is, tot de accu op dit doel staat. Je planning wacht zolang. Stoppen kan altijd.": "HESC then charges the car from the grid right away, even if power is expensive now or there is no sun, until the battery reaches this goal. Your planning waits until then. You can always stop.", "Heb je een eigen weerstation met een zonlichtsensor (W/m²)? Dan kan HESC starten op het zonlicht dat nu echt valt, in plaats van alleen op de verwachting. Uit = alleen de verwachting.": "Do you have your own weather station with a sunlight sensor (W/m²)? Then HESC can start on the sunlight that really falls now, instead of only on the forecast. Off = forecast only.", "Hoe ging het laden op zon: een samenvatting, het advies, een overzicht per dag, hoe betrouwbaar je sensoren waren en hoe goed de zonverwachting klopte. Om te begrijpen wat HESC gedaan heeft.": "How charging on sun went: a summary, the advice, an overview per day, how reliable your sensors were and how well the solar forecast matched. To understand what HESC did.", "HESC houdt hiermee het laden binnen de aansluiting als comfort. Jij blijft verantwoordelijk dat je elektrische installatie niet overbelast raakt; dat regelen laadpaal, load balancer en installateur.": "HESC uses this to keep charging within the connection, as comfort. You remain responsible that your electrical installation isn't overloaded; the charger, load balancer and installer take care of that.", "Een herinnering op je telefoon als de auto 's avonds niet aan de laadpaal hangt terwijl er morgen geladen moet worden. Kies hoe laat. De melding gaat naar de telefoons bij Instellingen › Standaard › Meldingen.": "A reminder on your phone when the car isn't on the charger in the evening while it has to charge tomorrow. Choose the time. The notification goes to the phones at Settings › Standard › Notifications.", "De komende zeven dagen per auto: accu-% en klaar-tijd. Tik op een auto of een dag om die auto te plannen.\\n\\nOranje rand = uitzondering: alleen deze keer, overgeslagen of een dag uit. Vette tekst = dag met eigen tijd of %.": "The next seven days per car: battery % and ready time. Tap a car or a day to plan that car.\\n\\nOrange border = exception: this time only, skipped or a day off. Bold text = day with its own time or %.", "Welke telefoons HESC-meldingen krijgen (alle apparaten met de Home Assistant-app staan erbij). Testmelding: probeer het uit. Ochtendoverzicht: één bericht per dag met de accustand, het volgende plan, de zon vandaag en gisteren.": "Which phones get HESC notifications (all devices with the Home Assistant app are listed). Test notification: try it out. Morning overview: one message a day with the battery level, the next plan, today's and yesterday's sun.", "Het vaste ritme van deze auto. Kies één standaard (klaar om, accu-%) en zet per weekdag aan of uit.\\n\\nTik op een dag om die dag aan of uit te zetten, of een eigen tijd of % te geven. Een dag met eigen waarden heeft vette tekst.": "This car's fixed rhythm. Choose one standard (ready at, battery %) and switch each weekday on or off.\\n\\nTap a day to switch it on or off, or give it its own time or %. A day with its own values has bold text.", "Hoe HESC de kosten rekent. **Waarde van een kWh zon:** wat je misloopt aan terugleververgoeding (0 = zon is gratis). Is de prijs uit je prijsbron al **all-in** (belasting, opslag, btw), zet dat aan; anders vul je opslag en btw in. Een wijziging rekent de hele geschiedenis opnieuw.": "How HESC calculates the costs. **Value of a kWh of sun:** what you miss in export compensation (0 = sun is free). If the price from your price source is already **all-in** (tax, surcharge, VAT), switch that on; otherwise fill in surcharge and VAT. A change recalculates the whole history.", "**HESC aan/uit** is de hoofdschakelaar: uit = HESC doet helemaal niets. **Schaduwmodus** aan = HESC rekent en plant gewoon mee en laat zien wat hij zou doen, maar stuurt de laadpaal niet aan. Handig om eerst te kijken. Dezelfde schaduwmodus zit ook in de knop Live · stuurt bovenaan.": "**HESC on/off** is the main switch: off = HESC does nothing at all. **Shadow mode** on = HESC calculates and plans along and shows what it would do, but doesn't control the charger. Handy to watch first. The same shadow mode is also in the Live · controls button at the top.", "Wie gaat voor en waarom.\\n\\n- Moeten beide op dezelfde tijd klaar zijn, dan gaat de auto voor die de meeste kWh nodig heeft.\\n- Zelfde tijd en zelfde kWh: de eerste auto gaat voor.\\n- Wisselen gebeurt alleen op een heel kwartier.\\n- **(geschat)** betekent: de accustand van die auto meldt niets, HESC rekent met een schatting.": "Who goes first and why.\\n\\n- If both must be ready at the same time, the car needing the most kWh goes first.\\n- Same time and same kWh: the first car goes first.\\n- Swapping only happens on a full quarter.\\n- **(estimated)** means: that car's battery level reports nothing, HESC uses an estimate.", "Wat het laden kostte, per dag, week, maand en jaar, van zon en van het net. **Laadkosten exporteren** (bij Instellen) zet de kosten per dag en per maand in twee spreadsheet-bestanden (CSV) in de map hesc_v4 van Home Assistant, om in Excel te openen. Het **Rapport** (knop bovenaan) is iets anders: een overzicht van je hele HESC, om te bewaren of te delen.": "What charging cost, per day, week, month and year, from sun and from the grid. **Export charging costs** (at Settings) puts the costs per day and per month in two spreadsheet files (CSV) in Home Assistant's hesc_v4 folder, to open in Excel. The **Report** (button at the top) is something else: an overview of your whole HESC, to keep or to share.", "Je auto's en laadpalen. HESC stuurt er maximaal twee van elk. **+ Auto toevoegen:** een tweede auto, op dezelfde laadpaal of met een eigen. **+ Laadpaal toevoegen:** als twee auto's één laadpaal delen, krijgt auto 2 een eigen laadpaal. **Verwijderen** kan alleen voor auto 2 en laadpaal 2; HESC laat eerst zien wat er weggaat. Laadkosten en geschiedenis worden niet gewist maar bewaard.": "Your cars and chargers. HESC controls at most two of each. **+ Add car:** a second car, on the same charger or with its own. **+ Add charger:** when two cars share one charger, car 2 gets its own charger. **Remove** is only possible for car 2 and charger 2; HESC first shows what will go. Charging costs and history are not deleted but kept.", "Een uitzondering voor de eerstvolgende keer. Daarna gaat HESC vanzelf terug naar het ritme. Laagste doel overal 15%: daaronder laadt de auto zijn 12V-accu niet meer bij.\\n\\n- **Overslaan:** de eerstvolgende lading vervalt.\\n- **Andere tijd of %:** alleen voor de eerstvolgende keer.\\n- **Nu laden tot:** laadt meteen, los van zon en prijs.\\n\\nVervangt in v3: plan voor één dag, één dag overslaan en nu laden tot.": "An exception for the next time. After that HESC goes back to the rhythm by itself. Lowest goal everywhere 15%: below that the car no longer charges its 12V battery.\\n\\n- **Skip:** the next charge is dropped.\\n- **Other time or %:** for the next time only.\\n- **Charge now to:** charges right away, regardless of sun and price.\\n\\nReplaces in v3: plan for one day, skip one day and charge now to.", "De maand met het ritme erin. Tik op een dag om hem **uit** te zetten (oranje streep), of een vrije dag **aan** met de standaardwaarden (gestreepte rand). Nog een keer tikken zet de dag terug naar het ritme.\\n\\nZo plan je ploegendienst of een dagje uit vooruit.\\n\\n**Vakantie:** tik op **+ Vakantie**, dan op de eerste en de laatste dag. Met de muis kun je ook van de eerste naar de laatste dag slepen. Al die dagen gaan uit; na de laatste dag gaat het ritme vanzelf verder. Tik in de vakantie of op ✕ om hem te stoppen.\\n\\n**Eén dag aanpassen:** tik twee keer snel op een dag. Dan kies je voor alleen die dag de tijd en de accu %.": "The month with the rhythm in it. Tap a day to switch it **off** (orange stripe), or a free day **on** with the standard values (striped border). Tapping again sets the day back to the rhythm.\\n\\nThis way you plan shift work or a day out ahead.\\n\\n**Holiday:** tap **+ Holiday**, then the first and the last day. With a mouse you can also drag from the first to the last day. All those days go off; after the last day the rhythm carries on by itself. Tap in the holiday or on ✕ to stop it.\\n\\n**Change one day:** tap a day twice quickly. Then you choose the time and battery % for that day only.", "Waar HESC zijn meldingen naartoe stuurt, als lijst van Home Assistant-meldingsdiensten (komma-gescheiden). **In Standaard** kies je met knoppen een telefoon met de Home Assistant-app; dat komt hier vanzelf in te staan. **Hier** kun je daarnaast elke andere meldingsdienst intypen die Home Assistant kent, bijvoorbeeld `notify.telegram`, `notify.email` of een groep van meerdere telefoons. Zo krijg je HESC-meldingen ook buiten de app. Laat je het leeg, dan stuurt HESC geen meldingen.": "Where HESC sends its notifications, as a list of Home Assistant notify services (comma-separated). **In Standard** you choose a phone with the Home Assistant app with buttons; it then appears here by itself. **Here** you can also type any other notify service Home Assistant knows, e.g. `notify.telegram`, `notify.email` or a group of several phones. That way you get HESC notifications outside the app too. Leave it empty and HESC sends no notifications.", "Zonverwachting": "Solar forecast", "Live": "Live", "Periode": "Period", "Periode laadkosten": "Charging cost period", "Instellen": "Set up", "Terugleververgoeding": "Export compensation", "Kosten: prijs is all-in": "Costs: price is all-in", "Kosten: opslag per kWh (energiebelasting + leverancier)": "Costs: surcharge per kWh (energy tax + supplier)", "Kosten: btw": "Costs: VAT", "Laadkosten exporteren": "Export charging costs", "Geladen": "Charged", "Van de zon": "From the sun", "Van het net": "From the grid", "Kosten net": "Grid cost", "Waarde zon (teruglevering)": "Sun value (export)", "Gemiddeld": "Average", "niet geladen": "not charged", "Startdrempel": "Start threshold", "Doorlaaddrempel": "Keep-charging threshold", "Verwacht laden op zon": "Expected charging on sun", "Zon": "Sun", "Verwachting": "Forecast", "Kalender": "Calendar", "Ritme": "Rhythm", "ritme": "rhythm", "extra dag": "extra day", "dag uit": "day off", "vrij": "free", "geweest": "passed", "standaard klaar om": "standard ready at", "standaard accu": "standard battery", "Alleen deze keer": "This time only", "Overslaan": "Skip", "Andere tijd of %": "Other time or %", "Type laadpaal": "Charger type", "Accucapaciteit": "Battery capacity", "Minimumlading": "Minimum charge", "Minimale accustand": "Minimum battery level", "Minimumlading binnen": "Minimum charge within", "Prijsbron": "Price source", "Nord Pool (officieel)": "Nord Pool (official)", "Sensor dagprijzen": "Day prices sensor", "Prijzen per": "Prices per", "Automatisch": "Automatic", "Per kwartier": "Per quarter", "Valuta": "Currency", "HESC staat aan": "HESC is on", "HESC staat uit": "HESC is off", "vast": "fixed", "HESC stuurt maximaal twee auto's.": "HESC controls at most two cars.", "Laadpalen": "Chargers", "HESC stuurt maximaal twee laadpalen.": "HESC controls at most two chargers.", "Basis": "Basic", "Expert": "Expert", "Goedkope kansen": "Cheap chances", "Laadplan: goedkope kansen pakken": "Charge plan: take cheap chances", "Laadplan: prijs voor een goedkope kans": "Charge plan: price for a cheap chance", "Back-up": "Back-up", "in orde": "OK", "✓ in orde": "✓ OK", "Waarde laadstand 'nu laden'": "Charging mode value 'charge now'", "Startdrempel per seizoen": "Start threshold per season", "stabiel": "stable", "HPVC gebruiken": "Use HPVC", "Zonnestroom en net uit HPVC": "Solar power and grid from HPVC", "Advies automatisch toepassen": "Apply advice automatically", "Meldingsdiensten": "Notify services", "Laadrapport": "Charging report", "Laadrapport maken": "Make charging report", "Laadrapport gemaakt": "Charging report made", "Laadrapport openen": "Open charging report", "Volledige back-up": "Full back-up", "Automatische bronnen wijzigen": "Change sources automatically", "Verwacht vermogen over 30 min": "Expected power in 30 min", "Kabel wisselen": "Swap the cable", "Planning": "Planning", "ma": "Mon", "di": "Tue", "wo": "Wed", "do": "Thu", "vr": "Fri", "za": "Sat", "zo": "Sun", "Ma": "Mon", "Di": "Tue", "Wo": "Wed", "Do": "Thu", "Vr": "Fri", "Za": "Sat", "Zo": "Sun", "start": "start", "kickstart": "kickstart", "Uitzetten": "Switch off", "Aanzetten": "Switch on", "Het merk van je tweede laadpaal. Daarmee zoekt HESC zelf de schakelaars en sensoren op.": "The brand of your second charger. HESC uses it to find the switches and sensors itself.", "Voorbeeld; het echte rekenwerk komt in de alpha.": "Example; the real calculation comes in the alpha.", "Instellingen terugzetten": "Restore settings", "tik de standen aan die laden op zon betekenen": "tick the modes that mean charging on sun", "tik de standen aan die betekenen: geen auto": "tick the states that mean: no car", "Kies er minstens één.": "Choose at least one.", "wordt opgeslagen": "being saved", "Kabel omzetten": "Move the cable", "Kabel omzetten uiterlijk om": "Move the cable at the latest at", "Herinnering op je telefoon": "Reminder on your phone", "Twee auto's aan één laadpaal: de eerste auto laadt vóór dit tijdstip, de andere erna. Op dit tijdstip krijg je een herinnering op je telefoon om de kabel om te zetten, als de eerste auto er nog aan hangt en de andere een plan heeft. HESC plant met dit tijdstip.": "Two cars on one charger: the first car charges before this time, the other one after. At this time you get a reminder on your phone to move the cable, if the first car is still plugged in and the other has a plan. HESC plans with this time.", "Laadkosten downloaden": "Download charging costs", "per dag": "per day", "per maand": "per month", "Download de laatste export als spreadsheetbestand (CSV), per dag of per maand. Druk eerst op Uitvoeren bij Laadkosten exporteren.": "Download the last export as a spreadsheet file (CSV), per day or per month. First press Run at Export charging costs.", "Druk eerst op Uitvoeren bij Laadkosten exporteren.": "First press Run at Export charging costs.", "Aan": "On", "Accustand auto (verklaart stops, bijv. auto vol)": "Car battery level (explains stops, e.g. car full)", "Alle instellingen van HESC terugzetten naar de laatste back-up?": "Restore all of HESC's settings from the last back-up?", "Attribuut van de verwachting (leeg = toestand)": "Attribute of the forecast (empty = state)", "Auto aangesloten (binaire of statussensor)": "Car plugged in (binary or status sensor)", "Auto telt als ladend boven": "Car counts as charging above", "Auto telt als vol bij": "Car counts as full at", "Drempels, tijden en advies terugzetten naar de standaardwaarden van HESC? Eerst wordt er een back-up gemaakt, dus je kunt dit ongedaan maken": "Set thresholds, times and advice back to HESC's standard values? A back-up is made first, so you can undo this", "Eindcontrole voor de klaar-tijd (0 = uit)": "Final check before the ready time (0 = off)", "Entiteit voor de laadstand": "Entity for the charging mode", "Meldingen naar je telefoon": "Notifications to your phone", "Meldingsdiensten (gevuld door de lijst hierboven; zo nodig met de hand aanpassen)": "Notification services (filled by the list above; change by hand if needed)", "Minimale zon over voor de auto": "Minimum sun left for the car", "Netsensor: teruglevering is positief (uit = afname positief, de meeste meters)": "Grid sensor: feed-in is positive (off = import positive, most meters)", "Prijs uit de prijsbron is al all-in": "Price from the price source is already all-in", "Prijssensor (met een prijslijst, of een sensor van EnergyZero / EasyEnergy / Tibber / Nord Pool official)": "Price sensor (with a price list, or a sensor of EnergyZero / EasyEnergy / Tibber / Nord Pool official)", "Prijzen per (Automatic volgt de bron; Per hour = je leverancier rekent per uur af)": "Prices per (Automatic follows the source; Per hour = your supplier bills per hour)", "Schakelaar HPVC aan/uit": "HPVC on/off switch", "Sensor(en) vermogen thuisbatterij, + = laden": "Home battery power sensor(s), + = charging", "Standen voor laden op zon": "Modes for charging on the sun", "Startdrempel per seizoen (zet de twee hieronder elke maand)": "Start threshold per season (sets the two below every month)", "Statuswaarden die \"geen auto\" betekenen (alleen bij een statussensor)": "Status values that mean \"no car\" (only with a status sensor)", "Teller zonne-energie (kWh uit zon in het rapport)": "Solar energy counter (kWh from the sun in the report)", "Valuta (Automatic volgt de prijssensor)": "Currency (Automatic follows the price sensor)", "Verwacht vermogen om door te laden": "Expected power to keep charging", "Waarde van een kWh zon (terugleververgoeding, 0 = gratis)": "Value of a kWh of sun (feed-in payment, 0 = free)", "Waarde(n) die laden op zon betekenen, gescheiden door komma's": "Value(s) that mean charging on the sun, separated by commas", "Wachten tot de laadpaal start": "Wait until the charger starts", "Zonlicht om door te laden": "Sunlight to keep charging", "Zonverwachting morgen (bijv. Solcast forecast tomorrow)": "Solar forecast tomorrow (e.g. Solcast forecast tomorrow)", "…of laadstandwaarde die 'nu laden' betekent": "…or charging mode value that means 'charge now'", "Een tweede laadpaal hoort bij een tweede auto: kies bij \"+ Auto toevoegen\" voor een eigen laadpaal.": "A second charger goes with a second car: pick \"+ Add car\" for its own charger.", "Thuisbatterij en EV": "Home battery and EV", "Vink per thuisbatterij één sensor aan ·": "Tick one sensor per home battery ·", "Hoeveel kWh je thuisbatterijen samen kunnen opslaan.": "How many kWh your home batteries can store together.", "De stand (%) van je thuisbatterij(en). Per accu één sensor, of één voor alle samen.": "The level (%) of your home battery(s). One sensor per battery, or one for all together.", "Alleen met een thuisbatterij: zo zitten je thuisbatterij en je auto elkaar niet in de weg.": "Only with a home battery: so your home battery and your car don't get in each other's way.", "Het vermogen van je thuisbatterij(en). + = laden. Per accu één sensor, of één totaal-sensor; niet allebei.": "Your home battery(s) power. + = charging. One sensor per battery, or one total sensor; not both.", "Standaard: wat je af en toe wilt bijstellen, zoals meldingen, goedkope kansen, de thuisbatterij en de back-up.": "Standard: what you want to adjust now and then, like notifications, cheap chances, the home battery and the back-up.", "Aan: HESC zorgt dat je thuisbatterij en je auto elkaar niet in de weg zitten (kickstart en pauze). Alleen met een thuisbatterij.": "On: HESC makes sure your home battery and your car don't get in each other's way (kickstart and pause). Only with a home battery."}, "frag": [["Hij is nog niet aangesloten: steek de kabel erin vóór", "It is not plugged in yet: plug it in before"], ["krijg je een herinnering op je telefoon", "you get a reminder on your phone"], ["Prijs, zonverwachting en accustand van", "Price, solar forecast and battery level of"], ["Advies op basis van de laatste", "Advice based on the last"], ["HESC stuurt deze auto niet", "HESC does not control this car"], ["Er is geen laden gepland.", "No charging planned."], ["Hij is niet aangesloten.", "It is not plugged in."], ["geldt voor beide auto's", "applies to both cars"], ["voor de komende 24 uur", "for the next 24 hours"], ["Auto vol bij accustand", "Car full at battery level"], ["de rest gratis op zon", "the rest free on sun"], ["daarna weer het ritme", "then the rhythm again"], ["HESC stuurt deze auto", "HESC controls this car"], ["geen netladen gepland", "no grid charging planned"], ["Geen auto aangesloten", "No car plugged in"], ["tik om uit te zetten", "tap to switch off"], ["tik om aan te zetten", "tap to switch on"], ["Hij is aangesloten.", "It is plugged in."], ["op zijn vroegst om", "at the earliest at"], ["van het net samen", "from the grid together"], ["De accu gaat van", "The battery goes from"], ["klaar vandaag om", "ready today at"], ["Verwachte kosten", "Expected cost"], ["laatste 12 weken", "last 12 weeks"], ["alleen deze keer", "this time only"], ["terug naar ritme", "back to rhythm"], ["niet aangesloten", "not plugged in"], ["klaar morgen om", "ready tomorrow at"], ["u laden op zon", "h charging on sun"], ["Batterijniveau", "Battery level"], ["Eerstvolgende", "Next"], ["een stand van", "a mode of"], ["Goedkope kans", "Cheap chance"], ["niet gevonden", "not found"], ["Laadt nu met", "Charging now at"], ["geteld sinds", "counted since"], ["Nu laden tot", "Charge now to"], ["verwijderen?", "– remove?"], ["van het net", "from the grid"], ["aangesloten", "plugged in"], ["deze maand", "this month"], ["slaat over", "skips"], ["uiterlijk", "at the latest"], ["deze keer", "this time"], ["ontbreekt", "missing"], ["per maand", "per month"], ["Laadstand", "Charging mode"], ["klaar om", "ready at"], ["laadt nu", "charging now"], ["vannacht", "tonight"], ["vanavond", "this evening"], ["Vakantie", "Holiday"], ["laadpaal", "charger"], ["Laadpaal", "Charger"], ["Planning", "Planning"], ["Kalender", "Calendar"], ["Omvormer", "Inverter"], ["onbekend", "unknown"], ["vandaag", "today"], ["Totalen", "Totals"], ["gekozen", "chosen"], ["per kWh", "per kWh"], ["per dag", "per day"], ["Accu nu", "Battery now"], ["op zon", "on sun"], ["morgen", "tomorrow"], ["daarna", "then"], ["opslag", "surcharge"], ["alleen", "only"], ["Laadt", "Charges"], ["prijs", "price"], ["Ritme", "Rhythm"], ["laadt", "charging"], ["klaar", "ready"], ["naar", "to"], ["voor", "for"], ["auto", "car"], ["accu", "battery"], ["doel", "goal"], ["van", "from"], ["tot", "to"], ["zon", "sun"], ["net", "grid"], ["btw", "VAT"], ["Om", "At"], ["om", "at"], ["en", "and"], ["nu", "now"]]}, "de": {"exact": {"Fasen-overzicht": "Phasen-Übersicht", "Hoe je zonnestroom over de drie fasen verdeeld is, of elke fase genoeg zon krijgt om je laadpaal te laten starten, en wat je eraan kunt doen.": "Wie dein Solarstrom über die drei Phasen verteilt ist, ob jede Phase genug Sonne bekommt, damit deine Wallbox startet, und was du dagegen tun kannst.", "Alleen met een thuisbatterij: zo zitten je thuisbatterij(en) en je auto elkaar niet in de weg.": "Nur mit einem Hausakku: so kommen sich Hausakku und Auto nicht in die Quere.", "Thuisbatterij(en)": "Hausakku", "Land": "Land", "Het land van je stroomcontract. Daarna zie je alleen de prijsbronnen van dat land, en de valuta gaat vanzelf goed. Automatisch = het land van Home Assistant.": "Das Land deines Stromvertrags. Danach siehst du nur die Preisquellen dieses Landes, und die Währung stimmt von selbst. Automatisch = das Land von Home Assistant.", "Waar HESC de stroomprijzen vandaan haalt. Een bron die HESC bij jou vindt staat erbij; bij Eigen sensor met prijslijst kies je de sensor hieronder.": "Woher HESC die Strompreise holt. Eine Quelle, die HESC bei dir findet, steht dabei; bei Eigener Sensor mit Preisliste wählst du den Sensor darunter.", "Alleen bij Eigen sensor met prijslijst: de sensor met de prijzen van vandaag en morgen.": "Nur bei Eigener Sensor mit Preisliste: der Sensor mit den Preisen von heute und morgen.", "De munt van je prijzen. Gaat vanzelf goed als je een land kiest; Automatisch = die van Home Assistant.": "Die Währung deiner Preise. Stimmt von selbst, wenn du ein Land wählst; Automatisch = die von Home Assistant.", "Nederland": "Niederlande", "België": "Belgien", "Duitsland": "Deutschland", "Oostenrijk": "Österreich", "Frankrijk": "Frankreich", "Spanje": "Spanien", "Zweden": "Schweden", "Noorwegen": "Norwegen", "Denemarken": "Dänemark", "Verenigd Koninkrijk": "Vereinigtes Königreich", "Australië": "Australien", "Ander land": "Anderes Land", "Eigen sensor met prijslijst": "Eigener Sensor mit Preisliste", "Hoe je zonnestroom over de drie fasen verdeeld is. Sommige laadpalen starten pas als er op elke fase genoeg zon is; de zwakste fase bepaalt dan wanneer je auto op zon kan laden.": "Wie dein Solarstrom über die drei Phasen verteilt ist. Manche Wallboxen starten erst, wenn auf jeder Phase genug Sonne ist; die schwächste Phase bestimmt dann, wann dein Auto mit Sonne laden kann.", "Netvermogen fase 1": "Netzleistung Phase 1", "Netvermogen fase 2": "Netzleistung Phase 2", "Netvermogen fase 3": "Netzleistung Phase 3", "Alleen bij 3 fasen. Met het netvermogen per fase meet HESC hoe je zonnestroom over de fasen verdeeld is.": "Nur bei 3 Phasen. Mit der Netzleistung pro Phase misst HESC, wie dein Solarstrom über die Phasen verteilt ist.", "alleen deze dag": "nur dieser Tag", "Opslaan": "Speichern", "Deze dag uit": "Diesen Tag aus", "Terug naar ritme": "Zurück zum Rhythmus", "+ Vakantie": "+ Urlaub", "✕ annuleren": "✕ abbrechen", "Tik de eerste dag van de vakantie": "Tippe auf den ersten Urlaubstag", "Tik nu de laatste dag van de vakantie": "Tippe jetzt auf den letzten Urlaubstag", "Op dit toestel HESC hier openen": "HESC auf diesem Gerät hier öffnen", "Maand": "Monat", "Ritme en deze keer": "Rhythmus und dieses Mal", "Nu": "Jetzt", "Om": "Um", "aan": "an", "een": "ein", "uit": "aus", "van": "von", "zon": "Sonne", "Auto": "Auto", "Jaar": "Jahr", "accu": "Akku", "auto": "Auto", "geen": "keine", "naar": "auf", "week": "Woche", "Dagen": "Tage", "Klaar": "Fertig", "Laadt": "Lädt", "Weken": "Wochen", "klaar": "fertig", "laadt": "lädt", "laden": "laden", "net ±": "Netz ±", "stand": "Modus", "wacht": "wartet", "+ Auto": "+ Auto", "Advies": "Empfehlung", "Auto's": "Autos", "Kosten": "Kosten", "Morgen": "Morgen", "Uitleg": "Anleitung", "accu %": "Akku %", "auto 1": "Auto 1", "auto 2": "Auto 2", "bezig…": "läuft…", "morgen": "morgen", "op zon": "mit Sonne", "stuurt": "steuert", "Accu nu": "Akku jetzt", "Je auto": "Dein Auto", "Je huis": "Dein Haus", "Maanden": "Monate", "Melding": "Meldung", "Per uur": "Pro Stunde", "Prijzen": "Preise", "Rapport": "Bericht", "Vandaag": "Heute", "Vol bij": "Voll bei", "laadt ·": "lädt ·", "nu, tot": "jetzt, bis", "vandaag": "heute", "· accu": "· Akku", ": ik zie": ": ich sehe", "Eén auto": "Ein Auto", "Laadpaal": "Ladestation", "Prijs nu": "Preis jetzt", "Vakantie": "Urlaub", "klaar om": "fertig um", "laadpaal": "Ladestation", "vakantie": "Urlaub", "vannacht": "heute Nacht", "volgende": "nächste", "— geen —": "— keine —", "⏻ uit ·": "⏻ aus ·", "· klaar": "· fertig", "<br>accu": "<br>Akku", "Annuleren": "Abbrechen", "Je auto's": "Deine Autos", "Kan niet:": "Nicht möglich:", "Kwartalen": "Quartale", "Meldingen": "Meldungen", "Ontbreekt": "Fehlt", "Standaard": "Standard", "Thuisaccu": "Hausakku", "Uitvoeren": "Ausführen", "alleen nu": "nur jetzt", "deze auto": "dieses Auto", "deze keer": "dieses Mal", "gaat voor": "hat Vorrang", "ontbreekt": "fehlt", "standaard": "Standard", "staat aan": "ist an", "staat uit": "ist aus", "+ Laadpaal": "+ Ladestation", "1 laadpaal": "1 Ladestation", "Alleen zon": "Nur Sonne", "Laadpaal 1": "Ladestation 1", "Laadpaal 2": "Ladestation 2", "Laadpaal ·": "Ladestation ·", "Zon en net": "Sonne und Netz", "auto laadt": "Auto lädt", "laadpaal 1": "Ladestation 1", "laadpaal 2": "Ladestation 2", "prijs (ct)": "Preis (ct)", "· klaar om": "· fertig um", "Je laadpaal": "Deine Ladestation", "Om de beurt": "Abwechselnd", "Verwijderen": "Entfernen", "Weerstation": "Wetterstation", "herinnering": "Erinnerung", "je laadpaal": "deine Ladestation", "n ontbreekt": "fehlen", "net ± 3 kWh": "Netz ± 3 kWh", "nog ± 3 kWh": "noch ± 3 kWh", "van het net": "aus dem Netz", "weerstation": "Wetterstation", "· deze keer": "· dieses Mal", "· geen auto": "· kein Auto", "Instellingen": "Einstellungen", "Je laadpalen": "Deine Ladestationen", "Komende week": "Kommende Woche", "Niet gekozen": "Nicht gewählt", "Niet gelukt:": "Fehlgeschlagen:", "Nu laden tot": "Jetzt laden bis", "Vorige maand": "Vorheriger Monat", "Weet ik niet": "Weiß ich nicht", "Zon verwacht": "Erwartete Sonne", "alleen {ev1}": "nur {ev1}", "alleen {ev2}": "nur {ev2}", "laden op zon": "Laden mit Sonne", "net ± 13 kWh": "Netz ± 13 kWh", "niet gekozen": "nicht gewählt", "nog ± 26 kWh": "noch ± 26 kWh", "zon ± 10 kWh": "Sonne ± 10 kWh", "Accustand van": "Akkustand von", "Ja, uitvoeren": "Ja, ausführen", "Laatste actie": "Letzte Aktion", "Uitleg openen": "Anleitung öffnen", "de meeste kWh": "die meisten kWh", "een stand van": "ein Modus von", "} verwijderen": "} entfernen", "· om de beurt": "· abwechselnd", "Accu nu → doel": "Akku jetzt → Ziel", "Laatste export": "Letzter Export", "Netvermogen nu": "Netzleistung jetzt", "Volgende maand": "Nächster Monat", "Zon · goedkoop": "Sonne · günstig", "Zonnestroom nu": "Solarleistung jetzt", "morgen ± 7 kWh": "morgen ± 7 kWh", "niet gevonden:": "nicht gefunden:", "Andere laadpaal": "Andere Ladestation", "Eco (zon + net)": "Eco (Sonne + Netz)", "Laatste back-up": "Letzte Sicherung", "Thuisaccu en EV": "Hausakku und E-Auto", "Tik om te typen": "Tippen zum Eingeben", "wacht op schema": "wartet auf Zeitplan", "zon verwachting": "Solarprognose", "kWh van het net": "kWh aus dem Netz", "+ Auto toevoegen": "+ Auto hinzufügen", "15 minuten later": "15 Minuten später", "Accustand-sensor": "Akkustand-Sensor", "Auto laadt vanaf": "Auto lädt ab", "Bewaren of delen": "Sichern oder teilen", "De accu gaat van": "Der Akku geht von", "Langste vrijgave": "Längste Freigabe", "Verwachte kosten": "Erwartete Kosten", "niet aangesloten": "nicht angesteckt", "15 minuten eerder": "15 Minuten früher", "Advies bijgewerkt": "Empfehlung aktualisiert", "Ik weet het zeker": "Ich bin sicher", "Kies een telefoon": "Wähle ein Handy", "Vandaag en morgen": "Heute und morgen", "laden van het net": "Laden aus dem Netz", "vandaag en morgen": "heute und morgen", "· met herinnering": "· mit Erinnerung", "(alleen deze keer)": "(nur dieses Mal)", "Herinnering sturen": "Erinnerung senden", "Hoe laad je thuis?": "Wie lädst du zu Hause?", "Kickstarts per dag": "Kickstarts pro Tag", "Rapport en back-up": "Bericht und Sicherung", "Start bij zonlicht": "Start bei Sonnenlicht", "Tijden en vrijgave": "Zeiten und Freigabe", "Tik om te wijzigen": "Tippen zum Ändern", "op zijn vroegst om": "frühestens um", "○ niet aangesloten": "○ nicht angesteckt", "✕ terug naar ritme": "✕ zurück zum Rhythmus", "✕ vakantie stoppen": "✕ Urlaub beenden", "· wacht op de auto": "· wartet auf das Auto", "Anoniem om te delen": "Anonym zum Teilen", "Auto's en laadpalen": "Autos und Ladestationen", "HESC aanzetten voor": "HESC einschalten für", "HESC laadt opnieuw…": "HESC lädt neu…", "HESC uitzetten voor": "HESC ausschalten für", "Hij is aangesloten.": "Es ist angesteckt.", "Ja, ik wil nu laden": "Ja, ich will jetzt laden", "Meldingen gaan naar": "Meldungen gehen an", "Wachten op laadpaal": "Wartet auf Ladestation", "geen lading gepland": "kein Laden geplant", "installeer eerst de": "installiere zuerst die", "ja, met verwachting": "ja, mit Prognose", "· vandaag en morgen": "· heute und morgen", "— kies een sensor —": "— Sensor wählen —", "<b>Echt</b> · 1 auto": "<b>Echt</b> · 1 Auto", "Afkoelen na vrijgave": "Abkühlen nach Freigabe", "Gemiddelde laadprijs": "Durchschnittlicher Ladepreis", "HESC stuurt laadpaal": "HESC steuert Ladestation", "Verwacht vermogen nu": "Erwartete Leistung jetzt", "Verwachte laadkosten": "Erwartete Ladekosten", "evcc (elke laadpaal)": "evcc (jede Ladestation)", "geen netblok gepland": "kein Netzblock geplant", "heb je zonnepanelen?": "hast du Solarmodule?", "tik om aan te zetten": "tippen zum Einschalten", "tik om uit te zetten": "tippen zum Ausschalten", "= wat HESC zou kiezen": "= was HESC wählen würde", "Aan/uit in de grafiek": "Ein/aus in der Grafik", "Stabiel vóór vrijgave": "Stabil vor Freigabe", "Start bij verwachting": "Start bei Prognose", "Zonverwachting morgen": "Solarprognose morgen", "geen netladen gepland": "kein Netzladen geplant", "laadt op zon · 3,7 kW": "lädt mit Sonne · 3,7 kW", "<b>Demo</b> · 2 auto's": "<b>Demo</b> · 2 Autos", "Advies over de laatste": "Empfehlung über die letzten", "Doorladen bij zonlicht": "Weiterladen bei Sonnenlicht", "Laadvermogen (W of kW)": "Ladeleistung (W oder kW)", ", de rest gratis op zon": ", der Rest gratis mit Sonne", "HPVC aan/uit-schakelaar": "HPVC Ein/Aus-Schalter", "geldt voor beide auto's": "gilt für beide Autos", "gestreept = van het net": "gestreift = aus dem Netz", "· daarna weer het ritme": "· danach wieder der Rhythmus", "Hij is niet aangesloten.": "Es ist nicht angesteckt.", "Ja, ik wil dit aanzetten": "Ja, ich will das einschalten", "Ja, ik wil dit uitzetten": "Ja, ich will das ausschalten", "Kort voor een bugmelding": "Kurz, für eine Fehlermeldung", "Laadvermogen van het net": "Ladeleistung aus dem Netz", "Min. sessies voor advies": "Min. Sitzungen für Empfehlung", "Prijslijst in een sensor": "Preisliste in einem Sensor", "kies het doel, dan Start": "Ziel wählen, dann Start", "laadt nu van het net tot": "lädt jetzt aus dem Netz bis", "wacht op zon (Eco-Smart)": "wartet auf Sonne (Eco-Smart)", "Deze auto kent HESC niet.": "HESC kennt dieses Auto nicht.", "Doorladen bij verwachting": "Weiterladen bei Prognose", "Geadviseerde startdrempel": "Empfohlene Startschwelle", "Melding: niet aangesloten": "Meldung: nicht angesteckt", "Twee auto's, één laadpaal": "Zwei Autos, eine Ladestation", "Zon: starten en doorladen": "Sonne: starten und weiterladen", ": integratie niet gevonden": ": Integration nicht gefunden", "Er is geen laden gepland.": "Kein Laden geplant.", "Min. zon over voor de auto": "Min. Sonne übrig für das Auto", "Mislukte vrijgaven per dag": "Fehlgeschlagene Freigaben pro Tag", "Verwachte laadkosten samen": "Erwartete Ladekosten zusammen", "leeg · tik om in te vullen": "leer · tippen zum Ausfüllen", "Nee, HESC werkt op zichzelf": "Nein, HESC arbeitet für sich", "kabel omzetten uiterlijk om": "Kabel spätestens umstecken um", "kandidaten, kies degene die": "Kandidaten, wähle den, der", "typ de waarde, bijv. 0,1116": "Wert eingeben, z. B. 0,1116", "1,9 kW overschot · gaat naar": "1,9 kW Überschuss · geht an", "Eerstvolgende keer overslaan": "Nächstes Mal überspringen", "Eindcontrole vóór klaar-tijd": "Endkontrolle vor Fertig-Zeit", "Wat wil je bewaren of delen?": "Was willst du sichern oder teilen?", "geen zonverwachting gevonden": "keine Solarprognose gefunden", "Deze laadpaal kent HESC niet.": "HESC kennt diese Ladestation nicht.", "nog niets van het net gepland": "noch nichts aus dem Netz geplant", "Vol vermogen (geen zonnestand)": "Volle Leistung (kein Solarmodus)", "Waar komen je prijzen vandaan?": "Woher kommen deine Preise?", "aangesloten, auto vraagt niets": "angesteckt, Auto will nichts", "het accu-% van deze auto geeft": "den Akku-% dieses Autos liefert", "waar komen je prijzen vandaan?": "woher kommen deine Preise?", "De aan/uit-schakelaar van HPVC.": "Der Ein/Aus-Schalter von HPVC.", "HESC kijkt wat er weg zou gaan…": "HESC prüft, was wegfallen würde…", "Instelscherm van Home Assistant": "Einstellungsseite von Home Assistant", "Klaar! HESC v4 gaat aan de slag.": "Fertig! HESC v4 legt los.", "Laden als de stroom goedkoop is.": "Laden, wenn Strom günstig ist.", "om de beurt, jij zet de kabel om": "abwechselnd, du steckst das Kabel um", "04:00–04:45 van het net (± 3 kWh)": "04:00–04:45 aus dem Netz (± 3 kWh)", "Geen geschikte sensoren gevonden.": "Keine passenden Sensoren gefunden.", "heb je dynamische energieprijzen?": "hast du dynamische Strompreise?", "Je andere auto merkt er niets van.": "Dein anderes Auto merkt nichts davon.", "taal van je Home Assistant-profiel": "Sprache deines Home-Assistant-Profils", "De uitleg van HESC, in gewone taal.": "Die Anleitung von HESC, in einfacher Sprache.", "Eerstvolgende keer andere tijd of %": "Nächstes Mal andere Zeit oder %", "Niet nodig: er laadt maar één auto.": "Nicht nötig: nur ein Auto lädt.", "Twee auto's, elk een eigen laadpaal": "Zwei Autos, jedes mit eigener Ladestation", "Vink per thuisaccu één sensor aan ·": "Pro Hausakku einen Sensor ankreuzen ·", "Zonverwachting en realisatie · auto": "Solarprognose und Ist · Auto", "Hoeveel je zonnepanelen nu opwekken.": "Wie viel deine Solarmodule gerade erzeugen.", "Verwachting laadmogelijkheden op zon": "Erwartetes Laden mit Sonne", "Verwijderd. HESC laadt zich opnieuw.": "Entfernt. HESC lädt neu.", "Alleen auto 2 kan weg; auto 1 blijft.": "Nur Auto 2 kann weg; Auto 1 bleibt.", "Verwachting-attribuut (leeg = waarde)": "Prognose-Attribut (leer = Wert)", "Zonverwachting vandaag (per half uur)": "Solarprognose heute (pro halbe Stunde)", "HESC houdt auto 1 en laadpaal 1 altijd": "HESC behält Auto 1 und Ladestation 1 immer", "Hoe lang een vrijgave hoogstens duurt.": "Wie lange eine Freigabe höchstens dauert.", "Netvermogen (negatief = teruglevering)": "Netzleistung (negativ = Einspeisung)", "Staat in de specificaties van je auto.": "Steht in den technischen Daten deines Autos.", "de prijzen van vandaag en morgen heeft": "die Preise von heute und morgen hat", "heeft panelen vrijgegeven voor de auto": "hat Module für das Auto freigegeben", "· voorbeeld, er wordt niets opgeslagen": "· Beispiel, es wird nichts gespeichert", "Alleen als je Home PV Control gebruikt.": "Nur wenn du Home PV Control nutzt.", "Schaduwmodus (rekent mee, stuurt niets)": "Schattenmodus (rechnet mit, steuert nichts)", "geen sensor voor zonnevermogen gevonden": "kein Sensor für Solarleistung gefunden", "De startdrempel die het advies aanraadt.": "Die Startschwelle, die die Empfehlung rät.", "Deze HESC-versie kan nog niets weghalen.": "Diese HESC-Version kann noch nichts entfernen.", "Planning, laadkosten en instellingen van": "Planung, Ladekosten und Einstellungen von", "Waar HESC zon, net en verwachting leest.": "Wo HESC Sonne, Netz und Prognose liest.", "het totale vermogen van je panelen geeft": "die Gesamtleistung deiner Module liefert", "krijg je een herinnering op je telefoon.": "bekommst du eine Erinnerung auf dein Handy.", "Hoeveel de laadpaal nu laadt, in W of kW.": "Wie viel die Ladestation gerade lädt, in W oder kW.", "Dashboardpatroon — knoppenrij met vensters": "Dashboard-Muster — Knopfleiste mit Fenstern", "De zonverwachting van morgen per half uur.": "Die Solarprognose für morgen pro halbe Stunde.", "Auto aangesloten (aan/uit- of statussensor)": "Auto angesteckt (Ein/Aus- oder Statussensor)", "Boven dit vermogen telt de auto als ladend.": "Über dieser Leistung gilt das Auto als ladend.", "maximum dat de installateur heeft ingesteld": "vom Installateur eingestelltes Maximum", "s laden aan dezelfde laadpaal. De auto die": "s laden an derselben Ladestation. Das Auto, das", "Het verwachte zonvermogen over een half uur.": "Die erwartete Solarleistung in einer halben Stunde.", "Je HESC-instellingen bewaren en terugzetten.": "Deine HESC-Einstellungen sichern und wiederherstellen.", "Start/stop-schakelaar laadpaal (aan = laden)": "Start/Stopp-Schalter Ladestation (an = laden)", "Alleen laadpaal 2 kan weg; laadpaal 1 blijft.": "Nur Ladestation 2 kann weg; Ladestation 1 bleibt.", "Waarde(n) voor laden op zon, komma-gescheiden": "Wert(e) für Laden mit Sonne, durch Komma getrennt", "afname en teruglevering van het hele huis meet": "Bezug und Einspeisung des ganzen Hauses misst", "gaat voor: beide moeten wo 07:30 klaar zijn en": "hat Vorrang: beide müssen Mi 07:30 fertig sein und", "zon genoeg · prijs onder je goedkope-kansprijs": "genug Sonne · Preis unter deinem Günstig-Preis", "Hoeveel kWh je thuisaccu’s samen kunnen opslaan.": "Wie viele kWh deine Hausakkus zusammen speichern können.", "Je hebt in dit venster nog geen back-up gemaakt.": "Du hast in diesem Fenster noch keine Sicherung erstellt.", "Zonne-energieteller (kWh van zon in het rapport)": "Solarenergiezähler (kWh aus Sonne im Bericht)", "de verwachting geeft (Solcast of Forecast.Solar)": "die Prognose liefert (Solcast oder Forecast.Solar)", "Pas na zoveel zonnesessies geeft HESC een advies.": "Erst nach so vielen Solarsitzungen gibt HESC eine Empfehlung.", "Terug naar zonnestand (Wallbox: schema hervatten)": "Zurück in den Solarmodus (Wallbox: Zeitplan fortsetzen)", "Wanneer het advies voor het laatst is bijgewerkt.": "Wann die Empfehlung zuletzt aktualisiert wurde.", "Zet de instellingen uit de laatste back-up terug.": "Die Einstellungen aus der letzten Sicherung wiederherstellen.", "Zonder namen en codes. Bovenaan staat wat je deelt.": "Ohne Namen und Codes. Oben steht, was du teilst.", "Hoe lang HESC na een vrijgave wacht voor een nieuwe.": "Wie lange HESC nach einer Freigabe auf eine neue wartet.", "Hij is nog niet aangesloten: steek de kabel erin vóór": "Es ist noch nicht angesteckt: steck das Kabel ein vor", "geen netmeter gevonden (bijv. P1 / DSMR / HomeWizard)": "kein Netzzähler gefunden (z. B. P1 / DSMR / HomeWizard)", "wordt opgeslagen · HESC laadt opnieuw (± half minuut)": "wird gespeichert · HESC lädt neu (± eine halbe Minute)", "Aan als je Home PV Control gebruikt. Zonder HPVC: uit.": "An, wenn du Home PV Control nutzt. Ohne HPVC: aus.", "heb je een load balancer die het huisverbruik meeneemt?": "hast du einen Lastmanager, der den Hausverbrauch berücksichtigt?", "Alles, ook namen. Om zelf te bewaren of terug te zetten.": "Alles, auch Namen. Zum Selbst-Aufbewahren oder Wiederherstellen.", "Een ✓ betekent dat HESC die bron in Home Assistant vond.": "Ein ✓ heißt, HESC hat diese Quelle in Home Assistant gefunden.", "Wat je slimme meter nu meet. Negatief = je levert terug.": "Was dein Smart Meter gerade misst. Negativ = du speist ein.", "Weet je het zeker? Dit kan niet ongedaan worden gemaakt.": "Bist du sicher? Das kann nicht rückgängig gemacht werden.", "kies straks bij Instellingen de sensor met de prijslijst": "wähle später in den Einstellungen den Sensor mit der Preisliste", "· HESC zoekt laadvermogen, aangesloten en laadstand zelf": "· HESC findet Ladeleistung, angesteckt und Lademodus selbst", "€ 0,231 /kWh · goedkoopst vannacht 02:15–04:00 (€ 0,171)": "€ 0,231 /kWh · am günstigsten heute Nacht 02:15–04:00 (€ 0,171)", "<b>Komt in v4: het rapport maakt de v4-integratie.</b> ·": "<b>Kommt in v4: die v4-Integration erstellt den Bericht.</b> ·", "De naam komt uit Home Assistant; pas hem aan als je wilt.": "Der Name kommt aus Home Assistant; ändere ihn, wenn du willst.", "Geen prijzen ontvangen: HESC kan nu niet plannen op prijs.": "Keine Preise empfangen: HESC kann jetzt nicht nach Preis planen.", "Binnen hoeveel uur de minimale accustand bereikt moet zijn.": "Innerhalb wie vieler Stunden der Mindest-Akkustand erreicht sein muss.", "Het verwachte zonvermogen van nu, bijvoorbeeld van Solcast.": "Die erwartete Solarleistung jetzt, z. B. von Solcast.", "Welke laadstand(en) van je laadpaal laden op zon betekenen.": "Welche Modi deiner Ladestation Laden mit Sonne bedeuten.", "dan weer laden op zon en goedkope uren volgens de planning.": "dann wieder Laden mit Sonne und günstigen Stunden laut Planung.", "Boven dit verwachte zonvermogen begint HESC op zon te laden.": "Über dieser erwarteten Solarleistung beginnt HESC mit Sonne zu laden.", "De sensor van HPVC die zegt of hij de zonnepanelen begrenst.": "Der Sensor von HPVC, der sagt, ob er die Solarmodule begrenzt.", "Statuswaarden voor \"geen auto\" (alleen bij een statussensor)": "Statuswerte für „kein Auto“ (nur bei Statussensor)", "✓ Alles gevonden. Dit scherm wordt in het echt overgeslagen.": "✓ Alles gefunden. In echt wird dieser Schritt übersprungen.", "De munt van je prijzen. Automatisch = die van Home Assistant.": "Die Währung deiner Preise. Automatisch = die von Home Assistant.", "Het merk, en wat de installateur als maximum heeft ingesteld.": "Die Marke, und welches Maximum der Installateur eingestellt hat.", "Hoe lang de laadpaal gestopt moet zijn voordat HESC terugzet.": "Wie lange die Ladestation gestoppt sein muss, bevor HESC zurückschaltet.", "Hoe vaak per dag HESC de laadpaal hoogstens een duwtje geeft.": "Wie oft pro Tag HESC der Ladestation höchstens einen Schubs gibt.", "Aan: HESC neemt het advies zelf over. Uit: je ziet het alleen.": "An: HESC übernimmt die Empfehlung selbst. Aus: du siehst sie nur.", "dan met rust: geen planning, niet pauzeren of hervatten. Heeft": "dann in Ruhe: keine Planung, kein Pausieren oder Fortsetzen. Hat", "HESC v4 start in schaduwmodus: het kijkt mee en schakelt niets.": "HESC v4 startet im Schattenmodus: es schaut zu und schaltet nichts.", "Hoe lang HESC wacht tot de laadpaal na de vrijgave echt begint.": "Wie lange HESC wartet, bis die Ladestation nach der Freigabe wirklich startet.", "Over hoeveel dagen HESC je laadsessies bekijkt voor het advies.": "Über wie viele Tage HESC deine Ladesitzungen für die Empfehlung betrachtet.", "Wanneer de laatste back-up van je HESC-instellingen is gemaakt.": "Wann die letzte Sicherung deiner HESC-Einstellungen erstellt wurde.", "Wat het advies nu zegt, of hoeveel sessies het nog nodig heeft.": "Was die Empfehlung jetzt sagt, oder wie viele Sitzungen sie noch braucht.", "Kabel wisselen is niet nodig: elke auto heeft een eigen laadpaal.": "Kein Kabelwechsel nötig: jedes Auto hat seine eigene Ladestation.", "Samenvatting in het Engels, om in een issue op GitHub te plakken.": "Zusammenfassung auf Englisch, für ein Issue auf GitHub.", "12:30–16:30 op zon (± 10 kWh) · 02:15–04:00 van het net (± 13 kWh)": "12:30–16:30 mit Sonne (± 10 kWh) · 02:15–04:00 aus dem Netz (± 13 kWh)", "Of HESC op 1 of 3 fasen zou moeten laden, als je laadpaal dat kan.": "Ob HESC mit 1 oder 3 Phasen laden sollte, wenn deine Ladestation das kann.", "Herinnering op je telefoon als het tijd is om de kabel om te zetten": "Erinnerung auf dem Handy, wenn es Zeit ist, das Kabel umzustecken", "Op of onder deze prijs per kWh telt een kwartier als goedkope kans.": "Bei oder unter diesem Preis pro kWh gilt eine Viertelstunde als günstige Gelegenheit.", "De teller van de laadpaal voor energie uit de zon, voor het rapport.": "Der Zähler der Ladestation für Energie aus der Sonne, für den Bericht.", "HESC maakt eerst zelf een back-up; die kun je hierboven terugzetten.": "HESC erstellt zuerst selbst eine Sicherung; die kannst du oben wiederherstellen.", "Hoe lang de zon even mag wegvallen (een wolk) zonder dat HESC stopt.": "Wie lange die Sonne kurz wegfallen darf (eine Wolke), ohne dass HESC stoppt.", "Onder dit zonlicht stopt HESC weer (alleen met het weerstation aan).": "Unter diesem Sonnenlicht stoppt HESC wieder (nur mit eingeschalteter Wetterstation).", "HESC gaat dan weer laden op zon en goedkope uren volgens je planning.": "HESC lädt dann wieder mit Sonne und in günstigen Stunden laut Planung.", "Hoe geduldig HESC is. De standaardwaarden werken voor de meeste huizen.": "Wie geduldig HESC ist. Die Standardwerte passen für die meisten Häuser.", "Dit kon HESC niet (zeker) vinden. Kies het zelf; de rest is al ingevuld.": "Das konnte HESC nicht (sicher) finden. Wähle es selbst; der Rest ist schon ausgefüllt.", "Onder dit % laadt HESC de auto meteen bij, in de goedkoopste kwartieren.": "Unter diesem % lädt HESC das Auto sofort nach, in den günstigsten Viertelstunden.", "Boven dit zonlicht begint HESC te laden (alleen met het weerstation aan).": "Über diesem Sonnenlicht beginnt HESC zu laden (nur mit eingeschalteter Wetterstation).", "De bestanden van deze auto blijven bewaard (hernoemd), niets wordt gewist.": "Die Dateien dieses Autos bleiben erhalten (umbenannt), nichts wird gelöscht.", "HESC vraagt straks zelf naar het laadvermogen, aangesloten en de laadstand": "HESC fragt später selbst nach Ladeleistung, angesteckt und Lademodus", "HESC kijkt naar je eigen laadsessies en stelt een betere startdrempel voor.": "HESC schaut sich deine eigenen Ladesitzungen an und schlägt eine bessere Startschwelle vor.", "Netsensor: teruglevering positief (uit = afname positief, de meeste meters)": "Netzsensor: Einspeisung positiv (aus = Bezug positiv, die meisten Zähler)", "Prijzen per uur of per kwartier. Automatisch = zoals je prijsbron ze geeft.": "Preise pro Stunde oder pro Viertelstunde. Automatisch = wie deine Preisquelle sie liefert.", "Bewaart al je HESC-instellingen in Home Assistant, plus een kopie met datum.": "Speichert alle deine HESC-Einstellungen in Home Assistant, plus eine Kopie mit Datum.", "De sensor waaruit HESC het % van je auto leest. Tik om een andere te kiezen.": "Der Sensor, aus dem HESC den % deines Autos liest. Tippen, um einen anderen zu wählen.", "Hoe lang de zon stabiel genoeg moet zijn voordat HESC de laadpaal vrijgeeft.": "Wie lange die Sonne stabil genug sein muss, bevor HESC die Ladestation freigibt.", "Na zoveel mislukte vrijgaven op een dag probeert HESC het die dag niet meer.": "Nach so vielen fehlgeschlagenen Freigaben an einem Tag versucht HESC es an dem Tag nicht mehr.", "Voorbeeld: de auto's en laadtijden zijn verzonnen, prijzen en zon zijn echt.": "Beispiel: Autos und Ladezeiten sind erfunden, Preise und Sonne sind echt.", "Tot hoeveel % HESC de auto als vol rekent. Vaak 80 %; bij een LFP-accu 100 %.": "Bis zu welchem % HESC das Auto als voll rechnet. Oft 80 %; bei einem LFP-Akku 100 %.", "De stand (%) van je thuisaccu(s). Per accu één sensor, of één voor alle samen.": "Der Stand (%) deiner Hausakkus. Ein Sensor pro Akku, oder einer für alle zusammen.", "De zonverwachting van vandaag per half uur. HESC plant daarmee het laden op zon.": "Die Solarprognose für heute pro halbe Stunde. Damit plant HESC das Laden mit Sonne.", "Aan: HESC leest zonnestroom en netvermogen uit HPVC in plaats van uit Zon en net.": "An: HESC liest Solar- und Netzleistung aus HPVC statt aus Sonne und Netz.", "Alleen met een thuisaccu: zo zitten je thuisaccu en je auto elkaar niet in de weg.": "Nur mit Hausakku: so kommen sich Hausakku und Auto nicht in die Quere.", "Bijvoorbeeld Wallbox Power Boost, of een laadpaal die via de slimme meter meekijkt.": "Zum Beispiel Wallbox Power Boost, oder eine Ladestation, die über den Smart Meter mitschaut.", "Alleen bij Prijslijst in een sensor: de sensor met de prijzen van vandaag en morgen.": "Nur bei Preisliste in einem Sensor: der Sensor mit den Preisen von heute und morgen.", "vannacht van 01:45 tot 02:00, van 03:00 tot 03:15 en van 04:45 tot 05:00 van het net": "heute Nacht von 01:45 bis 02:00, von 03:00 bis 03:15 und von 04:45 bis 05:00 aus dem Netz", "Zon verwacht tegen werkelijk, en wanneer de auto met behulp van zonne-energie kan laden.": "Erwartete gegen tatsächliche Sonne, und wann das Auto mit Solarenergie laden kann.", "De sensor van je weerstation die het zonlicht meet, in W/m². Tik om een andere te kiezen.": "Der Sensor deiner Wetterstation, der das Sonnenlicht misst, in W/m². Tippen, um einen anderen zu wählen.", "Voor laadpalen die iets extra nodig hebben. Bij de meeste laadpalen vult HESC dit zelf in.": "Für Ladestationen, die etwas extra brauchen. Bei den meisten füllt HESC das selbst aus.", "Maakt het laadrapport opnieuw met de gegevens van nu. Daarna verschijnt Laadrapport openen.": "Erstellt den Ladebericht neu mit den aktuellen Daten. Danach erscheint Ladebericht öffnen.", "De schakelaar waarmee HESC de laadpaal laat laden of pauzeren. Nodig om van het net te laden.": "Der Schalter, mit dem HESC die Ladestation laden oder pausieren lässt. Nötig zum Laden aus dem Netz.", "Een extra schakelaar die sommige laadpalen nodig hebben om op zon te laden (go-e, Wattpilot).": "Ein zusätzlicher Schalter, den manche Ladestationen zum Laden mit Sonne brauchen (go-e, Wattpilot).", "Telt je meter teruglevering als positief? Zet dit dan aan. De meeste meters doen het andersom.": "Zählt dein Zähler Einspeisung als positiv? Dann schalte das ein. Die meisten Zähler machen es umgekehrt.", "HPVC gevonden. HPVC regelt je zonnepanelen bij negatieve prijzen. Zal HESC daarmee samenwerken?": "HPVC gefunden. HPVC regelt deine Solarmodule bei negativen Preisen. Soll HESC damit zusammenarbeiten?", "Hoeveel zon er vandaag minstens over moet blijven voor de auto voordat HESC een kickstart doet.": "Wie viel Sonne heute mindestens für das Auto übrig bleiben muss, bevor HESC einen Kickstart macht.", "Het merk van je laadpaal. Daarmee zoekt HESC zelf de schakelaars en sensoren van de laadpaal op.": "Die Marke deiner Ladestation. Damit sucht HESC die Schalter und Sensoren der Ladestation selbst.", "Zet de instellingen uit de back-up terug. Welke back-up hij gebruikt, staat bij Laatste back-up.": "Die Einstellungen aus der Sicherung wiederherstellen. Welche Sicherung, steht bei Letzte Sicherung.", "Aan: de startdrempel past zich aan de tijd van het jaar aan (in de winter lager dan in de zomer).": "An: die Startschwelle passt sich der Jahreszeit an (im Winter niedriger als im Sommer).", "Met hoeveel kW HESC rekent als hij van het net laadt. Bepaalt hoeveel kwartieren hij nodig heeft.": "Mit wie vielen kW HESC rechnet, wenn es aus dem Netz lädt. Bestimmt, wie viele Viertelstunden es braucht.", "Waar de zonverwachting vandaan komt, bijvoorbeeld Solcast of Forecast.Solar. HESC kiest dit zelf.": "Woher die Solarprognose kommt, z. B. Solcast oder Forecast.Solar. HESC wählt das selbst.", "Bewaart al je HESC-instellingen in Home Assistant (map hesc_v3), plus een kopie met datum en tijd.": "Speichert alle deine HESC-Einstellungen in Home Assistant (Ordner hesc_v3), plus eine Kopie mit Datum und Uhrzeit.", "De laadstand van je laadpaal (bijvoorbeeld zon, eco of direct). HESC zet hem op zon en weer terug.": "Der Lademodus deiner Ladestation (z. B. Sonne, Eco oder direkt). HESC schaltet ihn auf Sonne und zurück.", "Welke statuswaarden betekenen dat er geen auto aan de laadpaal hangt. Alleen bij een statussensor.": "Welche Statuswerte bedeuten, dass kein Auto an der Ladestation hängt. Nur bei Statussensor.", "De knop die de laadpaal na het netladen terugzet naar laden op zon (bij Wallbox: schema hervatten).": "Der Knopf, der die Ladestation nach dem Netzladen zurück auf Laden mit Sonne stellt (Wallbox: Zeitplan fortsetzen).", "Geen: HESC schat het zelf. Je kunt de accustand ook zelf invullen op de startpagina of je telefoon.": "Keiner: HESC schätzt ihn selbst. Du kannst den Akkustand auch selbst auf der Startseite oder am Handy eingeben.", "Waaruit HESC ziet of de auto aan de laadpaal hangt: een aan/uit-sensor of de status van de laadpaal.": "Woran HESC sieht, ob das Auto an der Ladestation hängt: ein Ein/Aus-Sensor oder der Status der Ladestation.", "Aan: vindt HESC een betere sensor dan de gekozen, dan neemt hij die zelf. Uit: je keuze blijft staan.": "An: findet HESC einen besseren Sensor als den gewählten, nimmt es den. Aus: deine Wahl bleibt.", "Het vermogen van je thuisaccu(s). + = laden. Per accu één sensor, of één totaal-sensor; niet allebei.": "Die Leistung deiner Hausakkus. + = laden. Ein Sensor pro Akku, oder ein Gesamtsensor; nicht beides.", "Aan: HESC laadt ook buiten je planning als de stroom goedkoop is, tenzij de zon het later die dag dekt.": "An: HESC lädt auch außerhalb deiner Planung, wenn Strom günstig ist, außer die Sonne deckt es später am Tag.", "Let op: de totaal-sensor telt andersom dan de losse accu's. HESC rekent met + = laden; kijk welke klopt.": "Achtung: der Gesamtsensor zählt umgekehrt als die einzelnen Akkus. HESC rechnet mit + = laden; prüfe, was stimmt.", "Zoveel minuten voor de klaar-tijd kijkt HESC nog één keer of de auto het doel haalt, en laadt anders bij.": "So viele Minuten vor der Fertig-Zeit prüft HESC noch einmal, ob das Auto sein Ziel erreicht, und lädt sonst nach.", "Standaard: wat je af en toe wilt bijstellen, zoals meldingen, goedkope kansen, de thuisaccu en de back-up.": "Standard: was du ab und zu anpassen willst, wie Meldungen, günstige Gelegenheiten, den Hausakku und die Sicherung.", "Aan: komt de auto thuis met minder dan de minimale accustand, dan laadt HESC hem eerst snel tot dat niveau.": "An: kommt das Auto mit weniger als dem Mindest-Akkustand nach Hause, lädt HESC es zuerst schnell bis dahin.", "Hoeveel kWh je auto echt kan laden (staat in de handleiding). HESC leest het uit de auto als die het meldt.": "Wie viele kWh dein Auto wirklich laden kann (steht im Handbuch). HESC liest es aus dem Auto, wenn es das meldet.", "De stand van je laadpaal die nu laden betekent. Alleen nodig als je laadpaal geen start/stop-schakelaar heeft.": "Der Modus deiner Ladestation, der jetzt laden bedeutet. Nur nötig, wenn deine Ladestation keinen Start/Stopp-Schalter hat.", "HESC stuurt dan niets meer aan: de laadpaal laadt zoals hij zelf staat ingesteld, zonder zon- of prijsplanning.": "HESC steuert dann nichts mehr: die Ladestation lädt, wie sie selbst eingestellt ist, ohne Sonnen- oder Preisplanung.", "Weet je het niet, laat dan 16 A staan. Bij Easee, Peblar en Wallbox leest HESC dit straks zelf uit de laadpaal.": "Wenn du es nicht weißt, lass 16 A stehen. Bei Easee, Peblar und Wallbox liest HESC das bald selbst aus der Ladestation.", "Zet de afstelling terug: drempels, tijden, advies en eindcontrole. Sensoren, doelen, prijzen en kosten blijven.": "Die Feineinstellung zurücksetzen: Schwellen, Zeiten, Empfehlung und Endkontrolle. Sensoren, Ziele, Preise und Kosten bleiben.", "Expert: laadregels, HPVC, weerstation, advies en kickstart. Zelden nodig; wie het simpel houdt, komt hier nooit.": "Experte: Laderegeln, HPVC, Wetterstation, Empfehlung und Kickstart. Selten nötig; wer es einfach hält, kommt nie hierher.", "Onder dit verwachte zonvermogen stopt HESC weer. Iets lager dan de start, zodat hij niet steeds aan en uit gaat.": "Unter dieser erwarteten Solarleistung stoppt HESC wieder. Etwas niedriger als der Start, damit es nicht ständig an und aus geht.", "Zoekt de sensoren en schakelaars van je laadpaal opnieuw op, bijvoorbeeld na een update van de laadpaal-integratie.": "Sucht die Sensoren und Schalter deiner Ladestation neu, z. B. nach einem Update der Ladestations-Integration.", "Alleen nodig als de verwachting in een attribuut van de sensor staat (bijvoorbeeld estimate10). Leeg = de waarde zelf.": "Nur nötig, wenn die Prognose in einem Attribut des Sensors steht (z. B. estimate10). Leer = der Wert selbst.", "Aan: HESC zorgt dat je thuisaccu en je auto elkaar niet in de weg zitten (kickstart en pauze). Alleen met een thuisaccu.": "An: HESC sorgt dafür, dass sich Hausakku und Auto nicht in die Quere kommen (Kickstart und Pause). Nur mit Hausakku.", "Welke sensoren en schakelaars van je laadpaal HESC gebruikt. Meestal vindt HESC ze zelf; voorstel is wat HESC het best vindt.": "Welche Sensoren und Schalter deiner Ladestation HESC nutzt. Meist findet HESC sie selbst; Vorschlag ist, was HESC am besten findet.", "een eigen laadpaal, dan laat HESC die ook met rust. Een andere auto gaat gewoon door, ook als die dezelfde laadpaal gebruikt.": "eine eigene Ladestation, lässt HESC auch die in Ruhe. Ein anderes Auto lädt einfach weiter, auch an derselben Ladestation.", "Het rapport opent in een nieuw tabblad. Met \"Rapport downloaden\" bewaar je het als één bestand; daarin zitten ook de gegevens.": "Der Bericht öffnet sich in einem neuen Tab. Mit „Bericht herunterladen“ speicherst du ihn als eine Datei; darin sind auch die Daten.", "Kies de maand of het jaar. Bij twee auto's zie je het totaal en per auto een regel; de balkjes per dag in de kleur van de auto.": "Wähle den Monat oder das Jahr. Bei zwei Autos siehst du die Summe und eine Zeile pro Auto; die Balken pro Tag in der Farbe des Autos.", ": het kijkt mee en schakelt niets. Zet hem aan op de startpagina als je zover bent. Alles kun je later wijzigen bij Instellingen.": ": es schaut zu und schaltet nichts. Schalte es auf der Startseite ein, wenn du so weit bist. Alles kannst du später in den Einstellungen ändern.", "Maakt eerst een back-up en zet dan alleen de afstelling terug (drempels, tijden, advies). Sensoren, doelen, prijzen en kosten blijven.": "Erstellt zuerst eine Sicherung und setzt dann nur die Feineinstellung zurück (Schwellen, Zeiten, Empfehlung). Sensoren, Ziele, Preise und Kosten bleiben.", "Waar HESC de stroomprijzen vandaan haalt. De meeste bronnen vindt HESC zelf; bij Prijslijst in een sensor kies je de sensor hieronder.": "Woher HESC die Strompreise holt. Die meisten Quellen findet HESC selbst; bei Preisliste in einem Sensor wählst du den Sensor unten.", "Je auto: hoe groot de accu is, wanneer hij vol is en of hij een minimumlading krijgt. Het labeltje ⏻ zet HESC voor deze auto aan of uit.": "Dein Auto: wie groß der Akku ist, wann er voll ist und ob er eine Mindestladung bekommt. Das Etikett ⏻ schaltet HESC für dieses Auto ein oder aus.", "Beide auto's laden aan dezelfde laadpaal. De auto die 's avonds aan de paal hangt laadt eerst; de andere nadat jij de kabel hebt omgezet.": "Beide Autos laden an derselben Ladestation. Das Auto, das abends angesteckt ist, lädt zuerst; das andere, nachdem du das Kabel umgesteckt hast.", "Een export van je HESC zelf: instellingen, planning en wat HESC geleerd heeft. Om te bewaren, te delen op een forum of bij een foutmelding.": "Ein Export deines HESC selbst: Einstellungen, Planung und was HESC gelernt hat. Zum Aufbewahren, zum Teilen in einem Forum oder bei einer Fehlermeldung.", "Basis: wat elke installatie nodig heeft: je laadpaal, je auto('s), de prijzen en HESC aan/uit. Meestal vult de eerste start dit al voor je in.": "Basis: was jede Installation braucht: deine Ladestation, dein(e) Auto(s), die Preise und HESC an/aus. Meist füllt der erste Start das schon für dich aus.", "Wanneer HESC op zon begint en blijft laden: op de verwachting, en als je wilt ook op je eigen weerstation. Het advies kan deze drempels voor je bijstellen.": "Wann HESC mit Sonne startet und weiterlädt: nach der Prognose, und wenn du willst auch nach deiner eigenen Wetterstation. Die Empfehlung kann diese Schwellen für dich anpassen.", "HESC laadt de auto dan meteen van het net, ook als stroom nu duur is of er geen zon is, tot de accu op dit doel staat. Je planning wacht zolang. Stoppen kan altijd.": "HESC lädt das Auto dann sofort aus dem Netz, auch wenn Strom gerade teuer ist oder keine Sonne scheint, bis der Akku dieses Ziel erreicht. Deine Planung wartet so lange. Stoppen geht immer.", "Heb je een eigen weerstation met een zonlichtsensor (W/m²)? Dan kan HESC starten op het zonlicht dat nu echt valt, in plaats van alleen op de verwachting. Uit = alleen de verwachting.": "Hast du eine eigene Wetterstation mit Sonnenlichtsensor (W/m²)? Dann kann HESC auf das Sonnenlicht starten, das gerade wirklich fällt, statt nur auf die Prognose. Aus = nur die Prognose.", "Hoe ging het laden op zon: een samenvatting, het advies, een overzicht per dag, hoe betrouwbaar je sensoren waren en hoe goed de zonverwachting klopte. Om te begrijpen wat HESC gedaan heeft.": "Wie das Laden mit Sonne lief: eine Zusammenfassung, die Empfehlung, eine Übersicht pro Tag, wie zuverlässig deine Sensoren waren und wie gut die Solarprognose stimmte. Um zu verstehen, was HESC getan hat.", "HESC houdt hiermee het laden binnen de aansluiting als comfort. Jij blijft verantwoordelijk dat je elektrische installatie niet overbelast raakt; dat regelen laadpaal, load balancer en installateur.": "HESC hält damit das Laden als Komfort innerhalb des Anschlusses. Du bleibst dafür verantwortlich, dass deine Elektroinstallation nicht überlastet wird; das regeln Ladestation, Lastmanager und Installateur.", "Een herinnering op je telefoon als de auto 's avonds niet aan de laadpaal hangt terwijl er morgen geladen moet worden. Kies hoe laat. De melding gaat naar de telefoons bij Instellingen › Standaard › Meldingen.": "Eine Erinnerung auf dem Handy, wenn das Auto abends nicht an der Ladestation hängt, obwohl morgen geladen werden muss. Wähle die Uhrzeit. Die Meldung geht an die Handys bei Einstellungen › Standard › Meldungen.", "De komende zeven dagen per auto: accu-% en klaar-tijd. Tik op een auto of een dag om die auto te plannen.\\n\\nOranje rand = uitzondering: alleen deze keer, overgeslagen of een dag uit. Vette tekst = dag met eigen tijd of %.": "Die nächsten sieben Tage pro Auto: Akku-% und Fertig-Zeit. Tippe auf ein Auto oder einen Tag, um dieses Auto zu planen.\\n\\nOranger Rand = Ausnahme: nur dieses Mal, übersprungen oder ein freier Tag. Fetter Text = Tag mit eigener Zeit oder %.", "Welke telefoons HESC-meldingen krijgen (alle apparaten met de Home Assistant-app staan erbij). Testmelding: probeer het uit. Ochtendoverzicht: één bericht per dag met de accustand, het volgende plan, de zon vandaag en gisteren.": "Welche Handys HESC-Meldungen bekommen (alle Geräte mit der Home-Assistant-App stehen dabei). Testmeldung: ausprobieren. Morgenübersicht: eine Nachricht pro Tag mit Akkustand, dem nächsten Plan, der Sonne heute und gestern.", "Het vaste ritme van deze auto. Kies één standaard (klaar om, accu-%) en zet per weekdag aan of uit.\\n\\nTik op een dag om die dag aan of uit te zetten, of een eigen tijd of % te geven. Een dag met eigen waarden heeft vette tekst.": "Der feste Rhythmus dieses Autos. Wähle einen Standard (fertig um, Akku-%) und schalte jeden Wochentag ein oder aus.\\n\\nTippe auf einen Tag, um ihn ein- oder auszuschalten oder ihm eine eigene Zeit oder % zu geben. Ein Tag mit eigenen Werten hat fetten Text.", "Hoe HESC de kosten rekent. **Waarde van een kWh zon:** wat je misloopt aan terugleververgoeding (0 = zon is gratis). Is de prijs uit je prijsbron al **all-in** (belasting, opslag, btw), zet dat aan; anders vul je opslag en btw in. Een wijziging rekent de hele geschiedenis opnieuw.": "Wie HESC die Kosten berechnet. **Wert einer kWh Sonne:** was dir an Einspeisevergütung entgeht (0 = Sonne ist gratis). Ist der Preis aus deiner Preisquelle schon **all-in** (Steuern, Aufschlag, MwSt.), schalte das ein; sonst trägst du Aufschlag und MwSt. ein. Eine Änderung berechnet die ganze Historie neu.", "**HESC aan/uit** is de hoofdschakelaar: uit = HESC doet helemaal niets. **Schaduwmodus** aan = HESC rekent en plant gewoon mee en laat zien wat hij zou doen, maar stuurt de laadpaal niet aan. Handig om eerst te kijken. Dezelfde schaduwmodus zit ook in de knop Live · stuurt bovenaan.": "**HESC an/aus** ist der Hauptschalter: aus = HESC tut gar nichts. **Schattenmodus** an = HESC rechnet und plant ganz normal mit und zeigt, was es tun würde, steuert die Ladestation aber nicht. Praktisch, um erst zuzuschauen. Derselbe Schattenmodus steckt auch im Knopf Live · steuert oben.", "Wie gaat voor en waarom.\\n\\n- Moeten beide op dezelfde tijd klaar zijn, dan gaat de auto voor die de meeste kWh nodig heeft.\\n- Zelfde tijd en zelfde kWh: de eerste auto gaat voor.\\n- Wisselen gebeurt alleen op een heel kwartier.\\n- **(geschat)** betekent: de accustand van die auto meldt niets, HESC rekent met een schatting.": "Wer Vorrang hat und warum.\\n\\n- Müssen beide zur selben Zeit fertig sein, hat das Auto Vorrang, das die meisten kWh braucht.\\n- Gleiche Zeit und gleiche kWh: das erste Auto hat Vorrang.\\n- Gewechselt wird nur zur vollen Viertelstunde.\\n- **(geschätzt)** heißt: der Akkustand dieses Autos meldet nichts, HESC rechnet mit einer Schätzung.", "Wat het laden kostte, per dag, week, maand en jaar, van zon en van het net. **Laadkosten exporteren** (bij Instellen) zet de kosten per dag en per maand in twee spreadsheet-bestanden (CSV) in de map hesc_v4 van Home Assistant, om in Excel te openen. Het **Rapport** (knop bovenaan) is iets anders: een overzicht van je hele HESC, om te bewaren of te delen.": "Was das Laden gekostet hat, pro Tag, Woche, Monat und Jahr, aus Sonne und aus dem Netz. **Ladekosten exportieren** (bei Einstellen) legt die Kosten pro Tag und pro Monat in zwei Tabellendateien (CSV) im Ordner hesc_v4 von Home Assistant ab, zum Öffnen in Excel. Der **Bericht** (Knopf oben) ist etwas anderes: eine Übersicht deines ganzen HESC, zum Aufbewahren oder Teilen.", "Je auto's en laadpalen. HESC stuurt er maximaal twee van elk. **+ Auto toevoegen:** een tweede auto, op dezelfde laadpaal of met een eigen. **+ Laadpaal toevoegen:** als twee auto's één laadpaal delen, krijgt auto 2 een eigen laadpaal. **Verwijderen** kan alleen voor auto 2 en laadpaal 2; HESC laat eerst zien wat er weggaat. Laadkosten en geschiedenis worden niet gewist maar bewaard.": "Deine Autos und Ladestationen. HESC steuert höchstens zwei von jedem. **+ Auto hinzufügen:** ein zweites Auto, an derselben Ladestation oder mit einer eigenen. **+ Ladestation hinzufügen:** teilen sich zwei Autos eine Ladestation, bekommt Auto 2 eine eigene. **Entfernen** geht nur für Auto 2 und Ladestation 2; HESC zeigt zuerst, was wegfällt. Ladekosten und Historie werden nicht gelöscht, sondern aufbewahrt.", "Een uitzondering voor de eerstvolgende keer. Daarna gaat HESC vanzelf terug naar het ritme. Laagste doel overal 15%: daaronder laadt de auto zijn 12V-accu niet meer bij.\\n\\n- **Overslaan:** de eerstvolgende lading vervalt.\\n- **Andere tijd of %:** alleen voor de eerstvolgende keer.\\n- **Nu laden tot:** laadt meteen, los van zon en prijs.\\n\\nVervangt in v3: plan voor één dag, één dag overslaan en nu laden tot.": "Eine Ausnahme für das nächste Mal. Danach kehrt HESC von selbst zum Rhythmus zurück. Niedrigstes Ziel überall 15%: darunter lädt das Auto seinen 12-V-Akku nicht mehr nach.\\n\\n- **Überspringen:** die nächste Ladung entfällt.\\n- **Andere Zeit oder %:** nur für das nächste Mal.\\n- **Jetzt laden bis:** lädt sofort, unabhängig von Sonne und Preis.\\n\\nErsetzt in v3: Plan für einen Tag, einen Tag überspringen und jetzt laden bis.", "De maand met het ritme erin. Tik op een dag om hem **uit** te zetten (oranje streep), of een vrije dag **aan** met de standaardwaarden (gestreepte rand). Nog een keer tikken zet de dag terug naar het ritme.\\n\\nZo plan je ploegendienst of een dagje uit vooruit.\\n\\n**Vakantie:** tik op **+ Vakantie**, dan op de eerste en de laatste dag. Met de muis kun je ook van de eerste naar de laatste dag slepen. Al die dagen gaan uit; na de laatste dag gaat het ritme vanzelf verder. Tik in de vakantie of op ✕ om hem te stoppen.\\n\\n**Eén dag aanpassen:** tik twee keer snel op een dag. Dan kies je voor alleen die dag de tijd en de accu %.": "Der Monat mit dem Rhythmus. Tippe auf einen Tag, um ihn **aus**zuschalten (oranger Streifen), oder einen freien Tag **an** mit den Standardwerten (gestreifter Rand). Nochmal tippen setzt den Tag zurück auf den Rhythmus.\\n\\nSo planst du Schichtdienst oder einen Ausflug im Voraus.\\n\\n**Urlaub:** tippe auf **+ Urlaub**, dann auf den ersten und den letzten Tag. Mit der Maus kannst du auch vom ersten bis zum letzten Tag ziehen. Alle diese Tage gehen aus; nach dem letzten Tag geht der Rhythmus von selbst weiter. Tippe in den Urlaub oder auf ✕, um ihn zu beenden.\\n\\n**Einen Tag ändern:** tippe zweimal schnell auf einen Tag. Dann wählst du Zeit und Akku-% nur für diesen Tag.", "Waar HESC zijn meldingen naartoe stuurt, als lijst van Home Assistant-meldingsdiensten (komma-gescheiden). **In Standaard** kies je met knoppen een telefoon met de Home Assistant-app; dat komt hier vanzelf in te staan. **Hier** kun je daarnaast elke andere meldingsdienst intypen die Home Assistant kent, bijvoorbeeld `notify.telegram`, `notify.email` of een groep van meerdere telefoons. Zo krijg je HESC-meldingen ook buiten de app. Laat je het leeg, dan stuurt HESC geen meldingen.": "Wohin HESC seine Meldungen schickt, als Liste von Home-Assistant-Benachrichtigungsdiensten (durch Komma getrennt). **In Standard** wählst du mit Knöpfen ein Handy mit der Home-Assistant-App; das erscheint dann von selbst hier. **Hier** kannst du außerdem jeden anderen Benachrichtigungsdienst eintippen, den Home Assistant kennt, z. B. `notify.telegram`, `notify.email` oder eine Gruppe mehrerer Handys. So bekommst du HESC-Meldungen auch außerhalb der App. Lässt du es leer, schickt HESC keine Meldungen.", "Zonverwachting": "Solarprognose", "Live": "Live", "Periode": "Zeitraum", "Periode laadkosten": "Zeitraum Ladekosten", "Instellen": "Einstellen", "Terugleververgoeding": "Einspeisevergütung", "Kosten: prijs is all-in": "Kosten: Preis ist all-in", "Kosten: opslag per kWh (energiebelasting + leverancier)": "Kosten: Aufschlag pro kWh (Energiesteuer + Lieferant)", "Kosten: btw": "Kosten: MwSt.", "Laadkosten exporteren": "Ladekosten exportieren", "Geladen": "Geladen", "Van de zon": "Von der Sonne", "Van het net": "Aus dem Netz", "Kosten net": "Netzkosten", "Waarde zon (teruglevering)": "Wert Sonne (Einspeisung)", "Gemiddeld": "Durchschnitt", "niet geladen": "nicht geladen", "Startdrempel": "Startschwelle", "Doorlaaddrempel": "Weiterladeschwelle", "Verwacht laden op zon": "Erwartetes Laden mit Sonne", "Zon": "Sonne", "Verwachting": "Prognose", "Kalender": "Kalender", "Ritme": "Rhythmus", "ritme": "Rhythmus", "extra dag": "Extratag", "dag uit": "freier Tag", "vrij": "frei", "geweest": "vorbei", "standaard klaar om": "Standard fertig um", "standaard accu": "Standard-Akku", "Alleen deze keer": "Nur dieses Mal", "Overslaan": "Überspringen", "Andere tijd of %": "Andere Zeit oder %", "Type laadpaal": "Ladestationstyp", "Accucapaciteit": "Akkukapazität", "Minimumlading": "Mindestladung", "Minimale accustand": "Mindest-Akkustand", "Minimumlading binnen": "Mindestladung innerhalb", "Prijsbron": "Preisquelle", "Nord Pool (officieel)": "Nord Pool (offiziell)", "Sensor dagprijzen": "Sensor Tagespreise", "Prijzen per": "Preise pro", "Automatisch": "Automatisch", "Per kwartier": "Pro Viertelstunde", "Valuta": "Währung", "HESC staat aan": "HESC ist an", "HESC staat uit": "HESC ist aus", "vast": "fest", "HESC stuurt maximaal twee auto's.": "HESC steuert höchstens zwei Autos.", "Laadpalen": "Ladestationen", "HESC stuurt maximaal twee laadpalen.": "HESC steuert höchstens zwei Ladestationen.", "Basis": "Basis", "Expert": "Experte", "Goedkope kansen": "Günstige Gelegenheiten", "Laadplan: goedkope kansen pakken": "Ladeplan: günstige Gelegenheiten nutzen", "Laadplan: prijs voor een goedkope kans": "Ladeplan: Preis für eine günstige Gelegenheit", "Back-up": "Sicherung", "in orde": "in Ordnung", "✓ in orde": "✓ in Ordnung", "Waarde laadstand 'nu laden'": "Wert Lademodus „jetzt laden“", "Startdrempel per seizoen": "Startschwelle pro Jahreszeit", "stabiel": "stabil", "HPVC gebruiken": "HPVC nutzen", "Zonnestroom en net uit HPVC": "Solarstrom und Netz aus HPVC", "Advies automatisch toepassen": "Empfehlung automatisch anwenden", "Meldingsdiensten": "Benachrichtigungsdienste", "Laadrapport": "Ladebericht", "Laadrapport maken": "Ladebericht erstellen", "Laadrapport gemaakt": "Ladebericht erstellt", "Laadrapport openen": "Ladebericht öffnen", "Volledige back-up": "Vollständige Sicherung", "Automatische bronnen wijzigen": "Quellen automatisch ändern", "Verwacht vermogen over 30 min": "Erwartete Leistung in 30 Min.", "Kabel wisselen": "Kabel umstecken", "Planning": "Planung", "ma": "Mo", "di": "Di", "wo": "Mi", "do": "Do", "vr": "Fr", "za": "Sa", "zo": "So", "Ma": "Mo", "Di": "Di", "Wo": "Mi", "Do": "Do", "Vr": "Fr", "Za": "Sa", "Zo": "So", "start": "Start", "kickstart": "Kickstart", "Uitzetten": "Ausschalten", "Aanzetten": "Einschalten", "Het merk van je tweede laadpaal. Daarmee zoekt HESC zelf de schakelaars en sensoren op.": "Die Marke deiner zweiten Ladestation. Damit sucht HESC die Schalter und Sensoren selbst.", "Voorbeeld; het echte rekenwerk komt in de alpha.": "Beispiel; die echte Berechnung kommt in der Alpha.", "Instellingen terugzetten": "Einstellungen wiederherstellen", "tik de standen aan die laden op zon betekenen": "die Modi ankreuzen, die Laden mit Sonne bedeuten", "tik de standen aan die betekenen: geen auto": "die Zustände ankreuzen, die bedeuten: kein Auto", "Kies er minstens één.": "Wähle mindestens einen.", "wordt opgeslagen": "wird gespeichert", "Kabel omzetten": "Kabel umstecken", "Kabel omzetten uiterlijk om": "Kabel spätestens umstecken um", "Herinnering op je telefoon": "Erinnerung auf dem Handy", "Twee auto's aan één laadpaal: de eerste auto laadt vóór dit tijdstip, de andere erna. Op dit tijdstip krijg je een herinnering op je telefoon om de kabel om te zetten, als de eerste auto er nog aan hangt en de andere een plan heeft. HESC plant met dit tijdstip.": "Zwei Autos an einer Ladestation: das erste Auto lädt vor dieser Uhrzeit, das andere danach. Zu dieser Uhrzeit bekommst du eine Erinnerung auf dein Handy, das Kabel umzustecken, wenn das erste Auto noch angesteckt ist und das andere einen Plan hat. HESC plant mit dieser Uhrzeit.", "Laadkosten downloaden": "Ladekosten herunterladen", "per dag": "pro Tag", "per maand": "pro Monat", "Download de laatste export als spreadsheetbestand (CSV), per dag of per maand. Druk eerst op Uitvoeren bij Laadkosten exporteren.": "Lade den letzten Export als Tabellendatei (CSV) herunter, pro Tag oder pro Monat. Drücke zuerst Ausführen bei Ladekosten exportieren.", "Druk eerst op Uitvoeren bij Laadkosten exporteren.": "Drücke zuerst Ausführen bei Ladekosten exportieren.", "Aan": "Ein", "Accustand auto (verklaart stops, bijv. auto vol)": "Akkustand Auto (erklärt Stopps, z. B. Auto voll)", "Alle instellingen van HESC terugzetten naar de laatste back-up?": "Alle Einstellungen von HESC aus der letzten Sicherung wiederherstellen?", "Attribuut van de verwachting (leeg = toestand)": "Attribut der Prognose (leer = Zustand)", "Auto aangesloten (binaire of statussensor)": "Auto angeschlossen (Binär- oder Statussensor)", "Auto telt als ladend boven": "Auto gilt als ladend über", "Auto telt als vol bij": "Auto gilt als voll bei", "Drempels, tijden en advies terugzetten naar de standaardwaarden van HESC? Eerst wordt er een back-up gemaakt, dus je kunt dit ongedaan maken": "Schwellen, Zeiten und Rat auf die Standardwerte von HESC zurücksetzen? Vorher wird eine Sicherung gemacht, du kannst es also rückgängig machen", "Eindcontrole voor de klaar-tijd (0 = uit)": "Schlusskontrolle vor der Fertig-Zeit (0 = aus)", "Entiteit voor de laadstand": "Entität für den Lademodus", "Meldingen naar je telefoon": "Benachrichtigungen an dein Telefon", "Meldingsdiensten (gevuld door de lijst hierboven; zo nodig met de hand aanpassen)": "Benachrichtigungsdienste (aus der Liste oben gefüllt; bei Bedarf von Hand ändern)", "Minimale zon over voor de auto": "Mindestens übrige Sonne für das Auto", "Netsensor: teruglevering is positief (uit = afname positief, de meeste meters)": "Netzsensor: Einspeisung ist positiv (aus = Bezug positiv, die meisten Zähler)", "Prijs uit de prijsbron is al all-in": "Preis aus der Preisquelle ist schon all-in", "Prijssensor (met een prijslijst, of een sensor van EnergyZero / EasyEnergy / Tibber / Nord Pool official)": "Preissensor (mit einer Preisliste, oder ein Sensor von EnergyZero / EasyEnergy / Tibber / Nord Pool official)", "Prijzen per (Automatic volgt de bron; Per hour = je leverancier rekent per uur af)": "Preise pro (Automatic folgt der Quelle; Per hour = dein Anbieter rechnet pro Stunde ab)", "Schakelaar HPVC aan/uit": "Schalter HPVC an/aus", "Sensor(en) vermogen thuisbatterij, + = laden": "Leistungssensor(en) Hausakku, + = Laden", "Standen voor laden op zon": "Modi für Laden mit Sonne", "Startdrempel per seizoen (zet de twee hieronder elke maand)": "Startschwelle pro Saison (stellt die zwei unten jeden Monat ein)", "Statuswaarden die \"geen auto\" betekenen (alleen bij een statussensor)": "Statuswerte, die \"kein Auto\" bedeuten (nur bei einem Statussensor)", "Teller zonne-energie (kWh uit zon in het rapport)": "Zähler Solarenergie (kWh aus Sonne im Bericht)", "Valuta (Automatic volgt de prijssensor)": "Währung (Automatic folgt dem Preissensor)", "Verwacht vermogen om door te laden": "Erwartete Leistung zum Weiterladen", "Waarde van een kWh zon (terugleververgoeding, 0 = gratis)": "Wert einer kWh Sonne (Einspeisevergütung, 0 = kostenlos)", "Waarde(n) die laden op zon betekenen, gescheiden door komma's": "Wert(e), die Laden mit Sonne bedeuten, durch Kommas getrennt", "Wachten tot de laadpaal start": "Warten, bis die Wallbox startet", "Zonlicht om door te laden": "Sonnenlicht zum Weiterladen", "Zonverwachting morgen (bijv. Solcast forecast tomorrow)": "PV-Prognose morgen (z. B. Solcast forecast tomorrow)", "…of laadstandwaarde die 'nu laden' betekent": "…oder Lademoduswert, der 'jetzt laden' bedeutet", "Een tweede laadpaal hoort bij een tweede auto: kies bij \"+ Auto toevoegen\" voor een eigen laadpaal.": "Eine zweite Wallbox gehört zu einem zweiten Auto: wähle \"+ Auto hinzufügen\" für eine eigene Wallbox.", "Thuisbatterij en EV": "Hausakku und E-Auto", "Vink per thuisbatterij één sensor aan ·": "Pro Hausakku einen Sensor ankreuzen ·", "Hoeveel kWh je thuisbatterijen samen kunnen opslaan.": "Wie viele kWh deine Hausakkus zusammen speichern können.", "De stand (%) van je thuisbatterij(en). Per accu één sensor, of één voor alle samen.": "Der Stand (%) deiner Hausakkus. Ein Sensor pro Akku, oder einer für alle zusammen.", "Alleen met een thuisbatterij: zo zitten je thuisbatterij en je auto elkaar niet in de weg.": "Nur mit Hausakku: so kommen sich Hausakku und Auto nicht in die Quere.", "Het vermogen van je thuisbatterij(en). + = laden. Per accu één sensor, of één totaal-sensor; niet allebei.": "Die Leistung deiner Hausakkus. + = laden. Ein Sensor pro Akku, oder ein Gesamtsensor; nicht beides.", "Standaard: wat je af en toe wilt bijstellen, zoals meldingen, goedkope kansen, de thuisbatterij en de back-up.": "Standard: was du ab und zu anpassen willst, wie Meldungen, günstige Gelegenheiten, den Hausakku und die Sicherung.", "Aan: HESC zorgt dat je thuisbatterij en je auto elkaar niet in de weg zitten (kickstart en pauze). Alleen met een thuisbatterij.": "An: HESC sorgt dafür, dass sich Hausakku und Auto nicht in die Quere kommen (Kickstart und Pause). Nur mit Hausakku."}, "frag": [["Hij is nog niet aangesloten: steek de kabel erin vóór", "Es ist noch nicht angesteckt: steck das Kabel ein vor"], ["krijg je een herinnering op je telefoon", "bekommst du eine Erinnerung auf dein Handy"], ["Prijs, zonverwachting en accustand van", "Preis, Solarprognose und Akkustand von"], ["Advies op basis van de laatste", "Empfehlung auf Basis der letzten"], ["HESC stuurt deze auto niet", "HESC steuert dieses Auto nicht"], ["Er is geen laden gepland.", "Kein Laden geplant."], ["Hij is niet aangesloten.", "Es ist nicht angesteckt."], ["geldt voor beide auto's", "gilt für beide Autos"], ["voor de komende 24 uur", "für die nächsten 24 Stunden"], ["Auto vol bij accustand", "Auto voll bei Akkustand"], ["de rest gratis op zon", "der Rest gratis mit Sonne"], ["daarna weer het ritme", "danach wieder der Rhythmus"], ["HESC stuurt deze auto", "HESC steuert dieses Auto"], ["geen netladen gepland", "kein Netzladen geplant"], ["Geen auto aangesloten", "Kein Auto angeschlossen"], ["tik om uit te zetten", "tippen zum Ausschalten"], ["tik om aan te zetten", "tippen zum Einschalten"], ["Hij is aangesloten.", "Es ist angesteckt."], ["op zijn vroegst om", "frühestens um"], ["van het net samen", "aus dem Netz zusammen"], ["De accu gaat van", "Der Akku geht von"], ["klaar vandaag om", "fertig heute um"], ["Verwachte kosten", "Erwartete Kosten"], ["laatste 12 weken", "letzte 12 Wochen"], ["alleen deze keer", "nur dieses Mal"], ["terug naar ritme", "zurück zum Rhythmus"], ["niet aangesloten", "nicht angeschlossen"], ["klaar morgen om", "fertig morgen um"], ["u laden op zon", "Std. Laden mit Sonne"], ["Batterijniveau", "Batteriestand"], ["Eerstvolgende", "Nächstes"], ["een stand van", "ein Modus von"], ["Goedkope kans", "Günstige Chance"], ["niet gevonden", "nicht gefunden"], ["Laadt nu met", "Lädt jetzt mit"], ["geteld sinds", "gezählt seit"], ["Nu laden tot", "Jetzt laden bis"], ["verwijderen?", "– entfernen?"], ["van het net", "aus dem Netz"], ["aangesloten", "angeschlossen"], ["deze maand", "diesen Monat"], ["slaat over", "überspringt"], ["uiterlijk", "spätestens"], ["deze keer", "dieses Mal"], ["ontbreekt", "fehlt"], ["per maand", "pro Monat"], ["Laadstand", "Lademodus"], ["klaar om", "fertig um"], ["laadt nu", "lädt jetzt"], ["vannacht", "heute Nacht"], ["vanavond", "heute Abend"], ["Vakantie", "Urlaub"], ["laadpaal", "Ladestation"], ["Laadpaal", "Ladestation"], ["Planning", "Planung"], ["Kalender", "Kalender"], ["Omvormer", "Wechselrichter"], ["onbekend", "unbekannt"], ["vandaag", "heute"], ["Totalen", "Summen"], ["gekozen", "gewählt"], ["per kWh", "pro kWh"], ["per dag", "pro Tag"], ["Accu nu", "Akku jetzt"], ["op zon", "mit Sonne"], ["morgen", "morgen"], ["daarna", "danach"], ["opslag", "Aufschlag"], ["alleen", "nur"], ["Laadt", "Lädt"], ["prijs", "Preis"], ["Ritme", "Rhythmus"], ["laadt", "lädt"], ["klaar", "fertig"], ["naar", "auf"], ["voor", "für"], ["auto", "Auto"], ["accu", "Akku"], ["doel", "Ziel"], ["van", "von"], ["tot", "bis"], ["zon", "Sonne"], ["net", "Netz"], ["btw", "MwSt."], ["Om", "Um"], ["om", "um"], ["en", "und"], ["nu", "jetzt"]]}};
function hv4Lang() {
  let o = null; try { o = localStorage.getItem("hesc-v4-lang"); } catch (e) { /* private window */ }
  if (o === "nl" || o === "en" || o === "de") return o;
  const ha = document.querySelector("home-assistant"), h = ha && ha.hass;
  const l = String((h && ((h.locale && h.locale.language) || h.language)) || "nl").slice(0, 2).toLowerCase();
  return l === "nl" ? "nl" : l === "de" ? "de" : "en";
}
// the same text written slightly differently still counts: real line breaks or "\n", with or without **bold**
const hv4Norm = (k) => k.replace(/\\n/g, "\n").replace(/\*\*/g, "").replace(/\s+/g, " ").trim();
for (const L of Object.values(HV4_I18N)) { L.norm = {}; for (const [k, v] of Object.entries(L.exact)) L.norm[hv4Norm(k)] = v.replace(/\\n/g, "\n"); }
// fragments only replace whole words: "van" never changes "vandaag"
for (const L of Object.values(HV4_I18N)) L.frag = L.frag.map(([a, b]) => [a, b, new RegExp("(?<![\\p{L}\\p{N}])" + a.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![\\p{L}\\p{N}])", "gu")]);
// a list of names (days, months) that follows the language each time it is read
const hv4Arr = (by) => new Proxy([], { get: (_t, k) => { const a = by[hv4Lang()] || by.nl, v = a[k]; return typeof v === "function" ? v.bind(a) : v; } });
const hv4Loc = () => ({ nl: "nl-NL", de: "de-DE", en: "en-GB" })[hv4Lang()];
const HV4_NL = /\b(de|het|een|van|niet|naar|wordt|laadt|laden|kies|geen|voor|met|bij|zon|auto|laadpaal|vandaag|morgen|vannacht|klaar|uit|aan|nu|kosten|instellingen)\b/i;
window.__hv4Miss = window.__hv4Miss || new Set();
const hv4Done = new WeakMap(); // node -> the text we gave it (so a translated text is not translated again)
function hv4Tx(s) { // one text: exact, else fragments; the Dutch text when nothing fits
  const L = HV4_I18N[hv4Lang()]; if (!L || !s) return s;
  const m = /^(\s*)([\s\S]*?)(\s*)$/.exec(s), core = m[2]; if (!core) return s;
  if (L.exact[core] !== undefined) return m[1] + L.exact[core] + m[3];
  const nk = hv4Norm(core); if (L.norm[nk] !== undefined) return m[1] + L.norm[nk] + m[3];
  let out = core; for (const [a, b, re] of L.frag) if (out.includes(a)) out = out.replace(re, b);
  if (out === core && HV4_NL.test(core) && /[a-z]{3}/.test(core)) window.__hv4Miss.add(core);
  return m[1] + out + m[3];
}
const HV4_INLINE = new Set(["B", "I", "BR", "SMALL", "STRONG", "EM", "U", "CODE", "A", "SPAN"]);
function hv4Tr(root) {
  const L = HV4_I18N[hv4Lang()]; if (!L || !root) return;
  const walk = (n) => {
    if (n.nodeType === 3) { if (hv4Done.get(n) === n.data) return; const t = hv4Tx(n.data); if (t !== n.data) n.data = t; hv4Done.set(n, n.data); return; }
    if (n.nodeType !== 1 && n.nodeType !== 11) return;
    if (n.nodeType === 1) {
      if (n.tagName === "STYLE" || n.tagName === "SCRIPT") return;
      for (const a of ["title", "aria-label", "placeholder"]) { const v = n.getAttribute(a); if (v && hv4Done.get(n) !== "a" + a + v) { const t = hv4Tx(v); if (t !== v) n.setAttribute(a, t); } }
      // a text with markup (<b>, <br> ...): the whole inner HTML first, so its pieces are not translated one by one
      if (n.children.length && [...n.children].every((c) => HV4_INLINE.has(c.tagName))) {
        const k = n.innerHTML.replace(/\s+/g, " ").trim();
        if (L.exact[k] !== undefined) { n.innerHTML = L.exact[k]; n.childNodes.forEach((c) => hv4Done.set(c, c.nodeType === 3 ? c.data : true)); return; }
      }
    }
    n.childNodes.forEach(walk);
  };
  walk(root);
}
/* HESC's own text sensors carry their text per language in the attributes nl and de (rekenchat b3283f2: the advice,
 * the costs export line); the cards show that text instead of the English state. */
const hv4HL = new WeakMap();
function hv4HassLang(h) {
  const lang = hv4Lang(); if (!h || !h.states || lang === "en") return h;
  if (hv4HL.has(h)) return hv4HL.get(h);
  let states = null;
  for (const id in h.states) {
    if (!id.startsWith("sensor.hesc_v4_")) continue;
    const s = h.states[id], t = s && s.attributes && s.attributes[lang];
    if (typeof t === "string" && t && t !== s.state) { states = states || { ...h.states }; states[id] = { ...s, state: t }; }
  }
  const out = states ? { ...h, states } : h; hv4HL.set(h, out); return out;
}
/* The cards' own config (titles, names, (i) texts) is translated when the card gets it, before markdown becomes HTML. */
function hv4TrCfg(o) {
  if (hv4Lang() === "nl") return o;
  if (typeof o === "string") return hv4Tx(o);
  if (Array.isArray(o)) return o.map(hv4TrCfg);
  if (o && typeof o === "object") { const r = {}; for (const k of Object.keys(o)) r[k] = /^(type|entity|attribute|tag_power|if_entity|icon|url_path|navigation_path|car|pick|id|color|card_mod)$/.test(k) ? o[k] : hv4TrCfg(o[k]); return r; }
  return o;
}
(() => {
  const def = customElements.define.bind(customElements);
  if (customElements.define.__hv4) return;
  const d2 = function (name, cls, opts) {
    if (/^hesc-v4/.test(name) && !/first-start/.test(name) && cls && cls.prototype && typeof cls.prototype.setConfig === "function") {
      const sc = cls.prototype.setConfig;
      cls.prototype.setConfig = function (c) { return sc.call(this, hv4TrCfg(c)); };
      const d = Object.getOwnPropertyDescriptor(cls.prototype, "hass");
      if (d && d.set) Object.defineProperty(cls.prototype, "hass", { ...d, set(h) { d.set.call(this, hv4HassLang(h)); } });
    }
    return def(name, cls, opts);
  };
  d2.__hv4 = true;
  customElements.define = d2;
})();
/* Watch the panel's own elements: whatever they render (innerHTML, textContent, a new window) is translated right away. */
(() => {
  const orig = Element.prototype.attachShadow;
  if (orig.__hv4) return;
  const patched = function (init) {
    const root = orig.call(this, init);
    if (/^HESC-V4/.test(this.tagName) && !/FIRST-START/.test(this.tagName) && hv4Lang() !== "nl") {
      new MutationObserver((ms) => ms.forEach((m) => {
        if (m.type === "characterData") hv4Tr(m.target);
        else if (m.type === "attributes") hv4Tr(m.target);
        else m.addedNodes.forEach((x) => hv4Tr(x));
      })).observe(root, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ["title", "aria-label", "placeholder"] });
      queueMicrotask(() => hv4Tr(root));
    }
    return root;
  };
  patched.__hv4 = true;
  Element.prototype.attachShadow = patched;
})();
/* HESC v4 test board (proefbord) — not part of the integration yet.
 *
 * Two cards:
 *  - custom:hesc-v4-buttons   the house-style button row (main switch "Live" + round buttons that
 *                             open a window with ordinary Home Assistant cards; orange dot = action needed).
 *  - custom:hesc-v4-planning  the start page with example data for two cars (no logic behind it).
 *
 * Pattern: house style "button row with windows" (27-10-2026).
 */

/* Info shown behind an (i) button: plain text, **bold**, "- " bullets, blank line = new paragraph. */
const INFO_CSS = `.ib{flex:none;width:26px;height:26px;border-radius:50%;border:1.5px solid var(--secondary-text-color,#9aa0aa);background:none;
  color:var(--secondary-text-color,#9aa0aa);font:italic 600 14px/1 Georgia,serif;cursor:pointer;padding:0}
.ib:hover,.ib[aria-expanded=true]{border-color:var(--primary-color);color:var(--primary-color)}
.ib[hidden],.tip[hidden]{display:none}
.tip{background:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));border-left:3px solid var(--primary-color);border-radius:8px;
  padding:10px 14px;font-size:14px;line-height:1.45;color:var(--primary-text-color)}
.tip p{margin:0 0 6px}.tip p:last-child,.tip ul:last-child{margin-bottom:0}.tip ul{margin:0 0 6px;padding-left:18px}
`;
function infoHtml(text) { text = hv4Tx(String(text)); // the (i) text in the panel's language
  const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  return String(text).split(/\n\s*\n/).map((blk) => {
    const lines = blk.split("\n");
    return lines.every((l) => l.startsWith("- "))
      ? `<ul>${lines.map((l) => `<li>${esc(l.slice(2))}</li>`).join("")}</ul>`
      : `<p>${esc(blk)}</p>`;
  }).join("");
}

/* Temporary proefbord switch (besluit 30-10, nr 29): "real" = only SatScan's own car (real v3 data, one EV),
 * "demo" = the example with two cars. Kept per browser; nothing is written to Home Assistant. Remove before the release. */
const HV4_MODE_KEY = "hesc-v4-proefbord-mode";
function hv4Mode() {
  try { return localStorage.getItem(HV4_MODE_KEY) === "real" ? "real" : "demo"; } catch (e) { return "demo"; }
}
function hv4SetMode(m) {
  try { localStorage.setItem(HV4_MODE_KEY, m); } catch (e) { /* private window: switch lasts until reload */ }
  window.__hescV4Mode = m;
  window.dispatchEvent(new CustomEvent("hesc-v4-mode", { detail: { mode: m } }));
  setTimeout(() => location.reload(), 50); // decision 31-10: Demo swaps the real car for an example car; reload so every card restarts with it
}
/* decision 31-10: in Demo both cars are examples (BMW i3, BYD Atto 3 Evo); the real car's name, data and settings appear only in Echt.
 * Every card gets its config through hv4Swap: names swapped, "real" sources dropped, "demo_cards" used instead of "cards". */
const HV4_DEMO_NAMES = [["BYD Atto3", "BYD Atto 3 Evo"]];
function hv4Swap(c) {
  if (hv4Cur() === "real" || !c) return c;
  const walk = (o) => {
    if (typeof o === "string") return HV4_DEMO_NAMES.reduce((t, [a, b]) => t.split(a).join(b), o);
    if (Array.isArray(o)) return o.map(walk);
    if (o && typeof o === "object") {
      const out = {};
      for (const [k, v] of Object.entries(o)) {
        if (k === "real" || k === "demo_cards" || k === "demo_info") continue;
        out[k] = walk(k === "cards" && o.demo_cards ? o.demo_cards : v);
      }
      if (o.demo_info) out.info = walk(o.demo_info);
      return out;
    }
    return o;
  };
  return walk(c);
}
const hv4Cur = () => "real"; // HESC v4 panel: always the real cars, never the demo
/* Tokens in the panel config: {ev1} = the car's name, {ev1c} = its colour, both from HESC itself. */
function hv4Known() { const h = document.querySelector("home-assistant") && document.querySelector("home-assistant").hass, s = h && h.states["text.hesc_v4_ev1_car_name"]; return !!(s && !["unknown", "unavailable", ""].includes(s.state)); }
function hv4Tokens(c) {
  const h = document.querySelector("home-assistant") && document.querySelector("home-assistant").hass;
  const st = (id) => h && h.states[id];
  const name = (st("text.hesc_v4_ev1_car_name") && st("text.hesc_v4_ev1_car_name").state) || "";
  const col = (st("select.hesc_v4_ev1_colour") && st("select.hesc_v4_ev1_colour").attributes.hex) || "#3fc8f4";
  const nm = ["unknown", "unavailable", ""].includes(name) ? "EV1" : name;
  const n2 = (st("text.hesc_v4_ev2_car_name") && st("text.hesc_v4_ev2_car_name").state) || "", c2 = (st("select.hesc_v4_ev2_colour") && st("select.hesc_v4_ev2_colour").attributes.hex) || "#ff8a65";
  const nm2 = ["unknown", "unavailable", ""].includes(n2) ? "EV2" : n2; // 08-11: the second car in Instellingen
  return JSON.parse(JSON.stringify(c).split("{ev1}").join(nm.replace(/"/g, "'")).split("{ev1c}").join(col).split("{ev2}").join(nm2.replace(/"/g, "'")).split("{ev2c}").join(c2));
}

const CSS = `
:host{--hv-line:var(--divider-color,#30333c);--hv-muted:var(--secondary-text-color,#9aa0aa);
  --hv-card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));--hv-live:#5fbf6a;--hv-dot:#ff9800}
.bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:12px 14px}
.live{display:flex;align-items:center;gap:10px;border:1px solid var(--hv-line);border-radius:999px;
  padding:5px 14px 5px 5px;background:var(--hv-card2);cursor:pointer;font:inherit;color:var(--primary-text-color)}
.live.on{border-color:var(--hv-live);background:rgba(95,191,106,.15)}
.sw{width:42px;height:24px;border-radius:999px;background:rgba(0,0,0,.25);border:1px solid var(--hv-line);position:relative}
.sw::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:var(--hv-muted);transition:left .2s}
.live.on .sw::after{left:20px;background:var(--hv-live)}
.live span{color:var(--hv-muted);font-size:13px}.live.on span{color:var(--hv-live)}
.sep{width:1px;height:30px;background:var(--hv-line);margin:0 4px}
.pill{position:relative;font:inherit;font-size:14px;color:var(--hv-muted);background:transparent;
  border:1px solid var(--hv-line);border-radius:999px;padding:8px 18px;cursor:pointer;display:flex;align-items:center;gap:8px}
.pill:hover,.pill.open{color:var(--primary-text-color);background:var(--hv-card2)}
.pill i{width:9px;height:9px;border-radius:50%}
.pill[hidden]{display:none}
.pill.mode{margin-left:auto;border-style:dashed;font-size:13px;padding:6px 14px}
.pill.mode b{font-weight:600;color:var(--primary-text-color)}
.dot{position:absolute;top:-2px;right:-2px;width:10px;height:10px;border-radius:50%;background:var(--hv-dot);
  border:2px solid var(--ha-card-background,var(--card-background-color,#1f2128))}
button:focus-visible{outline:2px solid var(--primary-color);outline-offset:2px}
.ov[hidden],.dot[hidden]{display:none}
.ov{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:flex-start;justify-content:center;
  padding:40px 16px 24px;z-index:999;overflow:auto}
.win{background:var(--ha-card-background,var(--card-background-color));border:1px solid var(--hv-line);
  border-radius:14px;width:100%;max-width:640px;padding:16px 18px 20px;display:grid;gap:12px}
.win.wide{max-width:1640px}
.win.cols{max-width:1640px}
.win.cols>#body{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))!important;align-items:start}
@media (max-height:540px),(max-width:700px){.win.cols>#body{grid-template-columns:minmax(0,1fr)!important}}
.win.wide>#body{display:block!important;columns:380px;column-gap:12px}
.win.wide>#body>*{break-inside:avoid;display:block;margin-bottom:12px}
.win{box-sizing:border-box;min-width:0}.win>#body>*{min-width:0;max-width:100%}
.win header{display:flex;align-items:center;gap:10px}
.foot[hidden]{display:none}.foot{border-top:1px solid var(--hv-line);padding-top:12px;text-align:right}
.foot a{color:var(--hv-muted);text-decoration:underline;font-size:14px}.foot a:hover{color:var(--primary-text-color)}
.win h3{margin:0;font-size:17px;font-weight:500}
.x{margin-left:auto;background:none;border:0;color:var(--hv-muted);font-size:20px;cursor:pointer;width:36px;height:36px;border-radius:50%}
.back{background:none;border:0;color:var(--hv-muted);font-size:26px;line-height:1;cursor:pointer;width:36px;height:36px;border-radius:50%}
.back[hidden],.subs[hidden]{display:none}.back:hover{background:var(--hv-card2);color:var(--primary-text-color)}
.subs{display:flex;gap:8px;flex-wrap:wrap}
.tabs[hidden]{display:none}.tabs{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;background:var(--hv-card2);border-radius:12px;padding:4px;gap:4px}
.tab{font:inherit;font-size:14px;border:0;border-radius:9px;background:none;color:var(--hv-muted);padding:8px 6px;cursor:pointer;position:relative}
.tab.on{background:var(--primary-color);color:var(--text-primary-color,#fff);font-weight:600}
.tab .dot{top:2px;right:6px}
.x:hover{background:var(--hv-card2);color:var(--primary-text-color)}
.win .ib{margin-left:auto}.win .ib+.x{margin-left:0}
${INFO_CSS}`;

/* Decision 10-11-2026: the phase advice as an info item under Settings › Standard › Sun and grid:
   how the solar power is spread over the three phases (from sensor.hesc_v4_phase_advice). Advice only. */
function hv4Phases(hass, eid, sub = "") {
  const st = hass.states[eid];
  // 11-11-2026 (as v3): the split only means something with 3 phases - with 1 phase or no meter per phase it is not shown
  if (!st || st.state === "not_available") return "";
  const a = st.attributes, lang = hv4Lang();
  const TT = {
    nl: { t: "Fasen-opbrengst verdeling", now: "Nu:", nosun: "Nu geen zon over.", avg: (d) => `Gemiddeld over ${d} dag${d === 1 ? "" : "en"} met genoeg zon:`, na: "Niet beschikbaar: alleen bij 3 fasen, met een slimme meter die het vermogen per fase meldt.",
      me: (u, n) => `Aan het meten: ${u} van ${n} dagen met genoeg zon.`, pr: "Voorlopig", co: "Bevestigd",
      ph: "fase", weak: (p) => `Zwakste fase: fase ${p}.`, bl: (h, w) => `Op zonnige dagen houdt de zwakste fase je laadpaal ongeveer ${h} uur per dag tegen (je laadpaal wil minstens ${w} W zon op elke fase).`,
      top: (p) => `Zonnigste periode bij jou: ${p}.`, note: "Alleen advies: HESC verandert niets." },
    de: { t: "Ertrag pro Phase", now: "Jetzt:", nosun: "Gerade keine Sonne übrig.", avg: (d) => `Im Schnitt über ${d} Tag${d === 1 ? "" : "e"} mit genug Sonne:`, na: "Nicht verfügbar: nur bei 3 Phasen, mit einem Zähler, der die Leistung pro Phase meldet.",
      me: (u, n) => `Messung läuft: ${u} von ${n} Tagen mit genug Sonne.`, pr: "Vorläufig", co: "Bestätigt",
      ph: "Phase", weak: (p) => `Schwächste Phase: Phase ${p}.`, bl: (h, w) => `An sonnigen Tagen hält die schwächste Phase deine Wallbox etwa ${h} Stunden pro Tag zurück (deine Wallbox braucht mindestens ${w} W Sonne auf jeder Phase).`,
      top: (p) => `Sonnigste Zeit bei dir: ${p}.`, note: "Nur ein Rat: HESC ändert nichts." },
    en: { t: "Yield split over the phases", now: "Now:", nosun: "No sun to spare right now.", avg: (d) => `Average over ${d} day${d === 1 ? "" : "s"} with enough sun:`, na: "Not available: 3 phases only, with a meter that reports the power per phase.",
      me: (u, n) => `Measuring: ${u} of ${n} days with enough sun.`, pr: "Provisional", co: "Confirmed",
      ph: "phase", weak: (p) => `Weakest phase: phase ${p}.`, bl: (h, w) => `On sunny days the weakest phase holds your charger back for about ${h} hours a day (your charger wants at least ${w} W of sun on every phase).`,
      top: (p) => `Sunniest period where you live: ${p}.`, note: "Advice only: HESC changes nothing." },
  };
  const L = TT[lang] || TT.en;
  const n = (v) => (lang === "en" ? String(v) : String(v).replace(".", ","));
  const stTxt = st.state === "not_available" ? L.na : st.state === "measuring" ? L.me(a.usable_days || 0, a.need_days || 14)
    : `${st.state === "confirmed" ? L.co : L.pr} · ${L.me(a.usable_days || 0, a.need_days || 14).replace(/^[^:]*: /, "")}`;
  const sh = [1, 2, 3].map((p) => +a[`share_phase_${p}`] || 0), has = (a.usable_days || 0) > 0 && sh.some((v) => v > 0);
  const fmt = (xs) => { const lo = xs.indexOf(Math.min(...xs)); return xs.map((v, k) => `<b${k === lo ? ' style="color:#ef6c00"' : ""}>${n(Math.round(v))}%</b>`).join(" · "); };
  // 11-11-2026 (as v3, but right away): the split of the sun now, from the meter per phase (only while there is sun over)
  const ids = a.phase_sensors || [], sign = a.phase_sign;
  let live = "";
  if (ids.length === 3 && sign) {
    const w = ids.map((id) => { const s = hass.states[id]; const v = s ? Number(s.state) : NaN; return /kW/i.test((s && s.attributes.unit_of_measurement) || "") ? v * 1000 : v; });
    if (w.every((v) => isFinite(v))) {
      const sur = w.map((v) => Math.max(0, -sign * v)), tot = sur.reduce((x, y) => x + y, 0);
      live = tot >= 200 ? fmt(sur.map((v) => (100 * v) / tot)) : "";
      if (!live) live = `<span class="sm">${L.nosun}</span>`;
    }
  }
  const rows = (live ? `<div class="st">${L.now}</div><div class="big" style="font-size:18px">${live}</div>` : "")
    + (has ? `<div class="st">${L.avg(a.usable_days)}</div><div class="big" style="font-size:18px">${fmt(sh)}</div>` : "");
  return `<div class="ph"><h5>${L.t}${sub}</h5>${rows}<div class="st">${stTxt}</div></div>`;
}

/* Decision 10-11-2026: "Thuisaccu instellen" step by step, like the first start - plug and play with
   HESC's suggestions, the live value to check, and the kickstart explained in plain words.
   It only sets the Thuisaccu fields (text/number/switch entities); nothing else. */
const HV4_BW = { home: "text.hesc_v4_home_battery_level_sensors", pow: "text.hesc_v4_home_battery_power_sensors",
  size: "number.hesc_v4_home_battery_size_all_together", kick: "switch.hesc_v4_home_battery_and_ev_kickstart" };
const HV4_BW_TXT = {
  nl: { open: "Thuisbatterij(en) instellen, stap voor stap", t: "Thuisbatterij(en) instellen", step: (i, n) => `Stap ${i} van ${n}`,
    q1: "Heb je een of meer thuisbatterijen?", q1s: "Een batterij in huis die zonnestroom opslaat, bijvoorbeeld een Marstek, Zendure of Powerwall.", yes: "Ja", no: "Nee",
    q2: "Welke thuisbatterijen zijn van jou?", q2s: "Dit vond HESC in Home Assistant. Vink je eigen thuisbatterijen aan.", none: "HESC vond geen thuisbatterij. Je kunt de sensoren later zelf kiezen in de tegel.",
    q3: "Vermogen van je thuisbatterij(en)", q3s: "Hoeveel je thuisbatterij(en) nu laadt (+) of ontlaadt (−). HESC kiest de beste sensor; kijk of het getal klopt met wat je thuisbatterij(en) nu doen.",
    tot: "Eén totaal-sensor voor alle thuisbatterijen", per: "Eén sensor per thuisbatterij", note: "Let op: de totaal-sensor telt andersom dan de losse sensoren. Kijk na welke + = laden gebruikt.",
    q4: "Laadstand", q4s: "Hoe vol je thuisbatterij(en) nu zijn, in %.", q5: "Hoe groot zijn je thuisbatterijen samen?", q5s: "In kWh, alle thuisbatterijen bij elkaar.",
    q6: "Wat HESC met je thuisbatterij(en) doet", q6s: "Slurpen je thuisbatterij(en) alle zonnestroom op, dan ziet je laadpaal geen zon over en start je auto niet. HESC geeft dan een duwtje: de auto begint met laden (kickstart), maar alleen als er vandaag nog genoeg zon komt om ook je thuisbatterij(en) vol te krijgen. Wordt het krap voor de thuisbatterij(en), dan pauzeert HESC de auto weer.",
    kon: "Kickstart aan", koff: "Kickstart uit", q7: "Klaar", q7s: "Dit zet HESC in de tegel Thuisbatterij(en):", save: "Opslaan", back: "Terug", next: "Volgende", cancel: "Annuleren",
    now: "nu", noBat: "Geen thuisbatterij: kickstart uit.", sens: "sensor", sensP: "sensoren", saved: "Opgeslagen." },
  de: { open: "Hausakku einrichten, Schritt für Schritt", t: "Hausakku einrichten", step: (i, n) => `Schritt ${i} von ${n}`,
    q1: "Hast du einen Hausakku?", q1s: "Ein Akku im Haus, der Solarstrom speichert, zum Beispiel Marstek, Zendure oder Powerwall.", yes: "Ja", no: "Nein",
    q2: "Welche Akkus gehören dir?", q2s: "Das hat HESC in Home Assistant gefunden. Hake deine eigenen Akkus an.", none: "HESC hat keinen Hausakku gefunden. Du kannst die Sensoren später selbst in der Kachel wählen.",
    q3: "Leistung deines Hausakkus", q3s: "Wie viel dein Akku jetzt lädt (+) oder entlädt (−). HESC wählt den besten Sensor; schau, ob die Zahl zu dem passt, was dein Akku gerade tut.",
    tot: "Ein Summen-Sensor für alle Akkus", per: "Ein Sensor pro Akku", note: "Achtung: der Summen-Sensor zählt andersherum als die einzelnen Sensoren. Prüfe, welcher + = Laden nutzt.",
    q4: "Ladestand", q4s: "Wie voll dein Akku jetzt ist, in %.", q5: "Wie groß sind deine Akkus zusammen?", q5s: "In kWh, alle Akkus zusammen.",
    q6: "Was HESC mit deinem Hausakku macht", q6s: "Schluckt dein Hausakku den ganzen Solarstrom, sieht deine Wallbox keine Sonne übrig und dein Auto startet nicht. HESC gibt dann einen Schubs: das Auto beginnt zu laden (Kickstart), aber nur wenn heute noch genug Sonne kommt, um auch deinen Hausakku voll zu bekommen. Wird es für den Hausakku knapp, pausiert HESC das Auto wieder.",
    kon: "Kickstart an", koff: "Kickstart aus", q7: "Fertig", q7s: "Das trägt HESC in die Kachel Hausakku ein:", save: "Speichern", back: "Zurück", next: "Weiter", cancel: "Abbrechen",
    now: "jetzt", noBat: "Kein Hausakku: Kickstart aus.", sens: "Sensor", sensP: "Sensoren", saved: "Gespeichert." },
  en: { open: "Set up the home battery, step by step", t: "Set up the home battery", step: (i, n) => `Step ${i} of ${n}`,
    q1: "Do you have a home battery?", q1s: "A battery in the house that stores solar power, for example a Marstek, Zendure or Powerwall.", yes: "Yes", no: "No",
    q2: "Which batteries are yours?", q2s: "This is what HESC found in Home Assistant. Tick your own batteries.", none: "HESC found no home battery. You can pick the sensors yourself in the tile later.",
    q3: "Power of your home battery", q3s: "How much your battery charges (+) or discharges (−) now. HESC picks the best sensor; check that the number matches what your battery is doing.",
    tot: "One total sensor for all batteries", per: "One sensor per battery", note: "Note: the total sensor counts the other way round than the single sensors. Check which one uses + = charging.",
    q4: "Battery level", q4s: "How full your battery is now, in %.", q5: "How big are your batteries together?", q5s: "In kWh, all batteries together.",
    q6: "What HESC does with your home battery", q6s: "If your home battery soaks up all the solar power, your charger sees no sun left and your car does not start. HESC then gives a nudge: the car starts charging (kickstart), but only when enough sun is still coming today to fill your home battery as well. When it gets tight for the home battery, HESC pauses the car again.",
    kon: "Kickstart on", koff: "Kickstart off", q7: "Done", q7s: "HESC puts this in the Home battery tile:", save: "Save", back: "Back", next: "Next", cancel: "Cancel",
    now: "now", noBat: "No home battery: kickstart off.", sens: "sensor", sensP: "sensors", saved: "Saved." },
};
window.__hv4Bw = window.__hv4Bw || null;
function hv4BwLang(h) { const l = hv4Lang(); return HV4_BW_TXT[l] || HV4_BW_TXT.en; }
async function hv4BwLoad(card) {
  const h = card._hass, w = window.__hv4Bw;
  const [f, ents, devs] = await Promise.all([h.callWS({ type: "hesc_v4/setup/find" }), h.callWS({ type: "config/entity_registry/list" }), h.callWS({ type: "config/device_registry/list" })]);
  const src = f.sources || {}, soc = (src.home_battery_soc_sensors || {}).candidates || [], pow = (src.home_battery_power_sensors || {}).candidates || [];
  const platOf = Object.fromEntries(ents.map((e) => [e.entity_id, e.platform])),
    devOf = Object.fromEntries(ents.map((e) => [e.entity_id, e.device_id])), devName = Object.fromEntries(devs.map((d) => [d.id, d.name_by_user || d.name || d.id]));
  // 10-11 (first real try): group by device; sensors without a device by their name without the measure
  // ("Marstek M1 SOC", "Marstek M1 AC Power" -> "Marstek M1"); totals, air conditioners and forecasts are no battery
  const TOT = /total|totaal|som\b|sum\b|gesamt/i, NOT = /clima|airco|thermostat|remote|solcast|forecast|verwacht|morgen|vandaag|demo|plan|capaciteit|capacity|specificatie|health|gezondheid|beschikbaar|cycli|cycles|marge/i,
    NOTPLAT = /capacity_monitor|battery_notes/; // 11-11: measurements about a battery (capacity, health) are no battery level
  const nameOf = (c) => { const x = h.states[c.entity_id]; return (x && x.attributes.friendly_name) || c.name || c.entity_id; };
  const base = (n) => n.replace(/\b(battery|batterij|state of charge|soc|ac power|dc power|power|vermogen|level|stand|charge|discharge|percentage)\b/gi, " ").replace(/\s+/g, " ").trim();
  const by = {};
  [...soc.map((c) => ({ ...c, k: "soc" })), ...pow.map((c) => ({ ...c, k: "pow" }))].forEach((c) => {
    const n = nameOf(c);
    if (TOT.test(n + " " + c.entity_id) || NOT.test(n) || NOTPLAT.test(platOf[c.entity_id] || "")) return;
    const d = devOf[c.entity_id] ? "d:" + devOf[c.entity_id] : "n:" + base(n).toLowerCase();
    (by[d] = by[d] || { id: d, name: devOf[c.entity_id] ? devName[devOf[c.entity_id]] : base(n), soc: [], pow: [] })[c.k].push(c);
  });
  const tot = (l) => l.find((c) => TOT.test(nameOf(c) + " " + c.entity_id)) || null;
  const total = tot(pow), totalSoc = tot(soc);
  w.devs = Object.values(by).filter((d) => d.soc.length || d.pow.length);
  w.totalSoc = totalSoc; w.useTotalSoc = !!totalSoc;
  w.pick = new Set(w.devs.filter((d) => [...d.soc, ...d.pow].some((c) => c.suggested)).map((d) => d.id));
  w.total = total; w.useTotal = !!total; w.note = (src.home_battery_power_sensors || {}).sign_note;
  w.size = +((h.states[HV4_BW.size] || {}).state) || 0; w.kick = (h.states[HV4_BW.kick] || {}).state !== "off";
  w.loading = false; card._sig = ""; card._render();
}
function hv4BwSel(w) { // the sensors that follow from the choices
  const ds = w.devs.filter((d) => w.pick.has(d.id)), first = (l) => (l.find((c) => c.suggested) || l[0] || {}).entity_id;
  const soc = w.useTotalSoc && w.totalSoc ? [w.totalSoc.entity_id] : ds.map((d) => first(d.soc)).filter(Boolean);
  const pow = w.useTotal && w.total ? [w.total.entity_id] : ds.map((d) => first(d.pow)).filter(Boolean);
  return { soc, pow };
}
function hv4BatWiz(card) {
  const h = card._hass, T = hv4BwLang(h), w = window.__hv4Bw;
  if (!w) return `<button class="bwb" data-bw="open">${T.open}</button>`;
  if (w.loading) return `<div class="bw"><h5>${T.t}</h5><p>…</p></div>`;
  const st = (id) => h.states[id], val = (id) => { const x = st(id); return x ? `${hv4Num(x.state, x.attributes.unit_of_measurement)} ${x.attributes.unit_of_measurement || ""}` : ""; };
  const nm = (id) => { const x = st(id); return (x && x.attributes.friendly_name) || id; };
  const steps = w.has === false ? ["q1", "q7"] : ["q1", "q2", "q3", "q4", "q5", "q6", "q7"], i = Math.min(w.i || 0, steps.length - 1), k = steps[i];
  const sel = w.devs ? hv4BwSel(w) : { soc: [], pow: [] };
  let body = "";
  if (k === "q1") body = `<p>${T.q1s}</p><div class="nav"><button class="btn${w.has === true ? " act" : ""}" data-bw="has1">${T.yes}</button><button class="btn${w.has === false ? " act" : ""}" data-bw="has0">${T.no}</button></div>`;
  if (k === "q2") body = `<p>${T.q2s}</p>` + (w.devs.length ? w.devs.map((d) => `<label><input type="checkbox" data-bwd="${d.id}"${w.pick.has(d.id) ? " checked" : ""}><span>${d.name}</span><small>${[...d.soc, ...d.pow].map((c) => val(c.entity_id)).filter(Boolean).slice(0, 2).join(" · ")}</small></label>`).join("") : `<p>${T.none}</p>`);
  if (k === "q3") body = `<p>${T.q3s}</p>` + (w.total ? `<label><input type="radio" name="bwt" data-bwt="1"${w.useTotal ? " checked" : ""}><span>${T.tot}: ${nm(w.total.entity_id)}</span><small>${val(w.total.entity_id)}</small></label><label><input type="radio" name="bwt" data-bwt="0"${w.useTotal ? "" : " checked"}><span>${T.per}</span></label>` : "")
    + (!w.useTotal || !w.total ? sel.pow.map((id) => `<label><span>${nm(id)}</span><small>${val(id)}</small></label>`).join("") : "") + (w.note ? `<p class="warn">${T.note}</p>` : "");
  if (k === "q4") body = `<p>${T.q4s}</p>` + (w.totalSoc ? `<label><input type="radio" name="bws" data-bws="1"${w.useTotalSoc ? " checked" : ""}><span>${T.tot}: ${nm(w.totalSoc.entity_id)}</span><small>${val(w.totalSoc.entity_id)}</small></label><label><input type="radio" name="bws" data-bws="0"${w.useTotalSoc ? "" : " checked"}><span>${T.per}</span></label>` : "") + sel.soc.filter(() => !w.useTotalSoc).map((id) => `<label><span>${nm(id)}</span><small>${val(id)}</small></label>`).join("");
  if (k === "q5") body = `<p>${T.q5s}</p><div class="nav"><button class="btn" data-bw="s-">−</button><input class="big bwin" type="number" inputmode="decimal" min="0" max="200" step="0.01" data-bwsize value="${w.size}"> <span class="big">kWh</span><button class="btn" data-bw="s+">+</button></div>`;
  if (k === "q6") body = `<p>${T.q6s}</p><div class="nav"><button class="btn${w.kick ? " act" : ""}" data-bw="k1">${T.kon}</button><button class="btn${!w.kick ? " act" : ""}" data-bw="k0">${T.koff}</button></div>`;
  if (k === "q7") body = w.has === false ? `<p>${T.noBat}</p>` : `<p>${T.q7s}</p><label><span>${T.q3}</span><small>${sel.pow.map(nm).join(", ")}</small></label><label><span>${T.q4}</span><small>${sel.soc.map(nm).join(", ")}</small></label><label><span>${T.q5}</span><small>${hv4Num(w.size, "")} kWh</small></label><label><span>Kickstart</span><small>${w.kick ? T.kon : T.koff}</small></label>`;
  const okNext = k === "q1" ? w.has !== undefined : k === "q2" ? w.pick.size > 0 || !w.devs.length : true;
  return `<div class="bw"><h5>${T[k]}</h5><div class="stp2">${T.t} · ${T.step(i + 1, steps.length)}</div>${body}
    <div class="nav">${i > 0 ? `<button class="btn" data-bw="prev">${T.back}</button>` : ""}<button class="btn" data-bw="cancel">${T.cancel}</button><span class="sp"></span>
    ${k === "q7" ? `<button class="btn act" data-bw="save">${T.save}</button>` : `<button class="btn act" data-bw="next"${okNext ? "" : " disabled"}>${T.next}</button>`}</div></div>`;
}
function hv4BatWizWire(card) {
  const r = card.shadowRoot, re = () => { card._sig = ""; card._render(); };
  r.querySelectorAll("[data-bw]").forEach((b) => b.addEventListener("click", async () => {
    const a = b.dataset.bw, w = window.__hv4Bw;
    if (a === "open") { window.__hv4Bw = { i: 0, loading: true, pick: new Set(), devs: [] }; re(); hv4BwLoad(card).catch(() => { window.__hv4Bw.loading = false; re(); }); return; }
    if (a === "cancel") { window.__hv4Bw = null; re(); return; }
    if (a === "has1") w.has = true; if (a === "has0") w.has = false;
    if (a === "next") w.i = (w.i || 0) + 1; if (a === "prev") w.i = Math.max(0, (w.i || 0) - 1);
    if (a === "s-") w.size = Math.max(0, Math.round((w.size - 0.5) * 100) / 100); if (a === "s+") w.size = Math.round((w.size + 0.5) * 100) / 100;
    if (a === "k1") w.kick = true; if (a === "k0") w.kick = false;
    if (a === "save") {
      const h = card._hass;
      if (w.has === false) await h.callService("switch", "turn_off", { entity_id: HV4_BW.kick });
      else {
        const sel = hv4BwSel(w);
        await h.callService("text", "set_value", { entity_id: HV4_BW.home, value: sel.soc.join(", ") });
        await h.callService("text", "set_value", { entity_id: HV4_BW.pow, value: sel.pow.join(", ") });
        if (w.size > 0) await h.callService("number", "set_value", { entity_id: HV4_BW.size, value: w.size });
        await h.callService("switch", w.kick ? "turn_on" : "turn_off", { entity_id: HV4_BW.kick });
      }
      window.__hv4Bw = null;
    }
    re();
  }));
  r.querySelectorAll("[data-bwd]").forEach((c) => c.addEventListener("change", () => { const w = window.__hv4Bw; if (c.checked) w.pick.add(c.dataset.bwd); else w.pick.delete(c.dataset.bwd); re(); }));
  r.querySelectorAll("[data-bwsize]").forEach((c) => c.addEventListener("change", () => { const v = parseFloat(String(c.value).replace(",", ".")); if (isFinite(v) && v >= 0) window.__hv4Bw.size = Math.round(v * 100) / 100; re(); }));
  r.querySelectorAll("[data-bws]").forEach((c) => c.addEventListener("change", () => { window.__hv4Bw.useTotalSoc = c.dataset.bws === "1"; re(); }));
  r.querySelectorAll("[data-bwt]").forEach((c) => c.addEventListener("change", () => { window.__hv4Bw.useTotal = c.dataset.bwt === "1"; re(); }));
}

/* Decision 11-11-2026 ("alles meenemen"): the other tiles step by step too, the same way as the home battery -
   one question per screen, HESC's suggestion ticked, live values to check, a summary before saving.
   Step kinds: src (a source from hesc_v4/setup/find, saved with hesc_v4/setup/source), phases (the three
   phase meters together), toggle / number / select (an entity of HESC, saved with its service), phones
   (add or remove a phone, test message), done (summary). */
// the wizard ids have no Dutch word in them: the panel translates words in the card config (11-11-2026)
const HV4_WZ_TXT = {
  nl: { open: "Stap voor stap instellen", step: (i, n) => `stap ${i} van ${n}`, back: "Terug", next: "Volgende", cancel: "Annuleren", save: "Opslaan",
    yes: "Ja", no: "Nee", none: "Geen (leeg laten)", now: "nu", saving: "Bezig met opslaan…", saved: "Opgeslagen.", sug: "voorstel van HESC", cur: "nu ingesteld",
    done: "Klaar", doneS: "Dit zet HESC in deze tegel:", nothing: "Niets gevonden. Je kunt dit later nog instellen.", ph: (p) => `Fase ${p}`,
    wzon: { t: "Zon en net",
      pv: ["Zonnestroom nu", "Welke meter telt al je zonnepanelen samen? Kijk of het getal klopt met wat je panelen nu leveren."],
      grid: ["Netvermogen nu", "Welke meter meet wat je huis met het net uitwisselt (je slimme meter)?"],
      fc: ["Zonverwachting nu", "Welke sensor geeft het verwachte zonnevermogen van nu (bijv. Solcast)?"],
      fc30: ["Zonverwachting over 30 minuten", "En het verwachte zonnevermogen over een half uur?"],
      today: ["Zonverwachting vandaag", "De zonverwachting van vandaag (per half uur), voor de planning."],
      tom: ["Zonverwachting morgen", "En die van morgen."],
      phases: ["Netvermogen per fase", "Niet verplicht. Alleen bij 3 fasen: de meter per fase. Daarmee laat HESC de verdeling van je zon over de fasen zien."] },
    wkans: { t: "Goedkope kansen",
      on: ["Goedkope kansen pakken", "Mag HESC extra laden als de stroom heel goedkoop is, ook als dat niet nodig is voor je planning?"],
      price: ["Tot welke prijs", "Tot welke prijs per kWh is stroom goedkoop genoeg?"] },
    wmeld: { t: "Meldingen",
      phones: ["Naar welke telefoons", "Kies een telefoon om toe te voegen of weg te halen. Nu gaan meldingen naar:"],
      test: ["Testbericht", "Stuur een testbericht om te zien of het aankomt."], send: "Stuur testbericht", sent: "Verstuurd: kijk op je telefoon.",
      morning: ["Ochtendoverzicht", "Wil je elke ochtend een kort overzicht van de dag?"],
      time: ["Hoe laat", "Hoe laat wil je het ochtendoverzicht?"] } },
  de: { open: "Schritt für Schritt einstellen", step: (i, n) => `Schritt ${i} von ${n}`, back: "Zurück", next: "Weiter", cancel: "Abbrechen", save: "Speichern",
    yes: "Ja", no: "Nein", none: "Keiner (leer lassen)", now: "jetzt", saving: "Wird gespeichert…", saved: "Gespeichert.", sug: "Vorschlag von HESC", cur: "jetzt eingestellt",
    done: "Fertig", doneS: "Das stellt HESC in dieser Kachel ein:", nothing: "Nichts gefunden. Du kannst das später einstellen.", ph: (p) => `Phase ${p}`,
    wzon: { t: "Sonne und Netz",
      pv: ["Solarleistung jetzt", "Welcher Zähler zählt alle deine Solarmodule zusammen? Prüfe, ob die Zahl zu dem passt, was deine Module jetzt liefern."],
      grid: ["Netzleistung jetzt", "Welcher Zähler misst, was dein Haus mit dem Netz austauscht (dein Smart Meter)?"],
      fc: ["PV-Prognose jetzt", "Welcher Sensor gibt die erwartete Solarleistung von jetzt (z. B. Solcast)?"],
      fc30: ["PV-Prognose in 30 Minuten", "Und die erwartete Solarleistung in einer halben Stunde?"],
      today: ["PV-Prognose heute", "Die Solarprognose von heute (pro halbe Stunde), für die Planung."],
      tom: ["PV-Prognose morgen", "Und die von morgen."],
      phases: ["Netzleistung pro Phase", "Nicht nötig. Nur bei 3 Phasen: der Zähler pro Phase. Damit zeigt HESC die Verteilung deiner Sonne über die Phasen."] },
    wkans: { t: "Günstige Chancen",
      on: ["Günstige Chancen nutzen", "Darf HESC zusätzlich laden, wenn Strom sehr günstig ist, auch wenn es für die Planung nicht nötig ist?"],
      price: ["Bis zu welchem Preis", "Bis zu welchem Preis pro kWh ist Strom günstig genug?"] },
    wmeld: { t: "Benachrichtigungen",
      phones: ["An welche Telefone", "Wähle ein Telefon zum Hinzufügen oder Entfernen. Jetzt gehen Meldungen an:"],
      test: ["Testnachricht", "Sende eine Testnachricht, um zu sehen, ob sie ankommt."], send: "Testnachricht senden", sent: "Gesendet: schau auf dein Telefon.",
      morning: ["Morgenübersicht", "Möchtest du jeden Morgen eine kurze Übersicht über den Tag?"],
      time: ["Um wie viel Uhr", "Um wie viel Uhr möchtest du die Morgenübersicht?"] } },
  en: { open: "Set up step by step", step: (i, n) => `step ${i} of ${n}`, back: "Back", next: "Next", cancel: "Cancel", save: "Save",
    yes: "Yes", no: "No", none: "None (leave empty)", now: "now", saving: "Saving…", saved: "Saved.", sug: "HESC's suggestion", cur: "set now",
    done: "Done", doneS: "This is what HESC sets in this tile:", nothing: "Nothing found. You can set this later.", ph: (p) => `Phase ${p}`,
    wzon: { t: "Sun and grid",
      pv: ["Solar power now", "Which meter counts all your solar panels together? Check that the number matches what your panels deliver now."],
      grid: ["Grid power now", "Which meter measures what your house exchanges with the grid (your smart meter)?"],
      fc: ["Solar forecast now", "Which sensor gives the expected solar power of now (e.g. Solcast)?"],
      fc30: ["Solar forecast in 30 minutes", "And the expected solar power in half an hour?"],
      today: ["Solar forecast today", "Today's solar forecast (per half hour), for the planning."],
      tom: ["Solar forecast tomorrow", "And tomorrow's."],
      phases: ["Grid power per phase", "Optional. Only with 3 phases: the meter per phase. HESC then shows how your sun is spread over the phases."] },
    wkans: { t: "Cheap chances",
      on: ["Take cheap chances", "May HESC charge extra when power is very cheap, also when the planning does not need it?"],
      price: ["Up to which price", "Up to which price per kWh is power cheap enough?"] },
    wmeld: { t: "Notifications",
      phones: ["To which phones", "Pick a phone to add or remove. Notifications now go to:"],
      test: ["Test message", "Send a test message to see that it arrives."], send: "Send test message", sent: "Sent: look at your phone.",
      morning: ["Morning summary", "Would you like a short summary of the day every morning?"],
      time: ["What time", "At what time would you like the morning summary?"] } },
};
const HV4_WZ = {
  wzon: [{ k: "src", key: "pv_power_sensor", h: "hesc_pv_power_sensor", t: "pv" }, { k: "src", key: "grid_power_sensor", h: "hesc_grid_power_sensor", t: "grid" },
    { k: "src", key: "forecast_now_sensor", h: "hesc_forecast_now_sensor", t: "fc", opt: 1 }, { k: "src", key: "forecast_30m_sensor", h: "hesc_forecast_30m_sensor", t: "fc30", opt: 1 },
    { k: "src", key: "solar_today_sensor", h: "hesc_solar_today_sensor", t: "today", opt: 1 }, { k: "src", key: "solar_tomorrow_sensor", h: "hesc_solar_tomorrow_sensor", t: "tom", opt: 1 },
    { k: "phases", t: "phases" }, { k: "done" }],
  wkans: [{ k: "toggle", e: "switch.hesc_v4_charge_plan_take_cheap_chances", t: "on" }, { k: "number", e: "number.hesc_v4_charge_plan_opportunity_price", t: "price", if: 0 }, { k: "done" }],
  wmeld: [{ k: "phones", e: "select.hesc_v4_ev1_notifications_add_or_remove_a_phone", s: "sensor.hesc_v4_notification_phones", t: "phones" },
    { k: "test", e: "button.hesc_v4_send_a_test_notification", t: "test" }, { k: "toggle", e: "switch.hesc_v4_ev1_morning_summary", t: "morning" },
    { k: "select", e: "select.hesc_v4_ev1_morning_summary_time", t: "time", if: 2 }, { k: "done" }],
};
const HV4_PH = ["grid_power_l1_sensor", "grid_power_l2_sensor", "grid_power_l3_sensor"];
function hv4WzLang(h) { const l = hv4Lang(); return HV4_WZ_TXT[l] || HV4_WZ_TXT.en; }
function hv4WzVal(h, id) { const x = h.states[id]; return x ? `${hv4Num(x.state, x.attributes.unit_of_measurement)} ${x.attributes.unit_of_measurement || ""}`.trim() : ""; }
function hv4WzName(h, id) { const x = h.states[id]; return (x && x.attributes.friendly_name) || id; }
function hv4WzSteps(w) { return HV4_WZ[w.id].filter((s) => s.if === undefined || w.ans[s.if] !== false); }
function hv4Wiz(card, id) {
  const h = card._hass, L = hv4WzLang(h), T = L[id], w = (window.__hv4Wz || {})[id];
  if (!T) return "";
  if (!w) return `<button class="bwb" data-wz="open" data-wzid="${id}">${L.open}</button>`;
  if (w.loading) return `<div class="bw"><h5>${T.t}</h5><p>…</p></div>`;
  const steps = hv4WzSteps(w), i = Math.min(w.i, steps.length - 1), s = steps[i], si = HV4_WZ[id].indexOf(s);
  const setup = (h.states["sensor.hesc_v4_setup"] || { attributes: {} }).attributes;
  const radio = (name, list, cur, sug, opt) => (list.length || opt ? "" : `<p>${L.nothing}</p>`)
    + list.map((e) => `<label><input type="radio" name="${name}" data-wzr="${si}" data-wzid="${id}" value="${e}"${cur === e ? " checked" : ""}><span>${hv4WzName(h, e)}${e === sug ? ` <small>· ${L.sug}</small>` : ""}${e === w.cur[si] ? ` <small>· ${L.cur}</small>` : ""}</span><small>${hv4WzVal(h, e)}</small></label>`).join("")
    + (opt ? `<label><input type="radio" name="${name}" data-wzr="${si}" data-wzid="${id}" value=""${cur === "" ? " checked" : ""}><span>${L.none}</span></label>` : "");
  let head = s.k === "done" ? L.done : T[s.t][0], body = "";
  if (s.k !== "done") body = `<p>${T[s.t][1]}</p>`;
  if (s.k === "src") {
    const c = ((w.find.sources || {})[s.key] || { candidates: [] }).candidates.map((x) => x.entity_id), sug = (((w.find.sources || {})[s.key] || { candidates: [] }).candidates.find((x) => x.suggested) || {}).entity_id;
    const list = [...new Set([w.cur[si], ...c].filter(Boolean))];
    body += radio(`wz${si}`, list, w.ans[si], sug, s.opt);
  }
  if (s.k === "phases") body += [0, 1, 2].map((p) => { const c = ((w.find.sources || {})[HV4_PH[p]] || { candidates: [] }).candidates.map((x) => x.entity_id); const list = [...new Set([w.ans[si][p], ...c].filter(Boolean))];
    return `<label><span>${L.ph(p + 1)}</span><select data-wzp="${si}:${p}" data-wzid="${id}"><option value="">${L.none}</option>${list.map((e) => `<option value="${e}"${w.ans[si][p] === e ? " selected" : ""}>${hv4WzName(h, e)} · ${hv4WzVal(h, e)}</option>`).join("")}</select></label>`; }).join("");
  if (s.k === "toggle") body += `<div class="nav"><button class="btn${w.ans[si] === true ? " act" : ""}" data-wz="t1" data-wzs="${si}" data-wzid="${id}">${L.yes}</button><button class="btn${w.ans[si] === false ? " act" : ""}" data-wz="t0" data-wzs="${si}" data-wzid="${id}">${L.no}</button></div>`;
  if (s.k === "number") { const st = h.states[s.e] || { attributes: {} }; body += `<div class="nav"><input class="big bwin" type="number" inputmode="decimal" step="${st.attributes.step || 0.01}" min="${st.attributes.min ?? ""}" max="${st.attributes.max ?? ""}" data-wzn="${si}" data-wzid="${id}" value="${w.ans[si]}"> <span class="big">${st.attributes.unit_of_measurement || ""}</span></div>`; }
  if (s.k === "select") { const st = h.states[s.e] || { attributes: { options: [] } }; body += `<div class="chips">${(st.attributes.options || []).map((o) => `<button class="chip${w.ans[si] === o ? " on" : ""}" data-wzo="${si}" data-wzid="${id}" data-o="${o}">${optNl(o)}</button>`).join("")}</div>`; }
  if (s.k === "phones") { const st = h.states[s.e] || { attributes: { options: [] } }; body += `<p><b>${(h.states[s.s] || {}).state || "-"}</b></p><div class="chips">${(st.attributes.options || []).filter((o) => o && !/^-|choose|kies/i.test(o)).map((o) => `<button class="chip" data-wzph="${s.e}" data-o="${o}">${optNl(o)}</button>`).join("")}</div>`; }
  if (s.k === "test") body += `<div class="nav"><button class="btn" data-wz="test" data-wze="${s.e}" data-wzid="${id}">${T.send}</button></div>${w.sent ? `<p>${T.sent}</p>` : ""}`;
  if (s.k === "done") body = `<p>${L.doneS}</p>` + steps.filter((x) => x.k !== "done" && x.k !== "test" && x.k !== "phones").map((x) => { const j = HV4_WZ[id].indexOf(x), a = w.ans[j];
    const v = x.k === "phases" ? a.map((e) => (e ? hv4WzName(h, e) : "-")).join(" · ") : x.k === "toggle" ? (a ? L.yes : L.no) : x.k === "src" ? (a ? `${hv4WzName(h, a)} (${hv4WzVal(h, a)})` : L.none) : x.k === "select" ? optNl(a) : String(a);
    return `<label><span>${T[x.t][0]}</span><small>${v}</small></label>`; }).join("") + (w.msg ? `<p>${w.msg}</p>` : "");
  return `<div class="bw"><h5>${head}</h5><div class="stp2">${T.t} · ${L.step(i + 1, steps.length)}</div>${body}
    <div class="nav">${i > 0 ? `<button class="btn" data-wz="prev" data-wzid="${id}">${L.back}</button>` : ""}<button class="btn" data-wz="cancel" data-wzid="${id}">${L.cancel}</button><span class="sp"></span>
    ${s.k === "done" ? `<button class="btn act" data-wz="save" data-wzid="${id}"${w.busy ? " disabled" : ""}>${w.busy ? L.saving : L.save}</button>` : `<button class="btn act" data-wz="next" data-wzid="${id}">${L.next}</button>`}</div></div>`;
}
async function hv4WzOpen(card, id) {
  const h = card._hass, setup = (h.states["sensor.hesc_v4_setup"] || { attributes: {} }).attributes;
  window.__hv4Wz = window.__hv4Wz || {};
  const w = window.__hv4Wz[id] = { id, i: 0, loading: true, ans: {}, cur: {}, find: {} };
  if (id === "wzon") w.find = await h.callWS({ type: "hesc_v4/setup/find" });
  HV4_WZ[id].forEach((s, j) => {
    if (s.k === "src") { const c = ((w.find.sources || {})[s.key] || { candidates: [] }).candidates; w.cur[j] = String(setup[s.h] || ""); w.ans[j] = w.cur[j] || ((c.find((x) => x.suggested) || {}).entity_id || ""); }
    if (s.k === "phases") { w.cur[j] = [1, 2, 3].map((p) => String(setup[`hesc_grid_power_phase_${p}`] || "")); w.ans[j] = [...w.cur[j]]; }
    if (s.k === "toggle") w.ans[j] = w.cur[j] = (h.states[s.e] || {}).state === "on";
    if (s.k === "number" || s.k === "select") w.ans[j] = w.cur[j] = (h.states[s.e] || {}).state;
  });
  w.loading = false;
}
async function hv4WzSave(card, id) {
  const h = card._hass, w = window.__hv4Wz[id];
  for (const s of hv4WzSteps(w)) {
    const j = HV4_WZ[id].indexOf(s), a = w.ans[j];
    const pause = () => new Promise((ok) => setTimeout(ok, 1500)); // HESC reloads after each source
    if (s.k === "src" && a !== w.cur[j]) { await h.callWS({ type: "hesc_v4/setup/source", key: s.key, entity_id: a || null }); await pause(); }
    if (s.k === "phases") for (let p = 0; p < 3; p++) if (a[p] !== w.cur[j][p]) { await h.callWS({ type: "hesc_v4/setup/source", key: HV4_PH[p], entity_id: a[p] || null }); await pause(); }
    if (s.k === "toggle" && a !== w.cur[j]) await h.callService("switch", a ? "turn_on" : "turn_off", { entity_id: s.e });
    if (s.k === "number" && String(a) !== String(w.cur[j])) await h.callService("number", "set_value", { entity_id: s.e, value: a });
    if (s.k === "select" && a !== w.cur[j]) await h.callService("select", "select_option", { entity_id: s.e, option: a });
  }
}
function hv4WizWire(card) {
  const r = card.shadowRoot, re = () => { card._sig = ""; card._render(); }, W = () => window.__hv4Wz || {};
  r.querySelectorAll("[data-wz]").forEach((b) => b.addEventListener("click", async () => {
    const a = b.dataset.wz, id = b.dataset.wzid, w = W()[id];
    if (a === "open") { hv4WzOpen(card, id).then(re, re); re(); return; }
    if (!w) return;
    if (a === "t1" || a === "t0") { w.ans[+b.dataset.wzs] = a === "t1"; re(); return; }
    if (a === "test") { await card._hass.callService("button", "press", { entity_id: b.dataset.wze }); w.sent = true; re(); return; }
    if (a === "cancel") { W()[id] = null; re(); return; }
    if (a === "next") w.i++; if (a === "prev") w.i = Math.max(0, w.i - 1);
    if (a === "save") { w.busy = true; re(); try { await hv4WzSave(card, id); W()[id] = null; } catch (e) { w.busy = false; w.msg = String(e.message || e); } }
    re();
  }));
  const at = (c) => { const w = W()[c.dataset.wzid]; return w && !w.loading ? w : null; };
  r.querySelectorAll("[data-wzr]").forEach((c) => c.addEventListener("change", () => { const w = at(c); if (w) { w.ans[+c.dataset.wzr] = c.value; re(); } }));
  r.querySelectorAll("[data-wzp]").forEach((c) => c.addEventListener("change", () => { const w = at(c), [j, p] = c.dataset.wzp.split(":").map(Number); if (w) { w.ans[j][p] = c.value; re(); } }));
  r.querySelectorAll("[data-wzn]").forEach((c) => c.addEventListener("change", () => { const w = at(c), v = parseFloat(String(c.value).replace(",", ".")); if (w && isFinite(v)) { w.ans[+c.dataset.wzn] = v; re(); } }));
  r.querySelectorAll("[data-wzo]").forEach((b) => b.addEventListener("click", () => { const w = at(b); if (w) { w.ans[+b.dataset.wzo] = b.dataset.o; re(); } }));
  r.querySelectorAll("[data-wzph]").forEach((b) => b.addEventListener("click", async () => { await card._hass.callService("select", "select_option", { entity_id: b.dataset.wzph, option: b.dataset.o }); setTimeout(re, 800); }));
}

/* Decision 11-11-2026: the price source per country (postbus 11-11 "prijsbronnen per land"). Only the sources HESC
   reads now, per country; a source HESC finds here is always shown; Nord Pool from HACS has its own name; the own
   sensor with a price list goes last. The country follows the currencies; it also sets the currency. */
const HV4_ISO = { NL: "Netherlands", BE: "Belgium", DE: "Germany", AT: "Austria", FR: "France", ES: "Spain", FI: "Finland",
  SE: "Sweden", NO: "Norway", DK: "Denmark", GB: "United Kingdom", AU: "Australia" };
const HV4_CUR = { Netherlands: "EUR", Belgium: "EUR", Germany: "EUR", Austria: "EUR", France: "EUR", Spain: "EUR", Finland: "EUR",
  Sweden: "SEK", Norway: "NOK", Denmark: "DKK", "United Kingdom": "GBP", Australia: "AUD" };
/* 11-11-2026: price sources per country. Plain names are HESC's own sources (select options); the short keys are
   integrations with a price list in one sensor (source "Price list in sensor" + that sensor), shown when found;
   "own" = any other sensor with a price list (always last). */
const HV4_LIST = {
  np: ["Nord Pool (HACS)", (id, a) => id.startsWith("sensor.nordpool") && a.raw_today],
  eds: ["Energi Data Service", (id, a) => /energi_data_service/.test(id) && a.raw_today],
  epex: ["EPEX Spot", (id, a) => /epex_spot/.test(id) && Array.isArray(a.data)],
  pvpc: ["PVPC (ESIOS)", (id, a) => /pvpc|esios/.test(id) && a.price_00h !== undefined],
  omie: ["OMIE", (id, a) => /omie/.test(id) && a.today_hours],
  octo: ["Octopus Energy", (id) => /^event\.octopus_energy_electricity_.*_current_day_rates$/.test(id)],
  amber: ["Amber Electric", (id, a) => /_general_forecast$/.test(id) && Array.isArray(a.forecasts)],
  zp: ["Zonneplan", (id, a) => /zonneplan/.test(id) && Array.isArray(a.forecast)],
  entsoe: ["ENTSO-e", (id, a) => /entsoe|entso_e/.test(id) && (a.prices_today || a.prices)],
};
const HV4_SRC = { // 11-11-2026: Grid Clock (free ENTSO-e day-ahead prices, about 40 European zones) in every European country
  Netherlands: ["EnergyZero / ANWB Energie", "EasyEnergy", "Tibber", "zp", "Nord Pool (official)", "np", "Grid Clock", "entsoe"],
  Belgium: ["Nord Pool (official)", "np", "Grid Clock", "epex", "entsoe"], Germany: ["Tibber", "Nord Pool (official)", "np", "Grid Clock", "epex", "entsoe"],
  Austria: ["Nord Pool (official)", "np", "Grid Clock", "epex", "entsoe"], France: ["Nord Pool (official)", "np", "Grid Clock", "epex", "entsoe"],
  Spain: ["pvpc", "omie", "Grid Clock", "entsoe"], Finland: ["Nord Pool (official)", "np", "Grid Clock", "entsoe"],
  Sweden: ["Tibber", "Nord Pool (official)", "np", "Grid Clock", "entsoe"], Norway: ["Tibber", "Nord Pool (official)", "np", "Grid Clock", "entsoe"],
  Denmark: ["eds", "Nord Pool (official)", "np", "Grid Clock", "entsoe"],
  "United Kingdom": ["octo"], Australia: ["amber"], Other: ["Nord Pool (official)", "np", "Grid Clock", "entsoe"] };
const HV4_PSTXT = { nl: (x) => `Nog niet gevonden, te installeren: ${x}.`, de: (x) => `Noch nicht gefunden, installierbar: ${x}.`, en: (x) => `Not found yet, can be installed: ${x}.` };
const HV4_CNL = { Netherlands: "Nederland", Belgium: "België", Germany: "Duitsland", Austria: "Oostenrijk", France: "Frankrijk", Spain: "Spanje",
  Finland: "Finland", Sweden: "Zweden", Norway: "Noorwegen", Denmark: "Denemarken", "United Kingdom": "Verenigd Koninkrijk", Australia: "Australië",
  Other: "Ander land" };
function hv4CountryName(c) { return c; }
function hv4Country(h, v) {
  if (v && v !== "Automatic") return v;
  return HV4_ISO[String((h.config && h.config.country) || "").toUpperCase()] || "Other";
}
function hv4PriceSrc(h, s, i, name, sub) {
  const cs = h.states["select.hesc_v4_price_country"], country = hv4Country(h, cs ? cs.state : "Automatic");
  const te = h.states["text.hesc_v4_day_ahead_price_sensor"], sens = te ? String(te.state || "") : "";
  const ids = Object.keys(h.states);
  const found = {}; // list key -> entity id
  Object.entries(HV4_LIST).forEach(([k, [, f]]) => { const id = ids.find((x) => f(x, h.states[x].attributes || {})); if (id) found[k] = id; });
  const opts = s.attributes.options || [], isList = s.state === "Price list in sensor";
  const want = HV4_SRC[country] || HV4_SRC.Other;
  const gc = ids.some((x) => /^sensor\.grid_clock_.*_prices$/.test(x)); // Grid Clock only when installed
  let list = want.filter((o) => (HV4_LIST[o] ? found[o] : o === "Grid Clock" ? gc && opts.includes(o) : opts.includes(o)));
  if (found.np && !list.includes("np")) list.push("np"); // Nord Pool from HACS found here: always shown
  if (s.state && !isList && opts.includes(s.state) && !list.includes(s.state)) list.unshift(s.state); // the current choice stays visible
  const cur = Object.keys(found).find((k) => isList && found[k] === sens);
  if (cur && !list.includes(cur)) list.unshift(cur);
  list.push("own");
  const on = (o) => (HV4_LIST[o] ? cur === o : o === "own" ? isList && !cur : o === s.state);
  const lab = (o) => (HV4_LIST[o] ? HV4_LIST[o][0] : optNl(o));
  const btn = (o) => `<button class="chip${on(o) ? " on" : ""}" data-psrc="${i}" data-o="${HV4_LIST[o] || o === "own" ? "Price list in sensor" : o}"${HV4_LIST[o] ? ` data-sensor="${found[o]}"` : ""}>${lab(o)}</button>`;
  const miss = want.filter((o) => (HV4_LIST[o] && !found[o]) || (o === "Grid Clock" && !gc)).map((o) => (HV4_LIST[o] ? HV4_LIST[o][0] : o));
  const lang = hv4Lang();
  const hint = miss.length ? `<div class="rtxt sm" style="grid-column:1/-1">${(HV4_PSTXT[lang] || HV4_PSTXT.en)(miss.join(", "))}</div>` : "";
  return `<div class="f wide"><div class="nm">${name}${sub}</div><div class="chips">${list.map(btn).join("")}</div>${hint}</div>`;
}

/* Decision 11-11-2026: right after the first start, the home battery step by step in a pop-up (the same menu as
   in the tile Thuisaccu). "Annuleren" = set it up later via the tile. Waits until the reloaded integration has its
   home battery entities. */
window.hv4OpenBatWizPopup = function () {
  let tries = 0;
  const go = () => {
    const ha = document.querySelector("home-assistant"), h = ha && ha.hass;
    if (!h || !h.states[HV4_BW.kick]) { if (++tries < 60) setTimeout(go, 1000); return; }
    const pop = document.createElement("div");
    pop.style.cssText = "position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:40px 16px";
    pop.innerHTML = `<div style="position:relative;width:min(640px,100%);background:var(--card-background-color,#1f2128);border-radius:16px;padding:8px;box-shadow:0 10px 40px rgba(0,0,0,.5)"><div data-body></div></div>`;
    const el = document.createElement("hesc-v4p-fields");
    el.setConfig({ title: hv4BwLang(h).t, rows: [{ type: "batwiz" }] });
    pop.querySelector("[data-body]").appendChild(el);
    document.body.appendChild(pop);
    window.__hv4Bw = { i: 0, loading: true, pick: new Set(), devs: [] };
    el.hass = h;
    hv4BwLoad(el).catch(() => { window.__hv4Bw = null; });
    const tick = setInterval(() => { const x = document.querySelector("home-assistant"); if (x && x.hass) el.hass = x.hass;
      if (window.__hv4Bw === null) { clearInterval(tick); pop.remove(); } }, 800);
  };
  setTimeout(go, 6000); // first let the integration reload after saving
};

/* Decision 11-11-2026: run the first start again, from Expert › Meldingen. It replaces the setup choices
   (charger, car, sensors) with the new answers; the planning, costs and history stay. */
const HV4_REDO = { nl: ["Eerste start opnieuw doorlopen", "Loop de stappen van de eerste start nog een keer door. Je keuzes voor laadpaal, auto en sensoren worden vervangen door wat je nu kiest; je planning, kosten en geschiedenis blijven bewaard."],
  de: ["Ersten Start erneut durchlaufen", "Gehe die Schritte des ersten Starts noch einmal durch. Deine Wahl für Wallbox, Auto und Sensoren wird durch das ersetzt, was du jetzt wählst; Planung, Kosten und Verlauf bleiben erhalten."],
  en: ["Run the first start again", "Go through the steps of the first start once more. Your choices for charger, car and sensors are replaced by what you pick now; your planning, costs and history stay."] };
function hv4RedoTxt(h) { const l = hv4Lang(); return HV4_REDO[l] || HV4_REDO.en; }
/* W1 + W2 (decision 11-11-2026): the full phase overview under Expert › Advies - the split, whether every
   phase gets the minimum your charger wants, what to do about it, and a switch to show the split on Standard. */
const HV4_PHSHOW = "hesc_v4_phase_show";
const hv4PhShow = () => { try { return localStorage.getItem(HV4_PHSHOW) !== "0"; } catch (e) { return true; } };
const HV4_PHD = {
  nl: { t: "Fasen-overzicht", show: "Verdeling ook tonen bij Standaard (Zon en net)", per: (w) => `Je laadpaal wil minstens ${w} W zon op elke fase voordat hij start.`,
    tot: "Je laadpaal kijkt naar het totaal van de drie fasen: de verdeling houdt hem niet tegen.",
    ok: (p) => `Fase ${p}: haalt het minimum.`, low: (p, h) => `Fase ${p}: te weinig zon, houdt je laadpaal ongeveer ${h} uur per dag tegen.`,
    even: "Je zonnestroom is mooi gelijk verdeeld over de fasen. Niets aan doen.",
    tip: (p, h) => `Tip: zet een omvormer of een deel van je panelen op fase ${p}. Dan kun je tot ongeveer ${h} uur per dag eerder op zon laden.`,
    fine: (p) => `Fase ${p} krijgt het minst, maar dat houdt je laadpaal niet tegen. Niets aan doen.`,
    wait: "Een advies volgt als er genoeg dagen gemeten zijn.", top: (p) => `Zonnigste periode bij jou: ${p}.`, note: "Alleen advies: HESC verandert niets." },
  de: { t: "Phasen-Übersicht", show: "Verteilung auch bei Standard zeigen (Sonne und Netz)", per: (w) => `Deine Wallbox braucht mindestens ${w} W Sonne auf jeder Phase, bevor sie startet.`,
    tot: "Deine Wallbox schaut auf die Summe der drei Phasen: die Verteilung hält sie nicht auf.",
    ok: (p) => `Phase ${p}: erreicht das Minimum.`, low: (p, h) => `Phase ${p}: zu wenig Sonne, hält deine Wallbox etwa ${h} Stunden pro Tag zurück.`,
    even: "Dein Solarstrom ist schön gleich über die Phasen verteilt. Nichts zu tun.",
    tip: (p, h) => `Tipp: Lege einen Wechselrichter oder einen Teil der Module auf Phase ${p}. Dann kannst du bis zu etwa ${h} Stunden pro Tag früher mit Sonne laden.`,
    fine: (p) => `Phase ${p} bekommt am wenigsten, aber das hält deine Wallbox nicht auf. Nichts zu tun.`,
    wait: "Ein Rat folgt, wenn genug Tage gemessen sind.", top: (p) => `Sonnigste Zeit bei dir: ${p}.`, note: "Nur ein Rat: HESC ändert nichts." },
  en: { t: "Phase overview", show: "Also show the split on Standard (Sun and grid)", per: (w) => `Your charger wants at least ${w} W of sun on every phase before it starts.`,
    tot: "Your charger looks at the total of the three phases: the split does not hold it back.",
    ok: (p) => `Phase ${p}: gets the minimum.`, low: (p, h) => `Phase ${p}: too little sun, holds your charger back for about ${h} hours a day.`,
    even: "Your solar power is nicely even over the phases. Nothing to do.",
    tip: (p, h) => `Tip: put an inverter or part of your panels on phase ${p}. Then you can charge on the sun up to about ${h} hours a day earlier.`,
    fine: (p) => `Phase ${p} gets the least, but that does not hold your charger back. Nothing to do.`,
    wait: "Advice follows once enough days are measured.", top: (p) => `Sunniest period where you live: ${p}.`, note: "Advice only: HESC changes nothing." },
};
function hv4PhasesDetail(hass, eid) {
  const st = hass.states[eid];
  if (!st) return "";
  const a = st.attributes, lang = hv4Lang(), D = HV4_PHD[lang] || HV4_PHD.en;
  const n = (v) => (lang === "en" ? String(v) : String(v).replace(".", ","));
  if (st.state === "not_available") return "";
  const base = hv4Phases(hass, eid).replace(/<h5>[^<]*<\/h5>/, `<h5>${D.t}</h5>`);
  const ln = [], w = a.per_phase_need_w, ready = st.state === "provisional" || st.state === "confirmed";
  ln.push(w ? D.per(n(Math.round(w))) : D.tot);
  if (w && (a.usable_days || 0) > 0) [1, 2, 3].forEach((p) => { const h = +a[`low_hours_phase_${p}`] || 0; ln.push(h >= 0.1 ? D.low(p, n(h)) : D.ok(p)); });
  if (!ready) ln.push(D.wait);
  else if (a.even) ln.push(D.even);
  else { const h = +(a.blocked_hours_per_day_top ?? a.blocked_hours_per_day) || 0; ln.push(w && h >= 0.1 ? D.tip(a.weakest_phase, n(h)) : D.fine(a.weakest_phase)); }
  if (a.top_period) ln.push(D.top(a.top_period));
  ln.push(D.note);
  return base.replace(/<\/div>$/, `${ln.map((x) => `<div class="st">${x}</div>`).join("")}<label class="land"><input type="checkbox" data-phshow${hv4PhShow() ? " checked" : ""}> ${D.show}</label></div>`);
}

/* RC1 (decision 11-11-2026): back to v3 - turns v3 on again and pauses v4 (nothing removed); two taps */
const HV4_BACK = { nl: ["Terug naar v3", "Tik nog een keer om terug te gaan naar v3", "Zet v3 weer aan en v4 op pauze. Er wordt niets weggegooid: je kunt later weer overstappen. Staat v3 niet meer in HACS? Kies daar eerst een v3-versie.", "v3 staat niet meer in Home Assistant. Installeer eerst een v3-versie via HACS, herstart, en tik dan opnieuw.", "v3 staat weer aan en v4 is gepauzeerd."],
  de: ["Zurück zu v3", "Nochmal tippen, um zu v3 zurückzukehren", "Schaltet v3 wieder ein und pausiert v4. Nichts wird gelöscht: du kannst später wieder wechseln. Ist v3 nicht mehr in HACS? Wähle dort zuerst eine v3-Version.", "v3 ist nicht mehr in Home Assistant. Installiere zuerst eine v3-Version über HACS, starte neu und tippe dann erneut.", "v3 ist wieder an und v4 pausiert."],
  en: ["Back to v3", "Tap once more to go back to v3", "Turns v3 on again and pauses v4. Nothing is removed: you can switch again later. Is v3 no longer in HACS? Pick a v3 version there first.", "v3 is no longer in Home Assistant. Install a v3 version through HACS, restart, then tap again.", "v3 is on again and v4 is paused."] };
function hv4BackTxt(h) { const l = hv4Lang(); return HV4_BACK[l] || HV4_BACK.en; }
function hv4RedoBtn(h) { const [t, x] = hv4RedoTxt(h), k = hv4BackTxt(h); return `<button class="bwb" data-redo>${t}</button><div class="rtxt sm" style="grid-column:1/-1">${x}</div><button class="bwb" data-backv3>${k[0]}</button><div class="rtxt sm" style="grid-column:1/-1" data-backmsg>${k[2]}</div>`; }
async function hv4BackV3(h, b) {
  const k = hv4BackTxt(h), msg = b.parentNode.querySelector("[data-backmsg]");
  if (!b.dataset.sure) { b.dataset.sure = "1"; b.textContent = k[1]; return; }
  b.disabled = true;
  try { const r = await h.callWS({ type: "hesc_v4/setup/back_to_v3" }); if (msg) msg.textContent = r.v3 ? k[4] : k[3]; }
  catch (e) { if (msg) msg.textContent = String(e.message || e); }
  delete b.dataset.sure; b.textContent = k[0]; b.disabled = false;
}
function hv4RedoOpen(h) {
  const pop = document.createElement("div");
  pop.style.cssText = "position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:40px 16px";
  pop.innerHTML = `<div style="position:relative;width:min(760px,100%);background:var(--card-background-color,#1f2128);border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.5)"><button data-x aria-label="Sluiten" style="position:absolute;top:10px;right:12px;z-index:2;background:none;border:0;color:inherit;font-size:22px;cursor:pointer">✕</button><div data-body></div></div>`;
  const el = document.createElement("hesc-v4-first-start");
  if (el.setConfig) el.setConfig({ redo: true });
  pop.querySelector("[data-body]").appendChild(el);
  el.hass = h;
  const close = () => { clearInterval(tick); pop.remove(); };
  const tick = setInterval(() => { const ha = document.querySelector("home-assistant"); if (ha && ha.hass) el.hass = ha.hass; if (el.style.display === "none") close(); }, 1000);
  pop.addEventListener("click", (e) => { if (e.target === pop || e.target.closest("[data-x]")) close(); });
  document.body.appendChild(pop);
}

/* 10-11-2026: a sensor value as people read it - 14.8537 kWh -> 14,9 kWh, 3208.0 W -> 3208 W (display only) */
function hv4Num(v, unit) {
  const x = Number(v);
  if (v === null || v === undefined || v === "" || !isFinite(x)) return v ?? "";
  const u = String(unit || "");
  const d = /^(W|VA|var|Wh|%|A)$/.test(u) ? 0 : /kWh|kW|MWh|kVA|V$|°/.test(u) ? 1 : Math.abs(x) >= 100 ? 0 : Math.abs(x) >= 1 ? 2 : 3;
  const lang = String(((window.__hv4Hass || {}).locale || {}).language || "nl").slice(0, 2);
  return x.toLocaleString(lang === "en" ? "en-GB" : lang, { maximumFractionDigits: d });
}

const HV4_PHONE = "(max-height:540px),(max-width:700px)"; // phone, upright or sideways
/* Decision 10-11-2026: on a phone HESC can open on the planning's month page ("Openen op", kept per device). */
const HV4_LAND = "hesc_v4_open_on";
const hv4Land = () => { try { return localStorage.getItem(HV4_LAND) || ""; } catch (e) { return ""; } };
const hv4SetLand = (v) => { try { if (v) localStorage.setItem(HV4_LAND, v); else localStorage.removeItem(HV4_LAND); } catch (e) { /* no storage */ } };

class HescV4Buttons extends HTMLElement {
  setConfig(config) {
    if (!config || !Array.isArray(config.buttons)) throw new Error("buttons: list required");
    this._config = config;
    this._open = -1;
    this._cards = [];
    this._built = false;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._built) this._build();
    this._update();
    this._cards.forEach((c) => { c.hass = hass; });
  }

  getCardSize() { return 1; }
  getGridOptions() { return { columns: "full", rows: "auto" }; }

  _build() {
    const root = this.attachShadow({ mode: "open" });
    const c = this._config;
    root.innerHTML = `<style>${CSS}</style><ha-card><div class="bar">
      ${c.live ? `<button class="live" id="live"><span class="sw"></span><b>Live</b><span id="lt"></span></button><div class="sep"></div>` : ""}
      ${c.buttons.map((b, i) => b.hidden ? "" : `<button class="pill" data-i="${i}"${b.demo_only ? " data-demo=\"1\"" : ""}>${b.color ? `<i style="background:${b.color}"></i>` : ""}<span>${b.name}</span><span class="dot" hidden></span></button>`).join("")}
      ${c.mode_toggle ? `<button class="pill mode" id="mode" title="Tijdelijke proefbordknop: alleen je eigen auto (echte gegevens) of de demo met twee auto's"></button>` : ""}
    </div></ha-card><div class="ov" id="ov" hidden><div class="win" role="dialog" aria-modal="true"><header><button class="back" id="back" hidden aria-label="Terug">‹</button><h3 id="wt"></h3><button class="ib" id="ib" hidden aria-label="Uitleg" aria-expanded="false">i</button><button class="x" aria-label="Close">✕</button></header><div class="tip" id="tip" hidden></div><div class="tabs" id="lvs" hidden></div><div class="tabs" id="tabs" hidden></div><div class="subs" id="subs" hidden></div><div class="tabs" id="pgs" hidden></div><div id="body" style="display:grid;gap:12px;grid-template-columns:minmax(0,1fr)"></div><div class="foot" id="foot" hidden><a href="#" id="setup">Instelscherm van Home Assistant</a></div></div></div>`;
    root.querySelectorAll(".pill[data-i]").forEach((p) => p.addEventListener("click", () => this._openWin(+p.dataset.i)));
    root.querySelector(".x").addEventListener("click", () => this._close());
    root.getElementById("ib").addEventListener("click", (e) => {
      const tip = root.getElementById("tip");
      tip.hidden = !tip.hidden;
      e.currentTarget.setAttribute("aria-expanded", String(!tip.hidden));
    });
    root.getElementById("back").addEventListener("click", () => { if (this._parent >= 0) this._openWin(this._parent); });
    root.getElementById("setup").addEventListener("click", (e) => {
      e.preventDefault();
      const b = this._config.buttons[this._open], path = b && b.setup_link;
      if (!path) return;
      this._close();
      history.pushState(null, "", path);
      window.dispatchEvent(new CustomEvent("location-changed"));
    });
    root.getElementById("ov").addEventListener("click", (e) => { if (e.target.id === "ov") this._close(); });
    const live = root.getElementById("live");
    if (live) live.addEventListener("click", () => this._toggleLive());
    const mode = root.getElementById("mode");
    if (mode) {
      mode.addEventListener("click", () => hv4SetMode(hv4Cur() === "real" ? "demo" : "real"));
      window.addEventListener("hesc-v4-mode", () => { this._modeText(); if (this._open >= 0) this._openWin(this._open, this._parent); });
      this._modeText();
    }
    this._esc = (e) => { if (e.key === "Escape" && this._open >= 0) this._close(); };
    // Other cards (the week overview) open a window by its id: hesc-v4-open {id}.
    window.addEventListener("hesc-v4-close", () => { if (this._open >= 0) this._close(); }); // the first start's "Klaar" button
    window.addEventListener("hesc-v4-open", (e) => {
      const i = this._config.buttons.findIndex((b) => b.id === e.detail.id);
      if (i >= 0) this._openWin(i);
    });
    this._built = true;
    // Decision 10-11-2026: "Openen op" the month page on this device (phone only)
    const land = hv4Land();
    if (land.startsWith("cal:") && window.matchMedia(HV4_PHONE).matches) {
      const ev = land.slice(4), i = this._config.buttons.findIndex((b) => (b.cards || []).some((c) => c.type === "custom:hesc-v4p-plan" && c.part === "calendar" && (c.ev || "ev1") === ev));
      if (i >= 0) setTimeout(() => this._openWin(i), 0);
    }
  }

  _modeText() {
    const m = this.shadowRoot.getElementById("mode");
    if (m) m.innerHTML = hv4Cur() === "real" ? "<b>Echt</b> · 1 auto" : "<b>Demo</b> · 2 auto's";
    this.shadowRoot.querySelectorAll("[data-demo]").forEach((p) => { p.hidden = hv4Cur() === "real"; }); // the example car's button goes with one car
  }

  _isLive() {
    // Live = HESC switches. With the shadow-mode switch, "on" means shadow, so Live is the opposite.
    const l = this._config.live;
    const s = this._hass.states[l.entity];
    if (!s) return false;
    return l.inverted ? s.state === "off" : s.state === "on";
  }

  _toggleLive() {
    const l = this._config.live;
    const goLive = !this._isLive();
    const turnOn = l.inverted ? !goLive : goLive;
    this._hass.callService(l.entity.split(".")[0], turnOn ? "turn_on" : "turn_off", { entity_id: l.entity });
  }

  _dot(b, deep = true) {
    const subs = (b.sub || []).concat(deep ? (b.tabs || []) : []).filter((id) => id !== b.id)
      .map((id) => this._config.buttons.find((x) => x.id === id)).filter(Boolean)
      .map((x) => ({ ...x, tabs: undefined }));
    if (subs.some((x) => this._dot(x))) return true;
    return (b.dot_when || []).some((r) => {
      const s = this._hass.states[r.entity];
      const v = s ? s.state : "unavailable";
      if (r.state !== undefined) return v === String(r.state);
      if (r.not_state !== undefined) return v !== String(r.not_state);
      if (r.missing) return !s || v === "unavailable" || v === "unknown";
      return false;
    });
  }

  _update() {
    const root = this.shadowRoot;
    const live = root.getElementById("live");
    if (live) {
      const on = this._isLive();
      live.classList.toggle("on", on);
      root.getElementById("lt").textContent = on ? (this._config.live.on_text || "stuurt") : (this._config.live.off_text || "schaduw");
    }
    root.querySelectorAll(".bar .pill").forEach((p) => {
      if (!p.querySelector(".dot")) return;
      p.querySelector(".dot").hidden = !this._dot(this._config.buttons[+p.dataset.i]);
    });
  }

  async _openWin(i, parent = -1) {
    const b = this._config.buttons[i];
    const root = this.shadowRoot;
    this._open = i;
    this._parent = parent;
    root.getElementById("wt").textContent = b.title || b.name;
    // wide windows show their cards in columns on a big screen, one below the other on a phone
    root.querySelector(".win").classList.toggle("wide", !!b.wide);
    root.querySelector(".win").classList.toggle("cols", !!b.cols); // fixed columns: one card per column
    root.getElementById("back").hidden = parent < 0;
    root.getElementById("foot").hidden = !b.setup_link; // decision 30-10 20:50: setup screen as a link at the bottom, like MCM
    const ib = root.getElementById("ib"), tip = root.getElementById("tip");
    ib.hidden = !b.info;
    ib.setAttribute("aria-expanded", "false");
    tip.hidden = true;
    tip.innerHTML = b.info ? infoHtml(b.info) : "";
    // Basis · Standaard · Expert on Algemeen and the car (decision 06-11-2026): "levels" = the same window at each level
    const lvs = root.getElementById("lvs"), lvIdx = (b.levels || []).map((id) => this._config.buttons.findIndex((x) => x.id === id)).filter((x) => x >= 0);
    lvs.hidden = lvIdx.length < 2;
    lvs.innerHTML = lvIdx.map((j) => `<button class="tab${j === i ? " on" : ""}" data-lv="${j}">${this._config.buttons[j].level}</button>`).join("");
    lvs.querySelectorAll("[data-lv]").forEach((t) => t.addEventListener("click", () => this._openWin(+t.dataset.lv, parent)));
    // level tabs (Basis · Standaard · Expert): each tab is a window of its own, sharing one tab row
    const tabs = root.getElementById("tabs"), tabIdx = (b.tabs || []).map((id) => this._config.buttons.findIndex((x) => x.id === id))
      .filter((x) => x >= 0 && !(hv4Cur() === "real" && this._config.buttons[x].demo_only));
    tabs.hidden = tabIdx.length < 2; // car tabs (Algemeen · EV1 · EV2) also show when opened from Instellingen
    tabs.innerHTML = tabIdx.map((j) => {
      const x = this._config.buttons[j];
      return `<button class="tab${j === i ? " on" : ""}" data-tab="${j}">${x.tab || x.name}${j !== i && this._dot({ ...x, tabs: undefined }) ? `<span class="dot"></span>` : ""}</button>`;
    }).join("");
    tabs.querySelectorAll("[data-tab]").forEach((t) => t.addEventListener("click", () => this._openWin(+t.dataset.tab, parent)));
    const subs = root.getElementById("subs");
    const subIdx = (b.sub || []).map((id) => this._config.buttons.findIndex((x) => x.id === id))
      .filter((x) => x >= 0 && !(hv4Cur() === "real" && this._config.buttons[x].demo_only));
    subs.hidden = !subIdx.length;
    subs.innerHTML = subIdx.map((j) => {
      const x = this._config.buttons[j];
      return `<button class="pill" data-sub="${j}">${x.color ? `<i style="background:${x.color}"></i>` : ""}<span>${x.name}</span>${this._dot(x) ? `<span class="dot"></span>` : ""}</button>`;
    }).join("");
    subs.querySelectorAll("[data-sub]").forEach((p) => p.addEventListener("click", () => this._openWin(+p.dataset.sub, i)));
    const body = root.getElementById("body");
    body.innerHTML = "";
    this._cards = [];
    const home = (x) => (x.tabs && x.tabs.length ? this._config.buttons.findIndex((y) => y.id === x.tabs[0]) : -1);
    let top = parent >= 0 ? parent : i;
    if (home(this._config.buttons[top]) >= 0) top = home(this._config.buttons[top]);
    root.querySelectorAll(".bar .pill").forEach((p) => p.classList.toggle("open", +p.dataset.i === top));
    // decision 01-11: keep the window clear of the HA sidebar - the overlay starts where this dashboard starts
    const ovEl = root.getElementById("ov"), left = Math.max(0, Math.round(this.getBoundingClientRect().left) - 8);
    ovEl.style.left = `${left}px`;
    ovEl.hidden = false;
    document.addEventListener("keydown", this._esc);
    const helpers = await window.loadCardHelpers();
    for (const cfg of b.cards || []) {
      const el = helpers.createCardElement(cfg);
      if (cfg.full_width) { el.style.columnSpan = "all"; el.style.gridColumn = "1/-1"; }
      el.hass = this._hass;
      body.appendChild(el);
      this._cards.push(el);
    }
    this._pages(b);
    root.querySelector(".x").focus();
  }

  /* Decision 10-11-2026: on a phone a window with columns (the planning) shows one column per page, with a
     tab row on top; the first column (the month) comes first. A big screen keeps the columns side by side. */
  _pages(b) {
    const root = this.shadowRoot, pgs = root.getElementById("pgs"), mq = window.matchMedia(HV4_PHONE);
    const cards = this._cards, names = (b.cards || []).map((c, j) => c.page || (j === 0 ? "Maand" : "Ritme en deze keer"));
    const show = () => {
      const paged = !!b.cols && cards.length > 1 && mq.matches;
      pgs.hidden = !paged;
      if (!paged) { cards.forEach((el) => { el.style.display = ""; }); return; }
      const k = Math.min(this._pg || 0, cards.length - 1);
      cards.forEach((el, j) => { el.style.display = j === k ? "" : "none"; });
      pgs.innerHTML = names.map((n, j) => `<button class="tab${j === k ? " on" : ""}" data-pg="${j}">${n}</button>`).join("");
      pgs.querySelectorAll("[data-pg]").forEach((t) => t.addEventListener("click", () => { this._pg = +t.dataset.pg; show(); root.getElementById("ov").scrollTop = 0; }));
    };
    this._pg = 0;
    if (this._mq) this._mq.removeEventListener("change", this._mqFn);
    this._mq = mq; this._mqFn = show; mq.addEventListener("change", show);
    show();
  }

  _close() {
    const root = this.shadowRoot;
    root.getElementById("ov").hidden = true;
    root.getElementById("body").innerHTML = "";
    this._cards = [];
    this._open = -1;
    document.removeEventListener("keydown", this._esc);
    root.querySelectorAll(".pill").forEach((p) => p.classList.remove("open"));
  }
}

/* ---------- start page with example data ---------- */

const PCSS = `
:host{--line:var(--divider-color,#30333c);--muted:var(--secondary-text-color,#9aa0aa);--card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));
  --ev1:#3fc8f4;--ev2:#ff8a65;--sun:#f5c542;--cheap:#b388ff;--dot:#ff9800}
.wrap{display:grid;gap:14px;container-type:inline-size}
.card{padding:16px 18px;min-width:0}
h2{font-size:16px;font-weight:500;margin:0 0 12px;display:flex;align-items:center;gap:8px}
h2 small{color:var(--muted);font-weight:400;font-size:12px;margin-left:auto}
h2 .ib{margin-left:auto}h2 small+.ib{margin-left:0}.card>.tip{margin:0 0 12px}
${INFO_CSS}
.row{display:grid;grid-template-columns:1.25fr 1fr;gap:14px}
@container (max-width:1100px){.row{grid-template-columns:minmax(0,1fr)}}
.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:13px;margin:0 0 12px}
.kv dt{color:var(--muted)}.kv dd{margin:0}
.kv2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 24px;margin:0 0 12px}.kv2 .kv{margin:0;align-content:start}
@media(max-width:600px){.kv2{grid-template-columns:minmax(0,1fr)}.kv2 .kv+.kv{margin-top:6px}}
.tl{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:0 10px;font-size:12px;color:var(--muted)}
.labs{display:grid;grid-auto-rows:26px;row-gap:8px;padding-top:24px}
.labs span{display:flex;flex-direction:column;justify-content:center;line-height:1.15;color:var(--primary-text-color);font-size:13px}
.labs small{color:var(--muted);font-size:11px}
.plot{position:relative;container-type:inline-size;padding-top:24px}
.rows{display:grid;grid-auto-rows:26px;row-gap:8px;position:relative}
.track{position:relative;background:var(--card2);border-radius:5px}
.blk{position:absolute;top:0;bottom:0;z-index:2;border-radius:4px;container-type:inline-size;overflow:hidden;display:flex;align-items:center;justify-content:center}
.blk.hi{bottom:auto;height:50%;border-radius:4px 4px 0 0}.scl{grid-column:1/-1;position:relative;height:30px;font-size:11px;color:var(--muted);margin:2px 0 4px}.scl span{position:absolute;top:0;transform:translateX(-50%)}.scl span:first-child{transform:none}.scl span:last-child{transform:translateX(-100%)}.scl em{position:absolute;top:14px;transform:translateX(-50%);font-style:normal;font-weight:600;white-space:nowrap}.scl em.g{color:var(--primary-text-color)}
.blk.low{top:auto;height:50%;border-radius:0 0 4px 4px}.blk.hi span,.blk.low span{display:none} /* decision 06-11 12:36: sun above, cheap below, no values (they show on hover) */.blk span{font-size:11px;font-weight:600;color:#14161b;white-space:nowrap;padding:0 4px}
@container (max-width:52px){.blk span{display:none}}
.blk.grid{background-image:repeating-linear-gradient(135deg,rgba(0,0,0,.22) 0 4px,transparent 4px 8px)}
.gl{position:absolute;top:24px;bottom:22px;width:1px;background:rgba(255,255,255,.07);pointer-events:none;z-index:1}
.gl.major{background:rgba(255,255,255,.18)}
.axis{position:relative;height:22px;font-size:12px;color:var(--primary-text-color)}
.axis span{position:absolute;top:5px;transform:translateX(-50%)}
@container (max-width:520px){.axis .odd{display:none}}
.now{position:absolute;top:18px;bottom:22px;width:3px;margin-left:-1.5px;background:var(--dot);border-radius:2px;z-index:3;box-shadow:0 0 0 1px rgba(0,0,0,.35);pointer-events:none}
.now b{position:absolute;top:-18px;left:50%;transform:translateX(-50%);background:var(--dot);color:#14161b;font-size:11px;
  font-weight:600;padding:1px 6px;border-radius:8px;white-space:nowrap}
.plan{display:grid;gap:4px;margin-top:10px;font-size:13px}
.plan div{display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}.plan i{display:inline-block;width:10px;height:10px;border-radius:50%;flex:none}
.plan em{font-style:normal;color:var(--muted)}
.conn{font-size:11px;white-space:nowrap}.conn.on{color:#66bb6a}.conn.off{color:var(--dot)}.conn.unk{color:var(--muted)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.car{display:grid;grid-template-columns:auto 1fr auto;gap:4px 12px;padding:10px 0;border-top:1px solid var(--line);align-items:center}
.car.first{border-top:0;padding-top:0}
.nm{font-weight:500;display:flex;align-items:center;gap:8px}.nm i{width:10px;height:10px;border-radius:50%}
.badge{font-size:11px;border-radius:999px;padding:2px 9px;border:1px solid var(--line);color:var(--muted)}
.badge.p1{color:var(--primary-text-color);border-color:var(--primary-text-color)}
.meta{grid-column:1/-1;font-size:12px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap}
.soc{grid-column:1/-1;height:8px;border-radius:4px;background:var(--card2);position:relative;overflow:hidden}
.soc b{position:absolute;inset:0 auto 0 0;border-radius:4px}.soc u{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--primary-text-color)}
.why{font-size:12px;color:var(--muted);background:var(--card2);border-radius:8px;padding:8px 10px;margin-top:6px}
.why b{color:var(--primary-text-color);font-weight:500}
.week{display:grid;grid-template-columns:70px repeat(7,minmax(56px,1fr));gap:6px;font-size:12px;min-width:520px}
.scroll{overflow-x:auto}
.hd{color:var(--muted);text-align:center}.hd.today{color:var(--primary-text-color);font-weight:500}
.lb{display:flex;align-items:center;gap:6px;color:var(--primary-text-color);font:inherit;font-size:12px;background:none;border:1px solid var(--line);border-radius:999px;padding:4px 8px;cursor:pointer;text-align:left}
.lb:hover,.cell:hover{background:var(--card2)}button.cell{font:inherit;font-size:12px;color:inherit;cursor:pointer;border:0}button.cell.off{border:1px dashed var(--line)}
.lb:focus-visible,.cell:focus-visible{outline:2px solid var(--primary-color);outline-offset:2px}
.lbx{display:none}.lb i{width:9px;height:9px;border-radius:50%}
.cell{background:var(--card2);border-radius:6px;padding:6px 4px;text-align:center;line-height:1.35}
.cell b{display:block;font-size:13px;font-weight:500}.cell span{color:var(--muted)}
.cell.off{color:var(--muted);background:transparent;border:1px dashed var(--line)}
button.cell.xoff{border:1.5px dashed var(--dot);color:var(--dot)}
button.cell.add{box-shadow:inset 0 0 0 1.5px var(--muted)}
.cell.own b{font-weight:700}
/* decision 30-10 20:27: the running (next) plan shows green */
button.cell.act{box-shadow:inset 0 0 0 1.5px #66bb6a;background:rgba(102,187,106,.16)}.cell.act span{color:#66bb6a}
.chg{border-top:1px solid var(--line);padding:12px 0 4px;display:grid;gap:8px}
.chg .hd2{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:500}.chg .hd2 .st{margin-left:auto}
.chg .st{font-size:12px;border-radius:999px;padding:3px 10px;border:1px solid var(--line);color:var(--muted)}
.chg .st.busy{border-color:var(--c);color:var(--c)}.chg .st.load{border-color:#66bb6a;color:#66bb6a}.chg .st.err{border-color:var(--dot);color:var(--dot)}
.chg .facts{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--muted)}.chg .facts b{color:var(--primary-text-color);font-weight:500}.badge.real{border-color:#66bb6a;color:#66bb6a}.cell.gone{opacity:.45}
.cell.skip b{text-decoration:line-through;color:var(--muted)}.cell.skip span{color:var(--dot)}
button.cell.once,button.cell.now{box-shadow:inset 0 0 0 1.5px var(--dot)}.cell.once span,.cell.now span{color:var(--dot)}
.demo{font-size:12px;color:var(--muted);padding:0 4px}
.wrap.one [data-car=ev1],.wrap.one [data-ev=ev1],.wrap.one .two{display:none!important}
.wrap:not(.one) .one-only{display:none!important}
`;

class HescV4Planning extends HTMLElement {
  setConfig(config) { this._config = config || {}; this._done = false; }
  set hass(hass) {
    { const ovw = this.shadowRoot && this.shadowRoot.querySelector("hesc-v4p-overview"); if (ovw) { if (!ovw._config) ovw.setConfig({ car: "ev1" }); ovw.hass = hass; } }
    if (!this._done) {
      this._seed(hass); this._render(); this._done = true;
      { const ovw = this.shadowRoot && this.shadowRoot.querySelector("hesc-v4p-overview"); if (ovw) { if (!ovw._config) ovw.setConfig({ car: "ev1" }); ovw.hass = hass; } }
      window.addEventListener("hesc-v4-mode", () => { this._mode(); this._status(this._hass); });
    }
    this._hass = hass;
    this._status(hass);
    this._real(hass);
    this._chargers(hass);
  }

  /* Start the planning sketch of the real car from its real v3 week plan (days, ready time, goal). */
  _seed(hass) {
    const real = this._config.real || {};
    window.__hescPlanSeed = window.__hescPlanSeed || {};
    for (const [k, r] of Object.entries(real)) {
      const w = r.week; if (!w) continue;
      const st = (id) => hass.states[id] && hass.states[id].state;
      const pct = parseInt(st(w.goal), 10), time = st(w.time);
      window.__hescPlanSeed[k] = {
        time: /^\d\d:\d\d$/.test(time || "") ? time : "07:00", pct: isNaN(pct) ? 75 : pct,
        days: w.days.map((id) => (st(w.on) === "on" && st(id) === "on" ? 1 : 0)),
        cal: {},
      };
      // v3's current charging plan (one day or the next week-plan day) shows as an extra day in the calendar
      try {
        const a = hass.states[r.plan] && hass.states[r.plan].attributes.plan, plan = typeof a === "string" ? JSON.parse(a) : a;
        if (plan && plan.deadline && plan.goal) {
          const d = new Date(plan.deadline);
          window.__hescPlanSeed[k].cal[plKey(d)] = { on: true, pct: plan.goal,
            time: `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}` };
        }
      } catch (e) { /* no plan */ }
    }
  }

  /* Charger status block(s): free / occupied / charging, its mode, pause, current. Only shown. */
  _chargers(hass) {
    const box = this.shadowRoot && this.shadowRoot.getElementById("chg");
    if (!box) return;
    const MODE = { eco_mode: "Eco (zon + net)", full_solar: "Alleen zon", off: "Vol vermogen (geen zonnestand)" };
    const STAT = [[/charging/i, "laadt"], [/eco-smart|waiting in queue/i, "wacht op zon (Eco-Smart)"], [/schedul/i, "wacht op schema"],
      [/paus/i, "gepauzeerd"], [/waiting for car|car demand/i, "aangesloten, auto vraagt niets"], [/ready|disconnected/i, "vrij"],
      [/lock/i, "vergrendeld"], [/error|fault/i, "storing"], [/update/i, "bijwerken"]];
    box.innerHTML = (this._config.chargers || []).map((c) => {
      if (c.example) { // example charger of the example car (two cars, two chargers); hidden with the real car alone
        const car = this._names[c.car];
        return `<div class="chg" data-car="${c.car}" style="--c:var(--${c.car})"><div class="hd2">Laadpaal · ${c.name}<span class="st load">laadt · ${car}</span></div>
          <div class="facts"><span>status <b>laadt</b></span><span>stand <b>Alleen zon</b></span><span>max. <b>32 A · 22 kW</b></span><span>vermogen <b>3,7 kW</b></span><span><em>voorbeeld</em></span></div></div>`;
      }
      const S = (id) => id && hass.states[id], v = (id) => (S(id) ? S(id).state : null);
      const raw = v(c.status) || "", stat = (STAT.find(([re]) => re.test(raw)) || [null, raw || "?"])[1];
      const con = v(c.connected) === "on", kwRaw = parseFloat(v(c.power)), kw = isNaN(kwRaw) ? null : (kwRaw > 100 ? kwRaw / 1000 : kwRaw);
      const car = c.car && this._names[c.car], col = c.car ? `var(--${c.car})` : "var(--primary-color)";
      const [cls, label] = kw && kw > 0.05 ? ["load", `laadt${car ? ` · ${car}` : ""}`] : /storing/.test(stat) ? ["err", "storing"]
        : con ? ["busy", `bezet${car ? ` · ${car}` : ""}`] : ["", "vrij"];
      const mode = v(c.mode), amps = v(c.current); // the pause switch is left out: "off" also means "waiting for sun"
      return `<div class="chg" style="--c:${col}"><div class="hd2">Laadpaal · ${c.name || "laadpaal"}<span class="st ${cls}">${label}</span></div>
        <div class="facts"><span>status <b>${stat}</b></span>${mode ? `<span>stand <b>${MODE[mode] || mode}</b></span>` : ""}
        ${amps ? `<span>max. <b>${amps} A</b></span>` : ""}
        ${kw !== null ? `<span>vermogen <b>${kw.toLocaleString(hv4Loc(), { maximumFractionDigits: 1 })} kW</b></span>` : ""}</div></div>`;
    }).join("");
  }

  /* Real numbers for the car that HESC v3 already drives: battery, charging, its charging plan. Only shown, nothing calculated. */
  _real(hass) {
    const root = this.shadowRoot, real = this._config.real || {};
    if (!root) return;
    const lang = (hass.locale && hass.locale.language) || hass.language || "en";
    for (const [k, r] of Object.entries(real)) {
      const S = (id) => hass.states[id], num = (id) => { const x = S(id); const v = x ? parseFloat(x.state) : NaN; return isNaN(v) ? null : v; };
      let plan = {};
      try { const a = S(r.plan) && S(r.plan).attributes.plan; plan = typeof a === "string" ? JSON.parse(a) : (a || {}); } catch (e) { plan = {}; }
      const soc = num(r.soc), kw = num(r.power), con = S(r.connected) && S(r.connected).state === "on";
      const fb = S(r.soc) ? S(r.soc).attributes : {}, est = fb.estimated === true || (fb.source && fb.source !== "main");
      const goal = plan.goal || num(r.full) || 80, now = Date.now();
      const q = [...new Set((plan.planned || []).map((t) => new Date(t).getTime()))].filter((t) => t + 15 * 60000 > now).sort((a, b) => a - b);
      const hm = (t) => new Date(t).toLocaleTimeString(hv4Loc(), { hour: "2-digit", minute: "2-digit" });
      const day = (t) => { const d = new Date(t), td = new Date(); const n = Math.round((new Date(d).setHours(0, 0, 0, 0) - td.setHours(0, 0, 0, 0)) / 864e5);
        return n === 0 ? "" : n === 1 ? "morgen " : `${PL_DAYS[plWd(d)]} ${d.getDate()} `; };
      const stTxt = S(r.status) ? ((S(r.status).attributes || {})[lang] || S(r.status).state) : "";
      const doing = kw && kw > 0.05 ? `laadt · ${(kw > 100 ? kw / 1000 : kw).toLocaleString(hv4Loc(), { maximumFractionDigits: 1 })} kW` : !con ? "niet aangesloten" : (stTxt || "wacht");
      const row = root.getElementById(`car-${k}`);
      if (row) row.innerHTML = `<span class="nm"><i style="background:var(--${k})"></i>${this._names[k]}</span><span class="meta" style="grid-column:auto">${doing}</span><span class="badge real">echt</span>
        <div class="soc"><b style="width:${soc ?? 0}%;background:var(--${k})"></b><u style="left:${goal}%"></u></div>
        <div class="scl">${[0, 25, 50, 75, 100].map((x) => `<span style="left:${x}%">${x}%</span>`).join("")}${soc === null ? "" : `<em style="left:${soc}%;color:var(--${k})">nu ${Math.round(soc)}%</em>`}<em class="g" style="left:${goal}%">doel ${goal}%</em></div>
        <div class="meta"><span>${soc === null ? "?" : Math.round(soc)}% → ${goal}%${est ? ` <em style="color:var(--dot);font-style:normal">(geschat)</em>` : ""}</span>${plan.deadline_text ? `<span>gereed ${plan.deadline_text}</span>` : ""}${plan.need_kwh ? `<span>nog ± ${Math.round(plan.need_kwh)} kWh</span>` : ""}<span>${q.length ? `volgend netblok ${day(q[0])}${hm(q[0])}` : "geen netblok gepland"}</span></div>`;
      // its grid quarters in the timeline (12:00 today/yesterday → 24 h)
      const start = new Date(); if (start.getHours() < 12) start.setDate(start.getDate() - 1); start.setHours(12, 0, 0, 0);
      const W = 24 * 3600000, blocks = [];
      for (const t of q) {
        const b = blocks[blocks.length - 1];
        if (b && t === b[1]) b[1] = t + 15 * 60000; else blocks.push([t, t + 15 * 60000]);
      }
      const kwh = (b) => ((b[1] - b[0]) / 3600000 * (plan.kw || 11));
      const trk = root.getElementById(`trk-${k}`);
      if (trk) trk.innerHTML = blocks.filter((b) => b[1] > start && b[0] < start.getTime() + W).map((b) => {
        const l = Math.max(0, (b[0] - start) / W * 100), w = Math.min(100, (b[1] - start) / W * 100) - l;
        return `<div class="blk grid" style="left:${l}%;width:${w}%;background-color:var(--${k})" title="${hm(b[0])}–${hm(b[1])} · net ± ${Math.round(kwh(b))} kWh"><span>net ± ${Math.round(kwh(b))} kWh</span></div>`;
      }).join("");
      const pl = root.getElementById(`pl-${k}`);
      if (pl) pl.innerHTML = blocks.length
        ? `${blocks.slice(0, 3).map((b) => `${day(b[0])}${hm(b[0])}–${hm(b[1])} van het net (± ${Math.round(kwh(b))} kWh)`).join(" · ")}${blocks.length > 3 ? " · …" : ""} <em>→ ${goal}% ${plan.deadline_text || ""}</em>`
        : `nog niets van het net gepland <em>→ ${goal}% ${plan.deadline_text || ""}</em>`;
      const nl = root.getElementById("nowl");
      if (nl) { const p = (now - start) / W * 100; nl.style.left = `${p}%`; nl.querySelector("b").textContent = `nu ${hm(now)}`; }
    }
  }

  // Real status lines from HESC (v3 entities): text in the user's language when HESC provides it.
  _status(hass) {
    const box = this.shadowRoot && this.shadowRoot.getElementById("st");
    if (!box) return;
    const lang = (hass.locale && hass.locale.language) || hass.language || "en";
    const txt = (id) => {
      const s = hass.states[id];
      if (!s || ["unknown", "unavailable", "", "none"].includes(s.state)) return null;
      return (s.attributes && s.attributes[lang]) || s.state;
    };
    const rows = (this._config.status || []).map((r) => {
      if (r.when && (!hass.states[r.when] || hass.states[r.when].state !== "on")) return null;
      const v = r.text || txt(r.entity);
      return v ? [r.name, v] : null;
    }).filter(Boolean).concat((this._extra || []).filter((r) => !(hv4Cur() === "real" && r[2] === "ev1"))
      .map((r) => (hv4Cur() === "real" ? [r[0], `${r[1]} <em style="color:var(--muted)">(voorbeeld)</em>`] : [r[0], r[1]])));
    // Two blocks side by side in the same card (one column on a phone); left gets the extra row when odd.
    const half = Math.ceil(rows.length / 2);
    const dl = (part) => `<dl class="kv">${part.map(([n, v]) => `<dt>${n}</dt><dd>${v}</dd>`).join("")}</dl>`;
    box.innerHTML = dl(rows.slice(0, half)) + dl(rows.slice(half));
    // Plugged in or not, per car (config connected: {ev1: entity, ev2: entity}; no entity = example "unknown").
    const con = this._config.connected || {};
    this.shadowRoot.querySelectorAll("[data-conn]").forEach((el) => {
      const id = con[el.dataset.conn], st = id && hass.states[id];
      const v = st ? st.state : null;
      const on = v === "on" || v === "true", off = v === "off" || v === "false";
      el.className = `conn ${on ? "on" : off ? "off" : "unk"}`;
      el.textContent = on ? "● aangesloten" : off ? "○ niet aangesloten" : "? onbekend";
    });
  }
  getCardSize() { return 12; }
  getGridOptions() { return { columns: "full", rows: "auto" }; }

  _render() {
    const ev1 = this._config.ev1 || "EV1", ev2 = this._config.ev2 || "EV2";
    this._extra = [
      ["Prijs nu", "€ 0,231 /kWh · goedkoopst vannacht 02:15–04:00 (€ 0,171)"],
      ["Zon nu", `1,9 kW overschot · gaat naar <b style="color:var(--ev1)">${ev1}</b> (meeste kWh nodig)`, "ev1"],
    ];
    const H = (h) => ((h - 12 + 24) % 24) / 24 * 100;
    // [start h, end h, colour, opacity, text in the block, from the grid (hatched)]
    const rows = [
      ["Zon · goedkoop", "", [[12, 16.5, "sun", 1, "± 9 kWh over", false, "hi"], [8.5, 12, "sun", .55, "morgen ± 7 kWh", false, "hi"], [1.5, 5, "cheap", .9, "€ 0,17", false, "low"], [13.25, 14.5, "cheap", .9, "€ 0,19", false, "low"]]],
      [ev1, "ev1", [[12.5, 16.5, "ev1", 1, "zon ± 10 kWh"], [2.25, 4, "ev1", 1, "net ± 13 kWh", true]]],
      [ev2, "ev2", (this._config.real || {}).ev2 ? "real" : [[4, 4.75, "ev2", 1, "net ± 3 kWh", true]]],
    ];
    const NOW = 13.75;
    const hhmm = (h) => `${String(Math.floor(h) % 24).padStart(2, "0")}:${String(Math.round((h % 1) * 60)).padStart(2, "0")}`;
    const labs = rows.map(([lab, ev]) => `<span${ev ? ` data-car="${ev}"` : ""}>${lab}${ev ? `<small class="conn" data-conn="${ev}"></small>` : ""}</span>`).join("");
    const tracks = rows.map(([, k, bl]) => bl === "real" ? `<div class="track" id="trk-${k}"></div>` : `<div class="track"${k ? ` data-car="${k}"` : ""}>${bl.map(([a, b, c, o, t, g, low]) => {
      let st = H(a), e = H(b); if (e <= st) e = 100;
      return `<div class="blk${g ? " grid" : ""}${low ? " " + low : ""}" style="left:${st}%;width:${e - st}%;background-color:var(--${c});opacity:${o}" title="${hhmm(a)}–${hhmm(b)} · ${t}"><span>${t}</span></div>`;
    }).join("")}</div>`).join("");
    const hours = Array.from({ length: 24 }, (_, k) => (12 + k) % 24);
    const grid = hours.map((x) => `<div class="gl${x % 4 === 0 ? " major" : ""}" style="left:${H(x)}%"></div>`).join("");
    const axis = hours.filter((x) => x % 2 === 0).map((x) => `<span class="${x % 4 ? "odd" : ""}" style="left:${H(x)}%">${String(x).padStart(2, "0")}:00</span>`).join("");
    const tl = `<div class="labs">${labs}</div><div class="plot">${grid}<div class="now" id="nowl" style="left:${H(NOW)}%"><b>nu ${hhmm(NOW)}</b></div>`
      + `<div class="rows">${tracks}</div><div class="axis">${axis}</div></div>`;
    const planTxt = `<div class="plan">
      <div data-car="ev1"><i style="background:var(--ev1)"></i><b>${ev1}</b><small class="conn" data-conn="ev1"></small><span>12:30–16:30 op zon (± 10 kWh) · 02:15–04:00 van het net (± 13 kWh) <em>→ 80% wo 07:30</em></span></div>
      <div><i style="background:var(--ev2)"></i><b>${ev2}</b><small class="conn" data-conn="ev2"></small><span id="pl-ev2">04:00–04:45 van het net (± 3 kWh) <em>→ 70% wo 07:30</em></span></div></div>`;
    const root = this.attachShadow({ mode: "open" });
    root.innerHTML = `<style>${PCSS}</style><div class="wrap">
      <div class="demo"><span class="two">Proefbord HESC v4 · demo met twee voorbeeldauto's (${ev1} en ${ev2}) · je echte auto staat in de stand Echt · nog geen rekenwerk voor twee auto's</span><span class="one-only"></span></div>
      <div class="row" style="grid-template-columns:minmax(0,1fr)">
        <hesc-v4p-overview></hesc-v4p-overview>
        <ha-card class="card" style="display:none"><h2>Vandaag en morgen <small>${this._config.version || ""}</small></h2>
          <div class="kv2" id="st"></div>
          <div class="tl">${tl}</div>${planTxt}
          <div class="legend"><span><i style="background:var(--sun)"></i>Zon verwacht</span><span data-car="ev1"><i style="background:var(--ev1)"></i>${ev1} laadt</span><span><i style="background:var(--ev2)"></i>${ev2} laadt</span><span><i style="background:var(--cheap)"></i>Goedkope kans</span><span><i style="background:repeating-linear-gradient(135deg,var(--muted) 0 3px,transparent 3px 6px)"></i>gestreept = van het net</span></div>
        </ha-card>
        <ha-card class="card" style="display:none"><h2>Lopende planning <button class="ib" data-tip="tp" aria-label="Uitleg" aria-expanded="false">i</button></h2><div class="tip" id="tp" hidden>${infoHtml("Wie gaat voor en waarom.\n\n- Moeten beide op dezelfde tijd klaar zijn, dan gaat de auto voor die de meeste kWh nodig heeft.\n- Zelfde tijd en zelfde kWh: de eerste auto gaat voor.\n- Wisselen gebeurt alleen op een heel kwartier.\n- **(geschat)** betekent: de accustand van die auto meldt niets, HESC rekent met een schatting.")}</div>
          <div class="car first" data-car="ev1"><span class="nm"><i style="background:var(--ev1)"></i>${ev1}</span><span class="meta" style="grid-column:auto">laadt op zon · 3,7 kW</span><span class="badge p1">gaat voor</span>
            <div class="soc"><b style="width:46%;background:var(--ev1)"></b><u style="left:80%"></u></div>
            <div class="meta"><span>46% → 80%</span><span>gereed wo 07:30</span><span>nog ± 26 kWh</span><span>volgend netblok 02:15</span></div></div>
          <div class="car" id="car-ev2"><span class="nm"><i style="background:var(--ev2)"></i>${ev2}</span><span class="meta" style="grid-column:auto">wacht</span><span class="badge">daarna</span>
            <div class="soc"><b style="width:58%;background:var(--ev2)"></b><u style="left:70%"></u></div>
            <div class="meta"><span>58% → 70% <em style="color:var(--dot);font-style:normal">(geschat)</em></span><span>gereed wo 07:30</span><span>nog ± 3 kWh</span><span>volgend netblok 04:00</span></div></div>
          <div id="chg"></div>
          <div class="why two"><b style="color:var(--ev1)">${ev1}</b> gaat voor: beide moeten wo 07:30 klaar zijn en ${ev1} heeft <b>de meeste kWh</b> nodig (± 26 tegen ± 3). <em>Voorbeeld; het echte rekenwerk komt in de alpha.</em></div>
        </ha-card>
      </div>
      <ha-card class="card"><h2>Komende week <button class="ib" data-tip="tw" aria-label="Uitleg" aria-expanded="false">i</button></h2><div class="tip" id="tw" hidden>${infoHtml("De komende zeven dagen per auto: accu-% en klaar-tijd. Tik op een auto of een dag om die auto te plannen.\n\nOranje rand = uitzondering: alleen deze keer, overgeslagen of een dag uit. Vette tekst = dag met eigen tijd of %.")}</div><div class="scroll"><div class="week" id="wk"></div></div></ha-card>
    </div>`;
    root.querySelectorAll("[data-tip]").forEach((btn) => btn.addEventListener("click", () => {
      const tip = root.getElementById(btn.dataset.tip);
      tip.hidden = !tip.hidden;
      btn.setAttribute("aria-expanded", String(!tip.hidden));
    }));
    this._names = { ev1, ev2 };
    this._mode();
    this._week();
    if (!this._onPlan) {
      this._onPlan = () => this._week();
      window.addEventListener("hesc-v4-plan-changed", this._onPlan);
    }
  }

  /* Temporary switch: "real" shows only the real car (one EV, as a v4 user with one car sees it). */
  _mode() {
    const w = this.shadowRoot && this.shadowRoot.querySelector(".wrap");
    if (w) w.classList.toggle("one", hv4Cur() === "real");
  }

  /* The next seven days per car, from the same example planning as the planning windows. */
  _week() {
    const root = this.shadowRoot, box = root && root.getElementById("wk");
    if (!box) return;
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const dates = Array.from({ length: 7 }, (_, i) => { const d = new Date(today); d.setDate(today.getDate() + i); return d; });
    const head = `<span></span>` + dates.map((d, i) => `<span class="hd${i < 2 ? " today" : ""}">${i === 0 ? "vandaag" : i === 1 ? "morgen" : `${PL_DAYS[plWd(d)]} ${d.getDate()}`}</span>`).join("");
    const rows = ["ev1", "ev2"].map((k) => {
      const s = plState(k), n = this._names[k], nx = plNext(s), o = s.once;
      const cells = dates.map((d, i) => {
        const p = plDay(s, d), isNext = nx && +new Date(nx.d).setHours(0, 0, 0, 0) === +d;
        const gone = i === 0 && p.on && !isNext; // today's ready time has already passed
        if (i === 0 && o && o.kind === "now") return `<button class="cell now" data-ev="${k}"><b>nu → ${o.pct}%</b><span>alleen nu</span></button>`;
        if (!p.on) return `<button class="cell off${p.src === "off" || p.src === "vac" ? " xoff" : ""}" data-ev="${k}">${p.src === "off" ? "uit" : p.src === "vac" ? "vakantie" : "vrij"}</button>`;
        if (isNext && o && o.kind === "skip") return `<button class="cell skip" data-ev="${k}"><b>${p.pct}%</b><span>slaat over</span></button>`;
        if (isNext && o && o.kind === "other") return `<button class="cell once" data-ev="${k}"><b>${o.pct}%</b><span>${o.time} · deze keer</span></button>`;
        if (gone) return `<button class="cell gone" data-ev="${k}"><b>${p.pct}%</b><span>geweest</span></button>`;
        return `<button class="cell${p.src === "add" ? " add" : ""}${p.src === "own" ? " own" : ""}${isNext ? " act" : ""}" data-ev="${k}"><b>${p.pct}%</b><span>${p.time}</span></button>`;
      }).join("");
      return `<button class="lb" data-ev="${k}" aria-label="Planning ${n}"><i style="background:var(--${k})"></i>${n}</button>` + cells;
    }).join("");
    box.innerHTML = head + rows;
    const open = this._config.open || {};
    box.querySelectorAll("[data-ev]").forEach((el) => el.addEventListener("click", () => {
      const id = open[el.dataset.ev];
      if (id) window.dispatchEvent(new CustomEvent("hesc-v4-open", { detail: { id } }));
    }));
  }
}

/* ---------- planning sketch per car: rhythm, only this time, calendar (example data, in memory only) ---------- */

const PLCSS = `
:host{--line:var(--divider-color,#30333c);--muted:var(--secondary-text-color,#9aa0aa);--card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));--dot:#ff9800}
ha-card{padding:16px 18px;display:grid;gap:18px}
section{display:grid;gap:12px}
h4{margin:0;font-size:15px;font-weight:500;display:flex;align-items:center;gap:8px}
h4 .ib{margin-left:auto}
.lbl{font-size:12px;color:var(--muted);margin-bottom:4px}
.pair{display:grid;grid-template-columns:auto minmax(0,1fr);gap:14px 18px;align-items:end}
@media(max-width:480px){.pair{grid-template-columns:minmax(0,1fr)}}
/* own controls: time stepper, % slider, switch */
.stp{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:var(--card2);height:40px}
.stp button{width:40px;height:40px;border:0;background:none;color:var(--primary-text-color);font-size:20px;cursor:pointer;border-radius:50%}
.stp button:hover{background:color-mix(in srgb,var(--c) 25%,transparent)}
.stp b{min-width:62px;text-align:center;font-size:18px;font-weight:600;font-variant-numeric:tabular-nums}
.stp.sm{height:34px}.stp.sm button{width:34px;height:34px;font-size:18px}.stp.sm b{min-width:46px;font-size:15px}
.sl{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;height:40px}
.sl output{font-size:18px;font-weight:600;min-width:52px;text-align:right;font-variant-numeric:tabular-nums}
.sl input{-webkit-appearance:none;appearance:none;width:100%;height:10px;border-radius:999px;margin:0;cursor:pointer;
  background:linear-gradient(90deg,var(--c) 0 var(--v),var(--card2) var(--v) 100%);border:1px solid var(--line)}
.sl input::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:#fff;border:3px solid var(--c);box-shadow:0 1px 4px rgba(0,0,0,.4)}
.sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid var(--c)}
.sl input:focus-visible{outline:2px solid var(--primary-color);outline-offset:4px}
.tg{width:48px;height:28px;border-radius:999px;border:0;background:var(--card2);box-shadow:inset 0 0 0 1.5px var(--line);position:relative;cursor:pointer;flex:none}
.tg::after{content:"";position:absolute;top:4px;left:4px;width:20px;height:20px;border-radius:50%;background:var(--muted);transition:left .15s,background .15s}
.tg.on{background:var(--c);box-shadow:none}.tg.on::after{left:24px;background:#fff}
.days{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px}
.day{display:grid;gap:2px;justify-items:center;padding:8px 2px;border-radius:12px;border:1.5px solid var(--line);background:none;
  color:var(--primary-text-color);font:inherit;cursor:pointer;min-width:0}
.day b{font-size:13px}.day span{font-size:11px;color:var(--muted);white-space:nowrap}
.day.on{background:color-mix(in srgb,var(--c) 22%,transparent);border-color:var(--c)}
.day.own span{color:var(--primary-text-color);font-weight:600}
.day.sel{outline:2px solid var(--primary-color);outline-offset:1px}
.ed{display:grid;gap:12px;background:var(--card2);border-radius:12px;padding:12px 14px}
.ed .top{display:flex;align-items:center;gap:10px;font-size:15px}.ed .top b{flex:1}
.ed .pair .stp{background:var(--ha-card-background,var(--card-background-color,#1c1c1c))}
.ed .sl input{background:linear-gradient(90deg,var(--c) 0 var(--v),var(--ha-card-background,var(--card-background-color,#1c1c1c)) var(--v) 100%)}
.ed.off .pair{opacity:.35;pointer-events:none}
.btn{font:inherit;font-size:13px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:7px 14px;cursor:pointer}
.btn:hover{border-color:var(--c)}.btn.pri{background:var(--c);border-color:var(--c);color:#14161b;font-weight:600}
.btn.act{border-color:var(--c);background:color-mix(in srgb,var(--c) 22%,transparent)}
.next{font-size:14px}.next em{font-style:normal;color:var(--muted)}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.exc{display:flex;gap:10px;align-items:center;flex-wrap:wrap;border-left:3px solid var(--dot);background:var(--card2);border-radius:8px;padding:8px 12px;font-size:14px}
details{border-top:1px solid var(--line);padding-top:12px}
summary{cursor:pointer;font-size:15px;font-weight:500;list-style:none;display:flex;align-items:center;gap:8px}
summary::-webkit-details-marker{display:none}summary::before{content:"›";font-size:20px;transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details.fix{border-top:0;padding-top:0}details.fix summary{pointer-events:none}details.fix summary::before{display:none}details.fix summary .ib{pointer-events:auto}
.cal{display:grid;gap:8px;margin-top:10px}
.mon{display:flex;align-items:center;gap:8px;font-size:14px}.mon b{flex:1;text-align:center;font-weight:500}
.grid7{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px}
.wd{font-size:11px;color:var(--muted);text-align:center}
.cd{min-height:46px;border-radius:8px;border:1px solid var(--line);background:none;color:var(--primary-text-color);font:inherit;
  display:grid;align-content:start;justify-items:start;padding:4px 5px;cursor:pointer;min-width:0;text-align:left}
.cd b{font-size:12px;font-weight:500}.cd span{font-size:10px;color:var(--muted);white-space:nowrap;overflow:hidden;max-width:100%}
.cd.on{background:color-mix(in srgb,var(--c) 18%,transparent);border-color:color-mix(in srgb,var(--c) 60%,transparent)}
.cd.add{border:1.5px dashed var(--c)}.cd.off{border:1.5px dashed var(--dot)}.cd.off span{color:var(--dot)}
.cd.past{opacity:.35;cursor:default}.cd.today b{color:var(--primary-color);font-weight:700}
.cd.today{outline:2px solid var(--primary-text-color);outline-offset:2px;box-shadow:0 0 0 5px color-mix(in srgb,var(--primary-text-color) 18%,transparent)}
.cd.today b{background:var(--primary-text-color);color:var(--ha-card-background,#1f2128)!important;border-radius:6px;padding:0 5px} /* decision 01-11: today stands out, also on a blue car */
.cd.blank{visibility:hidden}
summary{display:flex;align-items:center;gap:8px}summary .ib{margin-left:auto}
.grid7{touch-action:pan-y;user-select:none}.dayed{margin:10px 0;border:1px solid var(--c);border-radius:12px;padding:10px 12px;background:color-mix(in srgb,var(--c) 8%,transparent)}.dayh{display:flex;gap:8px;align-items:baseline;margin-bottom:6px}.dayh span{font-size:12px;color:var(--muted)}.dayed .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.vpick{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:6px 0}.vpick span{flex:1;font-size:13px;color:var(--muted)}.btn.act{background:color-mix(in srgb,var(--c) 30%,transparent)}.land{display:flex;gap:8px;align-items:center;font-size:13px;color:var(--muted);margin-top:10px;cursor:pointer}.land input{width:18px;height:18px;accent-color:var(--c)}.cd.vac{border:1.5px solid var(--c);background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--c) 28%,transparent) 0 4px,transparent 4px 8px)}.cd.vac span{color:var(--c)}
.cd.sel{outline:2px solid var(--primary-color);outline-offset:-1px}.vacl{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:4px 0 8px}.vacl b{color:var(--primary-text-color)}.vacl .btn{margin-left:auto}
.vacsw{background:repeating-linear-gradient(135deg,var(--c) 0 3px,transparent 3px 6px);border:1px solid var(--c)}
@media(max-width:520px){.cd span{display:none}.cd{min-height:36px}.cd.on::after,.cd.add::after{content:"";width:6px;height:6px;border-radius:50%;background:var(--c);margin-top:3px}}
.leg{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.leg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-2px;border:1px solid var(--line)}
${INFO_CSS}`;

const PL_DAYS = hv4Arr({ nl: ["ma", "di", "wo", "do", "vr", "za", "zo"], en: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], de: ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"] });
const PL_LONG = hv4Arr({ nl: ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"], en: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], de: ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"] });
const PL_MON = hv4Arr({ nl: ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"], en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], de: ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"] });
const plFmt = (k) => { const d = new Date(k + "T12:00:00"); return `${d.getDate()} ${PL_MON[d.getMonth()].slice(0, 3)}`; };
const plKey = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const plWd = (d) => (d.getDay() + 6) % 7; // monday = 0
const plStep = (t, dir) => { // time +/- 15 minutes, wraps around midnight
  const [h, m] = t.split(":").map(Number), v = (h * 60 + m + dir * 15 + 1440) % 1440;
  return `${String(Math.floor(v / 60)).padStart(2, "0")}:${String(v % 60).padStart(2, "0")}`;
};
// Example data per car, shared by the planning windows and the start page (kept for this page visit only).
const PL_DEFAULTS = {
  ev1: { time: "07:30", pct: 65, days: [1, 1, 1, 1, 1, 0, 0], sunday: { on: true, time: "18:00", pct: 60 } },
  ev2: { time: "07:30", pct: 70, days: [1, 1, 1, 0, 1, 0, 0] },
};
function plState(ev) {
  window.__hescPlan = window.__hescPlan || {};
  if (!window.__hescPlan[ev]) {
    const d = (window.__hescPlanSeed && window.__hescPlanSeed[ev]) || PL_DEFAULTS[ev] || PL_DEFAULTS.ev1;
    window.__hescPlan[ev] = { std: { time: d.time, pct: d.pct }, week: d.days.map((x) => ({ on: !!x })), cal: { ...(d.cal || {}) }, once: null };
    if (d.sunday) window.__hescPlan[ev].week[6] = { ...d.sunday };
  }
  return window.__hescPlan[ev];
}
function plDay(s, d) { // effective plan for a date: {on, time, pct, src: "week"|"own"|"add"|"off"|"vac"|""}
  const c = s.cal[plKey(d)], w = s.week[plWd(d)], std = s.std;
  // decision 30-10 21:06: a holiday period (dragged in the calendar) switches every day in it off; afterwards the rhythm is back
  if (s.vac && plKey(d) >= s.vac.from && plKey(d) <= s.vac.to) return { on: false, src: "vac" };
  if (c) return c.on ? { on: true, time: c.time || std.time, pct: c.pct || std.pct, src: "add" } : { on: false, src: "off" };
  if (!w.on) return { on: false, src: "" };
  return { on: true, time: w.time || std.time, pct: w.pct || std.pct, src: w.time || w.pct ? "own" : "week" };
}
function plNext(s, skip = 0) {
  const now = new Date();
  for (let i = 0; i < 21; i++) {
    const d = new Date(now); d.setDate(now.getDate() + i);
    const p = plDay(s, d);
    if (!p.on) continue;
    const [h, m] = p.time.split(":").map(Number);
    const t = new Date(d); t.setHours(h, m, 0, 0);
    if (t > now && skip-- <= 0) return { d, ...p };
  }
  return null;
}
const plChanged = () => window.dispatchEvent(new CustomEvent("hesc-v4-plan-changed"));

class HescV4Plan extends HTMLElement {
  setConfig(config) {
    this._config = config || {};
    this._s = plState(this._config.ev || "ev1");
    this._sel = -1;
    this._month = new Date(); this._month.setDate(1);
    // decision 30-10 20:55: part "plan" = rhythm + only this time, part "calendar" = the calendar alone (own column)
    this._part = this._config.part || "all";
    if (!this._onChg) { this._onChg = () => this._render(); window.addEventListener("hesc-v4-plan-changed", this._onChg); }
    this._render();
  }
  set hass(hass) { this._hass = hass; }
  getCardSize() { return 8; }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const s = this._s, c = this._config.color || "var(--primary-color)", name = this._config.name || "EV";
    const stp = (id, t, sm) => `<div class="stp${sm ? " sm" : ""}" data-t="${id}"><button data-dir="-1" aria-label="15 minuten eerder">−</button><b>${t}</b><button data-dir="1" aria-label="15 minuten later">+</button></div>`;
    const pstp = (id, v) => `<div class="stp sm" data-pp="${id}"><button data-dir="-1" aria-label="5% minder">−</button><b>${v}%</b><button data-dir="1" aria-label="5% meer">+</button></div>`;
    const sl = (id, v) => `<div class="sl"><input type="range" min="15" max="100" step="5" value="${v}" data-p="${id}" style="--v:${(v - 15) / 85 * 100}%" aria-label="accu %"><output>${v}%</output></div>`;
    const days = s.week.map((w, i) => {
      const t = w.time || s.std.time, p = w.pct || s.std.pct;
      return `<button class="day${w.on ? " on" : ""}${w.time || w.pct ? " own" : ""}${this._sel === i ? " sel" : ""}" data-d="${i}"><b>${PL_DAYS[i]}</b><span>${w.on ? t : "vrij"}</span><span>${w.on ? `${p}%` : "&nbsp;"}</span></button>`;
    }).join("");
    let ed = "";
    if (this._sel >= 0) {
      const w = s.week[this._sel];
      ed = `<div class="ed${w.on ? "" : " off"}"><div class="top"><b>${PL_LONG[this._sel]}</b><span>laden</span><button class="tg${w.on ? " on" : ""}" id="eon" role="switch" aria-checked="${w.on}" aria-label="laden op ${PL_LONG[this._sel]}"></button></div>
        <div class="pair"><div><div class="lbl">klaar om</div>${stp("day", w.time || s.std.time)}</div><div><div class="lbl">accu</div>${sl("day", w.pct || s.std.pct)}</div></div>
        <div class="row"><span style="flex:1"></span><button class="btn" id="estd">standaard</button><button class="btn pri" id="eok">klaar</button></div></div>`;
    }
    const o = s.once;
    const when = (x) => `${PL_DAYS[plWd(x.d)]} ${x.d.getDate()} ${PL_MON[x.d.getMonth()].slice(0, 3)}`;
    const nx = plNext(s);
    let nxTxt = nx ? `${when(nx)} · klaar om <b>${nx.time}</b> · <b>${nx.pct}%</b>` : "geen lading gepland";
    if (nx && o && o.kind === "skip") {
      const n2 = plNext(s, 1);
      nxTxt = `<s>${when(nx)} ${nx.time}</s> overgeslagen · daarna ${n2 ? `${when(n2)} · klaar om <b>${n2.time}</b> · <b>${n2.pct}%</b>` : "niets gepland"}`;
    } else if (nx && o && o.kind === "other") {
      nxTxt = `${when(nx)} · klaar om <b>${o.time}</b> · <b>${o.pct}%</b> <em>(alleen deze keer)</em>`;
    } else if (o && o.kind === "now") {
      nxTxt = `nu, tot <b>${o.pct}%</b> · daarna weer het ritme`;
    }
    const onceTxt = !o ? "" : o.kind === "skip" ? "Eerstvolgende keer overslaan" : o.kind === "now" ? `Nu laden tot <b>${o.pct}%</b>` : "Eerstvolgende keer andere tijd of %";
    this._nowPct = this._nowPct || 80;
    const m = this._month, first = new Date(m), today = new Date(); today.setHours(0, 0, 0, 0);
    const dim = new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
    let cells = PL_DAYS.map((d) => `<span class="wd">${d}</span>`).join("") + `<span class="cd blank"></span>`.repeat(plWd(first));
    for (let n = 1; n <= dim; n++) {
      const d = new Date(m.getFullYear(), m.getMonth(), n), p = plDay(s, d), past = d < today;
      const cls = ["cd", p.on ? "on" : "", p.src === "add" ? "add" : "", p.src === "off" ? "off" : "", p.src === "vac" ? "vac" : "", past ? "past" : "", +d === +today ? "today" : ""].join(" ");
      cells += `<button class="${cls}" data-k="${plKey(d)}" ${past ? "disabled" : ""}><b>${n}</b><span>${p.on ? `${p.time} · ${p.pct}%` : p.src === "off" ? "uit" : p.src === "vac" ? "vakantie" : ""}</span></button>`;
    }
    this.shadowRoot.innerHTML = `<style>${PLCSS}</style><ha-card style="--c:${c}">${this._part === "calendar" ? "" : `
      <section>
        <h4>Ritme · ${name} <button class="ib" data-tip="t1" aria-label="Uitleg" aria-expanded="false">i</button></h4>
        <div class="tip" id="t1" hidden>${infoHtml("Het vaste ritme van deze auto. Kies één standaard (klaar om, accu-%) en zet per weekdag aan of uit.\n\nTik op een dag om die dag aan of uit te zetten, of een eigen tijd of % te geven. Een dag met eigen waarden heeft vette tekst.")}</div>
        <div class="pair"><div><div class="lbl">standaard klaar om</div>${stp("std", s.std.time)}</div><div><div class="lbl">standaard accu</div>${sl("std", s.std.pct)}</div></div>
        <div class="days">${days}</div>${ed}
      </section>
      <section>
        <h4>Alleen deze keer <button class="ib" data-tip="t2" aria-label="Uitleg" aria-expanded="false">i</button></h4>
        <div class="tip" id="t2" hidden>${infoHtml("Een uitzondering voor de eerstvolgende keer. Daarna gaat HESC vanzelf terug naar het ritme. Laagste doel overal 15%: daaronder laadt de auto zijn 12V-accu niet meer bij.\n\n- **Overslaan:** de eerstvolgende lading vervalt.\n- **Andere tijd of %:** alleen voor de eerstvolgende keer.\n- **Nu laden tot:** laadt meteen, los van zon en prijs.\n\nVervangt in v3: plan voor één dag, één dag overslaan en nu laden tot.")}</div>
        <div class="next">Eerstvolgende: ${nxTxt}</div>
        ${o ? `<div class="exc"><span>${onceTxt}</span><span style="flex:1"></span><button class="btn" id="oclr">✕ terug naar ritme</button></div>` : ""}
        ${o && o.kind === "other" ? `<div class="ed"><div class="pair"><div><div class="lbl">klaar om</div>${stp("once", o.time)}</div><div><div class="lbl">accu</div>${sl("once", o.pct)}</div></div></div>` : ""}
        <div class="row"><button class="btn${o && o.kind === "skip" ? " act" : ""}" id="oskip">Overslaan</button><button class="btn${o && o.kind === "other" ? " act" : ""}" id="oother">Andere tijd of %</button>
          <span style="flex:1"></span><button class="btn${o && o.kind === "now" ? " act" : ""}" id="onow">Nu laden tot</button>${pstp("now", this._nowPct)}</div>
      </section>`}${this._part === "plan" ? "" : `
      <details ${this._open || this._part === "calendar" ? "open" : ""}${this._part === "calendar" ? ' class="fix"' : ""}><summary>${this._part === "calendar" ? `Kalender · ${name}` : "Geavanceerd: kalender"}<button class="ib" data-tip="t3" aria-label="Uitleg" aria-expanded="${!!this._t3}">i</button></summary>
        <div class="cal">
          <div class="tip" id="t3"${this._t3 ? "" : " hidden"}>${infoHtml("De maand met het ritme erin. Tik op een dag om hem **uit** te zetten (oranje streep), of een vrije dag **aan** met de standaardwaarden (gestreepte rand). Nog een keer tikken zet de dag terug naar het ritme.\n\nZo plan je ploegendienst of een dagje uit vooruit.\n\n**Vakantie:** tik op **+ Vakantie**, dan op de eerste en de laatste dag. Met de muis kun je ook van de eerste naar de laatste dag slepen. Al die dagen gaan uit; na de laatste dag gaat het ritme vanzelf verder. Tik in de vakantie of op ✕ om hem te stoppen.\n\n**Eén dag aanpassen:** tik twee keer snel op een dag. Dan kies je voor alleen die dag de tijd en de accu %.")}</div>
          <div class="mon"><button class="btn" id="mprev" aria-label="Vorige maand">‹</button><b>${PL_MON[m.getMonth()]} ${m.getFullYear()}</b><button class="btn" id="mnext" aria-label="Volgende maand">›</button></div>
          ${s.vac ? `<div class="vacl"><span>Vakantie <b>${plFmt(s.vac.from)} – ${plFmt(s.vac.to)}</b> · daarna weer het ritme</span><button class="btn" id="vstop">✕ vakantie stoppen</button></div>` : ""}
          <div class="vpick"><span>${this._vpick ? (this._vfrom ? "Tik nu de laatste dag van de vakantie" : "Tik de eerste dag van de vakantie") : ""}</span><button class="btn${this._vpick ? " act" : ""}" id="vpick">${this._vpick ? "✕ annuleren" : "+ Vakantie"}</button></div>
          <div class="grid7">${cells}</div>
          ${this._dayEd ? `<div class="dayed"><div class="dayh"><b>${plFmt(this._dayEd.k)}</b><span>alleen deze dag</span></div>
            <div class="pair"><div><div class="lbl">klaar om</div>${stp("dayed", this._dayEd.time)}</div><div><div class="lbl">accu</div>${sl("dayed", this._dayEd.pct)}</div></div>
            <div class="row"><button class="btn act" id="dok">Opslaan</button><button class="btn" id="doff">Deze dag uit</button><button class="btn" id="drhy">Terug naar ritme</button><span style="flex:1"></span><button class="btn" id="dcan">Annuleren</button></div></div>` : ""}
          <div class="leg"><span><i style="background:color-mix(in srgb,${c} 18%,transparent)"></i>ritme</span><span><i style="border:1.5px dashed ${c}"></i>extra dag</span><span><i style="border:1.5px dashed var(--dot)"></i>dag uit</span><span><i class="vacsw"></i>vakantie</span></div>
          ${window.matchMedia(HV4_PHONE).matches ? `<label class="land"><input type="checkbox" id="land"${hv4Land() === `cal:${this._config.ev || "ev1"}` ? " checked" : ""}>Op dit toestel HESC hier openen</label>` : ""}
        </div></details>`}
    </ha-card>`;
    this._wire();
  }

  _wire() {
    const r = this.shadowRoot, s = this._s, $ = (id) => r.getElementById(id);
    const re = () => { this._render(); plChanged(); };
    const sel = () => s.week[this._sel];
    r.querySelectorAll("[data-tip]").forEach((b) => b.addEventListener("click", (e) => {
      e.preventDefault(); // the calendar's (i) sits in the summary line: do not fold the calendar
      const t = r.getElementById(b.dataset.tip); t.hidden = !t.hidden; b.setAttribute("aria-expanded", String(!t.hidden));
      if (b.dataset.tip === "t3") this._t3 = !t.hidden; // decision 30-10 21:16: explanation behind (i), board shorter
    }));
    // time steppers
    r.querySelectorAll("[data-t]").forEach((box) => box.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      const dir = +b.dataset.dir, k = box.dataset.t;
      if (k === "std") s.std.time = plStep(s.std.time, dir);
      if (k === "day") { const w = sel(), t = plStep(w.time || s.std.time, dir); w.time = t === s.std.time ? undefined : t; }
      if (k === "once") s.once.time = plStep(s.once.time, dir);
      if (k === "dayed") { this._dayEd.time = plStep(this._dayEd.time, dir); this._render(); return; }
      re();
    })));
    // % sliders: live value while dragging, store on release
    r.querySelectorAll("[data-p]").forEach((inp) => {
      inp.addEventListener("input", () => { inp.style.setProperty("--v", `${(inp.value - 15) / 85 * 100}%`); inp.nextElementSibling.textContent = `${inp.value}%`; });
      inp.addEventListener("change", () => {
        const v = +inp.value, k = inp.dataset.p;
        if (k === "std") s.std.pct = v;
        if (k === "day") sel().pct = v === s.std.pct ? undefined : v;
        if (k === "once") s.once.pct = v;
        if (k === "dayed") { this._dayEd.pct = v; this._render(); return; }
        re();
      });
    });
    r.querySelectorAll("[data-pp]").forEach((box) => box.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      this._nowPct = Math.min(100, Math.max(15, this._nowPct + 5 * b.dataset.dir));
      if (s.once && s.once.kind === "now") s.once.pct = this._nowPct;
      re();
    })));
    r.querySelectorAll("[data-d]").forEach((b) => b.addEventListener("click", () => { const i = +b.dataset.d; this._sel = this._sel === i ? -1 : i; this._render(); }));
    if (this._sel >= 0) {
      $("eon").addEventListener("click", () => { sel().on = !sel().on; re(); });
      $("estd").addEventListener("click", () => { delete sel().time; delete sel().pct; re(); });
      $("eok").addEventListener("click", () => { this._sel = -1; this._render(); });
    }
    if (!$("oskip")) { this._wireCal(re); return; }
    $("oskip").addEventListener("click", () => { s.once = { kind: "skip" }; re(); });
    $("oother").addEventListener("click", () => { const n = plNext(s); s.once = { kind: "other", time: n ? n.time : s.std.time, pct: n ? n.pct : s.std.pct }; re(); });
    $("onow").addEventListener("click", () => { s.once = { kind: "now", pct: this._nowPct }; re(); });
    if ($("oclr")) $("oclr").addEventListener("click", () => { s.once = null; re(); });
    this._wireCal(re);
  }

  _wireCal(re) {
    const r = this.shadowRoot, s = this._s, $ = (id) => r.getElementById(id);
    if (!r.querySelector("details")) return;
    r.querySelector("details").addEventListener("toggle", (e) => { this._open = e.target.open; });
    $("mprev").addEventListener("click", () => { this._month = new Date(this._month.getFullYear(), this._month.getMonth() - 1, 1); this._render(); });
    $("mnext").addEventListener("click", () => { this._month = new Date(this._month.getFullYear(), this._month.getMonth() + 1, 1); this._render(); });
    // one tap = day off/on; with the mouse, press and drag over two or more days = a holiday period.
    // Decision 10-11-2026: a finger scrolls the page; a holiday is "+ Vakantie", then tap the first and the last day.
    const grid = r.querySelector(".grid7"), cellAt = (e) => { const el = r.elementFromPoint(e.clientX, e.clientY); return el && el.closest && el.closest("[data-k]:not([disabled])"); };
    const mark = () => { const [a, b] = [this._from, this._to].sort(); r.querySelectorAll("[data-k]").forEach((c) => c.classList.toggle("sel", !!this._from && c.dataset.k >= a && c.dataset.k <= b)); };
    const tap = (a) => {
      if (this._vpick) {
        if (!this._vfrom) { this._vfrom = a; this._render(); r.querySelectorAll(`[data-k="${a}"]`).forEach((c) => c.classList.add("sel")); return; }
        const [x, y] = [this._vfrom, a].sort(); this._vpick = false; this._vfrom = null; s.vac = { from: x, to: y }; re(); return;
      }
      // decision 10-11-2026: a double tap (double click) opens this one day: its own time and battery %
      const now = Date.now();
      if (this._tapK === a && now - this._tapT < 350) {
        clearTimeout(this._tapTimer); this._tapK = null;
        const p = plDay(s, new Date(a + "T12:00:00"));
        this._dayEd = { k: a, time: (p.on && p.time) || s.std.time, pct: (p.on && p.pct) || s.std.pct }; this._render(); return;
      }
      this._tapK = a; this._tapT = now; clearTimeout(this._tapTimer);
      this._tapTimer = setTimeout(() => { this._tapK = null; tap1(a); }, 350);
    };
    const tap1 = (a) => {
      const d = new Date(a + "T12:00:00");
      if (s.vac && a >= s.vac.from && a <= s.vac.to) { s.vac = null; re(); return; } // tap inside the holiday = stop it
      if (s.cal[a]) delete s.cal[a];                       // back to the rhythm
      else s.cal[a] = { on: !plDay(s, d).on };             // planned -> off, free -> on with the standard
      re();
    };
    grid.addEventListener("pointerdown", (e) => {
      const c = cellAt(e); if (!c) return;
      if (e.pointerType !== "mouse") { this._tk = c.dataset.k; return; } // finger: no drag, the page may scroll
      e.preventDefault(); this._from = this._to = c.dataset.k; mark();
    });
    grid.addEventListener("pointermove", (e) => { if (!this._from) return; const c = cellAt(e); if (c && c.dataset.k !== this._to) { this._to = c.dataset.k; mark(); } });
    grid.addEventListener("pointercancel", () => { this._tk = null; }); // the finger scrolled
    const up = (e) => {
      if (this._tk) { const c = e && cellAt(e), k = this._tk; this._tk = null; if (c && c.dataset.k === k) tap(k); return; }
      if (!this._from) return;
      const [a, b] = [this._from, this._to].sort(); this._from = this._to = null;
      if (a !== b && !this._vpick) { s.vac = { from: a, to: b }; re(); return; }
      tap(a);
    };
    grid.addEventListener("pointerup", up);
    grid.addEventListener("pointerleave", (e) => { if (this._from) up(e); });
    if ($("dok")) {
      const k = this._dayEd.k, done = () => { this._dayEd = null; re(); };
      $("dok").addEventListener("click", () => { s.cal[k] = { on: true, time: this._dayEd.time, pct: this._dayEd.pct }; done(); });
      $("doff").addEventListener("click", () => { s.cal[k] = { on: false }; done(); });
      $("drhy").addEventListener("click", () => { delete s.cal[k]; done(); });
      $("dcan").addEventListener("click", () => { this._dayEd = null; this._render(); });
    }
    $("vpick").addEventListener("click", () => { this._vpick = !this._vpick; this._vfrom = null; this._render(); });
    if ($("land")) $("land").addEventListener("change", (e) => hv4SetLand(e.target.checked ? `cal:${this._config.ev || "ev1"}` : ""));
    if ($("vstop")) $("vstop").addEventListener("click", () => { s.vac = null; re(); });
  }
}

/* ---------- real settings in the v4 input style: one card per group of HA entities ---------- */

const FLCSS = `
:host{--line:var(--divider-color,#30333c);--muted:var(--secondary-text-color,#9aa0aa);--card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));--dot:#ff9800}
ha-card{padding:14px 18px 6px;container-type:inline-size}
h4{margin:0 0 4px;font-size:15px;font-weight:500;display:flex;align-items:center;gap:8px}h4 .ib{margin-left:auto}
.f{display:grid;grid-template-columns:minmax(110px,1fr) minmax(0,auto);gap:6px 16px;align-items:center;padding:12px 0;border-top:1px solid var(--line)}
.rows>.f:first-child,.sec+.f{border-top:0}
.sec{font-size:15px;font-weight:500;margin:14px 0 2px;padding-top:12px;border-top:2px solid var(--line)}
.f>.nm{font-size:14px;line-height:1.3}.f>.nm small{display:block;color:var(--muted);font-size:12px}
.f.wide{grid-template-columns:minmax(0,1fr)}
.f.slr{grid-template-columns:minmax(80px,1fr) minmax(120px,1.25fr);gap:6px 10px}.f.slr .sl{gap:8px}.f.slr .sl output{min-width:0;font-size:14px}@container (max-width:240px){.f.slr{grid-template-columns:minmax(0,1fr)}}
.f.ro{padding:6px 0}.f.ro>.nm{font-size:13px;font-weight:400;color:var(--muted)}.f.ro .val{font-size:13px}
.f.attr{padding:8px 0}
.ed select{font:inherit;font-size:14px;flex:1;min-width:0;max-width:100%;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:7px 10px;color-scheme:dark}
.pwr{font:inherit;width:100%;border-radius:14px;padding:14px 16px;cursor:pointer;text-align:left;display:grid;gap:2px;color:#fff;border:0;background:#e57390}.pwr.on{background:#43a047}.pwr b{font-size:16px}.pwr span{font-size:12px;opacity:.85}.pwr.dim{opacity:.55}
.bpl{flex:1;min-width:0;max-height:170px;overflow:auto;border:1px solid var(--line);border-radius:10px;padding:4px 8px}.bpl label{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:center;padding:5px 0;font-size:13px;cursor:pointer}.bpl label span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bpl small{opacity:.7;white-space:nowrap}
.ib.ri{width:18px;height:18px;font-size:11px;margin-left:6px;vertical-align:1px}.rinfo[hidden]{display:none!important}.rinfo{display:block;margin:-2px 0 8px;padding:6px 8px;border-left:2px solid var(--primary-color);background:color-mix(in srgb,var(--primary-text-color) 5%,transparent);border-radius:4px;font-size:12px;line-height:1.45;color:var(--secondary-text-color);white-space:normal}.rinfo p{margin:0}
.f.na{opacity:.45}
.stp{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:var(--card2);height:36px}
.stp button{width:36px;height:36px;border:0;background:none;color:var(--primary-text-color);font-size:19px;cursor:pointer;border-radius:50%}
.stp button:hover{background:color-mix(in srgb,var(--c) 25%,transparent)}
.stp b{min-width:64px;text-align:center;font-size:15px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
.sl{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center}
.sl output{font-size:15px;font-weight:600;min-width:74px;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.sl input{-webkit-appearance:none;appearance:none;width:100%;height:10px;border-radius:999px;margin:0;cursor:pointer;
  background:linear-gradient(90deg,var(--c) 0 var(--v),var(--card2) var(--v) 100%);border:1px solid var(--line)}
.sl input::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:#fff;border:3px solid var(--c);box-shadow:0 1px 4px rgba(0,0,0,.4)}
.sl input::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#fff;border:3px solid var(--c)}
.tg{width:48px;height:28px;border-radius:999px;border:0;background:var(--card2);box-shadow:inset 0 0 0 1.5px var(--line);position:relative;cursor:pointer}
.tg::after{content:"";position:absolute;top:4px;left:4px;width:20px;height:20px;border-radius:50%;background:var(--muted);transition:left .15s,background .15s}
.tg.on{background:var(--on,var(--c));box-shadow:none}.tg.on::after{left:24px;background:#fff}
.tg.ro{display:inline-block;flex:none;cursor:default;opacity:.7}
.chips{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.chip{font:inherit;font-size:13px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:6px 12px;cursor:pointer}
.chip.on{border-color:var(--on,var(--c));background:color-mix(in srgb,var(--on,var(--c)) 25%,transparent);font-weight:600} /* chosen = green (decision 30-10 20:35) */
.chips.days{justify-content:space-between;flex-wrap:nowrap}.chips.days .chip{flex:1;min-width:0;padding:6px 0;text-align:center}
.chip[disabled]{opacity:.4;cursor:default}
.rep{display:block;width:100%;text-align:left;font:inherit;color:var(--primary-text-color);background:none;border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin-top:8px;cursor:pointer}.rep:hover{border-color:var(--c)}
.rep b{display:block;font-weight:600}.rep span{display:block;font-size:11.5px;color:var(--muted);margin-top:2px}.rtxt{font-size:12px;color:var(--muted);padding-top:4px}.bw{grid-column:1/-1;border:1px solid var(--primary-color);border-radius:12px;padding:12px 14px;margin:2px 0 8px;font-size:13px;line-height:1.45}.bw h5{margin:0 0 2px;font-size:14px}.bw .stp2{font-size:11.5px;color:var(--muted);margin-bottom:6px}.bw p{margin:4px 0 8px;color:var(--muted)}.bw label{display:flex;gap:8px;align-items:center;padding:5px 0;border-bottom:1px solid var(--divider-color)}.bw label span{flex:1}.bw label small{color:var(--muted)}.bw .nav{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}.bw .nav .sp{flex:1}.bw .big{font-size:20px;font-weight:600}.bw .warn{color:#ef6c00}.bwin{width:6.5em;padding:6px 8px;border-radius:10px;border:1px solid var(--primary-color);background:none;color:inherit;font:inherit;font-size:20px;font-weight:600;text-align:right}.bw .btn.act{background:var(--primary-color);color:var(--text-primary-color,#fff);border-color:var(--primary-color);font-weight:600}.bw .btn[disabled]{opacity:.4;cursor:default}.bw .btn.act::before{content:"✓ "}.bw [data-bw=next].act::before,.bw [data-bw=save].act::before{content:""}.bwb{grid-column:1/-1;width:100%;padding:12px;border-radius:12px;border:1px dashed var(--primary-color);background:none;color:var(--primary-color);font:inherit;font-weight:600;cursor:pointer;margin-bottom:6px}.ph{grid-column:1/-1;border-top:1px solid var(--divider-color);padding-top:10px;margin-top:4px;font-size:12.5px;line-height:1.45}.ph h5{margin:0 0 4px;font-size:13px}.ph .st{color:var(--muted)}.ph .bar{display:grid;grid-template-columns:52px 1fr 40px;gap:8px;align-items:center;margin:4px 0}.ph .bar i{display:block;height:10px;border-radius:5px;background:color-mix(in srgb,#ffb300 70%,transparent)}.ph .bar.w i{background:#ef6c00}.ph .bar b{font-weight:600;text-align:right}.ph .trk{background:var(--divider-color);border-radius:5px}.rtxt.sm{font-size:11px;line-height:1.35;margin-top:8px}
.btn{font:inherit;font-size:13px;border-radius:999px;border:1.5px solid var(--c);background:none;color:var(--primary-text-color);padding:7px 16px;cursor:pointer}
.btn:hover{background:color-mix(in srgb,var(--c) 22%,transparent)}
.btn.danger{border-color:#ef5350}.btn.danger:hover{background:color-mix(in srgb,#ef5350 18%,transparent)}.btn.dim{opacity:.45} /* warning red, house style v2.3 */
.ask{border:1.5px solid #ef5350;border-radius:12px;background:color-mix(in srgb,#ef5350 14%,transparent);padding:14px 16px;margin:4px 0 10px;display:grid;gap:10px;font-size:14px}.ask p{margin:0}.ask .f{border-top:0;padding:0}
.askbtns{display:flex;gap:10px;justify-content:flex-end}.btn.yes{background:#ef5350;border-color:#ef5350;color:#fff;font-weight:600}.btn.yes[disabled]{opacity:.45;cursor:default}
.val{font-size:14px;font-weight:600;text-align:right}
.ok{color:var(--muted);font-size:12px}
.tag{margin-left:auto;font-size:11px;font-weight:500;border:1px solid var(--line);border-radius:999px;padding:2px 9px;color:var(--muted);white-space:nowrap}
.tag.car{border-color:var(--c);color:var(--c)}button.tag{font-family:inherit;cursor:pointer;background:none}button.tag.off{border-color:#e57390;color:#e57390;text-decoration:line-through}button.tag[disabled]{cursor:default;opacity:.6}.tag+.ib{margin-left:8px}
.val{min-width:0;overflow-wrap:anywhere}.val small{display:block;color:var(--muted);font-weight:400;font-size:12px}
@container (max-width:460px){.f.attr,.f.tx{grid-template-columns:minmax(0,1fr)}.f.attr .val{text-align:left}}
.txt{font:inherit;font-size:14px;font-weight:600;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:7px 12px;cursor:pointer;text-align:left;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.txt.empty{color:var(--muted);font-weight:400;font-style:italic}
.ed{display:flex;gap:8px;align-items:center}
.ed input{font:inherit;font-size:14px;flex:1;min-width:0;border-radius:10px;border:1.5px solid var(--c);background:var(--card2);color:var(--primary-text-color);padding:7px 12px;outline:none}
.date{font:inherit;font-size:14px;font-weight:600;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:6px 10px;color-scheme:dark}
.f.wide .txt,.f.wide .ed{width:100%}
${INFO_CSS}`;

/* Opmaakronde (besluit 30-10 nr 38): v3's select options are English; show them in Dutch (display only, the value stays). */
const OPT_NL = {
  "Today": "Vandaag", "Tomorrow": "Morgen", "Mon": "ma", "Tue": "di", "Wed": "wo", "Thu": "do", "Fri": "vr", "Sat": "za", "Sun": "zo",
  "Price list in sensor": "Prijslijst in een sensor", "Nord Pool (official)": "Nord Pool (officieel)", "Automatic": "Automatisch",
  "Per quarter": "Per kwartier", "Per hour": "Per uur", "Days": "Dagen", "Weeks": "Weken", "Months": "Maanden", "Quarters": "Kwartalen",
  "Year": "Jaar", "Choose a phone": "Kies een telefoon", "Not chosen": "Niet gekozen", "evcc (any charger)": "evcc (elke laadpaal)",
  "Other (manual)": "Anders (zelf invullen)", "Off": "Uit",
};
Object.assign(OPT_NL, HV4_CNL, { "own": "Eigen sensor met prijslijst", "hacs": "Nord Pool (HACS)" }); // 11-11: countries, price sources
const optNl = (o) => OPT_NL[o] || o;

class HescV4Fields extends HTMLElement {
  setConfig(config) {
    this._config = config || {}; this._busy = null; this._sig = "";
    // demo_only cards (two-car settings) disappear with the real car alone; redraw when the switch changes
    if (!this._onMode) {
      this._onMode = () => { if (this._hass) this._render(); };
      window.addEventListener("hesc-v4-mode", this._onMode); window.addEventListener("hesc-v4-demo", this._onMode);
    }
  }
  set hass(hass) {
    this._hass = hass;
    // redraw only when one of our entities changed, and never while a slider is being dragged
    const sig = (this._config.rows || []).map((r) => {
      if (r.type === "days") return (r.entities || []).map((id) => (hass.states[id] || {}).state).join(",");
      const s = r.entity && hass.states[r.entity];
      if (!s) return "-";
      if (r.type === "attribute") { const t = s.attributes[r.attribute], x = t && hass.states[t]; return String(t) + (x ? x.state : ""); }
      if (r.type === "phases") return s.state + JSON.stringify(s.attributes);
      return s.state + JSON.stringify(s.attributes.options || "") + (r.show_if ? (hass.states[r.show_if.entity] || {}).state : "") + (s.attributes.waiting ? "w" : "") + (r.type === "attribute" ? String(s.attributes[r.attribute]) : "");
    }).join("|") + (this._config.tag_power ? "|" + ((hass.states[this._config.tag_power] || {}).state) : "") + (this._config.if_entity ? "|" + !!hass.states[this._config.if_entity] : "");
    if (sig === this._sig || this._busy || this._edit !== undefined || this._ask !== undefined) return;
    this._sig = sig;
    this._render();
  }
  getCardSize() { return 1 + (this._config.rows || []).length; }

  _name(r, s) {
    if (r.name) return r.name;
    const f = (s && s.attributes.friendly_name) || r.entity;
    return f.replace(/^HESC v[34]\s*/i, "").replace(/^(EV|Charger)\d+\s+/i, "");
  }
  _num(v, step) { const d = String(step).includes(".") ? String(step).split(".")[1].length : 0; return Number(v).toLocaleString(hv4Loc(), { minimumFractionDigits: d, maximumFractionDigits: d }); }

  /* Example settings for two cars (besluit 4-7, 30-33): kept in memory only, nothing is written to HA. */
  _demoRow(r, i) {
    const D = (window.__hv4Demo = window.__hv4Demo || {}), v = r.key in D ? D[r.key] : r.value;
    const sub = r.hint ? `<small>${r.hint}</small>` : "";
    if (r.kind === "switch") return `<div class="f"><div class="nm">${r.name}${sub}</div><button class="tg${v ? " on" : ""}" role="switch" aria-checked="${!!v}" data-dm="${i}"></button></div>`;
    if (r.kind === "time") return `<div class="f"><div class="nm">${r.name}${sub}</div><div class="stp"><button data-dm="${i}" data-dir="-1">−</button><b>${v}</b><button data-dm="${i}" data-dir="1">+</button></div></div>`;
    if (r.kind === "number") return `<div class="f"><div class="nm">${r.name}${sub}</div><div class="stp"><button data-dm="${i}" data-dir="-1">−</button><b>${v ? `${this._num(v, r.step || 1)} ${r.unit || ""}` : "leeg"}</b><button data-dm="${i}" data-dir="1">+</button></div></div>`;
    if (r.kind === "chips") {
      const blocked = (o) => r.need && r.need.option === o && !(r.need.key in D ? D[r.need.key] : r.need.value);
      return `<div class="f${r.options.join("").length > 30 ? " wide" : ""}"><div class="nm">${r.name}${sub}${r.need && blocked(r.need.option) ? `<small>${r.need.why}</small>` : ""}</div><div class="chips">${r.options.map((o) => `<button class="chip${o === v ? " on" : ""}" data-dm="${i}" data-o="${o}"${blocked(o) ? " disabled" : ""}>${o}</button>`).join("")}</div></div>`;
    }
    return "";
  }

  _askBox(r) {
    const warn = r.warn || "Weet je het zeker? Dit kan niet ongedaan worden gemaakt.";
    const bk = r.backup ? `<p>${this._bk ? "✓ Back-up gemaakt." : "Je hebt in dit venster nog geen back-up gemaakt."}</p><div><button class="btn" data-bk="1">Back-up maken</button></div>` : "";
    return `<div class="ask"><b>${warn}</b>${r.note ? `<p>${r.note}</p>` : ""}${bk}
      <div class="f"><div class="nm">${r.sure || "Ik weet het zeker"}</div><button class="tg${this._sure ? " on" : ""}" role="switch" aria-checked="${!!this._sure}" data-sure="1" style="--on:#ef5350"></button></div>
      <div class="askbtns"><button class="btn" data-ask="no">Annuleren</button><button class="btn yes" data-ask="yes"${this._sure ? "" : " disabled"}>${r.yes || "Ja, uitvoeren"}</button></div></div>`;
  }

  _row(r, i) {
    const sub = (r.hint ? `<small>${r.hint}</small>` : "") + (r.info ? ` <button class="ib ri" data-ri="${i}" aria-label="Uitleg" aria-expanded="${!!(this._ri || {})[i]}">i</button>` : "");
    if (r.type === "section") return `<div class="sec">${r.name}</div>`;
    if (r.type === "power") { const ps = this._hass.states[r.entity], on = (ps || {}).state === "on", who = r.who || "HESC";
      if (!ps) return `<div class="f wide"><button class="pwr" disabled style="opacity:.5;background:var(--divider-color)"><b>${r.onText || who + " staat aan"}</b><span>nog niet beschikbaar: de rekenchat bouwt dit nog</span></button></div>`;
      return `<div class="f wide"><button class="pwr${on ? " on" : ""}${this._ask === i ? " dim" : ""}" data-pw="${i}" aria-pressed="${on}"><b>${on ? (r.onText || who + " staat aan") : (r.offText || who + " staat uit")}</b><span>${on ? "tik om uit te zetten" : "tik om aan te zetten"}</span></button></div>`; }
    if (r.type === "report") { // as in Marstek Capacity Monitor: the whole tile is the button; the report itself comes from the v4 integration
      const rr = this._repRes && this._repRes.i === i ? this._repRes : null;
      const res = !rr ? "" : rr.busy ? `<div class="rtxt sm">bezig…</div>` : rr.err ? `<div class="rtxt sm" style="color:#ef5350">${rr.err}</div>`
        : `<div class="rtxt sm">✓ Klaar${rr.url ? ` · <a href="${rr.url}" target="_blank" rel="noopener">openen</a>` : rr.file ? ` · bewaard in HESC (${rr.file})` : ""}${rr.text ? `<textarea readonly style="width:100%;height:110px;margin-top:6px;font:12px monospace">${rr.text.replace(/</g, "&lt;")}</textarea>` : ""}</div>`;
      return `<button class="rep" data-rep="${i}"${rr && rr.busy ? " disabled" : ""}><b>${r.name}</b><span>${r.hint || ""}</span></button>${res}`;
    }
    if (r.type === "text") return `<div class="rtxt${r.small ? " sm" : ""}">${r.small && this._rep !== undefined ? "<b>Komt in v4: het rapport maakt de v4-integratie.</b> · " : ""}${r.name}</div>`;
    if (r.type === "demo") return this._demoRow(r, i);
    if (r.type === "phases") return r.detail ? hv4PhasesDetail(this._hass, r.entity) : hv4PhShow() ? hv4Phases(this._hass, r.entity, sub) : "";
    if (r.type === "batwiz") return hv4BatWiz(this);
    if (r.type === "wiz") return hv4Wiz(this, r.wiz);
    if (r.type === "redo") return hv4RedoBtn(this._hass);
    if (r.type === "days") { // decision 30-10 20:53: weekdays as chips (green = on), one tap toggles that day's switch
      return `<div class="f wide"><div class="nm">${r.name || ""}</div><div class="chips days">${(r.entities || []).map((id, j) => {
        const st = this._hass.states[id], on = st && st.state === "on";
        return `<button class="chip${on ? " on" : ""}" data-day="${id}">${(r.labels || [])[j] || j + 1}</button>`; }).join("")}</div></div>`;
    }
    if (r.type === "download") { // rekenchat 89e1de6: GET /api/hesc_v4/costs/{car}/{days|months}.csv, only when logged in
      const cars = ["ev1", ...(this._hass.states["sensor.hesc_v4_ev2_setup"] || this._hass.states["select.hesc_v4_ev2_charge_now_to"] ? ["ev2"] : [])];
      const nm = (c) => { const t = this._hass.states[`text.hesc_v4_${c}_car_name`]; return t && !["unknown", "unavailable", ""].includes(t.state) ? t.state : (c === "ev1" ? "auto 1" : "auto 2"); };
      return `<div class="f wide"><div class="nm">${r.name || ""}${sub}</div><div class="chips">${cars.flatMap((c) => ["days", "months"].map((w) => `<button class="chip" data-dl="${c}/${w}">${cars.length > 1 ? nm(c) + " · " : ""}${w === "days" ? "per dag" : "per maand"}</button>`)).join("")}</div></div>`;
    }
    if (r.type === "button") return `<div class="f"><div class="nm">${r.name || ""}</div><button class="btn" data-nav="${i}">${r.action_name || "Openen"}</button></div>`;
    if (r.type === "attribute") { // a setup choice: show which sensor is chosen, with its live value
      const st = this._hass.states[r.entity], v = st ? st.attributes[r.attribute] : undefined;
      const t = v === undefined || v === null || v === "" ? "" : String(v), tgt = /^[a-z_]+\.[a-z0-9_]+$/.test(t) && this._hass.states[t];
      const shown = !t ? `<span class="ok">niet gekozen</span>` : tgt ? `<span title="${t}">${(tgt.attributes.friendly_name || t)}</span><small>${hv4Num(tgt.state, tgt.attributes.unit_of_measurement)}${tgt.attributes.unit_of_measurement ? " " + tgt.attributes.unit_of_measurement : ""}</small>` : t === "on" ? "aan" : t === "off" ? "uit" : t;
      // decision 30-10 20:34: an on/off choice looks like the house-style switch (read-only here: it is changed in the setup screen)
      if (t === "on" || t === "off") return `<div class="f attr"><div class="nm">${r.name || r.attribute}${sub}</div><span class="tg ro${t === "on" ? " on" : ""}" role="switch" aria-checked="${t === "on"}" aria-disabled="true" title="wijzigen via Instelscherm"></span></div>`;
      if (r.attribute === "hesc_charger_eco_value" || r.attribute === "hesc_ev_disconnected_values") { // decision 08-11-2026: tick instead of type (rekenchat 1867036)
        const su = (st && st.attributes) || {}, eco = r.attribute === "hesc_charger_eco_value", cur = t.split(",").map((x) => x.trim()).filter(Boolean);
        let opts = [];
        if (eco) { const ms = this._hass.states[su.hesc_charger_mode_entity]; opts = (ms && ms.attributes.options) || []; }
        else { const cs = su.hesc_ev_connected_sensor, seen = (this._seen || {})[cs]; if (cs && seen === undefined && this._hass.callWS) { this._seen = { ...(this._seen || {}), [cs]: null };
            this._hass.callWS({ type: "hesc_v4/setup/values_seen", entity_id: cs, days: 30 }).then((x) => { this._seen[cs] = [...(x.seen || []), ...(x.options || [])]; this._sig = ""; this._render(); }).catch(() => { this._seen[cs] = []; }); }
          opts = seen || []; }
        const all = [...new Set([...cur, ...opts.filter((o) => !["unknown", "unavailable", ""].includes(o))])];
        if (all.length) return `<div class="f wide"><div class="nm">${r.name || r.attribute}${sub}<small>${eco ? "tik de standen aan die laden op zon betekenen" : "tik de standen aan die betekenen: geen auto"}</small></div><div class="chips">${all.map((o) => `<button class="chip${cur.includes(o) ? " on" : ""}" data-vk="${i}" data-o="${o.replace(/"/g, "&quot;")}">${cur.includes(o) ? "✓ " : ""}${o}</button>`).join("")}</div></div>`;
      }
      if (this._edit === i && this._srcList) {
        const key = r.attribute.replace(/^hesc_/, ""), src = (this._srcList[key] || this._srcList[r.attribute] || {}).candidates || [];
        if (!src.length) return `<div class="f wide"><div class="nm">${r.name || r.attribute}${sub}</div><div class="hint">Geen geschikte sensoren gevonden. <button class="btn" data-setup="1">Instelscherm</button></div></div>`;
        return `<div class="f wide"><div class="nm">${r.name || r.attribute}${sub}</div><div class="ed" style="align-items:flex-start"><input type="hidden" data-sv="${i}" value="${t || ""}"><div class="bpl">${[...src.filter((c) => c.entity_id === t), ...(t && !src.some((c) => c.entity_id === t) && this._hass.states[t] ? [{ entity_id: t, name: this._hass.states[t].attributes.friendly_name, state: this._hass.states[t].state, unit: this._hass.states[t].attributes.unit_of_measurement }] : []), ...src.filter((c) => c.entity_id !== t && !["unavailable", "unknown"].includes(String(c.state)))].map((c) => `<label><input type="radio" name="sv${i}" data-svr="${c.entity_id}"${c.entity_id === t ? " checked" : ""}><span title="${c.name || c.entity_id}">${c.entity_id === t ? '<b style="color:var(--primary-color)">nu gekozen · </b>' : ""}${c.suggested ? '<b style="color:#66bb6a">voorstel · </b>' : ""}${c.name || c.entity_id}</span><small>${hv4Num(c.state, c.unit)} ${c.unit || ""}</small></label>`).join("")}<label><input type="radio" name="sv${i}" data-svr=""${t ? "" : " checked"}><span>— geen —</span><small></small></label></div><button class="btn" data-sok="${i}">OK</button></div></div>`; // decision 08-11-2026 09:23: the same short list with a suggestion as for the home batteries
      }
      { const pd = (this._pendSrc || {})[i], loading = st && st.state !== "ok";
        if (pd && (t === pd.v || Date.now() - pd.at > 120000)) delete this._pendSrc[i];
        else if (pd) { const ps = this._hass.states[pd.v]; return `<div class="f attr"><div class="nm">${r.name || r.attribute}${sub}</div><span class="val">${pd.v ? (ps ? ps.attributes.friendly_name || pd.v : pd.v) : "geen"}<small style="color:#ffb74d">wordt opgeslagen</small></span></div>`; }
        else if (loading) return `<div class="f attr"><div class="nm">${r.name || r.attribute}${sub}</div><span class="val"><small>HESC laadt opnieuw…</small></span></div>`; }
      return `<div class="f attr" data-src="${i}" style="cursor:pointer" title="Tik om te wijzigen"><div class="nm">${r.name || r.attribute}${sub}</div><span class="val">${/<small>/.test(shown) ? shown.replace("</span><small>", " ›</span><small>") : shown + " ›"}</span></div>`;
    }
    if (r.show_if && ((this._hass.states[r.show_if.entity] || {}).state !== r.show_if.state)) return ""; // only when it matters
    if (!r.entity) return "";
    const s = this._hass.states[r.entity], dom = r.entity.split(".")[0], name = this._name(r, s);
    if (!s) return `<div class="f na"><div class="nm">${name}<small>niet gevonden: ${r.entity}</small></div><span></span></div>`;
    const a = s.attributes, unit = a.unit_of_measurement ? ` ${a.unit_of_measurement}` : "";
    if (dom === "number" || dom === "input_number") {
      const min = +a.min, max = +a.max, step = +a.step || 1, v = +s.state, n = Math.round((max - min) / step);
      if (n <= 400 && r.kind !== "stepper") {
        const pc = (v - min) / (max - min) * 100;
        return `<div class="f slr"><div class="nm"${r.full && s.attributes.friendly_name ? ` title="${s.attributes.friendly_name.replace(/^HESC v[34]\s*/i, "")}"` : ""}>${name}${sub}</div><div class="sl"><input type="range" min="${min}" max="${max}" step="${step}" value="${v}" data-i="${i}" style="--v:${pc}%" aria-label="${name}"><output>${this._num(v, step)}${unit}</output></div></div>`;
      }
      if (this._edit === i) return `<div class="f"><div class="nm">${name}${sub}<small>typ de waarde, bijv. 0,1116</small></div><div class="ed"><input type="text" inputmode="decimal" data-nv="${i}" value="${String(v).replace(".", ",")}" aria-label="${name}"><button class="btn" data-nok="${i}">OK</button></div></div>`;
      return `<div class="f"><div class="nm">${name}${sub}</div><div class="stp" data-i="${i}"><button data-dir="-1" aria-label="minder">−</button><b data-ne="${i}" title="Tik om te typen" style="cursor:text;text-decoration:underline dotted">${this._num(v, step)}${unit}</b><button data-dir="1" aria-label="meer">+</button></div></div>`;
    }
    if (dom === "switch" || dom === "input_boolean") {
      const on = s.state === "on";
      return `<div class="f"><div class="nm">${name}${sub}</div><button class="tg${on ? " on" : ""}" role="switch" aria-checked="${on}" aria-label="${name}" data-i="${i}"></button></div>`;
    }
    if (dom === "select" || dom === "input_select") {
      if (/_price_source$/.test(r.entity)) return hv4PriceSrc(this._hass, s, i, name, sub);
      if (/_price_country$/.test(r.entity)) return `<div class="f"><div class="nm">${name}${sub}</div><div class="ed"><select data-pcountry="${i}" aria-label="${name}">${(a.options || []).map((o) => `<option value="${o}"${o === s.state ? " selected" : ""}>${o === "Automatic" ? `${optNl("Automatic")} (${optNl(hv4CountryName(hv4Country(this._hass, "Automatic")))})` : optNl(o)}</option>`).join("")}</select></div></div>`;
      const opts = a.options || [];
      if (opts.length <= 6) return `<div class="f${opts.join("").length > 40 ? " wide" : ""}"><div class="nm">${name}${sub}</div><div class="chips">${opts.map((o) => `<button class="chip${o === s.state || String(o).startsWith("✓") ? " on" : ""}" data-i="${i}" data-o="${o}">${optNl(o)}</button>`).join("")}</div></div>`;
      if (/_charge_now_to$/.test(r.entity)) { const o = (a.options || []).filter((x) => x !== "Off"), on = !!s.state && !["Off", "unknown", "unavailable"].includes(s.state); this._pend = this._pend || {};
        const pv = this._pend[i] || (o.includes("80%") ? "80%" : o[0] || ""), wt = s.attributes.waiting ? " · wacht op de auto" : "";
        if (on) return `<div class="f"><div class="nm">${name}${sub}<small style="color:#ffb74d">laadt nu van het net tot ${s.state}${wt}</small></div><button class="btn" data-nowstop="${i}">Stoppen</button></div>`;
        return `<div class="f"><div class="nm">${name}${sub}<small>kies het doel, dan Start</small></div><div style="display:flex;gap:8px;align-items:center;justify-content:flex-end"><div class="stp" data-nowp="${i}"><button data-dir="-1" aria-label="lager">‹</button><b>${pv}</b><button data-dir="1" aria-label="hoger">›</button></div><button class="btn" data-nowgo="${i}">Start</button></div></div>`; }
      return `<div class="f"><div class="nm">${name}${sub}${s.attributes.waiting ? `<small style="color:#ffb74d">wacht op de auto</small>` : ""}</div><div class="stp" data-i="${i}" data-sel="1"><button data-dir="-1" aria-label="vorige">‹</button><b>${optNl(s.state)}</b><button data-dir="1" aria-label="volgende">›</button></div></div>`;
    }
    if (dom === "text" || dom === "input_text") {
      if (this._edit === i && r.pick === "price") { // decision 06-11: choose the price sensor from a list instead of typing its name
        const cand = Object.keys(this._hass.states).filter((id) => id.startsWith("sensor.") && !id.startsWith("sensor.hesc_")
          && (/nordpool|energyzero|easyenergy|tibber|entsoe|epex|day_ahead|dagprij|price|prijs/i.test(id) || /\/kwh/i.test(this._hass.states[id].attributes.unit_of_measurement || "")));
        // a price LIST is needed: sensors that carry today's prices as a list come first; the rest only if none does
        const isList = (id) => Object.values(this._hass.states[id].attributes).some((v) => Array.isArray(v) && v.length >= 24);
        const lists = cand.filter(isList); if (lists.length) cand.splice(0, cand.length, ...lists);
        const cur = String(s.state === "unknown" ? "" : s.state);
        return `<div class="f wide"><div class="nm">${name}${sub}</div><div class="ed"><select data-ti="${i}" aria-label="${name}"><option value="">— kies een sensor —</option>${cand.map((id) => `<option value="${id}"${id === cur ? " selected" : ""}>${this._hass.states[id].attributes.friendly_name || id} · ${id}</option>`).join("")}</select><button class="btn" data-tok="${i}">OK</button></div></div>`;
      }
      if (this._edit === i && (r.pick === "soc" || r.pick === "power")) { // decision 06-11 13:28: suggestions for the home battery sensors (more than one allowed)
        const st = this._hass.states, unitOf = (id) => String(st[id].attributes.unit_of_measurement || "");
        const cand = Object.keys(st).filter((id) => id.startsWith("sensor.") && !id.startsWith("sensor.hesc") && (r.pick === "soc"
          ? unitOf(id) === "%" && (st[id].attributes.device_class === "battery" || /soc|batter|accu|marstek|venus|state_of_charge/i.test(id))
          : /^k?W$/.test(unitOf(id)) && /batter|accu|marstek|venus/i.test(id)));
        const rank = (id) => (/marstek|venus|home_batt|thuis|huisaccu/i.test(id) ? 0 : /iphone|pixel|phone|watch|airco|sensor_batter|_batterij$/i.test(id) ? 2 : 1);
        cand.sort((x, y) => rank(x) - rank(y));
        { // decision 08-11-2026 09:19: leave out what is clearly not a home battery (house use, the cars, demo sensors) and suggest a choice
          const carNames = ["ev1", "ev2"].map((k) => (st[`text.hesc_v4_${k}_car_name`] || {}).state).filter(Boolean).map((n) => n.toLowerCase());
          const fn = (id) => String(st[id].attributes.friendly_name || id).toLowerCase();
          for (let j = cand.length - 1; j >= 0; j--) { const f = fn(cand[j]) + " " + cand[j]; if (/verbruik|consumption|demo/.test(f) || carNames.some((n) => f.includes(n))) cand.splice(j, 1); }
        }
        const sugg = (() => { // one total sensor if there is one, else one "battery" (DC) sensor per battery
          const st0 = this._hass.states, fn = (id) => String(st0[id].attributes.friendly_name || id).toLowerCase() + " " + id;
          if (r.pick === "soc") return cand.filter((id) => !/total|totaal|alle/.test(fn(id)));
          const tot = cand.filter((id) => /total|totaal/.test(fn(id)));
          if (tot.length) return [tot[0]];
          const dc = cand.filter((id) => /battery.?power/.test(fn(id)) && !/ac|_ac_/.test(fn(id))), seen = new Set();
          return dc.filter((id) => { const k = Math.round(+st0[id].state || 0); if (seen.has(k)) return false; seen.add(k); return true; });
        })();
        if (!this._srcList && !this._hbLoad) { this._hbLoad = true; this._hass.callWS({ type: "hesc_v4/setup/find" }).then((f) => { this._srcList = f.sources || {}; this._hbLoad = false; this._render(); }).catch(() => { this._srcList = {}; }); }
        const hb = this._srcList && this._srcList[r.pick === "soc" ? "home_battery_soc_sensors" : "home_battery_power_sensors"];
        if (hb && (hb.candidates || []).length) { cand.length = 0; hb.candidates.forEach((c) => { if (st[c.entity_id]) cand.push(c.entity_id); }); sugg.length = 0; hb.candidates.filter((c) => c.suggested).forEach((c) => sugg.push(c.entity_id)); }
        const signNote = hb && hb.sign_note ? `<small style="color:#ffb74d;display:block">Let op: de totaal-sensor telt andersom dan de losse accu's. HESC rekent met + = laden; kijk welke klopt.</small>` : "";
        cand.sort((x, y) => (sugg.includes(y) ? 1 : 0) - (sugg.includes(x) ? 1 : 0));
        const cur = String(s.state === "unknown" ? "" : s.state).split(",").map((x) => x.trim()).filter(Boolean);
        // decision 08-11-2026 09:17: tick boxes in a short list instead of a Ctrl-select, and every chosen sensor stays visible
        return `<div class="f wide"><div class="nm">${name}${sub}<small>Vink per thuisbatterij één sensor aan · <b>voorstel</b> = wat HESC zou kiezen</small>${signNote}${sugg.length ? `<button class="btn" data-bps="${sugg.join(",")}" style="margin-top:6px">Voorstel overnemen</button>` : ""}</div><div class="ed" style="align-items:flex-start"><input type="hidden" data-ti="${i}" value="${cur.join(", ")}"><div class="bpl">${cand.map((id) => `<label><input type="checkbox" data-bp="${id}"${cur.includes(id) ? " checked" : ""}><span title="${st[id].attributes.friendly_name || id}">${sugg.includes(id) ? '<b style="color:var(--primary-color)">voorstel · </b>' : ""}${st[id].attributes.friendly_name || id}</span><small>${hv4Num(st[id].state, unitOf(id))} ${unitOf(id)}</small></label>`).join("")}</div><button class="btn" data-tok="${i}">OK</button></div></div>`;
      }
      if (/_charge_now_mode_value$/.test(r.entity)) { // decision 08-11-2026 10:36: choose from the charger's own modes instead of typing
        const me = ((this._hass.states[/charger2/.test(r.entity) ? "sensor.hesc_v4_ev2_setup" : "sensor.hesc_v4_setup"] || {}).attributes || {}).hesc_charger_mode_entity, ms = me && this._hass.states[me], opts = (ms && ms.attributes.options) || [];
        if (opts.length) { const cur = ["unknown", "unavailable"].includes(s.state) ? "" : s.state;
          return `<div class="f wide"><div class="nm">${name}${sub}<small>een stand van ${(ms.attributes.friendly_name || me)}</small></div><div class="chips">${["", ...opts].map((o) => `<button class="chip${o === cur ? " on" : ""}" data-mv="${i}" data-o="${o}">${o || "geen"}</button>`).join("")}</div></div>`; }
      }
      if (this._edit === i) return `<div class="f wide"><div class="nm">${name}${sub}</div><div class="ed"><input data-ti="${i}" value="${String(s.state === "unknown" ? "" : s.state).replace(/"/g, "&quot;")}" aria-label="${name}"><button class="btn" data-tok="${i}">OK</button></div></div>`;
      const v = ["unknown", "unavailable", ""].includes(s.state) ? "" : s.state;
      if (r.pick === "soc" || r.pick === "power") { const ids = v.split(",").map((x) => x.trim()).filter(Boolean); return `<div class="f tx wide"><div class="nm">${name}${sub}</div><button class="txt${ids.length ? "" : " empty"}" data-te="${i}" style="text-align:left">${ids.length ? ids.map((id) => `${(this._hass.states[id] || { attributes: {} }).attributes.friendly_name || id}${this._hass.states[id] ? ` <small style="opacity:.7">· ${this._hass.states[id].state} ${this._hass.states[id].attributes.unit_of_measurement || ""}</small>` : ""}`).join("<br>") : "leeg · tik om in te vullen"}</button></div>`; }
      return `<div class="f tx${v.length > 24 ? " wide" : ""}"><div class="nm">${name}${sub}</div><button class="txt${v ? "" : " empty"}" data-te="${i}">${v || "leeg · tik om in te vullen"}</button></div>`;
    }
    if (dom === "date" || dom === "input_datetime") return `<div class="f"><div class="nm">${name}${sub}</div><input type="date" class="date" data-di="${i}" value="${/^\d{4}-\d{2}-\d{2}$/.test(s.state) ? s.state : ""}" aria-label="${name}"></div>`;
    if (dom === "binary_sensor") return `<div class="f ro"><div class="nm">${name}${sub}</div><span class="val">${s.state === "on" ? "ja" : s.state === "off" ? "nee" : s.state}</span></div>`;
    if (dom === "button" || dom === "input_button") {
      const danger = r.danger || /to_standard|standard_values/.test(r.entity);
      return `<div class="f"><div class="nm">${name}${sub}</div><button class="btn${danger ? " danger" : ""}${this._ask === i ? " dim" : ""}" data-i="${i}">${r.label || "Uitvoeren"}</button></div>`;
    }
    return `<div class="f ro"><div class="nm">${name}${sub}</div><span class="val">${s.state}${unit}</span></div>`;
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const c = this._config, rows = c.rows || [];
    if (c.if_entity && this._hass && !this._hass.states[c.if_entity]) { this.shadowRoot.innerHTML = ""; this.style.display = "none"; return; }
    if (c.demo_only && hv4Cur() === "real") { this.shadowRoot.innerHTML = ""; this.style.display = "none"; return; }
    this.style.display = "";
    this.shadowRoot.innerHTML = `<style>${FLCSS}</style><ha-card style="--c:${c.color || "var(--primary-color)"};--on:${c.color || "#66bb6a"}">
      ${c.title || c.tag ? `<h4>${c.title || ""}${c.tag && !(/beide auto/.test(c.tag) && this._hass && !this._hass.states["text.hesc_v4_ev2_car_name"]) ? (c.tag_power ? (() => { const ps = this._hass && this._hass.states[c.tag_power], off = ps && ps.state === "off"; return `<button class="tag car tp${off ? " off" : ""}" data-tp="1" ${ps ? "" : "disabled"} title="${ps ? (off ? "HESC stuurt deze auto niet · tik om aan te zetten" : "HESC stuurt deze auto · tik om uit te zetten") : "nog niet beschikbaar: de rekenchat bouwt dit nog"}">${off ? "⏻ uit · " : "⏻ "}${c.tag}</button>`; })() : `<span class="tag${c.color ? " car" : ""}">${c.tag}</span>`) : ""}${c.info ? ` <button class="ib" data-tip="1" aria-label="Uitleg" aria-expanded="false">i</button>` : ""}</h4>` : ""}
      ${c.info ? `<div class="tip" id="tip" hidden>${infoHtml(c.info)}</div>` : ""}
      ${this._ask === "tp" && this._tpRow ? this._askBox(this._tpRow) : ""}<div class="rows">${rows.map((r, i) => this._row(r, i) + (r.info && r.type !== "section" ? `<div class="rinfo" data-rt="${i}" ${(this._ri || {})[i] ? "" : "hidden"}>${infoHtml(r.info)}</div>` : "") + (this._ask === i ? this._askBox(r) : this._ask === "now" + i && this._nowRow ? this._askBox(this._nowRow) : "")).join("")}</div></ha-card>`;
    this._wire();
    if (c.tag_power) { const R = this.shadowRoot, ent = c.tag_power, who = c.tag_who || "deze auto";
      R.querySelectorAll("[data-tp]").forEach((b) => b.addEventListener("click", () => { const on = ((this._hass.states[ent] || {}).state) !== "off";
        this._tpRow = { warn: on ? `HESC uitzetten voor ${who}?` : `HESC aanzetten voor ${who}?`, note: on ? `HESC laat ${who} dan met rust: geen planning, niet pauzeren of hervatten. Heeft ${who} een eigen laadpaal, dan laat HESC die ook met rust. Een andere auto gaat gewoon door, ook als die dezelfde laadpaal gebruikt.` : `HESC gaat ${who} dan weer laden op zon en goedkope uren volgens de planning.`, sure: on ? "Ja, ik wil dit uitzetten" : "Ja, ik wil dit aanzetten", yes: on ? "Uitzetten" : "Aanzetten" };
        this._ask = this._ask === "tp" ? undefined : "tp"; this._sure = false; this._render(); }));
      if (this._ask === "tp") R.querySelectorAll("[data-ask=yes]").forEach((b) => b.addEventListener("click", (e) => { e.stopImmediatePropagation(); if (!this._sure) return; const on = ((this._hass.states[ent] || {}).state) !== "off"; this._call("switch", on ? "turn_off" : "turn_on", { entity_id: ent }); this._ask = undefined; this._sure = false; this._render(); }, true)); }
  }

  _call(dom, svc, data) {
    return this._hass.callService(dom, svc, data).catch((e) => {
      this.dispatchEvent(new CustomEvent("hass-notification", { bubbles: true, composed: true, detail: { message: `HESC: ${(e && e.message) || e}` } }));
      this._sig = ""; if (this._hass) this.hass = this._hass;
    });
  }

  _wire() {
    const r = this.shadowRoot, rows = this._config.rows || [];
    if (rows.some((x) => x.type === "batwiz")) hv4BatWizWire(this);
    if (rows.some((x) => x.type === "wiz")) hv4WizWire(this);
    r.querySelectorAll("[data-pcountry]").forEach((el) => el.addEventListener("change", () => {
      const row = rows[+el.dataset.pcountry], c = hv4Country(this._hass, el.value), cur = HV4_CUR[c];
      this._call("select", "select_option", { entity_id: row.entity, option: el.value });
      const ce = row.entity.replace(/_price_country$/, "_currency");
      if (cur && this._hass.states[ce]) this._call("select", "select_option", { entity_id: ce, option: cur }); // the country sets the currency
    }));
    r.querySelectorAll("[data-psrc]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+b.dataset.psrc], ent = row.entity;
      this._call("select", "select_option", { entity_id: ent, option: b.dataset.o });
      const te = ent.replace(/^select\.(.*)_price_source$/, "text.$1_day_ahead_price_sensor");
      if (b.dataset.sensor && this._hass.states[te]) this._call("text", "set_value", { entity_id: te, value: b.dataset.sensor });
    }));
    r.querySelectorAll("[data-redo]").forEach((b) => b.addEventListener("click", () => hv4RedoOpen(this._hass)));
    r.querySelectorAll("[data-phshow]").forEach((c) => c.addEventListener("change", () => { try { localStorage.setItem(HV4_PHSHOW, c.checked ? "1" : "0"); } catch (e) { /* private window */ } }));
    r.querySelectorAll("[data-backv3]").forEach((b) => b.addEventListener("click", () => hv4BackV3(this._hass, b)));
    const tipb = r.querySelector("[data-tip]");
    if (tipb) { const t0 = r.getElementById("tip"); if (t0 && this._tipOpen) { t0.hidden = false; tipb.setAttribute("aria-expanded", "true"); }
      tipb.addEventListener("click", () => { const t = r.getElementById("tip"); t.hidden = !t.hidden; this._tipOpen = !t.hidden; tipb.setAttribute("aria-expanded", String(!t.hidden)); }); }
    r.querySelectorAll("input[type=range][data-i]").forEach((inp) => {
      const row = rows[+inp.dataset.i], s = this._hass.states[row.entity], a = s.attributes, unit = a.unit_of_measurement ? ` ${a.unit_of_measurement}` : "";
      inp.addEventListener("pointerdown", () => { this._busy = row.entity; });
      inp.addEventListener("input", () => {
        this._busy = row.entity;
        inp.style.setProperty("--v", `${(inp.value - a.min) / (a.max - a.min) * 100}%`);
        inp.nextElementSibling.textContent = `${this._num(inp.value, a.step || 1)}${unit}`;
      });
      inp.addEventListener("change", () => {
        this._busy = null;
        this._call(row.entity.split(".")[0], "set_value", { entity_id: row.entity, value: +inp.value });
      });
    });
    r.querySelectorAll("[data-ri]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); e.preventDefault(); const k = +b.dataset.ri; this._ri = { ...(this._ri || {}), [k]: !(this._ri || {})[k] }; const t = r.querySelector(`[data-rt="${k}"]`); if (t) t.hidden = !this._ri[k]; b.setAttribute("aria-expanded", String(this._ri[k])); }, true));
    r.querySelectorAll("[data-mv]").forEach((b) => b.addEventListener("click", () => { const row = rows[+b.dataset.mv]; this._call(row.entity.split(".")[0], "set_value", { entity_id: row.entity, value: b.dataset.o }); }));
    r.querySelectorAll("[data-ne]").forEach((b) => b.addEventListener("click", () => { this._edit = +b.dataset.ne; this._render(); const inp = this.shadowRoot.querySelector("[data-nv]"); if (inp) { inp.focus(); inp.select(); } }));
    const nok = (i) => { const inp = this.shadowRoot.querySelector(`[data-nv="${i}"]`), row = rows[i], x = parseFloat(String(inp ? inp.value : "").replace(",", ".")); this._edit = undefined; if (row && Number.isFinite(x)) this._call(row.entity.split(".")[0], "set_value", { entity_id: row.entity, value: x }); this._render(); };
    r.querySelectorAll("[data-nok]").forEach((b) => b.addEventListener("click", () => nok(+b.dataset.nok)));
    r.querySelectorAll("[data-nv]").forEach((inp) => inp.addEventListener("keydown", (e) => { if (e.key === "Enter") nok(+inp.dataset.nv); if (e.key === "Escape") { this._edit = undefined; this._render(); } }));
    r.querySelectorAll("[data-nowp]").forEach((box) => box.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      const i = +box.dataset.nowp, s = this._hass.states[rows[i].entity], o = (s.attributes.options || []).filter((x) => x !== "Off"), cur = (this._pend || {})[i] || (o.includes("80%") ? "80%" : o[0]);
      this._pend = { ...(this._pend || {}), [i]: o[Math.min(o.length - 1, Math.max(0, o.indexOf(cur) + +b.dataset.dir))] }; this._render(); })));
    r.querySelectorAll("[data-nowgo]").forEach((b) => b.addEventListener("click", () => {
      const i = +b.dataset.nowgo, s = this._hass.states[rows[i].entity], o = (s.attributes.options || []).filter((x) => x !== "Off"), pv = (this._pend || {})[i] || (o.includes("80%") ? "80%" : o[0]);
      this._pend = { ...(this._pend || {}), [i]: pv };
      this._nowRow = { warn: `Nu laden tot ${pv}?`, note: "HESC laadt de auto dan meteen van het net, ook als stroom nu duur is of er geen zon is, tot de accu op dit doel staat. Je planning wacht zolang. Stoppen kan altijd.", sure: "Ja, ik wil nu laden", yes: "Start" };
      this._ask = this._ask === "now" + i ? undefined : "now" + i; this._sure = false; this._render(); }));
    r.querySelectorAll("[data-nowstop]").forEach((b) => b.addEventListener("click", () => { const row = rows[+b.dataset.nowstop]; this._call("select", "select_option", { entity_id: row.entity, option: "Off" }); }));
    if (typeof this._ask === "string" && this._ask.startsWith("now")) r.querySelectorAll("[data-ask=yes]").forEach((b) => b.addEventListener("click", (e) => {
      e.stopImmediatePropagation(); if (!this._sure) return; const i = +this._ask.slice(3), pv = (this._pend || {})[i];
      if (pv) this._call("select", "select_option", { entity_id: rows[i].entity, option: pv }); this._ask = undefined; this._sure = false; this._sig = ""; this._render(); }, true));
    r.querySelectorAll(".stp[data-i]").forEach((box) => box.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+box.dataset.i], s = this._hass.states[row.entity], dom = row.entity.split(".")[0], dir = +b.dataset.dir;
      if (box.dataset.sel) {
        const o = s.attributes.options, j = (o.indexOf(s.state) + dir + o.length) % o.length;
        this._call(dom, "select_option", { entity_id: row.entity, option: o[j] });
      } else {
        const a = s.attributes, st = row.step || +a.step || 1, v = Math.min(+a.max, Math.max(+a.min, Math.round((+s.state + dir * st) / st) * st));
        this._call(dom, "set_value", { entity_id: row.entity, value: v });
      }
    })));
    r.querySelectorAll(".tg[data-i]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+b.dataset.i], dom = row.entity.split(".")[0];
      this._call(dom === "input_boolean" ? "input_boolean" : "switch", b.classList.contains("on") ? "turn_off" : "turn_on", { entity_id: row.entity });
    }));
    r.querySelectorAll(".chip[data-i]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+b.dataset.i];
      this._call(row.entity.split(".")[0], "select_option", { entity_id: row.entity, option: b.dataset.o });
    }));
    r.querySelectorAll("[data-nav]").forEach((b) => b.addEventListener("click", () => {
      const ta = rows[+b.dataset.nav].tap_action || {};
      if (ta.action === "navigate" && ta.navigation_path) {
        history.pushState(null, "", ta.navigation_path);
        window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } }));
      }
    }));
    r.querySelectorAll("[data-dl]").forEach((b) => b.addEventListener("click", async () => {
      const [car, what] = b.dataset.dl.split("/");
      try {
        const res = await this._hass.fetchWithAuth(`/api/hesc_v4/costs/${car}/${what}.csv`);
        if (res.status === 404) throw new Error("Druk eerst op Uitvoeren bij Laadkosten exporteren.");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const url = URL.createObjectURL(await res.blob()), a = document.createElement("a");
        a.href = url; a.download = `hesc_v4_laadkosten_${car}_${what}.csv`; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 5000);
      } catch (e) { this.dispatchEvent(new CustomEvent("hass-notification", { bubbles: true, composed: true, detail: { message: `HESC: ${(e && e.message) || e}` } })); }
    }));
    r.querySelectorAll("[data-vk]").forEach((b) => b.addEventListener("click", async () => {
      const row = rows[+b.dataset.vk], st = this._hass.states[row.entity], t = String(((st && st.attributes) || {})[row.attribute] || "");
      let cur = t.split(",").map((x) => x.trim()).filter(Boolean); const o = b.dataset.o;
      cur = cur.includes(o) ? cur.filter((x) => x !== o) : [...cur, o];
      if (!cur.length) { this.dispatchEvent(new CustomEvent("hass-notification", { bubbles: true, composed: true, detail: { message: "Kies er minstens één." } })); return; }
      b.classList.toggle("on"); b.textContent = (b.classList.contains("on") ? "✓ " : "") + o;
      const res = await this._hass.callWS({ type: "hesc_v4/setup/value", key: row.attribute, value: cur, ...(row.car ? { car: row.car } : {}) }).catch((e) => ({ ok: false, error: (e && e.message) || e }));
      if (!res.ok) this.dispatchEvent(new CustomEvent("hass-notification", { bubbles: true, composed: true, detail: { message: `HESC: ${res.error}` } }));
    }));
    r.querySelectorAll("[data-setup]").forEach((b) => b.addEventListener("click", () => { history.pushState(null, "", "/config/integrations/integration/hesc_v4"); window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } })); }));
    r.querySelectorAll("[data-src]").forEach((b) => b.addEventListener("click", async () => {
      try {
        if (!this._srcList) { const f = await this._hass.callWS({ type: "hesc_v4/setup/find" }); if (!(f.features || []).includes("set_source")) throw new Error("old"); this._srcList = f.sources || {}; }
        this._edit = +b.dataset.src; this._render();
      } catch (e) { history.pushState(null, "", "/config/integrations/integration/hesc_v4"); window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } })); }
    }));
    r.querySelectorAll("[data-svr]").forEach((x) => x.addEventListener("change", () => { const h = r.querySelector("[data-sv]"); if (h) h.value = x.dataset.svr; }));
    r.querySelectorAll("[data-sok]").forEach((b) => b.addEventListener("click", async () => {
      const row = rows[+b.dataset.sok], sel = r.querySelector(`[data-sv="${b.dataset.sok}"]`);
      const res = await this._hass.callWS({ type: "hesc_v4/setup/source", key: row.attribute, entity_id: sel.value || null, ...(row.car ? { car: row.car } : {}) }).catch((e) => ({ ok: false, error: (e && e.message) || e }));
      if (!res.ok) this.dispatchEvent(new CustomEvent("hass-notification", { bubbles: true, composed: true, detail: { message: `HESC: ${res.error}` } }));
      if (res.ok) this._pendSrc = { ...(this._pendSrc || {}), [b.dataset.sok]: { v: sel.value || "", at: Date.now() } }; // decision 08-11 10:20: show that it is being saved
      this._edit = undefined; this._srcList = undefined; this._sig = ""; this._render();
    }));
    r.querySelectorAll("[data-te]").forEach((b) => b.addEventListener("click", () => {
      this._edit = +b.dataset.te; this._render();
      const inp = r.querySelector("[data-ti]"); if (inp) { inp.focus(); inp.select(); }
    }));
    const save = () => {
      const inp = r.querySelector("[data-ti]"); if (!inp) return;
      const row = rows[+inp.dataset.ti]; this._edit = undefined;
      this._call(row.entity.split(".")[0], "set_value", { entity_id: row.entity, value: inp.multiple ? [...inp.selectedOptions].map((o) => o.value).filter(Boolean).join(", ") : inp.value.trim() });
      this._sig = ""; this._render();
    };
    r.querySelectorAll("[data-bps]").forEach((b) => b.addEventListener("click", () => { const want = b.dataset.bps.split(","); r.querySelectorAll("[data-bp]").forEach((x) => { x.checked = want.includes(x.dataset.bp); }); const h = r.querySelector("input[type=hidden][data-ti]"); if (h) h.value = want.join(", "); }));
    r.querySelectorAll("[data-bp]").forEach((cb) => cb.addEventListener("change", () => { const h = r.querySelector("input[type=hidden][data-ti]"); if (h) h.value = [...r.querySelectorAll("[data-bp]:checked")].map((x) => x.dataset.bp).join(", "); }));
    r.querySelectorAll("[data-tok]").forEach((b) => b.addEventListener("click", save));
    r.querySelectorAll("[data-ti]").forEach((inp) => inp.addEventListener("keydown", (e) => {
      if (e.key === "Enter") save();
      if (e.key === "Escape") { e.stopPropagation(); this._edit = undefined; this._render(); }
    }));
    r.querySelectorAll("[data-di]").forEach((inp) => inp.addEventListener("change", () => {
      const row = rows[+inp.dataset.di], dom = row.entity.split(".")[0];
      if (inp.value) this._call(dom === "date" ? "date" : "input_datetime", dom === "date" ? "set_value" : "set_datetime", { entity_id: row.entity, date: inp.value });
    }));
    r.querySelectorAll("[data-dm]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+b.dataset.dm], D = (window.__hv4Demo = window.__hv4Demo || {}), v = row.key in D ? D[row.key] : row.value;
      if (row.kind === "switch") D[row.key] = !v;
      if (row.kind === "time") D[row.key] = plStep(v, +b.dataset.dir);
      if (row.kind === "number") D[row.key] = !v && +b.dataset.dir > 0 && row.start ? row.start : Math.max(0, Math.min(row.max || 99, (v || 0) + (+b.dataset.dir) * (row.step || 1))) || null;
      if (row.kind === "chips") D[row.key] = b.dataset.o;
      window.dispatchEvent(new CustomEvent("hesc-v4-demo")); // other example blocks that depend on this value redraw too
    }));
    r.querySelectorAll("[data-rep]").forEach((b) => b.addEventListener("click", async () => {
      const i = +b.dataset.rep, row = rows[i]; this._repRes = { i, busy: true }; this._render();
      try {
        const ans = await this._hass.callWS({ type: "call_service", domain: "hesc_v4", service: "export", service_data: { form: row.variant }, return_response: true }), x = (ans && ans.response) || {};
        this._repRes = { i, url: x.url || "", file: x.file || "", text: x.text || "" };
      } catch (e) { this._repRes = { i, err: `Mislukt: ${(e && e.message) || e}` }; }
      this._render();
    }));
    r.querySelectorAll("[data-day]").forEach((d) => d.addEventListener("click", () => {
      const st = this._hass.states[d.dataset.day];
      this._call("switch", st && st.state === "on" ? "turn_off" : "turn_on", { entity_id: d.dataset.day });
    }));
    const bkb = r.querySelector("[data-bk]");
    if (bkb) bkb.addEventListener("click", () => { // same as Marstek Capacity Monitor: make a back-up from inside the box
      const row = rows[this._ask]; this._call("button", "press", { entity_id: row.backup }); this._bk = true; this._render();
    });
    const sure = r.querySelector("[data-sure]");
    if (sure) sure.addEventListener("click", () => { this._sure = !this._sure; this._render(); });
    r.querySelectorAll("[data-ask]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[this._ask];
      if (b.dataset.ask === "yes" && this._sure && row && row.type === "power") this._call("switch", ((this._hass.states[row.entity] || {}).state) === "on" ? "turn_off" : "turn_on", { entity_id: row.entity });
      else if (b.dataset.ask === "yes" && this._sure && row) this._call(row.entity.split(".")[0], "press", { entity_id: row.entity });
      this._ask = undefined; this._sure = false; this._bk = false; this._render();
    }));
    r.querySelectorAll("[data-pw]").forEach((b) => b.addEventListener("click", () => {
      const i = +b.dataset.pw, row = rows[i], on = ((this._hass.states[row.entity] || {}).state) === "on";
      row.warn = row.warnOff && on ? row.warnOff : row.warnOn && !on ? row.warnOn : on ? "HESC uitzetten?" : "HESC aanzetten?";
      row.note = (on ? row.noteOff : row.noteOn) || (on ? "HESC stuurt dan niets meer aan: de laadpaal laadt zoals hij zelf staat ingesteld, zonder zon- of prijsplanning." : "HESC gaat dan weer laden op zon en goedkope uren volgens je planning.");
      row.sure = on ? "Ja, ik wil dit uitzetten" : "Ja, ik wil dit aanzetten"; row.yes = on ? "Uitzetten" : "Aanzetten";
      this._ask = this._ask === i ? undefined : i; this._sure = false; this._render();
    }));
    r.querySelectorAll(".btn[data-i]").forEach((b) => b.addEventListener("click", () => {
      const row = rows[+b.dataset.i];
      // decision 30-10 20:36/20:43: a risky button opens a confirmation box, as in Marstek Capacity Monitor:
      // warning, a switch "I know …", then "Yes" (only after the switch) or Cancel
      if (b.classList.contains("danger")) { this._ask = this._ask === +b.dataset.i ? undefined : +b.dataset.i; this._sure = false; this._render(); return; }
      this._call(row.entity.split(".")[0], "press", { entity_id: row.entity });
    }));
  }
}

/* ---------- first start: a few simple questions, one per screen (sketch, example data, nothing saved) ---------- */

const SUCSS = `
:host{--line:var(--divider-color,#30333c);--muted:var(--secondary-text-color,#9aa0aa);--card2:color-mix(in srgb,var(--primary-text-color,#e1e1e1) 6%,var(--ha-card-background,var(--card-background-color,#1f2128)));--dot:#ff9800;--c:var(--primary-color)}
ha-card{padding:18px 20px;display:grid;gap:16px}
.prog{display:flex;gap:6px}.prog i{flex:1;height:4px;border-radius:2px;background:var(--card2)}.prog i.on{background:var(--c)}
.step{font-size:12px;color:var(--muted)}
h3{margin:0;font-size:20px;font-weight:500;line-height:1.3}
.sub{margin:0;color:var(--muted);font-size:14px;line-height:1.45}
.big{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}
.opt{font:inherit;border-radius:14px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:14px 12px;cursor:pointer;text-align:left;display:grid;gap:4px}
.opt b{font-size:17px}.opt span{font-size:12px;color:var(--muted)}
.opt.on{border-color:var(--c);background:color-mix(in srgb,var(--c) 22%,transparent)}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{font:inherit;font-size:14px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:8px 14px;cursor:pointer}
.chip.on{border-color:var(--c);background:color-mix(in srgb,var(--c) 25%,transparent);font-weight:600}
.found{display:flex;gap:10px;align-items:center;background:var(--card2);border-radius:12px;padding:10px 14px;font-size:14px}
.found select{display:block;width:100%;margin-top:6px;font:inherit;font-size:14px;color:var(--primary-text-color);background:var(--ha-card-background,var(--card-background-color,#1f2128));
  border:1.5px solid var(--line);border-radius:10px;padding:7px 10px}
.found.pick .ok{color:var(--dot)}
.found .ok{color:#66bb6a;font-size:18px}.found .no{color:var(--dot);font-size:18px}.found small{display:block;color:var(--muted);font-size:12px}
.car{display:grid;gap:12px;border:1.5px solid var(--line);border-radius:14px;padding:14px}
.car h4{margin:0;font-size:15px;font-weight:500;display:flex;gap:8px;align-items:center}.car h4 i{width:10px;height:10px;border-radius:50%}
.name{font:inherit;font-size:15px;font-weight:600;border-radius:10px;border:1.5px solid var(--line);background:var(--card2);color:var(--primary-text-color);padding:8px 12px;width:100%;box-sizing:border-box}
.name:focus{outline:none;border-color:var(--c)}
.lbl{font-size:12px;color:var(--muted);margin-bottom:4px}
.sl{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center}
.sl output{font-size:16px;font-weight:600;min-width:70px;text-align:right}
.sl input{-webkit-appearance:none;appearance:none;width:100%;height:10px;border-radius:999px;margin:0;cursor:pointer;
  background:linear-gradient(90deg,var(--cc,var(--c)) 0 var(--v),var(--card2) var(--v) 100%);border:1px solid var(--line)}
.sl input::-webkit-slider-thumb{-webkit-appearance:none;width:24px;height:24px;border-radius:50%;background:#fff;border:3px solid var(--cc,var(--c));box-shadow:0 1px 4px rgba(0,0,0,.4)}
.sl input::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid var(--cc,var(--c))}
.nav{display:flex;gap:10px;align-items:center}
.btn{font:inherit;font-size:14px;border-radius:999px;border:1.5px solid var(--line);background:none;color:var(--primary-text-color);padding:9px 18px;cursor:pointer}
.btn.pri{background:var(--c);border-color:var(--c);color:var(--text-primary-color,#fff);font-weight:600}
.btn[disabled]{opacity:.4;cursor:default}
.stp2{display:inline-flex;align-items:center;border:1.5px solid var(--line);border-radius:999px;background:var(--card2);height:40px}
.stp2 button{width:40px;height:40px;border:0;background:none;color:var(--primary-text-color);font-size:20px;cursor:pointer;border-radius:50%}
.stp2 b{min-width:62px;text-align:center;font-size:18px;font-weight:600}
.tg{width:48px;height:28px;border-radius:999px;border:0;background:var(--card2);box-shadow:inset 0 0 0 1.5px var(--line);position:relative;cursor:pointer;flex:none}
.tg::after{content:"";position:absolute;top:4px;left:4px;width:20px;height:20px;border-radius:50%;background:var(--muted);transition:left .15s}
.tg.on{background:var(--c);box-shadow:none}.tg.on::after{left:24px;background:#fff}
.sum{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 16px;font-size:14px}.sum dt{color:var(--muted)}.sum dd{margin:0}
.note{font-size:12px;color:var(--dot)}
${INFO_CSS}`;

const SU_CHARGERS = ["Wallbox", "Alfen Eve", "Peblar", "myenergi Zappi", "go-e Charger", "Fronius Wattpilot", "SMA EV Charger", "evcc", "Ohme", "Easee", "Anders"];
const SU_PRICES = ["Nord Pool", "EnergyZero / ANWB", "EasyEnergy", "Tibber", "Grid Clock", "Prijslijst in een sensor"];

/* ---------- first start: look for candidates in this Home Assistant (besluit 28-10 nr 17, 30-10 nr 37) ----------
 * Only reads hass.states / hass.entities / hass.devices; nothing is saved. One candidate = found, several = a choice list
 * with today's value, none = what is needed. */
const SU_CHARGER_PLATFORMS = {
  wallbox: "Wallbox", alfen_wallbox: "Alfen Eve", peblar: "Peblar", myenergi: "myenergi Zappi", goecharger: "go-e Charger",
  goecharger_api2: "go-e Charger", go_echarger: "go-e Charger", wattpilot: "Fronius Wattpilot", fronius_wattpilot: "Fronius Wattpilot",
  smaev: "SMA EV Charger", sma_ev_charger: "SMA EV Charger", evcc_intg: "evcc", evcc: "evcc", ohme: "Ohme", easee: "Easee",
};
const SU_PRICE_PLATFORMS = {
  nordpool: "Nord Pool", energyzero: "EnergyZero / ANWB", anwb_energie: "EnergyZero / ANWB", easyenergy: "EasyEnergy",
  tibber: "Tibber", gridclock: "Grid Clock", ha_gridclock: "Grid Clock", entsoe: "Prijslijst in een sensor",
};
const SU_CAR_PLATFORMS = /byd|skoda|volkswagen|vw|tesla|kia|hyundai|renault|bmw|mercedes|polestar|volvo|audi|cupra|seat|nissan|peugeot|opel|citroen|dacia|mg|toyota|ford|wican|myskoda|connected_?drive|uvo|bluelink|ev_?smart/i;
const SU_NOT_CAR = /phone|iphone|pixel|galaxy|tablet|ipad|watch|airpods|laptop|macbook|marstek|venus|mt\d|thuisaccu|home.?battery|powerwall|zendure|remote|button|knop|motion|beweging|door|deur|window|raam|thermostat|smoke|rook|leak|lekk|zigbee|aqara|hue|ikea|sonoff/i;

function suEnt(hass, id) {
  const st = hass.states[id], reg = (hass.entities || {})[id] || {}, dev = reg.device_id && (hass.devices || {})[reg.device_id];
  const name = (st && st.attributes.friendly_name) || id;
  const unit = st && st.attributes.unit_of_measurement;
  const v = st ? st.state : "?";
  const num = parseFloat(v);
  const val = isNaN(num) ? v : `${num.toLocaleString(hv4Loc(), { maximumFractionDigits: unit === "%" ? 0 : 2 })}${unit ? ` ${unit}` : ""}`;
  return { id, name, val, platform: reg.platform || "", dev: dev ? (dev.name_by_user || dev.name || "") : "", unit, dc: st && st.attributes.device_class };
}

function suFind(hass, kind) {
  if (!hass) return [];
  const all = Object.keys(hass.states).filter((id) => id.startsWith("sensor.") && !id.includes("hesc_v3") && !id.includes("hesc_v4"));
  const E = all.map((id) => suEnt(hass, id)), txt = (e) => `${e.id} ${e.name} ${e.dev}`;
  const power = (e) => e.dc === "power" || /^(k?W)$/.test(e.unit || "");
  let list = [];
  if (kind === "soc") {
    list = E.filter((e) => e.unit === "%" && !SU_NOT_CAR.test(txt(e))
      && (SU_CAR_PLATFORMS.test(e.platform) || /soc|state.?of.?charge|accustand|laadniveau|battery.?level|batterij/i.test(txt(e))))
      .map((e) => ({ ...e, score: (SU_CAR_PLATFORMS.test(e.platform) || SU_CAR_PLATFORMS.test(e.dev) ? 3 : 0) + (/soc|state.?of.?charge/i.test(txt(e)) ? 2 : 0) }));
  } else if (kind === "pv") {
    list = E.filter((e) => power(e) && /pv|solar|zon|omvormer|inverter/i.test(txt(e)) && !/forecast|verwacht|predict|solcast/i.test(txt(e)))
      .map((e) => ({ ...e, score: /total|totaal|som/i.test(txt(e)) ? 2 : 0 }));
  } else if (kind === "forecast") {
    list = E.filter((e) => /solcast|forecast_solar|open_meteo_solar/.test(e.platform) || /solcast|forecast.?solar|zonverwachting/i.test(txt(e)))
      .filter((e) => /today|vandaag|forecast_today/i.test(txt(e)))
      .map((e) => ({ ...e, score: /solcast/i.test(e.platform + e.id) ? 2 : 1 }));
  } else if (kind === "grid") {
    list = E.filter((e) => power(e) && (/dsmr|homewizard|p1_monitor|slimmelezer/.test(e.platform) || /grid|\bnet\b|p1|netvermogen|power_consumption|active_power/i.test(txt(e))))
      .filter((e) => !/pv|solar|zon|car|ev_|wallbox|charger|laad/i.test(txt(e)))
      .map((e) => ({ ...e, score: (/dsmr|homewizard|p1_monitor/.test(e.platform) ? 2 : 0) + (/p1|grid|net/i.test(e.id) ? 1 : 0) }));
  } else if (kind === "price") {
    list = E.filter((e) => SU_PRICE_PLATFORMS[e.platform] || /^sensor\.grid_clock_.*_prices$/.test(e.id) || /^sensor\.nordpool/.test(e.id))
      .filter((e) => /^sensor\.grid_clock_.*_prices$/.test(e.id) || /EUR|€|ct|kWh/i.test(e.unit || "") || /price|prijs/i.test(txt(e)))
      .map((e) => ({ ...e, src: SU_PRICE_PLATFORMS[e.platform] || (/grid_clock/.test(e.id) ? "Grid Clock" : "Nord Pool"),
        score: /current|now|nu|_prices$|kwh_nl/i.test(e.id) ? 2 : 0 }));
    // Grid Clock: the list sensor counts quarters; show the price of now from its sibling sensor
    list.forEach((e) => { const m = e.id.match(/^sensor\.grid_clock_(.+)_prices$/); const cur = m && hass.states[`sensor.grid_clock_${m[1]}_current_price`];
      if (m) e.val = cur ? `${cur.state} ct/kWh · zone ${m[1].toUpperCase()}` : `zone ${m[1].toUpperCase()}`; });
  }
  // what HESC v3 already uses comes first (overstap van v3, besluit 9)
  const used = suV3Refs(hass);
  list.forEach((e) => { if (used.has(e.id)) e.score += 5; });
  const top = list.sort((a, b) => b.score - a.score || a.name.localeCompare(b.name)).slice(0, 8);
  top.total = list.length;
  return top;
}

function suV3Refs(hass) { // entity ids mentioned in HESC v3's setup sensor
  const a = (hass.states["sensor.hesc_v3_setup"] || {}).attributes || {}, out = new Set();
  const walk = (v) => { if (typeof v === "string") v.split(/[\s,]+/).forEach((x) => out.add(x)); else if (v && typeof v === "object") Object.values(v).forEach(walk); };
  walk(a);
  return out;
}

function suChargers(hass) { // charger types found via their integration, with the device names
  const out = {};
  for (const reg of Object.values((hass && hass.entities) || {})) {
    const t = SU_CHARGER_PLATFORMS[reg.platform];
    if (!t) continue;
    const dev = reg.device_id && (hass.devices || {})[reg.device_id];
    (out[t] = out[t] || new Set()).add(dev ? (dev.name_by_user || dev.name) : t);
  }
  return Object.fromEntries(Object.entries(out).map(([k, v]) => [k, [...v]]));
}

/* One "found" block: ✓ with the single candidate, a choice list when there are more, or what is needed when none. */
function suPick(key, label, help, list, picked, need) {
  if (!list.length) return `<div class="found"><span class="no">!</span><div>${label}: niets gevonden<small>${need}</small></div></div>`;
  const cur = list.find((e) => e.id === picked) || list[0];
  if (list.length === 1) return `<div class="found"><span class="ok">✓</span><div>${label} gevonden<small>${cur.name} · nu ${cur.val}</small></div></div>`;
  return `<div class="found pick"><span class="ok">?</span><div style="flex:1;min-width:0">${label}: ik zie ${list.total || list.length} kandidaten, kies degene die ${help}
    <select data-pick="${key}">${list.map((e) => `<option value="${e.id}"${e.id === cur.id ? " selected" : ""}>${e.name} — nu ${e.val}</option>`).join("")}</select></div></div>`;
}

class HescV4Setup extends HTMLElement {
  setConfig(config) {
    this._config = config || {};
    this._s = window.__hescSetup = window.__hescSetup || {
      cars: 0, chargers: 0, ctype: ["Wallbox", "Wallbox"], amp: [16, 16], phase: "", famp: "", lb: "", how: "", who: "", first: 0, swap: "22:30", remind: true,
      car: [{ name: "BMW i3", kwh: 108.7 }, { name: "BYD Atto 3 Evo", kwh: 75 }], sun: null, dyn: null, src: "Nord Pool",
    };
    this._s.pick = this._s.pick || {};
    this._i = 0;
    this._render();
  }
  set hass(h) {
    const first = !this._hass;
    this._hass = h;
    if (first) { this._seedFound(); this._render(); } // the first time HA data is there: fill in what was found
  }
  getCardSize() { return 6; }

  /* Pre-select what this Home Assistant already has: charger type, price source. */
  _seedFound() {
    const s = this._s, h = this._hass;
    if (s.seeded || !h) return;
    s.seeded = true;
    const ch = Object.keys(suChargers(h));
    if (ch.length) { s.ctype[0] = ch[0]; s.ctype[1] = ch[1] || ch[0]; }
    const pr = suFind(h, "price");
    if (pr.length) s.src = pr[0].src;
    // with the real car alone (proefbord switch), car 1 gets the name of the car HA knows
    const soc = suFind(h, "soc");
    if (hv4Cur() === "real" && soc.length && soc[0].dev) {
      const cap = parseFloat((h.states["number.hesc_v3_ev_usable_battery_capacity"] || {}).state); // what HESC v3 already knows
      s.car[0] = { ...s.car[0], name: soc[0].dev, kwh: isNaN(cap) ? s.car[0].kwh : Math.round(cap) };
    }
  }

  _priceStep() {
    const s = this._s, all = suFind(this._hass, "price"), have = new Set(all.map((e) => e.src)), list = all.filter((e) => e.src === s.src);
    return `<div class="lbl">waar komen je prijzen vandaan?</div><div class="chips">${SU_PRICES.map((p) => `<button class="chip${s.src === p ? " on" : ""}" data-src="${p}">${have.has(p) ? "✓ " : ""}${p}</button>`).join("")}</div>
      ${suPick("price", "Prijzen", "de prijzen van vandaag en morgen heeft", list, s.pick.price,
        s.src === "Prijslijst in een sensor" ? "kies straks bij Instellingen de sensor met de prijslijst" : `de ${s.src}-integratie is niet gevonden; installeer die eerst`)}
      ${s.src === "Grid Clock" ? `<p class="sub">Grid Clock geeft de kale beursprijs per uur in euro; vul opslag en btw in bij Kosten.</p>` : ""}`;
  }

  _chargerFound(type) {
    const found = suChargers(this._hass)[type];
    if (found) return `<div class="found"><span class="ok">✓</span><div>${type} gevonden<small>${found.join(" · ")} · HESC zoekt laadvermogen, aangesloten en laadstand zelf</small></div></div>`;
    if (type === "Anders") return `<div class="found"><span class="no">!</span><div>Andere laadpaal<small>HESC vraagt straks zelf naar het laadvermogen, aangesloten en de laadstand</small></div></div>`;
    return `<div class="found"><span class="no">!</span><div>${type}: integratie niet gevonden<small>installeer eerst de ${type}-integratie in Home Assistant</small></div></div>`;
  }

  _steps() { // besluit 01-11 10:17-10:34: part 1 questions, then part 2 only what HESC did not find
    const s = this._s, st = ["how", "house", "ctype", "car"];
    if (s.cars === 2 && s.chargers === 1) st.push("swap");
    st.push("found");
    if (s.dyn === "ja") st.push("prices");
    st.push("done");
    return st;
  }

  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const s = this._s, steps = this._steps();
    this._i = Math.min(this._i, steps.length - 1);
    const id = steps[this._i], last = id === "done";
    const opt = (k, v, t, sub) => `<button class="opt${s[k] === v ? " on" : ""}" data-k="${k}" data-v="${v}"><b>${t}</b>${sub ? `<span>${sub}</span>` : ""}</button>`;
    const opt2 = (k) => ["ja", "nee"].map((v) => `<button class="chip${s[k] === v ? " on" : ""}" data-hk="${k}" data-v="${v}">${v === "ja" ? "Ja" : "Nee"}</button>`).join("");
    const nCh = s.cars === 2 ? s.chargers : 1, colors = ["#3fc8f4", "#ff8a65"];
    let body = "", ok = true;
    if (id === "how") {
      body = `<h3>Hoe laad je thuis?</h3><p class="sub">HESC v4 start in schaduwmodus: het kijkt mee en schakelt niets.</p>
        <div class="big">${opt("how", "een", "Eén auto")}${opt("how", "2x1", "Twee auto's, één laadpaal", "om de beurt, jij zet de kabel om")}${opt("how", "2x2", "Twee auto's, elk een eigen laadpaal")}</div>`;
      ok = !!s.how;
    } else if (id === "ctype") {
      body = `<h3>${nCh === 2 ? "Je laadpalen" : "Je laadpaal"}</h3><p class="sub">Het merk, en wat de installateur als maximum heeft ingesteld.</p>`
        + Array.from({ length: nCh }, (_, j) => `${nCh === 2 ? `<div class="lbl">laadpaal ${j + 1}</div>` : ""}<div class="chips">${SU_CHARGERS.map((c) => `<button class="chip${s.ctype[j] === c ? " on" : ""}" data-ct="${j}" data-v="${c}">${c}</button>`).join("")}</div>
          <div class="found"><span style="flex:1">maximum dat de installateur heeft ingesteld<small>Weet je het niet, laat dan 16 A staan. Bij Easee, Peblar en Wallbox leest HESC dit straks zelf uit de laadpaal.</small></span><div class="stp2"><button data-amp="${j}" data-dir="-1" aria-label="1 ampère minder">−</button><b>${s.amp[j]} A</b><button data-amp="${j}" data-dir="1" aria-label="1 ampère meer">+</button></div></div>`).join("");
    } else if (id === "swap") {
      body = `<h3>Om de beurt</h3><p class="sub">Beide auto's laden aan dezelfde laadpaal. De auto die 's avonds aan de paal hangt laadt eerst; de andere nadat jij de kabel hebt omgezet.</p>
        <div><div class="lbl">kabel omzetten uiterlijk om</div><div class="stp2"><button data-sw="-1" aria-label="15 minuten eerder">−</button><b>${s.swap}</b><button data-sw="1" aria-label="15 minuten later">+</button></div></div>
        <div class="found"><span style="flex:1">Herinnering op je telefoon als het tijd is om de kabel om te zetten</span><button class="tg${s.remind ? " on" : ""}" id="rem" role="switch" aria-checked="${s.remind}" aria-label="herinnering"></button></div>`;
    } else if (id === "house") {
      const ch = (k, v) => `<button class="chip${s[k] === v ? " on" : ""}" data-hk="${k}" data-v="${v}">${v}</button>`;
      body = `<h3>Je huis</h3>
        <div><div class="lbl">huisaansluiting: aantal fasen</div><div class="chips">${["1 fase", "3 fasen", "Weet ik niet"].map((v) => ch("phase", v)).join("")}</div></div>
        ${s.phase && s.phase !== "Weet ik niet" ? `<div><div class="lbl">ampère per fase</div><div class="chips">${(s.phase === "3 fasen" ? ["16", "20", "25", "35", "40", "63"] : ["25", "35", "40", "50", "63"]).map((v) => `<button class="chip${s.famp === v ? " on" : ""}" data-hk="famp" data-v="${v}">${v} A</button>`).join("")}<input class="name amp" data-famp type="number" min="6" max="250" placeholder="zelf" value="${(s.phase === "3 fasen" ? ["16", "20", "25", "35", "40", "63"] : ["25", "35", "40", "50", "63"]).includes(s.famp) ? "" : s.famp}" style="width:80px"></div></div>` : ""}
        <div><div class="lbl">heb je een load balancer die het huisverbruik meeneemt?</div><div class="chips">${["Ja", "Nee", "Weet ik niet"].map((v) => ch("lb", v)).join("")}</div><p class="sub">Bijvoorbeeld Wallbox Power Boost, of een laadpaal die via de slimme meter meekijkt.</p></div>
        <div><div class="lbl">heb je zonnepanelen?</div><div class="chips">${opt2("sun")}</div></div>
        <div><div class="lbl">heb je dynamische energieprijzen?</div><div class="chips">${opt2("dyn")}</div></div>
        <p class="sub"><span class="note">HESC houdt hiermee het laden binnen de aansluiting als comfort. Jij blijft verantwoordelijk dat je elektrische installatie niet overbelast raakt; dat regelen laadpaal, load balancer en installateur.</span></p>`;
      ok = !!s.phase && (s.phase === "Weet ik niet" || !!s.famp) && !!s.lb && !!s.sun && !!s.dyn;
    } else if (id === "car") {
      body = `<h3>${s.cars === 2 ? "Je auto's" : "Je auto"}</h3><p class="sub">De naam komt uit Home Assistant; pas hem aan als je wilt.</p>`
        + Array.from({ length: s.cars || 1 }, (_, j) => {
          const c = s.car[j], v = (c.kwh - 10) / 140 * 100;
          return `<div class="car"><h4><i style="background:${colors[j]}"></i>Auto ${j + 1}</h4>
            <div><div class="lbl">naam</div><input class="name" data-nm="${j}" value="${c.name}"></div>
            <div><div class="lbl">accucapaciteit</div><div class="sl" style="--cc:${colors[j]}"><input type="range" min="10" max="150" step="1" value="${c.kwh}" data-kw="${j}" style="--v:${v}%"><output>${c.kwh} kWh</output></div><p class="sub">Staat in de specificaties van je auto.</p></div></div>`;
        }).join("");
    } else if (id === "found") {
      const miss = (k) => suFind(this._hass, k).length !== 1; // exactly one found = taken, nothing to ask
      const parts = [];
      Array.from({ length: nCh }, (_, j) => { if (!suChargers(this._hass)[s.ctype[j]]) parts.push(this._chargerFound(s.ctype[j])); });
      Array.from({ length: s.cars || 1 }, (_, j) => { if (miss("soc")) parts.push(suPick(`soc${j}`, `Accustand van ${s.car[j].name}`, "het accu-% van deze auto geeft", suFind(this._hass, "soc"), s.pick[`soc${j}`],
        "Geen: HESC schat het zelf. Je kunt de accustand ook zelf invullen op de startpagina of je telefoon.")); });
      if (s.sun === "ja" && miss("pv")) parts.push(suPick("pv", "Zonnestroom nu", "het totale vermogen van je panelen geeft", suFind(this._hass, "pv"), s.pick.pv, "geen sensor voor zonnevermogen gevonden"));
      if (s.sun === "ja" && miss("forecast")) parts.push(suPick("forecast", "Zonverwachting", "de verwachting geeft (Solcast of Forecast.Solar)", suFind(this._hass, "forecast"), s.pick.forecast, "geen zonverwachting gevonden"));
      if (miss("grid")) parts.push(suPick("grid", "Netvermogen nu", "afname en teruglevering van het hele huis meet", suFind(this._hass, "grid"), s.pick.grid, "geen netmeter gevonden (bijv. P1 / DSMR / HomeWizard)"));
      if (this._hass && this._hass.states["input_boolean.hpvc_enabled"]) parts.push(`<div><div class="lbl">HPVC gevonden. HPVC regelt je zonnepanelen bij negatieve prijzen. Zal HESC daarmee samenwerken?</div><div class="chips">${["Ja", "Nee, HESC werkt op zichzelf"].map((v) => `<button class="chip${(s.hpvc || "Ja") === v ? " on" : ""}" data-hk="hpvc" data-v="${v}">${v}</button>`).join("")}</div></div>`);
      body = `<h3>HESC heeft gezocht</h3><p class="sub">${parts.length ? "Dit kon HESC niet (zeker) vinden. Kies het zelf; de rest is al ingevuld." : "✓ Alles gevonden. Dit scherm wordt in het echt overgeslagen."}</p>${parts.join("")}`;
    } else if (id === "prices") {
      body = `<h3>Waar komen je prijzen vandaan?</h3><p class="sub">Een ✓ betekent dat HESC die bron in Home Assistant vond.</p>${this._priceStep()}`;
    } else {
      const names = s.car.slice(0, s.cars || 1).map((c) => `${c.name} (${c.kwh} kWh)`).join(" · ");
      body = `<h3>Klaar! HESC v4 gaat aan de slag.</h3><p class="sub">HESC start in <b>schaduwmodus</b>: het kijkt mee en schakelt niets. Zet hem aan op de startpagina als je zover bent. Alles kun je later wijzigen bij Instellingen.</p>
        <dl class="sum"><dt>Auto's</dt><dd>${names}</dd><dt>Laadpalen</dt><dd>${Array.from({ length: nCh }, (_, j) => s.ctype[j]).join(" · ")}${s.cars === 2 && nCh === 1 ? " · om de beurt" : ""}</dd>
        ${s.cars === 2 && nCh === 1 ? `<dt>Wisselen</dt><dd>kabel om uiterlijk ${s.swap}${s.remind ? " · met herinnering" : ""}</dd>` : ""}
        <dt>Huis</dt><dd>${s.phase === "Weet ik niet" || !s.phase ? "aansluiting onbekend" : `${s.phase[0]}×${s.famp} A`} · load balancer: ${(s.lb || "-").toLowerCase()} · max. laadpaal ${Array.from({ length: nCh }, (_, j) => `${s.amp[j]} A`).join(" / ")}</dd>
        <dt>Zon</dt><dd>${s.sun === "ja" ? "ja, met verwachting" : "nee"}</dd><dt>Prijzen</dt><dd>${s.dyn === "ja" ? `dynamisch · ${s.src}` : "vast"}</dd></dl>`;
    }
    this.shadowRoot.innerHTML = `<style>${SUCSS}</style><ha-card>
      <div class="prog">${steps.map((_, k) => `<i class="${k <= this._i ? "on" : ""}"></i>`).join("")}</div>
      <div class="step">Eerste start · stap ${this._i + 1} van ${steps.length} · voorbeeld, er wordt niets opgeslagen</div>
      ${body}
      <div class="nav">${this._i > 0 ? `<button class="btn" id="prev">‹ Terug</button>` : ""}<span style="flex:1"></span>
        ${last ? `<button class="btn" id="more">Meer instellen</button><button class="btn pri" id="fin">Klaar</button>` : `<button class="btn pri" id="next" ${ok ? "" : "disabled"}>Volgende ›</button>`}</div>
    </ha-card>`;
    this._wire();
  }

  _wire() {
    const r = this.shadowRoot, s = this._s, re = () => this._render();
    r.querySelectorAll("[data-k]").forEach((b) => b.addEventListener("click", () => {
      const k = b.dataset.k, v = isNaN(+b.dataset.v) ? b.dataset.v : +b.dataset.v;
      s[k] = v; if (k === "cars" && v === 1) s.chargers = 1;
      if (k === "how") { s.cars = v === "een" ? 1 : 2; s.chargers = v === "2x2" ? 2 : 1; }
      re();
    }));
    r.querySelectorAll("[data-ct]").forEach((b) => b.addEventListener("click", () => { s.ctype[+b.dataset.ct] = b.dataset.v; re(); }));
    r.querySelectorAll("[data-amp]").forEach((b) => b.addEventListener("click", () => { const j = +b.dataset.amp; s.amp[j] = Math.max(6, Math.min(32, s.amp[j] + +b.dataset.dir)); re(); }));
    r.querySelectorAll("[data-hk]").forEach((b) => b.addEventListener("click", () => { s[b.dataset.hk] = b.dataset.v; re(); }));
    r.querySelectorAll("[data-famp]").forEach((i) => i.addEventListener("change", () => { s.famp = i.value ? String(Math.round(+i.value)) : ""; re(); }));
    r.querySelectorAll("[data-first]").forEach((b) => b.addEventListener("click", () => { s.first = +b.dataset.first; re(); }));
    r.querySelectorAll("[data-sw]").forEach((b) => b.addEventListener("click", () => { s.swap = plStep(s.swap, +b.dataset.sw); re(); }));
    if (r.getElementById("rem")) r.getElementById("rem").addEventListener("click", () => { s.remind = !s.remind; re(); });
    r.querySelectorAll("[data-src]").forEach((b) => b.addEventListener("click", () => { s.src = b.dataset.src; delete s.pick.price; re(); }));
    r.querySelectorAll("[data-pick]").forEach((el) => el.addEventListener("change", () => { s.pick[el.dataset.pick] = el.value; }));
    r.querySelectorAll("[data-nm]").forEach((i) => i.addEventListener("change", () => { s.car[+i.dataset.nm].name = i.value.trim() || s.car[+i.dataset.nm].name; }));
    r.querySelectorAll("[data-kw]").forEach((i) => {
      i.addEventListener("input", () => { i.style.setProperty("--v", `${(i.value - 10) / 140 * 100}%`); i.nextElementSibling.textContent = `${i.value} kWh`; });
      i.addEventListener("change", () => { s.car[+i.dataset.kw].kwh = +i.value; });
    });
    const go = (d) => { this._i += d; re(); };
    if (r.getElementById("next")) r.getElementById("next").addEventListener("click", () => go(1));
    if (r.getElementById("prev")) r.getElementById("prev").addEventListener("click", () => go(-1));
    if (r.getElementById("fin")) r.getElementById("fin").addEventListener("click", () => { this._i = 0; window.dispatchEvent(new CustomEvent("hesc-v4-close")); }); // decision 01-11 12:58: a clear way to finish
    if (r.getElementById("more")) r.getElementById("more").addEventListener("click", () => window.dispatchEvent(new CustomEvent("hesc-v4-open", { detail: { id: this._config.more || "settings" } })));
  }
}

for (const C of [HescV4Buttons, HescV4Setup, HescV4Fields, HescV4Plan, HescV4Planning]) {
  const set = C.prototype.setConfig;
  C.prototype.setConfig = function (c) { this.__raw = c; this.__tok = hv4Known(); return set.call(this, hv4Tokens(c)); };
  // decision 08-11-2026 11:48: right after a restart the car name is not there yet (EV1); fill it in once it is
  const hd = Object.getOwnPropertyDescriptor(C.prototype, "hass");
  if (hd && hd.set) Object.defineProperty(C.prototype, "hass", { configurable: true, get: hd.get, set(h) { if (this.__raw && !this.__tok && hv4Known()) { this.__tok = true; set.call(this, hv4Tokens(this.__raw)); this._sig = undefined; } hd.set.call(this, h); } });
}
customElements.define("hesc-v4p-buttons", HescV4Buttons);
customElements.define("hesc-v4p-setup", HescV4Setup);
customElements.define("hesc-v4p-fields", HescV4Fields);
customElements.define("hesc-v4p-plan", HescV4Plan);
customElements.define("hesc-v4p-planning", HescV4Planning);
/* Overview "vandaag en morgen" in the Batterijplan layout (decision 06-11-2026 17:48 "E"; two cars 19:17 "F"): key figures,
 * one chart (price steps, sun, each car's battery level and goal in its own colour), one charge bar per car, hover. */
const OV_CARS = ["ev1", "ev2"];
class HescV4Overview extends HTMLElement {
  setConfig(c) { this._config = c || {}; }
  _cars(st) { return OV_CARS.filter((c) => st[`sensor.hesc_v4_${c}_charge_plan`]); }
  set hass(h) {
    this._hass = h;
    const st = h.states, ids = ["sensor.hesc_v4_prices"];
    this._cars(st).forEach((c) => ids.push(`sensor.hesc_v4_${c}_charge_plan`, `sensor.hesc_v4_${c}_expected_charge_cost`, `sensor.hesc_v4_${c}_ev_battery_level_with_fallbacks`, `select.hesc_v4_${c}_colour`));
    const sig = ids.map((id) => (st[id] || {}).last_updated).join("|") + Math.floor(Date.now() / 300000) + "|" + Math.round(this.getBoundingClientRect().width) + "|" + (window.__hv4OneCharger ? 1 : 0);
    if (!this._ro && window.ResizeObserver) { this._ro = new ResizeObserver(() => { if (this._hass) this.hass = this._hass; }); this._ro.observe(this); }
    if (sig === this._sig) return;
    this._sig = sig; this._render();
  }
  /* Letter on the left (decision 07-11-2026 18:14): per car when and how it charges, battery levels and costs, which charger,
   * and with two cars on one charger the earliest time to swap the cable. */
  _brief(cars, st, now) {
    const hm = (t) => new Date(t).toLocaleTimeString(hv4Loc(), { hour: "2-digit", minute: "2-digit" });
    const day = (t) => { const d = new Date(t), a = new Date(now); a.setHours(0, 0, 0, 0); const k = Math.round((new Date(t).setHours(0, 0, 0, 0) - a) / 86400000); return k === 0 ? (d.getHours() < 18 ? "vandaag" : "vanavond") : k === 1 ? (d.getHours() < 6 ? "vannacht" : "morgen") : d.toLocaleDateString(hv4Loc(), { weekday: "long" }); };
    const sess = (c) => { const out = []; c.q.filter(([t]) => t + 900000 > now).forEach(([t, k]) => { const l = out[out.length - 1]; if (l && l.k === k && t - l.e <= 900000) l.e = t + 900000; else out.push({ s: t, e: t + 900000, k }); }); return out; };
    const nm = (c) => `<b style="color:${c.col}">${c.name}</b>`, demo = false;
    const box = (c) => c.plan.charger || ((st["sensor.hesc_v4_setup"] || {}).attributes || {}).hesc_charger_type || "je laadpaal";
    // decision 07-11-2026 23:05: the Prijzen window is gone; its warning lives here
    const noPrices = ((st["binary_sensor.hesc_v4_prices_available"] || {}).state) === "off";
    let html = noPrices ? `<p style="color:#ff9800;font-weight:600">Geen prijzen ontvangen: HESC kan nu niet plannen op prijs.</p>` : "";
    html += demo && cars.length > 1 ? `<div class="sw"><button data-ch="2" class="${window.__hv4OneCharger ? "" : "on"}">2 laadpalen</button><button data-ch="1" class="${window.__hv4OneCharger ? "on" : ""}">1 laadpaal</button></div>` : "";
    // the plug-in reminder the user set in the planning window (decision 08-11-2026 15:53)
    const rem = (c) => { const on = ((st[`switch.hesc_v4_${c.car}_reminder_plug_in_the_car`] || {}).state) === "on", at = ((st[`select.hesc_v4_${c.car}_reminder_plug_in_the_car_at`] || {}).state) || "";
      return on && /^\d\d:\d\d$/.test(at) ? ` Om ${at} krijg je een herinnering op je telefoon.` : ""; };
    cars.forEach((c) => {
      const ss = sess(c), conn = ((st[`binary_sensor.hesc_v4_${c.car}_ev_connected`] || {}).state) === "on", dl = Date.parse(c.plan.deadline || "");
      // group per day word and source: "vannacht van 01:45 tot 02:00, van 03:00 tot 03:15 en van 04:45 tot 05:00 van het net"
      const and = (xs) => xs.length > 1 ? xs.slice(0, -1).join(", ") + " en " + xs[xs.length - 1] : xs[0] || "";
      const grp = []; ss.forEach((x) => { const d = day(x.s), l = grp[grp.length - 1]; if (l && l.d === d && l.k === x.k) l.t.push(x); else grp.push({ d, k: x.k, t: [x] }); });
      const parts = grp.map((g) => `${g.d} ${and(g.t.map((x) => `van ${hm(x.s)} tot ${hm(x.e)}`))} ${g.k === "sun" ? "op zon" : "van het net"}`);
      const list = grp.length > 1 ? parts.slice(0, -1).join(", ") + ", daarna " + parts[parts.length - 1] : parts[0];
      html += `<h3>${nm(c)} <span class="note">· ${box(c)}</span></h3><p>`
        + (ss.length ? `Laadt ${list}. ` : "Er is geen laden gepland. ")
        + `De accu gaat van ${c.soc != null ? Math.round(c.soc) + "%" : "onbekend"} naar ${c.plan.goal ?? "–"}%${Number.isFinite(dl) ? `, klaar ${day(dl)} om ${hm(dl)}` : ""}. `
        + `Verwachte kosten ${c.costTxt || "–"}${+c.plan.grid_kwh ? ` voor ± ${(+c.plan.grid_kwh).toLocaleString(hv4Loc(), { maximumFractionDigits: 1 })} kWh van het net` : ""}${ss.some((x) => x.k === "sun") ? ", de rest gratis op zon" : ""}. `
        + (+((st[`sensor.hesc_v4_${c.car}_ev_charging_power`] || {}).state) > 400 ? `<b style="color:${c.col}">Laadt nu met ${(+st[`sensor.hesc_v4_${c.car}_ev_charging_power`].state / 1000).toLocaleString(hv4Loc(), { maximumFractionDigits: 1 })} kW.</b> ` : "") + (conn ? "Hij is aangesloten." : ss.length ? `Hij is nog niet aangesloten: steek de kabel erin vóór ${hm(ss[0].s)}.${rem(c)}` : "Hij is niet aangesloten.") + "</p>";
    });
    const shared = cars.length > 1 && (demo ? !!window.__hv4OneCharger : box(cars[0]) === box(cars[1]));
    if (shared) {
      const all = cars.flatMap((c) => c.q.filter(([t]) => t + 900000 > now).map(([t]) => ({ t, c }))).sort((a, b) => a.t - b.t), sw = [];
      all.forEach((x, i) => { const p = all[i - 1]; if (p && p.c !== x.c) sw.push({ from: p.c, to: x.c, at: p.t + 900000, by: x.t }); });
      html += `<h3>Kabel wisselen</h3><p>` + (sw.length ? sw.map((w) => `${day(w.at)} op zijn vroegst om <b>${hm(w.at)}</b> van ${nm(w.from)} naar ${nm(w.to)}${w.by > w.at ? ` (uiterlijk ${hm(w.by)})` : ""}.`).join("<br>") : "Niet nodig: er laadt maar één auto.") + "</p>";
    } else if (cars.length > 1) html += `<p class="note">Kabel wisselen is niet nodig: elke auto heeft een eigen laadpaal.</p>`;
    return html + (demo ? `<p class="note">Voorbeeld: de auto's en laadtijden zijn verzonnen, prijzen en zon zijn echt.</p>` : "");
  }
  _car(car) {
    const st = this._hass.states, su = (st["sensor.hesc_v4_setup"] || {}).attributes || {};
    let plan = {}; try { plan = JSON.parse(((st[`sensor.hesc_v4_${car}_charge_plan`] || {}).attributes || {}).plan || "{}"); } catch (e) { plan = {}; }
    const socS = st[`sensor.hesc_v4_${car}_ev_battery_level_with_fallbacks`] || (car === "ev1" ? st[su.hesc_ev_soc_sensor] : null) || {};
    const soc = Number.isFinite(+socS.state) ? +socS.state : (plan.soc ?? null);
    const cost = st[`sensor.hesc_v4_${car}_expected_charge_cost`] || {};
    const name = ((st[`text.hesc_v4_${car}_car_name`] || {}).state || "").trim() || car.toUpperCase();
    const col = ((st[`select.hesc_v4_${car}_colour`] || {}).attributes || {}).hex || (car === "ev1" ? "#3fc8f4" : "#ff8a65");
    const q = [...(plan.planned || []).map((x) => [Date.parse(x), "grid"]), ...(plan.planned_forecast || []).map((x) => [Date.parse(x), "sun"])].sort((a, b) => a[0] - b[0]);
    return { car, plan, soc, cost: +cost.state || 0, costTxt: Number.isFinite(parseFloat(cost.state)) ? `€ ${(+cost.state).toLocaleString(hv4Loc(), { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : (cost.attributes || {}).display, cap: +((st[`number.hesc_v4_${car}_ev_usable_battery_capacity`] || {}).state) || 60, name, col, q, kw: +plan.kw || 11 };
  }
  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const st = this._hass.states, su = (st["sensor.hesc_v4_setup"] || {}).attributes || {}, cars = this._cars(st).map((c) => this._car(c));
    const pa = (st["sensor.hesc_v4_prices"] || {}).attributes || {};
    const prices = [].concat(pa.raw_today || [], pa.tomorrow_valid === false ? [] : (pa.raw_tomorrow || [])).map((p) => ({ t: Date.parse(p.start), e: Date.parse(p.end), ct: p.value * 100 }));
    const sunD = [];
    [su.hesc_solar_today_sensor, su.hesc_solar_tomorrow_sensor].forEach((id) => ((id && st[id] && st[id].attributes.detailedForecast) || []).forEach((x) => sunD.push({ t: Date.parse(x.period_start), kw: +(x[su.hesc_forecast_attribute || "pv_estimate"] ?? x.pv_estimate) || 0 })));
    const hostW = Math.round(this.getBoundingClientRect().width) || 1200, wide = hostW >= 900, W = Math.max(320, Math.round(wide ? (hostW - 36 - 20) * 2 / 3 : hostW - 36));
    const n = cars.length, now = Date.now(), t0 = now - 15 * 60000, t1 = t0 + 24 * 3600000, L = 44, R = W - 44, T = 16, B = Math.round(Math.min(300, Math.max(170, W * 0.3))), BAR = 12, H = B + 14 + (n + 1) * BAR + 34;
    const X = (t) => L + ((t - t0) / (t1 - t0)) * (R - L);
    const vis = prices.filter((p) => p.e > t0 && p.t < t1), maxCt = Math.max(40, ...vis.map((p) => p.ct));
    const Yp = (v) => B - (Math.max(0, v) / maxCt) * (B - T), Yc = (v) => B - (v / 100) * (B - T);
    const maxKw = Math.max(1, ...sunD.map((s) => s.kw)), Ys = (v) => B - (v / maxKw) * (B - T) * 0.75;
    let price = ""; vis.forEach((p, i) => { const y = Yp(p.ct).toFixed(1); price += `${i ? "L" : "M"}${X(Math.max(p.t, t0)).toFixed(1)} ${y} L${X(Math.min(p.e, t1)).toFixed(1)} ${y} `; });
    const sp = sunD.filter((s) => s.t >= t0 - 1800000 && s.t <= t1);
    const sun = sp.length ? `M${X(Math.max(sp[0].t, t0)).toFixed(1)} ${B} ` + sp.map((s) => `L${X(Math.min(Math.max(s.t, t0), t1)).toFixed(1)} ${Ys(s.kw).toFixed(1)}`).join(" ") + ` L${X(Math.min(sp[sp.length - 1].t, t1)).toFixed(1)} ${B} Z` : "";
    // battery level per car: flat, rising during each planned quarter (kw x 0.25 h of the usable capacity) — an estimate
    cars.forEach((c, ci) => {
      let lvl = c.soc ?? 0, path = `M${X(t0).toFixed(1)} ${Yc(lvl).toFixed(1)}`; c.lv = [];
      c.q.forEach(([t, k]) => { if (t + 900000 < t0) return; path += ` L${X(Math.max(t, t0)).toFixed(1)} ${Yc(lvl).toFixed(1)}`;
        // a sun quarter adds what the sun forecast gives then, not the charger's full power (decision 08-11-2026 15:53: fade out once full)
        const s = k === "sun" ? sunD.find((x) => x.t <= t + 450000 && x.t + 1800000 > t + 450000) : null, kw = k === "sun" ? Math.min(c.kw, s ? s.kw : 0) : c.kw;
        if (c.full != null) return; lvl = Math.min(c.plan.goal != null ? Math.max(c.plan.goal, c.soc ?? 0) : 100, lvl + (kw * 0.25 / c.cap) * 100); c.lv.push([t + 900000, lvl]);
        if (c.plan.goal != null && lvl >= c.plan.goal) c.full = t + 900000; path += ` L${X(Math.min(t + 900000, t1)).toFixed(1)} ${Yc(lvl).toFixed(1)}`; });
      c.path = path + ` L${R} ${Yc(lvl).toFixed(1)}`;
      const y = B + 12 + ci * BAR;
      c.bar = `<text x="${L - 6}" y="${y + 9}" class="ax" text-anchor="end" style="fill:${c.col}">${n > 1 ? c.name.split(" ")[0] : "auto"}</text><rect x="${L}" y="${y}" width="${R - L}" height="${BAR - 3}" rx="2" fill="var(--divider-color)" fill-opacity=".5"></rect>`
        + c.q.filter(([t]) => t + 900000 > t0 && t < t1).map(([t, k]) => `<rect x="${X(Math.max(t, t0)).toFixed(1)}" y="${y}" width="${(X(t + 900000) - X(t)).toFixed(1)}" height="${BAR - 3}" rx="2" fill="${k === "sun" ? "#f5c542" : "#4a7dff"}"></rect>`).join("");
    });
    const ticks = []; { const h0 = new Date(t0); h0.setMinutes(h0.getMinutes() < 30 ? 30 : 60, 0, 0); for (let t = +h0; t < t1; t += 1800000) { const full = new Date(t).getMinutes() === 0; ticks.push(`<line x1="${X(t)}" x2="${X(t)}" y1="${T}" y2="${B}" class="gl${full ? "" : " gh"}"></line>` + (full ? `<text x="${X(t)}" y="${H - 4}" class="ax" text-anchor="middle">${new Date(t).toLocaleTimeString(hv4Loc(), { hour: "2-digit", minute: "2-digit" })}</text>` : "")); } }
    const fmt = (v, d = 1) => (v ?? 0).toLocaleString(hv4Loc(), { minimumFractionDigits: d, maximumFractionDigits: d });
    const eur = (v) => "€ " + fmt(v, 2);
    const pNow = (prices.find((p) => p.t <= now && p.e > now) || {}).ct;
    const gridKwh = cars.reduce((a, c) => a + (+c.plan.grid_kwh || 0), 0), gridCt = cars.reduce((a, c) => a + (+c.plan.grid_kwh || 0) * (+c.plan.avg_price_ct || 0), 0);
    const avg = gridKwh ? gridCt / gridKwh : (cars[0] && cars[0].plan.avg_price_ct);
    const hid = (window.__hv4Hide = window.__hv4Hide || {}), title = cars.map((c) => `<button class="ct${hid[c.car] ? " off" : ""}" data-tg="${c.car}" style="color:${c.col}" aria-pressed="${!hid[c.car]}" title="Aan/uit in de grafiek">${c.name}</button>`).join(" + ") || "HESC";
    const costMid = n > 1
      ? `<div class="big" style="color:#f5c542">${eur(cars.reduce((a, c) => a + c.cost, 0))}</div><div class="lb">Verwachte laadkosten samen</div><div class="sm">${cars.map((c) => `<span style="color:${c.col}">${c.costTxt || eur(c.cost)}</span>`).join(" · ")}</div>`
      : `<div class="big" style="color:#f5c542">${(cars[0] && cars[0].costTxt) || "–"}</div><div class="lb">Verwachte laadkosten</div>`;
    const right = n > 1
      ? cars.map((c) => `<div class="mbig"><span style="color:${c.col}">${c.soc != null ? Math.round(c.soc) : "–"}</span> <small>→ ${c.plan.goal ?? "–"}%${c.plan.deadline_text ? " " + c.plan.deadline_text : ""}</small></div>`).join("") + `<div class="lb">Accu nu → doel</div>`
      : cars.map((c) => `<div class="big" style="color:${c.col}">${c.soc != null ? Math.round(c.soc) : "–"} <small>%</small></div><div class="lb">Accu nu${c.plan.goal != null ? " · doel " + c.plan.goal + "%" : ""}</div>`).join("");
    const one = cars[0] || {};
    this.shadowRoot.innerHTML = `<style>
:host{display:block}.c{position:relative;padding:16px 18px;color:var(--primary-text-color)}
h2{margin:0 0 8px;font-size:16px;font-weight:600}.k{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.box{border:1px solid var(--divider-color);border-radius:8px;padding:8px 12px}.big{font-size:26px;line-height:1.1}.big small,.mbig small{font-size:12px;color:var(--secondary-text-color)}.mbig{font-size:20px;line-height:1.2}
.lb{font-size:12px;color:var(--secondary-text-color);text-decoration:underline dotted}.sm{font-size:11px;color:var(--secondary-text-color)}
.mid{text-align:center}.rt{text-align:right}svg{width:100%;height:auto;display:block}.ct{font:inherit;font-weight:600;background:none;border:0;padding:0;cursor:pointer}.ct.off{opacity:.35;text-decoration:line-through}${cars.filter((c) => hid[c.car]).map((c) => `svg [data-car="${c.car}"]{display:none}`).join("")}.grid{display:grid;gap:20px}.grid.w{grid-template-columns:minmax(0,1fr) minmax(0,2fr);align-items:start}.brief{font-size:14px;line-height:1.6}.brief p{margin:0 0 10px}.brief h3{margin:0 0 6px;font-size:14px;font-weight:600}.brief .sw{display:inline-flex;gap:4px;margin-bottom:10px}.brief .sw button{font:inherit;font-size:12px;padding:2px 10px;border-radius:12px;border:1px solid var(--divider-color);background:none;color:var(--secondary-text-color);cursor:pointer}.brief .sw button.on{color:var(--primary-text-color);border-color:var(--primary-text-color)}.brief .note{font-size:12px;color:var(--secondary-text-color)}.gl{stroke:var(--divider-color);stroke-opacity:.7;stroke-dasharray:2 4}.gh{stroke-opacity:.3}.pl{transform-box:fill-box;transform-origin:center;animation:hv4pl 2s ease-out infinite}@keyframes hv4pl{0%{transform:scale(1);opacity:.7}100%{transform:scale(3);opacity:0}}.ax{fill:var(--secondary-text-color);font-size:11px}
.lg{display:flex;flex-wrap:wrap;gap:14px;font-size:12px;color:var(--secondary-text-color);margin-top:4px}.lg i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px}.lg i.ln{height:3px;width:14px;vertical-align:3px}
.tip{position:absolute;pointer-events:none;z-index:2;display:none;padding:8px 10px;font-size:11px;background:var(--card-background-color);border:1px solid var(--divider-color);border-radius:6px;width:max-content;line-height:1.5}.tip span{color:var(--secondary-text-color)}
</style><ha-card><div class="c">
<h2>${title} · vandaag en morgen</h2>
<div class="grid${wide ? " w" : ""}"><div class="brief">${this._brief(cars, st, now)}</div><div class="chart">
<div class="k"><div class="box"><div class="big">${avg != null ? fmt(avg) : "–"} <small>ct</small></div><div class="lb">Gemiddelde laadprijs</div><div class="sm">${gridKwh ? fmt(gridKwh) + " kWh van het net" + (n > 1 ? " samen" : "") : "geen netladen gepland"}${n === 1 && one.plan && one.plan.deadline_text ? " · klaar " + one.plan.deadline_text : ""}${pNow != null ? " · nu " + fmt(pNow) + " ct" : ""}</div></div>
<div class="mid">${costMid}</div><div class="rt">${right}</div></div>
<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Prijs, zonverwachting en accustand van ${cars.map((c) => c.name).join(" en ")} voor de komende 24 uur">
${ticks.join("")}
<text x="${L - 6}" y="${T + 4}" class="ax" text-anchor="end">${Math.round(maxCt)} ct</text><text x="${L - 6}" y="${B + 4}" class="ax" text-anchor="end">0</text>
<text x="${R + 4}" y="${T + 4}" class="ax">100%</text><text x="${R + 4}" y="${B + 4}" class="ax">0%</text>
${sun ? `<path d="${sun}" fill="#f5c542" fill-opacity=".35" stroke="#f5c542" stroke-width="1.5"></path>` : ""}
<path d="${price}" fill="none" stroke="var(--secondary-text-color)" stroke-width="1.3"></path>
<defs>${cars.map((c) => { /* decision 06-11 20:07: plugged in = solid line; not plugged in = hidden, fades in 1 h before charging, stays until the ready time (expected unplug), then fades out */
  const conn = ((st[`binary_sensor.hesc_v4_${c.car}_ev_connected`] || {}).state) === "on", F = 3600000, ses = [], dl = Date.parse(c.plan.deadline || "");
  c.q.map(([t]) => t).filter((t) => t + 900000 > t0 && t < t1).forEach((t) => { const l = ses[ses.length - 1]; if (l && t - l[1] <= 2 * 3600000) l[1] = t + 900000; else ses.push([t, t + 900000]); });
  const off = (t) => Math.min(1, Math.max(0, (X(Math.min(Math.max(t, t0), t1)) - L) / (R - L))).toFixed(4), stp = (t, o) => `<stop offset="${off(t)}" stop-color="${c.col}" stop-opacity="${o}"></stop>`;
  let g = conn || !ses.length ? stp(t0, conn ? 1 : 0.18) : stp(t0, 0);
  if (conn && ses.length) { const e = Math.min(ses[ses.length - 1][1], c.full ?? Infinity); g += stp(e, 1) + stp(e + F, 0); } /* decision 07-11 18:29: plugged in, fully charged by plan -> fade out */
  /* decision 08-11-2026 15:55: with the plug-in reminder on, the car fades in during the half hour before the reminder (that is when it gets plugged in) */
  const ra = (() => { const on = ((st[`switch.hesc_v4_${c.car}_reminder_plug_in_the_car`] || {}).state) === "on", m = /^(\d\d):(\d\d)$/.exec(((st[`select.hesc_v4_${c.car}_reminder_plug_in_the_car_at`] || {}).state) || ""); if (!on || !m) return null; const d = new Date(now); d.setHours(+m[1], +m[2], 0, 0); if (+d <= now) d.setDate(d.getDate() + 1); return +d; })();
  if (!conn) ses.forEach(([a, b], i) => { const nx = ses[i + 1], end = Number.isFinite(dl) && dl > b && (!nx || dl < nx[0]) ? dl : b, r = i === 0 && ra && ra < a && a - ra < 12 * F ? ra : null; g += (r ? stp(r - 1800000, 0) + stp(r, 1) : stp(a - F, 0) + stp(a, 1)) + stp(end, 1) + stp(end + (end === b ? F : 1800000), 0); });
  return `<linearGradient id="fl-${c.car}" gradientUnits="userSpaceOnUse" x1="${L}" y1="0" x2="${R}" y2="0">${g}</linearGradient>`; }).join("")}${cars.map((c) => `<linearGradient id="fg-${c.car}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.col}" stop-opacity=".55"></stop><stop offset="1" stop-color="${c.col}" stop-opacity="0"></stop></linearGradient>`).join("")}</defs>${cars.map((c) => `<g data-car="${c.car}">` + c.lv.map(([te, lv]) => { const ts = te - 900000; if (te <= t0 || ts >= t1) return ""; const x = X(Math.max(ts, t0)), y = Yc(lv); return `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${(X(Math.min(te, t1)) - x).toFixed(1)}" height="${(B - y).toFixed(1)}" fill="url(#fg-${c.car})"></rect>`; }).join("") + "</g>").join("")}
${cars.map((c) => `<g data-car="${c.car}"><path d="${c.path}" fill="none" stroke="url(#fl-${c.car})" stroke-width="2.5"></path>${c.plan.goal != null ? `<line x1="${L}" x2="${R}" y1="${Yc(c.plan.goal)}" y2="${Yc(c.plan.goal)}" stroke="${c.col}" stroke-dasharray="5 5" stroke-opacity=".7"></line>` : ""}</g>`).join("")}
${cars.map((c) => `<g data-car="${c.car}">${c.bar}</g>`).join("")}${(() => { /* fixed row: sun above the start level (top half, yellow), price at or below the cheap-chance price (bottom half, purple) */
  const y = B + 12 + n * BAR, h = (BAR - 3) / 2, demo = false, sunW = demo ? 0.5 : (+((st["number.hesc_v4_charger1_forecast_power_to_start"] || {}).state) / 1000 || 1.45), lim = demo ? ([...vis].sort((a, b) => a.ct - b.ct)[Math.floor(vis.length / 4)] || { ct: 0 }).ct / 100 : +((st["number.hesc_v4_charge_plan_opportunity_price"] || {}).state); /* demo: sun from 0.5 kW, cheap = the cheapest quarter of the 24 h (decision 06-11 20:05 "zet het eens in de proef") */
  const sunB = sunD.filter((s) => s.kw >= sunW && s.t + 1800000 > t0 && s.t < t1).map((s) => `<rect x="${X(Math.max(s.t, t0)).toFixed(1)}" y="${y}" width="${(X(Math.min(s.t + 1800000, t1)) - X(Math.max(s.t, t0))).toFixed(1)}" height="${h}" fill="#f5c542"><title>zon boven de startdrempel</title></rect>`).join("");
  const chB = Number.isFinite(lim) ? vis.filter((p) => p.ct <= lim * 100).map((p) => `<rect x="${X(Math.max(p.t, t0)).toFixed(1)}" y="${(y + h).toFixed(1)}" width="${(X(Math.min(p.e, t1)) - X(Math.max(p.t, t0))).toFixed(1)}" height="${h}" fill="#b388ff"><title>prijs onder je goedkope-kansprijs</title></rect>`).join("") : "";
  return `<text x="${L - 6}" y="${y + 9}" class="ax" text-anchor="end">zon/€</text><rect x="${L}" y="${y}" width="${R - L}" height="${BAR - 3}" rx="2" fill="var(--divider-color)" fill-opacity=".5"></rect>${sunB}${chB}`; })()}
<line x1="${X(now)}" x2="${X(now)}" y1="${T - 2}" y2="${B + 12 + n * BAR}" stroke="#03a9f4" stroke-width="2"></line><rect x="${X(now) - 14}" y="0" width="28" height="14" rx="3" fill="#03a9f4"></rect><text x="${X(now)}" y="10.5" font-size="9" font-weight="700" fill="#06121a" text-anchor="middle">Nu</text>
${cars.map((c, i) => { const pw = +((st[`sensor.hesc_v4_${c.car}_ev_charging_power`] || {}).state), thr = +((st["number.hesc_v4_charger1_ev_charging_threshold"] || {}).state) || 400; if (!(pw > thr) || c.soc == null) return ""; const x = X(now), y = Yc(c.soc); return `<g data-car="${c.car}"><circle cx="${x}" cy="${y}" r="6" fill="${c.col}" class="pl"></circle><circle cx="${x}" cy="${y}" r="5" fill="${c.col}" stroke="var(--card-background-color)" stroke-width="1.5"></circle><text x="${x + 10}" y="${y + (i ? 14 : -8)}" font-size="11" font-weight="600" fill="${c.col}">⚡ laadt nu ${(pw / 1000).toLocaleString(hv4Loc(), { maximumFractionDigits: 1 })} kW</text></g>`; }).join("")}
<line id="hl" x1="0" x2="0" y1="${T}" y2="${B + 12 + n * BAR}" stroke="var(--primary-text-color)" stroke-opacity=".5" visibility="hidden"></line>
</svg><div class="tip" id="tip"></div>
<div class="lg"><span><i style="background:#f5c542"></i>zon verwachting</span>${cars.map((c) => `<span><i class="ln" style="background:${c.col}"></i>accu ${c.name}</span>`).join("")}<span><i class="ln" style="background:var(--secondary-text-color);height:2px"></i>prijs (ct)</span><span><i style="background:#4a7dff"></i>laden van het net</span><span><i style="background:#f5c542"></i>laden op zon</span><span><i style="background:linear-gradient(#f5c542 50%,#b388ff 50%)"></i>zon genoeg · prijs onder je goedkope-kansprijs</span></div></div></div>
</div></ha-card>`;
    this.shadowRoot.querySelectorAll("[data-tg]").forEach((b) => b.addEventListener("click", () => { const h = window.__hv4Hide; h[b.dataset.tg] = !h[b.dataset.tg]; this._render(); }));
    this.shadowRoot.querySelectorAll("[data-ch]").forEach((b) => b.addEventListener("click", () => { window.__hv4OneCharger = b.dataset.ch === "1"; window.dispatchEvent(new CustomEvent("hesc-v4-demo")); }));
    const svg = this.shadowRoot.querySelector("svg"), tip = this.shadowRoot.getElementById("tip"), hl = this.shadowRoot.getElementById("hl");
    const hide = () => { tip.style.display = "none"; hl.setAttribute("visibility", "hidden"); };
    svg.addEventListener("pointerleave", hide);
    svg.addEventListener("pointermove", (e) => {
      const r = svg.getBoundingClientRect(), vx = ((e.clientX - r.left) / r.width) * W;
      if (vx < L || vx > R) return hide();
      const t = t0 + ((vx - L) / (R - L)) * (t1 - t0), qs = Math.floor(t / 900000) * 900000;
      const p = prices.find((x) => x.t <= t && x.e > t), s = sunD.reduce((a, x) => (Math.abs(x.t - t) < Math.abs((a || { t: 1e15 }).t - t) ? x : a), null);
      const dt = new Date(qs), when = dt.toLocaleDateString(hv4Loc(), { weekday: "short" }) + " " + dt.toLocaleTimeString(hv4Loc(), { hour: "2-digit", minute: "2-digit" });
      const planned = cars.some((c) => c.q.some(([qt]) => qt === qs));
      const lines = cars.map((c) => {
        const k = c.q.find(([qt]) => qt === qs), lvAt = (c.lv.filter(([lt]) => lt <= t).pop() || [0, c.soc])[1];
        const who = n > 1 ? `<b style="color:${c.col}">${c.name}</b> ` : "";
        return k ? `${who}${n > 1 ? "laadt" : "auto laadt"} · ${fmt(c.kw, 0)} kW ${k[1] === "sun" ? "op zon" : "van het net"}${lvAt != null ? (n > 1 ? " · accu " : "<br>accu ") + Math.round(lvAt) + "%" : ""}`
          : (lvAt != null ? `${who}${n > 1 ? "accu " : "accu "}${Math.round(lvAt)}%` : "");
      }).filter(Boolean).join("<br>");
      tip.innerHTML = `<b>${when}</b> <span>(${qs + 900000 <= now ? "voorbij" : planned ? "gepland" : "verwacht"})</span><br>${p ? `kale prijs ${fmt(p.ct)} ct<br>` : ""}${s && s.kw > 0.005 && Math.abs(s.t - t) < 3600000 ? `zon ${fmt(s.kw, 2)} kW<br>` : ""}${lines}`;
      const c = this.shadowRoot.querySelector(".c").getBoundingClientRect(), px = e.clientX - c.left;
      tip.style.display = "block";
      tip.style.left = (px + 14 + tip.offsetWidth > c.width ? px - tip.offsetWidth - 14 : px + 14) + "px";
      tip.style.top = (e.clientY - c.top + 12) + "px";
      hl.setAttribute("x1", vx); hl.setAttribute("x2", vx); hl.setAttribute("visibility", "visible");
    });
  }
  getCardSize() { return 6; }
}
customElements.define("hesc-v4p-overview", HescV4Overview);

/* ---------- the planning windows on HESC's real rhythm (decision 07-11-2026 19:53 "rekenwerk dit gelijk oplossen") ----------
 * The rekenchat's step 4 (v4/alpha fbd4bb3): the rhythm is the repeating-plan entities, "only this time", the calendar and
 * the vacation are HESC actions, and sensor.hesc_v4_evN_coming_week tells what HESC really does in the next 7 days.
 * The sketch's state object stays the same shape; it is now read from Home Assistant, and every change made in the window
 * is turned into the matching action (a diff against what was read). In the panel the sketch key "ev2" is HESC's EV1. */
const PLR_WD = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];
const plrCar = (ev) => (ev === "ev2" ? "ev1" : ev === "ev1" ? "ev2" : ev);
const plrHass = () => window.__hv4Hass;
const plrHas = (ev) => { const h = plrHass(); return !!(h && h.states[`select.hesc_v4_${plrCar(ev)}_repeating_plan_time`]); };
const plSketchState = plState, plSketchDay = plDay;
function plrRead(ev) {
  const h = plrHass(), car = plrCar(ev), p = `hesc_v4_${car}_repeating_plan`, st = (id) => (h.states[id] || {}).state;
  const master = st(`switch.${p}`) === "on", pct = (v) => (v && v !== "Standard" ? parseInt(v, 10) : undefined);
  const std = { time: st(`select.${p}_time`) || "07:00", pct: pct(st(`select.${p}_goal`)) || 75 };
  const week = PLR_WD.map((d) => {
    const t = st(`select.${p}_${d}_time`);
    return { on: master && st(`switch.${p}_${d}`) === "on", time: t && t !== "Standard" ? t : undefined, pct: pct(st(`select.${p}_${d}_goal`)) };
  });
  const cw = h.states[`sensor.hesc_v4_${car}_coming_week`], pl = (cw && cw.attributes.planning) || {}, cal = {};
  (pl.off || []).forEach((k) => { cal[k] = { on: false }; });
  (pl.extra || []).forEach((k) => { const o = (pl.own || {})[k] || {}; cal[k] = { on: true, ...(o.time ? { time: o.time } : {}), ...(o.goal != null ? { pct: o.goal } : {}) }; });
  const o = pl.once, now = st(`select.hesc_v4_${car}_charge_now_to`);
  const once = now && now !== "Off" ? { kind: "now", pct: parseInt(now, 10) }
    : o ? (o.skip ? { kind: "skip", date: o.date } : { kind: "other", date: o.date, time: o.time || std.time, pct: o.goal || std.pct }) : null;
  return { real: true, car, std, week, cal, once, vac: pl.vacation ? { from: pl.vacation.from, to: pl.vacation.to || "9999-12-31" } : null, days: (cw && cw.attributes.days) || [] };
}
plState = function (ev) { return plrHas(ev) ? plrRead(ev) : plSketchState(ev); }; // eslint-disable-line no-func-assign
plDay = function (s, d) { // eslint-disable-line no-func-assign
  if (s && s.real) { // the coming week as HESC computed it; further ahead the rhythm and calendar as stored
    const k = plKey(d), x = s.days.find((y) => y.date === k);
    if (x) {
      if (x.kind === "vacation") return { on: false, src: "vac" };
      if (x.kind === "off") return { on: false, src: "off" };
      if (x.kind === "none" || !x.time) return x.kind === "skipped" ? plSketchDay({ ...s, once: null }, d) : { on: false, src: "" };
      if (x.kind === "skipped" || x.kind === "once") return plSketchDay({ ...s, once: null }, d); // shown as "deze keer" / "slaat over" by the window
      return { on: true, time: x.time, pct: x.goal, src: x.kind === "extra" ? "add" : x.own ? "own" : "week" };
    }
  }
  return plSketchDay(s, d);
};
{
  const P = HescV4Plan.prototype, render0 = P._render, cfg0 = P.setConfig;
  const call = (h, svc, data) => h.callService("hesc_v4", svc, data).catch((e) => window.dispatchEvent(new CustomEvent("hass-notification", { detail: { message: `HESC: ${(e && e.message) || e}` } })));
  const sel = (h, id, option) => h.callService("select", "select_option", { entity_id: id, option });
  const sw = (h, id, on) => h.callService("switch", on ? "turn_on" : "turn_off", { entity_id: id });
  P.setConfig = function (c) { cfg0.call(this, c); this._snap = this._s && this._s.real ? JSON.stringify(this._s) : null; };
  Object.defineProperty(P, "hass", { configurable: true, set(h) {
    this._hass = h; window.__hv4Hass = h;
    const ev = (this._config || {}).ev || "ev1";
    if (!plrHas(ev)) return;
    const car = plrCar(ev), sig = Object.keys(h.states).filter((k) => k.includes(`hesc_v4_${car}_repeating_plan`) || k === `sensor.hesc_v4_${car}_coming_week` || k === `select.hesc_v4_${car}_charge_now_to`).map((k) => h.states[k].last_updated).join("|");
    if (sig === this._rsig) return;
    this._rsig = sig; this._s = plrRead(ev); this._snap = JSON.stringify(this._s); render0.call(this); plChanged();
  } });
  // every change in the window: compare with what was read from HESC and send the matching actions
  P._render = function () {
    const s = this._s, h = this._hass;
    if (s && s.real && h && this._snap) {
      const was = JSON.parse(this._snap), p = `hesc_v4_${s.car}_repeating_plan`, car = s.car, k0 = (o) => JSON.stringify(o || null);
      if (s.std.time !== was.std.time) sel(h, `select.${p}_time`, s.std.time);
      if (s.std.pct !== was.std.pct) sel(h, `select.${p}_goal`, `${s.std.pct}%`);
      s.week.forEach((w, i) => {
        const v = was.week[i], d = PLR_WD[i];
        if (w.on !== v.on) sw(h, `switch.${p}_${d}`, w.on);
        if (w.time !== v.time) sel(h, `select.${p}_${d}_time`, w.time || "Standard");
        if (w.pct !== v.pct) sel(h, `select.${p}_${d}_goal`, w.pct ? `${w.pct}%` : "Standard");
      });
      const anyOn = s.week.some((w) => w.on), master = (h.states[`switch.${p}`] || {}).state === "on";
      if (anyOn && !master) sw(h, `switch.${p}`, true);
      if (!anyOn && master && s.week.some((w, i) => w.on !== was.week[i].on)) sw(h, `switch.${p}`, false);
      if (k0(s.once) !== k0(was.once)) {
        const o = s.once, wasNow = was.once && was.once.kind === "now";
        if (wasNow && (!o || o.kind !== "now")) sel(h, `select.hesc_v4_${car}_charge_now_to`, "Off");
        if (!o) { if (was.once && !wasNow) call(h, "only_this_time_clear", { car }); }
        else if (o.kind === "now") this._nowAsk = o.pct; // fail-safe (decision 08-11-2026 09:39): only after Start + confirmation
        else {
          const nx = plNext({ ...s, once: null }), date = o.date || (nx ? plKey(nx.d) : null);
          if (date) call(h, "only_this_time", o.kind === "skip" ? { car, date, skip: true } : { car, date, time: o.time, goal: o.pct });
        }
      }
      const keys = new Set([...Object.keys(s.cal), ...Object.keys(was.cal)]);
      keys.forEach((k) => {
        const a = s.cal[k], b = was.cal[k];
        if (k0(a) === k0(b)) return;
        call(h, "calendar_day", { car, date: k, what: !a ? "rhythm" : a.on ? "extra" : "off",
          ...(a && a.on && a.time ? { time: a.time } : {}), ...(a && a.on && a.pct != null ? { goal: a.pct } : {}) });
      });
      if (k0(s.vac) !== k0(was.vac)) {
        if (s.vac) call(h, "vacation", { car, start: s.vac.from, end: s.vac.to === "9999-12-31" ? null : s.vac.to });
        else call(h, "vacation_stop", { car });
      }
      const keep = this._nowAsk !== undefined ? { ...s, once: was.once } : s; // a "now" not yet confirmed stays a difference
      this._snap = JSON.stringify(keep); // optimistic; HESC's answer arrives through hass and is read again
    }
    const out = render0.call(this);
    if (this._nowAsk !== undefined && s && s.real && this.shadowRoot) {
      const box = document.createElement("div"), pct = this._nowAsk, me = this;
      box.innerHTML = `<div style="margin:10px 0;border:1px solid #ef5350;border-radius:10px;padding:10px 12px;background:rgba(239,83,80,.08);font-size:13px;line-height:1.5">
        <b style="display:block;margin-bottom:4px">Nu laden tot ${pct}%?</b>HESC laadt de auto dan meteen van het net, ook als stroom nu duur is of er geen zon is, tot de accu op dit doel staat. Je planning wacht zolang. Stoppen kan altijd.
        <label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input type="checkbox" data-nsure> Ja, ik wil nu laden</label>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:8px"><button class="btn" data-nno>Annuleren</button><button class="btn" data-nyes disabled style="opacity:.4">Start</button></div></div>`;
      const host = this.shadowRoot.querySelector("ha-card") || this.shadowRoot;
      host.insertBefore(box, host.firstChild ? host.firstChild.nextSibling : null);
      const yes = box.querySelector("[data-nyes]");
      box.querySelector("[data-nsure]").addEventListener("change", (e) => { yes.disabled = !e.target.checked; yes.style.opacity = e.target.checked ? "" : ".4"; });
      box.querySelector("[data-nno]").addEventListener("click", () => { me._nowAsk = undefined; me._s = JSON.parse(me._snap); render0.call(me); });
      yes.addEventListener("click", () => { if (yes.disabled) return; sel(h, `select.hesc_v4_${s.car}_charge_now_to`, `${pct}%`); me._nowAsk = undefined; me._snap = JSON.stringify(s); render0.call(me); });
    }
    return out;
  };
}
{
  const PP = HescV4Planning.prototype, d = Object.getOwnPropertyDescriptor(PP, "hass");
  if (d && d.set) Object.defineProperty(PP, "hass", { configurable: true, set(h) { window.__hv4Hass = h; d.set.call(this, h); const sig = Object.keys(h.states).filter((k) => /^sensor\.hesc_v4_ev\d_coming_week$/.test(k)).map((k) => h.states[k].last_updated).join("|"); if (sig !== this._cwsig) { this._cwsig = sig; if (this._mode) this._mode(); if (this._week) this._week(); } } });
}
// Komende week: one row per car HESC has (the second row only when there is a second car)
HescV4Planning.prototype._mode = function () {
  const w = this.shadowRoot && this.shadowRoot.querySelector(".wrap"), h = window.__hv4Hass;
  if (w) w.classList.toggle("one", !(h && h.states["select.hesc_v4_ev2_repeating_plan_time"]));
};

/* ---------- Instellingen › "Auto's en laadpalen" (decision 08-11-2026 08:43, design in the postbus) ----------
 * Per car and per charger: name, colour, which charger. HESC can remove only car 2 and charger 2 (rekenchat 9c97238):
 * car 1 and charger 1 stay. Removing first asks HESC what would happen (check_only) and shows that in a red box that
 * needs a confirmation. "+ Auto" opens the first start in add mode; "+ Laadpaal" (car 2 sharing charger 1) opens it in
 * charger mode. */
const CARS_ERR = { only_ev2: "Alleen auto 2 kan weg; auto 1 blijft.", unknown_car: "Deze auto kent HESC niet.",
  only_charger2: "Alleen laadpaal 2 kan weg; laadpaal 1 blijft.", unknown_charger: "Deze laadpaal kent HESC niet." };
class HescV4Cars extends HTMLElement {
  setConfig(c) { this._config = c || {}; }
  getCardSize() { return 3; }
  disconnectedCallback() { if (this._pop) { this._pop.remove(); this._pop = null; this._adding = undefined; this._addEl = null; } }
  set hass(h) {
    this._hass = h;
    const sig = ["ev1", "ev2"].map((k) => ["text", "select"].map((d) => ((h.states[`${d}.hesc_v4_${k}_${d === "text" ? "car_name" : "colour"}`] || {}).state)).join("/")
      + (((h.states[`sensor.hesc_v4_${k}_charge_plan`] || {}).attributes || {}).plan || "").slice(0, 60)).join("|")
      + ["charger1", "charger2"].map((c) => (h.states[`select.hesc_v4_${c}_charger_type`] || {}).state).join("/");
    if (this._addEl) this._addEl.hass = h;
    if (sig === this._sig && this.shadowRoot) return;
    this._sig = sig; this._render();
  }
  _cars() {
    const st = this._hass.states, out = [];
    ["ev1", "ev2"].forEach((k) => {
      const n = st[`text.hesc_v4_${k}_car_name`];
      if (!n) return;
      let charger = "", cid = "";
      try { const pl = JSON.parse(((st[`sensor.hesc_v4_${k}_charge_plan`] || {}).attributes || {}).plan || "{}"); charger = pl.charger || ""; cid = pl.charger_id || ""; } catch (e) { /* no plan yet */ }
      if (!cid) cid = k === "ev2" && st["select.hesc_v4_charger2_charger_type"] ? "charger2" : "charger1";
      const brand = (st[`select.hesc_v4_${cid}_charger_type`] || {}).state || charger || ((st["sensor.hesc_v4_setup"] || {}).attributes || {}).hesc_charger_type || "";
      out.push({ k, cid, name: n.state, col: ((st[`select.hesc_v4_${k}_colour`] || {}).attributes || {}).hex || "#9aa0aa", charger: brand });
    });
    return out;
  }
  _chargers() {
    const st = this._hass.states, cars = this._cars();
    return ["charger1", "charger2"].filter((c) => c === "charger1" || st[`select.hesc_v4_${c}_charger_type`] || cars.some((x) => x.cid === c))
      .map((c) => ({ id: c, n: c.slice(-1), name: (st[`select.hesc_v4_${c}_charger_type`] || {}).state || (cars.find((x) => x.cid === c) || {}).charger || "laadpaal",
        cars: cars.filter((x) => x.cid === c).map((x) => x.name) }));
  }
  async _check(kind, id) { // what HESC would do; shown before anything is removed
    const type = kind === "car" ? "hesc_v4/setup/remove_car" : "hesc_v4/setup/remove_charger";
    try { this._pre = await this._hass.callWS({ type, [kind]: id, check_only: true }); }
    catch (e) { this._pre = { ok: false, error: /unknown_command|Unknown command/i.test(String((e && (e.code || e.message)) || e)) ? "old" : (e && e.message) || String(e) }; }
    this._render();
  }
  _preText(kind, x) {
    const p = this._pre;
    if (!p) return "HESC kijkt wat er weg zou gaan…";
    if (!p.ok) return p.error === "old" ? "Deze HESC-versie kan nog niets weghalen." : (CARS_ERR[p.error] || `Kan niet: ${p.error}`);
    const n = (p.entities || []).length;
    if (kind === "car") return `Planning, laadkosten en instellingen van ${x.name} verdwijnen uit HESC${p.charger_removed ? `, en laadpaal ${p.charger_removed.slice(-1)} gaat mee` : ""}. ${n} entiteit${n === 1 ? "" : "en"} in Home Assistant ${n === 1 ? "verdwijnt" : "verdwijnen"}. ${(p.files_kept || []).length ? "De bestanden van deze auto blijven bewaard (hernoemd), niets wordt gewist." : ""} Je andere auto merkt er niets van.`;
    const mv = p.cars_moved_to_charger1 || [];
    const names = mv.map((k) => (this._cars().find((c) => c.k === k) || { name: k }).name);
    return `HESC stuurt laadpaal ${x.n} (${x.name}) dan niet meer en zijn instellingen verdwijnen. ${names.length ? `${names.join(" en ")} laadt daarna op laadpaal 1, samen met de andere auto.` : ""} ${n} entiteit${n === 1 ? "" : "en"} in Home Assistant ${n === 1 ? "verdwijnt" : "verdwijnen"}.`;
  }
  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const cars = this._cars(), chs = this._chargers(), ask = this._ask, msg = this._msg || "";
    const shared2 = cars.length === 2 && cars.every((c) => c.cid === "charger1");
    const delBtn = (attr, id, can) => (can ? `<button class="del" ${attr}="${id}">Verwijderen</button>` : `<span class="sub" title="HESC houdt auto 1 en laadpaal 1 altijd">vast</span>`);
    const box = (kind, x, id) => `<div class="ask"><b>${kind === "car" ? `${x.name} verwijderen?` : `Laadpaal ${x.n} (${x.name}) verwijderen?`}</b>${this._preText(kind, x)}
          <label style="display:flex;gap:8px;align-items:center;margin-top:8px"><input type="checkbox" data-sure ${this._pre && this._pre.ok ? "" : "disabled"}> Ja, ik wil ${kind === "car" ? x.name : `laadpaal ${x.n}`} verwijderen</label>
          <div class="row"><button data-cancel>Annuleren</button><button class="del" data-yes="${kind}:${id}" ${this._sure ? "" : "disabled style=\"opacity:.4\""}>Verwijderen</button></div></div>`;
    this.shadowRoot.innerHTML = `<style>${INFO_CSS}
      :host{display:block}ha-card{padding:14px 16px}h2{margin:0 0 10px;font-size:16px;font-weight:600}
      .car{display:grid;grid-template-columns:auto 1fr auto;gap:4px 12px;align-items:center;padding:8px 0;border-top:1px solid var(--divider-color)}
      .dot{width:12px;height:12px;border-radius:50%}.nm{font-weight:600}.sub{font-size:12px;color:var(--secondary-text-color)}
      button{font:inherit;font-size:13px;border-radius:14px;padding:5px 12px;cursor:pointer;background:none;color:var(--primary-text-color);border:1px solid var(--divider-color)}
      button.add{border-color:var(--primary-color);color:var(--primary-color);margin-top:10px}button.del{border-color:#ef5350;color:#ef5350}
      .ask{margin:8px 0;border:1px solid #ef5350;border-radius:10px;padding:10px 12px;background:rgba(239,83,80,.08);font-size:13px;line-height:1.5}
      .ask b{display:block;margin-bottom:4px}.row{display:flex;gap:8px;justify-content:flex-end;margin-top:8px;align-items:center}
      .msg{font-size:12px;margin-top:6px;color:var(--secondary-text-color)}</style>
      <ha-card><h2 style="display:flex;align-items:center">Auto's en laadpalen${(this._config || {}).info ? `<button class="ib" data-info aria-label="Uitleg" aria-expanded="${!!this._tip}" style="margin-left:auto">i</button>` : ""}</h2>
      ${(this._config || {}).info ? `<div class="tip" ${this._tip ? "" : "hidden"}>${infoHtml(this._config.info)}</div>` : ""}
      ${cars.map((c) => `<div class="car"><span class="dot" style="background:${c.col}"></span>
        <div><div class="nm">${c.name}</div><div class="sub">${c.k === "ev1" ? "auto 1" : "auto 2"} · laadpaal ${c.cid.slice(-1)}${c.charger ? ` (${c.charger})` : ""}</div></div>
        ${delBtn("data-del", c.k, c.k === "ev2")}</div>${ask === `car:${c.k}` ? box("car", c, c.k) : ""}`).join("")}
      ${cars.length >= 2 ? `<div class="sub" style="margin-top:8px">HESC stuurt maximaal twee auto's.</div>` : `<button class="add" data-add>+ Auto toevoegen</button>`}
      <h2 style="margin-top:16px">Laadpalen</h2>
      ${chs.map((g) => `<div class="car"><span class="dot" style="background:var(--secondary-text-color)"></span>
        <div><div class="nm">${g.name}</div><div class="sub">laadpaal ${g.n}${g.cars.length ? " · " + g.cars.join(" en ") : " · geen auto"}</div></div>
        ${delBtn("data-delc", g.id, g.id === "charger2")}</div>${ask === `charger:${g.id}` ? box("charger", g, g.id) : ""}`).join("")}
      ${chs.length >= 2 ? `<div class="sub" style="margin-top:8px">HESC stuurt maximaal twee laadpalen.</div>`
        : shared2 ? `<button class="add" data-addc>+ Laadpaal toevoegen</button><div class="sub">Voor ${cars[1].name}, die nu laadpaal 1 deelt.</div>`
        : `<div class="sub" style="margin-top:8px">Een tweede laadpaal hoort bij een tweede auto: kies bij "+ Auto toevoegen" voor een eigen laadpaal.</div>`}
      ${msg ? `<div class="msg">${msg}</div>` : ""}</ha-card>`;
    if (!this._wl) { this._wl = true; window.addEventListener("hesc-v4-close", () => { if (!this._adding) return; this._adding = undefined; this._addEl = null; this._render(); }); }
    this.shadowRoot.querySelectorAll("[data-info]").forEach((b) => b.addEventListener("click", () => { this._tip = !this._tip; const t = this.shadowRoot.querySelector(".tip"); if (t) t.hidden = !this._tip; b.setAttribute("aria-expanded", String(this._tip)); }));
    const r = this.shadowRoot, open = (key, kind, id) => { this._ask = this._ask === key ? undefined : key; this._sure = false; this._msg = ""; this._pre = null; this._render(); if (this._ask) this._check(kind, id); };
    r.querySelectorAll("[data-del]").forEach((b) => b.addEventListener("click", () => open(`car:${b.dataset.del}`, "car", b.dataset.del)));
    r.querySelectorAll("[data-delc]").forEach((b) => b.addEventListener("click", () => open(`charger:${b.dataset.delc}`, "charger", b.dataset.delc)));
    r.querySelectorAll("[data-cancel]").forEach((b) => b.addEventListener("click", () => { this._ask = undefined; this._render(); }));
    r.querySelectorAll("[data-sure]").forEach((b) => { b.checked = !!this._sure; b.addEventListener("change", () => { this._sure = b.checked; this._render(); }); });
    r.querySelectorAll("[data-yes]").forEach((b) => b.addEventListener("click", async () => {
      if (!this._sure) return;
      const [kind, id] = b.dataset.yes.split(":");
      try {
        const res = await this._hass.callWS({ type: kind === "car" ? "hesc_v4/setup/remove_car" : "hesc_v4/setup/remove_charger", [kind]: id });
        this._msg = res && res.ok ? "Verwijderd. HESC laadt zich opnieuw." : `Niet gelukt: ${CARS_ERR[(res || {}).error] || (res || {}).error}`;
      } catch (e) { this._msg = `Niet gelukt: ${(e && e.message) || e}`; }
      this._ask = undefined; this._sure = false; this._render();
    }));
    const adder = (mode) => () => { this._adding = mode; this._msg = ""; this._addEl = null; this._render(); };
    r.querySelectorAll("[data-add]").forEach((b) => b.addEventListener("click", adder("car")));
    r.querySelectorAll("[data-addc]").forEach((b) => b.addEventListener("click", adder("charger")));
    // decision 08-11-2026 11:03: adding opens in a pop-up over the page, not squeezed into this column
    if (this._adding) {
      if (!this._pop) {
        const pop = this._pop = document.createElement("div");
        pop.style.cssText = "position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:40px 16px";
        pop.innerHTML = `<div style="position:relative;width:min(760px,100%);background:var(--card-background-color,#1f2128);border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.5)"><button data-x aria-label="Sluiten" style="position:absolute;top:10px;right:12px;z-index:2;font:inherit;font-size:18px;background:none;border:0;color:var(--primary-text-color);cursor:pointer">✕</button><div data-body></div></div>`;
        pop.addEventListener("click", (e) => { if (e.target === pop || e.target.closest("[data-x]")) { this._adding = undefined; this._addEl = null; this._render(); } });
        document.body.appendChild(pop);
      }
      if (!this._addEl) {
        this._addEl = document.createElement("hesc-v4-first-start");
        if (this._addEl.setConfig) this._addEl.setConfig({ add: this._adding === "charger" ? "charger" : true });
        this._pop.querySelector("[data-body]").replaceChildren(this._addEl);
      }
      this._addEl.hass = this._hass;
    } else if (this._pop) { this._pop.remove(); this._pop = null; }
  }
}
customElements.define("hesc-v4p-cars", HescV4Cars);

/* ---------- a settings block as a tile that opens in a pop-up (decision 08-11-2026 11:12, first in Standaard) ----------
 * Config: {type: custom:hesc-v4p-tile, title, tag?, color?, facts?: [{entity, attribute?, name?}], card: <the block>}.
 * The tile shows the title, a green tick or an orange "n ontbreekt" (setup choices in the block that are empty) and a
 * few facts; a tap opens the block itself in a pop-up over the page. */
class HescV4Tile extends HTMLElement {
  setConfig(c) { this._config = c || {}; }
  getCardSize() { return 2; }
  disconnectedCallback() { this._close(); }
  set hass(h) {
    this._hass = h;
    if (this._inner) this._inner.hass = h;
    if (this._inl) { this._inl.hass = h; this._flat(); }
    const sig = this._sum().join("|");
    if (sig === this._sig && this.shadowRoot) return;
    this._sig = sig; this._render();
  }
  _flat() { requestAnimationFrame(() => { const hc = this._inl && this._inl.shadowRoot && this._inl.shadowRoot.querySelector("ha-card"); if (hc) hc.style.cssText += ";background:none;box-shadow:none;border:0;border-top:1px solid var(--divider-color);border-radius:0"; }); }
  _isIn(r) { const m = (this._config || {}).inline || []; return m.includes(r.entity) || (r.attribute && m.includes(r.attribute)); }
  _strip(card) { // the block without the rows that are shown on the tile itself
    if (!card) return card;
    if (card.cards) return { ...card, cards: card.cards.map((x) => this._strip(x)) };
    if (card.card) return { ...card, card: this._strip(card.card) };
    return card.rows ? { ...card, rows: card.rows.filter((r) => !this._isIn(r)) } : card;
  }
  _ftype(card) { if (!card) return null; if (card.cards) { for (const x of card.cards) { const t = this._ftype(x); if (t) return t; } return null; } if (card.card) return this._ftype(card.card); return card.rows ? card.type : null; }
  _rows(card) { // every row of the fields cards inside (also in stacks)
    if (!card) return [];
    if (card.cards) return card.cards.flatMap((x) => this._rows(x));
    if (card.card) return this._rows(card.card);
    return card.rows || [];
  }
  _sum() {
    const h = this._hass, c = this._config || {}, out = [];
    if (!h) return out;
    let miss = 0, have = 0;
    this._rows(c.card).forEach((r) => {
      if (r.type !== "attribute" || r.optional) return;
      const st = h.states[r.entity]; if (!st) return;
      const v = st.attributes[r.attribute];
      if (v === undefined || v === null || v === "") miss += 1; else have += 1;
    });
    out.push(miss ? `<span class="warn">⚠ ${miss} ontbreekt</span>` : `<span class="ok">✓${have ? ` ${have} gekozen` : " in orde"}</span>`);
    (c.facts || []).forEach((f) => {
      const st = h.states[f.entity]; if (!st) return;
      let v = f.attribute ? st.attributes[f.attribute] : st.state;
      if (v === undefined || v === null || v === "") return;
      if (v === "on") v = "aan"; else if (v === "off") v = "uit";
      const t = typeof v === "string" && /^[a-z_]+\.[a-z0-9_]+$/.test(v) && h.states[v];
      if (t) v = t.attributes.friendly_name || v;
      const u = !f.attribute && st.attributes.unit_of_measurement ? ` ${st.attributes.unit_of_measurement}` : "";
      out.push(`${f.name ? `${f.name} ` : ""}<b>${v}${u}</b>`);
    });
    return out;
  }
  _render() {
    if (!this.shadowRoot) this.attachShadow({ mode: "open" });
    const c = this._config || {};
    if (c.if_entity && this._hass && !this._hass.states[c.if_entity]) { this.shadowRoot.innerHTML = ""; this.style.display = "none"; return; }
    this.style.display = "";
    const tag = c.tag && !(/beide auto/.test(c.tag) && this._hass && !this._hass.states["text.hesc_v4_ev2_car_name"]) ? c.tag : "";
    this.shadowRoot.innerHTML = `<style>
      :host{display:block}ha-card{padding:14px 16px;cursor:pointer;transition:background .15s}ha-card:hover{background:color-mix(in srgb,var(--primary-color) 6%,var(--ha-card-background,var(--card-background-color)))}
      h4{margin:0;display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600}.tag{margin-left:auto;font-size:11px;font-weight:500;border:1px solid var(--divider-color);border-radius:999px;padding:2px 9px;color:var(--secondary-text-color);white-space:nowrap}
      .tag.car{border-color:var(--c);color:var(--c)}.go{color:var(--secondary-text-color);font-size:18px;line-height:1}
      .sum{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13px;color:var(--secondary-text-color)}.sum b{color:var(--primary-text-color);font-weight:500}
      .ok{color:#66bb6a}.warn{color:#ffb74d}</style>
      <ha-card style="--c:${c.color || "var(--primary-color)"}" role="button" tabindex="0" aria-label="${c.title || ""} openen"><h4>${c.title || ""}${tag ? `<span class="tag${c.color ? " car" : ""}">${tag}</span>` : `<span style="margin-left:auto"></span>`}<span class="go">›</span></h4>
      <div class="sum">${this._sum().join("")}</div><div class="inl"></div></ha-card>`;
    const card = this.shadowRoot.querySelector("ha-card");
    // decision 08-11-2026 11:21: some settings stay on the tile itself (they are changed often); the rest is in the pop-up
    const inRows = this._rows(c.card).filter((r) => this._isIn(r));
    if (inRows.length) {
      if (!this._inl) { const t = this._ftype(c.card); if (t) { this._inl = document.createElement(t.replace("custom:", "")); this._inl.setConfig({ type: t, rows: inRows, flat: true }); } }
      if (this._inl) { this._inl.style.cssText = "display:block;margin:8px -16px -14px;cursor:default"; this._inl.hass = this._hass; this.shadowRoot.querySelector(".inl").appendChild(this._inl); this._flat(); }
    }
    card.addEventListener("click", (e) => { if (e.composedPath().includes(this._inl)) return; this._open(); });
    card.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); this._open(); } });
  }
  async _open() {
    if (this._pop) return;
    const c = this._config || {}, pop = this._pop = document.createElement("div");
    pop.style.cssText = "position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:40px 16px";
    pop.innerHTML = `<div style="position:relative;width:min(560px,100%);background:var(--card-background-color,#1f2128);border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.5);padding:36px 6px 6px">
      <button data-x aria-label="Sluiten" style="position:absolute;top:10px;right:12px;z-index:2;font:inherit;font-size:18px;background:none;border:0;color:var(--primary-text-color);cursor:pointer">✕</button><div data-body></div></div>`;
    pop.addEventListener("click", (e) => { if (e.target === pop || e.target.closest("[data-x]")) this._close(); });
    this._esc = (e) => { if (e.key === "Escape") this._close(); };
    window.addEventListener("keydown", this._esc);
    document.body.appendChild(pop);
    const helpers = await window.loadCardHelpers();
    const el = this._inner = helpers.createCardElement(this._strip(c.card));
    el.hass = this._hass;
    pop.querySelector("[data-body]").appendChild(el);
  }
  _close() {
    if (this._pop) { this._pop.remove(); this._pop = null; this._inner = null; }
    if (this._esc) { window.removeEventListener("keydown", this._esc); this._esc = null; }
    this._sig = ""; if (this._hass) this.hass = this._hass;
  }
}
customElements.define("hesc-v4p-tile", HescV4Tile);
