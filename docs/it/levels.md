---
title: "Livelli"
nav_order: 9
lang: "it"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Livelli (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` trasforma i livelli della tua installazione di War Thunder in livelli `.glb` per il visualizzatore, nello stesso sistema di riferimento delle tabelle dei replay.

## Passo dopo passo {#step-by-step}

1. Elenca i livelli della tua installazione: `heat3d-wt-level list`. Stampa una riga per livello: il suo nome, il suo terreno e le sue mappe, poi il conteggio. Per esempio (un livello inventato):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Estrai uno, più d'uno (sono ammessi i caratteri jolly) o tutti:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Carica `levels/<level>/<level>.glb` nel pannello Sfondo / livello del visualizzatore, sotto le battaglie di quella mappa.

I livelli che scrivi restano sul tuo computer: non pubblicarli mai (vedi [Condizioni e licenza](terms.md)).

## Opzioni {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Comando / opzione | Cosa fa |
|---|---|
| `list [--game FOLDER]` | ogni livello dell'installazione |
| `extract <levels...>` / `--all` | i livelli nominati (come li stampa `list`; sono ammessi i caratteri jolly), oppure ogni livello |
| `-o`, `--out` | cartella di output; ogni livello va in `<out>/<level>/` |
| `--game FOLDER` | la cartella di War Thunder (predefinita: trovata tramite Steam o il launcher; anche `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | campionatura del terreno, colore del terreno e budget degli oggetti sulla mappa dei carri (predefinito `medium`) |
| `--max-object-triangles N` | il budget degli oggetti (predefinito: quello del dettaglio) |
| `--max-grid N` | campioni della heightmap per lato, per parte (predefinito 1024) |
| `--no-objects` | lascia fuori edifici, alberi e altri oggetti posati |
| `--no-generated` | lascia fuori gli oggetti che generano le classi di terreno (foreste, città) |
| `--no-terrain-colour` | riveste il terreno con la mappa tattica, non con le classi di terreno |
| `--no-texture` | lascia il terreno senza texture |
| `--skip-existing` | lascia i livelli il cui `.glb` esiste già |

## Cosa viene scritto {#what-is-written}

Ogni livello diventa `<out>/<level>/<level>.glb`, `<level>.json` (ciò che è stato letto, il livello dell'acqua, i rettangoli delle mappe, i conteggi dei triangoli, i tempi) e le mappe tattiche del livello come `<level>_map.png` (la mappa aerea) e `<level>_tankmap.png`; le mappe di terra ricevono anche `<level>_terrain.png`, i colori del terreno stesso sopra la mappa dei carri. Il glb viene scritto in `<level>.glb.part` e rinominato quando è completo; mentre un livello viene scritto, `<out>/<level>/.<level>.lock` è tenuto, così due estrazioni non scrivono mai lo stesso livello (la seconda stampa `busy <level>`). L'installazione viene trovata tramite Steam o le cartelle predefinite del launcher; `--game <cartella>` o `HEAT3D_WT_GAME` indicano dove si trova se non la trova da sola.

| Parte | Cos'è |
|---|---|
| `ground:<level>` | la heightmap del terreno (`HM2`) come griglia; sulle mappe di terra il centro della mappa dei carri (metà della sua larghezza) al passo di `--detail`, colorato con le classi di terreno, le decalcomanie del suolo e le strade (`<level>_terrain.png`; la mappa tattica dove non si può fare); sulle mappe senza mappa dei carri (mappe aeree), l'intera heightmap a un solo passo (2048 campioni per lato con `high`, 1024 altrimenti), colorata con le classi di terreno sull'area della mappa aerea (4096 pixel per lato, circa 32 m per pixel su 131 km; la mappa tattica dove non si può fare); sui livelli senza heightmap, la land mesh |
| `ground:<level> tank map` | il resto della mappa dei carri, un passo più grossolano |
| `ground:<level> heightmap surroundings` | il resto della heightmap, ancora più grossolano |
| `ground:<level> land mesh` | i triangoli di collisione della land mesh dove la heightmap non arriva (i dintorni di una mappa dei carri, fino a decine di chilometri); sui livelli senza heightmap è il terreno, colorato come sopra |
| `ground:<level> outside the map` | terreno che l'immagine non copre, senza texture |
| `water:<level>` | un unico rettangolo piatto al `water_level` del livello su tutto il terreno: il gioco disegna l'acqua come un unico piano, e il terreno basso sotto di essa è mare, lago o letto di fiume |
| `water:<level> rivers` | sui livelli con una heightmap dell'acqua (`WHM`), la superficie d'acqua in pendenza sulle celle che copre |
| `structure:<level> buildings` | ogni oggetto posato che non è una pianta: case, rovine, muri, recinzioni, ponti, binari, rocce, oggetti di scena. Quelli fissi (`RIGz`) e, sulla mappa dei carri, quelli che generano le classi di terreno (isolati cittadini, pietre). Ognuno è disegnato con la sua mesh di render (muri, tetti, aperture delle finestre, travi), al LOD che consente il budget dei triangoli, colorato per materiale con la media della sua texture diffusa |
| `structure:<level> trees` | alberi e cespugli, fissi e generati (foreste, siepi): la loro mesh di render dove il budget lo consente, altrimenti un tronco e una chioma (un cono per le conifere) nel colore fogliare proprio dell'albero, alla sua dimensione reale |

Gli oggetti senza mesh di render ricadono sulla loro forma di collisione; gli alberi senza una, sulla chioma. I colori dei vertici (`COLOR_0`) contengono valori codificati sRGB, che è il modo in cui il visualizzatore 3DHeat li legge.

Le **coordinate** sono i metri del gioco con z specchiato: glb (x, y, z) = gioco (x, y, -z). Il mondo del gioco è sinistrorso (x est, y su, z nord); glTF è destrorso. `heat3d-wt-replay` mantiene la z del gioco e dice al visualizzatore di specchiarla, così un replay e il livello della sua mappa cadono uno sopra l'altro senza nessun passo di posizionamento. Il JSON dà il rettangolo di ogni mappa tattica in metri di gioco e i suoi angoli nello spazio del glb, per caricare il PNG come immagine di mappa.

**Dettaglio.** `--detail low|medium|high` (predefinito medium) imposta, sulla mappa dei carri:

| | centro della mappa dei carri | resto della mappa dei carri | colore del terreno | budget degli oggetti | triangoli massimi per oggetto | piante generate mantenute |
|---|---|---|---|---|---|---|
| low | ogni 4° campione | ogni 8° | 4 m per pixel | 1,2 M | 1.500 | alberi 35 %, cespugli 20 % |
| medium | ogni 2° | ogni 4° | 2 m | 3,5 M | 4.000 | alberi 70 %, cespugli 50 % |
| high | ogni campione (2 m sulla maggior parte delle mappe di terra) | ogni 2° | 1 m (al massimo 4096 pixel per lato) | 4,5 M | 12.000 | tutte |

I due anelli della mappa dei carri sono tenuti entro 0,3 M (low), 1 M (medium) e 3,7 M (high)
triangoli: sulle mappe la cui heightmap è più fine di 2 m, i passi raddoppiano
(prima l'anello esterno) finché non entrano, così anche quelle escono a circa 2 m.

Una mappa di terra con `high` esce a circa 8 milioni di triangoli (3,5 M di terreno,
4,5 M di oggetti) e 250 MB; con `medium` a circa 4,5 M. I LOD degli oggetti sono quelli che il gioco stesso disegnerebbe da una sola distanza di vista, il più corto
il cui totale rientra nel budget: i piccoli oggetti di scena scendono per primi a LOD grossolani e i grandi edifici per ultimi, secondo le distanze che i loro autori hanno dato a ogni LOD (`lodDistance` del JSON); ciò che quel passo fa risparmiare oltre il budget torna agli oggetti più grandi. Il colore grossolano del terreno (mappe aeree) fa prima la media delle texture a piastrelle di ogni classe di terreno fino alla dimensione del pixel, così le piastrelle non danno un effetto moiré. Se nemmeno i LOD più grossolani entrano, gli alberi che risparmiano di più diventano chiome, e poi i tipi più piccoli vengono lasciati fuori (`leftOut`); nessun oggetto viene disegnato come una scatola (una forma di collisione, se c'è, è quella propria dell'oggetto).
Gli oggetti generati vengono diradati in modo deterministico per tipo (`density`), sempre gli stessi a ogni esecuzione. `--max-object-triangles` sostituisce il budget, `--max-grid` (predefinito 1024) limita le parti più grossolane della heightmap, `--no-objects` lascia fuori gli oggetti, `--no-generated` quelli generati, `--no-terrain-colour` riveste il terreno con la mappa tattica, `--no-texture` lo lascia senza texture.

`parts.objects` del JSON elenca le istanze (fisse e generate, per tipo e classe di terreno), quante ne sono state disegnate a quale LOD (`drawnAs`), i triangoli, la distanza del LOD e i secondi; `parts.heightmap.rings` il passo e i triangoli di ogni anello di terreno; `parts.terrainColour` le classi di terreno e i loro colori, strade e decalcomanie del suolo; `trianglesTotal`, `glbBytes` e `secondsBy` i totali.

## Cosa viene letto, e quanto bene {#what-is-read-and-how-well}

| Parte | Stato |
|---|---|
| Binario del livello (`levels/<level>.bin`, `DBLD` 3x64): tabella dei blocchi | ogni livello verificato |
| Heightmap (`HM2`, versioni 0-2; la versione 2 sono valori a 8 bit in blocchi, chunk Oodle o zstd) | ogni livello la cui heightmap è versione 2 con chunk Oodle; verificata a occhio sulle mappe tattiche (fiumi, valli, coste e città combaciano) |
| Collisione della land mesh (`lmap`, il suo traccia-raggi del terreno `LTdump`) | letta dove un livello ne ha una (compressa con Oodle). È la superficie di collisione del gioco, non la mesh renderizzata, quindi è più grossolana dove il terreno è piatto |
| Colore del terreno (classi di terreno `lmap` e mappa dei pesi, mappa fisica `LMp2`, spline `hspl`) | le mappe di colore delle classi di terreno e le texture di dettaglio (i loro colori medi) pesate dalla mappa dei pesi, l'indice biomi a 1 m delle classi di terreno indicizzate, le forme di strade e decalcomanie della mappa fisica con il colore della texture della loro spline o del loro materiale, falesie sui pendii ripidi. Verificato sulle mappe dei carri: strade, città, laghi, fasce di foresta e affioramenti rocciosi combaciano. La formula del colore dello shader del terreno di War Thunder non è nel codice pubblico; si usa quella pubblicata del motore (daNetGame), che esce più satura della mappa tattica |
| Livello dell'acqua | `water_level` dal BLK del livello in `aces.vromfs.bin` (0 dove non ne ha uno) |
| Heightmap dell'acqua (`WHM`: una griglia di celle piatte e pagine 130x130 di altezze a 16 bit) | letta dove un livello ne ha una; i suoi fiumi sono in pendenza con il terreno |
| Mappe tattiche | da `content/base/res/locations_maps.dxp.bin`, posizionate da `mapCoord0/1` e `tankMapCoord0/1` del BLK; il bordo superiore dell'immagine è il nord |
| Oggetti posati (`RIGz`: le istanze fisse del generatore di istanze di render) | ogni istanza, come matrice 3x4 di valori a 16 bit o, su alcuni livelli, a 32 bit (decide il numero di byte della cella); ogni byte di ogni cella conteggiato sui livelli controllati |
| Oggetti generati (maschere di classe di terreno `RIGz` e risorse `LandClass`) | il generatore del gioco, portato: gli stessi punti provati nello stesso ordine con gli stessi numeri casuali, le maschere di classe di terreno ed esclusione, l'oggetto scelto in ogni punto, la sua rotazione, scala e scostamento in altezza; entità a piastrelle (isolati cittadini) e piantate (foreste, cespugli, campi). Generati solo sulla mappa dei carri. Approssimati: l'altezza e la normale del terreno (dalla heightmap; il gioco traccia un raggio), i riquadri di esclusione che il gioco registra a tempo di esecuzione, e l'imbardata degli alberi (il gioco la aggancia alla tavolozza di rotazioni dell'impostore). |
| Mesh di render (risorse `RendInst` in `content/*/res/*.grp`, materiali in `riDesc.bin`) | i vertici e i triangoli di ogni LOD (posizioni float; indici a 16 o 32 bit, semplici o compressi con meshoptimizer), il materiale di ogni elemento. Gli elementi di decalcomania e di impostore a cartellone sono lasciati fuori; quelli trasparenti (vetro) vengono mantenuti |
| Colori degli oggetti | per materiale, la media del mip piccolo della sua texture diffusa (ponderata sull'alfa per le foglie), dai pacchetti di texture dell'installazione: t0 per la maggior parte degli shader, la prima texture diffusa di dettaglio dove t0 è una sovrapposizione o una maschera. Un colore per materiale: nessuna texture sugli oggetti |
| Forme di collisione (`<object>_collision`) | risorse di collisione della versione 3 di stream, usate dove un oggetto non ha una mesh di render. Vengono disegnati solo ciò che i raggi del gioco colpiscono (nodi `TRACEABLE`), e scatole, sfere e capsule solo quando la risorsa non ha una mesh: il resto sono sostituti fisici grossolani che apparirebbero come cubi intorno all'oggetto |
| Mesh di navigazione (`Lnav`), la land mesh renderizzata, l'erba, `spgz`, `stbl`, `d2co` | non letti |

I livelli sono compressi con Oodle, che è proprietario. Il gioco ne distribuisce una copia,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (una normale build x64), ed è quella che viene caricata; `HEAT3D_OODLE=<dll o cartella>` indica un'altra. Nulla di Oodle è incluso qui.

## Formati, e dove sono documentati {#formats-and-where-they-are-documented}

Gaijin ha pubblicato il codice sorgente del Dagor Engine con licenza BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). I lettori qui sono stati scritti a partire da esso;
nessun codice del gioco è stato decompilato. Ogni modulo nomina i file sorgente che segue:

- `vromfs.py`: `*.vromfs.bin` (intestazione `VRFs`/`VRFx`, un corpo zstd i cui primi e ultimi 16 byte sono in XOR con una chiave fissa, una tabella dei nomi e una tabella degli scostamenti:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  e BLK binario (forme 1-5, con la mappa dei nomi condivisa dell'archivio `\xff?nm` e il dizionario zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: pacchetti di texture `DxP2` (`lib3d/texPackMgr2.cpp`) e intestazioni DDSx (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 sono decodificati da Pillow.
- `dagorlevel.py`: il binario del livello (`scene/loadLevel.cpp`), la heightmap
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  il traccia-raggi del terreno (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) e la heightmap dell'acqua (`fftWater/fftWater.cpp`).
- `rigen.py`: gli oggetti posati (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: gli oggetti generati (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: istanze di render (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) e il codec degli indici di meshoptimizer
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: il colore del terreno (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: pacchetti di risorse (`gameRes/grpData.h`) e risorse di collisione
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  i cui triangoli sono memorizzati come BVH di quad (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) legge gli stessi archivi; non serve e non viene usato.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
