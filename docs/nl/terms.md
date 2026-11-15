---
title: "Voorwaarden en licentie"
nav_order: 16
lang: "nl"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Voorwaarden en licentie {#terms-and-licence}

## De voorwaarden {#the-terms}

De Terms of Service van Gaijin (bijgewerkt 2026-08-17), EULA (Bijlage 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
buiten de client. Dat de levelbestanden van je eigen kopie in een lokale 3D-weergave
lezen, is een beslissing van de gebruiker, die dit weet. De levels die geschreven worden
blijven op je eigen computer: **publiceer ze nooit**, en niets hier levert gamegegevens mee.

## Bronnen {#sources}

Alle code hier is geschreven voor dit project; er is geen code van een andere parser
overgenomen. Wat het over het formaat weet, komt uit:

- De broncode van de Dagor Engine van Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` en `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` voor de entiteitenstroom (`ecs.py`), en `net/message.cpp`
  (`MessageClass::initImpl`) voor hoe entiteitsberichten hun klassen nummeren. Component- en typenamen
  worden vergeleken via hun FNV-1a-hashes met woorden uit de eigen archieven van het spel;
  `ecs.py` somt de gevonden namen op.
- Dezelfde broncode, `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  en `daNet/bitStream.h`: hoe een bericht het object noemt waarvoor het bestemd is
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, en de eigen parser `web/wrpl-parse.js`,
  gelezen voor de bitindelingen van het vluchtmodel, de grondsynchronisatie, wapens in de vlucht,
  berichten met id-velden, spelersslots, de cockpitwaarden en de binaire blk. WTACRP noemt
  maxsupermanhd/wrpl-inspector, wt_blk en wrpl-acmi (AGPL-3.0) als eigen referenties; hun code is
  hier niet gelezen.
- De eigen replays van de auteur, als bestanden gelezen: de verschillen van 2025 (de oudere
  indeling van het vluchtmodel, chat zonder vlagbyte, zlib), de grondhouding, de
  gepakte hoogteverschuiving, de afwerppunten van wapens en de cockpitinstrumenten zijn hier
  op die replays uitgewerkt.

## Tests {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<map met de voorbeeldreplays> python -m pytest -q   # controleert ook de openbare voorbeeldreplays van 2025
HEAT3D_WT_REPLAYS=<map met je eigen replays> python -m pytest -q        # stappen, identiteiten, AI-vlaggen, rolteken, de smoother, namen
```

De unittests lezen nooit een installatie (`HEAT3D_WT_NO_NAMES` is ingesteld); de test
met je eigen replays leest de namen uit je installatie.

De tests bouwen replays in code (`tests/synth.py`: kop, pakketten, resultaten,
de entiteitenstroom, wapens in de vlucht) in de indeling die de lezers beschrijven; er staat
geen replay in de repository.

## Licentie {#licence}

MIT - zie [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Gebruikt pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) en Pillow (MIT-CMU). De levellezers zijn geschreven
op basis van de broncode van de Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause-licentie; er is geen code daarvan overgenomen, en de gebruikte formaatconstanten
(de XOR-sleutel van vromfs, de rasterverschuivingen van het hoogtebereik) worden genoemd waar ze
voorkomen.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
