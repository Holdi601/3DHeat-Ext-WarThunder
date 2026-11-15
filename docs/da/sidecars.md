---
title: Sidecars og fuldstændighed
nav_order: 8
lang: "da"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecars og fuldstændighed {#sidecars-and-completeness}

Intet i et replay bliver smidt væk. Det konverteren læser, går ind i tabellen og
kampdokumentet; alt det øvrige gemmes helt i tre sidecar-filer ved siden af tabellen
(inde i `.3dheat`-filen, eller løse med `--loose`). Dette er reglen, alle 3DHeat-konvertere
deler: [Konvertere bevarer alt](https://holdi601.github.io/3DHeat/converters.html).

## Sidecars {#the-sidecars}

- `<match>.messages.parquet`: hver meddelelse til en enhed (tid, meddelelses-id og -navn,
  uid, eid, skabelon, køretøj, dets id-felter som hex, `decoded` (det, der læses ud af den,
  som JSON), nyttelasten), hver replikeret komponentværdi (`name` komponenten, `fields`
  dens værdi), hver entitetsmeddelelse (med sin entitet og klasse-nummer), hvert replikeret
  objekt (`ReflectionData <kind>/<index>`, dets felter som hex) og hver pakke, som ingen
  læser her tager, komplet.
- `<match>.objectives.parquet`: erobringszonerne over tid, én række pr. ændring serveren
  sendte: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (dens
  bogstav), `zoneId`, `object`, `owner` (0 ingen, 1, 2), `progress` (-100..100, positiv mod
  hold 2), zonens `x`, `y`, `z`, og alle objektets `fields` som hex (se
  [Mål](objectives.md)).
- `<match>.flight.parquet`: hver flyvemodel-post for hvert fly komplet (dens bits, og
  `phase`: bitten i dens første byte, den startede ved), med dens hastighed, de 14
  styrings-nibbles (`control1-3`, `throttle`), dens motorer med deres tilstand,
  efterbrænder og tilstand, og dens skud pr. våben (`ammo`; `numbers` er hele listen).
  Andre flys værdier er som sidst opdateret.

## Hvad tællerne garanterer {#what-the-counts-guarantee}

Kampdokumentets `counts` siger, hvad replayet indeholdt, og hvad der blev af det:

| Nøgle | Hvad |
|---|---|
| `packets`, `unreadPackets` | hver pakketype der er truffet, og dem ingen læser tager (gemt helt i meddelelses-sidecaren) |
| `messageIds`, `messageIdsNotRead` | hvert meddelelses-id der er truffet og hvor ofte, og dem der kun gemmes, ikke læses |
| `replicatedComponents`, `replicatedNotRead` | komponentværdier læst, og dem der kun gemmes |
| `entities`, `entityTemplates`, `entityMessages` | hvad entitetsstrømmen oprettede og sendte |
| `droppedSamples` | samples udeladt med vilje (en landenheds vrag, efter dens entitet er væk), efter årsag |

Intet andet udelades: et element i replayet er enten læst ind i tabellen eller
kampdokumentet, eller gemt helt i en sidecar. Kampdokumentets `selfCheck` indeholder
kontrollerne af det, der blev læst ([Sådan læses et replay](how-it-reads.md)).

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
