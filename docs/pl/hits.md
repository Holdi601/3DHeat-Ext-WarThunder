---
title: Trafienia, ostrzał i pożary
nav_order: 13
lang: pl
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Trafienia, ostrzał i pożary {#hits-gunfire-and-fires}

Dla czytelników, którzy chcą wiedzieć, skąd biorą się kolumny trafień, amunicji i pożarów.
Sprawdzenia podają tylko metodę i zgodność.

## Ostrzał {#gunfire}

Każdy pocisk, który trafił w jednostkę, jest w replayu (komunikat 0xF0E9): wiersz `shot`
w miejscu strzelca w chwili trafienia, `targetX/Y/Z` to punkt trafienia (trafiona jednostka,
przesunięta o punkt trafienia w jej układzie, obrócona jej postawą), kierunek ku niej,
`other` to trafiona jednostka. Pociski i kule, które chybiły, nie są wysyłane: nie są
obiektami, a komunikaty o broni w locie niosą tylko rakiety, pociski kierowane, bomby i torpedy.
Naboje wystrzelone przez nagrywającego gracza (jego kolumna `ammo`) spadają przy strzelaniu,
więc da się rozpoznać jego serie, ale nie to, dokąd te naboje poszły. Ciężkie
działa przeciwlotnicze i artyleria wysyłają każdy pojedynczy strzał (`gun_shot`, bez kierunku), a
działka przeciwlotnicze 40 mm swoje serie (`fire_start`, `fire_stop`).

## Wyniki trafień {#hit-outcomes}

Przy każdym trafieniu pociskiem w jednostkę naziemną serwer wysyła do tej jednostki komunikat 0xF144
(UnitOnHit): cztery pola po jednym bajcie, czwarte to bity tego, co trafienie zrobiło
(`selfCheck.unitMessages.outcome_*`):

| Bit | Znaczenie | Dowód |
|---|---|---|
| 0x20 | własne trafienie pocisku | prawie wszystkie przychodzą z trafieniem 0xF0E9 w jednostkę w ciągu 5 ms; bez niego, z wybuchem (odłamki) |
| 0x01 | przebił (penetracja) | każdy komunikat z 0x02, 0x04 lub 0x08 też go ma |
| 0x02 | trafienie krytyczne | większość zapisów trafień krytycznych go ma, znacznie częściej niż przypadkiem |
| 0x04 | zniszczenie | większość przychodzi z zapisem zabójstwa i śmiercią jednostki w ciągu sekundy |
| 0x08 | ciężkie uszkodzenie | niektóre zapisy trafień krytycznych go mają; poza tym rzadko |

`hitOutcome` bierze najgorszy: `kill` (0x04), `critical` (0x02 lub 0x08),
`penetration` (0x01), `nonpenetration` (samo 0x20). Trafienie łączy się z
najbliższym niesparowanym 0xF144 z 0x20 jego jednostki w ciągu 5 ms. Kamera trafień
gry odróżnia odbicie od braku przebicia, ale żaden bit ani pole znalezione tutaj tego nie robi:
pierwsze trzy bajty zmieniają się od trafienia do trafienia i nie są znane.
Replaye klienta wysyłają 0xF144 tylko dla własnego samolotu nagrywającego gracza, wszystkie bity wyzerowane:
trafienia w samoloty i okręty nie mają wyniku.

## Amunicja {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Wybuchowy czy nie.** Pocisk, który eksploduje, wysyła 0xF133 (UnitOnExplosion)
  z identyfikatorem strzelca i numerem trafienia; trafienie z takim komunikatem to
  `explosive`, reszta to `kinetic`.
* **Działo i jego slot.** 0xF0BD (UnitBulletRearm) to następny załadowany nabój:
  indeks broni na liście broni pojazdu, slot amunicji i pozostałe naboje. Ładowniczego
  ręcznego przychodzi stały czas przeładowania po każdym jego trafieniu, a działka automatycznego
  ułamek sekundy po. Trafienia strzelca grupuje się wg pojazdu, sygnatury i serii; grupa należy
  do broni, gdy ta broń ładuje nabój w ciągu 20 s po połowie lub więcej jej trafień
  przy stałym opóźnieniu. `ammoSlot` to `weapon/slot`, slot załadowany
  przed trafieniem: prawdopodobnie ten, z którego strzelano, chyba że gracz zmienił
  amunicję w międzyczasie. Karabiny maszynowe nie wysyłają 0xF0BD.
* **Pocisk.** Bronią zabójstwa jest identyfikator pocisku (`125mm_3bm46`); ostatnie
  trafienie zabójcy w ofiarę przypisuje go slotowi tego strzelca, gdzie kaliber
  działa się zgadza. Jego typ i kaliber to z pliku broni
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Kaliber** reszty: broni danego slotu; grupy karabinu maszynowego to jedyny kaliber
  karabinu maszynowego, jaki może mieć jej sygnatura; w przeciwnym razie działo główne pojazdu.
  Bez instalacji (`--game`) nie ma typu, nazwy ani kalibru poza `explosive` / `kinetic`.

Nie znaleziono: odbicia. Kilka innych komunikatów niesie strzelca i numer trafienia
(0xF0C2, prawdopodobnie ścieżka kamery trafień przez pojazd; 0xF117,
0xF13C, 0xF13E); są zachowane w sidecarze, nie dekodowane. Brak przebicia pozostaje
`nonpenetration`.

## Pożary pojazdów {#vehicle-fires}

Pojazd w ogniu widzi każdy klient: serwer wysyła komunikat o obiekcie do pojazdu (zdarzenie `0a519c58`) z listą
pożarów na nim, za każdym razem, gdy lista się zmienia. Na pożar: dwa 16-bitowe
identyfikatory (drugi to węzeł modelu uszkodzeń), jego rodzaj i -1, dopóki pożar się nie
rozpali. Pożar zapalony trafieniem dostaje też komunikat z punktem, w którym się pali, w układzie
pojazdu (x przód, y góra, z lewo).

Wiersze: `fire_on`, gdy pożar pojawia się na liście, `fire_off`, gdy go nie ma,
przy pojeździe, z `fireId` (`first:node`), `fireKind` i, dla pożarów, które zapaliło
trafienie, `fireLocalX/Y/Z` (przód, góra, prawo). Gdy pojazd jest martwy, jego
lista często nie jest już wysyłana: jego pożary kończą się wraz z jego wrakiem, w przeciwnym razie z
jego obiektem, w przeciwnym razie z replayem (`selfCheck.fires`).

Sprawdzono: za każdym razem, gdy liczba gaśnic czołgu spadała, pożar znikał z jego
listy w ciągu ułamka sekundy; większość punktów pożaru leży po tej samej stronie
pojazdu co trafienie, które go zapaliło. Rodzaje są liczbami; nie wiadomo, co nazywają,
ani jaka część jest węzłem. Samoloty nie wysyłają takiej listy: samolot w ogniu nie jest odczytywany.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
