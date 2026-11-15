---
title: La taula
nav_order: 6
lang: "ca"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# La taula {#the-table}

![La taula d'una repetició sintètica, resumida](../assets/img/table.svg)

Una fila per mostra o esdeveniment, 105 columnes ([Llista de columnes](../columns.md),
generada a partir del codi); al peu, sota `heat3d`, hi ha les instruccions de lectura
del visualitzador, de manera que el visualitzador no necessita cap formulari omplert.

| Columna | Què és |
|---|---|
| `time` | segons al rellotge propi de la repetició |
| `event` | `position`; les files d'esdeveniment són sobre la trajectòria al seu moment (entre dues mostres, sobre la línia que les uneix); `kill` (al qui mata), `death` (a la víctima), `hit_critical` / `hit_severe` (a la unitat impactada), `module_destroyed` (a la unitat), `launch` (a la unitat que ha llançat una arma), `impact` (l'última mostra d'una arma quan es va eliminar just després); `explosion` i `flak` (0xD08E, 0xD01F) a la seva posició, amb el tipus `effect`, sense trajectòria, amb la direcció de l'explosió quan en té; `shot` (un projectil que ha impactat, a qui dispara), `gun_shot`, `fire_start`, `fire_stop` (una ràfega d'un canó, no un vehicle en flames), `fire_on`, `fire_off` (un vehicle en flames, mira [Focs als vehicles](hits.md#vehicle-fires)), `reward` (Lleons de plata i punts d'investigació guanyats, mira [Economia](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (mira [Missatges a les unitats](how-it-reads.md#messages-to-units)); `despawn`: l'última fila d'una trajectòria la unitat de la qual ha desaparegut abans que acabi la repetició (mira [Final d'una trajectòria](ground.md#end-of-a-track)) |
| `track` | què dibuixa el visualitzador com una sola cosa: una vida d'una unitat, o el vol d'una arma - `<jugador o vehicle> #<hex>` (el visualitzador mostra el nom sense la part `#`) |
| `x`, `y`, `z` | metres del joc: x est, y amunt, z nord (les indicacions reflecteixen z, de manera que el nord no es dibuixa al sud) |
| `player` | el nom del jugador; una unitat IA `<NomVehicle> #<uid>` (per exemple `F-15A #204`); `uid <n>` quan res no la nomena; per a una arma, qui l'ha llançada |
| `userId`, `team` | l'identificador Gaijin del jugador i l'equip (`1`, `2`) |
| `ai`, `isPlayer` | `ai` és cert per a cada unitat que cap compte de jugador no maneja (unitats de la missió, avions IA, objectius terrestres, canons antiaeris, vaixells sense jugador, marcadors de posició), `isPlayer` és el contrari: un jugador és una unitat l'entitat de la qual nomena una ranura de jugador amb un identificador Gaijin. Una arma té la de qui la llança; buit quan no es coneix |
| `match` | l'identificador de la partida (`match` del document de partida), a cada fila; les indicacions l'agafen com a sessió, de manera que dues repeticions carregades mai no uneixen trajectòries |
| `life` | `uid#n`: la trajectòria d'una unitat, tallada quan el uid passa a una altra unitat, la unitat es mou més ràpid del que pot (una reaparició, una recàrrega, el joc que la mou, el client que corregeix una unitat llunyana; mira Teletransports a [Com llegeix una repetició](how-it-reads.md#what-is-read-and-the-check)) o no es veu durant molt de temps; `w<hex>` el vol d'una arma (`w<hex>#n` després d'un tall) |
| `uid` | l'identificador de la unitat dins la repetició |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (un tramvia o un vagó de tren que col·loca el nivell, mira [Unitats d'escena](objectives.md#scene-units-trams-and-rail-wagons)); armes `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` la càmera de repetició del jugador (mira [La càmera](ground.md#the-camera)) |
| `type` | el tipus propi del joc quan els resultats el nomenen (`fighter`, `assault`, `destroyer`, `gun_boat`), si no, com `kind` |
| `Vehicle` | l'identificador del vehicle al joc (`f_15a`, `germ_flakpz_I_Gepard`), que casen les figures del visualitzador |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | el nom en anglès del vehicle de la teva instal·lació (`Pz.Kpfw. III Ausf. J1`, abreujat `Pz.III J1`) i la seva clau (`germ_pzkpfw_III_ausf_J_0`); les marques de país de la font del joc no hi són. Quan el joc no en dona cap nom, o no es troba cap instal·lació, el nom és l'identificador i la clau és buida |
| `mission` | el nom de la unitat a la missió (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | cap on apunta la unitat (el vector de mirada): els avions amb l'actitud del model de vol, les unitats terrestres i els vaixells amb la seva pròpia, les armes segons el seu vol |
| `heading`, `pitch`, `roll` | el mateix en graus; heading és la brúixola, en sentit horari des del nord, pitch positiu amb el morro amunt, roll positiu amb l'ala dreta avall (el model de vol envia el signe contrari, mira [Actitud, comprovada](aircraft.md#attitude-checked); el costat dret d'una unitat terrestre avall). Les pistes ho indiquen a `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | la torreta principal d'un tanc - on apunta el canó, no on mira el seu jugador; el valor de la repetició, subjectat a la velocitat de la maquinària de la torreta i fixat a la línia de cada tret del canó principal (mira [Torretes](ground.md#turrets)): el seu guinyol respecte al casc (graus, positiu en sentit horari vist des de dalt, 0 tot endavant) i l'elevació del canó respecte al casc (graus, positiu amunt); `turrets` totes les torretes del vehicle com `yaw pitch;yaw pitch;...` en el seu propi ordre (una ranura sense ús es llegeix `0.00 0.00`). Tancs, SPAA, APC i camions, en repeticions de client i de servidor; no vaixells (mira [Torretes](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | la torreta principal tal com l'envia la repetició; `turretYaw` / `gunPitch` són aquesta subjectada a la velocitat de la maquinària i fixada a la línia de cada tret del canó principal (mira [Torretes](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | cap on mira el jugador (apunta amb la càmera) al món: graus de brúixola (0 nord, en sentit horari) i graus amunt, la mateixa convenció que `aimHeading` / `aimPitch` (a diferència de `turretYaw` / `gunPitch`, que es queden relatius al casc). El tanc de cada jugador en una repetició de servidor, el propi del jugador que grava en una repetició de client; buit quan el jugador no apunta enlloc (els quatre floats d'apuntament a 0). La torreta el segueix a la seva pròpia velocitat de gir, de manera que les dues difereixen mentre gira (mira [Torretes](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | el tanc propi del jugador que grava: cap on apunta (graus de brúixola, graus amunt, la distància en m; 2000 quan no hi ha res a la mira); files de càmera: cap on apunta el jugador (heading, pitch) |
| `zoom` | files de càmera: l'augment de la càmera (mira [La càmera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | el `AB`, `RB` o `SB` de la batalla, i `ground`, `air` o `naval`, a cada fila (mira [Mode de batalla](ground.md#battle-mode)) |
| `extrapolated` | una mostra d'avió que és l'estimació per navegació del client, no un estat rebut (mira [Estimació per navegació](aircraft.md#dead-reckoning-and-the-smoother)); una mostra d'una bomba calculada a partir del seu llançament (mira Bombes sense registres de vol a [Com llegeix una repetició](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | quant ha mogut l'alisador la mostra (m), i la posició i l'actitud pròpies de la repetició (roll amb el signe de la taula) |
| `targetX`, `targetY`, `targetZ` | el punt d'impacte d'un `shot` |
| `hitOutcome`, `hitFlags` | el resultat d'un `shot` sobre una unitat terrestre: `kill`, `critical`, `penetration` o `nonpenetration` (rebotat o aturat: la repetició no distingeix un rebot), a partir dels bits que envia el servidor amb l'impacte (`hitFlags`, en brut); buit quan no n'envia cap (avions, vaixells). Mira [Resultats dels impactes](hits.md#hit-outcomes) |
| `hitShell` | la signatura de projectil d'un `shot`: quatre bytes del missatge d'impacte (hex en brut); una signatura pot representar projectils diferents (els APFSDS de 120 i 125 mm en comparteixen una), per això es guarda en brut, no es llegeix com a calibre |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | la munició d'un `shot`: el seu tipus (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) i identificador (`125mm_3bm46`) quan una mort nomena la ranura del tirador, si no `explosive` (la ràfega d'impacte) o `kinetic`; el `weapon/slot` del canó a partir de les seves recàrregues; el calibre en mm dels fitxers d'armes de la instal·lació. Mira [Resultats dels impactes](hits.md#hit-outcomes) |
| `rpm` | les rpm del motor d'un avió (la mitjana dels seus motors) tal com l'últim que es va enviar, en 2 s |
| `vx`, `vy`, `vz` | la velocitat d'un avió tal com l'envia la seva entrada de vol (m/s, els eixos del joc; les velocitats per sobre de 500 m/s es llegeixen com a 500) |
| `engine`, `afterburner`, `engineCondition` | els motors d'un avió a partir de la seva entrada de vol: `off`, `starting`, `running`, `dead` (unides amb `/` quan els seus motors difereixen); el postcombustor 0-1; un byte que només s'envia després que el motor rebi un impacte |
| `weaponName` | morts i baixes: l'arma o la munició en anglès de la teva instal·lació (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | només l'avió del jugador que grava: l'accelerador 0-1.1 de la seva cabina (1.1 potència d'emergència de guerra o postcombustor; si no, les quinzenes de la seva entrada de vol), els comandaments -1..1 de la seva entrada de vol (elevator positiu tirant, aileron positiu rodant a la dreta), les municions que queden per arma (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | només l'avió del jugador que grava, de la seva cabina: velocitat indicada i velocitat de pujada (m/s), combustible, pressió del col·lector (atm), tren d'aterratge (0-1, 1 baixat), temperatura de l'oli i del cap de cilindres, quan la seva cabina té l'indicador |
| `speed` | m/s sobre uns dos segons de la trajectòria (calculat aquí; la repetició no envia velocitat per a les altres unitats) |
| `alive` | 0 per a les mostres d'una unitat després de la seva mort (les seves restes): la d'una unitat terrestre o un vaixell fins que el joc la treu o s'acaben les seves mostres, la d'un avió com a molt 60 s |
| `otherVehicle`, `otherLife` | la víctima d'un `shot`: el seu vehicle i la seva `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | el punt d'impacte d'un `shot` al marc propi de la víctima (m; x endavant, y amunt, z esquerra; mira [Missatges a les unitats](how-it-reads.md#messages-to-units)) i la manera com va arribar el tret, girada a aquell marc per l'actitud de la víctima en aquell moment |
| `hitPart`, `hitFlag` | el missatge d'impacte d'un `shot`: la seva paraula de part tal com s'envia, i el seu byte alt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | què ha costat i què ha guanyat la batalla, i qui ha guanyat: mira [Economia](economy.md) |
| `other`, `weapon` | morts: l'altre bàndol i l'arma; impactes: qui ha impactat (de l'uid del registre, si no de la ranura del jugador), el seu vehicle; llançaments: l'arma; mòduls destruïts: qui ha impactat la unitat per última vegada dins els 5 s anteriors, i `part <n>` |

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
