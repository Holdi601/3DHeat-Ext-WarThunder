---
title: Tabellen
nav_order: 6
lang: da
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabellen {#the-table}

![Tabellen fra et syntetisk replay, opsummeret](../assets/img/table.svg)

Én række pr. sample eller begivenhed, 105 kolonner ([Kolonneliste](../columns.md), genereret ud fra koden); i fodnoten, under `heat3d`, står viewerens
læseinstruktioner, så vieweren ikke behøver at få udfyldt en formular.

| Kolonne | Hvad |
|---|---|
| `time` | sekunder på replayets eget ur |
| `event` | `position`; begivenhedsrækker ligger på sporet på deres tidspunkt (mellem to samples, på linjen mellem dem); `kill` (ved dræberen), `death` (ved offeret), `hit_critical` / `hit_severe` (ved den ramte enhed), `module_destroyed` (ved enheden), `launch` (ved den enhed, der affyrede et våben), `impact` (et våbens sidste sample, når det blev fjernet straks efter); `explosion` og `flak` (0xD08E, 0xD01F) ved deres position, art `effect`, intet spor, med eksplosionens retning, hvor den har en; `shot` (et projektil, der ramte, ved skytten), `gun_shot`, `fire_start`, `fire_stop` (et kanons skudserie, ikke et køretøj i brand), `fire_on`, `fire_off` (et køretøj i brand, se [Brande i køretøjer](hits.md#vehicle-fires)), `reward` (Silver Lions og forskningspoint optjent, se [Økonomi](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (se [Meddelelser til enheder](how-it-reads.md#messages-to-units)); `despawn`: den sidste række i et spor, hvis enhed er væk, før replayet slutter (se [Slutningen af et spor](ground.md#end-of-a-track)) |
| `track` | det vieweren tegner som én ting: ét liv for en enhed, eller et våbens flyvning - `<spiller eller køretøj> #<hex>` (vieweren viser navnet uden delen `#`) |
| `x`, `y`, `z` | spillets meter: x øst, y op, z nord (hints spejler z, så nord ikke tegnes som syd) |
| `player` | spillerens navn; en AI-enhed `<VehicleName> #<uid>` (for eksempel `F-15A #204`); `uid <n>`, når intet navngiver den; for et våben, hvem der affyrede det |
| `userId`, `team` | spillerens Gaijin-id og holdet (`1`, `2`) |
| `ai`, `isPlayer` | `ai` er sand for hver enhed, som ingen spilkonto styrer (missionsenheder, AI-fly, mål på land, luftværnskanoner, skibe uden spiller, pladsholdere), `isPlayer` er det modsatte: en spiller er en enhed, hvis entitet angiver en spillerplads med et Gaijin-id. Et våben har sin affyrers værdi; tom, når den ikke kendes |
| `match` | kampens id (kampdokumentets `match`), på hver række; hints kortlægger det som sessionen, så to indlæste replays aldrig sammenføjer spor |
| `life` | `uid#n`: én enheds spor, skåret, hvor uid'et går over til en anden enhed, enheden bevæger sig hurtigere, end den kan (en genopstandelse, en genbevæbning, spillet flytter den, klienten korrigerer en fjern enhed; se Teleports i [Sådan læses et replay](how-it-reads.md#what-is-read-and-the-check)) eller er længe usynlig; `w<hex>` et våbens flyvning (`w<hex>#n` efter et snit) |
| `uid` | enhedens id i replayet |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (en sporvogn eller jernbanevogn, banen placerer, se [Scene-enheder](objectives.md#scene-units-trams-and-rail-wagons)); våben `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` den optagende spillers replay-kamera (se [Kameraet](ground.md#the-camera)) |
| `type` | spillets egen type, hvor resultaterne nævner den (`fighter`, `assault`, `destroyer`, `gun_boat`), ellers som `kind` |
| `Vehicle` | spillets køretøjs-id (`f_15a`, `germ_flakpz_I_Gepard`), som viewerens figurer matcher |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | køretøjets engelske navn fra din installations lokalisering (`Pz.Kpfw. III Ausf. J1`, kort `Pz.III J1`) og dets nøgle (`germ_pzkpfw_III_ausf_J_0`); spilskriftets landemærker er udeladt. Hvor spillet intet navngiver, eller ingen installation findes, er navnet id'et og nøglen tom |
| `mission` | enhedens navn i missionen (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | hvor enheden peger (kigvektoren): fly ud fra flyvemodellens holdning, landenheder og skibe ud fra deres egen, våben langs deres flyvning |
| `heading`, `pitch`, `roll` | det samme i grader; heading er kompasset, med uret fra nord, pitch positiv med næsen op, roll positiv med højre vinge ned (flyvemodellen sender det modsatte fortegn, se [Holdning, kontrolleret](aircraft.md#attitude-checked); en landenhed med højre side ned). Hints siger det under `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | en tanks hovedtårn - hvor kanonen peger, ikke hvor dens spiller kigger; replayets værdi holdt til tårnmotorens hastighed og sat til hver hovedkanons skudlinje (se [Tårne](ground.md#turrets)): dets drejning i forhold til skroget (grader, med uret set oppefra positiv, 0 lige frem) og kanonens hævning i forhold til skroget (grader, op positiv); `turrets` hvert tårn på køretøjet som `yaw pitch;yaw pitch;...` i sin egen rækkefølge (en ubrugt plads læses `0.00 0.00`). Tanks, luftværnskøretøjer, pansrede mandskabsvogne og lastbiler, i klient- og serverreplays; ikke skibe (se [Tårne](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | hovedtårnet, som replayet sender det; `turretYaw` / `gunPitch` er det holdt til tårnmotorens hastighed og sat til hver hovedkanons skudlinje (se [Tårne](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | hvor spilleren kigger (sigter med kameraet) i verden: kompasgrader (0 nord, med uret) og grader op, samme konvention som `aimHeading` / `aimPitch` (i modsætning til `turretYaw` / `gunPitch`, som forbliver i forhold til skroget). Hver spillers tank i et serverreplay, den optagende spillers egen i et klientreplay; tom, hvor spilleren ikke sigter nogen steder (alle fire sigteflydere 0). Tårnet følger den med sin egen drejehastighed, så de to adskiller sig, mens det drejer (se [Tårne](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | den optagende spillers egen tank: hvor den sigter (kompasgrader, grader op, afstanden i m; 2000, når intet er i sigtet); kamerarækker: hvor spilleren sigter (heading, pitch) |
| `zoom` | kamerarækker: kameraets forstørrelse (se [Kameraet](ground.md#the-camera)) |
| `difficulty`, `gameMode` | kampens `AB`, `RB` eller `SB`, og `ground`, `air` eller `naval`, på hver række (se [Kamptilstand](ground.md#battle-mode)) |
| `extrapolated` | en flyprøve, der er klientens dead reckoning, ikke en tilstand, den modtog (se [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); en bombes prøve beregnet ud fra dens udløsning (se Bomber uden flyvedata i [Sådan læses et replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | hvor langt udjævneren flyttede prøven (m), og replayets egen position og holdning (roll i tabellens fortegn) |
| `targetX`, `targetY`, `targetZ` | et `shot`s ramtepunkt |
| `hitOutcome`, `hitFlags` | et `shot`s udfald på en landenhed: `kill`, `critical`, `penetration` eller `nonpenetration` (afbøjet eller stoppet: replayet kan ikke skelne en afprallen fra andet), ud fra bitene serveren sender med træffet (`hitFlags`, rå); tom, hvor intet sendes (fly, skibe). Se [Træfudfald](hits.md#hit-outcomes) |
| `hitShell` | et `shot`s granatsignatur: fire bytes fra træffets meddelelse (rå hex); én signatur kan stå for forskellige granater (120 og 125 mm APFSDS deler én), så den gemmes rå og læses ikke som kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | et `shot`s ammunition: dens type (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) og id (`125mm_3bm46`), hvor et drab angiver skytterens plads, ellers `explosive` (træffets udbrud) eller `kinetic`; kanonens `weapon/slot` fra dens genladninger; kaliberen i mm fra installationens våbenfiler. Se [Træfudfald](hits.md#hit-outcomes) |
| `rpm` | et flys motoromdrejninger (gennemsnittet for dets motorer) som sidst sendt, inden for 2 s |
| `vx`, `vy`, `vz` | et flys hastighed, som dets flyveprøve sender den (m/s, spillets akser; hastigheder over 500 m/s læses som 500) |
| `engine`, `afterburner`, `engineCondition` | et flys motorer fra dets flyveprøve: `off`, `starting`, `running`, `dead` (`/`-adskilt, når dens motorer er forskellige); efterbrænderen 0-1; en byte, der kun sendes, efter motoren blev ramt |
| `weaponName` | drab og dødsfald: våbnet eller ammunitionen på din installations engelsk (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | kun den optagende spillers fly: gasset 0-1.1 fra dets cockpit (1.1 nødeffekt eller efterbrænder; ellers dets flyveprøves sekstendedele), styrefladerne -1..1 fra dets flyveprøve (højderor positiv når trækkende op, krængeror positiv, når flyet ruller til højre), de tilbageværende skud pr. våben (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | kun den optagende spillers fly, fra dets cockpit: indikeret lufthastighed og stigehastighed (m/s), brændstof, indsugningstryk (atm), understel (0-1, 1 nede), olie- og cylinderhovedtemperatur, hvor dets cockpit har måleren |
| `speed` | m/s over ca. to sekunder af sporet (beregnet her; replayet sender ingen hastighed for andre enheder) |
| `alive` | 0 for en enheds samples efter dens død (dens vrag): for en landenhed eller et skib, til spillet fjerner den eller dens samples ender, for et fly i højst 60 s |
| `otherVehicle`, `otherLife` | et `shot`s offer: dets køretøj og dets `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | et `shot`s ramtepunkt i offerets egen ramme (m; x fremad, y op, z venstre; se [Meddelelser til enheder](how-it-reads.md#messages-to-units)) og den måde, skuddet kom på, omsat til den ramme af offerets holdning dengang |
| `hitPart`, `hitFlag` | et `shot`s træffemeddelelse: dets delord som sendt, og dets høje byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | hvad kampen kostede og indbragte, og hvem der vandt: se [Økonomi](economy.md) |
| `other`, `weapon` | drab: den anden side og våbnet; træf: hvem der ramte (ud fra rekordens uid, ellers dens spillerplads), deres køretøj; affyringer: våbnet; ødelagte moduler: hvem der sidst ramte enheden inden for 5 s før, og `part <n>` |

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
