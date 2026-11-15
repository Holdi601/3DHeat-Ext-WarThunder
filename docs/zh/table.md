---
title: "表格"
nav_order: 6
lang: "zh"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# 表格 {#the-table}

![一份合成录像的表格，已概括](../assets/img/table.svg)

每个采样或事件占一行，共 105 列（[列清单](../columns.md)，由代码生成）；在页脚中，`heat3d` 下保存着查看器的读取说明，因此查看器无需填写任何表单。

| 列 | 内容 |
|---|---|
| `time` | 录像自身时钟上的秒数 |
| `event` | `position`：事件行位于轨迹上其发生的时刻（两个采样之间，即它们之间的连线上）；`kill`（位于击杀者处）、`death`（位于受害者处）、`hit_critical` / `hit_severe`（位于被命中的单位处）、`module_destroyed`（位于单位处）、`launch`（位于投放武器的单位处）、`impact`（武器被移除前紧接的最后一个采样）；`explosion` 和 `flak`（0xD08E、0xD01F）位于其位置处，种类为 `effect`，没有轨迹，若有爆炸方向则带有该方向；`shot`（命中的弹丸，位于射手处）、`gun_shot`、`fire_start`、`fire_stop`（火炮的连发，而非着火的载具）、`fire_on`、`fire_off`（着火的载具，见 [载具火灾](hits.md#vehicle-fires)）、`reward`（获得的 Silver Lions 和研究点数，见 [经济](economy.md)）、`dead`、`bailout`、`repair`、`rearm`、`bullet_rearm`、`reload`（见 [发给单位的消息](how-it-reads.md#messages-to-units)）；`despawn`：单位在录像结束前消失的轨迹的最后一行（见 [轨迹的结束](ground.md#end-of-a-track)） |
| `track` | 查看器画作一个整体的对象：单位的一次生命，或一枚武器的飞行 —— `<玩家或载具> #<十六进制>`（查看器显示名称时不含 `#` 部分） |
| `x`、`y`、`z` | 游戏中的米：x 朝东，y 朝上，z 朝北（提示会对 z 取反，因此北方不会被画成南方） |
| `player` | 玩家名称；AI 单位为 `<VehicleName> #<uid>`（例如 `F-15A #204`）；没有任何名称时为 `uid <n>`；对于武器，则为投放它的人 |
| `userId`、`team` | 玩家的 Gaijin ID 和队伍（`1`、`2`） |
| `ai`、`isPlayer` | 对于每个没有玩家账号驾驶的单位（任务单位、AI 飞机、地面目标、高射炮、没有玩家的舰船、占位物），`ai` 为 true；`isPlayer` 则相反：玩家是其实体指向一个带有 Gaijin ID 的玩家槽位的单位。武器则与其发射器相同；未知时为空 |
| `match` | 对局 ID（对局文档中的 `match`），出现在每一行上；提示将其作为会话，因此两个已加载的录像永远不会合并轨迹 |
| `life` | `uid#n`：单个单位的轨迹；当 uid 转到另一个单位时、单位的移动速度超过其能力（重生、重新装填、游戏移动了它、客户端修正了远处的单位；见 [工具如何读取录像](how-it-reads.md#what-is-read-and-the-check) 中的瞬移）或长时间未被看到时，该轨迹会被切断；`w<十六进制>` 为一枚武器的飞行（切断后为 `w<十六进制>#n`） |
| `uid` | 单位在录像中的 ID |
| `kind` | `aircraft`（飞机）、`helicopter`（直升机）、`tank`（坦克）、`apc`（装甲运兵车）、`spaa`（防空车）、`truck`（卡车）、`ship`（舰船）、`boat`（小艇）、`structure`（建筑）、`train`（关卡放置的有轨电车或铁路车厢，见 [场景单位](objectives.md#scene-units-trams-and-rail-wagons)）；武器为 `missile`（导弹）、`rocket`（火箭弹）、`bomb`（炸弹）、`torpedo`（鱼雷）、`payload`（载荷）、`jettisoned`（抛弃的装载）；`camera` 为录像播放者的录像相机（见 [相机](ground.md#the-camera)） |
| `type` | 结果中给出游戏自身的类型时使用该类型（`fighter`、`assault`、`destroyer`、`gun_boat`），否则与 `kind` 相同 |
| `Vehicle` | 游戏的载具 ID（`f_15a`、`germ_flakpz_I_Gepard`），查看器的造型与之匹配 |
| `VehicleName`、`VehicleShortName`、`VehicleNameKey` | 来自你安装中的本地化，载具的英文名称（`Pz.Kpfw. III Ausf. J1`，简称 `Pz.III J1`）及其键（`germ_pzkpfw_III_ausf_J_0`）；游戏字体中的国家标志被省略。游戏中没有名称、或找不到安装时，名称为 ID，键为空 |
| `mission` | 任务中该单位的名称（`t1_tank_05`、`t2_player03_0`） |
| `dirX`、`dirY`、`dirZ` | 单位朝向的方向（视线向量）：飞机由飞行模型的姿态决定，地面单位和舰船由它们自身的姿态决定，武器则沿其飞行方向 |
| `heading`、`pitch`、`roll` | 同样的内容，以度为单位；航向为罗盘方向，从北向顺时针；俯仰为机头朝上为正；横滚为右翼下沉为正（飞行模型发送的符号相反，见 [姿态核对](aircraft.md#attitude-checked)；地面单位则为右侧朝下）。提示在 `conventions` 中对此有说明 |
| `turretYaw`、`gunPitch`、`turrets` | 坦克的主炮塔：即火炮指向的方向，而不是玩家所看的方向；录像的数值受炮塔驱动机构的速度约束，并设置到每次主炮射击的连线上（见 [炮塔](ground.md#turrets)）：其相对于车体的偏航（度，从上方看顺时针为正，0 为正前方）以及其火炮相对于车体的俯仰（度，朝上为正）；`turrets` 按其自身顺序，以 `偏航 俯仰;偏航 俯仰;...` 的形式列出载具的每个炮塔（未使用的槽位显示为 `0.00 0.00`）。适用于客户端和服务器录像中的坦克、防空车、装甲运兵车和卡车；不适用于舰船（见 [炮塔](ground.md#turrets)） |
| `turretYawRaw`、`gunPitchRaw` | 录像所发送的主炮塔原始值；`turretYaw` / `gunPitch` 则是将其约束在炮塔驱动机构速度之内，并设置到每次主炮射击的连线上（见 [炮塔](ground.md#turrets)） |
| `viewYaw`、`viewPitch` | 玩家在世界中所看的方向（用相机瞄准）：罗盘度数（0 为北，顺时针）及向上的度数，与 `aimHeading` / `aimPitch` 的约定相同（不同于 `turretYaw` / `gunPitch`，后者保持相对于车体）。服务器录像中每位玩家的坦克，客户端录像中则为录像播放者自己的坦克；玩家没有瞄准任何地方时为空（四个瞄准浮点数都为 0）。炮塔以其自身的转动速度跟随它，因此在它转动时两者会有差异（见 [炮塔](ground.md#turrets)） |
| `aimHeading`、`aimPitch`、`aimDistance` | 录像播放者自己的坦克：它的瞄准方向（罗盘度数、向上的度数，以及以米为单位的距离；瞄准镜中没有任何目标时为 2000）；相机行：玩家瞄准的方向（航向、俯仰） |
| `zoom` | 相机行：相机的放大倍率（见 [相机](ground.md#the-camera)） |
| `difficulty`、`gameMode` | 每一行都有：战斗的 `AB`、`RB` 或 `SB`，以及 `ground`、`air` 或 `naval`（见 [战斗模式](ground.md#battle-mode)） |
| `extrapolated` | 飞机的采样，是客户端的航位推算结果，而不是它收到的状态（见 [航位推算](aircraft.md#dead-reckoning-and-the-smoother)）；炸弹的采样则根据其投放推算得出（见 [工具如何读取录像](how-it-reads.md#what-is-read-and-the-check) 中的“没有飞行记录的炸弹”） |
| `moved`、`xRaw`、`yRaw`、`zRaw`、`headingRaw`、`pitchRaw`、`rollRaw` | 平滑器移动该采样的距离（米），以及录像自身的位置和姿态（横滚采用表格中的符号） |
| `targetX`、`targetY`、`targetZ` | `shot` 的命中点 |
| `hitOutcome`、`hitFlags` | `shot` 对地面单位的结果：`kill`、`critical`、`penetration` 或 `nonpenetration`（弹开或被挡住：录像无法区分跳弹），由服务器随命中发送的位得出（`hitFlags`，原始值）；未发送任何位时为空（飞机、舰船）。见 [命中结果](hits.md#hit-outcomes) |
| `hitShell` | `shot` 的炮弹特征：命中消息中的四个字节（原始十六进制）；同一特征可能代表不同的炮弹（120 毫米和 125 毫米 APFSDS 共用一个），因此保留为原始值，不作为口径解读 |
| `ammoType`、`ammoName`、`ammoSlot`、`calibre` | `shot` 的弹药：其类型（`APFSDS`、`APDS`、`HE`、`HEAT-FS`、`HESH`、`ATGM`……）和 ID（`125mm_3bm46`），当击杀指明了射手的槽位时使用，否则为 `explosive`（命中时爆炸）或 `kinetic`（动能）；火炮的 `weapon/slot` 来自其装填记录；口径以毫米计，取自安装中的武器文件。见 [命中结果](hits.md#hit-outcomes) |
| `rpm` | 飞机的发动机转速（其各发动机的平均值），为 2 秒之内最后一次发送的数值 |
| `vx`、`vy`、`vz` | 飞机的速度，即其飞行记录所发送的值（米/秒，游戏的坐标轴；超过 500 米/秒的速度记为 500） |
| `engine`、`afterburner`、`engineCondition` | 飞机发动机的状态，来自其飞行记录：`off`、`starting`、`running`、`dead`（发动机不一致时以 `/` 连接）；加力燃烧室为 0-1；仅在发动机被命中后才发送的字节 |
| `weaponName` | 击杀和死亡：你安装中英文名称的武器或弹药（`AIM-120C-5 AMRAAM air-to-air missiles`、`Fragmentation incendiary tracer shell`） |
| `throttle`、`elevator`、`aileron`、`rudder`、`ammo` | 仅限录像播放者的飞机：来自座舱的油门 0-1.1（1.1 表示战时紧急动力或加力燃烧室；否则为其飞行记录中的十五分之一），来自其飞行记录的操纵 -1..1（升降舵为正表示拉杆，副翼为正表示向右滚转），每种武器剩余的弹数（`250 140 170`） |
| `ias`、`vario`、`fuel`、`manifoldPressure`、`gear`、`oilTemperature`、`headTemperature` | 仅限录像播放者的飞机，来自其座舱：指示空速和爬升率（米/秒）、燃油、进气歧管压力（atm）、起落架（0-1，1 为放下）、机油和气缸盖温度，前提是其座舱有相应仪表 |
| `speed` | 轨迹上约两秒内的速度（米/秒，在此计算；录像不为其他单位发送速度） |
| `alive` | 单位死亡后（即其残骸）采样的值为 0：地面单位或舰船的残骸，直到游戏将其移除或其采样结束为止；飞机的残骸最多保持 60 秒 |
| `otherVehicle`、`otherLife` | `shot` 的受害者：其载具及其 `life` |
| `hitLocalX`、`hitLocalY`、`hitLocalZ`、`hitDirX`、`hitDirY`、`hitDirZ` | `shot` 在受害者自身坐标系中的命中点（米；x 为前方，y 为上方，z 为左侧；见 [发给单位的消息](how-it-reads.md#messages-to-units)），以及射击来自的方向，并按当时受害者的姿态转换到该坐标系中 |
| `hitPart`、`hitFlag` | `shot` 的命中消息：其所发送的部件字，以及其高位字节 |
| `cost_fired_sl`、`cost_lost_sl`、`earn_sl`、`earn_rp`、`rewardType`、`currency`、`econ_basis`、`won` | 一场战斗花费和赚取了多少，以及谁赢了：见 [经济](economy.md) |
| `other`、`weapon` | 击杀：另一方及武器；命中：谁命中了（来自记录的 uid，否则来自其玩家槽位）及其载具；发射：武器；被摧毁的模块：在此之前 5 秒之内最后命中该单位的人，以及 `part <n>` |

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
