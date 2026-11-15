---
title: "Ziler"
nav_order: 15
lang: lb
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Ziler {#objectives}

`objectives` am Match-Dokument lëscht op, ëm wat d'Gefecht gekämpft gëtt, aus zwou Quellen (`source`):

- **De Replay** (`replay`): d'Missiounsobjeten, déi 0xD039 nennt (Eroberungszonen `cz_circle_NN`, Fluchhäfen, Helipads,
  Basen), do gesat, wou d'replizéiert Objete vun der Aart 3 (0xF02D) se elo hinsetzen - eng Eroberungszon fänkt um
  Plaz vu sengem Template un a gëtt um Ufank op d'Zon vun dësem Modus geréckelt (`moved`). Dem Aart 3 seng Zuelen follegen der Reiefolleg vun 0xD039;
  all Objet, dat net geréckelt gëtt, läit genau do, wou 0xD039 en huet, wat d'Reiefolleg préift. Eng Eroberungszon kritt d'
  Form an de Radius vum Missiounsgebitt op hirer Plaz (`area`, bannent 2 m) a säi Buschtaf vu sengem eegenen Index (Aart
  5 Feld 69: 0 = A); d'Buschtafereiefolleg ass déi vum Replay, net géint dem Spill seng Kaart gepréift.
- **D'Mission** (`mission`): d'Missiounsdatei `<mission>.blk` an der `mis.vromfs.bin` vun denger Installatioun an d'
  Templates, déi se importéiert (nëmme gelies, beim Émwandele): hir Gebidder, no Numm klasséiert - Spawns (d'nummeréiert
  Punkte `..._spawnareaNN` vun engem Spawn als een `points`-Spawn), Kampfgebidder, Bombenziler (`bomb_zone`), Konvoi-Spawn-
  Punkten (`road_NN_spawn`), Exit- a Kill-Gebidder. Gebidder vun engem anere Modus vun der selwechter Kaart (`conq_`, `dom_`, `bttl_`,
  ...) falen ewech, a vun `_arcade` / `_realistic` / `_hardcore`-Varianten déi vum Gefecht selwer (RB hëlt
  `_realistic`, soss `_hardcore`, wéi d'Missiounsskripter et maachen); Briefing-Markéierungen, Fligerofwier-Punkten a Gebidder, déi méi breet sinn wéi
  5 km (d'Gebidder, iwwer déi Spawns verstreet ginn) och. All Spawn seet, wéi vill Spiller hir Spuren dran
  ugefaangen hunn (`used`, `usedByTeam`). Eng Mission kann hir Säiten zoufälleg tauschen (`randomSpawnTeams`): wann d'Spawns d'Teams vum Replay
  anescht ronderëm weisen, gëtt all `team` getauscht an d'Säit vum Numm als `missionTeam` behalen. Konvoi-Routen sinn
  net an de Wegpunkte vun de Missioune, sou wéi se gelies ginn; et gëtt nëmmen, wou Konvoien opdauchen.

D'Eroberungszone iwwer d'Zäit sinn de Sidecar `<match>.objectives.parquet`: d'replizéiert Objete vun der Aart 5, ee
pro Zon - Feld 2 säin Besëtzer (0, 1, 2), Feld 67 säi Eroberungsfortschrëtt, e signéierte Byte vun -100 bis 100 (positiv
a Richtung Team 2), Feld 69 säin Index. Gepréift (`selfCheck.objectives`) op Buedem-Server-Replays vu Conquest- an Domination-Gefechter: all Besëtzerwiessel
kënnt zesumme mat engem Spiller vum erobernden Team, deen am selwechten Ament (bannent
1.5 s) eng `captureZone` am Scoreboard kritt, a mat enger liewender Buedemeenheet vun deem Team an der Zon; d'Spawns vun all Gefecht weisen d'Teams vum Replay
nëmmen op eng Manéier (dacks géint dem Mission säin `t1_` / `t2_` getauscht).

## Zeeneneenheeten: Tramen a Schinnewaggonen {#scene-units-trams-and-rail-wagons}

E Level kann eegen Eenheeten setzen: d'`unit_loader+rail_wagon`-Entitéite vun engem Server-Replay sinn d'Tramen vun der
Zeenendatei vum Level (`gamedata/scenes/<level>_objects.blk` an `aces.vromfs.bin`: `setting__unit_class`, seng
Transformatioun a `setting__isDead`). Hir Entitéite droen keng liesbar uid, dofir ass eng Buedemspur ouni Eenheet-Entitéit,
där hiert éischt Echantillon bannent 2 m vun enger Zeeneneenheet läit, dës Eenheet: hir Klass als `Vehicle`, kind `train`, type
`tram`, `locomotive` oder `wagon`, kee Team; eng Eenheet, déi d'Zeen dout setzt (wéi ausgebrannt Tramen), ass vu senger éischter Zeil un e Wrack (`alive` 0). D'Spill huet keen englesche Numm fir si; `VehicleName` ass d'ID
als Wierder gelies ("Railway tram A"). Hir Positioune wackelen net: bal all beweege sech ni (all
Echantillon bis op de Bit datselwecht). De Replay schéckt se ongeféier zéngmol d'Sekonn,
egal ob se sech beweegen, dofir bleiwe vun hiren Echantillonen nëmmen déi, déi se beweegen (0.05 m oder 0.1 Grad), an ee all 10 s
(`selfCheck.sceneUnits` zielt d'verworf Echantillonen). Virdru ware si Spuren mam Numm `uid 8`
ouni Gefier.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
