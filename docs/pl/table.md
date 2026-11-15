---
title: Tabela
nav_order: 6
lang: "pl"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabela {#the-table}

![Tabela syntetycznego replaya, w skrócie](../assets/img/table.svg)

Jeden wiersz na próbkę lub zdarzenie, 105 kolumn ([Lista kolumn](../columns.md), generowana z kodu); w stopce, w sekcji `heat3d`, instrukcje odczytu dla przeglądarki, więc przeglądarka nie potrzebuje żadnego formularza.

| Kolumna | Co to jest |
|---|---|
| `time` | sekundy na własnym zegarze replaya |
| `event` | `position`; wiersze zdarzeń leżą na torze w swoim momencie (między dwiema próbkami, na linii między nimi); `kill` (przy zabójcy), `death` (przy ofierze), `hit_critical` / `hit_severe` (przy trafionej jednostce), `module_destroyed` (przy jednostce), `launch` (przy jednostce, która zrzuciła broń), `impact` (ostatnia próbka broni, gdy została usunięta zaraz po tym); `explosion` i `flak` (0xD08E, 0xD01F) przy ich pozycji, rodzaj `effect`, bez toru, z kierunkiem eksplozji tam, gdzie go ma; `shot` (pocisk, który trafił, przy strzelcu), `gun_shot`, `fire_start`, `fire_stop` (seria działa, a nie pojazd w ogniu), `fire_on`, `fire_off` (pojazd w ogniu, zob. [Pożary pojazdów](hits.md#vehicle-fires)), `reward` (zarobione Srebrne Lwy i punkty badań, zob. [Ekonomia](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (zob. [Komunikaty do jednostek](how-it-reads.md#messages-to-units)); `despawn`: ostatni wiersz toru, którego jednostka zniknęła przed końcem replaya (zob. [Koniec toru](ground.md#end-of-a-track)) |
| `track` | to, co przeglądarka rysuje jako jedną rzecz: jedno życie jednostki albo lot jednego pocisku - `<player or vehicle> #<hex>` (przeglądarka pokazuje nazwę bez części `#`) |
| `x`, `y`, `z` | metry gry: x na wschód, y w górę, z na północ (wskazówki odbijają z, więc północ nie jest rysowana jako południe) |
| `player` | nazwa gracza; jednostka AI `<VehicleName> #<uid>` (na przykład `F-15A #204`); `uid <n>`, gdy nic jej nie nazywa; przy broni – kto ją zrzucił |
| `userId`, `team` | identyfikator Gaijin gracza i drużyna (`1`, `2`) |
| `ai`, `isPlayer` | `ai` ma wartość true dla każdej jednostki, którą nie kieruje żadne konto gracza (jednostki misji, samoloty AI, cele naziemne, działka przeciwlotnicze, okręty bez gracza, atrapy), `isPlayer` to odwrotność: gracz to jednostka, której obiekt nazywa slot gracza z identyfikatorem Gaijin. Pocisk ma tę samą wartość co jego wyrzutnia; pusta, gdy nie wiadomo |
| `match` | identyfikator meczu (`match` z dokumentu meczu), w każdym wierszu; wskazówki traktują go jako sesję, więc dwa wczytane replaye nigdy nie łączą torów |
| `life` | `uid#n`: tor jednej jednostki, cięty tam, gdzie uid przechodzi na inną jednostkę, jednostka przesuwa się szybciej, niż może (odrodzenie, ponowne uzbrojenie, gra ją przesuwa, klient poprawia odległą jednostkę; zob. Teleporty w [Jak czytany jest replay](how-it-reads.md#what-is-read-and-the-check)) albo gdy długo jej nie widać; `w<hex>` lot pocisku (`w<hex>#n` po cięciu) |
| `uid` | identyfikator jednostki w replayu |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramwaj lub wagon kolejowy postawiony przez poziom, zob. [Jednostki sceny](objectives.md#scene-units-trams-and-rail-wagons)); pociski `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` to kamera replayu nagrywającego gracza (zob. [Kamera](ground.md#the-camera)) |
| `type` | własny typ gry, tam gdzie podają go wyniki (`fighter`, `assault`, `destroyer`, `gun_boat`), w przeciwnym razie jak `kind` |
| `Vehicle` | identyfikator pojazdu w grze (`f_15a`, `germ_flakpz_I_Gepard`), do którego pasują figury przeglądarki |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | angielska nazwa pojazdu z lokalizacji Twojej instalacji (`Pz.Kpfw. III Ausf. J1`, krótka `Pz.III J1`) i jego klucz (`germ_pzkpfw_III_ausf_J_0`); znaki państw z czcionki gry są pomijane. Tam, gdzie gra nic nie nazywa albo nie znaleziono instalacji, nazwą jest identyfikator, a klucz jest pusty |
| `mission` | nazwa jednostki w misji (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | dokąd wskazuje jednostka (wektor patrzenia): samoloty z postawy z modelu lotu, jednostki naziemne i okręty z własnej, pociski wzdłuż ich lotu |
| `heading`, `pitch`, `roll` | to samo w stopniach; kurs to kompas, zgodnie z ruchem wskazówek zegara od północy, pochylenie dodatnie w górę dziobem, przechył dodatni gdy prawe skrzydło w dół (model lotu wysyła znak przeciwny, zob. [Postawa, sprawdzona](aircraft.md#attitude-checked); prawy bok jednostki naziemnej w dół). Wskazówki mówią o tym w `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | główna wieża czołgu – dokąd wskazuje działo, a nie dokąd patrzy gracz; wartość replaya przytrzymana przy prędkości napędu wieży i ustawiona na linię każdego strzału z działa głównego (zob. [Wieżyczki](ground.md#turrets)): jej obrót względem kadłuba (stopnie, zgodnie z ruchem wskazówek zegara widziane z góry dodatnie, 0 prosto przed siebie) i podniesienie działa względem kadłuba (stopnie, dodatnie w górę); `turrets` każda wieża pojazdu jako `yaw pitch;yaw pitch;...` w jego własnej kolejności (nieużywany slot ma `0.00 0.00`). Czołgi, SPAA, transportery opancerzone i ciężarówki, w replayach klienta i serwerowych; nie okręty (zob. [Wieżyczki](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | wieża główna tak, jak wysyła ją replay; `turretYaw` / `gunPitch` to ona przytrzymana przy prędkości napędu wieży i ustawiona na linię każdego strzału z działa głównego (zob. [Wieżyczki](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | dokąd gracz patrzy (celuje kamerą) w świecie: stopnie kompasu (0 północ, zgodnie z ruchem wskazówek zegara) i stopnie w górę, ta sama konwencja co `aimHeading` / `aimPitch` (w odróżnieniu od `turretYaw` / `gunPitch`, które pozostają względem kadłuba). Czołg każdego gracza w replayu serwerowym, własny nagrywającego gracza w replayu klienta; pusta tam, gdzie gracz w nic nie celuje (wszystkie cztery wartości celowania 0). Wieża za nim podąża z własną prędkością obrotu, więc obie wartości różnią się, gdy wieża się obraca (zob. [Wieżyczki](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | własny czołg nagrywającego gracza: dokąd celuje (stopnie kompasu, stopnie w górę, odległość w m; 2000, gdy w celowniku nic nie ma); wiersze kamery: dokąd celuje gracz (kurs, pochylenie) |
| `zoom` | wiersze kamery: powiększenie kamery (zob. [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` lub `SB` bitwy oraz `ground`, `air` lub `naval`, w każdym wierszu (zob. [Tryb bitwy](ground.md#battle-mode)) |
| `extrapolated` | próbka samolotu, która jest martwym liczeniem pozycji klienta, a nie stanem, który odebrał (zob. [Martwe liczenie pozycji](aircraft.md#dead-reckoning-and-the-smoother)); próbka bomby wyliczona od jej zrzutu (zob. Bomby bez zapisów lotu w [Jak czytany jest replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | o ile wygładzacz przesunął próbkę (m) oraz własna pozycja i postawa replaya (przechył w znaku tabeli) |
| `targetX`, `targetY`, `targetZ` | punkt trafienia `shot` |
| `hitOutcome`, `hitFlags` | wynik `shot` na jednostce naziemnej: `kill`, `critical`, `penetration` albo `nonpenetration` (odbił się lub został zatrzymany: replay nie odróżnia odbicia), z bitów, które serwer wysyła z trafieniem (`hitFlags`, surowe); pusta, gdy nic nie jest wysyłane (samoloty, okręty). Zob. [Wyniki trafień](hits.md#hit-outcomes) |
| `hitShell` | sygnatura pocisku `shot`: cztery bajty komunikatu trafienia (surowy hex); jedna sygnatura może oznaczać różne pociski (APFSDS 120 i 125 mm mają jedną), więc jest zachowana surowo, nie odczytana jako kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | amunicja `shot`: jej typ (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) i identyfikator (`125mm_3bm46`) tam, gdzie zabójstwo nazywa slot strzelca, w przeciwnym razie `explosive` (seria trafienia) lub `kinetic`; `weapon/slot` działa z jego przeładowań; kaliber w mm z plików broni instalacji. Zob. [Wyniki trafień](hits.md#hit-outcomes) |
| `rpm` | obroty silnika samolotu (średnia po jego silnikach) jak ostatnio wysłane, w ciągu 2 s |
| `vx`, `vy`, `vz` | prędkość samolotu tak, jak wysyła ją jego wpis lotu (m/s, osie gry; prędkości powyżej 500 m/s czytają się jako 500) |
| `engine`, `afterburner`, `engineCondition` | silniki samolotu z jego wpisu lotu: `off`, `starting`, `running`, `dead` (łączone `/`, gdy jego silniki się różnią); dopalacz 0-1; bajt wysyłany dopiero po trafieniu w silnik |
| `weaponName` | zabójstwa i zgony: broń lub amunicja w angielskiej nazwie z Twojej instalacji (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | tylko samolot nagrywającego gracza: przepustnica 0-1,1 z jego kabiny (1,1 awaryjne zasilanie bojowe lub dopalacz; w przeciwnym razie piętnaste z jego wpisu lotu), sterowanie -1..1 z jego wpisu lotu (ster wysokości dodatni przy ciągnięciu, lotki dodatnie przy przechyle w prawo), pozostałe naboje na broń (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | tylko samolot nagrywającego gracza, z jego kabiny: wskazywana prędkość i prędkość wznoszenia (m/s), paliwo, ciśnienie doładowania (atm), podwozie (0-1, 1 wysunięte), temperatura oleju i głowic cylindrów, tam gdzie jego kabina ma ten wskaźnik |
| `speed` | m/s z około dwóch sekund toru (wyliczone tutaj; replay nie wysyła prędkości dla innych jednostek) |
| `alive` | 0 dla próbek jednostki po jej śmierci (jej wraku): jednostki naziemnej lub okrętu – aż gra ją usunie albo jej próbki się skończą; samolotu – co najwyżej przez 60 s |
| `otherVehicle`, `otherLife` | ofiara `shot`: jej pojazd i jej `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | punkt trafienia `shot` w układzie własnym ofiary (m; x przód, y góra, z lewo; zob. [Komunikaty do jednostek](how-it-reads.md#messages-to-units)) i kierunek, z którego przyszedł strzał, przeliczony na ten układ wg ówczesnej postawy ofiary |
| `hitPart`, `hitFlag` | komunikat trafienia `shot`: jego słowo części tak, jak wysłane, i jego najwyższy bajt |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | ile bitwa kosztowała i ile przyniosła oraz kto wygrał: zob. [Ekonomia](economy.md) |
| `other`, `weapon` | zabójstwa: druga strona i broń; trafienia: kto trafił (z uid rekordu, w przeciwnym razie z jego slotu gracza), ich pojazd; wystrzelenia: broń; zniszczone moduły: kto ostatni trafił jednostkę w ciągu 5 s wcześniej, oraz `part <n>` |

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
