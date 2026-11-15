---
title: Tingimused ja litsents
nav_order: 16
lang: et
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Tingimused ja litsents {#terms-and-licence}

## Tingimused {#the-terms}

Gaijini kasutustingimused (uuendatud 2026-08-17), EULA (Lisa 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
väljaspool klienti. Oma koopia tasemefailide lugemine kohaliku 3D-vaate jaoks on
kasutaja otsus, tehtud seda teades. Kirjutatud tasemed jäävad sinu masinasse:
**ära avalda neid kunagi**, ja siit ei tule kaasa mingit mängu andmet.

## Allikad {#sources}

Kogu siinne kood on kirjutatud selle projekti jaoks; ühtegi koodi ei ole kopeeritud
teisest parserist. Formaadi kohta teatakse see järgmistest allikatest:

- Gaijini Dagor Engine'i lähtekood (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` ja `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` olemi voo jaoks (`ecs.py`), ning `net/message.cpp`
  (`MessageClass::initImpl`) selle kohta, kuidas olemi sõnumid oma klassid
  nummerdavad. Komponentide ja tüüpide nimed sobitatakse nende FNV-1a räsidega
  mängu enda arhiivide sõnadega; `ecs.py` loetleb leitud nimed.
- Sama lähtekoodi `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  ja `daNet/bitStream.h`: kuidas sõnum nimetab objekti, kellele ta on
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` ja tema enda parser
  `web/wrpl-parse.js`, loetud lennumudeli, maapealse sünkroonimise, rakettide
  lennu, ID-väljadega sõnumite, mängijaslotide, kabiini väärtuste ja binaarse blk
  bitipaigutuste jaoks. WTACRP nimetab oma viidetena maxsupermanhd/wrpl-inspector,
  wt_blk ja wrpl-acmi (AGPL-3.0); nende koodi siin ei loetud.
- Autori enda kordused, loetud failidena: 2025. aasta erinevused (lennumudeli vanem
  paigutus, vestlus ilma lipubaidita, zlib), maapealse asendi, pakitud kõrguse nihke,
  relvade vabastuspunktide ja kabiini instrumentide tööd tehti nende peal siin.

## Testid {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Üksustestid ei loe kunagi installatsiooni (`HEAT3D_WT_NO_NAMES` on seatud); test
sinu enda kordustega loeb nimed sinu installatsioonist.

Testid koostavad kordused koodis (`tests/synth.py`: päis, paketid, tulemused,
olemi voog, rakettide lend) lugejate dokumenteeritud paigutuse järgi; hoidlas ei ole
ühtegi kordust.

## Litsents {#licence}

MIT - vt [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Kasutab pyarrow'd (Apache-2.0), numpy'd (BSD-3-Clause),
zstandardi (BSD-3-Clause) ja Pillow'd (MIT-CMU). Tasemelugejad on kirjutatud Dagor Engine'i
lähtekoodi järgi, Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause litsents;
selle koodi ei ole siia kopeeritud, ja kasutatud formaadikonstandid (vromfs XOR-võti,
kõrguste vahemiku ruudustiku nihked) on tsiteeritud seal, kus need esinevad.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
