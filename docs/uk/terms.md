---
title: "Умови і ліцензія"
nav_order: 16
lang: uk
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Умови і ліцензія {#terms-and-licence}

## Умови {#the-terms}

Умови надання послуг Gaijin (оновлено 2026-08-17), EULA (Додаток 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Читання файлів рівнів з вашої власної копії гри в локальний
3D-перегляд — це рішення користувача, ухвалене з усвідомленням цього. Записані
рівні залишаються на вашому комп'ютері: **ніколи не публікуйте їх**, і ніщо тут
не постачає жодних даних гри.

## Джерела {#sources}

Весь код тут написано для цього проєкту; жоден код не скопійовано з іншого
парсера. Те, що він знає про формат, походить із:

- Вихідного коду Dagor Engine від Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` та `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` для потоку сутностей (`ecs.py`), і `net/message.cpp`
  (`MessageClass::initImpl`) для того, як повідомлення сутностей нумерують свої
  класи. Назви компонентів і типів зіставляються з їхніми хешами FNV-1a зі словами
  власних архівів гри; `ecs.py` перелічує знайдені назви.
- Тих самих `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` і
  `daNet/bitStream.h` вихідного коду: як повідомлення називає об'єкт, для якого
  воно (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` і його власний парсер
  `web/wrpl-parse.js`, прочитані для бітових розкладок льотної моделі, наземної
  синхронізації, зброї в польоті, повідомлень з полями id, слотів гравців,
  значень кабіни і бінарного blk. WTACRP називає як свої посилання
  maxsupermanhd/wrpl-inspector, wt_blk і wrpl-acmi (AGPL-3.0); їхній код тут не
  читали.
- Власні повтори автора, прочитані як файли: відмінності 2025 року (старіша
  розкладка льотної моделі, чат без байта прапорця, zlib), орієнтація наземних
  юнітів, упакований зсув висоти, точки скидання зброї і прилади кабіни було
  з'ясовано саме на них.

## Тести {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # також перевіряє публічні зразки повторів 2025 року
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # кроки, ідентичності, прапорці ШІ, знак крену, згладжувач, назви
```

Модульні тести ніколи не читають встановлення (`HEAT3D_WT_NO_NAMES` задано);
тест з вашими власними повторами читає назви з вашої встановленої гри.

Тести будують повтори в коді (`tests/synth.py`: заголовок, пакети, результати,
потік сутностей, зброя в польоті) за розкладкою, яку описують читачі; жодного
повтору в репозиторії немає.

## Ліцензія {#licence}

MIT — див. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE).
Використовуються pyarrow (Apache-2.0), numpy (BSD-3-Clause), zstandard
(BSD-3-Clause) і Pillow (MIT-CMU). Читачі рівнів написані за вихідним кодом Dagor
Engine, Copyright (c) 2023 Gaijin Entertainment, ліцензія BSD 3-Clause; жодного
коду з нього тут не скопійовано, а константи формату, які використовуються
(ключ XOR для vromfs, зміщення сітки діапазону висот), наведено там, де вони
з'являються.

---

Частина [3DHeat](https://github.com/Holdi601/3DHeat) ([документація](https://holdi601.github.io/3DHeat/)). Джерело: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
