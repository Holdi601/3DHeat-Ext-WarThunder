---
title: "Levely"
nav_order: 9
lang: "sk"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Levely (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` premení levely z vašej vlastnej inštalácie War Thunderu na `.glb` levely pre prehliadač, v tom istom
súradnicovom systéme ako tabuľky replayov.

## Krok za krokom {#step-by-step}

1. Vypíšte levely vo vašej inštalácii: `heat3d-wt-level list`. Vypíše jeden riadok na level: jeho názov, jeho terén
   a jeho mapy, potom počet. Napríklad (vymyslený level):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Rozbaľte jeden, niekoľko (zástupné znaky sú povolené) alebo všetky:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Načítajte `levels/<level>/<level>.glb` do panelu Pozadie / level v prehliadači, pod bitky tej mapy.

Levely, ktoré zapíšete, zostávajú vo vašom počítači: nikdy ich nezverejňujte (pozri
[Podmienky a licencia](terms.md)).

## Možnosti {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Príkaz / možnosť | Čo robí |
|---|---|
| `list [--game FOLDER]` | každý level v inštalácii |
| `extract <levels...>` / `--all` | pomenované levely (tak, ako ich vypíše `list`; zástupné znaky sú povolené), alebo všetky levely |
| `-o`, `--out` | výstupný priečinok; každý level ide do `<out>/<level>/` |
| `--game FOLDER` | priečinok War Thunderu (predvolene: nájde sa cez Steam alebo spúšťač; aj `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | vzorkovanie terénu, farba terénu a rozpočet objektov nad mapou tankov (predvolene `medium`) |
| `--max-object-triangles N` | rozpočet objektov (predvolene podľa úrovne detailu) |
| `--max-grid N` | vzorky výškovej mapy na jednu stranu, na časť (predvolene 1024) |
| `--no-objects` | nevynechať budovy, stromy a iné umiestnené objekty |
| `--no-generated` | vynechať objekty, ktoré generujú triedy terénu (lesy, mestá) |
| `--no-terrain-colour` | obaliť zem taktickou mapou, nie triedami terénu |
| `--no-texture` | nechať zem bez textúry |
| `--skip-existing` | nechať levely, ktorých `.glb` existuje |

## Čo sa zapisuje {#what-is-written}

Každý level sa stane `<out>/<level>/<level>.glb`, `<level>.json` (čo sa prečítalo, výška hladiny vody, obdĺžniky
máp, počty trojuholníkov, časy) a taktické mapy levelu ako `<level>_map.png` (vzdušná mapa) a `<level>_tankmap.png`;
pozemné mapy dostanú aj `<level>_terrain.png`, vlastné farby zeme nad mapou tankov. Glb sa zapisuje do
`<level>.glb.part` a po dokončení sa premenuje; kým sa level zapisuje, drží sa `<out>/<level>/.<level>.lock`, takže
dve extrakcie nikdy nezapisujú ten istý level (druhá vypíše `busy <level>`). Inštalácia sa hľadá cez Steam alebo
predvolené priečinky spúšťača; inak to povie `--game <priečinok>` alebo `HEAT3D_WT_GAME`.

| Časť | Čo je |
|---|---|
| `ground:<level>` | výškovú mapu terénu (`HM2`) ako mriežku; na pozemných mapách stred mapy tankov (polovica jej šírky) s krokom `--detail`, obarvený triedami terénu, pozemnými nánosmi a cestami (`<level>_terrain.png`; taktická mapa, kde to nejde); na mapách bez mapy tankov (vzdušné mapy) celá výšková mapa v jednom kroku (2048 vzoriek na stranu pri `high`, inak 1024), obarvená triedami terénu nad oblasťou vzdušnej mapy (4096 pixelov na stranu, asi 32 m na pixel na 131 km; taktická mapa, kde to nejde); na levelech bez výškovej mapy zemný mesh |
| `ground:<level> tank map` | zvyšok mapy tankov, o jeden krok hrubší |
| `ground:<level> heightmap surroundings` | zvyšok výškovej mapy, ešte hrubší |
| `ground:<level> land mesh` | kolízne trojuholníky zemného meshu tam, kde výšková mapa nedosahuje (okolie mapy tankov, do desiatok kilometrov); na levelech bez výškovej mapy je to zem, obarvená ako vyššie |
| `ground:<level> outside the map` | zem, ktorú obrázok nepokrýva, bez textúry |
| `water:<level>` | jeden plochý obdĺžnik vo výške `water_level` levelu nad celým terénom: hra kreslí vodu ako jednu rovinu a nízka zem pod ňou je more, jazero alebo koryto rieky |
| `water:<level> rivers` | na levelech s výškovou mapou vody (`WHM`) šikmá vodná hladina nad bunkami, ktoré pokrýva |
| `structure:<level> buildings` | každý umiestnený objekt, ktorý nie je rastlina: domy, ruiny, steny, ploty, mosty, koľajnice, skaly, rekvizity. Pevné (`RIGz`) a tie, ktoré nad mapou tankov generujú triedy terénu (mestské bloky, kamene). Každý sa kreslí svojím renderovacím meshom (steny, strechy, okenné otvory, trámy), na úrovni LOD, ktorú dovolí rozpočet trojuholníkov, a farbí sa podľa materiálu priemerom jeho difúznej textúry |
| `structure:<level> trees` | stromy a kríky, pevné aj generované (lesy, živé ploty): ich renderovací mesh, kde to rozpočet dovolí, inak kmeň a koruna (kužeľ pri ihličnanoch) vo farbe listu daného stromu, v jeho skutočnej veľkosti |

Objekty bez renderovacieho meshu majú náhradu v tvare kolízie; stromy bez neho v korune. Farby vrcholov (`COLOR_0`)
držia hodnoty kódované v sRGB, tak ich číta 3DHeat prehliadač.

**Súradnice** sú metre hry so zrkadlením z: glb (x, y, z) = hra (x, y, -z). Svet hry je ľavotočivý (x na východ, y nahor,
z na sever); glTF je pravotočivý. `heat3d-wt-replay` ponecháva z hry a hovorí prehliadaču, aby ju zrkadlil, takže replay
a level jeho mapy na seba dopadnú bez kroku umiestňovania. JSON dáva obdĺžnik každej taktickej mapy v metroch hry a jej rohy
v priestore glb, aby sa PNG dalo načítať ako obrázok mapy.

**Detail.** `--detail low|medium|high` (predvolene medium) nastavuje nad mapou tankov:

| | stred mapy tankov | zvyšok mapy tankov | farba terénu | rozpočet objektov | najviac trojuholníkov na objekt | zachované generované rastliny |
|---|---|---|---|---|---|---|
| low | každá 4. vzorka | každá 8. | 4 m na pixel | 1,2 M | 1 500 | stromy 35 %, kríky 20 % |
| medium | každá 2. | každá 4. | 2 m | 3,5 M | 4 000 | stromy 70 %, kríky 50 % |
| high | každá vzorka (2 m na väčšine pozemných máp) | každá 2. | 1 m (najviac 4096 pixelov na stranu) | 4,5 M | 12 000 | všetky |

Dva prstence mapy tankov sú obmedzené na 0,3 M (low), 1 M (medium) a 3,7 M (high) trojuholníkov: na mapách, ktorých
výšková mapa je jemnejšia ako 2 m, sa kroky zdvojnásobia (najprv vonkajší prstenec), kým sa nevojdú, takže vyjdú tiež
asi na 2 m.

Pozemná mapa pri `high` vyjde asi na 8 miliónov trojuholníkov (3,5 M terénu, 4,5 M objektov) a 250 MB; pri `medium` asi
na 4,5 M. LOD objektov sú tie, ktoré by hra sama kreslila z jednej vzdialenosti pozerania, najkratšie, ktorých súčet sa
vojde do rozpočtu: malé rekvizity prvé klesajú na hrubé LOD, veľké budovy posledné, podľa rozsahov, ktoré ich tvorcovia
dali každému LOD (`lodDistance` v JSON); to, čo tento krok ušetrí nad rozpočet, sa vráti najväčším objektom. Hrubá farba
terénu (vzdušné mapy) najprv spriemeruje dlaždicové textúry každej triedy terénu na veľkosť pixela, aby sa dlaždice
nepremietli do moaré. Ak sa nevojdú ani najhrubšie LOD, stromy, ktoré ušetria najviac, sa stanú korunami a potom sa
vynechajú najmenšie typy (`leftOut`); žiadny objekt sa nekreslí ako škatuľa (kolízny tvar, ak existuje, je vlastný
tvar objektu). Generované objekty sa prerieďujú deterministicky podľa druhu (`density`), tie isté pri každom spustení.
`--max-object-triangles` prepíše rozpočet, `--max-grid` (predvolene 1024) obmedzuje hrubšie časti výškovej mapy,
`--no-objects` vynechá objekty, `--no-generated` generované, `--no-terrain-colour` obalí zem taktickou mapou a
`--no-texture` ju nechá bez textúry.

Pole `parts.objects` v JSON uvádza inštancie (pevné aj generované, podľa druhu a triedy terénu), koľko ich bolo nakreslených
na akom LOD (`drawnAs`), trojuholníky, vzdialenosť LOD a sekundy; `parts.heightmap.rings` krok a trojuholníky každého
prstenca zeme; `parts.terrainColour` triedy terénu a ich farby, cesty a pozemné nánosy; `trianglesTotal`, `glbBytes` a
`secondsBy` súčty.

## Čo sa číta a ako dobre {#what-is-read-and-how-well}

| Časť | Stav |
|---|---|
| Binárny súbor levelu (`levels/<level>.bin`, `DBLD` 3x64): tabuľka blokov | každý level overený |
| Výšková mapa (`HM2`, verzie 0-2; verzia 2 sú 8-bitové hodnoty v blokoch, Oodle alebo zstd časti) | každý level, ktorého výšková mapa je verzie 2 s Oodle časťami; overené okom oproti ich taktickým mapám (rieky, údolia, pobrežia a mestá sedia) |
| Kolízia zemného meshu (`lmap`, jeho `LTdump` sledovač lúčov terénu) | čítané tam, kde ju level má (zabalené Oodle). Je to kolízny povrch hry, nie vykreslený mesh, takže je hrubší tam, kde je zem rovná |
| Farba terénu (`lmap` triedy terénu a váhová mapa, `LMp2` fyzikálna mapa, `hspl` splajny) | farebné mapy tried terénu a detailné textúry (ich priemerné farby) vážené váhovou mapou, 1 m biómový index indexovaných tried terénu, tvary ciest a pozemných nánosov z fyzikálnej mapy vo farbe textúry ich splajnu alebo materiálu, útesy na strmých svahoch. Overené oproti mapám tankov: cesty, mestá, jazerá, pásy lesov a skalné výchozy sedia. Vzorec farby vlastného shadera terénu War Thunderu nie je vo verejnom zdroji; použitý je verejný vzorec motora (daNetGame), ktorý vychádza sýtejší ako taktická mapa |
| Výška hladiny vody | `water_level` z BLK levelu v `aces.vromfs.bin` (0, ak ho nemá) |
| Výšková mapa vody (`WHM`: mriežka plochých buniek a 130x130 strán 16-bitových výšok) | čítané tam, kde ju level má; jeho rieky klesajú s terénom |
| Taktické mapy | z `content/base/res/locations_maps.dxp.bin`, umiestnené podľa `mapCoord0/1` a `tankMapCoord0/1` z BLK; vrch obrázka je sever |
| Umiestnené objekty (`RIGz`: pevné inštancie generátora renderových inštancií) | každá inštancia ako matica 3x4 hodnôt po 16 bitoch, alebo na niektorých levelech po 32 bitoch (počet bajtov bunky rozhodne); každý bajt každej bunky sa počíta na skontrolovaných levelech |
| Generované objekty (`RIGz` masky tried terénu a zdroje `LandClass`) | generátor hry, prenesený: tie isté miesta, skúšané v tom istom poradí s tými istými náhodnými číslami, masky tried terénu a vylúčenia, objekt vybraný na každom mieste, jeho otočenie, mierka a výškový posun; entity dlaždíc (mestské bloky) a sadené (lesy, kríky, polia). Generované len nad mapou tankov. Aproximované: výška a normála terénu (z výškovej mapy; hra sleduje lúč), vylučovacie boxy, ktoré hra registruje za behu, a natočenie stromov (hra ho prichytí na paletu rotácií impostora). |
| Renderovacie meshe (zdroje `RendInst` v `content/*/res/*.grp`, materiály v `riDesc.bin`) | vrcholy a trojuholníky každého LOD (float pozície; indexy 16 alebo 32 bitov, obyčajné alebo zabalené meshoptimizerom), materiál každého prvku. Prvky dekálov a impostorových bilboardov sa vynechávajú; priehľadné (sklo) sa zachovávajú |
| Farby objektov | na materiál priemer malej mipmapy difúznej textúry (vážený alfou pri listoch), z textúrových balíkov inštalácie: t0 pre väčšinu shaderov, prvá detailná difúzna, kde je t0 prekryv alebo maska. Jedna farba na materiál: na objektoch žiadna textúra |
| Kolízne tvary (`<object>_collision`) | kolízne zdroje streamu verzie 3, použité tam, kde objekt nemá renderovací mesh. Kreslí sa len to, do čoho hra zasahuje lúčmi (uzly `TRACEABLE`), a škatule, gule a kapsule len keď zdroj nemá mesh: ostatné sú hrubé fyzikálne náhrady, ktoré by sa ukázali ako kocky okolo objektu |
| Navigačný mesh (`Lnav`), vykreslený zemný mesh, tráva, `spgz`, `stbl`, `d2co` | nečítajú sa |

Levely sú komprimované Oodle, ktorý je proprietárny. Hra obsahuje jeho kópiu,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (obyčajný x64 build), a tá sa načítava;
`HEAT3D_OODLE=<dll alebo priečinok>` ukazuje na inú. Nič z Oodle tu nie je.

## Formáty a kde sú zdokumentované {#formats-and-where-they-are-documented}

Gaijin zverejnil zdroj Dagor Engine pod licenciou BSD 3-Clause (github.com/GaijinEntertainment/DagorEngine). Čítačky
tu boli napísané podľa neho; žiadny herný kód nebol dekompilovaný. Každý modul uvádza zdrojové súbory, ktoré nasleduje:

- `vromfs.py`: `*.vromfs.bin` (hlavička `VRFs`/`VRFx`, telo zstd, ktorého prvých a posledných 16 bajtov sa XORuje pevným kľúčom,
  tabuľka mien a tabuľka posunov: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  a binárny BLK (formy 1-5, so zdieľanou mapou mien archívu `\xff?nm` a zstd slovníkom:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: textúrové balíky `DxP2` (`lib3d/texPackMgr2.cpp`) a hlavičky DDSx (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7
  dekóduje Pillow.
- `dagorlevel.py`: binárny súbor levelu (`scene/loadLevel.cpp`), výšková mapa (`heightmap/heightmapPhysHandler.cpp`,
  `heightMapLand/compressedHeightmap.cpp`), sledovač lúčov terénu (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) a výšková mapa vody (`fftWater/fftWater.cpp`).
- `rigen.py`: umiestnené objekty (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generované objekty (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`,
  `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`,
  `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: renderovacie inštancie (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`,
  `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`,
  `gameRes/gameResDescBin.cpp`) a kodek indexov meshoptimizera (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: farba terénu (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: balíky zdrojov (`gameRes/grpData.h`) a kolízne zdroje (`sharedInclude/gameRes/collResStream.h`,
  `gameRes/collisionGameResLoad.cpp`), ktorých trojuholníky sú uložené ako štvorcový BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) číta tie isté archívy; nie je potrebný a nepoužíva sa.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
