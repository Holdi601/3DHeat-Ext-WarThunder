---
title: "Levelen"
nav_order: 9
lang: lb
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Levelen (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` mécht aus de Levelen vun Ärer eegener War-Thunder-Installatioun
`.glb`-Levelen fir de Viewer, am selwechte System wéi d'Tabelle vun de Replays.

## Schrëtt fir Schrëtt {#step-by-step}

1. Lëscht d'Levelen vun Ärer Installatioun op: `heat3d-wt-level list`. Et dréckt eng
   Zeil pro Level: säin Numm, säin Terrain a seng Kaarten, dann d'Zuel. Zum
   Beispill (e erfonnent Level):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrahéiert een, e puer (Wildcards erlaabt) oder all:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Luet `levels/<level>/<level>.glb` am Panel „Hannergrond / Level“ vum Viewer, ënner de
   Gefechter vun där Kaart.

D'Levelen, déi Dir schreift, bleiwen op Ärer Maschinn: verëffentlecht se ni (kuck
[Konditiounen a Lizenz](terms.md)).

## Optiounen {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Befehl / Optioun | Wat et mécht |
|---|---|
| `list [--game FOLDER]` | all Level an der Installatioun |
| `extract <levels...>` / `--all` | d'Levelen, déi genannt ginn (wéi `list` se dréckt; Wildcards erlaabt), oder all Level |
| `-o`, `--out` | Ausgabdossier; all Level geet an `<out>/<level>/` |
| `--game FOLDER` | den War-Thunder-Dossier (Standard: iwwer Steam oder de Launcher fonnt; och `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | Buedem-Sampling, Buedemfaarf an Objetbudget iwwer der Panzerkaart (Standard `medium`) |
| `--max-object-triangles N` | d'Objetbudget (Standard: dat vum Detail) |
| `--max-grid N` | Héichtekaart-Echantillonen pro Säit, pro Deel (Standard 1024) |
| `--no-objects` | Gebaier, Beem an aner gesat Objeten ewechloossen |
| `--no-generated` | d'Objeten ewechloossen, déi d'Land-Klasse generéieren (Wälder, Stied) |
| `--no-terrain-colour` | de Buedem mat der taktescher Kaart texturéieren, net mat de Land-Klassen |
| `--no-texture` | de Buedem ouni Textur loossen |
| `--skip-existing` | Levelen iwwersprangen, där hir `.glb` et gëtt |

## Wat geschriwwen gëtt {#what-is-written}

All Level gëtt `<out>/<level>/<level>.glb`, `<level>.json` (wat gelies gouf,
d'Waasserniveau, d'Kaartrechtecker, Dräieckszuelen, Zäiten) an d'taktesch Kaarte vum Level
als `<level>_map.png` (d'Loftkaart) an `<level>_tankmap.png`;
Buedemkaarte kréien och `<level>_terrain.png`, dem Buedem seng eege Faarwen iwwer der
Panzerkaart. D'glb gëtt an `<level>.glb.part` geschriwwen an ëmbenannt, wann se fäerdeg ass;
während e Level geschriwwen gëtt, gëtt `<out>/<level>/.<level>.lock` gehalen, sou datt zwou
Extraktiounen ni dat selwecht Level schreiwen (déi zweet dréckt `busy <level>`).
D'Installatioun gëtt iwwer Steam oder d'Standarddossiere vum Launcher fonnt;
`--game <folder>` oder `HEAT3D_WT_GAME` soen, wou se soss ass.

| Deel | Wat et ass |
|---|---|
| `ground:<level>` | d'Terrain-Héichtekaart (`HM2`) als Gitter; op Buedemkaarten d'Mëtt vun der Panzerkaart (hallef hir Breet) am Schrëtt vum `--detail`, agefierft mat de Land-Klassen, Buedemdecals a Stroossen (`<level>_terrain.png`; d'taktesch Kaart, wou dat net gemaach ka ginn); op Kaarten ouni Panzerkaart (Loftkaarten) déi ganz Héichtekaart an engem Schrëtt (2048 Echantillonen pro Säit bei `high`, soss 1024), agefierft mat de Land-Klassen iwwer dem Gebitt vun der Loftkaart (4096 Pixel pro Säit, ongeféier 32 m de Pixel iwwer 131 km; d'taktesch Kaart, wou dat net gemaach ka ginn); op Levelen ouni Héichtekaart d'Land-Mesh |
| `ground:<level> tank map` | de Rescht vun der Panzerkaart, een Schrëtt gréber |
| `ground:<level> heightmap surroundings` | de Rescht vun der Héichtekaart, nach gréber |
| `ground:<level> land mesh` | d'Kollisiounsdräiecker vum Land-Mesh, wou d'Héichtekaart net hinreecht (d'Ëmgéigend vun enger Panzerkaart, bis op zéng Kilometer); op Levelen ouni Héichtekaart ass et de Buedem, agefierft wéi uewen |
| `ground:<level> outside the map` | Buedem, deen d'Bild net deckt, ouni Textur |
| `water:<level>` | ee flacht Rechteck um `water_level` vum Level iwwer dem ganzen Terrain: d'Spill zeechent Waasser als eng Fläch, an niddregt Land drënner ass Mier-, Séi- oder Floss-Buedem |
| `water:<level> rivers` | op Levelen mat enger Waasser-Héichtekaart (`WHM`) d'schréi Waasseroberfläch iwwer den Zellen, déi se deckt |
| `structure:<level> buildings` | all gesat Objet, dat keng Planz ass: Haiser, Ruinen, Maueren, Zonen, Brécken, Schinnen, Fielsen, Props. Déi fest (`RIGz`) an, iwwer der Panzerkaart, déi, déi d'Land-Klasse generéieren (Stadblocken, Steng). Jiddwer gëtt duerch säi Render-Mesh gezeechent (Maueren, Daach, Fënsteröffnungen, Balken), am LOD, dat d'Dräieckbudget erlaabt, pro Material agefierft mam Duerchschnëtt vu senger Diffus-Textur |
| `structure:<level> trees` | Beem a Bëscher, fest a generéiert (Wälder, Hecken): hire Render-Mesh, wou d'Budget et erlaabt, soss e Stamm an eng Kroun (e Kegel bei Nolbeem) an der eegener Blieder-Faarf vum Bam, iwwer der richteger Gréisst vum Bam |

Objeten ouni Render-Mesh falen op hir Kollisiounsform zeréck; Beem
ouni een op d'Kroun. Vertex-Faarwen (`COLOR_0`) halen sRGB-kodéiert Wäerter,
sou wéi den 3DHeat-Viewer se liest.

**Koordinaten** sinn d'Meter vum Spill mat gespigeltem z: glb (x, y, z) = Spill
(x, y, -z). Dem Spill seng Welt ass lénkshändeg (x Ouschten, y erop, z Norden); glTF ass
rietshändeg. `heat3d-wt-replay` behält dem Spill säi z a seet dem Viewer, et ze
spigelen, sou datt e Replay an d'Level vu senger Kaart openeen landen, ouni
Plazéierungsschrëtt. D'JSON gëtt dem Rechteck vun all taktescher Kaart a Spillmeter
a seng Ecker am Raum vun der glb, fir d'PNG als Kaartbild ze lueden.

**Detail.** `--detail low|medium|high` (Standard medium) setzt, iwwer der Panzerkaart:

| | Mëtt vun der Panzerkaart | Rescht vun der Panzerkaart | Buedemfaarf | Objetbudget | meescht Dräiecker pro Objet | generéiert Planzen behalen |
|---|---|---|---|---|---|---|
| low | all 4. Echantillon | all 8. | 4 m de Pixel | 1.2 M | 1,500 | Beem 35 %, Bëscher 20 % |
| medium | all 2. | all 4. | 2 m | 3.5 M | 4,000 | Beem 70 %, Bëscher 50 % |
| high | all Echantillon (2 m op de meeschte Buedemkaarten) | all 2. | 1 m (héchstens 4096 Pixel pro Säit) | 4.5 M | 12,000 | all |

Déi zwee Panzerkaart-Réng gi bei 0.3 M (low), 1 M (medium) an 3.7 M (high)
Dräiecker gehalen: op de Kaarten, där hir Héichtekaart méi fein ass wéi 2 m, verduebelen sech d'Schrëtt
(de baussent Rank als éischt), bis se passen, dofir kommen déi och bei ongeféier 2 m eraus.

Eng Buedemkaart bei `high` kënnt bei ongeféier 8 Millioune Dräiecker eraus (3.5 M Buedem,
4.5 M Objeten) an 250 MB; bei `medium` bei ongeféier 4.5 M. D'LODe vun den Objete sinn
déi, déi d'Spill selwer vun enger Bekuckdistanz géif zeechnen, déi kierzest,
där hir Zomm an d'Budget passt: kleng Props falen als éischt op gréif LODen, grouss
Gebaier als lescht, no de Reechwäiten, déi hir Hiersteller all LOD ginn hunn (dem JSON säi
`lodDistance`); wat dee Schrëtt iwwer d'Budget eraus spuert, geet zréck un déi gréissten
Objeten. Gréif Buedemfaarf (Loftkaarten) mëttelt d'getilte Texture vun all Land-Klass fir d'éischt op d'Pixelgréisst erof, sou datt
d'Kachele net zu engem Moiré aliasen. Wann och déi gréifste LODen net passen, ginn d'Beem, déi am meeschte spueren,
Kroune, an dann ginn déi klengste Typen ewechgelooss (`leftOut`); kee Objet gëtt
als Këscht gezeechent (eng Kollisiounsform, wann et eng gëtt, ass dem Objet seng eege).
Generéiert Objete ginn deterministesch no Aart verdënnt (`density`), émmer déiselwecht
bei all Laf. `--max-object-triangles` iwwerschreift d'Budget,
`--max-grid` (Standard 1024) begrenzt déi gréberen Deeler vun der Héichtekaart, `--no-objects`
léisst Objeten ewech, `--no-generated` déi generéiert, `--no-terrain-colour`
texturéiert de Buedem mat der taktescher Kaart, `--no-texture` léisst en ouni Textur.

D'`parts.objects` vum JSON lëscht d'Instanzen (fest a generéiert, no Aart a
Land-Klass), wéi vill an wéi engem LOD gezeechent goufen (`drawnAs`), d'Dräiecker, d'
LOD-Distanz an d'Sekonnen; `parts.heightmap.rings` dem Schrëtt an d'Dräiecker vun all Buedemrank;
`parts.terrainColour` d'Land-Klassen an hir Faarwen, Stroossen
a Buedemdecals; `trianglesTotal`, `glbBytes` an `secondsBy` d'Totaler.

## Wat gelies gëtt, a wéi gutt {#what-is-read-and-how-well}

| Deel | Status |
|---|---|
| Level-Binär (`levels/<level>.bin`, `DBLD` 3x64): Blocktabell | all Level gepréift |
| Héichtekaart (`HM2`, Versiounen 0-2; Versioun 2 sinn 8-Bit-Wäerter a Blöck, Oodle- oder zstd-Chunken) | all Level, deem seng Héichtekaart Versioun 2 mat Oodle-Chunke ass; mam A géint hir taktesch Kaarte gepréift (Flëss, Däller, Küsten a Stied passen openeen) |
| Land-Mesh-Kollisioun (`lmap`, säin `LTdump`-Land-Ray-Tracer) | gelies, wou e Level een huet (Oodle-gepaakt). Et ass dem Spill seng Kollisiounsfläch, net de gerenderte Mesh, dofir ass et méi grob, wou d'Land flaach ass |
| Buedemfaarf (`lmap`-Land-Klassen a Gewiichtskaart, `LMp2`-Physikkaart, `hspl`-Splines) | d'Faarfkaarten an Detail-Texture vun de Land-Klassen (hir Duerchschnëttsfaarwen), mat der Gewiichtskaart gewichtet, den 1-m-Biom-Index vun indexéierte Land-Klassen, d'Stroossen- an Buedemdecal-Formen vun der Physikkaart an der Faarf vun der Textur vun hirem Spline oder Material, Klippen op steile Hänn. Géint d'Panzerkaarte gepréift: Stroossen, Stied, Séien, Bëschstreifen a Fielsenausbréch passen openeen. D'Faarfformel vum eegenen Terrain-Shader vu War Thunder ass net am ëffentleche Quellcode; déi publizéiert vun der Engine (daNetGame) gëtt benotzt, déi méi gesätteg erauskënnt wéi d'taktesch Kaart |
| Waasserniveau | `water_level` aus dem BLK vum Level an `aces.vromfs.bin` (0, wou et keen huet) |
| Waasser-Héichtekaart (`WHM`: e Gitter vu flache Zellen a 130x130-Säite vu 16-Bit-Héichten) | gelies, wou e Level een huet; seng Flëss sinn mam Buedem schräi |
| Taktesch Kaarten | aus `content/base/res/locations_maps.dxp.bin`, gesat duerch dem BLK säin `mapCoord0/1` an `tankMapCoord0/1`; d'Uewen vum Bild ass Norden |
| Gesat Objeten (`RIGz`: déi fest Instanze vum Render-Instanz-Generator) | all Instanz, als 3x4-Matrix vu 16-Bit-Wäerter oder, op e puer Levelen, 32-Bit-Wäerter (d'Byte-Zuel vun der Zell entscheet); all Byte vun all Zell erkläert op de gepréiften Levelen |
| Generéiert Objeten (`RIGz`-Land-Klass-Maskë an d'`LandClass`-Ressourcen) | dem Spill säi Generator, portéiert: déiselwecht Plazen an der selwechter Reiefolleg probéiert mat de selwechten Zoufallszuelen, d'Land-Klass- an Ausschlossmaskë, dat Objet, dat un all Plaz gewielt gëtt, seng Rotatioun, Skala a Héicheoffset; getilte (Stadblocken) a gepflanzten (Wälder, Bëscher, Felder) Entitéiten. Nëmmen iwwer der Panzerkaart generéiert. Approximéiert: d'Buedemhéicht an d'Normal (aus der Héichtekaart; d'Spill verfollegt e Stral), d'Ausschlossboxen, déi d'Spill zur Laafzäit registréiert, an dem Beem säi Yaw (d'Spill rastert en op d'Rotatiounspalett vum Impostor) |
| Render-Meshen (`RendInst`-Ressourcen an `content/*/res/*.grp`, Materialien an `riDesc.bin`) | d'Vertexen an Dräiecker vun all LOD (Float-Positiounen; 16- oder 32-Bit-Indexen, plain oder meshoptimizer-gepaakt), d'Material vun all Element. Decal- an Impostor-Billboard-Elementer ginn ewechgelooss; déi duerchsiichteg (Glas) bleiwen |
| Objetfaarwen | pro Material, den Duerchschnëtt vum klenge Mip vu senger Diffus-Textur (alpha-gewichtet bei Blieder), aus den Texturpäck vun der Installatioun: t0 fir déi meescht Shader, den éischten Detail-Diffus, wou t0 en Overlay oder eng Mask ass. Eng Faarf pro Material: keng Textur op den Objeten |
| Kollisiounsformen (`<object>_collision`) | Kollisiounsressourcen vum Stroumversioun 3, benotzt, wou en Objet kee Render-Mesh huet. Nëmmen dat, wat dem Spill seng Strale treffen (`TRACEABLE`-Knuet), gëtt gezeechent, a Këschten, Kugelen a Kapselen nëmmen, wann d'Ressource kee Mesh huet: de Rescht sinn gréif Physik-Ersatzformen, déi als Kuben ëm den Objet géife erschéngen |
| Navigatiounsmesh (`Lnav`), de gerenderte Land-Mesh, Gras, `spgz`, `stbl`, `d2co` | net gelies |

Levelen si mat Oodle komprimiert, dat proprietär ass. D'Spill liwwert eng Kopie mat,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (en normale x64-Build), an
déi gëtt gelueden; `HEAT3D_OODLE=<dll or folder>` weist op eng aner.
Näischt vun Oodle ass hei abegraff.

## Formater, a wou se dokumentéiert sinn {#formats-and-where-they-are-documented}

Gaijin huet de Quellcode vun der Dagor Engine ënner der BSD-3-Clause-Lizenz verëffentlecht
(github.com/GaijinEntertainment/DagorEngine). D'Reader hei goufen domat
geschriwwen; et gouf kee Spillcode dekompiléiert. All Modul nennt d'Quelldateien, deenen en follegt:

- `vromfs.py`: `*.vromfs.bin` (Header `VRFs`/`VRFx`, e zstd-Kierper, dee seng éischt a
  lescht 16 Bytes mat engem fixe Schlëssel XOR-t kréien, eng Nimmtabell an eng Offsettabell:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  a binäre BLK (Forme 1-5, mat der gedeelter Nimmkaart vum Archiv `\xff?nm` an
  zstd-Dictionnaire: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: Texturpäck `DxP2` (`lib3d/texPackMgr2.cpp`) an DDSx-Header
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 ginn vu Pillow decodéiert.
- `dagorlevel.py`: d'Level-Binär (`scene/loadLevel.cpp`), d'Héichtekaart
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  de Land-Ray-Tracer (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) an d'Waasser-Héichtekaart
  (`fftWater/fftWater.cpp`).
- `rigen.py`: déi gesat Objeten (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: déi generéiert Objeten (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: Render-Instanzen (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) an dem
  Index-Codec vum meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: d'Faarf vum Buedem (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: Ressourcepäck (`gameRes/grpData.h`) a Kollisiounsressourcen
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  där hir Dräiecker als Quad-BVH gespäichert sinn (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) liest déiselwecht Archiven; et ass net néideg a gëtt net benotzt.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
