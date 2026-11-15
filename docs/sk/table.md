---
title: "Tabuľka"
nav_order: 6
lang: sk
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabuľka {#the-table}

![Tabuľka syntetického replaye, zhrnutá](../assets/img/table.svg)

Jeden riadok na vzorku alebo udalosť, 105 stĺpcov ([Zoznam stĺpcov](../columns.md), generovaný z kódu); v päte, pod `heat3d`,
pokyny na čítanie pre prehliadač, takže prehliadač nepotrebuje nič vypĺňať.

| Stĺpec | Čo |
|---|---|
| `time` | sekundy na vlastných hodinách replaye |
| `event` | `position`; riadky udalostí ležia na stope v ich okamihu (medzi dvoma vzorkami, na priamke medzi nimi); `kill` (pri vrahovi), `death` (pri obeti), `hit_critical` / `hit_severe` (pri zasiahnutej jednotke), `module_destroyed` (pri jednotke), `launch` (pri jednotke, ktorá vypustila zbraň), `impact` (posledná vzorka zbrane, keď bola odstránená ihneď po nej); `explosion` a `flak` (0xD08E, 0xD01F) na svojej pozícii, druh `effect`, bez stopy, so smerom výbuchu, ak ho má; `shot` (projektil, ktorý zasiahol, pri strelcovi), `gun_shot`, `fire_start`, `fire_stop` (dávka delostrelectva, nie vozidlo v plameňoch), `fire_on`, `fire_off` (vozidlo v plameňoch, pozri [Požiare vozidiel](hits.md#vehicle-fires)), `reward` (zarobené Silver Lions a výskumné body, pozri [Ekonomika](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (pozri [Správy pre jednotky](how-it-reads.md#messages-to-units)); `despawn`: posledný riadok stopy, ktorej jednotka zanikla pred koncom replaye (pozri [Koniec stopy](ground.md#end-of-a-track)) |
| `track` | to, čo prehliadač kreslí ako jednu vec: jeden život jednotky alebo let jednej zbrane - `<player or vehicle> #<hex>` (prehliadač zobrazuje názov bez časti `#`) |
| `x`, `y`, `z` | metre hry: x na východ, y nahor, z na sever (nápovedy zrkadlia z, takže sever sa nekreslí ako juh) |
| `player` | meno hráča; jednotka AI `<VehicleName> #<uid>` (napríklad `F-15A #204`); `uid <n>`, keď ju nič nepomenúva; pri zbrani, kto ju vypustil |
| `userId`, `team` | Gaijin id hráča a tím (`1`, `2`) |
| `ai`, `isPlayer` | `ai` true pri každej jednotke, ktorú neriadi herný účet (jednotky misie, lietadlá AI, pozemné ciele, protilietadlové zbrane, lode bez hráča, zástupné jednotky), `isPlayer` opak: hráč je jednotka, ktorej entita pomenúva slot hráča s Gaijin id. Zbraň má tú svojho odpaľovača; prázdne, keď nie je známe |
| `match` | id zápasu (`match` dokumentu zápasu) na každom riadku; nápovedy ho berú ako reláciu, takže dva načítané replaye nikdy nespájajú stopy |
| `life` | `uid#n`: stopa jednej jednotky, prerezaná tam, kde uid prejde na inú jednotku, jednotka sa pohne rýchlejšie, než môže (oživenie, doplnenie, hra ju pohla, klient korigoval vzdialenú jednotku; pozri Teleporty v [Ako sa replay číta](how-it-reads.md#what-is-read-and-the-check)), alebo ju dlho nevidieť; `w<hex>` let zbrane (`w<hex>#n` po reze) |
| `uid` | id jednotky v replaye |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (električka alebo vagón na koľajniciach, ktoré level umiestni, pozri [Scénické jednotky](objectives.md#scene-units-trams-and-rail-wagons)); zbrane `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` kamera replaye hráča, ktorý replay nahral (pozri [Kamera](ground.md#the-camera)) |
| `type` | vlastný typ hry, ak ho výsledky uvádzajú (`fighter`, `assault`, `destroyer`, `gun_boat`), inak ako `kind` |
| `Vehicle` | herné id vozidla (`f_15a`, `germ_flakpz_I_Gepard`), podľa ktorého sa párujú postavy prehliadača |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | anglický názov vozidla z lokalizácie vašej inštalácie (`Pz.Kpfw. III Ausf. J1`, krátky `Pz.III J1`) a jeho kľúč (`germ_pzkpfw_III_ausf_J_0`); značky krajín z písma hry sú vynechané. Tam, kde hra nič nepomenúva, alebo sa nenašla inštalácia, je názov id a kľúč prázdny |
| `mission` | názov jednotky v misii (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kam jednotka smeruje (vektor pohľadu): lietadlá z postoja modelu letu, pozemné jednotky a lode z ich vlastného, zbrane pozdĺž svojho letu |
| `heading`, `pitch`, `roll` | to isté v stupňoch; smer hlavy je kompas, v smere hodinových ručičiek od severu, sklon nos nahor kladný, náklon pravé krídlo nižšie kladný (model letu posiela opačné znamienko, pozri [Postoj, overený](aircraft.md#attitude-checked); pravá strana pozemnej jednotky nižšie). Nápovedy to uvádzajú pod `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | hlavná veža tanku - kam ukazuje delo, nie kam sa pozerá jeho hráč; hodnota replaye držaná na rýchlosti pohonu veže a nastavená na priamku každého výstrelu hlavným delom (pozri [Veže](ground.md#turrets)): jej uhol voči trupu (stupne, v smere hodinových ručičiek pri pohľade zhora kladný, 0 rovno vpred) a sklon jeho dela voči trupu (stupne, nahor kladný); `turrets` každá veža vozidla ako `yaw pitch;yaw pitch;...` v jeho vlastnom poradí (nepoužitý slot je `0.00 0.00`). Tanky, SPAA, obrnené transportéry a nákladiaky, v klientských aj serverových replayoch; nie lode (pozri [Veže](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | hlavná veža tak, ako ju replay posiela; `turretYaw` / `gunPitch` sú ona držaná na rýchlosti pohonu veže a nastavená na priamku každého výstrelu hlavným delom (pozri [Veže](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kam hráč hľadí (mieri kamerou) vo svete: stupne kompasu (0 sever, v smere hodinových ručičiek) a stupne nahor, rovnaká konvencia ako `aimHeading` / `aimPitch` (na rozdiel od `turretYaw` / `gunPitch`, ktoré zostávajú voči trupu). Tank každého hráča v serverovom replaye, vlastný tank hráča, ktorý replay nahral, v klientskom replayi; prázdne, kde hráč nemieri nikam (všetky štyri plávajúce hodnoty mierenia 0). Veža to sleduje rýchlosťou vlastného otáčania, takže sa obe líšia, kým sa otáča (pozri [Veže](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | vlastný tank hráča, ktorý replay nahral: kam mieri (stupne kompasu, stupne nahor, vzdialenosť v m; 2000, keď nič nie je v zameriavači); riadky kamery: kam hráč mieri (smer, sklon) |
| `zoom` | riadky kamery: zväčšenie kamery (pozri [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` alebo `SB` bitky a `ground`, `air` alebo `naval`, na každom riadku (pozri [Režim bitky](ground.md#battle-mode)) |
| `extrapolated` | vzorka lietadla, ktorá je odhadom klienta, nie stavom, ktorý prijal (pozri [Odhad polohy](aircraft.md#dead-reckoning-and-the-smoother)); vzorka bomby dopočítaná od jej vypustenia (pozri Bomby bez záznamov letu v [Ako sa replay číta](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | o koľko vyhladzovač pohol vzorku (m), a vlastná poloha a postoj replaye (náklon v znamienku tabuľky) |
| `targetX`, `targetY`, `targetZ` | bod zásahu riadku `shot` |
| `hitOutcome`, `hitFlags` | výsledok `shot` na pozemnej jednotke: `kill`, `critical`, `penetration` alebo `nonpenetration` (odrazený alebo zastavený: replay odraz od prieniku nerozlišuje), z bitov, ktoré server posiela so zásahom (`hitFlags`, surové); prázdne, keď sa neposielajú (lietadlá, lode). Pozri [Výsledky zásahov](hits.md#hit-outcomes) |
| `hitShell` | podpis strely `shot`: štyri bajty zo správy o zásahu (surový hex); jeden podpis môže označovať rôzne strely (120 a 125 mm APFSDS majú jeden), preto sa uchováva surový, nečíta sa ako kalibrom |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | munícia `shot`: jej typ (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) a id (`125mm_3bm46`), kde zabitie pomenuje slot strelca, inak `explosive` (dávka výbuchu) alebo `kinetic`; `weapon/slot` dela z jeho nabíjania; kalibrom v mm zo súborov zbrane z inštalácie. Pozri [Výsledky zásahov](hits.md#hit-outcomes) |
| `rpm` | otáčky motora lietadla (priemer cez jeho motory), posledne poslané, do 2 s |
| `vx`, `vy`, `vz` | rýchlosť lietadla tak, ako ju posiela jeho záznam letu (m/s, osi hry; rýchlosti nad 500 m/s sa čítajú ako 500) |
| `engine`, `afterburner`, `engineCondition` | motory lietadla zo záznamu letu: `off`, `starting`, `running`, `dead` (spojené `/`, keď sa jeho motory líšia); prepaľovanie 0-1; bajt posielaný len potom, čo bol motor zasiahnutý |
| `weaponName` | zabitia a smrti: zbraň alebo munícia v anglickej lokalizácii vašej inštalácie (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | len lietadlo hráča, ktorý replay nahral: plyn 0-1,1 z jeho kokpitu (1,1 bojový núdzový výkon alebo prepaľovanie; inak pätnástiny jeho záznamu letu), ovládanie -1..1 zo svojho záznamu letu (výškovka kladná ťahom, krídelká kladné kotúľaním doprava), zostávajúce náboje na zbraň (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | len lietadlo hráča, ktorý replay nahral, z jeho kokpitu: indikovaná vzdušná rýchlosť a rýchlosť stúpania (m/s), palivo, tlak v sacom potrubí (atm), podvozok (0-1, 1 spustený), teplota oleja a hlavy valcov, kde kokpit má ciferník |
| `speed` | m/s za asi dve sekundy stopy (dopočítané tu; replay neposiela rýchlosť pre iné jednotky) |
| `alive` | 0 pri vzorkách jednotky po jej smrti (jej vrak): pri pozemnej jednotke alebo lodi, kým ju hra neodstráni alebo jej vzorky neskončia, pri lietadle najviac 60 s |
| `otherVehicle`, `otherLife` | obeť `shot`: jej vozidlo a jej `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | bod zásahu `shot` v súradniciach vlastnej obete (m; x dopredu, y nahor, z vľavo; pozri [Správy pre jednotky](how-it-reads.md#messages-to-units)) a smer, akým strela prišla, prevedený do tých súradníc postojom obete vtedy |
| `hitPart`, `hitFlag` | správa o zásahu `shot`: jej slovo časti tak, ako bolo poslané, a jej najvyšší bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | čo bitka stála a zarobila a kto vyhral: pozri [Ekonomika](economy.md) |
| `other`, `weapon` | zabitia: druhá strana a zbraň; zásahy: kto zasiahol (z uid záznamu, inak zo slotu hráča), ich vozidlo; vypustenia: zbraň; zničené moduly: kto zasiahol jednotku naposledy do 5 s pred tým, a `part <n>` |

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
