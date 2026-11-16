---
title: "Podmínky a licence"
nav_order: 16
lang: "cs"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Podmínky a licence {#terms-and-licence}

## Co se čte {#what-it-reads}

Převodník čte replaye, které War Thunder ukládá na váš počítač (nebo replaye vašich bitev, které jste si sami stáhli z warthunder.com), a soubory úrovní z vaší vlastní instalace War Thunder. Nic ze hry tu není obsaženo ani dále šířeno: žádná herní data, žádný herní kód, žádné DLL; Oodle se načítá z vaší vlastní instalace. Co zapíše, zůstává na vašem počítači: **úrovně nikdy nezveřejňujte**.

3DHeat není přidružen ke společnosti Gaijin Entertainment ani jí schválen. War Thunder a související názvy a ochranné známky patří jejich vlastníkům.

Držitelé práv: založte issue na <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - odpovídáme rychle a na požádání cokoli odstraníme.

## Zdroje {#sources}

Veškerý kód je napsán pro tento projekt; žádný kód nebyl zkopírován z jiného čtení formátu. Co
o formátu ví, pochází z:

- zdrojového kódu Dagor Engine od Gaijinu (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` a `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` pro proud entit (`ecs.py`), a `net/message.cpp`
  (`MessageClass::initImpl`) pro to, jak zprávy entit číslují své třídy. Názvy komponent a typů se páruje
  jejich hashe FNV-1a se slovy z vlastních archivů hry; `ecs.py` vypisuje nalezené názvy.
- stejného zdroje `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  a `daNet/bitStream.h`: jak zpráva jmenuje objekt, pro který je (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` a jeho vlastní čtečka
  `web/wrpl-parse.js`, čtené kvůli bitovým rozložením letového modelu, pozemní synchronizace, zbraní za letu,
  zpráv s id poli, slotů hráčů, hodnot kokpitu a binárního blk. WTACRP jmenuje jako své vlastní reference
  maxsupermanhd/wrpl-inspector, wt_blk a wrpl-acmi (AGPL-3.0); jejich kód zde přečten nebyl.
- replayů autora samotného, čtených jako soubory: rozdíly roku 2025 (starší rozložení letového modelu, chat bez
  bajtu příznaků, zlib), postoj na zemi, posun zabalené výšky, body vypuštění zbraní a palubní přístroje byly
  zde odvozeny právě z nich.

## Testy {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # ověří i veřejné ukázkové replaye 2025
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # kroky, identity, příznaky AI, znaménko náklonu, vyhlazovač, názvy
```

Jednotkové testy nikdy nečtou instalaci (`HEAT3D_WT_NO_NAMES` je nastaveno); test
s vašimi vlastními replayi čte názvy z vaší instalace.

Testy vytvářejí replaye v kódu (`tests/synth.py`: hlavička, pakety, výsledky,
proud entit, zbraně za letu) podle rozložení, které čtečky dokumentují; v repozitáři
není žádný replay.

## Licence {#licence}

MIT - viz [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Používá pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) a Pillow (MIT-CMU). Čtečky úrovní byly napsány
podle zdrojového kódu Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licence BSD
3-Clause; žádný jeho kód se zde nekopíruje a použité konstanty formátu (XOR klíč vromfs,
posuny mřížky rozsahu výšek) jsou uvedeny tam, kde se objevují.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
