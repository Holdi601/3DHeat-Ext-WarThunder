---
title: "轉換回放"
nav_order: 4
lang: zh-Hant
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# 轉換回放 {#converting-replays}

輸出：預設每場戰鬥是一個 `.3dheat` 檔案，使用 `--loose` 時則是分開的多個檔案。

## 逐步說明 {#step-by-step}

1. **開啟回放功能。**當遊戲選項中開啟回放儲存時，War Thunder 會把客戶端回放存在遊戲的 `Replays` 資料夾中，例如 `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`。從遊戲的回放頁面儲存的伺服器回放（一個含有 `0000.wrpl`、`0001.wrpl`、... 的 zip 檔）也可以轉換。
2. **開啟終端機**，位於可以存放結果的資料夾中（[開始之前](before-you-start.md)）。
3. **轉換：**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # 檔案、資料夾，或兩者皆可
   heat3d-wt-replay battle.zip -o out              # 伺服器回放的 zip 檔
   heat3d-wt-replay a.wrpl -o out --loose          # 分開的檔案，而非一個 .3dheat
   ```

   `out` 會建立在終端機所在的資料夾中。
4. **閱讀輸出內容。**你會看到每場戰鬥一行。
5. **開啟結果：**在 3DHeat 檢視器中載入 `out/<map>/<match>.3dheat`（[載入檔案](https://holdi601.github.io/3DHeat/container.html#loading-one)）。

![對合成回放執行的結果：一個 .3dheat、--loose、一個損壞的檔案、一個空資料夾](../assets/img/convert.svg)

圖片是對測試程式以程式碼建立的回放所做的執行結果（沒有真實回放，也沒有安裝）：

- `ok <file>`：一場戰鬥已轉換（使用 `--loose` 時為 `ok <table> <match document>`）；
- `failed <file>: <why>`：無法讀取的檔案（結束狀態為 1；其餘檔案仍會轉換）；
- `no .wrpl files given`：沒有可轉換的內容（結束狀態為 2）；
- `note: ...`：例如找不到用來命名載具的 War Thunder 安裝目錄。

## 選項 {#options}

| 選項 | 預設 | 作用 |
|---|---|---|
| `replays`（一個或多個） | - | `.wrpl` 檔案、其中的資料夾（只限該資料夾本身，不含子資料夾），或它們的 zip 檔（伺服器回放：其 `.wrpl` 分段會解壓到暫存資料夾） |
| `-o`、`--out` | 必填 | 寫入的位置：其中會為每張地圖建立一個資料夾 |
| `--game FOLDER` | 自動找到 | War Thunder 的資料夾，其文字用來命名載具、武器與彈藥，其價格表用來計算[經濟](economy.md)；也可使用 `HEAT3D_WT_GAME` |
| `--no-smoothing` | 關閉 | 保留其他單位的航位推算與收到的取樣，與回放中的原樣相同（[航位推算](aircraft.md#dead-reckoning-and-the-smoother)） |
| `--container` | 開啟 | 將每場戰鬥打包成一個 `.3dheat` 檔案 |
| `--loose` | 關閉 | 將每場戰鬥保留為分開的檔案（表格、對應文件、附屬檔案） |
| `--version` | - | 印出 `heat3d-wt-replay <version>` 後停止 |
| `-h`、`--help` | - | 印出選項後停止 |

同一場戰鬥若再次轉換，會重新寫入。程式印出的選項：[指令參考](../cli-reference.md)。

## 哪些檔案屬於同一場戰鬥 {#which-files-are-one-battle}

每場戰鬥會成為一個檔案，
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`。AB、RB 與 SB 是遊戲對競技、實況與模擬戰鬥的簡寫；`<mode>` 是遊戲以任務的鍵名所記的模式（`Conq4` 為征服 #4、`Dom` 為佔領、`Bttl` 為戰鬥；見[戰鬥模式](ground.md#battle-mode)）；回放中沒有命名的部分會被省略。伺服器回放的各分段（`0000.wrpl`、`0001.wrpl`、...）會一起讀取，視為同一場戰鬥；客戶端回放與同一場戰鬥的伺服器分段則是兩份紀錄，會保持為兩個。

## 結束狀態 {#exit-status}

所有戰鬥都轉換成功時為 `0`；任何一場失敗時為 `1`（其餘仍會轉換）；引數中找不到任何回放檔案時為 `2`。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
