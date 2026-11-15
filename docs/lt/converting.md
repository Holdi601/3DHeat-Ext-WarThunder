---
title: Įrašų konvertavimas
nav_order: 4
lang: lt
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Įrašų konvertavimas {#converting-replays}

Rezultatas: vienas `.3dheat` failas mūšiui (numatytasis), arba atskiri failai su `--loose`.

## Žingsnis po žingsnio {#step-by-step}

1. **Įjunkite įrašus.** War Thunder išsaugo kliento įrašus žaidimo aplanke `Replays`, kai jo
   nustatymuose įjungtas įrašų saugojimas, pavyzdžiui
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Serverio įrašą, išsaugotą iš žaidimo įrašų puslapio (zip failas su `0000.wrpl`,
   `0001.wrpl`, ...), taip pat galima konvertuoti.
2. **Atidarykite terminalą** aplanke, kuriame gali būti įrašomi rezultatai
   ([Prieš pradedant](before-you-start.md)).
3. **Konvertuokite:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` sukuriamas aplanke, kuriame yra jūsų terminalas.
4. **Perskaitykite, ką jis praneša.** Turėtumėte matyti po vieną eilutę kiekvienam mūšiui.
5. **Atidarykite:** įkelkite `out/<map>/<match>.3dheat` 3DHeat žiūryklėje
   ([Įkėlimas vieno](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![A run on a synthetic replay: one .3dheat, --loose, a broken file, an empty folder](../assets/img/convert.svg)

Paveikslėlis - tai paleidimas su sintetiniu įrašu, kurį testai sukuria kode (jokio tikro įrašo,
jokio diegimo):

- `ok <file>`: mūšis konvertuotas (su `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: failo nepavyko perskaityti (išėjimo statusas 1; kiti vis tiek
  konvertuojami);
- `no .wrpl files given`: nėra ką konvertuoti (išėjimo statusas 2);
- `note: ...`: pavyzdžiui, kad techninės įrangos vardams nerasta War Thunder diegimo.

## Parametrai {#options}

| Parametras | Numatytasis | Ką daro |
|---|---|---|
| `replays` (vienas ar daugiau) | - | `.wrpl` failai, jų aplankai (pats aplankas, ne jo poaplankiai) arba jų zip archyvai (serverio įrašas: jo `.wrpl` dalys išskleidžiamos į laikiną aplanką) |
| `-o`, `--out` | privalomas | kur rašyti: kiekvieno žemėlapio aplankas viduje |
| `--game FOLDER` | randamas | War Thunder aplankas, kurio tekstas įvardija techniką, ginklus ir šaudmenis ir kurio lentelės nustato [ekonomiką](economy.md); taip pat `HEAT3D_WT_GAME` |
| `--no-smoothing` | išjungtas | palikti kitų vienetų dead reckoning ir gautus pavyzdžius taip, kaip juos turi įrašas ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | įjungtas | supakuoti kiekvieną mūšį į vieną `.3dheat` failą |
| `--loose` | išjungtas | palikti kiekvieną mūšį atskirais failais (lentelė, rungtynių dokumentas, papildomi failai) |
| `--version` | - | išvesti `heat3d-wt-replay <version>` ir sustoti |
| `-h`, `--help` | - | išvesti parametrus ir sustoti |

Mūšis, konvertuotas dar kartą, įrašomas iš naujo. Parametrai taip, kaip juos rodo programa:
[Komandų nuoroda](../cli-reference.md).

## Kurie failai yra vienas mūšis {#which-files-are-one-battle}

Kiekvienas mūšis tampa vienu failu,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB ir SB yra žaidimo
trumpos arkadinių, realistinių ir simuliatoriaus mūšių formos; `<mode>` yra misijos režimas, kaip
jį pažymi žaidimas (`Conq4` - Konkvista #4, `Dom` - Dominavimas, `Bttl` - Mūšis; žr.
[Mūšio režimas](ground.md#battle-mode)); bet kuri dalis praleidžiama, jei įraše jos nėra. Serverio
įrašo dalys (`0000.wrpl`, `0001.wrpl`, ...) skaitomos kartu kaip vienas mūšis; kliento įrašas ir
serverio dalys to paties mūšio yra du įrašai ir lieka du.

## Išėjimo statusas {#exit-status}

`0`, kai kiekvienas mūšis konvertuotas, `1`, kai kuris nepavyko (kiti vis tiek konvertuojami), `2`,
kai tarp argumentų nerasta jokio įrašo failo.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
