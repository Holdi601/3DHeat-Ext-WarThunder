---
title: レベル（heat3d-wt-level）
nav_order: 9
lang: "ja"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# レベル（heat3d-wt-level） {#levels-heat3d-wt-level}

`heat3d-wt-level` は、お使いの War Thunder のインストールにあるレベルを、ビューアのための `.glb` のレベルに変えます。リプレイのテーブルと同じ座標系です。

## 手順 {#step-by-step}

1. インストールのレベルを一覧にします: `heat3d-wt-level list`。レベルごとに 1 行が表示されます: その名前、地形、マップ、そして最後に数。たとえば次のとおりです（架空のレベル）:

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. 1 つ、いくつか（ワイルドカード可）、またはすべてを取り出します:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```
3. `levels/<level>/<level>.glb` を、そのマップの戦闘の下にあるビューアの「背景/レベル」パネルに読み込みます。

書き出したレベルはお使いのマシンに残ります。決して公開しないでください（[利用条件とライセンス](terms.md) を参照）。

## オプション {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| コマンド / オプション | 働き |
|---|---|
| `list [--game FOLDER]` | インストールにあるすべてのレベル |
| `extract <levels...>` / `--all` | 名指しされたレベル（`list` が表示するとおり。ワイルドカード可）、またはすべてのレベル |
| `-o`、`--out` | 出力フォルダー。各レベルは `<out>/<level>/` に入る |
| `--game FOLDER` | War Thunder のフォルダー（既定: Steam またはランチャーから検出。`HEAT3D_WT_GAME` でも指定可） |
| `--detail low/medium/high` | タンクマップの上の地表のサンプリング、地表の色、オブジェクトの予算（既定は `medium`） |
| `--max-object-triangles N` | オブジェクトの予算（既定: 詳細度によるもの） |
| `--max-grid N` | 部分ごとの、高さマップのサンプルの一辺の数（既定 1024） |
| `--no-objects` | 建物、木、そのほか配置されたオブジェクトを除く |
| `--no-generated` | 地表の種類が生成するオブジェクト（森、町）を除く |
| `--no-terrain-colour` | 地表は地表の種類ではなく、戦術マップで着色する |
| `--no-texture` | 地表にテクスチャを付けない |
| `--skip-existing` | `.glb` がすでにあるレベルは残す |

## 書き出されるもの {#what-is-written}

各レベルは `<out>/<level>/<level>.glb`、`<level>.json`（読み取った内容、水面の高さ、マップの矩形、三角形の数、所要時間）、そしてレベルの戦術マップ `<level>_map.png`（空のマップ）と `<level>_tankmap.png` になります。地上のマップには `<level>_terrain.png` もあります。これは地表自身の色を、タンクマップに重ねたものです。glb は `<level>.glb.part` に書かれ、完成すると名前が変わります。レベルが書かれている間、`<out>/<level>/.<level>.lock` が保持されるので、2 つの取り出しが同じレベルに書き込むことはありません（2 つ目は `busy <level>` を表示します）。インストールは、Steam またはランチャーの標準のフォルダーから見つけられます。そうでない場合は、`--game <フォルダー>` または `HEAT3D_WT_GAME` で指定します。

| 部分 | 内容 |
|---|---|
| `ground:<level>` | 地形の高さマップ（`HM2`）をグリッドとして。地上のマップでは、タンクマップの中央（その幅の半分）を `--detail` の刻みで、地表の種類、地表のデカール、道路で着色したもの（`<level>_terrain.png`。それができない場合は戦術マップ）。タンクマップのないマップ（空のマップ）では、高さマップ全体を 1 刻みで（`high` では一辺 2048 サンプル、それ以外は 1024）、空のマップの範囲に対して地表の種類で着色したもの（一辺 4096 ピクセル、約 131 km に対して 1 ピクセルあたり約 32 m。それができない場合は戦術マップ）。高さマップのないレベルでは、陸地のメッシュ |
| `ground:<level> tank map` | タンクマップの残り。1 刻み粗いもの |
| `ground:<level> heightmap surroundings` | 高さマップの残り。さらに粗いもの |
| `ground:<level> land mesh` | 高さマップが届かない部分の、陸地のメッシュの衝突三角形（タンクマップの周り。数十 km まで）。高さマップのないレベルでは、上のように着色された地面 |
| `ground:<level> outside the map` | 画像がカバーしていない地面。テクスチャなし |
| `water:<level>` | すべての地形の上に、レベルの `water_level` にある 1 つの平らな矩形。ゲームは水を 1 つの面として描くので、その下の低い地面は海、湖、または川床です |
| `water:<level> rivers` | 水の高さマップ（`WHM`）のあるレベルでは、それが覆うセルの上の、傾斜した水面 |
| `structure:<level> buildings` | 植物ではない、配置されたすべてのオブジェクト: 家、廃墟、壁、柵、橋、線路、岩、小道具。固定のもの（`RIGz`）と、タンクマップの上では地表の種類が生成するもの（町のブロック、石）。それぞれ描画メッシュ（壁、屋根、窓の開口、梁）で描かれ、三角形の予算が許す LOD で、拡散テクスチャの平均による素材ごとの色つき |
| `structure:<level> trees` | 木と低木。固定のものと生成されるもの（森、生垣）。描画メッシュは予算が許すところで使い、そうでなければ幹と樹冠（針葉樹は円錐）を、木自身の葉の色で、本来の大きさのまま |

描画メッシュのないオブジェクトは、衝突の形状にフォールバックします。描画メッシュのない木は樹冠にフォールバックします。頂点の色（`COLOR_0`）は sRGB で符号化された値を持ち、3DHeat ビューアはそのように読みます。

**座標** は、ゲームのメートル単位で、z は反転しています: glb の (x, y, z) = ゲームの (x, y, −z)。ゲームの世界は左手系（x が東、y が上、z が北）で、glTF は右手系です。`heat3d-wt-replay` はゲームの z をそのまま保ち、ビューアにそれを反転するよう伝えるので、リプレイとそのマップのレベルは、配置の手順なしにぴったり重なります。JSON は、それぞれの戦術マップの矩形を、ゲームのメートル単位で、そして角を glb の空間で与えるので、PNG をマップの画像として読み込めます。

**詳細度。** `--detail low|medium|high`（既定は medium）は、タンクマップの上で次のように設定します:

| | タンクマップの中央 | タンクマップの残り | 地表の色 | オブジェクトの予算 | オブジェクトごとの最大三角形 | 生成された植物の残す割合 |
|---|---|---|---|---|---|---|
| low | 4 サンプルごと | 8 サンプルごと | 1 ピクセルあたり 4 m | 1.2 M | 1,500 | 木 35 %、低木 20 % |
| medium | 2 サンプルごと | 4 サンプルごと | 2 m | 3.5 M | 4,000 | 木 70 %、低木 50 % |
| high | サンプルごと（ほとんどの地上のマップで 2 m） | 2 サンプルごと | 1 m（一辺最大 4096 ピクセル） | 4.5 M | 12,000 | すべて |

2 つのタンクマップのリングは、三角形を低（0.3 M）、中（1 M）、高（3.7 M）に抑えます。高さマップが 2 m より細かいマップでは、刻みが（外側のリングが最初に）倍になり、収まるまで続きます。そのため、それらも約 2 m になります。

`high` での地上のマップは約 800 万の三角形（地表 3.5 M、オブジェクト 4.5 M）と 250 MB になります。`medium` では約 450 万です。オブジェクトの LOD は、ゲームが 1 つの見る距離から描くであろう LOD です。合計が予算に収まる最も短いもの: 小さな小道具は最初に粗い LOD になり、大きな建物は最後になります。それぞれの作り手が LOD に与えた範囲（JSON の `lodDistance`）によります。予算を超えて節約されるものは、最も大きなオブジェクトに戻されます。粗い地表の色（空のマップ）は、各地表の種類のタイルのテクスチャを、まずピクセルの大きさまで平均化するので、タイルがモアレになりません。最も粗い LOD でも収まらない場合は、最もよく節約できる木が樹冠になり、そのあと最も小さい種類が除かれます（`leftOut`）。どのオブジェクトも箱として描かれません（衝突の形状があれば、それはそのオブジェクト自身のものです）。生成されたオブジェクトは、種類ごとの `density` に従って決定的に間引かれるので、毎回同じものが残ります。`--max-object-triangles` は予算を上書きし、`--max-grid`（既定 1024）は高さマップの粗い部分を制限し、`--no-objects` はオブジェクトを除き、`--no-generated` は生成されたものを除き、`--no-terrain-colour` は地表を戦術マップでテクスチャ付けし、`--no-texture` はテクスチャを付けないままにします。

JSON の `parts.objects` は、インスタンス（固定と生成、種類と地表の種類別）、どの LOD で何個描かれたか（`drawnAs`）、三角形、LOD の距離、そして秒数を挙げます。`parts.heightmap.rings` は、各地表のリングの刻みと三角形。`parts.terrainColour` は地表の種類とその色、道路、地表のデカール。`trianglesTotal`、`glbBytes`、`secondsBy` は合計です。

## 読み取った内容と、その精度 {#what-is-read-and-how-well}

| 部分 | 状態 |
|---|---|
| レベルのバイナリ（`levels/<level>.bin`、`DBLD` 3x64）: ブロックの表 | すべてのレベルを確認 |
| 高さマップ（`HM2`、バージョン 0〜2。バージョン 2 は、ブロック内の 8 ビットの値で、Oodle または zstd のチャンク） | 高さマップがバージョン 2 で Oodle のチャンクのあるすべてのレベル。戦術マップと目視で照合（川、谷、海岸、町が合う） |
| 陸地のメッシュの衝突（`lmap`、その `LTdump` の陸地の光線追跡） | レベルが持つところで読む（Oodle で詰められたもの）。描画されるメッシュではなく、ゲームの衝突の面なので、平らな地面では粗い |
| 地表の色（`lmap` の地表の種類と重みマップ、`LMp2` の物理マップ、`hspl` のスプライン） | 地表の種類の色のマップと詳細テクスチャ（それらの平均の色）を、重みマップで重み付けしたもの。インデックスされた地表の種類の 1 m のバイオームのインデックス。物理マップの道路とデカールの形を、そのスプラインまたは素材のテクスチャの色で。急斜面の崖。タンクマップと照合: 道路、町、湖、森の帯、岩の露頭が合う。War Thunder 自身の地形のシェーダーの色の式は、公開されたソースにはありません。エンジンの公開された式（daNetGame）を使っており、それは戦術マップより彩度が高く出ます |
| 水面の高さ | `aces.vromfs.bin` にあるレベルの BLK の `water_level`（ないものは 0） |
| 水の高さマップ（`WHM`: 平らなセルのグリッドと、16 ビットの高さの 130x130 のページ） | 持つレベルで読む。その川は地面に沿って傾斜する |
| 戦術マップ | `content/base/res/locations_maps.dxp.bin` から。BLK の `mapCoord0/1` と `tankMapCoord0/1` で配置。画像の上は北 |
| 配置されたオブジェクト（`RIGz`: 描画インスタンスの生成器の固定インスタンス） | すべてのインスタンス。3x4 の行列で、16 ビットの値、または一部のレベルでは 32 ビット（セルのバイト数で決まる）。確認したレベルでは、すべてのセルのすべてのバイトが説明されている |
| 生成されたオブジェクト（`RIGz` の地表の種類のマスクと `LandClass` のリソース） | ゲームの生成器を移植したもの。同じ場所を同じ順番で、同じ乱数で試し、地表の種類と除外のマスク、各地点で選ばれるオブジェクト、その回転、尺度、高さのずれ。タイル状（町のブロック）と植えられたもの（森、低木、畑）のエンティティ。タンクマップの上でだけ生成。近似している部分: 地面の高さと法線（高さマップから。ゲームは光線を追う）、ゲームが実行時に登録する除外のボックス、木の yaw（ゲームはそれをインポスターの回転のパレットに合わせる） |
| 描画メッシュ（`content/*/res/*.grp` の `RendInst` リソース。素材は `riDesc.bin`） | すべての LOD の頂点と三角形（浮動小数点の位置、16 ビットまたは 32 ビットのインデックス。そのままか、meshoptimizer で詰められたもの）、各要素の素材。デカールとインポスターの板の要素は除かれ、透明なもの（ガラス）は残る |
| オブジェクトの色 | 素材ごとに、その拡散テクスチャの小さいミップの平均（葉はアルファで重み付け）。インストールのテクスチャパックから。ほとんどのシェーダーは t0、t0 がオーバーレイまたはマスクの場合は最初の詳細拡散。素材ごとに 1 色: オブジェクトにテクスチャはなし |
| 衝突の形状（`<object>_collision`） | ストリームのバージョン 3 の衝突リソース。描画メッシュのないオブジェクトに使う。ゲームの光線が当たるもの（`TRACEABLE` のノード）だけを描き、箱、球、カプセルは、リソースにメッシュがない場合だけ。そのほかは粗い物理の代用品で、オブジェクトの周りの立方体として見えてしまうため使わない |
| ナビゲーションメッシュ（`Lnav`）、描画される陸地のメッシュ、草、`spgz`、`stbl`、`d2co` | 読まない |

レベルは Oodle で圧縮されています。Oodle は独自仕様です。ゲームはそのコピーを `<War Thunder>\win-arm64ec\oo2core_9_win64.dll`（普通の x64 版）として同梱しており、それが読み込まれます。`HEAT3D_OODLE=<dll またはフォルダー>` で別の場所を指定できます。Oodle はここには含まれていません。

## フォーマットと、その文書 {#formats-and-where-they-are-documented}

Gaijin は Dagor Engine のソースを BSD 3-Clause ライセンスで公開しました（github.com/GaijinEntertainment/DagorEngine）。ここの読み取りは、それをもとに書かれています。ゲームのコードは逆コンパイルされていません。各モジュールは、従っているソースファイルを挙げています:

- `vromfs.py`: `*.vromfs.bin`（ヘッダー `VRFs`/`VRFx`、先頭と末尾の 16 バイトが固定のキーで XOR された zstd の本体、名前の表、オフセットの表: `osApiWrappers/dag_vromfs.h`、`ioSys/vromfsLoad.cpp`、`supp/dag_zstdObfuscate.h`）と、バイナリの BLK（形式 1〜5。アーカイブの共有名前マップ `\xff?nm` と zstd の辞書つき: `ioSys/dataBlock/blk_serialize.cpp`、`blk_parser.cpp`、`blk_zstd.cpp`）。
- `dxp.py`: テクスチャパック `DxP2`（`lib3d/texPackMgr2.cpp`）と DDSx のヘッダー（`sharedInclude/3d/ddsxTex.h`）。DXT1/DXT5/BC7 は Pillow で復号します。
- `dagorlevel.py`: レベルのバイナリ（`scene/loadLevel.cpp`）、高さマップ（`heightmap/heightmapPhysHandler.cpp`、`heightMapLand/compressedHeightmap.cpp`）、陸地の光線追跡（`landMesh/lmeshManager.cpp`、`landMesh/landRayTracerSoA4.cpp`）、水の高さマップ（`fftWater/fftWater.cpp`）。
- `rigen.py`: 配置されたオブジェクト（`rendInst/riGen/riGenData.h`、`rendInst/rendInstGen.cpp`、`rendInst/riGen/genObjUtil.h`）。
- `landgen.py`: 生成されたオブジェクト（`rendInst/rendInstGenLand.cpp`、`riGen/landClassData.h`、`riGen/genObjByMask.h`、`riGen/genObjByDensGridMask.h`、`riGen/genObjUtil.h`、`riGen/riGenData.h`、`riGen/multiPointData.h`、`riGen/riRotationPalette.h`、`rendInstGen.cpp`（`create`、`precomputeCell`、`generateCell`）、`gameMath/objgenPrng.h`、`util/dag_roHugeHierBitMap2d.h`、`util/dag_hierBitMap2d.h`、`ioSys/dag_roDataBlock.h`、`ioSys/roDataBlk.cpp`、`gameRes/grpData.h`）。
- `rendinst.py`: 描画インスタンス（`shaders/rendInstRes.cpp`、`shaders/dag_rendInstRes.h`、`shaders/matVdataLoad.cpp`、`shaders/shaderMesh.cpp`、`shaders/dag_shaderMesh.h`、`shaders/dag_shaderCommon.h`、`drv/3d/dag_consts_base.h`、`gameRes/gameResDescBin.cpp`）と、meshoptimizer のインデックスのコーデック（`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`、MIT）。
- `terrain.py`: 地表の色（`landMesh/lmeshManager.cpp`、`lmeshLandClasses.cpp`、`lmeshWeightAtlas*.cpp`、`lmeshRenderer.cpp`、`landMesh/shaders/land_weight_atlas.hlsli`、`land_weight_inc.dshl`、`biomes.dshl`、`daNetGame/shaders/land_aces.dshl`、`make_clipmap.dshl`、`physMap/physMapLoad.cpp`、`baseUtil/treeBitmap.cpp`、`levelSplines/levelSplines.cpp`）。
- `collision.py`: リソースのパック（`gameRes/grpData.h`）と衝突リソース（`sharedInclude/gameRes/collResStream.h`、`gameRes/collisionGameResLoad.cpp`）。その三角形は四分木の BVH として保存されています（`daBVH/bvhIO.cpp`、`daBVH/dag_swBLAS_leaf.h`、`swBLASLeafDefs.hlsli`）。

wt_ext_cli（Apache-2.0）も同じアーカイブを読みます。それは必要なく、使っていません。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
