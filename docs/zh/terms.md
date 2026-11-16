---
title: "条款与许可"
nav_order: 16
lang: "zh"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# 条款与许可 {#terms-and-licence}

## 读取的内容 {#what-it-reads}

转换器读取 War Thunder 保存在你电脑上的录像（或你自己从 warthunder.com 下载的自己战斗的录像），以及你自己安装的 War Thunder 中的关卡文件。这里不包含也不再分发游戏的任何内容：没有游戏资源，没有游戏代码，没有 DLL；Oodle 从你自己的安装中加载。它写出的内容留在你的电脑上：**绝不要发布这些关卡**。

3DHeat 与 Gaijin Entertainment 无关联，也未获得其认可。War Thunder 及相关名称和商标归其各自所有者所有。

权利人：请在 <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> 提交 issue - 我们会尽快回复，并按要求删除任何内容。

## 来源 {#sources}

这里的所有代码都是为本项目编写的；没有从其他解析器复制任何代码。本工具对该格式的了解来自：

- Gaijin 的 Dagor Engine 源代码（github.com/GaijinEntertainment/DagorEngine，BSD 3-Clause）：`prog/engine/daECS/net/network.cpp`、`connection.cpp`、`object.cpp`、`serialize.cpp`、`compression.h`，以及 `prog/engine/daECS/core/baseIo.cpp`、`componentTypes.cpp`（用于实体流，即 `ecs.py`），还有 `net/message.cpp`（`MessageClass::initImpl`，用于了解实体消息如何为其类别编号）。组件和类型名称通过其 FNV-1a 哈希与游戏自身归档中的词汇进行匹配；`ecs.py` 列出了找到的名称。
- 同一源代码中的 `prog/dagorInclude/daNet/mpi.h`、`prog/engine/daNet/ext/mpi.cpp` 和 `daNet/bitStream.h`：消息如何指明它所面向的对象（`wrpl.read_mpi`）。
- ShioUmiusi/WTACRP（MIT）：`docs/REPLAY-FORMAT.md`、`docs/REPLAY-DECODE.md`、`docs/REPLAY-DECODE-ECS.md`、`docs/QUICK-REF.md`，以及其自身的解析器 `web/wrpl-parse.js`，用于了解飞行模型、地面同步、飞行中的武器、带 ID 字段的消息、玩家槽位、座舱数值和二进制 blk 的位布局。WTACRP 将 maxsupermanhd/wrpl-inspector、wt_blk 和 wrpl-acmi（AGPL-3.0）列为其自身的参考；这些项目的代码并未在此阅读。
- 作者自己的录像，以文件形式读取：2025 年的差异（飞行模型较旧的布局、无标志字节的聊天、zlib）、地面姿态、打包高度的偏移、武器的发射点，以及座舱仪表，都是在这些录像上推算出来的。

## 测试 {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<包含示例录像的文件夹> python -m pytest -q   # 同时核对公开的 2025 年示例录像
HEAT3D_WT_REPLAYS=<你自己录像的文件夹> python -m pytest -q        # 步进、身份、AI 标志、横滚符号、平滑器、名称
```

单元测试从不读取安装目录（已设置 `HEAT3D_WT_NO_NAMES`）；使用你自己录像的测试会从你的安装中读取名称。

测试通过代码生成录像（`tests/synth.py`：文件头、数据包、结果、实体流、飞行中的武器），其布局与读取器所记录的布局一致；仓库中不包含任何录像。

## 许可证 {#licence}

MIT：见 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE)。使用了 pyarrow（Apache-2.0）、numpy（BSD-3-Clause）、zstandard（BSD-3-Clause）和 Pillow（MIT-CMU）。关卡读取器是根据 Dagor Engine 的源代码编写的，其版权归 (c) 2023 Gaijin Entertainment 所有，采用 BSD 3-Clause 许可证；其代码并未复制到此处，所用的格式常量（vromfs 的 XOR 密钥、高度范围网格的偏移）在出现的地方都已注明出处。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
