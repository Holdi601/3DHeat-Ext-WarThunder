---
title: "Tabela"
nav_order: 6
lang: bs
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabela {#the-table}

![Tabela sintetičkog replaya, sažeta](../assets/img/table.svg)

Jedan red po uzorku ili događaju, 105 kolona ([Lista kolona](../columns.md), generisana iz koda); u podnožju, pod `heat3d`, nalaze se upute za čitanje
za preglednik, tako da preglednik ne treba popunjavati nikakav obrazac.

| Kolona | Šta |
|---|---|
| `time` | sekunde na vlastitom satu replaya |
| `event` | `position`; redovi događaja leže na stazi u svom trenutku (između dva uzorka, na liniji između njih); `kill` (kod ubice), `death` (kod žrtve), `hit_critical` / `hit_severe` (kod pogođene jedinice), `module_destroyed` (kod jedinice), `launch` (kod jedinice koja je ispustila oružje), `impact` (posljednji uzorak oružja kada je uklonjeno odmah poslije); `explosion` i `flak` (0xD08E, 0xD01F) na svojoj poziciji, vrsta `effect`, bez staze, sa smjerom eksplozije gdje ga ima; `shot` (projektil koji je pogodio, kod strijelca), `gun_shot`, `fire_start`, `fire_stop` (rafal topa, ne vozilo koje gori), `fire_on`, `fire_off` (vozilo koje gori, vidi [Požari vozila](hits.md#vehicle-fires)), `reward` (zarađeni Silver Lions i bodovi istraživanja, vidi [Ekonomija](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (vidi [Poruke jedinicama](how-it-reads.md#messages-to-units)); `despawn`: posljednji red staze čija jedinica nestane prije kraja replaya (vidi [Kraj staze](ground.md#end-of-a-track)) |
| `track` | ono što preglednik crta kao jednu stvar: jedan život jedinice ili let jednog oružja - `<player or vehicle> #<hex>` (preglednik prikazuje ime bez dijela s `#`) |
| `x`, `y`, `z` | metri igre: x istok, y gore, z sjever (upute zrcale z, pa sjever nije nacrtan na jugu) |
| `player` | ime igrača; AI jedinica `<VehicleName> #<uid>` (na primjer `F-15A #204`); `uid <n>` kada je ništa ne imenuje; za oružje, ko ga je ispustio |
| `userId`, `team` | Gaijin id igrača i tim (`1`, `2`) |
| `ai`, `isPlayer` | `ai` je tačno za svaku jedinicu koju ne vozi nijedan igrački račun (jedinice misije, AI avioni, kopnene mete, AA topovi, brodovi bez igrača, rezervirana mjesta), `isPlayer` suprotno: igrač je jedinica čiji entitet imenuje igrački slot s Gaijin id-om. Oružje ima vrijednost svog lansera; prazno kada nije poznato |
| `match` | id meča (`match` iz dokumenta meča), na svakom redu; upute ga mapiraju kao sesiju, pa se dva učitana replaya nikad ne spajaju u staze |
| `life` | `uid#n`: staza jedne jedinice, presječena tamo gdje uid prelazi na drugu jedinicu, jedinica se kreće brže nego što može (respawn, ponovno punjenje, igra je pomjerila, klijent ispravlja udaljenu jedinicu; vidi Teleporti u [Kako čita replay](how-it-reads.md#what-is-read-and-the-check)) ili je dugo nevidljiva; `w<hex>` let oružja (`w<hex>#n` poslije reza) |
| `uid` | id jedinice u replayu |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvaj ili željeznički vagon koji nivo postavlja, vidi [Scenske jedinice](objectives.md#scene-units-trams-and-rail-wagons)); oružja `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` je replay kamera igrača koji snima (vidi [Kamera](ground.md#the-camera)) |
| `type` | vlastiti tip igre gdje ga rezultati imenuju (`fighter`, `assault`, `destroyer`, `gun_boat`), inače kao `kind` |
| `Vehicle` | id vozila u igri (`f_15a`, `germ_flakpz_I_Gepard`), koji odgovara figurama u pregledniku |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | englesko ime vozila iz lokalizacije vaše instalacije (`Pz.Kpfw. III Ausf. J1`, kratko `Pz.III J1`) i njegov ključ (`germ_pzkpfw_III_ausf_J_0`); oznake država iz fonta igre su izostavljene. Gdje igra ništa ne imenuje ili instalacija nije pronađena, ime je id, a ključ prazan |
| `mission` | ime jedinice u misiji (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kamo jedinica pokazuje (vektor pogleda): avioni iz stava modela leta, kopnene jedinice i brodovi iz vlastitog, oružja duž svog leta |
| `heading`, `pitch`, `roll` | isto u stepenima; heading je kompas, u smjeru kazaljke na satu od sjevera, pitch je pozitivan kada je nos gore, roll je pozitivan kada je desno krilo dolje (model leta šalje suprotan predznak, vidi [Stav, provjeren](aircraft.md#attitude-checked); desna strana kopnene jedinice dolje). Upute to kažu pod `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | glavna kupola tenka - kamo pokazuje top, ne kamo gleda njegov igrač; vrijednost replaya držana na brzinu pogona kupole i postavljena na liniju svakog hica glavnog topa (vidi [Kupole](ground.md#turrets)): njen yaw u odnosu na trup (stepeni, pozitivno u smjeru kazaljke na satu gledano odozgo, 0 ravno naprijed) i pitch njenog topa u odnosu na trup (stepeni, pozitivno gore); `turrets` je svaka kupola vozila kao `yaw pitch;yaw pitch;...` svojim redoslijedom (neiskorišteni slot se čita kao `0.00 0.00`). Tenkovi, SPAA, APC i kamioni, u klijentskim i serverskim replayevima; ne brodovi (vidi [Kupole](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | glavna kupola onako kako je replay šalje; `turretYaw` / `gunPitch` su ona držana na brzinu pogona kupole i postavljena na liniju svakog hica glavnog topa (vidi [Kupole](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kamo igrač gleda (cilja kamerom) u svijetu: kompasni stepeni (0 sjever, u smjeru kazaljke na satu) i stepeni prema gore, ista konvencija kao `aimHeading` / `aimPitch` (za razliku od `turretYaw` / `gunPitch`, koji ostaju relativni prema trupu). Tenk svakog igrača u serverskom replayu, vlastiti tenk igrača koji snima u klijentskom replayu; prazno gdje igrač nigdje ne cilja (sva četiri float-a cilja su 0). Kupola ga prati vlastitom brzinom okretanja, pa se njih dvoje razlikuju dok se okreće (vidi [Kupole](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | vlastiti tenk igrača koji snima: kamo cilja (kompasni stepeni, stepeni prema gore, udaljenost u m; 2000 kada u nišanu nema ničega); redovi kamere: kamo igrač cilja (heading, pitch) |
| `zoom` | redovi kamere: uvećanje kamere (vidi [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` ili `SB` bitke, i `ground`, `air` ili `naval`, na svakom redu (vidi [Način bitke](ground.md#battle-mode)) |
| `extrapolated` | uzorak aviona koji je dead reckoning klijenta, a ne stanje koje je primljeno (vidi [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); uzorak bombe izračunat iz njenog ispuštanja (vidi Bombe bez zapisa leta u [Kako čita replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | koliko je glatkač pomjerio uzorak (m) te vlastita pozicija i stav replaya (roll u predznaku tabele) |
| `targetX`, `targetY`, `targetZ` | tačka pogotka jednog `shot` |
| `hitOutcome`, `hitFlags` | ishod jednog `shot` na kopnenu jedinicu: `kill`, `critical`, `penetration` ili `nonpenetration` (odbijen ili zaustavljen: replay ne razlikuje rikošet), iz bitova koje server šalje s pogotkom (`hitFlags`, sirovo); prazno gdje se ništa ne šalje (avioni, brodovi). Vidi [Ishodi pogodaka](hits.md#hit-outcomes) |
| `hitShell` | potpis granate jednog `shot`: četiri bajta poruke o pogotku (sirovi hex); jedan potpis može označavati različite granate (120 i 125 mm APFSDS dijele jedan), pa se čuva sirov, a ne čita kao kalibar |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | municija jednog `shot`: njen tip (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) i id (`125mm_3bm46`) gdje ubistvo imenuje slot strijelca, inače `explosive` (rafal pogotka) ili `kinetic`; `weapon/slot` topa iz njegovih ponovnih punjenja; kalibar u mm iz datoteka oružja instalacije. Vidi [Ishodi pogodaka](hits.md#hit-outcomes) |
| `rpm` | broj okretaja motora aviona (srednja vrijednost svih motora) kako je zadnji put poslan, unutar 2 s |
| `vx`, `vy`, `vz` | brzina aviona kako je šalje njegov unos leta (m/s, osi igre; brzine preko 500 m/s čitaju se kao 500) |
| `engine`, `afterburner`, `engineCondition` | motori aviona iz njegovog unosa leta: `off`, `starting`, `running`, `dead` (spojeno sa `/` kada se motori razlikuju); naknadno sagorijevanje 0-1; bajt koji se šalje tek nakon što je motor pogođen |
| `weaponName` | ubistva i smrti: oružje ili municija na engleskom iz vaše instalacije (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | samo avion igrača koji snima: gas 0-1.1 iz njegovog kokpita (1.1 je ratna nužna snaga ili naknadno sagorijevanje; inače petnaestine iz unosa leta), komande -1..1 iz njegovog unosa leta (elevator pozitivan pri povlačenju, aileron pozitivan pri valjanju udesno), preostali meci po oružju (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | samo avion igrača koji snima, iz njegovog kokpita: indicirana brzina i brzina penjanja (m/s), gorivo, pritisak u usisnoj grani (atm), stajni trap (0-1, 1 je izvučen), temperatura ulja i glave cilindra, gdje kokpit ima instrument |
| `speed` | m/s tokom otprilike dvije sekunde staze (izračunato ovdje; replay ne šalje brzinu za druge jedinice) |
| `alive` | 0 za uzorke jedinice poslije njene smrti (njen olupina): kopnene jedinice ili broda dok ih igra ne ukloni ili dok njihovi uzorci ne završe, aviona najviše 60 s |
| `otherVehicle`, `otherLife` | žrtva jednog `shot`: njeno vozilo i njen `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | tačka pogotka jednog `shot` u vlastitom okviru žrtve (m; x naprijed, y gore, z lijevo; vidi [Poruke jedinicama](how-it-reads.md#messages-to-units)) i smjer iz kojeg je hitac došao, okrenut u taj okvir stavom žrtve u tom trenutku |
| `hitPart`, `hitFlag` | poruka o pogotku jednog `shot`: njena riječ dijela kako je poslana i njen viši bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | šta je bitka koštala i donijela, i ko je pobijedio: vidi [Ekonomija](economy.md) |
| `other`, `weapon` | ubistva: druga strana i oružje; pogoci: ko je pogodio (iz uid-a zapisa, inače iz njegovog igračkog slota), njihovo vozilo; lansiranja: oružje; uništeni moduli: ko je zadnji pogodio jedinicu unutar 5 s prije, i `part <n>` |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
