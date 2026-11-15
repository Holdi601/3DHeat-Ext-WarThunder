---
title: Kampdokumentet
nav_order: 7
lang: "da"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet {#the-match-document}

![Starten af et syntetisk kampdokument, og dets nøgler](../assets/img/match-document.svg)

`<match>.match.json` indeholder alt det, replayet siger, som ikke er en række i
tabellen. Viewerens Kamp-fane læser den.

## Slaget {#the-battle}

| Nøgle | Hvad |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | kampens id (som i filnavnet); kortets id; banefilen den bruger |
| `mission`, `missionKey` | missionens navn og dens nøgle i spillets tekstfiler |
| `battleClass`, `environment`, `weather` | som headeren angiver dem |
| `sessionId`, `server` | slagets session-id; serveren |
| `replayVersion`, `flightLayout` | replay-formatets version; det læste flypakke-layout (`2025` eller `2026`) |
| `files` | de replay-filer, der er læst (én, eller en serverreplays dele) |
| `started`, `timePlayed`, `replayEnd` | starttidspunkt (ISO, UTC); sekunder spillet, fra resultaterne; sekunder for replayets sidste pakke |
| `author`, `authorUserId` | den optagende spiller og dennes Gaijin-id (klientreplays) |
| `teams` | holdene i kampen (`1`, `2`) |
| `result` | `winner`, `status` (`success` eller `fail`, optagerens udfald), `authorTeam`, `teams` ([Økonomi](economy.md)) |
| `vehicleNames` | hvor køretøjsnavnene kom fra (din installation) og deres sprog |
| `conventions` | tabellens enheder og fortegn: akser, tid, liv, spor, alive, roll, og mere |

## Alt det øvrige {#everything-else}

| Nøgle | Hvad |
|---|---|
| `battle`, `difficulty`, `gameMode` | kampens tilstand: `difficulty` `AB` / `RB` / `SB` (og dets navn, og headerbyten), `gameMode` `ground` / `air` / `naval`, missionens tilstand (`Dom`, `Conq`, `Bttl`, `I2M`, ...) og dets engelske navn fra din installation (`Domination`, `Enduring Confrontation`), de tilladte enhedstyper (se [Kamptilstand](ground.md#battle-mode)) |
| `settings` | missionens blk efter headeren: tilstand, miljø, vejr, point- og tidsgrænser, lande, tilladte enhedstyper, vind, og `stars` (breddegrad, længdegrad, dato, lokal tid) |
| `sky` | den første `CustomWeatherParams`: sol- og månens retning, vind, himmelfarver, skyforskydninger |
| `players`, `slots` | resultaternes linje pr. spiller (drab, landdrab, dødsfald, assists, score, erobringer, trup, klan, land, opstilling, de uid'er de kørte); replayets spillerpladser (navn, bruger-id, hold) |
| `units` | hver enhedsentitet replayet oprettede: eid, uid, skabelon, køretøj, art, type, hold, spiller, missionsnavn, hvornår den blev oprettet og fjernet, hvor den blev oprettet, hvilke komponenter der ikke kunne læses |
| `objects` | missionens navngivne objekter: erobringszoner og flyvepladser med deres position og størrelse, flyvepladsers konturer som punkter, spawn-områder |
| `objectives` | kampens mål, hver `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (replayets 1 eller 2, tom for begge), `name` (en erobringszone dens bogstav, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) med `position`, `radius` / `height` / `size` og `heading`, `source` (`replay` eller `mission`) og hvad ellers der er kendt (se [Mål](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | med navne og køretøjer for begge sider; drab med våbnets engelske navn |
| `weapons` | hver raket, missil, bombe, torpedo, udsmidsbar tank og smidt last: hvornår, hvor den blev udløst (position, holdning, hastighed), af hvilken enhed (den nærmeste inden for 300 m og 1,5 s), hvor mange flyprøver, hvor den sidst blev set, hvornår den blev fjernet |
| `explosions`, `flak` | `PlayExplosionVisual` (position, retning, art) og `PlayFlakExplosionVisual` (position) |
| `awards` | den optagende spillers priser (`TextStreak`: first_blood, serier, udfordringstællere) |
| `detections`, `unitStates` | `UnitDetected`-par af enheder; en meddelelse (0xF093) med en enheds position, holdning og hastighed, hvis betydning ikke kendes |
| `authorInstruments` | den optagende spillers cockpitværdier (`ReplayCockpitParams`) efter instrumentnummer, højst én pr. sekund; `known` navngiver hvert nummer, replayet sendte (navn, enhed, hvordan det blev kontrolleret), `notNamed` resten |
| `scoreboard` | hver spillers statistik, hver gang den ændrede sig (drab, dødsfald, assists, score, AI-drab, sødrab, zoner, skade, undvigelser af missiler, trup), og hvert holds score og sandsynlige billetter over tid (se [Reflekteringsdata](aircraft.md#reflection-data)) |
| `economy` | kampens Silver Lions og forskningspoint (se [Økonomi](economy.md)): summer, pr. spiller, pr. køretøj, multiplikatorerne, vinderen, kontrollerne |
| `entityMessages` | entitetsmeddelelserne (0x20) efter klassenummer: antal, måleskabeloner, størrelser |
| `chat` | hver chatlinje |
| `triggers`, `hints`, `missionProgress` | missionsscriptets handlinger (RunTriggerAction), dets hints, dets fremskridtsmeddelelser |
| `camera` | den optagende spillers replay-kameras felter hver 0,25 s, som sendt (tabellen har det som et spor) |
| `projectileHitReplays` | den optagende spillers egne træf og det at blive ramt, med våben og ammunition og deres engelske navne |
| `results` | hele resultat-blk'en, som spillet skrev den |
| `counts` | rækker, begivenheder, liv, arter, samples, entiteter efter skabelon, våben, pakker læst og ikke læst, hver meddelelses-id set og de ikke læste, udeladte samples |
| `trackBreaks` | hvert snit i et spor for et spring hurtigere, end enheden kan gå: hvor, hvor langt, hvor hurtigt, og hvad det mest sandsynligt er |
| `selfCheck` | kontrollerne listet i [Sådan læses et replay](how-it-reads.md), beregnet ved hver konvertering; `stepSpeed` angiver pr. art hastigheden mellem på hinanden følgende rækker i et spor, som vieweren samler dem (median, 99. percentil, højeste, og spring hurtigere end muligt, som skal være 0) |

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
