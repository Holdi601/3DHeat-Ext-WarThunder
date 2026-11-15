---
title: Ziele
nav_order: 15
lang: de
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Ziele {#objectives}

`objectives` im Match-Dokument listet auf, worum im Gefecht gekämpft wird, aus zwei Quellen (`source`):

- **Das Replay** (`replay`): die Missionsobjekte, die 0xD039 benennt (Eroberungszonen `cz_circle_NN`, Flugplätze, Hubschrauberlandeplätze,
  Basen), dort platziert, wo die replizierten Objekte der Art 3 (0xF02D) sie jetzt setzen. Eine Eroberungszone beginnt an der Stelle
  ihres Templates und wird zu Beginn an die Zone dieses Modus verschoben (`moved`). Die Nummern der Art 3 folgen der Reihenfolge von
  0xD039; jedes Objekt, das nicht verschoben wird, liegt genau dort, wo 0xD039 es hat, was die Reihenfolge prüft. Eine Eroberungszone
  bekommt Form und Radius des Missionsbereichs an ihrer Stelle (`area`, innerhalb von 2 m) und ihren Buchstaben aus ihrem eigenen Index
  (Art 5, Feld 69: 0 = A); die Buchstabenfolge ist die des Replays und nicht gegen die Karte des Spiels geprüft.
- **Die Mission** (`mission`): die Missionsdatei `<mission>.blk` in der `mis.vromfs.bin` deiner Installation und die Templates, die sie
  importiert (nur lesend, zum Zeitpunkt der Umwandlung): ihre Bereiche, nach dem Namen eingeordnet - Spawns (die nummerierten Punkte
  eines Spawns `..._spawnareaNN` als ein Spawn vom Typ `points`), Gefechtsbereiche, Bombenziele (`bomb_zone`), Konvoi-Spawnpunkte
  (`road_NN_spawn`), Austritts- und Tötungsbereiche. Bereiche eines anderen Modus derselben Karte (`conq_`, `dom_`, `bttl_`, ...) fallen
  weg, und von den Varianten `_arcade` / `_realistic` / `_hardcore` nimmt man die des Gefechts (RB nimmt `_realistic`, sonst
  `_hardcore`, wie es die Missionsskripte tun); ebenso Briefing-Markierungen, Punkte der Flak und Bereiche breiter als 5 km (die
  Bereiche, über die Spawns verstreut sind). Jeder Spawn sagt, wie viele Spieler mit ihrer Spur in ihm begannen (`used`, `usedByTeam`). Eine
  Mission darf ihre Seiten zufällig tauschen (`randomSpawnTeams`): Zeigen die Spawns die Teams des Replays andersherum, wird jedes
  `team` getauscht und die Seite des Namens als `missionTeam` behalten. Konvoi-Routen stehen, so wie sie gelesen werden, nicht in den
  Wegpunkten der Missionen; angegeben wird nur, wo Konvois erscheinen.

Die Eroberungszonen im Zeitverlauf stehen im Sidecar `<match>.objectives.parquet`: die replizierten Objekte der Art 5, eines pro
Zone - Feld 2 ihr Besitzer (0, 1, 2), Feld 67 ihr Eroberungsfortschritt, ein Vorzeichen-Byte von -100 bis 100 (positiv in Richtung Team 2),
Feld 69 ihr Index. Geprüft (`selfCheck.objectives`) an Bodengefechten von Server-Replays der Modi Eroberung und Dominanz: Jeder Besitzerwechsel
kommt zusammen mit einem Spieler des erobernden Teams, der im Scoreboard eine `captureZone` gewinnt, im selben Moment (innerhalb von
1,5 s) und mit einer lebenden Bodeneinheit dieses Teams innerhalb der Zone; die Spawns jedes Gefechts zeigen die Teams des Replays
nur in einer Richtung (oft gegenüber den `t1_` / `t2_` der Mission vertauscht).

## Szenen-Einheiten: Straßenbahnen und Schienenwagen {#scene-units-trams-and-rail-wagons}

Ein Level kann eigene Einheiten platzieren: Die Entitäten `unit_loader+rail_wagon` eines Server-Replays sind die Straßenbahnen der
Szenendatei des Levels (`gamedata/scenes/<level>_objects.blk` in `aces.vromfs.bin`: `setting__unit_class`, ihre Transformation und
`setting__isDead`). Ihre Entitäten tragen keine lesbare uid. Deshalb ist eine Bodenspur ohne Einheiten-Entität, deren erster Messwert
innerhalb von 2 m einer Szenen-Einheit liegt, genau diese Einheit: ihre Klasse als `Vehicle`, Art `train`, Typ `tram`, `locomotive` oder
`wagon`, ohne Team; eine Einheit, die die Szene tot platziert (etwa ausgebrannte Straßenbahnen), ist ab ihrer ersten Zeile ein Wrack
(`alive` 0). Das Spiel hat keinen englischen Namen für sie; `VehicleName` ist die ID, als Wörter gelesen ("Railway tram A"). Ihre
Positionen wackeln nicht: fast alle bewegen sich nie (jeder Messwert auf das Bit gleich). Das Replay sendet sie trotzdem etwa zehnmal
pro Sekunde. Deshalb werden von ihren Messwerten nur die behalten, die sie bewegen (0,05 m oder 0,1 Grad), und einer alle 10 s
(`selfCheck.sceneUnits` zählt die verworfenen Messwerte). Früher waren sie Spuren namens `uid 8` ohne Fahrzeug.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
