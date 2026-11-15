---
title: Bodeneinheiten und Kamera
nav_order: 12
lang: de
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Bodeneinheiten und Kamera {#ground-units-and-camera}

Für Leser, die wissen wollen, woher die Spalten für Geschütztürme, Kamera und Gefechtsmodus
kommen und wie weit man ihnen trauen kann. Prüfungen geben nur die Methode und die
Übereinstimmung an.

## Geschütztürme {#turrets}

Der Bodenzustand eines Panzers (Lage mit 16 Bit) enthält nach seiner Position 141 Bit,
die nicht gelesen werden, dann je Turm 62 Bit: der Gierwinkel des Turms und der Höhenwinkel
des Geschützes (je 16 Bit, 360/65536 Grad pro Schritt, mit Vorzeichen) und 30 Bit, die nicht
gelesen werden; danach Füllbits und bei manchen Zuständen 200 weitere Bit. Die Anzahl der
Türme ist das Byte, das vor dem Zustand gesendet wird. Ein Zustand, dessen Länge nicht passt,
ergibt keine Türme (statische Einheiten senden einen kürzeren Zustand). Der Gierwinkel ist relativ
zur Wanne, im Uhrzeigersinn positiv, 0 geradeaus; der Höhenwinkel relativ zur Wanne, nach oben positiv.

So wurde geprüft:

- **Gegen die Schüsse:** für jeden Treffer eines Panzers wird die Weltrichtung seines
  Hauptgeschützes (Wannenlage, gedreht um den Gierwinkel des Turms und den Höhenwinkel des
  Geschützes) mit der Linie vom Schützen zur getroffenen Einheit verglichen, mindestens 30 m
  entfernt. Je Gefecht liegt der Median bei etwa 98 % innerhalb von 3 Grad im Kurs und 99 %
  in der Höhe (`selfCheck.turretsVsShots`). Die übrigen sind meist Treffer eines
  Maschinengewehrs aus einem anderen Turm.
- **Gegen das Zielen des aufnehmenden Spielers:** Sein eigener Panzer sendet den Weltwinkel
  seines Zielens (gegen den Uhrzeigersinn von Osten), Höhe und Entfernung. Der Kurs der Wanne
  plus der Gierwinkel des Turms liegt im Median innerhalb eines halben Grades des Zielens.

**Server-Replays** (0xF074) senden den Zustand jedes Panzers im selben Aufbau, gefolgt von
eigenen Daten. Deshalb wird jeder Turm gelesen, dessen zwei Winkel innerhalb des Zustands
liegen (bei fast jeder Panzer-Zeile mindestens der Hauptturm). Gemeint ist der Turm, nicht die Kamera:

- **Gegen die Schüsse**, wie oben: je Gefecht über 90 % innerhalb von 3 Grad im Kurs und 99 % in der Höhe.
- **Gegen die Sicht:** Ein Server-Replay sendet das Zielen jedes Spielers (`viewYaw`,
  `viewPitch`). Der Turm folgt der Sicht innerhalb eines halben Grades (Median), dreht sich
  aber weit langsamer, als die Sicht schwenkt, wie es ein Turmantrieb tut (`selfCheck.turretVsView`).
- **Aber nicht immer mit der Geschwindigkeit eines Antriebs:** Messwert für Messwert springt
  der gesendete Wert manchmal auf das Zielen, wenn das Zielen nahe am Geschütz liegt, schneller,
  als irgendein Antrieb dreht.

Die Tabelle hält den Turm deshalb **an seinen Antrieb gebunden**: `turretYaw` / `gunPitch`
bewegen sich auf den gesendeten Wert zu, höchstens mit der Drehgeschwindigkeit des Hauptgeschützes
aus der Fahrzeugdatei der Installation (mal 1,3 für Besatzungsfähigkeiten und Modifikationen;
45 und 20 Grad pro Sekunde, wo die Installation keine nennt). Bei jedem Treffer des Hauptgeschützes
wird der Turm genau auf die Linie des Schusses gesetzt, und ein Rücklauf bringt ihn rechtzeitig
dorthin (`selfCheck.turretLimit`). Die Zeile `shot` trägt ebenfalls `turretYaw` / `gunPitch`.
Der gesendete Wert bleibt in `turretYawRaw` / `gunPitchRaw`. Ein Panzer, dessen Zustand keinen
Turm enthält, hat leere Turmspalten (der Viewer kann auf `viewYaw` zurückfallen).
`gunPitch` liegt auf weite Entfernung etwas über `viewPitch`: die Höhe des Geschützes für den
Fall des Geschosses.

Die Zustände der Schiffe haben einen anderen Aufbau; ihre Türme werden nicht gelesen. Flugzeuge
senden keine Kopf- oder Sichtrichtung; die Nachricht 0xD020 der Flugabwehr bleibt ungelesen.

## Die Kamera {#the-camera}

Nachricht 0xD043, etwa 20 pro Sekunde, ist die eigene Replay-Kamera des aufnehmenden Spielers:
Feld 1 ist ein Quaternion, das die Vorwärtsrichtung der Kamera dorthin dreht, wohin sie schaut;
2 der Ort der Kamera relativ zum verfolgten Fahrzeug (m); 4 derselbe Versatz im eigenen
Koordinatensystem des Fahrzeugs (x vorwärts, y oben, z links); 5 wohin der Spieler zielt
(ein Einheitsvektor); 3 der Zoom (etwa 1,2 in der Verfolgeransicht eines Panzers, etwa 1,0 im
Flugzeug, höher im Zielfernrohr des Richtschützen oder durch ein Fernglas). Geprüft: Feld 4 ist
Feld 2 in das Koordinatensystem des Fahrzeugs gedreht, auf 0,5 m genau bei fast jeder Nachricht;
die Vorwärtsrichtung der Kamera hat den Kurs des Zielens. Das Replay sendet kein Blickfeld in
Grad, nur den Zoom.

Die Tabelle führt die Kamera als eigene Spur: Art `camera`, Spur `<player> camera #ca`, eine
Zeile höchstens alle 0,1 s, am Ort des verfolgten Fahrzeugs plus Feld 2, mit Blick entlang des
Quaternions (`dirX/Y/Z`, `heading`, `pitch`, `roll`), mit `zoom`, `aimHeading` und `aimPitch`,
und `otherLife` ist das Leben, dem sie folgt. `selfCheck.camera` zählt die Zeilen und die Prüfung.

## Ende einer Spur {#end-of-a-track}

Eine Spur wird von ihrer ersten bis zu ihrer letzten Zeile gezeichnet. Ist ihre Einheit vor dem
Ende des Replays verschwunden, ist ihre letzte Zeile eine Zeile `despawn` an ihrem letzten Ort:
zu dem Zeitpunkt, an dem das Spiel ihre Entität entfernt hat (wenn das innerhalb von 6 s nach
ihrem letzten Messwert lag), sonst an ihrem letzten Messwert. Eine Spur ohne so eine Zeile reicht
bis zum Ende des Replays. Zeilen einer Spur können weit auseinanderliegen (eine entfernte Einheit
oder ein Wrack wird alle paar Sekunden aufgefrischt, ein Wrack manchmal minutenlang nicht): Ihr
letzter Zustand gilt bis zur nächsten Zeile.

## Gefechtsmodus {#battle-mode}

Das Byte bei Versatz 688 des Kopfes enthält den Schwierigkeitsgrad in seinen unteren vier Bit:
0 Arcade (AB), 5 realistisch (RB), 10 Simulator (SB). Geprüft an den Gefechtsarten, von denen
bekannt war, dass die Replays sie enthielten. Der Spielmodus ist `ground`, wenn die Mission
das Erscheinen von Panzern erlaubt, sonst `naval`, wenn sie Schiffe erlaubt, sonst `air`
(`allowedUnitTypes`). Der eigene Modus der Mission kommt aus ihrem Schlüssel (`missions/_Dom`),
benannt nach der `lang/missions_versus.csv` deiner Installation. Derselbe Schlüssel ist der
Teil `<mode>` der Dateinamen und der Match-Kennung (`Conq4`, `Dom`); er fehlt, wo der Kopf
keinen hat.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
