---
title: Begriffe und Lizenz
nav_order: 16
lang: "de"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Begriffe und Lizenz {#terms-and-licence}

## Was gelesen wird {#what-it-reads}

Der Umwandler liest die Replays, die War Thunder auf deinem Computer speichert (oder Replays deiner Gefechte, die du selbst von warthunder.com heruntergeladen hast), und die Level-Dateien deiner eigenen War-Thunder-Installation. Nichts aus dem Spiel ist hier enthalten oder wird weitergegeben: keine Spiel-Assets, kein Spielcode, keine DLLs; Oodle wird aus deiner eigenen Installation geladen. Was er schreibt, bleibt auf deinem Rechner: **veröffentliche die Level nie**.

3DHeat ist nicht mit Gaijin Entertainment verbunden und wird nicht von Gaijin Entertainment unterstützt. War Thunder und zugehörige Namen und Marken gehören ihren Inhabern.

Rechteinhaber: Eröffnet ein Issue unter <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - wir antworten schnell und entfernen auf Anfrage alles.

## Quellen {#sources}

Der gesamte Code hier wurde für dieses Projekt geschrieben; kein Code wurde aus einem
anderen Parser kopiert. Was es über das Format weiß, stammt aus:

- dem Quellcode der Dagor Engine von Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` und `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` für den Entitätsstrom (`ecs.py`), und `net/message.cpp`
  (`MessageClass::initImpl`) dafür, wie Entitätsnachrichten ihre Klassen nummerieren.
  Komponenten- und Typnamen werden über ihre FNV-1a-Hashes mit Wörtern aus den eigenen
  Archiven des Spiels abgeglichen; `ecs.py` listet die gefundenen Namen.
- demselben Quellcode, `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  und `daNet/bitStream.h`: wie eine Nachricht das Objekt nennt, für das sie ist
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` und sein eigener Parser
  `web/wrpl-parse.js`, gelesen für die Bit-Layouts des Flugmodells, der Bodensynchronisation,
  der Waffen im Flug, der Nachrichten mit ID-Feldern, der Spielerplätze, der Cockpit-Werte und
  des binären BLK. WTACRP nennt maxsupermanhd/wrpl-inspector, wt_blk und wrpl-acmi
  (AGPL-3.0) als eigene Referenzen; deren Code wurde hier nicht gelesen.
- den eigenen Replays des Autors, als Dateien gelesen: Die Unterschiede von 2025 (das ältere
  Layout des Flugmodells, Chat ohne Flag-Byte, zlib), die Lage am Boden, der Versatz gepackter
  Höhen, die Abwurfpunkte der Waffen und die Cockpit-Instrumente wurden an ihnen hier erarbeitet.

## Tests {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # prüft außerdem die öffentlichen Beispiel-Replays von 2025
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # Schritte, Identitäten, KI-Markierungen, Vorzeichen des Rollens, der Glätter, Namen
```

Die Unit-Tests lesen nie eine Installation (`HEAT3D_WT_NO_NAMES` ist gesetzt); der Test
mit deinen eigenen Replays liest die Namen aus deiner Installation.

Die Tests bauen Replays im Code (`tests/synth.py`: Kopf, Pakete, Ergebnisse, der
Entitätsstrom, Waffen im Flug) in dem Layout, das die Leser dokumentieren; im Repository
liegt kein Replay.

## Lizenz {#licence}

MIT - siehe [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Verwendet werden pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) und Pillow (MIT-CMU). Die Level-Leser wurden aus dem Quellcode der
Dagor Engine geschrieben, Copyright (c) 2023 Gaijin Entertainment, BSD-3-Clause-Lizenz; kein
Code davon wird hier kopiert, und die verwendeten Formatkonstanten (der XOR-Schlüssel von
vromfs, die Versätze des Höhenbereichsrasters) sind dort zitiert, wo sie vorkommen.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
