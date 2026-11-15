---
title: "A táblázat"
nav_order: 6
lang: hu
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# A táblázat {#the-table}

![Egy szintetikus visszajátszás táblázata, összefoglalva](../assets/img/table.svg)

Mintánként vagy eseményenként egy sor, 105 oszloppal ([Oszloplista](../columns.md), a kódból generálva); a
láblécben, a `heat3d` alatt találhatók a megjelenítő olvasási utasításai, így a megjelenítőnek nem kell semmit
kitöltenie.

| Oszlop | Mi |
|---|---|
| `time` | másodpercek a visszajátszás saját órája szerint |
| `event` | `position`; az eseménysorok a pályán vannak a pillanatukban (két minta között, a közöttük húzódó vonalon); `kill` (a gyilkosnál), `death` (az áldozatnál), `hit_critical` / `hit_severe` (az eltalált egységnél), `module_destroyed` (az egységnél), `launch` (az egységnél, amely fegyvert indított), `impact` (egy fegyver utolsó mintája, ha azonnal a találat után eltávolították); `explosion` és `flak` (0xD08E, 0xD01F) a helyükön, `effect` fajtával, pálya nélkül, ahol van, a robbanás irányával; `shot` (egy találó lövedék, a lövőnél), `gun_shot`, `fire_start`, `fire_stop` (egy ágyú sorozata, nem égő jármű), `fire_on`, `fire_off` (egy égő jármű, lásd [Járműtüzek](hits.md#vehicle-fires)), `reward` (megszerzett ezüstoroszlánok és kutatási pontok, lásd [Gazdaság](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (lásd [Üzenetek egységeknek](how-it-reads.md#messages-to-units)); `despawn`: egy pálya utolsó sora, amelynek egysége még a visszajátszás vége előtt eltűnt (lásd [Egy pálya vége](ground.md#end-of-a-track)) |
| `track` | amit a megjelenítő egy egységként rajzol: egy egység egy élete, vagy egy fegyver repülése – `<player or vehicle> #<hex>` (a megjelenítő a `#` rész nélkül mutatja a nevet) |
| `x`, `y`, `z` | a játék méterei: x kelet, y fel, z észak (a súgók tükrözik a z-t, így az észak nem délre rajzolódik) |
| `player` | a játékos neve; egy MI-egység `<VehicleName> #<uid>` (például `F-15A #204`); `uid <n>`, ha semmi sem nevezi meg; fegyvernél az, aki kilőtte |
| `userId`, `team` | a játékos Gaijin-azonosítója és a csapat (`1`, `2`) |
| `ai`, `isPlayer` | `ai` igaz minden olyan egységre, amelyet egyetlen játékosfiók sem vezet (küldetésegységek, MI-repülőgépek, földi célpontok, légvédelmi ágyúk, játékos nélküli hajók, helykitöltők), `isPlayer` az ellenkezője: játékos az az egység, amelynek entitása egy játékos-helyet nevez meg Gaijin-azonosítóval. A fegyvernek a kilövőjéé; üres, ha nem ismert |
| `match` | a meccs azonosítója (a meccsdokumentum `match` mezője), minden soron; a súgók munkamenetként képezik le, így két betöltött visszajátszás soha nem kapcsolódik egymáshoz |
| `life` | `uid#n`: egy egység pályája, ott vágva, ahol az uid másik egységre száll át, ahol az egység gyorsabban mozdul, mint ahogy tudna (újraéledés, újratöltés, a játék mozgatja, a kliens korrigál egy távoli egységet; lásd a Teleportálások részt a [Hogyan olvassa a visszajátszást](how-it-reads.md#what-is-read-and-the-check) oldalon), vagy sokáig nem látták; `w<hex>` egy fegyver repülése (`w<hex>#n` egy vágás után) |
| `uid` | az egység azonosítója a visszajátszásban |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (a pálya által elhelyezett villamos vagy sínkocsi, lásd [Jelenetegységek](objectives.md#scene-units-trams-and-rail-wagons)); fegyverek: `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` a felvevő játékos visszajátszás-kamerája (lásd [A kamera](ground.md#the-camera)) |
| `type` | a játék saját típusa, ahol az eredmények megnevezik (`fighter`, `assault`, `destroyer`, `gun_boat`), különben mint a `kind` |
| `Vehicle` | a játék járműazonosítója (`f_15a`, `germ_flakpz_I_Gepard`), amelyhez a megjelenítő alakjai illeszkednek |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | a jármű angol neve a telepítésed lokalizációjából (`Pz.Kpfw. III Ausf. J1`, rövid alakja `Pz.III J1`), és a kulcsa (`germ_pzkpfw_III_ausf_J_0`); a játék betűtípusának országjelei kimaradnak. Ahol a játék nem nevez meg semmit, vagy nincs telepítés, a név az azonosító, a kulcs pedig üres |
| `mission` | az egység neve a küldetésben (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | amerre az egység néz (a nézési vektor): a repülőgépeknél a repülési modell állásából, a földi egységeknél és hajóknál a sajátjukból, a fegyvereknél a repülési pályájuk mentén |
| `heading`, `pitch`, `roll` | ugyanez fokban; az irány az iránytű, az óramutató járásával megegyezően, északtól; a dőlés (pitch) orral felfelé pozitív, a billenés (roll) jobb szárny lefelé pozitív (a repülési modell az ellenkező előjelet küldi, lásd [Állás, ellenőrizve](aircraft.md#attitude-checked); a földi egységnél a jobb oldal lefelé). A súgók ezt a `conventions` alatt írják le |
| `turretYaw`, `gunPitch`, `turrets` | egy tank fő tornya – ahová az ágyú mutat, nem ahová a játékosa néz; a visszajátszás értéke, a toronyhajtás sebességére korlátozva és minden fő ágyúlövés vonalára állítva (lásd [Tornyok](ground.md#turrets)): az elfordulása a törzshöz képest (fok, felülnézetből az óramutató járásával megegyezően pozitív, 0 egyenesen előre), és az ágyú emelkedése a törzshöz képest (fok, felfelé pozitív); a `turrets` a jármű minden tornyát `yaw pitch;yaw pitch;...` formában adja a saját sorrendjében (egy nem használt rekesz `0.00 0.00`). Tankok, légvédelmi páncélosok (SPAA), páncélozott szállító-járművek és teherautók, kliens- és szerver-visszajátszásban; hajók nem (lásd [Tornyok](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | a fő torony úgy, ahogy a visszajátszás elküldi; a `turretYaw` / `gunPitch` ennek a toronyhajtás sebességére korlátozott és minden fő ágyúlövés vonalára állított változata (lásd [Tornyok](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | ahová a játékos néz (a kamerával céloz) a világban: iránytű-fok (0 észak, az óramutató járásával) és felfelé fok, ugyanaz a jelölés, mint az `aimHeading` / `aimPitch` (ellentétben a `turretYaw` / `gunPitch`-csal, amelyek a törzshöz képest maradnak). Minden játékos tankja szerver-visszajátszásban, a felvevő játékosé a saját kliens-visszajátszásban; üres, ahol a játékos sehová sem céloz (mind a négy célozási lebegőpontos érték 0). A torony a saját fordulási sebességével követi, így a kettő eltér, amíg fordul (lásd [Tornyok](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | a felvevő játékos saját tankja: hová céloz (iránytű-fok, felfelé fok, a távolság m-ben; 2000, ha semmi sincs a célkeresőben); kamera-sorok: hová céloz a játékos (irány, dőlés) |
| `zoom` | kamera-sorok: a kamera nagyítása (lásd [A kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | a csata `AB`, `RB` vagy `SB`, és `ground`, `air` vagy `naval`, minden soron (lásd [Csatamód](ground.md#battle-mode)) |
| `extrapolated` | egy repülőgép-minta, amely a kliens holtpont-számítása, nem pedig kapott állapot (lásd [Holtpont-számítás](aircraft.md#dead-reckoning-and-the-smoother)); egy bomba mintája, amelyet a kilövéséből számoltunk ki (lásd a Repülési rekord nélküli bombák részt a [Hogyan olvassa a visszajátszást](how-it-reads.md#what-is-read-and-the-check) oldalon) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | mennyivel mozdította a simító a mintát (m), és a visszajátszás saját helyzete és állása (a billenés a táblázat előjelével) |
| `targetX`, `targetY`, `targetZ` | egy `shot` találati pontja |
| `hitOutcome`, `hitFlags` | egy `shot` kimenetele egy földi egységen: `kill`, `critical`, `penetration` vagy `nonpenetration` (lepattant vagy megállt: a visszajátszás nem különbözteti meg a ricochet-et), a találattal együtt a szerver által küldött bitekből (`hitFlags`, nyers); üres, ahol nem küldenek (repülőgépek, hajók). Lásd [Találatok kimenetele](hits.md#hit-outcomes) |
| `hitShell` | egy `shot` lövedék-azonosítója: a találat üzenetének négy bájtja (nyers hex); egy azonosító különböző lövedékeket is jelölhet (a 120 és 125 mm-es APFSDS ugyanazt), ezért nyersen tartjuk meg, nem olvassuk kalibernek |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | egy `shot` lőszere: típusa (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) és azonosítója (`125mm_3bm46`), ahol egy ölés megnevezi a lövő rekeszét, különben `explosive` (a találat robbanása) vagy `kinetic`; az ágyú `weapon/slot` értéke a töltéseiből; a kaliber mm-ben a telepítés fegyverfájljaiból. Lásd [Találatok kimenetele](hits.md#hit-outcomes) |
| `rpm` | egy repülőgép motorjának fordulatszáma (a motorjai átlaga), az utoljára küldött érték, 2 s-on belül |
| `vx`, `vy`, `vz` | egy repülőgép sebessége, ahogy a repülési bejegyzése küldi (m/s, a játék tengelyei; az 500 m/s feletti sebességek 500-at mutatnak) |
| `engine`, `afterburner`, `engineCondition` | egy repülőgép motorjai a repülési bejegyzéséből: `off`, `starting`, `running`, `dead` (`/`-jellel összekötve, ha a motorjai eltérnek); az utánégető 0-1; egy bájt, amely csak miután a motort eltalálták, érkezik |
| `weaponName` | ölések és halálok: a fegyver vagy lőszer neve a telepítésed angol nyelvű szövegeiben (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | csak a felvevő játékos repülőgépe: a gázkar 0-1,1 a fedélzetéről (1,1 háborús vészteljesítmény vagy utánégető; különben a repülési bejegyzés tizenötödei), a vezérlők -1..1 a repülési bejegyzéséből (a magassági kormány pozitív húzásnál, a csűrő pozitív jobbra dőlésnél), a fegyverenkénti hátralévő lőszer (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | csak a felvevő játékos repülőgépe, a fedélzetéről: a jelzett légsebesség és emelkedési sebesség (m/s), üzemanyag, töltőnyomás (atm), futómű (0-1, 1 lent), olaj- és hengerfej-hőmérséklet, ahol a fedélzeten van a műszer |
| `speed` | m/s a pálya körülbelül két másodpercén át (itt számolva; a visszajátszás más egységekre nem küld sebességet) |
| `alive` | 0 egy egység mintáin a halála után (a roncsa): egy föld- vagy hajó-egységnél addig, amíg a játék el nem távolítja, vagy a mintái véget nem érnek; egy repülőgépnél legfeljebb 60 s-ig |
| `otherVehicle`, `otherLife` | egy `shot` áldozata: a járműve és annak `life` értéke |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | egy `shot` találati pontja az áldozat saját koordinátarendszerében (m; x előre, y fel, z balra; lásd [Üzenetek egységeknek](how-it-reads.md#messages-to-units)), és a lövés iránya, ebbe a koordinátarendszerbe fordítva az áldozat akkori állásával |
| `hitPart`, `hitFlag` | egy `shot` találati üzenete: a része szóként, ahogy elküldik, és a felső bájtja |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | mibe került és mit hozott a csata, és ki nyert: lásd [Gazdaság](economy.md) |
| `other`, `weapon` | ölések: a másik oldal és a fegyver; találatok: aki eltalálta (a rekord uid-jából, különben a játékos-helyéből), a járműve; indítások: a fegyver; megsemmisült modulok: aki utoljára eltalálta az egységet 5 s-on belül előtte, és `part <n>` |

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
