---
title: "Sidecar datoteke i potpunost"
nav_order: 8
lang: bs
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecar datoteke i potpunost {#sidecars-and-completeness}

Ništa iz replaya se ne baca. Ono što konverter pročita ide u
tabelu i dokument meča; sve ostalo se čuva cijelo u tri
sidecar datoteke pored tabele (unutar `.3dheat` datoteke, ili odvojeno uz
`--loose`). To je pravilo koje dijele svi 3DHeat konverteri:
[Konverteri čuvaju sve](https://holdi601.github.io/3DHeat/converters.html).

## Sidecar datoteke {#the-sidecars}

- `<match>.messages.parquet`: svaka poruka jedinici (vrijeme, id poruke i
  ime, uid, eid, šablon, vozilo, njena polja id-a kao hex, `decoded` (šta
  je od nje pročitano, kao JSON), payload), svaka replicirana vrijednost komponente
  (`name` komponenta, `fields` njena vrijednost), svaka poruka entiteta (s njenim
  entitetom i brojem klase), svaki replicirani objekt (`ReflectionData
  <kind>/<index>`, njegova polja kao hex) i svaki paket koji nijedan ovdašnji čitač ne uzima,
  cijeli.
- `<match>.objectives.parquet`: zone zauzimanja kroz vrijeme, jedan red po
  promjeni koju je server poslao: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (njeno slovo), `zoneId`, `object`, `owner` (0 nijedan,
  1, 2), `progress` (-100..100, pozitivno prema timu 2), `x`, `y`, `z` zone,
  i sva `fields` objekta kao hex (vidi
  [Ciljevi](objectives.md)).
- `<match>.flight.parquet`: svaki unos modela leta svakog aviona cijeli
  (njegovi bitovi i `phase`: bit njegovog prvog bajta na kojem je počeo), s njegovom
  brzinom, 14 kontrolnih nibble-ova (`control1-3`, `throttle`), njegovim motorima
  sa stanjem, naknadnim sagorijevanjem i stanjem, i njegovim mecima po oružju
  (`ammo`; `numbers` je cijela lista). Vrijednosti drugih aviona su onakve kakve su zadnji put osvježene.

## Šta brojevi jamče {#what-the-counts-guarantee}

`counts` dokumenta meča kaže šta je replay sadržavao i šta se s
tim desilo:

| Ključ | Šta |
|---|---|
| `packets`, `unreadPackets` | svaki susretnuti tip paketa, i oni koje nijedan čitač ne uzima (čuvaju se cijeli u sidecar datoteci poruka) |
| `messageIds`, `messageIdsNotRead` | svaki susretnuti id poruke i koliko često, i oni koji su samo sačuvani, a ne pročitani |
| `replicatedComponents`, `replicatedNotRead` | pročitane vrijednosti komponenti, i one koje su samo sačuvane |
| `entities`, `entityTemplates`, `entityMessages` | šta je tok entiteta napravio i poslao |
| `droppedSamples` | uzorci namjerno izostavljeni (olupina kopnene jedinice poslije nestanka njenog entiteta), po razlogu |

Ništa drugo nije izostavljeno: svaka stavka replaya ili je pročitana u
tabelu ili dokument meča, ili je sačuvana cijela u sidecar datoteci. `selfCheck`
dokumenta meča sadrži provjere pročitanog
([Kako čita replay](how-it-reads.md)).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
