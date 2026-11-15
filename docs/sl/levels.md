---
title: Zemljevidi (heat3d-wt-level)
nav_order: 9
lang: sl
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Zemljevidi (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` pretvori zemljevide vaše lastne namestitve War Thunder v `.glb` zemljevide za pregledovalnik, v istem
okviru kot tabele posnetkov.

## Korak za korakom {#step-by-step}

1. Izpišite zemljevide vaše namestitve: `heat3d-wt-level list`. Izpiše eno vrstico za vsak zemljevid: njegovo ime, teren
   in njegove karte, nato število. Na primer (izmišljen zemljevid):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Izvlecite enega, več (dovoljeni so nadomestni znaki) ali vse:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Naložite `levels/<level>/<level>.glb` na plošči Ozadje / nivo pregledovalnika, pod bitkami tega zemljevida.

Zemljevidi, ki jih zapišete, ostanejo na vašem računalniku: nikoli jih ne objavljajte (glejte
[Pogoji in licenca](terms.md)).

## Možnosti {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Ukaz / možnost | Kaj počne |
|---|---|
| `list [--game FOLDER]` | vsak zemljevid v namestitvi |
| `extract <levels...>` / `--all` | navedeni zemljevidi (kot jih izpiše `list`; dovoljeni so nadomestni znaki) ali vsi zemljevidi |
| `-o`, `--out` | izhodna mapa; vsak zemljevid gre v `<out>/<level>/` |
| `--game FOLDER` | mapa War Thunder (privzeto: najdena prek Steam ali zaganjalnika; tudi `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | vzorčenje tal, barva tal in proračun predmetov čez tankovski zemljevid (privzeto `medium`) |
| `--max-object-triangles N` | proračun predmetov (privzeto: tisti za podrobnost) |
| `--max-grid N` | vzorci višinske karte na stran, na del (privzeto 1024) |
| `--no-objects` | izpusti stavbe, drevesa in druge postavljene predmete |
| `--no-generated` | izpusti predmete, ki jih ustvarjajo razredi zemljišča (gozdovi, mesta) |
| `--no-terrain-colour` | teksturiraj tla s taktično karto, ne z razredi zemljišča |
| `--no-texture` | pusti tla brez teksture |
| `--skip-existing` | pusti zemljevide, katerih `.glb` obstaja |

## Kaj se zapiše {#what-is-written}

Vsak zemljevid postane `<out>/<level>/<level>.glb`, `<level>.json` (kaj je bilo prebrano, višina vode, pravokotniki kart,
števila trikotnikov, časi) in taktični zemljevidi ravni kot `<level>_map.png` (zračna karta) in `<level>_tankmap.png`;
kopenske karte dobijo tudi `<level>_terrain.png`, lastne barve tal čez tankovsko karto. Glb se zapiše v `<level>.glb.part`
in preimenuje, ko je končan; med zapisovanjem zemljevida je zaklenjen `<out>/<level>/.<level>.lock`, zato dva izvlečka
nikoli ne zapisujeta istega zemljevida (drugi izpiše `busy <level>`). Namestitev se najde prek Steam ali privzetih map
zaganjalnika; `--game <folder>` ali `HEAT3D_WT_GAME` povesta, kje je sicer.

| Del | Kaj je |
|---|---|
| `ground:<level>` | višinska karta terena (`HM2`) kot mreža; na kopenskih zemljevidih sredina tankovske karte (polovica njene širine) pri koraku `--detail`, obarvana z razredi zemljišča, kopenskimi nalepkami in cestami (`<level>_terrain.png`; taktična karta, kjer tega ni mogoče narediti); na zemljevidih brez tankovske karte (zračnih zemljevidih) celotna višinska karta pri enem koraku (2048 vzorcev na stran pri `high`, sicer 1024), obarvana z razredi zemljišča čez območje zračne karte (4096 slikovnih pik na stran, približno 32 m na slikovno piko čez 131 km; taktična karta, kjer tega ni mogoče narediti); na zemljevidih brez višinske karte mreža zemljišča |
| `ground:<level> tank map` | preostanek tankovske karte, en korak bolj grob |
| `ground:<level> heightmap surroundings` | preostanek višinske karte, še bolj grob |
| `ground:<level> land mesh` | trikotniki trkov mreže zemljišča tam, kjer višinska karta ne sega (okolica tankovske karte, do desetin kilometrov); na zemljevidih brez višinske karte je to tla, obarvana kot zgoraj |
| `ground:<level> outside the map` | tla, ki jih slika ne pokriva, brez teksture |
| `water:<level>` | en ploščat pravokotnik na `water_level` zemljevida čez ves teren: igra voda riše kot eno ravnino, nizka tla pod njo pa so morje, jezero ali strugo reke |
| `water:<level> rivers` | na zemljevidih z vodno višinsko karto (`WHM`) nagnjena vodna gladina čez celice, ki jih pokriva |
| `structure:<level> buildings` | vsak postavljen predmet, ki ni rastlina: hiše, ruševine, zidovi, ograje, mostovi, tiri, skale, rekviziti. Fiksni (`RIGz`) in, čez tankovsko karto, tisti, ki jih ustvarjajo razredi zemljišča (mestni bloki, kamni). Vsak je narisan s svojo mrežo upodabljanja (stene, strehe, odprtine oken, nosilci), na stopnji LOD, ki jo dovoli proračun trikotnikov, obarvan po materialu s povprečjem njegove difuzne teksture |
| `structure:<level> trees` | drevesa in grmovje, fiksni in ustvarjeni (gozdovi, žive meje): njihova mreža upodabljanja, kjer proračun dovoli, sicer deblo in krošnja (stožec za iglavce) v lastni barvi listja drevesa, v njegovi pravi velikosti |

Predmeti brez mreže upodabljanja se vrnejo na svojo obliko trkov; drevesa brez nje na krošnjo. Barvne vrednosti vozlišč
(`COLOR_0`) hranijo vrednosti, kodirane v sRGB, kar je tisto, kar pregledovalnik 3DHeat bere.

**Koordinate** so igrini metri z zrcaljenim z: glb (x, y, z) = igra (x, y, -z). Svet igre je levosučen (x vzhod, y gor, z
sever); glTF je desnosučen. `heat3d-wt-replay` ohrani z igre in pregledovalniku pove, naj ga zrcali, zato se posnetek in
zemljevid njegove karte položita drug na drugega brez koraka namestitve. JSON v igrinih metrih poda pravokotnik vsake
taktične karte in njene vogale v prostoru glb, za nalaganje PNG kot slike karte.

**Podrobnost.** `--detail low|medium|high` (privzeto medium) nastavi čez tankovsko karto:

| | sredina tankovske karte | preostanek tankovske karte | barva tal | proračun predmetov | največ trikotnikov na predmet | ohranjene ustvarjene rastline |
|---|---|---|---|---|---|---|
| low | vsak 4. vzorec | vsak 8. | 4 m na piko | 1,2 M | 1.500 | drevesa 35 %, grmovje 20 % |
| medium | vsak 2. | vsak 4. | 2 m | 3,5 M | 4.000 | drevesa 70 %, grmovje 50 % |
| high | vsak vzorec (na večini kopenskih zemljevidov 2 m) | vsak 2. | 1 m (največ 4096 slikovnih pik na stran) | 4,5 M | 12.000 | vse |

Dva obroča tankovske karte sta zadržana na 0,3 M (low), 1 M (medium) in 3,7 M (high) trikotnikov: na zemljevidih, katerih
višinska karta je finejša od 2 m, se koraki podvojijo (najprej zunanji obroč), dokler se ne prilegajo, zato pridejo tudi
ti ven približno pri 2 m.

Kopenski zemljevid pri `high` pride na približno 8 milijonov trikotnikov (3,5 M tal, 4,5 M predmetov) in 250 MB; pri
`medium` na približno 4,5 M. LOD-i predmetov so tisti, ki bi jih igra sama narisala z ene same razdalje gledanja, najkrajši,
katerega skupna vsota se prilega proračunu: majhni rekviziti najprej padejo na grobe LOD-e, velike stavbe nazadnje, po
razdaljah, ki so jih navedli njihovi ustvarjalci za vsak LOD (`lodDistance` v JSON-u); kar ta korak prihrani čez proračun,
se vrne največjim predmetom. Groba barva tal (zračni zemljevidi) najprej povpreči popločene teksture vsakega razreda
zemljišča na velikost slikovne pike, da se ploščice ne prekrivajo v moiré. Če se tudi najgrobejši LOD-i ne prilegajo,
drevesa, ki prihranijo največ, postanejo krošnje, nato pa se izpustijo najmanjše vrste (`leftOut`); noben predmet ni
narisan kot škatla (oblika trkov, če obstaja, je lastna oblika predmeta).
Ustvarjeni predmeti se po vrsti redčijo determinirano (`density`), vedno isti pri vsakem zagonu.
`--max-object-triangles` prepiše proračun, `--max-grid` (privzeto 1024) omeji grobe dele višinske karte, `--no-objects`
izpusti predmete, `--no-generated` ustvarjene, `--no-terrain-colour` teksturira tla s taktično karto, `--no-texture` pa
pusti tla brez teksture.

`parts.objects` v JSON-u navaja primerke (fiksne in ustvarjene, po vrsti in razredu zemljišča), koliko jih je bilo narisanih
na katerem LOD-u (`drawnAs`), trikotnike, razdaljo LOD-a in sekunde; `parts.heightmap.rings` korak in trikotnike vsakega
obroča tal; `parts.terrainColour` razrede zemljišča in njihove barve, ceste in kopenske nalepke; `trianglesTotal`,
`glbBytes` in `secondsBy` skupne vrednosti.

## Kaj se bere in kako dobro {#what-is-read-and-how-well}

| Del | Stanje |
|---|---|
| Binarnik ravni (`levels/<level>.bin`, `DBLD` 3x64): tabela blokov | preverjeno za vsak zemljevid |
| Višinska karta (`HM2`, različice 0-2; različica 2 so 8-bitne vrednosti v blokih, Oodle ali zstd kosi) | vsak zemljevid, katerega višinska karta je različice 2 z Oodle kosi; preverjeno z očesom glede na njegove taktične karte (reke, doline, obale in mesta se ujemajo) |
| Trki mreže zemljišča (`lmap`, njen `LTdump` sledilnik žarkov za zemljišče) | prebrano, kjer ga zemljevid ima (zapakirano z Oodle). Je površina trkov igre, ne upodobljena mreža, zato je na ravnih tleh grobejša |
| Barva tal (`lmap` razredi zemljišča in mapa uteži, `LMp2` fizikalna karta, `hspl` krivulje) | barvne karte razredov zemljišča in teksture podrobnosti (njihove povprečne barve), uteženo z mapo uteži, indeks bioma 1 m za indeksirane razrede zemljišča, oblike cest in kopenskih nalepk fizikalne karte v barvi teksture njihove krivulje ali materiala, klife na strmih pobočjih. Preverjeno s tankovskimi kartami: ceste, mesta, jezera, gozdni pasovi in kamnite izdanke se ujemajo. Formula barve terenskega senčilnika War Thunder ni v javni izvorni kodi; uporabljena je objavljena formula mehanike (daNetGame), ki je bolj nasičena kot taktična karta |
| Višina vode | `water_level` iz BLK zemljevida v `aces.vromfs.bin` (0, kjer ga ni) |
| Vodna višinska karta (`WHM`: mreža ploskih celic in strani 130x130 16-bitnih višin) | prebrano, kjer ga zemljevid ima; njene reke se nagibajo z zemljo |
| Taktične karte | iz `content/base/res/locations_maps.dxp.bin`, postavljene z `mapCoord0/1` in `tankMapCoord0/1` iz BLK; vrh slike je sever |
| Postavljeni predmeti (`RIGz`: fiksni primerki generatorja primerkov upodabljanja) | vsak primerek kot matrika 3x4 16-bitnih vrednosti ali na nekaterih zemljevidih 32-bitnih (število bajtov celice odloči); vsak bajt vsake celice je upoštevan na preverjenih zemljevidih |
| Ustvarjeni predmeti (`RIGz` maske razredov zemljišča in viri `LandClass`) | generator igre, prenesen: ista mesta, preizkušena v istem vrstnem redu z istimi naključnimi števili, maske razredov zemljišča in izključitev, predmet, izbran na vsakem mestu, njegova rotacija, merilo in odmik višine; entitete, popločene (mestni bloki) in zasajene (gozdovi, grmovje, polja). Ustvarjeno samo čez tankovsko karto. Približno: višina tal in normala (iz višinske karte; igra sledi žarku), škatle izključitev, ki jih igra registrira med izvajanjem, in smer drevesa (igra jo prilepi na paleto rotacij impostorja). |
| Mreže upodabljanja (viri `RendInst` v `content/*/res/*.grp`, materiali v `riDesc.bin`) | oglišča in trikotniki vsakega LOD-a (položaji s plavajočo vejico; indeksi 16 ali 32-bitni, navadni ali stisnjeni z meshoptimizer), material vsakega elementa. Elementi nalepk in impostor-oglasnih plošč so izpuščeni; prosojni (steklo) ostanejo |
| Barve predmetov | za material, povprečje majhnega mipa njegove difuzne teksture (utežene z alfo za liste), iz paketov tekstur namestitve: t0 za večino senčilnikov, prva difuzna podrobnost, kjer je t0 prekrivna ali maska. Ena barva na material: brez teksture na predmetih |
| Oblike trkov (`<object>_collision`) | viri trkov različice toka 3, uporabljeni tam, kjer predmet nima mreže upodabljanja. Narisano je samo to, kar igrini žarki zadenejo (vozlišča `TRACEABLE`), škatle, krogle in kapsule pa samo, kadar vir nima mreže: ostalo so grobi fizikalni nadomestki, ki bi se pokazali kot kocke okoli predmeta |
| Navigacijska mreža (`Lnav`), upodobljena mreža zemljišča, trava, `spgz`, `stbl`, `d2co` | niso prebrani |

Zemljevidi so stisnjeni z Oodle, ki je lastniški. Igra prinaša kopijo, `<War Thunder>\win-arm64ec\oo2core_9_win64.dll`
(običajna gradnja x64), in ta se naloži; `HEAT3D_OODLE=<dll ali mapa>` kaže na drugo. Tukaj ni vključen noben del Oodle.

## Formati in kje so dokumentirani {#formats-and-where-they-are-documented}

Gaijin je objavil izvorno kodo Dagor Engine pod licenco BSD 3-Clause (github.com/GaijinEntertainment/DagorEngine). Bralniki
tukaj so bili napisani po njej; nobena koda igre ni bila dekompilirana. Vsak modul navaja izvorne datoteke, ki jim sledi:

- `vromfs.py`: `*.vromfs.bin` (glava `VRFs`/`VRFx`, telo zstd, katerega prvih in zadnjih 16 bajtov je XOR-anih z
  določenim ključem, tabela imen in tabela zamikov: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) in binarni BLK (oblike 1-5, z deljeno tabelo imen arhiva `\xff?nm` in dictionary zstd:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: paketi tekstur `DxP2` (`lib3d/texPackMgr2.cpp`) in glave DDSx (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7
  dekodira Pillow.
- `dagorlevel.py`: binarnik ravni (`scene/loadLevel.cpp`), višinska karta (`heightmap/heightmapPhysHandler.cpp`,
  `heightMapLand/compressedHeightmap.cpp`), sledilnik žarkov za zemljišče (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) in vodna višinska karta (`fftWater/fftWater.cpp`).
- `rigen.py`: postavljeni predmeti (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: ustvarjeni predmeti (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`,
  `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`,
  `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: primerki upodabljanja (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) in kodek indeksov meshoptimizer
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: barva tal (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paketi virov (`gameRes/grpData.h`) in viri trkov (`sharedInclude/gameRes/collResStream.h`,
  `gameRes/collisionGameResLoad.cpp`), katerih trikotniki so shranjeni kot četverokotni BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) bere iste arhive; ni potreben in se ne uporablja.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
