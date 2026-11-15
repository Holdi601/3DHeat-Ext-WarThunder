---
title: "Mål"
nav_order: 15
lang: "no"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Mål {#objectives}

`objectives` i kampdokumentet lister det slaget kjempes om, fra to kilder (`source`):

- **Replayen** (`replay`): oppdragsobjektene 0xD039 navngir (erobringssoner `cz_circle_NN`, flyplasser, helikopterplasser,
  baser), plassert der de replikerte objektene av type 3 (0xF02D) setter dem nå - en erobringssone starter på sin malplass og flyttes
  til denne modusens sone ved starten (`moved`). Type 3s nummer følger 0xD039s rekkefølge; hvert objekt som ikke er flyttet ligger
  nøyaktig der 0xD039 har det, noe som kontrollerer rekkefølgen. En erobringssone får formen og radiusen til oppdragsområdet på sin
  plass (`area`, innen 2 m) og sin bokstav fra sin egen indeks (type 5 felt 69: 0 = A); bokstavrekkefølgen er replayens, ikke kontrollert
  mot spillets kart.
- **Oppdraget** (`mission`): oppdragsfilen `<oppdrag>.blk` i installasjonens `mis.vromfs.bin` og malene den importerer (bare lest, ved
  konvertering): dets områder, klassifisert etter navn - spawn (et spawns nummererte punkter `..._spawnareaNN` som én `points`-spawn),
  kampområder, bombemål (`bomb_zone`), konvoispawn-punkter (`road_NN_spawn`), utgangs- og drapsområder. Områder for en annen modus på
  samme kart (`conq_`, `dom_`, `bttl_`, ...) er utelatt, og av `_arcade` / `_realistic` / `_hardcore`-variantene tas slagets egen (RB
  tar `_realistic`, ellers `_hardcore`, slik oppdragsskriptene gjør); briefing-markører, luftvernkanonpunkter og områder bredere enn
  5 km (områdene spawnene er spredt over) også. Hvert spawn sier hvor mange spilleres spor begynte der (`used`, `usedByTeam`). Et oppdrag
  kan bytte sidene tilfeldig (`randomSpawnTeams`): når spawnene viser replayens lag den andre veien, snus hver `team` og sidens navn
  beholdes som `missionTeam`. Konvoiruter står ikke i oppdragenes veipunkter slik de leses; bare der konvoier dukker opp, gis det.

Erobringssonene over tid er sidefilen `<kamp>.objectives.parquet`: de replikerte objektene av type 5, ett per sone - felt 2 dens eier (0, 1,
2), felt 67 dens erobringsfremdrift, en fortegnet byte fra -100 til 100 (positiv mot lag 2), felt 69 dens indeks. Kontrollert
(`selfCheck.objectives`) på bakkeserverreplayer fra Conquest- og Domination-slag: hver eierendring kommer med en spiller fra det erobrende
laget som får en `captureZone` i resultattavlen samme øyeblikk (innen 1,5 s) og med en levende bakkeenhet fra det laget inne i sonen; hvert
slags spawn viser replayens lag bare én vei (ofte byttet mot oppdragets `t1_` / `t2_`).

## Scene-enheter: trikker og skinnevogner {#scene-units-trams-and-rail-wagons}

Et nivå kan plassere enheter av sitt eget: `unit_loader+rail_wagon`-entitetene i en serverreplay er nivåets trikker fra sin scene-fil
(`gamedata/scenes/<nivå>_objects.blk` i `aces.vromfs.bin`: `setting__unit_class`, dens transform og `setting__isDead`). Entitetene deres
bærer ingen lesbar uid, så et bakkespor uten en enhetsentitet hvis første sample ligger innen 2 m fra en scene-enhet er den enheten: dens
klasse som `Vehicle`, type `train`, typen `tram`, `locomotive` eller `wagon`, uten lag; en enhet scenen plasserer død (som utbrente trikker)
er et vrak (`alive` 0) fra sin første rad. Spillet har ingen engelsk navn for dem; `VehicleName` er ID-en lest som ord («Railway tram A»).
Deres posisjoner vakler ikke: nesten alle beveger seg aldri (hver sample lik til biten). Replayen sender dem omtrent ti ganger i sekundet
uansett, så av deres samples beholdes bare de som flytter dem (0,05 m eller 0,1 grad), og én hver 10. s (`selfCheck.sceneUnits` teller
de droppede samplene). Før dette var de spor kalt `uid 8` uten kjøretøy.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
