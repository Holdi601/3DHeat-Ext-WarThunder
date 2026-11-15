---
title: "經濟"
nav_order: 14
lang: zh-Hant
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# 經濟 {#economy}

本場戰鬥的花費與收入，以欄位的形式列在它的事件列上，這些數值是在**轉換時從你的安裝目錄**讀取（`char.vromfs.bin`：每個載具的 `config/wpcost.blk`、`config/warpoints.blk` 與 `config/rank.blk`；`aces.vromfs.bin` 的武器 blk 則說明每發彈藥是哪種改裝）。本儲存庫中沒有任何遊戲的數值：這些數值只會寫入你自己的輸出中。沒有安裝目錄中的 `char.vromfs.bin` 時，不會寫入任何經濟資料（`economy.available` 為 false）。價格採用該場戰鬥難度的數值（RB 用 `repairCostHistorical`，AB 用 `...Arcade`，SB 用 `...Simulation`）。

| 欄位 | 列 | 內容 |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm`（射擊後補充的一發，地面載具）、`launch`（飛機、直升機） | 這發砲彈、火箭、飛彈或炸彈的 SL 花費 |
| `cost_lost_sl` | 玩家載具的 `death` | 載具的維修費用（原廠狀態；區塊中為完全升級後的狀態） |
| `earn_sl`、`earn_rp` | `reward`（新事件，位於獲得者的位置與時間） | 獲得的 SL 與 RP |
| `rewardType` | `reward` | `kill`、`assist`、`capture`、`base_damage`、`damage`、`missile_evade`、`critical_hit`、`severe_damage`、`scouting`、`other`、`battle_end` |
| `currency` | 每一列含有 `cost_*` 或 `earn_sl` 的列 | `SL`（`earn_rp` 為研究點數） |
| `econ_basis` | 同上 | `install`（從安裝目錄讀取的價格）或 `inferred`（依下文推算） |

**誰獲勝。**若回放有提供，則該隊每一列都有 `won`（0/1）。客戶端回放的結算中含有作者自己的結果（`status`：`success` 或 `fail`），因此作者的隊伍勝或敗，另一隊則相反；對戰文件中的 `result` 會說明這一點（`winner`、`status`、`authorTeam`）。伺服器回放與在戰鬥結束前留下的回放都不含結果（伺服器回放的 `status` 永遠是 `success`，且不指出作者），兩種回放也都不含已安裝的改裝：結算只會列出每位玩家的載具名稱與類型。在這些情況下，`won` 會保持空白。

檢視器的花費模型會讀取 `cost_*`（與 `earn_*`）欄位以及 `currency`；把 `cost_fired_sl + cost_lost_sl` 加總，就能得到 Silver Lions 花在哪裡、損失在哪裡；`earn_sl` 則是它們在哪裡獲得。擊殺的獎勵記在它的 `reward` 列上，而不在 `kill` 列上，因此不會重複計算。

- **砲彈**（若該槽位的彈藥已知，則為 `install`，即擊殺時已辨識出它，見[擊中結果](hits.md#hit-outcomes)；否則為 `inferred`：該門砲在該載具上能發射的彈藥的平均價格；原廠彈藥免費；機槍不由回放計算，花費為零）。
- **發射**（`inferred`）：遊戲是依每次出擊而非依每件物品來計價飛機的武器預設；一件物品的價格，是該載具有價格的預設的價格除以件數後的中位數（不計 `sum_weapons`、干擾彈與副油箱）；若其預設免費，則為 0。
- **獎勵**（全部為 `inferred`）：回放中沒有獎勵紀錄——結算區塊只有分數與次數，沒有任何訊息包含 Silver Lions（已在客戶端與伺服器回放上核對）。`kill` 的獎勵為：擊殺者的 `aKill` × 其 `rewardMul<mode>` × 被擊殺者類別的權重（warpoints.blk 中 `units`，依其 `unitClass`；AI 單位依其種類）× 對 AI 目標的 `aiKillK` × 飛機擊毀地面單位時的 `groundKillMul`；RP 亦同，但使用 `expMul` 與 rank.blk 的權重。回放分數中該玩家其他每一步分數，都是以其分數乘上本場戰鬥每分的 SL 計算的獎勵（一次擊殺的 SL 除以各擊殺步驟的中位分數，即區塊中的 `pointsPerKill`）；其類型取決於與它一起上升的計數器（助攻、佔領區域、區域傷害、傷害獎勵、導彈規避），否則為該玩家在 3 秒內的關鍵或嚴重命中，否則為 2 秒內偵測到該玩家單位（`scouting`），否則為 `other`。`battle_end` 是該玩家在戰鬥中所得的 `winK`（獲勝）或 `defeatK`（落敗），獲勝方由剩餘票數決定，然後看分數。高級時間、加成道具、組員與改裝都無從得知，也不會套用；地面戰鬥的擊殺預算（`def_ground_kill_wp_budget*`）尚未建模。

對戰文件中的 `economy`（以及在 `.3dheat` 容器中，清單中的 `extensions["heat3d/economy"]`）包含：`currency` 為 `SL`、`researchCurrency` 為 `RP`、`difficulty`、`totals`（`firedSl`、`lostSl`、`earnedSl`、`earnedRp`）、`players`（相同的數值，依玩家分列，並含 `netSl`）、`vehicles`（每位玩家的載具：`repairSl`、`repairFullUpgradedSl`、`purchaseSl`、`researchRp`、`crewSl`、`crewExpertSl`、`rewardMul`、`expMul`、`groundKillMul`、`battleTimeAwardSl`、`rank`、`economicRank`、`unitClass`）、`multipliers`（`aKill`、`aiKillK`、`winK`、`defeatK`、`wpMultiplier`）、`winnerTeam`、`pointsPerKill`，以及 `check`（每種列有多少已計價、為估算或未計價）。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
