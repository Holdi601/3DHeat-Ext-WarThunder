---
title: Flugzeuge
nav_order: 11
lang: de
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Flugzeuge {#aircraft}

Für Leser, die wissen wollen, woher die Flugzeug-Spalten kommen und wie weit
man ihnen trauen kann. Jede Prüfung unten vergleicht einen Wert mit etwas, das
das Replay auf eine zweite, unabhängige Weise sagt. Angegeben werden nur die
Methode und die Übereinstimmung.

## Cockpit-Instrumente {#cockpit-instruments}

Nachricht 0xD04A sendet die Anzeigen des Spieler-Cockpits als Paare (Nummer,
Wert): vier pro Sekunde in Arcade-Gefechten, nur geänderte Werte in
Simulator-Gefechten. Die Nummern bilden eine einzige Liste über alle Cockpits,
und ein Cockpit sendet die Anzeigen, die sein Modell hat. Der Spielcode legt
fest, welche Nummer welche Anzeige ist. Deshalb wurde jede Nummer nach ihrer
Funktion benannt und am Replay geprüft (`convert.INSTRUMENTS` enthält das
Ergebnis; nichts wird aus der Installation gelesen):

| Nummer | Name | Geprüft gegen |
|---|---|---|
| 0 | angezeigte Fluggeschwindigkeit, m/s | die um die Luftdichte korrigierte Geschwindigkeit der Spur: Korrelation 0,99 |
| 39 | Steigrate, m/s | die Steigrate der Spur: Korrelation über 0,99 |
| 40, 41 | Höhe, m; Höhe modulo 1000 | die Höhe der Spur, wenige Meter Abweichung |
| 52, 53 | Rollen und Nicken des künstlichen Horizonts | minus Rollen und Nicken der Tabelle, unter 1 Grad Abweichung |
| 64 | Kompass | der Kurs der Tabelle, unter 0,1 Grad Abweichung |
| 15-20 | Seitenruder-Pedale | die Seitenkraft am Flugzeug |
| 23, 31 | Steuerknüppel: Höhenruder und Querruder (Vorzeichen wie beim Cockpit-Modell) | der Anstellwinkel; die Rollrate |
| 69, 71, 73 | Uhr: Stunden (12-Stunden-Zifferblatt), Minuten, Sekunden | die Ortszeit des aufnehmenden Rechners, auf die Minute genau |
| 75 | Ladedruck, atm | höher bei Kriegs-Notleistung als bei Vollgas |
| 81-86, 87-92, 93-98 | Drehzahl je Motor, Drehzahl modulo 1000, Drehzahlmesser | einander genau; die Motordrehzahl: Korrelation über 0,97 |
| 195 | Treibstoff | sinkt während eines Einsatzes, nach einem Wiedereinstieg wieder voll |
| 228-230 | Fahrwerksbeine, 1 = ausgefahren | nur nahe der Höhe der Flugplätze und bei Landegeschwindigkeit ausgefahren |
| 240, 241 | Schub je Motor (1,1 bei Kriegs-Notleistung oder Nachbrenner) | der Schub aus dem Flugeintrag |
| 330-332, 346-348 | Munitionszähler (zwei gleiche Sätze) | die Munition der Waffenvorgabe, sinkend mit der Munition des Flugeintrags |
| 135, 159 | Öl- und Zylinderkopftemperatur | wahrscheinlich: sie steigen während eines Einsatzes |
| 58, 61 | Wendekugel, Wendezeiger | wahrscheinlich: sie folgen der Seitenkraft und der Drehrate |
| 223 | Luftbremse | wahrscheinlich: nur im Anflug gesetzt |
| 490-497, 500-505 | Radbremsen | wahrscheinlich: nur gesetzt, wenn man auf einem Flugplatz steht |

Einige weitere Nummern werden gesendet, deren Bedeutung nicht bekannt ist.
Sie werden in `authorInstruments.notNamed` im Match-Dokument aufbewahrt.

Die Felder `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` und `throttle` der Tabelle stammen aus
diesen Werten, aus den eigenen Zeilen des aufnehmenden Spielers. Genommen wird
die letzte Nachricht, höchstens 0,2 s nach dem Messwert.

## Flugeinträge {#flight-entries}

Der Flugeintrag jedes Flugzeugs (Pakettyp 2) enthält neben Position und
Lage auch:

- **Geschwindigkeit**: ein 32-Bit-Wort nach der Lage. Die Bits 31, 30 und 29
  sind die Vorzeichen von x, y und z. Danach folgt die Geschwindigkeit in
  11 Bit mit 500/2047 m/s (bei 500 m/s hört sie auf), dann |x| und |y| als
  Bruchteile der Geschwindigkeit mit je 9 Bit. z macht den Vektor zu einem
  Einheitsvektor. Geprüft am Schritt zwischen empfangenen Messwerten: Die
  Richtung stimmt für den aufnehmenden Spieler auf einen Bruchteil eines
  Grades genau überein und für alle anderen auf etwa 2 Grad; die
  Geschwindigkeit auf 0,2 %. `selfCheck.flightEntries`.
- **Munition je Waffe**: eine Liste vor der Position, ein Eintrag je Waffe,
  zuerst die verbleibenden Schuss. Bei dem aufnehmenden Spieler entspricht sie
  bei fast jeder Messung den Zählern des Cockpits einen Takt später.
- **Steuerung und Schub**: 7 Bytes nach der Geschwindigkeit, gelesen als
  14 Halbbytes. Beim aufnehmenden Spieler bei jedem Takt: 1 das Höhenruder,
  2 die Querruder, 3 das Seitenruder (8 in Ruhe), 11 der Schub in Fünfzehnteln
  (15 auch bei Kriegs-Notleistung und Nachbrenner), 4 die Radbremsen, 5 die
  Luftbremse, 8 wahrscheinlich der Bremsschirm. Die Halbbytes anderer
  Flugzeuge ändern sich nur wenige Male pro Gefecht und sind nicht deren
  Steuerung zu dem Zeitpunkt.
- **Triebwerke**: je Triebwerk ein Zustandsbyte (0 aus; 1-6 startet; 7 läuft;
  8 tot), ein 16-Bit-Wert nur bei Nachbrenner (32767 voll) und ein Byte nur,
  nachdem das Triebwerk getroffen wurde. Die meisten Flugzeuge, deren
  Triebwerk "tot" wird, werden abgeschossen oder enden innerhalb von Minuten.

## Spiegelungsdaten {#reflection-data}

Die Nachrichten 0xF02D und 0xF0AA spiegeln die nummerierten Objekte des
Spiels: je Objekt seine Kennung (die oberen 5 Bit die Art, die unteren 11 Bit
ein Index) und eine Feldtabelle. Art 14 sind die Spielerplätze (Feld 2
Benutzer-ID und Name, Feld 9 das Team), Art 15 die Teams (Index 1 und 2):

- Das Feld 39 eines Platzes enthält seine Statistik an festen Stellen: Abschüsse
  (Versatz 0), Team-Abschüsse (2), Tode (4), Marine-Abschüsse (10),
  KI-Abschüsse (12), KI-Bodenabschüsse (14), Assists (20), Eroberungszonen
  (22), Zonenschaden (24, 32 Bit), Schadensbelohnung (40, 32 Bit),
  Raketenausweichen (50). Feld 38 beginnt mit der Punktzahl, Feld 42 ist die
  Staffel. Am Ende eines Gefechts ist jeder Wert für jeden Spieler gleich dem
  der Ergebnisse (`selfCheck.scoreboardVsResults`). Wo die Bodenabschüsse
  gespeichert werden, ist nicht bekannt.
- Das Feld 7 eines Teams ist seine Punktzahl: am Ende ist es gleich der Summe
  der Punkte seiner Spieler in den Ergebnissen. Feld 3 sind wahrscheinlich
  seine Tickets.
- Jede Nachricht sendet nur die Felder, die sich geändert haben. Deshalb listet
  `scoreboard` im Match-Dokument die Statistik jedes Spielers und die
  Punktzahl jedes Teams bei jeder Änderung.

## Totrechnung und Glätter {#dead-reckoning-and-the-smoother}

Ein Client-Replay zeichnet jedes Flugzeug viermal pro Sekunde auf, so wie der
Client es gezeichnet hat. Zwischen den Aktualisierungen, die er für ein
entferntes Flugzeug empfängt, bewegt der Client es mit seiner letzten
Geschwindigkeit weiter und dreht es mit seinen letzten Raten, und bei der
nächsten Aktualisierung springt er es dorthin. So gelesen verläuft eine Spur
gerade und springt dann. Im Flugeintrag steht nichts darüber, welche Messwerte
empfangen wurden. Ein totgerechneter Messwert wird an seiner Beschaffenheit
erkannt: Er setzt die gerade Linie der zwei vorangegangenen Messwerte fort, im
selben Tempo, auf 3 cm genau.

Wie sehr das ins Gewicht fällt, hängt vom Gefecht ab: In Arcade-Gefechten
kann etwa die Hälfte der Messwerte anderer Flugzeuge totgerechnet sein, in
Simulator-Gefechten nur wenige Prozent. Der Glätter reduziert die Sprünge über
15 g auf etwa ein Fünftel (`selfCheck.deadReckoning`). Das eigene Flugzeug des
aufnehmenden Spielers wird vom Client nicht extrapoliert und bleibt daher, wie
es ist.

Standardmäßig (`--no-smoothing` schaltet das aus) werden die Spuren aller Einheiten
außer der eigenen des aufnehmenden Spielers dorthin gesetzt, wo die empfangenen
Zustände sie laut Replay hatten: Ein totgerechneter Messwert liegt auf einer
Kurve durch die empfangenen Messwerte davor und danach, jeder mit seiner
eigenen Geschwindigkeit. Über mehr als 3 s wird die gerade Linie nur zum
nächsten empfangenen Messwert hin gebogen, sodass kein Messwert weiter
springt als der eigene Sprung des Clients. Seine Lage wird gleichmäßig von
einer empfangenen Lage zur nächsten gedreht. Empfangene Messwerte werden um
höchstens 2 m oder 0,04 s ihrer Geschwindigkeit geglättet; eine gleichmäßige
Kurve bleibt, wie sie ist. Die eigenen Werte des Replays bleiben in den
`Raw`-Spalten erhalten.

## Lage, geprüft {#attitude-checked}

Beim eigenen Flugzeug des aufnehmenden Spielers liegt der Kurs (Median) innerhalb
eines Grades der Flugrichtung, das Nicken innerhalb weniger Grad des Steigwinkels,
und in klaren Kurven hat das Rollen für fast jeden Messwert das Vorzeichen der
Kurve: Das Rollen des Flugmodells ist linke Fläche unten positiv, und die Tabelle
dreht es auf rechte Fläche unten positiv (`selfCheck.aircraftAttitude`). Die
10-Bit-Winkel schreiten in 0,18 Grad fort. Die Lage der Bodeneinheiten wird an
ihren Schüssen geprüft ([Geschütztürme](ground.md#turrets)).

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
