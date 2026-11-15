---
title: So liest es ein Replay
nav_order: 10
lang: "de"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# So liest es ein Replay {#how-it-reads-a-replay}

Diese Seite ist für Leute, die wissen wollen, was der Umwandler liest, wie das
geprüft wurde und wie weit man daher jeder Spalte trauen kann. Zum Umwandeln von
Replays brauchst du sie nicht.

Das Lesen wurde an Client-Replays von Luft-Arcade-, Luft-Simulator- und
Seegefechten geprüft, an Server-Replays von Bodengefechten und, für die Layouts
von 2025, an den öffentlichen Beispiel-Replays von
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Jede Prüfung vergleicht einen Wert mit etwas, das das Replay auf eine zweite,
unabhängige Weise sagt. Hier werden nur die Methode und die Übereinstimmung angegeben.

## Was gelesen wird, und die Prüfung {#what-is-read-and-the-check}

| Teil | Stand, und die Prüfung |
|---|---|
| Kopf, Karte, Mission, Startzeit, Sitzung; Ergebnisse | jede Datei |
| Missionseinstellungen (der blk nach dem Kopf) | Modus, Wetter, Grenzen, `stars` (Datum, Uhrzeit, Ort) |
| Paketstrom (zlib in 2025, zstd in 2026) | jedes Paket eingerahmt |
| Positionen und Lage der Flugzeuge (Layout 2026) | 4 Messwerte pro Sekunde, kein Paket ungelesen; der Kurs stimmt mit der Flugrichtung überein |
| Flugpakete vor ihrer Zeit | nach einem Netzwerkhänger enthält das Flugpaket eines Client-Replays manchmal alle anderen Flugzeuge dort, wo sie etwa 0,75 s später sein werden. Der Vorlauf wird je Paket gemessen, und jedes Flugzeug, das vorausläuft, bekommt die Zeit, für die es steht (`selfCheck.flightPacketsRetimed`) |
| Sprünge der Totrechnung | ein Schritt aus einem totgerechneten Lauf wird von dem letzten empfangenen Zustand aus gemessen, sodass die Korrekturen des Clients die Spuren nicht mehr zerschneiden ([Totrechnung](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportationen | eine Spur wird an der Stelle getrennt, an der sich ihre Einheit weiter bewegt, als sie kann: zuerst nach ihrer Art (Flugzeug 750 m/s, Boden und Schiffe 40 m/s, Waffen 1800 m/s), dann nach ihrem eigenen Tempo. Jede Trennung steht in `trackBreaks` mit ihrer wahrscheinlichen Ursache (Wiedereinstieg, das Spiel bewegt den Spieler, eine Korrektur einer entfernten Einheit). Nach den Trennungen ist kein Schritt zwischen Zeilen einer Spur schneller, als ihre Art erlaubt (`selfCheck.stepSpeed`) |
| Positionen von Boden und Schiffen (0xF073 / 0xF074) | kein Paket ungelesen. Kurs, Nicken und Rollen aus der Lage mit 16 Bit: der Kurs stimmt mit der Flugrichtung auf etwa 2 Grad überein (Median); das Nicken zählt 180/65536 Grad pro Schritt; mit umgedrehtem Vorzeichen des Rollens zeigt die Richtung des Geschützes von Wanne und Turm bei fast jedem Panzerschuss auf die getroffene Einheit. Schiffe liegen auf Wasserhöhe |
| Türme | Gierwinkel des Turms und Höhenwinkel des Geschützes der Panzer: siehe [Geschütztürme](ground.md#turrets) |
| Gepackte Bodenhöhen | Positionen, die in 64 Bit gepackt sind, zählen ihre Höhe auf den meisten Leveln ab -100 m, auf manchen ab der Wasserhöhe; der Versatz wird in jedem Replay an Einheiten gemessen, die in beiden Formen gesehen wurden (`selfCheck.packedGroundHeight`) |
| Entitätsstrom (Entstehen, Vergehen) | jedes Entstehen gelesen. Das Layout stammt aus dem veröffentlichten Quellcode der Dagor Engine; die eigenen Komponententypen von War Thunder werden übersprungen, indem man findet, wo die nächste Komponente beginnt. Das Fahrzeug und der Spielerplatz jeder Einheit entsprechen denen, die die Abschuss- und Trefferdatensätze nennen, bei jedem geprüften Datensatz |
| Wer welche Einheit fuhr, KI-Einheiten, Schiffe, Bodenziele | aus dem Entitätsstrom: jede Einheit hat ihr Fahrzeug und Team, die Einheit jedes Spielers gehört ihm |
| Abschüsse gegen die Ergebnisse | die Tode je Spieler sind gleich denen der Ergebnisse; die Ergebnisse zählen mehr Abschüsse, weil dem Client nicht jeder Abschuss gesendet wird. Ein Replay, das nach Beginn des Gefechts startet, enthält nur die Abschüsse ab dann |
| Abschüsse, kritische Treffer, schwerer Schaden | jede Datei |
| Zerstörte Module (0xF118) | die Einheit und die Nummer des Teils; der Name des Teils braucht das Schadensmodell des Fahrzeugs, das nicht im Replay steht |
| Abgeworfene Waffen (Entitätsstrom) | der Abwurfpunkt liegt etwa 10-20 m (Median) von der nächsten Einheit entfernt, die als Abschussrampe gilt |
| Waffen im Flug (0xF0DB) | Lenkwaffen, Raketen und Bomben, jede an ihre Entität gebunden |
| Bomben ohne Flugdatensätze | eine Bombe ohne sie bekommt ihren Fall aus Abwurf und Aufprall berechnet (Schwerkraft und Luftwiderstand, eine Messung alle 0,1 s, `extrapolated` true). Geprüft über dem Meer, wo die Aufprallhöhe bekannt ist: Die berechneten Fälle enden innerhalb von etwa 15 m über dem Wasser. Im Match-Dokument hat so eine Waffe `ballisticImpact`; `counts.bombsBallistic` zählt sie |
| Spielerplätze, Chat | jede Datei |
| Explosionen, Flak-Detonationen, Auszeichnungen, Entdeckungen, Wetter, Missionsobjekte | gelesen; die Positionen mit dem Auge im Viewer geprüft |
| Die Instrumente des aufnehmenden Spielers (0xD04A) | nach ihrer Funktion benannt: [Cockpit-Instrumente](aircraft.md#cockpit-instruments); der Rest unter `notNamed` |
| Weitere Felder der Flugeinträge | Geschwindigkeit, Munition, Steuerung, Triebwerke: [Flugeinträge](aircraft.md#flight-entries) |
| Lage in den Ereigniszeilen | jede Ereigniszeile trägt Kurs, Nicken, Rollen und Blickvektor ihrer Einheit zu diesem Zeitpunkt |
| Spielerstatistik und Teampunkte | am Ende des Gefechts ist jede Statistik für jeden Spieler gleich der der Ergebnisse: [Spiegelungsdaten](aircraft.md#reflection-data) |
| Namen von Waffen und Fahrzeugen | aus der englischen Lokalisierung deiner Installation; einige Standardgurte von Schiffen und Flugplatz-Radare haben im Spiel keinen Namen |
| Spieler und KI | keine Zeile eines Ergebnis-Spielers ist KI, jede Zeile, die keine KI ist, gehört einem Ergebnis-Spieler (`selfCheck.identity`) |
| Wracks | die Messwerte einer Einheit nach ihrem Tod kommen weiter; das Wrack einer Bodeneinheit oder eines Schiffs ist `alive` 0, bis seine Entität entfernt wird, und bleibt eine Spur; Flugzeuge behalten `alive` 0 höchstens 60 s (`selfCheck.wrecks`) |
| Fahrzeugwechsel | eine Einheit des Spielers, die noch lebt, wenn die nächste Einheit desselben Spielers erscheint, endet dort (ein zurückgelassenes Fahrzeug). `selfCheck.vehicleSwitch.twoLiveVehicles` muss 0 sein |
| Spielmodus | [Gefechtsmodus](ground.md#battle-mode) |
| Flugzeuge in einem Server-Replay von 2026 | im Layout von 2026 gelesen; Kurs und Vorzeichen des Rollens stimmen mit den Kurven überein; Platzhalter-Flugzeuge und Aufklärungsdrohnen tragen keine Daten |
| Spieler eines Server-Replays | über den Namen in den Plätzen gefunden; jede Statistik ist gleich der der Ergebnisse (`selfCheck.players`) |
| Flugzeuge in Server-Replays von 2025 und Version 101286 | nicht gelesen: ihre Flugpakete haben ein anderes Layout |

## Nachrichten an Einheiten {#messages-to-units}

Jedes Paket vom Typ 4 ist eine mpi-Nachricht von daNet der Dagor Engine: die
Kennung des Empfängerobjekts, dann (wenn seine unteren 11 Bit alle gesetzt sind)
die externe UID des Objekts, die Nachrichten-ID und die Nutzdaten. Eine
Nachricht an eine Einheit trägt als externe UID die Entitäts-ID der Einheit,
`index << 10 | generation`. Geprüft: Jede solche Nachricht nennt eine
Entität, die in diesem Moment lebt.

Für Fachleute: Die gelesenen Nachrichten sind:

| Nachricht | Was, und die Prüfung |
|---|---|
| 0xF0E9 UnitHitEffects | der Treffer eines Geschosses: die uid des Schützen und der Trefferpunkt im Koordinatensystem der Einheit (x vorwärts, y oben, z links): Zentimeter bei Flugzeugen und Schiffen, 20/32768 m pro Schritt bei Bodeneinheiten (angepasst an die Größe der Panzertürme). `hitLocalX/Y/Z` in Metern. Wird zu einer Zeile `shot` ([Beschuss](hits.md#gunfire)). Der Angreifer fast jedes Treffer- und Abschussdatensatzes steht unter diesen Schützen; die Trefferpunkte liegen auf der Seite, die dem Schützen zugewandt ist |
| 0xF133 UnitOnExplosion | dieselbe uid des Schützen |
| 0xF04B OnUnitDead | Zeilen `dead`: jedes Opfer eines Abschussdatensatzes hat eine innerhalb von 2 s |
| 0xD047 FmwRpm | die Drehzahl der Triebwerke (`rpm`); stimmt mit dem Drehzahlmesser des Cockpits überein |
| 0xF0B1, 0xF0A0 | Zeilen `gun_shot`: einzelne Schüsse der schweren Flugabwehr und der Artillerie |
| 0xF01B, 0xF01C | Zeilen `fire_start`, `fire_stop`: Feuerstöße der 40-mm-Flak (ein feuerndes Geschütz; ein Brand an einem Fahrzeug ist `fire_on`, siehe [Brände am Fahrzeug](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | Zeilen `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | die eigenen Treffer des aufnehmenden Spielers und die Treffer, die er erhält, mit Waffe und Munition, aus der Installation benannt (`projectileHitReplays`) |
| 0xF13E, 0xF031 | die optische Wirkung eines Treffers und ein Effekt auf der Einheit; sie kommen mit einem Treffer auf dieselbe Einheit |
| 0xD041 | eines je Abwehrgeschütz eines Flugzeugs, zweimal pro Sekunde; seine Indizes passen zu den Schützenwaffen des Flugmodells |
| 0xD048, 0xF117 | Layout gelesen, Bedeutung nicht bekannt |
| der Rest (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | in der Nachrichten-Sidecar mit ihrer Einheit und ihren Feldern |

Die Namen stammen aus der Community (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Außerdem gelesen {#also-read}

- **Replikation des Entitätsstroms** (0x22, 0x23): je Entität ein Block von
  Komponentenwerten: Reparaturtimer von Schiffen, Anzahl der Verbrauchsgüter,
  Wechsel von Besitzer und Team, Überhitzung des Triebwerks. Gezählt in
  `counts.replicatedComponents`; die Werte in der Nachrichten-Sidecar.
- **Aktionen des Missionsskripts** (0xF028) und **Hinweise** (0xF0EC): `triggers`,
  `hints`. **Missionsfortschritt** (0xF07A, 0xF07C): `missionProgress`.
- **Die Replay-Kamera** (0xD043): siehe [Die Kamera](ground.md#the-camera).

## Nicht gelesen, und warum {#not-read-and-why}

- **Namen und Inhalte der Entitätsnachrichten** (0x20, 0x21): Die Klassennummer
  ist ein Platz in einer Liste, die im Spiel einkompiliert ist; sie wird nicht
  gesendet und steht nicht in seinen Daten. Zwei werden gelesen (die Brände eines
  Fahrzeugs und seine Feuerlöscher); der Rest wird vollständig mit seiner
  Entität und Klassennummer aufbewahrt.
- **Andere replizierte Objekte** (andere Arten als Spielerplätze und Teams):
  gelesen und aufbewahrt, nicht benannt; im Ergebnis gibt es nichts, womit man
  sie prüfen könnte.
- **Steuerung, Schub und Munition anderer Flugzeuge**: werden nur ab und zu
  aufgefrischt; sie stehen in der Flug-Sidecar, nicht in der Tabelle.
- **Brände an Flugzeugen**: in keiner Nachricht gefunden; ein brennendes
  Flugzeug hat keine Zeile `fire_on`.
- **Namen abgeworfener Waffen**: die Entität einer Bombe oder Rakete trägt keinen
  Namen; Abschussdatensätze nennen die Waffe eines Abschusses.
- **Schüsse, die danebengingen**: ein Replay enthält nur die Treffer.

`counts.messageIdsNotRead` und `selfCheck` im Match-Dokument jedes Gefechts sagen,
was ein neues Replay enthält und wie gut es gelesen wurde.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
