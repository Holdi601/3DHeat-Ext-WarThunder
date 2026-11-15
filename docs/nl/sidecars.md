---
title: "Sidecars en volledigheid"
nav_order: 8
lang: "nl"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecars en volledigheid {#sidecars-and-completeness}

Niets in een replay wordt weggegooid. Wat de converter leest, gaat in de tabel
en het wedstrijddocument; al het andere wordt volledig bewaard in drie
sidecar-bestanden naast de tabel (in het `.3dheat`-bestand, of los met
`--loose`). Dit is de regel die alle 3DHeat-converters delen:
[Converters bewaren alles](https://holdi601.github.io/3DHeat/converters.html).

## De sidecars {#the-sidecars}

- `<match>.messages.parquet`: elk bericht aan een eenheid (tijd, bericht-id en
  naam, uid, eid, sjabloon, voertuig, de id-velden als hex, `decoded` (wat ervan gelezen
  is, als JSON), de payload), elke gerepliceerde componentwaarde (`name` de component,
  `fields` de waarde ervan), elk entiteitsbericht (met zijn entiteit en klassenummer), elk
  gerepliceerd object (`ReflectionData <soort>/<index>`, de velden als hex) en elk
  pakket dat geen enkele lezer hier neemt, volledig.
- `<match>.objectives.parquet`: de veroveringszones door de tijd heen, één rij per
  wijziging die de server stuurde: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (zijn letter), `zoneId`, `object`, `owner` (0 geen,
  1, 2), `progress` (-100..100, positief richting team 2), de `x`, `y` en `z` van de
  zone, en alle `fields` van het object als hex (zie [Doelen](objectives.md)).
- `<match>.flight.parquet`: elke vluchtmodelregel van elk vliegtuig, volledig (zijn
  bits, en `phase`: de bit van zijn eerste byte waarbij hij begon), met zijn
  snelheid, de 14 besturingsnibbles (`control1-3`, `throttle`), zijn motoren
  met hun toestand, naverbrander en conditie, en zijn rondes per wapen
  (`ammo`; `numbers` is de hele lijst). Waarden van andere vliegtuigen zijn zoals
  ze laatst ververst werden.

## Wat de tellingen garanderen {#what-the-counts-guarantee}

De `counts` van het wedstrijddocument zeggen wat de replay bevatte en wat er mee
gebeurd is:

| Sleutel | Wat |
|---|---|
| `packets`, `unreadPackets` | elk pakkettype dat tegenkwam, en die welke geen enkele lezer neemt (volledig bewaard in de messages-sidecar) |
| `messageIds`, `messageIdsNotRead` | elk bericht-id dat tegenkwam en hoe vaak, en die welke alleen bewaard en niet gelezen worden |
| `replicatedComponents`, `replicatedNotRead` | gelezen componentwaarden, en die welke alleen bewaard worden |
| `entities`, `entityTemplates`, `entityMessages` | wat de entiteitenstroom aanmaakte en verstuurde |
| `droppedSamples` | samples die bewust zijn weggelaten (het wrak van een grondeenheid nadat zijn entiteit weg is), per reden |

Verder wordt niets weggelaten: elk onderdeel van de replay wordt ofwel in de
tabel of het wedstrijddocument gelezen, ofwel volledig bewaard in een sidecar. Het
`selfCheck` van het wedstrijddocument bevat de controles van wat gelezen is
([Hoe het een replay leest](how-it-reads.md)).

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
