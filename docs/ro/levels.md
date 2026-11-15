---
title: Niveluri
nav_order: 9
lang: ro
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Niveluri (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` transformă nivelurile din propria dumneavoastră instalare War Thunder în niveluri `.glb`
pentru vizualizator, în același cadru ca tabelele replay-urilor.

## Pas cu pas {#step-by-step}

1. Listează nivelurile din instalarea dumneavoastră: `heat3d-wt-level list`. Afișează câte o
   linie pentru fiecare nivel: numele său, terenul și hărțile sale, apoi numărul. De exemplu
   (un nivel inventat):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrage unul, mai multe (sunt permise wildcard-uri) sau toate:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Încarcă `levels/<level>/<level>.glb` în panoul Fundal / nivel al vizualizatorului, sub
   bătăliile acelei hărți.

Nivelurile pe care le scrieți rămân pe calculatorul dumneavoastră: nu le publicați niciodată (vedeți
[Termeni și licență](terms.md)).

## Opțiuni {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Comandă / opțiune | Ce face |
|---|---|
| `list [--game FOLDER]` | fiecare nivel din instalare |
| `extract <levels...>` / `--all` | nivelurile numite (așa cum le afișează `list`; sunt permise wildcard-uri), sau fiecare nivel |
| `-o`, `--out` | folderul de ieșire; fiecare nivel intră în `<out>/<level>/` |
| `--game FOLDER` | folderul War Thunder (implicit: găsit prin Steam sau launcher; de asemenea `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | pasul de eșantionare a terenului, culoarea terenului și bugetul de obiecte peste harta de tancuri (implicit `medium`) |
| `--max-object-triangles N` | bugetul de obiecte (implicit: al detaliului) |
| `--max-grid N` | eșantioane ale heightmap-ului pe o latură, pe parte (implicit 1024) |
| `--no-objects` | lasă afară clădirile, copacii și alte obiecte plasate |
| `--no-generated` | lasă afară obiectele generate de clasele de teren (păduri, orașe) |
| `--no-terrain-colour` | texturează terenul cu harta tactică, nu cu clasele de teren |
| `--no-texture` | lasă terenul fără textură |
| `--skip-existing` | lasă nivelurile al căror `.glb` există deja |

## Ce se scrie {#what-is-written}

Fiecare nivel devine `<out>/<level>/<level>.glb`, `<level>.json` (ce s-a citit,
nivelul apei, dreptunghiurile hărților, numărul de triunghiuri, duratele) și hărțile tactice
ale nivelului ca `<level>_map.png` (harta aerului) și `<level>_tankmap.png`;
hărțile de sol primesc și `<level>_terrain.png`, culorile proprii ale terenului peste harta de tancuri. Fișierul glb este scris în
`<level>.glb.part` și redenumit când este gata;
cât timp un nivel este scris, `<out>/<level>/.<level>.lock` este ținut, deci două
extrageri nu scriu niciodată același nivel (a doua afișează `busy <level>`).
Instalarea este găsită prin Steam sau prin folderele implicite ale launcher-ului;
`--game <folder>` sau `HEAT3D_WT_GAME` arată altfel unde se află.

| Parte | Ce este |
|---|---|
| `ground:<level>` | heightmap-ul terenului (`HM2`) ca o grilă; pe hărțile de sol mijlocul hărții de tancuri (jumătate din lățimea sa) la pasul din `--detail`, colorat cu clasele de teren, decalurile de sol și drumurile (`<level>_terrain.png`; harta tactică acolo unde nu poate fi făcută); pe hărțile fără hartă de tancuri (hărți de aer), tot heightmap-ul la un singur pas (2048 de eșantioane pe o latură la `high`, 1024 altfel), colorat cu clasele de teren peste zona hărții aerului (4096 de pixeli pe o latură, aproximativ 32 m un pixel peste 131 km; harta tactică acolo unde nu poate fi făcută); pe niveluri fără heightmap, plasa terenului |
| `ground:<level> tank map` | restul hărții de tancuri, cu un pas mai grosier |
| `ground:<level> heightmap surroundings` | restul heightmap-ului, și mai grosier |
| `ground:<level> land mesh` | triunghiurile de coliziune ale plasei terenului acolo unde heightmap-ul nu ajunge (împrejurimile unei hărți de tancuri, până la zeci de kilometri); pe niveluri fără heightmap este terenul, colorat ca mai sus |
| `ground:<level> outside the map` | teren pe care imaginea nu îl acoperă, fără textură |
| `water:<level>` | un dreptunghi plat la `water_level` al nivelului peste tot terenul: jocul desenează apa ca un singur plan, iar terenul jos de sub ea este mare, lac sau albie de râu |
| `water:<level> rivers` | pe niveluri cu un heightmap de apă (`WHM`), suprafața de apă înclinată peste celulele pe care le acoperă |
| `structure:<level> buildings` | fiecare obiect plasat care nu este o plantă: case, ruine, ziduri, garduri, poduri, șine, stânci, recuzită. Cele fixe (`RIGz`) și, peste harta de tancuri, cele pe care le generează clasele de teren (blocuri de oraș, pietre). Fiecare este desenat cu plasa sa de randare (ziduri, acoperișuri, deschideri de ferestre, grinzi), la LOD-ul pe care îl permite bugetul de triunghiuri, colorat pe material după media texturii sale difuze |
| `structure:<level> trees` | copaci și tufișuri, fixi și generați (păduri, garduri vii): plasa lor de randare acolo unde permite bugetul, altfel un trunchi și o coroană (un con pentru conifere) în culoarea frunzelor copacului, la dimensiunea sa reală |

Obiectele fără plasă de randare revin la forma lor de coliziune; copacii fără una, la
coroană. Culorile vârfurilor (`COLOR_0`) țin valori codificate sRGB,
așa cum le citește vizualizatorul 3DHeat.

**Coordonatele** sunt metrii jocului cu z oglindit: glb (x, y, z) = joc
(x, y, -z). Lumea jocului este cu sistemul de coordonate stângaci (x est, y sus, z nord); glTF este
dreptaci. `heat3d-wt-replay` păstrează z-ul jocului și îi spune vizualizatorului să îl oglindească, deci un replay și nivelul
hărții sale se așază unul peste celălalt fără niciun pas de plasare. JSON-ul dă dreptunghiul
fiecărei hărți tactice în metri ai jocului și colțurile sale în spațiul glb, pentru încărcarea PNG-ului ca imagine de hartă.

**Detaliul.** `--detail low|medium|high` (implicit medium) stabilește, peste harta de tancuri:

| | mijlocul hărții de tancuri | restul hărții de tancuri | culoarea terenului | bugetul obiectelor | cele mai multe triunghiuri per obiect | plante generate păstrate |
|---|---|---|---|---|---|---|
| low | la fiecare al 4-lea eșantion | la fiecare al 8-lea | 4 m un pixel | 1,2 M | 1.500 | copaci 35 %, tufișuri 20 % |
| medium | la fiecare al 2-lea | la fiecare al 4-lea | 2 m | 3,5 M | 4.000 | copaci 70 %, tufișuri 50 % |
| high | fiecare eșantion (2 m pe majoritatea hărților de sol) | la fiecare al 2-lea | 1 m (cel mult 4096 de pixeli pe o latură) | 4,5 M | 12.000 | toate |

Cele două inele ale hărții de tancuri sunt ținute la 0,3 M (low), 1 M (medium) și 3,7 M (high)
triunghiuri: pe hărțile al căror heightmap este mai fin de 2 m, pașii se dublează
(inelul exterior primul) până când încap, deci și acelea ies la aproximativ 2 m.

O hartă de sol la `high` iese la aproximativ 8 milioane de triunghiuri (3,5 M de teren,
4,5 M de obiecte) și 250 MB; la `medium` la aproximativ 4,5 M. LOD-urile obiectelor sunt
cele pe care le-ar desena jocul însuși de la o singură distanță de vizualizare, cel mai scurt
al cărui total încape în buget: recuzita mică trece mai întâi la LOD-uri grosiere și clădirile mari ultimele, după
intervalele date de creatorii lor pentru fiecare LOD (`lodDistance` din JSON); ce economisește pasul
peste buget se întoarce către cele mai mari obiecte. Culoarea grosieră a terenului (hărți de aer) face media
texturilor reținute ale fiecărei clase de teren până la dimensiunea pixelului înainte, ca
plăcile să nu producă moire. Dacă nici cele mai grosiere LOD-uri nu încap, copacii care economisesc cel mai mult devin
coroane, iar apoi tipurile cele mai mici sunt lăsate afară (`leftOut`); niciun obiect
nu este desenat ca o cutie (o formă de coliziune, dacă există, este a obiectului însuși).
Obiectele generate sunt rărite determinist după fel (`density`), aceleași
la fiecare rulare. `--max-object-triangles` înlocuiește bugetul, `--max-grid` (implicit 1024) limitează părțile mai grosiere ale heightmap-ului, `--no-objects`
lasă obiectele afară, `--no-generated` pe cele generate, `--no-terrain-colour`
texturează terenul cu harta tactică, `--no-texture` lasă terenul fără textură.

`parts.objects` din JSON listează instanțele (fixe și generate, după fel și clasă de teren), câte au fost desenate la ce LOD (`drawnAs`), triunghiurile, distanța LOD și secundele; `parts.heightmap.rings` pasul și triunghiurile fiecărui inel de teren; `parts.terrainColour` clasele de teren și culorile lor, drumurile și decalurile de sol; `trianglesTotal`, `glbBytes` și `secondsBy` totalurile.

## Ce se citește, și cât de bine {#what-is-read-and-how-well}

| Parte | Stare |
|---|---|
| Fișierul binar al nivelului (`levels/<level>.bin`, `DBLD` 3x64): tabela de blocuri | fiecare nivel verificat |
| Heightmap (`HM2`, versiunile 0-2; versiunea 2 are valori de 8 biți în blocuri, bucăți Oodle sau zstd) | fiecare nivel al cărui heightmap este versiunea 2 cu bucăți Oodle; verificat cu ochiul față de hărțile lor tactice (râurile, văile, țărmurile și orașele se aliniază) |
| Coliziunea plasei terenului (`lmap`, trasorul său de raze `LTdump`) | citită acolo unde un nivel are una (împachetată Oodle). Este suprafața de coliziune a jocului, nu plasa desenată, deci este mai grosieră acolo unde terenul este plat |
| Culoarea terenului (clasele de teren și harta de greutăți din `lmap`, harta fizică `LMp2`, `hspl` splines) | hărțile de culoare ale claselor de teren și texturile lor de detaliu (culorile lor medii) ponderate de harta de greutăți, indexul de biom de 1 m al claselor de teren indexate, formele drumurilor și ale decalurilor de sol din harta fizică în culoarea texturii splines-ului sau materialului lor, stânci pe pante abrupte. Verificat față de hărțile de tancuri: drumurile, orașele, lacurile, centurile de pădure și afloramentele de stâncă se aliniază. Formula de culoare a shaderului de teren al War Thunder nu este în codul sursă public; se folosește cea publicată de motor (daNetGame), care iese mai saturată decât harta tactică |
| Nivelul apei | `water_level` din BLK-ul nivelului din `aces.vromfs.bin` (0 unde nu are) |
| Heightmap-ul apei (`WHM`: o grilă de celule plate și pagini de 130x130 de înălțimi pe 16 biți) | citit acolo unde un nivel are unul; râurile sale se înclină odată cu terenul |
| Hărțile tactice | din `content/base/res/locations_maps.dxp.bin`, plasate prin `mapCoord0/1` și `tankMapCoord0/1` din BLK; partea de sus a imaginii este nordul |
| Obiectele plasate (`RIGz`: instanțele fixe ale generatorului de instanțe de randare) | fiecare instanță, ca o matrice 3x4 de valori pe 16 biți sau, pe unele niveluri, pe 32 de biți (numărul de octeți al celulei decide); fiecare octet al fiecărei celule contabilizat pe nivelurile verificate |
| Obiectele generate (măștile claselor de teren `RIGz` și resursele `LandClass`) | generatorul jocului, portat: aceleași locuri încercate în aceeași ordine cu aceleași numere aleatoare, măștile claselor de teren și de excludere, obiectul ales în fiecare loc, rotația, scara și decalajul de înălțime ale sale; entități așezate pe plăci (blocuri de oraș) și plantate (păduri, tufișuri, câmpuri). Generate doar peste harta de tancuri. Aproximat: înălțimea și normala terenului (din heightmap; jocul trasează o rază), cutiile de excludere pe care jocul le înregistrează la rulare și unghiul de rotație al copacilor (jocul îl fixează pe paleta de rotații a imposterului) |
| Plase de randare (resursele `RendInst` din `content/*/res/*.grp`, materialele din `riDesc.bin`) | vârfurile și triunghiurile fiecărui LOD (poziții float; indici pe 16 sau 32 de biți, simpli sau împachetați cu meshoptimizer), materialul fiecărui element. Elementele de decal și de imposter-billboard sunt lăsate afară; cele transparente (sticla) sunt păstrate |
| Culorile obiectelor | pe material, media micului mip al texturii sale difuze (ponderată după alfa pentru frunze), din pachetele de texturi ale instalării: t0 pentru majoritatea shaderelor, prima difuză de detaliu acolo unde t0 este o suprapunere sau o mască. O culoare pe material: fără textură pe obiecte |
| Formele de coliziune (`<object>_collision`) | resurse de coliziune din versiunea 3 a fluxului, folosite acolo unde un obiect nu are plasă de randare. Sunt desenate doar ce lovesc razele jocului (nodurile `TRACEABLE`), iar cutiile, sferele și capsulele doar când resursa nu are plasă: restul sunt substituenți grosieri de fizică, care ar apărea ca niște cuburi în jurul obiectului |
| Plasa de navigare (`Lnav`), plasa terenului desenată, iarba, `spgz`, `stbl`, `d2co` | nu sunt citite |

Nivelurile sunt comprimate cu Oodle, care este proprietar. Jocul livrează o copie,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (o construcție x64 obișnuită),
și aceasta este încărcată; `HEAT3D_OODLE=<dll or folder>` indică alta.
Nimic din Oodle nu este inclus aici.

## Formate, și unde sunt documentate {#formats-and-where-they-are-documented}

Gaijin a publicat codul sursă al Dagor Engine sub licența BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Cititorii de aici au fost scriși după el;
niciun cod al jocului nu a fost decompilat. Fiecare modul numește fișierele sursă pe care le urmează:

- `vromfs.py`: `*.vromfs.bin` (antetul `VRFs`/`VRFx`, un corp zstd al cărui primii și ultimii 16 octeți sunt
  XOR-ați cu o cheie fixă, o tabelă de nume și o tabelă de decalaje:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  și BLK binar (formele 1-5, cu harta de nume comună a arhivei `\xff?nm` și
  dicționarul zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: pachete de texturi `DxP2` (`lib3d/texPackMgr2.cpp`) și antete DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 sunt decodate de Pillow.
- `dagorlevel.py`: fișierul binar al nivelului (`scene/loadLevel.cpp`), heightmap-ul
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  trasorul de raze al terenului (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) și heightmap-ul apei
  (`fftWater/fftWater.cpp`).
- `rigen.py`: obiectele plasate (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: obiectele generate (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: instanțele de randare (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) și codecul de indici
  al meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: culoarea terenului (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: pachetele de resurse (`gameRes/grpData.h`) și resursele de coliziune
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  ale căror triunghiuri sunt stocate ca un BVH de patrulatere (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) citește aceleași arhive; nu este necesar și nu este folosit.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
