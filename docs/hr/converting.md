---
title: Pretvaranje snimki
nav_order: 4
lang: "hr"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Pretvaranje snimki {#converting-replays}

Rezultat: jedna datoteka `.3dheat` po bitki (zadano), ili odvojene datoteke s
`--loose`.

## Korak po korak {#step-by-step}

1. **Uključi snimke.** War Thunder sprema snimke klijenta u mapu `Replays` igre kad je
   spremanje snimki uključeno u njegovim opcijama, na primjer
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Poslužiteljska snimka spremljena sa stranice snimki igre (zip s `0000.wrpl`,
   `0001.wrpl`, ...) također se može pretvoriti.
2. **Otvori terminal** u mapi u kojoj rezultati smiju biti
   ([Prije početka](before-you-start.md)).
3. **Pretvori:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # datoteke, mape, ili oboje
   heat3d-wt-replay battle.zip -o out              # zip poslužiteljske snimke
   heat3d-wt-replay a.wrpl -o out --loose          # odvojene datoteke umjesto jedne .3dheat
   ```

   `out` se napravi u mapi u kojoj je tvoj terminal.
4. **Pročitaj što piše.** Trebao bi vidjeti jedan redak po bitki.
5. **Otvori ga:** učitaj `out/<map>/<match>.3dheat` u 3DHeat pregledniku
   ([Učitavanje jedne](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Pokretanje na sintetičkoj snimci: jedna .3dheat, --loose, neispravna datoteka, prazna mapa](../assets/img/convert.svg)

Slika prikazuje pokretanje na snimci koju testovi grade u kodu (nema prave snimke,
nema instalacije):

- `ok <file>`: bitka pretvorena (uz `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: datoteka koja se nije mogla pročitati (status izlaza 1; ostale
  se i dalje pretvaraju);
- `no .wrpl files given`: ništa za pretvoriti (status izlaza 2);
- `note: ...`: na primjer da nije nađena instalacija War Thundera za imenovanje vozila.

## Opcije {#options}

| Opcija | Zadano | Radi |
|---|---|---|
| `replays` (jedna ili više) | - | `.wrpl` datoteke, mape s njima (sama mapa, ne njezine podmape), ili zipovi s njima (poslužiteljska snimka: njezini `.wrpl` dijelovi raspakiraju se u privremenu mapu) |
| `-o`, `--out` | obavezno | gdje pisati: mapa po karti unutar |
| `--game MAPA` | pronađeno | mapa War Thundera čiji tekst imenuje vozila, oružje i streljivo i čije tablice određuju cijenu [ekonomije](economy.md); također `HEAT3D_WT_GAME` |
| `--no-smoothing` | isključeno | zadrži uzorke drugih jedinica izračunate mrtvim računom i primljene uzorke kako ih snimka ima ([Mrtvi račun](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | uključeno | spakiraj svaku bitku u jednu datoteku `.3dheat` |
| `--loose` | isključeno | zadrži svaku bitku kao odvojene datoteke (tablica, dokument meča, pomoćne datoteke) |
| `--version` | - | ispiši `heat3d-wt-replay <version>` i stani |
| `-h`, `--help` | - | ispiši opcije i stani |

Bitka pretvorena ponovno bit će ponovno zapisana. Opcije kako ih program ispisuje:
[Referenca naredbi](../cli-reference.md).

## Koje datoteke čine jednu bitku {#which-files-are-one-battle}

Svaka bitka postaje jedna datoteka
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
i SB su kratice igre za arkadne, realistične i simulacijske bitke; `<mode>` je način rada
misije kako ga igra označava (`Conq4` Conquest #4, `Dom` Domination, `Bttl` Battle; vidi
[Način bitke](ground.md#battle-mode)); bilo koji dio se izostavi ako snimka ne imenuje
ništa. Dijelovi poslužiteljske snimke (`0000.wrpl`, `0001.wrpl`, ...) čitaju se zajedno kao
jedna bitka; klijentska snimka i poslužiteljski dijelovi iste bitke su dvije snimke i ostaju dvije.

## Status izlaza {#exit-status}

`0` kad je svaka bitka pretvorena, `1` kad je neka nije uspjela (ostale se i dalje
pretvaraju), `2` kad među argumentima nije nađena nijedna datoteka snimke.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
