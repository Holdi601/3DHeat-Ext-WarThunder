---
title: "目标"
nav_order: 15
lang: zh
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# 目标 {#objectives}

对局文档中的 `objectives` 列出了这场战斗争夺的对象，来源有两类（`source`）：

- **录像**（`replay`）：任务对象 0xD039 指定的对象（占领区 `cz_circle_NN`、机场、直升机停机坪、基地），放置在种类为 3 的复制对象（0xF02D）如今所在的位置上：占领区从其模板的位置开始，并在对局开始时被移到本模式的区域（`moved`）。种类 3 的编号遵循 0xD039 的顺序；每个未被移动的对象，都精确位于 0xD039 所给出的位置，这也核对了顺序。占领区会取其所在位置任务区域的形状和半径（`area`，误差在 2 米之内），其字母则取自它自己的索引（种类 5 的字段 69：0 = A）；字母顺序以录像为准，未与游戏地图进行核对。
- **任务**（`mission`）：你安装中 `mis.vromfs.bin` 里的任务文件 `<任务>.blk`，以及它导入的模板（仅在转换时读取）：其中的区域按名称分类——出生点（出生点的编号点 `..._spawnareaNN` 合并为一个 `points` 出生点）、战斗区域、轰炸目标（`bomb_zone`）、护送出生点（`road_NN_spawn`）、离开区域和击杀区域。同一地图其他模式的区域（`conq_`、`dom_`、`bttl_` 等）会被排除；对于 `_arcade`、`_realistic`、`_hardcore` 变体，则采用本场战斗自己的版本（RB 取 `_realistic`，否则取 `_hardcore`，与任务脚本的做法相同）；简报标记、高射炮位置，以及宽于 5 公里的区域（出生点分散分布于其中）也会被排除。每个出生点会说明有多少玩家的轨迹从其中开始（`used`、`usedByTeam`）。任务可能会随机交换双方（`randomSpawnTeams`）：当出生点显示录像中的队伍方向相反时，每个 `team` 都会被交换，而名称所对应的一方则以 `missionTeam` 保留。护送路线在读取的任务航路点中并不存在；只给出护送出现的位置。

随时间变化的占领区记录在附属文件 `<对局>.objectives.parquet` 中：即种类 5 的复制对象，每个区域一个——字段 2 为其所有者（0、1、2），字段 67 为其占领进度，是从 -100 到 100 的带符号字节（朝向队伍 2 为正），字段 69 为其索引。已在攻占与统治对局的地面服务器录像上核对（`selfCheck.objectives`）：每次所有者变化，都会伴随该占领队伍的一名玩家在记分板上同一时刻获得 `captureZone`（在 1.5 秒之内），并且该队伍有一个存活的地面单位位于该区域之内；每场对局的出生点都只显示录像中的队伍方向为一种（通常与任务中的 `t1_` / `t2_` 相反）。

## 场景单位：有轨电车和铁路车厢 {#scene-units-trams-and-rail-wagons}

关卡可以放置它自己的单位：服务器录像中的 `unit_loader+rail_wagon` 实体，即关卡场景文件中的有轨电车（`gamedata/scenes/<关卡>_objects.blk`，位于 `aces.vromfs.bin` 中：`setting__unit_class`、其变换和 `setting__isDead`）。这些实体不携带可读取的 uid，因此没有单位实体、且其第一个采样位于某个场景单位 2 米之内的地面轨迹，即该单位：其类别为 `Vehicle`，种类 `train`，类型为 `tram`、`locomotive` 或 `wagon`，没有队伍；场景中被放置为已死亡的单位（例如烧毁的有轨电车）则从其第一行开始就是残骸（`alive` 为 0）。游戏中它们没有英文名称；`VehicleName` 取其 ID 并将其读作单词（"Railway tram A"）。它们的位置不会晃动：几乎所有都从不移动（每个采样在每一位上都完全相同）。录像无论如何都会大约每秒发送十次，因此在它们的采样中，只保留那些确实使其移动的采样（0.05 米或 0.1 度），并且每 10 秒保留一个（`selfCheck.sceneUnits` 统计被丢弃的采样数）。在此之前，它们是名为 `uid 8` 且没有载具的轨迹。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
