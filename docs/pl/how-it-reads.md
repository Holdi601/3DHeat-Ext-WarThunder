---
title: Jak czytany jest replay
nav_order: 10
lang: pl
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Jak czytany jest replay {#how-it-reads-a-replay}

Ta strona jest dla osób, które chcą wiedzieć, co konwerter czyta, jak to
sprawdzono i na ile ufać każdej kolumnie. Do konwertowania replayów jej nie potrzebujesz.

Odczyt sprawdzono na replayach klienta bitew lotniczych zręcznościowych, lotniczych symulacyjnych
i morskich, na replayach serwerowych bitew naziemnych, a dla układów z 2025 roku
na publicznych przykładowych replayach
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Każde sprawdzenie porównuje wartość z czymś, co replay mówi drugą, niezależną drogą;
tutaj podano tylko metodę i zgodność.

## Co jest czytane i sprawdzenie {#what-is-read-and-the-check}

| Część | Stan i sprawdzenie |
|---|---|
| Nagłówek, mapa, misja, czas startu, sesja; wyniki | każdy plik |
| Ustawienia misji (blk po nagłówku) | tryb, pogoda, limity, `stars` (data, godzina, miejsce) |
| Strumień pakietów (zlib w 2025, zstd w 2026) | każdy pakiet ujęty w ramy |
| Pozycje i postawa samolotów (układ 2026) | 4 próbki na sekundę, żaden pakiet nieodczytany; kurs zgadza się z kierunkiem ruchu |
| Pakiety lotu wyprzedzające swój czas | po zakłóceniu sieci pakiet lotu replaya klienta czasem trzyma każdy inny samolot tam, gdzie będzie około 0,75 s później. Wyprzedzenie mierzy się dla każdego pakietu, a każdemu wyprzedzającemu samolotowi przypisuje się czas, który reprezentuje (`selfCheck.flightPacketsRetimed`) |
| Przeskoki martwego liczenia pozycji | krok z przebiegu liczonego martwo mierzy się od ostatniego odebranego stanu, więc poprawki klienta już nie tną torów ([Martwe liczenie pozycji](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporty | tor jest cięty tam, gdzie jednostka przesuwa się dalej, niż może: najpierw wg rodzaju (samoloty 750 m/s, jednostki naziemne i okręty 40 m/s, broń 1800 m/s), potem wg własnego tempa. Każde cięcie jest wypisane w `trackBreaks` z prawdopodobną przyczyną (odrodzenie, gra przesuwa gracza, poprawka odległej jednostki). Po cięciach żaden krok między wierszami toru nie jest szybszy, niż na to pozwala jego rodzaj (`selfCheck.stepSpeed`) |
| Pozycje jednostek naziemnych i okrętów (0xF073 / 0xF074) | żaden pakiet nieodczytany. Kurs, pochylenie i przechył z 16-bitowej postawy: kurs zgadza się z kierunkiem ruchu w granicach około 2 stopni (mediana); pochylenie liczy się w krokach 180/65536 stopnia; po odwróceniu znaku przechyłu kierunek działa z kadłuba i wieżyczki wskazuje na trafioną jednostkę przy niemal każdym strzale czołgu. Okręty stoją na poziomie wody |
| Wieżyczki | obrót wieżyczki i podniesienie działa czołgów: zob. [Wieżyczki](ground.md#turrets) |
| Upakowane wysokości terenu | pozycje upakowane w 64 bitach liczą wysokość od -100 m na większości poziomów, a od poziomu wody na niektórych; przesunięcie mierzy się w każdym replayu na jednostkach widzianych w obu postaciach (`selfCheck.packedGroundHeight`) |
| Strumień obiektów (tworzenie, niszczenie) | każde tworzenie odczytane. Układ pochodzi z opublikowanego kodu Dagor Engine; typy komponentów War Thunder są pomijane przez znalezienie, gdzie zaczyna się następny komponent. Pojazd i slot gracza każdej jednostki równają się tym, które podają rekordy zabójstw i trafień, dla każdego sprawdzonego rekordu |
| Kto prowadził którą jednostkę, jednostki AI, okręty, cele naziemne | ze strumienia obiektów: każda jednostka ma swój pojazd i drużynę, jednostka każdego gracza – jego samego |
| Zabójstwa względem wyników | zgony na gracza równają się wynikom; wyniki liczą więcej zabójstw, bo klient nie dostaje każdego zabójstwa. Replay, który zaczyna się po rozpoczęciu bitwy, zawiera tylko zabójstwa po tym momencie |
| Zabójstwa, trafienia krytyczne, poważne uszkodzenia | każdy plik |
| Zniszczone moduły (0xF118) | jednostka i numer części; nazwa części wymaga modelu uszkodzeń pojazdu, którego nie ma w replayu |
| Zrzucona broń (strumień obiektów) | punkt zrzutu leży około 10-20 m (mediana) od najbliższej jednostki, którą uznaje się za wyrzutnię |
| Broń w locie (0xF0DB) | pociski kierowane, rakiety i bomby, każda przypisana do swojego obiektu |
| Bomby bez zapisów lotu | bomba bez nich ma swój upadek wyliczony od zrzutu do uderzenia (grawitacja i opór, próbka co 0,1 s, `extrapolated` ma wartość true). Sprawdzono nad morzem, gdzie wysokość uderzenia jest znana: wyliczone upadki kończą się w granicach około 15 m od wody. W dokumencie meczu taka broń ma `ballisticImpact`; `counts.bombsBallistic` je liczy |
| Sloty graczy, czat | każdy plik |
| Eksplozje, serie artylerii przeciwlotniczej, nagrody, wykrycia, pogoda, obiekty misji | odczytane; pozycje sprawdzone na oko w przeglądarce |
| Wskaźniki nagrywającego gracza (0xD04A) | nazwane według tego, co robią: [Wskaźniki w kabinie](aircraft.md#cockpit-instruments); reszta w `notNamed` |
| Inne pola wpisów lotu | prędkość, naboje, sterowanie, silniki: [Wpisy lotu](aircraft.md#flight-entries) |
| Postawa w wierszach zdarzeń | każdy wiersz zdarzenia niesie kurs, pochylenie, przechył i wektor patrzenia jednostki w tej chwili |
| Statystyki graczy i wyniki drużyn | na końcu bitwy każda statystyka równa się wynikom dla każdego gracza: [Dane odbicia](aircraft.md#reflection-data) |
| Nazwy broni i pojazdów | z angielskiej lokalizacji Twojej instalacji; kilka domyślnych pasów okrętów i radarów lotnisk nie ma nazwy w grze |
| Gracze i AI | żaden wiersz gracza z wyników nie jest AI, każdy wiersz nie-AI jest graczem z wyników (`selfCheck.identity`) |
| Wraki | próbki jednostki po jej śmierci nadal napływają; wrak jednostki naziemnej lub okrętu ma `alive` 0, dopóki jego obiekt nie zostanie usunięty, i pozostaje jednym torem; samoloty mają `alive` 0 najwyżej przez 60 s (`selfCheck.wrecks`) |
| Zmiany pojazdu | jednostka gracza wciąż żywa, gdy pojawia się następna jednostka tego samego gracza, jest tam kończona (pojazd pozostawiony na polu). `selfCheck.vehicleSwitch.twoLiveVehicles` musi wynosić 0 |
| Tryb bitwy | [Tryb bitwy](ground.md#battle-mode) |
| Samoloty w replayu serwerowym z 2026 | odczytane w układzie 2026; kurs i znak przechyłu zgadzają się z zakrętami; atrapy samolotów i drony rozpoznawcze nie niosą danych |
| Gracze replaya serwerowego | znalezieni po nazwie w slotach; każda statystyka równa się wynikom (`selfCheck.players`) |
| Samoloty w replayach serwerowych z 2025 i wersji 101286 | nieodczytane: ich pakiety lotu mają inny układ |

## Komunikaty do jednostek {#messages-to-units}

Każdy pakiet typu 4 to komunikat mpi daNet z Dagor Engine: identyfikator obiektu
adresata, a potem (gdy jego 11 niskich bitów są wszystkie ustawione) rozszerzony UID obiektu,
identyfikator komunikatu i ładunek. Komunikat do jednostki niesie jako rozszerzony UID
identyfikator obiektu jednostki, `index << 10 | generation`. Sprawdzono: każdy taki
komunikat wskazuje obiekt żywy w tej chwili.

Dla specjalistów komunikaty odczytują się tak:

| Komunikat | Co, i sprawdzenie |
|---|---|
| 0xF0E9 UnitHitEffects | trafienie jednym pociskiem: identyfikator strzelca i punkt trafienia w układzie jednostki (x przód, y góra, z lewo): centymetry dla samolotów i okrętów, 20/32768 m na krok dla jednostek naziemnych (dopasowane do rozmiaru wież czołgów). `hitLocalX/Y/Z` w metrach. Staje się wierszem `shot` ([Ostrzał](hits.md#gunfire)). Strzelec niemal każdego rekordu trafienia i zabójstwa jest wśród tych strzelców; punkty trafień leżą po stronie zwróconej do strzelca |
| 0xF133 UnitOnExplosion | ten sam identyfikator strzelca |
| 0xF04B OnUnitDead | wiersze `dead`: ofiara każdego rekordu zabójstwa ma jeden w ciągu 2 s |
| 0xD047 FmwRpm | obroty silników (`rpm`); zgadza się ze wskaźnikiem obrotów w kabinie |
| 0xF0B1, 0xF0A0 | wiersze `gun_shot`: pojedyncze strzały ciężkiej artylerii przeciwlotniczej i artylerii |
| 0xF01B, 0xF01C | wiersze `fire_start`, `fire_stop`: serie działek przeciwlotniczych 40 mm (działo strzela; pożar pojazdu to `fire_on`, zob. [Pożary pojazdów](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | wiersze `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | własne trafienia nagrywającego gracza i trafienia w niego, z bronią i amunicją, nazwane z instalacji (`projectileHitReplays`) |
| 0xF13E, 0xF031 | efekt wizualny trafienia i efekt odtworzony na jednostce; przychodzą z trafieniem w tę samą jednostkę |
| 0xD041 | jeden na każde działo obronne samolotu, dwa razy na sekundę; jego indeksy zgadzają się z bronią strzelców z modelu lotu |
| 0xD048, 0xF117 | układ odczytany, znaczenie nieznane |
| reszta (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | w sidecarze komunikatów z ich jednostką i polami |

Nazwy pochodzą od społeczności (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Także odczytane {#also-read}

- **Replikacja strumienia obiektów** (0x22, 0x23): na obiekt blok wartości komponentów: czasomierze
  napraw okrętów, liczniki materiałów eksploatacyjnych, zmiany właściciela i drużyny, przegrzanie silnika. Liczone w `counts.replicatedComponents`; wartości w sidecarze komunikatów.
- **Akcje skryptu misji** (0xF028) i **podpowiedzi** (0xF0EC): `triggers`,
  `hints`. **Postęp misji** (0xF07A, 0xF07C): `missionProgress`.
- **Kamera replayu** (0xD043): zob. [Kamera](ground.md#the-camera).

## Nieodczytane i dlaczego {#not-read-and-why}

- **Nazwy i treść komunikatów obiektów** (0x20, 0x21): numer klasy to miejsce na liście
  skompilowanej w grze, nie jest wysyłany i nie ma go w jej danych. Dwa są odczytane (pożary pojazdu i jego gaśnice); reszta jest
  zachowana w całości wraz z obiektem i numerem klasy.
- **Inne replikowane obiekty** (rodzaje inne niż sloty graczy i drużyny): odczytane i zachowane,
  bez nazw; nie ma w wynikach nic, z czym można by je sprawdzić.
- **Sterowanie, przepustnica i naboje innych samolotów**: odświeżane tylko od czasu do czasu; trzymane w sidecarze lotu, nie w tabeli.
- **Pożary samolotów**: nie znaleziono ich w żadnym komunikacie; samolot w ogniu nie ma wiersza `fire_on`.
- **Nazwy zrzuconej broni**: obiekt bomby lub rakiety nie niesie nazwy; rekordy zabójstw nazywają broń zabójstwa.
- **Pociski, które chybiły**: replay zawiera tylko trafienia.

`counts.messageIdsNotRead` i `selfCheck` każdego dokumentu meczu mówią, co zawiera
nowy replay i jak dobrze został odczytany.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
