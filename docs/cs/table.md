---
title: "Tabulka"
nav_order: 6
lang: "cs"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabulka {#the-table}

![Tabulka syntetického replaye, shrnutá](../assets/img/table.svg)

Jeden řádek na vzorek nebo událost, 105 sloupců ([Seznam sloupců](../columns.md), generovaný z kódu); v zápatí, pod `heat3d`, jsou
pokyny pro čtení prohlížečem, takže prohlížeč nepotřebuje nic vyplňovat.

| Sloupec | Co |
|---|---|
| `time` | vteřiny na vlastních hodinách replaye |
| `event` | `position`; řádky událostí leží na trati v jejich okamžiku (mezi dvěma vzorky, na přímce mezi nimi); `kill` (u zabijáka), `death` (u oběti), `hit_critical` / `hit_severe` (u zasažené jednotky), `module_destroyed` (u jednotky), `launch` (u jednotky, která vypustila zbraň), `impact` (poslední vzorek zbraně, když byla odstraněna hned potom); `explosion` a `flak` (0xD08E, 0xD01F) na své pozici, druh `effect`, bez tratě, se směrem výbuchu, kde ho má; `shot` (projektil, který zasáhl, u střelce), `gun_shot`, `fire_start`, `fire_stop` (dávka děla, ne vozidlo v plamenech), `fire_on`, `fire_off` (vozidlo v plamenech, viz [Požáry vozidel](hits.md#vehicle-fires)), `reward` (získané Stříbrné lvy a výzkumné body, viz [Ekonomika](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (viz [Zprávy jednotkám](how-it-reads.md#messages-to-units)); `despawn`: poslední řádek tratě, jejíž jednotka zmizela dřív, než replay skončí (viz [Konec tratě](ground.md#end-of-a-track)) |
| `track` | co prohlížeč kreslí jako jednu věc: jeden život jednotky, nebo let jedné zbraně - `<player or vehicle> #<hex>` (prohlížeč ukazuje jméno bez části `#`) |
| `x`, `y`, `z` | metry hry: x na východ, y nahoru, z na sever (nápovědy zrcadlí z, takže sever se nekreslí na jih) |
| `player` | jméno hráče; jednotka AI `<VehicleName> #<uid>` (například `F-15A #204`); `uid <n>`, když ji nic nejmenuje; u zbraně, kdo ji vypustil |
| `userId`, `team` | Gaijin id hráče a tým (`1`, `2`) |
| `ai`, `isPlayer` | `ai` je true u každé jednotky, kterou neřídí žádný účet hráče (jednotky misí, letadla AI, pozemní cíle, protiletadlová děla, lodě bez hráče, zástupné jednotky), `isPlayer` opak: hráč je jednotka, jejíž entita jmenuje slot hráče s Gaijin id. Zbraň má svého vypouštěče; prázdné, když není známo |
| `match` | id zápasu (`match` z dokumentu zápasu), na každém řádku; nápovědy ho berou jako relaci, takže dva načtené replaye se nikdy nespojí do jedné tratě |
| `life` | `uid#n`: trať jedné jednotky, přerušená tam, kde se uid přesune na jinou jednotku, jednotka se pohne rychleji, než může (respawn, přezbrojení, hra ji přesunula, klient opravil vzdálenou jednotku; viz Teleporty v [Jak se replay čte](how-it-reads.md#what-is-read-and-the-check)), nebo je dlouho neviděna; `w<hex>` let zbraně (`w<hex>#n` po přerušení) |
| `uid` | id jednotky v replayi |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvaj nebo vagón na kolejích, které úroveň umisťuje, viz [Jednotky scény](objectives.md#scene-units-trams-and-rail-wagons)); zbraně `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` kamera replaye hráče, který nahrával (viz [Kamera](ground.md#the-camera)) |
| `type` | vlastní typ hry, tam kde ho výsledky jmenují (`fighter`, `assault`, `destroyer`, `gun_boat`), jinak jako `kind` |
| `Vehicle` | vlastní id vozidla ve hře (`f_15a`, `germ_flakpz_I_Gepard`), podle kterého prohlížeč páruje figury |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | anglický název vozidla z lokalizace vaší instalace (`Pz.Kpfw. III Ausf. J1`, krátký `Pz.III J1`) a jeho klíč (`germ_pzkpfw_III_ausf_J_0`); značky zemí z písma hry jsou vynechány. Kde hra nic nejmenuje, nebo se nenajde instalace, je název id a klíč prázdný |
| `mission` | název jednotky v misi (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kam jednotka míří (vektor pohledu): letadla z postoje letového modelu, pozemní jednotky a lodě z vlastního, zbraně podle jejich letu |
| `heading`, `pitch`, `roll` | totéž ve stupních; kurz je kompas, po směru hodinových ručiček od severu, sklon kladný nos nahoru, náklon kladný pravé křídlo dolů (letový model posílá opačné znaménko, viz [Postoj, ověřený](aircraft.md#attitude-checked); pravá strana pozemní jednotky dolů). Nápovědy to říkají pod `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | hlavní věž tanku - kam míří dělo, ne kam se dívá jeho hráč; hodnota replaye držená na rychlosti pohonu věže a nastavená na přímku každého výstřelu hlavním dělem (viz [Věže](ground.md#turrets)): její natočení vzhledem k trupu (stupně, po směru hodinových ručiček při pohledu shora kladné, 0 rovně vpřed) a sklon děla vzhledem k trupu (stupně, nahoru kladné); `turrets` každá věž vozidla jako `yaw pitch;yaw pitch;...` v jejím vlastním pořadí (nepoužitý slot se čte `0.00 0.00`). Tanky, SPAA, obrněná vozidla a nákladní auta v klientských i serverových replayích; ne lodě (viz [Věže](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | hlavní věž tak, jak ji replay posílá; `turretYaw` / `gunPitch` jsou ona držená na rychlosti pohonu věže a nastavená na přímku každého výstřelu hlavním dělem (viz [Věže](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kam hráč míří (míří kamerou) ve světě: stupně kompasu (0 sever, po směru hodinových ručiček) a stupně nahoru, stejná konvence jako `aimHeading` / `aimPitch` (na rozdíl od `turretYaw` / `gunPitch`, které zůstávají vzhledem k trupu). Tank každého hráče na serverovém replayi, na klientském replayi vlastní tank hráče, který nahrával; prázdné, kde hráč nic nemíří (všechna čtyři plovoucí čísla míření 0). Věž ho sleduje svou vlastní rychlostí otáčení, takže se oba liší, dokud se točí (viz [Věže](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | vlastní tank hráče, který nahrával: kam míří (stupně kompasu, stupně nahoru, vzdálenost v m; 2000, když nic není v zaměřovači); řádky kamery: kam hráč míří (kurz, sklon) |
| `zoom` | řádky kamery: zvětšení kamery (viz [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` nebo `SB` bitvy, a `ground`, `air` nebo `naval`, na každém řádku (viz [Režim bitvy](ground.md#battle-mode)) |
| `extrapolated` | vzorek letadla, který je odhad polohy klienta (dead reckoning), ne stav, který přijal (viz [Odhad polohy](aircraft.md#dead-reckoning-and-the-smoother)); vzorek bomby dopočítaný od jejího vypuštění (viz Bomby bez letových záznamů v [Jak se replay čte](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | jak daleko vyhlazovač posunul vzorek (m), a vlastní pozice a postoj replaye (náklon ve znaménku tabulky) |
| `targetX`, `targetY`, `targetZ` | bod zásahu řádku `shot` |
| `hitOutcome`, `hitFlags` | výsledek `shot` na pozemní jednotce: `kill`, `critical`, `penetration` nebo `nonpenetration` (odraženo nebo zastaveno: replay neodliší odraz), z bitů, které server posílá se zásahem (`hitFlags`, surové); prázdné tam, kde se neposílá (letadla, lodě). Viz [Výsledky zásahů](hits.md#hit-outcomes) |
| `hitShell` | podpis střely `shot`: čtyři bajty zprávy o zásahu (surový hex); jeden podpis může znamenat různé střely (120 a 125mm APFSDS sdílejí jeden), proto se drží surový, nečte se jako ráže |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | munice `shot`: její typ (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) a id (`125mm_3bm46`), kde zabití pojmenuje slot střelce, jinak `explosive` (dávka zásahu) nebo `kinetic`; `weapon/slot` děla z jeho přebíjení; ráže v mm z váhových souborů zbraní instalace. Viz [Výsledky zásahů](hits.md#hit-outcomes) |
| `rpm` | otáčky motoru letadla (průměr přes jeho motory), jak byly naposledy poslány, do 2 s |
| `vx`, `vy`, `vz` | rychlost letadla tak, jak ji posílá jeho záznam letu (m/s, osy hry; rychlosti nad 500 m/s se čtou jako 500) |
| `engine`, `afterburner`, `engineCondition` | motory letadla z jeho záznamu letu: `off`, `starting`, `running`, `dead` (oddělené `/`, když se jeho motory liší); přídavné spalování 0-1; bajt poslaný jen poté, co byl motor zasažen |
| `weaponName` | zabití a smrti: zbraň nebo munice v anglickém názvu z vaší instalace (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | jen letadlo hráče, který nahrával: plyn 0-1,1 z jeho kokpitu (1,1 válečný nouzový výkon nebo přídavné spalování; jinak patnáctiny z jeho záznamu letu), ovládání -1..1 z jeho záznamu letu (výškovka kladná při tahu, křidélka kladná při náklonu doprava), zbývající náboje na zbraň (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | jen letadlo hráče, který nahrával, z jeho kokpitu: indikovaná vzdušná rychlost a rychlost stoupání (m/s), palivo, tlak v sání (atm), podvozek (0-1, 1 vysunuto), teplota oleje a hlavy válců, kde kokpit má ručičku |
| `speed` | m/s přes asi dvě vteřiny tratě (počítáno zde; replay neposílá rychlost pro ostatní jednotky) |
| `alive` | 0 u vzorků jednotky po její smrti (její vrak): u pozemní jednotky nebo lodi, dokud ji hra neodstraní nebo její vzorky neskončí, u letadla nejvýš 60 s |
| `otherVehicle`, `otherLife` | oběť `shot`: její vozidlo a její `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | bod zásahu `shot` v rámci oběti (m; x dopředu, y nahoru, z vlevo; viz [Zprávy jednotkám](how-it-reads.md#messages-to-units)) a směr, odkud výstřel přišel, převedený do tohoto rámce postojem oběti tehdy |
| `hitPart`, `hitFlag` | zpráva o zásahu `shot`: jeho slovo části tak, jak bylo posláno, a jeho nejvyšší bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | co bitva stála a vynesla, a kdo vyhrál: viz [Ekonomika](economy.md) |
| `other`, `weapon` | zabití: druhá strana a zbraň; zásahy: kdo zasáhl (z uid záznamu, jinak ze slotu hráče), jejich vozidlo; vypuštění: zbraň; zničené moduly: kdo jednotku naposledy zasáhl do 5 s předtím, a `part <n>` |

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
