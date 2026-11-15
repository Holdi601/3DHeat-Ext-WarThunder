---
title: "D'Tabell"
nav_order: 6
lang: lb
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# D'Tabell {#the-table}

![D'Tabell vun engem synthetesche Replay, zesummegefasst](../assets/img/table.svg)

Eng Zeil pro Echantillon oder Evenement, 105 Kolonnen ([Kolonnelëscht](../columns.md), aus dem Code generéiert); am Fouss, ënner `heat3d`, d'Liesuweisunge fir
de Viewer, sou datt de Viewer kee Formulaire muss ausfëllen.

| Kolonn | Wat |
|---|---|
| `time` | Sekonnen op der eegener Auer vum Replay |
| `event` | `position`; Evenement-Zeile leien op der Spur an hirem Moment (tëscht zwee Echantillonen, op der Linn tëscht hinnen); `kill` (beim Killer), `death` (beim Opfer), `hit_critical` / `hit_severe` (bei der getraffener Eenheet), `module_destroyed` (bei der Eenheet), `launch` (bei der Eenheet, déi eng Waff ofgeschoss huet), `impact` (dat leschte Echantillon vun enger Waff, wa se direkt duerno ewechgeholl gouf); `explosion` a `flak` (0xD08E, 0xD01F) un hirer Positioun, Aart `effect`, keng Spur, mat der Richtung vun der Explosioun, wou se eng huet; `shot` (e Projektil, dat getraff huet, beim Schëtze), `gun_shot`, `fire_start`, `fire_stop` (e Feierstouss vun enger Kanoun, net e brennend Gefier), `fire_on`, `fire_off` (e brennend Gefier, kuck [Gefierbränn](hits.md#vehicle-fires)), `reward` (verdéngte Silver Lions a Fuerschungspunkten, kuck [Wirtschaft](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (kuck [Messagen un Eenheeten](how-it-reads.md#messages-to-units)); `despawn`: déi lescht Zeil vun enger Spur, wou d'Eenheet fort ass, ier de Replay ophält (kuck [Enn vun enger Spur](ground.md#end-of-a-track)) |
| `track` | wat de Viewer als eng Saach zeechent: ee Liewe vun enger Eenheet, oder de Fluch vun enger Waff - `<player or vehicle> #<hex>` (de Viewer weist den Numm ouni de `#`-Deel) |
| `x`, `y`, `z` | d'Meter vum Spill: x Ouschten, y erop, z Norden (d'Hiweiser spigele z, sou datt Norden net no Süden gezeechent gëtt) |
| `player` | den Numm vum Spiller; eng KI-Eenheet `<VehicleName> #<uid>` (zum Beispill `F-15A #204`); `uid <n>`, wann näischt se nennt; bei enger Waff, wien se ofgeschoss huet |
| `userId`, `team` | d'Gaijin-ID vum Spiller an d'Team (`1`, `2`) |
| `ai`, `isPlayer` | `ai` wouer fir all Eenheet, déi kee Spiller-Kont fiert (Missiounseenheeten, KI-Fliger, Buedemziler, Fligerofwier, Schëff ouni Spiller, Platzhalter), `isPlayer` de Géigendeel: e Spiller ass eng Eenheet, där hir Entitéit e Spiller-Slot mat enger Gaijin-ID nennt. Eng Waff huet déi vu sengem Ofschosser; eidel, wann et net bekannt ass |
| `match` | d'Match-ID (dem Match-Dokument säin `match`), op all Zeil; d'Hiweiser mappen et als Sessioun, sou datt zwee gelueden Replays ni Spuren zesummeféieren |
| `life` | `uid#n`: d'Spur vun enger Eenheet, geschnidde wou d'uid op eng aner Eenheet geet, d'Eenheet méi séier geet, wéi se kann (e Respawn, e Rearm, d'Spill dat se beweegt, de Client deen eng wäit Eenheet korrigéiert; kuck Teleporte a [Wéi e Replay gelies gëtt](how-it-reads.md#what-is-read-and-the-check)) oder laang net gesi gëtt; `w<hex>` de Fluch vun enger Waff (`w<hex>#n` no engem Schnëtt) |
| `uid` | d'ID vun der Eenheet am Replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (eng Tram oder e Schinnewaggon, dee Level setzt, kuck [Zeeneneenheeten](objectives.md#scene-units-trams-and-rail-wagons)); Waffen `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` d'Replay-Kamera vum opuelende Spiller (kuck [D'Kamera](ground.md#the-camera)) |
| `type` | dem Spill säin eegenen Typ, wou d'Resultater en nennen (`fighter`, `assault`, `destroyer`, `gun_boat`), soss wéi `kind` |
| `Vehicle` | dem Spill seng Gefier-ID (`f_15a`, `germ_flakpz_I_Gepard`), déi d'Figure vum Viewer zesummepasse |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | den englesche Numm vum Gefier aus der Lokalisatioun vun Ärer Installatioun (`Pz.Kpfw. III Ausf. J1`, kuerz `Pz.III J1`) a säi Schlëssel (`germ_pzkpfw_III_ausf_J_0`); d'Landeszeechen vun der Spillschrëft fale weg. Wou d'Spill näischt nennt, oder keng Installatioun fonnt gëtt, ass den Numm d'ID an de Schlëssel eidel |
| `mission` | den Numm vun der Eenheet an der Mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | wouhin d'Eenheet weist (de Bléckvektor): Fliger aus der Lag vum Flugmodell, Buedemeenheeten a Schëff aus hirer eegener, Waffen laanscht hire Fluch |
| `heading`, `pitch`, `roll` | datselwecht a Grad; heading ass de Kompass, am Auerzäigersënn vum Norden aus, pitch Nues erop positiv, roll rietse Flilleck erof positiv (d'Flugmodell schéckt dat entgéintgesate Virzeechen, kuck [Lag, gepréift](aircraft.md#attitude-checked); bei enger Buedemeenheet déi riets Säit erof). D'Hiweiser soen dat ënner `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | den Haaptturm vun engem Panzer - wouhin d'Kanoun weist, net wouhin säi Spiller kuckt; de Wäert vum Replay, op d'Geschwindegkeet vum Turmantrieb gehalen an op d'Linn vun all Haaptkanounschoss gesat (kuck [Tierm](ground.md#turrets)): säi Yaw relativ zum Rumpf (Grad, am Auerzäigersënn vun uewen gesi positiv, 0 grad no vir) a säi Kanounpitch relativ zum Rumpf (Grad, erop positiv); `turrets` all Turm vum Gefier als `yaw pitch;yaw pitch;...` a senger eegener Reiefolleg (e onbenotzte Slot liest `0.00 0.00`). Panzer, SPAA, APCs a Camionen, a Client- a Server-Replays; keng Schëff (kuck [Tierm](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | den Haaptturm, wéi de Replay en schéckt; `turretYaw` / `gunPitch` sinn en, gehalen op d'Geschwindegkeet vum Turmantrieb a gesat op d'Linn vun all Haaptkanounschoss (kuck [Tierm](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | wouhin de Spiller kuckt (mat der Kamera ziilt) an der Welt: Kompassgrad (0 Norden, am Auerzäigersënn) a Grad erop, déiselwecht Konventioun wéi `aimHeading` / `aimPitch` (am Géigesaz zu `turretYaw` / `gunPitch`, déi relativ zum Rumpf bleiwen). All Spiller säi Panzer an engem Server-Replay, deen eegenen vum opuelende Spiller an engem Client-Replay; eidel, wou de Spiller nach net ziilt (all véier Ziel-Floats 0). Den Turm follegt him mat senger eegener Dréigeschwindegkeet, sou datt déi zwee ofwäichen, während en dréit (kuck [Tierm](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | dem opuelende Spiller säi Panzer: wouhin en ziilt (Kompassgrad, Grad erop, d'Distanz a m; 2000, wann näischt am Visier ass); Kamera-Zeilen: wouhin de Spiller ziilt (heading, pitch) |
| `zoom` | Kamera-Zeilen: d'Vergréisserung vun der Kamera (kuck [D'Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | dem Gefecht säin `AB`, `RB` oder `SB`, an `ground`, `air` oder `naval`, op all Zeil (kuck [Battle-Modus](ground.md#battle-mode)) |
| `extrapolated` | e Fliger-Echantillon, dat dem Client säin Dead Reckoning ass, net en empfangenen Zoustand (kuck [Dead Reckoning](aircraft.md#dead-reckoning-and-the-smoother)); dem Bomm säin Echantillon, ausgerechent aus sengem Ofwerfen (kuck Bommen ouni Fluchopzeechnungen a [Wéi e Replay gelies gëtt](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | wéi wäit de Glätter d'Echantillon verréckelt huet (m), an dem Replay seng eege Positioun a Lag (roll mat dem Virzeechen vun der Tabell) |
| `targetX`, `targetY`, `targetZ` | dem `shot` säin Treffpunkt |
| `hitOutcome`, `hitFlags` | dem `shot` säin Ausgang op enger Buedemeenheet: `kill`, `critical`, `penetration` oder `nonpenetration` (ofgeprallt oder gestoppt: de Replay ennerscheet keen Ofpraller), aus de Bits, déi de Server mam Treffer schéckt (`hitFlags`, rau); eidel, wou keng geschéckt ginn (Fliger, Schëff). Kuck [Treffer-Ausgäng](hits.md#hit-outcomes) |
| `hitShell` | d'Granat-Signatur vun engem `shot`: véier Bytes vun der Treffer-Message (rau Hex); eng Signatur kann fir verschidde Granate stoen (120 an 125 mm APFSDS deelen eng), dofir gëtt se rau behalen, net als Kaliber gelies |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | d'Munitioun vun engem `shot`: säin Typ (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) a seng ID (`125mm_3bm46`), wou en Ofschoss de Slot vum Schëtze nennt, soss `explosive` (de Treffer-Knall) oder `kinetic`; dem Kanoun säin `weapon/slot` aus sengem Nolueden; d'Kaliber a mm aus de Waffendateien vun der Installatioun. Kuck [Treffer-Ausgäng](hits.md#hit-outcomes) |
| `rpm` | d'Motordréizuel vun engem Fliger (de Mëttelwäert iwwer seng Motoren), wéi zuletzt geschéckt, bannent 2 s |
| `vx`, `vy`, `vz` | d'Geschwindegkeet vun engem Fliger, wéi säin Fluchentrée se schéckt (m/s, d'Achse vum Spill; Geschwindegkeete iwwer 500 m/s liesen 500) |
| `engine`, `afterburner`, `engineCondition` | d'Motore vun engem Fliger aus sengem Fluchentrée: `off`, `starting`, `running`, `dead` (mat `/` verbonnen, wann seng Motore sech ennerscheeden); den Nobrenner 0-1; e Byte, dat nëmmen no engem Motortreffer geschéckt gëtt |
| `weaponName` | Kills an Doudeger: d'Waff oder d'Munitioun am Englesche vun Ärer Installatioun (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | nëmmen de Fliger vum opuelende Spiller: de Gashiewel 0-1.1 aus sengem Cockpit (1.1 Kriichsnuetfall-Leeschtung oder Nobrenner; soss d'Fofzéntel vu sengem Fluchentrée), d'Rudere -1..1 aus sengem Fluchentrée (elevator positiv zéien, aileron positiv no riets rollen), d'iwwreg Schëss pro Waff (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | nëmmen de Fliger vum opuelende Spiller, aus sengem Cockpit: ugewisen Loftgeschwindegkeet a Steigrate (m/s), Brennstoff, Luedduck (atm), Fahrwierk (0-1, 1 ausgefuer), Ueleg- a Zylinderkäpptemperatur, wou säi Cockpit d'Instrument huet |
| `speed` | m/s iwwer ongeféier zwou Sekonne vun der Spur (hei ausgerechent; de Replay schéckt keng Geschwindegkeet fir aner Eenheeten) |
| `alive` | 0 fir d'Echantillone vun enger Eenheet no hirem Doud (hir Wrack): bei enger Buedemeenheet oder engem Schëff bis d'Spill se ewechhëlt oder hir Echantillone ophalen, bei engem Fliger héchstens 60 s |
| `otherVehicle`, `otherLife` | dem `shot` säin Opfer: säi Gefier a säi `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | dem `shot` säin Treffpunkt am eegene Koordinatesystem vum Opfer (m; x no vir, y erop, z no lénks; kuck [Messagen un Eenheeten](how-it-reads.md#messages-to-units)) an d'Richtung, aus där de Schoss koum, mat der Lag vum Opfer deemools an dat System gedréint |
| `hitPart`, `hitFlag` | d'Treffer-Message vun engem `shot`: säi Deelwuert, wéi geschéckt, a säin héije Byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | wat d'Gefecht kascht an agedron huet, a wien gewonnen huet: kuck [Wirtschaft](economy.md) |
| `other`, `weapon` | Kills: déi aner Säit an d'Waff; Treffer: wien getraff huet (aus der uid vum Enregistrement, soss sengem Spiller-Slot), säi Gefier; Launches: d'Waff; zerstéiert Moduler: wien d'Eenheet zuletzt bannent 5 s virdrun getraff huet, a `part <n>` |

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
