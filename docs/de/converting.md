---
title: Replays umwandeln
nav_order: 4
lang: "de"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Replays umwandeln {#converting-replays}

Ergebnis: eine `.3dheat`-Datei pro Gefecht (der Standard) oder einzelne Dateien
mit `--loose`.

## Schritt für Schritt {#step-by-step}

1. **Replays einschalten.** War Thunder speichert Client-Replays im Ordner
   `Replays` des Spiels, wenn das Speichern von Replays in seinen Optionen an
   ist, zum Beispiel
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Ein Server-Replay, das über die Replay-Seite des Spiels gespeichert wurde
   (eine ZIP-Datei mit `0000.wrpl`, `0001.wrpl`, ...), kann ebenfalls
   umgewandelt werden.
2. **Ein Terminal öffnen** in einem Ordner, in den die Ergebnisse gelegt werden
   dürfen ([Bevor du anfängst](before-you-start.md)).
3. **Umwandeln:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # Dateien, Ordner oder beides
   heat3d-wt-replay battle.zip -o out              # die ZIP-Datei eines Server-Replays
   heat3d-wt-replay a.wrpl -o out --loose          # einzelne Dateien statt einer .3dheat
   ```

   `out` wird in dem Ordner angelegt, in dem dein Terminal steht.
4. **Lies, was es meldet.** Du solltest eine Zeile pro Gefecht sehen.
5. **Öffne es:** Lade `out/<map>/<match>.3dheat` in den 3DHeat-Viewer
   ([Eine Datei laden](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Ein Lauf mit einem synthetischen Replay: eine .3dheat, --loose, eine defekte Datei, ein leerer Ordner](../assets/img/convert.svg)

Das Bild zeigt einen Lauf mit einem Replay, das die Tests im Code erzeugen
(kein echtes Replay, keine Installation nötig):

- `ok <file>`: ein Gefecht wurde umgewandelt (mit `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: eine Datei, die nicht gelesen werden konnte (Exit-Status 1;
  die anderen werden trotzdem umgewandelt);
- `no .wrpl files given`: nichts zum Umwandeln da (Exit-Status 2);
- `note: ...`: zum Beispiel dass keine Installation von War Thunder gefunden wurde,
  um die Fahrzeuge zu benennen.

## Optionen {#options}

| Option | Standard | Wirkung |
|---|---|---|
| `replays` (eine oder mehrere) | - | `.wrpl`-Dateien, Ordner mit solchen Dateien (der Ordner selbst, nicht seine Unterordner) oder ZIP-Dateien mit ihnen (ein Server-Replay: seine `.wrpl`-Teile werden in einen temporären Ordner entpackt) |
| `-o`, `--out` | nötig | wohin geschrieben wird: ein Ordner pro Karte darin |
| `--game FOLDER` | gefunden | der Ordner von War Thunder, dessen Texte Fahrzeuge, Waffen und Munition benennen und dessen Tabellen die [Wirtschaft](economy.md) bepreisen; auch `HEAT3D_WT_GAME` |
| `--no-smoothing` | aus | die totgerechneten und empfangenen Messwerte anderer Einheiten so lassen, wie das Replay sie hat ([Totrechnung](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | an | jedes Gefecht in eine `.3dheat`-Datei packen |
| `--loose` | aus | jedes Gefecht als einzelne Dateien behalten (Tabelle, Match-Dokument, Sidecars) |
| `--version` | - | gibt `heat3d-wt-replay <version>` aus und endet |
| `-h`, `--help` | - | gibt die Optionen aus und endet |

Ein Gefecht, das erneut umgewandelt wird, wird neu geschrieben. Die Optionen,
so wie das Programm sie ausgibt: [Befehlsreferenz](../cli-reference.md).

## Welche Dateien ein Gefecht ergeben {#which-files-are-one-battle}

Jedes Gefecht wird zu einer Datei
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
und SB sind die Kurzformen des Spiels für Arcade-, Realistische und
Simulator-Gefechte; `<mode>` ist der Modus der Mission, so wie das Spiel ihn
kennt (`Conq4` Eroberung Nr. 4, `Dom` Dominanz, `Bttl` Schlacht; siehe
[Gefechtsmodus](ground.md#battle-mode)). Ein Teil fehlt, wenn das Replay
keinen nennt. Die Teile eines Server-Replays (`0000.wrpl`, `0001.wrpl`, ...)
werden zusammen als ein Gefecht gelesen. Ein Client-Replay und die Teile des
Servers desselben Gefechts sind zwei Aufnahmen und bleiben zwei.

## Exit-Status {#exit-status}

`0`, wenn jedes Gefecht umgewandelt wurde, `1`, wenn eines fehlgeschlagen ist
(die übrigen werden trotzdem umgewandelt), `2`, wenn unter den Argumenten keine
Replay-Datei gefunden wurde.

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
