---
title: "Levels"
nav_order: 9
lang: "nl"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Levels (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` zet de levels van je eigen installatie van War Thunder om in
`.glb`-levels voor de viewer, in hetzelfde assenstelsel als de tabellen van de replays.

## Stap voor stap {#step-by-step}

1. Maak een lijst van de levels in je installatie: `heat3d-wt-level list`. Die drukt
   één regel per level af: de naam, het terrein en de kaarten, daarna het aantal. Bijvoorbeeld
   (een verzonnen level):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Haal er één, meerdere (jokertekens zijn toegestaan) of alle uit:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Laad `levels/<level>/<level>.glb` in het paneel Achtergrond / level van de viewer, onder de
   gevechten van die kaart.

De levels die je schrijft blijven op je eigen computer: publiceer ze nooit (zie
[Voorwaarden en licentie](terms.md)).

## Opties {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Commando / optie | Doet |
|---|---|
| `list [--game MAP]` | elk level in de installatie |
| `extract <levels...>` / `--all` | de genoemde levels (zoals `list` ze afdrukt; jokertekens zijn toegestaan), of elk level |
| `-o`, `--out` | uitvoermap; elk level gaat in `<out>/<level>/` |
| `--game MAP` | de map van War Thunder (standaard: gevonden via Steam of de launcher; ook `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | bemonstering van de grond, grondkleur en objectbudget over de tankkaart (standaard `medium`) |
| `--max-object-triangles N` | het objectbudget (standaard: dat van het detailniveau) |
| `--max-grid N` | hoogtekaartsamples per zijde, per deel (standaard 1024) |
| `--no-objects` | laat gebouwen, bomen en andere geplaatste objecten weg |
| `--no-generated` | laat de objecten weg die de landklassen genereren (bossen, steden) |
| `--no-terrain-colour` | bekleed de grond met de tactische kaart, niet met de landklassen |
| `--no-texture` | laat de grond zonder textuur |
| `--skip-existing` | laat levels over waarvan de `.glb` al bestaat |

## Wat er geschreven wordt {#what-is-written}

Elk level wordt `<out>/<level>/<level>.glb`, `<level>.json` (wat er gelezen is, het
waterniveau, de kaartrechthoeken, aantallen driehoeken, tijden) en de tactische kaarten
van het level als `<level>_map.png` (de luchtkaart) en `<level>_tankmap.png`;
grondkaarten krijgen ook `<level>_terrain.png`, de eigen kleuren van de grond over de
tankkaart. De glb wordt eerst naar `<level>.glb.part` geschreven en daarna hernoemd als
hij klaar is; zolang een level geschreven wordt, is `<out>/<level>/.<level>.lock`
bezet, zodat twee extracties nooit hetzelfde level schrijven (de tweede drukt
`busy <level>` af). De installatie wordt gevonden via Steam of de standaardmappen van
de launcher; `--game <map>` of `HEAT3D_WT_GAME` geven anders aan waar die staat.

| Onderdeel | Wat het is |
|---|---|
| `ground:<level>` | de hoogtekaart van het terrein (`HM2`) als raster; op grondkaarten het midden van de tankkaart (de halve breedte) op de stap van `--detail`, gekleurd met de landklassen, grondafbeeldingen en wegen (`<level>_terrain.png`; de tactische kaart waar dat niet te maken is); op kaarten zonder tankkaart (luchtkaarten) de hele hoogtekaart op één stap (2048 samples per zijde bij `high`, anders 1024), gekleurd met de landklassen over het gebied van de luchtkaart (4096 pixels per zijde, ongeveer 32 m per pixel over 131 km; de tactische kaart waar dat niet te maken is); op levels zonder hoogtekaart het landmesh |
| `ground:<level> tank map` | de rest van de tankkaart, één stap grover |
| `ground:<level> heightmap surroundings` | de rest van de hoogtekaart, nog grover |
| `ground:<level> land mesh` | de botsingsdriehoeken van het landmesh waar de hoogtekaart niet reikt (de omgeving van een tankkaart, tot tientallen kilometers); op levels zonder hoogtekaart is het de grond, gekleurd zoals hierboven |
| `ground:<level> outside the map` | grond die het beeld niet dekt, zonder textuur |
| `water:<level>` | één vlakke rechthoek op het `water_level` van het level over al het terrein: het spel tekent water als één vlak, en laag terrein eronder is zee, meer of rivierbedding |
| `water:<level> rivers` | op levels met een waterhoogtekaart (`WHM`) het hellende wateroppervlak over de cellen die het bedekt |
| `structure:<level> buildings` | elk geplaatst object dat geen plant is: huizen, ruïnes, muren, hekken, bruggen, rails, rotsen, rekwisieten. De vaste (`RIGz`) en, over de tankkaart, die welke de landklassen genereren (stadsblokken, stenen). Elk wordt getekend met zijn rendermesh (muren, daken, raamopeningen, balken), op het LOD dat het driehoekenbudget toelaat, per materiaal gekleurd met het gemiddelde van zijn diffuse textuur |
| `structure:<level> trees` | bomen en struiken, vast en gegenereerd (bossen, heggen): hun rendermesh waar het budget het toelaat, anders een stam en een kruin (een kegel voor naaldbomen) in de eigen bladkleur van de boom, op de echte grootte van de boom |

Objecten zonder rendermesh vallen terug op hun botsingsvorm; bomen zonder rendermesh op de
kruin. Hoekkleuren (`COLOR_0`) bevatten sRGB-gecodeerde waarden, zoals de 3DHeat-viewer ze leest.

**Coördinaten** zijn de meters van het spel met z gespiegeld: glb (x, y, z) = spel
(x, y, -z). De wereld van het spel is linkshandig (x oost, y omhoog, z noord); glTF is
rechtshandig. `heat3d-wt-replay` houdt de z van het spel en vertelt de viewer die te
spiegelen, zodat een replay en het level van zijn kaart op elkaar vallen zonder plaatsingsstap.
De JSON geeft de rechthoek van elke tactische kaart in meters van het spel en de hoeken ervan
in de ruimte van de glb, om de PNG als kaartafbeelding te laden.

**Detail.** `--detail low|medium|high` (standaard medium) stelt, over de tankkaart, het volgende in:

| | midden van de tankkaart | rest van de tankkaart | grondkleur | objectbudget | meeste driehoeken per object | gegenereerde planten behouden |
|---|---|---|---|---|---|---|
| low | elke 4e sample | elke 8e | 4 m per pixel | 1,2 M | 1.500 | bomen 35 %, struiken 20 % |
| medium | elke 2e | elke 4e | 2 m | 3,5 M | 4.000 | bomen 70 %, struiken 50 % |
| high | elke sample (op de meeste grondkaarten 2 m) | elke 2e | 1 m (hooguit 4096 pixels per zijde) | 4,5 M | 12.000 | alle |

De twee ringen van de tankkaart worden begrensd tot 0,3 M (low), 1 M (medium) en 3,7 M (high)
driehoeken: op de kaarten waarvan de hoogtekaart fijner is dan 2 m, verdubbelen de
stappen (de buitenste ring eerst) tot ze passen, zodat die ook op ongeveer 2 m uitkomen.

Een grondkaart op `high` komt uit op ongeveer 8 miljoen driehoeken (3,5 M grond,
4,5 M objecten) en 250 MB; op `medium` op ongeveer 4,5 M. De LOD's van de objecten zijn
die welke het spel zelf van één kijkafstand zou tekenen, de kortste waarvan het totaal past in
het budget: kleine rekwisieten vallen het eerst terug op grove LOD's en grote gebouwen het
laatst, volgens de afstanden die hun makers voor elk LOD gaven (de `lodDistance` in de JSON);
wat die stap boven het budget uitspaart, gaat terug naar de grootste objecten. Grove grondkleur
(luchtkaarten) middelt eerst de getegelde textuur van elke landklasse terug naar de pixelgrootte,
zodat de tegels geen moiré geven. Passen zelfs de grofste LOD's niet, dan worden de bomen die
het meest besparen kruinen, en daarna worden de kleinste typen weggelaten (`leftOut`); geen object
wordt als doos getekend (een botsingsvorm, als die er is, is het eigen object).
Gegenereerde objecten worden per soort deterministisch uitgedund (`density`), dezelfde
elke keer. `--max-object-triangles` overschrijft het budget, `--max-grid` (standaard 1024)
begrenst de grovere delen van de hoogtekaart, `--no-objects` laat objecten weg, `--no-generated`
de gegenereerde, `--no-terrain-colour` bekleedt de grond met de tactische kaart, en `--no-texture`
laat de grond zonder textuur.

De `parts.objects` van de JSON somt de exemplaren op (vast en gegenereerd, per soort en landklasse),
hoeveel er op welk LOD getekend zijn (`drawnAs`), de driehoeken, de LOD-afstand en de seconden;
`parts.heightmap.rings` de stap en driehoeken van elke grondring; `parts.terrainColour` de landklassen
en hun kleuren, wegen en grondafbeeldingen; `trianglesTotal`, `glbBytes` en `secondsBy` de totalen.

## Wat er gelezen wordt, en hoe goed {#what-is-read-and-how-well}

| Onderdeel | Status |
|---|---|
| Levelbinair (`levels/<level>.bin`, `DBLD` 3x64): de blokkentabel | elk level gecontroleerd |
| Hoogtekaart (`HM2`, versies 0-2; versie 2 is 8-bits waarden in blokken, Oodle- of zstd-chunks) | elk level waarvan de hoogtekaart versie 2 is met Oodle-chunks; met het oog gecontroleerd tegen hun tactische kaarten (rivieren, dalen, kusten en steden lopen gelijk) |
| Botsing van het landmesh (`lmap`, zijn `LTdump`-straalvolger) | gelezen waar een level er een heeft (Oodle-gepakt). Het is het botsingsoppervlak van het spel, niet het getekende mesh, dus het is grover waar het land vlak is |
| Grondkleur (`lmap`-landklassen en gewichtskaart, `LMp2`-fysicakaart, `hspl`-splines) | de kleurkaarten van de landklassen en hun detailtexturen (hun gemiddelde kleuren), gewogen met de gewichtskaart, de biome-index van 1 m van geïndexeerde landklassen, de vorm van wegen en grondafbeeldingen uit de fysicakaart in de kleur van de textuur van hun spline of materiaal, en steile hellingen als rotswanden. Gecontroleerd tegen de tankkaarten: wegen, steden, meren, bosstroken en rotsuitsteeksels lopen gelijk. De kleurformule van de eigen terreinshader van War Thunder staat niet in de openbare broncode; de gepubliceerde formule van de engine (daNetGame) wordt gebruikt, die verzadigder uitkomt dan de tactische kaart |
| Waterniveau | `water_level` uit de BLK van het level in `aces.vromfs.bin` (0 waar er geen is) |
| Waterhoogtekaart (`WHM`: een raster van vlakke cellen en pagina's van 130x130 met 16-bits hoogtes) | gelezen waar een level er een heeft; zijn rivieren hellen mee met het terrein |
| Tactische kaarten | uit `content/base/res/locations_maps.dxp.bin`, geplaatst volgens `mapCoord0/1` en `tankMapCoord0/1` van de BLK; de bovenkant van het beeld is noord |
| Geplaatste objecten (`RIGz`: de vaste exemplaren van de generator van render-instances) | elk exemplaar, als een 3x4-matrix van 16-bits waarden of, op sommige levels, 32-bits (het aantal bytes van de cel bepaalt het); elke byte van elke cel verklaard op de gecontroleerde levels |
| Gegenereerde objecten (`RIGz`-maskers van landklassen en de `LandClass`-resources) | de generator van het spel, overgezet: dezelfde plekken in dezelfde volgorde met dezelfde willekeurige getallen, de maskers van landklassen en uitsluiting, het object dat op elke plek gekozen wordt, zijn rotatie, schaal en hoogteverschuiving; getegelde (stadsblokken) en beplante (bossen, struiken, velden) entiteiten. Alleen over de tankkaart gegenereerd. Benaderd: de grondhoogte en -normaal (uit de hoogtekaart; het spel volgt een straal), de uitsluitingsdozen die het spel tijdens het draaien registreert, en de gier van bomen (het spel snapt die naar de rotatiepalet van de impostor). |
| Rendermeshes (`RendInst`-resources in `content/*/res/*.grp`, materialen in `riDesc.bin`) | de hoekpunten en driehoeken van elk LOD (float-posities; 16- of 32-bits indices, gewoon of met meshoptimizer gepakt), het materiaal van elk element. Decal- en impostor-billboardelementen worden weggelaten; de transparante (glas) blijven behouden |
| Kleuren van objecten | per materiaal het gemiddelde van de kleine mip van de diffuse textuur (alfa-gewogen voor bladeren), uit de texturenpakketten van de installatie: t0 voor de meeste shaders, de eerste detail-diffuse waar t0 een overlay of masker is. Eén kleur per materiaal: geen textuur op de objecten |
| Botsingsvormen (`<object>_collision`) | botsingsresources van streamversie 3, gebruikt waar een object geen rendermesh heeft. Alleen wat de stralen van het spel raken (`TRACEABLE`-knopen) wordt getekend, en dozen, bollen en capsules alleen als de resource geen mesh heeft: de rest zijn grove fysicastandaarden die als kubussen rond het object zouden verschijnen |
| Navigatiemesh (`Lnav`), het getekende landmesh, gras, `spgz`, `stbl`, `d2co` | niet gelezen |

Levels zijn gecomprimeerd met Oodle, dat eigendom is van een ander bedrijf. Het spel levert een kopie,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (een gewone x64-build), en die wordt
geladen; `HEAT3D_OODLE=<dll of map>` wijst naar een andere. Niets van Oodle is hier
meegeleverd.

## Formaten, en waar ze gedocumenteerd zijn {#formats-and-where-they-are-documented}

Gaijin heeft de broncode van de Dagor Engine gepubliceerd onder de BSD 3-Clause-licentie
(github.com/GaijinEntertainment/DagorEngine). De lezers hier zijn daarop geschreven;
er is geen spelcode gedecompileerd. Elke module noemt de broncodebestanden die hij volgt:

- `vromfs.py`: `*.vromfs.bin` (kop `VRFs`/`VRFx`, een zstd-romp waarvan de eerste en
  laatste 16 bytes met een vaste sleutel worden geXORd, een naamtabel en een offsettabel:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  en binaire BLK (vormen 1-5, met de gedeelde naamkaart van het archief `\xff?nm` en het
  zstd-woordenboek: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: texturenpakketten `DxP2` (`lib3d/texPackMgr2.cpp`) en DDSx-koppen
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 worden door Pillow gedecodeerd.
- `dagorlevel.py`: het levelbinair (`scene/loadLevel.cpp`), de hoogtekaart
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  de straalvolger van het land (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) en de waterhoogtekaart
  (`fftWater/fftWater.cpp`).
- `rigen.py`: de geplaatste objecten (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: de gegenereerde objecten (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: render-instances (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) en de indexcodec van
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: de grondkleur (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: resourcepakketten (`gameRes/grpData.h`) en botsingsresources
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  waarvan de driehoeken worden opgeslagen als een quad-BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) leest dezelfde archieven; het is niet nodig en wordt niet gebruikt.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
