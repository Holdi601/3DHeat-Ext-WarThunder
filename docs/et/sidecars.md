---
title: Lisafailid ja täielikkus
nav_order: 8
lang: "et"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Lisafailid ja täielikkus {#sidecars-and-completeness}

Kordusest ei visata midagi ära. See, mida konverter loeb, läheb tabelisse ja mängu
dokumenti; kõik muu hoitakse tervena kolmes lisafailis tabeli kõrval (`.3dheat`
faili sees või lahtisena valikuga `--loose`). See on reegel, mida jagavad kõik 3DHeati
konverterid: [Konverterid hoiavad kõike](https://holdi601.github.io/3DHeat/converters.html).

## Lisafailid {#the-sidecars}

- `<match>.messages.parquet`: iga sõnum üksusele (aeg, sõnumi ID ja nimi, uid, eid,
  mall, sõiduk, selle ID-väljad kuueteistkümnendsüsteemis, `decoded` (mis sellest
  loetakse, JSON-ina), sisu), iga replikeeritud komponendi väärtus (`name` komponent,
  `fields` tema väärtus), iga olemi sõnum (koos oma olemi ja klassi numbriga), iga
  replikeeritud objekt (`ReflectionData <kind>/<index>`, tema väljad kuueteistkümnendsüsteemis)
  ning iga pakett, mida ükski siinne lugeja ei võta, tervena.
- `<match>.objectives.parquet`: vallutussoonid ajas, üks rida iga muudatuse kohta, mille
  server saatis: `time`, `event` (`state`, `progress`, `captured`, `neutralised`),
  `zone` (tema täht), `zoneId`, `object`, `owner` (0 pole, 1, 2), `progress`
  (-100..100, positiivne meeskonna 2 poole), soone `x`, `y`, `z` ja objekti kõik `fields`
  kuueteistkümnendsüsteemis (vt [Eesmärgid](objectives.md)).
- `<match>.flight.parquet`: iga lennuki iga lennumudeli kirje tervena (tema bitid ja
  `phase`: selle baidi bit, millest see algas), koos kiiruse, 14 juhtimisnibbliga
  (`control1-3`, `throttle`), oma mootorite ja nende olekuga, järelpõletaja ja
  seisukorraga ning relvade kaupa laskemoonaga (`ammo`; `numbers` on kogu loend).
  Teiste lennukite väärtused on viimati värskendatud seisuga.

## Mida loendid garanteerivad {#what-the-counts-guarantee}

Mängu dokumendi `counts` ütlevad, mis kordus sisaldas ja mis sellest sai:

| Võti | Mida see on |
|---|---|
| `packets`, `unreadPackets` | iga kohatud paketi tüüp ja need, mida ükski lugeja ei võta (hoitakse tervena sõnumite lisafailis) |
| `messageIds`, `messageIdsNotRead` | iga kohatud sõnumi ID ja kui tihti, ning need, mida ainult hoitakse, ei loeta |
| `replicatedComponents`, `replicatedNotRead` | loetud komponentide väärtused ja need, mida ainult hoitakse |
| `entities`, `entityTemplates`, `entityMessages` | mida olemi voog lõi ja saatis |
| `droppedSamples` | tahtlikult välja jäetud näidised (maapealse üksuse vrakk pärast selle olemi kadumist), põhjuse järgi |

Muud ei jäeta välja: kordusest üksus on kas loetud tabelisse või mängu dokumenti või
hoitud tervena lisafailis. Mängu dokumendi `selfCheck` sisaldab loetu kontrolle
([Kuidas tööriist kordust loeb](how-it-reads.md)).

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
