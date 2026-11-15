---
title: Jednostki naziemne i kamera
nav_order: 12
lang: "pl"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Jednostki naziemne i kamera {#ground-units-and-camera}

Dla czytelników, którzy chcą wiedzieć, skąd biorą się kolumny wieżyczki, kamery i trybu bitwy
i na ile im ufać. Sprawdzenia podają tylko metodę i zgodność.

## Wieżyczki {#turrets}

Stan naziemny czołgu (postawa 16-bitowa) zawiera po pozycji 141 nieodczytanych bitów,
a potem dla każdej wieżyczki 62 bity: kąt obrotu wieżyczki i kąt podniesienia
działa (po 16 bitów, 360/65536 stopnia na krok, ze znakiem) i 30 nieodczytanych bitów; potem dopełnienie,
a w niektórych stanach jeszcze 200 bitów. Liczbę wieżyczek podaje bajt wysłany
przed stanem. Stan, którego długość się nie zgadza, nie daje wieżyczek (jednostki
statyczne wysyłają krótszy stan). Obrót jest względem kadłuba, dodatni zgodnie
z ruchem wskazówek zegara, 0 prosto przed siebie; podniesienie względem kadłuba, dodatnie w górę.

Jak to sprawdzono:

- **Względem strzałów:** przy każdym trafieniu czołgu kierunek w świecie jego głównego działa
  (postawa kadłuba obrócona o obrót wieżyczki i podniesienie działa) porównano z
  linią od strzelca do trafionej jednostki, co najmniej 30 m dalej: w bitwie mediana około 98 %
  w granicach 3 stopni w kierunku i 99 % w podniesieniu (`selfCheck.turretsVsShots`). Reszta to przeważnie
  trafienia karabinem maszynowym z innej wieżyczki.
- **Względem celowania gracza nagrywającego:** jego własny czołg wysyła kąt celowania w świecie
  (przeciwnie do wskazówek zegara, od wschodu), podniesienie i odległość. Kierunek kadłuba
  plus obrót wieżyczki mieści się w pół stopnia (mediana) od celowania.

**Replaye serwerowe** (0xF074) wysyłają stan każdego czołgu w tym samym układzie,
a za nim dane własne, więc czytana jest każda wieżyczka, której dwa kąty leżą w obrębie
stanu (przy niemal każdym wierszu czołgu co najmniej główna). To wieżyczka, nie kamera:

- **Względem strzałów**, jak wyżej: w bitwie ponad 90 % w granicach 3 stopni w kierunku i 99 % w podniesieniu.
- **Względem widoku:** replay serwerowy wysyła celowanie każdego gracza
  (`viewYaw`, `viewPitch`). Wieżyczka podąża za widokiem w granicach pół stopnia
  (mediana), ale obraca się znacznie wolniej niż widok się porusza, tak jak robi to napęd wieżyczki
  (`selfCheck.turretVsView`).
- **Ale nie zawsze z prędkością napędu:** próbka po próbce wartość wysłana
  czasem skacze na celowanie, gdy celowanie jest blisko działa, szybciej niż jakikolwiek napęd się obraca.

Tabela trzyma więc wieżyczkę **przytrzymaną przy jej napędzie**: `turretYaw` /
`gunPitch` zbliżają się do wartości wysłanej nie szybciej niż z prędkością obrotu głównego działa
z pliku pojazdu z Twojej instalacji (razy 1.3 za umiejętności załogi i modyfikacje; 45 i 20 stopni na sekundę tam, gdzie instalacja
nie podaje żadnej). Przy każdym trafieniu głównego działa wieżyczka jest ustawiana dokładnie na
linię strzału, a przebieg wsteczny doprowadza ją tam na czas (`selfCheck.turretLimit`).
Wiersz `shot` niesie także `turretYaw` / `gunPitch`. Wartość wysłana
pozostaje w `turretYawRaw` / `gunPitchRaw`. Czołg, którego stan nie zawiera
wieżyczki, ma puste kolumny wieżyczki (przeglądarka może wrócić do `viewYaw`).
`gunPitch` leży trochę powyżej `viewPitch` na dystansie: to podniesienie działa na spadek pocisku.

Stany okrętów mają inny układ; ich wieżyczek się nie czyta. Samoloty nie wysyłają
kierunku głowy ani widoku; komunikat 0xD020 dział przeciwlotniczych pozostaje nieodczytany.

## Kamera {#the-camera}

Komunikat 0xD043, około 20 na sekundę, to kamera replayu samego nagrywającego gracza:
pole 1 to kwaternion obracający przód kamery w stronę, w którą patrzy; 2 to miejsce kamery
względem pojazdu, za którym podąża (m); 4 to to samo przesunięcie w układzie własnym pojazdu (x przód, y góra,
z lewo); 5 to miejsce, w które gracz celuje (wektor jednostkowy); 3 to zoom (około 1,2 w widoku zza czołgu,
około 1,0 w samolocie, więcej w celowniku strzelca lub przez lornetkę).
Sprawdzono: pole 4 to pole 2 obrócone do układu pojazdu, w granicach 0,5 m
dla niemal każdego komunikatu; przód kamery ma kierunek celowania. Replay nie wysyła pola widzenia w stopniach,
tylko zoom.

Tabela ma kamerę jako osobny tor: rodzaj `camera`, tor
`<player> camera #ca`, wiersz co najwyżej co 0,1 s, w miejscu śledzonego pojazdu plus pole 2,
patrzący wzdłuż kwaternionu (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), z `zoom`, `aimHeading` i `aimPitch` oraz `otherLife`,
czyli życiem, które śledzi. `selfCheck.camera` liczy wiersze i sprawdzenie.

## Koniec toru {#end-of-a-track}

Tor rysuje się od pierwszego wiersza do ostatniego. Gdy jego jednostka zniknie
przed końcem replaya, jego ostatni wiersz to wiersz `despawn` w jego ostatnim miejscu:
w czasie, gdy gra usunęła jego obiekt (gdy to nastąpiło w ciągu 6 s od jego
ostatniej próbki), w przeciwnym razie przy jego ostatniej próbce. Tor bez takiego wiersza trwa do końca
replaya. Wiersze jednego toru mogą być daleko od siebie (odległa jednostka albo wrak
odświeża się co kilka sekund, a wrak czasem nie przez minuty): jego ostatni
stan obowiązuje do następnego wiersza.

## Tryb bitwy {#battle-mode}

Bajt nagłówka pod przesunięciem 688 niesie trudność w czterech niskich bitach:
0 zręcznościowa (AB), 5 realistyczna (RB), 10 symulacyjna (SB). Sprawdzono to na
typach bitew, o których wiadomo było, jakie były replaye. Tryb gry to `ground`, gdy
misja pozwala pojawiać się czołgom, w przeciwnym razie `naval`, gdy pozwala na okręty, w przeciwnym razie `air`
(`allowedUnitTypes`); własny tryb misji pochodzi z jej klucza
(`missions/_Dom`), nazwany z `lang/missions_versus.csv` Twojej instalacji. Ten sam
klucz to część `<mode>` nazw plików i identyfikatora meczu (`Conq4`,
`Dom`), pomijana tam, gdzie nagłówek go nie ma.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
