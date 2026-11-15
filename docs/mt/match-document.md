---
title: "Id-dokument tal-partita"
nav_order: 7
lang: mt
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Id-dokument tal-partita {#the-match-document}

![Il-bidu ta' dokument tal-partita sintetiku, u ċ-ċwievet tiegħu](../assets/img/match-document.svg)

`<match>.match.json` iżomm dak kollu li r-ripetizzjoni tgħid li mhuwiex ringiela tat-tabella.
It-tab Partita tal-viewer taqrah.

## Il-battalja {#the-battle}

| Ċavetta | X'inhi |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | l-id tal-partita (kif fl-isem tal-fajl); l-id tal-mappa; il-fajl tal-livell li tuża |
| `mission`, `missionKey` | l-isem tal-missjoni u ċ-ċavetta tagħha fil-fajls tat-test tal-logħba |
| `battleClass`, `environment`, `weather` | kif jagħtihom il-header |
| `sessionId`, `server` | l-id tas-sessjoni tal-battalja; is-server |
| `replayVersion`, `flightLayout` | il-verżjoni tal-format tar-ripetizzjoni; il-layout tal-pakkett tat-titjira moqri (`2025` jew `2026`) |
| `files` | il-fajls tar-ripetizzjoni moqrija (wieħed, jew il-partijiet ta' ripetizzjoni tas-server) |
| `started`, `timePlayed`, `replayEnd` | il-ħin tal-bidu (ISO, UTC); sekondi milgħuba, mir-riżultati; sekondi tal-aħħar pakkett tar-ripetizzjoni |
| `author`, `authorUserId` | il-plejer li rreġistra u l-id tiegħu ta' Gaijin (ripetizzjonijiet tal-klijent) |
| `teams` | it-timijiet fil-battalja (`1`, `2`) |
| `result` | `winner`, `status` (`success` jew `fail`, ir-riżultat tal-awtur), `authorTeam`, `teams` ([Ekonomija](economy.md)) |
| `vehicleNames` | minn fejn ġew l-ismijiet tal-vetturi (l-installazzjoni tiegħek) u l-lingwa tagħhom |
| `conventions` | l-unitajiet u s-sinjali tat-tabella: assi, ħin, ħajja, mogħdija, ħaj, roll, u aktar |

## Kull ħaġa oħra {#everything-else}

| Ċavetta | X'inhi |
|---|---|
| `battle`, `difficulty`, `gameMode` | il-modalità tal-battalja: `difficulty` `AB` / `RB` / `SB` (u l-isem tagħha, u l-byte tal-header), `gameMode` `ground` / `air` / `naval`, il-modalità tal-missjoni (`Dom`, `Conq`, `Bttl`, `I2M`, ...) u l-isem Ingliż tagħha mill-installazzjoni tiegħek (`Domination`, `Enduring Confrontation`), it-tipi ta' unitajiet permessi (ara [Battle mode](ground.md#battle-mode)) |
| `settings` | il-blk tal-missjoni wara l-header: modalità, ambjent, temp, limiti tal-punti u tal-ħin, pajjiżi, tipi ta' unitajiet permessi, riħ, u `stars` (latitudni, lonġitudni, data, ħin lokali) |
| `sky` | l-ewwel `CustomWeatherParams`: direzzjoni tax-xemx u tal-qamar, riħ, kuluri tas-sema, offsets tas-sħab |
| `players`, `slots` | il-linja tar-riżultati għal kull plejer (qtil, qtil fuq l-art, imwiet, assists, punti, qbid, squad, clan, pajjiż, line-up, l-uids li saq); is-slots tal-plejers tar-ripetizzjoni (isem, id tal-utent, tim) |
| `units` | kull entità ta' unità li ħolqot ir-ripetizzjoni: eid, uid, template, vettura, ġeneru (kind), tip (type), tim, plejer, isem fil-missjoni, meta nħolqot u tneħħiet, fejn nħolqot, liema komponenti ma setgħux jinqraw |
| `objects` | l-oġġetti bl-isem tal-missjoni: żoni tal-qbid u ajrudromi bil-pożizzjoni u d-daqs tagħhom, il-kontorni tal-ajrudromi bħala punti, żoni tal-ispawn |
| `objectives` | l-objettivi tal-battalja, kull wieħed bil-`type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 jew 2 tar-ripetizzjoni, vojt għaż-żewġ naħat), `name` (żona tal-qbid l-ittra tagħha, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) bi `position`, `radius` / `height` / `size` u `heading`, `source` (`replay` jew `mission`) u dak li hu magħruf aktar (ara [Objettivi](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | bl-ismijiet u l-vetturi taż-żewġ naħat; qtil bl-isem Ingliż tal-arma |
| `weapons` | kull rokit, missila, bomba, torpidni, drop tank u tagħbija mitfugħa: meta, fejn ġiet rilaxxata (pożizzjoni, attitudni, veloċità), minn liema unità (l-eqreb fi ħdan 300 m u 1.5 s), kemm-il kampjun ta' titjira, fejn dehret l-aħħar, meta tneħħiet |
| `explosions`, `flak` | `PlayExplosionVisual` (pożizzjoni, direzzjoni, tip) u `PlayFlakExplosionVisual` (pożizzjoni) |
| `awards` | il-premjijiet tal-plejer li rreġistra (`TextStreak`: first_blood, streaks, challenge counters) |
| `detections`, `unitStates` | pari `UnitDetected` ta' unitajiet; messaġġ (0xF093) bil-pożizzjoni, l-attitudni u l-veloċità ta' unità li tifsira tiegħu mhix magħrufa |
| `authorInstruments` | il-valuri tal-cockpit tal-plejer li rreġistra (`ReplayCockpitParams`) bin-numru tal-istrument, l-iktar wieħed fis-sekonda; `known` jagħti isem lil kull numru li bagħtet din ir-ripetizzjoni (isem, unità, kif ġie kkontrollat), `notNamed` il-bqija |
| `scoreboard` | l-istatistika ta' kull plejer kull darba li nbidlet (qtil, imwiet, assists, punti, qtil ta' AI, qtil navali, żoni, ħsara, missili evaded, squad), u l-punti ta' kull tim u t-tickets probabbli maż-żmien (ara [Reflection data](aircraft.md#reflection-data)) |
| `economy` | is-Silver Lions u l-punti tar-riċerka tal-battalja (ara [Ekonomija](economy.md)): totali, għal kull plejer, għal kull vettura, il-multipliers, ir-rebbieħ, il-kontrolli |
| `entityMessages` | il-messaġġi tal-entitajiet (0x20) skont in-numru tal-klassi: għadd, templates fil-mira, daqsijiet |
| `chat` | kull linja taċ-chat |
| `triggers`, `hints`, `missionProgress` | l-azzjonijiet tal-iscript tal-missjoni (RunTriggerAction), l-hints tagħha, il-messaġġi tal-progress tagħha |
| `camera` | il-kampi tal-kamera tar-ripetizzjoni tal-plejer li rreġistra kull 0.25 s kif intbagħtu (it-tabella għandha bħala mogħdija) |
| `projectileHitReplays` | id-daqqiet tal-plejer li rreġistra stess u meta ġie milqut, bl-arma u l-munizzjon u l-ismijiet Ingliżi tagħhom |
| `results` | il-blk sħiħ tar-riżultati kif kitbitu l-logħba |
| `counts` | ringieli, avvenimenti, ħajjiet, tipi, kampjuni, entitajiet skont it-template, armi, pakketti moqrija u mhux moqrija, kull id ta' messaġġ li deher u dawk mhux moqrija, kampjuni mwarrba |
| `trackBreaks` | kull qtugħ ta' mogħdija għal pass aktar mgħaġġel minn dak li l-unità tista' tagħmel: fejn, kemm 'il bogħod, kemm malajr, u x'inhu x'aktarx |
| `selfCheck` | il-kontrolli elenkati f'[Kif taqra ripetizzjoni](how-it-reads.md), ikkalkulati f'kull konverżjoni; `stepSpeed` jagħti għal kull tip il-veloċità bejn ringieli konsekuttivi ta' mogħdija kif jgħaqqadhom il-viewer (medjan, il-99 perċentili, l-ogħla, u passi aktar mgħaġġla milli possibbli, li jridu jkunu 0) |

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
