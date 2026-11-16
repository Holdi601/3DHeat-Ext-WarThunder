---
title: Das Match-Dokument
nav_order: 7
lang: "de"
source: match-document.md
source_hash: "3bd1f4245ad0"
nav_exclude: true
search_exclude: true
---
# Das Match-Dokument {#the-match-document}

![Der Anfang eines synthetischen Match-Dokuments und seine Schlüssel](../assets/img/match-document.svg)

`<match>.match.json` enthält alles, was das Replay sagt und das keine Zeile der
Tabelle ist. Der Match-Tab des Viewers liest es.

## Das Gefecht {#the-battle}

| Schlüssel | Was |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | die Match-Kennung (wie im Dateinamen); die Kennung der Karte; die Leveldatei, die sie benutzt |
| `mission`, `missionKey` | der Name der Mission und ihr Schlüssel in den Textdateien des Spiels |
| `battleClass`, `environment`, `weather` | so, wie der Kopf sie angibt |
| `sessionId`, `server` | die Sitzungs-ID des Gefechts; der Server |
| `replayVersion`, `flightLayout` | die Version des Replay-Formats; das gelesene Layout der Flugpakete (`2025` oder `2026`) |
| `files` | die gelesenen Replay-Dateien (eine, oder die Teile eines Server-Replays) |
| `started`, `timePlayed`, `replayEnd` | Startzeit (ISO, UTC); gespielte Sekunden aus den Ergebnissen; Sekunden des letzten Pakets des Replays |
| `author`, `authorUserId` | der aufnehmende Spieler und seine Gaijin-ID (Client-Replays) |
| `teams` | die Teams im Gefecht (`1`, `2`) |
| `result` | `winner`, `source` (`results.status` oder `tickets`), `status` (`success` oder `fail`, das Ergebnis des Autors), `authorTeam`, `teams`, `endReason` (`destruction`, `capture`, `tickets`, `time`) ([Wirtschaft](economy.md)) |
| `vehicleNames` | woher die Fahrzeugnamen stammen (deine Installation) und ihre Sprache |
| `conventions` | die Einheiten und Vorzeichen der Tabelle: Achsen, Zeit, Leben, Spur, `alive`, Rollwinkel und mehr |

## Alles Übrige {#everything-else}


| Schlüssel | Was |
|---|---|
| `battle`, `difficulty`, `gameMode` | der Gefechtsmodus: `difficulty` `AB` / `RB` / `SB` (samt Name und Kopf-Byte), `gameMode` `ground` / `air` / `naval`, der Modus der Mission (`Dom`, `Conq`, `Bttl`, `I2M`, ...) und sein englischer Name aus deiner Installation (`Domination`, `Enduring Confrontation`), die erlaubten Einheitentypen (siehe [Gefechtsmodus](ground.md#battle-mode)) |
| `settings` | der Missions-blk nach dem Kopf: Modus, Umgebung, Wetter, Punkt- und Zeitgrenzen, Länder, erlaubte Einheitentypen, Wind und `stars` (Breitengrad, Längengrad, Datum, Ortszeit) |
| `sky` | der erste `CustomWeatherParams`: Richtung von Sonne und Mond, Wind, Himmelsfarben, Wolkenversatz |
| `players`, `slots` | die Zeile der Ergebnisse je Spieler (Abschüsse, Bodenabschüsse, Tode, Assists, Punktzahl, Eroberungen, Staffel, Clan, Land, Aufstellung, die uids, die sie fuhren); die Spielerplätze des Replays (Name, Benutzer-ID, Team) |
| `units` | jede Einheiten-Entität, die das Replay erzeugt hat: eid, uid, template, vehicle, kind, type, team, player, Missionsname, wann sie entstand und entfernt wurde, wo sie entstand, welche Komponenten nicht gelesen werden konnten |
| `objects` | die benannten Objekte der Mission: Eroberungszonen und Flugplätze mit Position und Größe, die Umrisse der Flugplätze als Punkte, Spawn-Bereiche |
| `objectives` | die Ziele des Gefechts, jeweils mit `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 oder 2 aus dem Replay, leer für beide), `name` (bei einer Eroberungszone ihr Buchstabe, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) mit `position`, `radius` / `height` / `size` und `heading`, `source` (`replay` oder `mission`) und dem, was sonst bekannt ist (siehe [Ziele](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | mit den Namen und Fahrzeugen beider Seiten; Abschüsse mit dem englischen Namen der Waffe |
| `weapons` | jede Rakete, Lenkwaffe, Bombe, Torpedo, jeder Zusatztank und jede abgeworfene Ladung: wann, wo abgeworfen (Position, Lage, Geschwindigkeit), von welcher Einheit (die nächste innerhalb von 300 m und 1,5 s), wie viele Messwerte des Flugs, wo zuletzt gesehen, wann entfernt |
| `explosions`, `flak` | `PlayExplosionVisual` (Position, Richtung, Art) und `PlayFlakExplosionVisual` (Position) |
| `awards` | die Auszeichnungen des aufnehmenden Spielers (`TextStreak`: first_blood, Serien, Zähler der Herausforderungen) |
| `detections`, `unitStates` | `UnitDetected`-Paare von Einheiten; eine Nachricht (0xF093) mit Position, Lage und Geschwindigkeit einer Einheit, deren Bedeutung nicht bekannt ist |
| `authorInstruments` | die Cockpit-Werte des aufnehmenden Spielers (`ReplayCockpitParams`) nach Instrumentennummer, höchstens einer pro Sekunde; `known` benennt jede Nummer, die dieses Replay gesendet hat (Name, Einheit, wie geprüft), `notNamed` den Rest |
| `scoreboard` | die Statistik jedes Spielers jedes Mal, wenn sie sich änderte (Abschüsse, Tode, Assists, Punktzahl, KI-Abschüsse, Marine-Abschüsse, Zonen, Schaden, Raketenausweichen, Staffel), und die Punktzahl und wahrscheinlichen Tickets jedes Teams im Zeitverlauf (siehe [Spiegelungsdaten](aircraft.md#reflection-data)) |
| `economy` | die Silberlöwen und Forschungspunkte des Gefechts (siehe [Wirtschaft](economy.md)): Summen, je Spieler, je Fahrzeug, die Multiplikatoren, der Sieger, die Prüfungen |
| `entityMessages` | die Entitätsnachrichten (0x20) nach Klassennummer: Anzahl, Zieltemplates, Größen |
| `chat` | jede Chatzeile |
| `triggers`, `hints`, `missionProgress` | die Aktionen des Missionsskripts (RunTriggerAction), seine Hinweise, seine Fortschrittsmeldungen |
| `camera` | die Felder der Replay-Kamera des aufnehmenden Spielers alle 0,25 s, so wie gesendet (die Tabelle hat sie als Spur) |
| `projectileHitReplays` | die eigenen Treffer des aufnehmenden Spielers und die Treffer, die er erhält, mit Waffe und Munition und ihren englischen Namen |
| `results` | der ganze Ergebnis-blk, so wie das Spiel ihn geschrieben hat |
| `counts` | Zeilen, Ereignisse, Leben, Arten, Messwerte, Entitäten nach Template, Waffen, gelesene und nicht gelesene Pakete, jede gesehene Nachrichten-ID und die nicht gelesenen, verworfene Messwerte |
| `trackBreaks` | jede Trennung einer Spur bei einem Schritt, schneller als die Einheit fahren kann: wo, wie weit, wie schnell, und was es am wahrscheinlichsten ist |
| `selfCheck` | die Prüfungen aus [So liest es ein Replay](how-it-reads.md), bei jeder Umwandlung berechnet; `stepSpeed` gibt je Art die Geschwindigkeit zwischen aufeinanderfolgenden Zeilen einer Spur an, so wie der Viewer sie verbindet (Median, 99. Perzentil, höchste, und Schritte, die schneller als möglich sind; das muss 0 sein) |

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
