---
title: "Pályák"
nav_order: 9
lang: hu
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Pályák (heat3d-wt-level) {#levels-heat3d-wt-level}

A `heat3d-wt-level` a saját War Thunder-telepítésed pályáit a megjelenítő számára `.glb`
pályákká alakítja, ugyanabban a koordinátarendszerben, mint a visszajátszások táblázatai.

## Lépésről lépésre {#step-by-step}

1. Sorold fel a telepítésed pályáit: `heat3d-wt-level list`. Pályánként egy sort ír ki:
   a neve, a terepe és a térképei, majd a darabszám. Például (kitalált pálya):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Csomagolj ki egyet, többet (helyettesítő karakter megengedett) vagy mindet:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Töltsd be a `levels/<level>/<level>.glb` fájlt a megjelenítő Háttér / pálya paneljébe, annak a
   térképnek a csatái alá.

Az általad írt pályák a gépeden maradnak: soha ne tedd közzé (lásd
[Fogalmak és licenc](terms.md)).

## Kapcsolók {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Parancs / kapcsoló | Mit tesz |
|---|---|
| `list [--game FOLDER]` | minden pálya a telepítésben |
| `extract <levels...>` / `--all` | a megnevezett pályák (ahogy a `list` kiírja; helyettesítő karakter megengedett), vagy minden pálya |
| `-o`, `--out` | kimeneti mappa; minden pálya a `<out>/<level>/` mappába kerül |
| `--game FOLDER` | a War Thunder mappája (alapértelmezés: a Steamen vagy az indítón keresztül megtalálva; a `HEAT3D_WT_GAME` is) |
| `--detail low/medium/high` | a talaj mintavételezése, a talaj színe és az objektumkeret a tankok térképén (alapértelmezés `medium`) |
| `--max-object-triangles N` | az objektumkeret (alapértelmezés: a részletességé) |
| `--max-grid N` | a magasságtérkép mintái oldalanként, részenként (alapértelmezés 1024) |
| `--no-objects` | épületek, fák és egyéb elhelyezett objektumok kihagyása |
| `--no-generated` | a talajosztályok által generált objektumok kihagyása (erdők, városok) |
| `--no-terrain-colour` | a talaj textúrázása a taktikai térképpel, nem a talajosztályokkal |
| `--no-texture` | a talaj textúra nélkül marad |
| `--skip-existing` | azok a pályák kimaradnak, amelyeknek már van `.glb` fájljuk |

## Mi íródik ki {#what-is-written}

Minden pályából lesz: `<out>/<level>/<level>.glb`, `<level>.json` (amit beolvastunk, a
víz szintje, a térképek téglalapjai, háromszögszámok, időmérések), és a pálya taktikai
térképei: `<level>_map.png` (a légi térkép) és `<level>_tankmap.png`; a földi térképek
kapnak egy `<level>_terrain.png` fájlt is, a talaj saját színeit a tankok térképén. A glb
a `<level>.glb.part` fájlba íródik, és kész állapotban kapja meg a végleges nevét; amíg
egy pálya íródik, a `<out>/<level>/.<level>.lock` zár van rajta, így két kicsomagolás
soha nem írja ugyanazt a pályát (a második kiírja: `busy <level>`). A telepítést a Steamen
vagy az indító alapértelmezett mappáin keresztül találjuk meg; ha másutt van, a
`--game <folder>` vagy a `HEAT3D_WT_GAME` mondja meg.

| Rész | Mi ez |
|---|---|
| `ground:<level>` | a terep magasságtérképe (`HM2`) rácsként; a földi térképeken a tankok térképének közepe (szélességének fele) a `--detail` lépésközével, a talajosztályokkal, talajmatricákkal és utakkal színezve (`<level>_terrain.png`; ahol ez nem készíthető, a taktikai térkép); a tankok térképe nélküli térképeken (légi térképek) az egész magasságtérkép egy lépésben (oldalanként 2048 minta `high`-nál, különben 1024), a talajosztályokkal színezve a légi térkép területén (oldalanként 4096 képpont, körülbelül 32 m képpontonként 131 km-en; ahol ez nem készíthető, a taktikai térkép); a magasságtérkép nélküli pályákon a talajháló |
| `ground:<level> tank map` | a tankok térképének többi része, eggyel durvább lépésben |
| `ground:<level> heightmap surroundings` | a magasságtérkép többi része, még durvábban |
| `ground:<level> land mesh` | a talajháló ütközési háromszögei ott, ahol a magasságtérkép nem ér el (a tankok térképének környéke, tíz kilométerekig); a magasságtérkép nélküli pályákon ez a talaj, a fent leírtak szerint színezve |
| `ground:<level> outside the map` | a talaj, amelyet a kép nem fed le, textúra nélkül |
| `water:<level>` | egy lapos téglalap a pálya `water_level` értékén az egész terep felett: a játék a vizet egy síkként rajzolja, és az alacsony talaj alatta tenger, tó vagy folyómeder |
| `water:<level> rivers` | vízmagasságtérképpel (`WHM`) rendelkező pályákon a lejtős vízfelszín azokon a cellákon, amelyeket lefed |
| `structure:<level> buildings` | minden elhelyezett objektum, amely nem növény: házak, romok, falak, kerítések, hidak, sínek, sziklák, díszletek. A rögzítettek (`RIGz`) és a tankok térképén azok, amelyeket a talajosztályok generálnak (városi tömbök, kövek). Mindegyiket a renderelő hálója rajzolja (falak, tetők, ablaknyílások, gerendák), azon a LOD-on, amelyet a háromszögkeret enged, anyagonként színezve a diffúz textúrájuk átlagával |
| `structure:<level> trees` | fák és bokrok, rögzítettek és generáltak (erdők, sövények): a renderelő hálójuk, ahol a keret engedi, különben egy törzs és egy lombkorona (fenyőknél kúp) a fa saját lombszínével, a fa valódi méretében |

Azok az objektumok, amelyeknek nincs renderelő hálójuk, az ütközési alakjukat kapják;
a fák, ha nincs, a lombkoronájukat. A csúcsszínek (`COLOR_0`) sRGB-kódolt értékeket
tartalmaznak, így olvassa őket a 3DHeat megjelenítő.

**Koordináták:** a játék méterei, a z tükrözve: glb (x, y, z) = játék (x, y, -z). A játék
világa balkezes (x kelet, y fel, z észak); a glTF jobbkezes. A `heat3d-wt-replay` megtartja
a játék z-jét, és megmondja a megjelenítőnek, hogy tükrözze, így a visszajátszás és a térképének
pályája egymásra esik, lépés nélkül. A JSON minden taktikai térkép téglalapját a játék
méterében adja meg, a sarkait pedig a glb terében, hogy a PNG térképképként betölthető legyen.

**Részletesség.** A `--detail low|medium|high` (alapértelmezés medium) a tankok térképére:

| | a tankok térképének közepe | a tankok térképének többi része | talajszín | objektumkeret | legtöbb háromszög egy objektumon | megtartott generált növények |
|---|---|---|---|---|---|---|
| low | minden 4. minta | minden 8. | 4 m képpontonként | 1,2 M | 1 500 | fák 35 %, bokrok 20 % |
| medium | minden 2. | minden 4. | 2 m | 3,5 M | 4 000 | fák 70 %, bokrok 50 % |
| high | minden minta (a legtöbb földi térképen 2 m) | minden 2. | 1 m (oldalanként legfeljebb 4096 képpont) | 4,5 M | 12 000 | mind |

A két tanktérkép-gyűrű a 0,3 M (low), 1 M (medium) és 3,7 M (high) háromszögre van korlátozva:
azokon a térképeken, amelyek magasságtérképe 2 m-nél finomabb, a lépések megduplázódnak (először a
külső gyűrű), amíg bele nem férnek, így azok is körülbelül 2 m-en jönnek ki.

Egy földi térkép `high` beállításon körülbelül 8 millió háromszög (3,5 M talaj, 4,5 M objektum) és
250 MB; `medium`-on körülbelül 4,5 M. Az objektumok LOD-jai azok, amelyeket maga a játék rajzolna
egyetlen nézési távolságból: a legrövidebb, amelynek összege belefér a keretbe; a kis díszletek
először a durva LOD-okra esnek, a nagy épületek utoljára, az egyes LOD-okhoz készítőik által adott
távolságok szerint (a JSON `lodDistance` mezője). Amit ez a lépés a kereten túl megspórol, az a
legnagyobb objektumokhoz kerül vissza. A durva talajszín (légi térképek) minden talajosztály
csempézett textúráit először a képpontméretre átlagolja, így a csempék nem kelnek moiré-mintát.
Ha még a legdurvább LOD-ok sem férnek bele, a legtöbbet megspóroló fák lombkoronává lesznek, és
ezután a legkisebb típusok kimaradnak (`leftOut`); egyetlen objektum sincs dobozként rajzolva
(egy ütközési alak, ha van, az objektum saját).
A generált objektumokat típusonként determinisztikusan ritkítjuk (`density`), minden futásban
ugyanazokat. A `--max-object-triangles` felülírja a keretet, a `--max-grid` (alapértelmezés 1024)
korlátozza a magasságtérkép durvább részeit, a `--no-objects` kihagyja az objektumokat, a
`--no-generated` a generáltakat, a `--no-terrain-colour` a taktikai térképpel textúrázza a talajt,
a `--no-texture` textúra nélkül hagyja.

A JSON `parts.objects` mezője felsorolja a példányokat (rögzített és generált, fajta és talajosztály
szerint), hogy hányat rajzoltak melyik LOD-on (`drawnAs`), a háromszögeket, a LOD-távolságot és a
másodperceket; a `parts.heightmap.rings` minden talajgyűrű lépését és háromszögeit; a
`parts.terrainColour` a talajosztályokat és színeiket, az utakat és a talajmatricákat; a
`trianglesTotal`, `glbBytes` és `secondsBy` az összegeket.

## Mi olvasódik be, és mennyire jól {#what-is-read-and-how-well}

| Rész | Állapot |
|---|---|
| Pálya bináris fájlja (`levels/<level>.bin`, `DBLD` 3x64): blokktábla | minden pálya ellenőrizve |
| Magasságtérkép (`HM2`, 0-2-es verziók; a 2-es verzióban 8 bites értékek blokkokban, Oodle vagy zstd darabokban) | minden pálya, amelynek magasságtérképe 2-es verziójú Oodle darabokkal; szemmel ellenőrizve a taktikai térképekhez képest (folyók, völgyek, partok és városok egybeesnek) |
| Talajháló ütközése (`lmap`, a `LTdump` talajsugárkövetőjével) | ott olvasva, ahol a pályának van (Oodle-csomagolt). Ez a játék ütközési felülete, nem a renderelt háló, ezért lapos területen durvább |
| Talajszín (`lmap` talajosztályok és súlytérkép, `LMp2` fizikai térkép, `hspl` görbék) | a talajosztályok színtérképei és részletes textúrái (átlagos színeikkel), a súlytérképpel súlyozva; az indexelt talajosztályok 1 m-es biomindexe; a fizikai térkép út- és talajmatrica-alakzatai annak a görbéjének vagy anyagának textúrájának színében; meredek lejtőkön szirtek. A tankok térképeivel ellenőrizve: az utak, városok, tavak, erdősávok és sziklakibúvások egybeesnek. A War Thunder saját terepárnyalójának színképlete nincs a nyilvános forrásban; a motor közzétett képletét használjuk (daNetGame), amely telítettebb lesz, mint a taktikai térkép |
| Vízszint | a pálya BLK-jának `water_level` értéke az `aces.vromfs.bin`-ből (0, ahol nincs) |
| Vízmagasságtérkép (`WHM`: lapos cellák rácsa és 130x130-as, 16 bites magasságú lapok) | ott olvasva, ahol a pályának van; folyói a talajjal együtt lejtenek |
| Taktikai térképek | a `content/base/res/locations_maps.dxp.bin`-ből, a BLK `mapCoord0/1` és `tankMapCoord0/1` értékei szerint elhelyezve; a kép teteje észak |
| Elhelyezett objektumok (`RIGz`: a renderpéldány-generátor rögzített példányai) | minden példány, 3x4-es mátrixként 16 bites értékekből, vagy egyes pályákon 32 bitesekből (a cella bájtszáma dönt); az ellenőrzött pályákon minden cella minden bájtja elszámolva |
| Generált objektumok (`RIGz` talajosztály-maszkok és a `LandClass` erőforrások) | a játék generátora, átültetve: ugyanazok a helyek, ugyanabban a sorrendben, ugyanazokkal a véletlenszámokkal, a talajosztály- és kizárási maszkok, a helyenként kiválasztott objektum, forgatása, méretezése és magasságeltolása; csempézett (városi tömbök) és ültetett (erdők, bokrok, mezők) entitások. Csak a tankok térképe felett generálva. Közelítve: a talaj magassága és normálja (a magasságtérképből; a játék sugarat követ), a futásidőben a játék által regisztrált kizárási dobozok, és a fák iránya (a játék a bélyegkép forgatási palettájára illeszti). |
| Renderelő hálók (`RendInst` erőforrások a `content/*/res/*.grp`-ben, anyagok a `riDesc.bin`-ben) | minden LOD csúcsai és háromszögei (lebegőpontos pozíciók; 16 vagy 32 bites indexek, sima vagy meshoptimizer-csomagolt), minden elem anyaga. A matrica- és bélyegkép-elemeket kihagyjuk; az áttetszőek (üveg) megmaradnak |
| Objektumszínek | anyagonként, a diffúz textúra kis mipjének átlaga (levelekre alfa-súlyozva), a telepítés textúrcsomagjaiból: a legtöbb árnyalónál a t0, ahol a t0 átfedés vagy maszk, az első részletes diffúz. Anyagonként egy szín: az objektumokon nincs textúra |
| Ütközési alakok (`<object>_collision`) | a 3-as verziójú folyam ütközési erőforrásai, ott használva, ahol az objektumnak nincs renderelő hálója. Csak az látszik, amit a játék sugarai eltalálnak (`TRACEABLE` csomópontok), a dobozok, gömbök és kapszulák pedig csak akkor, ha az erőforrásnak nincs hálója: a többi durva fizikai helyettesítő, amely kockaként látszana az objektum körül |
| Navigációs háló (`Lnav`), a renderelt talajháló, fű, `spgz`, `stbl`, `d2co` | nincs olvasva |

A pályák Oodle-lel vannak tömörítve, ez zárt forráskódú. A játék tartalmaz egy példányt
(`<War Thunder>\win-arm64ec\oo2core_9_win64.dll`, egy szokásos x64 build), és ezt töltjük be;
a `HEAT3D_OODLE=<dll or folder>` másik helyre mutat. Az Oodle-ből semmi sincs ebben a tárolóban.

## Formátumok, és hol vannak dokumentálva {#formats-and-where-they-are-documented}

A Gaijin a Dagor Engine forráskódját BSD 3-Clause licenc alatt tette közzé
(github.com/GaijinEntertainment/DagorEngine). Az itteni olvasók abból készültek; játékkód
nem lett visszafejtve. Minden modul megnevezi a forrásfájlokat, amelyeket követ:

- `vromfs.py`: `*.vromfs.bin` (fejléc `VRFs`/`VRFx`, zstd törzs, amelynek első és utolsó 16
  bájtja egy rögzített kulccsal XOR-olva van, egy névtábla és egy eltolástábla:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) és a bináris
  BLK (1-5-ös formák, az archívum közös névtérképével `\xff?nm` és zstd-szótárral:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: textúrcsomagok `DxP2` (`lib3d/texPackMgr2.cpp`) és DDSx-fejlécek
  (`sharedInclude/3d/ddsxTex.h`); a DXT1/DXT5/BC7-et a Pillow dekódolja.
- `dagorlevel.py`: a pálya bináris fájlja (`scene/loadLevel.cpp`), a magasságtérkép
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), a talaj
  sugárkövetője (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) és a
  vízmagasságtérkép (`fftWater/fftWater.cpp`).
- `rigen.py`: az elhelyezett objektumok (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: a generált objektumok (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: renderpéldányok (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) és a meshoptimizer indexkódeka
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: a talaj színe (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: erőforráscsomagok (`gameRes/grpData.h`) és ütközési erőforrások
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), amelyek
  háromszögei négyszög-BVH-ként vannak tárolva (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

A wt_ext_cli (Apache-2.0) ugyanezeket az archívumokat olvassa; nincs rá szükség, és nem is használjuk.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
