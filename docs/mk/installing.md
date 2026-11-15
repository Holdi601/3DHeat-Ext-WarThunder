---
title: "Инсталирање"
nav_order: 3
lang: "mk"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Инсталирање {#installing}

Нови сте со командната линија? Прво прочитајте [Пред да започнете](before-you-start.md). Потребен е Python 3.10 или понов; pyarrow, numpy, zstandard и Pillow се инсталираат заедно со него.

## Чекор по чекор {#step-by-step}

1. Земете го кодот: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`, или преземете zip од [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases) и распакувајте го.
2. Отворете терминал во таа папка и напишете `pip install -e .`. Ова инсталира две команди: `heat3d-wt-replay` (снимки) и `heat3d-wt-level` (нивоа).
3. Проверете: `heat3d-wt-replay --version`. Треба да видите `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` ги наведува опциите:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без инсталирање: `python -m heat3d_ext_warthunder ...` и `python -m heat3d_ext_warthunder.levelcli ...` во папката на алатката.

## Имиња од вашата инсталација {#names-from-your-install}

Возилата, оружјата и муницијата ги добиваат англиските имиња од сопствените текстуални датотеки на играта, кои се читаат од вашата инсталација при претворањето. Инсталацијата се наоѓа преку Steam или стандардните папки на лансерот; инаку `--game <folder>` или променливата на околината `HEAT3D_WT_GAME` кажуваат каде е. Ништо од текстот на играта не е во ова складиште; без инсталација имињата се ид-ата на возилата (конверторот го кажува тоа во линија `note:`).

## Ажурирања {#updates}

Секој почеток прво ги проверува GitHub изданијата на проектот (најмногу едно барање на неколку часа; никогаш не го запира претворањето, со или без интернет). Кога има ново издание, командата прашува пред да го инсталира: `git clone` се ажурира со `git pull --ff-only` (одбива додека имате локални промени), а преземена копија од архивата на изданието. `HEAT3D_NO_UPDATE=1` ги исклучува проверката и ажурирањето.

---

Дел од [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
