---
title: "Replays émwandelen"
nav_order: 4
lang: lb
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Replays émwandelen {#converting-replays}

Ausgab: eng `.3dheat`-Datei pro Gefecht (de Standard), oder lose Dateie mat
`--loose`.

## Schrëtt fir Schrëtt {#step-by-step}

1. **Replays uschalten.** War Thunder späichert Client-Replays am `Replays`-
   Dossier vum Spill, wann d'Replay-Späichere a sengen Optioune ugeschalt ass, zum Beispill
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   E Server-Replay, deen op der Replay-Säit vum Spill gespäichert gouf (eng Zip mat `0000.wrpl`,
   `0001.wrpl`, ...), kann och émgewandelt ginn.
2. **Mécht en Terminal op** an engem Dossier, an dee d'Resultater däerfen goen
   ([Ier Dir ufänkt](before-you-start.md)).
3. **Wandelt em:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` gëtt an dem Dossier gemaach, an deem Äre Terminal ass.
4. **Liest, wat et seet.** Dir sollt eng Zeil pro Gefecht gesinn.
5. **Mécht et op:** luet `out/<map>/<match>.3dheat` am 3DHeat-Viewer
   ([Eng lueden](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![E Laf op engem synthetesche Replay: eng .3dheat, --loose, eng futtis Datei, en eidele Dossier](../assets/img/convert.svg)

D'Bild ass e Laf op engem Replay, deen d'Tester am Code bauen (kee richtege Replay,
keng Installatioun):

- `ok <file>`: e Gefecht gouf émgewandelt (mat `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: eng Datei, déi net konnt gelies ginn (Exit-Status 1; déi
  anerer ginn trotzdem émgewandelt);
- `no .wrpl files given`: näischt zum Émwandelen (Exit-Status 2);
- `note: ...`: zum Beispill, datt keng War-Thunder-Installatioun fonnt gouf, fir d'
  Gefierer ze benennen.

## Optiounen {#options}

| Optioun | Standard | Wat se mécht |
|---|---|---|
| `replays` (ee oder méi) | - | `.wrpl`-Dateien, Dossiere dovunner (den Dossier selwer, net seng Ënnerdossieren), oder Zips dovunner (e Server-Replay: seng `.wrpl`-Deeler ginn an en temporären Dossier ausgepaakt) |
| `-o`, `--out` | erfuerderlech | wou geschriwwe gëtt: dran een Dossier pro Kaart |
| `--game FOLDER` | fonnt | den War-Thunder-Dossier, deem seng Texter Gefierer, Waffen a Munitioun benennen, an deem seng Tabelle fir d'[Wirtschaft](economy.md) d'Präisser ginn; och `HEAT3D_WT_GAME` |
| `--no-smoothing` | aus | d'Echantillone vun aneren Eenheeten, déi duerch Dead Reckoning geschat oder empfaange goufen, esou behalen, wéi de Replay se huet ([Dead Reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | un | all Gefecht an eng `.3dheat`-Datei paken |
| `--loose` | aus | all Gefecht als getrennten Dateie behalen (Tabell, Match-Dokument, Niewendateien) |
| `--version` | - | `heat3d-wt-replay <version>` drécken an ophalen |
| `-h`, `--help` | - | d'Optiounen drécken an ophalen |

E Gefecht, dat nach eng Kéier émgewandelt gëtt, gëtt nei geschriwwen. D'Optioune sou, wéi de Programm
se dréckt: [Befehlsreferenz](../cli-reference.md).

## Wéi eng Dateie ee Gefecht sinn {#which-files-are-one-battle}

All Gefecht gëtt eng Datei,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
a SB sinn d'Kuerzformen vum Spill fir Arcade-, Realistic- a Simulator-
Gefechter; `<mode>` ass de Modus vun der Mission, wéi d'Spill en schlësselt (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; kuck
[Battle-Modus](ground.md#battle-mode)); jidde Part fält ewech, wou de
Replay keen nennt. D'Deeler vun engem Server-Replay (`0000.wrpl`, `0001.wrpl`, ...)
ginn zesummen als ee Gefecht gelies; e Client-Replay an d'Server-Deeler
vum selwechte Gefecht sinn zwou Opnamen a bleiwen zwee.

## Exit-Status {#exit-status}

`0`, wann all Gefecht émgewandelt gouf, `1`, wann ee gescheitert ass (déi aner ginn trotzdem
émgewandelt), `2`, wann ënnert den Argumenter keng Replay-Datei fonnt gouf.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
