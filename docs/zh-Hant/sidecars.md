---
title: "附屬檔案與完整性"
nav_order: 8
lang: "zh-Hant"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# 附屬檔案與完整性 {#sidecars-and-completeness}

回放中沒有任何東西會被丟棄。轉換器讀取的內容會放入表格與對戰文件；其餘一切都會完整保留在表格旁的三個附屬檔案中（位於 `.3dheat` 檔案內，或使用 `--loose` 時為獨立檔案）。這是所有 3DHeat 轉換器共同遵守的規則：[轉換器保留一切](https://holdi601.github.io/3DHeat/converters.html)。

## 附屬檔案 {#the-sidecars}

- `<match>.messages.parquet`：送往單位的每則訊息（時間、訊息 id 與名稱、uid、eid、模板、載具、以十六進位表示的 id 欄位、`decoded`（讀取到的內容，以 JSON 表示）、承載資料）、每個複製元件的數值（`name` 為元件，`fields` 為其數值）、每則實體訊息（附其實體與類別編號）、每個複製物件（`ReflectionData <kind>/<index>`，其欄位以十六進位表示），以及此處任何讀取器都不處理的每個封包，完整保存。
- `<match>.objectives.parquet`：隨時間變化的佔領區域，伺服器每送出一次變化就有一列：`time`、`event`（`state`、`progress`、`captured`、`neutralised`）、`zone`（其字母）、`zoneId`、`object`、`owner`（0 為無、1、2）、`progress`（-100 到 100，正值朝向隊伍 2）、區域的 `x`、`y`、`z`，以及該物件的所有 `fields`（以十六進位表示；見[目標](objectives.md)）。
- `<match>.flight.parquet`：每架飛機的每一筆飛行模型紀錄，完整保存（其位元，以及 `phase`：其開始時所在的第一個位元組的位元），附帶其速度、14 個操縱半位元組（`control1-3`、`throttle`）、其引擎及其狀態、加力燃燒室與狀況，以及每種武器的發數（`ammo`；`numbers` 為完整清單）。其他飛機的數值為最後一次更新時的值。

## 計數所保證的內容 {#what-the-counts-guarantee}

對戰文件中的 `counts` 說明回放包含了什麼，以及它們的去向：

| 鍵 | 內容 |
|---|---|
| `packets`、`unreadPackets` | 遇到的每種封包類型，以及沒有任何讀取器處理的封包（完整保存於訊息附屬檔案中） |
| `messageIds`、`messageIdsNotRead` | 遇到的每個訊息 id 及其次數，以及只保留、未讀取的訊息 |
| `replicatedComponents`、`replicatedNotRead` | 已讀取的元件數值，以及只保留的元件數值 |
| `entities`、`entityTemplates`、`entityMessages` | 實體串流所建立與送出的內容 |
| `droppedSamples` | 刻意略去的取樣（實體消失後的地面單位殘骸），依原因列出 |

除此之外沒有其他內容被略去：回放中的每一項，要麼讀入表格或對戰文件，要麼完整保存在附屬檔案中。對戰文件中的 `selfCheck` 保存了已讀取內容的檢查結果（[讀取回放的方式](how-it-reads.md)）。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
