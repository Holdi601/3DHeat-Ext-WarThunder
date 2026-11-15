---
title: Die Tabelle
nav_order: 6
lang: de
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Die Tabelle {#the-table}

![Die Tabelle eines synthetischen Replays, zusammengefasst](../assets/img/table.svg)

Eine Zeile je Messwert oder Ereignis, 105 Spalten ([Spaltenliste](../columns.md), aus dem Code erzeugt);
in der Fußzeile, unter `heat3d`, stehen die Leseanweisungen des Viewers, sodass der Viewer kein
Formular ausgefüllt braucht.

| Spalte | Was |
|---|---|
| `time` | Sekunden auf der eigenen Uhr des Replays |
| `event` | `position`; Ereigniszeilen liegen zu ihrem Zeitpunkt auf der Spur (zwischen zwei Messwerten, auf der Linie zwischen ihnen); `kill` (beim Killer), `death` (beim Opfer), `hit_critical` / `hit_severe` (bei der getroffenen Einheit), `module_destroyed` (bei der Einheit), `launch` (bei der Einheit, die eine Waffe abgeworfen hat), `impact` (der letzte Messwert einer Waffe, wenn sie direkt danach entfernt wurde); `explosion` und `flak` (0xD08E, 0xD01F) an ihrer Position, Art `effect`, ohne Spur, mit der Richtung der Explosion, wo es eine gibt; `shot` (ein Geschoss, das getroffen hat, beim Schützen), `gun_shot`, `fire_start`, `fire_stop` (der Feuerstoß eines Geschützes, nicht ein brennendes Fahrzeug), `fire_on`, `fire_off` (ein brennendes Fahrzeug, siehe [Brände am Fahrzeug](hits.md#vehicle-fires)), `reward` (verdiente Silberlöwen und Forschungspunkte, siehe [Wirtschaft](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (siehe [Nachrichten an Einheiten](how-it-reads.md#messages-to-units)); `despawn`: die letzte Zeile einer Spur, deren Einheit verschwunden ist, bevor das Replay endet (siehe [Ende einer Spur](ground.md#end-of-a-track)) |
| `track` | was der Viewer als eine Sache zeichnet: ein Leben einer Einheit oder der Flug einer Waffe - `<Spieler oder Fahrzeug> #<hex>` (der Viewer zeigt den Namen ohne den Teil `#`) |
| `x`, `y`, `z` | die Meter des Spiels: x Osten, y oben, z Norden (die Hinweise spiegeln z, sodass Norden nicht nach Süden gezeichnet wird) |
| `player` | der Name des Spielers; eine KI-Einheit `<VehicleName> #<uid>` (zum Beispiel `F-15A #204`); `uid <n>`, wenn nichts sie benennt; bei einer Waffe, wer sie abgeworfen hat |
| `userId`, `team` | die Gaijin-ID des Spielers und das Team (`1`, `2`) |
| `ai`, `isPlayer` | `ai` ist true für jede Einheit, die kein Spielerkonto fährt (Missionseinheiten, KI-Flugzeuge, Bodenziele, Flugabwehr, Schiffe ohne Spieler, Platzhalter), `isPlayer` das Gegenteil: Ein Spieler ist eine Einheit, deren Entität einen Spielerplatz mit einer Gaijin-ID nennt. Eine Waffe hat die ihres Abschussgeräts; leer, wenn unbekannt |
| `match` | die Match-Kennung (das `match` des Match-Dokuments) in jeder Zeile; die Hinweise ordnen sie als Sitzung zu, sodass zwei geladene Replays nie Spuren verbinden |
| `life` | `uid#n`: die Spur einer Einheit, getrennt, wenn die uid auf eine andere Einheit übergeht, die Einheit sich schneller bewegt, als sie kann (ein Wiedereinstieg, ein Nachladen, das Spiel bewegt sie, der Client korrigiert eine entfernte Einheit; siehe Teleportationen in [So liest es ein Replay](how-it-reads.md#what-is-read-and-the-check)) oder lange nicht gesehen wurde; `w<hex>` der Flug einer Waffe (`w<hex>#n` nach einer Trennung) |
| `uid` | die ID der Einheit im Replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (eine Straßenbahn oder ein Schienenwagen, den das Level platziert, siehe [Szenen-Einheiten](objectives.md#scene-units-trams-and-rail-wagons)); Waffen `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` die Replay-Kamera des aufnehmenden Spielers (siehe [Die Kamera](ground.md#the-camera)) |
| `type` | der eigene Typ des Spiels, wo die Ergebnisse ihn nennen (`fighter`, `assault`, `destroyer`, `gun_boat`), sonst wie `kind` |
| `Vehicle` | die Fahrzeug-ID des Spiels (`f_15a`, `germ_flakpz_I_Gepard`), zu der die Figuren des Viewers passen |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | der englische Name des Fahrzeugs aus der Lokalisierung deiner Installation (`Pz.Kpfw. III Ausf. J1`, kurz `Pz.III J1`) und sein Schlüssel (`germ_pzkpfw_III_ausf_J_0`); die Länderzeichen der Schrift des Spiels fallen weg. Wo das Spiel nichts nennt oder keine Installation gefunden wird, ist der Name die ID und der Schlüssel leer |
| `mission` | der Name der Einheit in der Mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | wohin die Einheit zeigt (der Blickvektor): Flugzeuge aus der Lage des Flugmodells, Bodeneinheiten und Schiffe aus ihrer eigenen, Waffen entlang ihres Flugs |
| `heading`, `pitch`, `roll` | dasselbe in Grad; der Kurs ist der Kompass, im Uhrzeigersinn von Norden, das Nicken positiv mit der Nase nach oben, das Rollen positiv mit dem rechten Flügel nach unten (das Flugmodell sendet das umgekehrte Vorzeichen, siehe [Lage, geprüft](aircraft.md#attitude-checked); eine Bodeneinheit mit der rechten Seite nach unten). Die Hinweise sagen es unter `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | der Hauptturm eines Panzers - wohin das Geschütz zeigt, nicht wohin sein Spieler schaut; der Wert des Replays, auf die Drehgeschwindigkeit des Turmantriebs gehalten und auf die Linie jedes Schusses des Hauptgeschützes gesetzt (siehe [Geschütztürme](ground.md#turrets)): sein Gierwinkel relativ zur Wanne (Grad, im Uhrzeigersinn von oben gesehen positiv, 0 geradeaus) und der Höhenwinkel seines Geschützes relativ zur Wanne (Grad, nach oben positiv); `turrets` jeder Turm des Fahrzeugs als `yaw pitch;yaw pitch;...` in seiner eigenen Reihenfolge (ein ungenutzter Platz steht als `0.00 0.00`). Panzer, Flugabwehr, Schützenpanzer und Lkw, in Client- und Server-Replays; nicht Schiffe (siehe [Geschütztürme](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | der Hauptturm, so wie das Replay ihn sendet; `turretYaw` / `gunPitch` sind er, an die Drehgeschwindigkeit des Turmantriebs gehalten und auf die Linie jedes Schusses des Hauptgeschützes gesetzt (siehe [Geschütztürme](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | wohin der Spieler schaut (mit der Kamera zielt) in der Welt: Kompassgrad (0 Norden, im Uhrzeigersinn) und Grad nach oben, dieselbe Konvention wie `aimHeading` / `aimPitch` (anders als `turretYaw` / `gunPitch`, die relativ zur Wanne bleiben). Der Panzer jedes Spielers in einem Server-Replay, im Client-Replay den des aufnehmenden Spielers; leer, wo der Spieler nirgends zielt (alle vier Zielwerte 0). Der Turm folgt ihr mit seiner eigenen Schwenkgeschwindigkeit, daher unterscheiden sich beide, während er sich dreht (siehe [Geschütztürme](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | der eigene Panzer des aufnehmenden Spielers: wohin er zielt (Kompassgrad, Grad nach oben, die Entfernung in m; 2000, wenn nichts im Visier ist); Kamerazeilen: wohin der Spieler zielt (Kurs, Nicken) |
| `zoom` | Kamerazeilen: die Vergrößerung der Kamera (siehe [Die Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | das `AB`, `RB` oder `SB` des Gefechts und `ground`, `air` oder `naval` in jeder Zeile (siehe [Gefechtsmodus](ground.md#battle-mode)) |
| `extrapolated` | ein Flugzeug-Messwert, der die Totrechnung des Clients ist und kein empfangener Zustand (siehe [Totrechnung](aircraft.md#dead-reckoning-and-the-smoother)); ein Messwert einer Bombe, der aus ihrem Abwurf berechnet wurde (siehe Bomben ohne Flugdatensätze in [So liest es ein Replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | wie weit der Glätter den Messwert verschoben hat (m), und die eigene Position und Lage des Replays (Rollen mit dem Vorzeichen der Tabelle) |
| `targetX`, `targetY`, `targetZ` | der Trefferpunkt eines `shot` |
| `hitOutcome`, `hitFlags` | das Ergebnis eines `shot` auf einer Bodeneinheit: `kill`, `critical`, `penetration` oder `nonpenetration` (abgeprallt oder aufgehalten: Das Replay unterscheidet einen Abpraller nicht), aus den Bit, die der Server mit dem Treffer sendet (`hitFlags`, roh); leer, wo keines gesendet wird (Flugzeuge, Schiffe). Siehe [Trefferergebnisse](hits.md#hit-outcomes) |
| `hitShell` | die Geschosssignatur eines `shot`: vier Bytes der Treffernachricht (roher Hex); eine Signatur kann für verschiedene Geschosse stehen (120 und 125 mm APFSDS teilen sich eine), daher bleibt sie roh und wird nicht als Kaliber gelesen |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | die Munition eines `shot`: ihre Art (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) und Kennung (`125mm_3bm46`), wo ein Abschuss den Platz des Schützen nennt, sonst `explosive` (der Trefferstoß) oder `kinetic`; das `weapon/slot` des Geschützes aus seinen Nachladungen; das Kaliber in mm aus den Waffendateien der Installation. Siehe [Trefferergebnisse](hits.md#hit-outcomes) |
| `rpm` | die Drehzahl des Triebwerks eines Flugzeugs (der Mittelwert über seine Triebwerke), wie zuletzt gesendet, innerhalb von 2 s |
| `vx`, `vy`, `vz` | die Geschwindigkeit eines Flugzeugs, wie sein Flugeintrag sie sendet (m/s, die Achsen des Spiels; Geschwindigkeiten über 500 m/s lesen sich als 500) |
| `engine`, `afterburner`, `engineCondition` | die Triebwerke eines Flugzeugs aus seinem Flugeintrag: `off`, `starting`, `running`, `dead` (mit `/` verbunden, wenn sich seine Triebwerke unterscheiden); der Nachbrenner 0-1; ein Byte, das nur gesendet wird, nachdem das Triebwerk getroffen wurde |
| `weaponName` | Abschüsse und Tode: die Waffe oder Munition im Englisch deiner Installation (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | nur das Flugzeug des aufnehmenden Spielers: der Schub 0-1,1 aus seinem Cockpit (1,1 bei Kriegs-Notleistung oder Nachbrenner; sonst die Fünfzehntel seines Flugeintrags), die Steuerung -1..1 aus seinem Flugeintrag (Höhenruder positiv beim Ziehen, Querruder positiv beim Rollen nach rechts), die verbleibenden Schüsse je Waffe (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | nur das Flugzeug des aufnehmenden Spielers, aus seinem Cockpit: angezeigte Fluggeschwindigkeit und Steigrate (m/s), Treibstoff, Ladedruck (atm), Fahrwerk (0-1, 1 ausgefahren), Öl- und Zylinderkopftemperatur, wo sein Cockpit die Anzeige hat |
| `speed` | m/s über etwa zwei Sekunden der Spur (hier berechnet; das Replay sendet keine Geschwindigkeit für andere Einheiten) |
| `alive` | 0 für die Messwerte einer Einheit nach ihrem Tod (ihr Wrack): das einer Bodeneinheit oder eines Schiffs, bis das Spiel es entfernt oder seine Messwerte enden, das eines Flugzeugs höchstens 60 s |
| `otherVehicle`, `otherLife` | das Opfer eines `shot`: sein Fahrzeug und sein `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | der Trefferpunkt eines `shot` im eigenen Koordinatensystem des Opfers (m; x vorwärts, y oben, z links; siehe [Nachrichten an Einheiten](how-it-reads.md#messages-to-units)) und die Richtung, aus der der Schuss kam, umgerechnet in dieses Koordinatensystem über die damalige Lage des Opfers |
| `hitPart`, `hitFlag` | die Treffernachricht eines `shot`: ihr Teilwort, so wie gesendet, und ihr höchstes Byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | was das Gefecht gekostet und eingebracht hat und wer gewonnen hat: siehe [Wirtschaft](economy.md) |
| `other`, `weapon` | Abschüsse: die andere Seite und die Waffe; Treffer: wer getroffen hat (aus der uid des Datensatzes, sonst aus seinem Spielerplatz), deren Fahrzeug; Starts: die Waffe; zerstörte Module: wer die Einheit zuletzt innerhalb von 5 s davor getroffen hat, und `part <n>` |

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
