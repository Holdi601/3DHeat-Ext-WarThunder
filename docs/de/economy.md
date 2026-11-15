---
title: Wirtschaft
nav_order: 14
lang: de
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Wirtschaft {#economy}

Was das Gefecht gekostet und eingebracht hat, als Spalten in seinen Ereigniszeilen, gelesen aus **deiner Installation zum Zeitpunkt der Umwandlung**
(`char.vromfs.bin`: `config/wpcost.blk` je Fahrzeug, `config/warpoints.blk` und `config/rank.blk`; die Waffen-blks
von `aces.vromfs.bin` sagen, welche Modifikation jede Granate ist). Keine Zahl des Spiels steht in diesem Repository: die
Werte landen nur in deiner eigenen Ausgabe. Ohne die `char.vromfs.bin` der Installation wird keine Wirtschaft geschrieben
(`economy.available` false). Die Preise sind die des Schwierigkeitsgrads des Gefechts (`repairCostHistorical` für RB,
`...Arcade` für AB, `...Simulation` für SB).

| Spalte | Zeilen | Was |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (eine Granate, die nach einem Schuss nachgeladen wird, Bodenfahrzeuge), `launch` (Flugzeuge, Hubschrauber) | SL, was die Granate, Rakete, Lenkwaffe oder Bombe gekostet hat |
| `cost_lost_sl` | `death` eines Fahrzeugs eines Spielers | die Reparaturkosten des Fahrzeugs (Serie; das voll ausgebaute im Block) |
| `earn_sl`, `earn_rp` | `reward` (neues Ereignis, am Ort und zur Zeit des Verdienenden) | verdiente SL und RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | jede Zeile mit einem `cost_*` oder `earn_sl` | `SL` (`earn_rp` sind Forschungspunkte) |
| `econ_basis` | dasselbe | `install` (ein Preis aus der Installation gelesen) oder `inferred` (berechnet, siehe unten) |

**Wer gewonnen hat.** `won` (0/1) auf jeder Zeile eines Teams, wenn das Replay es angibt: Die Ergebnisse eines Client-Replays
tragen das eigene Ergebnis des Autors (`status`: `success` oder `fail`), also hat das Team des Autors gewonnen oder verloren
und das andere Team umgekehrt. `result` im Match-Dokument sagt es (`winner`, `status`, `authorTeam`). Server-Replays und
Replays, die vor dem Ende abbrechen, tragen kein Ergebnis (der `status` eines Server-Replays ist immer `success` und nennt
keinen Autor). Beide Arten enthalten auch keine eingebauten Modifikationen: Die Ergebnisse listen die Fahrzeuge jedes Spielers
nur nach Name und Typ. Dort bleibt `won` leer.

Das Kostenmodell des Viewers liest die Spalten `cost_*` (und `earn_*`) mit `currency`. Die Summe von `cost_fired_sl +
cost_lost_sl` zeigt, wo SL ausgegeben und verloren wurden, `earn_sl`, wo sie verdient wurden. Die Belohnung eines Abschusses
steht in seiner `reward`-Zeile, nicht in der `kill`-Zeile, so wird nichts doppelt gezählt.

- **Granaten** (`install`, wenn der Munitionsplatz des Schusses bekannt ist, ein Abschuss hat ihn benannt, siehe [Trefferergebnisse](hits.md#hit-outcomes);
  sonst `inferred`: der mittlere Preis der Granaten, die dieses Geschütz auf diesem Fahrzeug verschießen kann; eine Serien-Granate ist
  kostenlos; Maschinengewehre zählt das Replay nicht und sie kosten nichts).
- **Starts** (`inferred`): Das Spiel bepreist die Waffenvorgabe eines Flugzeugs pro Einsatz, nicht pro Stück. Ein Stück
  ist der Median über die bepreisten Vorgaben des Fahrzeugs von Preis / Stück (`sum_weapons`; Gegenmaßnahmen und Zusatztanks
  ausgenommen); 0, wo seine Vorgaben kostenlos sind.
- **Belohnungen** (alle `inferred`): Das Replay enthält keinen Belohnungsdatensatz. Der Ergebnisblock hat nur Punkte und Zählungen,
  keine Nachricht trägt Silberlöwen (geprüft an Client- und Server-Replays). Ein `kill` bringt `aKill` x das `rewardMul<mode>` des
  Killers x das Gewicht der Fahrzeugklasse des Opfers (`units` in warpoints.blk, nach seiner `unitClass`; KI-Einheiten nach
  ihrer Art) x `aiKillK` bei einem KI-Opfer x `groundKillMul`, wenn ein Flugzeug eine Bodeneinheit abschießt. RP genauso mit
  `expMul` und den Gewichten aus rank.blk. Jeder andere Schritt der Punktzahl eines Spielers im nachgebildeten Scoreboard ist eine
  Belohnung, die ihre Punkte zu den SL des Gefechts pro Punkt wert ist (ein Abschuss-SL über den Median-Punkten der Abschuss-Schritte,
  das `pointsPerKill` des Blocks). Ihr Typ ist der Zähler, der mit ihr gestiegen ist (Assists, eroberte Zonen, Zonenschaden,
  Schadensbelohnung, Raketenausweichen). Sonst der kritische oder schwere Treffer dieses Spielers innerhalb von 3 s, sonst eine
  Entdeckung der Einheit des Spielers innerhalb von 2 s (`scouting`), sonst `other`. `battle_end` ist `winK` (gewonnen) oder `defeatK`
  (verloren) der Verdienste des Spielers im Gefecht; Sieger ist, wer mehr Tickets übrig hat, dann nach Punktzahl. Prämienzeit,
  Booster, Besatzung und Modifikationen sind nicht bekannt und werden nicht angewendet. Die Abschussbudgets der Bodengefechte
  (`def_ground_kill_wp_budget*`) sind nicht nachgebildet.

Die `economy` des Match-Dokuments (und in einem `.3dheat`-Container `extensions["heat3d/economy"]` im Manifest)
enthält `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (dasselbe je Spieler, mit `netSl`), `vehicles` (je Fahrzeug eines Spielers: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` und `check` (wie viele Zeilen jeder Art bepreist,
geschätzt oder nicht bepreist wurden).

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
