---
title: "名詞與授權"
nav_order: 16
lang: "zh-Hant"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# 條款與授權 {#terms-and-licence}

## 條款 {#the-terms}

Gaijin 的服務條款（2026-08-17 更新）、使用者授權條款（附件 2）：
3.2.2 "modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the Game(s)"，3.2.9 "mine or collect any data from the Game(s) that is not intended to be publicly displayed"；1.2 "are not permitted to store, download, modify, or otherwise use any part of the Game(s)"，客戶端除外。將你自己副本的地圖檔案讀入本機 3D 檢視，是使用者在知情的情況下自行做出的決定。寫出的地圖會留在你的電腦上：**絕對不要公開發布**，而且這裡不附帶任何遊戲資料。

## 來源 {#sources}

這裡所有的程式碼都是為本專案編寫的；沒有任何程式碼是從其他解析器複製而來。它對格式的了解來自：

- Gaijin 的 Dagor Engine 原始碼（github.com/GaijinEntertainment/DagorEngine，BSD 3-Clause）：`prog/engine/daECS/net/network.cpp`、`connection.cpp`、`object.cpp`、`serialize.cpp`、`compression.h`，以及 `prog/engine/daECS/core/baseIo.cpp`、`componentTypes.cpp`，用於實體串流（`ecs.py`）；`net/message.cpp`（`MessageClass::initImpl`），用於實體訊息如何為其類別編號。元件與類型名稱是以 FNV-1a 雜湊值與遊戲自身封存檔中的字詞比對；`ecs.py` 列出找到的名稱。
- 同一份原始碼中的 `prog/dagorInclude/daNet/mpi.h`、`prog/engine/daNet/ext/mpi.cpp` 與 `daNet/bitStream.h`：訊息如何指定其對象的物件（`wrpl.read_mpi`）。
- ShioUmiusi/WTACRP（MIT）：`docs/REPLAY-FORMAT.md`、`docs/REPLAY-DECODE.md`、`docs/REPLAY-DECODE-ECS.md`、`docs/QUICK-REF.md`，以及其自己的解析器 `web/wrpl-parse.js`，用於查閱飛行模型、地面同步、飛行中武器、含 id 欄位的訊息、玩家槽位、座艙數值與二進位 blk 的位元格式。WTACRP 將 maxsupermanhd/wrpl-inspector、wt_blk 與 wrpl-acmi（AGPL-3.0）列為其參考；這些程式碼並未在此閱讀。
- 作者自己的回放，以檔案形式讀取：2025 年的差異（飛行模型較舊的格式、沒有旗標位元組的聊天、zlib）、地面姿態、壓縮高度的偏移、武器的釋放點，以及座艙儀表，都是在這些回放上找出來的。

## 測試 {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # 也會核對公開的 2025 範例回放
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # 步距、身分、AI 旗標、橫滾符號、平滑器、名稱
```

單元測試從不讀取安裝目錄（已設定 `HEAT3D_WT_NO_NAMES`）；使用你自己回放的測試，則會從你的安裝目錄讀取名稱。

測試以程式碼建立回放（`tests/synth.py`：標頭、封包、結算、實體串流、飛行中的武器），其格式即讀取器所記載的格式；儲存庫中沒有任何回放。

## 授權 {#licence}

MIT，見 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE)。使用 pyarrow（Apache-2.0）、numpy（BSD-3-Clause）、zstandard（BSD-3-Clause）與 Pillow（MIT-CMU）。地圖讀取器是依據 Dagor Engine 的原始碼編寫的，版權為 (c) 2023 Gaijin Entertainment，採 BSD 3-Clause 授權；這裡沒有複製其中的任何程式碼，而使用的格式常數（vromfs 的 XOR 金鑰、高度範圍的網格偏移）則會在出現之處註明出處。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
