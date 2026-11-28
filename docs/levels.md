---
title: Levels
nav_order: 9
---

# Levels (heat3d-wt-level)

`heat3d-wt-level` turns the levels of your own War Thunder install into
`.glb` levels for the viewer, in the same frame as the replays' tables.

## Step by step

1. List the levels of your install: `heat3d-wt-level list`. It prints one
   line per level: its name, its terrain and its maps, then the count. For
   example (an invented level):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extract one, several (wildcards allowed) or all:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Load `levels/<level>/<level>.glb` in the viewer's Background / level panel, under the
   battles of that map.

The levels you write stay on your machine: never publish them (see
[Terms and licence](terms.md)).

## Options

![heat3d-wt-level extract --help](assets/img/level-help.svg)

| Command / option | Does |
|---|---|
| `list [--game FOLDER]` | every level in the install |
| `extract <levels...>` / `--all` | the levels named (as `list` prints them; wildcards allowed), or every level |
| `-o`, `--out` | output folder; each level goes in `<out>/<level>/` |
| `--game FOLDER` | the War Thunder folder (default: found through Steam or the launcher; also `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | ground sampling, ground colour and object budget over the tank map (default `medium`) |
| `--max-object-triangles N` | the object budget (default: the detail's) |
| `--max-grid N` | heightmap samples a side, per part (default 1024) |
| `--no-objects` | leave out buildings, trees and other placed objects |
| `--no-generated` | leave out the objects the land classes generate (forests, towns) |
| `--no-terrain-colour` | texture the ground with the tactical map, not the land classes |
| `--no-texture` | leave the ground untextured |
| `--skip-existing` | leave levels whose `.glb` exists |

## What is written

Each level becomes `<out>/<level>/<level>.glb`, `<level>.json` (what was read,
the water level, the map rectangles, triangle counts, timings) and the level's
tactical maps as `<level>_map.png` (the air map) and `<level>_tankmap.png`;
ground maps also get `<level>_terrain.png`, the ground's own colours over the
tank map. The glb is written to `<level>.glb.part` and renamed when complete;
while a level is written, `<out>/<level>/.<level>.lock` is held, so two
extractions never write the same level (the second prints `busy <level>`).
The install is found through Steam or the launcher's default folders;
`--game <folder>` or `HEAT3D_WT_GAME` say where it is otherwise.

| Part | What it is |
|---|---|
| `ground:<level>` | the terrain heightmap (`HM2`) as a grid; on ground maps the middle of the tank map (half its width) at the `--detail`'s step, coloured with the land classes, ground decals and roads (`<level>_terrain.png`; the tactical map where that cannot be made); on maps without a tank map (air maps), the whole heightmap at one step (2048 samples a side at `high`, 1024 otherwise), coloured with the land classes over the air map's area (4096 pixels a side, about 32 m a pixel over 131 km; the tactical map where that cannot be made); on levels without a heightmap, the land mesh |
| `ground:<level> tank map` | the rest of the tank map, one step coarser |
| `ground:<level> heightmap surroundings` | the rest of the heightmap, coarser still |
| `ground:<level> land mesh` | the land mesh's collision triangles where the heightmap does not reach (the surroundings of a tank map, out to tens of kilometres); on levels with no heightmap it is the ground, coloured as above |
| `ground:<level> outside the map` | ground the image does not cover, untextured |
| `water:<level>` | one flat rectangle at the level's `water_level` over all the terrain: the game draws water as one plane, and low ground under it is sea, lake or river bed |
| `water:<level> rivers` | on levels with a water heightmap (`WHM`), the sloping water surface over the cells it covers |
| `structure:<level> buildings` | every placed object that is not a plant: houses, ruins, walls, fences, bridges, rails, rocks, props. The fixed ones (`RIGz`) and, over the tank map, those the land classes generate (town blocks, stones). Each is drawn by its render mesh (walls, roofs, window openings, beams), at the LOD the triangle budget allows, coloured per material by the average of its diffuse texture |
| `structure:<level> trees` | trees and bushes, fixed and generated (forests, hedgerows): their render mesh where the budget allows, otherwise a trunk and a crown (a cone for conifers) in the tree's own leaf colour, over the tree's real size |

Objects without a render mesh fall back to their collision shape; trees
without one to the crown. Vertex colours (`COLOR_0`) hold sRGB-encoded values,
which is how the 3DHeat viewer reads them.

**Coordinates** are the game's metres with z mirrored: glb (x, y, z) = game
(x, y, -z). The game's world is left-handed (x east, y up, z north); glTF is
right-handed. `heat3d-wt-replay` keeps the game's z and tells the viewer to
mirror it, so a replay and the level of its map land on top of each other with
no placement step. The JSON gives each tactical map's rectangle in game metres
and its corners in the glb's space, for loading the PNG as a map image.

**Detail.** `--detail low|medium|high` (default medium) sets, over the tank map:

| | middle of the tank map | rest of the tank map | ground colour | object budget | most triangles per object | generated plants kept |
|---|---|---|---|---|---|---|
| low | every 4th sample | every 8th | 4 m a pixel | 1.2 M | 1,500 | trees 35 %, bushes 20 % |
| medium | every 2nd | every 4th | 2 m | 3.5 M | 4,000 | trees 70 %, bushes 50 % |
| high | every sample (2 m on most ground maps) | every 2nd | 1 m (at most 4096 pixels a side) | 4.5 M | 12,000 | all |

The two tank-map rings are held to 0.3 M (low), 1 M (medium) and 3.7 M (high)
triangles: on the maps whose heightmap is finer than 2 m, the steps double
(the outer ring first) until they fit, so those come out at about 2 m too.

A ground map at `high` comes out at about 8 million triangles (3.5 M of ground,
4.5 M of objects) and 250 MB; at `medium` at about 4.5 M. The objects' LODs are
the ones the game itself would draw from one viewing distance, the shortest
whose total fits the budget: small props drop to coarse LODs first and large
buildings last, by the ranges their makers gave each LOD (the JSON's
`lodDistance`); what that step saves beyond the budget goes back to the largest
objects. Coarse ground colour (air maps) averages each land class's tiled textures down to the pixel size first, so
the tiles do not alias into a moire. If even the coarsest LODs do not fit, the trees that save most become
crowns, and then the smallest types are left out (`leftOut`); no object is
drawn as a box (a collision shape, if any, is the object's own).
Generated objects are thinned deterministically by kind (`density`), the same
ones every run. `--max-object-triangles` overrides the budget,
`--max-grid` (default 1024) caps the heightmap's coarser parts, `--no-objects`
leaves objects out, `--no-generated` the generated ones, `--no-terrain-colour`
textures the ground with the tactical map, `--no-texture` leaves it untextured.

The JSON's `parts.objects` lists instances (fixed and generated, by kind and
land class), how many were drawn at which LOD (`drawnAs`), the triangles, the
LOD distance and the seconds; `parts.heightmap.rings` each ground ring's step
and triangles; `parts.terrainColour` the land classes and their colours, roads
and ground decals; `trianglesTotal`, `glbBytes` and `secondsBy` the totals.

## Game-mode layouts

`heat3d-wt-level layouts <level>... | --all | --extracted -o <folder>` reads the
multiplayer missions of your install (`mis.vromfs.bin`) and writes each level's
`<folder>/<level>/<level>.layouts.json` beside its `.glb`. The viewer draws the
layout on the level by itself (Objectives panel, and the Tactics board):

- one layout per mission and difficulty (arcade, realistic, simulator; one
  layout where they are the same): capture zones with their letters, the
  battle area, the ground the battle excludes and each side's spawn kill area
  (hatched as out of bounds), spawn points (ground, air, helicopter, naval,
  convoys), airfields, helipads, bases and bombing targets;
- where a mission has separate sets for battle-rating tiers (airfields, air
  spawns, bombing targets), each tier is a stage of the layout, picked under
  **Layout**.

`--extracted` writes the levels already extracted into the output folder. A
mission may swap the sides at random: team 1 is the mission's first side.

## What is read, and how well

| Part | Status |
|---|---|
| Level binary (`levels/<level>.bin`, `DBLD` 3x64): block table | every level checked |
| Heightmap (`HM2`, versions 0-2; version 2 is 8-bit values in blocks, Oodle or zstd chunks) | every level whose heightmap is version 2 with Oodle chunks; checked by eye against their tactical maps (rivers, valleys, coasts and towns line up) |
| Land mesh collision (`lmap`, its `LTdump` land ray tracer) | read where a level has one (Oodle-packed). It is the game's collision surface, not the rendered mesh, so it is coarser where the land is flat |
| Rendered land mesh (`lmap` mesh data: vertex data as a render instance's, per cell a `ShaderMesh` per LOD; 16-bit positions over the cell in x and z and over the land's height range in y) | the finest LOD of every cell, where a level has no land ray tracer: the levels of game builds 2.61 and later carry none, so their land (air maps, naval and older ground maps without a heightmap, the surroundings of a heightmap) is this mesh; on the levels checked it has about as many triangles as the tracer had, over the same area and heights |
| Ground colour (`lmap` land classes and weight map, `LMp2` physics map, `hspl` splines) | the land classes' colour maps and detail textures (their average colours) weighted by the weight map, the 1 m biome index of indexed land classes, the road and ground-decal shapes of the physics map in the colour of their spline's or material's texture, cliffs on steep slopes. Checked against the tank maps: roads, towns, lakes, forest belts and rock outcrops line up. The colour formula of War Thunder's own terrain shader is not in the public source; the engine's published one (daNetGame) is used, which comes out more saturated than the tactical map |
| Water level | `water_level` from the level's BLK in `aces.vromfs.bin` (0 where it has none) |
| Water heightmap (`WHM`: a grid of flat cells and 130x130 pages of 16-bit heights) | read where a level has one; its rivers slope with the ground |
| Tactical maps | from `content/base/res/locations_maps.dxp.bin`, placed by the BLK's `mapCoord0/1` and `tankMapCoord0/1`; the image's top is north |
| Placed objects (`RIGz`: the render-instance generator's fixed instances) | every instance, as a 3x4 matrix of 16-bit values or, on some levels, 32-bit ones (the cell's byte count decides); every byte of every cell accounted for on the levels checked |
| Generated objects (`RIGz` land-class masks and the `LandClass` resources) | the game's generator, ported: the same spots tried in the same order with the same random numbers, the land-class and exclusion masks, the object picked at each spot, its rotation, scale and height offset; tiled (town blocks) and planted (forests, bushes, fields) entities. Generated over the tank map only. Approximated: the ground height and normal (from the heightmap; the game traces a ray), the exclusion boxes the game registers at run time, and trees' yaw (the game snaps it to the impostor's rotation palette). |
| Render meshes (`RendInst` resources in `content/*/res/*.grp`, materials in `riDesc.bin`) | every LOD's vertices and triangles (float positions; 16 or 32-bit indices, plain or meshoptimizer-packed), each element's material. Decal and impostor-billboard elements are left out; the transparent ones (glass) are kept |
| Object colours | per material, the average of its diffuse texture's small mip (alpha-weighted for leaves), from the install's texture packs: t0 for most shaders, the first detail diffuse where t0 is an overlay or a mask. One colour per material: no texture on the objects |
| Collision shapes (`<object>_collision`) | collision resources of stream version 3, used where an object has no render mesh. Only what the game's rays hit (`TRACEABLE` nodes) is drawn, and boxes, spheres and capsules only when the resource has no mesh: the rest are coarse physics stand-ins that would show as cubes around the object |
| Navigation mesh (`Lnav`), the rendered land mesh's decal, combined and patch meshes, grass, `spgz`, `stbl`, `d2co` | not read |

Levels are compressed with Oodle, which is proprietary. The game ships a copy,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (an ordinary x64 build), and
that is what is loaded; `HEAT3D_OODLE=<dll or folder>` points at another.
Nothing of Oodle is included here.

## Formats, and where they are documented

Gaijin published the Dagor Engine's source under the BSD 3-Clause licence
(github.com/GaijinEntertainment/DagorEngine). The readers here were written from
it; no game code was decompiled. Each module names the source files it follows:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, a zstd body whose first and
  last 16 bytes are XORed with a fixed key, a name table and an offset table:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  and binary BLK (forms 1-5, with the archive's shared name map `\xff?nm` and
  zstd dictionary: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: texture packs `DxP2` (`lib3d/texPackMgr2.cpp`) and DDSx headers
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 are decoded by Pillow.
- `dagorlevel.py`: the level binary (`scene/loadLevel.cpp`), the heightmap
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  the land ray tracer and the rendered land mesh (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`, `landMesh/lmeshRenderer.cpp`) and the water heightmap
  (`fftWater/fftWater.cpp`).
- `rigen.py`: the placed objects (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: the generated objects (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: render instances (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) and meshoptimizer's
  index codec (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: the ground's colour (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: resource packs (`gameRes/grpData.h`) and collision resources
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  whose triangles are stored as a quad BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) reads the same archives; it is not needed and not used.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
