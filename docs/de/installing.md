---
title: Installation
nav_order: 3
lang: de
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installation {#installing}

Neu auf der Kommandozeile? Lies zuerst [Bevor du anfängst](before-you-start.md).
Man braucht Python 3.10 oder neuer; pyarrow, numpy, zstandard und Pillow werden
mit installiert.

## Schritt für Schritt {#step-by-step}

1. Hol dir den Code: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   oder lade eine ZIP-Datei von [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   herunter und entpacke sie.
2. Öffne ein Terminal in diesem Ordner und tippe `pip install -e .`. Dabei werden
   zwei Befehle installiert: `heat3d-wt-replay` (Replays) und `heat3d-wt-level` (Level).
3. Prüfe es: `heat3d-wt-replay --version`. Du solltest
   `heat3d-wt-replay 0.2.0` sehen. `heat3d-wt-replay --help` listet die Optionen:

![heat3d-wt-replay --help](../assets/img/help.svg)

Ohne Installation: `python -m heat3d_ext_warthunder ...` und
`python -m heat3d_ext_warthunder.levelcli ...` im Ordner des Werkzeugs.

## Namen aus deiner Installation {#names-from-your-install}

Fahrzeuge, Waffen und Munition bekommen ihre englischen Namen aus den eigenen
Textdateien des Spiels, die beim Umwandeln aus deiner Installation gelesen werden.
Die Installation wird über Steam oder die Standardordner des Launchers gefunden;
`--game <folder>` oder die Umgebungsvariable `HEAT3D_WT_GAME` sagen sonst, wo sie
liegt. Vom Text des Spiels ist nichts in diesem Repository. Ohne Installation sind
die Namen die Fahrzeug-IDs (der Umwandler sagt das in einer Zeile `note:`).

## Aktualisierungen {#updates}

Jeder Start prüft zuerst die GitHub-Releases des Projekts (höchstens eine Anfrage
alle paar Stunden; das hält eine Umwandlung nie an, online oder offline). Ist ein
neueres Release da, fragt der Befehl, bevor er es installiert: Ein `git clone` wird
mit `git pull --ff-only` aktualisiert (abgelehnt, solange du lokale Änderungen hast),
eine heruntergeladene Kopie aus dem Archiv des Releases. `HEAT3D_NO_UPDATE=1` schaltet
die Prüfung und die Aktualisierung ab.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
