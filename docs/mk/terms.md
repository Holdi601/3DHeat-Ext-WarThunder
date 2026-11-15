---
title: "Услови и лиценца"
nav_order: 16
lang: "mk"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Услови и лиценца {#terms-and-licence}

## Условите {#the-terms}

Условите за користење на Gaijin (ажурирани 2026-08-17), EULA (Annex 2): 3.2.2 „modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the Game(s)“, 3.2.9 „mine or collect any data from the Game(s) that is not intended to be publicly displayed“; 1.2 „are not permitted to store, download, modify, or otherwise use any part of the Game(s)“ надвор од клиентот. Читањето на датотеките на нивоата од вашата сопствена копија во локален 3D приказ е одлука на корисникот, донесена со знаење за ова. Напишаните нивоа остануваат на вашата машина: **никогаш не ги објавувајте**, и ништо тука не испорачува податоци од играта.

## Извори {#sources}

Сиот код тука е напишан за овој проект; ниту еден код не е копиран од друг парсер. Она што го знае за форматот доаѓа од:

- Изворот на Dagor Engine на Gaijin (github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h` и `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` за текот на ентитети (`ecs.py`), и `net/message.cpp` (`MessageClass::initImpl`) за тоа како пораките на ентитетите ги нумерираат своите класи. Имињата на компоненти и типови се совпаѓаат по нивните FNV-1a хешови со зборови од сопствените архиви на играта; `ecs.py` ги наведува најдените имиња.
- Истиот извор `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` и `daNet/bitStream.h`: како пораката го именува објектот за кој е наменета (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, и неговиот сопствен парсер `web/wrpl-parse.js`, читани за распоредот на битови на летачкиот модел, копнената синхронизација, оружјата во лет, пораките со ид полиња, играчките слотови, вредностите од кабината и бинарниот blk. WTACRP ги именува maxsupermanhd/wrpl-inspector, wt_blk и wrpl-acmi (AGPL-3.0) како свои референци; нивниот код тука не беше читан.
- Сопствените снимки на авторот, читани како датотеки: разликите од 2025 (постариот распоред на летачкиот модел, разговор без бајт за знаменце, zlib), положбата на копното, поместувањето на спакуваната височина, точките на испуштање на оружјата и инструментите во кабината беа изработени врз нив тука.

## Тестови {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Тестовите на единици никогаш не читаат инсталација (поставено е `HEAT3D_WT_NO_NAMES`); тестот со вашите сопствени снимки ги чита имињата од вашата инсталација.

Тестовите градат снимки во код (`tests/synth.py`: заглавие, пакети, резултати, тек на ентитети, оружја во лет) според распоредот што го документираат читачите; ниту една снимка не е во складиштето.

## Лиценца {#licence}

MIT - видете [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Користи pyarrow (Apache-2.0), numpy (BSD-3-Clause), zstandard (BSD-3-Clause) и Pillow (MIT-CMU). Читачите на нивоа се напишани според изворот на Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, лиценца BSD 3-Clause; ниту еден негов код не е копиран тука, а користените константи на форматот (XOR клучот на vromfs, поместувањата на мрежата на опсегот на височини) се цитирани таму каде што се појавуваат.

---

Дел од [3DHeat](https://github.com/Holdi601/3DHeat) ([документација](https://holdi601.github.io/3DHeat/)). Извор: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
