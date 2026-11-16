---
title: "Konditiounen a Lizenz"
nav_order: 16
lang: "lb"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Konditiounen a Lizenz {#terms-and-licence}

## Wat gelies gëtt {#what-it-reads}

De Konverter liest d'Replays, déi War Thunder op Ärem Computer späichert (oder Replays vun Äre Schluechten, déi Dir selwer vu warthunder.com erofgelueden hutt), an d'Level-Dateie vun Ärer eegener War-Thunder-Installatioun. Näischt aus dem Spill ass hei dran oder gëtt weiderverdeelt: keng Spill-Assets, kee Spillcode, keng DLLen; Oodle gëtt aus Ärer eegener Installatioun gelueden. Wat e schreift, bleift op Ärer Maschinn: **verëffentlecht d'Leveln ni**.

3DHeat ass net mat Gaijin Entertainment verbonnen an net vun Gaijin Entertainment ënnerstëtzt. War Thunder an déi verbonnen Nimm a Marken gehéieren hiren Eegentümer.

Rechteinhaber: maacht en Issue op <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> op - mir äntweren séier an huelen op Ufro alles erof.

## Quellen {#sources}

Dee ganze Code hei ass fir dëse Projet geschriwwen; et gouf kee Code vun engem anere Parser kopéiert. Wat
en iwwert d'Format weess, kënnt vun:

- Dem Gaijin säi Dagor-Engine-Quellcode (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` an `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` fir den Entitéit-Stroum (`ecs.py`), an `net/message.cpp`
  (`MessageClass::initImpl`) dofir, wéi Entitéit-Messagen hir Klassen nummeréieren. Komponent- an Typ-
  Nimm ginn iwwer hir FNV-1a-Hashen mat Wierder aus den eegenen Archive vum Spill
  zesummegebracht; `ecs.py` lëscht déi fonnte Nimm op.
- Dem selwechte Quellcode säi `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  an `daNet/bitStream.h`: wéi eng Message d'Objet nennt, fir dat se ass
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, a säin eegene Parser
  `web/wrpl-parse.js`, gelies fir d'Bit-Layouten vum Flugmodell, vum Buedem-
  Sync, vun de Waffen am Fluch, vun den ID-Feld-Messagen, de Spiller-Slots, de Cockpit-
  Wäerter an dem binäre blk. WTACRP nennt maxsupermanhd/wrpl-inspector,
  wt_blk a wrpl-acmi (AGPL-3.0) als seng eege Referenzen; hire Code gouf hei net
  gelies.
- Dem Auteur seng eege Replays, als Dateie gelies: d'Ënnerscheeder vun 2025 (dem Flugmodell säin eelere
  Layout, Chat ouni Flag-Byte, zlib), d'Buedemlag, den agepaakten
  Héicheoffset, d'Ofschosspunkte vun de Waffen an d'Cockpit-Instrumenter goufen
  hei dorop erausfonnt.

## Tester {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

D'Eenheetstester liesen ni eng Installatioun (`HEAT3D_WT_NO_NAMES` ass gesat); den
Test mat Ären eegene Replays liest d'Nimm aus Ärer Installatioun.

D'Tester bauen Replays am Code (`tests/synth.py`: Header, Pakete, Resultater,
den Entitéit-Stroum, Waffen am Fluch) no der Layout, déi d'Reader dokumentéieren; kee
Replay ass am Repository.

## Lizenz {#licence}

MIT - kuck [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Benotzt pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) a Pillow (MIT-CMU). D'Level-Reader goufen aus dem
Quellcode vun der Dagor Engine geschriwwen, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause-Lizenz; näischt vu sengem Code ass hei kopéiert, an déi benotzte Formatkonstanten
(de vromfs-XOR-Schlëssel, d'Offsete vum Héichtebereichsgitter) sinn zitéiert, wou se virkommen.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
