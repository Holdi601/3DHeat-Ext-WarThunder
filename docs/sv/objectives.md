---
title: "Mål"
nav_order: 15
lang: sv
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Mål {#objectives}

`objectives` i matchdokumentet listar vad striden utkämpas om, från två källor (`source`):

- **Repriserna** (`replay`): uppdragsobjekten som 0xD039 namnger (erövringszoner `cz_circle_NN`,
  flygfält, helikopterplatser, baser), placerade där de replikerade objekten av slag 3 (0xF02D)
  lägger dem nu - en erövringszon börjar på sin mallens plats och flyttas till detta läges zon
  vid start (`moved`). Slag 3:s nummer följer 0xD039:s ordning; varje objekt som inte flyttats
  ligger exakt där 0xD039 har det, vilket kontrollerar ordningen. En erövringszon får formen och
  radien för uppdragsområdet på sin plats (`area`, inom 2 m) och sin bokstav från sitt eget index
  (slag 5 fält 69: 0 = A); bokstavsordningen är repriserns, inte kontrollerad mot spelets karta.
- **Uppdraget** (`mission`): uppdragsfilen `<mission>.blk` i din installations `mis.vromfs.bin` och
  de mallar den importerar (endast läst, vid konverteringstillfället): dess områden, klassade efter
  namn - spawner (en spawners numrerade punkter `..._spawnareaNN` som en `points`-spawner),
  stridsområden, bombmål (`bomb_zone`), konvojens spawnpunkter (`road_NN_spawn`), utgångs- och
  dödsområden. Områden för ett annat läge på samma karta (`conq_`, `dom_`, `bttl_`, ...) lämnas
  bort, och av varianterna `_arcade` / `_realistic` / `_hardcore` tas stridens egen (RB tar
  `_realistic`, annars `_hardcore`, precis som uppdragsskripten gör); briefingmarkörer,
  luftvärnskanonernas punkter och områden bredare än 5 km (de områden spawners sprids över) också.
  Varje spawner anger hur många spelares spår som började i den (`used`, `usedByTeam`). Ett uppdrag
  kan byta sidor slumpmässigt (`randomSpawnTeams`): när spawnerna visar repriserna lag åt andra
  hållet, byts varje `team` och sidan från namnet behålls som `missionTeam`. Konvojrutter finns inte
  i uppdragens waypoints som de läses; bara var konvojer dyker upp anges.

Erövringszonerna över tid är sidofilen `<match>.objectives.parquet`: de replikerade objekten av slag
5, ett per zon - fält 2 dess ägare (0, 1, 2), fält 67 dess erövringsframsteg, en signerad byte från
-100 till 100 (positiv mot lag 2), fält 69 dess index. Kontrollerat (`selfCheck.objectives`) på
markserverrepriser av Conquest- och Domination-strider: varje ägarbyte kommer med en spelare i det
erövrande laget som får en `captureZone` i resultattavlan samma ögonblick (inom 1,5 s) och med en
levande markenhet i det laget inne i zonen; varje strids spawners visar repriserna lag åt bara ett
håll (ofta bytta mot uppdragets `t1_` / `t2_`).

## Scenenheter: spårvagnar och järnvägsvagnar {#scene-units-trams-and-rail-wagons}

En nivå kan placera enheter av egen rätt: `unit_loader+rail_wagon`-entiteterna i en serverrepris är
nivåns sceneSpårvagnar i scenfilen (`gamedata/scenes/<level>_objects.blk` i `aces.vromfs.bin`:
`setting__unit_class`, dess transform och `setting__isDead`). Deras entiteter bär ingen läsbar uid,
så en markbana utan en enhetsentitet vars första mätpunkt ligger inom 2 m från en scenenhet är den
enheten: dess klass som `Vehicle`, slag `train`, typ `tram`, `locomotive` eller `wagon`, inget lag; en
enhet som scenen placerar död (som utbrända spårvagnar) är ett vrak (`alive` 0) från sin första rad.
Spelet har inget engelskt namn för dem; `VehicleName` är id:t läst som ord ("Railway tram A").
Deras positioner vajar inte: nästan alla rör sig aldrig (varje mätpunkt är densamma bit för bit).
Repriserna skickar dem ungefär tio gånger per sekund ändå, så av deras mätpunkter behålls bara de
som flyttar dem (0,05 m eller 0,1 grader), och en var 10:e s (`selfCheck.sceneUnits` räknar de
bortkastade mätpunkterna). Förut var de banor som hette `uid 8` utan fordon.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
