---
title: "Wirtschaft"
nav_order: 14
lang: lb
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Wirtschaft {#economy}

Wat d'Gefecht kascht an agedron huet, als Kolonnen op senge Evenement-Zeilen, gelies aus **denger Installatioun beim Émwandelen**
(`char.vromfs.bin`: `config/wpcost.blk` pro Gefier, `config/warpoints.blk` an `config/rank.blk`; d'Waffen-blks
vun `aces.vromfs.bin` soen, wéi eng Modifikatioun all Granat ass). Keng Zuel vum Spill ass an dësem Repository: d'
Wäerter ginn nëmmen an deng eege Ausgab. Ouni d'`char.vromfs.bin` vun der Installatioun gëtt keng Wirtschaft geschriwwen
(`economy.available` false). D'Präisser sinn déi vun der Schwieregkeet vum Gefecht (`repairCostHistorical` fir RB,
`...Arcade` AB, `...Simulation` SB).

| Kolonn | Zeilen | Wat |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (eng Patroun, déi no engem Schoss geholl gëtt, Buedemgefierer), `launch` (Fliger, Helikopteren) | SL, déi d'Patroun, d'Rakéitegeschoss, d'Rakéit oder d'Bomm kascht huet |
| `cost_lost_sl` | `death` vum Gefier vun engem Spiller | d'Reparaturkäschte vum Gefier (Serie; dat voll opgerüsten am Block) |
| `earn_sl`, `earn_rp` | `reward` (neit Evenement, op der Plaz an Zäit vum Verdéngenden) | verdéngte SL an RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | all Zeil mat engem `cost_*` oder `earn_sl` | `SL` (`earn_rp` sinn Fuerschungspunkten) |
| `econ_basis` | déiselwecht | `install` (e Präis aus der Installatioun gelies) oder `inferred` (ausgerechent, ënnen) |

**Wien gewonnen huet.** `won` (0/1) op all Zeil vun engem Team, wou de Replay et seet: d'Resultater vun engem Client-
Replay droen dem Auteur säin eegenen Ausgang (`status`: `success` oder `fail`), dofir huet dem
Auteur säin Team gewonnen oder verluer an dat anert Team de Géigendeel; `result` am Match-Dokument
seet wéi eent (`winner`, `status`, `authorTeam`). Server-Replays a Replays, déi virum
Enn verlooss goufen, droen keen Ausgang (dem Server-Replay säi `status` ass émmer `success` a nennt keen Auteur),
an keng vun deenen Aarte hält installéiert Modifikatiounen: d'Resultater lëschten d'Gefierer vun all Spiller nëmmen no
Numm an Typ. Do bleift `won` eidel.

Dem Viewer säi Käschtemodell liest d'Kolonnen `cost_*` (an `earn_*`) mat `currency`; d'Zomm vun `cost_fired_sl +
cost_lost_sl` gëtt, wou Silver Lions ausginn a verluer goufen, `earn_sl`, wou se verdéngt goufen (dem Kill seng Belounung ass
op senger `reward`-Zeil, net op der `kill`-Zeil, sou datt näischt duebel zielt).

- **Patroune** (`install`, wou d'Granat vum Slot bekannt ass - e Kill huet se genannt, kuck [Treffer-Ausgäng](hits.md#hit-outcomes) -
  soss `inferred`: de Mëttelpräis vun de Granaten, déi dës Kanoun op deem Gefier ka schéissen; eng Serie-Granat ass gratis; Maschinn-
  gewierer ginn net vum Replay gezielt a kaschten näischt).
- **Launches** (`inferred`): d'Spill preist dem Fliger säi Waffepreset pro Asaz, net pro Stéck; ee Stéck ass de
  Median iwwer d'gepreist Presets vum Gefier vu Präis / Stécker (`sum_weapons`, Géigemoossnamen an Zousazdanke
  ewechgelooss); 0, wou seng Presets gratis sinn.
- **Belounungen** (all `inferred`): de Replay huet kee Belounungs-Enregistrement - de Resultater-Block huet nëmmen Scoren an Zuelen,
  keng Message dréit Silver Lions (op Client- a Server-Replays gepréift). E `kill` verdéngt `aKill` x dem Killer säi
  `rewardMul<mode>` x dem Gewiicht vun der Affer-Klass (`units` an warpoints.blk, no senger `unitClass`; KI-Eenheeten no hirer
  Aart) x `aiKillK` fir en KI-Affer x `groundKillMul` fir e Fliger, deen eng Buedemeenheet ëmbréngt; RP datselwecht mat
  `expMul` an de Gewiichter vun rank.blk. All aner Schrëtt vum Score vun engem Spiller am replizéierte Scoreboard ass eng Belounung
  wäert seng Punkten zum SL pro Punkt vum Gefecht (dem Kill seng SL iwwer dem Median vun de Punkten vun de Kill-Schrëtt, dem
  `pointsPerKill` vum Block); säin Typ ass den Zieler, deen domat geklommen ass (Assists, eroberte Zonen, Zonenschued,
  Schuedauszeechnung, Rakéiteausweichungen), soss dem Spiller säi kritesche / schwéieren Treffer bannent 3 s, soss eng Erkennung vun der
  Eenheet vum Spiller bannent 2 s (`scouting`), soss `other`. `battle_end` ass `winK` (gewonnen) oder `defeatK` (verluer) vun de
  Verdéngschten vum Spiller am Gefecht, de Gewënner no de Tickets, déi dem Team bleiwen, dann hirem Score. Premium-Zäit, Booster,
  Crew a Modifikatioune si net bekannt a ginn net ugewannt; d'Kill-Budgeten vun de Buedemgefechter
  (`def_ground_kill_wp_budget*`) ginn net modelléiert.

D'`economy` vum Match-Dokument (an, an engem `.3dheat`-Container, d'`extensions["heat3d/economy"]` vum Manifest)
hält `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (datselwecht pro Spiller, mat `netSl`), `vehicles` (pro Spillergefier: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` an `check` (wéi vill Zeile vun all Aart
gepreist, geschat oder net gepreist goufen).

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
