---
title: "Kampdokumentet"
nav_order: 7
lang: no
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Kampdokumentet {#the-match-document}

![Starten på et syntetisk kampdokument, og dets nøkler](../assets/img/match-document.svg)

`<kamp>.match.json` inneholder alt replayen sier som ikke er en rad i tabellen.
Visningsprogrammets fane Kamp leser det.

## Slaget {#the-battle}

| Nøkkel | Hva |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | kamp-ID-en (som i filnavnet); kartets ID; nivåfilen den bruker |
| `mission`, `missionKey` | oppdragets navn og nøkkelen i spillets tekstfiler |
| `battleClass`, `environment`, `weather` | som headeren oppgir dem |
| `sessionId`, `server` | slagets økt-ID; serveren |
| `replayVersion`, `flightLayout` | replay-formatets versjon; oppsettet for flygepakkene som ble lest (`2025` eller `2026`) |
| `files` | replayfilene som ble lest (én, eller delene av en serverreplay) |
| `started`, `timePlayed`, `replayEnd` | starttid (ISO, UTC); spilte sekunder, fra resultatene; sekunder til replayens siste pakke |
| `author`, `authorUserId` | spilleren som tok opp, og hans Gaijin-ID (klientreplayer) |
| `teams` | lagene i slaget (`1`, `2`) |
| `result` | `winner`, `status` (`success` eller `fail`, forfatterens utfall), `authorTeam`, `teams` ([Økonomi](economy.md)) |
| `vehicleNames` | hvor kjøretøynavnene kom fra (installasjonen din) og deres språk |
| `conventions` | enhetene og fortegnene i tabellen: akser, tid, liv, spor, levende, rull, og mer |

## Alt annet {#everything-else}

| Nøkkel | Hva |
|---|---|
| `battle`, `difficulty`, `gameMode` | slagsmodusen: `difficulty` `AB` / `RB` / `SB` (og navnet, og headerbyten), `gameMode` `ground` / `air` / `naval`, oppdragets modus (`Dom`, `Conq`, `Bttl`, `I2M`, ...) og dets engelske navn fra installasjonen din (`Domination`, `Enduring Confrontation`), de tillatte enhetstypene (se [Kampmodus](ground.md#battle-mode)) |
| `settings` | oppdragets blk etter headeren: modus, miljø, vær, grenser for poeng og tid, land, tillatte enhetstyper, vind, og `stars` (breddegrad, lengdegrad, dato, lokal tid) |
| `sky` | den første `CustomWeatherParams`: retning til sol og måne, vind, fargene på himmelen, skyforskyvninger |
| `players`, `slots` | resultatlinjen per spiller (drap, bakkedrap, dødsfall, assists, poeng, erobringer, tropp, klan, land, mannskapsoppsett, uid-ene de kjørte); replayens spillerplasser (navn, bruker-ID, lag) |
| `units` | hver enhetsentitet replayen opprettet: eid, uid, mal, kjøretøy, type, lag, spiller, navn i oppdraget, når den ble opprettet og fjernet, hvor den ble opprettet, hvilke komponenter som ikke kunne leses |
| `objects` | oppdragets navngitte objekter: erobringssoner og flyplasser med posisjon og størrelse, flyplassers konturer som punkter, spawn-områder |
| `objectives` | slagets mål, hver `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (replayens 1 eller 2, tom for begge), `name` (en erobringssone sin bokstav, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) med `position`, `radius` / `height` / `size` og `heading`, `source` (`replay` eller `mission`) og det som ellers er kjent (se [Mål](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | med navn og kjøretøy for begge sider; drap med våpenets engelske navn |
| `weapons` | hver rakett, missil, bombe, torpedo, hjelpetank og kastet last: når, hvor den ble sluppet (posisjon, holdning, hastighet), av hvilken enhet (den nærmeste innen 300 m og 1,5 s), hvor mange flysamples, hvor sist sett, når fjernet |
| `explosions`, `flak` | `PlayExplosionVisual` (posisjon, retning, type) og `PlayFlakExplosionVisual` (posisjon) |
| `awards` | opptakspillerens utmerkelser (`TextStreak`: first_blood, streaks, utfordringstellere) |
| `detections`, `unitStates` | `UnitDetected`-par av enheter; en melding (0xF093) med en enhets posisjon, holdning og hastighet hvis betydning ikke er kjent |
| `authorInstruments` | opptakspillerens cockpit-verdier (`ReplayCockpitParams`) etter instrumentnummer, høyst én per sekund; `known` navngir hvert nummer replayen sendte (navn, enhet, hvordan det ble kontrollert), `notNamed` de øvrige |
| `scoreboard` | hver spillers statistikk hver gang den endret seg (drap, dødsfall, assists, poeng, KI-drap, sjødrap, soner, skade, unndratte missiler, tropp), og hvert lags poengsum og sannsynlige gjenværende billetter over tid (se [Refleksjonsdata](aircraft.md#reflection-data)) |
| `economy` | slagets Silver Lions og forskningspoeng (se [Økonomi](economy.md)): totaler, per spiller, per kjøretøy, multiplikatorene, vinneren, kontrollene |
| `entityMessages` | entitetsmeldingene (0x20) etter klassenummer: antall, målmaler, størrelser |
| `chat` | hver chat-linje |
| `triggers`, `hints`, `missionProgress` | oppdragsskriptets handlinger (RunTriggerAction), hintene, fremdriftsmeldingene |
| `camera` | opptakspillerens replay-kameras felt hvert 0,25 s slik det ble sendt (tabellen har det som et spor) |
| `projectileHitReplays` | opptakspillerens egne treff og treff mot seg, med våpen og ammunisjon og deres engelske navn |
| `results` | hele resultatblokken slik spillet skrev den |
| `counts` | rader, hendelser, liv, typer, samples, entiteter etter mal, våpen, pakker lest og ikke lest, hver meldings-ID sett og de som ikke ble lest, droppede samples |
| `trackBreaks` | hvert kutt i et spor for et steg raskere enn enheten kan gå: hvor, hvor langt, hvor fort, og hva det mest sannsynlig er |
| `selfCheck` | kontrollene som er listet i [Slik leser den en replay](how-it-reads.md), beregnet ved hver konvertering; `stepSpeed` gir per type hastigheten mellom påfølgende rader i et spor slik visningsprogrammet setter dem sammen (median, 99. persentil, høyeste, og steg raskere enn mulig, som må være 0) |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
