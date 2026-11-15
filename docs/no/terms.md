---
title: "Vilkår og lisens"
nav_order: 16
lang: no
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Vilkår og lisens {#terms-and-licence}

## Vilkårene {#the-terms}

Gaijins tjenestevilkår (oppdatert 2026-08-17), sluttbrukerlisensavtalen (vedlegg 2):
3.2.2 «modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)», 3.2.9 «mine or collect any data from
the Game(s) that is not intended to be publicly displayed»; 1.2 «are not
permitted to store, download, modify, or otherwise use any part of the Game(s)»
utover klienten. Å lese dine egne kopiers nivåfiler inn i en lokal 3D-visning er brukerens
egen beslutning, tatt med kjennskap til dette. De skrevne nivåene blir på din maskin: **publiser dem aldri**,
og ingenting her sender ut spilldata.

## Kilder {#sources}

All kode her er skrevet for dette prosjektet; ingen kode er kopiert fra en annen parser. Det
den vet om formatet, kommer fra:

- Gaijins Dagor Engine-kilde (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` og `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` for entitetsstrømmen (`ecs.py`), og `net/message.cpp`
  (`MessageClass::initImpl`) for hvordan entitetsmeldinger nummererer sine klasser. Komponent- og typenavn
  matches mot deres FNV-1a-hasher mot ord i spillets egne arkiver; `ecs.py` lister navnene som ble funnet.
- Samme kildes `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  og `daNet/bitStream.h`: hvordan en melding navngir objektet den er for
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, og dens egen parser
  `web/wrpl-parse.js`, lest for bitoppsettene til flymodellen, bakkesynkronisering, våpen i flukt, id-felt-meldinger, spillerplasser, cockpit-
  verdiene og den binære blk-en. WTACRP nevner maxsupermanhd/wrpl-inspector,
  wt_blk og wrpl-acmi (AGPL-3.0) som sine egne referanser; deres kode ble ikke lest her.
- Forfatterens egne replayer, lest som filer: forskjellene i 2025 (flymodellens eldre oppsett, chat uten flaggbyte, zlib), bakkeholdningen,
  den pakkede høydeforskyvningen, våpnenes slippunkter og cockpit-instrumentene ble utarbeidet på dem her.

## Tester {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<mappe med eksempelreplayene> python -m pytest -q   # sjekker også de offentlige 2025-eksempelreplayene
HEAT3D_WT_REPLAYS=<mappe med dine egne replayer> python -m pytest -q        # steg, identiteter, KI-flagg, rullefortegn, utjevneren, navn
```

Enhetstestene leser aldri en installasjon (`HEAT3D_WT_NO_NAMES` er satt); testen
med dine egne replayer leser navnene fra installasjonen din.

Testene bygger replayer i kode (`tests/synth.py`: header, pakker, resultater,
entitetsstrømmen, våpen i flukt) til oppsettet som leserne dokumenterer; ingen replay ligger i depotet.

## Lisens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Bruker pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) og Pillow (MIT-CMU). Nivålesere ble skrevet
fra Dagor Engines kilde, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause-lisensen; ingen kode fra den er kopiert her, og formatkonstantene som brukes
(vromfs-XOR-nøkkelen, rutenettforskyvningene for høydeområdet) er referert der de står.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
