---
title: "Doelen"
nav_order: 15
lang: "nl"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Doelen {#objectives}

`objectives` in het wedstrijddocument somt op waar om het gevecht gaat, uit twee bronnen (`source`):

- **De replay** (`replay`): de missieobjecten die 0xD039 noemt (veroveringszones `cz_circle_NN`, vliegvelden, helipads,
  bases), geplaatst waar de gerepliceerde objecten van soort 3 (0xF02D) ze nu neerzetten - een veroveringszone begint op de plek van zijn
  sjabloon en wordt bij de start naar de zone van deze modus verplaatst (`moved`). De nummers van soort 3 volgen de volgorde van 0xD039;
  elk object dat niet verplaatst is, ligt precies waar 0xD039 het heeft, wat de volgorde controleert. Een veroveringszone krijgt de
  vorm en straal van het missiegebied op zijn plek (`area`, binnen 2 m) en zijn letter uit zijn eigen index (soort
  5, veld 69: 0 = A); de lettervolgorde is die van de replay, niet gecontroleerd tegen de kaart van het spel.
- **De missie** (`mission`): het missiebestand `<missie>.blk` in `mis.vromfs.bin` van je installatie en de
  sjablonen die het importeert (alleen lezen, op het moment van omzetten): de gebieden ervan, per naam ingedeeld: spawns (de
  genummerde punten van een spawn `..._spawnareaNN` als één `points`-spawn), gevechtsgebieden, bomdoelen (`bomb_zone`),
  spawnpunten van konvooien (`road_NN_spawn`), uitgangs- en killgebieden. Gebieden van een andere modus van dezelfde kaart (`conq_`, `dom_`, `bttl_`,
  ...) worden weggelaten, en van de varianten `_arcade` / `_realistic` / `_hardcore` die van het gevecht zelf (RB neemt
  `_realistic`, anders `_hardcore`, zoals de missiescripts doen); briefingmarkeringen, luchtdoelgeschut-punten en gebieden breder
  dan 5 km (de gebieden waarover spawns verspreid zijn) ook. Elke spawn zegt hoeveel sporen van spelers erin begonnen (`used`,
  `usedByTeam`). Een missie mag zijn zijden willekeurig wisselen (`randomSpawnTeams`): wanneer de spawns de teams van de replay
  omgekeerd tonen, wordt elk `team` gewisseld en de zijde van de naam bewaard als `missionTeam`. Konvooiroutes staan niet in de
  waypoints van de missies zoals ze gelezen worden; alleen waar konvooien verschijnen, wordt dat gegeven.

De veroveringszones door de tijd heen staan in de sidecar `<match>.objectives.parquet`: de gerepliceerde objecten van soort 5, één
per zone - veld 2 is de eigenaar (0, 1, 2), veld 67 de veroveringsvoortgang, een getekende byte van -100 tot 100 (positief
richting team 2), veld 69 zijn index. Gecontroleerd (`selfCheck.objectives`) op grond-serverreplays van Conquest- en Domination-gevechten: elke wisseling
van eigenaar gaat samen met een speler van het veroverende team die een `captureZone` op het scorebord krijgt op hetzelfde moment (binnen
1,5 s) en met een levende grondeenheid van dat team in de zone; de spawns van elk gevecht tonen de teams van de replay
maar op één manier (vaak omgekeerd ten opzichte van de `t1_` / `t2_` van de missie).

## Sceneeenheden: trams en railwagons {#scene-units-trams-and-rail-wagons}

Een level kan eenheden van zichzelf plaatsen: de `unit_loader+rail_wagon`-entiteiten van een server-replay zijn de trams van het
scenebestand van het level (`gamedata/scenes/<level>_objects.blk` in `aces.vromfs.bin`: `setting__unit_class`, zijn
transformatie en `setting__isDead`). Hun entiteiten dragen geen leesbare uid, dus een grondspoor zonder eenheidsentiteit
waarvan het eerste sample binnen 2 m van een sceneeenheid ligt, is die eenheid: zijn klasse als `Vehicle`, soort `train`, type
`tram`, `locomotive` of `wagon`, geen team; een eenheid die de scene dood plaatst (zoals uitgebrande trams) is een wrak (`alive` 0) vanaf zijn eerste rij. Het spel heeft geen Engelse naam voor hen; `VehicleName` is de id
gelezen als woorden (`Railway tram A`). Hun posities wiebelen niet: bijna geen enkele beweegt ooit (elk
sample hetzelfde tot op de bit). De replay stuurt ze toch ongeveer tien keer per seconde,
dus van hun samples worden alleen die bewaard die ze verplaatsen (0,05 m of 0,1 graden), en één per 10 s
(`selfCheck.sceneUnits` telt de weggelaten samples). Vroeger waren het sporen met de naam `uid 8`
zonder voertuig.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
