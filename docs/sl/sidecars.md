---
title: Spremljevalne datoteke in popolnost
nav_order: 8
lang: sl
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Spremljevalne datoteke in popolnost {#sidecars-and-completeness}

Nič v posnetku se ne zavrže. Kar pretvornik prebere, gre v tabelo in dokument tekme;
vse ostalo se ohrani celo v treh spremljevalnih datotekah poleg tabele (v datoteki
`.3dheat` ali ločeno z `--loose`). To je pravilo, ki ga delijo vsi pretvorniki 3DHeat:
[Pretvorniki ohranijo vse](https://holdi601.github.io/3DHeat/converters.html).

## Spremljevalne datoteke {#the-sidecars}

- `<match>.messages.parquet`: vsako sporočilo enoti (čas, identifikator in ime sporočila, uid,
  eid, predloga, vozilo, njegova polja z identifikatorji v šestnajstiškem zapisu, `decoded` (kar
  se iz njega prebere, kot JSON), tovor), vsaka replicirana vrednost komponente (`name`
  komponenta, `fields` njena vrednost), vsako sporočilo entitete (z njeno entiteto in številko
  razreda), vsak replicirani predmet (`ReflectionData <kind>/<index>`, njegova polja v
  šestnajstiškem zapisu) in vsak paket, ki ga tukajšnji bralniki ne vzamejo, celo.
- `<match>.objectives.parquet`: območja zajema skozi čas, ena vrstica na vsako spremembo, ki jo
  je poslal strežnik: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone`
  (njegova črka), `zoneId`, `object`, `owner` (0 nihče, 1, 2), `progress` (-100..100, pozitivno
  proti ekipi 2), `x`, `y`, `z` območja ter vsa `fields` predmeta v šestnajstiškem zapisu (glejte
  [Cilji](objectives.md)).
- `<match>.flight.parquet`: vsak vnos modela leta vsakega letala, celo (njegovi biti in `phase`:
  bit njegovega prvega bajta, pri katerem se je začel), s hitrostjo, 14 krmilnimi nibbli
  (`control1-3`, `throttle`), njegovimi motorji z njihovim stanjem, post-zgorevanjem in stanjem
  ter njegovimi streli na orožje (`ammo`; `numbers` je celoten seznam). Vrednosti drugih letal so
  take, kot so bile nazadnje osvežene.

## Kaj jamčijo števila {#what-the-counts-guarantee}

Števila `counts` v dokumentu tekme povedo, kaj je posnetek vseboval in kaj se je z
njim zgodilo:

| Ključ | Kaj |
|---|---|
| `packets`, `unreadPackets` | vsaka vrsta paketa, ki je bila srečana, in tisti, ki jih nobeden bralnik ne vzame (ohranjeni celi v spremljevalni datoteki sporočil) |
| `messageIds`, `messageIdsNotRead` | vsak identifikator sporočila, ki je bil srečan, in kolikokrat, ter tisti, ki so samo ohranjeni, ne pa prebrani |
| `replicatedComponents`, `replicatedNotRead` | prebrane vrednosti komponent, in tiste, ki so samo ohranjene |
| `entities`, `entityTemplates`, `entityMessages` | kaj je tok entitet ustvaril in poslal |
| `droppedSamples` | vzorci, namenoma izpuščeni (vrak enote na tleh, potem ko njena entiteta izgine), z razlogom |

Nič drugega ni izpuščeno: vsaka stvar posnetka je ali prebrana v tabelo ali dokument
tekme ali pa ohranjena celo v spremljevalni datoteki. Element `selfCheck` v dokumentu tekme
vsebuje preverjanja tega, kar je bilo prebrano ([Kako bere posnetek](how-it-reads.md)).

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
