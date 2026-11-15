---
title: "Nivåer (heat3d-wt-level)"
nav_order: 9
lang: sv
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Nivåer (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` gör nivåerna i din egen War Thunder-installation till
`.glb`-nivåer för visaren, i samma koordinatsystem som tabellerna för repriserna.

## Steg för steg {#step-by-step}

1. Lista nivåerna i din installation: `heat3d-wt-level list`. Det skriver en
   rad per nivå: dess namn, terräng och kartor, sedan antalet. Till exempel
   (en påhittad nivå):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrahera en, flera (jokertecken tillåtna) eller alla:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Ladda `levels/<level>/<level>.glb` i visarens Nivå-panel, under stridena på
   den kartan.

Nivåerna du skriver stannar på din dator: publicera dem aldrig (se
[Villkor och licens](terms.md)).

## Alternativ {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Kommando / alternativ | Gör |
|---|---|
| `list [--game MAPP]` | varje nivå i installationen |
| `extract <levels...>` / `--all` | de nivåer som namnges (så som `list` skriver dem; jokertecken tillåtna), eller alla nivåer |
| `-o`, `--out` | utdatamapp; varje nivå hamnar i `<out>/<level>/` |
| `--game MAPP` | War Thunder-mappen (standard: hittas via Steam eller startprogrammet; även `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | markens provtagning, markfärg och objektbudget över stridsvagnskartan (standard `medium`) |
| `--max-object-triangles N` | objektbudgeten (standard: den från detaljnivån) |
| `--max-grid N` | höjdkartans provpunkter per sida, per del (standard 1024) |
| `--no-objects` | lämna bort byggnader, träd och andra placerade objekt |
| `--no-generated` | lämna bort objekten som markklasserna genererar (skogar, städer) |
| `--no-terrain-colour` | texturera marken med taktikkartan, inte med markklasserna |
| `--no-texture` | lämna marken otexturerad |
| `--skip-existing` | hoppa över nivåer vars `.glb` redan finns |

## Vad som skrivs {#what-is-written}

Varje nivå blir `<out>/<level>/<level>.glb`, `<level>.json` (vad som lästes,
vattennivån, kartrektanglarna, antal trianglar, tider) och nivåns taktikkartor
som `<level>_map.png` (flygkartan) och `<level>_tankmap.png`; markkartor får även
`<level>_terrain.png`, markens egna färger över stridsvagnskartan. Glb-filen skrivs
till `<level>.glb.part` och byter namn när den är klar; medan en nivå skrivs hålls
`<out>/<level>/.<level>.lock`, så två extraheringar aldrig skriver samma nivå (den
andra skriver `busy <level>`). Installationen hittas via Steam eller
startprogrammets standardmappar; `--game <mapp>` eller `HEAT3D_WT_GAME` anger
annars var den finns.

| Del | Vad det är |
|---|---|
| `ground:<level>` | terrängens höjdkarta (`HM2`) som ett rutnät; på markkartor mitten av stridsvagnskartan (halva dess bredd) med steget från `--detail`, färgad med markklasserna, markdekaler och vägar (`<level>_terrain.png`; taktikkartan där det inte går att göra); på kartor utan stridsvagnskarta (flygkartor) hela höjdkartan med ett steg (2048 provpunkter per sida vid `high`, annars 1024), färgad med markklasserna över flygkartans område (4096 bildpunkter per sida, ungefär 32 m per bildpunkt över 131 km; taktikkartan där det inte går att göra); på nivåer utan höjdkarta markens landnät |
| `ground:<level> tank map` | resten av stridsvagnskartan, ett steg grövre |
| `ground:<level> heightmap surroundings` | resten av höjdkartan, ännu grövre |
| `ground:<level> land mesh` | landnätets kollisionstrianglar där höjdkartan inte når (omgivningen av en stridsvagnskarta, ut till tiotals kilometer); på nivåer utan höjdkarta är det marken, färgad som ovan |
| `ground:<level> outside the map` | mark som bilden inte täcker, otexturerad |
| `water:<level>` | en platt rektangel på nivåns `water_level` över all terräng: spelet ritar vatten som ett plan, och låg mark under det är hav, sjö eller flodbotten |
| `water:<level> rivers` | på nivåer med en vattenhöjdkarta (`WHM`) den sluttande vattenytan över de celler den täcker |
| `structure:<level> buildings` | varje placerat objekt som inte är en växt: hus, ruiner, murar, staket, broar, räls, stenar, rekvisita. De fasta (`RIGz`) och, över stridsvagnskartan, de som markklasserna genererar (stadskvarter, stenar). Varje ritas med sin renderingsmesh (väggar, tak, fönsteröppningar, balkar), i den LOD som triangelbudgeten tillåter, färgad per material efter medelvärdet av dess diffusa textur |
| `structure:<level> trees` | träd och buskar, fasta och genererade (skogar, häckar): deras renderingsmesh där budgeten tillåter, annars en stam och en krona (en kon för barrträd) i trädets egen lövfärg, i trädets verkliga storlek |

Objekt utan renderingsmesh faller tillbaka på sin kollisionsform; träd utan en
på kronan. Vertexfärger (`COLOR_0`) håller sRGB-kodade värden, vilket är
så 3DHeat-visaren läser dem.

**Koordinater** är spelets meter med z speglad: glb (x, y, z) = spel (x, y, -z).
Spelets värld är vänsterhänt (x öster, y upp, z norr); glTF är högerhänt.
`heat3d-wt-replay` behåller spelets z och säger åt visaren att spegla den, så en
repris och nivån för dess karta hamnar ovanpå varandra utan något placeringssteg.
JSON-filen ger varje taktikkartas rektangel i spelmeter och dess hörn i glb:ens
rum, för att läsa in PNG-filen som kartbild.

**Detaljnivå.** `--detail low|medium|high` (standard medium) sätter, över
stridsvagnskartan:

| | mitten av stridsvagnskartan | resten av stridsvagnskartan | markfärg | objektbudget | flest trianglar per objekt | kvarvarande genererade växter |
|---|---|---|---|---|---|---|
| low | var 4:e provpunkt | var 8:e | 4 m per bildpunkt | 1,2 M | 1 500 | träd 35 %, buskar 20 % |
| medium | var 2:a | var 4:e | 2 m | 3,5 M | 4 000 | träd 70 %, buskar 50 % |
| high | varje provpunkt (2 m på de flesta markkartor) | var 2:a | 1 m (högst 4096 bildpunkter per sida) | 4,5 M | 12 000 | alla |

De två ringarna över stridsvagnskartan hålls till 0,3 M (low), 1 M (medium) och
3,7 M (high) trianglar: på kartor vars höjdkarta är finare än 2 m dubbleras
stegen (den yttre ringen först) tills de passar, så de hamnar också på ungefär 2 m.

En markkarta på `high` blir ungefär 8 miljoner trianglar (3,5 M mark,
4,5 M objekt) och 250 MB; på `medium` ungefär 4,5 M. Objektens LOD:er är de
spelet självt skulle rita från ett enda betraktningsavstånd, den kortaste vars
summa ryms i budgeten: små rekvisita faller först till grova LOD:er och stora
byggnader sist, efter de avstånd deras skapare angav för varje LOD (JSON:ens
`lodDistance`); det som det steget sparar utöver budgeten går tillbaka till de
största objekten. Grov markfärg (flygkartor) jämnar först ut varje markklass
upprepade texturer till bildpunktens storlek, så kakelmönstren inte ger moiré.
Om inte ens de grövsta LOD:erna ryms blir de träd som sparar mest till kronor,
och sedan lämnas de minsta typerna bort (`leftOut`); inget objekt ritas som en
låda (en kollisionsform, om en finns, är objektets egen).
Genererade objekt gallras deterministiskt per slag (`density`), samma
varje körning. `--max-object-triangles` åsidosätter budgeten, `--max-grid` (standard
1024) begränsar höjdkartans grövre delar, `--no-objects` lämnar bort objekten,
`--no-generated` de genererade, `--no-terrain-colour` texturerar marken med
taktikkartan, `--no-texture` lämnar den otexturerad.

JSON:ens `parts.objects` listar instanserna (fasta och genererade, per slag och
markklass), hur många som ritades i vilken LOD (`drawnAs`), trianglarna, LOD-avståndet
och sekunderna; `parts.heightmap.rings` varje markrings steg och trianglar;
`parts.terrainColour` markklasserna och deras färger, vägar och markdekaler;
`trianglesTotal`, `glbBytes` och `secondsBy` summorna.

## Vad som läses, och hur väl {#what-is-read-and-how-well}

| Del | Status |
|---|---|
| Nivåbinären (`levels/<level>.bin`, `DBLD` 3x64): blocktabellen | varje nivå kontrollerad |
| Höjdkarta (`HM2`, versionerna 0-2; version 2 är 8-bitsvärden i block, Oodle- eller zstd-bitar) | varje nivå vars höjdkarta är version 2 med Oodle-bitar; kontrollerad för ögat mot deras taktikkartor (floder, dalar, kuster och städer stämmer) |
| Landnätets kollision (`lmap`, dess `LTdump`-markstrålspårare) | läst där en nivå har ett (Oodle-packat). Det är spelets kollisionsyta, inte den renderade mesh:en, så den är grövre där marken är platt |
| Markfärg (`lmap` markklasser och viktkarta, `LMp2`-fysikkartan, `hspl`-splines) | markklassernas färgkartor och detaljtexturer (deras medelfärger) viktade med viktkartan, 1 m:s biotopindex för indexerade markklasser, vägarnas och markdekalernas former i fysikkartan i färgen av deras splines eller materials textur, klippor i branta sluttningar. Kontrollerad mot stridsvagnskartorna: vägar, städer, sjöar, skogsbälten och bergsklippor stämmer. Färgformeln i War Thunders egen terrängshader finns inte i den publika källkoden; den publicerade formeln från motorn (daNetGame) används, och den blir mer mättad än taktikkartan |
| Vattenhöjd | `water_level` ur nivåns BLK i `aces.vromfs.bin` (0 där den saknar en) |
| Vattenhöjdkarta (`WHM`: ett rutnät av platta celler och 130x130-sidor med 16-bitars höjder) | läst där en nivå har en; dess floder sluttar med marken |
| Taktikkartor | från `content/base/res/locations_maps.dxp.bin`, placerade via BLK:ens `mapCoord0/1` och `tankMapCoord0/1`; bildens överkant är norr |
| Placerade objekt (`RIGz`: renderingsinstansgeneratorns fasta instanser) | varje instans, som en 3x4-matris av 16-bitars värden eller, på vissa nivåer, 32-bitars (cellens bytestorlek avgör); varje byte i varje cell redovisad på de kontrollerade nivåerna |
| Genererade objekt (`RIGz`:s markklassmasker och `LandClass`-resurserna) | spelets generator, portad: samma platser prövas i samma ordning med samma slumptal, markklass- och uteslutningsmaskerna, objektet som väljs på varje plats, dess rotation, skala och höjdförskjutning; kakelsatta (stadskvarter) och planterade (skogar, buskar, åkrar) enheter. Genereras bara över stridsvagnskartan. Approximerat: markhöjden och normalen (från höjdkartan; spelet spårar en stråle), uteslutningslådorna som spelet registrerar vid körning, och trädens gir (spelet fäster den vid impostorns rotationspalett) |
| Renderingsmeshar (`RendInst`-resurser i `content/*/res/*.grp`, material i `riDesc.bin`) | varje LOD:s hörn och trianglar (flyttalspositioner; 16- eller 32-bitars index, vanliga eller meshoptimizer-packade), varje elements material. Dekal- och impostor-skyltelement lämnas bort; de genomskinliga (glas) behålls |
| Objektfärger | per material, medelvärdet av dess diffusa textur i en liten mip (alfaviktat för löv), från installationens texturpaket: t0 för de flesta shaders, första detaljdiffusa där t0 är ett överlägg eller en mask. En färg per material: ingen textur på objekten |
| Kollisionsformer (`<object>_collision`) | kollisionsresurser av strömversion 3, används där ett objekt saknar renderingsmesh. Endast det som spelets strålar träffar (`TRACEABLE`-noder) ritas, och lådor, sfärer och kapslar bara när resursen saknar mesh; resten är grova fysikersättningar som skulle synas som kuber runt objektet |
| Navigeringsmesh (`Lnav`), den renderade landnätet, gräs, `spgz`, `stbl`, `d2co` | inte lästa |

Nivåerna är komprimerade med Oodle, som är proprietärt. Spelet levererar en kopia,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (en vanlig x64-version), och det
är den som läses in; `HEAT3D_OODLE=<dll eller mapp>` pekar på en annan.
Inget av Oodle ingår här.

## Format, och var de dokumenteras {#formats-and-where-they-are-documented}

Gaijin publicerade Dagor Engines källkod under BSD 3-Clause-licensen
(github.com/GaijinEntertainment/DagorEngine). Läsarna här skrevs utifrån den;
ingen spelkod dekompilerades. Varje modul anger vilka källfiler den följer:

- `vromfs.py`: `*.vromfs.bin` (huvud `VRFs`/`VRFx`, en zstd-kropp vars första och
  sista 16 byte XOR:as med en fast nyckel, en namntabell och en förskjutningstabell:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  och binär BLK (form 1-5, med arkivets delade namnkarta `\xff?nm` och zstd-ordbok:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: texturpaket `DxP2` (`lib3d/texPackMgr2.cpp`) och DDSx-huvuden
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 avkodas av Pillow.
- `dagorlevel.py`: nivåbinären (`scene/loadLevel.cpp`), höjdkartan
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  markstrålspåraren (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) och vattenhöjdkartan
  (`fftWater/fftWater.cpp`).
- `rigen.py`: de placerade objekten (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: de genererade objekten (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: renderingsinstanser (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) och meshoptimizers
  indexkodek (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: markens färg (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: resurspaket (`gameRes/grpData.h`) och kollisionsresurser
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  vars trianglar lagras som en fyrkants-BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) läser samma arkiv; det behövs inte och används inte.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
