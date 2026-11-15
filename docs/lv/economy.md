---
title: Ekonomika
nav_order: 14
lang: "lv"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomika {#economy}

Ko kauja izmaksāja un ko nopelnīja, kā kolonnas uz tās notikumu rindām. Tās tiek nolasītas no **jūsu instalācijas konvertēšanas laikā**
(`char.vromfs.bin`: `config/wpcost.blk` katram transportlīdzeklim, `config/warpoints.blk` un `config/rank.blk`; ieroču blk faili no
`aces.vromfs.bin` norāda, kura modifikācija ir katrs šāviņš). Šajā repozitorijā nav neviena spēles skaitļa: vērtības nonāk tikai jūsu
pašā izvadē. Bez instalācijas `char.vromfs.bin` nekāds ekonomikas ieraksts netiek veidots (`economy.available` ir false). Cenas ir
kaujas grūtības cenas (RB `repairCostHistorical`, AB `...Arcade`, SB `...Simulation`).

| Kolonna | Rindas | Ko nozīmē |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (šāviņš, kas ņemts pēc šāviena, sauszemes transportlīdzekļi), `launch` (lidmašīnas, helikopteri) | cik SL maksāja šāviņš, raķete, rakete vai bumba |
| `cost_lost_sl` | `death` spēlētāja transportlīdzeklim | transportlīdzekļa remonta cena (sākotnējā; blk pilnīgi uzlabotā) |
| `earn_sl`, `earn_rp` | `reward` (jauns notikums, nopelnītāja vietā un laikā) | nopelnītie SL un RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | katra rinda ar `cost_*` vai `earn_sl` | `SL` (`earn_rp` ir pētniecības punkti) |
| `econ_basis` | tas pats | `install` (cena nolasīta no instalācijas) vai `inferred` (aprēķināta, zemāk) |

**Kurš uzvarēja.** `won` (0/1) katrā komandas rindā, kur atkārtojums to nosaka. Klienta atkārtojuma rezultātos ir autora paša iznākums
(`status`: `success` vai `fail`), tātad autora komanda uzvarēja vai zaudēja, bet otra komanda — otrādi. Mača dokumentā `result` norāda, kas
ir (`winner`, `status`, `authorTeam`). Servera atkārtojumos un atkārtojumos, kas pamesti pirms beigām, iznākuma nav (servera atkārtojuma
`status` vienmēr ir `success` un autoru nenosauc), un abos gadījumos nav uzstādītu modifikāciju: rezultāti katra spēlētāja transportlīdzekļus
parāda tikai pēc nosaukuma un tipa. Tur `won` paliek tukšs.

Skatītāja izmaksu modelis lasa kolonnas `cost_*` (un `earn_*`) kopā ar `currency`; `cost_fired_sl + cost_lost_sl` summa rāda, kur tika
iztērēti un zaudēti Sudraba lauvas, `earn_sl` — kur tās tika nopelnītas (`kill` nopelnītā atlīdzība ir uz tās `reward` rindas, nevis uz
`kill` rindas, tāpēc nekas netiek skaitīts divreiz).

- **Šāviņi** (`install`, ja slota šāviņš ir zināms — nogalinājums to nosauca, skat. [Trāpījumu iznākumi](hits.md#hit-outcomes) —
  citādi `inferred`: tās ieroča šāviņu vidējā cena, ko šis lielgabals var šaut uz šī transportlīdzekļa; standarta šāviņš ir bez maksas;
  ložmetēji netiek skaitīti atkārtojumā un nemaksā neko).
- **Palaišana** (`inferred`): spēle cenu lidmašīnas ieroču komplektam nosaka par lidojumu, nevis par vienību; viena vienība ir mediāna
  pār transportlīdzekļa cenotajiem komplektiem cena / vienību skaits (`sum_weapons`; pretpasākumi un nomešanas tvertnes nav ieskaitītas);
  0, ja tās komplekti ir bez maksas.
- **Atlīdzības** (visas `inferred`): atkārtojumā nav atlīdzības ieraksta — rezultātu blokā ir tikai punkti un skaitītāji, neviens
  ziņojums nenes Sudraba lauvas (pārbaudīts klienta un servera atkārtojumos). `kill` nopelna `aKill` × nogalinātāja `rewardMul<mode>` ×
  upura klases svaru (`units` warpoints.blk pēc tā `unitClass`; MI vienības pēc to veida) × `aiKillK` MI upuram × `groundKillMul`, ja
  lidmašīna nogalina sauszemes vienību; RP tāpat ar `expMul` un rank.blk svariem. Visi pārējie spēlētāja punktu soļi replicētajā
  rezultātu tabulā ir atlīdzības, kas vērtas savus punktus kaujas SL par punktu (kill SL pār nogalinājumu soļu punktu mediānu, bloka
  `pointsPerKill`); to tips ir skaitītājs, kas ar tiem pieauga (palīdzības, iekarotas zonas, zonas bojājumi, bojājumu balva, raķešu
  izvairīšanās), citādi šī spēlētāja kritiskais / smagais trāpījums 3 s laikā, citādi spēlētāja vienības atklāšana 2 s laikā
  (`scouting`), citādi `other`. `battle_end` ir `winK` (uzvara) vai `defeatK` (zaudējums) no spēlētāja ieņēmumiem kaujā; uzvarētāju nosaka
  atlikušās komandu biļetes, tad punkti. Prēmijas laiks, pastiprinātāji, apkalpe un modifikācijas nav zināmi un netiek piemēroti;
  sauszemes kaujas nogalinājumu budžeti (`def_ground_kill_wp_budget*`) nav modelēti.

Mača dokumenta `economy` (un `.3dheat` konteinerā — manifesta `extensions["heat3d/economy"]`) satur `currency` `SL`, `researchCurrency`
`RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`), `players` (tas pats katram spēlētājam, ar `netSl`), `vehicles`
(katram spēlētāja transportlīdzeklim: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`,
`rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` un `check` (cik katra veida rindas tika novērtētas, aplēstas vai nav
novērtētas).

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
