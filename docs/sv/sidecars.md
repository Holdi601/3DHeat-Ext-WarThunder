---
title: "Sidofiler och fullständighet"
nav_order: 8
lang: sv
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidofiler och fullständighet {#sidecars-and-completeness}

Ingenting i en repris kastas bort. Det konverteraren läser går in i tabellen och
matchdokumentet; allt annat behålls helt i tre sidofiler bredvid tabellen (inuti
`.3dheat`-filen, eller löst med `--loose`). Det här är regeln alla 3DHeat-konverterare
delar: [Konverterare behåller allt](https://holdi601.github.io/3DHeat/converters.html).

## Sidofilerna {#the-sidecars}

- `<match>.messages.parquet`: varje meddelande till en enhet (tid, meddelande-id och namn,
  uid, eid, mall, fordon, dess id-fält som hex, `decoded` (vad som läses av det, som JSON),
  nyttolasten), varje replikerat komponentvärde (`name` komponenten, `fields` dess värde),
  varje entitetsmeddelande (med sin entitet och sitt klassnummer), varje replikerat objekt
  (`ReflectionData <kind>/<index>`, dess fält som hex) och varje paket som ingen läsare här tar,
  helt.
- `<match>.objectives.parquet`: erövringszonerna över tid, en rad per ändring som servern
  skickade: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (dess
  bokstav), `zoneId`, `object`, `owner` (0 ingen, 1, 2), `progress` (-100..100, positiv mot lag 2),
  zonens `x`, `y`, `z`, och alla objektets `fields` som hex (se [Mål](objectives.md)).
- `<match>.flight.parquet`: varje flygmodellpost för varje flygplan helt (dess bitar, och `phase`:
  biten i dess första byte den startade vid), med dess hastighet, de 14 reglage-halvbytena
  (`control1-3`, `throttle`), dess motorer med deras tillstånd, efterbrännare och skick, och dess
  skott per vapen (`ammo`; `numbers` är hela listan). Andra flygplans värden är som senast
  uppfriskade.

## Vad räknarna garanterar {#what-the-counts-guarantee}

Matchdokumentets `counts` säger vad repriset innehöll och vad som blev av det:

| Nyckel | Vad |
|---|---|
| `packets`, `unreadPackets` | varje paketsort som träffats, och de som ingen läsare tar (behållna helt i meddelandesidofilen) |
| `messageIds`, `messageIdsNotRead` | varje meddelande-id som träffats och hur ofta, och de som bara behållits, inte lästs |
| `replicatedComponents`, `replicatedNotRead` | komponentvärden lästa, och de som bara behållits |
| `entities`, `entityTemplates`, `entityMessages` | vad entitetsströmmen skapade och skickade |
| `droppedSamples` | mätpunkter som lämnats bort med avsikt (en markenhets vrak efter att dess entitet är borta), per orsak |

Inget annat lämnas bort: ett objekt i repriset är antingen läst till tabellen eller
matchdokumentet, eller behållet helt i en sidofil. Matchdokumentets `selfCheck` innehåller
kontrollerna av det som lästes ([Så läser den en repris](how-it-reads.md)).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
