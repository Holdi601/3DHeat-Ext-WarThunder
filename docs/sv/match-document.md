---
title: "Matchdokumentet"
nav_order: 7
lang: sv
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Matchdokumentet {#the-match-document}

![Början av ett syntetiskt matchdokument, och dess nycklar](../assets/img/match-document.svg)

`<match>.match.json` håller allt repriset säger som inte är en rad i tabellen. Visarens
Match-flik läser det.

## Striden {#the-battle}

| Nyckel | Vad |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | matchens id (som i filnamnet); kartans id; nivåfilen den använder |
| `mission`, `missionKey` | uppdragets namn och dess nyckel i spelets textfiler |
| `battleClass`, `environment`, `weather` | så som headern anger dem |
| `sessionId`, `server` | stridens session-id; servern |
| `replayVersion`, `flightLayout` | repriformatets version; den läsda flygpaketslayouten (`2025` eller `2026`) |
| `files` | de repriserfiler som lästes (en, eller delarna av en serverrepris) |
| `started`, `timePlayed`, `replayEnd` | starttid (ISO, UTC); spelade sekunder, från resultaten; sekunder till repriets sista paket |
| `author`, `authorUserId` | den inspelande spelaren och dess Gaijin-id (klientrepriser) |
| `teams` | lagen i striden (`1`, `2`) |
| `result` | `winner`, `status` (`success` eller `fail`, författarens utfall), `authorTeam`, `teams` ([Ekonomi](economy.md)) |
| `vehicleNames` | varifrån fordonsnamnen kom (din installation) och deras språk |
| `conventions` | tabellens enheter och tecken: axlar, tid, liv, bana, alive, rulle, med mera |

## Allt annat {#everything-else}

| Nyckel | Vad |
|---|---|
| `battle`, `difficulty`, `gameMode` | stridsläget: `difficulty` `AB` / `RB` / `SB` (med sitt namn och headerbyten), `gameMode` `ground` / `air` / `naval`, uppdragets läge (`Dom`, `Conq`, `Bttl`, `I2M`, ...) och dess engelska namn från din installation (`Domination`, `Enduring Confrontation`), de tillåtna enhetstyperna (se [Stridsläge](ground.md#battle-mode)) |
| `settings` | uppdragets blk efter headern: läge, miljö, väder, poäng- och tidsgränser, länder, tillåtna enhetstyper, vind, och `stars` (latitud, longitud, datum, lokal tid) |
| `sky` | den första `CustomWeatherParams`: sol- och månriktning, vind, himmelsfärger, molnförskjutningar |
| `players`, `slots` | resultatets rad per spelare (dödsfall, markdödsfall, egna dödsfall, assists, poäng, erövringar, trupp, klan, land, uppställning, uid:na de förde); repriets spelarplatser (namn, användar-id, lag) |
| `units` | varje enhetsentitet repriset skapade: eid, uid, mall, fordon, slag, typ, lag, spelare, uppdragsnamn, när den skapades och togs bort, var den skapades, vilka komponenter som inte kunde läsas |
| `objects` | uppdragets namngivna objekt: erövringszoner och flygfält med deras position och storlek, flygfältens konturer som punkter, spawnområden |
| `objectives` | stridens mål, var och en av `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (repriets 1 eller 2, tomt för båda), `name` (en erövringszon sin bokstav, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) med `position`, `radius` / `height` / `size` och `heading`, `source` (`replay` eller `mission`) och vad mer som är känt (se [Mål](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | med namn och fordon för båda sidor; dödsfall med vapnets engelska namn |
| `weapons` | varje raket, robot, bomb, torped, släppbar tank och kastad last: när, var den släpptes (position, attityd, hastighet), av vilken enhet (den närmaste inom 300 m och 1,5 s), hur många flygmätpunkter, var den sist sågs, när den togs bort |
| `explosions`, `flak` | `PlayExplosionVisual` (position, riktning, slag) och `PlayFlakExplosionVisual` (position) |
| `awards` | den inspelande spelarens utmärkelser (`TextStreak`: first_blood, serier, utmaningsräknare) |
| `detections`, `unitStates` | `UnitDetected`-par av enheter; ett meddelande (0xF093) med en enhets position, attityd och hastighet vars betydelse inte är känd |
| `authorInstruments` | den inspelande spelarens cockpitvärden (`ReplayCockpitParams`) per instrumentnummer, högst ett per sekund; `known` namnger varje nummer som repriset skickade (namn, enhet, hur det kontrollerades), `notNamed` resten |
| `scoreboard` | varje spelares statistik varje gång den ändrades (dödsfall, egna dödsfall, assists, poäng, AI-dödsfall, sjödödsfall, zoner, skada, undvikna robotar, trupp), och varje lags poäng och troliga biljetter över tid (se [Reflektionsdata](aircraft.md#reflection-data)) |
| `economy` | stridens Silver Lions och forskningspoäng (se [Ekonomi](economy.md)): summor, per spelare, per fordon, multiplikatorerna, vinnaren, kontrollerna |
| `entityMessages` | entitetsmeddelandena (0x20) per klassnummer: antal, mallar, storlekar |
| `chat` | varje chattrad |
| `triggers`, `hints`, `missionProgress` | uppdragsskriptets åtgärder (RunTriggerAction), dess tips, dess förloppsmeddelanden |
| `camera` | repriskamerans fält var 0,25 s som de skickades (tabellen har den som en bana) |
| `projectileHitReplays` | den inspelande spelarens egna träffar och att bli träffad, med vapen och ammunition och deras engelska namn |
| `results` | hela resultatblocket så som spelet skrev det |
| `counts` | rader, händelser, liv, slag, mätpunkter, entiteter per mall, vapen, paket lästa och inte lästa, varje meddelande-id som setts och de som inte lästes, bortkastade mätpunkter |
| `trackBreaks` | varje klipp av en bana för ett steg snabbare än enheten kan gå: var, hur långt, hur snabbt, och vad det mest sannolikt är |
| `selfCheck` | kontrollerna som listas i [Så läser den en repris](how-it-reads.md), beräknade vid varje konvertering; `stepSpeed` ger per slag hastigheten mellan på varandra följande rader i en bana så som visaren sammanfogar dem (median, 99:e percentilen, högsta, och steg snabbare än möjligt, vilket måste vara 0) |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
