---
title: Niveaux (heat3d-wt-level)
nav_order: 9
lang: fr
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Niveaux (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` transforme les niveaux de votre propre installation de War Thunder en niveaux `.glb`
pour la visionneuse, dans le même repère que les tables des replays.

## Étape par étape {#step-by-step}

1. Listez les niveaux de votre installation : `heat3d-wt-level list`. La commande affiche une ligne par
   niveau : son nom, son terrain et ses cartes, puis le nombre. Par exemple (un niveau inventé) :

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extrayez un niveau, plusieurs (les jokers sont permis) ou tous :

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Chargez `levels/<level>/<level>.glb` dans le panneau Arrière-plan / niveau de la visionneuse, sous les batailles
   de cette carte.

Les niveaux que vous écrivez restent sur votre machine : ne les publiez jamais (voir
[Termes et licence](terms.md)).

## Options {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Commande / option | Rôle |
|---|---|
| `list [--game FOLDER]` | chaque niveau de l'installation |
| `extract <levels...>` / `--all` | les niveaux nommés (comme les affiche `list` ; jokers permis), ou tous les niveaux |
| `-o`, `--out` | dossier de sortie ; chaque niveau va dans `<out>/<level>/` |
| `--game FOLDER` | le dossier de War Thunder (par défaut : trouvé par Steam ou le lanceur ; aussi `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | pas du sol, couleur du sol et budget d'objets sur la carte de char (par défaut `medium`) |
| `--max-object-triangles N` | le budget d'objets (par défaut : celui du niveau de détail) |
| `--max-grid N` | échantillons de la carte de hauteur par côté, par partie (par défaut 1024) |
| `--no-objects` | omettre les bâtiments, arbres et autres objets placés |
| `--no-generated` | omettre les objets que génèrent les classes de terrain (forêts, villes) |
| `--no-terrain-colour` | texturer le sol avec la carte tactique, non avec les classes de terrain |
| `--no-texture` | laisser le sol sans texture |
| `--skip-existing` | laisser les niveaux dont le `.glb` existe déjà |

## Ce qui est écrit {#what-is-written}

Chaque niveau devient `<out>/<level>/<level>.glb`, `<level>.json` (ce qui a été lu, le niveau de l'eau, les
rectangles des cartes, les nombres de triangles, les temps) et les cartes tactiques du niveau sous forme de
`<level>_map.png` (la carte aérienne) et `<level>_tankmap.png` ; les cartes au sol reçoivent aussi
`<level>_terrain.png`, les couleurs propres au sol par-dessus la carte de char. Le glb est écrit dans
`<level>.glb.part` puis renommé une fois terminé ; pendant l'écriture d'un niveau, `<out>/<level>/.<level>.lock`
est maintenu, de sorte que deux extractions n'écrivent jamais le même niveau (la seconde affiche
`busy <level>`). L'installation est trouvée grâce à Steam ou aux dossiers par défaut du lanceur ;
`--game <dossier>` ou `HEAT3D_WT_GAME` indiquent où elle se trouve sinon.

| Partie | Ce que c'est |
|---|---|
| `ground:<level>` | la carte de hauteur du terrain (`HM2`) sous forme de grille ; sur les cartes au sol, le milieu de la carte de char (la moitié de sa largeur) au pas de `--detail`, coloré avec les classes de terrain, les décalcomanies de sol et les routes (`<level>_terrain.png` ; la carte tactique là où cela ne peut pas se faire) ; sur les cartes sans carte de char (cartes aériennes), toute la carte de hauteur à un seul pas (2048 échantillons par côté en `high`, 1024 sinon), colorée avec les classes de terrain sur la zone de la carte aérienne (4096 pixels par côté, environ 32 m par pixel sur 131 km ; la carte tactique là où cela ne peut pas se faire) ; sur les niveaux sans carte de hauteur, le maillage du terrain |
| `ground:<level> tank map` | le reste de la carte de char, un pas plus grossier |
| `ground:<level> heightmap surroundings` | le reste de la carte de hauteur, encore plus grossier |
| `ground:<level> land mesh` | les triangles de collision du maillage du terrain là où la carte de hauteur n'atteint pas (les abords d'une carte de char, jusqu'à des dizaines de kilomètres) ; sur les niveaux sans carte de hauteur, c'est le sol, coloré comme ci-dessus |
| `ground:<level> outside the map` | le sol que l'image ne couvre pas, sans texture |
| `water:<level>` | un rectangle plat au `water_level` du niveau sur tout le terrain : le jeu dessine l'eau comme un seul plan, et le sol bas situé dessous est mer, lac ou lit de rivière |
| `water:<level> rivers` | sur les niveaux qui ont une carte de hauteur d'eau (`WHM`), la surface d'eau en pente sur les cellules qu'elle couvre |
| `structure:<level> buildings` | chaque objet placé qui n'est pas une plante : maisons, ruines, murs, clôtures, ponts, rails, rochers, accessoires. Les objets fixes (`RIGz`) et, sur la carte de char, ceux que génèrent les classes de terrain (blocs de villes, pierres). Chacun est dessiné par son maillage de rendu (murs, toits, ouvertures de fenêtres, poutres), au niveau de détail que permet le budget de triangles, coloré par matériau selon la moyenne de sa texture diffuse |
| `structure:<level> trees` | arbres et buissons, fixes et générés (forêts, haies) : leur maillage de rendu quand le budget le permet, sinon un tronc et une couronne (un cône pour les conifères) dans la couleur de feuillage propre à l'arbre, à sa taille réelle |

Les objets sans maillage de rendu reprennent leur forme de collision ; les arbres sans maillage prennent la
couronne. Les couleurs de sommet (`COLOR_0`) contiennent des valeurs encodées en sRGB, ce que la visionneuse
3DHeat lit ainsi.

**Coordonnées.** Ce sont les mètres du jeu avec z retourné : glb (x, y, z) = jeu (x, y, -z). Le monde du jeu
est gaucher (x est, y haut, z nord) ; glTF est droitier. `heat3d-wt-replay` garde le z du jeu et indique à la
visionneuse de le retourner, de sorte qu'un replay et le niveau de sa carte se superposent sans étape de
placement. Le JSON donne le rectangle de chaque carte tactique en mètres du jeu et ses coins dans l'espace du
glb, pour charger le PNG comme image de carte.

**Détail.** `--detail low|medium|high` (par défaut medium) règle, sur la carte de char :

| | milieu de la carte de char | reste de la carte de char | couleur du sol | budget d'objets | triangles max par objet | plantes générées conservées |
|---|---|---|---|---|---|---|
| low | un échantillon sur 4 | un sur 8 | 4 m par pixel | 1,2 M | 1 500 | arbres 35 %, buissons 20 % |
| medium | un sur 2 | un sur 4 | 2 m | 3,5 M | 4 000 | arbres 70 %, buissons 50 % |
| high | chaque échantillon (2 m sur la plupart des cartes au sol) | un sur 2 | 1 m (4096 pixels par côté au plus) | 4,5 M | 12 000 | toutes |

Les deux anneaux de la carte de char sont contenus dans 0,3 M (low), 1 M (medium) et 3,7 M (high) de
triangles : sur les cartes dont la carte de hauteur est plus fine que 2 m, les pas doublent (l'anneau
extérieur d'abord) jusqu'à rentrer, de sorte qu'ils ressortent eux aussi à environ 2 m.

Une carte au sol en `high` donne environ 8 millions de triangles (3,5 M de sol, 4,5 M d'objets) et 250 Mo ; en
`medium`, environ 4,5 M. Les LOD des objets sont ceux que le jeu lui-même dessinerait depuis une seule distance
de vue, le plus court dont le total tient dans le budget : les petits accessoires passent d'abord aux LOD
grossiers et les grands bâtiments en dernier, selon les distances que leurs auteurs ont données à chaque LOD
(`lodDistance` du JSON) ; ce que cette étape économise au-delà du budget revient aux plus grands objets. La
couleur grossière du sol (cartes aériennes) moyenne d'abord les textures en tuiles de chaque classe de terrain
à la taille du pixel, pour que les tuiles ne créent pas de moiré. Si même les LOD les plus grossiers ne tiennent
pas, les arbres qui économisent le plus deviennent des couronnes, puis les plus petits types sont omis
(`leftOut`) ; aucun objet n'est dessiné comme une boîte (une forme de collision, s'il y en a une, est celle de
l'objet lui-même). Les objets générés sont éclaircis de façon déterministe selon leur genre (`density`), les
mêmes à chaque exécution. `--max-object-triangles` remplace le budget, `--max-grid` (par défaut 1024) plafonne
les parties plus grossières de la carte de hauteur, `--no-objects` omet les objets, `--no-generated` les
objets générés, `--no-terrain-colour` texture le sol avec la carte tactique, `--no-texture` le laisse sans texture.

Le JSON `parts.objects` liste les instances (fixes et générées, par genre et classe de terrain), combien ont été
dessinées à quel LOD (`drawnAs`), les triangles, la distance de LOD et les secondes ; `parts.heightmap.rings`
donne le pas et les triangles de chaque anneau du sol ; `parts.terrainColour` les classes de terrain et leurs
couleurs, routes et décalcomanies de sol ; `trianglesTotal`, `glbBytes` et `secondsBy` les totaux.

## Ce qui est lu, et dans quelle mesure {#what-is-read-and-how-well}

| Partie | État |
|---|---|
| Binaire du niveau (`levels/<level>.bin`, `DBLD` 3x64) : table des blocs | chaque niveau vérifié |
| Carte de hauteur (`HM2`, versions 0-2 ; la version 2 contient des valeurs sur 8 bits en blocs, des morceaux Oodle ou zstd) | chaque niveau dont la carte de hauteur est en version 2 avec des morceaux Oodle ; vérifié à l'œil par rapport à leurs cartes tactiques (rivières, vallées, côtes et villes s'alignent) |
| Collision du maillage du terrain (`lmap`, son lancer de rayons `LTdump`) | lu là où un niveau en a un (compressé en Oodle). C'est la surface de collision du jeu, non le maillage rendu ; elle est donc plus grossière là où le terrain est plat |
| Couleur du sol (classes de terrain et carte de poids de `lmap`, carte physique `LMp2`, `hspl` splines) | les cartes de couleur des classes de terrain et leurs textures de détail (leurs couleurs moyennes), pondérées par la carte de poids, l'index de biome au mètre des classes de terrain indexées, les formes des routes et des décalcomanies de sol de la carte physique, à la couleur de la texture de leur spline ou matériau, falaises sur les pentes raides. Vérifié par rapport aux cartes de char : routes, villes, lacs, bandes forestières et affleurements rocheux s'alignent. La formule de couleur du shader de terrain de War Thunder n'est pas dans le code source public ; celle, publiée, du moteur (daNetGame) est utilisée, qui donne un rendu plus saturé que la carte tactique |
| Niveau de l'eau | `water_level` du BLK du niveau dans `aces.vromfs.bin` (0 là où il n'en a pas) |
| Carte de hauteur d'eau (`WHM` : une grille de cellules plates et des pages 130x130 de hauteurs sur 16 bits) | lue là où un niveau en a une ; ses rivières suivent la pente du sol |
| Cartes tactiques | depuis `content/base/res/locations_maps.dxp.bin`, placées selon `mapCoord0/1` et `tankMapCoord0/1` du BLK ; le haut de l'image est le nord |
| Objets placés (`RIGz` : les instances fixes du générateur d'instances de rendu) | chaque instance, sous forme de matrice 3x4 de valeurs sur 16 bits ou, sur certains niveaux, sur 32 bits (le nombre d'octets de la cellule décide) ; chaque octet de chaque cellule est comptabilisé sur les niveaux vérifiés |
| Objets générés (masques de classes de terrain de `RIGz` et ressources `LandClass`) | le générateur du jeu, porté : mêmes emplacements essayés dans le même ordre avec les mêmes nombres aléatoires, les masques de classes de terrain et d'exclusion, l'objet choisi à chaque emplacement, sa rotation, son échelle et son décalage de hauteur ; entités en tuiles (blocs de villes) et plantées (forêts, buissons, champs). Généré sur la carte de char seulement. Approximations : la hauteur et la normale du sol (depuis la carte de hauteur ; le jeu trace un rayon), les boîtes d'exclusion que le jeu enregistre à l'exécution, et l'orientation des arbres (le jeu l'aligne sur la palette de rotation de l'imposteur) |
| Maillages de rendu (ressources `RendInst` dans `content/*/res/*.grp`, matériaux dans `riDesc.bin`) | les sommets et triangles de chaque LOD (positions en flottants ; index sur 16 ou 32 bits, simples ou compressés par meshoptimizer), le matériau de chaque élément. Les éléments de décalcomanie et de panneau-impostor sont omis ; les éléments transparents (verre) sont conservés |
| Couleurs des objets | par matériau, la moyenne du petit mip de sa texture diffuse (pondérée par l'alpha pour les feuilles), issue des paquets de textures de l'installation : t0 pour la plupart des shaders, la première diffuse de détail là où t0 est une superposition ou un masque. Une couleur par matériau : aucune texture sur les objets |
| Formes de collision (`<object>_collision`) | ressources de collision de la version de flux 3, utilisées là où un objet n'a pas de maillage de rendu. Seul ce que touchent les rayons du jeu (nœuds `TRACEABLE`) est dessiné, et les boîtes, sphères et capsules seulement lorsque la ressource n'a pas de maillage : le reste sont des substituts physiques grossiers qui apparaîtraient comme des cubes autour de l'objet |
| Maillage de navigation (`Lnav`), maillage de terrain rendu, herbe, `spgz`, `stbl`, `d2co` | non lus |

Les niveaux sont compressés avec Oodle, qui est propriétaire. Le jeu en livre une copie,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (une version x64 ordinaire), et c'est celle qui est chargée ;
`HEAT3D_OODLE=<dll ou dossier>` désigne une autre copie. Rien d'Oodle n'est inclus ici.

## Formats, et où ils sont documentés {#formats-and-where-they-are-documented}

Gaijin a publié le code source du Dagor Engine sous licence BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Les lecteurs d'ici ont été écrits à partir de lui ; aucun code du
jeu n'a été décompilé. Chaque module nomme les fichiers source qu'il suit :

- `vromfs.py` : `*.vromfs.bin` (en-tête `VRFs`/`VRFx`, un corps zstd dont les 16 premiers et derniers octets
  sont combinés en XOR avec une clé fixe, une table de noms et une table de décalages :
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) et BLK binaire (formes 1-5,
  avec la table de noms partagée de l'archive `\xff?nm` et le dictionnaire zstd :
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py` : paquets de textures `DxP2` (`lib3d/texPackMgr2.cpp`) et en-têtes DDSx (`sharedInclude/3d/ddsxTex.h`) ;
  DXT1/DXT5/BC7 sont décodés par Pillow.
- `dagorlevel.py` : le binaire du niveau (`scene/loadLevel.cpp`), la carte de hauteur
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), le lancer de rayons du terrain
  (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) et la carte de hauteur d'eau
  (`fftWater/fftWater.cpp`).
- `rigen.py` : les objets placés (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py` : les objets générés (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`,
  `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py` : instances de rendu (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) et le codec d'index de meshoptimizer
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py` : la couleur du sol (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py` : paquets de ressources (`gameRes/grpData.h`) et ressources de collision
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), dont les triangles sont stockés
  comme un BVH de quadrilatères (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) lit les mêmes archives ; il n'est ni nécessaire ni utilisé.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
