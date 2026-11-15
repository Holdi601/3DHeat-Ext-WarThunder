---
title: Papildomi failai ir pilnumas
nav_order: 8
lang: lt
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Papildomi failai ir pilnumas {#sidecars-and-completeness}

Niekas įraše neišmetama. Tai, ką konverteris perskaito, patenka į lentelę ir rungtynių dokumentą;
viskas kita išsaugoma pilnai trijuose papildomuose failuose šalia lentelės (`.3dheat` failo viduje
arba atskirai su `--loose`). Tai taisyklė, kurios laikosi visi 3DHeat konverteriai:
[Konverteriai išsaugo viską](https://holdi601.github.io/3DHeat/converters.html).

## Papildomi failai {#the-sidecars}

- `<match>.messages.parquet`: kiekvienas pranešimas vienetui (laikas, pranešimo id ir vardas, uid,
  eid, šablonas, technika, jos id laukai šešioliktainiu pavidalu, `decoded` (kas perskaityta, JSON
  formatu), turinys), kiekviena replikuota komponento reikšmė (`name` - komponentas, `fields` - jo
  reikšmė), kiekvienas esybės pranešimas (su jo esybe ir klasės numeriu), kiekvienas replikuotas
  objektas (`ReflectionData <kind>/<index>`, jo laukai šešioliktainiu pavidalu) ir kiekvienas
  paketas, kurio neskaito joks čia esantis skaitytuvas, pilnai.
- `<match>.objectives.parquet`: kapitalo zonos laikui bėgant, viena eilutė kiekvienam serverio
  siųstam pokyčiui: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone`
  (jos raidė), `zoneId`, `object`, `owner` (0 - nieko, 1, 2), `progress` (-100..100, teigiamas link
  2 komandos), zonos `x`, `y`, `z`, ir visi objekto `fields` šešioliktainiu pavidalu (žr.
  [Tikslai](objectives.md)).
- `<match>.flight.parquet`: kiekvienas skrydžio modelio įrašas kiekvieno orlaivio, visas (jo bitai ir
  `phase`: bitas jo pirmame baite, nuo kurio jis prasidėjo), su jo greičiu, 14 valdymo pusbaiščių
  (`control1-3`, `throttle`), jo varikliais ir jų būsena, degikliu ir būkle, bei šaudmenimis kiekvienam
  ginklui (`ammo`; `numbers` yra visas sąrašas). Kitų orlaivių reikšmės yra tokios, kokios buvo
  paskutinį kartą atnaujintos.

## Ką garantuoja skaičiai {#what-the-counts-guarantee}

Rungtynių dokumento `counts` parodo, ką įrašas turėjo ir kas su tuo nutiko:

| Raktas | Ką reiškia |
|---|---|
| `packets`, `unreadPackets` | kiekvienas sutiktas paketo tipas ir tie, kurių neskaito joks skaitytuvas (pilnai išsaugoti pranešimų papildomame faile) |
| `messageIds`, `messageIdsNotRead` | kiekvienas sutiktas pranešimo id ir kiek kartų, bei tie, kurie tik išsaugoti, bet neperskaityti |
| `replicatedComponents`, `replicatedNotRead` | perskaitytos komponentų reikšmės ir tos, kurios tik išsaugotos |
| `entities`, `entityTemplates`, `entityMessages` | ką sukūrė ir nusiuntė esybių srautas |
| `droppedSamples` | pavyzdžiai, tyčia praleisti (sausumos vieneto griuvėsiai, kai jo esybės nebėra), pagal priežastį |

Daugiau nieko nepraleidžiama: kiekvienas įrašo elementas arba perskaitomas į lentelę ar rungtynių
dokumentą, arba pilnai išsaugomas papildomame faile. Rungtynių dokumento `selfCheck` laiko
perskaitytų dalykų patikrinimus ([Kaip įrankis skaito įrašą](how-it-reads.md)).

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
