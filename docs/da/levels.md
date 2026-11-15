---
title: Baner
nav_order: 9
lang: "da"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Baner (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` laver baner fra din egen War Thunder-installation om til `.glb`-baner
til vieweren, i samme koordinatsystem som replayenes tabeller.

## Trin for trin {#step-by-step}

1. List banerne i din installation: `heat3d-wt-level list`. Den skriver én linje pr. bane:
   dens navn, dens terræn og dens kort, og så antallet. For eksempel (en opdigtet bane):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Udpak én, flere (jokertegn tilladt) eller alle:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Indlæs `levels/<level>/<level>.glb` i viewerens panel Baggrund / bane, under kampene på det kort.

Banerne, du skriver, bliver på din maskine: publicér dem aldrig (se
[Vilkår og licens](terms.md)).

## Valgmuligheder {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Kommando / valg | Gør |
|---|---|
| `list [--game FOLDER]` | hver bane i installationen |
| `extract <levels...>` / `--all` | de angivne baner (som `list` skriver dem; jokertegn tilladt), eller alle |
| `-o`, `--out` | outputmappe; hver bane lægges i `<out>/<level>/` |
| `--game FOLDER` | War Thunder-mappen (standard: fundet via Steam eller launcheren; også `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | jordens samplingstæthed, jordfarve og objektbudget over stridsvognskortet (standard `medium`) |
| `--max-object-triangles N` | objektbudgettet (standard: detaljeniveauets) |
| `--max-grid N` | heightmap-samples pr. side, pr. del (standard 1024) |
| `--no-objects` | udelad bygninger, træer og andre placerede objekter |
| `--no-generated` | udelad de objekter, landklasserne genererer (skove, byer) |
| `--no-terrain-colour` | tegn jorden med det taktiske kort, ikke landklasserne |
| `--no-texture` | lad jorden være uden tekstur |
| `--skip-existing` | spring baner over, hvis deres `.glb` findes |

## Hvad der skrives {#what-is-written}

Hver bane bliver til `<out>/<level>/<level>.glb`, `<level>.json` (hvad der blev læst,
vandstanden, kortrektanglerne, antal trekanter, tider) og banens taktiske kort som
`<level>_map.png` (luftkortet) og `<level>_tankmap.png`; jordkort får også
`<level>_terrain.png`, jordens egne farver over stridsvognskortet. glb'en skrives til
`<level>.glb.part` og omdøbes, når den er færdig; mens en bane skrives, holdes
`<out>/<level>/.<level>.lock`, så to udtræk aldrig skriver den samme bane (den anden
skriver `busy <level>`). Installationen findes via Steam eller launcherens
standardmapper; `--game <folder>` eller `HEAT3D_WT_GAME` angiver den ellers.

| Del | Hvad det er |
|---|---|
| `ground:<level>` | terrænets heightmap (`HM2`) som et gitter; på jordkort midten af stridsvognskortet (halvdelen af dets bredde) med trinet fra `--detail`, farvet med landklasserne, jorddekaler og veje (`<level>_terrain.png`; det taktiske kort, hvor det ikke kan laves); på kort uden stridsvognskort (luftkort) hele heightmap'et i ét trin (2048 samples pr. side ved `high`, ellers 1024), farvet med landklasserne over luftkortets område (4096 pixels pr. side, ca. 32 m pr. pixel over 131 km; det taktiske kort, hvor det ikke kan laves); på baner uden heightmap landmeshet |
| `ground:<level> tank map` | resten af stridsvognskortet, ét trin grovere |
| `ground:<level> heightmap surroundings` | resten af heightmap'et, endnu grovere |
| `ground:<level> land mesh` | landmeshets kollisionstrekanter, hvor heightmap'et ikke rækker (omgivelserne af et stridsvognskort, ud til snesevis af kilometer); på baner uden heightmap er det jorden, farvet som ovenfor |
| `ground:<level> outside the map` | jord, som billedet ikke dækker, uden tekstur |
| `water:<level>` | ét fladt rektangel ved banens `water_level` over alt terrænet: spillet tegner vand som ét plan, og lavt land under det er hav, sø eller flodbund |
| `water:<level> rivers` | på baner med et vand-heightmap (`WHM`), den skrånende vandflade over de celler, den dækker |
| `structure:<level> buildings` | hvert placerede objekt, der ikke er en plante: huse, ruiner, mure, hegn, broer, skinner, sten, rekvisitter. De faste (`RIGz`) og, over stridsvognskortet, dem landklasserne genererer (byblokke, sten). Hver tegnes ud fra sin render-mesh (mure, tage, vinduesåbninger, bjælker) i det LOD, trekantbudgettet tillader, farvet pr. materiale efter gennemsnittet af dets diffuse tekstur |
| `structure:<level> trees` | træer og buske, faste og genererede (skove, hække): deres render-mesh, hvor budgettet tillader det, ellers en stamme og en krone (en kegle for nåletræer) i træets eget løvfarve, i træets rigtige størrelse |

Objekter uden render-mesh falder tilbage til deres kollisionsform; træer uden en
falder tilbage til kronen. Hjørnefarverne (`COLOR_0`) holder sRGB-kodede værdier,
som 3DHeat-vieweren læser dem.

**Koordinater** er spillets meter med z spejlet: glb (x, y, z) = spil (x, y, -z). Spillets
verden er venstrehåndet (x øst, y op, z nord); glTF er højrehåndet. `heat3d-wt-replay`
beholder spillets z og fortæller vieweren at spejle det, så et replay og banen for dets
kort ligger oven på hinanden uden et placeringstrin. JSON'en giver hvert taktisk kort's
rektangel i spillets meter og dets hjørner i glb'ens rum, til at indlæse PNG'en som et
kortbillede.

**Detaljeniveau.** `--detail low|medium|high` (standard medium) sætter, over
stridsvognskortet:

| | midten af stridsvognskortet | resten af stridsvognskortet | jordfarve | objektbudget | flest trekanter pr. objekt | bevarede genererede planter |
|---|---|---|---|---|---|---|
| low | hver 4. sample | hver 8. | 4 m pr. pixel | 1,2 M | 1.500 | træer 35 %, buske 20 % |
| medium | hver 2. | hver 4. | 2 m | 3,5 M | 4.000 | træer 70 %, buske 50 % |
| high | hver sample (2 m på de fleste jordkort) | hver 2. | 1 m (højst 4096 pixels pr. side) | 4,5 M | 12.000 | alle |

De to ringe af stridsvognskortet holdes til 0,3 M (low), 1 M (medium) og 3,7 M (high)
trekanter: på kort, hvis heightmap er finere end 2 m, fordobles trinene (den yderste ring
først), til de passer, så de også ender på ca. 2 m.

Et jordkort i `high` ender på ca. 8 millioner trekanter (3,5 M jord, 4,5 M objekter) og
250 MB; i `medium` på ca. 4,5 M. Objekternes LOD'er er dem, spillet selv ville tegne fra
én synsafstand: den korteste, hvis samlede størrelse passer i budgettet. Små rekvisitter
falder først til grove LOD'er, og store bygninger sidst, efter de afstande deres skabere
gav hvert LOD (JSON'ens `lodDistance`); det, trinet sparer ud over budgettet, går tilbage
til de største objekter. Grov jordfarve (luftkort) gennemsnitter først hver landklasses
flisede teksturer ned til pixelstørrelsen, så flisene ikke aliaser til et moiré.
Hvis selv de groveste LOD'er ikke passer, bliver de træer, der sparer mest, til kroner,
og derefter udelades de mindste typer (`leftOut`); intet objekt tegnes som en kasse
(en kollisionsform, hvis der er en, er objektets egen).
Genererede objekter tyndes deterministisk efter art (`density`), de samme hver gang.
`--max-object-triangles` overskriver budgettet, `--max-grid` (standard 1024) begrænser
heightmap'ets grovere dele, `--no-objects` udelader objekterne, `--no-generated` de
genererede, `--no-terrain-colour` tekstur jorden med det taktiske kort, `--no-texture`
lader den være uden tekstur.

JSON'ens `parts.objects` lister instanser (faste og genererede, efter art og landklasse),
hvor mange der blev tegnet i hvilket LOD (`drawnAs`), trekanterne, LOD-afstanden og
sekunderne; `parts.heightmap.rings` hver jordrings trin og trekanter; `parts.terrainColour`
landklasserne og deres farver, veje og jorddekaler; `trianglesTotal`, `glbBytes` og
`secondsBy` summerne.

## Hvad der læses, og hvor godt {#what-is-read-and-how-well}

| Del | Status |
|---|---|
| Banebinær (`levels/<level>.bin`, `DBLD` 3x64): blokkeskema | hver bane kontrolleret |
| Heightmap (`HM2`, versioner 0-2; version 2 er 8-bit-værdier i blokke, Oodle- eller zstd-bidder) | hver bane, hvis heightmap er version 2 med Oodle-bidder; kontrolleret med øjnene mod deres taktiske kort (floder, dale, kyster og byer flugter) |
| Landmesh-kollision (`lmap`, dens `LTdump`-landstrålesporer) | læst, hvor en bane har en (Oodle-pakket). Det er spillets kollisionsflade, ikke det tegnede mesh, så den er grovere, hvor landet er fladt |
| Jordfarve (`lmap`-landklasser og vægtkort, `LMp2`-fysikkort, `hspl`-splines) | landklassernes farvekort og detaljeteksturer (deres gennemsnitsfarver) vægtet med vægtkortet, 1 m biomeindekset for indekserede landklasser, vej- og jorddekalformerne på fysikkortet i farven af deres splines eller materiales tekstur, klipper på stejle skråninger. Kontrolleret mod stridsvognskortene: veje, byer, søer, skovbælter og klippeudspring flugter. Farveformlen i War Thunders egen terrainshader er ikke i den offentlige kildekode; motorens offentliggjorte (daNetGame) bruges, og den bliver mere mættet end det taktiske kort |
| Vandniveau | `water_level` fra banens BLK i `aces.vromfs.bin` (0, hvor den ikke har en) |
| Vand-heightmap (`WHM`: et gitter af flade celler og 130x130-sider med 16-bit-højder) | læst, hvor en bane har et; dens floder skråner med terrænet |
| Taktiske kort | fra `content/base/res/locations_maps.dxp.bin`, placeret ud fra BLK'ens `mapCoord0/1` og `tankMapCoord0/1`; billedets top er nord |
| Placerede objekter (`RIGz`: render-instansgeneratorens faste instanser) | hver instans, som en 3x4-matrix af 16-bit-værdier eller, på nogle baner, 32-bit-værdier (cellens bytetal afgør det); hver byte i hver celle regnskabsført på de kontrollerede baner |
| Genererede objekter (`RIGz`-landklasse-masker og `LandClass`-ressourcer) | spillets generator, porteret: de samme steder prøvet i samme rækkefølge med de samme tilfældige tal, landklasse- og udelukkelsesmaskerne, objektet valgt på hvert sted, dets rotation, skala og højdeforskydning; flisede (byblokke) og plantede (skove, buske, marker) entiteter. Genereret kun over stridsvognskortet. Tilnærmet: jordhøjden og normalen (fra heightmap'et; spillet sporer en stråle), udelukkelseskasserne spillet registrerer under kørsel, og træers giring (spillet fanger det til impostorens rotationspalet). |
| Render-meshes (`RendInst`-ressourcer i `content/*/res/*.grp`, materialer i `riDesc.bin`) | hver LOD's hjørner og trekanter (flydende positioner; 16- eller 32-bit-indekser, almindelige eller meshoptimizer-pakkede), hvert elements materiale. Decal- og impostor-billboard-elementer udelades; de gennemsigtige (glas) beholdes |
| Objektfarver | pr. materiale, gennemsnittet af dets diffuse teksturs lille mip (alfa-vægtet for blade), fra installationens teksturpakker: t0 for de fleste shadere, den første detaljediffuse, hvor t0 er et overlay eller en maske. Én farve pr. materiale: ingen tekstur på objekterne |
| Kollisionsformer (`<object>_collision`) | kollisionsressourcer af strømversion 3, brugt, hvor et objekt ikke har en render-mesh. Kun det spillets stråler rammer (`TRACEABLE`-noder) tegnes, og kasser, kugler og kapsler kun, når ressourcen ingen mesh har: resten er grove fysikstand-ins, der ville vise sig som kuber omkring objektet |
| Navigationsmesh (`Lnav`), det tegnede landmesh, græs, `spgz`, `stbl`, `d2co` | ikke læst |

Baner er komprimeret med Oodle, som er proprietær. Spillet leverer en kopi,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (en almindelig x64-build), og den er
det, der indlæses; `HEAT3D_OODLE=<dll or folder>` peger på en anden. Intet af Oodle er
medtaget her.

## Formater, og hvor de er dokumenteret {#formats-and-where-they-are-documented}

Gaijin har offentliggjort Dagor Engines kildekode under BSD 3-Clause-licensen
(github.com/GaijinEntertainment/DagorEngine). Læserne her er skrevet ud fra den; intet
spilkode er dekompileret. Hvert modul nævner de kildefiler, det følger:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, en zstd-krop, hvis første og sidste
  16 bytes er XOR'et med en fast nøgle, en navnetabel og en offsettabel:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  og binær BLK (former 1-5, med arkivets fælles navnekort `\xff?nm` og zstd-ordbog:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: teksturpakker `DxP2` (`lib3d/texPackMgr2.cpp`) og DDSx-headere
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 afkodes af Pillow.
- `dagorlevel.py`: banebinæren (`scene/loadLevel.cpp`), heightmap'et
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  landstråle-sporeren (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) og vand-heightmap'et
  (`fftWater/fftWater.cpp`).
- `rigen.py`: de placerede objekter (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: de genererede objekter (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: render-instanser (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) og meshoptimizers
  indeks-kodek (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: jordens farve (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: ressourcepakker (`gameRes/grpData.h`) og kollisionsressourcer
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  hvis trekanter er gemt som et quad-BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) læser de samme arkiver; den er hverken nødvendig eller brugt.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
