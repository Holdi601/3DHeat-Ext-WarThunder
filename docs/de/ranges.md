---
title: Reichweitenkatalog
nav_order: 10
lang: "de"
source: ranges.md
source_hash: "2a50d5a33e69"
nav_exclude: true
search_exclude: true
---
# Reichweitenkatalog (heat3d-wt-ranges) {#ranges-catalogue-heat3d-wt-ranges}

`heat3d-wt-ranges` baut einen Katalog aus deiner eigenen Installation: wie weit
jede Waffe reicht, was jedes Fahrzeug trägt, seine Visiere und seine Sensoren.
Der 3DHeat-Viewer nutzt ihn für die Einsatzreichweiten, Sichtkegel und
Sensorsektoren eines War-Thunder-Gefechts, anstelle seiner allgemeinen Werte.
Die Datei bleibt auf deinem Rechner.

## Schritt für Schritt {#step-by-step}

1. Installiere den Konverter (siehe [Installation](installing.md)).
2. Führe aus:

   ```
   heat3d-wt-ranges -o ranges.json
   ```

   oder gleichwertig `heat3d-wt-replay ranges -o ranges.json`. Das Spiel wird
   über Steam oder die Ordner des Launchers gefunden; sonst sagen `--game <Ordner>`
   oder die Umgebungsvariable `HEAT3D_WT_GAME`, wo es liegt.
3. Sag dem Viewer, wo die Datei liegt: in der `tools/local-data.json` des
   Viewers ergänzt du

   ```json
   "ranges": { "wt": "C:/Pfad/zu/ranges.json" }
   ```

   und lädst den Viewer neu. Das Reichweitenfeld kennzeichnet diese Werte dann
   mit „aus deiner Installation“.

Das dauert ein bis zwei Minuten und gibt `ok <Datei> <n> weapons, <n> sensors, <n> units` aus.
`--quiet` lässt die Fortschrittszeilen weg. Rückgabewerte: 0 geschrieben, 2 das
Spiel wurde nicht gefunden.

## Was darin steht {#what-is-in-it}

| Teil | Inhalt |
|---|---|
| Waffen | je Waffe: ihre Klasse (Maschinengewehr, Maschinenkanone, Kanone, Lenkflugkörper, Bombe, Rakete, Torpedo), ihre kleinste, beste und größte Reichweite in Metern; bei Granaten Geschwindigkeit und Flugweite sowie die Visierweite der Kanone; bei Lenkflugkörpern Lenkung, Suchkopf, Aufschaltweite, G-Grenze und Starttabellen; die Namen, unter denen ein Replay sie nennen kann |
| Einheiten | je Bodenfahrzeug, Flugzeug, Hubschrauber und Schiff: seine Waffen, seine Sensoren und seine Visiere |
| Visiere | Richtschütze, Kommandant und Fahrer (bei Flugzeugen das Waffenvisier und der Zielbehälter): weitestes und engstes Sichtfeld, Wärmebildgerät und seine Generation, Nachtsicht, und ob das Visier mit der Kanone, dem Turm oder der Wanne dreht |
| Sensoren | Radare (Reichweite für ihre Bezugszielgröße, Suchsektor, Betriebsarten einschließlich Boden und See), Infrarot-Such- und Verfolgungsgeräte, passive Empfänger, Radarwarner, Raketen- und Laserwarner, Laserentfernungsmesser |

Wo das Spiel keine beste Reichweite angibt (ein Maschinengewehr ohne
Visierweite, eine Bombe), steht ein Klassenwert, und der Eintrag sagt das in
seinem `detail`. Die wirkliche Reichweite einer Bombe rechnet der Viewer aus
Höhe und Geschwindigkeit beim Abwurf.

## Die Datei {#the-file}

Eine JSON-Datei, `version` 1:

- `weapons`: eine Liste von `{ id, cls, name, range: [kleinste, beste, größte], shape, cone, alt, labels, detail }`
- `sensors`: nach Kennung, `{ kind, name, range, az, el, rcsRef, modes, mount, detail }`
- `units`: eine Liste von `{ names, weapons, sensors, optics }`; `names` sind
  die Kennung des Fahrzeugs und seine Namen in der englischen Lokalisierung des Spiels

Baue sie nach einem Spielupdate neu, um den Änderungen des Spiels zu folgen.
