---
title: Noteikumi un licence
nav_order: 16
lang: lv
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Noteikumi un licence {#terms-and-licence}

## Noteikumi {#the-terms}

Gaijin Pakalpojumu noteikumi (atjaunināti 2026-08-17), EULA (2. pielikums):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Savas kopijas līmeņu failu nolasīšana vietējā 3D skatā ir
lietotāja lēmums, kas pieņemts, to zinot. Uzrakstītie līmeņi paliek tavā datorā:
**nekad tos nepublicē**, un šeit nekas nepiegādā spēles datus.

## Avoti {#sources}

Viss šeit esošais kods ir rakstīts šim projektam; nekāds kods nav nokopēts no
cita parsera. Ko tas zina par formātu, nāk no:

- Gaijin Dagor Engine koda (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` un `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` entītiju plūsmai (`ecs.py`), un `net/message.cpp`
  (`MessageClass::initImpl`) tam, kā entītiju ziņojumi numurē savas klases.
  Komponenšu un tipu nosaukumi tiek sasaistīti pēc to FNV-1a jaucējkodiem ar
  vārdiem no spēles pašu arhīviem; `ecs.py` uzskaita atrastos nosaukumus.
- Tā paša koda `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  un `daNet/bitStream.h`: kā ziņojums nosauc objektu, kuram tas paredzēts
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, un tā pašu parseri
  `web/wrpl-parse.js`, lasīti bitu izkārtojumiem lidojuma modelim, zemes
  sinhronizācijai, lidojumā esošiem ieročiem, ID lauku ziņojumiem, spēlētāju
  slotiem, kabīnes vērtībām un bināro blk. WTACRP nosauc maxsupermanhd/wrpl-inspector,
  wt_blk un wrpl-acmi (AGPL-3.0) kā savas atsauces; to kods šeit nav lasīts.
- Autora paša atkārtojumi, lasīti kā faili: 2025. gada atšķirības (lidojuma modeļa vecākais izkārtojums, tērzēšana bez karoga baita,
  zlib), zemes orientācija, iepakotā augstuma nobīde, ieroču izlaišanas punkti un kabīnes instrumenti tika izstrādāti uz tiem šeit.

## Testi {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Vienības testi nekad nelasa instalāciju (`HEAT3D_WT_NO_NAMES` ir uzstādīts);
tests ar tavu atkārtojumu nolasa nosaukumus no tavas instalācijas.

Testi izveido atkārtojumus kodā (`tests/synth.py`: galvene, pakete, rezultāti,
entītiju plūsma, lidojumā esoši ieroči) saskaņā ar izkārtojumu, ko lasītāji dokumentē;
neviens atkārtojums nav repozitorijā.

## Licence {#licence}

MIT — skat. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Izmanto pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) un Pillow (MIT-CMU). Līmeņu lasītāji ir rakstīti pēc Dagor Engine koda, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause licence; tā kods šeit nav kopēts, un izmantotās formāta konstantes (vromfs XOR atslēga, augstuma diapazona režģa nobīdes) ir citētas
tur, kur tās parādās.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
