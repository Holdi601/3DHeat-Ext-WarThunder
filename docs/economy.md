---
title: Economy
nav_order: 14
---

# Economy

What the battle cost and earned, as columns on its event rows, read from **your install at conversion time**
(`char.vromfs.bin`: `config/wpcost.blk` per vehicle, `config/warpoints.blk` and `config/rank.blk`; the weapon blks
of `aces.vromfs.bin` say which modification each shell is). No number of the game's is in this repository: the
values go into your own output only. Without the install's `char.vromfs.bin` no economy is written
(`economy.available` false). The prices are those of the battle's difficulty (`repairCostHistorical` for RB,
`...Arcade` AB, `...Simulation` SB).

| Column | Rows | What |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (a round taken after a shot, ground vehicles), `launch` (aircraft, helicopters) | SL the round, rocket, missile or bomb cost |
| `cost_lost_sl` | `death` of a player's vehicle | the vehicle's repair cost (stock; the fully upgraded one in the block) |
| `earn_sl`, `earn_rp` | `reward` (new event, at the earner's place and time) | SL and RP earned |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | every row with a `cost_*` or `earn_sl` | `SL` (`earn_rp` is research points) |
| `econ_basis` | the same | `install` (a price read from the install) or `inferred` (worked out, below) |

**Who won.** `won` (0/1) on every row of a team's, where the replay says: a client
replay's results carry the author's own outcome (`status`: `success` or `fail`), so the
author's team won or lost and the other team the reverse; `result` in the match document
says which (`winner`, `status`, `authorTeam`). Server replays and replays left before the
end carry no outcome (a server replay's `status` is always `success` and names no author),
and neither kind holds installed modifications: the results list each player's vehicles by
name and type only. There `won` stays empty.

The viewer's cost model reads the columns `cost_*` (and `earn_*`) with `currency`; summing `cost_fired_sl +
cost_lost_sl` gives where Silver Lions were spent and lost, `earn_sl` where they were earned (a kill's reward is
on its `reward` row, not on the `kill` row, so nothing counts twice).

- **Rounds** (`install` where the slot's shell is known - a kill named it, see [Hit outcomes](hits.md#hit-outcomes) -
  else `inferred`: the mean price of the shells that gun can fire on that vehicle; a stock shell is free; machine
  guns are not counted by the replay and cost nothing).
- **Launches** (`inferred`): the game prices an aircraft's weapon preset per sortie, not per item; one item is the
  median over the vehicle's priced presets of price / items (`sum_weapons`, countermeasures and drop tanks left
  out); 0 where its presets are free.
- **Rewards** (all `inferred`): the replay holds no reward record - the results block has scores and counts only,
  no message carries Silver Lions (checked on client and server replays). A `kill` earns `aKill` x the killer's
  `rewardMul<mode>` x the victim class's weight (`units` in warpoints.blk, by its `unitClass`; AI units by their
  kind) x `aiKillK` for an AI victim x `groundKillMul` for an aircraft killing a ground unit; RP the same with
  `expMul` and rank.blk's weights. Every other step of a player's score in the replicated scoreboard is a reward
  worth its points at the battle's SL a point (a kill's SL over the median points of the kills' steps, the
  `pointsPerKill` of the block); its type is the counter that rose with it (assists, zones captured, zone damage,
  damage award, missile evades), else that player's critical / severe hit within 3 s, else a detection of the
  player's unit within 2 s (`scouting`), else `other`. `battle_end` is `winK` (won) or `defeatK` (lost) of the
  player's in-battle earnings, the winner by the teams' tickets left, then their score. Premium time, boosters,
  crew and modifications are not known and not applied; the ground battles' kill budgets
  (`def_ground_kill_wp_budget*`) are not modelled.

The match document's `economy` (and, in a `.3dheat` container, the manifest's `extensions["heat3d/economy"]`)
holds `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (the same per player, with `netSl`), `vehicles` (per player vehicle: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` and `check` (how many rows of each kind were
priced, estimated or not priced).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
