---
title: "Dokumenti i ndeshjes"
nav_order: 7
lang: sq
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokumenti i ndeshjes {#the-match-document}

![Fillimi i një dokumenti ndeshjeje sintetik, dhe çelësat e tij](../assets/img/match-document.svg)

`<match>.match.json` mban gjithçka që thotë riluajtja dhe që nuk është rresht i
tabelës. Skeda Ndeshja e shikuesit e lexon.

## Beteja {#the-battle}

| Çelësi | Çfarë |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | ID e ndeshjes (si në emrin e skedarit); ID e hartës; skedari i nivelit që përdor |
| `mission`, `missionKey` | emri i misionit dhe çelësi i tij në skedarët e tekstit të lojës |
| `battleClass`, `environment`, `weather` | siç i jep header-i |
| `sessionId`, `server` | ID e sesionit të betejës; serveri |
| `replayVersion`, `flightLayout` | versioni i formatit të riluajtjes; struktura e paketës së fluturimit që u lexua (`2025` ose `2026`) |
| `files` | skedarët e riluajtjes që u lexuan (një, ose pjesët e një riluajtjeje serveri) |
| `started`, `timePlayed`, `replayEnd` | koha e fillimit (ISO, UTC); sekondat e luajtura, nga rezultatet; sekondat e paketës së fundit të riluajtjes |
| `author`, `authorUserId` | lojtari që regjistron dhe ID-ja e tij Gaijin (riluajtjet e klientit) |
| `teams` | skuadrat në betejë (`1`, `2`) |
| `result` | `winner`, `status` (`success` ose `fail`, rezultati i autorit), `authorTeam`, `teams` ([Ekonomia](economy.md)) |
| `vehicleNames` | nga erdhën emrat e mjeteve (instalimi yt) dhe gjuha e tyre |
| `conventions` | njësitë dhe shenjat e tabelës: boshtet, koha, life, track, alive, roll, e më shumë |

## Gjithçka tjetër {#everything-else}


| Çelësi | Çfarë |
|---|---|
| `battle`, `difficulty`, `gameMode` | mënyra e betejës: `difficulty` `AB` / `RB` / `SB` (dhe emri i saj, dhe bajti i header-it), `gameMode` `ground` / `air` / `naval`, mënyra e misionit (`Dom`, `Conq`, `Bttl`, `I2M`, ...) dhe emri i saj në anglisht nga instalimi yt (`Domination`, `Enduring Confrontation`), llojet e lejuara të njësive (shih [Mënyra e betejës](ground.md#battle-mode)) |
| `settings` | blk-ja e misionit pas header-it: mënyra, mjedisi, moti, kufijtë e pikëve dhe të kohës, vendet, llojet e lejuara të njësive, era, dhe `stars` (gjerësia, gjatësia, data, ora vendore) |
| `sky` | `CustomWeatherParams` e parë: drejtimi i diellit dhe i hënës, era, ngjyrat e qiellit, zhvendosjet e reve |
| `players`, `slots` | rreshti i rezultateve për çdo lojtar (vrasje, vrasje tokësore, vdekje, ndihma, pikë, kapje, skuadër, klan, vend, përbërje, uid-et që ka drejtuar); vendet e lojtarëve të riluajtjes (emri, ID e përdoruesit, skuadra) |
| `units` | çdo entitet njësie që krijoi riluajtja: eid, uid, shabllon, mjet, kind, type, skuadër, lojtar, emri në mision, kur u krijua dhe u hoq, ku u krijua, cilët komponentë nuk u lexuan dot |
| `objects` | objektet me emër të misionit: zonat e kapjes dhe fushat ajrore me pozicionin dhe madhësinë, konturet e fushave ajrore si pika, zonat e ripërtëritjes |
| `objectives` | objektivat e betejës, secili `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 ose 2 e riluajtjes, bosh për të dyja), `name` (një zonë kapjeje shkronja e saj, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) me `position`, `radius` / `height` / `size` dhe `heading`, `source` (`replay` ose `mission`) dhe çfarë tjetër dihet (shih [Objektivat](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | me emrat dhe mjetet e të dyja palëve; vrasjet me emrin e armës në anglisht |
| `weapons` | çdo raketë, projektil, bombë, silurë, depozitë e hedhshme dhe ngarkesë e hedhur: kur, ku u lëshua (pozicioni, qëndrimi, shpejtësia), nga cila njësi (më e afërta brenda 300 m dhe 1.5 s), sa mostra fluturimi, ku u pa së fundmi, kur u hoq |
| `explosions`, `flak` | `PlayExplosionVisual` (pozicioni, drejtimi, lloji) dhe `PlayFlakExplosionVisual` (pozicioni) |
| `awards` | çmimet e lojtarit që regjistron (`TextStreak`: first_blood, seri, numëruesit e sfidave) |
| `detections`, `unitStates` | çiftet `UnitDetected` të njësive; një mesazh (0xF093) me pozicionin, qëndrimin dhe shpejtësinë e një njësie, kuptimi i të cilit nuk dihet |
| `authorInstruments` | vlerat e kabinës së lojtarit që regjistron (`ReplayCockpitParams`) sipas numrit të instrumentit, më së shumti një në sekondë; `known` emërton çdo numër që dërgoi kjo riluajtje (emri, njësia, si u kontrollua), `notNamed` pjesën tjetër |
| `scoreboard` | statistikat e çdo lojtari sa herë ndryshuan (vrasje, vdekje, ndihma, pikë, vrasje AI, vrasje detare, zona, dëm, shmangie raketash, skuadër), dhe pikët e secilës skuadër dhe biletat e mundshme me kalimin e kohës (shih [Të dhënat e reflektimit](aircraft.md#reflection-data)) |
| `economy` | Silver Lions dhe pikët e kërkimit të betejës (shih [Ekonomia](economy.md)): totalet, për lojtar, për mjet, shumëzuesit, fituesi, kontrollet |
| `entityMessages` | mesazhet e entiteteve (0x20) sipas numrit të klasës: numri, shabllonet e synuara, madhësitë |
| `chat` | çdo rresht bisede |
| `triggers`, `hints`, `missionProgress` | veprimet e skriptit të misionit (RunTriggerAction), sugjerimet e tij, mesazhet e progresit |
| `camera` | fushat e kamerës së riluajtjes së lojtarit që regjistron çdo 0.25 s siç u dërguan (tabela e ka si gjurmë) |
| `projectileHitReplays` | goditjet e vetë lojtarit që regjistron dhe goditjet që mori, me armën dhe municionin dhe emrat e tyre në anglisht |
| `results` | i gjithë blk-ja e rezultateve siç e shkroi loja |
| `counts` | rreshta, ngjarje, jetë, lloje, mostra, entitete sipas shabllonit, armë, paketa të lexuara dhe të palexuara, çdo ID mesazhi e parë dhe ato të palexuara, mostra të hedhura |
| `trackBreaks` | çdo prerje e një gjurme për një hap më të shpejtë se sa mund të shkojë njësia: ku, sa larg, sa shpejt, dhe çfarë është më së shumti |
| `selfCheck` | kontrollet e listuara te [Si e lexon një riluajtje](how-it-reads.md), të llogaritura në çdo konvertim; `stepSpeed` jep për çdo lloj shpejtësinë midis rreshtave të njëpasnjëshëm të një gjurme siç i bashkon shikuesi (mediana, përqindësi i 99-të, më e larta, dhe hapat më të shpejtë se e mundura, që duhet të jenë 0) |

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
