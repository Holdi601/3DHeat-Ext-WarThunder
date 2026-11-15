---
title: "Villkor och licens"
nav_order: 16
lang: sv
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Villkor och licens {#terms-and-licence}

## Villkoren {#the-terms}

Gaijins användarvillkor (uppdaterade 2026-08-17), EULA (bilaga 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
utöver klienten. Att läsa dina egna kopior av spelets nivåfiler in i en lokal 3D-vy
är användarens beslut, fattat med vetskap om detta. Nivåerna som skrivs stannar på
din dator: **publicera dem aldrig**, och inget här levererar någon speldata.

## Källor {#sources}

All kod här är skriven för det här projektet; ingen kod kopierades från någon annan
parser. Vad den vet om formatet kommer från:

- Gaijins Dagor Engine-källkod (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` och `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` för entitetsströmmen (`ecs.py`), och `net/message.cpp`
  (`MessageClass::initImpl`) för hur entitetsmeddelanden numrerar sina klasser.
  Komponent- och typnamn matchas med deras FNV-1a-hashar mot ord i spelets egna
  arkiv; `ecs.py` listar de namn som hittats.
- Samma källkods `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  och `daNet/bitStream.h`: hur ett meddelande anger vilket objekt det är till
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, och dess egen parser
  `web/wrpl-parse.js`, lästa för bitlayouterna i flygmodellen, markens synk,
  vapen i luften, id-fältsmeddelanden, spelarplatser, cockpitvärdena och den binära
  blk:en. WTACRP nämner maxsupermanhd/wrpl-inspector, wt_blk och wrpl-acmi
  (AGPL-3.0) som egna referenser; deras kod lästes inte här.
- Författarens egna repriser, lästa som filer: skillnaderna 2025 (flygmodellens äldre
  layout, chatt utan flaggbyte, zlib), markattityden, den packade höjdförskjutningen,
  vapnens släppunkter och cockpitinstrumenten räknades ut på dem här.

## Tester {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<mapp med exempelrepriserna> python -m pytest -q   # kontrollerar även de publika 2025-exempelrepriserna
HEAT3D_WT_REPLAYS=<mapp med dina egna repriser> python -m pytest -q        # steg, identiteter, AI-flaggor, rullens tecken, utjämnaren, namn
```

Enhetstesterna läser aldrig en installation (`HEAT3D_WT_NO_NAMES` är satt); testet
med dina egna repriser läser namnen ur din installation.

Testerna bygger repriser i kod (`tests/synth.py`: huvud, paket, resultat,
entitetsströmmen, vapen i luften) enligt layouten som läsarna dokumenterar; ingen
repris finns i arkivet.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Använder pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) och Pillow (MIT-CMU). Nivåläsarna skrevs utifrån Dagor
Engines källkod, Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause-licensen;
ingen kod ur den kopieras här, och de formatkonstanter som används (vromfs-XOR-nyckeln,
höjdintervallets rutnätsförskjutningar) anges där de förekommer.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
