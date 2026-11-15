---
title: Условия и лицензия
nav_order: 16
lang: "ru"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Условия и лицензия {#terms-and-licence}

## Условия {#the-terms}

Условия использования Gaijin (обновлены 2026-08-17), EULA (Приложение 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Чтение файлов уровней из собственной копии игры для локального
трёхмерного просмотра — решение пользователя, принятое с учётом этого. Записанные
уровни остаются на вашем компьютере: **никогда не публикуйте их**, а здесь никакие
данные игры не поставляются.

## Источники {#sources}

Весь код здесь написан специально для этого проекта; ни один код не скопирован из
другого парсера. То, что известно о формате, взято из:

- Исходного кода движка Dagor Engine от Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` и `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` для потока сущностей (`ecs.py`), и `net/message.cpp`
  (`MessageClass::initImpl`) для того, как сообщения сущностей нумеруют свои классы.
  Имена компонентов и типов сопоставляются по их хешам FNV-1a со словами из собственных
  архивов игры; `ecs.py` перечисляет найденные имена.
- Тех же исходников `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  и `daNet/bitStream.h`: как сообщение называет объект, которому оно адресовано
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, а также его собственный парсер
  `web/wrpl-parse.js`, прочитанные ради битовых раскладок модели полёта, синхронизации
  наземной техники, снарядов в полёте, сообщений с полем id, слотов игроков, значений
  кабины и бинарного blk. WTACRP называет своими ссылками maxsupermanhd/wrpl-inspector,
  wt_blk и wrpl-acmi (AGPL-3.0); их код здесь не читался.
- Собственных реплеев автора, прочитанных как файлы: различия 2025 года (более старая
  раскладка модели полёта, чат без байта флагов, zlib), наземная ориентация, упакованное
  смещение высоты, точки отпуска оружия и приборы кабины были выяснены здесь именно на них.

## Тесты {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Модульные тесты никогда не читают установку (`HEAT3D_WT_NO_NAMES` задан); тест
с вашими собственными реплеями берёт названия из вашей установки.

Тесты строят реплеи в коде (`tests/synth.py`: заголовок, пакеты, результаты, поток
сущностей, снаряды в полёте) в той раскладке, которую описывают читатели; ни одного
реплея в репозитории нет.

## Лицензия {#licence}

MIT — см. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Используются pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) и Pillow (MIT-CMU). Читатели уровней написаны по исходному
коду Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, лицензия BSD
3-Clause; никакой их код здесь не скопирован, а константы формата, которые используются
(ключ XOR для vromfs, смещения сетки диапазона высот), указаны там, где они встречаются.

---

Часть [3DHeat](https://github.com/Holdi601/3DHeat) ([документация](https://holdi601.github.io/3DHeat/)). Исходный код: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
