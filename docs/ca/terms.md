---
title: Condicions i llicència
nav_order: 16
lang: "ca"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Condicions i llicència {#terms-and-licence}

## Què es llegeix {#what-it-reads}

El convertidor llegeix les repeticions que War Thunder desa al teu ordinador (o repeticions de les teves batalles que has baixat tu mateix de warthunder.com) i els fitxers de nivells de la teva pròpia instal·lació de War Thunder. Aquí no s'inclou ni es redistribueix res del joc: cap recurs del joc, cap codi del joc, cap DLL; Oodle es carrega des de la teva pròpia instal·lació. El que escriu es queda al teu ordinador: **no publiquis mai els nivells**.

3DHeat no està afiliat a Gaijin Entertainment ni té el seu aval. War Thunder i els noms i marques relacionats pertanyen als seus propietaris.

Titulars de drets: obriu una incidència a <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - responem ràpidament i retirem el que calgui si se'ns demana.

## Fonts {#sources}

Tot el codi d'aquí s'ha escrit per a aquest projecte; no s'ha copiat codi de cap altre analitzador. El que
en sap sobre el format ve de:

- El codi font del Dagor Engine de Gaijin (github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause):
  `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h` i
  `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` per al flux d'entitats (`ecs.py`), i
  `net/message.cpp` (`MessageClass::initImpl`) per a com els missatges d'entitat numeren les seves classes.
  Els noms de components i de tipus s'esparien pels seus hashos FNV-1a amb paraules dels arxius propis del
  joc; `ecs.py` llista els noms trobats.
- El mateix codi font: `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` i `daNet/bitStream.h`:
  com un missatge nomena l'objecte al qual va dirigit (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`,
  `docs/QUICK-REF.md`, i el seu propi analitzador `web/wrpl-parse.js`, llegits per als dissenys de bits del
  model de vol, la sincronització terrestre, les armes en vol, els missatges amb camps d'identificació, les
  ranures de jugador, els valors de cabina i el blk binari. WTACRP cita com a referències pròpies
  maxsupermanhd/wrpl-inspector, wt_blk i wrpl-acmi (AGPL-3.0); el seu codi no es va llegir aquí.
- Les repeticions pròpies de l'autor, llegides com a fitxers: les diferències del 2025 (la disposició més
  antiga del model de vol, el xat sense byte d'indicador, zlib), l'actitud terrestre, el desplaçament d'alçada
  empaquetada, els punts de llançament de les armes i els instruments de cabina es van calcular aquí amb elles.

## Proves {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<carpeta amb les repeticions de mostra> python -m pytest -q   # comprova també les repeticions de mostra públiques del 2025
HEAT3D_WT_REPLAYS=<carpeta amb les teves pròpies repeticions> python -m pytest -q        # passos, identitats, marques IA, signe del roll, l'alisador, els noms
```

Les proves unitàries no llegeixen mai una instal·lació (`HEAT3D_WT_NO_NAMES` és definit); la prova amb les
teves pròpies repeticions llegeix els noms de la teva instal·lació.

Les proves construeixen repeticions en codi (`tests/synth.py`: capçalera, paquets, resultats, el flux
d'entitats, armes en vol) segons la disposició que documenten els lectors; cap repetició no és al repositori.

## Llicència {#licence}

MIT - mira [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Usa pyarrow
(Apache-2.0), numpy (BSD-3-Clause), zstandard (BSD-3-Clause) i Pillow (MIT-CMU). Els lectors de nivells
s'han escrit a partir del codi font del Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, llicència BSD
3-Clause; no s'hi copia cap codi seu, i les constants de format usades (la clau XOR de vromfs, els
desplaçaments de la graella de rang d'alçada) es citen on apareixen.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
