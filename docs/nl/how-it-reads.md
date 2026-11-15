---
title: "Hoe het een replay leest"
nav_order: 10
lang: "nl"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Hoe het een replay leest {#how-it-reads-a-replay}

Deze pagina is voor mensen die willen weten wat de converter leest, hoe het gecontroleerd is, en dus hoe ver je elke kolom kunt vertrouwen. Je hebt haar niet nodig om replays om te zetten.

De lezing is gecontroleerd op clientreplays van arcade-luchtgevechten, luchtsimulatorgevechten en zeegevechten, op serverreplays van grondgevechten, en, voor de indelingen van 2025, op de openbare voorbeeldreplays van
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Elke controle vergelijkt een waarde met iets dat de replay op een tweede, onafhankelijke manier zegt; hier worden alleen de methode en de overeenstemming gegeven.

## Wat er gelezen wordt, en de controle {#what-is-read-and-the-check}

| Onderdeel | Status, en de controle |
|---|---|
| Kop, kaart, missie, starttijd, sessie; resultaten | elk bestand |
| Missie-instellingen (de blk na de kop) | modus, weer, limieten, `stars` (datum, tijd, plaats) |
| Pakketstroom (zlib in 2025, zstd in 2026) | elk pakket afgebakend |
| Posities en houding van vliegtuigen (indeling 2026) | 4 samples per seconde, geen enkel pakket ongelezen; de heading komt overeen met de richting van de beweging |
| Vluchtpakketten vóór hun tijd | na een netwerkhapering toont het vluchtpakket van een clientreplay soms elk ander vliegtuig waar het ongeveer 0,75 s later zal zijn. De voorsprong wordt per pakket gemeten, en elk vliegtuig dat voorloopt krijgt de tijd die het voorstelt (`selfCheck.flightPacketsRetimed`) |
| Dead-reckoning-sprongen | een sprong uit een dead-reckoned reeks wordt gemeten vanaf de laatst ontvangen toestand, zodat de correcties van de client sporen niet meer afsnijden ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleports | een spoor wordt afgesneden waar zijn eenheid verder beweegt dan ze kan: eerst tegen haar soort (vliegtuig 750 m/s, grond en schepen 40 m/s, wapens 1800 m/s), dan tegen haar eigen tempo. Elke afsnijding staat in `trackBreaks` met de waarschijnlijke oorzaak (respawn, het spel dat de speler verplaatst, een correctie van een verre eenheid). Na de afsnijdingen is geen enkele stap tussen rijen van een spoor sneller dan haar soort toestaat (`selfCheck.stepSpeed`) |
| Posities van grond en schepen (0xF073 / 0xF074) | geen enkel pakket ongelezen. Heading, pitch en roll uit de houding van 16 bits: de heading komt overeen met de richting van de beweging binnen ongeveer 2 graden (mediaan); de pitch telt 180/65536 graden per stap; met het teken van de roll omgedraaid, wijst de richting van het kanon uit romp en toren voor bijna elk schot van een tank naar de getroffen eenheid. Schepen liggen op het waterniveau |
| Torens | de gier van de toren en de kanonhoogte van tanks: zie [Torens](ground.md#turrets) |
| Gepakte grondhoogten | posities die in 64 bits gepakt zijn, tellen hun hoogte vanaf -100 m op de meeste levels en vanaf het waterniveau op sommige; de verschuiving wordt per replay gemeten aan eenheden die in beide vormen gezien zijn (`selfCheck.packedGroundHeight`) |
| Entiteitenstroom (aanmaken, verwijderen) | elk aanmaken gelezen. De indeling komt uit de gepubliceerde broncode van de Dagor Engine; de eigen componenttypen van War Thunder worden overgeslagen door te zoeken waar de volgende component begint. Het voertuig en de spelersslot van elke eenheid zijn gelijk aan die welke het kill- en treffer-record noemt, voor elk gecontroleerd record |
| Wie welke eenheid bestuurde, AI-eenheden, schepen, grondobjecten | uit de entiteitenstroom: elke eenheid heeft haar voertuig en team, de eenheid van elke speler haar speler |
| Kills tegenover de resultaten | de doden per speler zijn gelijk aan die van de resultaten; de resultaten tellen meer kills, omdat de client niet elke kill krijgt. Een replay die begint nadat het gevecht al begonnen was, bevat alleen de kills na dat moment |
| Kills, kritieke treffers, zware schade | elk bestand |
| Vernietigde modules (0xF118) | de eenheid en het nummer van het onderdeel; de naam van het onderdeel heeft het schademodel van het voertuig nodig, dat niet in de replay staat |
| Afgevuurde wapens (entiteitenstroom) | het afvuurpunt ligt ongeveer 10-20 m (mediaan) van de dichtstbijzijnde eenheid, die als lanceerder genomen wordt |
| Wapens in de vlucht (0xF0DB) | missielen, raketten en bommen, elk gekoppeld aan zijn entiteit |
| Bommen zonder vluchtrecords | een bom zonder die records krijgt zijn val uitgerekend vanaf het afwerpen tot de inslag (zwaartekracht en weerstand, een sample elke 0,1 s, `extrapolated` waar). Gecontroleerd boven zee, waar de hoogte van de inslag bekend is: de uitgerekende vallen eindigen binnen ongeveer 15 m van het water. In het wedstrijddocument heeft zo'n wapen `ballisticImpact`; `counts.bombsBallistic` telt ze |
| Spelersslots, chat | elk bestand |
| Explosies, flakbuien, onderscheidingen, detecties, weer, missieobjecten | gelezen; posities met het oog gecontroleerd in de viewer |
| De instrumenten van de opnemende speler (0xD04A) | benoemd naar wat ze doen: [Cockpitinstrumenten](aircraft.md#cockpit-instruments); de rest onder `notNamed` |
| Andere velden van vluchtregels | snelheid, rondes, besturing, motoren: [Vluchtregels](aircraft.md#flight-entries) |
| Houding van gebeurtenisrijen | elke gebeurtenisrij draagt de heading, pitch, roll en kijkvector van zijn eenheid op dat moment |
| Statistieken van spelers en teamscores | aan het eind van het gevecht is elke statistiek voor elke speler gelijk aan die van de resultaten: [Reflectiegegevens](aircraft.md#reflection-data) |
| Namen van wapens en voertuigen | uit de Engelse lokalisatie van je installatie; een paar standaardgordels van schepen en radars van vliegvelden hebben geen naam in het spel |
| Spelers en AI | geen enkele rij van een speler uit de resultaten is AI, elke rij die geen AI is, is van een speler uit de resultaten (`selfCheck.identity`) |
| Wrakken | de samples van een eenheid na haar dood blijven komen; het wrak van een grondeenheid of schip is `alive` 0 tot haar entiteit verwijderd wordt, en blijft één spoor; vliegtuigen houden `alive` 0 hoogstens 60 s (`selfCheck.wrecks`) |
| Voertuigwisselingen | een eenheid van een speler die nog leeft wanneer de volgende eenheid van dezelfde speler verschijnt, wordt daar beëindigd (een voertuig dat blijft staan). `selfCheck.vehicleSwitch.twoLiveVehicles` moet 0 zijn |
| Gevechtsmodus | [Gevechtsmodus](ground.md#battle-mode) |
| Vliegtuigen in een serverreplay van 2026 | gelezen in de indeling van 2026; de heading en het teken van de roll komen overeen met de bochten; plaatshouders-vliegtuigen en verkenningsdrones dragen geen gegevens |
| Spelers van een serverreplay | gevonden op naam in de slots; elke statistiek is gelijk aan die van de resultaten (`selfCheck.players`) |
| Vliegtuigen in serverreplays van 2025 en versie 101286 | niet gelezen: hun vluchtpakketten hebben een andere indeling |

## Berichten aan eenheden {#messages-to-units}

Elk pakket van type 4 is een mpi-bericht van de daNet van de Dagor Engine: het id van het ontvangende object, dan (wanneer de laagste 11 bits allemaal gezet zijn) de ext-UID van het object, het berichtid en de inhoud. Een bericht aan een eenheid draagt als ext-UID het entiteits-id van de eenheid, `index << 10 | generatie`. Gecontroleerd: elk zo'n bericht noemt een entiteit die op dat moment leeft.

Voor specialisten: de gelezen berichten:

| Bericht | Wat, en de controle |
|---|---|
| 0xF0E9 UnitHitEffects | het treffen van één projectiel: het uid van de schutter en het trefpunt in het stelsel van de eenheid (x vooruit, y omhoog, z links): centimeters bij vliegtuigen en schepen, 20/32768 m per stap bij grondeenheden (afgestemd op de grootte van tanktorens). `hitLocalX/Y/Z` in meters. Wordt een `shot`-rij ([Vuur](hits.md#gunfire)). De aanvaller van bijna elk treffer- en killrecord staat onder deze schutters; de trefpunten liggen aan de kant die naar de schutter gericht is |
| 0xF133 UnitOnExplosion | hetzelfde uid van de schutter |
| 0xF04B OnUnitDead | `dead`-rijen: het slachtoffer van elk killrecord heeft er één binnen 2 s |
| 0xD047 FmwRpm | het toerental van de motoren (`rpm`); komt overeen met de toerenmeter van de cockpit |
| 0xF0B1, 0xF0A0 | `gun_shot`-rijen: losse schoten van zware luchtafweer en artillerie |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-rijen: salvo's van 40 mm-luchtafweergeschut (een kanon dat vuurt; een brand op een voertuig is `fire_on`, zie [Branden van voertuigen](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`-, `repair`-, `rearm`-, `bullet_rearm`-, `reload`-rijen |
| 0xD0FE ProjectileHitReplay | de eigen treffers van de opnemende speler en wat hem trof, met wapen en munitie, genoemd uit de installatie (`projectileHitReplays`) |
| 0xF13E, 0xF031 | het visuele effect van een treffer en een effect op de eenheid; ze komen met een treffer op dezelfde eenheid |
| 0xD041 | één per verdedigend kanon van een vliegtuig, twee keer per seconde; zijn indices komen overeen met de schutterswapens van het vluchtmodel |
| 0xD048, 0xF117 | indeling gelezen, betekenis niet bekend |
| de rest (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | in de sidecar van berichten met hun eenheid en velden |

De namen komen van de gemeenschap (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Ook gelezen {#also-read}

- **Replicatie van de entiteitenstroom** (0x22, 0x23): per entiteit een blok met componentwaarden: timers voor de reparatie van schepen, aantallen verbruiksgoederen, wijzigingen van eigenaar en team, oververhitting van motoren. Geteld in `counts.replicatedComponents`; de waarden in de sidecar van berichten.
- **Acties van het missiescript** (0xF028) en **hints** (0xF0EC): `triggers`, `hints`. **Voortgang van de missie** (0xF07A, 0xF07C): `missionProgress`.
- **De replaycamera** (0xD043): zie [De camera](ground.md#the-camera).

## Niet gelezen, en waarom {#not-read-and-why}

- **Namen en inhoud van entiteitsberichten** (0x20, 0x21): het klassenummer is een plek in een lijst die in het spel gecompileerd is, niet gestuurd en niet in haar gegevens. Twee worden gelezen (de branden van een voertuig en zijn blusapparaten); de rest wordt volledig bewaard met hun entiteit en klassenummer.
- **Andere gerepliceerde objecten** (soorten anders dan spelersslots en teams): gelezen en bewaard, niet benoemd; er is niets in de resultaten om ze tegen te controleren.
- **Besturing, gas en rondes van andere vliegtuigen**: alleen nu en dan ververst; bewaard in de vluchtsidecar, niet in de tabel.
- **Branden van vliegtuigen**: in geen enkel bericht gevonden; een vliegtuig in brand heeft geen `fire_on`-rij.
- **Namen van afgevuurde wapens**: de entiteit van een bom of raket bevat geen naam; killrecords noemen het wapen van een kill.
- **Schoten die misten**: een replay bevat alleen de treffers.

De `counts.messageIdsNotRead` en `selfCheck` van elk wedstrijddocument zeggen wat een nieuwe replay bevat en hoe goed hij gelezen is.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
