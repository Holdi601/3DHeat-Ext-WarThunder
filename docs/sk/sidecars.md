---
title: "Sprievodné súbory a úplnosť"
nav_order: 8
lang: sk
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sprievodné súbory a úplnosť {#sidecars-and-completeness}

Nič z replaye sa nevyhodí. To, čo konvertor číta, ide do tabuľky a dokumentu zápasu; všetko ostatné sa uchová celé v troch
sprievodných súboroch vedľa tabuľky (vo vnútri súboru `.3dheat`, alebo samostatne s `--loose`). Toto je pravidlo, ktoré
zdieľajú všetky konvertory 3DHeat: [Konvertory zachovávajú všetko](https://holdi601.github.io/3DHeat/converters.html).

## Sprievodné súbory {#the-sidecars}

- `<match>.messages.parquet`: každá správa pre jednotku (čas, id a názov správy, uid, eid, šablóna, vozidlo, jej id polia
  v hex, `decoded` (čo sa z nej číta, ako JSON), obsah), každá hodnota replikovaného komponentu (`name` komponent, `fields`
  jeho hodnota), každá entitná správa (s jej entitou a číslom triedy), každý replikovaný objekt (`ReflectionData
  <kind>/<index>`, jeho polia v hex) a každý paket, ktorý tu žiadny čitateľ neprevezme, celý.
- `<match>.objectives.parquet`: zóny dobytia v čase, jeden riadok na každú zmenu, ktorú server poslal: `time`, `event`
  (`state`, `progress`, `captured`, `neutralised`), `zone` (jej písmeno), `zoneId`, `object`, `owner` (0 žiadny,
  1, 2), `progress` (-100..100, kladný smerom k tímu 2), `x`, `y`, `z` zóny a všetky `fields` objektu v hex (pozri
  [Ciele](objectives.md)).
- `<match>.flight.parquet`: každý záznam modelu letu každého lietadla celý (jeho bity a `phase`: bit prvého bajtu, na ktorom
  začal), s jeho rýchlosťou, 14 štvorbitmi ovládania (`control1-3`, `throttle`), jeho motormi s ich stavom, prepaľovaním
  a stavom, a jeho nábojmi na zbraň (`ammo`; `numbers` je celý zoznam). Hodnoty iných lietadiel sú také, aké boli naposledy obnovené.

## Čo zaručujú počty {#what-the-counts-guarantee}

Položky `counts` v dokumente zápasu hovoria, čo replay obsahoval a čo sa s tým stalo:

| Kľúč | Čo |
|---|---|
| `packets`, `unreadPackets` | každý stretnutý typ paketu a tie, ktoré žiadny čitateľ nepreberá (celé uchované v sprievodnom súbore správ) |
| `messageIds`, `messageIdsNotRead` | každé stretnuté id správy a ako často, a tie, ktoré sa len uchovali, nečítali |
| `replicatedComponents`, `replicatedNotRead` | prečítané hodnoty komponentov a tie, ktoré sa len uchovali |
| `entities`, `entityTemplates`, `entityMessages` | čo tok entít vytvoril a poslal |
| `droppedSamples` | vzorky vynechané úmyselne (vrak pozemnej jednotky po tom, ako je jej entita preč), podľa dôvodu |

Nič iné sa nevynecháva: položka replaye je buď prečítaná do tabuľky alebo dokumentu zápasu, alebo uchovaná celá
v sprievodnom súbore. Položka `selfCheck` dokumentu zápasu obsahuje kontroly toho, čo sa prečítalo
([Ako sa replay číta](how-it-reads.md)).

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
