---
title: Pojmovi i licenca
nav_order: 16
lang: hr
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Pojmovi i licenca {#terms-and-licence}

## Uvjeti {#the-terms}

Gaijinovi Uvjeti korištenja (ažurirani 2026-08-17), EULA (Prilog 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Čitanje datoteka razina vlastite kopije igre u lokalni 3D prikaz
odluka je korisnika, donesena znajući to. Razine koje se zapišu ostaju na tvom računalu:
**nikad ih ne objavljuj**, a ovdje se ne isporučuju nikakvi podaci igre.

## Izvori {#sources}

Sav kod ovdje napisan je za ovaj projekt; nijedan kod nije kopiran iz drugog čitača.
Ono što zna o formatu dolazi iz:

- Gaijinova izvornog koda Dagor Enginea (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` i `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` za tok entiteta (`ecs.py`), i `net/message.cpp`
  (`MessageClass::initImpl`) za to kako poruke entiteta numeriraju svoje klase. Nazivi komponenti i tipova
  uspoređuju se s njihovim FNV-1a hashevima prema riječima iz igrinih vlastitih arhiva; `ecs.py` navodi
  pronađene nazive.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` i `daNet/bitStream.h` istog izvora: kako
  poruka imenuje objekt za koji je (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, i njegov vlastiti čitač
  `web/wrpl-parse.js`, čitani za rasporede bitova modela leta, sinkronizaciju kopna, oružje u letu, poruke
  s id poljima, utore igrača, vrijednosti kabine i binarni blk. WTACRP navodi maxsupermanhd/wrpl-inspector,
  wt_blk i wrpl-acmi (AGPL-3.0) kao svoje reference; njihov kod ovdje nije čitan.
- Vlastite snimke autora, čitane kao datoteke: razlike iz 2025. (stariji raspored modela leta, razgovor bez bajta
  zastave, zlib), stav kopnenih jedinica, pomak zapakirane visine, točke ispuštanja oružja i instrumenti kabine
  razrađeni su ovdje na njima.

## Testovi {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # provjerava i javne uzorke snimki 2025.
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # koraci, identiteti, AI zastavice, predznak valjanja, izglađivač, imena
```

Jedinični testovi nikad ne čitaju instalaciju (postavljen je `HEAT3D_WT_NO_NAMES`); test s tvojim vlastitim
snimkama čita nazive iz tvoje instalacije.

Testovi grade snimke u kodu (`tests/synth.py`: zaglavlje, paketi, rezultati, tok entiteta, oružje u letu) prema
rasporedu koji čitači dokumentiraju; nijedna snimka nije u repozitoriju.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Koristi pyarrow (Apache-2.0),
numpy (BSD-3-Clause), zstandard (BSD-3-Clause) i Pillow (MIT-CMU). Čitači razina napisani su prema izvornom kodu
Dagor Enginea, Copyright (c) 2023 Gaijin Entertainment, licenca BSD 3-Clause; nijedan njegov kod nije ovdje kopiran,
a korištene konstante formata (XOR ključ vromfs-a, pomaci mreže raspona visina) navedene su gdje se pojavljuju.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
