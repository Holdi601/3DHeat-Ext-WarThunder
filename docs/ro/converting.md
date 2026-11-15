---
title: Convertirea replay-urilor
nav_order: 4
lang: ro
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Convertirea replay-urilor {#converting-replays}

Rezultat: un fișier `.3dheat` pentru fiecare bătălie (implicit), sau fișiere separate cu
`--loose`.

## Pas cu pas {#step-by-step}

1. **Activați salvarea replay-urilor.** War Thunder salvează replay-urile de client în folderul
   `Replays` al jocului, când salvarea replay-urilor este activată în opțiuni, de exemplu
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Un replay de server salvat din pagina de replay-uri a jocului (un zip cu `0000.wrpl`,
   `0001.wrpl`, ...) poate fi și el convertit.
2. **Deschideți un terminal** într-un folder în care rezultatele pot fi scrise
   ([Înainte de început](before-you-start.md)).
3. **Convertiți:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # fișiere, foldere, sau ambele
   heat3d-wt-replay battle.zip -o out              # zip-ul unui replay de server
   heat3d-wt-replay a.wrpl -o out --loose          # fișiere separate în loc de un .3dheat
   ```

   `out` este creat în folderul în care se află terminalul.
4. **Citiți ce afișează.** Ar trebui să vedeți câte o linie pentru fiecare bătălie.
5. **Deschideți-l:** încărcați `out/<map>/<match>.3dheat` în vizualizatorul 3DHeat
   ([Încărcarea unui fișier](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![O rulare pe un replay sintetic: un .3dheat, --loose, un fișier defect, un folder gol](../assets/img/convert.svg)

Imaginea este o rulare pe un replay pe care testele îl construiesc în cod (fără replay real,
fără instalare):

- `ok <file>`: o bătălie convertită (cu `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: un fișier care nu a putut fi citit (codul de ieșire 1; celelalte
  sunt convertite în continuare);
- `no .wrpl files given`: nimic de convertit (codul de ieșire 2);
- `note: ...`: de exemplu că nu s-a găsit nicio instalare War Thunder din care să se
  dea numele vehiculelor.

## Opțiuni {#options}

| Opțiune | Implicit | Ce face |
|---|---|---|
| `replays` (una sau mai multe) | - | fișiere `.wrpl`, foldere cu ele (folderul în sine, nu subfolderele sale), sau zip-uri cu ele (un replay de server: părțile sale `.wrpl` sunt dezarhivate într-un folder temporar) |
| `-o`, `--out` | obligatoriu | unde se scrie: un folder pentru fiecare hartă, în interior |
| `--game FOLDER` | găsit | folderul War Thunder al cărui text dă numele vehiculelor, armelor și muniției și ale cărui tabele prețuiesc [economia](economy.md); de asemenea `HEAT3D_WT_GAME` |
| `--no-smoothing` | oprit | păstrează eșantioanele estimate prin navigare pe baza vitezei („dead reckoning”) și cele primite ale celorlalte unități așa cum le are replay-ul ([Estimarea prin navigare](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | pornit | împachetează fiecare bătălie într-un fișier `.3dheat` |
| `--loose` | oprit | păstrează fiecare bătălie ca fișiere separate (tabel, document al meciului, fișiere auxiliare) |
| `--version` | - | afișează `heat3d-wt-replay <version>` și se oprește |
| `-h`, `--help` | - | afișează opțiunile și se oprește |

O bătălie convertită din nou este scrisă din nou. Opțiunile așa cum le afișează programul:
[Referința comenzilor](../cli-reference.md).

## Ce fișiere sunt o bătălie {#which-files-are-one-battle}

Fiecare bătălie devine un fișier,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
și SB sunt formele scurte ale jocului pentru bătăliile arcade, realiste și simulator;
`<mode>` este modul misiunii, cum îl notează jocul (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; vedeți
[Modul de bătălie](ground.md#battle-mode)); oricare parte este lăsată afară acolo unde replay-ul
nu o numește. Părțile unui replay de server (`0000.wrpl`, `0001.wrpl`, ...)
sunt citite împreună ca o singură bătălie; un replay de client și părțile serverului
pentru aceeași bătălie sunt două înregistrări și rămân două.

## Codul de ieșire {#exit-status}

`0` când toate bătăliile au fost convertite, `1` când vreuna a eșuat (celelalte sunt
convertite în continuare), `2` când nu s-a găsit niciun fișier de replay printre argumente.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
