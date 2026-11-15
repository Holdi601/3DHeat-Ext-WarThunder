---
title: Economia
nav_order: 14
lang: ca
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economia {#economy}

Quant ha costat i guanyat la batalla, com a columnes de les seves files d'esdeveniment, llegides de
**la teva instal·lació en el moment de la conversió** (`char.vromfs.bin`: `config/wpcost.blk` per vehicle,
`config/warpoints.blk` i `config/rank.blk`; els blocs d'armes de `aces.vromfs.bin` indiquen quina
modificació és cada obús). Cap número del joc és en aquest repositori: els valors només van a la teva
pròpia sortida. Sense el `char.vromfs.bin` de la instal·lació no s'escriu cap economia
(`economy.available` fals). Els preus són els de la dificultat de la batalla (`repairCostHistorical` per a
RB, `...Arcade` per a AB, `...Simulation` per a SB).

| Columna | Files | Què és |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (una ronda presa després d'un tret, vehicles terrestres), `launch` (avions, helicòpters) | el cost en SL de la ronda, coet, míssil o bomba |
| `cost_lost_sl` | `death` d'un vehicle d'un jugador | el cost de reparació del vehicle (de sèrie; el totalment millorat del bloc) |
| `earn_sl`, `earn_rp` | `reward` (esdeveniment nou, al lloc i moment de qui el guanya) | SL i RP guanyats |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | cada fila amb un `cost_*` o `earn_sl` | `SL` (`earn_rp` són punts d'investigació) |
| `econ_basis` | el mateix | `install` (un preu llegit de la instal·lació) o `inferred` (calculat, més avall) |

**Qui va guanyar.** `won` (0/1) a cada fila d'un equip, quan la repetició ho diu: els resultats d'una
repetició de client porten el resultat propi de qui grava (`status`: `success` o `fail`), de manera que
l'equip de qui grava va guanyar o perdre, i l'altre equip el contrari; `result` al document de partida ho
indica (`winner`, `status`, `authorTeam`). Les repeticions de servidor i les repeticions abandonades abans
del final no porten un resultat (el `status` d'una repetició de servidor és sempre `success` i no nomena
cap jugador que gravi), i cap de les dues no porta modificacions instal·lades: els resultats llisten els
vehicles de cada jugador només pel nom i el tipus. Allà, `won` queda buit.

El model de cost del visualitzador llegeix les columnes `cost_*` (i `earn_*`) amb `currency`; sumar
`cost_fired_sl + cost_lost_sl` dona on s'han gastat i perdut els Lleons de plata, i `earn_sl` on se n'han
guanyat (la recompensa d'una mort és a la seva fila `reward`, no a la fila `kill`, de manera que res no
es compta dues vegades).

- **Rondes** (`install` quan se sap l'obús de la ranura, que una mort ha nomenat, mira
  [Resultats dels impactes](hits.md#hit-outcomes); en cas contrari `inferred`: el preu mitjà dels obusos
  que aquell canó pot disparar en aquell vehicle; un obús de sèrie és gratuït; les metralladores no les
  compta la repetició i no costen res).
- **Llançaments** (`inferred`): el joc valora el preajust d'armes d'un avió per sortida, no per element;
  un element és la mediana, entre els preajusts valorats del vehicle, de preu / elements (s'exclouen
  `sum_weapons`, les contramesures i els dipòsits de caiguda); 0 quan els seus preajusts són gratuïts.
- **Recompenses** (totes `inferred`): la repetició no té cap registre de recompensa: el bloc de resultats
  només té puntuacions i recomptes, cap missatge porta Lleons de plata (comprovat en repeticions de client i
  de servidor). Una `kill` guanya `aKill` × el `rewardMul<mode>` de l'assassí × el pes de la classe de la
  víctima (`units` a warpoints.blk, segons el seu `unitClass`; les unitats IA segons el seu tipus) × `aiKillK`
  per a una víctima IA × `groundKillMul` quan un avió mata una unitat terrestre; els RP igual amb `expMul` i
  els pesos de rank.blk. Cada altre pas de la puntuació d'un jugador a la taula replicada és una recompensa
  valorada pels seus punts a SL per punt de la batalla (el SL d'una mort sobre els punts mitjans dels passos
  de les morts, el `pointsPerKill` del bloc); el seu tipus és el comptador que va pujar amb ell (assistències,
  zones capturades, dany a zones, premi per dany, evasions de míssils), si no el dany crític o greu d'aquell
  jugador dins de 3 s, si no una detecció de la unitat del jugador dins de 2 s (`scouting`), si no `other`.
  `battle_end` és `winK` (guanyat) o `defeatK` (perdut) dels guanys del jugador dins la batalla, el guanyador
  pels tiquets que han quedat als equips, i després per la seva puntuació. El temps premium, els potenciadors,
  la tripulació i les modificacions no se sap quins són i no s'apliquen; els pressupostos de morts a terra de
  les batalles terrestres (`def_ground_kill_wp_budget*`) no es modelen.

L'`economy` del document de partida (i, en un contenidor `.3dheat`, el `extensions["heat3d/economy"]` del
manifest) conté `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`,
`earnedSl`, `earnedRp`), `players` (el mateix per jugador, amb `netSl`), `vehicles` (per vehicle de jugador:
`repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`,
`expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`,
`aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` i `check` (quantes files de cada
tipus s'han valorat, estimat o no valorat).

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
