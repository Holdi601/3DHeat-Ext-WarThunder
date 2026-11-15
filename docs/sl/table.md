---
title: Tabela
nav_order: 6
lang: "sl"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabela {#the-table}

![Tabela sintetičnega posnetka, povzeta](../assets/img/table.svg)

Ena vrstica na vzorec ali dogodek, 105 stolpcev ([Seznam stolpcev](../columns.md), ustvarjen iz kode); v nogi, pod `heat3d`,
navodila za branje pregledovalnika, tako da pregledovalnik ne potrebuje izpolnjenega obrazca.

| Stolpec | Kaj |
|---|---|
| `time` | sekunde po posnetkovi lastni uri |
| `event` | `position`; vrstice dogodkov ležijo na poti ob svojem trenutku (med dvema vzorcema, na črti med njima); `kill` (pri ubijalcu), `death` (pri žrtvi), `hit_critical` / `hit_severe` (pri zadeti enoti), `module_destroyed` (pri enoti), `launch` (pri enoti, ki je izpustila orožje), `impact` (zadnji vzorec orožja, ko je bilo odstranjeno takoj po tem); `explosion` in `flak` (0xD08E, 0xD01F) na svojem položaju, vrsta `effect`, brez poti, s smerjo eksplozije, kjer jo ima; `shot` (izstrelek, ki je zadel, pri strelcu), `gun_shot`, `fire_start`, `fire_stop` (rafal topa, ne vozilo v ognju), `fire_on`, `fire_off` (vozilo v ognju, glejte [Požari vozil](hits.md#vehicle-fires)), `reward` (zaslužen Silver Lions in točke raziskav, glejte [Gospodarstvo](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (glejte [Sporočila enotam](how-it-reads.md#messages-to-units)); `despawn`: zadnja vrstica poti, katere enota je izginila, preden se posnetek konča (glejte [Konec poti](ground.md#end-of-a-track)) |
| `track` | kar pregledovalnik riše kot eno stvar: eno življenje enote ali let enega orožja - `<player or vehicle> #<hex>` (pregledovalnik prikaže ime brez dela `#`) |
| `x`, `y`, `z` | igrini metri: x vzhod, y gor, z sever (namigi zrcalijo z, zato sever ni narisan na jug) |
| `player` | ime igralca; enota AI `<VehicleName> #<uid>` (na primer `F-15A #204`); `uid <n>`, kadar je ne poimenuje nič; za orožje, kdo ga je izpustil |
| `userId`, `team` | Gaijin id igralca in ekipa (`1`, `2`) |
| `ai`, `isPlayer` | `ai` je true za vsako enoto, ki je ne vodi noben igralski račun (enote misije, letala AI, tarče na kopnem, protiletalski topovi, ladje brez igralca, nadomestki), `isPlayer` je nasprotno: igralec je enota, katere entiteta navaja režo igralca z Gaijin id-jem. Orožje ima tistega, ki ga je izstrelil; prazno, kadar ni znano |
| `match` | identifikator tekme (`match` dokumenta tekme), na vsaki vrstici; namigi ga preslikajo kot sejo, zato se dva naložena posnetka nikoli ne zlijeta v poti |
| `life` | `uid#n`: pot ene enote, prekinjena tam, kjer uid preide na drugo enoto, enota se premakne hitreje, kot lahko (ponovni pojav, ponovno oborožitev, igra jo premakne, odjemalec popravi oddaljeno enoto; glejte Teleportacije v [Kako bere posnetek](how-it-reads.md#what-is-read-and-the-check)) ali je dolgo ni bilo videti; `w<hex>` let orožja (`w<hex>#n` po prerezu) |
| `uid` | id enote v posnetku |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvaj ali železniški vagon, ki ga postavi stopnja, glejte [Scenske enote](objectives.md#scene-units-trams-and-rail-wagons)); orožja `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` nadomestna kamera igralca, ki je snemal (glejte [Kamera](ground.md#the-camera)) |
| `type` | igrin lastni tip, kjer ga rezultati navajajo (`fighter`, `assault`, `destroyer`, `gun_boat`), sicer kot `kind` |
| `Vehicle` | igrin identifikator vozila (`f_15a`, `germ_flakpz_I_Gepard`), s katerim se ujemajo figure pregledovalnika |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | angleško ime vozila iz lokalizacije vaše namestitve (`Pz.Kpfw. III Ausf. J1`, kratko `Pz.III J1`) in njegov ključ (`germ_pzkpfw_III_ausf_J_0`); oznake držav pisave igre so izpuščene. Kjer igra ničesar ne poimenuje ali namestitev ni najdena, je ime identifikator, ključ pa prazen |
| `mission` | ime enote v misiji (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kam enota kaže (vektor pogleda): letala iz drže modela leta, kopenske enote in ladje iz njihove lastne, orožja vzdolž njihovega leta |
| `heading`, `pitch`, `roll` | isto v stopinjah; smer je kompas, v smeri urnega kazalca od severa, naklon nos gor pozitiven, zvitek desno krilo navzdol pozitiven (model leta pošilja nasprotni predznak, glejte [Preverjena drža](aircraft.md#attitude-checked); spodnja desna stran kopenske enote). Namigi to povedo pod `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | glavni stolp tanka - kam kaže top, ne kam gleda njegov igralec; vrednost posnetka, omejena na hitrost pogona stolpa in nastavljena na črto vsakega strela glavnega topa (glejte [Strelski stolpi](ground.md#turrets)): njegov vodoravni kot glede na trup (stopinje, v smeri urnega kazalca gledano od zgoraj pozitivno, 0 naravnost naprej) in naklon njegovega topa glede na trup (stopinje, navzgor pozitivno); `turrets` vsak stolp vozila kot `yaw pitch;yaw pitch;...` v svojem vrstnem redu (neuporabljena reža prebere `0.00 0.00`). Tanki, SPAA, oklepniki in tovornjaki, v posnetkih odjemalca in strežnika; ne ladje (glejte [Strelski stolpi](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | glavni stolp, kot ga posnetek pošlje; `turretYaw` / `gunPitch` sta omejena na hitrost pogona stolpa in nastavljena na črto vsakega strela glavnega topa (glejte [Strelski stolpi](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kam igralec gleda (cilja s kamero) v svetu: stopinje kompasa (0 sever, v smeri urnega kazalca) in stopinje navzgor, ista konvencija kot `aimHeading` / `aimPitch` (za razliko od `turretYaw` / `gunPitch`, ki ostajata glede na trup). Tank vsakega igralca v strežniškem posnetku, v posnetku odjemalca pa lastni tank igralca, ki je snemal; prazno, kjer igralec nikamor ne cilja (vseh štirje plavajoči cilji 0). Stolp mu sledi s svojo hitrostjo obračanja, zato se ob vrtenju razlikujeta (glejte [Strelski stolpi](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | lastni tank igralca, ki je snemal: kam cilja (stopinje kompasa, stopinje navzgor, razdalja v m; 2000, kadar v nišanu ni nič); vrstice kamere: kam igralec cilja (smer, naklon) |
| `zoom` | vrstice kamere: povečava kamere (glejte [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` ali `SB` bitke ter `ground`, `air` ali `naval`, na vsaki vrstici (glejte [Način bitke](ground.md#battle-mode)) |
| `extrapolated` | vzorec letala, ki je mrtvo računanje odjemalca, ne stanje, ki bi ga prejel (glejte [Mrtvo računanje](aircraft.md#dead-reckoning-and-the-smoother)); vzorec bombe, izračunan iz njenega izpusta (glejte Bombe brez zapisov leta v [Kako bere posnetek](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | za koliko je zglajevalnik premaknil vzorec (m), ter lastni položaj in drža posnetka (zvitek v predznaku tabele) |
| `targetX`, `targetY`, `targetZ` | točka zadetka vrstice `shot` |
| `hitOutcome`, `hitFlags` | izid `shot` na kopenski enoti: `kill`, `critical`, `penetration` ali `nonpenetration` (odbito ali ustavljeno: posnetek ne ločuje odboja), iz bitov, ki jih strežnik pošlje z zadetkom (`hitFlags`, surovo); prazno, kjer se ne pošlje (letala, ladje). Glejte [Izidi zadetkov](hits.md#hit-outcomes) |
| `hitShell` | podpis izstrelka `shot`: štirje bajti sporočila o zadetku (surovo šestnajstiško); en podpis lahko pomeni različne izstrelke (120 in 125 mm APFSDS delita enega), zato se hrani surovo, ne bere kot kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | strelivo `shot`: njegov tip (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) in identifikator (`125mm_3bm46`), kjer ubijanje navaja režo strelca, sicer `explosive` (rafal zadetka) ali `kinetic`; `weapon/slot` topa iz njegovih nabojev; kaliber v mm iz datotek orožij namestitve. Glejte [Izidi zadetkov](hits.md#hit-outcomes) |
| `rpm` | vrtljaji motorja letala (povprečje njegovih motorjev), kot so bili nazadnje poslani, v 2 s |
| `vx`, `vy`, `vz` | hitrost letala, kot jo pošlje njegov vnos letenja (m/s, osi igre; hitrosti nad 500 m/s se preberejo kot 500) |
| `engine`, `afterburner`, `engineCondition` | motorji letala iz njegovega vnosa letenja: `off`, `starting`, `running`, `dead` (z `/` povezano, kadar se njegovi motorji razlikujejo); post-zgorevanje 0-1; bajt, poslan samo potem, ko je bil motor zadet |
| `weaponName` | ubijanja in smrti: orožje ali strelivo v angleščini vaše namestitve (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | samo letalo igralca, ki je snemal: plin 0-1,1 iz njegove kabine (1,1 vojni nujni režim ali post-zgorevanje; sicer petnajstinke iz njegovega vnosa letenja), krmiljenje -1..1 iz njegovega vnosa letenja (višinsko krmilo pozitivno pri vleku, krilca pozitivno pri zvijanju desno), preostali naboji po orožju (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | samo letalo igralca, ki je snemal, iz njegove kabine: prikazana zračna hitrost in hitrost vzpenjanja (m/s), gorivo, tlak v sesalni cevi (atm), podvozje (0-1, 1 spuščeno), temperatura olja in glave valjev, kjer ima kabina merilnik |
| `speed` | m/s čez približno dve sekundi poti (izračunano tukaj; posnetek ne pošlje hitrosti za druge enote) |
| `alive` | 0 za vzorce enote po njeni smrti (njena olupina): kopenske enote in ladje, dokler jo igra ne odstrani ali se njeni vzorci ne končajo, letala največ 60 s |
| `otherVehicle`, `otherLife` | žrtev `shot`: njeno vozilo in njeno `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | točka zadetka `shot` v lastnem okviru žrtve (m; x naprej, y gor, z levo; glejte [Sporočila enotam](how-it-reads.md#messages-to-units)) in smer, s katero je strel prišel, preoblikovana v ta okvir s takratno držo žrtve |
| `hitPart`, `hitFlag` | sporočilo o zadetku `shot`: njegova beseda dela, kot je poslana, in njen visoki bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | koliko je bitka stala in koliko prinesla ter kdo je zmagal: glejte [Gospodarstvo](economy.md) |
| `other`, `weapon` | ubijanja: druga stran in orožje; zadetki: kdo je zadel (iz uid-ja zapisa, sicer iz njegove reže igralca), njihovo vozilo; izstrelitve: orožje; uničeni moduli: kdo je enoto nazadnje zadel v 5 s pred tem, in `part <n>` |

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
