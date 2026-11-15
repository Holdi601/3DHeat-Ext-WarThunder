---
title: "Visszajátszások konvertálása"
nav_order: 4
lang: "hu"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Visszajátszások konvertálása {#converting-replays}

Kimenet: egy csatánként egy `.3dheat` fájl (alapértelmezés), vagy külön fájlok
a `--loose` kapcsolóval.

## Lépésről lépésre {#step-by-step}

1. **Kapcsold be a visszajátszást.** A War Thunder a kliens-visszajátszásokat a játék
   `Replays` (Visszajátszások) mappájába menti, ha a beállításaiban be van kapcsolva
   a visszajátszás mentése, például:
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   A játék szerver-visszajátszás oldaláról mentett szerver-visszajátszás (egy zip
   a `0000.wrpl`, `0001.wrpl`, ... fájlokkal) is konvertálható.
2. **Nyiss egy terminált** abban a mappában, ahová az eredmények kerülhetnek
   ([Mielőtt elkezded](before-you-start.md)).
3. **Konvertálás:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   Az `out` a terminálod mappájában jön létre.
4. **Olvasd el, mit ír ki.** Csatánként egy sort kell látnod.
5. **Nyisd meg:** töltsd be az `out/<map>/<match>.3dheat` fájlt a 3DHeat
   megjelenítőben ([Betöltés](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Futtatás szintetikus visszajátszáson: egy .3dheat, --loose, egy sérült fájl, egy üres mappa](../assets/img/convert.svg)

A kép egy olyan visszajátszáson készült futtatást mutat, amelyet a tesztek kódban
hoznak létre (valódi visszajátszás és telepítés nélkül):

- `ok <file>`: egy csata konvertálva (a `--loose` kapcsolóval: `ok <table> <match document>`);
- `failed <file>: <why>`: egy fájl, amelyet nem lehetett beolvasni (kilépési állapot 1;
  a többit attól még konvertálja);
- `no .wrpl files given`: nincs mit konvertálni (kilépési állapot 2);
- `note: ...`: például hogy nem található War Thunder-telepítés, amelyből a járművek
  neveit ki lehetne olvasni.

## Kapcsolók {#options}

| Kapcsoló | Alapértelmezés | Mit tesz |
|---|---|---|
| `replays` (egy vagy több) | - | `.wrpl` fájlok, ezek mappái (maga a mappa, nem az almappái), vagy ezek zip-jei (szerver-visszajátszás: a `.wrpl` részei ideiglenes mappába csomagolódnak ki) |
| `-o`, `--out` | kötelező | hová írjon: bennük mappa minden térképhez |
| `--game FOLDER` | megtalálja | a War Thunder mappája, amelynek szövegei nevezik a járműveket, fegyvereket és lőszert, és amelynek táblázatai árazzák a [gazdaságot](economy.md); a `HEAT3D_WT_GAME` környezeti változóval is megadható |
| `--no-smoothing` | ki | a többi egység holtpont-számított és kapott mintáit úgy tartja meg, ahogy a visszajátszás adja ([Holtpont-számítás](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | be | minden csatát egy `.3dheat` fájlba csomagol |
| `--loose` | ki | minden csatát külön fájlokban tart (táblázat, meccsdokumentum, kísérőfájlok) |
| `--version` | - | kiírja a `heat3d-wt-replay <version>` szöveget, és leáll |
| `-h`, `--help` | - | kiírja a kapcsolókat, és leáll |

Egy már konvertált csata újra konvertálva újra íródik. A kapcsolók ahogy a program
kiírja: [Parancsreferencia](../cli-reference.md).

## Mely fájlok egy csata {#which-files-are-one-battle}

Minden csata egy fájlt alkot:
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. Az AB, RB és SB
a játék rövid alakjai az arcade, realisztikus és szimulátor csatákra; a `<mode>` a
küldetés módja, ahogy a játék kulcsolja (`Conq4` Conquest #4 (Hódítás #4), `Dom`
Domination (Dominancia), `Bttl` Battle (Csata); lásd [Csatamód](ground.md#battle-mode));
a részek bármelyike kimarad, ha a visszajátszás nem nevez meg egyet sem. Egy szerver-visszajátszás
részeit (`0000.wrpl`, `0001.wrpl`, ...) együtt, egy csataként olvassuk; egy kliens-visszajátszás
és ugyanannak a csatának a szerver-részei két különböző felvétel, ezért kettő marad.

## Kilépési állapot {#exit-status}

`0`, ha minden csata konvertálódott; `1`, ha bármelyik nem sikerült (a többit attól
még konvertálja); `2`, ha a paraméterek között nem volt visszajátszás-fájl.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
