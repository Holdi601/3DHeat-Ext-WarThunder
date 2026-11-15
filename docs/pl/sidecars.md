---
title: Pliki towarzyszące i kompletność
nav_order: 8
lang: pl
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Pliki towarzyszące i kompletność {#sidecars-and-completeness}

Nic z replaya nie jest wyrzucane. To, co odczytuje konwerter, trafia do
tabeli i dokumentu meczu; wszystko inne jest zachowane w całości w trzech
plikach towarzyszących obok tabeli (w środku pliku `.3dheat` albo luźno z
`--loose`). To zasada, którą dzielą wszystkie konwertery 3DHeat:
[Konwertery zachowują wszystko](https://holdi601.github.io/3DHeat/converters.html).

## Pliki towarzyszące {#the-sidecars}

- `<match>.messages.parquet`: każdy komunikat do jednostki (czas, identyfikator komunikatu i jego nazwa, uid, eid, szablon, pojazd, jego pola identyfikujące w hex, `decoded` (co z niego odczytano, jako JSON), ładunek), każda wartość replikowanego komponentu (`name` to komponent, `fields` jego wartość), każdy komunikat obiektu (z jego numerem obiektu i klasy), każdy replikowany obiekt (`ReflectionData
  <kind>/<index>`, jego pola w hex) i każdy pakiet, którego żaden czytnik tutaj nie przyjmuje, w całości.
- `<match>.objectives.parquet`: strefy przechwytu w czasie, jeden wiersz na
  każdą zmianę, którą wysłał serwer: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (jej litera), `zoneId`, `object`, `owner` (0 brak,
  1, 2), `progress` (-100..100, dodatni w stronę drużyny 2), `x`,
  `y`, `z` strefy i wszystkie `fields` obiektu w hex (zob.
  [Cele](objectives.md)).
- `<match>.flight.parquet`: każdy wpis modelu lotu każdego samolotu w całości
  (jego bity i `phase`: bit pierwszego bajtu, od którego się zaczął), z jego
  prędkością, 14 półbajtami sterowania (`control1-3`, `throttle`), jego silnikami
  z ich stanem, dopalaczem i kondycją oraz jego nabojami na broń
  (`ammo`; `numbers` to cała lista). Wartości innych samolotów są takie, jak ostatnio odświeżono.

## Co gwarantują liczniki {#what-the-counts-guarantee}

`counts` w dokumencie meczu mówią, co replay zawierał i co się z tym stało:

| Klucz | Co to jest |
|---|---|
| `packets`, `unreadPackets` | każdy typ pakietu, jaki napotkano, i te, których żaden czytnik nie przyjmuje (zachowane w całości w pliku towarzyszącym komunikatów) |
| `messageIds`, `messageIdsNotRead` | każdy identyfikator komunikatu, jaki napotkano, i jak często, oraz te tylko zachowane, nieodczytane |
| `replicatedComponents`, `replicatedNotRead` | odczytane wartości komponentów oraz te tylko zachowane |
| `entities`, `entityTemplates`, `entityMessages` | co utworzył i wysłał strumień obiektów |
| `droppedSamples` | próbki celowo pominięte (wrak jednostki naziemnej, gdy jej obiekt zniknął), wg przyczyny |

Nic innego nie jest pomijane: element replaya albo jest odczytany do
tabeli lub dokumentu meczu, albo zachowany w całości w pliku towarzyszącym. Sekcja
`selfCheck` dokumentu meczu zawiera sprawdzenia tego, co odczytano
([Jak czytany jest replay](how-it-reads.md)).

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
