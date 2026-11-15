---
title: Nivells (heat3d-wt-level)
nav_order: 9
lang: ca
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Nivells (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` converteix els nivells de la teva pròpia instal·lació de War Thunder en
nivells `.glb` per al visualitzador, en el mateix marc que les taules de les repeticions.

## Pas a pas {#step-by-step}

1. Llista els nivells de la teva instal·lació: `heat3d-wt-level list`. Escriu una línia per
   nivell: el seu nom, el seu terreny i els seus mapes, i després el recompte. Per exemple
   (un nivell inventat):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extreu-ne un, diversos (es permeten comodins) o tots:

   ```bash
   heat3d-wt-level extract <nivell> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <nivell> -o levels --detail high
   ```

3. Carrega `levels/<nivell>/<nivell>.glb` al panell de Nivell del visualitzador, sota les
   batalles d'aquell mapa.

Els nivells que escrius es queden a la teva màquina: no els publiquis mai (vegeu
[Condicions i llicència](terms.md)).

## Opcions {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Ordre / opció | Fa |
|---|---|
| `list [--game CARPETA]` | cada nivell de la instal·lació |
| `extract <nivells...>` / `--all` | els nivells indicats (tal com els escriu `list`; es permeten comodins), o tots |
| `-o`, `--out` | carpeta de sortida; cada nivell va a `<out>/<nivell>/` |
| `--game CARPETA` | la carpeta de War Thunder (per defecte: trobada a través de Steam o del llançador; també `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | mostreig del terreny, color del terreny i pressupost d'objectes sobre el mapa de tancs (per defecte `medium`) |
| `--max-object-triangles N` | el pressupost d'objectes (per defecte: el del detall) |
| `--max-grid N` | mostres del mapa d'alçades per costat, per part (per defecte 1024) |
| `--no-objects` | deixa fora edificis, arbres i altres objectes col·locats |
| `--no-generated` | deixa fora els objectes que generen les classes de terreny (boscos, pobles) |
| `--no-terrain-colour` | aplica al terreny el mapa tàctic, no les classes de terreny |
| `--no-texture` | deixa el terreny sense textura |
| `--skip-existing` | deixa els nivells que ja tenen el seu `.glb` |

## Què s'escriu {#what-is-written}

Cada nivell esdevé `<out>/<nivell>/<nivell>.glb`, `<nivell>.json` (què s'ha llegit, el nivell
de l'aigua, els rectangles dels mapes, els recomptes de triangles, els temps) i els mapes
tàctics del nivell com a `<nivell>_map.png` (el mapa aeri) i `<nivell>_tankmap.png`; els mapes
terrestres reben també `<nivell>_terrain.png`, els colors propis del terreny sobre el mapa de
tancs. El glb s'escriu a `<nivell>.glb.part` i es reanomena quan és complet; mentre s'escriu un
nivell, es manté `<out>/<nivell>/.<nivell>.lock`, de manera que dues extraccions mai no escriuen
el mateix nivell (la segona escriu `busy <nivell>`). La instal·lació es troba a través de Steam o
de les carpetes per defecte del llançador; `--game <carpeta>` o `HEAT3D_WT_GAME` indiquen on és,
si no es troba.

| Part | Què és |
|---|---|
| `ground:<nivell>` | el mapa d'alçades del terreny (`HM2`) com a graella; als mapes terrestres, el mig del mapa de tancs (la meitat de la seva amplada) al pas del `--detail`, acolorit amb les classes de terreny, calcomanies de terreny i carreteres (`<nivell>_terrain.png`; el mapa tàctic on no es pot fer això); als mapes sense mapa de tancs (mapes aeris), tot el mapa d'alçades a un sol pas (2048 mostres per costat a `high`, 1024 en la resta), acolorit amb les classes de terreny sobre l'àrea del mapa aeri (4096 píxels per costat, uns 32 m per píxel en 131 km; el mapa tàctic on no es pot fer això); als nivells sense mapa d'alçades, la malla del terreny |
| `ground:<nivell> tank map` | la resta del mapa de tancs, un pas més gruixut |
| `ground:<nivell> heightmap surroundings` | la resta del mapa d'alçades, encara més gruixut |
| `ground:<nivell> land mesh` | els triangles de col·lisió de la malla del terreny on el mapa d'alçades no arriba (els voltants d'un mapa de tancs, fins a desenes de quilòmetres); als nivells sense mapa d'alçades és el terreny, acolorit com s'ha dit |
| `ground:<nivell> outside the map` | el terreny que la imatge no cobreix, sense textura |
| `water:<nivell>` | un rectangle pla al `water_level` del nivell sobre tot el terreny: el joc dibuixa l'aigua com un sol pla, i el terreny baix que hi ha sota és mar, llac o llit de riu |
| `water:<nivell> rivers` | als nivells amb un mapa d'alçades d'aigua (`WHM`), la superfície d'aigua inclinada sobre les cel·les que cobreix |
| `structure:<nivell> buildings` | cada objecte col·locat que no és una planta: cases, runes, murs, tanques, ponts, vies, roques, elements. Els fixos (`RIGz`) i, sobre el mapa de tancs, els que generen les classes de terreny (blocs de pobles, pedres). Cada un es dibuixa amb la seva malla de render (murs, teulades, obertures de finestres, bigues), al nivell de detall que permet el pressupost de triangles, acolorit per material amb la mitjana de la seva textura difusa |
| `structure:<nivell> trees` | arbres i matolls, fixos i generats (boscos, filats): la seva malla de render on ho permet el pressupost, si no un tronc i una capçada (un con per a les coníferes) amb el color de fulla propi de l'arbre, a la seva mida real |

Els objectes sense malla de render recorren a la seva forma de col·lisió; els arbres sense
una, a la capçada. Els colors dels vèrtexs (`COLOR_0`) guarden valors codificats en sRGB, que
és com els llegeix el visualitzador de 3DHeat.

**Coordenades.** Són els metres del joc amb z reflectida: glb (x, y, z) = joc (x, y, -z). El
món del joc és de mà esquerra (x est, y amunt, z nord); glTF és de mà dreta. `heat3d-wt-replay`
manté la z del joc i indica al visualitzador que la reflecteixi, de manera que una repetició i el
nivell del seu mapa cauen l'un sobre l'altre sense cap pas de col·locació. El JSON dona el
rectangle de cada mapa tàctic en metres del joc i les seves cantonades en l'espai del glb, per
carregar el PNG com a imatge de mapa.

**Detall.** `--detail low|medium|high` (per defecte medium) fixa, sobre el mapa de tancs:

| | mig del mapa de tancs | resta del mapa de tancs | color del terreny | pressupost d'objectes | més triangles per objecte | plantes generades que es mantenen |
|---|---|---|---|---|---|---|
| low | cada 4a mostra | cada 8a | 4 m per píxel | 1,2 M | 1.500 | arbres 35 %, matolls 20 % |
| medium | cada 2a | cada 4a | 2 m | 3,5 M | 4.000 | arbres 70 %, matolls 50 % |
| high | cada mostra (2 m a la majoria de mapes terrestres) | cada 2a | 1 m (com a màxim 4096 píxels per costat) | 4,5 M | 12.000 | totes |

Els dos anells del mapa de tancs es limiten a 0,3 M (low), 1 M (medium) i 3,7 M (high)
triangles: als mapes amb un mapa d'alçades més fi que 2 m, els passos es dupliquen (primer
l'anell exterior) fins que hi caben, de manera que surten també a uns 2 m.

Un mapa terrestre a `high` surt a uns 8 milions de triangles (3,5 M de terreny, 4,5 M
d'objectes) i 250 MB; a `medium`, a uns 4,5 M. Els nivells de detall dels objectes són els
que el mateix joc dibuixaria des d'una sola distància de visió: el més curt que cap al
pressupost; els petits objectes baixen primer a nivells gruixuts, i els edificis grans
l'últim, segons els rangs que va donar el seu autor a cada nivell (el `lodDistance` del JSON);
allò que l'estalvi d'aquest pas deixa per sobre del pressupost es torna als objectes més
grans. El color del terreny de baixa resolució (mapes aeris) fa la mitjana de les textures en
mosaic de cada classe de terreny fins a la mida del píxel primer, perquè els mosaics no
produeixin patrons de batement. Si ni tan sols els nivells de detall més gruixuts hi caben, els
arbres que més estalvien es converteixen en capçades, i després es deixen fora els tipus més
petits (`leftOut`); cap objecte no es dibuixa com una caixa (una forma de col·lisió, si n'hi ha
una, és la pròpia de l'objecte). Els objectes generats es limiten de manera determinista per
tipus (`density`), els mateixos a cada execució. `--max-object-triangles` substitueix el
pressupost, `--max-grid` (per defecte 1024) limita les parts més gruixudes del mapa
d'alçades, `--no-objects` deixa fora els objectes, `--no-generated` els generats,
`--no-terrain-colour` aplica al terreny el mapa tàctic, i `--no-texture` el deixa sense
textura.

El JSON `parts.objects` llista les instàncies (fixes i generades, per tipus i classe de
terreny), quantes s'han dibuixat i a quin nivell de detall (`drawnAs`), els triangles, la
distància del nivell de detall i els segons; `parts.heightmap.rings` el pas i els triangles de
cada anell del terreny; `parts.terrainColour` les classes de terreny i els seus colors, les
carreteres i les calcomanies de terreny; `trianglesTotal`, `glbBytes` i `secondsBy` els totals.

## Què es llegeix, i com de bé {#what-is-read-and-how-well}

| Part | Estat |
|---|---|
| Binari del nivell (`levels/<nivell>.bin`, `DBLD` 3x64): taula de blocs | cada nivell comprovat |
| Mapa d'alçades (`HM2`, versions 0-2; la versió 2 són valors de 8 bits en blocs, en trossos Oodle o zstd) | cada nivell amb mapa d'alçades de versió 2 i trossos Oodle; comprovat a ull contra els seus mapes tàctics (rius, valls, costes i pobles casen) |
| Col·lisió de la malla del terreny (`lmap`, el seu traçador de rajos `LTdump`) | llegida on un nivell en té una (empaquetada en Oodle). És la superfície de col·lisió del joc, no la malla renderitzada, de manera que és més gruixuda on el terreny és pla |
| Color del terreny (classes de terreny i mapa de pesos de `lmap`, mapa de física `LMp2`, splines `hspl`) | els mapes de color de les classes de terreny i les seves textures de detall (els seus colors mitjans) ponderats pel mapa de pesos, l'índex de biomes d'1 m de les classes de terreny indexades, les formes de carretera i de calcomanies de terreny del mapa de física al color de la textura del seu spline o material, penya-segats a les pendents fortes. Comprovat amb els mapes de tancs: les carreteres, els pobles, els llacs, els cinturons de bosc i les aflorament de roca casen. La fórmula de color del shader del terreny propi de War Thunder no és al codi font públic; s'usa la publicada pel motor (daNetGame), que surt més saturada que el mapa tàctic |
| Nivell de l'aigua | `water_level` del BLK del nivell a `aces.vromfs.bin` (0 quan no en té) |
| Mapa d'alçades de l'aigua (`WHM`: una graella de cel·les planes i pàgines de 130x130 d'alçades de 16 bits) | llegit on un nivell en té un; els seus rius s'inclinen amb el terreny |
| Mapes tàctics | de `content/base/res/locations_maps.dxp.bin`, col·locats segons `mapCoord0/1` i `tankMapCoord0/1` del BLK; la part superior de la imatge és el nord |
| Objectes col·locats (`RIGz`: les instàncies fixes del generador d'instàncies de render) | cada instància, com una matriu 3x4 de valors de 16 bits o, en alguns nivells, de 32 bits (el nombre de bytes de la cel·la ho decideix); cada byte de cada cel·la comptat als nivells comprovats |
| Objectes generats (màscares de classes de terreny de `RIGz` i recursos `LandClass`) | el generador del joc, portat: els mateixos llocs provats en el mateix ordre amb els mateixos nombres aleatoris, les màscares de classes de terreny i d'exclusió, l'objecte escollit a cada lloc, la seva rotació, escala i desplaçament d'alçada; entitats en mosaic (blocs de pobles) i plantades (boscos, matolls, camps). Generats només sobre el mapa de tancs. Aproximats: l'alçada i la normal del terreny (del mapa d'alçades; el joc traça un raig), les caixes d'exclusió que el joc registra en temps d'execució, i el guinyol dels arbres (el joc l'ajusta a la paleta de rotacions de l'impostor) |
| Malles de render (recursos `RendInst` a `content/*/res/*.grp`, materials a `riDesc.bin`) | els vèrtexs i triangles de cada LOD (posicions en float; índexs de 16 o 32 bits, nets o empaquetats amb meshoptimizer), el material de cada element. Els elements de calcomania i d'impostor-cartell es deixen fora; els transparents (vidre) es mantenen |
| Colors dels objectes | per material, la mitjana del petit mipmap de la seva textura difusa (ponderada per alfa per a les fulles), dels paquets de textures de la instal·lació: t0 per a la majoria de shaders, la primera textura difusa de detall quan t0 és una superposició o una màscara. Un color per material: cap textura als objectes |
| Formes de col·lisió (`<objecte>_collision`) | recursos de col·lisió de versió de flux 3, usats quan un objecte no té malla de render. Només es dibuixa el que impacten els raigs del joc (els nodes `TRACEABLE`), i les caixes, esferes i càpsules només quan el recurs no té malla: la resta són substituts físics grollers que es veurien com a cubs al voltant de l'objecte |
| Malla de navegació (`Lnav`), la malla del terreny renderitzada, herba, `spgz`, `stbl`, `d2co` | no llegits |

Els nivells estan comprimits amb Oodle, que és propietari. El joc en porta una còpia,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (una compilació x64 corrent), i és la que es
carrega; `HEAT3D_OODLE=<dll o carpeta>` apunta a una altra. Aquí no s'inclou res d'Oodle.

## Formats, i on estan documentats {#formats-and-where-they-are-documented}

Gaijin va publicar el codi font del motor Dagor sota la llicència BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Els lectors d'aquí es van escriure a partir d'ell;
no es va descompilar cap codi del joc. Cada mòdul indica els fitxers font que segueix:

- `vromfs.py`: `*.vromfs.bin` (capçalera `VRFs`/`VRFx`, un cos zstd del qual els primers i els
  darrers 16 bytes són XOR amb una clau fixa, una taula de noms i una taula de desplaçaments:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) i BLK
  binari (formes 1-5, amb el mapa de noms compartit de l'arxiu `\xff?nm` i el diccionari zstd:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: paquets de textures `DxP2` (`lib3d/texPackMgr2.cpp`) i capçaleres DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 els decodifica Pillow.
- `dagorlevel.py`: el binari del nivell (`scene/loadLevel.cpp`), el mapa d'alçades
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), el traçador
  de rajos del terreny (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) i el mapa
  d'alçades de l'aigua (`fftWater/fftWater.cpp`).
- `rigen.py`: els objectes col·locats (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: els objectes generats (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`,
  `riGen/riGenData.h`, `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp`
  (`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`,
  `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`,
  `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: instàncies de render (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`,
  `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) i el
  codec d'índexs de meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: el color del terreny (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`,
  `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`,
  `land_weight_inc.dshl`, `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`,
  `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paquets de recursos (`gameRes/grpData.h`) i recursos de col·lisió
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), els triangles
  dels quals s'emmagatzemen com un BVH de quads (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`,
  `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) llegeix els mateixos arxius; no és necessari i no s'usa.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
