---
title: Niveles
nav_order: 9
lang: es
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Niveles (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` convierte los niveles de tu propia instalación de War Thunder en
archivos `.glb` para el visor, en el mismo sistema de referencia que las tablas de las repeticiones.

## Paso a paso {#step-by-step}

1. Lista los niveles de tu instalación: `heat3d-wt-level list`. Muestra una
   línea por nivel: su nombre, su terreno y sus mapas, y luego el recuento. Por
   ejemplo (un nivel inventado):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrae uno, varios (se permiten comodines) o todos:

   ```bash
   heat3d-wt-level extract <nivel> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <nivel> -o levels --detail high
   ```

3. Carga `levels/<nivel>/<nivel>.glb` en el panel Fondo / nivel del visor, bajo las
   batallas de ese mapa.

Los niveles que escribes se quedan en tu equipo: nunca los publiques (véase
[Términos y licencia](terms.md)).

## Opciones {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Comando / opción | Qué hace |
|---|---|
| `list [--game CARPETA]` | cada nivel de la instalación |
| `extract <niveles...>` / `--all` | los niveles indicados (como los muestra `list`; se permiten comodines), o todos |
| `-o`, `--out` | carpeta de salida; cada nivel va en `<out>/<nivel>/` |
| `--game CARPETA` | la carpeta de War Thunder (por defecto: encontrada a través de Steam o del lanzador; también `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | muestreo del terreno, color del suelo y presupuesto de objetos sobre el mapa de tanques (por defecto `medium`) |
| `--max-object-triangles N` | el presupuesto de objetos (por defecto, el del nivel de detalle) |
| `--max-grid N` | muestras del mapa de altura por lado, por parte (por defecto 1024) |
| `--no-objects` | omite edificios, árboles y otros objetos colocados |
| `--no-generated` | omite los objetos que generan las clases de terreno (bosques, pueblos) |
| `--no-terrain-colour` | aplica al suelo el mapa táctico, no las clases de terreno |
| `--no-texture` | deja el suelo sin textura |
| `--skip-existing` | omite los niveles cuyo `.glb` ya existe |

## Qué se escribe {#what-is-written}

Cada nivel se convierte en `<out>/<nivel>/<nivel>.glb`, `<nivel>.json` (lo que se leyó,
el nivel del agua, los rectángulos de los mapas, recuentos de triángulos, tiempos) y los
mapas tácticos del nivel como `<nivel>_map.png` (el mapa aéreo) y `<nivel>_tankmap.png`;
los mapas terrestres también reciben `<nivel>_terrain.png`, los colores propios del suelo
sobre el mapa de tanques. El glb se escribe en `<nivel>.glb.part` y se renombra al terminar;
mientras se escribe un nivel, se retiene `<out>/<nivel>/.<nivel>.lock`, así que dos
extracciones nunca escriben el mismo nivel (la segunda muestra `busy <nivel>`).
La instalación se busca a través de Steam o de las carpetas predeterminadas del lanzador;
`--game <carpeta>` o `HEAT3D_WT_GAME` indican dónde está si no la encuentra.

| Parte | Qué es |
|---|---|
| `ground:<nivel>` | el mapa de altura del terreno (`HM2`) como cuadrícula; en mapas terrestres, el centro del mapa de tanques (la mitad de su anchura) con el paso de `--detail`, coloreado con las clases de terreno, calcomanías del suelo y carreteras (`<nivel>_terrain.png`; el mapa táctico cuando eso no se puede hacer); en mapas sin mapa de tanques (mapas aéreos), todo el mapa de altura con un solo paso (2048 muestras por lado en `high`, 1024 en los demás), coloreado con las clases de terreno sobre la zona del mapa aéreo (4096 píxeles por lado, unos 32 m por píxel sobre 131 km; el mapa táctico cuando eso no se puede hacer); en niveles sin mapa de altura, la malla del terreno |
| `ground:<nivel> tank map` | el resto del mapa de tanques, con un paso más grueso |
| `ground:<nivel> heightmap surroundings` | el resto del mapa de altura, aún más grueso |
| `ground:<nivel> land mesh` | los triángulos de colisión de la malla del terreno donde el mapa de altura no llega (los alrededores de un mapa de tanques, hasta decenas de kilómetros); en niveles sin mapa de altura es el suelo, coloreado como arriba |
| `ground:<nivel> outside the map` | suelo que la imagen no cubre, sin textura |
| `water:<nivel>` | un rectángulo plano en el `water_level` del nivel sobre todo el terreno: el juego dibuja el agua como un solo plano, y el suelo bajo él es mar, lago o lecho de río |
| `water:<nivel> rivers` | en niveles con mapa de altura de agua (`WHM`), la superficie de agua inclinada sobre las celdas que cubre |
| `structure:<nivel> buildings` | cada objeto colocado que no es una planta: casas, ruinas, muros, vallas, puentes, vías, rocas, accesorios. Los fijos (`RIGz`) y, sobre el mapa de tanques, los que generan las clases de terreno (manzanas de pueblo, piedras). Cada uno se dibuja con su malla de render (muros, tejados, huecos de ventanas, vigas), al nivel de detalle que permite el presupuesto de triángulos, coloreado por material con el promedio de su textura difusa |
| `structure:<nivel> trees` | árboles y arbustos, fijos y generados (bosques, setos): su malla de render cuando el presupuesto lo permite; si no, un tronco y una copa (un cono para las coníferas) con el color de hoja propio del árbol, con su tamaño real |

Los objetos sin malla de render usan en su lugar su forma de colisión; los árboles
sin ella, la copa. Los colores de vértice (`COLOR_0`) guardan valores codificados en sRGB,
que es como los lee el visor de 3DHeat.

**Coordenadas**: son los metros del juego con z invertida: glb (x, y, z) = juego
(x, y, -z). El mundo del juego es zurdo (x este, y arriba, z norte); glTF es
diestro. `heat3d-wt-replay` conserva la z del juego y le indica al visor que la invierta,
así que una repetición y el nivel de su mapa quedan uno sobre otro sin ningún paso de colocación.
El JSON da el rectángulo de cada mapa táctico en metros del juego y sus esquinas en
el espacio del glb, para cargar el PNG como imagen de mapa.

**Detalle.** `--detail low|medium|high` (por defecto medium) fija, sobre el mapa de tanques:

| | centro del mapa de tanques | resto del mapa de tanques | color del suelo | presupuesto de objetos | triángulos máximos por objeto | plantas generadas conservadas |
|---|---|---|---|---|---|---|
| low | cada 4.ª muestra | cada 8.ª | 4 m por píxel | 1,2 M | 1.500 | árboles 35 %, arbustos 20 % |
| medium | cada 2.ª | cada 4.ª | 2 m | 3,5 M | 4.000 | árboles 70 %, arbustos 50 % |
| high | cada muestra (2 m en la mayoría de los mapas terrestres) | cada 2.ª | 1 m (como máximo 4096 píxeles por lado) | 4,5 M | 12.000 | todas |

Los dos anillos del mapa de tanques se ajustan a 0,3 M (low), 1 M (medium) y 3,7 M (high)
triángulos: en los mapas cuyo mapa de altura es más fino que 2 m, los pasos se duplican
(primero el anillo exterior) hasta que encajan, así que también salen a unos 2 m.

Un mapa terrestre en `high` sale con unos 8 millones de triángulos (3,5 M del terreno,
4,5 M de objetos) y 250 MB; en `medium`, unos 4,5 M. Los niveles de detalle (LOD) de los
objetos son los que el propio juego dibujaría desde una misma distancia de visión, el más corto
cuyo total cabe en el presupuesto: los accesorios pequeños bajan primero a LOD gruesos y los
edificios grandes al final, según los rangos que sus creadores dieron a cada LOD (`lodDistance`
del JSON); lo que ese paso ahorra más allá del presupuesto se devuelve a los objetos más grandes.
El color del suelo grueso (mapas aéreos) promedia primero las texturas en mosaico de cada clase de terreno
hasta el tamaño del píxel, para que las baldosas no generen patrones de interferencia (moiré). Si ni siquiera los LOD más gruesos
caben, los árboles que más ahorran se convierten en copas, y luego se dejan fuera los tipos más pequeños
(`leftOut`); ningún objeto se dibuja como una caja (una forma de colisión, si existe, es la propia del objeto).
Los objetos generados se aclaran de forma determinista por tipo (`density`), los mismos
en cada ejecución. `--max-object-triangles` cambia el presupuesto, `--max-grid` (por defecto 1024)
limita las partes más gruesas del mapa de altura, `--no-objects` omite los objetos, `--no-generated`
los generados, `--no-terrain-colour` aplica al suelo el mapa táctico, `--no-texture` lo deja sin textura.

La lista `parts.objects` del JSON enumera las instancias (fijas y generadas, por tipo y clase de
terreno), cuántas se dibujaron con qué LOD (`drawnAs`), los triángulos, la distancia de LOD
y los segundos; `parts.heightmap.rings` el paso y los triángulos de cada anillo del suelo;
`parts.terrainColour` las clases de terreno y sus colores, carreteras y calcomanías del suelo;
`trianglesTotal`, `glbBytes` y `secondsBy` los totales.

## Qué se lee, y con qué fiabilidad {#what-is-read-and-how-well}

| Parte | Estado |
|---|---|
| Binario del nivel (`levels/<nivel>.bin`, `DBLD` 3x64): tabla de bloques | cada nivel comprobado |
| Mapa de altura (`HM2`, versiones 0-2; la versión 2 son valores de 8 bits en bloques, fragmentos Oodle o zstd) | cada nivel cuyo mapa de altura es la versión 2 con fragmentos Oodle; comprobado a ojo frente a sus mapas tácticos (ríos, valles, costas y pueblos encajan) |
| Colisión de la malla del terreno (`lmap`, su trazador de rayos `LTdump`) | leída donde un nivel la tiene (empaquetada con Oodle). Es la superficie de colisión del juego, no la malla renderizada, así que es más gruesa donde el terreno es llano |
| Color del suelo (clases de terreno `lmap` y mapa de pesos, mapa de física `LMp2`, splines `hspl`) | los mapas de color de las clases de terreno y sus texturas de detalle (sus colores medios) ponderados por el mapa de pesos, el índice de bioma de 1 m de las clases indexadas, las formas de carreteras y calcomanías del mapa de física con el color de la textura de su spline o material, los acantilados en pendientes pronunciadas. Comprobado frente a los mapas de tanques: carreteras, pueblos, lagos, franjas de bosque y afloramientos rocosos encajan. La fórmula de color del sombreador de terreno de War Thunder no está en el código público; se usa la publicada por el motor (daNetGame), que sale más saturada que el mapa táctico |
| Nivel del agua | `water_level` del BLK del nivel en `aces.vromfs.bin` (0 donde no tiene) |
| Mapa de altura del agua (`WHM`: una cuadrícula de celdas planas y páginas de 130x130 de alturas de 16 bits) | leído donde un nivel lo tiene; sus ríos se inclinan con el terreno |
| Mapas tácticos | de `content/base/res/locations_maps.dxp.bin`, colocados por `mapCoord0/1` y `tankMapCoord0/1` del BLK; la parte superior de la imagen es el norte |
| Objetos colocados (`RIGz`: las instancias fijas del generador de instancias de render) | cada instancia, como una matriz 3x4 de valores de 16 bits o, en algunos niveles, de 32 bits (el número de bytes de la celda decide); cada byte de cada celda contabilizado en los niveles comprobados |
| Objetos generados (máscaras de clase de terreno `RIGz` y recursos `LandClass`) | el generador del juego, portado: se prueban los mismos puntos en el mismo orden con los mismos números aleatorios, las máscaras de clase de terreno y de exclusión, el objeto elegido en cada punto, su rotación, escala y desplazamiento de altura; entidades en mosaico (manzanas de pueblo) y plantadas (bosques, arbustos, campos). Se generan solo sobre el mapa de tanques. Aproximado: la altura y la normal del suelo (del mapa de altura; el juego traza un rayo), las cajas de exclusión que el juego registra en tiempo de ejecución, y el giro de los árboles (el juego lo ajusta a la paleta de rotaciones del impostor) |
| Mallas de render (recursos `RendInst` en `content/*/res/*.grp`, materiales en `riDesc.bin`) | los vértices y triángulos de cada LOD (posiciones en coma flotante; índices de 16 o 32 bits, sin comprimir o comprimidos con meshoptimizer), el material de cada elemento. Se omiten los elementos de calcomanía y de impostor en forma de panel; se conservan los transparentes (cristal) |
| Colores de los objetos | por material, el promedio de la mip pequeña de su textura difusa (ponderado por alfa en las hojas), de los paquetes de texturas de la instalación: t0 para la mayoría de los sombreadores, la primera difusa de detalle donde t0 es una superposición o una máscara. Un color por material: los objetos no llevan textura |
| Formas de colisión (`<objeto>_collision`) | recursos de colisión de la versión 3 del flujo, usados donde un objeto no tiene malla de render. Solo se dibuja lo que golpean los rayos del juego (nodos `TRACEABLE`), y las cajas, esferas y cápsulas solo cuando el recurso no tiene malla: el resto son sustitutos gruesos de física que se verían como cubos alrededor del objeto |
| Malla de navegación (`Lnav`), malla de terreno renderizada, hierba, `spgz`, `stbl`, `d2co` | no se leen |

Los niveles están comprimidos con Oodle, que es propietario. El juego incluye una copia,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (una compilación x64 corriente),
y es la que se carga; `HEAT3D_OODLE=<dll o carpeta>` apunta a otra.
Aquí no se incluye nada de Oodle.

## Formatos, y dónde están documentados {#formats-and-where-they-are-documented}

Gaijin publicó el código fuente del Dagor Engine bajo la licencia BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Los lectores de aquí se escribieron a partir
de él; no se descompiló código del juego. Cada módulo indica los archivos de código fuente que sigue:

- `vromfs.py`: `*.vromfs.bin` (cabecera `VRFs`/`VRFx`, un cuerpo zstd cuyos primeros y
  últimos 16 bytes se combinan con XOR con una clave fija, una tabla de nombres y una
  tabla de desplazamientos: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) y BLK binario (formas 1-5, con el mapa de nombres compartido
  del archivo `\xff?nm` y el diccionario zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: paquetes de texturas `DxP2` (`lib3d/texPackMgr2.cpp`) y cabeceras DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 los decodifica Pillow.
- `dagorlevel.py`: el binario del nivel (`scene/loadLevel.cpp`), el mapa de altura
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  el trazador de rayos del terreno (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) y el mapa de altura del agua
  (`fftWater/fftWater.cpp`).
- `rigen.py`: los objetos colocados (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: los objetos generados (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: instancias de render (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) y el códec de índices de
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: el color del suelo (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paquetes de recursos (`gameRes/grpData.h`) y recursos de colisión
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  cuyos triángulos se guardan como un BVH de cuádruples (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) lee los mismos archivos; no hace falta y no se usa.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
