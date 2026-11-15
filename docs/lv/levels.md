---
title: Līmeņi
nav_order: 9
lang: "lv"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Līmeņi (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` pārvērš jūsu pašu War Thunder instalācijas līmeņus `.glb` līmeņos skatītājam, tajā pašā koordinātu sistēmā kā atkārtojumu tabulas.

## Soli pa solim {#step-by-step}

1. Uzskaitiet savas instalācijas līmeņus: `heat3d-wt-level list`. Tas izdrukā vienu rindu katram līmenim: tā nosaukumu, reljefu un kartes, tad skaitu. Piemērs (izdomāts līmenis):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Izvelciet vienu, vairākus (aizstājējzīmes atļautas) vai visus:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Ielādējiet `levels/<level>/<level>.glb` skatītāja Līmeņa panelī, zem tās kartes kaujām.

Līmeņi, ko jūs rakstāt, paliek jūsu datorā: nekad tos nepublicējiet (skat. [Noteikumi un licence](terms.md)).

## Iespējas {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Komanda / iespēja | Ko dara |
|---|---|
| `list [--game MAPE]` | visi līmeņi instalācijā |
| `extract <levels...>` / `--all` | minētie līmeņi (kā tos izdrukā `list`; aizstājējzīmes atļautas) vai visi līmeņi |
| `-o`, `--out` | izvades mape; katrs līmenis ir `<out>/<level>/` |
| `--game MAPE` | War Thunder mape (noklusējums: atrasta caur Steam vai launcher; arī `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | zemes paraugu ņemšana, zemes krāsa un objektu budžets pār tanku karti (noklusējums `medium`) |
| `--max-object-triangles N` | objektu budžets (noklusējums: detaļas) |
| `--max-grid N` | augstuma karšu paraugi uz malu, katrai daļai (noklusējums 1024) |
| `--no-objects` | neiekļauj ēkas, kokus un citus novietotos objektus |
| `--no-generated` | neiekļauj objektus, ko ģenerē zemes klases (meži, pilsētas) |
| `--no-terrain-colour` | apklāj zemi ar taktisko karti, nevis ar zemes klasēm |
| `--no-texture` | atstāj zemi bez tekstūras |
| `--skip-existing` | atstāj līmeņus, kuriem `.glb` jau ir |

## Kas tiek rakstīts {#what-is-written}

Katrs līmenis kļūst par `<out>/<level>/<level>.glb`, `<level>.json` (kas tika nolasīts, ūdens līmenis, kartu taisnstūri, trijstūru skaits, laiki) un līmeņa taktiskajām kartēm kā `<level>_map.png` (gaisa karte) un `<level>_tankmap.png`; zemes kartēm ir arī `<level>_terrain.png`, zemes pašas krāsas pār tanku karti. `glb` tiek rakstīts uz `<level>.glb.part` un pārdēvēts, kad tas ir pabeigts; kamēr līmenis tiek rakstīts, tiek turēts `<out>/<level>/.<level>.lock`, tāpēc divas izvilkšanas nekad neraksta to pašu līmeni (otrā izdrukā `busy <level>`). Instalāciju atrod caur Steam vai launcher noklusētajām mapēm; `--game <mape>` vai `HEAT3D_WT_GAME` norāda, kur tā ir citādi.

| Daļa | Ko tā ir |
|---|---|
| `ground:<level>` | zemes augstuma karte (`HM2`) kā režģis; uz zemes kartēm tanku kartes vidus (puse no tās platuma) ar `--detail` soli, krāsota ar zemes klasēm, zemes uzlīmēm un ceļiem (`<level>_terrain.png`; taktiskā karte, ja tas nav iespējams); kartēs bez tanku kartes (gaisa kartēs) — visa augstuma karte vienā solī (2048 paraugi uz malu pie `high`, citādi 1024), krāsota ar zemes klasēm pār gaisa kartes laukumu (4096 pikseļi uz malu, apmēram 32 m pikselis pār 131 km; taktiskā karte, ja tas nav iespējams); līmeņos bez augstuma kartes — zemes sietu |
| `ground:<level> tank map` | pārējā tanku karte, vienu soli rupjāka |
| `ground:<level> heightmap surroundings` | pārējā augstuma karte, vēl rupjāka |
| `ground:<level> land mesh` | zemes sieta sadursmju trijstūri tur, kur augstuma karte nesniedzas (tanku kartes apkārtne, līdz desmitiem kilometru); līmeņos bez augstuma kartes tā ir zeme, krāsota kā iepriekš |
| `ground:<level> outside the map` | zeme, ko attēls neaptver, bez tekstūras |
| `water:<level>` | viens plakans taisnstūris līmeņa `water_level` augstumā pār visu reljefu: spēle ūdeni zīmē kā vienu plakni, un zems zeme zem tā ir jūra, ezers vai upes gultne |
| `water:<level> rivers` | līmeņos ar ūdens augstuma karti (`WHM`) — slīpa ūdens virsma pār šūnām, ko tā aizņem |
| `structure:<level> buildings` | katrs novietotais objekts, kas nav augs: mājas, drupas, sienas, žogi, tilti, sliedes, akmeņi, rekvizīti. Fiksētie (`RIGz`) un pār tanku karti tie, ko ģenerē zemes klases (pilsētu bloki, akmeņi). Katrs tiek zīmēts ar savu renderēšanas tīklu (sienas, jumti, logu atveres, sijas) LOD līmenī, ko atļauj trijstūru budžets, krāsots pa materiāliem pēc vidējā difūzās tekstūras |
| `structure:<level> trees` | koki un krūmi, fiksēti un ģenerēti (meži, dzīvžogi): to renderēšanas tīkls, kur budžets atļauj, citādi stumbrs un vainags (konusa formā skuju kokiem) ar koka pašu lapu krāsu, pēc koka reālā izmēra |

Objekti bez renderēšanas tīkla atgriežas pie savas sadursmes formas; koki bez tīkla — pie vainaga. Virsotņu krāsas (`COLOR_0`) satur sRGB kodētas vērtības, ko 3DHeat skatītājs arī lasa.

**Koordinātas** ir spēles metri ar apgrieztu z: glb (x, y, z) = spēle (x, y, -z). Spēles pasaule ir kreisēja (x uz austrumiem, y uz augšu, z uz ziemeļiem); glTF ir labēja. `heat3d-wt-replay` paturē spēles z un liek skatītājam to apgriezt, tāpēc atkārtojums un tā kartes līmenis sakrīt bez novietošanas soļa. JSON dod katras taktiskās kartes taisnstūri spēles metros un tā stūrus glb telpā, lai PNG varētu ielādēt kā kartes attēlu.

**Detaļa.** `--detail low|medium|high` (noklusējums medium) nosaka pār tanku karti:

| | tanku kartes vidus | pārējā tanku karte | zemes krāsa | objektu budžets | visvairāk trijstūru vienā objektā | paturētie ģenerētie augi |
|---|---|---|---|---|---|---|
| low | katrs 4. paraugs | katrs 8. | 4 m pikselis | 1,2 M | 1500 | koki 35 %, krūmi 20 % |
| medium | katrs 2. | katrs 4. | 2 m | 3,5 M | 4000 | koki 70 %, krūmi 50 % |
| high | katrs paraugs (uz lielākajai daļai zemes karšu 2 m) | katrs 2. | 1 m (ne vairāk kā 4096 pikseļi uz malu) | 4,5 M | 12 000 | visi |

Divi tanku kartes gredzeni tiek turēti pie 0,3 M (low), 1 M (medium) un 3,7 M (high) trijstūriem: kartēs, kuru augstuma karte ir smalkāka par 2 m, soļi dubultojas (vispirms ārējais gredzens), līdz tie iederas, tāpēc tie iznāk arī apmēram 2 m.

Zemes karte `high` līmenī iznāk apmēram 8 miljoni trijstūru (3,5 M zeme, 4,5 M objekti) un 250 MB; `medium` — apmēram 4,5 M. Objektu LOD ir tie, ko pati spēle zīmētu no viena skatīšanās attāluma: īsākais, kura kopējais iederas budžetā; mazi rekvizīti vispirms nokrīt uz rupjiem LOD, lieli ēkas — pēdējie, pēc attālumiem, ko to veidotāji devuši katram LOD (JSON `lodDistance`); tas, ko šis solis ietaupa pāri budžetam, atgriežas lielākajiem objektiem. Rupja zemes krāsa (gaisa kartes) vispirms apvieno katras zemes klases tekstūras līdz pikseļa izmēram, lai flīzes nedotu moire. Ja pat rupjākie LOD neiederas, koki, kas ietaupa visvairāk, kļūst par vainagiem, un tad mazākie tipi tiek atstāti ārpusē (`leftOut`); neviens objekts netiek zīmēts kā kaste (sadursmes forma, ja tāda ir, ir paša objekta).

Ģenerētie objekti tiek deterministiski retināti pēc veida (`density`), vienādi katrā izpildē. `--max-object-triangles` pārraksta budžetu, `--max-grid` (noklusējums 1024) ierobežo augstuma kartes rupjākās daļas, `--no-objects` atstāj objektus ārpusē, `--no-generated` — ģenerētos, `--no-terrain-colour` apklāj zemi ar taktisko karti, `--no-texture` atstāj to bez tekstūras.

JSON `parts.objects` uzskaita instances (fiksētās un ģenerētās, pēc veida un zemes klases), cik no tām zīmētas kurā LOD (`drawnAs`), trijstūrus, LOD attālumu un sekundes; `parts.heightmap.rings` katra zemes gredzena soli un trijstūrus; `parts.terrainColour` zemes klases un to krāsas, ceļus un zemes uzlīmes; `trianglesTotal`, `glbBytes` un `secondsBy` — kopsummas.

## Kas tiek nolasīts un cik labi {#what-is-read-and-how-well}

| Daļa | Statuss |
|---|---|
| Līmeņa bināro fails (`levels/<level>.bin`, `DBLD` 3x64): bloku tabula | katrs līmenis pārbaudīts |
| Augstuma karte (`HM2`, versijas 0–2; versija 2 ir 8 bitu vērtības blokos, Oodle vai zstd gabalos) | katrs līmenis, kura augstuma karte ir versija 2 ar Oodle gabaliem; pārbaudīts acīm pret to taktiskajām kartēm (upes, ielejas, krasti un pilsētas sakrīt) |
| Zemes sieta sadursmes (`lmap`, tā `LTdump` zemes staru izsekotājs) | nolasīts, kur līmenim tāds ir (Oodle saspiests). Tā ir spēles sadursmju virsma, nevis renderētais tīkls, tāpēc tā ir rupjāka, kur zeme ir līdzena |
| Zemes krāsa (`lmap` zemes klases un svaru karte, `LMp2` fizikas karte, `hspl` splaini) | zemes klašu krāsu kartes un detaļu tekstūras (to vidējās krāsas), svērtas ar svaru karti, 1 m biomu indekss indeksētām zemes klasēm, fizikas kartes ceļu un zemes uzlīmju formas to splaina vai materiāla tekstūras krāsā, klintis stāvās nogāzēs. Pārbaudīts pret tanku kartēm: ceļi, pilsētas, ezeri, meža joslas un klinšu izcelsmes sakrīt. Spēles pašas War Thunder reljefa ēnotāja krāsu formula nav publiskajā kodā; tiek izmantota dzinēja publicētā (daNetGame), kura rezultāts ir piesātinātāks nekā taktiskā karte |
| Ūdens līmenis | `water_level` no līmeņa BLK `aces.vromfs.bin` (0, ja tā nav) |
| Ūdens augstuma karte (`WHM`: režģis no plakanām šūnām un 130x130 lapām ar 16 bitu augstumiem) | nolasīts, kur līmenim tāda ir; tās upes slīpst kopā ar zemi |
| Taktiskās kartes | no `content/base/res/locations_maps.dxp.bin`, novietotas ar BLK `mapCoord0/1` un `tankMapCoord0/1`; attēla augša ir ziemeļi |
| Novietotie objekti (`RIGz`: renderēšanas instanču ģeneratora fiksētās instances) | katra instance kā 3x4 matrica ar 16 bitu vērtībām vai dažos līmeņos 32 bitu (šūnas baitu skaits nosaka); katrs šūnas baits uzskaitīts pārbaudītajos līmeņos |
| Ģenerētie objekti (`RIGz` zemes klašu maskas un `LandClass` resursi) | spēles ģenerators, pārnests: tās pašas vietas, pārbaudītas tādā pašā secībā ar tiem pašiem nejaušiem skaitļiem, zemes klašu un izslēgšanas maskas, objekts, kas izvēlēts katrā vietā, tā rotācija, mērogs un augstuma nobīde; flīzētas (pilsētu bloki) un iestādītas (meži, krūmi, lauki) vienības. Ģenerēts tikai pār tanku karti. Aptuveni: zemes augstums un normāle (no augstuma kartes; spēle izseko staru), izslēgšanas kastes, ko spēle reģistrē izpildes laikā, un koku virziens (spēle to piesaista pie impostora rotācijas paletes) |
| Renderēšanas tīkli (`RendInst` resursi `content/*/res/*.grp`, materiāli `riDesc.bin`) | katra LOD virsotnes un trijstūri (peldošā punkta pozīcijas; 16 vai 32 bitu indeksi, parasti vai meshoptimizer saspiesti), katra elementa materiāls. Dekālu un impostora bilbordu elementi ir ārpusē; caurspīdīgie (stikls) ir paturēti |
| Objektu krāsas | pa materiāliem, vidējā difūzās tekstūras mazā mip (alfas svērtā lapām), no instalācijas tekstūru paketēm: t0 lielākajai daļai shader, pirmā detaļas difūzā, kur t0 ir pārklājums vai maska. Viena krāsa uz materiālu: objektiem nav tekstūras |
| Sadursmju formas (`<object>_collision`) | sadursmju resursi straumes versijā 3, izmantoti, kur objektam nav renderēšanas tīkla. Zīmēts tikai tas, ko spēles stari trāpa (`TRACEABLE` mezgli), un kastes, sfēras un kapsulas tikai tad, kad resursam nav tīkla: pārējie ir rupji fizikas aizstājēji, kas parādītos kā kubi ap objektu |
| Navigācijas tīkls (`Lnav`), renderētais zemes tīkls, zāle, `spgz`, `stbl`, `d2co` | nav nolasīti |

Līmeņi ir saspiesti ar Oodle, kas ir patentēts. Spēle piegādā savu kopiju, `<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (parasta x64 versija), un tā ir tā, kas tiek ielādēta; `HEAT3D_OODLE=<dll vai mape>` norāda uz citu. Oodle šeit nav iekļauts.

## Formāti un to dokumentācija {#formats-and-where-they-are-documented}

Gaijin ir publicējis Dagor Engine kodu ar BSD 3-Clause licenci (github.com/GaijinEntertainment/DagorEngine). Šeit esošie lasītāji ir uzrakstīti pēc tā; spēles kods nav dekompilēts. Katrs modulis nosauc avota failus, kurus tas seko:

- `vromfs.py`: `*.vromfs.bin` (galvene `VRFs`/`VRFx`, zstd pamatteksts, kura pirmie un pēdējie 16 baiti ir XOR ar fiksētu atslēgu, nosaukumu tabula un nobīžu tabula: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) un binārais BLK (formas 1–5, ar arhīva kopīgo nosaukumu karti `\xff?nm` un zstd vārdnīcu: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: tekstūru paketes `DxP2` (`lib3d/texPackMgr2.cpp`) un DDSx galvenes (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekodē Pillow.
- `dagorlevel.py`: līmeņa binārais fails (`scene/loadLevel.cpp`), augstuma karte (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), zemes staru izsekotājs (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) un ūdens augstuma karte (`fftWater/fftWater.cpp`).
- `rigen.py`: novietotie objekti (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: ģenerētie objekti (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: renderēšanas instances (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) un meshoptimizer indeksu kodeks (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: zemes krāsa (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: resursu paketes (`gameRes/grpData.h`) un sadursmju resursi (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), kuru trijstūri ir glabāti kā četrstūru BVH (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) lasa tos pašus arhīvus; tas nav vajadzīgs un netiek izmantots.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
