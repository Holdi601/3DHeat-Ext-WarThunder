---
title: Услови и лиценца
nav_order: 16
lang: "sr"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Услови и лиценца {#terms-and-licence}

## Шта се чита {#what-it-reads}

Конвертор чита реплеје које War Thunder чува на вашем рачунару (или реплеје ваших битака које сте сами преузели са warthunder.com) и датотеке нивоа из ваше сопствене инсталације War Thunder-а. Ништа из игре није укључено нити се даље дистрибуира: нема садржаја игре, кода игре ни DLL-ова; Oodle се учитава из ваше сопствене инсталације. Оно што запише остаје на вашем рачунару: **никад не објављујте нивое**.

3DHeat није повезан са компанијом Gaijin Entertainment нити га она подржава. War Thunder и повезани називи и жигови припадају својим власницима.

Носиоци права: отворите issue на <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - брзо одговарамо и на захтев уклањамо било шта.

## Извори {#sources}

Сав код овде је написан за овај пројекат; ниједан код није копиран из другог
парсера. Оно што зна о формату долази из:

- Gaijin-овог извора Dagor Engine-а (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` и `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` за ток ентитета (`ecs.py`), и `net/message.cpp`
  (`MessageClass::initImpl`) за то како ентитетске поруке нумеришу своје класе.
  Називи компоненти и типова упоређују се по њиховим FNV-1a хешевима с речима из
  игриних сопствених архива; `ecs.py` наводи нађене називе.
- Исти извор `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` и
  `daNet/bitStream.h`: како порука именује објекат за који је (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, и његов сопствени парсер
  `web/wrpl-parse.js`, прочитани ради распореда битова модела лета, стања копна,
  оружја у лету, порука с ид-поља, слотова играча, вредности кабине и бинарног blk-а.
  WTACRP наводи maxsupermanhd/wrpl-inspector, wt_blk и wrpl-acmi (AGPL-3.0) као своје
  референце; њихов код овде није прочитан.
- Сопствени реплеји аутора, читани као датотеке: разлике 2025 (старији распоред модела
  лета, ћаскање без бајта заставице, zlib), став копна, помак спаковане висине,
  тачке испуштања оружја и инструменти кабине су овде израчунати на њима.

## Тестови {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Јединични тестови никад не читају инсталацију (`HEAT3D_WT_NO_NAMES` је постављен);
тест с вашим сопственим реплејима чита називе из ваше инсталације.

Тестови граде реплеје у коду (`tests/synth.py`: заглавље, пакети, резултати, ток
ентитета, оружје у лету) по распореду који читачи документују; ниједан реплеј није у
репозиторијуму.

## Лиценца {#licence}

MIT - видите [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Користите pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) и Pillow (MIT-CMU). Читачи нивоа су написани по извору
Dagor Engine-а, Copyright (c) 2023 Gaijin Entertainment, лиценца BSD 3-Clause; ниједан
његов код није копиран овде, а константе формата које се користе (XOR кључ vromfs-а,
помаци мреже опсега висина) наведене су тамо где се појављују.

---

Део [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
