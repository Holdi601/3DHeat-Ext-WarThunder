---
title: Samoloty
nav_order: 11
lang: "pl"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Samoloty {#aircraft}

Dla czytelników, którzy chcą wiedzieć, skąd biorą się kolumny samolotów i na ile im ufać. Każde
sprawdzenie poniżej porównuje wartość z czymś, co replay mówi drugą, niezależną drogą;
podano tylko metodę i zgodność.

## Wskaźniki w kabinie {#cockpit-instruments}

Komunikat 0xD04A wysyła wskazania przyrządów nagrywającego gracza jako pary (numer, wartość):
cztery na sekundę w bitwach zręcznościowych, tylko zmienione wartości w bitwach symulacyjnych. Numery tworzą jedną listę dla wszystkich kabin, a kabina wysyła
te wskaźniki, które ma jej model. Kod gry określa, który numer to który wskaźnik,
więc każdy numer nazwano według tego, co robi, i sprawdzono z replayem
(`convert.INSTRUMENTS` trzyma wynik; nic nie jest czytane z instalacji):

| Numer | Nazwa | Sprawdzono z |
|---|---|---|
| 0 | wskazywana prędkość, m/s | prędkość toru poprawiona o gęstość powietrza: korelacja 0,99 |
| 39 | prędkość wznoszenia, m/s | prędkość wznoszenia toru: korelacja powyżej 0,99 |
| 40, 41 | wysokość, m; wysokość modulo 1000 | wysokość toru, z dokładnością kilku metrów |
| 52, 53 | przechył i pochylenie sztucznego horyzontu | minus przechył i pochylenie tabeli, różnica poniżej 1 stopnia |
| 64 | kompas | kierunek tabeli, różnica poniżej 0,1 stopnia |
| 15-20 | pedały steru kierunku | siła boczna działająca na samolot |
| 23, 31 | drążek: ster wysokości i lotki (znak jak w modelu kabiny) | kąt natarcia; prędkość przechyłu |
| 69, 71, 73 | zegar: godziny (tarcza 12-godzinna), minuty, sekundy | lokalny czas komputera nagrywającego, co do minuty |
| 75 | ciśnienie doładowania, atm | wyższe przy awaryjnym zasilaniu bojowym niż przy pełnym gazie |
| 81-86, 87-92, 93-98 | obroty na silnik, obroty modulo 1000, wskaźnik obrotów | siebie nawzajem dokładnie; obroty silnika: korelacja powyżej 0,97 |
| 195 | paliwo | spada w trakcie lotu, znów pełne po odrodzeniu |
| 228-230 | nogi podwozia, 1 wysunięte | wysunięte tylko w pobliżu wysokości lotnisk i przy prędkości lądowania |
| 240, 241 | przepustnica na silnik (1,1 awaryjne zasilanie bojowe lub dopalacz) | przepustnica z wpisu lotu |
| 330-332, 346-348 | liczniki amunicji (dwa jednakowe zestawy) | liczba naboi zestawu uzbrojenia, malejąca wraz z liczbą naboi z wpisu lotu |
| 135, 159 | temperatura oleju i głowic cylindrów | prawdopodobnie: rosną w trakcie lotu |
| 58, 61 | kulka ślizgu, wskazówka zakrętu | prawdopodobnie: podążają za siłą boczną i prędkością skrętu |
| 223 | hamulec aerodynamiczny | prawdopodobnie: ustawiany tylko przy podejściu |
| 490-497, 500-505 | hamulce kół | prawdopodobnie: ustawiane tylko przy stojącym na lotnisku |

Wysyłanych jest jeszcze kilka numerów, których znaczenie nie jest znane; są
zachowane w `authorInstruments.notNamed` dokumentu meczu.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` i `throttle` w tabeli pochodzą z tych wskaźników, w wierszach
samego nagrywającego gracza, biorąc ostatni komunikat najwyżej 0,2 s po próbce.

## Wpisy lotu {#flight-entries}

Wpis lotu każdego samolotu (typ pakietu 2) niesie, oprócz pozycji
i postawy:

- **Prędkość**: 32-bitowe słowo po postawie. Bity 31, 30 i 29 to znaki x, y i z;
  potem prędkość w 11 bitach po 500/2047 m/s (zatrzymuje się na
  500 m/s), potem |x| i |y| jako ułamki prędkości, po 9 bitów każdy, a z to
  wartość, która czyni wektor wektorem jednostkowym. Sprawdzono to z krokiem między
  odebranymi próbkami: kierunek zgadza się w ułamku stopnia dla
  nagrywającego gracza i w granicach około 2 stopni dla wszystkich innych;
  prędkość w granicach 0,2 %. `selfCheck.flightEntries`.
- **Naboje na broń**: lista przed pozycją, jeden element na broń,
  najpierw pozostałe naboje. U nagrywającego gracza równa się licznikom kabiny
  o jeden takt później, dla niemal każdej próbki.
- **Sterowanie i przepustnica**: 7 bajtów po prędkości, czytane jako 14 półbajtów.
  Dla nagrywającego gracza, w każdym takcie: 1 ster wysokości, 2 lotki, 3
  ster kierunku (8 w spoczynku), 11 przepustnica w piętnastych (15 także dla
  awaryjnego zasilania bojowego i dopalacza), 4 hamulce kół, 5 hamulec aerodynamiczny, 8
  prawdopodobnie spadochron hamulcowy. Półbajty innych samolotów zmieniają się tylko kilka razy
  w bitwie i nie są ich sterowaniem w danej chwili.
- **Silniki**: na silnik bajt stanu (0 wyłączony; 1-6 uruchamianie; 7 pracuje;
  8 martwy), wartość 16-bitowa tylko przy dopalaczu (32767 pełne) i bajt
  dopiero po trafieniu w silnik. Większość samolotów, których silnik przechodzi w stan „martwy”, jest
  zestrzelona albo kończy w ciągu minut.

## Dane odbicia {#reflection-data}

Komunikaty 0xF02D i 0xF0AA replikują ponumerowane obiekty gry: dla każdego obiektu
jego identyfikator (5 górnych bitów to rodzaj, 11 niskich to indeks) i tabela pól.
Rodzaj 14 to sloty graczy (pole 2 to identyfikator użytkownika i nazwa, 9 to drużyna),
rodzaj 15 to drużyny (indeks 1 i 2):

- Pole 39 slotu gracza trzyma jego statystyki w stałych miejscach: zabójstwa (przesunięcie 0), zabójstwa
  w drużynie (2), zgony (4), zabójstwa okrętów (10), zabójstwa AI (12), zabójstwa
  naziemne AI (14), asysty (20), strefy przechwycone (22), obrażenia w strefach (24, 32-bitowe),
  nagroda za obrażenia (40, 32-bitowe), uniki pocisków (50). Pole 38 zaczyna się od
  wyniku, pole 42 to eskadra. Na końcu bitwy każda wartość równa się
  wartości z wyników dla każdego gracza (`selfCheck.scoreboardVsResults`). Gdzie przechowywane są
  zabójstwa naziemne, nie jest znane.
- Pole 7 drużyny to jej wynik: na końcu równa się sumie wyników jej
  graczy z wyników. Pole 3 prawdopodobnie to jej bilety.
- Każdy komunikat wysyła tylko pola, które się zmieniły, więc `scoreboard` w dokumencie meczu
  wypisuje statystyki każdego gracza i wynik każdej drużyny przy każdej zmianie.

## Martwe liczenie pozycji i wygładzanie {#dead-reckoning-and-the-smoother}

Replay klienta zapisuje każdy samolot cztery razy na sekundę, tak jak klient go rysował. Między
aktualizacjami, które klient odbiera dla odległego samolotu, klient przesuwa go dalej wzdłuż jego ostatniej prędkości i obraca go
z jego ostatnimi prędkościami obrotu, a przy następnej aktualizacji przeskakuje go na miejsce. Czytany
tak, jak jest, tor biegnie prosto, a potem skacze. Nic we wpisie lotu nie oznacza, które próbki
zostały odebrane; próbkę liczoną martwo rozpoznaje się po tym, czym jest: kontynuuje prostą
linię dwóch poprzednich próbek, w ich tempie, z dokładnością do 3 cm.

Ile to ma znaczenia, zależy od bitwy: w bitwach zręcznościowych około połowa
próbek innych samolotów może być liczona martwo, w bitwach symulacyjnych
tylko kilka procent. Wygładzacz obcina skoki powyżej 15 g mniej więcej pięciokrotnie
(`selfCheck.deadReckoning`). Własny samolot nagrywającego gracza nie jest
ekstrapolowany przez klienta i zostaje taki, jaki jest.

Domyślnie (`--no-smoothing` to wyłącza) tory wszystkich jednostek poza własną jednostką nagrywającego gracza
są ustawiane tam, gdzie mówią odebrane stany: próbka liczona martwo idzie krzywą przez odebrane
próbki przed nią i za nią, każda z własną prędkością; na dłuższym odcinku niż 3 s prosta
linia jest tylko zginana w stronę następnej odebranej próbki, więc żadna próbka nie przesuwa się
dalej niż własne przeskoczenie klienta. Jego postawa jest obracana równomiernie od jednej
odebranej postawy do następnej. Odebrane próbki są wygładzane co najwyżej o 2 m
albo 0,04 s ich prędkości; ustalony zakręt zostaje taki, jaki jest. Wartości samego replaya
zostają w kolumnach `Raw`.

## Postawa, sprawdzona {#attitude-checked}

Przy własnym samolocie nagrywającego gracza kierunek lotu (kurs) mieści się w granicach stopnia
(mediana) od kierunku ruchu, pochylenie w granicach kilku stopni od kąta wznoszenia,
a w wyraźnych zakrętach przechył ma znak zakrętu przy niemal każdej
próbce: przechył z modelu lotu to lewe skrzydło w dół jako dodatni, a tabela
zamienia go na prawe skrzydło w dół jako dodatni (`selfCheck.aircraftAttitude`).
Kąty 10-bitowe skaczą co 0,18 stopnia. Postawę jednostek naziemnych sprawdza się
przez ich strzały ([Wieżyczki](ground.md#turrets)).

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
