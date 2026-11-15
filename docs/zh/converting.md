---
title: "转换录像"
nav_order: 4
lang: zh
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# 转换录像 {#converting-replays}

输出：默认每场对局一个 `.3dheat` 文件；使用 `--loose` 则输出单独的文件。

## 一步一步来 {#step-by-step}

1. **打开录像保存功能。** 在游戏选项中开启录像保存后，战争雷霆会把客户端录像保存到游戏的 `Replays` 文件夹中，例如 `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`。从游戏的录像页面保存的服务器录像（一个包含 `0000.wrpl`、`0001.wrpl`……的压缩包）也可以转换。
2. **打开终端**，并进入一个可以存放结果的文件夹（[开始之前](before-you-start.md)）。
3. **转换：**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # 文件、文件夹，或两者都可以
   heat3d-wt-replay battle.zip -o out              # 服务器录像的压缩包
   heat3d-wt-replay a.wrpl -o out --loose          # 单独的文件，而不是一个 .3dheat
   ```

   `out` 会在你终端所在的文件夹中创建。
4. **阅读输出的内容。** 每场对局应输出一行。
5. **打开结果：** 在 3DHeat 查看器中加载 `out/<地图>/<对局>.3dheat`（[如何加载](https://holdi601.github.io/3DHeat/container.html#loading-one)）。

![在一段合成录像上的运行结果：一个 .3dheat、--loose、一个损坏的文件、一个空文件夹](../assets/img/convert.svg)

这张图是在测试程序以代码生成的录像上运行的结果（没有真实录像，也没有游戏安装）：

- `ok <文件>`：一场对局已转换（使用 `--loose` 时为：`ok <表格> <对局文档>`）；
- `failed <文件>: <原因>`：无法读取的文件（退出状态为 1；其他对局仍会被转换）；
- `no .wrpl files given`：没有可转换的内容（退出状态为 2）；
- `note: ...`：例如，没有找到用于命名载具的战争雷霆安装。

## 选项 {#options}

| 选项 | 默认值 | 作用 |
|---|---|---|
| `replays`（一个或多个） | - | `.wrpl` 文件、其中的文件夹（只包括文件夹本身，不含子文件夹），或它们的压缩包（服务器录像：其 `.wrpl` 分段会解压到一个临时文件夹中） |
| `-o`、`--out` | 必填 | 写入位置：在其中为每张地图建立一个文件夹 |
| `--game <文件夹>` | 自动查找 | 战争雷霆的文件夹，用于读取载具、武器和弹药的名称，并用于查询[经济数据](economy.md)的价格表；也可以用环境变量 `HEAT3D_WT_GAME` |
| `--no-smoothing` | 关闭 | 保留其他单位的航位推算和接收到的采样，与录像中的一致（[航位推算](aircraft.md#dead-reckoning-and-the-smoother)） |
| `--container` | 开启 | 将每场对局打包成一个 `.3dheat` 文件 |
| `--loose` | 关闭 | 将每场对局保存为单独的文件（表格、对局文档、附属文件） |
| `--version` | - | 输出 `heat3d-wt-replay <版本>` 并退出 |
| `-h`、`--help` | - | 输出选项列表并退出 |

同一场对局再次转换时，会重新写入。程序输出的选项列表见：[命令参考](../cli-reference.md)。

## 哪些文件属于同一场对局 {#which-files-are-one-battle}

每场对局会生成一个文件：
`out/<地图>/<地图>_<AB|RB|SB>_<模式>_<开始时间，UTC>_<会话 ID>.3dheat`。AB、RB 和 SB 是游戏对街机战斗、拟真战斗和模拟战斗的简写；`<模式>` 是游戏为任务设定的模式代码（`Conq4` 为征服 #4，`Dom` 为统治，`Bttl` 为战斗；见 [战斗模式](ground.md#battle-mode)）；如果录像中没有某一部分，则该部分会被省略。服务器录像的各分段（`0000.wrpl`、`0001.wrpl`……）会一起作为一场对局读取；客户端录像与服务器分段即使属于同一场战斗，也是两份录像，会保持为两个文件。

## 退出状态 {#exit-status}

`0` 表示所有对局都已转换；`1` 表示有任何一场失败（其余对局仍会被转换）；`2` 表示在参数中没有找到录像文件。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
