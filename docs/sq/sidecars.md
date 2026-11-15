---
title: "Skedarët anësorë dhe plotësia"
nav_order: 8
lang: "sq"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Skedarët anësorë dhe plotësia {#sidecars-and-completeness}

Asgjë në një riluajtje nuk hidhet tutje. Çfarë lexon konvertuesi shkon në
tabelë dhe në dokumentin e ndeshjes; gjithçka tjetër ruhet e plotë në tre
skedarë anësorë pranë tabelës (brenda skedarit `.3dheat`, ose të shkëputur me
`--loose`). Ky është rregulli që ndajnë të gjithë konvertuesit e 3DHeat:
[Konvertuesit ruajnë gjithçka](https://holdi601.github.io/3DHeat/converters.html).

## Skedarët anësorë {#the-sidecars}

- `<match>.messages.parquet`: çdo mesazh për një njësi (koha, ID e mesazhit dhe
  emri, uid, eid, shablloni, mjeti, fushat e tij ID si hex, `decoded` (çfarë
  lexohet prej tij, si JSON), ngarkesa), çdo vlerë komponenti e replikuar
  (`name` komponenti, `fields` vlera e tij), çdo mesazh entiteti (me entitetin dhe
  numrin e klasës), çdo objekt i replikuar (`ReflectionData
  <kind>/<index>`, fushat e tij si hex) dhe çdo paketë që nuk e merr asnjë lexues këtu,
  e plotë.
- `<match>.objectives.parquet`: zonat e kapjes me kalimin e kohës, një rresht për çdo
  ndryshim që dërgoi serveri: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (shkronja e saj), `zoneId`, `object`, `owner` (0 askush,
  1, 2), `progress` (-100..100, pozitiv drejt skuadrës 2), `x`, `y`, `z` të zonës,
  dhe të gjitha `fields` të objektit si hex (shih
  [Objektivat](objectives.md)).
- `<match>.flight.parquet`: çdo hyrje e modelit të fluturimit e çdo aeroplani e plotë
  (bitët e saj, dhe `phase`: biti i bajtit të parë nga ku filloi), me
  shpejtësinë e saj, 14 nibble-t e kontrollit (`control1-3`, `throttle`), motorët e saj
  me gjendjen, afterburner-in dhe gjendjen teknike, dhe predhat e saj për armë
  (`ammo`; `numbers` është lista e plotë). Vlerat e aeroplanëve të tjerë janë siç u
  rifreskuan së fundmi.

## Çfarë garantojnë numrat {#what-the-counts-guarantee}

`counts` i dokumentit të ndeshjes thotë çfarë mbante riluajtja dhe çfarë u bë me
të:

| Çelësi | Çfarë |
|---|---|
| `packets`, `unreadPackets` | çdo lloj pakete i hasur, dhe ato që nuk i merr asnjë lexues (ruhen të plota te skedari anësor i mesazheve) |
| `messageIds`, `messageIdsNotRead` | çdo ID mesazhi e hasur dhe sa herë, dhe ato vetëm të ruajtura, jo të lexuara |
| `replicatedComponents`, `replicatedNotRead` | vlerat e komponentëve të lexuara, dhe ato vetëm të ruajtura |
| `entities`, `entityTemplates`, `entityMessages` | çfarë krijoi dhe dërgoi rrjedha e entiteteve |
| `droppedSamples` | mostra të lëna jashtë me qëllim (mbetjet e një njësie tokësore pasi entiteti i saj ka ikur), sipas arsyes |

Asgjë tjetër nuk lihet jashtë: një element i riluajtjes ose lexohet në tabelë ose
në dokumentin e ndeshjes, ose ruhet i plotë në një skedar anësor. `selfCheck` i
dokumentit të ndeshjes mban kontrollet e asaj që u lexua
([Si e lexon një riluajtje](how-it-reads.md)).

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
