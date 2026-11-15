---
title: "Tabela"
nav_order: 6
lang: "sq"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabela {#the-table}

![Tabela e një riluajtjeje sintetike, e përmbledhur](../assets/img/table.svg)

Një rresht për çdo mostër ose ngjarje, 105 kolona ([Lista e kolonave](../columns.md), e gjeneruar nga kodi); në fund, nën `heat3d`, udhëzimet e leximit për shikuesin, kështu që shikuesi nuk ka nevojë të plotësojë asnjë formular.

| Kolona | Çfarë |
|---|---|
| `time` | sekonda në orën e vetë riluajtjes |
| `event` | `position`; rreshtat e ngjarjeve shtrihen mbi gjurmë në çastin e tyre (midis dy mostrave, në vijën midis tyre); `kill` (te vrasësi), `death` (te viktima), `hit_critical` / `hit_severe` (te njësia e goditur), `module_destroyed` (te njësia), `launch` (te njësia që lëshoi një armë), `impact` (mostra e fundit e një arme kur u hoq menjëherë pas); `explosion` dhe `flak` (0xD08E, 0xD01F) në pozicionin e tyre, lloji `effect`, pa gjurmë, me drejtimin e shpërthimit aty ku ka; `shot` (një predhë që goditi, te gjuajtësi), `gun_shot`, `fire_start`, `fire_stop` (një breshëri e një arme, jo një mjet që digjet), `fire_on`, `fire_off` (një mjet që digjet, shih [Zjarret e mjeteve](hits.md#vehicle-fires)), `reward` (Silver Lions dhe pikë kërkimi të fituara, shih [Ekonomia](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (shih [Mesazhet për njësitë](how-it-reads.md#messages-to-units)); `despawn`: rreshti i fundit i një gjurme, njësia e së cilës është zhdukur para fundit të riluajtjes (shih [Fundi i një gjurme](ground.md#end-of-a-track)) |
| `track` | ajo që shikuesi vizaton si një gjë të vetme: një jetë e një njësie, ose fluturimi i një arme - `<player or vehicle> #<hex>` (shikuesi e shfaq emrin pa pjesën `#`) |
| `x`, `y`, `z` | metrat e lojës: x lindje, y lart, z veri (udhëzimet e pasqyrojnë z, kështu që veriu nuk vizatohet nga jugu) |
| `player` | emri i lojtarit; një njësi AI `<VehicleName> #<uid>` (për shembull `F-15A #204`); `uid <n>` kur asgjë nuk e emërton; për një armë, kush e lëshoi |
| `userId`, `team` | ID-ja Gaijin e lojtarit dhe skuadra (`1`, `2`) |
| `ai`, `isPlayer` | `ai` e vërtetë për çdo njësi që nuk e drejton asnjë llogari lojtari (njësi misioni, aeroplanë AI, objektiva tokësorë, armë kundërajrore, anije pa lojtar, vendmbajtëse), `isPlayer` e kundërta: lojtar është një njësi, entiteti i së cilës emërton një vend lojtari me ID Gaijin. Një armë ka atë të lëshuesit të saj; bosh kur nuk dihet |
| `match` | ID e ndeshjes (`match` e dokumentit të ndeshjes), në çdo rresht; udhëzimet e lidhin me sesionin, kështu që dy riluajtje të ngarkuara nuk bashkojnë kurrë gjurmë |
| `life` | `uid#n`: gjurma e një njësie, e prerë aty ku uid kalon te një njësi tjetër, njësia lëviz më shpejt se sa mundet (një ripërtëritje, një rimbushje, loja që e lëviz, klienti që korrigjon një njësi të largët; shih Teleportimet te [Si e lexon një riluajtje](how-it-reads.md#what-is-read-and-the-check)) ose nuk është parë për kohë të gjatë; `w<hex>` fluturimi i një arme (`w<hex>#n` pas një prerjeje) |
| `uid` | ID e njësisë në riluajtje |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (një tramvaj ose vagon hekurudhor që e vendos niveli, shih [Njësitë e skenës](objectives.md#scene-units-trams-and-rail-wagons)); armët `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` kamera e riluajtjes e lojtarit që regjistron (shih [Kamera](ground.md#the-camera)) |
| `type` | lloji i vetë lojës aty ku rezultatet e emërtojnë (`fighter`, `assault`, `destroyer`, `gun_boat`), përndryshe si `kind` |
| `Vehicle` | ID e mjetit në lojë (`f_15a`, `germ_flakpz_I_Gepard`), me të cilën përputhen figurat e shikuesit |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | emri i mjetit në anglisht nga lokalizimi i instalimit tënd (`Pz.Kpfw. III Ausf. J1`, i shkurtër `Pz.III J1`) dhe çelësi i tij (`germ_pzkpfw_III_ausf_J_0`); shenjat e vendeve të shkronjave të lojës lihen jashtë. Aty ku loja nuk emërton asgjë, ose nuk gjendet instalim, emri është ID dhe çelësi bosh |
| `mission` | emri i njësisë në mision (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | ku tregon njësia (vektori i shikimit): aeroplanët nga qëndrimi i modelit të fluturimit, njësitë tokësore dhe anijet nga i tyri, armët përgjatë fluturimit të tyre |
| `heading`, `pitch`, `roll` | e njëjta në shkallë; heading është busulla, në drejtim të akrepave të orës nga veriu, pitch hunda lart pozitive, roll krahu i djathtë poshtë pozitiv (modeli i fluturimit dërgon shenjën e kundërt, shih [Qëndrimi, i kontrolluar](aircraft.md#attitude-checked); ana e djathtë poshtë e një njësie tokësore). Udhëzimet e thonë këtë nën `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | kupola kryesore e një tanku - ku tregon topi, jo ku shikon lojtari i tij; vlera e riluajtjes e mbajtur në shpejtësinë e motorit të kupolës dhe vendosur në vijën e çdo të shtëne të topit kryesor (shih [Kupolat](ground.md#turrets)): kthimi i saj ndaj trupit (shkallë, pozitiv në drejtim të akrepave të orës nga lart, 0 drejt përpara) dhe pitch i topit të saj ndaj trupit (shkallë, pozitiv lart); `turrets` çdo kupolë e mjetit si `yaw pitch;yaw pitch;...` në radhën e saj (një vend i papërdorur lexohet `0.00 0.00`). Tanke, SPAA, APC dhe kamionë, në riluajtje klienti dhe serveri; jo anije (shih [Kupolat](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | kupola kryesore siç e dërgon riluajtja; `turretYaw` / `gunPitch` janë ajo e mbajtur në shpejtësinë e motorit të kupolës dhe vendosur në vijën e çdo të shtëne të topit kryesor (shih [Kupolat](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | ku shikon lojtari (synon me kamerën) në botë: shkallë busulle (0 veri, në drejtim të akrepave të orës) dhe shkallë lart, e njëjta konventë si `aimHeading` / `aimPitch` (ndryshe nga `turretYaw` / `gunPitch`, që mbeten relative ndaj trupit). Tanku i çdo lojtari në një riluajtje serveri, ai i vetë lojtarit që regjistron në një riluajtje klienti; bosh aty ku lojtari nuk synon askund (të katër numrat e synimit 0). Kupola e ndjek me shpejtësinë e vet të rrotullimit, kështu që të dyja ndryshojnë ndërsa ajo kthehet (shih [Kupolat](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | tanku i vetë lojtarit që regjistron: ku synon (shkallë busulle, shkallë lart, distanca në m; 2000 kur nuk ka asgjë në shënjestër); rreshtat e kamerës: ku synon lojtari (heading, pitch) |
| `zoom` | rreshtat e kamerës: zmadhimi i kamerës (shih [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` ose `SB` e betejës, dhe `ground`, `air` ose `naval`, në çdo rresht (shih [Mënyra e betejës](ground.md#battle-mode)) |
| `extrapolated` | një mostër aeroplani që është dead reckoning i klientit, jo gjendje e marrë (shih [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); mostra e një bombe e llogaritur nga lëshimi i saj (shih Bombat pa regjistra fluturimi te [Si e lexon një riluajtje](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | sa e lëvizi mostrën zbutësi (m), dhe pozicioni dhe qëndrimi i vetë riluajtjes (roll me shenjën e tabelës) |
| `targetX`, `targetY`, `targetZ` | pika e goditjes e një `shot` |
| `hitOutcome`, `hitFlags` | rezultati i një `shot` mbi një njësi tokësore: `kill`, `critical`, `penetration` ose `nonpenetration` (u hodh prapa ose u ndal: riluajtja nuk e dallon një ricochet), nga bitët që dërgon serveri me goditjen (`hitFlags`, të papërpunuar); bosh aty ku nuk dërgohet asnjë (aeroplanë, anije). Shih [Rezultatet e goditjeve](hits.md#hit-outcomes) |
| `hitShell` | nënshkrimi i predhës së një `shot`: katër bajtë të mesazhit të goditjes (hex i papërpunuar); një nënshkrim mund të qëndrojë për predha të ndryshme (120 dhe 125 mm APFSDS ndajnë një), kështu që ruhet i papërpunuar, jo i lexuar si kalibër |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | municioni i një `shot`: lloji i tij (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) dhe ID (`125mm_3bm46`) aty ku një vrasje emërton vendin e gjuajtësit, përndryshe `explosive` (shpërthimi i goditjes) ose `kinetic`; `weapon/slot` i topit nga rimbushjet e tij; kalibri në mm nga skedarët e armëve të instalimit. Shih [Rezultatet e goditjeve](hits.md#hit-outcomes) |
| `rpm` | rpm i motorit të një aeroplani (mesatarja mbi motorët e tij) siç u dërgua së fundmi, brenda 2 s |
| `vx`, `vy`, `vz` | shpejtësia e një aeroplani siç e dërgon hyrja e tij e fluturimit (m/s, boshtet e lojës; shpejtësitë mbi 500 m/s lexohen 500) |
| `engine`, `afterburner`, `engineCondition` | motorët e një aeroplani nga hyrja e tij e fluturimit: `off`, `starting`, `running`, `dead` (të bashkuar me `/` kur motorët e tij ndryshojnë); afterburner 0-1; një bajt që dërgohet vetëm pasi motori u godit |
| `weaponName` | vrasjet dhe vdekjet: arma ose municioni në anglishten e instalimit tënd (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | vetëm aeroplani i lojtarit që regjistron: gazi 0-1.1 nga kabina e tij (1.1 fuqi emergjente lufte ose afterburner; përndryshe të pesëmbëdhjetat e hyrjes së fluturimit), kontrollet -1..1 nga hyrja e tij e fluturimit (elevator pozitiv tërheq, aileron pozitiv rrotullon djathtas), predhat e mbetura për armë (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | vetëm aeroplani i lojtarit që regjistron, nga kabina e tij: shpejtësia e treguar dhe shpejtësia e ngjitjes (m/s), karburanti, presioni i manifoldit (atm), trapi (0-1, 1 poshtë), temperatura e vajit dhe e kokës së cilindrave, aty ku kabina e tij ka matësin |
| `speed` | m/s mbi rreth dy sekonda të gjurmës (llogaritur këtu; riluajtja nuk dërgon shpejtësi për njësitë e tjera) |
| `alive` | 0 për mostrat e një njësie pas vdekjes së saj (mbetjet): të një njësie tokësore ose anijeje derisa loja ta heqë ose mostrat e saj mbarojnë, të një aeroplani për më së shumti 60 s |
| `otherVehicle`, `otherLife` | viktima e një `shot`: mjeti i saj dhe `life` e saj |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | pika e goditjes e një `shot` në kuadrin e vetë viktimës (m; x përpara, y lart, z majtas; shih [Mesazhet për njësitë](how-it-reads.md#messages-to-units)) dhe drejtimi nga erdhi e shtëna, i kthyer në atë kuadër nga qëndrimi i viktimës atëherë |
| `hitPart`, `hitFlag` | mesazhi i goditjes i një `shot`: fjala e pjesës siç u dërgua, dhe bajti i saj i lartë |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | sa kushtoi dhe sa fitoi beteja, dhe kush fitoi: shih [Ekonomia](economy.md) |
| `other`, `weapon` | vrasjet: ana tjetër dhe arma; goditjet: kush goditi (nga uid i regjistrit, përndryshe vendi i tij i lojtarit), mjeti i tij; lëshimet: arma; modulet e shkatërruara: kush e goditi së fundmi njësinë brenda 5 s para, dhe `part <n>` |

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
