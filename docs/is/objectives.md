---
title: "Markmið"
nav_order: 15
lang: is
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Markmið {#objectives}

`objectives` í leikjaskjalinu telur upp það sem barist er um, úr tveimur heimildum (`source`):

- **Upptakan** (`replay`): verkefnishlutirnir sem 0xD039 nefnir (handtökusvæði `cz_circle_NN`, flugvellir, þyrlupallar,
  bækistöðvar), settir þangað sem afrituðu hlutirnir af tegund 3 (0xF02D) setja þá nú - handtökusvæði byrjar á stað
  sniðmáts síns og er fært á svæði þessa hams í upphafi (`moved`). Númer tegundar 3 fylgja röð 0xD039;
  hver hlutur sem er ekki færður liggur nákvæmlega þar sem 0xD039 hefur hann, sem athugar röðina. Handtökusvæði fær
  lögun og radíus verkefnissvæðisins á sínum stað (`area`, innan 2 m) og bókstaf sinn úr eigin vísi (tegund
  5 reitur 69: 0 = A); bókstafaröðin er upptökunnar, ekki athuguð gegn korti leiksins.
- **Verkefnið** (`mission`): verkefnisskráin `<mission>.blk` í `mis.vromfs.bin` þinnar uppsetningar og
  sniðmátin sem hún flytur inn (aðeins lesið, við breytingu): svæði hennar, flokkuð eftir nafni - endurkomusvæði (númeraðir
  punktar endurkomu `..._spawnareaNN` sem ein `points` endurkoma), bardagasvæði, sprengjuskotmörk (`bomb_zone`), upphafspunktar
  skipalesta (`road_NN_spawn`), útgöngu- og drápssvæði. Svæði annars hams sama korts (`conq_`, `dom_`, `bttl_`,
  ...) eru felld niður, og af afbrigðum `_arcade` / `_realistic` / `_hardcore` það sem tilheyrir bardaganum (RB tekur
  `_realistic`, annars `_hardcore`, eins og verkefnisskriftur gera); kynningarmerki, punktar loftvarnabyssna og svæði breiðari en
  5 km (svæðin sem endurkomur dreifast yfir) líka. Hver endurkoma segir hve margir ferlar spilara byrjuðu í henni (`used`,
  `usedByTeam`). Verkefni getur víxlað hliðum sínum af handahófi (`randomSpawnTeams`): þegar endurkomurnar sýna lið
  upptökunnar öfugt, er hvert `team` víxlað og hlið nafnsins geymd sem `missionTeam`. Leiðir skipalesta eru
  ekki í leiðarpunktum verkefnanna eins og þeir eru lesnir; aðeins er gefið hvar skipalestir birtast.

Handtökusvæðin yfir tíma eru hliðarskráin `<match>.objectives.parquet`: afrituðu hlutirnir af tegund 5, einn
fyrir hvert svæði - reitur 2 eigandi þess (0, 1, 2), reitur 67 handtökuframvinda þess, bæti með formerki frá -100 til 100 (jákvætt
í átt að liði 2), reitur 69 vísir þess. Athugað (`selfCheck.objectives`) á landþjónsupptökum af Conquest- og Domination-bardögum: hver eigandaskipti
koma með því að spilari í handtökuliðinu fær `captureZone` í stigatöflunni á sömu stundu (innan
1,5 s) og með lifandi landeiningu þess liðs inni á svæðinu; endurkomur hvers bardaga sýna lið upptökunnar
aðeins á einn veg (oft víxluð miðað við `t1_` / `t2_` verkefnisins).

## Senueiningar: sporvagnar og járnbrautarvagnar {#scene-units-trams-and-rail-wagons}

Borð getur sett eigin einingar: `unit_loader+rail_wagon` einingarnar í þjónsupptöku eru sporvagnar
senuskrár borðsins (`gamedata/scenes/<level>_objects.blk` í `aces.vromfs.bin`: `setting__unit_class`, umbreyting þess
og `setting__isDead`). Einingar þeirra bera ekkert læsilegt uid, svo landferill án einingar
sem fyrsta sýni hans liggur innan 2 m frá senueiningu er sú eining: flokkur hennar sem `Vehicle`, kind `train`, type
`tram`, `locomotive` eða `wagon`, ekkert lið; eining sem senan setur dauða (eins og útbrunnir sporvagnar) er flak (`alive` 0) frá fyrstu röð sinni. Leikurinn hefur ekkert enskt nafn fyrir þá; `VehicleName` er auðkennið
lesið sem orð ("Railway tram A"). Staða þeirra sveiflast ekki: nær allir hreyfast aldrei (öll
sýni eins upp á bita). Upptakan sendir þá um tíu sinnum á sekúndu
án tillits til þess, svo af sýnum þeirra eru aðeins þau sem hreyfa þá (0,05 m eða 0,1 gráður) geymd, og eitt á 10 s fresti
(`selfCheck.sceneUnits` telur sýnin sem eru felld niður). Áður voru þeir ferlar sem hétu `uid 8`
án farartækis.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
