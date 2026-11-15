---
title: Tabelul
nav_order: 6
lang: ro
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabelul {#the-table}

![Tabelul unui replay sintetic, pe scurt](../assets/img/table.svg)

Un rând pentru fiecare eșantion sau eveniment, 105 coloane ([Lista coloanelor](../columns.md), generată din cod); în subsol, sub `heat3d`, instrucțiunile de citire ale vizualizatorului, deci vizualizatorului nu i se completează niciun formular.

| Coloană | Ce este |
|---|---|
| `time` | secunde pe ceasul propriu al replay-ului |
| `event` | `position`; rândurile de eveniment stau pe traseu în momentul lor (între două eșantioane, pe linia dintre ele); `kill` (la ucigaș), `death` (la victimă), `hit_critical` / `hit_severe` (la unitatea lovită), `module_destroyed` (la unitate), `launch` (la unitatea care a eliberat o armă), `impact` (ultimul eșantion al unei arme când a fost scoasă imediat după); `explosion` și `flak` (0xD08E, 0xD01F) la poziția lor, felul `effect`, fără traseu, cu direcția exploziei acolo unde o are; `shot` (un proiectil care a lovit, la trăgător), `gun_shot`, `fire_start`, `fire_stop` (rafala unui tun, nu un vehicul în flăcări), `fire_on`, `fire_off` (un vehicul în flăcări, vedeți [Incendiile vehiculelor](hits.md#vehicle-fires)), `reward` (Silver Lions și punctele de cercetare câștigate, vedeți [Economie](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (vedeți [Mesaje către unități](how-it-reads.md#messages-to-units)); `despawn`: ultimul rând al unui traseu a cărui unitate a dispărut înainte de sfârșitul replay-ului (vedeți [Sfârșitul unui traseu](ground.md#end-of-a-track)) |
| `track` | ce desenează vizualizatorul ca un singur lucru: o viață a unei unități sau zborul unei arme - `<player or vehicle> #<hex>` (vizualizatorul arată numele fără partea `#`) |
| `x`, `y`, `z` | metrii jocului: x est, y sus, z nord (indiciile oglindesc z, deci nordul nu se desenează la sud) |
| `player` | numele jucătorului; o unitate IA `<VehicleName> #<uid>` (de exemplu `F-15A #204`); `uid <n>` când nimic nu o numește; pentru o armă, cine a eliberat-o |
| `userId`, `team` | id-ul Gaijin al jucătorului și echipa (`1`, `2`) |
| `ai`, `isPlayer` | `ai` adevărat pentru fiecare unitate pe care niciun cont de jucător nu o conduce (unități de misiune, avioane IA, ținte terestre, tunuri antiaeriene, nave fără jucător, substituenți), `isPlayer` invers: un jucător este o unitate a cărei entitate numește un slot de jucător cu un id Gaijin. O armă are pe a lansatorului; gol când nu se știe |
| `match` | id-ul meciului (`match` din documentul meciului), pe fiecare rând; indiciile îl transformă în sesiune, deci două replay-uri încărcate nu unesc niciodată traseele |
| `life` | `uid#n`: traseul unei unități, tăiat unde uid-ul trece la altă unitate, unitatea se mută mai repede decât poate (o reapariție, o rearmare, jocul o mută, clientul corectează o unitate depărtată; vedeți Teleportările în [Cum citește un replay](how-it-reads.md#what-is-read-and-the-check)) sau este multă vreme nevăzută; `w<hex>` zborul unei arme (`w<hex>#n` după o tăiere) |
| `uid` | id-ul unității în replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (un tramvai sau vagon de cale ferată pe care îl plasează nivelul, vedeți [Unități de scenă](objectives.md#scene-units-trams-and-rail-wagons)); arme `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` camera de replay a jucătorului care înregistrează (vedeți [Camera](ground.md#the-camera)) |
| `type` | tipul propriu al jocului acolo unde rezultatele îl numesc (`fighter`, `assault`, `destroyer`, `gun_boat`), altfel ca `kind` |
| `Vehicle` | id-ul vehiculului din joc (`f_15a`, `germ_flakpz_I_Gepard`), cu care se potrivesc figurile vizualizatorului |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | numele vehiculului în engleză din localizarea instalării dumneavoastră (`Pz.Kpfw. III Ausf. J1`, scurt `Pz.III J1`) și cheia sa (`germ_pzkpfw_III_ausf_J_0`); semnele de țară ale fontului jocului sunt lăsate afară. Acolo unde jocul nu numește nimic, sau nu se găsește nicio instalare, numele este id-ul și cheia goală |
| `mission` | numele unității în misiune (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | unde indică unitatea (vectorul de privire): avioanele din atitudinea modelului de zbor, unitățile terestre și navele din ale lor, armele de-a lungul zborului lor |
| `heading`, `pitch`, `roll` | același lucru în grade; cursul este busola, în sensul acelor de ceas de la nord, tangajul pozitiv cu nasul în sus, rularea pozitivă cu aripa dreaptă în jos (modelul de zbor trimite semnul opus, vedeți [Atitudinea, verificată](aircraft.md#attitude-checked); o unitate terestră cu partea dreaptă în jos). Indiciile spun asta sub `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | turela principală a unui tanc - unde indică tunul, nu unde privește jucătorul; valoarea replay-ului ținută la viteza acționării turelei și pusă pe linia fiecărei lovituri de tun principal (vedeți [Turele](ground.md#turrets)): rotirea sa față de caroserie (grade, în sensul acelor de ceas văzut de sus pozitiv, 0 înainte) și înclinarea tunului său față de caroserie (grade, în sus pozitiv); `turrets` fiecare turelă a vehiculului ca `yaw pitch;yaw pitch;...` în ordinea sa (un slot neutilizat citește `0.00 0.00`). Tancuri, SPAA, APC-uri și camioane, în replay-uri de client și de server; nu nave (vedeți [Turele](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | turela principală așa cum o trimite replay-ul; `turretYaw` / `gunPitch` sunt ea ținută la viteza acționării turelei și pusă pe linia fiecărei lovituri de tun principal (vedeți [Turele](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | unde privește jucătorul (ține ținta cu camera) în lume: grade de busolă (0 nord, în sensul acelor de ceas) și grade în sus, aceeași convenție ca `aimHeading` / `aimPitch` (spre deosebire de `turretYaw` / `gunPitch`, care rămân relative la caroserie). Tancul fiecărui jucător într-un replay de server, al celui care înregistrează în propriul său replay de client; gol unde jucătorul nu ține nicăieri (toți cei patru plutitori de țintire 0). Turela îl urmează cu propria viteză de rotire, deci cele două diferă cât timp se întoarce (vedeți [Turele](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | tancul propriu al jucătorului care înregistrează: unde ține ținta (grade de busolă, grade în sus, distanța în m; 2000 când nimic nu este în ochire); rândurile camerei: unde ține ținta jucătorul (cursul, înclinarea) |
| `zoom` | rândurile camerei: mărirea camerei (vedeți [Camera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` sau `SB` al bătăliei, și `ground`, `air` sau `naval`, pe fiecare rând (vedeți [Modul de bătălie](ground.md#battle-mode)) |
| `extrapolated` | un eșantion de avion care este estimarea prin navigare a clientului, nu o stare primită (vedeți [Estimarea prin navigare](aircraft.md#dead-reckoning-and-the-smoother)); un eșantion al unei bombe calculat din eliberarea sa (vedeți Bombele fără înregistrări de zbor în [Cum citește un replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | cât a mutat netezirea eșantionul (m), și poziția și atitudinea proprii ale replay-ului (rularea în semnul tabelului) |
| `targetX`, `targetY`, `targetZ` | punctul de lovire al unui `shot` |
| `hitOutcome`, `hitFlags` | rezultatul unui `shot` asupra unei unități terestre: `kill`, `critical`, `penetration` sau `nonpenetration` (ricoșat sau oprit: replay-ul nu deosebește un ricoșeu), din biții pe care îi trimite serverul cu lovitura (`hitFlags`, brut); gol unde nu se trimite niciunul (avioane, nave). Vedeți [Rezultatele loviturilor](hits.md#hit-outcomes) |
| `hitShell` | semnătura proiectilului unui `shot`: patru octeți din mesajul de lovitură (hex brut); o semnătură poate reprezenta proiectile diferite (APFSDS de 120 și 125 mm au una comună), deci este păstrată brută, nu citită ca un calibru |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | muniția unui `shot`: tipul său (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) și id-ul (`125mm_3bm46`) acolo unde o ucidere numește slotul trăgătorului, altfel `explosive` (rafala de lovitură) sau `kinetic`; `weapon/slot` al tunului din reîncărcările sale; calibrul în mm din fișierele armelor din instalare. Vedeți [Rezultatele loviturilor](hits.md#hit-outcomes) |
| `rpm` | turația motorului unui avion (media peste motoarele sale) cum a fost trimisă ultima oară, în 2 s |
| `vx`, `vy`, `vz` | viteza unui avion cum o trimite intrarea sa de zbor (m/s, axele jocului; vitezele peste 500 m/s citesc 500) |
| `engine`, `afterburner`, `engineCondition` | motoarele unui avion din intrarea sa de zbor: `off`, `starting`, `running`, `dead` (unite cu `/` când motoarele sale diferă); postarderea 0-1; un octet trimis doar după ce motorul a fost lovit |
| `weaponName` | uciderile și morțile: arma sau muniția în engleza instalării dumneavoastră (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | doar avionul jucătorului care înregistrează: accelerația 0-1.1 din cabina sa (1.1 putere de urgență de război sau postardere; altfel cincisprezecimile intrării sale de zbor), comenzile -1..1 din intrarea sa de zbor (profundorul pozitiv trăgând, eleronul pozitiv rulând spre dreapta), rundele rămase pe armă (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | doar avionul jucătorului care înregistrează, din cabina sa: viteza indicată și viteza de urcare (m/s), combustibilul, presiunea din colector (atm), trenul de aterizare (0-1, 1 coborât), temperatura uleiului și a chiulasei, acolo unde cabina sa are indicatorul |
| `speed` | m/s peste aproximativ două secunde ale traseului (calculat aici; replay-ul nu trimite viteză pentru celelalte unități) |
| `alive` | 0 pentru eșantioanele unei unități după moartea sa (epava sa): al unei unități terestre sau al unei nave până când jocul o scoate sau până când eșantioanele sale se termină, al unui avion cel mult 60 s |
| `otherVehicle`, `otherLife` | victima unui `shot`: vehiculul său și `life` al său |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | punctul de lovire al unui `shot` în cadrul propriu al victimei (m; x înainte, y sus, z stânga; vedeți [Mesaje către unități](how-it-reads.md#messages-to-units)) și felul în care a venit lovitura, întors în acel cadru de atitudinea victimei de atunci |
| `hitPart`, `hitFlag` | mesajul de lovitură al unui `shot`: cuvântul său de piesă cum a fost trimis, și octetul său de sus |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | ce a costat și ce a câștigat bătălia și cine a câștigat: vedeți [Economie](economy.md) |
| `other`, `weapon` | uciderile: cealaltă tabără și arma; loviturile: cine a lovit (din uid-ul înregistrării, altfel din slotul de jucător), vehiculul lor; lansările: arma; modulele distruse: cine a lovit ultima oară unitatea cu cel mult 5 s înainte, și `part <n>` |

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
