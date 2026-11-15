---
title: Инсталација
nav_order: 3
lang: "sr"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Инсталација {#installing}

Први пут у командној линији? Прво прочитајте [Пре почетка](before-you-start.md).
Потребан је Python 3.10 или новији; pyarrow, numpy, zstandard и Pillow се
инсталирају с њим.

## Корак по корак {#step-by-step}

1. Преузмите код: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   или преузмите зип са [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   и распакујте га.
2. Отворите терминал у тој фасцикли и укуцајте `pip install -e .`. Ово инсталира
   две команде: `heat3d-wt-replay` (реплеји) и `heat3d-wt-level` (нивои).
3. Проверите: `heat3d-wt-replay --version`. Требало би да видите
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` исписује опције:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без инсталирања: `python -m heat3d_ext_warthunder ...` и
`python -m heat3d_ext_warthunder.levelcli ...` у фасцикли алатке.

## Називи из ваше инсталације {#names-from-your-install}

Возила, оружја и муниција добијају своје енглеске називе из текстуалних
датотека саме игре, које се при претварању читају из ваше инсталације. Инсталација
се налази преко Steam-а или подразумеваних фасцикли покретача; `--game <folder>`
или променљива окружења `HEAT3D_WT_GAME` кажу где је иначе. Ниједан текст игре
није у овом репозиторијуму; без инсталације називи су ид-еви возила (конвертор то
каже у реду `note:`).

## Ажурирања {#updates}

Сваки старт прво проверава GitHub издања пројекта (највише једном у
неколико сати; никад не зауставља претварање, на мрежи или ван ње). Кад је
нова верзија изашла, команда пита пре инсталације: `git clone` се ажурира
помоћу `git pull --ff-only` (одбија се док имате локалне измене), а преузета
копија из архиве издања. `HEAT3D_NO_UPDATE=1` искључује проверу и ажурирање.

---

Део [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
