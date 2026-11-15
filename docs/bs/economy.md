---
title: "Ekonomija"
nav_order: 14
lang: bs
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomija {#economy}

Šta je bitka koštala i donijela, kao kolone na njenim redovima događaja, pročitano iz **vaše instalacije u vrijeme pretvaranja**
(`char.vromfs.bin`: `config/wpcost.blk` po vozilu, `config/warpoints.blk` i `config/rank.blk`; blk-ovi oružja
iz `aces.vromfs.bin` kažu koja je modifikacija svaka granata). Nijedan broj igre nije u ovom repozitoriju:
vrijednosti idu samo u vaš vlastiti izlaz. Bez `char.vromfs.bin` iz instalacije ne piše se nikakva ekonomija
(`economy.available` netačno). Cijene su one za težinu bitke (`repairCostHistorical` za RB,
`...Arcade` AB, `...Simulation` SB).

| Kolona | Redovi | Šta |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (metak uzet poslije hica, kopnena vozila), `launch` (avioni, helikopteri) | SL koliko je koštao metak, raketa, projektil ili bomba |
| `cost_lost_sl` | `death` igračevog vozila | cijena popravke vozila (osnovno; potpuno nadograđeno u bloku) |
| `earn_sl`, `earn_rp` | `reward` (novi događaj, na mjestu i u vrijeme onoga ko zarađuje) | zarađeni SL i RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | svaki red s `cost_*` ili `earn_sl` | `SL` (`earn_rp` su bodovi istraživanja) |
| `econ_basis` | isto | `install` (cijena pročitana iz instalacije) ili `inferred` (izračunata, dolje) |

**Ko je pobijedio.** `won` (0/1) na svakom redu jednog tima, gdje replay to kaže: rezultati
klijentskog replaya nose vlastiti ishod autora (`status`: `success` ili `fail`), pa je
tim autora pobijedio ili izgubio, a drugi tim obrnuto; `result` u dokumentu meča
kaže koji (`winner`, `status`, `authorTeam`). Serverski replayevi i replayevi napušteni prije
kraja ne nose ishod (`status` serverskog replaya je uvijek `success` i ne imenuje autora),
a ni jedni ni drugi ne drže instalirane modifikacije: rezultati navode vozila svakog igrača samo
po imenu i tipu. Tamo `won` ostaje prazno.

Model troškova u pregledniku čita kolone `cost_*` (i `earn_*`) sa `currency`; zbir `cost_fired_sl +
cost_lost_sl` daje gdje su Silver Lions potrošeni i izgubljeni, `earn_sl` gdje su zarađeni (nagrada za ubistvo je
na svom redu `reward`, a ne na redu `kill`, pa se ništa ne broji dvaput).

- **Meci** (`install` gdje je poznata granata slota - ubistvo ju je imenovalo, vidi [Ishodi pogodaka](hits.md#hit-outcomes) -
  inače `inferred`: prosječna cijena granata koje taj top može ispaliti na tom vozilu; osnovna granata je besplatna; mitraljezi
  se ne broje u replayu i ne koštaju ništa).
- **Lansiranja** (`inferred`): igra određuje cijenu konfiguracije oružja aviona po izlasku, a ne po komadu; jedan komad je
  medijan preko cijenjenih konfiguracija vozila od cijena / komada (`sum_weapons`, protumjere i dodatni rezervoari
  izostavljeni); 0 gdje su njegove konfiguracije besplatne.
- **Nagrade** (sve `inferred`): replay ne drži zapis nagrade - blok rezultata ima samo bodove i brojeve,
  nijedna poruka ne nosi Silver Lions (provjereno na klijentskim i serverskim replayevima). `kill` zarađuje `aKill` x
  `rewardMul<mode>` ubice x težinu klase žrtve (`units` u warpoints.blk, po njenom `unitClass`; AI jedinice po svojoj
  vrsti) x `aiKillK` za AI žrtvu x `groundKillMul` za avion koji ubija kopnenu jedinicu; RP isto
  s `expMul` i težinama iz rank.blk. Svaki drugi korak igračevog rezultata u repliciranoj tabeli rezultata je nagrada
  vrijedna svojih bodova po SL-u bitke po bodu (SL ubistva preko medijana bodova koraka ubistava, 
  `pointsPerKill` bloka); njen tip je brojač koji je s njom porastao (asistencije, zauzete zone, šteta zonama,
  nagrada za štetu, izbjegnute rakete), inače kritični / teški pogodak tog igrača unutar 3 s, inače detekcija
  igračeve jedinice unutar 2 s (`scouting`), inače `other`. `battle_end` je `winK` (pobjeda) ili `defeatK` (poraz)
  igračeve zarade tokom bitke, pobjednik po preostalim tiketima timova, zatim po njihovom rezultatu. Premium vrijeme, pojačivači,
  posada i modifikacije nisu poznati i ne primjenjuju se; budžeti ubistava kopnenih bitaka
  (`def_ground_kill_wp_budget*`) nisu modelirani.

`economy` dokumenta meča (a u `.3dheat` kontejneru `extensions["heat3d/economy"]` manifesta)
drži `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (isto po igraču, sa `netSl`), `vehicles` (po igračevom vozilu: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` i `check` (koliko je redova svake vrste bilo
cijenjeno, procijenjeno ili necijenjeno).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
