---
title: Tabula
nav_order: 6
lang: lv
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabula {#the-table}

![Sintētiska atkārtojuma tabula, apkopota](../assets/img/table.svg)

Viena rinda katram paraugam vai notikumam, 105 kolonnas ([Kolonnu saraksts](../columns.md), ģenerēts no koda); kājenē zem `heat3d` skatītāja lasīšanas
norādījumi, tāpēc skatītājam nav jāaizpilda nekāda forma.

| Kolonna | Ko tā nozīmē |
|---|---|
| `time` | sekundes pēc paša atkārtojuma pulksteņa |
| `event` | `position`; notikumu rindas atrodas uz celiņa savā brīdī (starp diviem paraugiem, uz līnijas starp tiem); `kill` (pie slepkavas), `death` (pie upura), `hit_critical` / `hit_severe` (pie trāpītās vienības), `module_destroyed` (pie vienības), `launch` (pie vienības, kas izlaida ieroci), `impact` (ieroča pēdējais paraugs, kad tas tika noņemts uzreiz pēc tam); `explosion` un `flak` (0xD08E, 0xD01F) savā pozīcijā, veids `effect`, bez celiņa, ar sprādziena virzienu, kur tāds ir; `shot` (trāpījuma lidojums, pie šāvēja), `gun_shot`, `fire_start`, `fire_stop` (lielgabala sērija, nevis transportlīdzeklis, kas deg), `fire_on`, `fire_off` (transportlīdzeklis, kas deg, skat. [Transportlīdzekļu ugunsgrēki](hits.md#vehicle-fires)), `reward` (nopelnītās Sudraba lauvas un pētniecības punkti, skat. [Ekonomika](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (skat. [Ziņojumi vienībām](how-it-reads.md#messages-to-units)); `despawn`: celiņa pēdējā rinda, kad tā vienība ir pazudusi, pirms atkārtojums beidzas (skat. [Celiņa beigas](ground.md#end-of-a-track)) |
| `track` | ko skatītājs zīmē kā vienu lietu: viena vienības dzīve vai viena ieroča lidojums — `<spēlētājs vai transportlīdzeklis> #<hex>` (skatītājs parāda vārdu bez `#` daļas) |
| `x`, `y`, `z` | spēles metri: x uz austrumiem, y uz augšu, z uz ziemeļiem (norādes apgriež z, tāpēc ziemeļi netiek zīmēti uz dienvidiem) |
| `player` | spēlētāja vārds; MI vienība `<VehicleName> #<uid>` (piemēram `F-15A #204`); `uid <n>`, kad nekas to nenosauc; ieročam — kas to izlaida |
| `userId`, `team` | spēlētāja Gaijin ID un komanda (`1`, `2`) |
| `ai`, `isPlayer` | `ai` ir true katrai vienībai, ko nevada neviens spēlētāja konts (misijas vienības, MI lidmašīnas, sauszemes mērķi, pretgaisa lielgabali, kuģi bez spēlētāja, vietturi), `isPlayer` — pretēji: spēlētājs ir vienība, kuras entītija nosauc spēlētāja slotu ar Gaijin ID. Ierocim ir tā palaidēja; tukšs, kad nav zināms |
| `match` | mača ID (mača dokumenta `match`), katrā rindā; norādes to kartē kā sesiju, tāpēc divi ielādēti atkārtojumi nekad nesaista celiņus |
| `life` | `uid#n`: vienas vienības celiņš, pārtraukts tad, kad uid pāriet uz citu vienību, vienība pārvietojas ātrāk, nekā var (atdzimšana, pārmaiņa, spēle pārvieto vienību, klients koriģē tālu vienību; skat. [Kā tas nolasa atkārtojumu](how-it-reads.md#what-is-read-and-the-check) par teleportācijām), vai tā ilgi nav redzēta; `w<hex>` ieroča lidojums (`w<hex>#n` pēc pārtraukuma) |
| `uid` | vienības ID atkārtojumā |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvajs vai sliežu vagons, ko līmenis novieto, skat. [Skatuves vienības](objectives.md#scene-units-trams-and-rail-wagons)); ieroči `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` — ieraksta spēlētāja atkārtojuma kamera (skat. [Kamera](ground.md#the-camera)) |
| `type` | spēles pašas tips, kur rezultāti to nosauc (`fighter`, `assault`, `destroyer`, `gun_boat`), citādi kā `kind` |
| `Vehicle` | spēles transportlīdzekļa ID (`f_15a`, `germ_flakpz_I_Gepard`), kuram skatītāja figūras atbilst |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | transportlīdzekļa angļu nosaukums no jūsu instalācijas lokalizācijas (`Pz.Kpfw. III Ausf. J1`, īsais `Pz.III J1`) un tā atslēga (`germ_pzkpfw_III_ausf_J_0`); spēles fonta valstu zīmes ir ārpusē. Kur spēle nekas nenosauc vai instalācija nav atrasta, nosaukums ir ID, un atslēga tukša |
| `mission` | vienības nosaukums misijā (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kurp vienība vērsta (skatīšanās vektors): lidmašīnām no lidojuma modeļa orientācijas, sauszemes vienībām un kuģiem — no to pašu, ieročiem gar lidojumu |
| `heading`, `pitch`, `roll` | tas pats grādos; heading ir kompass, pulksteņrādītāja virzienā no ziemeļiem, pitch deguns uz augšu pozitīvs, roll labais spārns uz leju pozitīvs (lidojuma modelis sūta pretēju zīmi, skat. [Orientācija, pārbaudīta](aircraft.md#attitude-checked); sauszemes vienības labā puse uz leju). Norādes to noliek zem `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | tanka galvenais tornis — kur lielgabals vērsts, nevis kur spēlētājs skatās; atkārtojuma vērtība, turēta pie torņa piedziņas ātruma un iestatīta uz katra galvenā lielgabala šāviena līniju (skat. [Torņi](ground.md#turrets)): tā virziens attiecībā pret korpusu (grādi, no augšas redzot pulksteņrādītāja virzienā pozitīvs, 0 tieši uz priekšu) un tā lielgabala pacēlums attiecībā pret korpusu (grādi, uz augšu pozitīvs); `turrets` katrs transportlīdzekļa tornis kā `yaw pitch;yaw pitch;...` tā paša secībā (neizmantots slots ir `0.00 0.00`). Tanki, SPAA, APC un kravas automašīnas, klienta un servera atkārtojumos; kuģi nē (skat. [Torņi](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | galvenais tornis, kā to sūta atkārtojums; `turretYaw` / `gunPitch` ir tas, turēts pie torņa piedziņas ātruma un iestatīts uz katra galvenā lielgabala šāviena līniju (skat. [Torņi](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kur spēlētājs skatās (tēmē ar kameru) pasaulē: kompasa grādi (0 ziemeļi, pulksteņrādītāja virzienā) un grādi uz augšu, ar to pašu konvenciju kā `aimHeading` / `aimPitch` (atšķirībā no `turretYaw` / `gunPitch`, kas paliek attiecībā pret korpusu). Katra spēlētāja tanks servera atkārtojumā, ieraksta spēlētāja paša klienta atkārtojumā; tur, kur spēlētājs nekur netēmē, tukšs (visi četri tēmēšanas peldošie 0). Tornis seko tam ar savu traversa ātrumu, tāpēc tie atšķiras, kamēr tas griežas (skat. [Torņi](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | ieraksta spēlētāja paša tanks: kur tas tēmē (kompasa grādi, grādi uz augšu, attālums m; 2000, kad tēmeklī nekas nav); kameras rindas: kur spēlētājs tēmē (heading, pitch) |
| `zoom` | kameras rindas: kameras palielinājums (skat. [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | kaujas `AB`, `RB` vai `SB`, un `ground`, `air` vai `naval`, katrā rindā (skat. [Kaujas režīms](ground.md#battle-mode)) |
| `extrapolated` | lidmašīnas paraugs, kas ir klienta novērtētā kustība, nevis saņemts stāvoklis (skat. [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); bumbas paraugs, kas aprēķināts no tās izlaišanas (skat. Bumbas bez lidojuma ierakstiem [Kā tas nolasa atkārtojumu](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | cik tālu izlīdzinātājs pārvietoja paraugu (m), un atkārtojuma pašas pozīcija un orientācija (roll tabulas zīmē) |
| `targetX`, `targetY`, `targetZ` | `shot` trāpījuma punkts |
| `hitOutcome`, `hitFlags` | `shot` iznākums uz sauszemes vienības: `kill`, `critical`, `penetration` vai `nonpenetration` (atlēca vai apstājās: atkārtojums nestāsta, kas ir rikošets), no bitiem, ko serveris sūta ar trāpījumu (`hitFlags`, neapstrādāts); tukšs, kur nekas nav sūtīts (lidmašīnas, kuģi). Skat. [Trāpījumu iznākumi](hits.md#hit-outcomes) |
| `hitShell` | `shot` šāviņa paraksts: četri baiti no trāpījuma ziņojuma (neapstrādāts hex); viens paraksts var apzīmēt dažādus šāviņus (120 un 125 mm APFSDS dalās ar vienu), tāpēc tas tiek paturēts neapstrādāts, nevis nolasīts kā kalibrs |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | `shot` munīcija: tās tips (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) un ID (`125mm_3bm46`), kur nogalinājums nosauc šāvēja slotu, citādi `explosive` (trāpījuma sprādziens) vai `kinetic`; lielgabala `weapon/slot` no tā pārlādēšanām; kalibrs mm no instalācijas ieroču failiem. Skat. [Trāpījumu iznākumi](hits.md#hit-outcomes) |
| `rpm` | lidmašīnas dzinēja apgriezieni (vidēji pa dzinējiem), kā pēdējo reizi nosūtīti, 2 s robežās |
| `vx`, `vy`, `vz` | lidmašīnas ātrums, kā to sūta tās lidojuma ieraksts (m/s, spēles asis; ātrumi virs 500 m/s nolasās kā 500) |
| `engine`, `afterburner`, `engineCondition` | lidmašīnas dzinēji no tās lidojuma ieraksta: `off`, `starting`, `running`, `dead` (ar `/` savienoti, kad tā dzinēji atšķiras); pēcdedzinātājs 0–1; baits, kas sūtīts tikai pēc tam, kad dzinējs tika trāpīts |
| `weaponName` | nogalinājumi un nāves: ierocis vai munīcija jūsu instalācijas angļu valodā (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | tikai ieraksta spēlētāja lidmašīna: gāze 0–1,1 no tās kabīnes (1,1 kara avārijas jauda vai pēcdedzinātājs; citādi no tās lidojuma ieraksta piecpadsmitdaļām), vadība −1..1 no tās lidojuma ieraksta (elevator pozitīvs velkot, aileron pozitīvs, rullējot pa labi), atlikušie šāvieni katrā ieročā (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | tikai ieraksta spēlētāja lidmašīna, no tās kabīnes: indicētais gaisa ātrums un kāpšanas ātrums (m/s), degviela, ieplūdes spiediens (atm), šasija (0–1, 1 nolaista), eļļas un cilindru galvas temperatūra, kur kabīnē ir šis mērinstruments |
| `speed` | m/s pāri apmēram divām sekundēm celiņā (aprēķināts šeit; atkārtojums citu vienību ātrumu nesūta) |
| `alive` | 0 vienības paraugiem pēc tās nāves (tās vrakam): sauszemes vienībai vai kuģim līdz brīdim, kad spēle to noņem vai tā paraugi beidzas; lidmašīnai — ne ilgāk par 60 s |
| `otherVehicle`, `otherLife` | `shot` upuris: tā transportlīdzeklis un tā `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | `shot` trāpījuma punkts upura pašas koordinātu sistēmā (m; x uz priekšu, y uz augšu, z pa kreisi; skat. [Ziņojumi vienībām](how-it-reads.md#messages-to-units)) un tas, kā šāviens nāca, pārvērsts tajā koordinātu sistēmā pēc upura orientācijas tajā brīdī |
| `hitPart`, `hitFlag` | `shot` trāpījuma ziņojums: tā daļas vārds, kā nosūtīts, un tā augstais baits |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | ko kauja maksāja un nopelnīja un kas uzvarēja: skat. [Ekonomika](economy.md) |
| `other`, `weapon` | nogalinājumi: otra puse un ierocis; trāpījumi: kas trāpīja (no ieraksta uid, citādi no tā spēlētāja slota), viņu transportlīdzeklis; palaišanas: ierocis; iznīcināti moduļi: kas pēdējais trāpīja vienību 5 s iepriekš, un `part <n>` |

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
