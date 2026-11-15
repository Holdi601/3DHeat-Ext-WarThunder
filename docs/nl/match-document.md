---
title: "Het wedstrijddocument"
nav_order: 7
lang: "nl"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Het wedstrijddocument {#the-match-document}

![Het begin van een synthetisch wedstrijddocument, en zijn sleutels](../assets/img/match-document.svg)

`<match>.match.json` bevat alles wat de replay zegt en dat geen rij van de tabel is. Het tabblad Match van de viewer leest het.

## Het gevecht {#the-battle}

| Sleutel | Wat |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | het wedstrijd-id (zoals in de bestandsnaam); het id van de kaart; het levelbestand dat ze gebruikt |
| `mission`, `missionKey` | de naam van de missie en haar sleutel in de tekstbestanden van het spel |
| `battleClass`, `environment`, `weather` | zoals de kop ze geeft |
| `sessionId`, `server` | het sessie-id van het gevecht; de server |
| `replayVersion`, `flightLayout` | de versie van het replayformaat; de gelezen indeling van de vluchtpakketten (`2025` of `2026`) |
| `files` | de gelezen replaybestanden (één, of de delen van een server-replay) |
| `started`, `timePlayed`, `replayEnd` | starttijd (ISO, UTC); gespeelde seconden, uit de resultaten; seconden van het laatste pakket van de replay |
| `author`, `authorUserId` | de opnemende speler en zijn Gaijin-id (clientreplays) |
| `teams` | de teams in het gevecht (`1`, `2`) |
| `result` | `winner`, `status` (`success` of `fail`, de uitkomst van de auteur), `authorTeam`, `teams` ([Economie](economy.md)) |
| `vehicleNames` | waar de voertuignamen vandaan komen (je installatie) en hun taal |
| `conventions` | de eenheden en tekens van de tabel: assen, tijd, leven, spoor, levend, roll, en meer |

## Al het andere {#everything-else}

| Sleutel | Wat |
|---|---|
| `battle`, `difficulty`, `gameMode` | de gevechtsmodus: `difficulty` `AB` / `RB` / `SB` (en zijn naam, en de kopbyte), `gameMode` `ground` / `air` / `naval`, de modus van de missie (`Dom`, `Conq`, `Bttl`, `I2M`, ...) en zijn Engelse naam uit je installatie (`Domination`, `Enduring Confrontation`), de toegestane eenheidstypen (zie [Gevechtsmodus](ground.md#battle-mode)) |
| `settings` | de missie-blk na de kop: modus, omgeving, weer, score- en tijdslimieten, landen, toegestane eenheidstypen, wind, en `stars` (breedtegraad, lengtegraad, datum, lokale tijd) |
| `sky` | de eerste `CustomWeatherParams`: richting van zon en maan, wind, hemelkleuren, wolkverschuivingen |
| `players`, `slots` | de regel van de resultaten per speler (kills, grondkills, doden, assists, score, veroveringen, squad, clan, land, opstelling, de uids die ze bestuurden); de spelersslots van de replay (naam, gebruikers-id, team) |
| `units` | elke eenheidsentiteit die de replay aanmaakte: eid, uid, sjabloon, voertuig, soort, type, team, speler, naam in de missie, wanneer ze aangemaakt en verwijderd werd, waar ze aangemaakt werd, welke componenten niet gelezen konden worden |
| `objects` | de benoemde objecten van de missie: veroveringszones en vliegvelden met hun positie en grootte, omtrekken van vliegvelden als punten, spawngebieden |
| `objectives` | de doelen van het gevecht, elk met een `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (de 1 of 2 van de replay, leeg voor beide), `name` (een veroveringszone zijn letter, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) met `position`, `radius` / `height` / `size` en `heading`, `source` (`replay` of `mission`) en wat verder bekend is (zie [Doelen](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | met namen en voertuigen van beide kanten; kills met de Engelse naam van het wapen |
| `weapons` | elke raket, missiel, bom, torpedo, afwerptank en afgeworpen lading: wanneer, waar afgeworpen (positie, houding, snelheid), door welke eenheid (de dichtstbijzijnde binnen 300 m en 1,5 s), hoeveel vluchtsamples, waar het laatst gezien, wanneer verwijderd |
| `explosions`, `flak` | `PlayExplosionVisual` (positie, richting, soort) en `PlayFlakExplosionVisual` (positie) |
| `awards` | de onderscheidingen van de opnemende speler (`TextStreak`: first_blood, reeksen, uitdagingstellers) |
| `detections`, `unitStates` | `UnitDetected`-paren van eenheden; een bericht (0xF093) met de positie, houding en snelheid van een eenheid waarvan de betekenis niet bekend is |
| `authorInstruments` | de cockpitwaarden van de opnemende speler (`ReplayCockpitParams`) per instrumentnummer, hooguit één per seconde; `known` noemt elk nummer dat deze replay stuurde (naam, eenheid, hoe het gecontroleerd is), `notNamed` de rest |
| `scoreboard` | de statistieken van elke speler telkens als ze veranderden (kills, doden, assists, score, AI-kills, scheepskills, zones, schade, ontweken raketten, squad), en de score en waarschijnlijke tickets van elk team door de tijd (zie [Reflectiegegevens](aircraft.md#reflection-data)) |
| `economy` | de Zilveren Leeuwen en onderzoekspunten van het gevecht (zie [Economie](economy.md)): totalen, per speler, per voertuig, de vermenigvuldigers, de winnaar, de controles |
| `entityMessages` | de entiteitsberichten (0x20) per klassenummer: aantal, doelsjablonen, groottes |
| `chat` | elke chatregel |
| `triggers`, `hints`, `missionProgress` | de acties van het missiescript (RunTriggerAction), de hints, de voortgangsberichten van de missie |
| `camera` | de velden van de replaycamera van de opnemende speler elke 0,25 s zoals ze gestuurd werden (de tabel heeft die als spoor) |
| `projectileHitReplays` | de eigen treffers van de opnemende speler en wat hem trof, met wapen en munitie en hun Engelse namen |
| `results` | het hele resultaten-blk zoals het spel het schreef |
| `counts` | rijen, gebeurtenissen, levens, soorten, samples, entiteiten per sjabloon, wapens, pakketten gelezen en niet gelezen, elk berichtid gezien en die niet gelezen, samples weggelaten |
| `trackBreaks` | elke afsnijding van een spoor voor een stap sneller dan de eenheid kan gaan: waar, hoe ver, hoe snel, en wat het meest waarschijnlijk is |
| `selfCheck` | de controles uit [Hoe het een replay leest](how-it-reads.md), bij elke omzetting berekend; `stepSpeed` geeft per soort de snelheid tussen opeenvolgende rijen van een spoor zoals de viewer ze verbindt (mediaan, 99e percentiel, hoogste, en stappen sneller dan mogelijk, wat 0 moet zijn) |

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
