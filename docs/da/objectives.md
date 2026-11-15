---
title: Mål
nav_order: 15
lang: da
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Mål {#objectives}

`objectives` i kampdokumentet lister det, kampen drejer sig om, fra to kilder (`source`):

- **Replayet** (`replay`): missionsobjekterne, 0xD039 navngiver (erobringszoner `cz_circle_NN`, flyvepladser,
  helipads, baser), placeret, hvor de replikerede objekter af art 3 (0xF02D) sætter dem nu - en erobringszone
  starter på sin skabelons plads og flyttes til denne tilstands zone ved start (`moved`). Art 3's numre følger
  0xD039's rækkefølge; hvert objekt, der ikke flyttes, ligger præcis, hvor 0xD039 har det, hvilket kontrollerer
  rækkefølgen. En erobringszone får formen og radius af missionsområdet på dens plads (`area`, inden for 2 m)
  og sit bogstav ud fra sit eget indeks (art 5 felt 69: 0 = A); bogstavrækkefølgen er replayets, ikke kontrolleret
  mod spillets kort.
- **Missionen** (`mission`): missionsfilen `<mission>.blk` i din installations `mis.vromfs.bin` og de skabeloner, den
  importerer (kun læst, ved konverteringstidspunktet): dens områder, klassificeret efter navn - spawns (en spawns
  nummererede punkter `..._spawnareaNN` som ét `points`-spawn), kampområder, bombemål (`bomb_zone`), konvojens
  spawnpunkter (`road_NN_spawn`), udgangs- og drabsområder. Områder for en anden tilstand på samme kort (`conq_`,
  `dom_`, `bttl_`, ...) udelades, og af `_arcade` / `_realistic` / `_hardcore`-varianter tages kampens egen (RB
  tager `_realistic`, ellers `_hardcore`, som missionsscripts gør); briefingmarkører, luftværnskanonpunkter og områder
  bredere end 5 km (de områder, spawns er spredt over) også. Hvert spawn siger, hvor mange spilleres spor begyndte
  i det (`used`, `usedByTeam`). En mission kan tilfældigt bytte sine sider (`randomSpawnTeams`): når spawns viser
  replayets hold den anden vej rundt, bliver hvert `team` byttet, og sidens navn beholdes som `missionTeam`.
  Konvojruter står ikke i missionernes waypoints, som de læses; kun hvor konvojer optræder, angives det.

Erobringszonerne over tid er sidecaren `<match>.objectives.parquet`: de replikerede objekter af art 5, ét pr.
zone - felt 2 dens ejer (0, 1, 2), felt 67 dens erobringsfremskridt, en signeret byte fra -100 til 100 (positiv
mod hold 2), felt 69 dens indeks. Kontrolleret (`selfCheck.objectives`) på landkamps-serverreplays af Conquest- og
Domination-kampe: hver ejerskift kommer med en spiller fra det erobrende hold, der får en `captureZone` i scoreboard
på samme tidspunkt (inden for 1,5 s), og med en levende landenhed fra det hold inde i zonen; hvert kamps spawns viser
replayets hold kun den ene vej (ofte byttet i forhold til missionens `t1_` / `t2_`).

## Scene-enheder: sporvogne og jernbanevogne {#scene-units-trams-and-rail-wagons}

En bane kan placere enheder af sin egen: `unit_loader+rail_wagon`-entiteterne i et serverreplay er sporvognene i
banens scenefil (`gamedata/scenes/<level>_objects.blk` i `aces.vromfs.bin`: `setting__unit_class`, dens transform og
`setting__isDead`). Deres entiteter bærer intet læsbart uid, så et landspor uden en enhedsentitet, hvis første sample
ligger inden for 2 m af en scene-enhed, er den enhed: dens klasse som `Vehicle`, art `train`, type `tram`,
`locomotive` eller `wagon`, intet hold; en enhed, scenen placerer død (som udbrændte sporvogne), er et vrag (`alive` 0)
fra sin første række. Spillet har intet engelsk navn til dem; `VehicleName` er id'et læst som ord ("Railway tram A").
Deres positioner vakler ikke: næsten alle flytter sig aldrig (hver sample ens til bit'en). Replayet sender dem alligevel
ca. ti gange i sekundet, så af deres samples beholdes kun dem, der flytter dem (0,05 m eller 0,1 grader), og en hver 10. s
(`selfCheck.sceneUnits` tæller de udeladte samples). Før var de spor med navnet `uid 8` og intet køretøj.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
