---
title: "关卡"
nav_order: 9
lang: "zh"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# 关卡（heat3d-wt-level） {#levels-heat3d-wt-level}

`heat3d-wt-level` 会把你自己战争雷霆安装中的关卡转换为查看器所用的 `.glb` 关卡，其坐标系与录像表格相同。

## 一步一步来 {#step-by-step}

1. 列出你安装中的关卡：`heat3d-wt-level list`。它为每个关卡输出一行：名称、地形和其地图，然后是数量。例如（虚构的关卡）：

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. 提取一个、多个（可使用通配符）或全部关卡：

   ```bash
   heat3d-wt-level extract <关卡> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <关卡> -o levels --detail high
   ```

3. 在查看器的 **背景/关卡** 面板中加载 `levels/<关卡>/<关卡>.glb`，它位于该地图的对局之下。

你生成的关卡会保存在你自己的电脑上：永远不要发布它们（见 [条款与许可](terms.md)）。

## 选项 {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| 命令 / 选项 | 作用 |
|---|---|
| `list [--game <文件夹>]` | 安装中的每个关卡 |
| `extract <关卡...>` / `--all` | 指定的关卡（使用 `list` 所输出的名称；可使用通配符），或全部关卡 |
| `-o`、`--out` | 输出文件夹；每个关卡放在 `<输出>/<关卡>/` 中 |
| `--game <文件夹>` | 战争雷霆文件夹（默认：通过 Steam 或启动器找到；也可以用 `HEAT3D_WT_GAME`） |
| `--detail low/medium/high` | 战术地图上的地面采样、地面颜色和物体预算（默认 `medium`） |
| `--max-object-triangles N` | 物体预算（默认：取决于 detail） |
| `--max-grid N` | 每部分每一边的高度图采样数（默认 1024） |
| `--no-objects` | 不包括建筑、树木和其他放置的物体 |
| `--no-generated` | 不包括由地表类别生成的物体（森林、城镇） |
| `--no-terrain-colour` | 用战术地图为地面贴图，而不是用地表类别 |
| `--no-texture` | 地面不加贴图 |
| `--skip-existing` | 跳过已有 `.glb` 的关卡 |

## 输出内容 {#what-is-written}

每个关卡会生成 `<输出>/<关卡>/<关卡>.glb`、`<关卡>.json`（读取到的内容、水面高度、地图矩形、三角形数量、耗时），以及该关卡的战术地图，即 `<关卡>_map.png`（空中地图）和 `<关卡>_tankmap.png`；地面地图还会生成 `<关卡>_terrain.png`，即在坦克地图之上叠加的地面自身颜色。glb 文件会先写入 `<关卡>.glb.part`，完成后再重命名；写入某个关卡期间，会持有 `<输出>/<关卡>/.<关卡>.lock`，因此两次提取不会写入同一个关卡（第二次会输出 `busy <关卡>`）。安装位置通过 Steam 或启动器的默认文件夹找到；否则，可以用 `--game <文件夹>` 或 `HEAT3D_WT_GAME` 指定。

| 部分 | 内容 |
|---|---|
| `ground:<关卡>` | 地形高度图（`HM2`），以网格形式给出；在地面地图上，坦克地图的中间部分（宽度的一半）以 `--detail` 的步长生成，用地表类别、地面贴花和道路着色（`<关卡>_terrain.png`；无法生成时则使用战术地图）；在没有坦克地图的地图（空中地图）上，则以一个步长取整个高度图（`high` 时每边 2048 个采样，否则为 1024），并在空中地图的范围内用地表类别着色（每边 4096 像素，约 131 公里范围内每像素约 32 米；无法生成时使用战术地图）；在没有高度图的关卡上，则使用陆地网格 |
| `ground:<关卡> tank map` | 坦克地图的其余部分，步长粗一级 |
| `ground:<关卡> heightmap surroundings` | 高度图的其余部分，步长更粗 |
| `ground:<关卡> land mesh` | 高度图未覆盖之处的陆地网格碰撞三角形（坦克地图的周围，远至数十公里）；在没有高度图的关卡上，则为地面，按上述方式着色 |
| `ground:<关卡> outside the map` | 图像未覆盖的地面，不加贴图 |
| `water:<关卡>` | 位于关卡 `water_level` 处的一个平面矩形，覆盖全部地形：游戏将水面绘制为一个平面，其下的低地即为海、湖或河床 |
| `water:<关卡> rivers` | 在有水面高度图（`WHM`）的关卡上，覆盖其范围的倾斜水面 |
| `structure:<关卡> buildings` | 每个放置的非植物物体：房屋、废墟、墙、栅栏、桥、铁轨、岩石、道具。固定的物体（`RIGz`），以及在坦克地图上由地表类别生成的物体（城镇街区、石块）。每个物体都按其渲染网格绘制（墙、屋顶、窗口开口、梁），LOD 由三角形预算决定，并按材质以其漫反射贴图的平均颜色着色 |
| `structure:<关卡> trees` | 树木和灌木，包括固定的和生成的（森林、树篱）：在预算允许时使用其渲染网格，否则用树干和树冠（针叶树为圆锥形）表示，颜色为该树自己的叶色，大小为其真实尺寸 |

没有渲染网格的物体会退回到其碰撞形状；没有渲染网格的树木则退回为树冠。顶点颜色（`COLOR_0`）保存的是 sRGB 编码的数值，3DHeat 查看器正是以此读取它们的。

**坐标**采用游戏的米，并对 z 取反：glb 的 (x, y, z) = 游戏的 (x, y, -z)。游戏世界是左手坐标系（x 朝东，y 朝上，z 朝北）；glTF 则是右手坐标系。`heat3d-wt-replay` 保留游戏的 z，并告诉查看器对其取反，因此录像和其地图的关卡会彼此重合，无需任何摆放步骤。JSON 以游戏的米给出每张战术地图的矩形，并给出它在 glb 空间中的四角坐标，以便将 PNG 作为地图图像加载。

**细节。** `--detail low|medium|high`（默认 medium）在坦克地图上设置以下内容：

| | 坦克地图中间部分 | 坦克地图其余部分 | 地面颜色 | 物体预算 | 每个物体最多三角形数 | 保留的生成植物 |
|---|---|---|---|---|---|---|
| low | 每 4 个采样一个 | 每 8 个采样一个 | 每像素 4 米 | 120 万 | 1,500 | 树木 35%，灌木 20% |
| medium | 每 2 个采样一个 | 每 4 个采样一个 | 每像素 2 米 | 350 万 | 4,000 | 树木 70%，灌木 50% |
| high | 每个采样（在多数地面地图上为 2 米） | 每 2 个采样一个 | 每像素 1 米（每边至多 4096 像素） | 450 万 | 12,000 | 全部 |

两个坦克地图环带的三角形数量被限制为：low 30 万、medium 100 万、high 370 万。对于高度图精度高于 2 米的地图，步长会加倍（先处理外环），直到符合上限，因此这些地图的结果也大约为 2 米。

在 `high` 下，地面地图大约会生成 800 万个三角形（陆地 350 万，物体 450 万），占 250 MB；在 `medium` 下约为 450 万个。物体的 LOD 取的是游戏自身在同一观看距离下会绘制的版本：在总量符合预算的前提下，取最短的那一个。小道具会先降到粗糙的 LOD，大型建筑最后才降；降低的依据是制作者为每个 LOD 给出的距离范围（JSON 中的 `lodDistance`）；超出预算的节省量则回算到最大的物体上。空中地图的粗糙地面颜色，会先把每个地表类别的平铺贴图平均到像素大小，以免平铺纹理产生摩尔纹。如果即使最粗的 LOD 也无法放下，则节省最多的树木会变成树冠，然后最小的类型会被省略（`leftOut`）；没有任何物体会被画成方盒（如果有碰撞形状，则为物体自己的碰撞形状）。生成的物体会按类型（`density`）以确定的方式稀疏化，每次运行结果都相同。`--max-object-triangles` 可以覆盖预算；`--max-grid`（默认 1024）限制高度图较粗部分的大小；`--no-objects` 省略物体，`--no-generated` 省略生成的物体，`--no-terrain-colour` 用战术地图为地面贴图，`--no-texture` 则让地面不加贴图。

JSON 中的 `parts.objects` 列出实例（固定的和生成的，按类型和地表类别），每个实例以哪种 LOD 绘制（`drawnAs`）、三角形数、LOD 距离和耗时；`parts.heightmap.rings` 给出每个地面环带的步长和三角形数；`parts.terrainColour` 给出地表类别及其颜色、道路和地面贴花；`trianglesTotal`、`glbBytes` 和 `secondsBy` 给出总计。

## 读取了什么，以及读取的效果如何 {#what-is-read-and-how-well}

| 部分 | 状态 |
|---|---|
| 关卡二进制文件（`levels/<关卡>.bin`，`DBLD` 3x64）：块表 | 已核对每个关卡 |
| 高度图（`HM2`，版本 0-2；版本 2 是块中的 8 位数值，使用 Oodle 或 zstd 分块） | 已核对每个高度图为版本 2 且使用 Oodle 分块的关卡；已与战术地图逐一肉眼核对（河流、山谷、海岸和城镇吻合） |
| 陆地网格碰撞（`lmap`，及其 `LTdump` 陆地光线追踪器） | 在有该数据的关卡上读取（Oodle 打包）。它是游戏的碰撞表面，而不是渲染网格，因此在平坦的陆地上会更粗糙 |
| 地面颜色（`lmap` 的地表类别和权重图，`LMp2` 物理图，`hspl` 样条） | 地表类别的颜色图和细节贴图（取其平均颜色），按权重图加权；有索引的地表类别的 1 米群落索引；物理图中的道路和地面贴花形状，颜色取自其样条或材质的贴图；陡坡上的悬崖。已与坦克地图核对：道路、城镇、湖泊、森林带和岩石露头吻合。战争雷霆自身地形着色器的颜色公式不在公开源代码中；这里使用的是引擎公开的版本（daNetGame），其颜色比战术地图更饱和 |
| 水面高度 | 来自 `aces.vromfs.bin` 中关卡 BLK 的 `water_level`（没有则为 0） |
| 水面高度图（`WHM`：平坦单元格的网格，以及 130x130 页的 16 位高度） | 在有该数据的关卡上读取；其河流会随地面倾斜 |
| 战术地图 | 来自 `content/base/res/locations_maps.dxp.bin`，依据 BLK 中的 `mapCoord0/1` 和 `tankMapCoord0/1` 放置；图像顶部为北方 |
| 放置的物体（`RIGz`：渲染实例生成器的固定实例） | 每个实例，以 3x4 的 16 位数值矩阵表示，在某些关卡上为 32 位（由单元格的字节数决定）；已核对的关卡上，每个单元格的每个字节都有着落 |
| 生成的物体（`RIGz` 地表类别遮罩和 `LandClass` 资源） | 游戏的生成器已移植：以相同的顺序、相同的随机数尝试相同的位置，并应用地表类别和排除遮罩，在每个位置选出物体，然后确定其旋转、缩放和高度偏移；平铺（城镇街区）和种植（森林、灌木、田地）的实体。仅在坦克地图上生成。近似之处：地面高度和法线（来自高度图；游戏会进行光线追踪），游戏在运行时登记的排除框，以及树木的偏航（游戏会将其对齐到替身的旋转调色板） |
| 渲染网格（`content/*/res/*.grp` 中的 `RendInst` 资源，`riDesc.bin` 中的材质） | 每个 LOD 的顶点和三角形（浮点位置；16 位或 32 位索引，普通或经 meshoptimizer 打包），每个元素的材质。贴花和替身广告牌元素被省略；透明元素（玻璃）则保留 |
| 物体颜色 | 按材质取其漫反射贴图较小 mip 层级的平均值（叶子则按 alpha 加权），来自安装中的贴图包：多数着色器取 t0，若 t0 是叠加或遮罩，则取第一个细节漫反射。每种材质一个颜色：物体上没有贴图 |
| 碰撞形状（`<物体>_collision`） | 流版本 3 的碰撞资源，在物体没有渲染网格时使用。只绘制游戏光线所击中的内容（`TRACEABLE` 节点）；只有在资源没有网格时才绘制方盒、球体和胶囊体：其余都是粗糙的物理替身，会在物体周围显示为立方体 |
| 导航网格（`Lnav`）、渲染的陆地网格、草地、`spgz`、`stbl`、`d2co` | 未读取 |

关卡使用 Oodle 压缩，而 Oodle 是专有软件。游戏自带一份副本，即 `<War Thunder>\win-arm64ec\oo2core_9_win64.dll`（一个普通的 x64 版本），加载的就是它；`HEAT3D_OODLE=<dll 或文件夹>` 可以指定另一个。本仓库中不包含任何 Oodle 内容。

## 格式及其文档位置 {#formats-and-where-they-are-documented}

Gaijin 以 BSD 3-Clause 许可证公开了 Dagor Engine 的源代码（github.com/GaijinEntertainment/DagorEngine）。这里的读取器是依据它编写的；没有反编译任何游戏代码。每个模块都注明了它所遵循的源文件：

- `vromfs.py`：`*.vromfs.bin`（文件头 `VRFs`/`VRFx`，zstd 主体，其前 16 字节和后 16 字节与一个固定密钥进行 XOR，还有一个名称表和一个偏移表：`osApiWrappers/dag_vromfs.h`、`ioSys/vromfsLoad.cpp`、`supp/dag_zstdObfuscate.h`）以及二进制 BLK（格式 1-5，使用归档的共享名称映射 `\xff?nm` 和 zstd 字典：`ioSys/dataBlock/blk_serialize.cpp`、`blk_parser.cpp`、`blk_zstd.cpp`）。
- `dxp.py`：贴图包 `DxP2`（`lib3d/texPackMgr2.cpp`）和 DDSx 文件头（`sharedInclude/3d/ddsxTex.h`）；DXT1/DXT5/BC7 由 Pillow 解码。
- `dagorlevel.py`：关卡二进制文件（`scene/loadLevel.cpp`）、高度图（`heightmap/heightmapPhysHandler.cpp`、`heightMapLand/compressedHeightmap.cpp`）、陆地光线追踪器（`landMesh/lmeshManager.cpp`、`landMesh/landRayTracerSoA4.cpp`）以及水面高度图（`fftWater/fftWater.cpp`）。
- `rigen.py`：放置的物体（`rendInst/riGen/riGenData.h`、`rendInst/rendInstGen.cpp`、`rendInst/riGen/genObjUtil.h`）。
- `landgen.py`：生成的物体（`rendInst/rendInstGenLand.cpp`、`riGen/landClassData.h`、`riGen/genObjByMask.h`、`riGen/genObjByDensGridMask.h`、`riGen/genObjUtil.h`、`riGen/riGenData.h`、`riGen/multiPointData.h`、`riGen/riRotationPalette.h`、`rendInstGen.cpp`（`create`、`precomputeCell`、`generateCell`）、`gameMath/objgenPrng.h`、`util/dag_roHugeHierBitMap2d.h`、`util/dag_hierBitMap2d.h`、`ioSys/dag_roDataBlock.h`、`ioSys/roDataBlk.cpp`、`gameRes/grpData.h`）。
- `rendinst.py`：渲染实例（`shaders/rendInstRes.cpp`、`shaders/dag_rendInstRes.h`、`shaders/matVdataLoad.cpp`、`shaders/shaderMesh.cpp`、`shaders/dag_shaderMesh.h`、`shaders/dag_shaderCommon.h`、`drv/3d/dag_consts_base.h`、`gameRes/gameResDescBin.cpp`），以及 meshoptimizer 的索引编解码器（`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`，MIT）。
- `terrain.py`：地面颜色（`landMesh/lmeshManager.cpp`、`lmeshLandClasses.cpp`、`lmeshWeightAtlas*.cpp`、`lmeshRenderer.cpp`、`landMesh/shaders/land_weight_atlas.hlsli`、`land_weight_inc.dshl`、`biomes.dshl`、`daNetGame/shaders/land_aces.dshl`、`make_clipmap.dshl`、`physMap/physMapLoad.cpp`、`baseUtil/treeBitmap.cpp`、`levelSplines/levelSplines.cpp`）。
- `collision.py`：资源包（`gameRes/grpData.h`）和碰撞资源（`sharedInclude/gameRes/collResStream.h`、`gameRes/collisionGameResLoad.cpp`），其三角形以四边形 BVH 存储（`daBVH/bvhIO.cpp`、`daBVH/dag_swBLAS_leaf.h`、`swBLASLeafDefs.hlsli`）。

wt_ext_cli（Apache-2.0）也读取相同的归档；这里不需要它，也没有使用它。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
