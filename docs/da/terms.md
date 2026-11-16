---
title: Vilkår og licens
nav_order: 16
lang: "da"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Vilkår og licens {#terms-and-licence}

## Hvad der læses {#what-it-reads}

Konverteren læser de replays, War Thunder gemmer på din computer (eller replays af dine kampe, som du selv har hentet fra warthunder.com), og niveaufilerne fra din egen War Thunder-installation. Intet fra spillet er med her eller videredistribueres: ingen spilaktiver, ingen spilkode, ingen DLL'er; Oodle indlæses fra din egen installation. Det, den skriver, bliver på din maskine: **publicér aldrig niveauerne**.

3DHeat er ikke tilknyttet eller godkendt af Gaijin Entertainment. War Thunder og tilhørende navne og varemærker tilhører deres ejere.

Rettighedshavere: opret et issue på <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - vi svarer hurtigt og fjerner alt efter anmodning.

## Kilder {#sources}

Al kode her er skrevet til dette projekt; ingen kode er kopieret fra en anden parser. Det,
den ved om formatet, kommer fra:

- Gaijins Dagor Engine-kildekode (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` og `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` til entitetsstrømmen (`ecs.py`), og `net/message.cpp`
  (`MessageClass::initImpl`) for hvordan entitetsmeddelelser nummererer deres klasser. Komponent- og typenavne
  matches efter deres FNV-1a-hashes mod ord fra spillets egne arkiver; `ecs.py` lister de navne, der blev fundet.
- Samme kildekodes `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  og `daNet/bitStream.h`: hvordan en meddelelse navngiver det objekt, den er til
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, og dens egen parser
  `web/wrpl-parse.js`, læst for bitlayouterne af flyvemodellen, jordsynkronisering, våben i flugt,
  id-felt-meddelelser, spillerpladser, cockpitværdierne og den binære blk. WTACRP nævner
  maxsupermanhd/wrpl-inspector, wt_blk og wrpl-acmi (AGPL-3.0) som sine egne referencer; deres kode
  er ikke læst her.
- Forfatterens egne replays, læst som filer: forskellene i 2025 (flyvemodellens ældre layout, chat uden
  flagbyte, zlib), landholdningen, forskydningen af den pakkede højde, våbnenes udløsningspunkter og
  cockpitinstrumenterne blev udregnet på dem her.

## Tests {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Enhedstestene læser aldrig en installation (`HEAT3D_WT_NO_NAMES` er sat); testen
med dine egne replays læser navnene fra din installation.

Testene bygger replays i kode (`tests/synth.py`: header, pakker, resultater,
entitetsstrømmen, våben i flugt) efter det layout, læserne dokumenterer; intet replay
ligger i repositoryet.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Bruger pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) og Pillow (MIT-CMU). Banelæserne er skrevet
ud fra Dagor Engines kildekode, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause-licens; ingen kode fra den er kopieret her, og de formatkonstanter, der bruges
(vromfs-XOR-nøglen, forskydningerne i højdeintervalgitteret), er citeret, hvor de optræder.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
