---
title: Economie
nav_order: 14
lang: "ro"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economie {#economy}

Cât a costat și cât a câștigat bătălia, ca coloane pe rândurile ei de evenimente, citite din **instalarea dumneavoastră la momentul conversiei**
(`char.vromfs.bin`: `config/wpcost.blk` pe vehicul, `config/warpoints.blk` și `config/rank.blk`; blk-urile de arme
din `aces.vromfs.bin` spun ce modificare are fiecare proiectil). Niciun număr al jocului nu se află în acest depozit: valorile
ajung doar în rezultatul dumneavoastră. Fără `char.vromfs.bin` din instalare nu se scrie nicio economie
(`economy.available` false). Prețurile sunt cele ale dificultății bătăliei (`repairCostHistorical` pentru RB,
`...Arcade` pentru AB, `...Simulation` pentru SB).

| Coloană | Rânduri | Ce este |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (o rundă încărcată după o tragere, vehicule terestre), `launch` (avioane, elicoptere) | costul în SL al rundei, rachetei, rachetei ghidate sau bombei |
| `cost_lost_sl` | `death` al unui vehicul al unui jucător | costul reparației vehiculului (de serie; cel complet modernizat din blk) |
| `earn_sl`, `earn_rp` | `reward` (eveniment nou, la locul și momentul celui care câștigă) | SL și RP câștigate |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | fiecare rând cu un `cost_*` sau `earn_sl` | `SL` (`earn_rp` sunt puncte de cercetare) |
| `econ_basis` | la fel | `install` (un preț citit din instalare) sau `inferred` (calculat, mai jos) |

**Cine a câștigat.** `won` (0/1) pe fiecare rând al unei echipe, unde replay-ul o spune: rezultatele unui
replay de client poartă rezultatul propriu al autorului (`status`: `success` sau `fail`), deci echipa autorului
a câștigat sau a pierdut, iar cealaltă echipă invers; `result` din documentul meciului
spune care (`winner`, `status`, `authorTeam`). Replay-urile de server și cele lăsate înainte de
sfârșit nu au niciun rezultat (`status` al unui replay de server este mereu `success` și nu numește autorul),
iar niciunul dintre ele nu are modificările instalate: rezultatele listează vehiculele fiecărui jucător
doar după nume și tip. Acolo `won` rămâne gol.

Modelul de cost al vizualizatorului citește coloanele `cost_*` (și `earn_*`) cu `currency`; adunarea lui `cost_fired_sl +
cost_lost_sl` dă unde au fost cheltuiți și pierduți Silver Lions, `earn_sl` unde au fost câștigați (recompensa unei
uciderii este pe rândul ei `reward`, nu pe rândul `kill`, deci nimic nu se numără de două ori).

- **Runde** (`install` unde se cunoaște proiectilul slotului - o ucidere l-a numit, vedeți [Rezultatele loviturilor](hits.md#hit-outcomes) -
  altfel `inferred`: prețul mediu al proiectilelor pe care le poate trage tunul acela pe acel vehicul; un proiectil de serie este gratuit; mitralierele
  nu sunt numărate de replay și nu costă nimic).
- **Lansări** (`inferred`): jocul prețuiește prestabilirea de arme a unui avion pe ieșire, nu pe articol; un articol este
  mediana, peste prestabilirile prețuite ale vehiculului, a prețului / articolelor (`sum_weapons`, contramăsurile și rezervoarele
  de pe aripi lăsate afară); 0 unde prestabilirile sale sunt gratuite.
- **Recompense** (toate `inferred`): replay-ul nu are nicio înregistrare de recompensă - blocul rezultatelor are doar scoruri și
  numărători, niciun mesaj nu poartă Silver Lions (verificat pe replay-uri de client și de server). O `kill` câștigă `aKill` x
  `rewardMul<mode>` al ucigașului x greutatea clasei victimei (`units` din warpoints.blk, după `unitClass`; unitățile IA după
  tipul lor) x `aiKillK` pentru o victimă IA x `groundKillMul` pentru un avion care ucide o unitate terestră; RP la fel cu
  `expMul` și greutățile din rank.blk. Fiecare alt pas al scorului unui jucător din tabela de scor replicată este o recompensă
  cât valorează punctele sale la SL pe punct al bătăliei (SL-ul unei uciderii peste mediana punctelor pașilor uciderilor,
  `pointsPerKill` din bloc); tipul său este contorul care a crescut odată cu el (asistențe, zone capturate, daune
  zone, premiul pentru daune, evitări de rachete), altfel lovitura critică / gravă a acelui jucător în 3 s, altfel o detectare a
  unității jucătorului în 2 s (`scouting`), altfel `other`. `battle_end` este `winK` (câștigat) sau `defeatK` (pierdut) din
  câștigurile jucătorului din bătălie, câștigătorul după biletele rămase ale echipelor, apoi scorul lor. Timpul premium, boosterii,
  echipajul și modificările nu sunt cunoscute și nu sunt aplicate; bugetele de ucideri ale bătăliilor terestre
  (`def_ground_kill_wp_budget*`) nu sunt modelate.

Câmpul `economy` din documentul meciului (și, într-un container `.3dheat`, `extensions["heat3d/economy"]` din manifest)
ține `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (același lucru pe jucător, cu `netSl`), `vehicles` (pe vehicul al jucătorului: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` și `check` (câte rânduri de fiecare fel au fost
prețuite, estimate sau neprețuite).

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
