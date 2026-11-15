---
title: Ekonomija
nav_order: 14
lang: "hr"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomija {#economy}

Što je bitka koštala i donijela, kao stupci na njezinim retcima događaja, čitano iz **tvoje instalacije u
trenutku pretvaranja** (`char.vromfs.bin`: `config/wpcost.blk` po vozilu, `config/warpoints.blk` i
`config/rank.blk`; weapon blk datoteke iz `aces.vromfs.bin` kažu koja je modifikacija koja granata). Nijedan
igrin broj nije u ovom repozitoriju: vrijednosti idu samo u tvoj vlastiti izlaz. Bez `char.vromfs.bin` iz
instalacije ekonomija se ne zapisuje (`economy.available` false). Cijene su one za težinu bitke
(`repairCostHistorical` za RB, `...Arcade` za AB, `...Simulation` za SB).

| Stupac | Reci | Što |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (metak uzet nakon hica, kopnena vozila), `launch` (zrakoplovi, helikopteri) | cijena SL-a za metak, raketu, projektil ili bombu |
| `cost_lost_sl` | `death` vozila igrača | cijena popravka vozila (standardnog; u blk-u potpuno nadograđenog) |
| `earn_sl`, `earn_rp` | `reward` (novi događaj, na mjestu i vremenu onoga tko je zaradio) | zarađeni SL i RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | svaki redak s `cost_*` ili `earn_sl` | `SL` (`earn_rp` je bodovi za istraživanje) |
| `econ_basis` | isto | `install` (cijena pročitana iz instalacije) ili `inferred` (izračunato, dolje) |

**Tko je pobijedio.** `won` (0/1) na svakom retku tima, gdje to snimka kaže: rezultati snimke klijenta nose
ishod autora (`status`: `success` ili `fail`), pa je autorov tim pobijedio ili izgubio, a drugi tim obrnuto;
`result` u dokumentu meča kaže koje (`winner`, `status`, `authorTeam`). Poslužiteljske snimke i snimke
ostavljene prije kraja nemaju ishod (`status` poslužiteljske snimke uvijek je `success` i ne imenuje autora),
a nijedna vrsta ne sadrži instalirane modifikacije: rezultati navode vozila svakog igrača samo po nazivu i
vrsti. Tamo `won` ostaje prazan.

Model troška u pregledniku čita stupce `cost_*` (i `earn_*`) uz `currency`; zbroj `cost_fired_sl +
cost_lost_sl` daje gdje su SL-ovi potrošeni i izgubljeni, `earn_sl` gdje su zarađeni (nagrada za ubojstvo
je na svom retku `reward`, ne na retku `kill`, pa se ništa ne broji dvaput).

- **Streljivo** (`install` gdje je granata utora poznata - ubojstvo ju je imenovalo, vidi
  [Ishodi pogodaka](hits.md#hit-outcomes) - inače `inferred`: prosječna cijena granata koje taj top može
  ispaliti na tom vozilu; standardna granata je besplatna; mitraljezi snimka ne broji i koštaju nula).
- **Lansiranja** (`inferred`): igra cijeni paket oružja zrakoplova po letu, a ne po komadu; jedan komad je
  medijan preko cijenjenih paketa vozila (cijena / komadi; `sum_weapons`, protumjere i dodatni spremnici
  izostavljeni); 0 tamo gdje su paketi besplatni.
- **Nagrade** (sve `inferred`): snimka nema zapis o nagradi - blok rezultata nosi samo bodove i brojeve,
  nijedna poruka ne nosi SL-ove (provjereno na snimkama klijenta i poslužitelja). `kill` zarađuje `aKill` x
  `rewardMul<mode>` ubojice x težinu klase žrtve (`units` u warpoints.blk, prema njezinom `unitClass`; AI
  jedinice prema vrsti) x `aiKillK` za žrtvu AI x `groundKillMul` za zrakoplov koji ubija kopnenu jedinicu;
  RP isto s `expMul` i težinama iz rank.blk. Svaki drugi korak bodova igrača u replicirano tablici rezultata
  je nagrada vrijedna svojih bodova po SL-bodu bitke (SL ubojstva preko medijana bodova koraka ubojstava,
  `pointsPerKill` iz bloka); njezina vrsta je brojač koji je narastao s njim (asistencije, zauzete zone,
  šteta u zoni, nagrada za štetu, izbjegnute rakete), inače kritični / teški pogodak tog igrača unutar 3 s,
  inače otkrivanje jedinice igrača unutar 2 s (`scouting`), inače `other`. `battle_end` je `winK` (pobjeda)
  ili `defeatK` (poraz) od zarade igrača u bitci, pobjednik prema preostalim tiketima timova, pa njihovi
  bodovi. Vrijeme premium računa, pojačanja, posada i modifikacije nisu poznati i nisu primijenjeni;
  budžeti ubojstava u kopnenim bitkama (`def_ground_kill_wp_budget*`) nisu modelirani.

Dokument meča `economy` (a u kontejneru `.3dheat`, `extensions["heat3d/economy"]` iz manifesta) sadrži
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (isto po igraču, s `netSl`), `vehicles` (po vozilu igrača: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` i `check` (koliko je redaka svake vrste
cijenjeno, procijenjeno ili nije cijenjeno).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
