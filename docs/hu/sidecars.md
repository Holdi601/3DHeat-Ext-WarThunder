---
title: "Kísérőfájlok és teljesség"
nav_order: 8
lang: "hu"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Kísérőfájlok és teljesség {#sidecars-and-completeness}

A visszajátszásból semmi sem vész el. Amit a konvertáló beolvas, az a táblázatba és a
meccsdokumentumba kerül; minden más egészben megmarad három kísérőfájlban a táblázat mellett
(a `.3dheat` fájlon belül, vagy külön a `--loose` kapcsolóval). Ez az a szabály, amelyet
minden 3DHeat-konverter közösen követ:
[A konverterek mindent megtartanak](https://holdi601.github.io/3DHeat/converters.html).

## A kísérőfájlok {#the-sidecars}

- `<match>.messages.parquet`: minden egységnek szóló üzenet (idő, üzenetazonosító és név, uid,
  eid, sablon, jármű, azonosító-mezői hexadecimálisan, `decoded` (az, amit beolvastunk belőle,
  JSON-ként), a tartalom), minden replikált komponensérték (`name` a komponens, `fields` az értéke),
  minden entitásüzenet (az entitásával és osztályszámával), minden replikált objektum
  (`ReflectionData <kind>/<index>`, a mezői hexadecimálisan), és minden csomag, amelyet egyik
  olvasó sem vesz át, egészben.
- `<match>.objectives.parquet`: az elfoglalható zónák időbeli alakulása, soronként egy változás, amelyet
  a szerver küldött: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone`
  (a betűjele), `zoneId`, `object`, `owner` (0 nincs, 1, 2), `progress` (-100..100, pozitív a 2.
  csapat felé), a zóna `x`, `y`, `z` értékei, és az objektum minden `fields` mezője hexadecimálisan
  (lásd [Célok](objectives.md)).
- `<match>.flight.parquet`: minden repülőgép minden repülési modell-bejegyzése egészben (a bitjei, és a
  `phase`: az első bájtjának az a bitje, amelyiknél kezdődött), a sebességével, a 14 vezérlő nibble-jével
  (`control1-3`, `throttle`), a motorjaival az állapotukkal, az utánégetőjükkel és az állapotukkal, és
  fegyverenként a lőszerükkel (`ammo`; a `numbers` a teljes lista). Más repülőgépek értékei az utolsó
  frissítés szerintiek.

## Mit garantálnak a számlálók {#what-the-counts-guarantee}

A meccsdokumentum `counts` mezője megmondja, mit tartalmazott a visszajátszás, és mi lett vele:

| Kulcs | Mi |
|---|---|
| `packets`, `unreadPackets` | minden csomagtípus, amely előfordult, és azok, amelyeket egyik olvasó sem vesz át (a kísérőfájl üzeneteiben egészben megőrizve) |
| `messageIds`, `messageIdsNotRead` | minden üzenetazonosító, amely előfordult, és hányszor, valamint azok, amelyek csak megtartva vannak, nincsenek olvasva |
| `replicatedComponents`, `replicatedNotRead` | beolvasott komponensértékek, és azok, amelyek csak meg vannak tartva |
| `entities`, `entityTemplates`, `entityMessages` | amit az entitásfolyam létrehozott és küldött |
| `droppedSamples` | szándékosan kihagyott minták (egy földi egység roncsa, miután az entitása már nincs meg), okonként |

Más nem marad ki: a visszajátszás minden eleme vagy beolvasásra kerül a táblázatba vagy a
meccsdokumentumba, vagy egészben megmarad egy kísérőfájlban. A meccsdokumentum `selfCheck` mezője
tartalmazza a beolvasott adatok ellenőrzéseit ([Hogyan olvassa a visszajátszást](how-it-reads.md)).

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
