---
title: "De tabel"
nav_order: 6
lang: "nl"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# De tabel {#the-table}

![De tabel van een synthetische replay, samengevat](../assets/img/table.svg)

Eén rij per sample of gebeurtenis, 105 kolommen ([Kolomlijst](../columns.md), gegenereerd uit de code); in de voettekst, onder `heat3d`, de leesinstructies van de viewer, zodat de viewer geen formulier hoeft in te vullen.

| Kolom | Wat |
|---|---|
| `time` | seconden op de eigen klok van de replay |
| `event` | `position`; gebeurtenisrijen liggen op het spoor op hun moment (tussen twee samples, op de lijn tussen hen); `kill` (bij de killer), `death` (bij het slachtoffer), `hit_critical` / `hit_severe` (bij de getroffen eenheid), `module_destroyed` (bij de eenheid), `launch` (bij de eenheid die een wapen afvuurde), `impact` (het laatste sample van een wapen toen het direct daarna verwijderd werd); `explosion` en `flak` (0xD08E, 0xD01F) op hun positie, soort `effect`, geen spoor, met de richting van de explosie waar die er een heeft; `shot` (een projectiel dat trof, bij de schutter), `gun_shot`, `fire_start`, `fire_stop` (een salvo van een kanon, geen voertuig in brand), `fire_on`, `fire_off` (een voertuig in brand, zie [Branden van voertuigen](hits.md#vehicle-fires)), `reward` (Zilveren Leeuwen en onderzoekspunten verdiend, zie [Economie](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (zie [Berichten aan eenheden](how-it-reads.md#messages-to-units)); `despawn`: de laatste rij van een spoor waarvan de eenheid weg is voordat de replay eindigt (zie [Einde van een spoor](ground.md#end-of-a-track)) |
| `track` | wat de viewer als één ding tekent: één leven van een eenheid, of de vlucht van één wapen - `<speler of voertuig> #<hex>` (de viewer toont de naam zonder het deel `#`) |
| `x`, `y`, `z` | de meters van het spel: x oost, y omhoog, z noord (de leesinstructies spiegelen z, zodat noord niet als zuid getekend wordt) |
| `player` | de naam van de speler; een AI-eenheid `<VehicleName> #<uid>` (bijvoorbeeld `F-15A #204`); `uid <n>` als niets haar noemt; voor een wapen wie het afvuurde |
| `userId`, `team` | het Gaijin-id van de speler en het team (`1`, `2`) |
| `ai`, `isPlayer` | `ai` is waar voor elke eenheid die geen spelersaccount bestuurt (missie-eenheden, AI-vliegtuigen, grondobjecten, luchtafweergeschut, schepen zonder speler, plaatshouders), `isPlayer` het tegendeel: een speler is een eenheid waarvan de entiteit een spelersslot met een Gaijin-id noemt. Een wapen heeft die van zijn lanceerder; leeg als dat niet bekend is |
| `match` | het wedstrijd-id (`match` van het wedstrijddocument), op elke rij; de leesinstructies zien het als de sessie, zodat twee geladen replays nooit sporen samenvoegen |
| `life` | `uid#n`: het spoor van één eenheid, afgesneden waar de uid naar een andere eenheid overgaat, de eenheid sneller beweegt dan ze kan (een respawn, een herbewapening, het spel dat haar verplaatst, de client die een verre eenheid corrigeert; zie Teleports in [Hoe het een replay leest](how-it-reads.md#what-is-read-and-the-check)) of lang niet gezien is; `w<hex>` de vlucht van een wapen (`w<hex>#n` na een afsnijding) |
| `uid` | het id van de eenheid in de replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (een tram of spoorwagon die het level plaatst, zie [Sceneeenheden](objectives.md#scene-units-trams-and-rail-wagons)); wapens `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` de replaycamera van de opnemende speler (zie [De camera](ground.md#the-camera)) |
| `type` | het eigen type van het spel waar de resultaten dat noemen (`fighter`, `assault`, `destroyer`, `gun_boat`), anders als `kind` |
| `Vehicle` | het voertuig-id van het spel (`f_15a`, `germ_flakpz_I_Gepard`), waarmee de figuren van de viewer overeenkomen |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | de Engelse naam van het voertuig uit de lokalisatie van je installatie (`Pz.Kpfw. III Ausf. J1`, kort `Pz.III J1`) en de sleutel ervan (`germ_pzkpfw_III_ausf_J_0`); de landmarkeringen van het lettertype van het spel vallen weg. Waar het spel niets noemt, of er geen installatie gevonden is, is de naam het id en de sleutel leeg |
| `mission` | de naam van de eenheid in de missie (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | waar de eenheid naartoe wijst (de kijkvector): vliegtuigen uit de houding van het vluchtmodel, grondeenheden en schepen uit hun eigen houding, wapens langs hun vlucht |
| `heading`, `pitch`, `roll` | hetzelfde in graden; heading is het kompas, met de klok mee vanaf noord, pitch neus omhoog positief, roll rechtervleugel omlaag positief (het vluchtmodel stuurt het tegengestelde teken, zie [Houding, gecontroleerd](aircraft.md#attitude-checked); de rechterkant van een grondeenheid omlaag). De leesinstructies zeggen dat onder `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | de hoofdtoren van een tank - waar het kanon richt, niet waar zijn speler kijkt; de waarde van de replay, gehouden aan de snelheid van de torenaandrijving en gezet op de lijn van elk schot van het hoofdkanon (zie [Torens](ground.md#turrets)): zijn gier ten opzichte van de romp (graden, met de klok mee gezien van boven positief, 0 recht vooruit) en de hoogte van zijn kanon ten opzichte van de romp (graden, omhoog positief); `turrets` elke toren van het voertuig als `gier hoogte;gier hoogte;...` in zijn eigen volgorde (een ongebruikte plek leest `0.00 0.00`). Tanks, luchtafweer op de grond, pantserwagens en vrachtwagens, in client- en serverreplays; niet schepen (zie [Torens](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | de hoofdtoren zoals de replay hem stuurt; `turretYaw` / `gunPitch` zijn die gehouden aan de snelheid van de torenaandrijving en gezet op de lijn van elk schot van het hoofdkanon (zie [Torens](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | waar de speler kijkt (richt met de camera) in de wereld: kompasgraden (0 noord, met de klok mee) en graden omhoog, dezelfde conventie als `aimHeading` / `aimPitch` (anders dan `turretYaw` / `gunPitch`, die ten opzichte van de romp blijven). De tank van elke speler in een serverreplay, de eigen van de opnemende speler in een clientreplay; leeg waar de speler nergens op richt (alle vier de richtfloats 0). De toren volgt het met zijn eigen draaisnelheid, dus de twee verschillen terwijl hij draait (zie [Torens](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | de eigen tank van de opnemende speler: waar hij richt (kompasgraden, graden omhoog, de afstand in m; 2000 als er niets in het vizier zit); camerarijen: waar de speler richt (heading, pitch) |
| `zoom` | camerarijen: de vergroting van de camera (zie [De camera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | de `AB`, `RB` of `SB` van het gevecht, en `ground`, `air` of `naval`, op elke rij (zie [Gevechtsmodus](ground.md#battle-mode)) |
| `extrapolated` | een vliegtuigsample dat de dead reckoning van de client is, geen toestand die hij ontving (zie [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); een sample van een bom, uitgerekend vanaf het afwerpen (zie Bommen zonder vluchtrecords in [Hoe het een replay leest](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | hoe ver de smoother het sample verplaatste (m), en de eigen positie en houding van de replay (roll in het teken van de tabel) |
| `targetX`, `targetY`, `targetZ` | het trefpunt van een `shot` |
| `hitOutcome`, `hitFlags` | de uitkomst van een `shot` op een grondeenheid: `kill`, `critical`, `penetration` of `nonpenetration` (weggekaatst of gestopt: de replay onderscheidt een ricochet niet), uit de bits die de server met de treffer stuurt (`hitFlags`, ruw); leeg waar er geen gestuurd wordt (vliegtuigen, schepen). Zie [Uitkomsten van treffers](hits.md#hit-outcomes) |
| `hitShell` | de granaatsignatuur van een `shot`: vier bytes van het treffer-bericht (ruwe hex); één signatuur kan voor verschillende granaten staan (120 en 125 mm APFSDS delen er één), dus wordt hij ruw bewaard, niet als kaliber gelezen |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | de munitie van een `shot`: het type (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) en id (`125mm_3bm46`) waar een kill de slot van de schutter noemt, anders `explosive` (het trefferschot) of `kinetic`; het `weapon/slot` van het kanon uit zijn herladingen; het kaliber in mm uit de wapenbestanden van de installatie. Zie [Uitkomsten van treffers](hits.md#hit-outcomes) |
| `rpm` | het toerental van de motor van een vliegtuig (het gemiddelde over zijn motoren) zoals het laatst gestuurd, binnen 2 s |
| `vx`, `vy`, `vz` | de snelheid van een vliegtuig zoals zijn vluchtregel die stuurt (m/s, de assen van het spel; snelheden boven 500 m/s lezen 500) |
| `engine`, `afterburner`, `engineCondition` | de motoren van een vliegtuig uit zijn vluchtregel: `off`, `starting`, `running`, `dead` (met `/` ertussen als zijn motoren verschillen); de naverbrander 0-1; een byte die alleen gestuurd wordt nadat de motor getroffen was |
| `weaponName` | kills en doden: het wapen of de munitie in het Engels van je installatie (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | alleen het vliegtuig van de opnemende speler: de gashendel 0-1.1 uit zijn cockpit (1.1 noodvermogen of naverbrander; anders de zestiende van zijn vluchtregel), de besturing -1..1 uit zijn vluchtregel (elevator positief trekkend, aileron positief rollend naar rechts), de resterende rondes per wapen (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | alleen het vliegtuig van de opnemende speler, uit zijn cockpit: aangegeven vliegsnelheid en klimsnelheid (m/s), brandstof, inlaatdruk (atm), landingsgestel (0-1, 1 neer), olie- en cilinderkoptemperatuur, waar zijn cockpit de meter heeft |
| `speed` | m/s over ongeveer twee seconden van het spoor (hier uitgerekend; de replay stuurt geen snelheid voor andere eenheden) |
| `alive` | 0 voor de samples van een eenheid na haar dood (haar wrak): die van een grondeenheid of schip tot het spel haar verwijdert of haar samples eindigen, die van een vliegtuig hoogstens 60 s |
| `otherVehicle`, `otherLife` | het slachtoffer van een `shot`: zijn voertuig en zijn `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | het trefpunt van een `shot` in het eigen assenstelsel van het slachtoffer (m; x vooruit, y omhoog, z links; zie [Berichten aan eenheden](how-it-reads.md#messages-to-units)) en de richting waaruit het schot kwam, omgezet naar dat stelsel met de houding van het slachtoffer op dat moment |
| `hitPart`, `hitFlag` | het treffer-bericht van een `shot`: zijn onderdeelwoord zoals het gestuurd is, en zijn hoogste byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | wat het gevecht kostte en opleverde, en wie won: zie [Economie](economy.md) |
| `other`, `weapon` | kills: de andere partij en het wapen; treffers: wie trof (uit de uid van het record, anders zijn spelersslot), hun voertuig; lanceringen: het wapen; vernietigde modules: wie de eenheid het laatst trof binnen 5 s ervoor, en `part <n>` |

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
