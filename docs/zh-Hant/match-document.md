---
title: "對戰文件"
nav_order: 7
lang: "zh-Hant"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# 對戰文件 {#the-match-document}

![合成對戰文件的開頭，以及它的鍵](../assets/img/match-document.svg)

`<match>.match.json` 保存了回放所記錄、但不屬於表格中任何一列的所有內容。檢視器的對戰分頁會讀取它。

## 戰鬥 {#the-battle}

| 鍵 | 內容 |
|---|---|
| `format`、`version` | `heat3d-wt-replay-match`、`2` |
| `match`、`map`、`level` | 對戰 id（與檔案名稱相同）；地圖的 id；所使用的地圖檔案 |
| `mission`、`missionKey` | 任務的名稱，以及它在遊戲文字檔中的鍵名 |
| `battleClass`、`environment`、`weather` | 與標頭所給的相同 |
| `sessionId`、`server` | 戰鬥的工作階段 id；伺服器 |
| `replayVersion`、`flightLayout` | 回放格式的版本；所讀取的飛行封包格式（`2025` 或 `2026`） |
| `files` | 所讀取的回放檔案（一個，或伺服器回放的各分段） |
| `started`、`timePlayed`、`replayEnd` | 開始時間（ISO，UTC）；遊玩秒數（取自結算）；回放最後一個封包的秒數 |
| `author`、`authorUserId` | 錄製玩家及其 Gaijin id（客戶端回放） |
| `teams` | 戰鬥中的隊伍（`1`、`2`） |
| `result` | `winner`、`status`（`success` 或 `fail`，即作者的結果）、`authorTeam`、`teams`（[經濟](economy.md)） |
| `vehicleNames` | 載具名稱的來源（你的安裝目錄）及其語言 |
| `conventions` | 表格的單位與符號：軸、時間、生命、軌跡、存活、橫滾等 |

## 其他一切 {#everything-else}

| 鍵 | 內容 |
|---|---|
| `battle`、`difficulty`、`gameMode` | 戰鬥模式：`difficulty` 為 `AB` / `RB` / `SB`（以及其名稱與標頭位元組），`gameMode` 為 `ground` / `air` / `naval`，任務的模式（`Dom`、`Conq`、`Bttl`、`I2M` 等），以及其在你安裝目錄中的英文名稱（`Domination`、`Enduring Confrontation`），允許的單位類型（見[戰鬥模式](ground.md#battle-mode)） |
| `settings` | 標頭之後的任務 blk：模式、環境、天氣、分數與時間限制、國家、允許的單位類型、風，以及 `stars`（緯度、經度、日期、當地時間） |
| `sky` | 第一個 `CustomWeatherParams`：太陽與月亮的方向、風、天空顏色、雲的偏移 |
| `players`、`slots` | 結算中每位玩家的一行（擊殺、地面擊殺、死亡、助攻、分數、佔領、小隊、戰隊、國家、陣容、所駕駛的 uid）；回放中的玩家槽位（名稱、user id、隊伍） |
| `units` | 回放中建立的每個單位實體：eid、uid、模板、載具、種類、類型、隊伍、玩家、任務名稱、建立與移除的時間、建立的位置，以及哪些元件無法讀取 |
| `objects` | 任務中有名稱的物件：佔領區域與機場（含位置與大小）、機場的輪廓（以點表示）、生成區域 |
| `objectives` | 戰鬥的目標，每個包含 `type`（`capture_zone`、`airfield`、`helipad`、`base`、`spawn`、`convoy_spawn`、`battle_area`、`bombing_target`、`exit_zone`、`kill_area`、`rearm_zone`）、`team`（回放中的 1 或 2，兩隊皆是則為空）、`name`（佔領區域為其字母，如 `A`）、`shape`（`sphere`、`cylinder`、`box`、`point`、`points`、`outline`），並附上 `position`、`radius` / `height` / `size` 與 `heading`、`source`（`replay` 或 `mission`），以及其他已知資訊（見[目標](objectives.md)） |
| `kills`、`hits`、`modulesDestroyed` | 雙方的名稱與載具；擊殺附上武器的英文名稱 |
| `weapons` | 每一枚火箭、飛彈、炸彈、魚雷、副油箱與拋棄的裝備：何時、於何處釋放（位置、姿態、速度）、由哪個單位釋放（300 公尺與 1.5 秒內最近的單位）、飛行取樣的數量、最後一次被看到的位置、何時被移除 |
| `explosions`、`flak` | `PlayExplosionVisual`（位置、方向、種類）與 `PlayFlakExplosionVisual`（位置） |
| `awards` | 錄製玩家的獎章（`TextStreak`：first_blood、連殺、挑戰計數） |
| `detections`、`unitStates` | 單位的 `UnitDetected` 配對；一則（0xF093）含有單位位置、姿態與速度的訊息，其含義不明 |
| `authorInstruments` | 錄製玩家的座艙數值（`ReplayCockpitParams`），依儀表編號，每秒至多一筆；`known` 為此回放送出的每個編號命名（名稱、單位、核對方式），`notNamed` 則為其餘 |
| `scoreboard` | 每位玩家的統計，每次變動時記錄一次（擊殺、死亡、助攻、分數、AI 擊殺、海上擊殺、區域、傷害、導彈規避、小隊），以及每個隊伍隨時間變化的分數與可能的票數（見[反射資料](aircraft.md#reflection-data)） |
| `economy` | 戰鬥的銀獅幣與研究點數（見[經濟](economy.md)）：總計、每位玩家、每個載具、倍率、勝方、核對結果 |
| `entityMessages` | 依類別編號分列的實體訊息（0x20）：數量、目標模板、大小 |
| `chat` | 每一行聊天 |
| `triggers`、`hints`、`missionProgress` | 任務腳本的動作（RunTriggerAction）、提示，以及進度訊息 |
| `camera` | 錄製玩家回放攝影機的欄位，每 0.25 秒依送出的內容記錄（表格中以一條軌跡呈現） |
| `projectileHitReplays` | 錄製玩家自己的命中與被命中，附武器與彈藥及其英文名稱 |
| `results` | 遊戲寫入的完整結算 blk |
| `counts` | 列、事件、生命、種類、取樣、依模板分列的實體、武器、已讀取與未讀取的封包、所見與未讀取的每個訊息 id、丟棄的取樣 |
| `trackBreaks` | 軌跡的每一次切斷，即單位速度不可能達到的步距：位置、距離、速度，以及最可能的原因 |
| `selfCheck` | [讀取回放的方式](how-it-reads.md)中列出的檢查，每次轉換都會計算；`stepSpeed` 依種類列出檢視器接合的軌跡相鄰列之間的速度（中位數、第 99 百分位、最高值，以及不可能快的步距，該數值必須為 0） |

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
