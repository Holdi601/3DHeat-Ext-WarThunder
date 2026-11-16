---
title: Terms and licence
nav_order: 16
---

# Terms and licence

## What it reads

The converter reads the replays War Thunder saves on your computer (or replays
of your battles that you downloaded yourself from warthunder.com) and the level
files of your own War Thunder installation. Nothing from the game is included
or redistributed here: no game assets, no game code, no DLLs; Oodle is loaded
from your own install. What it writes stays on your machine: **never publish
the levels**.

3DHeat is not affiliated with or endorsed by Gaijin Entertainment. War Thunder
and related names and trademarks belong to their owners.

Rights holders: open an issue at
<https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - we respond quickly
and remove anything on request.

## Sources

All code here is written for this project; no code was copied from another parser. What
it knows of the format comes from:

- Gaijin's Dagor Engine source (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` and `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` for the entity stream (`ecs.py`), and `net/message.cpp`
  (`MessageClass::initImpl`) for how entity messages number their classes. Component and type
  names are matched by their FNV-1a hashes against words of the game's own
  archives; `ecs.py` lists the names found.
- The same source's `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  and `daNet/bitStream.h`: how a message names the object it is for
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, and its own parser
  `web/wrpl-parse.js`, read for the bit layouts of the flight model, ground
  sync, weapons in flight, id-field messages, player slots, the cockpit
  values and the binary blk. WTACRP names maxsupermanhd/wrpl-inspector,
  wt_blk and wrpl-acmi (AGPL-3.0) as its own references; their code was not
  read here.
- The author's own replays, read as files: the 2025 differences (the flight model's older
  layout, chat without a flag byte, zlib), the ground attitude, the packed
  height offset, the weapons' release points and the cockpit instruments were
  worked out on them here.

## Tests

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

The unit tests never read an install (`HEAT3D_WT_NO_NAMES` is set); the test
with your own replays reads the names from your install.

The tests build replays in code (`tests/synth.py`: header, packets, results,
the entity stream, weapons in flight) to the layout the readers document; no
replay is in the repository.

## Licence

MIT - see [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Uses pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) and Pillow (MIT-CMU). The level readers were written
from the Dagor Engine's source, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause licence; no code of it is copied here, and the format constants used
(the vromfs XOR key, the height-range grid offsets) are cited where they appear.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
