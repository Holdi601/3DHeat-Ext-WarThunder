---
title: "Wéi e Replay gelies gëtt"
nav_order: 10
lang: lb
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Wéi e Replay gelies gëtt {#how-it-reads-a-replay}

Dës Säit ass fir Leit, déi wëllen wëssen, wat de Konverter liest, wéi et gepréift
gouf, an domat, wéi wäit ee jidder Kolonn däerf trauen. Dir braucht se net, fir
Replays émzewandelen.

D'Liese gouf op Client-Replays vu Loft-Arcade-, Loft-Simulator- a
Marine-Gefechter gepréift, op Server-Replays vu Buedemgefechter, an, fir d'2025-
Layouten, op den ëffentleche Beispill-Replays vum
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
All Kontroll vergläicht e Wäert mat eppes, wat de Replay op eng zweet,
onofhängeg Manéier seet; nëmmen d'Method an d'Iwwereneestëmmung ginn hei ugi.

## Wat gelies gëtt, an d'Kontroll {#what-is-read-and-the-check}

| Deel | Status, an d'Kontroll |
|---|---|
| Header, Kaart, Mission, Startzäit, Sessioun; Resultater | all Datei |
| Missiounsastellungen (de blk nom Header) | Modus, Wieder, Limiten, `stars` (Datum, Zäit, Plaz) |
| Paketstroum (zlib an 2025, zstd an 2026) | all Paket gerahmt |
| Positioun a Lag vu Fliger (2026-Layout) | 4 Echantillonen d'Sekonn, kee Paket ongelies; d'Heading stëmmt mat der Beweegungsrichtung iwwereneen |
| Fluchpakete vir hirer Zäit | no engem Netzwierk-Hängen hält dem Client-Replay säi Fluchpaket heiansdo all aner Fliger do, wou en ongeféier 0.75 s méi spéit wäert sinn. De Virsprong gëtt pro Paket gemooss, a jidde Fliger, deen e Virsprong huet, kritt d'Zäit, fir déi en steet (`selfCheck.flightPacketsRetimed`) |
| Dead-Reckoning-Snaps | e Schrëtt aus engem dead-reckoned Laf gëtt vum leschten empfaangenen Zoustand gemooss, sou datt dem Client seng Korrekturen d'Spuren net méi schneiden ([Dead Reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporte | eng Spur gëtt geschnidden, wou hir Eenheet méi wäit geet, wéi se kann: fir d'éischt géint hir Aart (Fliger 750 m/s, Buedem a Schëff 40 m/s, Waffen 1800 m/s), dann géint hiren eegenen Tempo. All Schnëtt steet an `trackBreaks` mat senger wahrscheinlecher Ursaach (Respawn, d'Spill dat de Spiller beweegt, eng Korrektur vun enger wäiter Eenheet). No de Schnëtt ass kee Schrëtt tëscht Zeile vun enger Spur méi séier, wéi hir Aart erlaabt (`selfCheck.stepSpeed`) |
| Buedem- a Schëffspositiounen (0xF073 / 0xF074) | kee Paket ongelies. Heading, Pitch a Roll aus der 16-Bit-Lag: d'Heading stëmmt bannent ongeféier 2 Grad (Median) mat der Beweegungsrichtung iwwereneen; d'Pitch zielt 180/65536 Grad de Schrëtt; mat gedréintem Virzeechen vum Roll weist dem Rumpf an dem Turm seng Kanounrichtung bei bal all Panzerschoss op déi getraff Eenheet. Schëff sinn um Waasserniveau |
| Tierm | Turm-Yaw a Kanounpitch vu Panzer: kuck [Tierm](ground.md#turrets) |
| Gepaakte Buedemhéichten | a 64 Bits gepaakt Positioune zielen hir Héicht ab -100 m op de meeschte Levelen an ab Waasserniveau op e puer; den Offset gëtt op all Replay aus Eenheeten gemooss, déi a béide Forme gesi goufen (`selfCheck.packedGroundHeight`) |
| Entitéit-Stroum (Erstellung, Zerstéierung) | all Erstellung gelies. D'Layout kënnt aus dem verëffentlechte Quellcode vun der Dagor Engine; dem War Thunder seng eege Komponenttypen ginn iwwersprong, andeems fonnt gëtt, wou déi nächst Komponent ufänkt. D'Gefier an de Spiller-Slot vun all Eenheet sinn déi, déi d'Kill- an Treffer-Enregistrementer nennen, fir all kontrolléiert Enregistrement |
| Wien wéi eng Eenheet gefuer ass, KI-Eenheeten, Schëff, Buedemziler | aus dem Entitéit-Stroum: all Eenheet huet hiert Gefier an hiert Team, dem Spiller seng Eenheet säi Spiller |
| Kills géint d'Resultater | d'Doudeger pro Spiller si gläich wéi déi vun de Resultater; d'Resultater zielen méi Kills, well dem Client net all Kill geschéckt gëtt. E Replay, deen nom Ufank vum Gefecht ufänkt, hält nëmmen d'Kills duerno |
| Kills, kritesch Treffer, schwéiere Schued | all Datei |
| Zerstéiert Moduler (0xF118) | d'Eenheet an d'Nummer vum Deel; den Numm vum Deel brauch dem Gefier säi Schuedmodell, dat net am Replay ass |
| Ofgeschoss Waffen (Entitéit-Stroum) | den Ofschosspunkt ass e puer 10-20 m (Median) vun der nootster Eenheet, déi als Ofschosser geholl gëtt |
| Waffen am Fluch (0xF0DB) | Rakéiten, Rakéitegeschosser a Bommen, jiddwer un seng Entitéit gebonnen |
| Bommen ouni Fluchopzeechnungen | eng Bomm ouni se kritt hire Fall vum Ofwerfen bis zum Opschlag ausgerechent (Schwéierkraaft a Loftwiderstand, en Echantillon all 0.1 s, `extrapolated` true). Iwwer dem Mier gepréift, wou d'Opschlagshéicht bekannt ass: d'ausgerechent Fäll enden bannent ongeféier 15 m vum Waasser. Am Match-Dokument huet esou eng Waff `ballisticImpact`; `counts.bombsBallistic` zielt se |
| Spiller-Slots, Chat | all Datei |
| Explosiounen, Flak-Explosiounen, Auszeechnungen, Erkennungen, Wieder, Missiounsobjeten | gelies; Positioune mam A am Viewer gepréift |
| D'Instrumenter vum opuelende Spiller (0xD04A) | benannt no deem, wat se maachen: [Cockpit-Instrumenter](aircraft.md#cockpit-instruments); de Rescht ënner `notNamed` |
| Aner Felder vun de Fluchentréeën | Geschwindegkeet, Schëss, Rudere, Motoren: [Fluchentréeën](aircraft.md#flight-entries) |
| Lag vun den Evenement-Zeilen | all Evenement-Zeil dréit d'Heading, Pitch, Roll a de Bléckvecteur vu senger Eenheet an deem Moment |
| Spillerstatistiken a Teamscoren | um Enn vum Gefecht ass all Statistik gläich wéi déi vun de Resultater fir all Spiller: [Reflection-Daten](aircraft.md#reflection-data) |
| Waffen- a Gefiernimm | aus der englescher Lokalisatioun vun Ärer Installatioun; e puer Standard-Gurten vu Schëff a Fluchhafenradaren hunn keen Numm am Spill |
| Spiller a KI | keng Zeil vun engem Resultater-Spiller ass KI, all Zeil, déi net KI ass, ass vun engem Resultater-Spiller (`selfCheck.identity`) |
| Wracken | d'Echantillone vun enger Eenheet no hirem Doud kommen weider; dem Buedemeenheet oder Schëff säi Wrack ass `alive` 0, bis seng Entitéit ewechgeholl gëtt, a bleift eng Spur; Fliger halen `alive` 0 héchstens 60 s (`selfCheck.wrecks`) |
| Gefierwiesselen | d'Eenheet vun engem Spiller, déi nach lieft, wann dem selwechte Spiller seng nächst Eenheet opdaucht, gëtt do beendegt (e stoe gelooss Gefier). `selfCheck.vehicleSwitch.twoLiveVehicles` muss 0 sinn |
| Battle-Modus | [Battle-Modus](ground.md#battle-mode) |
| Fliger an engem 2026-Server-Replay | an der 2026-Layout gelies; d'Heading an d'Virzeechen vum Roll stëmmen mat de Kéiere iwwereneen; Platzhalter-Fliger a Recon-Dronen droen keng Daten |
| Spiller vun engem Server-Replay | no Numm an de Slots fonnt; all Statistik ass gläich wéi déi vun de Resultater (`selfCheck.players`) |
| Fliger an 2025-Server-Replays a Versioun 101286 | net gelies: hir Fluchpakete hunn eng aner Layout |

## Messagen un Eenheeten {#messages-to-units}

All Paket vum Typ 4 ass eng mpi-Message vum daNet vun der Dagor Engine: d'ID vum
Empfänger-Objet, dann (wann seng ënnescht 11 Bits all gesat sinn) dem Objet seng
Ext-UID, d'Message-ID an d'Payload. Eng Message un eng Eenheet dréit als Ext-UID
d'Entitéit-ID vun der Eenheet, `index << 10 | generation`. Gepréift: all
esou eng Message nennt eng Entitéit, déi an deem Moment lieft.

Fir Spezialisten, d'Messagen, déi gelies ginn:

| Message | Wat, an d'Kontroll |
|---|---|
| 0xF0E9 UnitHitEffects | den Treffer vun engem Projektil: d'uid vum Schëtze an den Treffpunkt am System vun der Eenheet (x no vir, y erop, z no lénks): Zentimeter bei Fliger a Schëff, 20/32768 m de Schrëtt bei Buedemeenheeten (un d'Gréisst vun de Panzertierm ugepasst). `hitLocalX/Y/Z` a Meter. Gëtt eng `shot`-Zeil ([Schéiss](hits.md#gunfire)). Den Ugräifer vu bal all Treffer- a Kill-Enregistrement ass ënnert dëse Schëtzen; d'Treffpunkte leien op der Säit, déi dem Schëtze gesicht ass |
| 0xF133 UnitOnExplosion | déiselwecht Schëtze-uid |
| 0xF04B OnUnitDead | `dead`-Zeilen: dem Victim vun all Kill-Enregistrement huet eng bannent 2 s |
| 0xD047 FmwRpm | d'Dréizuel vun de Motoren (`rpm`); stëmmt mam Dréizuelinstrument vum Cockpit iwwereneen |
| 0xF0B1, 0xF0A0 | `gun_shot`-Zeilen: Eenzelschëss vu schwéierer Fligerofwier an Artillerie |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-Zeilen: Stéiss vu 40-mm-Fligerofwier-Kanounen (eng Kanoun, déi schéisst; e Brand um Gefier ass `fire_on`, kuck [Gefierbränn](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`-Zeilen |
| 0xD0FE ProjectileHitReplay | dem opuelende Spiller seng eege Treffer an Treffer op hie, mat Waff a Munitioun, aus der Installatioun benannt (`projectileHitReplays`) |
| 0xF13E, 0xF031 | dem Treffer säi visuellen Effekt an en Effekt, deen op der Eenheet gespillt gëtt; si kommen mat engem Treffer op déiselwecht Eenheet |
| 0xD041 | eng pro Verdeedegungskanoun vun engem Fliger, zweemol d'Sekonn; hir Indexe passen zu de Schëtzewaffen vum Flugmodell |
| 0xD048, 0xF117 | Layout gelies, Bedeitung net bekannt |
| de Rescht (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | an der Messages-Niewendatei mat hirer Eenheet a Felder |

D'Nimm sinn déi vun der Communautéit (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Och gelies {#also-read}

- **Replikatioun vum Entitéit-Stroum** (0x22, 0x23): pro Entitéit e Block vu
  Komponentewäerter: Schëffsreparaturzäitgeber, Zuele vu Verbrauchsgidder, Besëtzer- an Team-
  Ännerungen, Motorüberhëtzung. Gezielt an `counts.replicatedComponents`; d'
  Wäerter an der Messages-Niewendatei.
- **Missiounsskript-Aktiounen** (0xF028) an **Hiweiser** (0xF0EC): `triggers`,
  `hints`. **Missiounsfortschrëtt** (0xF07A, 0xF07C): `missionProgress`.
- **D'Replay-Kamera** (0xD043): kuck [D'Kamera](ground.md#the-camera).

## Net gelies, a firwat {#not-read-and-why}

- **Nimm a Kierper vun Entitéit-Messagen** (0x20, 0x21): d'Klassennummer ass eng
  Plaz an enger Lëscht, déi an d'Spill kompiléiert ass, net geschéckt a net an hiren Daten. Zwee
  ginn gelies (d'Bränn vun engem Gefier a seng Feierläscher); de Rescht gëtt
  ganz mat hirer Entitéit a Klassennummer behalen.
- **Aner replizéiert Objeten** (aner Aarte wéi Spiller-Slots an Teams):
  gelies a behalen, net benannt; näischt an de Resultater, fir se dergéint ze préifen.
- **Rudere, Gashiewel a Schëss vun anere Fliger**: nëmmen heiansdo
  rafraîchéiert; an der Fluch-Niewendatei behalen, net an der Tabell.
- **Fligerbränn**: a kenger Message fonnt; e brennende Fliger huet keng
  `fire_on`-Zeil.
- **Nimm vun ofgeschoss Waffen**: d'Entitéit vun enger Bomm oder Rakéit hält keen Numm;
  Kill-Enregistrementer nennen d'Waff vun engem Kill.
- **Schëss, déi verfeelt hunn**: e Replay hält nëmmen d'Treffer.

Dem Match-Dokument säi `counts.messageIdsNotRead` an `selfCheck` soen, wat e
neie Replay hält a wéi gutt e gelies gouf.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
