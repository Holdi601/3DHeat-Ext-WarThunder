---
title: "Nivoi"
nav_order: 9
lang: "bs"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Nivoi (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` pretvara nivoe vaše vlastite War Thunder instalacije u
`.glb` nivoe za preglednik, u istom okviru kao tabele replayeva.

## Korak po korak {#step-by-step}

1. Izlistajte nivoe svoje instalacije: `heat3d-wt-level list`. Ispisuje jedan
   red po nivou: njegovo ime, njegov teren i njegove mape, zatim broj. Na
   primjer (izmišljen nivo):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Izvucite jedan, nekoliko (džokeri su dozvoljeni) ili sve:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Učitajte `levels/<level>/<level>.glb` u panel Pozadina / nivo preglednika, pod
   bitkama te mape.

Nivoi koje napišete ostaju na vašem računaru: nikad ih ne objavljujte (vidi
[Uvjeti i licenca](terms.md)).

## Opcije {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Naredba / opcija | Šta radi |
|---|---|
| `list [--game FOLDER]` | svaki nivo u instalaciji |
| `extract <levels...>` / `--all` | navedeni nivoi (kako ih ispisuje `list`; džokeri su dozvoljeni), ili svaki nivo |
| `-o`, `--out` | izlazni folder; svaki nivo ide u `<out>/<level>/` |
| `--game FOLDER` | War Thunder folder (zadano: pronađen preko Steama ili launchera; također `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | uzorkovanje tla, boja tla i budžet objekata preko tenkovske mape (zadano `medium`) |
| `--max-object-triangles N` | budžet objekata (zadano: onaj za dati detalj) |
| `--max-grid N` | uzoraka visinske mape po strani, po dijelu (zadano 1024) |
| `--no-objects` | izostavi zgrade, drveće i druge postavljene objekte |
| `--no-generated` | izostavi objekte koje generišu klase terena (šume, gradovi) |
| `--no-terrain-colour` | teksturiraj tlo taktičkom mapom, a ne klasama terena |
| `--no-texture` | ostavi tlo bez teksture |
| `--skip-existing` | preskoči nivoe čiji `.glb` postoji |

## Šta se piše {#what-is-written}

Svaki nivo postaje `<out>/<level>/<level>.glb`, `<level>.json` (šta je pročitano,
nivo vode, pravougaonici mapa, brojevi trouglova, vremena) i taktičke mape nivoa
kao `<level>_map.png` (zračna mapa) i `<level>_tankmap.png`;
kopnene mape dobivaju i `<level>_terrain.png`, vlastite boje tla preko
tenkovske mape. Glb se piše u `<level>.glb.part` i preimenuje kada je gotov;
dok se nivo piše, drži se `<out>/<level>/.<level>.lock`, pa dva
izvlačenja nikad ne pišu isti nivo (drugo ispisuje `busy <level>`).
Instalacija se nalazi preko Steama ili zadanih foldera launchera;
`--game <folder>` ili `HEAT3D_WT_GAME` kažu gdje je inače.

| Dio | Šta je to |
|---|---|
| `ground:<level>` | visinska mapa terena (`HM2`) kao mreža; na kopnenim mapama sredina tenkovske mape (pola njene širine) u koraku za `--detail`, obojena klasama terena, ukrasima tla i putevima (`<level>_terrain.png`; taktička mapa gdje se to ne može napraviti); na mapama bez tenkovske mape (zračne mape), cijela visinska mapa u jednom koraku (2048 uzoraka po strani na `high`, inače 1024), obojena klasama terena preko područja zračne mape (4096 piksela po strani, oko 32 m po pikselu preko 131 km; taktička mapa gdje se to ne može napraviti); na nivoima bez visinske mape, mesh tla |
| `ground:<level> tank map` | ostatak tenkovske mape, korak grublji |
| `ground:<level> heightmap surroundings` | ostatak visinske mape, još grublje |
| `ground:<level> land mesh` | kolizijski trouglovi mesha tla tamo gdje visinska mapa ne dopire (okolina tenkovske mape, do desetina kilometara); na nivoima bez visinske mape to je tlo, obojeno kao gore |
| `ground:<level> outside the map` | tlo koje slika ne pokriva, bez teksture |
| `water:<level>` | jedan ravan pravougaonik na `water_level` nivoa preko svog terena: igra crta vodu kao jednu ravan, a nisko tlo ispod nje je morsko, jezersko ili riječno dno |
| `water:<level> rivers` | na nivoima s visinskom mapom vode (`WHM`), nagnuta površina vode preko ćelija koje pokriva |
| `structure:<level> buildings` | svaki postavljeni objekt koji nije biljka: kuće, ruševine, zidovi, ograde, mostovi, šine, stijene, rekviziti. Fiksni (`RIGz`) i, preko tenkovske mape, oni koje generišu klase terena (gradski blokovi, kamenje). Svaki se crta svojim render meshom (zidovi, krovovi, otvori prozora, grede), na LOD-u koji dozvoljava budžet trouglova, obojen po materijalu prosjekom njegove difuzne teksture |
| `structure:<level> trees` | drveće i grmlje, fiksno i generisano (šume, živice): njihov render mesh gdje budžet dozvoljava, inače deblo i krošnja (čunj za četinare) u boji lišća tog drveta, preko stvarne veličine drveta |

Objekti bez render mesha vraćaju se na svoj oblik kolizije; drveće bez njega
na krošnju. Boje vrhova (`COLOR_0`) sadrže sRGB-kodirane vrijednosti,
što je način na koji ih čita 3DHeat preglednik.

**Koordinate** su metri igre sa zrcaljenim z: glb (x, y, z) = igra
(x, y, -z). Svijet igre je lijevosmjeran (x istok, y gore, z sjever); glTF je
desnosmjeran. `heat3d-wt-replay` zadržava z igre i govori pregledniku da ga
zrcali, pa replay i nivo njegove mape leže jedan na drugom bez
koraka postavljanja. JSON daje pravougaonik svake taktičke mape u metrima igre
i njene uglove u prostoru glb-a, za učitavanje PNG-a kao slike mape.

**Detalj.** `--detail low|medium|high` (zadano medium) određuje, preko tenkovske mape:

| | sredina tenkovske mape | ostatak tenkovske mape | boja tla | budžet objekata | najviše trouglova po objektu | zadržane generisane biljke |
|---|---|---|---|---|---|---|
| low | svaki 4. uzorak | svaki 8. | 4 m po pikselu | 1,2 M | 1.500 | drveće 35 %, grmlje 20 % |
| medium | svaki 2. | svaki 4. | 2 m | 3,5 M | 4.000 | drveće 70 %, grmlje 50 % |
| high | svaki uzorak (2 m na većini kopnenih mapa) | svaki 2. | 1 m (najviše 4096 piksela po strani) | 4,5 M | 12.000 | sve |

Dva prstena tenkovske mape drže se na 0,3 M (low), 1 M (medium) i 3,7 M (high)
trouglova: na mapama čija je visinska mapa finija od 2 m, koraci se udvostručuju
(prvo vanjski prsten) dok ne stanu, pa i one ispadnu otprilike na 2 m.

Kopnena mapa na `high` ispadne oko 8 miliona trouglova (3,5 M tla, 4,5 M
objekata) i 250 MB; na `medium` oko 4,5 M. LOD-ovi objekata su
oni koje bi igra sama crtala s jedne udaljenosti gledanja, najkraća
čiji zbir staje u budžet: mali rekviziti prvi padaju na grube LOD-ove, a velike
zgrade zadnje, prema rasponima koje su njihovi autori dali svakom LOD-u (`lodDistance` u JSON-u);
ono što taj korak uštedi preko budžeta vraća se najvećim
objektima. Gruba boja tla (zračne mape) prvo svodi prosjek tiled tekstura svake klase terena
na veličinu piksela, da se pločice ne preklope u moire. Ako ni najgrublji LOD-ovi ne stanu, drveće koje
najviše uštedi postaje krošnje, a zatim se izostavljaju najmanji tipovi (`leftOut`); nijedan objekt se
ne crta kao kutija (oblik kolizije, ako postoji, je vlastiti oblik objekta).
Generisani objekti se prorjeđuju deterministički po vrsti (`density`), isti
pri svakom pokretanju. `--max-object-triangles` zamjenjuje budžet,
`--max-grid` (zadano 1024) ograničava grublje dijelove visinske mape, `--no-objects`
izostavlja objekte, `--no-generated` generisane, `--no-terrain-colour`
teksturira tlo taktičkom mapom, `--no-texture` ostavlja ga bez teksture.

`parts.objects` u JSON-u navodi instance (fiksne i generisane, po vrsti i
klasi terena), koliko ih je nacrtano na kojem LOD-u (`drawnAs`), trouglove, udaljenost
LOD-a i sekunde; `parts.heightmap.rings` korak i trouglove svakog prstena tla; `parts.terrainColour` klase terena i njihove boje, puteve
i ukrase tla; `trianglesTotal`, `glbBytes` i `secondsBy` ukupne vrijednosti.

## Šta se čita i koliko dobro {#what-is-read-and-how-well}

| Dio | Status |
|---|---|
| Binarni nivo (`levels/<level>.bin`, `DBLD` 3x64): tabela blokova | svaki nivo provjeren |
| Visinska mapa (`HM2`, verzije 0-2; verzija 2 su 8-bitne vrijednosti u blokovima, Oodle ili zstd dijelovi) | svaki nivo čija je visinska mapa verzije 2 s Oodle dijelovima; provjereno okom prema njihovim taktičkim mapama (rijeke, doline, obale i gradovi se poklapaju) |
| Kolizija mesha tla (`lmap`, njegov `LTdump` land ray tracer) | čita se gdje nivo ima jedan (pakiran Oodleom). To je kolizijska površina igre, ne renderirani mesh, pa je grublja gdje je tlo ravno |
| Boja tla (`lmap` klase terena i mapa težina, `LMp2` fizička mapa, `hspl` splineovi) | mape boja klasa terena i detaljne teksture (njihove prosječne boje) ponderirane mapom težina, 1 m indeks biom-a indeksiranih klasa terena, oblici puteva i ukrasa tla iz fizičke mape u boji teksture njihovog splinea ili materijala, litice na strmim nagibima. Provjereno prema tenkovskim mapama: putevi, gradovi, jezera, šumski pojasevi i stjenoviti izdanci se poklapaju. Formula boje vlastitog shadera terena War Thundera nije u javnom izvoru; koristi se objavljena formula engine-a (daNetGame), koja ispada zasićenija od taktičke mape |
| Nivo vode | `water_level` iz BLK-a nivoa u `aces.vromfs.bin` (0 gdje ga nema) |
| Visinska mapa vode (`WHM`: mreža ravnih ćelija i stranice 130x130 16-bitnih visina) | čita se gdje je nivo ima; njene rijeke prate nagib tla |
| Taktičke mape | iz `content/base/res/locations_maps.dxp.bin`, postavljene prema `mapCoord0/1` i `tankMapCoord0/1` iz BLK-a; vrh slike je sjever |
| Postavljeni objekti (`RIGz`: fiksne instance generatora render instanci) | svaka instanca, kao matrica 3x4 16-bitnih vrijednosti ili, na nekim nivoima, 32-bitnih (odlučuje broj bajtova ćelije); svaki bajt svake ćelije obračunat na provjerenim nivoima |
| Generisani objekti (`RIGz` maske klasa terena i `LandClass` resursi) | generator igre, portiran: ista mjesta isprobana istim redoslijedom istim slučajnim brojevima, maske klasa terena i isključenja, objekt odabran na svakom mjestu, njegova rotacija, skala i pomak visine; tiled (gradski blokovi) i zasađeni (šume, grmlje, polja) entiteti. Generiše se samo preko tenkovske mape. Aproksimirano: visina i normala tla (iz visinske mape; igra prati zraku), kutije isključenja koje igra registruje za vrijeme rada i yaw drveća (igra ga lijepi na paletu rotacija impostora). |
| Render meshevi (`RendInst` resursi u `content/*/res/*.grp`, materijali u `riDesc.bin`) | vrhovi i trouglovi svakog LOD-a (float pozicije; 16 ili 32-bitni indeksi, obični ili pakirani meshoptimizerom), materijal svakog elementa. Elementi decal-a i impostor-billboarda su izostavljeni; prozirni (staklo) se zadržavaju |
| Boje objekata | po materijalu, prosjek malog mip-a njegove difuzne teksture (ponderiran alfom za lišće), iz paketa tekstura instalacije: t0 za većinu shadera, prva detaljna difuzna gdje je t0 overlay ili maska. Jedna boja po materijalu: nema teksture na objektima |
| Oblici kolizije (`<object>_collision`) | resursi kolizije verzije toka 3, koriste se gdje objekt nema render mesh. Crta se samo ono što zrake igre pogađaju (`TRACEABLE` čvorovi), a kutije, kugle i kapsule samo kada resurs nema mesh: ostalo su grube fizičke zamjene koje bi se pokazale kao kocke oko objekta |
| Navigacijski mesh (`Lnav`), renderirani mesh tla, trava, `spgz`, `stbl`, `d2co` | ne čita se |

Nivoi su komprimirani Oodleom, koji je vlasnički. Igra isporučuje kopiju,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (običan x64 build), i
to se učitava; `HEAT3D_OODLE=<dll or folder>` pokazuje na drugu.
Ništa od Oodlea nije ovdje uključeno.

## Formati i gdje su dokumentirani {#formats-and-where-they-are-documented}

Gaijin je objavio izvor Dagor Enginea pod licencom BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Ovdašnji čitači su pisani prema
njemu; nikakav kod igre nije dekompajliran. Svaki modul imenuje izvorne datoteke koje slijedi:

- `vromfs.py`: `*.vromfs.bin` (zaglavlje `VRFs`/`VRFx`, zstd tijelo čijih su prvih i
  zadnjih 16 bajtova XOR-ovano fiksnim ključem, tabela imena i tabela pomaka:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  i binarni BLK (oblici 1-5, sa zajedničkom mapom imena arhive `\xff?nm` i
  zstd rječnikom: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: paketi tekstura `DxP2` (`lib3d/texPackMgr2.cpp`) i DDSx zaglavlja
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekodira Pillow.
- `dagorlevel.py`: binarni nivo (`scene/loadLevel.cpp`), visinska mapa
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  land ray tracer (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) i visinska mapa vode
  (`fftWater/fftWater.cpp`).
- `rigen.py`: postavljeni objekti (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generisani objekti (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: render instance (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) i meshoptimizerov
  kodek indeksa (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: boja tla (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paketi resursa (`gameRes/grpData.h`) i resursi kolizije
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  čiji su trouglovi pohranjeni kao quad BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) čita iste arhive; nije potreban i ne koristi se.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
