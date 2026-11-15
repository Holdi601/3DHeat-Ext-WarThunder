---
title: Fișiere auxiliare și completitudine
nav_order: 8
lang: "ro"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Fișiere auxiliare și completitudine {#sidecars-and-completeness}

Nimic dintr-un replay nu se aruncă. Ce citește convertorul intră în
tabel și în documentul meciului; tot restul este păstrat întreg în trei
fișiere auxiliare lângă tabel (în fișierul `.3dheat`, sau separat cu
`--loose`). Aceasta este regula pe care o împart toți convertoarele 3DHeat:
[Convertoarele păstrează tot](https://holdi601.github.io/3DHeat/converters.html).

## Fișierele auxiliare {#the-sidecars}

- `<match>.messages.parquet`: fiecare mesaj către o unitate (ora, id-ul și numele mesajului, uid, eid, șablon, vehicul, câmpurile sale de id în hex, `decoded` (ce se citește din el, ca JSON), conținutul), fiecare valoare de componentă replicată (`name` componenta, `fields` valoarea sa), fiecare mesaj de entitate (cu entitatea și numărul clasei sale), fiecare obiect replicat (`ReflectionData
  <kind>/<index>`, câmpurile sale în hex) și fiecare pachet pe care niciun cititor de aici nu îl preia, întreg.
- `<match>.objectives.parquet`: zonele de capturare în timp, un rând pentru fiecare schimbare trimisă de server: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (litera sa), `zoneId`, `object`, `owner` (0 niciunul,
  1, 2), `progress` (-100..100, pozitiv spre echipa 2), `x`,
  `y`, `z` ale zonei, și toate `fields` ale obiectului în hex (vedeți
  [Obiective](objectives.md)).
- `<match>.flight.parquet`: fiecare intrare a modelului de zbor a fiecărui avion, întreagă (biții săi și `phase`: bitul din primul său octet la care a început), cu viteza sa, cele 14 semiocteți de comandă (`control1-3`, `throttle`), motoarele sale cu starea lor, postardere și starea, și rundele sale pe armă
  (`ammo`; `numbers` este lista întreagă). Valorile celorlalte avioane sunt cele reîmprospătate ultima dată.

## Ce garantează numărătorile {#what-the-counts-guarantee}

`counts` din documentul meciului spun ce conținea replay-ul și ce s-a întâmplat cu el:

| Cheie | Ce este |
|---|---|
| `packets`, `unreadPackets` | fiecare tip de pachet întâlnit, și cele pe care niciun cititor nu le preia (păstrate întregi în fișierul auxiliar al mesajelor) |
| `messageIds`, `messageIdsNotRead` | fiecare id de mesaj întâlnit și de câte ori, și cele doar păstrate, nu citite |
| `replicatedComponents`, `replicatedNotRead` | valorile de componente citite, și cele doar păstrate |
| `entities`, `entityTemplates`, `entityMessages` | ce a creat și ce a trimis fluxul de entități |
| `droppedSamples` | eșantioane lăsate afară intenționat (epava unei unități terestre după ce entitatea sa a dispărut), pe motiv |

Nimic altceva nu este lăsat afară: un element al replay-ului fie este citit în
tabel sau în documentul meciului, fie este păstrat întreg într-un fișier auxiliar. `selfCheck` din
documentul meciului conține verificările a ceea ce s-a citit
([Cum citește un replay](how-it-reads.md)).

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
