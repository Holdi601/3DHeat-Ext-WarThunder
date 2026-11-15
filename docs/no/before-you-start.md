---
title: "Før du starter"
nav_order: 2
lang: "no"
source: before-you-start.md
source_hash: "99034fb56b0d"
nav_exclude: true
search_exclude: true
---
# Før du starter {#before-you-start}

Ny på kommandolinjen? Denne siden tar deg fra ingenting til en fungerende
`heat3d-wt-replay` på ca. ti minutter. Bruker du Python fra før, gå rett til
[Installere](installing.md).

## 1. Installer Python {#install-python}

1. Last ned Python **3.10 eller nyere** fra
   [python.org/downloads](https://www.python.org/downloads/).
2. På Windows: kryss av for **Add python.exe to PATH** i det første vinduet i
   installasjonsprogrammet, og klikk deretter **Install Now**.
3. På macOS og Linux er Python 3 ofte installert fra før. Skriv `python3` der
   disse sidene sier `python`, og `pip3` der de sier `pip`.

## 2. Åpne en terminal {#open-a-terminal}

En terminal er et vindu der du skriver kommandoer.

- **Windows:** åpne mappen i Filutforsker, klikk i adressefeltet, skriv `cmd`
  og trykk Enter. Et vindu åpnes, allerede i den mappen.
- **macOS:** åpne appen **Terminal**. **Linux:** høyreklikk i mappen og velg
  **Open in Terminal**.

For å gå til en annen mappe, skriv `cd` og mappen:

```bash
cd "C:\Users\deg\Downloads\3DHeat-Ext-WarThunder-main"
```

## 3. Sjekk at Python fungerer {#check-that-python-works}

```bash
python --version
```

Du bør se `Python 3.` og et tall på 10 eller høyere, for eksempel
`Python 3.12.4`.

## 4. Hent verktøyet og installer det {#get-the-tool-and-install-it}

1. Gå til [verktøyets GitHub-side](https://github.com/Holdi601/3DHeat-Ext-WarThunder), klikk
   den grønne knappen **Code**, deretter **Download ZIP**, og pakk ut zip-filen.
2. Åpne en terminal i den utpakkede mappen (den som har `README.md` i seg).
3. Skriv:

   ```bash
   pip install -e .
   ```

   Til slutt bør du se: `Successfully installed heat3d-ext-warthunder-0.2.0`
   (kanskje med flere navn).
4. Sjekk det:

   ```bash
   heat3d-wt-replay --version
   ```

   Du bør se: `heat3d-wt-replay 0.2.0`

## Slik leser du kommandoene på disse sidene {#how-to-read-the-commands-on-these-pages}

- Ord i vinkelparenteser, som `<replays>`, er plassholdere: skriv din egen fil
  eller mappe der, uten parentesene.
- En sti med mellomrom trenger anførselstegn: `"C:\Program Files (x86)\Steam"`.
- Tekst etter `#` er en kommentar: den skriver du ikke.
- `-o out` skriver inn i en mappe som heter `out`, inne i mappen terminalen
  står i. Den lages hvis den ikke finnes.

## Slik ser suksess ut {#what-success-looks-like}

Kommandoen skriver ut én linje per replay, for eksempel:

```text
ok out/<kart>/<kamp>.3dheat
```

og avsluttes med exit-status `0`. De nye filene ligger i mappen `out`.

## Vanlige feil {#common-errors}

| Du ser | Hva du gjør |
|---|---|
| `'python' is not recognized ...` eller `command not found` | Python er ikke på PATH: installer på nytt med **Add python.exe to PATH** krysset av, eller skriv `py` i stedet for `python` (Windows) |
| `'pip' is not recognized ...` | skriv `python -m pip install -e .` i stedet |
| `'heat3d-wt-replay' is not recognized ...` | skriv `python -m heat3d_ext_warthunder` i stedet for `heat3d-wt-replay`; den gjør det samme |
| `No module named heat3d_ext_warthunder` | du er ikke i verktøyets mappe, eller det er ikke installert: `cd` dit og kjør `pip install -e .` |
| `the following arguments are required: -o/--out` | legg til `-o out` i kommandoen |

Neste: [Konvertere replayer](converting.md).
