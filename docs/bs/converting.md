---
title: "Pretvaranje replayeva"
nav_order: 4
lang: "bs"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Pretvaranje replayeva {#converting-replays}

Izlaz: jedna `.3dheat` datoteka po bici (zadano), ili odvojene datoteke s
`--loose`.

## Korak po korak {#step-by-step}

1. **Uključite replayeve.** War Thunder sprema klijentske replayeve u folder `Replays`
   igre kada je spremanje replayeva uključeno u njegovim opcijama, na primjer
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Serverski replay spremljen sa stranice replayeva u igri (zip s `0000.wrpl`,
   `0001.wrpl`, ...) također se može pretvoriti.
2. **Otvorite terminal** u folderu u koji rezultati smiju ići
   ([Prije nego počnete](before-you-start.md)).
3. **Pretvorite:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` se pravi u folderu u kojem je vaš terminal.
4. **Pročitajte šta ispiše.** Trebali biste vidjeti jedan red po bici.
5. **Otvorite:** učitajte `out/<map>/<match>.3dheat` u 3DHeat pregledniku
   ([Učitavanje jedne](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Pokretanje na sintetičkom replayu: jedna .3dheat, --loose, pokvarena datoteka, prazan folder](../assets/img/convert.svg)

Slika prikazuje pokretanje na replayu koji testovi grade u kodu (nije pravi replay,
nema instalacije):

- `ok <file>`: bitka je pretvorena (uz `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: datoteka koja se nije mogla pročitati (izlazni status 1;
  ostale se i dalje pretvaraju);
- `no .wrpl files given`: nema šta pretvarati (izlazni status 2);
- `note: ...`: na primjer da nije pronađena War Thunder instalacija za imenovanje
  vozila.

## Opcije {#options}

| Opcija | Zadano | Šta radi |
|---|---|---|
| `replays` (jedan ili više) | - | `.wrpl` datoteke, folderi s njima (sam folder, ne njegovi podfolderi) ili zipovi s njima (serverski replay: njegovi `.wrpl` dijelovi se raspakiraju u privremeni folder) |
| `-o`, `--out` | obavezno | gdje pisati: unutra folder po mapi |
| `--game FOLDER` | pronađeno | War Thunder folder čiji tekst imenuje vozila, oružje i municiju, a čije tabele određuju cijene [ekonomije](economy.md); također `HEAT3D_WT_GAME` |
| `--no-smoothing` | isključeno | zadrži izvedene (dead-reckoned) i primljene uzorke drugih jedinica onako kako ih replay ima ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | uključeno | spakuj svaku bitku u jednu `.3dheat` datoteku |
| `--loose` | isključeno | zadrži svaku bitku kao odvojene datoteke (tabela, dokument meča, sidecar datoteke) |
| `--version` | - | ispiši `heat3d-wt-replay <version>` i stani |
| `-h`, `--help` | - | ispiši opcije i stani |

Bitka koja se pretvori ponovo bit će ponovo upisana. Opcije onako kako ih program
ispisuje: [Referenca naredbi](../cli-reference.md).

## Koje datoteke čine jednu bitku {#which-files-are-one-battle}

Svaka bitka postaje jedna datoteka,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
i SB su skraćenice igre za arkadne, realistične i simulatorske
bitke; `<mode>` je način misije onako kako ga igra označava (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; vidi
[Način bitke](ground.md#battle-mode)); svaki dio se izostavlja tamo gdje ga
replay ne navodi. Dijelovi serverskog replaya (`0000.wrpl`, `0001.wrpl`, ...)
čitaju se zajedno kao jedna bitka; klijentski replay i serverski dijelovi
iste bitke su dva snimka i ostaju dva.

## Izlazni status {#exit-status}

`0` kada je svaka bitka pretvorena, `1` kada je neka propala (ostale se i dalje
pretvaraju), `2` kada među argumentima nije pronađena nijedna replay datoteka.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
