---
title: "Sidecars u kompletezza"
nav_order: 8
lang: "mt"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecars u kompletezza {#sidecars-and-completeness}

Xejn f'ripetizzjoni ma jintrema. Dak li l-konvertitur jaqra jmur fit-tabella u fid-dokument
tal-partita; kull ħaġa oħra tinżamm sħiħa fi tliet fajls sidecar ħdejn it-tabella (ġewwa l-fajl
`.3dheat`, jew separati b'`--loose`). Din hija r-regola li jaqsmu l-konvertituri kollha tad-3DHeat:
[Il-konvertituri jżommu kollox](https://holdi601.github.io/3DHeat/converters.html).

## Is-sidecars {#the-sidecars}

- `<match>.messages.parquet`: kull messaġġ lil unità (ħin, id u isem tal-messaġġ, uid, eid,
  template, vettura, il-kampi tal-id tagħha bħala hex, `decoded` (dak li ntqara minnha, bħala
  JSON), il-payload), kull valur ta' komponent replikat (`name` il-komponent, `fields` il-valur
  tiegħu), kull messaġġ ta' entità (bl-entità u n-numru tal-klassi tagħha), kull oġġett replikat
  (`ReflectionData <kind>/<index>`, il-kampi tiegħu bħala hex) u kull pakkett li ebda qarrej hawn
  ma jieħu, sħaħ.
- `<match>.objectives.parquet`: iż-żoni tal-qbid maż-żmien, ringiela waħda għal kull bidla li
  bagħat is-server: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone`
  (l-ittra tagħha), `zoneId`, `object`, `owner` (0 ħadd, 1, 2), `progress` (-100..100, pożittiv
  lejn it-tim 2), `x`, `y`, `z` taż-żona, u l-`fields` kollha tal-oġġett bħala hex (ara
  [Objettivi](objectives.md)).
- `<match>.flight.parquet`: kull daħla tal-flight model ta' kull ajruplan sħiħa (il-bits tagħha,
  u `phase`: il-bit tal-ewwel byte tagħha li minnu bdiet), bil-veloċità tagħha, id-14-il nibble
  tal-kontrolli (`control1-3`, `throttle`), il-magni tagħha bl-istat, l-afterburner u l-kundizzjoni
  tagħhom, u r-rawnds tagħha għal kull arma (`ammo`; `numbers` hija l-lista sħiħa). Il-valuri
  ta' ajruplani oħra huma kif ġew aġġornati l-aħħar.

## X'jiggarantixxi l-għadd {#what-the-counts-guarantee}

Il-`counts` tad-dokument tal-partita jgħidu x'kellha r-ripetizzjoni u x'sar minnha:

| Ċavetta | X'inhi |
|---|---|
| `packets`, `unreadPackets` | kull tip ta' pakkett li ltaqa' miegħu, u dawk li ebda qarrej ma jieħu (miżmuma sħaħ fis-sidecar tal-messaġġi) |
| `messageIds`, `messageIdsNotRead` | kull id ta' messaġġ li ltaqa' miegħu u kemm-il darba, u dawk li ġew miżmuma biss, mhux moqrija |
| `replicatedComponents`, `replicatedNotRead` | valuri ta' komponenti moqrija, u dawk miżmuma biss |
| `entities`, `entityTemplates`, `entityMessages` | dak li l-fluss tal-entitajiet ħoloq u bagħat |
| `droppedSamples` | kampjuni mħallija barra apposta (il-wreck ta' unità tal-art wara li l-entità tagħha tkun għaddiet), skont ir-raġuni |

Xejn ieħor ma jitħalla barra: element tar-ripetizzjoni jew jinqara fit-tabella jew fid-dokument
tal-partita, jew jinżamm sħiħ fi sidecar. Is-`selfCheck` tad-dokument tal-partita fih il-kontrolli
ta' dak li ntqara ([Kif taqra ripetizzjoni](how-it-reads.md)).

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
