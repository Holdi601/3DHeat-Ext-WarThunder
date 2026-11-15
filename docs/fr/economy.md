---
title: Économie
nav_order: 14
lang: fr
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Économie {#economy}

Ce que la bataille a coûté et rapporté, sous forme de colonnes sur ses lignes d'événements,
lu dans **votre installation au moment de la conversion** (`char.vromfs.bin` : `config/wpcost.blk`
pour chaque véhicule, `config/warpoints.blk` et `config/rank.blk` ; les blk d'armes de
`aces.vromfs.bin` indiquent quelle modification correspond à chaque obus). Aucun chiffre du jeu
ne figure dans ce dépôt : les valeurs n'entrent que dans votre propre résultat. Sans le
`char.vromfs.bin` de l'installation, aucune économie n'est écrite (`economy.available` à faux).
Les prix sont ceux de la difficulté de la bataille (`repairCostHistorical` pour RB,
`...Arcade` pour AB, `...Simulation` pour SB).

| Colonne | Lignes | Contenu |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (un coup rechargé après un tir, véhicules terrestres), `launch` (avions, hélicoptères) | coût en LA du coup, de la roquette, du missile ou de la bombe |
| `cost_lost_sl` | `death` d'un véhicule de joueur | le coût de réparation du véhicule (de base ; celui entièrement amélioré dans le blk) |
| `earn_sl`, `earn_rp` | `reward` (nouvel événement, à la place et à l'heure de celui qui gagne) | LA et PR gagnés |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | chaque ligne avec un `cost_*` ou `earn_sl` | `SL` (`earn_rp` sont des points de recherche) |
| `econ_basis` | la même chose | `install` (un prix lu dans l'installation) ou `inferred` (calculé, voir ci-dessous) |

**Qui a gagné.** `won` (0/1) sur chaque ligne d'une équipe, lorsque le replay le dit : les
résultats d'un replay client portent le résultat de l'auteur (`status` : `success` ou `fail`), donc
l'équipe de l'auteur a gagné ou perdu, et l'autre équipe l'inverse ; `result` dans le document
de match indique lequel (`winner`, `status`, `authorTeam`). Les replays serveur et les replays
arrêtés avant la fin ne portent pas de résultat (le `status` d'un replay serveur vaut toujours
`success` et ne nomme aucun auteur), et ni l'un ni l'autre ne contiennent les modifications
installées : les résultats listent les véhicules de chaque joueur seulement par leur nom et leur
type. Dans ce cas, `won` reste vide.

Le modèle de coût de la visionneuse lit les colonnes `cost_*` (et `earn_*`) avec `currency` ;
additionner `cost_fired_sl + cost_lost_sl` donne où les Lions d'argent ont été dépensés et perdus,
`earn_sl` où ils ont été gagnés (la récompense d'un frag est sur sa ligne `reward`, non sur la
ligne `kill`, donc rien ne compte deux fois).

- **Coups** (`install` lorsque l'obus du logement est connu - un frag l'a nommé, voir
  [Issues des impacts](hits.md#hit-outcomes) - sinon `inferred` : le prix moyen des obus que ce canon
  peut tirer sur ce véhicule ; un obus d'origine est gratuit ; les mitrailleuses ne sont pas
  comptées par le replay et ne coûtent rien).
- **Lancements** (`inferred`) : le jeu fixe le prix du préréglage d'armes d'un avion par sortie, et
  non par article ; un article vaut la médiane, sur les préréglages payants du véhicule, du prix /
  nombre d'articles (`sum_weapons`, contre-mesures et réservoirs largables exclus) ; 0 là où ses
  préréglages sont gratuits.
- **Récompenses** (toutes `inferred`) : le replay ne contient aucune trace de récompense - le bloc des
  résultats ne donne que les scores et les compteurs, aucun message ne porte de Lions d'argent
  (vérifié sur les replays client et serveur). Un `kill` rapporte `aKill` x le `rewardMul<mode>` du
  tueur x le poids de la classe de la victime (`units` dans warpoints.blk, selon son `unitClass` ;
  les unités d'IA selon leur type) x `aiKillK` pour une victime d'IA x `groundKillMul` pour un avion
  qui tue une unité au sol ; les PR de la même façon avec `expMul` et les poids de rank.blk. Chaque
  autre étape du score d'un joueur dans le tableau de bord répliqué est une récompense valant ses
  points au prix d'un point en LA pour la bataille (les LA d'un frag sur la médiane des points des
  étapes des frags, le `pointsPerKill` du bloc) ; son type est le compteur qui a monté avec lui
  (assistances, zones capturées, dégâts de zone, prime de dégâts, esquives de missiles), sinon le
  coup critique ou grave de ce joueur dans les 3 s, sinon une détection de l'unité du joueur dans
  les 2 s (`scouting`), sinon `other`. `battle_end` est `winK` (victoire) ou `defeatK` (défaite) des
  gains en bataille du joueur, le vainqueur étant désigné par les tickets restants des équipes, puis
  leur score. Le temps premium, les boosters, l'équipage et les modifications ne sont pas connus et ne
  sont pas appliqués ; les budgets de frags des batailles au sol (`def_ground_kill_wp_budget*`) ne
  sont pas modélisés.

L'`economy` du document de match (et, dans un conteneur `.3dheat`, `extensions["heat3d/economy"]`
du manifeste) contient `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`,
`lostSl`, `earnedSl`, `earnedRp`), `players` (les mêmes par joueur, avec `netSl`), `vehicles`
(par véhicule de joueur : `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`,
`crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`,
`unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`,
`pointsPerKill` et `check` (combien de lignes de chaque type ont été chiffrées, estimées ou non
chiffrées).

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
