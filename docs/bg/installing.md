---
title: Инсталиране
nav_order: 3
lang: bg
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Инсталиране {#installing}

Нов ли сте в командния ред? Първо прочетете [Преди да започнете](before-you-start.md).
Нужен е Python 3.10 или по-нов; pyarrow, numpy, zstandard и Pillow се инсталират заедно с него.

## Стъпка по стъпка {#step-by-step}

1. Вземете кода: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   или изтеглете zip от [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   и го разархивирайте.
2. Отворете терминал в тази папка и напишете `pip install -e .`. Това инсталира
   две команди: `heat3d-wt-replay` (повторения) и `heat3d-wt-level` (нива).
3. Проверете: `heat3d-wt-replay --version`. Трябва да видите
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` показва опциите:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без инсталиране: `python -m heat3d_ext_warthunder ...` и
`python -m heat3d_ext_warthunder.levelcli ...` в папката на инструмента.

## Имена от вашата инсталация {#names-from-your-install}

Техниките, оръжията и боеприпасите получават своите английски имена от текстовите
файлове на самата игра, четени от вашата инсталация при преобразуването. Инсталацията се
намира чрез Steam или стандартните папки на стартера; `--game <папка>` или
променливата на средата `HEAT3D_WT_GAME` показват къде е, ако не е там. Нищо от текста на
играта не се съдържа в това хранилище; без инсталация имената са идентификаторите на
техниките (преобразувателят казва това с ред `note:`).

## Обновявания {#updates}

При всеки старт първо се проверяват GitHub изданията на проекта (най-много една заявка
на няколко часа; никога не спира преобразуването, онлайн или офлайн). Когато има по-ново
издание, командата пита, преди да го инсталира: `git clone` се обновява с
`git pull --ff-only` (отказва, докато имате локални промени), а изтеглено копие – от
архива на издането. `HEAT3D_NO_UPDATE=1` изключва проверката и обновяването.

---

Част от [3DHeat](https://github.com/Holdi601/3DHeat) ([документация](https://holdi601.github.io/3DHeat/)). Източник: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
