---
title: Términos y licencia
nav_order: 16
lang: "es"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Términos y licencia {#terms-and-licence}

## Los términos {#the-terms}

Términos de Servicio de Gaijin (actualizados el 2026-08-17), EULA (Anexo 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
más allá del cliente. Leer los
archivos de nivel de tu propia copia para verlos en una vista 3D local es decisión del usuario,
tomada conociendo esto. Los niveles que se escriben se quedan en tu equipo: **nunca los publiques**,
y aquí no se distribuye ningún dato del juego.

## Fuentes {#sources}

Todo el código de aquí está escrito para este proyecto; no se copió código de ningún otro analizador. Lo que
sabe del formato procede de:

- El código fuente del Dagor Engine de Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` y `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` para el flujo de entidades (`ecs.py`), y `net/message.cpp`
  (`MessageClass::initImpl`) para cómo los mensajes de entidad numeran sus clases. Los nombres de
  componentes y tipos se emparejan por sus hashes FNV-1a con palabras de los propios
  archivos del juego; `ecs.py` enumera los nombres encontrados.
- Los mismos `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  y `daNet/bitStream.h`: cómo un mensaje nombra el objeto al que va (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, y su propio analizador
  `web/wrpl-parse.js`, leídos para las disposiciones de bits del modelo de vuelo, la sincronización
  terrestre, las armas en vuelo, los mensajes con campos de id, las ranuras de jugador, los valores de
  cabina y el blk binario. WTACRP nombra como referencias propias maxsupermanhd/wrpl-inspector,
  wt_blk y wrpl-acmi (AGPL-3.0); su código no se leyó aquí.
- Las repeticiones propias del autor, leídas como archivos: las diferencias de 2025 (la disposición
  más antigua del modelo de vuelo, el chat sin byte de indicador, zlib), la actitud terrestre, el
  desplazamiento de altura empaquetada, los puntos de suelta de las armas y los instrumentos de cabina
  se dedujeron de ellas aquí.

## Pruebas {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<carpeta con las repeticiones de muestra> python -m pytest -q   # comprueba también las repeticiones de muestra públicas de 2025
HEAT3D_WT_REPLAYS=<carpeta de tus propias repeticiones> python -m pytest -q        # pasos, identidades, marcas de IA, signo del balanceo, el suavizador, nombres
```

Las pruebas unitarias nunca leen una instalación (se define `HEAT3D_WT_NO_NAMES`); la prueba
con tus propias repeticiones lee los nombres de tu instalación.

Las pruebas construyen repeticiones en código (`tests/synth.py`: cabecera, paquetes, resultados,
el flujo de entidades, armas en vuelo) según la disposición que documentan los lectores; no hay
ninguna repetición en el repositorio.

## Licencia {#licence}

MIT - véase [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Usa pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) y Pillow (MIT-CMU). Los lectores de niveles se escribieron
a partir del código fuente del Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licencia BSD
3-Clause; no se copia aquí código suyo, y las constantes de formato usadas
(la clave XOR de vromfs, los desplazamientos de la cuadrícula de rangos de altura) se citan donde aparecen.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
