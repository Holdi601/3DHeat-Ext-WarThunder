---
title: "Termini u liċenzja"
nav_order: 16
lang: mt
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Termini u liċenzja {#terms-and-licence}

## It-termini {#the-terms}

It-Termini tas-Servizz ta' Gaijin (aġġornati 2026-08-17), EULA (Annex 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
lil hinn mill-klijent. Li taqra l-fajls tal-livelli tal-kopja tiegħek stess f'veduta 3D lokali
hija d-deċiżjoni tal-utent, meħuda b'taf dan. Il-livelli miktuba jibqgħu fuq il-magna tiegħek:
**qatt ma tippubblikahom**, u xejn hawn ma jġib data tal-logħba.

## Sorsi {#sources}

Kull kodiċi hawn inkiteb għal dan il-proġett; ebda kodiċi ma ġie kkupjat minn parser ieħor. Dak li
jaf dwar il-format jiġi minn:

- Is-sors tad-Dagor Engine ta' Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` u `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` għall-fluss tal-entitajiet (`ecs.py`), u `net/message.cpp`
  (`MessageClass::initImpl`) għal kif il-messaġġi tal-entitajiet jinnumeraw il-klassijiet tagħhom. L-ismijiet
  tal-komponenti u tat-tipi jitqabblu bl-FNV-1a hashes tagħhom ma' kliem mill-arkivji proprji tal-logħba;
  `ecs.py` jelenka l-ismijiet misjuba.
- L-istess sors `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  u `daNet/bitStream.h`: kif messaġġ jsemmi l-oġġett li huwa għalih
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, u l-parser tiegħu stess
  `web/wrpl-parse.js`, moqrijin għal-layouts tal-bits tal-flight model, ground
  sync, armi fit-titjira, messaġġi tal-kampi tal-id, slots tal-plejers, il-valuri tal-cockpit
  u l-blk binarju. WTACRP isemmi maxsupermanhd/wrpl-inspector,
  wt_blk u wrpl-acmi (AGPL-3.0) bħala r-referenzi tiegħu stess; il-kodiċi tagħhom ma nqarax
  hawn.
- Ir-ripetizzjonijiet proprji tal-awtur, moqrijin bħala fajls: id-differenzi tal-2025 (il-layout
  eqdem tal-flight model, chat mingħajr byte ta' flag, zlib), l-attitudni tal-art, l-offset tal-għoli
  ippakkjat, il-punti tar-rilaxx tal-armi u l-istrumenti tal-cockpit ġew
  magħmula fuqhom hawn.

## Testijiet {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

It-testijiet tal-unit qatt ma jaqraw installazzjoni (`HEAT3D_WT_NO_NAMES` huwa mqiegħed); it-test
bir-ripetizzjonijiet tiegħek stess jaqra l-ismijiet mill-installazzjoni tiegħek.

It-testijiet jibnu ripetizzjonijiet fil-kodiċi (`tests/synth.py`: header, pakketti, riżultati,
il-fluss tal-entitajiet, armi fit-titjira) bil-layout li jiddokumentaw il-qarrejja; ebda
ripetizzjoni mhi fir-repożitorju.

## Liċenzja {#licence}

MIT - ara [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Juża pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) u Pillow (MIT-CMU). Il-qarrejja tal-livelli nkitbu
mis-sors tad-Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, liċenzja BSD
3-Clause; ebda kodiċi minnu ma huwa kkupjat hawn, u l-kostanti tal-format użati
(iċ-ċavetta XOR tal-vromfs, l-offsets tal-grid tal-firxa tal-għoli) huma ċitati fejn jidhru.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
