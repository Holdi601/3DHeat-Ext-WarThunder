---
title: Pomoćne datoteke i potpunost
nav_order: 8
lang: "hr"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Pomoćne datoteke i potpunost {#sidecars-and-completeness}

Ništa iz snimke se ne baca. Što pretvarač čita ide u tablicu i dokument meča; sve ostalo čuva se cijelo u tri
pomoćne datoteke uz tablicu (unutar datoteke `.3dheat`, ili odvojeno uz `--loose`). Ovo je pravilo koje dijele svi
pretvarači 3DHeata: [Pretvarači zadržavaju sve](https://holdi601.github.io/3DHeat/converters.html).

## Pomoćne datoteke {#the-sidecars}

- `<match>.messages.parquet`: svaka poruka jedinici (vrijeme, id i naziv poruke, uid, eid, predložak, vozilo, njezina
  polja id-a kao heks, `decoded` (što se od nje čita, kao JSON), teret), svaka replicirana vrijednost komponente
  (`name` komponenta, `fields` njezina vrijednost), svaka poruka entiteta (s njezinim entitetom i brojem klase), svaki
  replicirani objekt (`ReflectionData <kind>/<index>`, njegova polja kao heks) i svaki paket koji nijedan čitač ovdje
  ne uzima, cijeli.
- `<match>.objectives.parquet`: zone zauzimanja kroz vrijeme, jedan redak po promjeni koju je poslao poslužitelj:
  `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (njezino slovo), `zoneId`, `object`,
  `owner` (0 nitko, 1, 2), `progress` (-100..100, pozitivno prema timu 2), `x`, `y`, `z` zone, i sva `fields` objekta
  kao heks (vidi [Ciljevi](objectives.md)).
- `<match>.flight.parquet`: svaki unos modela leta svakog zrakoplova cijel (njegovi bitovi, i `phase`: bit prvog bajta
  na kojem je počeo), s njegovom brzinom, 14 poluzalogaja upravljanja (`control1-3`, `throttle`), njegovim motorima s
  njihovim stanjem, naknadnim izgaranjem i stanjem, i njegovim metcima po oružju (`ammo`; `numbers` je cijeli popis).
  Vrijednosti drugih zrakoplova su kakve su bile pri zadnjem osvježenju.

## Što brojevi jamče {#what-the-counts-guarantee}

`counts` dokumenta meča kažu što je snimka sadržavala i što se s time dogodilo:

| Ključ | Što |
|---|---|
| `packets`, `unreadPackets` | svaka vrsta paketa koja se susrela, i one koje nijedan čitač ne uzima (cijeli čuvani u pomoćnoj datoteci poruka) |
| `messageIds`, `messageIdsNotRead` | svaki id poruke koji se susreo i koliko puta, i oni samo sačuvani, nepročitani |
| `replicatedComponents`, `replicatedNotRead` | pročitane vrijednosti komponenti, i one samo sačuvane |
| `entities`, `entityTemplates`, `entityMessages` | što je tok entiteta stvorio i poslao |
| `droppedSamples` | uzorci namjerno izostavljeni (olupina kopnene jedinice nakon što joj entitet nestane), po razlogu |

Ništa drugo se ne izostavlja: stavka snimke ili je pročitana u tablicu ili dokument meča, ili je sačuvana cijela u
pomoćnoj datoteci. `selfCheck` dokumenta meča drži provjere onoga što je pročitano
([Kako se snimka čita](how-it-reads.md)).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
