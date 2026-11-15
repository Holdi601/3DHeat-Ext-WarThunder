---
title: Instalacja
nav_order: 3
lang: "pl"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalacja {#installing}

Nowy w wierszu poleceń? Najpierw przeczytaj [Zanim zaczniesz](before-you-start.md).
Potrzebny jest Python 3.10 lub nowszy; pyarrow, numpy, zstandard i Pillow
instalują się razem z nim.

## Krok po kroku {#step-by-step}

1. Pobierz kod: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   albo pobierz archiwum zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   i rozpakuj je.
2. Otwórz terminal w tym folderze i wpisz `pip install -e .`. Instaluje to
   dwa polecenia: `heat3d-wt-replay` (replaye) i `heat3d-wt-level` (poziomy).
3. Sprawdź: `heat3d-wt-replay --version`. Powinieneś zobaczyć
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` wypisuje opcje:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez instalowania: `python -m heat3d_ext_warthunder ...` i
`python -m heat3d_ext_warthunder.levelcli ...` w folderze narzędzia.

## Nazwy z Twojej instalacji {#names-from-your-install}

Pojazdy, uzbrojenie i amunicja dostają angielskie nazwy z plików tekstowych
samej gry, odczytywanych z Twojej instalacji podczas konwertowania. Instalację znajduje
się przez Steam lub domyślne foldery launchera; `--game <folder>` albo zmienna
środowiskowa `HEAT3D_WT_GAME` mówią, gdzie ona jest, jeśli nie została znaleziona. W tym repozytorium nie ma żadnego tekstu z gry;
bez instalacji nazwami są identyfikatory pojazdów (konwerter mówi o tym w linii `note:`).

## Aktualizacje {#updates}

Każde uruchomienie najpierw sprawdza wydania projektu na GitHubie (najwyżej jedno
zapytanie co kilka godzin; nigdy nie przerywa konwersji, online czy offline). Gdy wychodzi
nowsze wydanie, polecenie pyta, zanim je zainstaluje: `git clone` jest
aktualizowany przez `git pull --ff-only` (odmawia, gdy masz lokalne zmiany), a
pobrana kopia z archiwum wydania. `HEAT3D_NO_UPDATE=1` wyłącza
sprawdzanie i aktualizację.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
