---
title: Eesmärgid
nav_order: 15
lang: et
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Eesmärgid {#objectives}

`objectives` mängu dokumendis loetleb, mille eest lahingut peetakse, kahest allikast (`source`):

- **Kordus** (`replay`): missiooni objektid, mille 0xD039 nimetab (vallutussoonid `cz_circle_NN`, lennuväljad,
  helipadid, baasid), asetatud sinna, kus liiki 3 replitseeritud objektid (0xF02D) need praegu panevad -
  vallutussoon algab oma malli kohast ja liigub alguses selle režiimi soonele (`moved`). Liigi 3 numbrid
  järgivad 0xD039 järjekorda; iga objekt, mida ei liigutata, on täpselt sinna, kus 0xD039 selle asetab, mis
  kontrollib järjekorda. Vallutussoonile antakse oma koha missiooniala kuju ja raadius (`area`, 2 m täpsusega)
  ning täht tema enda indeksist (liik 5 väli 69: 0 = A); tähtede järjekord on kordusest, seda ei kontrollitud
  mängu kaardiga.
- **Missioon** (`mission`): missioonifail `<mission>.blk` sinu installatsiooni `mis.vromfs.bin`-is ja tema
  imporditud mallid (ainult lugemiseks, konverteerimise ajal): tema alad, mis liigitatakse nime järgi -
  tekitamisalad (tekitamisala nummerdatud punktid `..._spawnareaNN` ühe `points` tekitamisena), lahingualad,
  pommitamise sihtmärgid (`bomb_zone`), konvoi tekitamispunktid (`road_NN_spawn`), väljumis- ja tapmisalad.
  Sama kaardi teise režiimi alad (`conq_`, `dom_`, `bttl_`, ...) jäetakse välja, ja `_arcade` / `_realistic` /
  `_hardcore` variantidest lahingu enda (RB võtab `_realistic`, muidu `_hardcore`, nagu teevad missiooniskriptid);
  samuti jäetakse välja briiefingu markerid, õhutõrjekahuri punktid ja alad laiemad kui 5 km (need, kuhu
  tekitamised hajutatakse). Iga tekitamisala ütleb, mitme mängija rada selles algas (`used`, `usedByTeam`).
  Missioon võib oma pooled juhuslikult vahetada (`randomSpawnTeams`): kui tekitamised näitavad kordusest
  teistpidi meeskondi, vahetatakse iga `team` ja külje nimi jääb kui `missionTeam`. Konvoi teekonnad ei ole
  missioonide teepunktides nii, nagu need loeti; antakse ainult see, kus konvoid esinevad.

Vallutussoonid ajas on lisafail `<match>.objectives.parquet`: liigi 5 replitseeritud objektid, üks iga soone
kohta - väli 2 tema omanik (0, 1, 2), väli 67 tema vallutuse edenemine, märgiga bait -100 kuni 100 (positiivne
meeskonna 2 poole), väli 69 tema indeks. Kontrollitud (`selfCheck.objectives`) serveri maapealsetel
kordustel Konquesti ja Dominationi lahingutest: iga omanikuvahetus tuleb koos mängijaga vallutavast
meeskonnast, kellel tekib skoorilaual `captureZone` samal hetkel (1,5 s täpsusega), ja elava maapealse
selle meeskonna üksusega soones; iga lahingu tekitamised näitavad kordusest meeskondi ainult ühel viisil
(sageli missiooni `t1_` / `t2_` vastupidi).

## Stseeni üksused: trammid ja raudteevagunid {#scene-units-trams-and-rail-wagons}

Tase võib paigutada oma üksusi: serveri kordusest `unit_loader+rail_wagon` olemid on taseme stseenifaili
trammid (`gamedata/scenes/<level>_objects.blk` failis `aces.vromfs.bin`: `setting__unit_class`, tema
teisendus ja `setting__isDead`). Nende olemitel ei ole loetavat uid-i, seega on maapealne rada ilma
üksuseolemita, mille esimene näidis jääb 2 m piiresse stseeni üksusest, see üksus: tema klass kui `Vehicle`,
liik `train`, tüüp `tram`, `locomotive` või `wagon`, ilma meeskonnata; stseeni järgi surnuna paigutatud
üksus (nagu läbipõlenud trammid) on vrak (`alive` 0) alates oma esimesest reast. Mäng ei anna neile
inglisekeelset nime; `VehicleName` on ID loetuna sõnadena ("Railway tram A"). Nende asukohad ei värise:
peaaegu kõik ei liigu kunagi (iga näidis sama bitini). Kordus saadab neid umbes kümme korda sekundis
sõltumata sellest, seega neist näidistest hoitakse ainult need, mis neid liigutavad (0,05 m või 0,1 kraadi),
ja üks iga 10 s (`selfCheck.sceneUnits` loeb langetatud näidised). Varem olid need rajad nimega `uid 8`
ilma sõidukita.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
