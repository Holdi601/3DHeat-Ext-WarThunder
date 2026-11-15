---
title: Dokument meczu
nav_order: 7
lang: "pl"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument meczu {#the-match-document}

![Początek syntetycznego dokumentu meczu i jego klucze](../assets/img/match-document.svg)

`<match>.match.json` zawiera wszystko, co replay mówi, a co nie jest wierszem
tabeli. Karta Mecz w przeglądarce czyta właśnie ten plik.

## Bitwa {#the-battle}

| Klucz | Co to jest |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | identyfikator meczu (jak w nazwie pliku); identyfikator mapy; plik poziomu, którego używa |
| `mission`, `missionKey` | nazwa misji i jej klucz w plikach tekstowych gry |
| `battleClass`, `environment`, `weather` | tak, jak podaje je nagłówek |
| `sessionId`, `server` | identyfikator sesji bitwy; serwer |
| `replayVersion`, `flightLayout` | wersja formatu replaya; odczytany układ pakietów lotu (`2025` lub `2026`) |
| `files` | odczytane pliki replaya (jeden albo części replaya serwerowego) |
| `started`, `timePlayed`, `replayEnd` | czas startu (ISO, UTC); rozegrane sekundy, z wyników; sekundy ostatniego pakietu replaya |
| `author`, `authorUserId` | nagrywający gracz i jego identyfikator Gaijin (replaye klienta) |
| `teams` | drużyny w bitwie (`1`, `2`) |
| `result` | `winner`, `status` (`success` lub `fail`, wynik autora), `authorTeam`, `teams` ([Ekonomia](economy.md)) |
| `vehicleNames` | skąd pochodzą nazwy pojazdów (Twoja instalacja) i ich język |
| `conventions` | jednostki i znaki tabeli: osie, czas, życie, tor, alive, przechył i inne |

## Cała reszta {#everything-else}

| Klucz | Co to jest |
|---|---|
| `battle`, `difficulty`, `gameMode` | tryb bitwy: `difficulty` `AB` / `RB` / `SB` (i jego nazwa oraz bajt nagłówka), `gameMode` `ground` / `air` / `naval`, tryb misji (`Dom`, `Conq`, `Bttl`, `I2M`, ...) i jego angielska nazwa z Twojej instalacji (`Domination`, `Enduring Confrontation`), dozwolone typy jednostek (zob. [Tryb bitwy](ground.md#battle-mode)) |
| `settings` | blk misji po nagłówku: tryb, środowisko, pogoda, limity wyniku i czasu, kraje, dozwolone typy jednostek, wiatr oraz `stars` (szerokość, długość, data, czas lokalny) |
| `sky` | pierwszy `CustomWeatherParams`: kierunek słońca i księżyca, wiatr, kolory nieba, przesunięcia chmur |
| `players`, `slots` | wiersz wyników na gracza (zabójstwa, zabójstwa naziemne, zgony, asysty, wynik, przechwycenia, eskadra, klan, kraj, skład, identyfikatory, którymi kierowali); sloty graczy replaya (nazwa, identyfikator użytkownika, drużyna) |
| `units` | każdy obiekt jednostki utworzony przez replay: eid, uid, szablon, pojazd, rodzaj, typ, drużyna, gracz, nazwa z misji, kiedy utworzony i usunięty, gdzie utworzony, które komponenty nie dały się odczytać |
| `objects` | nazwane obiekty misji: strefy przechwytu i lotniska z pozycją i rozmiarem, kontury lotnisk jako punkty, obszary odrodzenia |
| `objectives` | cele bitwy, każdy z `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 lub 2 z replaya, puste dla obu), `name` (strefa przechwytu jej litera, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) z `position`, `radius` / `height` / `size` i `heading`, `source` (`replay` lub `mission`) oraz to, co jeszcze wiadomo (zob. [Cele](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | z nazwami i pojazdami obu stron; zabójstwa z angielską nazwą broni |
| `weapons` | każda rakieta, pocisk kierowany, bomba, torpeda, zbiornik odrzutowy i zrzucony ładunek: kiedy, gdzie zrzucony (pozycja, postawa, prędkość), przez którą jednostkę (najbliższą w ciągu 300 m i 1,5 s), ile próbek lotu, gdzie ostatnio widziany, kiedy usunięty |
| `explosions`, `flak` | `PlayExplosionVisual` (pozycja, kierunek, rodzaj) i `PlayFlakExplosionVisual` (pozycja) |
| `awards` | nagrody nagrywającego gracza (`TextStreak`: first_blood, serie, liczniki wyzwań) |
| `detections`, `unitStates` | pary `UnitDetected` jednostek; komunikat (0xF093) z pozycją, postawą i prędkością jednostki, którego znaczenie nie jest znane |
| `authorInstruments` | wartości kabiny nagrywającego gracza (`ReplayCockpitParams`) wg numeru wskaźnika, najwyżej jeden na sekundę; `known` nazywa każdy numer, który ten replay wysłał (nazwa, jednostka, jak sprawdzono), `notNamed` resztę |
| `scoreboard` | statystyki każdego gracza za każdym razem, gdy się zmieniły (zabójstwa, zgony, asysty, wynik, zabójstwa AI, zabójstwa okrętów, strefy, obrażenia, uniki pocisków, eskadra), oraz wynik każdej drużyny i prawdopodobne bilety w czasie (zob. [Dane odbicia](aircraft.md#reflection-data)) |
| `economy` | Srebrne Lwy i punkty badań bitwy (zob. [Ekonomia](economy.md)): sumy, na gracza, na pojazd, mnożniki, zwycięzca, sprawdzenia |
| `entityMessages` | komunikaty obiektów (0x20) wg numeru klasy: liczba, szablony celów, rozmiary |
| `chat` | każda linia czatu |
| `triggers`, `hints`, `missionProgress` | akcje skryptu misji (RunTriggerAction), jej podpowiedzi, jej komunikaty postępu |
| `camera` | pola kamery replayu nagrywającego gracza co 0,25 s, tak jak wysłane (tabela ma je jako tor) |
| `projectileHitReplays` | własne trafienia nagrywającego gracza i trafienia w niego, z bronią, amunicją i ich angielskimi nazwami |
| `results` | cały blk wyników tak, jak zapisała go gra |
| `counts` | wiersze, zdarzenia, życia, rodzaje, próbki, obiekty wg szablonu, broń, pakiety odczytane i nieodczytane, każdy identyfikator komunikatu, jaki widziano, i te nieodczytane, odrzucone próbki |
| `trackBreaks` | każde cięcie toru za krok szybszy, niż jednostka może iść: gdzie, jak daleko, jak szybko i co to najprawdopodobniej jest |
| `selfCheck` | sprawdzenia wymienione w [Jak czytany jest replay](how-it-reads.md), liczone przy każdej konwersji; `stepSpeed` podaje dla każdego rodzaju prędkość między kolejnymi wierszami toru, tak jak przeglądarka je łączy (mediana, 99. percentyl, najwyższa i kroki szybsze niż możliwe, które muszą wynosić 0) |

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
