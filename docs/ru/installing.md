---
title: Установка
nav_order: 3
lang: "ru"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Установка {#installing}

Впервые работаете с командной строкой? Сначала прочитайте [Перед началом](before-you-start.md).
Нужен Python 3.10 или новее; pyarrow, numpy, zstandard и Pillow устанавливаются вместе с ним.

## Пошагово {#step-by-step}

1. Получите код: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`
   или скачайте архив из [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   и распакуйте его.
2. Откройте терминал в этой папке и введите `pip install -e .`. Установятся две
   команды: `heat3d-wt-replay` (реплеи) и `heat3d-wt-level` (уровни).
3. Проверьте: `heat3d-wt-replay --version`. Вы должны увидеть
   `heat3d-wt-replay 0.2.0`. Команда `heat3d-wt-replay --help` покажет параметры:

![heat3d-wt-replay --help](../assets/img/help.svg)

Без установки: `python -m heat3d_ext_warthunder ...` и
`python -m heat3d_ext_warthunder.levelcli ...` в папке инструмента.

## Названия из вашей установки {#names-from-your-install}

Техника, оружие и боеприпасы получают английские названия из текстовых файлов самой
игры. Они читаются из вашей установки во время преобразования. Установку находят
через Steam или папки по умолчанию у лаунчера; иначе, где она лежит, указывают
`--game <folder>` или переменная окружения `HEAT3D_WT_GAME`. Текста игры в этом
репозитории нет; без установки вместо названий будут идентификаторы техники
(преобразователь сообщит об этом в строке `note:`).

## Обновления {#updates}

При каждом запуске сначала проверяются релизы проекта на GitHub (не чаще одного
запроса в несколько часов; проверка никогда не останавливает преобразование, онлайн
или нет). Когда выходит новый релиз, команда спрашивает, ставить ли его. Копия из
`git clone` обновляется командой `git pull --ff-only` (отказывается работать, пока
есть локальные изменения), скачанная копия — из архива релиза. Переменная
`HEAT3D_NO_UPDATE=1` выключает и проверку, и обновление.

---

Часть [3DHeat](https://github.com/Holdi601/3DHeat) ([документация](https://holdi601.github.io/3DHeat/)). Исходный код: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
