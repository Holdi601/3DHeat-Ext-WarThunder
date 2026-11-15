---
title: "D'Match-Dokument"
nav_order: 7
lang: lb
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# D'Match-Dokument {#the-match-document}

![Den Ufank vun engem synthetesche Match-Dokument, a seng Schlësselen](../assets/img/match-document.svg)

`<match>.match.json` enthält alles, wat de Replay seet an net eng Zeil vun der
Tabell ass. Dem Viewer säi Match-Tab liest et.

## D'Gefecht {#the-battle}

| Schlëssel | Wat |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | d'Match-ID (wéi am Dateinumm); d'ID vun der Kaart; d'Level-Datei, déi se benotzt |
| `mission`, `missionKey` | den Numm vun der Mission a säi Schlëssel an den Textdateie vum Spill |
| `battleClass`, `environment`, `weather` | wéi den Header se gëtt |
| `sessionId`, `server` | d'Sessiouns-ID vum Gefecht; de Server |
| `replayVersion`, `flightLayout` | d'Versioun vum Replay-Format; d'Layout vum Fluchpaket, dat gelies gouf (`2025` oder `2026`) |
| `files` | d'Replay-Dateien, déi gelies goufen (eng, oder d'Deeler vun engem Server-Replay) |
| `started`, `timePlayed`, `replayEnd` | Startzäit (ISO, UTC); gespillte Sekonnen, aus de Resultater; Sekonne vum leschte Paket vum Replay |
| `author`, `authorUserId` | de opuelende Spiller a seng Gaijin-ID (Client-Replays) |
| `teams` | d'Teams am Gefecht (`1`, `2`) |
| `result` | `winner`, `status` (`success` oder `fail`, dem Auteur säin Ausgang), `authorTeam`, `teams` ([Wirtschaft](economy.md)) |
| `vehicleNames` | vu wou d'Gefiernimm koumen (deng Installatioun) an hir Sprooch |
| `conventions` | d'Eenheeten an d'Virzeeche vun der Tabell: Achsen, Zäit, life, track, alive, roll, a méi |

## Alles anescht {#everything-else}


| Schlëssel | Wat |
|---|---|
| `battle`, `difficulty`, `gameMode` | de Gefechtsmodus: `difficulty` `AB` / `RB` / `SB` (a säin Numm, an den Header-Byte), `gameMode` `ground` / `air` / `naval`, de Modus vun der Mission (`Dom`, `Conq`, `Bttl`, `I2M`, ...) a säin englesche Numm aus denger Installatioun (`Domination`, `Enduring Confrontation`), déi erlaabt Eenheetstypen (kuck [Battle-Modus](ground.md#battle-mode)) |
| `settings` | de Mission-blk nom Header: Modus, Émfeld, Wieder, Punkte- a Zäitlimiten, Länner, erlaabt Eenheetstypen, Wand, a `stars` (Breedegrad, Längegrad, Datum, Ortszäit) |
| `sky` | déi éischt `CustomWeatherParams`: Sonn- a Mounnrichtung, Wand, Himmelsfaarwen, Wollekenoffsets |
| `players`, `slots` | d'Zeil vun de Resultater pro Spiller (Kills, Buedem-Kills, Doudeger, Assists, Score, Eroberungen, Squad, Clan, Land, Line-up, d'uids, déi se gefuer hunn); d'Spiller-Slots vum Replay (Numm, User-ID, Team) |
| `units` | all Eenheet-Entitéit, déi de Replay erstallt huet: eid, uid, Template, Gefier, kind, type, Team, Spiller, Missiounsnumm, wéini erstallt an ewechgeholl, wou erstallt, wéi eng Komponente net konnte gelies ginn |
| `objects` | d'benannt Objete vun der Mission: Eroberungszonen a Fluchhäfe mat hirer Positioun a Gréisst, d'Ëmrësser vun de Fluchhäfen als Punkten, Spawn-Gebidder |
| `objectives` | d'Ziler vum Gefecht, jiddwer mat `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (dem Replay seng 1 oder 2, eidel fir béid), `name` (bei enger Eroberungszon hire Buschtaf, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) mat `position`, `radius` / `height` / `size` an `heading`, `source` (`replay` oder `mission`) a wat soss bekannt ass (kuck [Ziler](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | mat Nimm a Gefierer vu béide Säiten; Kills mam englesche Numm vun der Waff |
| `weapons` | all Rakéit, Rakéitegeschoss, Bomm, Torpedo, Zousazdank a ofgeworf Luedung: wéini, wou ofgeschoss (Positioun, Lag, Geschwindegkeet), vu wéi enger Eenheet (déi nootste bannent 300 m an 1.5 s), wéi vill Fluchechantillonen, wou zuletzt gesinn, wéini ewechgeholl |
| `explosions`, `flak` | `PlayExplosionVisual` (Positioun, Richtung, Aart) a `PlayFlakExplosionVisual` (Positioun) |
| `awards` | d'Auszeechnunge vum opuelende Spiller (`TextStreak`: first_blood, Serien, Challenge-Zieler) |
| `detections`, `unitStates` | `UnitDetected`-Pairen vun Eenheeten; eng Message (0xF093) mat der Positioun, der Lag an der Geschwindegkeet vun enger Eenheet, där hir Bedeitung net bekannt ass |
| `authorInstruments` | d'Cockpit-Wäerter vum opuelende Spiller (`ReplayCockpitParams`) no Instrumentnummer, héchstens ee pro Sekonn; `known` nennt all Nummer, déi dëse Replay geschéckt huet (Numm, Eenheet, wéi se gepréift gouf), `notNamed` den Rescht |
| `scoreboard` | d'Statistike vun all Spiller all Kéier, wann se sech geännert hunn (Kills, Doudeger, Assists, Score, KI-Kills, Marine-Kills, Zonen, Schued, Rakéiteausweichungen, Squad), an de Score vun all Team a séier Tickets iwwer d'Zäit (kuck [Reflection-Daten](aircraft.md#reflection-data)) |
| `economy` | d'Silver Lions a Fuerschungspunkte vum Gefecht (kuck [Wirtschaft](economy.md)): Totaler, pro Spiller, pro Gefier, d'Multiplikatoren, de Gewënner, d'Kontrollen |
| `entityMessages` | d'Entitéit-Messagen (0x20) no Klassennummer: Zuel, Zil-Templates, Gréissten |
| `chat` | all Chat-Zeil |
| `triggers`, `hints`, `missionProgress` | d'Aktioune vum Missiounsskript (RunTriggerAction), seng Hiweiser, seng Fortschrëtts-Messagen |
| `camera` | d'Felder vun der Replay-Kamera vum opuelende Spiller all 0.25 s, wéi geschéckt (d'Tabell huet se als Spur) |
| `projectileHitReplays` | dem opuelende Spiller seng eege Treffer an Treffer op hie, mat Waff a Munitioun an hiren englesche Nimm |
| `results` | de ganze Resultater-blk, wéi d'Spill en geschriwwen huet |
| `counts` | Zeilen, Evenementer, Liewen, Aarten, Echantillonen, Entitéite no Template, Waffen, Pakete gelies an net gelies, all Message-ID, déi gesi gouf, an déi net gelies goufen, verworf Echantillonen |
| `trackBreaks` | all Schnëtt vun enger Spur fir e Schrëtt méi séier, wéi d'Eenheet kann goen: wou, wéi wäit, wéi séier, a wat et héchstwahrscheinlech ass |
| `selfCheck` | d'Kontrollen, déi a [Wéi e Replay gelies gëtt](how-it-reads.md) opgelëscht sinn, bei all Émwandlung ausgerechent; `stepSpeed` gëtt pro Aart d'Geschwindegkeet tëscht openeen folgende Zeile vun enger Spur, wéi de Viewer se verbënnt (Median, 99. Perzentil, héchsten, a méi séier Schrëtt wéi méiglech, déi 0 musse sinn) |

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
