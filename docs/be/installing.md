---
title: "Усталёўка"
nav_order: 3
lang: "be"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Усталёўка {#installing}

Вы новічок у камандным радку? Спачатку прачытайце [Перад пачаткам](before-you-start.md).
Патрэбны Python 3.10 або навейшы; pyarrow, numpy, zstandard і Pillow
усталёўваюцца разам з ім.

## Крок за крокам {#step-by-step}

1. Атрымайце код: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`
   або спампуйце zip з [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   і распакуйце яго.
2. Адкрыйце тэрмінал у гэтай папцы і ўвядзіце `pip install -e .`. Гэта
   ўсталёўвае дзве каманды: `heat3d-wt-replay` (запісы) і `heat3d-wt-level`
   (узроўні).
3. Праверце: `heat3d-wt-replay --version`. Вы павінны ўбачыць
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` пералічвае параметры:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без усталёўкі: `python -m heat3d_ext_warthunder ...` і
`python -m heat3d_ext_warthunder.levelcli ...` у папцы інструмента.

## Назвы з вашай усталёўкі {#names-from-your-install}

Машыны, зброя і боепрыпасы атрымліваюць англійскія назвы з уласных тэкставых
файлаў гульні, якія чытаюцца з вашай усталёўкі пры канвертаванні.
Усталёўка знаходзіцца праз Steam або стандартныя папкі лаунчара; калі не, то
`--game <folder>` або зменная асяроддзя `HEAT3D_WT_GAME` кажуць, дзе яна.
Нічога з тэксту гульні ў гэтым рэпазіторыі няма; без усталёўкі назвамі
з'яўляюцца id машын (канвертар кажа пра гэта ў радку `note:`).

## Абнаўленні {#updates}

Кожны запуск спачатку правярае рэлізы праекта ў GitHub (не болей за адзін
запыт на некалькі гадзін; ён ніколі не спыняе канвертаванне, ці ёсць сетка,
ці няма). Калі выйшаў навейшы рэліз, каманда пытаецца перад ўсталёўкай:
`git clone` абнаўляецца праз `git pull --ff-only` (адмаўляецца, пакуль у вас
ёсць лакальныя змены), спампаваная копія - з архіва рэлізу.
`HEAT3D_NO_UPDATE=1` выключае праверку і абнаўленне.

---

Частка [3DHeat](https://github.com/Holdi601/3DHeat) ([дакументацыя](https://holdi601.github.io/3DHeat/)). Крыніца: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
