---
title: Razine
nav_order: 9
lang: "hr"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Razine (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` pretvara razine tvoje vlastite instalacije War Thundera u `.glb` razine za preglednik, u
istom okviru kao tablice snimki.

## Korak po korak {#step-by-step}

1. Popiši razine svoje instalacije: `heat3d-wt-level list`. Ispisuje jedan redak po razini: naziv, njezin teren
   i njezine karte, zatim broj. Na primjer (izmišljena razina):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Izvuci jednu, nekoliko (zamjenski znakovi dopušteni) ili sve:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Učitaj `levels/<level>/<level>.glb` u panel Pozadina / razina preglednika, pod bitkama te karte.

Razine koje zapišeš ostaju na tvom računalu: nikad ih ne objavljuj (vidi
[Pojmovi i licenca](terms.md)).

## Opcije {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Naredba / opcija | Radi |
|---|---|
| `list [--game MAPA]` | svaka razina u instalaciji |
| `extract <levels...>` / `--all` | navedene razine (kako ih ispisuje `list`; zamjenski znakovi dopušteni), ili svaka razina |
| `-o`, `--out` | izlazna mapa; svaka razina ide u `<out>/<level>/` |
| `--game MAPA` | mapa War Thundera (zadano: pronađeno preko Steama ili launchera; također `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | uzorkovanje tla, boja tla i proračun objekata nad kartom tenkova (zadano `medium`) |
| `--max-object-triangles N` | proračun objekata (zadano: onaj od detalja) |
| `--max-grid N` | uzorci visinske karte po strani, po dijelu (zadano 1024) |
| `--no-objects` | izostavi zgrade, drveće i druge postavljene objekte |
| `--no-generated` | izostavi objekte koje generiraju klase zemljišta (šume, gradovi) |
| `--no-terrain-colour` | teksturiraj tlo taktičkom kartom, ne klasama zemljišta |
| `--no-texture` | ostavi tlo bez teksture |
| `--skip-existing` | preskoči razine čiji `.glb` postoji |

## Što se zapisuje {#what-is-written}

Svaka razina postaje `<out>/<level>/<level>.glb`, `<level>.json` (što je pročitano, razina vode, pravokutnici
karata, broj trokuta, vremena) i taktičke karte razine kao `<level>_map.png` (zračna karta) i
`<level>_tankmap.png`; kopnene karte dobivaju i `<level>_terrain.png`, vlastite boje tla preko karte tenkova.
Glb se piše u `<level>.glb.part` i preimenuje kad je gotov; dok se razina piše, drži se
`<out>/<level>/.<level>.lock`, pa dva izvlačenja nikad ne pišu istu razinu (drugo ispiše `busy <level>`).
Instalacija se traži preko Steama ili zadanih mapa launchera; `--game <mapa>` ili `HEAT3D_WT_GAME` govore gdje
je inače.

| Dio | Što je |
|---|---|
| `ground:<level>` | visinska karta terena (`HM2`) kao mreža; na kopnenim kartama središte karte tenkova (polovica njezine širine) na koraku `--detail`, obojano klasama zemljišta, dekalima tla i cestama (`<level>_terrain.png`; taktička karta tamo gdje to nije moguće); na kartama bez karte tenkova (zračne karte) cijela visinska karta na jednom koraku (2048 uzoraka po strani na `high`, inače 1024), obojana klasama zemljišta preko područja zračne karte (4096 piksela po strani, oko 32 m po pikselu preko 131 km; taktička karta tamo gdje to nije moguće); na razinama bez visinske karte, mreža zemljišta |
| `ground:<level> tank map` | ostatak karte tenkova, jedan korak grublje |
| `ground:<level> heightmap surroundings` | ostatak visinske karte, još grublje |
| `ground:<level> land mesh` | sudarni trokuti mreže zemljišta tamo gdje visinska karta ne dopire (okolina karte tenkova, do desetaka kilometara); na razinama bez visinske karte to je tlo, obojano kao gore |
| `ground:<level> outside the map` | tlo koje slika ne pokriva, bez teksture |
| `water:<level>` | jedan ravan pravokutnik na `water_level` razine preko svega terena: igra vodu crta kao jednu ravninu, a nisko tlo ispod nje je more, jezero ili korito rijeke |
| `water:<level> rivers` | na razinama s vodenom visinskom kartom (`WHM`), nagnuta vodena površina nad ćelijama koje pokriva |
| `structure:<level> buildings` | svaki postavljeni objekt koji nije biljka: kuće, ruševine, zidovi, ograde, mostovi, tračnice, stijene, rekviziti. Fiksni (`RIGz`) i, nad kartom tenkova, oni koje generiraju klase zemljišta (gradski blokovi, kamenje). Svaki se crta svojom mrežom za prikaz (zidovi, krovovi, otvori prozora, grede), na LOD-u koji dopušta proračun trokuta, obojan po materijalu prosjekom njegove difuzne teksture |
| `structure:<level> trees` | drveće i grmlje, fiksni i generirani (šume, živice): njihova mreža za prikaz tamo gdje proračun dopušta, inače deblo i krošnja (stožac za četinjače) u vlastitoj boji lišća, u stvarnoj veličini |

Objekti bez mreže za prikaz vraćaju se na svoj sudarni oblik; drveće bez nje na krošnju. Boje vrhova (`COLOR_0`)
drže vrijednosti kodirane sRGB-om, kako ih preglednik 3DHeat čita.

**Koordinate** su metri igre sa zrcaljenim z: glb (x, y, z) = igra (x, y, -z). Svijet igre je lijevoruk (x istok, y
gore, z sjever); glTF je desnoruk. `heat3d-wt-replay` zadržava z igre i govori pregledniku da ga zrcali, pa snimka
i razina njezine karte padaju jedna na drugu bez koraka postavljanja. JSON daje pravokutnik svake taktičke karte
u metrima igre i njezine kutove u prostoru glb-a, za učitavanje PNG-a kao slike karte.

**Detalj.** `--detail low|medium|high` (zadano medium) postavlja, nad kartom tenkova:

| | središte karte tenkova | ostatak karte tenkova | boja tla | proračun objekata | najviše trokuta po objektu | zadržane generirane biljke |
|---|---|---|---|---|---|---|
| low | svaki 4. uzorak | svaki 8. | 4 m po pikselu | 1,2 M | 1.500 | drveće 35 %, grmlje 20 % |
| medium | svaki 2. | svaki 4. | 2 m | 3,5 M | 4.000 | drveće 70 %, grmlje 50 % |
| high | svaki uzorak (2 m na većini kopnenih karata) | svaki 2. | 1 m (najviše 4096 piksela po strani) | 4,5 M | 12.000 | sve |

Dva prstena karte tenkova ograničena su na 0,3 M (low), 1 M (medium) i 3,7 M (high) trokuta: na kartama čija je
visinska karta finija od 2 m, koraci se udvostručuju (prvo vanjski prsten) dok ne stanu, pa i oni izlaze na oko
2 m.

Kopnena karta na `high` izlazi na oko 8 milijuna trokuta (3,5 M tla, 4,5 M objekata) i 250 MB; na `medium` na
oko 4,5 M. LOD-ovi objekata su oni koje bi sama igra crtala s jedne udaljenosti gledanja, najkraći čiji zbroj
stane u proračun: mali rekviziti prvi prelaze na grube LOD-ove, a velike zgrade zadnje, prema rasponima koje su
im dali njihovi autori za svaki LOD (`lodDistance` u JSON-u); ono što taj korak uštedi preko proračuna vraća se
najvećim objektima. Gruba boja tla (zračne karte) prvo usrednjuje popločane teksture svake klase zemljišta na
veličinu piksela, da se pločice ne pretapaju u moire. Ako ni najgrublji LOD-ovi ne stanu, drveće koje štedi
najviše postaje krošnjama, pa se najmanje vrste izostavljaju (`leftOut`); nijedan objekt se ne crta kao kutija
(sudarni oblik, ako postoji, je vlastiti oblik objekta).
Generirani objekti se prorjeđuju deterministički po vrsti (`density`), isti svaki put. `--max-object-triangles`
nadjačava proračun, `--max-grid` (zadano 1024) ograničava grublje dijelove visinske karte, `--no-objects`
izostavlja objekte, `--no-generated` generirane, `--no-terrain-colour` tlo teksturira taktičkom kartom,
`--no-texture` ga ostavlja bez teksture.

`parts.objects` u JSON-u navodi instance (fiksne i generirane, po vrsti i klasi zemljišta), koliko ih je nacrtano
na kojem LOD-u (`drawnAs`), trokute, LOD udaljenost i sekunde; `parts.heightmap.rings` korak i trokute svakog
kopnenog prstena; `parts.terrainColour` klase zemljišta i njihove boje, ceste i dekale tla; `trianglesTotal`,
`glbBytes` i `secondsBy` ukupne vrijednosti.

## Što se čita, i koliko dobro {#what-is-read-and-how-well}

| Dio | Status |
|---|---|
| Binarna razina (`levels/<level>.bin`, `DBLD` 3x64): tablica blokova | svaka razina provjerena |
| Visinska karta (`HM2`, verzije 0-2; verzija 2 su 8-bitne vrijednosti u blokovima, Oodle ili zstd dijelovi) | svaka razina čija je visinska karta verzije 2 s Oodle dijelovima; provjereno okom prema njihovim taktičkim kartama (rijeke, doline, obale i gradovi se poklapaju) |
| Sudarna mreža zemljišta (`lmap`, njegov `LTdump` praćenik zraka za zemljište) | čita se tamo gdje razina ima jednu (spakiranu Oodleom). To je igrina sudarna površina, a ne crtana mreža, pa je grublja tamo gdje je zemljište ravno |
| Boja tla (`lmap` klase zemljišta i karta težina, `LMp2` fizička karta, `hspl` splajnovi) | karte boja klasa zemljišta i detalj teksture (njihove prosječne boje) ponderirane kartom težina, 1 m biomski indeks indeksiranih klasa zemljišta, oblici cesta i dekala tla iz fizičke karte u boji teksture njihova splajna ili materijala, litice na strmim padinama. Provjereno prema kartama tenkova: ceste, gradovi, jezera, pojasevi šuma i izdanci stijena se poklapaju. Formula boje War Thunderova vlastitog shadera terena nije u javnom izvornom kodu; koristi se objavljena Enginova (daNetGame), koja izlazi zasićenija od taktičke karte |
| Razina vode | `water_level` iz BLK-a razine u `aces.vromfs.bin` (0 ondje gdje nema) |
| Vodena visinska karta (`WHM`: mreža ravnih ćelija i stranica 130x130 visina od 16 bitova) | čita se tamo gdje razina ima jednu; njezine rijeke se nagibaju s tlom |
| Taktičke karte | iz `content/base/res/locations_maps.dxp.bin`, postavljene prema `mapCoord0/1` i `tankMapCoord0/1` iz BLK-a; vrh slike je sjever |
| Postavljeni objekti (`RIGz`: fiksne instance generatora instanci za prikaz) | svaka instanca, kao matrica 3x4 od 16-bitnih vrijednosti ili, na nekim razinama, 32-bitnih (broj bajtova ćelije odlučuje); svaki bajt svake ćelije obračunat na provjerenim razinama |
| Generirani objekti (`RIGz` maske klasa zemljišta i resursi `LandClass`) | generator igre, prenesen: ista mjesta isprobana istim redom s istim slučajnim brojevima, maske klasa zemljišta i isključenja, objekt odabran na svakom mjestu, njegova rotacija, mjerilo i visinski pomak; popločani (gradski blokovi) i posađeni (šume, grmlje, polja) entiteti. Generirano samo nad kartom tenkova. Aproksimirano: visina tla i normala (iz visinske karte; igra prati zraku), isključni okviri koje igra registrira za vrijeme rada, i zakret drveća (igra ga hvata na paletu rotacija impostora). |
| Mreže za prikaz (`RendInst` resursi u `content/*/res/*.grp`, materijali u `riDesc.bin`) | vrhovi i trokuti svakog LOD-a (pozicije u float-u; indeksi od 16 ili 32 bita, obični ili meshoptimizer-spakirani), materijal svakog elementa. Elementi dekala i impostor-bilborda se izostavljaju; prozirni (staklo) se zadržavaju |
| Boje objekata | po materijalu, prosjek male mip razine njegove difuzne teksture (ponderiran alfom za lišće), iz paketa tekstura instalacije: t0 za većinu shadera, prva detalj-difuzna tamo gdje je t0 prekrivanje ili maska. Jedna boja po materijalu: bez teksture na objektima |
| Sudarni oblici (`<object>_collision`) | sudarni resursi streama verzije 3, korišteni tamo gdje objekt nema mrežu za prikaz. Crta se samo ono što igrine zrake pogađaju (čvorovi `TRACEABLE`), a kutije, kugle i kapsule samo kad resurs nema mrežu: ostalo su grubi fizički zamjenici koji bi se pokazali kao kocke oko objekta |
| Navigacijska mreža (`Lnav`), crtana mreža zemljišta, trava, `spgz`, `stbl`, `d2co` | nisu čitani |

Razine su komprimirane Oodleom, koji je vlasnički. Igra ima svoju kopiju,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (obična x64 verzija), i ona se učitava;
`HEAT3D_OODLE=<dll ili mapa>` pokazuje na drugu. Ovdje nije uključen nikakav Oodle.

## Formati, i gdje su dokumentirani {#formats-and-where-they-are-documented}

Gaijin je objavio izvorni kod Dagor Enginea pod licencom BSD 3-Clause (github.com/GaijinEntertainment/DagorEngine).
Čitači ovdje su napisani prema njemu; nijedan igrin kod nije dekompiliran. Svaki modul navodi izvorne datoteke
koje slijedi:

- `vromfs.py`: `*.vromfs.bin` (zaglavlje `VRFs`/`VRFx`, zstd tijelo čiji su prvih i zadnjih 16 bajtova XOR-irani
  fiksnim ključem, tablica imena i tablica pomaka:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) i binarni BLK (oblici 1-5,
  sa zajedničkom mapom imena arhive `\xff?nm` i zstd rječnikom: `ioSys/dataBlock/blk_serialize.cpp`,
  `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: paketi tekstura `DxP2` (`lib3d/texPackMgr2.cpp`) i DDSx zaglavlja (`sharedInclude/3d/ddsxTex.h`);
  DXT1/DXT5/BC7 dekodira Pillow.
- `dagorlevel.py`: binarna razina (`scene/loadLevel.cpp`), visinska karta (`heightmap/heightmapPhysHandler.cpp`,
  `heightMapLand/compressedHeightmap.cpp`), praćenik zraka za zemljište (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) i vodena visinska karta (`fftWater/fftWater.cpp`).
- `rigen.py`: postavljeni objekti (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generirani objekti (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`,
  `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: instance za prikaz (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`,
  `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) i kodek indeksa
  meshoptimizera (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: boja tla (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`,
  `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: paketi resursa (`gameRes/grpData.h`) i sudarni resursi (`sharedInclude/gameRes/collResStream.h`,
  `gameRes/collisionGameResLoad.cpp`), čiji su trokuti spremljeni kao četverostablo BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) čita iste arhive; nije potreban i nije korišten.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
