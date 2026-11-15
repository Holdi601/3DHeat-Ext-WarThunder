---
title: "Nivåer"
nav_order: 9
lang: no
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Nivåer (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` gjør nivåene i din egen War Thunder-installasjon om til `.glb`-nivåer for
visningsprogrammet, i samme ramme som replayenes tabeller.

## Steg for steg {#step-by-step}

1. List nivåene i installasjonen din: `heat3d-wt-level list`. Den skriver én linje per nivå: navnet,
   terrenget og kartene, deretter antallet. For eksempel (et oppdiktet nivå):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Pakk ut ett, flere (jokertegn er tillatt) eller alle:

   ```bash
   heat3d-wt-level extract <nivå> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <nivå> -o levels --detail high
   ```

3. Last `levels/<nivå>/<nivå>.glb` inn i visningsprogrammets nivåpanel, under slagene for det kartet.

Nivåene du skriver, blir på din maskin: publiser dem aldri (se
[Vilkår og lisens](terms.md)).

## Valg {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Kommando / valg | Gjør |
|---|---|
| `list [--game MAPPE]` | hvert nivå i installasjonen |
| `extract <nivåer...>` / `--all` | de nivåene som er navngitt (slik `list` skriver dem; jokertegn er tillatt), eller alle |
| `-o`, `--out` | utdatamappe; hvert nivå havner i `<ut>/<nivå>/` |
| `--game MAPPE` | War Thunder-mappen (standard: funnet gjennom Steam eller startprogrammet; også `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | bakkeoppløsning, bakkefarge og objektbudsjett over stridsvognkartet (standard `medium`) |
| `--max-object-triangles N` | objektbudsjettet (standard: detaljnivåets) |
| `--max-grid N` | høydekart-samples per side, per del (standard 1024) |
| `--no-objects` | utelat bygninger, trær og andre plasserte objekter |
| `--no-generated` | utelat objektene landklassene lager (skoger, byer) |
| `--no-terrain-colour` | tekstur bakken med det taktiske kartet, ikke landklassene |
| `--no-texture` | la bakken være uten tekstur |
| `--skip-existing` | la være nivåer der `.glb` finnes |

## Hva som skrives {#what-is-written}

Hvert nivå blir til `<ut>/<nivå>/<nivå>.glb`, `<nivå>.json` (hva som ble lest,
vannivået, kartrektanglene, antall trekanter, tidsbruk) og nivåets taktiske kart som
`<nivå>_map.png` (luftkartet) og `<nivå>_tankmap.png`; bakkekart får også
`<nivå>_terrain.png`, bakkens egne farger over stridsvognkartet. Glb-filen skrives til
`<nivå>.glb.part` og gis nytt navn når den er ferdig; mens et nivå skrives, holdes
`<ut>/<nivå>/.<nivå>.lock`, så to utpakkinger aldri skriver samme nivå (den andre skriver
`busy <nivå>`). Installasjonen finnes gjennom Steam eller startprogrammets standardmapper;
`--game <mappe>` eller `HEAT3D_WT_GAME` sier hvor den ligger ellers.

| Del | Hva det er |
|---|---|
| `ground:<nivå>` | terrengets høydekart (`HM2`) som et rutenett; på bakkekart midten av stridsvognkartet (halve bredden) i `--detail`-steget, fargelagt med landklassene, bakkepåføringer og veier (`<nivå>_terrain.png`; det taktiske kartet der det ikke kan lages); på kart uten stridsvognkart (luftkart), hele høydekartet i ett steg (2048 samples per side ved `high`, ellers 1024), fargelagt med landklassene over luftkartets område (4096 piksler per side, ca. 32 m per piksel over 131 km; det taktiske kartet der det ikke kan lages); på nivåer uten høydekart, landnettet |
| `ground:<nivå> tank map` | resten av stridsvognkartet, ett steg grovere |
| `ground:<nivå> heightmap surroundings` | resten av høydekartet, enda grovere |
| `ground:<nivå> land mesh` | landnettets kolliderings-trekanter der høydekartet ikke når (omgivelsene til et stridsvognkart, ut til titalls kilometer); på nivåer uten høydekart er det bakken, fargelagt som over |
| `ground:<nivå> outside the map` | bakke bildet ikke dekker, uten tekstur |
| `water:<nivå>` | ett flatt rektangel på nivåets `water_level` over alt terreng: spillet tegner vann som ett plan, og lav bakke under det er sjø, innsjø eller elveleie |
| `water:<nivå> rivers` | på nivåer med et vannhøydekart (`WHM`), vannflaten med helning over cellene den dekker |
| `structure:<nivå> buildings` | hvert plasserte objekt som ikke er en plante: hus, ruiner, murer, gjerder, broer, skinner, steiner, rekvisitter. De faste (`RIGz`) og, over stridsvognkartet, de landklassene lager (bybolker, steiner). Hvert tegnes med sitt rendermesh (vegger, tak, vindusåpninger, bjelker), i den LOD-en triangelbudsjettet tillater, fargelagt per materiale etter gjennomsnittet av dets diffuse tekstur |
| `structure:<nivå> trees` | trær og busker, faste og laget (skoger, hekker): deres rendermesh der budsjettet tillater, ellers en stamme og en krone (en kjegle for bartrær) i trærnes egen løvfarge, over trærnes virkelige størrelse |

Objekter uten rendermesh faller tilbake til sin kollisjonsform; trær uten en til kronen. Hjørnefarger
(`COLOR_0`) holder sRGB-kodede verdier, som er slik 3DHeat-visningsprogrammet leser dem.

**Koordinater** er spillets meter med z speilet: glb (x, y, z) = spill (x, y, -z). Spillets verden er
venstrehendt (x øst, y opp, z nord); glTF er høyrehendt. `heat3d-wt-replay` beholder spillets z og forteller
visningsprogrammet å speile den, så en replay og nivået til dens kart havner oppå hverandre uten noe plasseringssteg.
JSON-filen gir hvert taktiske karts rektangel i spillets meter og dets hjørner i glb-ens rom, for å laste PNG-en som kartbilde.

**Detaljnivå.** `--detail low|medium|high` (standard medium) setter, over stridsvognkartet:

| | midten av stridsvognkartet | resten av stridsvognkartet | bakkefarge | objektbudsjett | flest trekanter per objekt | genererte planter beholdt |
|---|---|---|---|---|---|---|
| low | hver 4. sample | hver 8. | 4 m per piksel | 1,2 M | 1 500 | trær 35 %, busker 20 % |
| medium | hver 2. | hver 4. | 2 m | 3,5 M | 4 000 | trær 70 %, busker 50 % |
| high | hver sample (2 m på de fleste bakkekart) | hver 2. | 1 m (høyst 4096 piksler per side) | 4,5 M | 12 000 | alle |

De to stridsvognkart-ringene holdes til 0,3 M (low), 1 M (medium) og 3,7 M (high)
trekanter: på kartene der høydekartet er finere enn 2 m, dobles stegene (den ytre ringen først)
til de passer, så de kommer ut på ca. 2 m likevel.

Et bakkekart ved `high` blir ca. 8 millioner trekanter (3,5 M bakke, 4,5 M objekter) og 250 MB; ved `medium` ca.
4,5 M. Objektenes LOD-er er de spillet selv ville tegnet fra én sikteavstand, den korteste hvis totalsum
passer i budsjettet: små rekvisitter faller til grove LOD-er først og store bygninger sist, etter rekkeviddene deres
lagere ga hver LOD (JSON-ens `lodDistance`); det som spares utover budsjettet, går tilbake til de største
objektene. Grov bakkefarge (luftkart) midler hver landklasses flislagte teksturer ned til pikselstørrelsen først, så
flisene ikke gir moaré. Hvis selv de groveste LOD-ene ikke passer, blir de trærne som sparer mest til kroner, og så
utelates de minste typene (`leftOut`); intet objekt tegnes som en boks (en kollisjonsform, om den finnes, er objektets egen).
Genererte objekter tynnes deterministisk etter type (`density`), de samme hver gang. `--max-object-triangles` overstyrer
budsjettet, `--max-grid` (standard 1024) begrenser høydekartets grovere deler, `--no-objects` utelater objektene,
`--no-generated` de genererte, `--no-terrain-colour` tekstur bakken med det taktiske kartet, `--no-texture` lar den stå uten tekstur.

JSON-ens `parts.objects` lister forekomster (faste og genererte, etter type og landklasse), hvor mange som ble tegnet i hvilken LOD
(`drawnAs`), trekantene, LOD-avstanden og sekundene; `parts.heightmap.rings` hver bakkering sitt steg og trekanter;
`parts.terrainColour` landklassene og deres farger, veier og bakkepåføringer; `trianglesTotal`, `glbBytes` og `secondsBy` totalene.

## Hva som leses, og hvor godt {#what-is-read-and-how-well}

| Del | Status |
|---|---|
| Nivåbinæren (`levels/<nivå>.bin`, `DBLD` 3x64): blokktabellen | hvert nivå kontrollert |
| Høydekart (`HM2`, versjon 0-2; versjon 2 er 8-bits verdier i blokker, Oodle- eller zstd-biter) | hvert nivå der høydekartet er versjon 2 med Oodle-biter; kontrollert med øyet mot deres taktiske kart (elver, daler, kyster og byer stemmer) |
| Landnettets kollisjon (`lmap`, dens `LTdump`-landstråle-sporer) | lest der et nivå har en (Oodle-pakket). Det er spillets kollisjonsflate, ikke det tegnede nettet, så den er grovere der landet er flatt |
| Bakkefarge (`lmap`-landklasser og vektkart, `LMp2`-fysikkart, `hspl`-splines) | landklassenes fargekart og detaljteksturer (deres gjennomsnittsfarger) vektet av vektkartet, biomindeksen på 1 m for indekserte landklasser, vei- og bakkepåføringsformene i fysikkartet i farven til deres splines eller materials tekstur, klipper på bratte skråninger. Kontrollert mot stridsvognkartene: veier, byer, innsjøer, skogbelter og bergknauser stemmer. Fargeformelen til War Thunders egen terrengshader er ikke i den offentlige kilden; motorens publiserte (daNetGame) brukes, som kommer ut mer mettet enn det taktiske kartet |
| Vannivå | `water_level` fra nivåets BLK i `aces.vromfs.bin` (0 der den ikke har noen) |
| Vannhøydekart (`WHM`: et rutenett av flate celler og 130x130 sider med 16-bits høyder) | lest der et nivå har ett; elvene har helning med terrenget |
| Taktiske kart | fra `content/base/res/locations_maps.dxp.bin`, plassert av BLK-ens `mapCoord0/1` og `tankMapCoord0/1`; bildets topp er nord |
| Plasserte objekter (`RIGz`: render-instansgeneratorens faste instanser) | hver instans, som en 3x4-matrise med 16-bits verdier eller, på noen nivåer, 32-bits (cellens byteantall avgjør); hver byte i hver celle regnskapsført på de kontrollerte nivåene |
| Genererte objekter (`RIGz` landklassemasker og `LandClass`-ressursene) | spillets generator, portert: de samme stedene prøvd i samme rekkefølge med samme tilfeldige tall, landklasse- og utelukkelsesmaskene, objektet valgt på hvert sted, dets rotasjon, skala og høydeforskyvning; flislagte (bybolker) og plantede (skoger, busker, åkrer) entiteter. Generert bare over stridsvognkartet. Tilnærmet: bakkehøyden og normalen (fra høydekartet; spillet sporer en stråle), utelukkelsesboksene spillet registrerer ved kjøretid, og trærnes gir (spillet fester den til impostorens rotasjonspalett) |
| Rendermesh (`RendInst`-ressurser i `content/*/res/*.grp`, materialer i `riDesc.bin`) | hver LODs hjørner og trekanter (flyttallsposisjoner; 16- eller 32-bits indekser, vanlige eller meshoptimizer-pakkede), hvert elements materiale. Dekal- og impostor-billboard-elementer utelates; de gjennomsiktige (glass) beholdes |
| Objektfarger | per materiale, gjennomsnittet av dets diffuse teksturs lille mip (alfavektet for løv), fra installasjonens teksturpakker: t0 for de fleste shadere, den første detaljdiffuse der t0 er et overlegg eller en maske. Én farge per materiale: ingen tekstur på objektene |
| Kollisjonsformer (`<objekt>_collision`) | kollisjonsressurser av strømversjon 3, brukt der et objekt ikke har et rendermesh. Bare det spillets stråler treffer (`TRACEABLE`-noder) tegnes, og bokser, kuler og kapsler bare når ressursen ikke har et mesh: resten er grove fysikk-stand-ins som ville vist seg som kuber rundt objektet |
| Navigasjonsnett (`Lnav`), det tegnede landnettet, gress, `spgz`, `stbl`, `d2co` | ikke lest |

Nivåene er komprimert med Oodle, som er proprietær. Spillet leveres med en kopi,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (et vanlig x64-bygg), og det er den som lastes;
`HEAT3D_OODLE=<dll eller mappe>` peker på en annen. Ingenting av Oodle er inkludert her.

## Formater, og hvor de er dokumentert {#formats-and-where-they-are-documented}

Gaijin publiserte Dagor Engines kilde under BSD 3-Clause-lisensen
(github.com/GaijinEntertainment/DagorEngine). Leserne her ble skrevet etter den;
ingen spillkode ble dekompilert. Hver modul nevner kildefilene den følger:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, en zstd-kropp der de første og siste 16 byte
  er XOR-et med en fast nøkkel, en navnetabell og en forskyvningstabell:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  og binær BLK (former 1-5, med arkivets delte navnekart `\xff?nm` og zstd-ordboken:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: teksturpakker `DxP2` (`lib3d/texPackMgr2.cpp`) og DDSx-headere
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekodes av Pillow.
- `dagorlevel.py`: nivåbinæren (`scene/loadLevel.cpp`), høydekartet
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  landstråle-sporeren (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) og vannhøydekartet
  (`fftWater/fftWater.cpp`).
- `rigen.py`: de plasserte objektene (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: de genererte objektene (`rendInst/rendInstGenLand.cpp`,
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
  indekskodek (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: bakkens farge (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: ressurspakker (`gameRes/grpData.h`) og kollisjonsressurser
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  hvis trekanter lagres som et firkant-BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) leser de samme arkivene; den trengs ikke og brukes ikke.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
