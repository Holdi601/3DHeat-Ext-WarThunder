---
title: Treffer, Feuer und Brände
nav_order: 13
lang: de
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Treffer, Feuer und Brände {#hits-gunfire-and-fires}

Für Leser, die wissen wollen, woher die Spalten für Treffer, Munition und Brände
kommen. Prüfungen geben nur die Methode und die Übereinstimmung an.

## Beschuss {#gunfire}

Jedes Geschoss, das eine Einheit getroffen hat, steht im Replay (Nachricht 0xF0E9): eine
Zeile `shot` an der Position des Schützen im Moment des Treffers, `targetX/Y/Z` der Trefferpunkt
(die getroffene Einheit, um den Trefferpunkt in ihrem Koordinatensystem verschoben und mit
ihrer Lage gedreht), die Richtung darauf hin, `other` die getroffene Einheit. Granaten und
Kugeln, die danebengingen, werden nicht gesendet: Sie sind keine Entitäten, und die Nachrichten
über Waffen im Flug enthalten nur Raketen, Lenkwaffen, Bomben und Torpedos. Die verbleibenden
Schüsse des aufnehmenden Spielers (seine Spalte `ammo`) sinken beim Feuern, so lassen sich seine
Feuerstöße erkennen, aber nicht, wohin diese Schüsse gingen. Schwere Flugabwehr und Artillerie
senden jeden einzelnen Schuss (`gun_shot`, ohne Richtung), die 40-mm-Flak ihre Feuerstöße
(`fire_start`, `fire_stop`).

## Trefferergebnisse {#hit-outcomes}

Bei jedem Geschosstreffer auf eine Bodeneinheit sendet der Server die Nachricht 0xF144
(UnitOnHit) an die Einheit: vier Felder zu je einem Byte, das vierte sind die Bit dessen, was
der Treffer bewirkt hat (`selfCheck.unitMessages.outcome_*`):

| Bit | Bedeutung | Belege |
|---|---|---|
| 0x20 | der eigene Treffer eines Geschosses | fast alle kommen mit einem Treffer 0xF0E9 auf die Einheit innerhalb von 5 ms; ohne ihn mit einer Explosion (Splitter) |
| 0x01 | er ist durchgedrungen (Durchschlag) | jede Nachricht mit 0x02, 0x04 oder 0x08 hat es auch |
| 0x02 | kritischer Treffer | die meisten Datensätze kritischer Treffer haben es, weit öfter als der Zufall erwarten lässt |
| 0x04 | zerstört | die meisten kommen mit einem Abschuss-Datensatz und dem Tod der Einheit innerhalb einer Sekunde |
| 0x08 | schwerer Schaden | manche Datensätze kritischer Treffer haben es; sonst selten |

`hitOutcome` nimmt das Schlimmste: `kill` (0x04), `critical` (0x02 oder 0x08),
`penetration` (0x01), `nonpenetration` (0x20 allein). Ein Treffer wird mit der nächsten
ungepaarten 0xF144 mit 0x20 auf seine Einheit innerhalb von 5 ms gepaart. Die Trefferkamera des
Spiels unterscheidet einen Abpraller von einem Nicht-Durchschlag, aber kein hier gefundenes Bit
oder Feld tut das: Die ersten drei Bytes ändern sich von Treffer zu Treffer, und ihre Bedeutung
ist nicht bekannt. Client-Replays senden 0xF144 nur für das eigene Flugzeug des aufnehmenden
Spielers, alle Bit gelöscht: Flugzeug- und Schiffstreffer haben kein Ergebnis.

## Munition {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Sprengend oder nicht.** Eine Granate, die detoniert, sendet 0xF133 (UnitOnExplosion) mit
  der uid des Schützen und der Nummer des Treffers; ein Treffer mit einer solchen Nachricht ist
  `explosive`, die übrigen `kinetic`.
* **Das Geschütz und sein Platz.** 0xF0BD (UnitBulletRearm) ist die nächste geladene Granate:
  der Index der Waffe in der Waffenliste des Fahrzeugs, der Munitionsplatz und die verbleibenden
  Schüsse. Die Nachladung eines Richtschützen erfolgt eine gleichbleibende Ladezeit nach jedem seiner
  Treffer, die eines Schnellfeuergeschützes einen Bruchteil einer Sekunde danach. Die Treffer eines
  Schützen werden nach Fahrzeug, Signatur und Feuerstoß gruppiert; eine Gruppe gehört zu einer
  Waffe, wenn diese Waffe innerhalb von 20 s nach der Hälfte oder mehr ihrer Treffer mit gleichbleibender
  Verzögerung eine Granate lädt. `ammoSlot` ist `Waffe/Platz`, der Platz, der vor dem Treffer
  geladen war: wahrscheinlich der abgefeuerte, außer der Spieler hat die Munition dazwischen
  gewechselt. Maschinengewehre senden keine 0xF0BD.
* **Das Geschoss.** Die Waffe eines Abschusses ist die Kennung des Geschosses (`125mm_3bm46`);
  der letzte Treffer des Killers auf das Opfer ordnet sie dem Platz dieses Schützen zu,
  wo das Kaliber des Geschützes passt. Art und Kaliber stammen aus der Waffendatei
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Das Kaliber** des Übrigen: das der Waffe eines Platzes; bei einer Gruppe von Maschinengewehren
  das eine Maschinengewehr-Kaliber, das ihre Signatur haben kann; sonst das des Hauptgeschützes des
  Fahrzeugs. Ohne die Installation (`--game`) gibt es über `explosive` / `kinetic` hinaus keine Art,
  keinen Namen und kein Kaliber.

Nicht gefunden: der Abpraller. Mehrere weitere Nachrichten tragen den Schützen und die Nummer des
Treffers (0xF0C2, wahrscheinlich der Weg der Trefferkamera durch das Fahrzeug; 0xF117, 0xF13C,
0xF13E); sie werden im Sidecar aufbewahrt, nicht entschlüsselt. Ein Nicht-Durchschlag bleibt
`nonpenetration`.

## Brände am Fahrzeug {#vehicle-fires}

Ein brennendes Fahrzeug wird jedem Client angezeigt: Der Server sendet eine Entitätsnachricht an
das Fahrzeug (Ereignis `0a519c58`), die die Brände auflistet, die auf ihm brennen, jedes Mal,
wenn sich die Liste ändert. Je Brand: zwei 16-Bit-Kennungen (die zweite ein Knoten des
Schadensmodells), seine Art und -1, solange der Brand nicht gegriffen hat. Ein Brand, der durch
einen Treffer entfacht wurde, bekommt außerdem eine Nachricht mit dem Punkt, an dem er brennt,
im Koordinatensystem des Fahrzeugs (x vorwärts, y oben, z links).

Zeilen: `fire_on`, wenn ein Brand in der Liste erscheint, `fire_off`, wenn er verschwunden ist,
am Fahrzeug, mit `fireId` (`erster:Knoten`), `fireKind` und bei Bränden, die ein Treffer entfacht
hat, `fireLocalX/Y/Z` (vorwärts, oben, rechts). Ist ein Fahrzeug tot, wird seine Liste oft nicht
mehr gesendet: Seine Brände enden mit seinem Wrack, sonst mit seiner Entität, sonst mit dem
Replay (`selfCheck.fires`).

Geprüft: Jedes Mal, wenn die Zahl der Feuerlöscher eines Panzers sank, verschwand innerhalb eines
Bruchteils einer Sekunde ein Brand aus seiner Liste; die meisten Brandpunkte liegen auf derselben
Seite des Fahrzeugs wie der Treffer, der sie entfacht hat. Die Arten sind Zahlen; was sie
bezeichnen, ist nicht bekannt, ebenso wenig, welcher Teil zu einem Knoten gehört. Flugzeuge senden
keine solche Liste: Ein brennendes Flugzeug wird nicht gelesen.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
