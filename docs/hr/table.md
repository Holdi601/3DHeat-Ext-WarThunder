---
title: Tablica
nav_order: 6
lang: hr
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tablica {#the-table}

![Tablica sintetičke snimke, sažeto](../assets/img/table.svg)

Jedan redak po uzorku ili događaju, 105 stupaca ([Popis stupaca](../columns.md), generiran iz koda); u podnožju,
pod `heat3d`, upute čitanja za preglednik, pa pregledniku ne treba ništa popunjavati.

| Stupac | Što |
|---|---|
| `time` | sekunde na vlastitom satu snimke |
| `event` | `position`; retci događaja leže na putanji u svom trenutku (između dva uzorka, na pravcu među njima); `kill` (kod ubojice), `death` (kod žrtve), `hit_critical` / `hit_severe` (kod pogođene jedinice), `module_destroyed` (kod jedinice), `launch` (kod jedinice koja je ispustila oružje), `impact` (zadnji uzorak oružja kad je uklonjeno odmah nakon); `explosion` i `flak` (0xD08E, 0xD01F) na svom položaju, vrsta `effect`, bez putanje, sa smjerom eksplozije gdje ga ima; `shot` (projektil koji je pogodio, kod strijelca), `gun_shot`, `fire_start`, `fire_stop` (rafal topa, a ne vozilo u plamenu), `fire_on`, `fire_off` (vozilo u plamenu, vidi [Požari vozila](hits.md#vehicle-fires)), `reward` (zarađeni Silver Lions i bodovi za istraživanje, vidi [Ekonomija](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (vidi [Poruke jedinicama](how-it-reads.md#messages-to-units)); `despawn`: zadnji redak putanje čija je jedinica nestala prije kraja snimke (vidi [Kraj putanje](ground.md#end-of-a-track)) |
| `track` | ono što preglednik crta kao jednu stvar: jedan život jedinice ili let jednog oružja - `<player or vehicle> #<hex>` (preglednik prikazuje naziv bez dijela `#`) |
| `x`, `y`, `z` | metri igre: x istok, y gore, z sjever (napomene zrcale z, pa sjever nije nacrtan kao jug) |
| `player` | ime igrača; AI jedinica `<VehicleName> #<uid>` (na primjer `F-15A #204`); `uid <n>` kad ništa ne imenuje; za oružje, tko ga je ispustio |
| `userId`, `team` | Gaijin id igrača i tim (`1`, `2`) |
| `ai`, `isPlayer` | `ai` je true za svaku jedinicu koju nijedan igračev račun ne vodi (misijske jedinice, AI zrakoplovi, kopnene mete, protuzračni topovi, brodovi bez igrača, zamjenici), `isPlayer` je obrnuto: igrač je jedinica čiji entitet imenuje utor igrača s Gaijin id-om. Oružje ima onoga od lansera; prazno kad nije poznato |
| `match` | id meča (`match` dokumenta meča), na svakom retku; napomene ga preslikavaju kao sesiju, pa dvije učitane snimke nikad ne spajaju putanje |
| `life` | `uid#n`: putanja jedne jedinice, presječena tamo gdje uid prelazi na drugu jedinicu, jedinica se pomakne brže nego što može (ponovno pojavljivanje, ponovno punjenje, igra ju je pomaknula, klijent je korigirao udaljenu jedinicu; vidi Teleportacije u [Kako se snimka čita](how-it-reads.md#what-is-read-and-the-check)) ili je dugo nije bilo vidjeti; `w<hex>` let oružja (`w<hex>#n` nakon reza) |
| `uid` | id jedinice u snimci |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvaj ili željeznički vagon koji razina postavlja, vidi [Scenske jedinice](objectives.md#scene-units-trams-and-rail-wagons)); oružje `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` replay kamera igrača koji snima (vidi [Kamera](ground.md#the-camera)) |
| `type` | igrina vlastita vrsta gdje je rezultati imenuju (`fighter`, `assault`, `destroyer`, `gun_boat`), inače kao `kind` |
| `Vehicle` | igrin id vozila (`f_15a`, `germ_flakpz_I_Gepard`), prema kojem se podudaraju preglednikove figure |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | engleski naziv vozila iz lokalizacije tvoje instalacije (`Pz.Kpfw. III Ausf. J1`, kratki `Pz.III J1`) i njegov ključ (`germ_pzkpfw_III_ausf_J_0`); oznake država iz igrinog fonta su izostavljene. Gdje igra ništa ne imenuje, ili instalacija nije nađena, naziv je id, a ključ prazan |
| `mission` | naziv jedinice u misiji (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kamo jedinica gleda (vektor pogleda): zrakoplovi iz stava modela leta, kopnene jedinice i brodovi iz vlastitog, oružje duž svojeg leta |
| `heading`, `pitch`, `roll` | isto u stupnjevima; smjer je kompas, u smjeru kazaljke od sjevera, nagib pozitivan kad nos ide gore, valjanje pozitivno kad je desno krilo dolje (model leta šalje suprotan predznak, vidi [Stav, provjereno](aircraft.md#attitude-checked); bočna strana kopnene jedinice desno dolje). Napomene to kažu pod `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | glavni toranj tenka - kamo top gleda, a ne kamo igrač gleda; vrijednost snimke držana na brzini pogona tornja i postavljena na pravac svakog hica glavnim topom (vidi [Tornjevi](ground.md#turrets)): njegov zakret u odnosu na trup (stupnjevi, pozitivno u smjeru kazaljke gledano odozgo, 0 ravno naprijed) i nagib njegova topa u odnosu na trup (stupnjevi, pozitivno gore); `turrets` svaki toranj vozila kao `yaw pitch;yaw pitch;...` njegovim redom (neiskorišten utor glasi `0.00 0.00`). Tenkovi, SPAA, APC i kamioni, u snimkama klijenta i poslužitelja; ne brodovi (vidi [Tornjevi](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | glavni toranj kako ga snimka šalje; `turretYaw` / `gunPitch` su on držan na brzini pogona tornja i postavljen na pravac svakog hica glavnim topom (vidi [Tornjevi](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kamo igrač gleda (cilja kamerom) u svijetu: stupnjevi kompasa (0 sjever, u smjeru kazaljke) i stupnjevi gore, ista konvencija kao `aimHeading` / `aimPitch` (za razliku od `turretYaw` / `gunPitch`, koji ostaju u odnosu na trup). Tenk svakog igrača u poslužiteljskoj snimci, vlastiti tenk igrača koji snima u snimci klijenta; prazno gdje igrač ne cilja nigdje (sva četiri plutajuća broja cilja 0). Toranj ga prati vlastitom brzinom zakreta, pa se dvije vrijednosti razlikuju dok se on okreće (vidi [Tornjevi](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | vlastiti tenk igrača koji snima: kamo cilja (stupnjevi kompasa, stupnjevi gore, udaljenost u m; 2000 kad ništa nije u nišanu); retci kamere: kamo igrač cilja (smjer, nagib) |
| `zoom` | retci kamere: uvećanje kamere (vidi [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` ili `SB` bitke, i `ground`, `air` ili `naval`, na svakom retku (vidi [Način bitke](ground.md#battle-mode)) |
| `extrapolated` | uzorak zrakoplova koji je mrtvi račun klijenta, a ne stanje koje je primio (vidi [Mrtvi račun](aircraft.md#dead-reckoning-and-the-smoother)); uzorak bombe izračunat iz njezina ispuštanja (vidi Bombe bez zapisa leta u [Kako se snimka čita](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | koliko je izglađivač pomaknuo uzorak (m), i vlastiti položaj i stav snimke (valjanje u predznaku tablice) |
| `targetX`, `targetY`, `targetZ` | točka pogotka `shot`-a |
| `hitOutcome`, `hitFlags` | ishod `shot`-a na kopnenoj jedinici: `kill`, `critical`, `penetration` ili `nonpenetration` (odbijen ili zaustavljen: snimka ne razlikuje odbijanje), iz bitova koje poslužitelj šalje uz pogodak (`hitFlags`, sirovo); prazno gdje se ništa ne šalje (zrakoplovi, brodovi). Vidi [Ishodi pogodaka](hits.md#hit-outcomes) |
| `hitShell` | potpis granate `shot`-a: četiri bajta poruke pogotka (sirovi heks); jedan potpis može značiti različite granate (120 i 125 mm APFSDS dijele jedan), pa se čuva sirov, ne čita kao kalibar |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | streljivo `shot`-a: njegova vrsta (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) i id (`125mm_3bm46`) gdje ubojstvo imenuje utor strijelca, inače `explosive` (rafal pogotka) ili `kinetic`; `weapon/slot` topa iz njegova punjenja; kalibar u mm iz datoteka oružja instalacije. Vidi [Ishodi pogodaka](hits.md#hit-outcomes) |
| `rpm` | okretaji motora zrakoplova (prosjek preko njegovih motora) kako su zadnje poslani, unutar 2 s |
| `vx`, `vy`, `vz` | brzina zrakoplova kako je šalje njegov unos leta (m/s, osi igre; brzine preko 500 m/s čitaju se kao 500) |
| `engine`, `afterburner`, `engineCondition` | motori zrakoplova iz njegova unosa leta: `off`, `starting`, `running`, `dead` (spojeno s `/` kad se motori razlikuju); naknadno izgaranje 0-1; bajt poslan tek nakon što je motor pogođen |
| `weaponName` | ubojstva i smrti: oružje ili streljivo na engleskom iz tvoje instalacije (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | samo zrakoplov igrača koji snima: gas 0-1,1 iz njegove kabine (1,1 ratno pojačanje ili naknadno izgaranje; inače petnaestine iz njegova unosa leta), upravljanje -1..1 iz njegova unosa leta (visina pozitivna pri povlačenju, krilca pozitivna pri valjanju udesno), preostali meci po oružju (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | samo zrakoplov igrača koji snima, iz njegove kabine: indicirana brzina zraka i brzina penjanja (m/s), gorivo, tlak usisne grane (atm), podvozje (0-1, 1 spušteno), temperatura ulja i glave cilindra, gdje njegova kabina ima brojčanik |
| `speed` | m/s preko otprilike dvije sekunde putanje (izračunato ovdje; snimka ne šalje brzinu za druge jedinice) |
| `alive` | 0 za uzorke jedinice nakon njezine smrti (njezina olupina): kopnene jedinice i brodova dok je igra ne ukloni ili dok njihovi uzorci ne završe, zrakoplova najviše 60 s |
| `otherVehicle`, `otherLife` | žrtva `shot`-a: njezino vozilo i njezin `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | točka pogotka `shot`-a u vlastitom okviru žrtve (m; x naprijed, y gore, z lijevo; vidi [Poruke jedinicama](how-it-reads.md#messages-to-units)) i smjer kojim je hitac došao, pretvoren u taj okvir stavom žrtve tada |
| `hitPart`, `hitFlag` | poruka pogotka `shot`-a: njezina riječ dijela kako je poslana, i njezin najviši bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | što je bitka koštala i zaradila, i tko je pobijedio: vidi [Ekonomija](economy.md) |
| `other`, `weapon` | ubojstva: druga strana i oružje; pogoci: tko je pogodio (iz uid-a zapisa, inače iz utora igrača), njihovo vozilo; lansiranja: oružje; uništeni moduli: tko je zadnji pogodio jedinicu unutar 5 s prije, i `part <n>` |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
