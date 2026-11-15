---
title: Cele
nav_order: 15
lang: pl
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Cele {#objectives}

`objectives` w dokumencie meczu wymienia, o co toczy się bitwa, z dwóch źródeł (`source`):

- **Replay** (`replay`): obiekty misji, które nazywa 0xD039 (strefy przechwytu `cz_circle_NN`, lotniska, lądowiska,
  bazy), umieszczone tam, gdzie teraz stawiają je replikowane obiekty rodzaju 3 (0xF02D) – strefa przechwytu zaczyna
  w miejscu swojego szablonu i na początku zostaje przesunięta do strefy tego trybu (`moved`). Numery rodzaju 3 idą wg
  kolejności 0xD039; każdy obiekt, który nie został przesunięty, leży dokładnie tam, gdzie podaje go 0xD039, co
  sprawdza kolejność. Strefa przechwytu dostaje kształt i promień obszaru misji w swoim miejscu (`area`, w granicach 2 m),
  a literę z własnego indeksu (rodzaj 5, pole 69: 0 = A); kolejność liter jest z replaya, nie sprawdzona
  względem mapy gry.
- **Misja** (`mission`): plik misji `<mission>.blk` z `mis.vromfs.bin` Twojej instalacji i szablony, które
  importuje (tylko odczyt, w czasie konwersji): jej obszary, sklasyfikowane wg nazwy – odrodzenia (numerowane punkty odrodzenia
  `..._spawnareaNN` jako jedno odrodzenie `points`), obszary bitwy, cele bombardowania (`bomb_zone`), punkty odrodzenia
  konwoju (`road_NN_spawn`), obszary wyjścia i zabójstw. Obszary innego trybu tej samej mapy (`conq_`, `dom_`, `bttl_`,
  ...) są pomijane, a z wariantów `_arcade` / `_realistic` / `_hardcore` bierze się wariant bitwy (RB bierze
  `_realistic`, w przeciwnym razie `_hardcore`, tak jak robią to skrypty misji); pomijane są też znaczniki odprawy, punkty
  działek przeciwlotniczych i obszary szersze niż 5 km (te, po których rozrzucone są odrodzenia). Każde odrodzenie podaje, ile
  tras graczy się w nim zaczęło (`used`, `usedByTeam`). Misja może losowo zamieniać strony (`randomSpawnTeams`): gdy
  odrodzenia pokazują drużyny replaya w odwrotnej kolejności, każde `team` jest zamieniane, a strona z nazwy zachowana jako
  `missionTeam`. Trasy konwojów nie są w punktach trasy misji, tak jak je odczytano; podaje się tylko, gdzie pojawiają się konwoje.

Strefy przechwytu w czasie są w pliku towarzyszącym `<match>.objectives.parquet`: replikowane obiekty rodzaju 5, po jednym
na strefę – pole 2 to jej właściciel (0, 1, 2), pole 67 postęp przechwytu, bajt ze znakiem od -100 do 100 (dodatni w stronę drużyny 2),
pole 69 to jej indeks. Sprawdzono (`selfCheck.objectives`) na naziemnych replayach serwerowych bitew Conquest i Domination: każda
zmiana właściciela idzie w parze z graczem drużyny przechwytującej, który w tym samym momencie (w granicach 1,5 s) zyskuje
`captureZone` w tablicy wyników, i z żywą jednostką naziemną tej drużyny w strefie; odrodzenia każdej bitwy pokazują
drużyny replaya tylko w jedną stronę (często odwrotnie niż `t1_` / `t2_` misji).

## Jednostki sceny: tramwaje i wagony kolejowe {#scene-units-trams-and-rail-wagons}

Poziom może umieszczać własne jednostki: obiekty `unit_loader+rail_wagon` replaya serwerowego to tramwaje z
pliku sceny poziomu (`gamedata/scenes/<level>_objects.blk` w `aces.vromfs.bin`: `setting__unit_class`, jego
transformacja i `setting__isDead`). Ich obiekty nie niosą czytelnego uid, więc tor naziemny bez obiektu jednostki,
którego pierwsza próbka leży w granicach 2 m od jednostki sceny, jest tą jednostką: jej klasą jako `Vehicle`, rodzajem `train`, typem
`tram`, `locomotive` lub `wagon`, bez drużyny; jednostka, którą scena umieszcza martwą (jak wypalone tramwaje), jest wrakiem (`alive` 0) od swojego pierwszego wiersza. Gra nie ma dla nich angielskiej nazwy; `VehicleName` to identyfikator
odczytany jako słowa („Railway tram A”). Ich pozycje nie drgają: niemal wszystkie nigdy się nie ruszają (każda
próbka identyczna co do bitu). Replay i tak wysyła je około dziesięć razy na sekundę, więc z ich próbek zachowuje się tylko te, które je
przesuwają (0,05 m lub 0,1 stopnia), i jedną co 10 s (`selfCheck.sceneUnits` liczy odrzucone próbki).
Wcześniej były to tory o nazwie `uid 8` bez pojazdu.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
