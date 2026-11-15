---
title: "Kushtet dhe licenca"
nav_order: 16
lang: "sq"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Kushtet dhe licenca {#terms-and-licence}

## Kushtet {#the-terms}

Kushtet e Shërbimit të Gaijin (përditësuar 2026-08-17), EULA (Annex 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
përtej klientit. Leximi i skedarëve të niveleve të kopjes tënde në një pamje 3D lokale është
vendim i përdoruesit, i marrë duke e ditur këtë. Nivelet e shkruara mbeten në
makinën tënde: **mos i publiko kurrë**, dhe asgjë këtu nuk shpërndan të dhëna loje.

## Burimet {#sources}

I gjithë kodi këtu është shkruar për këtë projekt; asnjë kod nuk u kopjua nga një parser tjetër. Çfarë
di për formatin vjen nga:

- Burimi i Dagor Engine të Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` dhe `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` për rrjedhën e entiteteve (`ecs.py`), dhe `net/message.cpp`
  (`MessageClass::initImpl`) për mënyrën si mesazhet e entiteteve i numërojnë klasat e tyre. Emrat e komponentëve dhe të llojeve
  përputhen me hash-et e tyre FNV-1a me fjalë të arkivave të vetë lojës;
  `ecs.py` liston emrat e gjetur.
- Po i njëjti burim `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  dhe `daNet/bitStream.h`: si një mesazh emërton objektin për të cilin është
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, dhe parser-i i vet
  `web/wrpl-parse.js`, të lexuara për strukturat e bitëve të modelit të fluturimit, sinkronizimin
  tokësor, armët në fluturim, mesazhet me fusha ID, vendet e lojtarëve, vlerat e kabinës
  dhe blk-në binare. WTACRP emërton maxsupermanhd/wrpl-inspector,
  wt_blk dhe wrpl-acmi (AGPL-3.0) si referencat e veta; kodi i tyre nuk u
  lexua këtu.
- Riluajtjet e vetë autorit, të lexuara si skedarë: dallimet e 2025 (struktura më e vjetër e
  modelit të fluturimit, biseda pa bajt flamuri, zlib), qëndrimi tokësor, zhvendosja e paketuar
  e lartësisë, pikat e lëshimit të armëve dhe instrumentet e kabinës u
  zbuluan mbi to këtu.

## Testet {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Testet njësi nuk lexojnë kurrë një instalim (`HEAT3D_WT_NO_NAMES` është vendosur); testi
me riluajtjet e tua lexon emrat nga instalimi yt.

Testet i ndërtojnë riluajtjet në kod (`tests/synth.py`: header, paketa, rezultate,
rrjedha e entiteteve, armë në fluturim) sipas strukturës që dokumentojnë lexuesit; asnjë
riluajtje nuk është në depo.

## Licenca {#licence}

MIT - shih [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Përdor pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) dhe Pillow (MIT-CMU). Lexuesit e niveleve u shkruan
nga burimi i Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licenca BSD
3-Clause; asnjë kod i tij nuk është kopjuar këtu, dhe konstantet e formatit të përdorura
(çelësi XOR i vromfs, zhvendosjet e rrjetës së intervalit të lartësisë) citohen aty ku shfaqen.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
