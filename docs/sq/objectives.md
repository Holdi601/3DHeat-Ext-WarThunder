---
title: "Objektivat"
nav_order: 15
lang: "sq"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objektivat {#objectives}

`objectives` në dokumentin e ndeshjes liston për çfarë zhvillohet beteja, nga dy burime (`source`):

- **Riluajtja** (`replay`): objektet e misionit që emërton 0xD039 (zonat e kapjes `cz_circle_NN`, fushat ajrore, heliportet,
  bazat), të vendosura aty ku i vendosin tani objektet e replikuara të llojit 3 (0xF02D) - një zonë kapjeje fillon në
  vendin e shabllonit të saj dhe zhvendoset te zona e kësaj mënyre në fillim (`moved`). Numrat e llojit 3 ndjekin radhën e 0xD039;
  çdo objekt që nuk zhvendoset shtrihet saktësisht aty ku e ka 0xD039, gjë që kontrollon radhën. Një zonë kapjeje merr
  formën dhe rrezen e zonës së misionit në vendin e saj (`area`, brenda 2 m) dhe shkronjën e saj nga indeksi i vet (lloji
  5 fusha 69: 0 = A); radha e shkronjave është e riluajtjes, e pakontrolluar me hartën e lojës.
- **Misioni** (`mission`): skedari i misionit `<mission>.blk` te `mis.vromfs.bin` i instalimit tënd dhe
  shabllonet që importon (vetëm lexim, në kohën e konvertimit): zonat e tij, të klasifikuara sipas emrit - zonat e ripërtëritjes (pikat e numëruara
  të një zone ripërtëritjeje `..._spawnareaNN` si një zonë `points`), zonat e betejës, objektivat e bombardimit (`bomb_zone`), pikat e ripërtëritjes së
  autokolonave (`road_NN_spawn`), zonat e daljes dhe të vrasjes. Zonat e një mënyre tjetër të së njëjtës hartë (`conq_`, `dom_`, `bttl_`,
  ...) lihen jashtë, dhe nga variantet `_arcade` / `_realistic` / `_hardcore` merret ai i vetë betejës (RB merr
  `_realistic`, përndryshe `_hardcore`, siç bëjnë skriptet e misionit); lihen jashtë edhe shënuesit e briefing-ut, pikat e armëve kundërajrore dhe zonat më të gjera se
  5 km (zonat mbi të cilat shpërndahen ripërtëritjet). Çdo zonë ripërtëritjeje thotë sa gjurmë lojtarësh filluan në të (`used`,
  `usedByTeam`). Një mision mund t'i këmbejë anët rastësisht (`randomSpawnTeams`): kur zonat e ripërtëritjes tregojnë skuadrat e
  riluajtjes në anën tjetër, çdo `team` këmbehet dhe ana e emrit mbahet si `missionTeam`. Rrugët e autokolonave nuk
  janë te pikat e rrugës të misioneve siç lexohen; jepet vetëm ku shfaqen autokolonat.

Zonat e kapjes me kalimin e kohës janë skedari anësor `<match>.objectives.parquet`: objektet e replikuara të llojit 5, një
për zonë - fusha 2 pronari i saj (0, 1, 2), fusha 67 progresi i kapjes, një bajt me shenjë nga -100 deri 100 (pozitiv
drejt skuadrës 2), fusha 69 indeksi i saj. Kontrolluar (`selfCheck.objectives`) në riluajtje serveri tokësore të betejave Conquest dhe Domination: çdo ndryshim pronari
vjen me një lojtar të skuadrës që kap duke fituar një `captureZone` në tabelën e rezultateve në të njëjtin çast (brenda
1.5 s) dhe me një njësi tokësore të gjallë të asaj skuadre brenda zonës; ripërtëritjet e çdo beteje tregojnë skuadrat e riluajtjes
vetëm në një mënyrë (shpesh të këmbyera ndaj `t1_` / `t2_` të misionit).

## Njësitë e skenës: tramvajet dhe vagonët hekurudhorë {#scene-units-trams-and-rail-wagons}

Një nivel mund të vendosë njësi të veta: entitetet `unit_loader+rail_wagon` të një riluajtjeje serveri janë tramvajet e
skedarit të skenës së nivelit (`gamedata/scenes/<level>_objects.blk` te `aces.vromfs.bin`: `setting__unit_class`,
transformimi i tij dhe `setting__isDead`). Entitetet e tyre nuk mbajnë uid të lexueshëm, kështu që një gjurmë tokësore pa entitet njësie
mostra e parë e së cilës shtrihet brenda 2 m nga një njësi skene është ajo njësi: klasa e saj si `Vehicle`, kind `train`, type
`tram`, `locomotive` ose `wagon`, pa skuadër; një njësi që skena e vendos të vdekur (si tramvajet e djegur) është mbetje (`alive` 0) që nga rreshti i saj i parë. Loja nuk ka emër anglisht për to; `VehicleName` është id-ja
e lexuar si fjalë ("Railway tram A"). Pozicionet e tyre nuk lëkunden: pothuajse të gjitha nuk lëvizin kurrë (çdo
mostër e njëjtë deri te biti). Riluajtja i dërgon rreth dhjetë herë në sekondë
pavarësisht, kështu që nga mostrat e tyre mbahen vetëm ato që i lëvizin (0.05 m ose 0.1 gradë), dhe një çdo 10 s
(`selfCheck.sceneUnits` numëron mostrat e hedhura). Më parë ishin gjurmë me emrin `uid 8`
pa mjet.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
