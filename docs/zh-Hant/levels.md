---
title: "關卡"
nav_order: 9
lang: "zh-Hant"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# 關卡（heat3d-wt-level） {#levels-heat3d-wt-level}

`heat3d-wt-level` 會把你自己 War Thunder 安裝目錄中的關卡，轉換為檢視器可用的 `.glb` 關卡，其座標系與回放表格相同。

## 逐步說明 {#step-by-step}

1. 列出你安裝目錄中的關卡：`heat3d-wt-level list`。它會為每個關卡印出一行：名稱、地形與其地圖，最後是數量。例如（虛構的關卡）：

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. 擷取一張、多張（可使用萬用字元）或全部：

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. 在檢視器的背景／關卡面板中，於該關卡的戰鬥之下，載入 `levels/<level>/<level>.glb`。

你寫出的關卡會留在你的電腦上：絕對不要公開發布（見[名詞與授權](terms.md)）。

## 選項 {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| 指令 / 選項 | 作用 |
|---|---|
| `list [--game FOLDER]` | 安裝目錄中的每個關卡 |
| `extract <levels...>` / `--all` | 指定的關卡（與 `list` 印出的名稱相同，可使用萬用字元），或全部關卡 |
| `-o`、`--out` | 輸出資料夾；每個關卡放在 `<out>/<level>/` 中 |
| `--game FOLDER` | War Thunder 資料夾（預設：透過 Steam 或啟動器找到；也可使用 `HEAT3D_WT_GAME`） |
| `--detail low/medium/high` | 戰車地圖上的地面取樣、地面顏色與物件預算（預設 `medium`） |
| `--max-object-triangles N` | 物件預算（預設：依 detail 而定） |
| `--max-grid N` | 每部分每邊的高度圖取樣數（預設 1024） |
| `--no-objects` | 不含建築、樹木與其他放置的物件 |
| `--no-generated` | 不含地表類別產生的物件（森林、城鎮） |
| `--no-terrain-colour` | 以戰術地圖貼上地面材質，而非地表類別 |
| `--no-texture` | 地面不貼材質 |
| `--skip-existing` | 略過已有 `.glb` 的關卡 |

## 會寫出什麼 {#what-is-written}

每個關卡會產生 `<out>/<level>/<level>.glb`、`<level>.json`（讀取到的內容、水面高度、地圖矩形、三角形數量、耗時），以及地圖的戰術地圖 `<level>_map.png`（空戰地圖）與 `<level>_tankmap.png`（戰車地圖）；地面地圖還會有 `<level>_terrain.png`，即疊在戰車地圖上的地面自身顏色。glb 會先寫入 `<level>.glb.part`，完成後再更名；寫入某張地圖時會持有 `<out>/<level>/.<level>.lock`，因此兩次擷取不會寫入同一張地圖（第二次會印出 `busy <level>`）。安裝目錄會透過 Steam 或啟動器的預設資料夾找到；若找不到，可用 `--game <folder>` 或 `HEAT3D_WT_GAME` 指定位置。

| 部分 | 內容 |
|---|---|
| `ground:<level>` | 地形高度圖（`HM2`）的格狀資料；在地面地圖上，為戰車地圖的中央（寬度的一半），以 `--detail` 的步距取樣，依地表類別、地面貼花與道路上色（`<level>_terrain.png`；若無法產生，則使用戰術地圖）；在沒有戰車地圖的地圖（空戰地圖）上，為整張高度圖，以一個步距取樣（`high` 時每邊 2048 個取樣，否則 1024），在空戰地圖的範圍內依地表類別上色（每邊 4096 像素，約 131 公里範圍內每像素約 32 公尺；若無法產生，則使用戰術地圖）；沒有高度圖的地圖，則為陸地網格 |
| `ground:<level> tank map` | 戰車地圖的其餘部分，步距較粗一級 |
| `ground:<level> heightmap surroundings` | 高度圖的其餘部分，步距更粗 |
| `ground:<level> land mesh` | 高度圖未覆蓋之處的陸地網格碰撞三角形（戰車地圖周圍，延伸到數十公里）；沒有高度圖的地圖上，則為地面，並依上述方式上色 |
| `ground:<level> outside the map` | 圖像未覆蓋的地面，不貼材質 |
| `water:<level>` | 位於地圖 `water_level` 高度、覆蓋所有地形的一個平面矩形：遊戲以一個平面繪製水體，水面下的低地即為海、湖或河床 |
| `water:<level> rivers` | 在有水體高度圖（`WHM`）的地圖上，覆蓋其範圍內各格的傾斜水面 |
| `structure:<level> buildings` | 每個非植物的放置物件：房屋、廢墟、牆、柵欄、橋、鐵軌、岩石、道具。固定的物件（`RIGz`），以及在戰車地圖上由地表類別產生的物件（城鎮街區、石頭）。每個物件依其渲染網格（牆、屋頂、窗口、樑）繪製，細節等級取決於三角形預算，並依其漫反射材質的平均顏色上色 |
| `structure:<level> trees` | 樹木與灌木，固定的與產生的（森林、樹籬）：在預算允許時使用其渲染網格，否則以樹幹與樹冠（針葉樹為圓錐）表示，顏色為樹葉本身的顏色，大小為樹木的實際尺寸 |

沒有渲染網格的物件會退回使用其碰撞形狀；沒有渲染網格的樹木則退回使用樹冠。頂點顏色（`COLOR_0`）保存的是 sRGB 編碼的數值，這正是 3DHeat 檢視器讀取它們的方式。

**座標**使用遊戲的公尺單位，並將 z 軸鏡像：glb 的 (x, y, z) = 遊戲的 (x, y, -z)。遊戲的世界是左手座標系（x 朝東、y 向上、z 朝北）；glTF 則是右手座標系。`heat3d-wt-replay` 保留遊戲的 z，並告訴檢視器將其鏡像，因此回放與其地圖的地圖會疊在一起，無需任何擺放步驟。JSON 會以遊戲的公尺單位給出每張戰術地圖的矩形，並以 glb 空間給出其角點，用於把 PNG 載入為地圖影像。

**細節。**`--detail low|medium|high`（預設 medium）會在戰車地圖上設定以下參數：

| | 戰車地圖中央 | 戰車地圖其餘部分 | 地面顏色 | 物件預算 | 每個物件最多三角形 | 保留的產生植物 |
|---|---|---|---|---|---|---|
| low | 每 4 個取樣 | 每 8 個 | 每像素 4 公尺 | 1.2 M | 1,500 | 樹木 35%，灌木 20% |
| medium | 每 2 個 | 每 4 個 | 每像素 2 公尺 | 3.5 M | 4,000 | 樹木 70%，灌木 50% |
| high | 每個取樣（多數地面地圖上為 2 公尺） | 每 2 個 | 每像素 1 公尺（每邊最多 4096 像素） | 4.5 M | 12,000 | 全部 |

兩個戰車地圖環帶的三角形數量分別限定在 0.3 M（low）、1 M（medium）與 3.7 M（high）：在高度圖比 2 公尺更細的地圖上，步距會倍增（先從外環開始），直到符合限制，因此這些地圖的步距也約為 2 公尺。

`high` 的地面地圖約有 800 萬個三角形（地面 350 萬，物件 450 萬），大小約 250 MB；`medium` 則約為 450 萬個。物件的 LOD 是遊戲本身在同一觀看距離下會繪製的那一級：總量符合預算的最短距離。小道具會先降到粗略的 LOD，大型建築最後才降級，依據製作者為每級 LOD 設定的範圍（JSON 中的 `lodDistance`）；超出預算的部分節省量，會分配回最大的物件。粗略的地面顏色（空戰地圖）會先把每個地表類別的平鋪材質平均到像素大小，以免平鋪產生干涉紋。若連最粗的 LOD 都無法符合，則節省最多的樹木會變成樹冠，然後最小的類型會被略去（`leftOut`）；不會有任何物件以方塊繪製（若有碰撞形狀，則為物件本身的碰撞形狀）。產生的物件會依類型以確定的方式稀疏化（`density`），每次執行都相同。`--max-object-triangles` 可覆寫預算；`--max-grid`（預設 1024）限制高度圖較粗部分的大小；`--no-objects` 會略去物件；`--no-generated` 略去產生的物件；`--no-terrain-colour` 以戰術地圖貼上地面材質；`--no-texture` 則讓地面不貼材質。

JSON 的 `parts.objects` 會列出各個實例（固定與產生的，依類型與地表類別），以及各自以哪一級 LOD 繪製的數量（`drawnAs`）、三角形、LOD 距離與耗時；`parts.heightmap.rings` 列出每個地面環帶的步距與三角形；`parts.terrainColour` 列出地表類別及其顏色、道路與地面貼花；`trianglesTotal`、`glbBytes` 與 `secondsBy` 為總計。

## 讀取了什麼，以及讀取的程度 {#what-is-read-and-how-well}

| 部分 | 狀態 |
|---|---|
| 關卡二進位檔（`levels/<level>.bin`，`DBLD` 3x64）：區塊表 | 每張地圖都已核對 |
| 高度圖（`HM2`，版本 0-2；版本 2 是區塊中的 8 位元數值，Oodle 或 zstd 區塊） | 每張高度圖為版本 2 且使用 Oodle 區塊的地圖；已以目視對照戰術地圖核對（河流、山谷、海岸與城鎮都吻合） |
| 陸地網格碰撞（`lmap`，其 `LTdump` 陸地光線追蹤器） | 在地圖有此資料的地方讀取（Oodle 壓縮）。它是遊戲的碰撞表面，而非渲染網格，因此在平坦的陸地上較粗略 |
| 地面顏色（`lmap` 的地表類別與權重圖、`LMp2` 物理圖、`hspl` 樣條） | 地表類別的顏色圖與細節材質（其平均顏色），依權重圖加權；有索引的地表類別的 1 公尺生態區索引；物理圖中道路與地面貼花的形狀，以其樣條或材質的材質顏色上色；陡坡上的懸崖。已對照戰車地圖核對：道路、城鎮、湖泊、森林帶與岩層都吻合。War Thunder 自己的地形著色器的顏色公式不在公開的原始碼中；因此採用引擎公開的版本（daNetGame），其結果比戰術地圖更飽和 |
| 水面高度 | 取自 `aces.vromfs.bin` 中地圖 BLK 的 `water_level`（沒有時為 0） |
| 水體高度圖（`WHM`：平坦格子與 130x130 頁的 16 位元高度） | 在地圖有此資料的地方讀取；其河流會隨地面傾斜 |
| 戰術地圖 | 來自 `content/base/res/locations_maps.dxp.bin`，依 BLK 的 `mapCoord0/1` 與 `tankMapCoord0/1` 放置；圖像的上方為北方 |
| 放置的物件（`RIGz`：渲染實例產生器的固定實例） | 每個實例，為 3x4 的 16 位元數值矩陣，部分地圖為 32 位元（格子的位元組數決定）；在已核對的地圖上，每個格子的每個位元組都已計入 |
| 產生的物件（`RIGz` 的地表類別遮罩與 `LandClass` 資源） | 遊戲的產生器，已移植：以相同的隨機數、相同的順序嘗試相同的位置，套用地表類別與排除遮罩，決定每個位置的物件、旋轉、縮放與高度偏移；平鋪（城鎮街區）與種植（森林、灌木、田地）的實體。僅在戰車地圖上產生。近似之處：地面高度與法線（取自高度圖；遊戲會追蹤光線）、遊戲在執行時登錄的排除方塊，以及樹木的偏航角（遊戲會將其對齊到替身的旋轉調色盤）。 |
| 渲染網格（`content/*/res/*.grp` 中的 `RendInst` 資源，材質在 `riDesc.bin`） | 每一級 LOD 的頂點與三角形（浮點位置；16 或 32 位元索引，一般或 meshoptimizer 壓縮），以及每個元素的材質。貼花與替身告示牌元素會略去；透明的元素（玻璃）則保留 |
| 物件顏色 | 每個材質取其漫反射材質小型 mip 的平均值（樹葉依 alpha 加權），來自安裝目錄的材質包：大多數著色器用 t0，若 t0 是覆蓋或遮罩，則用第一個細節漫反射。每個材質一個顏色：物件上不貼材質 |
| 碰撞形狀（`<object>_collision`） | 串流版本 3 的碰撞資源，用於沒有渲染網格的物件。只繪製遊戲的光線所擊中的部分（`TRACEABLE` 節點），而方塊、球體與膠囊只在資源沒有網格時才繪製：其餘都是粗略的物理替身，會以方塊形式環繞物件顯示 |
| 導航網格（`Lnav`）、渲染的陸地網格、草、`spgz`、`stbl`、`d2co` | 未讀取 |

地圖使用 Oodle 壓縮，而 Oodle 是專屬的。遊戲隨附一份複本：`<War Thunder>\win-arm64ec\oo2core_9_win64.dll`（一般的 x64 版本），載入的就是它；`HEAT3D_OODLE=<dll 或資料夾>` 可指向其他位置。本儲存庫不包含 Oodle。

## 格式與其說明文件 {#formats-and-where-they-are-documented}

Gaijin 以 BSD 3-Clause 授權公開了 Dagor Engine 的原始碼（github.com/GaijinEntertainment/DagorEngine）。此處的讀取器是依據它編寫的；沒有任何遊戲程式碼經過反編譯。每個模組都註明它所依循的原始碼檔案：

- `vromfs.py`：`*.vromfs.bin`（標頭 `VRFs`/`VRFx`，一個 zstd 本體，其前後各 16 個位元組以固定金鑰進行 XOR，一張名稱表與一張偏移表：`osApiWrappers/dag_vromfs.h`、`ioSys/vromfsLoad.cpp`、`supp/dag_zstdObfuscate.h`），以及二進位 BLK（格式 1-5，使用封存的共用名稱對應 `\xff?nm` 與 zstd 字典：`ioSys/dataBlock/blk_serialize.cpp`、`blk_parser.cpp`、`blk_zstd.cpp`）。
- `dxp.py`：材質包 `DxP2`（`lib3d/texPackMgr2.cpp`）與 DDSx 標頭（`sharedInclude/3d/ddsxTex.h`）；DXT1/DXT5/BC7 由 Pillow 解碼。
- `dagorlevel.py`：關卡二進位檔（`scene/loadLevel.cpp`）、高度圖（`heightmap/heightmapPhysHandler.cpp`、`heightMapLand/compressedHeightmap.cpp`）、陸地光線追蹤器（`landMesh/lmeshManager.cpp`、`landMesh/landRayTracerSoA4.cpp`）與水體高度圖（`fftWater/fftWater.cpp`）。
- `rigen.py`：放置的物件（`rendInst/riGen/riGenData.h`、`rendInst/rendInstGen.cpp`、`rendInst/riGen/genObjUtil.h`）。
- `landgen.py`：產生的物件（`rendInst/rendInstGenLand.cpp`、`riGen/landClassData.h`、`riGen/genObjByMask.h`、`riGen/genObjByDensGridMask.h`、`riGen/genObjUtil.h`、`riGen/riGenData.h`、`riGen/multiPointData.h`、`riGen/riRotationPalette.h`、`rendInstGen.cpp`（`create`、`precomputeCell`、`generateCell`）、`gameMath/objgenPrng.h`、`util/dag_roHugeHierBitMap2d.h`、`util/dag_hierBitMap2d.h`、`ioSys/dag_roDataBlock.h`、`ioSys/roDataBlk.cpp`、`gameRes/grpData.h`）。
- `rendinst.py`：渲染實例（`shaders/rendInstRes.cpp`、`shaders/dag_rendInstRes.h`、`shaders/matVdataLoad.cpp`、`shaders/shaderMesh.cpp`、`shaders/dag_shaderMesh.h`、`shaders/dag_shaderCommon.h`、`drv/3d/dag_consts_base.h`、`gameRes/gameResDescBin.cpp`），以及 meshoptimizer 的索引編解碼器（`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`，MIT 授權）。
- `terrain.py`：地面顏色（`landMesh/lmeshManager.cpp`、`lmeshLandClasses.cpp`、`lmeshWeightAtlas*.cpp`、`lmeshRenderer.cpp`、`landMesh/shaders/land_weight_atlas.hlsli`、`land_weight_inc.dshl`、`biomes.dshl`、`daNetGame/shaders/land_aces.dshl`、`make_clipmap.dshl`、`physMap/physMapLoad.cpp`、`baseUtil/treeBitmap.cpp`、`levelSplines/levelSplines.cpp`）。
- `collision.py`：資源包（`gameRes/grpData.h`）與碰撞資源（`sharedInclude/gameRes/collResStream.h`、`gameRes/collisionGameResLoad.cpp`），其三角形以四邊形 BVH 儲存（`daBVH/bvhIO.cpp`、`daBVH/dag_swBLAS_leaf.h`、`swBLASLeafDefs.hlsli`）。

wt_ext_cli（Apache-2.0）也會讀取同樣的封存檔；這裡不需要、也不使用它。

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
