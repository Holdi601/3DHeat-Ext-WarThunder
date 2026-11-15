---
title: Tikslai
nav_order: 15
lang: "lt"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Tikslai {#objectives}

`objectives` rungtynių dokumente išvardija tai, dėl ko kovojama mūšyje, iš dviejų šaltinių (`source`):

- **Įrašas** (`replay`): misijos objektai, kuriuos nurodo 0xD039 (kapitalo zonos `cz_circle_NN`, aerodromai,
  sraigtasparnių aikštelės, bazės), padėti ten, kur replikuoti 3 tipo objektai (0xF02D) juos dabar nustato -
  kapitalo zona prasideda ten, kur yra jos šablonas, ir perkeliama į šio režimo zoną pradžioje (`moved`). 3 tipo
  numeriai seka 0xD039 eilę; kiekvienas objektas, kuris nebuvo perkeltas, guli tiksliai ten, kur jį turi 0xD039,
  o tai patikrina eilę. Kapitalo zona gauna misijos srities formą ir spindulį toje vietoje (`area`, 2 m tikslumu),
  o savo raidę - iš savo indekso (5 tipo laukas 69: 0 = A); raidžių tvarka yra įrašo, nepatikrinta su žaidimo
  žemėlapiu.
- **Misija** (`mission`): misijos failas `<mission>.blk` jūsų diegimo `mis.vromfs.bin` ir šablonai, kuriuos jis
  importuoja (tik skaitymas, konvertavimo metu): jos sritys, suskirstytos pagal vardą - atgimimo vietos (atgimimo
  vietos numeruoti taškai `..._spawnareaNN` kaip viena `points` atgimimo vieta), mūšio sritys, bombardavimo taikiniai
  (`bomb_zone`), konvojaus atgimimo taškai (`road_NN_spawn`), išėjimo ir naikinimo sritys. Kitų to paties žemėlapio
  režimų sritys (`conq_`, `dom_`, `bttl_`, ...) praleidžiamos, o `_arcade` / `_realistic` / `_hardcore` variantų
  paliekamas mūšio variantas (RB ima `_realistic`, kitu atveju `_hardcore`, kaip tai daro misijos scenarijai);
  praleidžiami ir žymekliai brifinguose, priešlėktuvinių patrankų taškai bei sritys, platesnės nei 5 km (plotai, per
  kuriuos išbarstyti atgimimai). Kiekvienas atgimimas nurodo, kiek žaidėjų trajektorijų jame prasidėjo (`used`,
  `usedByTeam`). Misija gali atsitiktinai sukeisti puses (`randomSpawnTeams`): kai atgimimai rodo, kad įrašo
  komandos yra priešingai, kiekvienas `team` apkeičiamas, o pusės pavadinimas išsaugomas kaip `missionTeam`.
  Konvojaus maršrutai nėra misijų taškų sąraše, kaip jie skaitomi; nurodoma tik tai, kur konvojai pasirodo.

Kapitalo zonos laikui bėgant yra papildomas failas `<match>.objectives.parquet`: replikuoti 5 tipo objektai, po
vieną kiekvienai zonai - 2 laukas jos savininkas (0, 1, 2), 67 laukas jos užėmimo eiga, su ženklu baitas nuo -100
iki 100 (teigiamas link 2 komandos), 69 laukas jos indeksas. Patikrinta (`selfCheck.objectives`) sausumos serverio
įrašuose su Konkvista ir Dominavimo mūšiais: kiekvienas savininko pasikeitimas ateina kartu su komandos žaidėju,
įgaunančiu `captureZone` rungtynių suvestinėje tuo pačiu metu (per 1,5 s), ir su gyvu tos komandos sausumos vienetu
zonoje; kiekvieno mūšio atgimimai rodo įrašo komandas tik viena kryptimi (dažnai apverstas palyginti su misijos
`t1_` / `t2_`).

## Scenos vienetai: tramvajai ir geležinkelio vagonai {#scene-units-trams-and-rail-wagons}

Lygis gali dėti savo vienetus: serverio įrašo `unit_loader+rail_wagon` esybės yra lygio scenos failo tramvajai
(`gamedata/scenes/<level>_objects.blk` `aces.vromfs.bin`: `setting__unit_class`, jo transformacija ir
`setting__isDead`). Jų esybės neturi nuskaitomo uid, todėl sausumos trajektorija be vieneto esybės, kurios pirmas
pavyzdys yra per 2 m nuo scenos vieneto, yra tas vienetas: jo klasė kaip `Vehicle`, rūšis `train`, tipas
`tram`, `locomotive` arba `wagon`, be komandos; vienetas, kurį scena patalpina jau negyvą (kaip sudegę tramvajai),
yra griuvėsiai (`alive` 0) nuo savo pirmos eilutės. Žaidimas jiems angliško vardo neturi; `VehicleName` yra id,
perskaitytas kaip žodžiai ("Railway tram A"). Jų pozicijos nesvyruoja: beveik niekada nejuda (kiekvienas pavyzdys
tiksliai toks pat iki bito). Įrašas juos siunčia maždaug dešimt kartų per sekundę nepriklausomai nuo to, todėl iš jų
pavyzdžių išsaugomi tik tie, kurie juos pajudina (0,05 m arba 0,1 laipsnio), ir vienas kas 10 s
(`selfCheck.sceneUnits` suskaičiuoja išmestus pavyzdžius). Anksčiau jie buvo trajektorijos, pavadintos `uid 8`, be
technikos.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
