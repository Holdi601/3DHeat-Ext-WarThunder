---
title: "Sidefiler og fullstendighet"
nav_order: 8
lang: no
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidefiler og fullstendighet {#sidecars-and-completeness}

Ingenting i en replay kastes. Det konverteren leser, går inn i tabellen og
kampdokumentet; alt annet beholdes helt i tre sidefiler ved siden av tabellen (inne i
`.3dheat`-filen, eller løst med `--loose`). Dette er regelen alle 3DHeat-konverterere deler:
[Konverterere beholder alt](https://holdi601.github.io/3DHeat/converters.html).

## Sidefilene {#the-sidecars}

- `<kamp>.messages.parquet`: hver melding til en enhet (tid, meldings-ID og navn, uid, eid, mal, kjøretøy, dens ID-felt
  i hex, `decoded` (det som leses av den, som JSON), nyttelasten), hver replikert komponentverdi (`name` komponenten, `fields`
  dens verdi), hver entitetsmelding (med sin entitet og klassenummer), hvert replikert objekt (`ReflectionData
  <type>/<indeks>`, dets felt i hex) og hver pakke ingen leser her, helt.
- `<kamp>.objectives.parquet`: erobringssonene over tid, én rad per endring serveren sendte: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (dens bokstav), `zoneId`, `object`, `owner` (0 ingen,
  1, 2), `progress` (-100..100, positiv mot lag 2), sonens `x`,
  `y`, `z`, og alle objektets `fields` i hex (se
  [Mål](objectives.md)).
- `<kamp>.flight.parquet`: hver flymodell-inngang for hvert fly, helt (dets bits, og `phase`: biten i dets første byte den startet på),
  med sin hastighet, de 14 kontrollhalvbyte (`control1-3`, `throttle`), sine motorer med deres tilstand, etterbrenner og
  tilstand, og sine runder per våpen (`ammo`; `numbers` er hele listen). Andre flys verdier er som sist oppdatert.

## Hva tellingene garanterer {#what-the-counts-guarantee}

Kampdokumentets `counts` sier hva replayen holdt og hva som ble av det:

| Nøkkel | Hva |
|---|---|
| `packets`, `unreadPackets` | hver pakketype som ble truffet, og de ingen leser tar (beholdt helt i meldingssidefilen) |
| `messageIds`, `messageIdsNotRead` | hver meldings-ID som ble truffet og hvor ofte, og de som bare beholdes, ikke leses |
| `replicatedComponents`, `replicatedNotRead` | komponentverdier lest, og de som bare beholdes |
| `entities`, `entityTemplates`, `entityMessages` | hva entitetsstrømmen opprettet og sendte |
| `droppedSamples` | samples utelatt med vilje (et bakkeenhets vrak etter at dens entitet er borte), etter grunn |

Ingenting annet utelates: en ting i replayen er enten lest inn i tabellen eller kampdokumentet, eller
beholdt helt i en sidefil. Kampdokumentets `selfCheck` holder kontrollene av det som ble lest
([Slik leser den en replay](how-it-reads.md)).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
