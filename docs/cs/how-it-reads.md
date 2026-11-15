---
title: "Jak se replay čte"
nav_order: 10
lang: cs
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Jak se replay čte {#how-it-reads-a-replay}

Tato stránka je pro lidi, kteří chtějí vědět, co převodník čte, jak bylo čtení ověřeno, a tedy jak moc věřit každému
sloupci. K převodu replayů ji nepotřebujete.

Čtení bylo ověřeno na replayích klienta z leteckých arkádových a simulátorových bitev a námořních bitev, na serverových
replayích pozemních bitev a u rozložení z roku 2025 na veřejných ukázkových replayích
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Každá kontrola porovnává hodnotu s něčím, co replay říká jiným, nezávislým způsobem; zde se uvádí jen metoda a míra shody.

## Co se čte a jak to bylo ověřeno {#what-is-read-and-the-check}

| Část | Stav a kontrola |
|---|---|
| Hlavička, mapa, mise, čas začátku, relace; výsledky | každý soubor |
| Nastavení mise (blk za hlavičkou) | režim, počasí, limity, `stars` (datum, čas, místo) |
| Proud paketů (zlib v roce 2025, zstd v roce 2026) | každý paket rozpoznán |
| Polohy a postoje letadel (rozložení 2026) | 4 vzorky za vteřinu, žádný paket nezůstane nepřečten; kurz souhlasí se směrem letu |
| Letové pakety předběhlé před svůj čas | po výpadku sítě někdy letový paket replaye klienta drží každé jiné letadlo tam, kde bude asi o 0,75 s později. Předstih se měří u každého paketu a každé letadlo, které předbíhá, dostane čas, který představuje (`selfCheck.flightPacketsRetimed`) |
| Přeskoky odhadu polohy (dead reckoning) | krok z běhu odhadu polohy se měří od posledního přijatého stavu, takže opravy klienta už netnou tratě ([Odhad polohy](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporty | trať se přeruší tam, kde se jednotka pohne dál, než může: nejdřív podle svého druhu (letadlo 750 m/s, pozemní a lodě 40 m/s, zbraně 1800 m/s), pak podle vlastního tempa. Každý přerušený úsek je v `trackBreaks` s pravděpodobnou příčinou (respawn, hra přesunula hráče, oprava vzdálené jednotky). Po přerušení žádný krok mezi řádky jedné tratě není rychlejší, než druh dovoluje (`selfCheck.stepSpeed`) |
| Polohy pozemních jednotek a lodí (0xF073 / 0xF074) | žádný paket nezůstane nepřečten. Kurz, sklon a náklon z 16bitového postoje: kurz souhlasí se směrem letu do asi 2 stupňů (medián); sklon se počítá po 180/65536 stupně; s otočeným znaménkem náklonu směřuje směr děla od trupu a věže téměř u každého výstřelu tanku na zasaženou jednotku. Lodě sedí na hladině vody |
| Věže | natočení věží a sklon děla tanků: viz [Věže](ground.md#turrets) |
| Zabalené výšky terénu | polohy zabalené do 64 bitů počítají výšku od -100 m na většině úrovní a od hladiny vody na některých; posun se měří u každého replaye z jednotek viděných v obou tvarech (`selfCheck.packedGroundHeight`) |
| Proud entit (vznik, zánik) | každý vznik přečten. Rozložení pochází z publikovaného zdrojového kódu Dagor Engine; typy komponent War Thunderu se přeskakují tím, že se najde, kde začíná další komponenta. Vozidlo a slot hráče každé jednotky se rovnají těm, které jmenují záznamy zabití a zásahů, u každého kontrolovaného záznamu |
| Kdo řídil kterou jednotku, jednotky AI, lodě, pozemní cíle | z proudu entit: každá jednotka má své vozidlo a tým, jednotka každého hráče jeho hráče |
| Zabití proti výsledkům | smrti na hráče se rovnají výsledkům; výsledky počítají více zabití, protože klientovi nejsou posílána všechna zabití. Replay, který začíná po začátku bitvy, obsahuje jen zabití po tomto začátku |
| Zabití, kritické zásahy, těžké poškození | každý soubor |
| Zničené moduly (0xF118) | jednotka a číslo části; název části potřebuje model poškození vozidla, který v replayi není |
| Vypuštěné zbraně (proud entit) | bod vypuštění je asi 10-20 m (medián) od nejbližší jednotky, která se bere jako vypouštěč |
| Zbraně za letu (0xF0DB) | řízené střely, rakety a bomby, každá navázaná na svou entitu |
| Bomby bez letových záznamů | bomba bez nich má svůj pád dopočítaný od vypuštění k dopadu (gravitace a odpor, vzorek každých 0,1 s, `extrapolated` true). Ověřeno nad mořem, kde je výška dopadu známa: dopočítané pády končí do asi 15 m od hladiny. V dokumentu zápasu má taková zbraň `ballisticImpact`; `counts.bombsBallistic` je počítá |
| Sloty hráčů, chat | každý soubor |
| Exploze, výbuchy protiletadlovek, ocenění, detekce, počasí, objekty misí | čteno; polohy ověřeny okem v prohlížeči |
| Přístroje hráče, který nahrával (0xD04A) | pojmenované podle toho, co dělají: [Palubní přístroje](aircraft.md#cockpit-instruments); zbytek pod `notNamed` |
| Ostatní pole záznamů letu | rychlost, náboje, ovládání, motory: [Záznamy letu](aircraft.md#flight-entries) |
| Postoj v řádcích událostí | každý řádek události nese kurz, sklon, náklon a vektor pohledu své jednotky v daném okamžiku |
| Statistiky hráčů a skóre týmů | na konci bitvy se každá statistika každého hráče rovná výsledkům: [Data odrazu](aircraft.md#reflection-data) |
| Názvy zbraní a vozidel | z anglické lokalizace vaší instalace; několik výchozích pásů lodí a radarů letišť nemá ve hře název |
| Hráči a AI | žádný řádek hráče z výsledků není AI, každý řádek, který není AI, je hráč z výsledků (`selfCheck.identity`) |
| Vraky | vzorky jednotky po její smrti dál přicházejí; vrak pozemní jednotky nebo lodi je `alive` 0, dokud se jeho entita neodstraní, a zůstává jednou tratí; letadla drží `alive` 0 nejdéle 60 s (`selfCheck.wrecks`) |
| Přepnutí vozidla | jednotka hráče, která je ještě živá, když se objeví další jednotka téhož hráče, tam končí (vozidlo ponechané stát). `selfCheck.vehicleSwitch.twoLiveVehicles` musí být 0 |
| Režim bitvy | [Režim bitvy](ground.md#battle-mode) |
| Letadla na serverovém replayi z roku 2026 | čtena v rozložení 2026; kurz a znaménko náklonu souhlasí se zatáčkami; zástupná letadla a průzkumné drony nenesou data |
| Hráči serverového replaye | nalezeni podle jména ve slotech; každá statistika se rovná výsledkům (`selfCheck.players`) |
| Letadla na serverových replayích z roku 2025 a verze 101286 | nečtena: jejich letové pakety mají jiné rozložení |

## Zprávy jednotkám {#messages-to-units}

Každý paket typu 4 je zpráva mpi z daNet Dagor Engine: id objektu příjemce, potom (když jsou jeho nižších 11 bitů
všechny nastavené) ext UID objektu, id zprávy a obsah. Zpráva jednotce nese jako svůj ext UID id entity jednotky,
`index << 10 | generation`. Ověřeno: každá taková zpráva jmenuje entitu, která je v tu chvíli živá.

Pro specialisty, zprávy se čtou takto:

| Zpráva | Co, a kontrola |
|---|---|
| 0xF0E9 UnitHitEffects | zásah jednoho projektilu: uid střelce a bod zásahu v rámci jednotky (x dopředu, y nahoru, z vlevo): centimetry u letadel a lodí, 20/32768 m na krok u pozemních jednotek (přizpůsobeno velikosti věží tanků). `hitLocalX/Y/Z` v metrech. Stane se řádkem `shot` ([Palba](hits.md#gunfire)). Střelec téměř každého záznamu zásahu a zabití je mezi těmito střelci; body zásahů leží na straně obrácené ke střelci |
| 0xF133 UnitOnExplosion | totéž uid střelce |
| 0xF04B OnUnitDead | řádky `dead`: každá oběť záznamu zabití jeden má do 2 s |
| 0xD047 FmwRpm | otáčky motorů (`rpm`); souhlasí s ručičkou otáček v kokpitu |
| 0xF0B1, 0xF0A0 | řádky `gun_shot`: jednotlivé výstřely těžkých protiletadlových a dělostřeleckých zbraní |
| 0xF01B, 0xF01C | řádky `fire_start`, `fire_stop`: dávky 40mm protiletadlových děl (dělo střílí; požár na vozidle je `fire_on`, viz [Požáry vozidel](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | řádky `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | vlastní zásahy hráče, který nahrával, a zásahy na něj, se zbraní a municí, pojmenované z instalace (`projectileHitReplays`) |
| 0xF13E, 0xF031 | vizuální efekt zásahu a efekt přehraný na jednotce; přicházejí se zásahem na tutéž jednotku |
| 0xD041 | jedna pro každé obranné dělo letadla, dvakrát za vteřinu; jeho indexy odpovídají střelcovým zbraním letového modelu |
| 0xD048, 0xF117 | rozložení čteno, význam není znám |
| zbytek (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | v doplňku zpráv s jejich jednotkou a poli |

Názvy jsou z komunity (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Také čteno {#also-read}

- **Replikace proudu entit** (0x22, 0x23): u každé entity blok hodnot komponent: časovače oprav lodí, počty
  spotřebního materiálu, změny vlastníka a týmu, přehřátí motoru. Počítá se v `counts.replicatedComponents`;
  hodnoty v doplňku zpráv.
- **Akce skriptu mise** (0xF028) a **nápovědy** (0xF0EC): `triggers`, `hints`. **Postup mise** (0xF07A, 0xF07C):
  `missionProgress`.
- **Kamera replaye** (0xD043): viz [Kamera](ground.md#the-camera).

## Nečteno a proč {#not-read-and-why}

- **Názvy a těla zpráv entit** (0x20, 0x21): číslo třídy je místo v seznamu zkompilovaném do hry, neposílá se a není
  v jejích datech. Dvě se čtou (požáry vozidla a jeho hasicí přístroje); zbytek se uchovává celý s entitou a číslem
  třídy.
- **Ostatní replikované objekty** (jiné druhy než sloty hráčů a týmy): čteny a uchovány, nepojmenovány; ve výsledcích
  nic, oproti čemu by se ověřily.
- **Ovládání, plyn a náboje ostatních letadel**: obnovují se jen občas; uchovávají se v letovém doplňku, ne v tabulce.
- **Požáry letadel**: v žádné zprávě nenalezeny; letadlo v plamenech nemá řádek `fire_on`.
- **Názvy vypuštěných zbraní**: entita bomby nebo rakety nemá název; záznamy zabití pojmenovávají zbraň zabití.
- **Střely, které minuly**: replay obsahuje jen zásahy.

`counts.messageIdsNotRead` a `selfCheck` v každém dokumentu zápasu říkají, co nový replay obsahuje a jak dobře byl přečten.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
