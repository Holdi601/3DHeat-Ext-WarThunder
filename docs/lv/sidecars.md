---
title: Papildfaili un pilnība
nav_order: 8
lang: lv
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Papildfaili un pilnība {#sidecars-and-completeness}

Neviens atkārtojuma saturs netiek izmests. Ko konvertētājs nolasa, nonāk tabulā un mača dokumentā; viss pārējais tiek paturēts pilnībā trīs papildfailos blakus tabulai (`.3dheat` failā vai atsevišķi ar `--loose`). Tas ir noteikums, ko visi 3DHeat konvertētāji dalīa: [Konvertētāji saglabā visu](https://holdi601.github.io/3DHeat/converters.html).

## Papildfaili {#the-sidecars}

- `<match>.messages.parquet`: katrs ziņojums vienībai (laiks, ziņojuma ID un nosaukums, uid, eid, šablons, transportlīdzeklis, tā ID lauki heksadecimāli, `decoded` (ko no tā nolasa, kā JSON), saturs), katra replicētās komponentes vērtība (`name` komponente, `fields` tās vērtība), katrs entītijas ziņojums (ar savu entītiju un klases numuru), katrs replicētais objekts (`ReflectionData <kind>/<index>`, tā lauki heksadecimāli) un katra pakete, ko neviens šeit neņem, pilnībā.
- `<match>.objectives.parquet`: kapitāla zonas laika gaitā, viena rinda katrai izmaiņai, ko serveris nosūtīja: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (tās burts), `zoneId`, `object`, `owner` (0 nav, 1, 2), `progress` (-100..100, pozitīvs uz komandu 2), zonas `x`, `y`, `z`, un visi objekta `fields` heksadecimāli (skat. [Mērķi](objectives.md)).
- `<match>.flight.parquet`: katrs lidmašīnas lidojuma modeļa ieraksts, katras lidmašīnas, pilnībā (tās biti un `phase`: bits tā pirmajā baitā, kurā tā sākās), ar tā ātrumu, 14 vadības nibbles (`control1-3`, `throttle`), tā dzinējiem ar to stāvokli, pēcdedzi un stāvokli, un tās šāviņiem katrā ieročā (`ammo`; `numbers` ir visa saraksts). Citu lidmašīnu vērtības ir tādas, kādas tās bija pēdējo reizi atjauninātas.

## Ko skaitļi garantē {#what-the-counts-guarantee}

Mača dokumenta `counts` saka, ko atkārtojums saturēja un kas ar to notika:

| Atslēga | Ko tā nozīmē |
|---|---|
| `packets`, `unreadPackets` | katrs sastaptais paketes tips un tās, ko neviens lasītājs neņem (paturētas pilnībā ziņojumu papildfailā) |
| `messageIds`, `messageIdsNotRead` | katrs sastaptais ziņojuma ID un cik bieži, un tie, kas tikai paturēti, nevis nolasīti |
| `replicatedComponents`, `replicatedNotRead` | nolasītās komponenšu vērtības un tās, kas tikai paturētas |
| `entities`, `entityTemplates`, `entityMessages` | ko entītiju plūsma izveidoja un nosūtīja |
| `droppedSamples` | paraugi, kas izlaisti tīši (sauszemes vienības vraks pēc tās entītijas aiziešanas), pa iemesliem |

Nekas cits netiek izlaists: katrs atkārtojuma vienums vai nu tiek nolasīts tabulā vai mača dokumentā, vai paturēts pilnībā papildfailā. Mača dokumenta `selfCheck` satur nolasītā pārbaudes ([Kā tas nolasa atkārtojumu](how-it-reads.md)).

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
