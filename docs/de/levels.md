---
title: Level
nav_order: 9
lang: de
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Level (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` macht aus den Leveln deiner eigenen War-Thunder-Installation
`.glb`-Level für den Viewer, im selben Koordinatensystem wie die Tabellen der Replays.

## Schritt für Schritt {#step-by-step}

1. Liste die Level deiner Installation auf: `heat3d-wt-level list`. Es gibt pro Level
   eine Zeile aus: seinen Namen, sein Gelände und seine Karten, dann die Anzahl. Zum
   Beispiel (ein erfundenes Level):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Entpacke eines, mehrere (Platzhalter sind erlaubt) oder alle:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Lade `levels/<level>/<level>.glb` im Panel „Hintergrund / Level“ des Viewers, unter den
   Gefechten dieser Karte.

Die Level, die du schreibst, bleiben auf deinem Rechner: veröffentliche sie nie
(siehe [Begriffe und Lizenz](terms.md)).

## Optionen {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Befehl / Option | Wirkung |
|---|---|
| `list [--game FOLDER]` | jedes Level der Installation |
| `extract <levels...>` / `--all` | die genannten Level (so, wie `list` sie ausgibt; Platzhalter erlaubt) oder alle Level |
| `-o`, `--out` | Ausgabeordner; jedes Level kommt in `<out>/<level>/` |
| `--game FOLDER` | der Ordner von War Thunder (Standard: über Steam oder den Launcher gefunden; auch `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | Bodenauflösung, Bodenfarbe und Objektbudget über der Panzerkarte (Standard `medium`) |
| `--max-object-triangles N` | das Objektbudget (Standard: das der Detailstufe) |
| `--max-grid N` | Höhenkarten-Punkte pro Seite, je Teil (Standard 1024) |
| `--no-objects` | Gebäude, Bäume und andere platzierte Objekte weglassen |
| `--no-generated` | die Objekte weglassen, die die Landklassen erzeugen (Wälder, Städte) |
| `--no-terrain-colour` | den Boden mit der taktischen Karte texturieren, nicht mit den Landklassen |
| `--no-texture` | den Boden ohne Textur lassen |
| `--skip-existing` | Level überspringen, deren `.glb` schon existiert |

## Was geschrieben wird {#what-is-written}

Jedes Level wird zu `<out>/<level>/<level>.glb`, `<level>.json` (was gelesen wurde,
die Wasserhöhe, die Rechtecke der Karten, Dreieckszahlen, Zeiten) und die taktischen
Karten des Levels als `<level>_map.png` (die Luftkarte) und `<level>_tankmap.png`;
Bodenkarten bekommen außerdem `<level>_terrain.png`, die eigenen Farben des Bodens über
der Panzerkarte. Die glb wird nach `<level>.glb.part` geschrieben und beim Abschluss
umbenannt. Solange ein Level geschrieben wird, ist `<out>/<level>/.<level>.lock` gesperrt,
damit zwei Entpackvorgänge nie dasselbe Level schreiben (der zweite gibt `busy <level>` aus).
Die Installation wird über Steam oder die Standardordner des Launchers gefunden;
`--game <folder>` oder `HEAT3D_WT_GAME` sagen sonst, wo sie liegt.

| Teil | Was es ist |
|---|---|
| `ground:<level>` | die Geländehöhenkarte (`HM2`) als Raster; auf Bodenkarten die Mitte der Panzerkarte (die halbe Breite) im Schritt der `--detail`-Stufe, gefärbt mit den Landklassen, Bodendekalen und Straßen (`<level>_terrain.png`; die taktische Karte, wo das nicht geht); auf Karten ohne Panzerkarte (Luftkarten) die ganze Höhenkarte in einem Schritt (bei `high` 2048 Punkte pro Seite, sonst 1024), mit den Landklassen über dem Gebiet der Luftkarte gefärbt (4096 Pixel pro Seite, etwa 32 m pro Pixel über 131 km; die taktische Karte, wo das nicht geht); auf Leveln ohne Höhenkarte das Landnetz |
| `ground:<level> tank map` | der Rest der Panzerkarte, einen Schritt gröber |
| `ground:<level> heightmap surroundings` | der Rest der Höhenkarte, noch gröber |
| `ground:<level> land mesh` | die Kollisionsdreiecke des Landnetzes, wo die Höhenkarte nicht hinreicht (die Umgebung einer Panzerkarte, bis zu zehn Kilometer weit); auf Leveln ohne Höhenkarte ist es der Boden, gefärbt wie oben |
| `ground:<level> outside the map` | Boden, den das Bild nicht abdeckt, ohne Textur |
| `water:<level>` | ein flaches Rechteck auf dem `water_level` des Levels über dem ganzen Gelände: Das Spiel zeichnet Wasser als eine Ebene, und tief liegender Boden darunter ist Meer, See oder Flussbett |
| `water:<level> rivers` | auf Leveln mit einer Wasser-Höhenkarte (`WHM`) die abfallende Wasserfläche über den Zellen, die sie bedeckt |
| `structure:<level> buildings` | jedes platzierte Objekt, das keine Pflanze ist: Häuser, Ruinen, Mauern, Zäune, Brücken, Schienen, Felsen, Requisiten. Die festen (`RIGz`) und, über der Panzerkarte, die, die die Landklassen erzeugen (Stadtblöcke, Steine). Jedes wird mit seinem Render-Netz gezeichnet (Wände, Dächer, Fensteröffnungen, Balken), in dem LOD, das das Dreiecksbudget erlaubt, gefärbt je Material nach dem Mittelwert seiner Diffusetextur |
| `structure:<level> trees` | Bäume und Büsche, feste und erzeugte (Wälder, Hecken): ihr Render-Netz, wo das Budget es erlaubt, sonst ein Stamm und eine Krone (ein Kegel bei Nadelbäumen) in der eigenen Blattfarbe des Baumes, in seiner echten Größe |

Objekte ohne Render-Netz weichen auf ihre Kollisionsform aus; Bäume ohne eines auf
die Krone. Die Eckpunktfarben (`COLOR_0`) enthalten sRGB-kodierte Werte, so liest sie
der 3DHeat-Viewer.

**Koordinaten** sind die Meter des Spiels mit gespiegeltem z: glb (x, y, z) = Spiel
(x, y, -z). Die Welt des Spiels ist linkshändig (x Osten, y oben, z Norden); glTF ist
rechtshändig. `heat3d-wt-replay` behält das z des Spiels und sagt dem Viewer, dass er
es spiegeln soll, sodass ein Replay und das Level seiner Karte ohne einen Platzierungsschritt
übereinanderliegen. Die JSON gibt das Rechteck jeder taktischen Karte in Spielmetern und
ihre Ecken im Raum der glb an, um das PNG als Kartenbild zu laden.

**Detailstufe.** `--detail low|medium|high` (Standard medium) legt über der Panzerkarte fest:

| | Mitte der Panzerkarte | Rest der Panzerkarte | Bodenfarbe | Objektbudget | meiste Dreiecke je Objekt | erzeugte Pflanzen behalten |
|---|---|---|---|---|---|---|
| low | jeder 4. Punkt | jeder 8. | 4 m pro Pixel | 1,2 Mio. | 1.500 | Bäume 35 %, Büsche 20 % |
| medium | jeder 2. | jeder 4. | 2 m | 3,5 Mio. | 4.000 | Bäume 70 %, Büsche 50 % |
| high | jeder Punkt (auf den meisten Bodenkarten 2 m) | jeder 2. | 1 m (höchstens 4096 Pixel pro Seite) | 4,5 Mio. | 12.000 | alle |

Die beiden Ringe der Panzerkarte werden auf 0,3 Mio. (low), 1 Mio. (medium) und 3,7 Mio. (high)
Dreiecke gehalten: Auf Karten, deren Höhenkarte feiner als 2 m ist, verdoppeln sich die Schritte
(der äußere Ring zuerst), bis sie passen, sodass sie dort etwa bei 2 m herauskommen.

Eine Bodenkarte bei `high` kommt auf etwa 8 Millionen Dreiecke (3,5 Mio. Boden, 4,5 Mio. Objekte)
und 250 MB; bei `medium` auf etwa 4,5 Mio. Die LODs der Objekte sind die, die das Spiel selbst aus
einer Blickweite zeichnen würde, das kürzeste, dessen Summe ins Budget passt: Kleine Requisiten fallen
zuerst auf grobe LODs, große Gebäude zuletzt, nach den Reichweiten, die ihre Hersteller für jedes LOD
angaben (`lodDistance` der JSON). Was dieser Schritt über das Budget hinaus spart, geht an die größten
Objekte zurück. Grobe Bodenfarbe (Luftkarten) mittelt zuerst die gekachelten Texturen jeder Landklasse
auf die Pixelgröße herunter, damit die Kacheln nicht flimmern. Passen auch die gröbsten LODs nicht, werden
die Bäume, die am meisten sparen, zu Kronen, und dann werden die kleinsten Typen weggelassen (`leftOut`);
kein Objekt wird als Kasten gezeichnet (eine Kollisionsform, falls vorhanden, ist die eigene des Objekts).
Erzeugte Objekte werden nach Art (`density`) deterministisch ausgedünnt, bei jedem Lauf dieselben.
`--max-object-triangles` überschreibt das Budget, `--max-grid` (Standard 1024) begrenzt die gröberen Teile
der Höhenkarte, `--no-objects` lässt Objekte weg, `--no-generated` die erzeugten, `--no-terrain-colour`
textuiert den Boden mit der taktischen Karte, `--no-texture` lässt ihn ohne Textur.

Die `parts.objects` der JSON listet die Instanzen (feste und erzeugte, nach Art und Landklasse), wie viele
in welchem LOD gezeichnet wurden (`drawnAs`), die Dreiecke, die LOD-Distanz und die Sekunden;
`parts.heightmap.rings` den Schritt und die Dreiecke jedes Bodenrings; `parts.terrainColour` die Landklassen
und ihre Farben, Straßen und Bodendekale; `trianglesTotal`, `glbBytes` und `secondsBy` die Summen.

## Was gelesen wird, und wie gut {#what-is-read-and-how-well}

| Teil | Stand |
|---|---|
| Level-Binärdatei (`levels/<level>.bin`, `DBLD` 3x64): Blocktabelle | jedes Level geprüft |
| Höhenkarte (`HM2`, Versionen 0-2; Version 2 sind 8-Bit-Werte in Blöcken, Oodle- oder zstd-Stücke) | jedes Level, dessen Höhenkarte Version 2 mit Oodle-Stücken ist; mit dem Auge gegen ihre taktischen Karten geprüft (Flüsse, Täler, Küsten und Städte liegen richtig) |
| Kollision des Landnetzes (`lmap`, sein Strahlverfolger `LTdump`) | gelesen, wo ein Level eines hat (Oodle-gepackt). Es ist die Kollisionsfläche des Spiels, nicht das gezeichnete Netz, daher gröber, wo das Land flach ist |
| Bodenfarbe (`lmap`-Landklassen und Gewichtskarte, `LMp2`-Physikkarte, `hspl`-Splines) | die Farbkarten der Landklassen und die Detailtexturen (ihre mittleren Farben), gewichtet mit der Gewichtskarte, dem 1-m-Biom-Index der indizierten Landklassen, den Straßen- und Bodendekal-Formen der Physikkarte in der Farbe der Textur ihres Splines oder Materials, Klippen an steilen Hängen. Gegen die Panzerkarten geprüft: Straßen, Städte, Seen, Waldgürtel und Felsvorsprünge liegen richtig. Die Farbformel des Bodenshaders von War Thunder selbst ist nicht im öffentlichen Quellcode; benutzt wird die veröffentlichte der Engine (daNetGame), die gesättigter herauskommt als die taktische Karte |
| Wasserhöhe | `water_level` aus dem BLK des Levels in `aces.vromfs.bin` (0, wo es keines hat) |
| Wasser-Höhenkarte (`WHM`: ein Raster aus flachen Zellen und 130x130-Seiten mit 16-Bit-Höhen) | gelesen, wo ein Level eines hat; seine Flüsse fallen mit dem Boden ab |
| Taktische Karten | aus `content/base/res/locations_maps.dxp.bin`, platziert über `mapCoord0/1` und `tankMapCoord0/1` des BLK; die Oberkante des Bildes ist Norden |
| Platzierte Objekte (`RIGz`: die festen Instanzen des Render-Instanz-Generators) | jede Instanz, als 3x4-Matrix aus 16-Bit-Werten oder, auf manchen Leveln, 32-Bit-Werten (die Bytezahl der Zelle entscheidet); jedes Byte jeder Zelle ist auf den geprüften Leveln erfasst |
| Erzeugte Objekte (`RIGz`-Landklassen-Masken und die `LandClass`-Ressourcen) | der Generator des Spiels, übertragen: dieselben Stellen in derselben Reihenfolge mit denselben Zufallszahlen, die Landklassen- und Ausschlussmasken, das Objekt, das an jeder Stelle gewählt wird, seine Drehung, Skalierung und Höhenverschiebung; gekachelte (Stadtblöcke) und gepflanzte Entitäten (Wälder, Büsche, Felder). Nur über der Panzerkarte erzeugt. Angenähert: die Bodenhöhe und Normale (aus der Höhenkarte; das Spiel verfolgt einen Strahl), die Ausschlusskästen, die das Spiel zur Laufzeit registriert, und der Gierwinkel der Bäume (das Spiel rastet ihn auf die Drehpalette des Impostors ein) |
| Render-Netze (`RendInst`-Ressourcen in `content/*/res/*.grp`, Materialien in `riDesc.bin`) | die Eckpunkte und Dreiecke jedes LOD (Fließkomma-Positionen; 16- oder 32-Bit-Indizes, einfach oder meshoptimizer-gepackt), das Material jedes Elements. Decal- und Impostor-Billboard-Elemente fallen weg; die transparenten (Glas) bleiben |
| Objektfarben | je Material der Mittelwert der kleinen Mip-Stufe seiner Diffusetextur (alpha-gewichtet bei Blättern), aus den Texturpaketen der Installation: t0 für die meisten Shader, die erste Detail-Diffusetextur, wo t0 ein Overlay oder eine Maske ist. Eine Farbe je Material: keine Textur auf den Objekten |
| Kollisionsformen (`<object>_collision`) | Kollisionsressourcen der Stream-Version 3, genutzt, wo ein Objekt kein Render-Netz hat. Gezeichnet wird nur, was die Strahlen des Spiels treffen (`TRACEABLE`-Knoten), und Kästen, Kugeln und Kapseln nur, wenn die Ressource kein Netz hat: Der Rest sind grobe Physik-Platzhalter, die als Würfel um das Objekt erscheinen würden |
| Navigationsnetz (`Lnav`), das gezeichnete Landnetz, Gras, `spgz`, `stbl`, `d2co` | nicht gelesen |

Level sind mit Oodle komprimiert, das proprietär ist. Das Spiel liefert eine Kopie mit,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (ein gewöhnlicher x64-Build), und die wird
geladen; `HEAT3D_OODLE=<dll or folder>` zeigt auf eine andere. Nichts von Oodle ist hier enthalten.

## Formate, und wo sie dokumentiert sind {#formats-and-where-they-are-documented}

Gaijin hat den Quellcode der Dagor Engine unter der BSD-3-Clause-Lizenz veröffentlicht
(github.com/GaijinEntertainment/DagorEngine). Die Leser hier wurden daraus geschrieben;
kein Spielcode wurde dekompiliert. Jedes Modul nennt die Quelldateien, denen es folgt:

- `vromfs.py`: `*.vromfs.bin` (Kopf `VRFs`/`VRFx`, ein zstd-Körper, dessen erste und
  letzte 16 Bytes mit einem festen Schlüssel XOR-verknüpft sind, eine Namenstabelle und
  eine Versatztabelle: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) und binäres BLK (Formen 1-5, mit der gemeinsamen
  Namenszuordnung des Archivs `\xff?nm` und dem zstd-Wörterbuch:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: Texturpakete `DxP2` (`lib3d/texPackMgr2.cpp`) und DDSx-Köpfe
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 werden mit Pillow dekodiert.
- `dagorlevel.py`: die Level-Binärdatei (`scene/loadLevel.cpp`), die Höhenkarte
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  der Strahlverfolger des Landes (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) und die Wasser-Höhenkarte (`fftWater/fftWater.cpp`).
- `rigen.py`: die platzierten Objekte (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: die erzeugten Objekte (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: Render-Instanzen (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) und der Indexcodec von
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: die Bodenfarbe (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: Ressourcenpakete (`gameRes/grpData.h`) und Kollisionsressourcen
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  deren Dreiecke als Quad-BVH gespeichert sind (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) liest dieselben Archive; es wird weder gebraucht noch benutzt.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
