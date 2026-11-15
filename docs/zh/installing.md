---
title: "安装"
nav_order: 3
lang: zh
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# 安装 {#installing}

刚接触命令行？先读 [开始之前](before-you-start.md)。
需要 Python 3.10 或更高版本；pyarrow、numpy、zstandard 和 Pillow 会随之一起安装。

## 一步一步来 {#step-by-step}

1. 获取代码：`git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`，
   或从 [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases) 下载压缩包并解压。
2. 在该文件夹里打开终端，输入 `pip install -e .`。这会安装两个命令：`heat3d-wt-replay`（对局录像）和 `heat3d-wt-level`（关卡）。
3. 检查安装：`heat3d-wt-replay --version`。你应该看到 `heat3d-wt-replay 0.2.0`。`heat3d-wt-replay --help` 会列出所有选项：

![heat3d-wt-replay --help](../assets/img/help.svg)

不安装也能用：在工具所在的文件夹里运行 `python -m heat3d_ext_warthunder ...` 和 `python -m heat3d_ext_warthunder.levelcli ...`。

## 来自你的游戏安装的名称 {#names-from-your-install}

载具、武器和弹药的英文名称来自游戏自带的文本文件，转换时从你的游戏安装中读取。程序通过 Steam 或启动器的默认文件夹找到安装位置；如果找不到，可以用 `--game <文件夹>` 或环境变量 `HEAT3D_WT_GAME` 指定。本仓库中不包含游戏的任何文字。没有安装时，名称就是载具的 ID（转换器会用 `note:` 行说明这一点）。

## 更新 {#updates}

每次启动时，程序都会先检查项目在 GitHub 上的发布版（最多每几个小时请求一次；无论能否联网，都不会因此中断转换）。出现新版本时，命令会先询问，再安装它：用 `git clone` 得到的副本会用 `git pull --ff-only` 更新（如果你有本地改动，则会拒绝更新），下载的副本则从该发布版的压缩包更新。设置 `HEAT3D_NO_UPDATE=1` 可以同时关闭检查和更新。

---

本页是 [3DHeat](https://github.com/Holdi601/3DHeat) 的一部分（[文档](https://holdi601.github.io/3DHeat/)）。来源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
