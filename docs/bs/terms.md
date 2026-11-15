---
title: "Uvjeti i licenca"
nav_order: 16
lang: bs
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Uvjeti i licenca {#terms-and-licence}

## Uvjeti {#the-terms}

Gaijinovi Uvjeti korištenja (ažurirani 2026-08-17), EULA (Annex 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
izvan klijenta. Čitanje datoteka nivoa vlastite kopije u lokalni 3D prikaz
je odluka korisnika, donesena sa znanjem o ovome. Napisani nivoi ostaju na vašem
računaru: **nikad ih ne objavljujte**, i ništa ovdje ne isporučuje podatke igre.

## Izvori {#sources}

Sav kod ovdje je napisan za ovaj projekat; nijedan kod nije kopiran iz drugog parsera. Ono što
zna o formatu dolazi iz:

- Izvora Gaijinovog Dagor Enginea (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` i `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` za tok entiteta (`ecs.py`), i `net/message.cpp`
  (`MessageClass::initImpl`) za to kako poruke entiteta numerišu svoje klase. Imena komponenti i tipova
  uparuju se njihovim FNV-1a hashevima s riječima iz vlastitih arhiva igre;
  `ecs.py` navodi pronađena imena.
- Istog izvora `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  i `daNet/bitStream.h`: kako poruka imenuje objekt kojem je namijenjena
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` i njegov vlastiti parser
  `web/wrpl-parse.js`, čitani zbog rasporeda bitova modela leta, kopnene
  sinhronizacije, oružja u letu, poruka s poljima id-a, igračkih slotova, vrijednosti kokpita
  i binarnog blk-a. WTACRP kao vlastite reference navodi maxsupermanhd/wrpl-inspector,
  wt_blk i wrpl-acmi (AGPL-3.0); njihov kod ovdje nije
  čitan.
- Autorovi vlastiti replayevi, čitani kao datoteke: razlike iz 2025. (stariji
  raspored modela leta, čet bez bajta zastavice, zlib), kopneni stav, pomak
  pakirane visine, tačke ispuštanja oružja i instrumenti kokpita
  izrađeni su na njima ovdje.

## Testovi {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Jedinični testovi nikad ne čitaju instalaciju (`HEAT3D_WT_NO_NAMES` je postavljen); test
s vašim vlastitim replayevima čita imena iz vaše instalacije.

Testovi grade replayeve u kodu (`tests/synth.py`: zaglavlje, paketi, rezultati,
tok entiteta, oružja u letu) prema rasporedu koji čitači dokumentiraju; nijedan
replay nije u repozitoriju.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Koristi pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) i Pillow (MIT-CMU). Čitači nivoa pisani su
prema izvoru Dagor Enginea, Copyright (c) 2023 Gaijin Entertainment, licenca BSD
3-Clause; nijedan njegov kod nije ovdje kopiran, a korištene konstante formata
(vromfs XOR ključ, pomaci mreže raspona visina) navedene su gdje se pojavljuju.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
