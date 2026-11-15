---
title: Konwertowanie replayów
nav_order: 4
lang: pl
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konwertowanie replayów {#converting-replays}

Wynik: jeden plik `.3dheat` na bitwę (domyślnie) albo osobne pliki z
`--loose`.

## Krok po kroku {#step-by-step}

1. **Włącz zapisywanie replayów.** War Thunder zapisuje replaye klienta w folderze
   `Replays` gry, gdy zapisywanie replayów jest włączone w jej opcjach, na przykład
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Replay serwerowy zapisany ze strony replayów gry (archiwum zip z `0000.wrpl`,
   `0001.wrpl`, ...) też można przekonwertować.
2. **Otwórz terminal** w folderze, do którego mogą trafić wyniki
   ([Zanim zaczniesz](before-you-start.md)).
3. **Konwertuj:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   Folder `out` powstaje w folderze, w którym jest terminal.
4. **Przeczytaj, co pisze.** Powinieneś zobaczyć jedną linię na bitwę.
5. **Otwórz wynik:** wczytaj `out/<map>/<match>.3dheat` w przeglądarce 3DHeat
   ([Wczytywanie jednego pliku](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Przebieg na syntetycznym replayu: jeden .3dheat, --loose, uszkodzony plik, pusty folder](../assets/img/convert.svg)

Obrazek to przebieg na replayu, który testy budują w kodzie (bez prawdziwego
replaya i bez instalacji gry):

- `ok <file>`: bitwa przekonwertowana (z `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: plik, którego nie udało się odczytać (status wyjścia 1;
  pozostałe są nadal konwertowane);
- `no .wrpl files given`: nic do konwersji (status wyjścia 2);
- `note: ...`: na przykład że nie znaleziono instalacji War Thunder, z której
  nazwano by pojazdy.

## Opcje {#options}

| Opcja | Domyślnie | Działanie |
|---|---|---|
| `replays` (jeden lub więcej) | - | pliki `.wrpl`, foldery z nimi (sam folder, nie jego podfoldery) albo ich archiwa zip (replay serwerowy: jego części `.wrpl` są rozpakowywane do folderu tymczasowego) |
| `-o`, `--out` | wymagana | dokąd zapisywać: folder na każdą mapę w środku |
| `--game FOLDER` | znajdowany | folder War Thunder, którego tekst nazywa pojazdy, uzbrojenie i amunicję, a tabele wyceniają [ekonomię](economy.md); także `HEAT3D_WT_GAME` |
| `--no-smoothing` | wyłączona | zachowaj próbki innych jednostek z martwego liczenia pozycji i odebrane tak, jak są w replayu ([Martwe liczenie pozycji](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | włączona | spakuj każdą bitwę w jeden plik `.3dheat` |
| `--loose` | wyłączona | zachowaj każdą bitwę jako osobne pliki (tabela, dokument meczu, pliki towarzyszące) |
| `--version` | - | wypisz `heat3d-wt-replay <version>` i zakończ |
| `-h`, `--help` | - | wypisz opcje i zakończ |

Bitwa przekonwertowana ponownie zapisze się ponownie. Opcje tak, jak wypisuje
je program: [Opis poleceń](../cli-reference.md).

## Które pliki to jedna bitwa {#which-files-are-one-battle}

Każda bitwa staje się jednym plikiem
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
i SB to skróty gry dla bitew zręcznościowych, realistycznych i symulacyjnych;
`<mode>` to tryb misji tak, jak gra go oznacza (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; zob.
[Tryb bitwy](ground.md#battle-mode)); każda część jest pomijana, gdy replay
jej nie podaje. Części replaya serwerowego (`0000.wrpl`, `0001.wrpl`, ...)
są czytane razem jako jedna bitwa; replay klienta i części serwera tej samej
bitwy to dwa nagrania i zostają dwoma.

## Status wyjścia {#exit-status}

`0`, gdy każda bitwa została przekonwertowana; `1`, gdy któraś się nie udała
(pozostałe są nadal konwertowane); `2`, gdy wśród argumentów nie znaleziono
żadnego pliku replaya.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
