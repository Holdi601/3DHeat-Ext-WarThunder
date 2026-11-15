---
title: "Livelli"
nav_order: 9
lang: mt
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Livelli (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` ibiddel il-livelli tal-installazzjoni tiegħek stess ta' War Thunder f'livelli
`.glb` għall-viewer, fl-istess qafas bħat-tabelli tar-ripetizzjonijiet.

## Pass b'pass {#step-by-step}

1. Elenka l-livelli tal-installazzjoni tiegħek: `heat3d-wt-level list`. Jistampa linja waħda
   għal kull livell: l-isem tiegħu, it-terren tiegħu u l-mapep tiegħu, imbagħad l-għadd. Pereżempju
   (livell maħluq):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Estratta wieħed, bosta (wildcards permessi) jew kollha:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Ikkarga `levels/<level>/<level>.glb` fil-pannell Sfond / livell tal-viewer, taħt il-battaljiet ta'
   dik il-mappa.

Il-livelli li tikteb jibqgħu fuq il-magna tiegħek: qatt ma tippubblikahom (ara
[Termini u liċenzja](terms.md)).

## Għażliet {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Kmand / għażla | X'jagħmel |
|---|---|
| `list [--game FOLDER]` | kull livell fl-installazzjoni |
| `extract <levels...>` / `--all` | il-livelli msemmija (kif jistampahom `list`; wildcards permessi), jew kull livell |
| `-o`, `--out` | folder tal-ħruġ; kull livell imur f'`<out>/<level>/` |
| `--game FOLDER` | il-folder ta' War Thunder (default: misjub permezz ta' Steam jew tal-launcher; ukoll `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | kampjunar tal-art, kulur tal-art u baġit tal-oġġetti fuq il-mappa tat-tankijiet (default `medium`) |
| `--max-object-triangles N` | il-baġit tal-oġġetti (default: dak tad-detail) |
| `--max-grid N` | kampjuni tal-heightmap għal kull naħa, għal kull parti (default 1024) |
| `--no-objects` | iħalli barra bini, siġar u oġġetti oħra mqiegħda |
| `--no-generated` | iħalli barra l-oġġetti li l-land classes jiġġeneraw (foresti, bliet) |
| `--no-terrain-colour` | jittextura l-art bil-mappa tattika, mhux bil-land classes |
| `--no-texture` | iħalli l-art mingħajr texture |
| `--skip-existing` | iħalli livelli li l-`.glb` tagħhom jeżisti |

## X'jinkiteb {#what-is-written}

Kull livell isir `<out>/<level>/<level>.glb`, `<level>.json` (dak li ntqara, il-livell tal-ilma,
ir-rettangoli tal-mapep, għadd ta' trijangoli, ħinijiet) u l-mapep tattiċi tal-livell bħala
`<level>_map.png` (il-mappa tal-ajru) u `<level>_tankmap.png`; il-mapep tal-art jingħataw ukoll
`<level>_terrain.png`, il-kuluri proprji tal-art fuq il-mappa tat-tankijiet. Il-glb jinkiteb
f'`<level>.glb.part` u jiġi msemmi mill-ġdid meta jitlesta; waqt li livell jinkiteb,
`<out>/<level>/.<level>.lock` jinżamm, biex żewġ estrazzjonijiet ma jiktbux qatt l-istess livell
(it-tieni jistampa `busy <level>`). L-installazzjoni tinstab permezz ta' Steam jew tal-folders
default tal-launcher; `--game <folder>` jew `HEAT3D_WT_GAME` jgħidu fejn inkella.

| Parti | X'inhi |
|---|---|
| `ground:<level>` | il-heightmap tat-terren (`HM2`) bħala grid; fuq mapep tal-art nofs il-mappa tat-tankijiet (nofs il-wisa' tagħha) fil-pass tad-`--detail`, ikkulurit bil-land classes, decals tal-art u toroq (`<level>_terrain.png`; il-mappa tattika fejn dan ma jistax isir); fuq mapep mingħajr mappa tat-tankijiet (mapep tal-ajru), il-heightmap kollha b'pass wieħed (2048 kampjun għal kull naħa f'`high`, 1024 inkella), ikkulurita bil-land classes fuq iż-żona tal-mappa tal-ajru (4096 pixel għal kull naħa, madwar 32 m għal kull pixel fuq 131 km; il-mappa tattika fejn dan ma jistax isir); fuq livelli mingħajr heightmap, il-land mesh |
| `ground:<level> tank map` | il-bqija tal-mappa tat-tankijiet, pass wieħed aktar goff |
| `ground:<level> heightmap surroundings` | il-bqija tal-heightmap, saħansitra aktar goff |
| `ground:<level> land mesh` | it-trijangoli tal-kolliżjoni tal-land mesh fejn il-heightmap ma tasalx (l-inħawi ta' mappa tat-tankijiet, sa għexieren ta' kilometri); fuq livelli mingħajr heightmap hija l-art, ikkulurita kif hawn fuq |
| `ground:<level> outside the map` | art li l-immaġni ma tkoprix, mingħajr texture |
| `water:<level>` | rettangolu ċatt wieħed fil-`water_level` tal-livell fuq it-terren kollu: il-logħba tiżżebgħa l-ilma bħala pjan wieħed, u art baxxa taħtu hija qiegħ ta' baħar, lag jew xmara |
| `water:<level> rivers` | fuq livelli b'heightmap tal-ilma (`WHM`), il-wiċċ tal-ilma inklinat fuq iċ-ċelloli li jkopri |
| `structure:<level> buildings` | kull oġġett imqiegħed li mhuwiex pjanta: djar, fdalijiet, ħitan, ċnut, pontijiet, linji tal-ferrovija, blat, props. Dawk fissi (`RIGz`) u, fuq il-mappa tat-tankijiet, dawk li l-land classes jiġġeneraw (blokok ta' bliet, ġebel). Kull wieħed jiġi miżbugħ bil-mesh tal-render tiegħu (ħitan, soqfa, miftuħ tat-twieqi, travi), bil-LOD li jippermetti l-baġit tat-trijangoli, ikkulurit għal kull materjal bil-medja tat-texture diffuża tiegħu |
| `structure:<level> trees` | siġar u arbuxxelli, fissi u ġġenerati (foresti, ċnut ħajjin): il-mesh tal-render tagħhom fejn jippermetti l-baġit, inkella zokk u kuruna (kon għall-koniferi) bil-kulur tal-weraq tas-siġra stess, fuq id-daqs veru tas-siġra |

Oġġetti mingħajr mesh tal-render jirritornaw għall-forma tal-kolliżjoni tagħhom; siġar mingħajr waħda
għall-kuruna. Il-kuluri tal-vertiċi (`COLOR_0`) iżommu valuri kkodifikati sRGB, li hija kif jaqrahom
id-3DHeat viewer.

**Koordinati** huma l-metri tal-logħba b'z mirri: glb (x, y, z) = logħba
(x, y, -z). Id-dinja tal-logħba hija xellugija (x lvant, y 'il fuq, z tramuntana); glTF hija
leminija. `heat3d-wt-replay` iżomm iz-z tal-logħba u jgħid lill-viewer biex jirriflettiha, biex ripetizzjoni u l-livell tal-mappa tagħha jinżlu waħda fuq l-oħra mingħajr
pass ta' tqegħid. Il-JSON jagħti r-rettangolu ta' kull mappa tattika f'metri tal-logħba
u l-kantunieri tagħha fl-ispazju tal-glb, biex tinġarr il-PNG bħala immaġni tal-mappa.

**Detail.** `--detail low|medium|high` (default medium) jistabbilixxi, fuq il-mappa tat-tankijiet:

| | nofs il-mappa tat-tankijiet | il-bqija tal-mappa tat-tankijiet | kulur tal-art | baġit tal-oġġetti | l-aktar trijangoli għal kull oġġett | pjanti ġġenerati miżmuma |
|---|---|---|---|---|---|---|
| low | kull 4 kampjuni | kull 8 | 4 m għal kull pixel | 1.2 M | 1,500 | siġar 35 %, arbuxxelli 20 % |
| medium | kull 2 | kull 4 | 2 m | 3.5 M | 4,000 | siġar 70 %, arbuxxelli 50 % |
| high | kull kampjun (2 m fuq il-biċċa l-kbira tal-mapep tal-art) | kull 2 | 1 m (l-iktar 4096 pixel għal kull naħa) | 4.5 M | 12,000 | kollha |

Iż-żewġ ċrieki tal-mappa tat-tankijiet huma miżmuma f'0.3 M (low), 1 M (medium) u 3.7 M (high)
trijangoli: fuq il-mapep li l-heightmap tagħhom hija aktar fina minn 2 m, il-passi jirdoppjaw
(iċ-ċirku ta' barra l-ewwel) sakemm jidħlu, għalhekk dawk joħorġu madwar 2 m ukoll.

Mappa tal-art f'`high` toħroġ b'madwar 8 miljun trijangolu (3.5 M ta' art, 4.5 M ta' oġġetti)
u 250 MB; f'`medium` b'madwar 4.5 M. Il-LODs tal-oġġetti huma dawk li l-logħba nnifisha tiżbogħ minn distanza waħda
ta' ħarsa, l-iqsar li t-total tagħha jidħol fil-baġit: props żgħar jinżlu għal LODs goffa l-ewwel u bini kbir
l-aħħar, skont il-firxiet li taw dawk li għamluhom lil kull LOD (il-`lodDistance` tal-JSON);
dak li dan il-pass jiffranka lil hinn mill-baġit jerġa' jmur lill-akbar oġġetti. Il-kulur goff tal-art (mapep tal-ajru) jagħmel il-medja tat-textures
tiled ta' kull land class sad-daqs tal-pixel l-ewwel, biex it-tiles ma jagħmlux aliasing f'moire. Jekk anke l-LODs l-aktar goffi ma jidħlux, is-siġar li jiffrankaw l-aktar
isiru kuruni, u mbagħad it-tipi l-iżgħar jitħallew barra (`leftOut`); ebda oġġett ma jiġi
miżbugħ bħala kaxxa (forma tal-kolliżjoni, jekk hemm, hija tal-oġġett stess).
L-oġġetti ġġenerati jitnaqqsu deterministikament skont it-tip (`density`), l-istess
wieħed f'kull tħaddim. `--max-object-triangles` jissostitwixxi l-baġit,
`--max-grid` (default 1024) jillimita l-partijiet aktar goffa tal-heightmap, `--no-objects`
iħalli barra l-oġġetti, `--no-generated` dawk iġġenerati, `--no-terrain-colour`
jittextura l-art bil-mappa tattika, `--no-texture` iħalliha mingħajr texture.

Il-`parts.objects` tal-JSON jelenka l-istanzi (fissi u ġġenerati, skont it-tip u
l-land class), kemm ġew miżbugħin f'liema LOD (`drawnAs`), it-trijangoli, id-distanza tal-LOD u s-sekondi;
`parts.heightmap.rings` il-pass u t-trijangoli ta' kull ċirku tal-art; `parts.terrainColour` il-land classes u l-kuluri tagħhom, toroq
u decals tal-art; `trianglesTotal`, `glbBytes` u `secondsBy` it-totali.

## X'jinqara, u kemm tajjeb {#what-is-read-and-how-well}

| Parti | Stat |
|---|---|
| Binarju tal-livell (`levels/<level>.bin`, `DBLD` 3x64): tabella tal-blokok | kull livell ikkontrollat |
| Heightmap (`HM2`, verżjonijiet 0-2; il-verżjoni 2 hija valuri ta' 8 bit f'blokok, chunks ta' Oodle jew zstd) | kull livell li l-heightmap tiegħu hija verżjoni 2 b'chunks ta' Oodle; ikkontrollata bl-għajn kontra l-mapep tattiċi tagħhom (xmajjar, widien, kosti u bliet jaqblu) |
| Kolliżjoni tal-land mesh (`lmap`, il-`LTdump` land ray tracer tiegħu) | moqrija fejn livell għandu waħda (ippakkjata b'Oodle). Hija l-wiċċ tal-kolliżjoni tal-logħba, mhux il-mesh miżbugħ, għalhekk hija aktar goffa fejn l-art hija ċatta |
| Kulur tal-art (land classes u weight map ta' `lmap`, physics map `LMp2`, splines `hspl`) | il-colour maps tal-land classes u t-textures tad-dettall (il-kuluri medji tagħhom) imwiżnin bil-weight map, l-indiċi tal-bijoma ta' 1 m tal-land classes indiċjati, il-forom tat-toroq u tad-decals tal-art tal-physics map bil-kulur tat-texture tal-spline jew tal-materjal tagħhom, irdumijiet fuq pendji ċatti. Ikkontrollat kontra l-mapep tat-tankijiet: toroq, bliet, lagi, ċinturi tal-foresti u blat jaqblu. Il-formula tal-kulur tas-shader tat-terren proprju ta' War Thunder mhix fis-sors pubbliku; tintuża dik ippubblikata tal-magna (daNetGame), li toħroġ aktar saturata mill-mappa tattika |
| Livell tal-ilma | `water_level` mill-BLK tal-livell f'`aces.vromfs.bin` (0 fejn m'għandu ebda) |
| Heightmap tal-ilma (`WHM`: grid ta' ċelloli ċatti u paġni ta' 130x130 ta' għoli ta' 16-il bit) | moqrija fejn livell għandu waħda; ix-xmajjar tagħha jinklinaw mal-art |
| Mapep tattiċi | minn `content/base/res/locations_maps.dxp.bin`, imqiegħda mill-`mapCoord0/1` u `tankMapCoord0/1` tal-BLK; il-quċċata tal-immaġni hija t-tramuntana |
| Oġġetti mqiegħda (`RIGz`: l-istanzi fissi tal-ġeneratur tal-render-instances) | kull istanza, bħala matriċi 3x4 ta' valuri ta' 16-il bit jew, fuq xi livelli, ta' 32-bit (l-għadd ta' bytes taċ-ċellola jiddeċiedi); kull byte ta' kull ċellola mqiegħed fil-kont fuq il-livelli ikkontrollati |
| Oġġetti ġġenerati (maskri tal-land-class `RIGz` u r-riżorsi `LandClass`) | il-ġeneratur tal-logħba, trasportat: l-istess spots ippruvati fl-istess ordni bl-istess numri każwali, il-maskri tal-land-class u tal-esklużjoni, l-oġġett magħżul f'kull spot, ir-rotazzjoni, l-iskala u l-offset tal-għoli tiegħu; entitajiet tiled (blokok ta' bliet) u mħawla (foresti, arbuxxelli, għelieqi). Iġġenerati biss fuq il-mappa tat-tankijiet. Approssimat: l-għoli tal-art u n-normal (mill-heightmap; il-logħba ssegwi raġġ), il-kaxxi tal-esklużjoni li l-logħba tirreġistra fil-ħin tat-tħaddim, u l-yaw tas-siġar (il-logħba tgħaqqadu mal-palett tar-rotazzjoni tal-impostor). |
| Mesh tar-render (riżorsi `RendInst` f'`content/*/res/*.grp`, materjali f'`riDesc.bin`) | il-vertiċi u t-trijangoli ta' kull LOD (pożizzjonijiet float; indiċi ta' 16 jew 32-bit, sempliċi jew ippakkjati b'meshoptimizer), il-materjal ta' kull element. L-elementi decal u impostor-billboard jitħallew barra; dawk trasparenti (ħġieġ) jinżammu |
| Kuluri tal-oġġetti | għal kull materjal, il-medja tal-mip żgħir tat-texture diffuża tiegħu (imwiżna bl-alpha għall-weraq), mill-pakketti tat-texture tal-installazzjoni: t0 għall-biċċa l-kbira tas-shaders, l-ewwel diffuża tad-dettall fejn t0 hija overlay jew maskra. Kulur wieħed għal kull materjal: ebda texture fuq l-oġġetti |
| Forom tal-kolliżjoni (`<object>_collision`) | riżorsi tal-kolliżjoni tal-verżjoni tal-fluss 3, użati fejn oġġett m'għandu ebda mesh tar-render. Jiġi miżbugħ biss dak li jolqtu r-raġġi tal-logħba (nodi `TRACEABLE`), u kaxxi, sferi u kapsuli biss meta r-riżorsa m'għandha ebda mesh: il-bqija huma sostituti goffi tal-fiżika li jidhru bħala kubi madwar l-oġġett |
| Navigation mesh (`Lnav`), il-land mesh miżbugħ, ħaxix, `spgz`, `stbl`, `d2co` | mhux moqri |

Il-livelli huma kkompressati b'Oodle, li huwa proprjetarju. Il-logħba tiġi b'kopja,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (bini x64 ordinarju), u dik hija li titgħabba;
`HEAT3D_OODLE=<dll or folder>` jindika oħra. Xejn minn Oodle mhu inkluż hawn.

## Formati, u fejn huma ddokumentati {#formats-and-where-they-are-documented}

Gaijin ippubblika s-sors tad-Dagor Engine taħt il-liċenzja BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Il-qarrejja hawn inkitbu minnu;
ebda kodiċi tal-logħba ma ġie dekompilat. Kull modulu jsemmi l-fajls tas-sors li jsegwi:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, korp zstd li l-ewwel u l-aħħar
  16-il byte tiegħu huma XORed b'ċavetta fissa, tabella tal-ismijiet u tabella tal-offsets:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  u BLK binarju (forom 1-5, bil-mappa tal-ismijiet maqsuma tal-arkivju `\xff?nm` u
  d-dizzjunarju zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: pakketti tat-texture `DxP2` (`lib3d/texPackMgr2.cpp`) u headers DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 jiġu deċifrati minn Pillow.
- `dagorlevel.py`: il-binarju tal-livell (`scene/loadLevel.cpp`), il-heightmap
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  il-land ray tracer (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) u l-heightmap tal-ilma
  (`fftWater/fftWater.cpp`).
- `rigen.py`: l-oġġetti mqiegħda (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: l-oġġetti ġġenerati (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: render instances (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) u l-index codec ta'
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: il-kulur tal-art (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: pakketti ta' riżorsi (`gameRes/grpData.h`) u riżorsi tal-kolliżjoni
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  li t-trijangoli tagħhom jinħażnu bħala quad BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) jaqra l-istess arkivji; mhux meħtieġ u mhux użat.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
