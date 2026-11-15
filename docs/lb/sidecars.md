---
title: "Sidecars a Vollstännegkeet"
nav_order: 8
lang: lb
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecars a Vollstännegkeet {#sidecars-and-completeness}

Näischt an engem Replay gëtt ewechgeheit. Wat de Konverter liest, kënnt an d'
Tabell an d'Match-Dokument; alles anescht gëtt ganz an dräi
Sidecar-Dateien niewent der Tabell behalen (an der `.3dheat`-Datei, oder lass mat
`--loose`). Dat ass d'Regel, déi all 3DHeat-Konverter deelen:
[Konverteren behalen alles](https://holdi601.github.io/3DHeat/converters.html).

## D'Sidecars {#the-sidecars}

- `<match>.messages.parquet`: all Message un eng Eenheet (Zäit, Message-ID an
  Numm, uid, eid, Template, Gefier, hir ID-Felder als Hex, `decoded` (wat
  dovunner gelies gëtt, als JSON), d'Payload), all replizéierte Komponentewäert
  (`name` d'Komponent, `fields` säi Wäert), all Entitéit-Message (mat hirer
  Entitéit a Klassennummer), all replizéiert Objet (`ReflectionData
  <kind>/<index>`, seng Felder als Hex) an all Paket, dat kee Reader hei hëlt,
  ganz.
- `<match>.objectives.parquet`: d'Eroberungszonen iwwer d'Zäit, eng Zeil pro
  Ännerung, déi de Server geschéckt huet: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (hire Buschtaf), `zoneId`, `object`, `owner` (0 keen,
  1, 2), `progress` (-100..100, positiv a Richtung Team 2), dem Zon säin `x`,
  `y`, `z`, an all `fields` vum Objet als Hex (kuck
  [Ziler](objectives.md)).
- `<match>.flight.parquet`: all Flugmodell-Androung vun all Fliger ganz
  (seng Bits, a `phase`: dat Bit vu sengem éischte Byte, wou en ugefaangen huet), mat senger
  Geschwindegkeet, de 14 Kontroll-Nibbles (`control1-3`, `throttle`), senge Motore
  mat hirem Zoustand, Nobrenner a Konditioun, a senge Schëss pro Waff
  (`ammo`; `numbers` ass déi ganz Lëscht). D'Wäerter vun aneren Fliger sinn, wéi se zuletzt
  aktualiséiert goufen.

## Wat d'Zuelen garantéieren {#what-the-counts-guarantee}

D'`counts` vum Match-Dokument soen, wat de Replay gehalen huet a wat doraus ginn ass:

| Schlëssel | Wat |
|---|---|
| `packets`, `unreadPackets` | all Pakettyp, deen ugetraff gouf, an déi, déi kee Reader hëlt (ganz am Messages-Sidecar behalen) |
| `messageIds`, `messageIdsNotRead` | all Message-ID, déi ugetraff gouf, a wéi dacks, an déi, déi nëmmen behalen, net gelies goufen |
| `replicatedComponents`, `replicatedNotRead` | Komponentewäerter, déi gelies goufen, an déi, déi nëmmen behalen goufen |
| `entities`, `entityTemplates`, `entityMessages` | wat de Entitéit-Stroum erstallt a geschéckt huet |
| `droppedSamples` | Echantillonen, déi absichtlech ewechgelooss goufen (dem Buedemeenheet säi Wrack, nodeems seng Entitéit fort ass), no Grond |

Näischt anescht gëtt ewechgelooss: e Stéck vum Replay gëtt entweder an
d'Tabell oder d'Match-Dokument gelies, oder ganz an engem Sidecar behalen. Dem Match-
Dokument säin `selfCheck` hält d'Kontrolle vun deem, wat gelies gouf
([Wéi e Replay gelies gëtt](how-it-reads.md)).

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
