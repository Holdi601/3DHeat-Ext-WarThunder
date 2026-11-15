---
title: "Vliegtuigen"
nav_order: 11
lang: "nl"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Vliegtuigen {#aircraft}

Voor lezers die willen weten waar de kolommen van vliegtuigen vandaan komen en hoe ver je ze kunt vertrouwen. Elke controle hieronder vergelijkt een waarde met iets dat de replay op een tweede, onafhankelijke manier zegt; alleen de methode en de overeenstemming worden gegeven.

## Cockpitinstrumenten {#cockpit-instruments}

Bericht 0xD04A stuurt de meters van de opnemende speler als paren (nummer, waarde): vier per seconde in arcadegevechten, alleen gewijzigde waarden in simulatorgevechten. De nummers vormen één lijst voor alle cockpits, en een cockpit stuurt de meters die zijn model heeft. De code van het spel bepaalt welk nummer welke meter is, dus elk nummer is benoemd naar wat het doet en gecontroleerd tegen de replay (`convert.INSTRUMENTS` bevat het resultaat; er wordt niets uit de installatie gelezen):

| Nummer | Naam | Gecontroleerd tegen |
|---|---|---|
| 0 | aangegeven vliegsnelheid, m/s | de snelheid van het spoor gecorrigeerd voor luchtdichtheid: correlatie 0,99 |
| 39 | klimsnelheid, m/s | de klimsnelheid van het spoor: correlatie boven 0,99 |
| 40, 41 | hoogte, m; hoogte modulo 1000 | de hoogte van het spoor, een paar meter verschil |
| 52, 53 | roll en pitch van de kunstmatige horizon | min de roll en pitch van de tabel, minder dan 1 graad verschil |
| 64 | kompas | de heading van de tabel, minder dan 0,1 graad verschil |
| 15-20 | roerpedalen | de zijwaartse kracht op het vliegtuig |
| 23, 31 | stuurknuppel: elevator en ailerons (teken zoals het cockpitmodel het heeft) | de aanvalshoek; de rolsnelheid |
| 69, 71, 73 | klok: uren (wijzerplaat van 12 uur), minuten, seconden | de lokale tijd van de opnamecomputer, tot de minuut |
| 75 | inlaatdruk, atm | hoger bij noodvermogen dan bij volle gas |
| 81-86, 87-92, 93-98 | toerental per motor, toerental modulo 1000, toerenmeter | elkaar exact; het toerental van de motor: correlatie boven 0,97 |
| 195 | brandstof | daalt tijdens een uitvlucht, weer vol bij een respawn |
| 228-230 | poten van het landingsgestel, 1 neer | neer alleen nabij de hoogte van vliegvelden en bij landingssnelheid |
| 240, 241 | gas per motor (1.1 noodvermogen of naverbrander) | de gas van de vluchtregel |
| 330-332, 346-348 | munitietellers (twee gelijke sets) | de rondes van de wapenpreset, dalend met de rondes van de vluchtregel |
| 135, 159 | olie- en cilinderkoptemperatuur | waarschijnlijk: ze stijgen tijdens een uitvlucht |
| 58, 61 | slipbal, draainaald | waarschijnlijk: ze volgen de zijwaartse kracht en de draaisnelheid |
| 223 | remklep | waarschijnlijk: alleen ingesteld bij de nadering |
| 490-497, 500-505 | wielremmen | waarschijnlijk: alleen ingesteld als je stilstaat op een vliegveld |

Er worden nog enkele nummers gestuurd waarvan de betekenis niet bekend is; die worden bewaard in `authorInstruments.notNamed` van het wedstrijddocument.

De `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` en `throttle` van de tabel komen hieruit, op de eigen rijen van de opnemende speler, waarbij het laatste bericht hoogstens 0,2 s na het sample wordt genomen.

## Vluchtregels {#flight-entries}

Elke vluchtregel van een vliegtuig (pakkettype 2) bevat, naast zijn positie en houding:

- **Snelheid**: een 32-bits woord na de houding. Bits 31, 30 en 29 zijn de tekens van x, y en z; daarna de snelheid in 11 bits van 500/2047 m/s (ze stopt bij 500 m/s), dan |x| en |y| als breuken van de snelheid in elk 9 bits, en z is wat de vector een eenheidsvector maakt. Gecontroleerd tegen de stap tussen ontvangen samples: de richting komt overeen binnen een fractie van een graad voor de opnemende speler en binnen ongeveer 2 graden voor iedereen anders; de snelheid binnen 0,2 %. `selfCheck.flightEntries`.
- **Rondes per wapen**: een lijst vóór de positie, één item per wapen, eerst de resterende rondes. Die van de opnemende speler is bij bijna elk sample gelijk aan de tellers van de cockpit één tik later.
- **Besturing en gas**: 7 bytes na de snelheid, gelezen als 14 nibbles. Voor de opnemende speler, elke tik: 1 de elevator, 2 de ailerons, 3 het roer (8 in rust), 11 het gas in zestiende (15 ook voor noodvermogen en naverbrander), 4 de wielremmen, 5 de remklep, 8 waarschijnlijk de remparachute. De nibbles van andere vliegtuigen veranderen maar een paar keer per gevecht en zijn op dat moment niet hun besturing.
- **Motoren**: per motor een statusbyte (0 uit; 1-6 starten; 7 draaiend; 8 dood), een waarde van 16 bits alleen met naverbrander (32767 vol), en een byte alleen nadat de motor getroffen was. De meeste vliegtuigen waarvan de motor "dood" gaat, worden vernietigd of eindigen binnen enkele minuten.

## Reflectiegegevens {#reflection-data}

De berichten 0xF02D en 0xF0AA repliceren de genummerde objecten van het spel: per object zijn id (de bovenste 5 bits de soort, de onderste 11 een index) en een veldtabel. Soort 14 zijn de spelersslots (veld 2 gebruikers-id en naam, 9 het team), soort 15 de teams (index 1 en 2):

- Veld 39 van een slot bevat zijn statistieken op vaste plaatsen: kills (offset 0), teamkills (2), doden (4), scheepskills (10), AI-kills (12), AI-grondkills (14), assists (20), veroveringszones (22), zoneschade (24, 32-bits), schadebeloning (40, 32-bits), ontweken raketten (50). Veld 38 begint met de score, veld 42 is de squad. Aan het eind van een gevecht is elke waarde voor elke speler gelijk aan die van de resultaten (`selfCheck.scoreboardVsResults`). Waar grondkills worden bijgehouden, is niet bekend.
- Veld 7 van een team is zijn score: aan het eind is die gelijk aan de som van de scores van zijn spelers in de resultaten. Veld 3 zijn waarschijnlijk zijn tickets.
- Elk bericht stuurt alleen de velden die veranderd zijn, dus `scoreboard` in het wedstrijddocument geeft bij elke wijziging de statistieken van elke speler en de score van elk team.

## Dead reckoning, en de smoother {#dead-reckoning-and-the-smoother}

Een clientreplay legt elk vliegtuig vier keer per seconde vast, zoals de client het tekende. Tussen de updates die hij ontvangt voor een verre vliegtuig, verplaatst de client het verder langs zijn laatste snelheid en draait hij het op zijn laatste draaisnelheden, en bij de volgende update springt hij het daarheen. Zo gelezen loopt een spoor recht, en springt dan. Niets in de vluchtregel markeert welke samples ontvangen zijn; een dead-reckoned sample wordt herkend aan wat het is: het zet de rechte lijn van de twee samples ervoor voort, in hun tempo, binnen 3 cm.

Hoeveel dit uitmaakt, hangt af van het gevecht: in arcadegevechten kan ongeveer de helft van de samples van andere vliegtuigen dead-reckoned zijn, in simulatorgevechten slechts enkele procenten. De smoother snijdt de stappen boven 15 g ongeveer vijf keer zo sterk af (`selfCheck.deadReckoning`). Het eigen vliegtuig van de opnemende speler wordt door de client niet geëxtrapoleerd en blijft zoals het is.

Standaard (`--no-smoothing` zet het uit) worden de sporen van alle eenheden behalve die van de opnemende speler zo geplaatst als de ontvangen toestanden zeggen dat ze waren: een dead-reckoned sample komt op een kromme door de ontvangen samples ervoor en erna, elk met hun eigen snelheid; over meer dan 3 s wordt de rechte lijn alleen gebogen richting het volgende ontvangen sample, zodat geen enkel sample verder beweegt dan de eigen sprong van de client. Zijn houding wordt gelijkmatig gedraaid van de ene ontvangen houding naar de volgende. Ontvangen samples worden hooguit 2 m of 0,04 s van hun snelheid gladgestreken; een gelijkmatige bocht blijft zoals hij is. De eigen waarden van de replay blijven in de `Raw`-kolommen.

## Houding, gecontroleerd {#attitude-checked}

Bij het eigen vliegtuig van de opnemende speler ligt de heading binnen een graad (mediaan) van de richting van de beweging, de pitch binnen enkele graden van de klimhoek, en in duidelijke bochten heeft de roll bij bijna elk sample het teken van de bocht: de roll van het vluchtmodel is linkervleugel omlaag positief, en de tabel zet hem om naar rechtervleugel omlaag positief (`selfCheck.aircraftAttitude`). De hoeken van 10 bits stappen 0,18 graad. De houding van grondeenheden wordt gecontroleerd aan hun schoten ([Torens](ground.md#turrets)).

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
