---
title: "Si e lexon një riluajtje"
nav_order: 10
lang: sq
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Si e lexon një riluajtje {#how-it-reads-a-replay}

Kjo faqe është për njerëzit që duan të dinë çfarë lexon konvertuesi, si u
kontrollua, dhe pra sa mund t'i besohet çdo kolone. Nuk të duhet për të
konvertuar riluajtje.

Leximi u kontrollua në riluajtje klienti të betejave ajrore arcade, ajrore simulator dhe
detare, në riluajtje serveri të betejave tokësore, dhe, për strukturat e 2025,
në riluajtjet publike shembull të
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Çdo kontroll e krahason një vlerë me diçka që riluajtja e thotë në një mënyrë të dytë,
të pavarur; këtu jepen vetëm metoda dhe përputhja.

## Çfarë lexohet, dhe kontrolli {#what-is-read-and-the-check}

| Pjesa | Gjendja, dhe kontrolli |
|---|---|
| Header, harta, misioni, koha e fillimit, sesioni; rezultatet | çdo skedar |
| Cilësimet e misionit (blk pas header-it) | mënyra, moti, kufijtë, `stars` (data, ora, vendi) |
| Rrjedha e paketave (zlib në 2025, zstd në 2026) | çdo paketë e kornizuar |
| Pozicionet dhe qëndrimi i aeroplanëve (struktura 2026) | 4 mostra në sekondë, asnjë paketë e palexuar; heading përputhet me drejtimin e udhëtimit |
| Paketat e fluturimit përpara kohës së tyre | pas një ngecjeje rrjeti, paketa e fluturimit e një riluajtjeje klienti ndonjëherë mban çdo aeroplan tjetër aty ku do të jetë rreth 0.75 s më vonë. Epërsia matet për paketë, dhe çdo aeroplani që prin i jepet koha që përfaqëson (`selfCheck.flightPacketsRetimed`) |
| Kapjet e dead-reckoning | një hap jashtë një vargu me dead reckoning matet nga gjendja e fundit e marrë, kështu që korrigjimet e klientit nuk i presin më gjurmët ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportimet | një gjurmë pritet aty ku njësia e saj lëviz më larg se sa mundet: së pari ndaj llojit të saj (aeroplan 750 m/s, tokë dhe anije 40 m/s, arma 1800 m/s), pastaj ndaj ritmit të vet. Çdo prerje listohet te `trackBreaks` me shkakun e mundshëm (ripërtëritje, loja që e lëviz lojtarin, korrigjim i një njësie të largët). Pas prerjeve, asnjë hap midis rreshtave të një gjurme nuk është më i shpejtë se sa lejon lloji i saj (`selfCheck.stepSpeed`) |
| Pozicionet e tokës dhe anijeve (0xF073 / 0xF074) | asnjë paketë e palexuar. Heading, pitch dhe roll nga qëndrimi 16-bitësh: heading përputhet me drejtimin e udhëtimit brenda rreth 2 gradësh (mediana); pitch numëron 180/65536 gradë një hap; me shenjën e roll të kthyer, drejtimi i topit nga trupi dhe kupola tregon njësinë e goditur për pothuajse çdo të shtënë tanku. Anijet ulen në nivelin e ujit |
| Kupolat | kthimi i kupolës dhe pitch i topit të tankeve: shih [Kupolat](ground.md#turrets) |
| Lartësitë e paketuara të tokës | pozicionet e paketuara në 64 bit e numërojnë lartësinë nga -100 m në shumicën e niveleve dhe nga niveli i ujit në disa; zhvendosja matet në çdo riluajtje nga njësi të parë në të dyja format (`selfCheck.packedGroundHeight`) |
| Rrjedha e entiteteve (krijimi, shkatërrimi) | çdo krijim i lexuar. Struktura vjen nga burimi i publikuar i Dagor Engine; llojet e komponentëve të vetë War Thunder anashkalohen duke gjetur ku fillon komponenti tjetër. Mjeti dhe vendi i lojtarit i çdo njësie janë të barabartë me ata që emërtojnë regjistrat e vrasjeve dhe goditjeve, për çdo regjistër të kontrolluar |
| Kush drejtoi cilën njësi, njësitë AI, anijet, objektivat tokësorë | nga rrjedha e entiteteve: çdo njësi ka mjetin dhe skuadrën e saj, çdo njësi lojtari lojtarin e saj |
| Vrasjet ndaj rezultateve | vdekjet për lojtar janë të barabarta me ato të rezultateve; rezultatet numërojnë më shumë vrasje, pasi klientit nuk i dërgohet çdo vrasje. Një riluajtje që fillon pasi beteja nisi mban vetëm vrasjet pas kësaj |
| Vrasjet, goditjet kritike, dëmi i rëndë | çdo skedar |
| Modulet e shkatërruara (0xF118) | njësia dhe numri i pjesës; emri i pjesës kërkon modelin e dëmit të mjetit, që nuk është në riluajtje |
| Armët e lëshuara (rrjedha e entiteteve) | pika e lëshimit është rreth 10-20 m (mediana) nga njësia më e afërt, që merret si lëshuesi |
| Armët në fluturim (0xF0DB) | raketa, rakata dhe bomba, secila e lidhur me entitetin e saj |
| Bombat pa regjistra fluturimi | një bombë pa ta merr rënien e llogaritur nga lëshimi deri te goditja (graviteti dhe rezistenca, një mostër çdo 0.1 s, `extrapolated` true). Kontrolluar mbi det, ku lartësia e goditjes dihet: rëniet e llogaritura mbarojnë brenda rreth 15 m nga uji. Në dokumentin e ndeshjes një armë e tillë ka `ballisticImpact`; `counts.bombsBallistic` i numëron |
| Vendet e lojtarëve, biseda | çdo skedar |
| Shpërthimet, flak, çmimet, zbulimet, moti, objektet e misionit | të lexuara; pozicionet të kontrolluara me sy në shikues |
| Instrumentet e lojtarit që regjistron (0xD04A) | të emërtuara sipas asaj që bëjnë: [Instrumentet e kabinës](aircraft.md#cockpit-instruments); pjesa tjetër nën `notNamed` |
| Fushat e tjera të hyrjeve të fluturimit | shpejtësia, predhat, kontrollet, motorët: [Hyrjet e fluturimit](aircraft.md#flight-entries) |
| Qëndrimi i rreshtave të ngjarjeve | çdo rresht ngjarjeje mbart heading, pitch, roll dhe vektorin e shikimit të njësisë së vet në atë çast |
| Statistikat e lojtarëve dhe pikët e skuadrave | në fund të betejës çdo statistikë është e barabartë me atë të rezultateve për çdo lojtar: [Të dhënat e reflektimit](aircraft.md#reflection-data) |
| Emrat e armëve dhe mjeteve | nga lokalizimi anglisht i instalimit tënd; rripat e parazgjedhur të disa anijeve dhe radarët e fushave ajrore nuk kanë emër në lojë |
| Lojtarët dhe AI | asnjë rresht i një lojtari të rezultateve nuk është AI, çdo rresht jo-AI është i një lojtari të rezultateve (`selfCheck.identity`) |
| Mbetjet | mostrat e një njësie pas vdekjes së saj vazhdojnë të vijnë; mbetja e një njësie tokësore ose anijeje është `alive` 0 derisa entiteti i saj hiqet, dhe mbetet një gjurmë; aeroplanët mbajnë `alive` 0 për më së shumti 60 s (`selfCheck.wrecks`) |
| Ndërrimet e mjeteve | njësia e një lojtari që është ende e gjallë kur shfaqet njësia tjetër e të njëjtit lojtar përfundon aty (një mjet i lënë në këmbë). `selfCheck.vehicleSwitch.twoLiveVehicles` duhet të jetë 0 |
| Mënyra e betejës | [Mënyra e betejës](ground.md#battle-mode) |
| Aeroplanët në një riluajtje serveri 2026 | lexuar në strukturën 2026; heading dhe shenja e roll përputhen me kthesat; aeroplanët vendmbajtës dhe dronët zbulues nuk mbartin të dhëna |
| Lojtarët e një riluajtjeje serveri | gjetur sipas emrit në vendet; çdo statistikë është e barabartë me atë të rezultateve (`selfCheck.players`) |
| Aeroplanët në riluajtje serveri 2025 dhe versioni 101286 | nuk lexohen: paketat e tyre të fluturimit kanë strukturë tjetër |

## Mesazhet për njësitë {#messages-to-units}

Çdo paketë e llojit 4 është një mesazh mpi i daNet të Dagor Engine: ID e
objektit marrës, pastaj (kur 11 bitët e saj të ulët janë të gjithë të vendosur) UID-ja ext e objektit,
ID e mesazhit dhe ngarkesa. Një mesazh për një njësi mbart si UID ext
ID-në e entitetit të njësisë, `index << 10 | generation`. Kontrolluar: çdo
mesazh i tillë emërton një entitet të gjallë në atë çast.

Për specialistët, mesazhet e lexuara:

| Mesazhi | Çfarë, dhe kontrolli |
|---|---|
| 0xF0E9 UnitHitEffects | goditja e një predhe: uid-i i gjuajtësit dhe pika e goditjes në kuadrin e njësisë (x përpara, y lart, z majtas): centimetra te aeroplanët dhe anijet, 20/32768 m një hap te njësitë tokësore (përshtatur me madhësinë e kupolave të tankeve). `hitLocalX/Y/Z` në metra. Bëhet një rresht `shot` ([Të shtënat](hits.md#gunfire)). Sulmuesi i pothuajse çdo regjistri goditjeje dhe vrasjeje është midis këtyre gjuajtësve; pikat e goditjes shtrihen në anën që i përballet gjuajtësit |
| 0xF133 UnitOnExplosion | i njëjti uid gjuajtësi |
| 0xF04B OnUnitDead | rreshta `dead`: viktima e çdo regjistri vrasjeje ka një brenda 2 s |
| 0xD047 FmwRpm | rpm e motorëve (`rpm`); përputhet me matësin e rpm të kabinës |
| 0xF0B1, 0xF0A0 | rreshta `gun_shot`: të shëna të vetme të armëve të rënda kundërajrore dhe artilerisë |
| 0xF01B, 0xF01C | rreshta `fire_start`, `fire_stop`: breshëri të armëve kundërajrore 40 mm (një armë që gjuan; një zjarr mbi një mjet është `fire_on`, shih [Zjarret e mjeteve](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | rreshta `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | goditjet e vetë lojtarit që regjistron dhe goditjet që mori, me armën dhe municionin, emërtuar nga instalimi (`projectileHitReplays`) |
| 0xF13E, 0xF031 | efekti pamor i një goditjeje dhe një efekt i luajtur mbi njësi; vijnë me një goditje mbi të njëjtën njësi |
| 0xD041 | një për çdo armë mbrojtëse të një aeroplani, dy herë në sekondë; indekset e tij përputhen me armët e gjuajtësit të modelit të fluturimit |
| 0xD048, 0xF117 | struktura e lexuar, kuptimi nuk dihet |
| pjesa tjetër (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | në skedarin anësor të mesazheve me njësinë dhe fushat e tyre |

Emrat janë të komunitetit (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Gjithashtu të lexuara {#also-read}

- **Replikimi i rrjedhës së entiteteve** (0x22, 0x23): për entitet një bllok
  vlerash komponentësh: kohëmatësit e riparimit të anijeve, numri i konsumueshmeve, ndryshimet e pronarit dhe skuadrës,
  mbinxehja e motorit. Numëruar te `counts.replicatedComponents`; vlerat
  në skedarin anësor të mesazheve.
- **Veprimet e skriptit të misionit** (0xF028) dhe **sugjerimet** (0xF0EC): `triggers`,
  `hints`. **Progresi i misionit** (0xF07A, 0xF07C): `missionProgress`.
- **Kamera e riluajtjes** (0xD043): shih [Kamera](ground.md#the-camera).

## Të palexuara, dhe pse {#not-read-and-why}

- **Emrat dhe trupat e mesazheve të entiteteve** (0x20, 0x21): numri i klasës është një
  vend në një listë të përpiluar në lojë, jo i dërguar dhe jo në të dhënat e saj. Dy
  lexohen (zjarret e një mjeti dhe fikëset e tij); pjesa tjetër ruhet
  e plotë me entitetin dhe numrin e klasës së tyre.
- **Objektet e tjera të replikuara** (lloje të ndryshme nga vendet e lojtarëve dhe skuadrat):
  lexuar dhe ruajtur, të paemërtuara; nuk ka asgjë në rezultate për t'i kontrolluar.
- **Kontrollet, gazi dhe predhat e aeroplanëve të tjerë**: rifreskohen vetëm herë pas here;
  ruhen në skedarin anësor të fluturimit, jo në tabelë.
- **Zjarret e aeroplanëve**: nuk u gjetën në asnjë mesazh; një aeroplan që digjet nuk ka
  rresht `fire_on`.
- **Emrat e armëve të lëshuara**: entiteti i një bombe ose rakate nuk mban emër;
  regjistrat e vrasjeve emërtojnë armën e një vrasjeje.
- **Të shtënat që humbën**: një riluajtje mban vetëm goditjet.

`counts.messageIdsNotRead` dhe `selfCheck` i çdo dokumenti ndeshjeje thonë çfarë mban një
riluajtje e re dhe sa mirë u lexua.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
