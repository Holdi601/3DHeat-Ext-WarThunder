---
title: "对局文档"
nav_order: 7
lang: zh
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# 对局文档 {#the-match-document}

![合成对局文档的开头部分及其键](../assets/img/match-document.svg)

`<对局>.match.json` 保存了录像中所有不属于表格中某一行的内容。查看器的 **对局** 标签页会读取它。

## 战斗 {#the-battle}

| 键 | 内容 |
|---|---|
| `format`、`version` | `heat3d-wt-replay-match`、`2` |
| `match`、`map`、`level` | 对局 ID（与文件名相同）；地图的 ID；它所使用的关卡文件 |
| `mission`、`missionKey` | 任务名称，以及它在游戏文本文件中的键 |
| `battleClass`、`environment`、`weather` | 与文件头所给出的一致 |
| `sessionId`、`server` | 战斗的会话 ID；服务器 |
| `replayVersion`、`flightLayout` | 录像格式的版本；所读取的飞行数据包布局（`2025` 或 `2026`） |
| `files` | 所读取的录像文件（一个，或服务器录像的各分段） |
| `started`、`timePlayed`、`replayEnd` | 开始时间（ISO，UTC）；游玩秒数（来自结果）；录像最后一个数据包的秒数 |
| `author`、`authorUserId` | 录像播放者及其 Gaijin ID（客户端录像） |
| `teams` | 战斗中的队伍（`1`、`2`） |
| `result` | `winner`、`status`（`success` 或 `fail`，即作者的结局）、`authorTeam`、`teams`（[经济](economy.md)） |
| `vehicleNames` | 载具名称的来源（你的安装）及其语言 |
| `conventions` | 表格中的单位和符号：坐标轴、时间、生命、轨迹、存活、横滚等 |

## 其余内容 {#everything-else}

| 键 | 内容 |
|---|---|
| `battle`、`difficulty`、`gameMode` | 战斗模式：`difficulty` 为 `AB` / `RB` / `SB`（及其名称，以及文件头字节），`gameMode` 为 `ground` / `air` / `naval`，任务模式（`Dom`、`Conq`、`Bttl`、`I2M` 等）及其在你安装中的英文名称（`Domination`、`Enduring Confrontation`），允许的单位类型（见 [战斗模式](ground.md#battle-mode)） |
| `settings` | 文件头之后的任务 blk：模式、环境、天气、得分和时间限制、国家、允许的单位类型、风，以及 `stars`（纬度、经度、日期、当地时间） |
| `sky` | 第一个 `CustomWeatherParams`：太阳和月亮的方向、风、天空颜色、云层偏移 |
| `players`、`slots` | 结果中每位玩家的一行（击杀、地面击杀、死亡、助攻、得分、占领、小队、战队、国家、阵容、他们驾驶过的 uid）；录像中的玩家槽位（名称、用户 ID、队伍） |
| `units` | 录像创建的每个单位实体：eid、uid、模板、载具、种类、类型、队伍、玩家、任务名称、创建和移除的时间、创建的位置，以及哪些组件无法读取 |
| `objects` | 任务中带名称的对象：占领区和机场及其位置和大小，机场轮廓（以点表示），出生区域 |
| `objectives` | 战斗的目标，每项包括 `type`（`capture_zone`、`airfield`、`helipad`、`base`、`spawn`、`convoy_spawn`、`battle_area`、`bombing_target`、`exit_zone`、`kill_area`、`rearm_zone`）、`team`（录像中的 1 或 2，对双方则为空）、`name`（占领区为其字母，如 `A`）、`shape`（`sphere`、`cylinder`、`box`、`point`、`points`、`outline`），并包含 `position`、`radius` / `height` / `size` 和 `heading`，`source`（`replay` 或 `mission`），以及其他已知信息（见 [目标](objectives.md)） |
| `kills`、`hits`、`modulesDestroyed` | 双方的名称和载具；击杀附带武器的英文名称 |
| `weapons` | 每一枚火箭弹、导弹、炸弹、鱼雷、副油箱和抛弃的装载：何时、何处投放（位置、姿态、速度）、由哪个单位投放（300 米和 1.5 秒之内最近的单位）、有多少个飞行采样、最后一次出现的位置、何时被移除 |
| `explosions`、`flak` | `PlayExplosionVisual`（位置、方向、类型）和 `PlayFlakExplosionVisual`（位置） |
| `awards` | 录像播放者的奖励（`TextStreak`：first_blood、连杀、挑战计数器） |
| `detections`、`unitStates` | 单位之间的 `UnitDetected` 配对；一条消息（0xF093），包含单位的位置、姿态和速度，其含义未知 |
| `authorInstruments` | 录像播放者的座舱数值（`ReplayCockpitParams`），按仪表编号列出，每秒至多一条；`known` 为本录像发送的每个编号命名（名称、单位、核对方式），`notNamed` 为其余的编号 |
| `scoreboard` | 每位玩家的统计数据在每次变化时的记录（击杀、死亡、助攻、得分、AI 击杀、海上击杀、占领区、伤害、导弹规避、小队），以及每个队伍的得分和随时间变化的可能兵力点数（见 [反射数据](aircraft.md#reflection-data)） |
| `economy` | 战斗的 Silver Lions 和研究点数（见 [经济](economy.md)）：总计、按玩家、按载具、各倍率、获胜方、核对结果 |
| `entityMessages` | 按类别编号列出的实体消息（0x20）：数量、目标模板、大小 |
| `chat` | 每一行聊天 |
| `triggers`、`hints`、`missionProgress` | 任务脚本的动作（RunTriggerAction）、其提示、其进度消息 |
| `camera` | 录像播放者的录像相机字段，每 0.25 秒一次，按发送时的原样记录（表格中则为一条轨迹） |
| `projectileHitReplays` | 录像播放者自己的命中以及被命中的情况，包括武器、弹药及其英文名称 |
| `results` | 游戏写入的完整结果 blk |
| `counts` | 行数、事件、生命、种类、采样、按模板统计的实体、武器、已读取和未读取的数据包，所见的每个消息 ID 以及未读取的那些，被丢弃的采样 |
| `trackBreaks` | 轨迹上每一次因速度超过该单位所能达到而被切断的地方：位置、距离、速度，以及它最可能是什么 |
| `selfCheck` | [工具如何读取录像](how-it-reads.md) 中列出的核对项，在每次转换时计算；`stepSpeed` 按种类给出查看器连接的轨迹相邻行之间的速度（中位数、第 99 百分位、最高值，以及超过可能速度的步数，该步数必须为 0） |

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
