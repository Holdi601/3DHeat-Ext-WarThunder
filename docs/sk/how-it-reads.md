---
title: "Ako sa replay číta"
nav_order: 10
lang: "sk"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Ako sa replay číta {#how-it-reads-a-replay}

Táto stránka je pre ľudí, ktorí chcú vedieť, čo konvertor číta, ako sa to overilo, a teda nakoľko dôverovať každému
stĺpcu. Na konverziu replayov ju nepotrebujete.

Čítanie sa overilo na klientských replayoch leteckých arkádových, leteckých simulátorových a námorných bitiek, na
serverových replayoch pozemných bitiek a pre rozloženia z roku 2025 na verejných ukážkových replayoch
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Každá kontrola porovnáva hodnotu s niečím, čo replay hovorí iným, nezávislým spôsobom; tu sa uvádza len metóda a zhoda.

## Čo sa číta a aká je kontrola {#what-is-read-and-the-check}

| Časť | Stav a kontrola |
|---|---|
| Hlavička, mapa, misia, čas začiatku, relácia; výsledky | každý súbor |
| Nastavenia misie (blk za hlavičkou) | režim, počasie, limity, `stars` (dátum, čas, miesto) |
| Tok paketov (zlib v roku 2025, zstd v roku 2026) | každý paket ohraničený |
| Polohy a postoje lietadiel (rozloženie 2026) | 4 vzorky za sekundu, žiadny paket nezostal nečítaný; smer hlavy sa zhoduje so smerom letu |
| Letové pakety pred svojím časom | po sieťovom zádrhele letový paket klientského replaye niekedy drží každé iné lietadlo tam, kde bude asi o 0,75 s neskôr. Predstih sa meria pre každý paket a každému lietadlu, ktoré predbieha, sa priradí čas, ktorý predstavuje (`selfCheck.flightPacketsRetimed`) |
| Skoky pri odhade polohy | krok z odhadnutého behu sa meria od posledného prijatého stavu, takže korekcie klienta už nerežú stopy ([Odhad polohy](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporty | stopa sa prereže, keď sa jednotka pohne ďalej, než môže: najprv podľa jej druhu (lietadlo 750 m/s, pozemné a lode 40 m/s, zbrane 1800 m/s), potom podľa jej vlastného tempa. Každý rez je uvedený v `trackBreaks` s pravdepodobnou príčinou (oživenie, hra pohla hráčom, korekcia vzdialenej jednotky). Po rezoch žiadny krok medzi riadkami stopy nie je rýchlejší, než jej druh dovoľuje (`selfCheck.stepSpeed`) |
| Pozície pozemných jednotiek a lodí (0xF073 / 0xF074) | žiadny paket nezostal nečítaný. Smer, sklon a náklon z 16-bitového postoja: smer sa zhoduje so smerom letu do asi 2 stupňov (medián); sklon počíta 180/65536 stupňa na krok; so znamienkom náklonu obráteným smer dela od trupu a veže ukazuje na zasiahnutú jednotku takmer pri každom výstrele tanku. Lode sú na úrovni vody |
| Veže | uhol otočenia veže a sklon dela tankov: pozri [Veže](ground.md#turrets) |
| Zabalené výšky terénu | polohy zabalené v 64 bitoch počítajú výšku od -100 m na väčšine levelov a od výšky vody na niektorých; posun sa meria na každom replaye z jednotiek videných v oboch tvaroch (`selfCheck.packedGroundHeight`) |
| Tok entít (vznik, zánik) | každý vznik sa číta. Rozloženie pochádza z publikovaného zdroja Dagor Engine; typy komponentov War Thunderu sa preskakujú nájdením, kde začína ďalší komponent. Vozidlo a slot hráča každej jednotky sa rovnajú tým, ktoré uvádzajú záznamy zabití a zásahov, pri každom skontrolovanom zázname |
| Kto riadil ktorú jednotku, jednotky AI, lode, pozemné ciele | z toku entít: každá jednotka má svoje vozidlo a tím, jednotka každého hráča jeho hráča |
| Zabitia oproti výsledkom | smrti na hráča sa rovnajú výsledkom; výsledky počítajú viac zabití, lebo klientovi sa neposiela každé zabitie. Replay, ktorý začína po začiatku bitky, drží len zabitia po tom čase |
| Zabitia, kritické zásahy, ťažké poškodenie | každý súbor |
| Zničené moduly (0xF118) | jednotka a číslo časti; názov časti potrebuje model poškodenia vozidla, ktorý v replaye nie je |
| Vypustené zbrane (tok entít) | bod vypustenia je asi 10-20 m (medián) od najbližšej jednotky, ktorá sa berie ako odpaľovač |
| Zbrane v lete (0xF0DB) | rakety, strely a bomby, každá viazaná na svoju entitu |
| Bomby bez záznamov letu | bomba bez nich má pád dopočítaný od vypustenia po dopad (gravitácia a odpor, vzorka každých 0,1 s, `extrapolated` true). Overené nad morom, kde je výška dopadu známa: dopočítané pády končia do asi 15 m od hladiny. V dokumente zápasu má taká zbraň `ballisticImpact`; `counts.bombsBallistic` ich počíta |
| Sloty hráčov, chat | každý súbor |
| Výbuchy, výbuchy protilietadlových zbraní, ocenenia, zistenia, počasie, objekty misie | čítané; pozície overené okom v prehliadači |
| Prístroje hráča, ktorý replay nahral (0xD04A) | pomenované podľa toho, čo robia: [Prístroje v kokpite](aircraft.md#cockpit-instruments); ostatné pod `notNamed` |
| Ďalšie polia záznamov letu | rýchlosť, náboje, ovládanie, motory: [Záznamy letu](aircraft.md#flight-entries) |
| Postoj v riadkoch udalostí | každý riadok udalosti nesie smer hlavy, sklon, náklon a vektor pohľadu jednotky v tom okamihu |
| Štatistiky hráčov a skóre tímov | na konci bitky sa každá štatistika každého hráča rovná výsledku: [Údaje odrazu](aircraft.md#reflection-data) |
| Názvy zbraní a vozidiel | z anglickej lokalizácie vašej inštalácie; niektoré predvolené pásy lodí a radary letísk nemajú v hre názov |
| Hráči a AI | žiadny riadok hráča z výsledkov nie je AI, každý riadok, ktorý nie je AI, je hráčom z výsledkov (`selfCheck.identity`) |
| Vraky | vzorky jednotky po jej smrti ďalej prichádzajú; vrak pozemnej jednotky alebo lode je `alive` 0, kým sa jej entita neodstráni, a zostáva jednou stopou; lietadlá nechávajú `alive` 0 najviac 60 s (`selfCheck.wrecks`) |
| Prepínanie vozidiel | jednotka hráča, ktorá ešte žije, keď sa objaví ďalšia jednotka toho istého hráča, sa tam ukončí (vozidlo, ktoré zostalo stáť). `selfCheck.vehicleSwitch.twoLiveVehicles` musí byť 0 |
| Režim bitky | [Režim bitky](ground.md#battle-mode) |
| Lietadlá v serverovom replaye z roku 2026 | čítané v rozložení z roku 2026; smer hlavy a znamienko náklonu sa zhodujú so zákrutami; zástupné lietadlá a prieskumné drony nenesú údaje |
| Hráči serverového replaye | nájdení menom v slotoch; každá štatistika sa rovná výsledku (`selfCheck.players`) |
| Lietadlá v serverových replayoch z roku 2025 a vo verzii 101286 | nečítajú sa: ich letové pakety majú iné rozloženie |

## Správy pre jednotky {#messages-to-units}

Každý paket typu 4 je správa mpi z daNet Dagor Engine: id cieľového objektu, potom (keď sú jeho nižších 11 bitov všetky
nastavené) rozšírené UID objektu, id správy a obsah. Správa pre jednotku nesie ako svoje rozšírené UID id entity jednotky,
`index << 10 | generation`. Overené: každá takáto správa pomenuje entitu, ktorá v tom okamihu žije.

Pre odborníkov, správy, ktoré sa čítajú:

| Správa | Čo, a kontrola |
|---|---|
| 0xF0E9 UnitHitEffects | zásah jedného projektilu: uid strelca a bod zásahu v súradniciach jednotky (x dopredu, y nahor, z vľavo): centimetre pri lietadlách a lodiach, 20/32768 m na krok pri pozemných jednotkách (prispôsobené veľkosti veží tankov). `hitLocalX/Y/Z` v metroch. Stane sa riadkom `shot` ([Streľba](hits.md#gunfire)). Strelec takmer každého záznamu zásahu a zabitia je medzi týmito strelcami; body zásahu ležia na strane otočenej k strelcovi |
| 0xF133 UnitOnExplosion | to isté uid strelca |
| 0xF04B OnUnitDead | riadky `dead`: obeť každého záznamu zabitia má jeden do 2 s |
| 0xD047 FmwRpm | otáčky motorov (`rpm`); sedia s ciferníkom otáčok v kokpite |
| 0xF0B1, 0xF0A0 | riadky `gun_shot`: jednotlivé výstrely ťažkého protilietadlového delostrelectva a delostrelectva |
| 0xF01B, 0xF01C | riadky `fire_start`, `fire_stop`: dávky 40 mm protilietadlových zbraní (streľba zbrane; požiar na vozidle je `fire_on`, pozri [Požiare vozidiel](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | riadky `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | vlastné zásahy hráča, ktorý replay nahral, a jeho zásahy, so zbraňou a muníciou, pomenované z inštalácie (`projectileHitReplays`) |
| 0xF13E, 0xF031 | vizuálny efekt zásahu a efekt prehraný na jednotke; prichádzajú so zásahom na tú istú jednotku |
| 0xD041 | jedna na každú obrannú zbraň lietadla, dvakrát za sekundu; jeho indexy sa zhodujú so strelcovými zbraňami modelu letu |
| 0xD048, 0xF117 | rozloženie prečítané, význam nie je známy |
| ostatné (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | v sprievodnom súbore správ s ich jednotkou a poľami |

Názvy sú komunitné (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Ďalej čítané {#also-read}

- **Replikácia toku entít** (0x22, 0x23): pri každej entite blok hodnôt komponentov: časovače opráv lodí, počty
  spotrebného materiálu, zmeny vlastníka a tímu, prehriatie motora. Počíta sa v `counts.replicatedComponents`; hodnoty
  v sprievodnom súbore správ.
- **Akcie skriptu misie** (0xF028) a **nápovedy** (0xF0EC): `triggers`, `hints`. **Priebeh misie** (0xF07A, 0xF07C): `missionProgress`.
- **Kamera replaye** (0xD043): pozri [Kamera](ground.md#the-camera).

## Nečítané, a prečo {#not-read-and-why}

- **Názvy a telá správ entít** (0x20, 0x21): číslo triedy je miesto v zozname zostavenom v hre, neposiela sa a nie je
  v jej údajoch. Dve sa čítajú (požiare vozidla a jeho hasiace prístroje); ostatné sa uchovávajú celé s ich entitou
  a číslom triedy.
- **Ostatné replikované objekty** (iné druhy než sloty hráčov a tímy): čítané a uchované, nepomenované; v výsledkoch
  nie je nič, s čím by sa dali overiť.
- **Ovládanie, plyn a náboje iných lietadiel**: obnovujú sa len občas; uchované v sprievodnom súbore letu, nie v tabuľke.
- **Požiare lietadiel**: nenájdené v žiadnej správe; lietadlo v plameňoch nemá riadok `fire_on`.
- **Názvy vypustených zbraní**: entita bomby alebo rakety nenesie názov; záznamy zabití pomenúvajú zbraň zabitia.
- **Vystrely, ktoré minuli**: replay nesie len zásahy.

`counts.messageIdsNotRead` a `selfCheck` v každom dokumente zápasu hovoria, čo nový replay obsahuje a ako dobre sa čítal.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
