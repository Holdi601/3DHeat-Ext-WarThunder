---
title: "附属文件与完整性"
nav_order: 8
lang: "zh"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# 附属文件与完整性 {#sidecars-and-completeness}

录像中的任何内容都不会被丢弃。转换器读取的内容进入表格和对局文档；其余的一切都会在表格旁边的三个附属文件中完整保存（在 `.3dheat` 文件内，或使用 `--loose` 时单独保存）。这是所有 3DHeat 转换器共同遵守的规则：[转换器保留所有内容](https://holdi601.github.io/3DHeat/converters.html)。

## 附属文件 {#the-sidecars}

- `<对局>.messages.parquet`：发给单位的每条消息（时间、消息 ID 和名称、uid、eid、模板、载具、以十六进制表示的 ID 字段、`decoded`（读取出的内容，以 JSON 表示）、负载），每个复制的组件值（`name` 为组件，`fields` 为其数值），每条实体消息（带有其实体和类别编号），每个复制对象（`ReflectionData <种类>/<索引>`，其字段以十六进制表示），以及本工具任何读取器都不处理的每个数据包，完整保存。
- `<对局>.objectives.parquet`：随时间变化的占领区，服务器每发送一次变化对应一行：`time`、`event`（`state`、`progress`、`captured`、`neutralised`）、`zone`（其字母）、`zoneId`、`object`、`owner`（0 为无，1、2）、`progress`（-100..100，朝向队伍 2 为正）、该区域的 `x`、`y`、`z`，以及该对象的所有 `fields`（以十六进制表示；见 [目标](objectives.md)）。
- `<对局>.flight.parquet`：每架飞机的每一条飞行模型记录，完整保存（其位，以及 `phase`：其开始时所在的首字节中的那一位），附带速度、14 个操纵半字节（`control1-3`、`throttle`），其发动机及其状态、加力燃烧室和工况，以及每种武器的弹数（`ammo`；`numbers` 为完整列表）。其他飞机的数值为其最后一次刷新时的值。

## 计数保证了什么 {#what-the-counts-guarantee}

对局文档中的 `counts` 说明了录像包含什么，以及这些内容的去向：

| 键 | 内容 |
|---|---|
| `packets`、`unreadPackets` | 遇到的每种数据包类型，以及没有任何读取器处理的那些（完整保存在消息附属文件中） |
| `messageIds`、`messageIdsNotRead` | 遇到的每个消息 ID 及其出现次数，以及那些仅被保留、未被读取的 |
| `replicatedComponents`、`replicatedNotRead` | 已读取的组件值，以及仅被保留的那些 |
| `entities`、`entityTemplates`、`entityMessages` | 实体流创建和发送的内容 |
| `droppedSamples` | 有意省略的采样（地面单位在其实体消失之后的残骸），按原因统计 |

除此之外没有任何内容被省略：录像中的每一项，要么被读取进表格或对局文档，要么被完整保存在附属文件中。对局文档中的 `selfCheck` 保存了对已读取内容的核对结果（[工具如何读取录像](how-it-reads.md)）。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
