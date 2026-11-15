---
title: "Hliðarskrár og heilleiki"
nav_order: 8
lang: "is"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Hliðarskrár og heilleiki {#sidecars-and-completeness}

Ekkert í upptöku er hent. Það sem umbreytirinn les fer í töfluna og
leikjaskjalið; allt annað er varðveitt í heild í þremur hliðarskrám við hlið
töflunnar (inni í `.3dheat` skránni, eða lausar með `--loose`). Þetta er
reglan sem allir 3DHeat umbreytar deila:
[Umbreytar varðveita allt](https://holdi601.github.io/3DHeat/converters.html).

## Hliðarskrárnar {#the-sidecars}

- `<match>.messages.parquet`: hver skilaboð til einingar (tími, auðkenni og
  nafn skilaboða, uid, eid, sniðmát, farartæki, auðkennisreitir þeirra sem hex,
  `decoded` (það sem er lesið úr þeim, sem JSON), farmurinn), hvert afritað
  íhlutagildi (`name` íhluturinn, `fields` gildi hans), hver einingarskilaboð
  (með einingu sinni og flokksnúmeri), hver afritaður hlutur (`ReflectionData
  <kind>/<index>`, reitir hans sem hex) og hver pakki sem enginn lesari hér
  tekur, í heild.
- `<match>.objectives.parquet`: handtökusvæðin yfir tíma, ein röð fyrir hverja
  breytingu sem þjónninn sendi: `time`, `event` (`state`, `progress`,
  `captured`, `neutralised`), `zone` (bókstafur þess), `zoneId`, `object`,
  `owner` (0 enginn, 1, 2), `progress` (-100..100, jákvætt í átt að liði 2),
  `x`, `y`, `z` svæðisins, og allir `fields` hlutarins sem hex (sjá
  [Markmið](objectives.md)).
- `<match>.flight.parquet`: hver færsla flugmódels hverrar flugvélar í heild
  (bitar hennar, og `phase`: bitinn í fyrsta bæti hennar sem hún byrjaði á),
  með hraða hennar, 14 stjórnnibbles (`control1-3`, `throttle`), hreyflum
  hennar með ástandi, eftirbrennara og skilyrði, og skotum á vopn (`ammo`;
  `numbers` er allur listinn). Gildi annarra flugvéla eru eins og þau voru
  síðast endurnýjuð.

## Hvað talningarnar tryggja {#what-the-counts-guarantee}

`counts` í leikjaskjalinu segja hvað upptakan geymdi og hvað varð um það:

| Lykill | Hvað |
|---|---|
| `packets`, `unreadPackets` | hver pakkategund sem mætti, og þær sem enginn lesari tekur (varðveittar í heild í skilaboðahliðarskránni) |
| `messageIds`, `messageIdsNotRead` | hvert skilaboðaauðkenni sem mætti og hversu oft, og þau sem aðeins eru varðveitt, ekki lesin |
| `replicatedComponents`, `replicatedNotRead` | íhlutagildi sem lesin eru, og þau sem aðeins eru varðveitt |
| `entities`, `entityTemplates`, `entityMessages` | það sem einingastraumurinn bjó til og sendi |
| `droppedSamples` | sýni sem viljandi eru felld niður (flak landeiningar eftir að eining hennar er horfin), eftir ástæðu |

Engu öðru er sleppt: hlutur í upptökunni er annaðhvort lesinn í töfluna eða
leikjaskjalið, eða varðveittur í heild í hliðarskrá. `selfCheck` í
leikjaskjalinu geymir athuganir á því sem var lesið
([Hvernig upptaka er lesin](how-it-reads.md)).

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
