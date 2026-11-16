---
title: "Skilmálar og leyfi"
nav_order: 16
lang: "is"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Skilmálar og leyfi {#terms-and-licence}

## Hvað er lesið {#what-it-reads}

Breytirinn les upptökurnar sem War Thunder vistar á tölvunni þinni (eða upptökur af orrustum þínum sem þú sóttir af warthunder.com) og borðaskrárnar úr þinni eigin War Thunder-uppsetningu. Ekkert úr leiknum fylgir hér með eða er dreift áfram: engin leikjagögn, enginn leikjakóði, engar DLL-skrár; Oodle er hlaðið úr þinni eigin uppsetningu. Það sem hann skrifar verður eftir á tölvunni þinni: **birtu borðin aldrei**.

3DHeat tengist ekki Gaijin Entertainment og er ekki samþykkt af Gaijin Entertainment. War Thunder og tengd heiti og vörumerki tilheyra eigendum sínum.

Rétthafar: stofnið issue á <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - við svörum fljótt og fjarlægjum hvað sem er sé þess óskað.

## Heimildir {#sources}

Allur kóði hér er skrifaður fyrir þetta verkefni; enginn kóði var afritaður úr öðrum lesara. Það
sem hann veit um sniðið kemur frá:

- Frumkóða Dagor Engine frá Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` og `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` fyrir einingastrauminn (`ecs.py`), og `net/message.cpp`
  (`MessageClass::initImpl`) fyrir hvernig einingarskilaboð númera flokka sína. Heiti íhluta og tegunda
  eru pöruð með FNV-1a tætigildum þeirra við orð úr eigin
  safnskrám leiksins; `ecs.py` telur upp nöfnin sem fundust.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  og `daNet/bitStream.h` úr sama frumkóða: hvernig skilaboð nefna hlutinn sem þau eru fyrir
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, og eigin lesari þess
  `web/wrpl-parse.js`, lesið fyrir bitaútlit flugmódelsins, landsamstillingar,
  vopna á flugi, auðkennisreitaskilaboða, spilararaufa, stjórnklefagilda
  og tvíundar blk. WTACRP nefnir maxsupermanhd/wrpl-inspector,
  wt_blk og wrpl-acmi (AGPL-3.0) sem eigin heimildir; kóði þeirra var ekki
  lesinn hér.
- Eigin upptökur höfundar, lesnar sem skrár: munurinn á 2025 (eldra útlit
  flugmódelsins, spjall án fánabætis, zlib), afstaða landeininga, frávik
  pakkaðrar hæðar, losunarpunktar vopna og mælar stjórnklefans
  voru unnir út á þeim hér.

## Prófanir {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Einingaprófanirnar lesa aldrei uppsetningu (`HEAT3D_WT_NO_NAMES` er stillt); prófið
með þínum eigin upptökum les nöfnin úr þinni uppsetningu.

Prófanirnar smíða upptökur í kóða (`tests/synth.py`: haus, pakkar, niðurstöður,
einingastraumurinn, vopn á flugi) samkvæmt útlitinu sem lesararnir skjalfesta; engin
upptaka er í geymslunni.

## Leyfi {#licence}

MIT - sjá [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Notar pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) og Pillow (MIT-CMU). Borðslesararnir voru skrifaðir
út frá frumkóða Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause leyfi; enginn kóði úr honum er afritaður hér, og sniðfastarnir sem eru notaðir
(vromfs XOR-lykillinn, offset hæðarsviðsnetsins) eru tilgreindir þar sem þeir birtast.

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Kóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
