---
title: "Tabellen"
nav_order: 6
lang: "no"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabellen {#the-table}

![Tabellen til en syntetisk replay, oppsummert](../assets/img/table.svg)

Én rad per sample eller hendelse, 105 kolonner ([Kolonneliste](../columns.md), generert fra koden); i bunntekst, under `heat3d`, visningsprogrammets
leseinstruksjoner, så visningsprogrammet trenger ikke at noe fylles ut.

| Kolonne | Hva |
|---|---|
| `time` | sekunder på replayens egen klokke |
| `event` | `position`; hendelsesrader ligger på sporet ved sitt øyeblikk (mellom to samples, på linjen mellom dem); `kill` (ved drapperen), `death` (ved offeret), `hit_critical` / `hit_severe` (ved enheten som ble truffet), `module_destroyed` (ved enheten), `launch` (ved enheten som slapp et våpen), `impact` (et våpens siste sample når det ble fjernet rett etter); `explosion` og `flak` (0xD08E, 0xD01F) på sin posisjon, type `effect`, ingen spor, med eksplosjonens retning der den har en; `shot` (et prosjektil som traff, ved skytteren), `gun_shot`, `fire_start`, `fire_stop` (en kanons skuddserie, ikke et kjøretøy i brann), `fire_on`, `fire_off` (et kjøretøy i brann, se [Kjøretøybranner](hits.md#vehicle-fires)), `reward` (Silver Lions og forskningspoeng tjent, se [Økonomi](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (se [Meldinger til enheter](how-it-reads.md#messages-to-units)); `despawn`: den siste raden i et spor der enheten er borte før replayen slutter (se [Slutten av et spor](ground.md#end-of-a-track)) |
| `track` | det visningsprogrammet tegner som én ting: ett liv til en enhet, eller ett våpens flukt - `<spiller eller kjøretøy> #<hex>` (visningsprogrammet viser navnet uten `#`-delen) |
| `x`, `y`, `z` | spillets meter: x øst, y opp, z nord (hintene speiler z, så nord tegnes ikke sør) |
| `player` | spillerens navn; en KI-enhet `<VehicleName> #<uid>` (for eksempel `F-15A #204`); `uid <n>` når ingenting navngir den; for et våpen, hvem som slapp det |
| `userId`, `team` | spillerens Gaijin-ID og laget (`1`, `2`) |
| `ai`, `isPlayer` | `ai` true for hver enhet ingen spillerkonto kjører (oppdragsenheter, KI-fly, bakkemål, luftvernkanoner, skip uten spiller, plassholdere), `isPlayer` det motsatte: en spiller er en enhet hvis entitet navngir en spillerplass med en Gaijin-ID. Et våpen har sin avfyrers; tom når det ikke er kjent |
| `match` | kamp-ID-en (kampdokumentets `match`), på hver rad; hintene kobler den som økten, så to innlastede replayer aldri slår sammen spor |
| `life` | `uid#n`: en enhets spor, kuttet der uid-en går over til en annen enhet, enheten beveger seg raskere enn den kan (en gjenoppstandelse, en omlasting, spillet som flytter den, klienten som korrigerer en fjern enhet; se Teleporteringer i [Slik leser den en replay](how-it-reads.md#what-is-read-and-the-check)) eller er lenge usett; `w<hex>` et våpens flukt (`w<hex>#n` etter et kutt) |
| `uid` | enhetens ID i replayen |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (en trikk eller skinnevogn nivået plasserer, se [Scene-enheter](objectives.md#scene-units-trams-and-rail-wagons)); våpen `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` opptakspilotens replay-kamera (se [Kameraet](ground.md#the-camera)) |
| `type` | spillets egen type der resultatene navngir den (`fighter`, `assault`, `destroyer`, `gun_boat`), ellers som `kind` |
| `Vehicle` | spillets kjøretøy-ID (`f_15a`, `germ_flakpz_I_Gepard`), som visningsprogrammets figurer matcher |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | kjøretøyets engelske navn fra installasjonens lokalisering (`Pz.Kpfw. III Ausf. J1`, kort `Pz.III J1`) og dets nøkkel (`germ_pzkpfw_III_ausf_J_0`); spillets skriftmerker for land utelates. Der spillet ikke navngir noe, eller ingen installasjon finnes, er navnet ID-en og nøkkelen tom |
| `mission` | enhetens navn i oppdraget (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | hvilken vei enheten peker (sikteretningsvektoren): fly fra flymodellens holdning, bakkeenheter og skip fra sine egne, våpen langs deres flukt |
| `heading`, `pitch`, `roll` | det samme i grader; heading er kompasset, med klokken fra nord, stigning med nesen opp positiv, rull høyre vinge ned positiv (flymodellen sender det motsatte fortegnet, se [Holdning, kontrollert](aircraft.md#attitude-checked); en bakkeenhets høyre side ned). Hintene sier det under `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | en stridsvogns hovedtårn - der kanonen peker, ikke dit spilleren ser; replayens verdi holdt til tårndrevets fart og satt til hver hovedkanons skuddlinje (se [Tårn](ground.md#turrets)): dens gir relativt til skroget (grader, med klokken sett ovenfra positiv, 0 rett frem) og kanonens stigning relativt til skroget (grader, opp positiv); `turrets` hvert tårn på kjøretøyet som `gir stigning;gir stigning;...` i sin egen rekkefølge (en ubrukt plass står `0.00 0.00`). Stridsvogner, SPAA, pansrede mannskapsvogner og lastebiler, i klient- og serverreplayer; ikke skip (se [Tårn](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | hovedtårnet slik replayen sender det; `turretYaw` / `gunPitch` er det holdt til tårndrevets fart og satt til hver hovedkanons skuddlinje (se [Tårn](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | dit spilleren ser (sikter med kameraet) i verden: kompassgrader (0 nord, med klokken) og grader opp, samme konvensjon som `aimHeading` / `aimPitch` (i motsetning til `turretYaw` / `gunPitch`, som forblir relative til skroget). Hver spillers stridsvogn i en serverreplay, opptakspilotens egen i en klientreplay; tom der spilleren ikke sikter noe sted (alle fire siktflyttall 0). Tårnet følger den i sin egen dreiehastighet, så de to skiller seg mens det dreier (se [Tårn](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | opptakspilotens egen stridsvogn: hvor den sikter (kompassgrader, grader opp, avstanden i m; 2000 når ingenting er i sikten); kamerarader: hvor spilleren sikter (retning, stigning) |
| `zoom` | kamerarader: kameraets forstørrelse (se [Kameraet](ground.md#the-camera)) |
| `difficulty`, `gameMode` | slagets `AB`, `RB` eller `SB`, og `ground`, `air` eller `naval`, på hver rad (se [Kampmodus](ground.md#battle-mode)) |
| `extrapolated` | en flyprøve som er klientens dead reckoning, ikke en tilstand den mottok (se [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); en bombes prøve regnet ut fra slippet (se Bomber uten flygeposter i [Slik leser den en replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | hvor langt utjevneren flyttet samplet (m), og replayens egen posisjon og holdning (rull i tabellens fortegn) |
| `targetX`, `targetY`, `targetZ` | en `shot`s treffpunkt |
| `hitOutcome`, `hitFlags` | en `shot`s utfall på en bakkeenhet: `kill`, `critical`, `penetration` eller `nonpenetration` (avvist eller stoppet: replayen skiller ikke en rikosjett), fra bitene serveren sender med treffet (`hitFlags`, rå); tom der ingen sendes (fly, skip). Se [Utfall av treff](hits.md#hit-outcomes) |
| `hitShell` | en `shot`s granatsignatur: fire byte fra treffmeldingen (rå hex); én signatur kan stå for ulike granater (120 og 125 mm APFSDS deler én), så den beholdes rå, ikke lest som kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | en `shot`s ammunisjon: dens type (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) og ID (`125mm_3bm46`) der et drap navngir skytterens plass, ellers `explosive` (treffskuddet) eller `kinetic`; kanonens `våpen/plass` fra dens omlastinger; kaliberen i mm fra installasjonens våpenfiler. Se [Utfall av treff](hits.md#hit-outcomes) |
| `rpm` | et flys motoromdreininger (gjennomsnittet over dets motorer) som sist sendt, innen 2 s |
| `vx`, `vy`, `vz` | et flys hastighet slik dets flyinngang sender den (m/s, spillets akser; fart over 500 m/s leses som 500) |
| `engine`, `afterburner`, `engineCondition` | et flys motorer fra dets flyinngang: `off`, `starting`, `running`, `dead` (`/`-skilt når motorene er ulike); etterbrenneren 0-1; en byte sendt bare etter at motoren ble truffet |
| `weaponName` | drap og dødsfall: våpenet eller ammunisjonen på din installasjons engelsk (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | bare opptakspilotens fly: gassen 0-1,1 fra dets cockpit (1,1 for krigsnødeffekt eller etterbrenner; ellers dets flyinngangs femtendedeler), kontrollene -1..1 fra dets flyinngang (høyderor positiv når det trekkes, krengeror positiv når det ruller til høyre), rundene igjen per våpen (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | bare opptakspilotens fly, fra dets cockpit: indikert lufthastighet og stigehastighet (m/s), drivstoff, ladetrykk (atm), landingsstell (0-1, 1 nede), olje- og sylinderhodetemperatur, der dets cockpit har måleren |
| `speed` | m/s over ca. to sekunder av sporet (regnet ut her; replayen sender ingen fart for andre enheter) |
| `alive` | 0 for en enhets samples etter dens død (dens vrak): en bakkeenhets eller skips til spillet fjerner den eller dens samples slutter, et flys i høyst 60 s |
| `otherVehicle`, `otherLife` | en `shot`s offer: dets kjøretøy og dets `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | en `shot`s treffpunkt i offerets egen ramme (m; x forover, y opp, z venstre; se [Meldinger til enheter](how-it-reads.md#messages-to-units)) og veien skuddet kom, dreiet inn i den rammen av offerets holdning da |
| `hitPart`, `hitFlag` | en `shot`s treffmelding: dens delord slik det ble sendt, og dens høye byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | hva slaget kostet og tjente, og hvem som vant: se [Økonomi](economy.md) |
| `other`, `weapon` | drap: den andre siden og våpenet; treff: hvem som traff (fra postens uid, ellers dens spillerplass), deres kjøretøy; oppskytinger: våpenet; ødelagte moduler: hvem som sist traff enheten innen 5 s før, og `part <n>` |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
