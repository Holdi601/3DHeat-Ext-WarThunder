---
title: "目標"
nav_order: 15
lang: zh-Hant
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# 目標 {#objectives}

對戰文件中的 `objectives` 列出這場戰鬥爭奪的目標，來源有兩個（`source`）：

- **回放**（`replay`）：回放的 0xD039 所命名的任務物件（佔領區域 `cz_circle_NN`、機場、直升機停機坪、基地），依種類 3 的 0xF02D 所複製的物件目前的位置放置——佔領區域一開始位於其模板的位置，並在戰鬥開始時移到本模式的區域（`moved`）。種類 3 的編號依 0xD039 的順序排列；每個未被移動的物件都正好位於 0xD039 所給的位置，這可以核對順序。佔領區域會取得其所在位置的任務範圍形狀與半徑（`area`，在 2 公尺內），其字母則取自它自己的索引（種類 5 欄位 69：0 = A）；字母的順序來自回放，未與遊戲的地圖核對。
- **任務**（`mission`）：你安裝目錄中 `mis.vromfs.bin` 裡的任務檔 `<mission>.blk`，以及它所匯入的模板（僅在轉換時讀取）：其區域依名稱分類——生成點（生成點中編號的各點 `..._spawnareaNN` 合併為一個 `points` 生成點）、戰鬥區域、轟炸目標（`bomb_zone`）、車隊生成點（`road_NN_spawn`）、離開與擊殺區域。同一地圖其他模式的區域（`conq_`、`dom_`、`bttl_` 等）會被略去；對於 `_arcade`、`_realistic`、`_hardcore` 等變體，則採用本場戰鬥自己的版本（RB 取 `_realistic`，否則取 `_hardcore`，與任務腳本的做法相同）；任務簡報標記、防空砲位置，以及超過 5 公里寬的區域（生成點分散其中的區域）也會被略去。每個生成點會說明有多少位玩家的航跡是從它開始的（`used`、`usedByTeam`）。任務可能會隨機交換雙方的陣營（`randomSpawnTeams`）：若生成點顯示回放中的隊伍是反過來的，則每個 `team` 都會被交換，而名稱所屬的陣營則保留為 `missionTeam`。車隊路線不在所讀取的任務路徑點中；只提供車隊出現的位置。

隨時間變化的佔領區域保存在附屬檔案 `<match>.objectives.parquet` 中：即種類 5 的複製物件，每個區域一個——欄位 2 為其擁有者（0、1、2），欄位 67 為其佔領進度，是一個從 -100 到 100 的帶正負號位元組（正值朝向隊伍 2），欄位 69 為其索引。已在征服與佔領戰鬥的伺服器地面回放上核對（`selfCheck.objectives`）：每次擁有者變更，都會伴隨同一時刻（1.5 秒內）捕獲隊伍的某位玩家在計分板上獲得一次 `captureZone`，且該隊有一個存活的地面單位位於區域內；每場戰鬥的生成點都只顯示回放中隊伍的一種方向（常與任務的 `t1_` / `t2_` 相反）。

## 場景單位：電車與鐵路車廂 {#scene-units-trams-and-rail-wagons}

地圖可以放置它自己的單位：伺服器回放中的 `unit_loader+rail_wagon` 實體，是地圖場景檔案中的電車（`aces.vromfs.bin` 中的 `gamedata/scenes/<level>_objects.blk`：`setting__unit_class`、其變換與 `setting__isDead`）。這些實體沒有可讀取的 uid，因此，一條沒有單位實體的地面航跡，若其第一個取樣位於某個場景單位 2 公尺內，就是該單位：其類別為 `Vehicle`，種類 `train`，類型為 `tram`、`locomotive` 或 `wagon`，沒有隊伍；場景中放置為已死亡的單位（例如燒毀的電車），從第一列起即為殘骸（`alive` 為 0）。遊戲中沒有它們的英文名稱；`VehicleName` 是其 id 拆成單字後的結果（"Railway tram A"）。它們的位置不會晃動：幾乎都從不移動（每個取樣在位元層級都完全相同）。不論如何，回放每秒約送出十次它們的取樣，因此只保留真正移動它們的取樣（0.05 公尺或 0.1 度），且每 10 秒保留一個（`selfCheck.sceneUnits` 會計算被丟棄的取樣數）。在此之前，它們是名為 `uid 8` 且沒有載具的航跡。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
