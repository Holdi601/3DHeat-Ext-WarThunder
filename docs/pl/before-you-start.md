---
title: Zanim zaczniesz
nav_order: 2
lang: "pl"
source: before-you-start.md
source_hash: "99034fb56b0d"
nav_exclude: true
search_exclude: true
---
# Zanim zaczniesz {#before-you-start}

Nowy w wierszu poleceń? Ta strona prowadzi od zera do działającego
`heat3d-wt-replay` w mniej więcej dziesięć minut. Jeśli już używasz Pythona,
przejdź od razu do [Instalacji](installing.md).

## 1. Zainstaluj Pythona {#install-python}

1. Pobierz Pythona **w wersji 3.10 lub nowszej** ze strony
   [python.org/downloads](https://www.python.org/downloads/).
2. W systemie Windows zaznacz **Add python.exe to PATH** w pierwszym oknie
   instalatora, a potem kliknij **Install Now**.
3. W systemie macOS i Linux Python 3 często jest już zainstalowany. Wpisz
   `python3` tam, gdzie te strony piszą `python`, oraz `pip3` zamiast `pip`.

## 2. Otwórz terminal {#open-a-terminal}

Terminal to okno, w którym wpisujesz polecenia.

- **Windows:** otwórz folder w Eksploratorze plików, kliknij pasek adresu,
  wpisz `cmd` i naciśnij Enter. Otworzy się okno już w tym folderze.
- **macOS:** otwórz aplikację **Terminal**. **Linux:** kliknij prawym
  przyciskiem myszy w folderze i wybierz **Otwórz w terminalu**.

Żeby przejść do innego folderu, wpisz `cd` i nazwę folderu:

```bash
cd "C:\Users\you\Downloads\3DHeat-Ext-WarThunder-main"
```

## 3. Sprawdź, czy Python działa {#check-that-python-works}

```bash
python --version
```

Powinieneś zobaczyć `Python 3.` i numer 10 lub wyższy, na przykład
`Python 3.12.4`.

## 4. Pobierz narzędzie i zainstaluj je {#get-the-tool-and-install-it}

1. Na [stronie narzędzia na GitHubie](https://github.com/Holdi601/3DHeat-Ext-WarThunder) kliknij
   zielony przycisk **Code**, potem **Download ZIP**, i rozpakuj archiwum zip.
2. Otwórz terminal w rozpakowanym folderze (tym, w którym leży `README.md`).
3. Wpisz:

   ```bash
   pip install -e .
   ```

   Na końcu powinieneś zobaczyć: `Successfully installed heat3d-ext-warthunder-0.2.0`
   (może z dodatkowymi nazwami).
4. Sprawdź:

   ```bash
   heat3d-wt-replay --version
   ```

   Powinieneś zobaczyć: `heat3d-wt-replay 0.2.0`

## Jak czytać polecenia na tych stronach {#how-to-read-the-commands-on-these-pages}

- Słowa w nawiasach ostrych, jak `<replays>`, to miejsca na Twoje dane: wpisz
  tam swój plik lub folder, bez nawiasów.
- Ścieżka ze spacjami potrzebuje cudzysłowów: `"C:\Program Files (x86)\Steam"`.
- Tekst po `#` to komentarz: nie wpisujesz go.
- `-o out` zapisuje do folderu `out` wewnątrz folderu, w którym jest terminal.
  Jeśli go nie ma, zostanie utworzony.

## Jak wygląda sukces {#what-success-looks-like}

Polecenie wypisuje jedną linię dla każdego replaya, na przykład:

```text
ok out/<map>/<match>.3dheat
```

i kończy się statusem `0`. Nowe pliki są w folderze `out`.

## Typowe błędy {#common-errors}

| Widzisz | Co zrobić |
|---|---|
| `'python' is not recognized ...` lub `command not found` | Python nie jest w PATH: zainstaluj go ponownie z zaznaczonym **Add python.exe to PATH** albo wpisz `py` zamiast `python` (Windows) |
| `'pip' is not recognized ...` | wpisz zamiast tego `python -m pip install -e .` |
| `'heat3d-wt-replay' is not recognized ...` | wpisz `python -m heat3d_ext_warthunder` zamiast `heat3d-wt-replay`; robi to samo |
| `No module named heat3d_ext_warthunder` | nie jesteś w folderze narzędzia albo nie jest ono zainstalowane: przejdź tam poleceniem `cd` i uruchom `pip install -e .` |
| `the following arguments are required: -o/--out` | dopisz do polecenia `-o out` |

Dalej: [Konwertowanie replayów](converting.md).
