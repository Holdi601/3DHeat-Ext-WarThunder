---
title: "It-tabella"
nav_order: 6
lang: mt
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# It-tabella {#the-table}

![It-tabella ta' ripetizzjoni sintetika, fil-qosor](../assets/img/table.svg)

Ringiela waħda għal kull kampjun jew avveniment, 105 kolonni ([Lista tal-kolonni](../columns.md), iġġenerata mill-kodiċi); fit-tarf, taħt `heat3d`, hemm l-istruzzjonijiet tal-qari tal-viewer, biex il-viewer ma jkollu bżonn jimla ebda formola.

| Kolonna | X'inhi |
|---|---|
| `time` | sekondi fuq l-arloġġ proprju tar-ripetizzjoni |
| `event` | `position`; ir-ringieli tal-avvenimenti jinsabu fuq il-mogħdija fil-mument tagħhom (bejn żewġ kampjuni, fuq il-linja bejniethom); `kill` (fil-qattiel), `death` (fil-vittma), `hit_critical` / `hit_severe` (fl-unità li nħabtet), `module_destroyed` (fl-unità), `launch` (fl-unità li rrilaxxat arma), `impact` (l-aħħar kampjun ta' arma meta tneħħiet minnufih wara); `explosion` u `flak` (0xD08E, 0xD01F) fil-pożizzjoni tagħhom, tip `effect`, ebda mogħdija, bid-direzzjoni tal-isplużjoni fejn ikollha waħda; `shot` (projettil li laqat, fix-xutter), `gun_shot`, `fire_start`, `fire_stop` (sensiela ta' kanun, mhux vettura tinxtegħel), `fire_on`, `fire_off` (vettura tinxtegħel, ara [Vehicle fires](hits.md#vehicle-fires)), `reward` (Silver Lions u punti tar-riċerka mqalgħa, ara [Ekonomija](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (ara [Messages to units](how-it-reads.md#messages-to-units)); `despawn`: l-aħħar ringiela ta' mogħdija li l-unità tagħha marret qabel it-tmiem tar-ripetizzjoni (ara [End of a track](ground.md#end-of-a-track)) |
| `track` | dak li l-viewer jiżżebgħa bħala ħaġa waħda: ħajja waħda ta' unità, jew titjira waħda ta' arma - `<player or vehicle> #<hex>` (il-viewer juri l-isem mingħajr il-parti `#`) |
| `x`, `y`, `z` | il-metri tal-logħba: x lvant, y 'il fuq, z tramuntana (is-suġġerimenti jirriflettu z, biex it-tramuntana ma tiġix imżebgħa fin-nofsinhar) |
| `player` | l-isem tal-plejer; unità AI `<VehicleName> #<uid>` (pereżempju `F-15A #204`); `uid <n>` meta xejn ma jsemmiha; għal arma, min irrilaxxaha |
| `userId`, `team` | l-id tal-plejer ta' Gaijin u t-tim (`1`, `2`) |
| `ai`, `isPlayer` | `ai` veru għal kull unità li ebda kont ta' plejer ma jsuq (unitajiet tal-missjoni, ajruplani AI, miri tal-art, kanuni AA, vapuri mingħajr plejer, placeholders), `isPlayer` l-oppost: plejer huwa unità li l-entità tagħha tagħti isem lil slot ta' plejer b'id ta' Gaijin. Arma għandha dak tal-launcher tagħha; vojt meta mhux magħruf |
| `match` | l-id tal-partita (il-`match` tad-dokument tal-partita), fuq kull ringiela; is-suġġerimenti jqabbluh mas-sessjoni, biex żewġ ripetizzjonijiet ikkargati ma jgħaqqdux qatt mogħdijiet |
| `life` | `uid#n`: mogħdija ta' unità waħda, maqtugħa fejn l-uid jgħaddi għal unità oħra, l-unità tiċċaqlaq aktar malajr milli tista' (respawn, rearm, il-logħba tċaqlaqha, il-klijent jikkoreġi unità 'l bogħod; ara Teleports f'[Kif taqra ripetizzjoni](how-it-reads.md#what-is-read-and-the-check)) jew ma tidhirx għal żmien twil; `w<hex>` titjira ta' arma (`w<hex>#n` wara qtugħ) |
| `uid` | l-id tal-unità fir-ripetizzjoni |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tram jew vagun tal-ferrovija li l-livell iqiegħed, ara [Scene units](objectives.md#scene-units-trams-and-rail-wagons)); armi `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` il-kamera tar-ripetizzjoni tal-plejer li rreġistra (ara [The camera](ground.md#the-camera)) |
| `type` | it-tip proprju tal-logħba fejn ir-riżultati jisimuh (`fighter`, `assault`, `destroyer`, `gun_boat`), inkella bħal `kind` |
| `Vehicle` | l-id tal-vettura tal-logħba (`f_15a`, `germ_flakpz_I_Gepard`), li l-figuri tal-viewer jaqblu miegħu |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | l-isem Ingliż tal-vettura mil-lokalizzazzjoni tal-installazzjoni tiegħek (`Pz.Kpfw. III Ausf. J1`, qasir `Pz.III J1`) u ċ-ċavetta tagħha (`germ_pzkpfw_III_ausf_J_0`); is-sinjali tal-pajjiż tal-font tal-logħba jitħallew barra. Fejn il-logħba ma tagħti l-ebda isem, jew ma tinstab ebda installazzjoni, l-isem huwa l-id u ċ-ċavetta vojta |
| `mission` | l-isem tal-unità fil-missjoni (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | fejn tipponta l-unità (il-vettur tal-ħarsa): ajruplani mill-attitudni tal-flight model, unitajiet tal-art u vapuri mill-attitudni tagħhom, armi tul it-titjira tagħhom |
| `heading`, `pitch`, `roll` | l-istess f'gradi; heading huwa l-kumpass, 'l quddiem mat-tramuntana, pitch imnieħer 'il fuq pożittiv, roll ġewnaħ il-lemin 'l isfel pożittiv (il-flight model jibgħat is-sinjal opposti, ara [Attitude, checked](aircraft.md#attitude-checked); in-naħa tal-lemin 'l isfel ta' unità tal-art). Is-suġġerimenti jgħidu hekk taħt `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | it-turret ewlenija ta' tank - fejn tipponta l-kanun, mhux fejn tħares il-plejer; il-valur tar-ripetizzjoni miżmum mal-veloċità tad-drive tat-turret u mqiegħed fuq il-linja ta' kull sparatura tal-kanun ewlieni (ara [Turrets](ground.md#turrets)): il-yaw tagħha relattiv għall-iskoss (gradi, 'l quddiem mal-arloġġ meta mqabbla minn fuq pożittiv, 0 dritt 'il quddiem) u l-pitch tal-kanun tagħha relattiv għall-iskoss (gradi, 'il fuq pożittiv); `turrets` kull turret tal-vettura bħala `yaw pitch;yaw pitch;...` fl-ordni tagħha stess (slot mhux użat jinqara `0.00 0.00`). Tankijiet, SPAA, APCs u trakkijiet, f'ripetizzjonijiet tal-klijent u tas-server; mhux vapuri (ara [Turrets](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | it-turret ewlenija kif tibgħatha r-ripetizzjoni; `turretYaw` / `gunPitch` huma hi miżmuma mal-veloċità tad-drive tat-turret u mqiegħda fuq il-linja ta' kull sparatura tal-kanun ewlieni (ara [Turrets](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | fejn iħares il-plejer (jimmira bil-kamera) fid-dinja: gradi tal-kumpass (0 tramuntana, 'l quddiem mal-arloġġ) u gradi 'il fuq, l-istess konvenzjoni bħal `aimHeading` / `aimPitch` (mhux bħal `turretYaw` / `gunPitch`, li jibqgħu relattivi għall-iskoss). It-tank ta' kull plejer f'ripetizzjoni tas-server, dak tal-plejer li rreġistra f'ripetizzjoni tal-klijent; vojt fejn il-plejer ma jimmira lejn imkien (l-erba' floats tal-aim kollha 0). It-turret issegwih bil-veloċità tat-traverse tagħha stess, għalhekk it-tnejn ivarjaw waqt li ddur (ara [Turrets](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | it-tank proprju tal-plejer li rreġistra: fejn jimmira (gradi tal-kumpass, gradi 'il fuq, id-distanza f'm; 2000 meta xejn mhu fil-mira); ringieli tal-kamera: fejn jimmira l-plejer (heading, pitch) |
| `zoom` | ringieli tal-kamera: l-ingrandiment tal-kamera (ara [The camera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` jew `SB` tal-battalja, u `ground`, `air` jew `naval`, fuq kull ringiela (ara [Battle mode](ground.md#battle-mode)) |
| `extrapolated` | kampjun ta' ajruplan li huwa d-dead reckoning tal-klijent, mhux stat li rċieva (ara [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); kampjun ta' bomba ikkalkulat mir-rilaxx tagħha (ara Bombs without flight records f'[Kif taqra ripetizzjoni](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | kemm ċaqlaq is-smoother il-kampjun (m), u l-pożizzjoni u l-attitudni proprji tar-ripetizzjoni (roll bis-sinjal tat-tabella) |
| `targetX`, `targetY`, `targetZ` | il-punt tad-daqqa ta' `shot` |
| `hitOutcome`, `hitFlags` | ir-riżultat ta' `shot` fuq unità tal-art: `kill`, `critical`, `penetration` jew `nonpenetration` (qabeż lura jew waqaf: ir-ripetizzjoni ma tifridx ricochet), mill-bits li s-server jibgħat mad-daqqa (`hitFlags`, raw); vojt fejn ebda ma tintbagħat (ajruplani, vapuri). Ara [Hit outcomes](hits.md#hit-outcomes) |
| `hitShell` | is-firma tal-qoxra ta' `shot`: erba' bytes tal-messaġġ tad-daqqa (hex raw); firma waħda tista' tirrappreżenta qxur differenti (120 u 125 mm APFSDS jaqsmu waħda), għalhekk tinżamm raw, mhux moqrija bħala kalibru |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | il-munizzjon ta' `shot`: it-tip tiegħu (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) u l-id (`125mm_3bm46`) fejn qtil jagħti isem lis-slot tax-xutter, inkella `explosive` (l-isplużjoni tad-daqqa) jew `kinetic`; il-`weapon/slot` tal-kanun mir-reloads tiegħu; il-kalibru f'mm mill-fajls tal-armi tal-installazzjoni. Ara [Hit outcomes](hits.md#hit-outcomes) |
| `rpm` | rpm tal-magna ta' ajruplan (il-medja fuq il-magni tiegħu) kif intbagħtet l-aħħar, fi ħdan 2 s |
| `vx`, `vy`, `vz` | il-veloċità ta' ajruplan kif tibgħatha d-daħla tat-titjira tiegħu (m/s, l-assi tal-logħba; veloċitajiet 'il fuq minn 500 m/s jinqraw 500) |
| `engine`, `afterburner`, `engineCondition` | il-magni ta' ajruplan mid-daħla tat-titjira tiegħu: `off`, `starting`, `running`, `dead` (marbutin b'`/` meta l-magni tiegħu jvarjaw); l-afterburner 0-1; byte mibgħut biss wara li l-magna nħabtet |
| `weaponName` | qtil u imwiet: l-arma jew il-munizzjon bl-Ingliż tal-installazzjoni tiegħek (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | l-ajruplan tal-plejer li rreġistra biss: it-throttle 0-1.1 mill-cockpit tiegħu (1.1 war emergency power jew afterburner; inkella l-ħmistax-il parti tad-daħla tat-titjira tiegħu), il-kontrolli -1..1 mid-daħla tat-titjira tiegħu (elevator pożittiv jiġbed, aileron pożittiv jirrombla lejn il-lemin), ir-rawnds li fadal għal kull arma (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | l-ajruplan tal-plejer li rreġistra biss, mill-cockpit tiegħu: veloċità indikata u rata ta' tlugħ (m/s), fjuwil, manifold pressure (atm), gear (0-1, 1 'l isfel), temperatura taz-zejt u tar-ras tas-silindru, fejn il-cockpit tiegħu għandu l-kejl |
| `speed` | m/s fuq madwar żewġ sekondi tal-mogħdija (ikkalkulata hawn; ir-ripetizzjoni ma tibgħat ebda veloċità għal unitajiet oħra) |
| `alive` | 0 għall-kampjuni ta' unità wara l-mewt tagħha (il-wreck): ta' unità tal-art jew vapur sakemm il-logħba tneħħiha jew il-kampjuni tagħha jispiċċaw, ta' ajruplan l-iktar 60 s |
| `otherVehicle`, `otherLife` | il-vittma ta' `shot`: il-vettura u l-`life` tagħha |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | il-punt tad-daqqa ta' `shot` fil-qafas proprju tal-vittma (m; x 'il quddiem, y 'il fuq, z lejn ix-xellug; ara [Messages to units](how-it-reads.md#messages-to-units)) u t-triq li ġiet id-daqqa, mibdula f'dak il-qafas bl-attitudni tal-vittma dak il-ħin |
| `hitPart`, `hitFlag` | il-messaġġ tad-daqqa ta' `shot`: il-kelma tal-parti kif intbagħtet, u l-byte għoli tagħha |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | x'kellfet u x'qalgħet il-battalja, u min rebaħ: ara [Ekonomija](economy.md) |
| `other`, `weapon` | qtil: in-naħa l-oħra u l-arma; daqqiet: min laqat (mill-uid tar-record, inkella mis-slot tal-plejer tiegħu), il-vettura tiegħu; launches: l-arma; moduli meqruda: min laqat l-unità l-aħħar fi ħdan 5 s qabel, u `part <n>` |

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
