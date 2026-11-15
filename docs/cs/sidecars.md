---
title: "Doplňky a úplnost"
nav_order: 8
lang: cs
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Doplňky a úplnost {#sidecars-and-completeness}

Nic z replaye se nezahazuje. Co převodník čte, jde do tabulky a dokumentu zápasu; vše ostatní se drží celé ve třech
souborech doplňků vedle tabulky (uvnitř souboru `.3dheat`, nebo samostatně s `--loose`). Toto je pravidlo, které
sdílejí všechny převodníky 3DHeat:
[Převodníky zachovávají vše](https://holdi601.github.io/3DHeat/converters.html).

## Doplňky {#the-sidecars}

- `<match>.messages.parquet`: každá zpráva jednotce (čas, id zprávy a název, uid, eid, šablona, vozidlo, jeho
  id pole v hex, `decoded` (co se z ní přečetlo, jako JSON), obsah), každá hodnota replikované komponenty
  (`name` komponenta, `fields` její hodnota), každá zpráva entity (s jejím číslem entity a třídy), každý replikovaný
  objekt (`ReflectionData <kind>/<index>`, jeho pole v hex) a každý paket, který tu žádný čtenář nebere, celé.
- `<match>.objectives.parquet`: zóny dobytí v čase, jeden řádek na každou změnu, kterou server poslal: `time`,
  `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (její písmeno), `zoneId`, `object`, `owner` (0
  žádný, 1, 2), `progress` (-100..100, kladný směrem k týmu 2), `x`, `y`, `z` zóny a všechna `fields` objektu v hex
  (viz [Cíle](objectives.md)).
- `<match>.flight.parquet`: každý záznam letového modelu každého letadla celý (jeho bity a `phase`: bit prvního
  bajtu, ve kterém začal), s jeho rychlostí, 14 půlbajty ovládání (`control1-3`, `throttle`), jeho motory s jejich
  stavem, přídavným spalováním a stavem, a jeho náboje na zbraň (`ammo`; `numbers` je celý seznam). Hodnoty
  ostatních letadel jsou ty, které se naposledy obnovily.

## Co zaručují počty {#what-the-counts-guarantee}

`counts` dokumentu zápasu říkají, co replay obsahoval a co se s tím stalo:

| Klíč | Co |
|---|---|
| `packets`, `unreadPackets` | každý typ paketu, který se potkal, a ty, které žádný čtenář nebere (uchovány celé v doplňku zpráv) |
| `messageIds`, `messageIdsNotRead` | každé id zprávy, které se potkalo, a kolikrát, a ty jen uchovány, ne čteny |
| `replicatedComponents`, `replicatedNotRead` | přečtené hodnoty komponent a ty jen uchovány |
| `entities`, `entityTemplates`, `entityMessages` | co proud entit vytvořil a poslal |
| `droppedSamples` | vzorky vynechané záměrně (vrak pozemní jednotky poté, co její entita zmizela), podle důvodu |

Nic dalšího se nevynechává: položka replaye se buď přečte do tabulky nebo do dokumentu zápasu, nebo se uchová celá
v doplňku. Ukazatel `selfCheck` dokumentu zápasu drží kontroly toho, co bylo přečteno
([Jak se replay čte](how-it-reads.md)).

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
