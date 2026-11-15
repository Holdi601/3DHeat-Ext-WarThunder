---
title: Условия и лиценз
nav_order: 16
lang: bg
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Условия и лиценз {#terms-and-licence}

## Условията {#the-terms}

Условията за ползване на Gaijin (актуализирани на 2026-08-17), EULA (Приложение 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
извън клиента. Четенето на файловете с нива от вашето собствено копие на играта в локален 3D изглед е решение
на потребителя, взето с пълно знание за това. Записаните нива остават на вашия
компютър: **никога не ги публикувайте**, а нищо тук не носи игрални данни.

## Източници {#sources}

Целият код тук е написан за този проект; никакъв код не е копиран от друг парсер. Това, което знае
за формата, идва от:

- Изходният код на Dagor Engine на Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` и `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` за потока на същностите (`ecs.py`), и `net/message.cpp`
  (`MessageClass::initImpl`) за това как съобщенията за същности номерират класовете си. Имената на компонентите и
  типовете се съпоставят по хешовете им FNV-1a с думи от собствените архиви на играта;
  `ecs.py` изброява намерените имена.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` и `daNet/bitStream.h` от същия
  код: как съобщението назовава обекта, за който е (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` и собствения му парсер
  `web/wrpl-parse.js`, прочетени за битовите разположения на полетния модел, наземната
  синхронизация, оръжията в полет, съобщенията с полета идентификатор, слотовете на играчите, стойностите на кабината и
  двоичния blk. WTACRP назовава като свои справки maxsupermanhd/wrpl-inspector,
  wt_blk и wrpl-acmi (AGPL-3.0); техният код не е четен тук.
- Собствените повторения на автора, прочетени като файлове: разликите от 2025 г. (по-старото
  разположение на полетния модел, чат без байт за флаг, zlib), наземното положение, опакованото
  отместване на височината, точките на освобождаване на оръжията и инструментите на кабината са установени тук върху тях.

## Тестове {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Модулните тестове никога не четат инсталация (`HEAT3D_WT_NO_NAMES` е зададена); тестът
с вашите собствени повторения чете имената от вашата инсталация.

Тестовете създават повторения в кода (`tests/synth.py`: заглавие, пакети, резултати,
поток от същности, оръжия в полет) по разположението, което описват четците; в хранилището няма
нито едно повторение.

## Лиценз {#licence}

MIT – вижте [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Ползва pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) и Pillow (MIT-CMU). Четците на нивата са написани
по изходния код на Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, лиценз BSD
3-Clause; никакъв код от него не е копиран тук, а константите на формата, които се ползват
(XOR ключът на vromfs, отмествания на решетката за диапазона на височините), са посочени там, където се появяват.

---

Част от [3DHeat](https://github.com/Holdi601/3DHeat) ([документация](https://holdi601.github.io/3DHeat/)). Източник: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
