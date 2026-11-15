---
title: "Úrovně (heat3d-wt-level)"
nav_order: 9
lang: cs
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Úrovně (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` převede úrovně z vaší vlastní instalace War Thunderu na `.glb` úrovně pro prohlížeč,
ve stejné soustavě souřadnic jako tabulky replayů.

## Krok za krokem {#step-by-step}

1. Vypište úrovně vaší instalace: `heat3d-wt-level list`. Vypíše jeden řádek na úroveň: její název, terén a její
   mapy, a potom počet. Například (vymyšlená úroveň):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrahujte jednu, několik (zástupné znaky jsou povoleny), nebo všechny:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Načtěte `levels/<level>/<level>.glb` v panelu Pozadí / úroveň prohlížeče, pod bitvami té mapy.

Úrovně, které zapíšete, zůstanou na vašem počítači: nikdy je nezveřejňujte (viz
[Podmínky a licence](terms.md)).

## Volby {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Příkaz / volba | Co dělá |
|---|---|
| `list [--game FOLDER]` | každá úroveň v instalaci |
| `extract <levels...>` / `--all` | jmenované úrovně (tak, jak je vypisuje `list`; zástupné znaky povoleny), nebo každá úroveň |
| `-o`, `--out` | výstupní složka; každá úroveň jde do `<out>/<level>/` |
| `--game FOLDER` | složka War Thunderu (výchozí: nalezena přes Steam nebo spouštěč; také `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | vzorkování terénu, barva terénu a rozpočet objektů nad mapou tanků (výchozí `medium`) |
| `--max-object-triangles N` | rozpočet objektů (výchozí: podle detailu) |
| `--max-grid N` | vzorky výškové mapy na jednu stranu, na část (výchozí 1024) |
| `--no-objects` | vynechat budovy, stromy a jiné umístěné objekty |
| `--no-generated` | vynechat objekty, které generují třídy terénu (lesy, města) |
| `--no-terrain-colour` | potáhnout zemi taktickou mapou, ne třídami terénu |
| `--no-texture` | nechat zem bez textury |
| `--skip-existing` | nechat úrovně, jejichž `.glb` existuje |

## Co se zapisuje {#what-is-written}

Každá úroveň se stane `<out>/<level>/<level>.glb`, `<level>.json` (co se přečetlo, hladina vody, obdélníky map,
počty trojúhelníků, časy) a taktické mapy úrovně jako `<level>_map.png` (letecká mapa) a `<level>_tankmap.png`;
pozemní mapy dostanou také `<level>_terrain.png`, vlastní barvy terénu nad mapou tanků. Soubor glb se zapisuje do
`<level>.glb.part` a po dokončení se přejmenuje; zatímco se úroveň zapisuje, je držen zámek
`<out>/<level>/.<level>.lock`, takže dvě extrakce nikdy nezapisují tutéž úroveň (druhá vypíše `busy <level>`).
Instalace se najde přes Steam nebo výchozí složky spouštěče; jinak řekne, kde je, `--game <folder>` nebo
`HEAT3D_WT_GAME`.

| Část | Co to je |
|---|---|
| `ground:<level>` | výšková mapa terénu (`HM2`) jako mřížka; na pozemních mapách střed mapy tanků (polovina její šířky) s krokem `--detail`, obarvený třídami terénu, pozemními nálepkami a silnicemi (`<level>_terrain.png`; taktická mapa tam, kde to nejde); na mapách bez mapy tanků (letecké mapy) celá výšková mapa v jednom kroku (2048 vzorků na stranu u `high`, jinak 1024), obarvená třídami terénu nad oblastí letecké mapy (4096 pixelů na stranu, asi 32 m na pixel přes 131 km; taktická mapa tam, kde to nejde); na úrovních bez výškové mapy síť terénu |
| `ground:<level> tank map` | zbytek mapy tanků, o jeden krok hrubší |
| `ground:<level> heightmap surroundings` | zbytek výškové mapy, ještě hrubší |
| `ground:<level> land mesh` | kolizní trojúhelníky sítě terénu tam, kde výšková mapa nesahá (okolí mapy tanků, až desítky kilometrů); na úrovních bez výškové mapy je to terén, obarvený jako výše |
| `ground:<level> outside the map` | terén, který obraz nepokrývá, bez textury |
| `water:<level>` | jeden plochý obdélník na `water_level` úrovně přes celý terén: hra kreslí vodu jako jednu plochu a nízký terén pod ní je mořské, jezerní nebo říční dno |
| `water:<level> rivers` | na úrovních s výškovou mapou vody (`WHM`) šikmá vodní hladina nad buňkami, které pokrývá |
| `structure:<level> buildings` | každý umístěný objekt, který není rostlina: domy, ruiny, zdi, ploty, mosty, koleje, skály, rekvizity. Pevné (`RIGz`) a na mapě tanků i ty, které generují třídy terénu (městské bloky, kameny). Každý se kreslí svou renderovací sítí (zdi, střechy, okenní otvory, trámy), na úrovni detailu, kterou rozpočet trojúhelníků dovolí, obarvený podle materiálu průměrem jeho difuzní textury |
| `structure:<level> trees` | stromy a keře, pevné i generované (lesy, živé ploty): jejich renderovací síť, kde to rozpočet dovolí, jinak kmen a koruna (kužel u jehličnanů) v barvě listí daného stromu, v jeho skutečné velikosti |

Objekty bez renderovací sítě se vykreslí svým kolizním tvarem; stromy bez ní korunou. Barvy vrcholů (`COLOR_0`) drží
hodnoty kódované sRGB, jak je čte prohlížeč 3DHeat.

**Souřadnice** jsou metry hry se zrcadlenou osou z: glb (x, y, z) = hra (x, y, -z). Svět hry je levoruký (x na východ,
y nahoru, z na sever); glTF je pravoruký. `heat3d-wt-replay` ponechá z hry a řekne prohlížeči, ať ji zrcadlí, takže
replay a úroveň jeho mapy na sebe dosednou bez kroku umisťování. JSON dává obdélník každé taktické mapy v metrech
hry a její rohy v prostoru glb, pro načtení PNG jako obrazu mapy.

**Detail.** `--detail low|medium|high` (výchozí medium) nastavuje nad mapou tanků:

| | střed mapy tanků | zbytek mapy tanků | barva terénu | rozpočet objektů | nejvíce trojúhelníků na objekt | ponechané generované rostliny |
|---|---|---|---|---|---|---|
| low | každý 4. vzorek | každý 8. | 4 m na pixel | 1,2 M | 1 500 | stromy 35 %, keře 20 % |
| medium | každý 2. | každý 4. | 2 m | 3,5 M | 4 000 | stromy 70 %, keře 50 % |
| high | každý vzorek (na většině pozemních map 2 m) | každý 2. | 1 m (nejvýš 4096 pixelů na stranu) | 4,5 M | 12 000 | všechny |

Oba prstence mapy tanků se drží na 0,3 M (low), 1 M (medium) a 3,7 M (high) trojúhelníků: u map, jejichž výšková
mapa je jemnější než 2 m, se kroky zdvojnásobí (nejdřív vnější prstenec), dokud se nevejdou, takže vyjdou také asi
na 2 m.

Pozemní mapa na `high` vyjde asi na 8 milionů trojúhelníků (3,5 M terénu, 4,5 M objektů) a 250 MB; na `medium` asi
na 4,5 M. LOD objektů jsou ty, které by hra sama vykreslila z jedné vzdálenosti pozorování, nejkratší, jejichž součet se
vejde do rozpočtu: malé rekvizity přecházejí na hrubé LOD jako první a velké budovy poslední, podle rozsahů, které
jejich tvůrci určili pro každé LOD (`lodDistance` v JSONu); co tento krok ušetří nad rozpočet, se vrátí největším
objektům. Hrubá barva terénu (letecké mapy) nejdřív zprůměruje dlaždicové textury každé třídy terénu na velikost
pixelu, aby se dlaždice nerozbily na moaré. Pokud se nevejdou ani nejhrubší LOD, stromy, které ušetří nejvíce,
se stanou korunami, a potom se vynechají nejmenší typy (`leftOut`); žádný objekt se nekreslí jako krabice (kolizní
tvar, je-li nějaký, je vlastní tvar objektu). Generované objekty se řídí deterministicky podle druhu (`density`),
stejné při každém běhu. `--max-object-triangles` přepíše rozpočet, `--max-grid` (výchozí 1024) omezí hrubší části
výškové mapy, `--no-objects` vynechá objekty, `--no-generated` generované, `--no-terrain-colour` potáhne zem
taktickou mapou, `--no-texture` ji nechá bez textury.

JSON `parts.objects` vypisuje instance (pevné i generované, podle druhu a třídy terénu), kolik se jich vykreslilo na
které LOD (`drawnAs`), trojúhelníky, vzdálenost LOD a vteřiny; `parts.heightmap.rings` krok a trojúhelníky každého
prstence terénu; `parts.terrainColour` třídy terénu a jejich barvy, silnice a nálepky; `trianglesTotal`, `glbBytes`
a `secondsBy` celkové součty.

## Co se čte a jak dobře {#what-is-read-and-how-well}

| Část | Stav |
|---|---|
| Binární soubor úrovně (`levels/<level>.bin`, `DBLD` 3x64): tabulka bloků | každá úroveň ověřena |
| Výšková mapa (`HM2`, verze 0-2; verze 2 jsou 8bitové hodnoty v blocích, bloky Oodle nebo zstd) | každá úroveň, jejíž výšková mapa je verze 2 s bloky Oodle; ověřeno okem proti jejich taktickým mapám (řeky, údolí, pobřeží a města sedí) |
| Kolize sítě terénu (`lmap`, jeho sledovač paprsků terénu `LTdump`) | čteno tam, kde úroveň ji má (zabalené Oodle). Je to kolizní povrch hry, ne vykreslená síť, takže je hrubší tam, kde je terén rovný |
| Barva terénu (`lmap` třídy terénu a mapa vah, fyzikální mapa `LMp2`, `hspl` splajny) | barevné mapy tříd terénu a detailní textury (jejich průměrné barvy) vážené mapou vah, 1m biomový index indexovaných tříd terénu, tvary silnic a nálepek země z fyzikální mapy v barvě textury jejich splajnu nebo materiálu, útesy na strmých svazích. Ověřeno proti mapám tanků: silnice, města, jezera, lesní pásy a skalní výchozy sedí. Barevný vzorec terénového shaderu samotného War Thunderu není ve veřejném zdrojovém kódu; použit je publikovaný z enginu (daNetGame), který vychází sytější než taktická mapa |
| Hladina vody | `water_level` z BLK úrovně v `aces.vromfs.bin` (0, když ho nemá) |
| Výšková mapa vody (`WHM`: mřížka plochých buněk a stránek 130x130 16bitových výšek) | čteno tam, kde ji úroveň má; její řeky se svažují s terénem |
| Taktické mapy | z `content/base/res/locations_maps.dxp.bin`, umístěné podle `mapCoord0/1` a `tankMapCoord0/1` v BLK; horní okraj obrazu je sever |
| Umístěné objekty (`RIGz`: pevné instance generátoru instancí vykreslování) | každá instance, jako matice 3x4 16bitových hodnot nebo, na některých úrovních, 32bitových (počet bajtů buňky rozhodne); na ověřených úrovních je každý bajt každé buňky započten |
| Generované objekty (masky tříd terénu `RIGz` a zdroje `LandClass`) | generátor hry, přenesený: stejná místa zkoušená ve stejném pořadí se stejnými náhodnými čísly, masky tříd terénu a vyloučení, objekt vybraný na každém místě, jeho rotace, měřítko a výškový posun; dlaždicové (městské bloky) a zasazené (lesy, keře, pole) entity. Generováno jen nad mapou tanků. Aproximováno: výška a normála terénu (z výškové mapy; hra vysílá paprsek), vylučovací boxy, které hra registruje za běhu, a yaw stromů (hra ho přichytí na paletu rotací impostoru) |
| Renderovací sítě (zdroje `RendInst` v `content/*/res/*.grp`, materiály v `riDesc.bin`) | vrcholy a trojúhelníky každého LOD (pozice v plovoucí čárce; indexy 16 nebo 32bitové, prosté nebo zabalené meshoptimizerem), materiál každého prvku. Prvky nálepek a impostorových billboardů se vynechají; průhledné (sklo) se zachovají |
| Barvy objektů | na materiál průměr malé mip úrovně jeho difuzní textury (u listí vážený alfou), z textur vaší instalace: t0 pro většinu shaderů, první detailní difuzní tam, kde je t0 překryv nebo maska. Jedna barva na materiál: na objektech žádná textura |
| Kolizní tvary (`<object>_collision`) | kolizní zdroje streamu verze 3, použité tam, kde objekt nemá renderovací síť. Kreslí se jen to, do čeho hra trefuje paprsky (uzly `TRACEABLE`), a krabice, koule a kapsle jen tehdy, když zdroj nemá síť: zbytek jsou hrubé fyzikální náhražky, které by se ukázaly jako kostky kolem objektu |
| Navigační síť (`Lnav`), vykreslená síť terénu, tráva, `spgz`, `stbl`, `d2co` | nečteno |

Úrovně jsou komprimované Oodle, což je proprietární. Hra přikládá kopii,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (běžný x64 build), a ta se načte;
`HEAT3D_OODLE=<dll nebo složka>` ukazuje na jinou. Nic z Oodle tu není přiloženo.

## Formáty a kde jsou zdokumentovány {#formats-and-where-they-are-documented}

Gaijin zveřejnil zdrojový kód Dagor Engine pod licencí BSD 3-Clause (github.com/GaijinEntertainment/DagorEngine).
Čtečky tady byly napsány podle něj; žádný herní kód nebyl dekompilován. Každý modul uvádí zdrojové soubory, které
sleduje:

- `vromfs.py`: `*.vromfs.bin` (hlavička `VRFs`/`VRFx`, tělo zstd, jehož prvních a posledních 16 bajtů se XORuje
  pevným klíčem, tabulka názvů a tabulka posunů: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) a binární BLK (formy 1-5, se sdílenou mapou názvů archivu `\xff?nm` a slovníkem zstd:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: balíčky textur `DxP2` (`lib3d/texPackMgr2.cpp`) a hlavičky DDSx (`sharedInclude/3d/ddsxTex.h`);
  DXT1/DXT5/BC7 dekóduje Pillow.
- `dagorlevel.py`: binární soubor úrovně (`scene/loadLevel.cpp`), výšková mapa (`heightmap/heightmapPhysHandler.cpp`,
  `heightMapLand/compressedHeightmap.cpp`), sledovač paprsků terénu (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) a výšková mapa vody (`fftWater/fftWater.cpp`).
- `rigen.py`: umístěné objekty (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generované objekty (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`,
  `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`, `generateCell`),
  `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`,
  `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: renderovací instance (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) a kodek indexů meshoptimizeru
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: barva terénu (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: balíčky zdrojů (`gameRes/grpData.h`) a kolizní zdroje (`sharedInclude/gameRes/collResStream.h`,
  `gameRes/collisionGameResLoad.cpp`), jejichž trojúhelníky jsou uloženy jako BVH čtyřúhelníků (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) čte tytéž archivy; není potřeba a nepoužívá se.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
