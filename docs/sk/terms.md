---
title: "Podmienky a licencia"
nav_order: 16
lang: "sk"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Podmienky a licencia {#terms-and-licence}

## Podmienky {#the-terms}

Podmienky služby Gaijin (aktualizované 2026-08-17), EULA (príloha 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the Game(s)",
3.2.9 "mine or collect any data from the Game(s) that is not intended to be publicly displayed"; 1.2 "are not permitted to store, download, modify, or otherwise use any part of the Game(s)" nad rámec klienta. Čítanie súborov levelu z vlastnej kópie hry
do lokálneho 3D pohľadu je rozhodnutie používateľa, urobené s vedomím tohto. Zapísané levely zostávajú vo vašom počítači:
**nikdy ich nezverejňujte**, a nič tu nedodáva herné dáta.

## Zdroje {#sources}

Všetok kód tu je napísaný pre tento projekt; žiadny kód sa neskopíroval z iného parsera. To, čo vie o formáte, pochádza z:

- zdroja Dagor Engine od Gaijinu (github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause):
  `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h` a
  `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` pre tok entít (`ecs.py`), a `net/message.cpp`
  (`MessageClass::initImpl`) pre to, ako entitné správy číslujú svoje triedy. Názvy komponentov a typov sa párujú
  podľa ich hashov FNV-1a so slovami z vlastných archívov hry; `ecs.py` vypisuje nájdené názvy.
- tiež `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` a `daNet/bitStream.h` z toho istého zdroja:
  ako správa pomenuje objekt, pre ktorý je (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`,
  `docs/QUICK-REF.md` a jeho vlastný parser `web/wrpl-parse.js`, čítané pre rozloženie bitov modelu letu, pozemnej
  synchronizácie, striel v letu, správ s id poľom, slotov hráčov, hodnôt kokpitu a binárneho blk. WTACRP uvádza
  maxsupermanhd/wrpl-inspector, wt_blk a wrpl-acmi (AGPL-3.0) ako vlastné referencie; ich kód sa tu nečítal.
- vlastné replaye autora, čítané ako súbory: rozdiely z roku 2025 (staršie rozloženie modelu letu, chat bez bajtu príznaku,
  zlib), postoj pozemných jednotiek, zabalený výškový posun, miesta vypustenia zbraní a prístroje kokpitu boli
  tu vypracované práve na nich.

## Testy {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<priečinok s ukážkovými replaymi> python -m pytest -q   # overí aj verejné ukážkové replaye z roku 2025
HEAT3D_WT_REPLAYS=<priečinok vlastných replayov> python -m pytest -q        # kroky, identity, príznaky AI, znamienko náklonu, vyhladzovač, názvy
```

Jednotkové testy nikdy nečítajú inštaláciu (nastavené `HEAT3D_WT_NO_NAMES`); test
s vlastnými replaymi číta názvy z vašej inštalácie.

Testy skladajú replaye v kóde (`tests/synth.py`: hlavička, pakety, výsledky, tok entít,
strely v letu) do rozloženia, ktoré čítačky dokumentujú; žiadny replay nie je v repozitári.

## Licencia {#licence}

MIT – pozri [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Používa pyarrow (Apache-2.0),
numpy (BSD-3-Clause), zstandard (BSD-3-Clause) a Pillow (MIT-CMU). Čítačky levelov boli napísané
podľa zdroja Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licencia BSD 3-Clause; žiadny jeho kód sa tu
nekopíruje, a použité konštanty formátu (XOR kľúč vromfs, posuny mriežky výškových rozsahov) sú uvedené tam, kde sa objavujú.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
