---
title: "经济"
nav_order: 14
lang: zh
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# 经济 {#economy}

一场战斗花费和赚取了多少，以列的形式记录在其事件行中，数据读取自**转换时你的安装**（`char.vromfs.bin`：每辆载具的 `config/wpcost.blk`，`config/warpoints.blk` 和 `config/rank.blk`；`aces.vromfs.bin` 中的武器 blk 则说明每发炮弹属于哪种改装）。本仓库中没有游戏的任何数字：这些数值只会进入你自己的输出。如果没有安装中的 `char.vromfs.bin`，就不会写入任何经济数据（`economy.available` 为 false）。价格取自该场战斗难度对应的数值（RB 使用 `repairCostHistorical`，街机 AB 使用 `...Arcade`，模拟 SB 使用 `...Simulation`）。

| 列 | 行 | 内容 |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm`（射击之后取得的一发弹药，地面载具），`launch`（飞机、直升机） | 一发弹药、火箭弹、导弹或炸弹的 SL 花费 |
| `cost_lost_sl` | 玩家载具的 `death` | 该载具的修理费用（标准配置；使用区块中完全升级的版本） |
| `earn_sl`、`earn_rp` | `reward`（新事件，位于获得者的位置和时间） | 获得的 SL 和 RP |
| `rewardType` | `reward` | `kill`、`assist`、`capture`、`base_damage`、`damage`、`missile_evade`、`critical_hit`、`severe_damage`、`scouting`、`other`、`battle_end` |
| `currency` | 每一行带有 `cost_*` 或 `earn_sl` 的记录 | `SL`（`earn_rp` 为研究点数） |
| `econ_basis` | 同上 | `install`（从安装中读取的价格）或 `inferred`（推算得出，见下文） |

**谁赢了。** 录像给出时，一个队伍的每一行都会带有 `won`（0/1）：客户端录像的结果中带有作者自己的结局（`status`：`success` 或 `fail`），因此作者所在的队伍赢了或输了，另一队则相反；对局文档中的 `result` 会说明具体情况（`winner`、`status`、`authorTeam`）。服务器录像，以及在战斗结束前离开的录像，不包含结局（服务器录像的 `status` 始终为 `success`，且不标明作者）；这两类录像也都不包含已安装的改装：结果中只按名称和类型列出每位玩家的载具。在这些情况下，`won` 保持为空。

查看器的花费模型会读取 `cost_*`（以及 `earn_*`）列，并结合 `currency` 使用；把 `cost_fired_sl + cost_lost_sl` 相加，就得到 Silver Lions 花在哪里、又损失在哪里，`earn_sl` 则是它们在哪里获得的（击杀的奖励记录在其 `reward` 行中，而不是 `kill` 行中，因此不会重复计算）。

- **弹药**（当该槽位的炮弹已知时为 `install`，即击杀中已指明它，参见 [命中结果](hits.md#hit-outcomes)；否则为 `inferred`：该火炮在该载具上能发射的炮弹的平均价格；标准炮弹是免费的；录像不统计机枪，机枪的花费为零）。
- **发射**（`inferred`）：游戏是按出击而不是按单个物品为飞机的武器预设定价的；一个物品的价格取该载具有价格的各预设中，价格除以物品数量后的中位数（不包括 `sum_weapons`、干扰装置和副油箱）；如果其预设是免费的，则为 0。
- **奖励**（全部为 `inferred`）：录像中没有奖励记录：结果块只包含得分和计数，没有任何消息包含 Silver Lions（已在客户端和服务器录像上核对）。一次 `kill` 获得的奖励为 `aKill` 乘以击杀者的 `rewardMul<模式>`，再乘以受害者类别的权重（`warpoints.blk` 中的 `units`，按其 `unitClass`；AI 单位则按其类型），对于 AI 受害者再乘以 `aiKillK`，飞机击毁地面单位时再乘以 `groundKillMul`；RP 的计算方法相同，但使用 `expMul` 和 `rank.blk` 中的权重。复制的记分板中，玩家得分的其他每一步，都按该场战斗中每一分得分对应的 SL 折算为奖励（击杀的 SL 除以各击杀步骤得分的中位数，即区块中的 `pointsPerKill`）；其类型取随之增加的计数项（助攻、占领的区域、区域伤害、伤害奖励、导弹规避），否则取该玩家在 3 秒内的要害或严重命中，否则取 2 秒内对该玩家单位的侦察（`scouting`），否则为 `other`。`battle_end` 为该玩家战斗收益的 `winK`（获胜）或 `defeatK`（失败），获胜方由剩余的兵力点数决定，然后再按得分计算。高级时间、加成道具、乘组和改装尚不清楚，也未被应用；地面战斗的击杀预算（`def_ground_kill_wp_budget*`）未被建模。

对局文档中的 `economy`（在 `.3dheat` 容器中，则为清单中的 `extensions["heat3d/economy"]`）包含：`currency` 为 `SL`，`researchCurrency` 为 `RP`，`difficulty`，`totals`（`firedSl`、`lostSl`、`earnedSl`、`earnedRp`），`players`（同样的数据，按玩家划分，并包含 `netSl`），`vehicles`（按玩家载具：`repairSl`、`repairFullUpgradedSl`、`purchaseSl`、`researchRp`、`crewSl`、`crewExpertSl`、`rewardMul`、`expMul`、`groundKillMul`、`battleTimeAwardSl`、`rank`、`economicRank`、`unitClass`），`multipliers`（`aKill`、`aiKillK`、`winK`、`defeatK`、`wpMultiplier`），`winnerTeam`，`pointsPerKill`，以及 `check`（每类记录中有多少被定价、被估算或未被定价）。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
