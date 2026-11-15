---
title: Poziomy
nav_order: 9
lang: pl
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Poziomy (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` zamienia poziomy z Twojej instalacji War Thunder w pliki
`.glb` dla przeglądarki, w tym samym układzie co tabele replayów.

## Krok po kroku {#step-by-step}

1. Wypisz poziomy swojej instalacji: `heat3d-wt-level list`. Wypisuje po jednej
   linii na poziom: jego nazwę, teren i mapy, a potem liczbę. Na przykład
   (wymyślony poziom):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Wypakuj jeden, kilka (można użyć wieloznaczników) albo wszystkie:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Wczytaj `levels/<level>/<level>.glb` w panelu **Tło / poziom** przeglądarki, pod bitwami
   tej mapy.

Poziomy, które zapisujesz, zostają na Twoim komputerze: nigdy ich nie publikuj (zob.
[Warunki i licencja](terms.md)).

## Opcje {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Polecenie / opcja | Działanie |
|---|---|
| `list [--game FOLDER]` | każdy poziom w instalacji |
| `extract <levels...>` / `--all` | wskazane poziomy (tak, jak wypisuje je `list`; można użyć wieloznaczników) albo wszystkie poziomy |
| `-o`, `--out` | folder wyjściowy; każdy poziom trafia do `<out>/<level>/` |
| `--game FOLDER` | folder War Thunder (domyślnie: znajdowany przez Steam lub launcher; także `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | krok siatki terenu, kolor terenu i budżet obiektów na mapie czołgów (domyślnie `medium`) |
| `--max-object-triangles N` | budżet obiektów (domyślnie zależny od `--detail`) |
| `--max-grid N` | próbki mapy wysokości na bok, na część (domyślnie 1024) |
| `--no-objects` | pomiń budynki, drzewa i inne postawione obiekty |
| `--no-generated` | pomiń obiekty generowane przez klasy terenu (lasy, miasta) |
| `--no-terrain-colour` | pokryj teren mapą taktyczną, a nie klasami terenu |
| `--no-texture` | zostaw teren bez tekstury |
| `--skip-existing` | pomiń poziomy, których `.glb` już istnieje |

## Co jest zapisywane {#what-is-written}

Każdy poziom staje się `<out>/<level>/<level>.glb`, `<level>.json` (co odczytano,
poziom wody, prostokąty map, liczby trójkątów, czasy) oraz taktyczne mapy poziomu
jako `<level>_map.png` (mapa powietrzna) i `<level>_tankmap.png`;
mapy naziemne dostają też `<level>_terrain.png`, czyli własne kolory terenu nałożone na
mapę czołgów. Plik glb zapisuje się jako `<level>.glb.part` i zmienia nazwę po zakończeniu;
podczas zapisu poziomu trzymany jest `<out>/<level>/.<level>.lock`, więc dwa wypakowania
nigdy nie zapiszą tego samego poziomu (drugie wypisze `busy <level>`).
Instalację znajduje się przez Steam lub domyślne foldery launchera;
`--game <folder>` albo `HEAT3D_WT_GAME` mówią, gdzie ona jest, jeśli nie została znaleziona.

| Część | Czym jest |
|---|---|
| `ground:<level>` | mapa wysokości terenu (`HM2`) jako siatka; na mapach naziemnych środek mapy czołgów (połowa jej szerokości) w kroku `--detail`, pokolorowany klasami terenu, nakładkami terenu i drogami (`<level>_terrain.png`; mapa taktyczna, gdy nie da się tego zrobić); na mapach bez mapy czołgów (mapy powietrzne) cała mapa wysokości w jednym kroku (2048 próbek na bok przy `high`, 1024 w pozostałych), pokolorowana klasami terenu na obszarze mapy powietrznej (4096 pikseli na bok, około 32 m na piksel przy 131 km; mapa taktyczna, gdy nie da się tego zrobić); na poziomach bez mapy wysokości – siatka terenu |
| `ground:<level> tank map` | reszta mapy czołgów, o jeden krok grubsza |
| `ground:<level> heightmap surroundings` | reszta mapy wysokości, jeszcze grubsza |
| `ground:<level> land mesh` | trójkąty kolizji siatki terenu tam, gdzie mapa wysokości nie sięga (okolice mapy czołgów, aż na dziesiątki kilometrów); na poziomach bez mapy wysokości to teren, pokolorowany jak wyżej |
| `ground:<level> outside the map` | teren, którego obraz nie obejmuje, bez tekstury |
| `water:<level>` | jeden płaski prostokąt na poziomie `water_level` nad całym terenem: gra rysuje wodę jako jedną płaszczyznę, a niski teren pod nią to morze, jezioro lub dno rzeki |
| `water:<level> rivers` | na poziomach z mapą wody (`WHM`) pochyła powierzchnia wody nad komórkami, które ona pokrywa |
| `structure:<level> buildings` | każdy postawiony obiekt, który nie jest rośliną: domy, ruiny, mury, ogrodzenia, mosty, tory, skały, rekwizyty. Stałe (`RIGz`) i, na mapie czołgów, te, które generują klasy terenu (bloki miejskie, kamienie). Każdy rysowany jest siatką renderującą (ściany, dachy, otwory okienne, belki) na poziomie LOD, na jaki pozwala budżet trójkątów, kolorem wg materiału, czyli średnią jego tekstury rozproszonej |
| `structure:<level> trees` | drzewa i krzewy, stałe i generowane (lasy, żywopłoty): ich siatka renderująca tam, gdzie pozwala budżet, w przeciwnym razie pień i korona (stożek dla iglastych) w kolorze liści tego drzewa, w jego prawdziwym rozmiarze |

Obiekty bez siatki renderującej wracają do swojego kształtu kolizji; drzewa bez niej
– do korony. Kolory wierzchołków (`COLOR_0`) trzymają wartości zakodowane w sRGB,
tak jak odczytuje je przeglądarka 3DHeat.

**Współrzędne** to metry gry z odbitym z: glb (x, y, z) = gra (x, y, -z). Świat gry jest
lewoskrętny (x na wschód, y w górę, z na północ); glTF jest prawoskrętny. `heat3d-wt-replay` zachowuje
z gry i każe przeglądarce odbić je, więc replay i poziom jego mapy lądują jeden na drugim
bez żadnego kroku ustawiania. JSON podaje prostokąt każdej mapy taktycznej w metrach gry
i jej rogi w przestrzeni glb, do wczytania PNG jako obrazu mapy.

**Szczegółowość.** `--detail low|medium|high` (domyślnie medium) ustawia, na mapie czołgów:

| | środek mapy czołgów | reszta mapy czołgów | kolor terenu | budżet obiektów | najwięcej trójkątów na obiekt | zachowane generowane rośliny |
|---|---|---|---|---|---|---|
| low | co 4. próbka | co 8. | 4 m na piksel | 1,2 M | 1 500 | drzewa 35 %, krzewy 20 % |
| medium | co 2. | co 4. | 2 m | 3,5 M | 4 000 | drzewa 70 %, krzewy 50 % |
| high | każda próbka (2 m na większości map naziemnych) | co 2. | 1 m (najwyżej 4096 pikseli na bok) | 4,5 M | 12 000 | wszystkie |

Dwa pierścienie mapy czołgów trzymane są w granicach 0,3 M (low), 1 M (medium) i 3,7 M (high)
trójkątów: na mapach, których mapa wysokości jest dokładniejsza niż 2 m, kroki się podwajają
(najpierw pierścień zewnętrzny), aż się zmieszczą, więc wychodzą też około 2 m.

Mapa naziemna przy `high` wychodzi około 8 milionów trójkątów (3,5 M terenu,
4,5 M obiektów) i 250 MB; przy `medium` około 4,5 M. LOD-y obiektów to te,
które sama gra narysowałaby z jednej odległości oglądania: najkrótszy, którego suma mieści się w budżecie.
Małe rekwizyty schodzą najpierw na grube LOD-y, a duże budynki na końcu, wg zasięgów,
jakie ich twórcy podali dla każdego LOD (`lodDistance` w JSON); to, co ten krok oszczędza ponad
budżet, wraca do największych obiektów. Gruba kolorystyka terenu (mapy powietrzne) najpierw uśrednia
kafelkowane tekstury każdej klasy terenu do rozmiaru piksela, żeby kafelki nie
tworzyły mory. Gdy nawet najgrubsze LOD-y się nie mieszczą, drzewa, które oszczędzają najwięcej,
stają się koronami, a potem wyłącza się najmniejsze typy (`leftOut`); żaden obiekt
nie jest rysowany jako pudełko (kształt kolizji, jeśli jest, to własny kształt obiektu).
Obiekty generowane są przerzedzane deterministycznie wg rodzaju (`density`), zawsze te same
przy każdym uruchomieniu. `--max-object-triangles` nadpisuje budżet,
`--max-grid` (domyślnie 1024) ogranicza grubsze części mapy wysokości, `--no-objects`
pomija obiekty, `--no-generated` – generowane, `--no-terrain-colour`
pokrywa teren mapą taktyczną, a `--no-texture` zostawia go bez tekstury.

`parts.objects` w JSON wypisuje instancje (stałe i generowane, wg rodzaju i klasy terenu),
ile narysowano na jakim LOD (`drawnAs`), trójkąty, zasięg LOD i sekundy;
`parts.heightmap.rings` krok i trójkąty każdego pierścienia terenu; `parts.terrainColour` klasy
terenu i ich kolory, drogi i nakładki terenu; `trianglesTotal`, `glbBytes` i `secondsBy` – sumy.

## Co jest odczytywane i jak dobrze {#what-is-read-and-how-well}

| Część | Stan |
|---|---|
| Plik binarny poziomu (`levels/<level>.bin`, `DBLD` 3x64): tabela bloków | sprawdzono każdy poziom |
| Mapa wysokości (`HM2`, wersje 0-2; wersja 2 to wartości 8-bitowe w blokach, fragmenty Oodle lub zstd) | każdy poziom, którego mapa wysokości to wersja 2 z fragmentami Oodle; sprawdzone na oko z ich mapami taktycznymi (rzeki, doliny, wybrzeża i miasta się zgadzają) |
| Kolizja siatki terenu (`lmap`, jej śledzenie promieni `LTdump`) | odczytywana tam, gdzie poziom ją ma (spakowana Oodle). To powierzchnia kolizji gry, a nie renderowana siatka, więc jest grubsza tam, gdzie teren jest płaski |
| Kolor terenu (mapy klas terenu `lmap` i mapa wag, mapa fizyki `LMp2`, `hspl` splajny) | mapy kolorów klas terenu i tekstury detali (ich średnie kolory) ważone mapą wag, indeks biomów 1 m indeksowanych klas terenu, kształty dróg i nakładek terenu z mapy fizyki w kolorze tekstury ich splajnu lub materiału, klify na stromych zboczach. Sprawdzone z mapami czołgów: drogi, miasta, jeziora, pasy lasów i wychodnie skał się zgadzają. Wzór kolorów shadera terenu War Thunder nie jest w publicznym kodzie; używany jest opublikowany przez silnik (daNetGame), który wychodzi bardziej nasycony niż mapa taktyczna |
| Poziom wody | `water_level` z BLK poziomu w `aces.vromfs.bin` (0, gdy go nie ma) |
| Mapa wody (`WHM`: siatka płaskich komórek i stron 130x130 16-bitowych wysokości) | odczytywana tam, gdzie poziom ją ma; jej rzeki pochylają się razem z terenem |
| Mapy taktyczne | z `content/base/res/locations_maps.dxp.bin`, ustawione wg `mapCoord0/1` i `tankMapCoord0/1` z BLK; góra obrazu to północ |
| Postawione obiekty (`RIGz`: stałe instancje generatora instancji renderowania) | każda instancja, jako macierz 3x4 wartości 16-bitowych albo, na części poziomów, 32-bitowych (decyduje liczba bajtów komórki); każdy bajt każdej komórki rozliczony na sprawdzonych poziomach |
| Obiekty generowane (maski klas terenu `RIGz` i zasoby `LandClass`) | generator gry przeniesiony: te same miejsca, sprawdzane w tej samej kolejności, z tymi samymi liczbami losowymi, maski klas terenu i wykluczeń, obiekt wybrany w każdym miejscu, jego obrót, skala i przesunięcie wysokości; jednostki kafelkowane (bloki miejskie) i sadzone (lasy, krzewy, pola). Generowane tylko na mapie czołgów. Przybliżone: wysokość i normalna terenu (z mapy wysokości; gra śledzi promień), pudełka wykluczeń, które gra rejestruje w czasie działania, oraz obrót drzew (gra przyciąga go do palety obrotów impostora) |
| Siatki renderujące (zasoby `RendInst` w `content/*/res/*.grp`, materiały w `riDesc.bin`) | wierzchołki i trójkąty każdego LOD (pozycje zmiennoprzecinkowe; indeksy 16- lub 32-bitowe, zwykłe albo spakowane meshoptimizerem), materiał każdego elementu. Elementy nalepek i impostorów-billboardów są pomijane; przezroczyste (szkło) zostają |
| Kolory obiektów | na materiał: średnia małego mipa jego tekstury rozproszonej (ważona alfą dla liści), z paczek tekstur instalacji: t0 dla większości shaderów, pierwsza tekstura rozproszona detalu tam, gdzie t0 jest nakładką lub maską. Jeden kolor na materiał: bez tekstury na obiektach |
| Kształty kolizji (`<object>_collision`) | zasoby kolizji strumienia w wersji 3, używane tam, gdzie obiekt nie ma siatki renderującej. Rysuje się tylko to, w co trafiają promienie gry (węzły `TRACEABLE`), a pudełka, kule i kapsuły tylko wtedy, gdy zasób nie ma siatki: reszta to grube zastępniki fizyki, które pokazałyby się jako sześciany wokół obiektu |
| Siatka nawigacyjna (`Lnav`), renderowana siatka terenu, trawa, `spgz`, `stbl`, `d2co` | nieodczytane |

Poziomy są kompresowane przez Oodle, które jest zastrzeżone. Gra dołącza własną kopię,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (zwykła wersja x64), i to ją się ładuje;
`HEAT3D_OODLE=<dll lub folder>` wskazuje inną. Nic z Oodle nie jest tu dołączone.

## Formaty i miejsca, w których są opisane {#formats-and-where-they-are-documented}

Gaijin opublikował kod Dagor Engine na licencji BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Czytniki tutaj zostały napisane na jego
podstawie; kod gry nie został zdekompilowany. Każdy moduł podaje pliki źródłowe, których się trzyma:

- `vromfs.py`: `*.vromfs.bin` (nagłówek `VRFs`/`VRFx`, treść zstd, której pierwsze i
  ostatnie 16 bajtów jest XOR-owane stałym kluczem, tabela nazw i tabela przesunięć:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  oraz binarny BLK (formy 1-5, ze wspólną mapą nazw archiwum `\xff?nm` i
  słownikiem zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: paczki tekstur `DxP2` (`lib3d/texPackMgr2.cpp`) i nagłówki DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekoduje Pillow.
- `dagorlevel.py`: plik binarny poziomu (`scene/loadLevel.cpp`), mapa wysokości
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  śledzenie promieni terenu (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) i mapa wody (`fftWater/fftWater.cpp`).
- `rigen.py`: postawione obiekty (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generowane obiekty (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: instancje renderowania (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) oraz kodek indeksów
  meshoptimizera (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: kolor terenu (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: paczki zasobów (`gameRes/grpData.h`) i zasoby kolizji
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  których trójkąty są przechowywane jako BVH czworokątów (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) czyta te same archiwa; nie jest potrzebny i nie jest używany.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
