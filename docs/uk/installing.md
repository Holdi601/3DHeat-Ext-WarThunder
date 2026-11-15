---
title: "Встановлення"
nav_order: 3
lang: uk
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Встановлення {#installing}

Ви ще не працювали з командним рядком? Спочатку прочитайте
[Перш ніж почати](before-you-start.md).
Потрібен Python 3.10 або новіший; pyarrow, numpy, zstandard і Pillow
встановлюються разом із ним.

## Крок за кроком {#step-by-step}

1. Отримайте код: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`
   або завантажте архів із [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   і розпакуйте його.
2. Відкрийте термінал у цій папці і введіть `pip install -e .`. Це встановлює
   дві команди: `heat3d-wt-replay` (повтори) і `heat3d-wt-level` (рівні).
3. Перевірте: `heat3d-wt-replay --version`. Ви маєте побачити
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` показує опції:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без встановлення: `python -m heat3d_ext_warthunder ...` і
`python -m heat3d_ext_warthunder.levelcli ...` у папці інструмента.

## Назви з вашої гри {#names-from-your-install}

Техніка, зброя і боєприпаси отримують англійські назви з текстових файлів самої
гри, які читаються з вашої встановленої гри під час перетворення. Встановлення
знаходиться через Steam або типові папки лаунчера; `--game <folder>` або змінна
середовища `HEAT3D_WT_GAME` вказують інше місце. Текст гри не зберігається в цьому
репозиторії; без встановлення назвами будуть ідентифікатори техніки (конвертер
попереджає про це рядком `note:`).

## Оновлення {#updates}

Під час кожного запуску спочатку перевіряються релізи проєкту на GitHub (не
частіше ніж раз на кілька годин; це ніколи не зупиняє перетворення, онлайн чи
офлайн). Коли новіший реліз готовий, команда питає, чи встановлювати його:
`git clone` оновлюється через `git pull --ff-only` (відмовляє, поки є ваші
локальні зміни), завантажена копія — з архіву релізу. `HEAT3D_NO_UPDATE=1`
вимикає перевірку і оновлення.

---

Частина [3DHeat](https://github.com/Holdi601/3DHeat) ([документація](https://holdi601.github.io/3DHeat/)). Джерело: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
