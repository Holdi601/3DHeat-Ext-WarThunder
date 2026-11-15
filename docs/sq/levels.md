---
title: "Nivelet"
nav_order: 9
lang: sq
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Nivelet (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` i kthen nivelet e instalimit tënd të War Thunder në
nivele `.glb` për shikuesin, në të njëjtin kuadër me tabelat e riluajtjeve.

## Hap pas hapi {#step-by-step}

1. Liston nivelet e instalimit tënd: `heat3d-wt-level list`. Printon një
   rresht për çdo nivel: emrin, terrenin dhe hartat e tij, pastaj numrin. Për
   shembull (një nivel i shpikur):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Nxirr një, disa (lejohen shenja wildcard) ose të gjitha:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Ngarko `levels/<level>/<level>.glb` te paneli Sfondi / niveli i shikuesit, nën
   betejat e asaj harte.

Nivelet që shkruan mbeten në makinën tënde: mos i publiko kurrë (shih
[Kushtet dhe licenca](terms.md)).

## Opsionet {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Komanda / opsioni | Çfarë bën |
|---|---|
| `list [--game FOLDER]` | çdo nivel në instalim |
| `extract <levels...>` / `--all` | nivelet e emërtuara (siç i printon `list`; lejohen wildcards), ose çdo nivel |
| `-o`, `--out` | dosja e daljes; çdo nivel shkon në `<out>/<level>/` |
| `--game FOLDER` | dosja e War Thunder (e paracaktuar: gjendet përmes Steam ose nisësit; edhe `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | mostrimi i tokës, ngjyra e tokës dhe buxheti i objekteve mbi hartën e tankeve (e paracaktuar `medium`) |
| `--max-object-triangles N` | buxheti i objekteve (e paracaktuar: ai i detajit) |
| `--max-grid N` | mostra heightmap për anë, për pjesë (e paracaktuar 1024) |
| `--no-objects` | lë jashtë ndërtesat, pemët dhe objekte të tjera të vendosura |
| `--no-generated` | lë jashtë objektet që gjenerojnë klasat e tokës (pyje, qytete) |
| `--no-terrain-colour` | teksturon tokën me hartën taktike, jo me klasat e tokës |
| `--no-texture` | e lë tokën pa teksturë |
| `--skip-existing` | lë nivelet, `.glb` e të cilave ekziston |

## Çfarë shkruhet {#what-is-written}

Çdo nivel bëhet `<out>/<level>/<level>.glb`, `<level>.json` (çfarë u lexua,
niveli i ujit, drejtkëndëshat e hartave, numrat e trekëndëshave, kohët) dhe hartat
taktike të nivelit si `<level>_map.png` (harta ajrore) dhe `<level>_tankmap.png`;
hartat tokësore marrin edhe `<level>_terrain.png`, ngjyrat e vetë tokës mbi
hartën e tankeve. Glb shkruhet te `<level>.glb.part` dhe riemërtohet kur mbaron;
ndërsa një nivel shkruhet, mbahet `<out>/<level>/.<level>.lock`, kështu që dy
nxjerrje nuk shkruajnë kurrë të njëjtin nivel (e dyta printon `busy <level>`).
Instalimi gjendet përmes Steam ose dosjeve të paracaktuara të nisësit;
përndryshe `--game <folder>` ose `HEAT3D_WT_GAME` tregojnë ku është.

| Pjesa | Çfarë është |
|---|---|
| `ground:<level>` | heightmap e terrenit (`HM2`) si rrjetë; në hartat tokësore mesi i hartës së tankeve (gjysma e gjerësisë së saj) me hapin e `--detail`, i ngjyrosur me klasat e tokës, decal-et e tokës dhe rrugët (`<level>_terrain.png`; harta taktike aty ku kjo nuk mund të bëhet); në harta pa hartë tankesh (harta ajrore), i gjithë heightmap me një hap (2048 mostra për anë në `high`, 1024 përndryshe), i ngjyrosur me klasat e tokës mbi sipërfaqen e hartës ajrore (4096 piksel për anë, rreth 32 m për piksel mbi 131 km; harta taktike aty ku kjo nuk mund të bëhet); në nivele pa heightmap, rrjeta e tokës |
| `ground:<level> tank map` | pjesa tjetër e hartës së tankeve, një hap më e trashë |
| `ground:<level> heightmap surroundings` | pjesa tjetër e heightmap, edhe më e trashë |
| `ground:<level> land mesh` | trekëndëshat e përplasjes së rrjetës së tokës aty ku heightmap nuk arrin (rrethinat e një harte tankesh, deri në dhjetëra kilometra); në nivele pa heightmap është toka, e ngjyrosur si më sipër |
| `ground:<level> outside the map` | toka që imazhi nuk e mbulon, pa teksturë |
| `water:<level>` | një drejtkëndësh i sheshtë në `water_level` të nivelit mbi të gjithë terrenin: loja e vizaton ujin si një plan, dhe toka e ulët nën të është shtrat deti, liqeni ose lumi |
| `water:<level> rivers` | në nivele me heightmap uji (`WHM`), sipërfaqja e pjerrët e ujit mbi qelizat që mbulon |
| `structure:<level> buildings` | çdo objekt i vendosur që nuk është bimë: shtëpi, rrënoja, mure, rrethoja, ura, shina, shkëmbinj, objekte. Ato fikse (`RIGz`) dhe, mbi hartën e tankeve, ato që gjenerojnë klasat e tokës (blloqe qyteti, gurë). Secili vizatohet nga rrjeta e tij e renderimit (mure, çati, hapje dritaresh, trarë), në LOD-in që lejon buxheti i trekëndëshave, i ngjyrosur për material me mesataren e teksturës së tij diffuse |
| `structure:<level> trees` | pemë dhe shkurre, fikse dhe të gjeneruara (pyje, gardhe): rrjeta e tyre e renderimit aty ku lejon buxheti, përndryshe një trung dhe një kurorë (një kon për halorët) në ngjyrën e gjetheve të vetë pemës, mbi madhësinë e vërtetë të pemës |

Objektet pa rrjetë renderimi kthehen te forma e tyre e përplasjes; pemët
pa të te kurora. Ngjyrat e kulmeve (`COLOR_0`) mbajnë vlera të koduara sRGB,
që është mënyra si i lexon shikuesi 3DHeat.

**Koordinatat** janë metrat e lojës me z të pasqyruar: glb (x, y, z) = lojë
(x, y, -z). Bota e lojës është me orientim të majtë (x lindje, y lart, z veri); glTF është
me orientim të djathtë. `heat3d-wt-replay` e mban z të lojës dhe i thotë shikuesit ta
pasqyrojë, kështu që një riluajtje dhe niveli i hartës së saj puthiten pa hap
vendosjeje. JSON jep drejtkëndëshin e çdo harte taktike në metra loje
dhe qoshet e saj në hapësirën e glb, për ngarkimin e PNG si imazh harte.

**Detajet.** `--detail low|medium|high` (e paracaktuar medium) vendos, mbi hartën e tankeve:

| | mesi i hartës së tankeve | pjesa tjetër e hartës së tankeve | ngjyra e tokës | buxheti i objekteve | maksimumi i trekëndëshave për objekt | bimë të gjeneruara të mbajtura |
|---|---|---|---|---|---|---|
| low | çdo mostër e 4-t | çdo e 8-ta | 4 m për piksel | 1.2 M | 1,500 | pemë 35 %, shkurre 20 % |
| medium | çdo e 2-ta | çdo e 4-ta | 2 m | 3.5 M | 4,000 | pemë 70 %, shkurre 50 % |
| high | çdo mostër (2 m në shumicën e hartave tokësore) | çdo e 2-ta | 1 m (më së shumti 4096 piksel për anë) | 4.5 M | 12,000 | të gjitha |

Dy unazat e hartës së tankeve mbahen te 0.3 M (low), 1 M (medium) dhe 3.7 M (high)
trekëndësha: në hartat, heightmap i të cilave është më i imët se 2 m, hapat dyfishohen
(unaza e jashtme së pari) derisa të përshtaten, kështu që edhe ato dalin rreth 2 m.

Një hartë tokësore në `high` del rreth 8 milionë trekëndësha (3.5 M tokë,
4.5 M objekte) dhe 250 MB; në `medium` rreth 4.5 M. LOD-et e objekteve janë
ato që loja vetë do t'i vizatonte nga një largësi shikimi, më e shkurtra
që totali i së cilës përshtatet në buxhet: objektet e vogla kalojnë së pari në LOD të trasha dhe ndërtesat
e mëdha të fundit, sipas intervaleve që u dhanë krijuesit e tyre çdo LOD-i (`lodDistance` i JSON);
çfarë kursen ai hap përtej buxhetit kthehet te objektet më të mëdha. Ngjyra e trashë e tokës (hartat ajrore) i mesatarizon teksturat e përsëritura të çdo klase toke deri te madhësia e pikselit
së pari, që pllakat të mos krijojnë moiré. Nëse as LOD-et më të trasha nuk përshtaten, pemët që kursejnë më shumë
bëhen kurora, dhe pastaj llojet më të vogla lihen jashtë (`leftOut`); asnjë objekt
nuk vizatohet si kuti (një formë përplasjeje, nëse ka, është e vetë objektit).
Objektet e gjeneruara rrallohen në mënyrë deterministe sipas llojit (`density`), të njëjtat
në çdo ekzekutim. `--max-object-triangles` e anashkalon buxhetin,
`--max-grid` (e paracaktuar 1024) kufizon pjesët më të trasha të heightmap, `--no-objects`
lë jashtë objektet, `--no-generated` ato të gjeneruarat, `--no-terrain-colour`
teksturon tokën me hartën taktike, `--no-texture` e lë pa teksturë.

`parts.objects` i JSON liston instancat (fikse dhe të gjeneruara, sipas llojit dhe
klasës së tokës), sa u vizatuan në cilin LOD (`drawnAs`), trekëndëshat, largësinë
e LOD dhe sekondat; `parts.heightmap.rings` hapin dhe trekëndëshat e çdo unaze toke;
`parts.terrainColour` klasat e tokës dhe ngjyrat e tyre, rrugët dhe decal-et e tokës;
`trianglesTotal`, `glbBytes` dhe `secondsBy` totalet.

## Çfarë lexohet, dhe sa mirë {#what-is-read-and-how-well}

| Pjesa | Gjendja |
|---|---|
| Binari i nivelit (`levels/<level>.bin`, `DBLD` 3x64): tabela e blloqeve | çdo nivel i kontrolluar |
| Heightmap (`HM2`, versionet 0-2; versioni 2 janë vlera 8-bitëshe në blloqe, copa Oodle ose zstd) | çdo nivel, heightmap i të cilit është version 2 me copa Oodle; kontrolluar me sy ndaj hartave të tyre taktike (lumenjtë, luginat, bregdetet dhe qytetet përputhen) |
| Përplasja e rrjetës së tokës (`lmap`, ray tracer-i i tokës `LTdump`) | lexuar aty ku një nivel e ka (i paketuar me Oodle). Është sipërfaqja e përplasjes së lojës, jo rrjeta e renderuar, kështu që është më e trashë aty ku toka është e sheshtë |
| Ngjyra e tokës (klasat e tokës `lmap` dhe harta e peshave, harta fizike `LMp2`, spline-t `hspl`) | hartat e ngjyrave të klasave të tokës dhe teksturat e detajeve (ngjyrat e tyre mesatare) të peshuara me hartën e peshave, indeksi biome 1 m i klasave të tokës të indeksuara, format e rrugëve dhe decal-eve të tokës të hartës fizike në ngjyrën e teksturës së spline-it ose materialit të tyre, shkëmbinj në pjerrësi të pjerrëta. Kontrolluar ndaj hartave të tankeve: rrugët, qytetet, liqenet, brezat e pyjeve dhe dalja e shkëmbinjve përputhen. Formula e ngjyrës e shaderit të terrenit të vetë War Thunder nuk është në burimin publik; përdoret ajo e publikuar e motorit (daNetGame), që del më e ngopur se harta taktike |
| Niveli i ujit | `water_level` nga BLK e nivelit te `aces.vromfs.bin` (0 aty ku nuk ka) |
| Heightmap i ujit (`WHM`: një rrjetë qelizash të sheshta dhe faqe 130x130 lartësish 16-bitëshe) | lexuar aty ku një nivel e ka; lumenjtë e tij pjerrësohen me tokën |
| Hartat taktike | nga `content/base/res/locations_maps.dxp.bin`, vendosur nga `mapCoord0/1` dhe `tankMapCoord0/1` të BLK; maja e imazhit është veriu |
| Objektet e vendosura (`RIGz`: instancat fikse të gjeneratorit të instancave të renderimit) | çdo instancë, si matricë 3x4 vlerash 16-bitëshe ose, në disa nivele, 32-bitëshe (numri i bajtëve të qelizës vendos); çdo bajt i çdo qelize i llogaritur në nivelet e kontrolluara |
| Objektet e gjeneruara (maskat e klasave të tokës `RIGz` dhe burimet `LandClass`) | gjeneratori i lojës, i portuar: të njëjtat vende të provuara në të njëjtën radhë me të njëjtët numra të rastësishëm, maskat e klasës së tokës dhe të përjashtimit, objekti i zgjedhur në çdo vend, rrotullimi, shkalla dhe zhvendosja e lartësisë; entitete të pllakëzuara (blloqe qyteti) dhe të mbjella (pyje, shkurre, fusha). Të gjeneruara vetëm mbi hartën e tankeve. Të përafërta: lartësia dhe normalja e tokës (nga heightmap; loja gjurmon një rreze), kutitë e përjashtimit që loja regjistron gjatë ekzekutimit, dhe yaw i pemëve (loja e kap te paleta e rrotullimit të impostor) |
| Rrjetat e renderimit (burimet `RendInst` te `content/*/res/*.grp`, materialet te `riDesc.bin`) | kulmet dhe trekëndëshat e çdo LOD (pozicione float; indekse 16 ose 32-bitëshe, të thjeshta ose të paketuara me meshoptimizer), materiali i çdo elementi. Elementet decal dhe impostor-billboard lihen jashtë; ato transparente (xhami) mbahen |
| Ngjyrat e objekteve | për material, mesatarja e mip-it të vogël të teksturës së tij diffuse (e peshuar me alfa për gjethet), nga paketat e teksturave të instalimit: t0 për shumicën e shaderave, diffuse e parë e detajeve aty ku t0 është overlay ose maskë. Një ngjyrë për material: pa teksturë mbi objektet |
| Format e përplasjes (`<object>_collision`) | burimet e përplasjes të stream version 3, të përdorura aty ku një objekt nuk ka rrjetë renderimi. Vizatohet vetëm ajo që godasin rrezet e lojës (nyjet `TRACEABLE`), dhe kutitë, sferat dhe kapsulat vetëm kur burimi nuk ka rrjetë: pjesa tjetër janë zëvendësues fizikë të trashë që do të dukeshin si kuba rreth objektit |
| Rrjeta e navigimit (`Lnav`), rrjeta e renderuar e tokës, bari, `spgz`, `stbl`, `d2co` | nuk lexohen |

Nivelet janë të kompresuara me Oodle, që është pronësor. Loja dërgon një kopje,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (një build i zakonshëm x64), dhe
kjo është ajo që ngarkohet; `HEAT3D_OODLE=<dll or folder>` tregon një tjetër.
Asgjë nga Oodle nuk përfshihet këtu.

## Format, dhe ku dokumentohen {#formats-and-where-they-are-documented}

Gaijin e botoi burimin e Dagor Engine nën licencën BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Lexuesit këtu u shkruan nga ai;
asnjë kod loje nuk u dekompilua. Çdo modul emërton skedarët burim që ndjek:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, një trup zstd, 16 bajtët e parë dhe
  të fundit të të cilit janë XOR me një çelës fiks, një tabelë emrash dhe një tabelë zhvendosjesh:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  dhe BLK binare (format 1-5, me hartën e përbashkët të emrave të arkivit `\xff?nm` dhe
  fjalorin zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: paketat e teksturave `DxP2` (`lib3d/texPackMgr2.cpp`) dhe header-at DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekodohen nga Pillow.
- `dagorlevel.py`: binari i nivelit (`scene/loadLevel.cpp`), heightmap
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  ray tracer-i i tokës (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) dhe heightmap i ujit
  (`fftWater/fftWater.cpp`).
- `rigen.py`: objektet e vendosura (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: objektet e gjeneruara (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: instancat e renderimit (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) dhe kodeku i indekseve të
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: ngjyra e tokës (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paketat e burimeve (`gameRes/grpData.h`) dhe burimet e përplasjes
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  trekëndëshat e të cilave ruhen si BVH katërshe (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) i lexon të njëjtat arkiva; nuk nevojitet dhe nuk përdoret.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
