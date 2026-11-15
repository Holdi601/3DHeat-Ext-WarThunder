---
title: Economía
nav_order: 14
lang: "es"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economía {#economy}

Lo que costó y ganó la batalla, como columnas en sus filas de evento, leídas de **tu instalación en el momento de convertir**
(`char.vromfs.bin`: `config/wpcost.blk` por vehículo, `config/warpoints.blk` y `config/rank.blk`; los blk de armas de
`aces.vromfs.bin` indican qué modificación es cada proyectil). Ningún número del juego está en este repositorio: los
valores van solo a tu propia salida. Sin el `char.vromfs.bin` de la instalación no se escribe ninguna economía
(`economy.available` falso). Los precios son los de la dificultad de la batalla (`repairCostHistorical` para RB,
`...Arcade` para AB, `...Simulation` para SB).

| Columna | Filas | Qué es |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (un proyectil tomado tras un disparo, vehículos terrestres), `launch` (aviones, helicópteros) | SL que cuesta el proyectil, cohete, misil o bomba |
| `cost_lost_sl` | `death` de un vehículo de un jugador | el coste de reparación del vehículo (de serie; el totalmente mejorado en el bloque) |
| `earn_sl`, `earn_rp` | `reward` (evento nuevo, en el lugar y el momento de quien lo gana) | SL y RP ganados |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | toda fila con un `cost_*` o `earn_sl` | `SL` (`earn_rp` son puntos de investigación) |
| `econ_basis` | lo mismo | `install` (un precio leído de la instalación) o `inferred` (calculado, abajo) |

**Quién ganó.** `won` (0/1) en cada fila de un equipo, cuando la repetición lo indica: los resultados de una
repetición de cliente contienen el resultado propio del autor (`status`: `success` o `fail`), así que el
equipo del autor ganó o perdió y el otro equipo al revés; `result` en el documento de la partida
indica cuál (`winner`, `status`, `authorTeam`). Las repeticiones de servidor y las que se dejan antes del
final no contienen resultado (el `status` de una repetición de servidor siempre es `success` y no nombra ningún autor),
y ninguna de las dos guarda las modificaciones instaladas: los resultados listan los vehículos de cada jugador
solo por nombre y tipo. Allí `won` queda vacío.

El modelo de coste del visor lee las columnas `cost_*` (y `earn_*`) con `currency`; sumar `cost_fired_sl +
cost_lost_sl` da dónde se gastaron y perdieron Leones de Plata, `earn_sl` dónde se ganaron (la recompensa de una baja
está en su fila `reward`, no en la fila `kill`, así que nada se cuenta dos veces).

- **Proyectiles** (`install` cuando se conoce el proyectil de la ranura - una baja lo nombró, véase [Resultados de impacto](hits.md#hit-outcomes) -
  si no `inferred`: el precio medio de los proyectiles que ese cañón puede disparar en ese vehículo; un proyectil de serie es gratis; las
  ametralladoras no las cuenta la repetición y no cuestan nada).
- **Lanzamientos** (`inferred`): el juego pone precio al preajuste de armas de un avión por salida, no por unidad; una unidad es la
  mediana, entre los preajustes con precio del vehículo, de precio / unidades (`sum_weapons`, contramedidas y depósitos
  auxiliares excluidos); 0 donde sus preajustes son gratuitos.
- **Recompensas** (todas `inferred`): la repetición no contiene ningún registro de recompensa - el bloque de resultados solo tiene puntuaciones y recuentos,
  ningún mensaje lleva Leones de Plata (comprobado en repeticiones de cliente y de servidor). Una `kill` gana `aKill` x el
  `rewardMul<modo>` del asesino x el peso de la clase de la víctima (`units` en warpoints.blk, según su `unitClass`; las unidades de IA según
  su tipo) x `aiKillK` si la víctima es de IA x `groundKillMul` si un avión derriba una unidad terrestre; los RP lo mismo con
  `expMul` y los pesos de rank.blk. Cada otro paso de la puntuación de un jugador en el marcador replicado es una recompensa
  que vale sus puntos a los SL de la batalla por punto (los SL de una baja sobre la mediana de los puntos de los pasos de las bajas,
  el `pointsPerKill` del bloque); su tipo es el contador que subió con él (asistencias, zonas capturadas, daño a zonas,
  premio por daño, evasiones de misiles), si no el impacto crítico o grave de ese jugador en 3 s, si no una detección de la
  unidad del jugador en 2 s (`scouting`), si no `other`. `battle_end` es `winK` (ganó) o `defeatK` (perdió) de las ganancias en
  batalla del jugador, con el ganador según los tickets que quedan a cada equipo, y luego su puntuación. Tiempo premium, potenciadores,
  tripulación y modificaciones no se conocen y no se aplican; los presupuestos de bajas de las batallas terrestres
  (`def_ground_kill_wp_budget*`) no están modelados.

El `economy` del documento de la partida (y, en un contenedor `.3dheat`, `extensions["heat3d/economy"]` del manifiesto)
contiene `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (lo mismo por jugador, con `netSl`), `vehicles` (por vehículo de jugador: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` y `check` (cuántas filas de cada tipo se
pusieron precio, se estimaron o no tuvieron precio).

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
