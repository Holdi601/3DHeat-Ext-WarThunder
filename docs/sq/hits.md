---
title: "Goditjet, të shtënat dhe zjarret"
nav_order: 13
lang: sq
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Goditjet, të shtënat dhe zjarret {#hits-gunfire-and-fires}

Për lexuesit që duan të dinë nga vijnë kolonat e goditjeve, municionit dhe zjarrit. Kontrollet japin vetëm metodën dhe përputhjen.

## Të shtënat {#gunfire}

Çdo predhë që goditi një njësi është në riluajtje (mesazhi 0xF0E9): një rresht `shot`
në pozicionin e gjuajtësit në çastin e goditjes, `targetX/Y/Z` pika e
goditjes (njësia e goditur, e zhvendosur nga pika e goditjes në kuadrin e saj, e kthyer nga
qëndrimi i saj), drejtimi drejt saj, `other` njësia e goditur. Predhat dhe
plumbat që humbën nuk dërgohen: nuk janë entitete, dhe mesazhet e
armëve në fluturim mbajnë vetëm rakata, raketa, bomba dhe silura.
Predhat e mbetura të lojtarit që regjistron (kolona e tij `ammo`) bien ndërsa gjuan, kështu që
breshëritë e tij dallohen, por jo ku shkuan ato predha. Armët e rënda kundërajrore dhe
artileria dërgojnë çdo të shtënë të vetme (`gun_shot`, pa drejtim), armët kundërajrore 40 mm
breshëritë e tyre (`fire_start`, `fire_stop`).

## Rezultatet e goditjeve {#hit-outcomes}

Me çdo goditje predhe mbi një njësi tokësore serveri i dërgon njësisë mesazhin 0xF144
(UnitOnHit): katër fusha njëbajtëshe, e katërta bitët e asaj që bëri
goditja (`selfCheck.unitMessages.outcome_*`):

| Biti | Kuptimi | Dëshmia |
|---|---|---|
| 0x20 | goditje e vetë një predhe | pothuajse të gjitha vijnë me një goditje 0xF0E9 mbi njësinë brenda 5 ms; pa të, me një shpërthim (splash) |
| 0x01 | kaloi përmes (depërtim) | çdo mesazh me 0x02, 0x04 ose 0x08 e ka edhe këtë |
| 0x02 | goditje kritike | shumica e regjistrave të goditjeve kritike e kanë, shumë më shpesh se rastësisht |
| 0x04 | shkatërruar | shumica vijnë me një regjistër vrasjeje dhe vdekjen e njësisë brenda një sekonde |
| 0x08 | dëm i rëndë | disa regjistra goditjesh kritike e kanë; rrallë përndryshe |

`hitOutcome` merr më të keqen: `kill` (0x04), `critical` (0x02 ose 0x08),
`penetration` (0x01), `nonpenetration` (0x20 vetëm). Një goditje çiftëzohet me
0xF144-n më të afërt të pa çiftëzuar me 0x20 për njësinë e saj brenda 5 ms. Kamera
e goditjes e lojës e dallon një ricochet nga një mosdepërtim, por asnjë bit ose fushë
e gjetur këtu nuk e dallon: tre bajtët e parë ndryshojnë nga goditja në goditje dhe nuk
dihen. Riluajtjet e klientit dërgojnë 0xF144 vetëm për aeroplanin e vetë lojtarit që regjistron,
me të gjithë bitët të pastër: goditjet mbi aeroplanë dhe anije nuk kanë rezultat.

## Municioni {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Shpërthyese apo jo.** Një predhë që shpërthen dërgon 0xF133 (UnitOnExplosion)
  me uid-in e gjuajtësit dhe numrin e goditjes; një goditje me të është
  `explosive`, të tjerat `kinetic`.
* **Topi dhe vendi i tij.** 0xF0BD (UnitBulletRearm) është predha tjetër e
  ngarkuar: indeksi i armës në listën e armëve të mjetit, vendi i municionit
  dhe predhat e mbetura. Ajo e një ngarkuesi manual vjen një kohë të qëndrueshme rimbushjeje
  pas çdo goditjeje të tij, ajo e një autotopi një pjesë të sekondës pas. Goditjet e një
  gjuajtësi grupohen sipas mjetit, nënshkrimit dhe breshërisë; një grup është i një
  arme kur ajo armë ngarkon një predhë brenda 20 s pas gjysmës së goditjeve të tij
  ose më shumë me një vonesë të qëndrueshme. `ammoSlot` është `weapon/slot`, vendi i ngarkuar
  para goditjes: ndoshta ai i gjuajtur, përveç nëse lojtari ndryshoi
  municionin ndërkohë. Automatikët nuk dërgojnë 0xF0BD.
* **Predha.** Arma e një vrasjeje është id-ja e predhës (`125mm_3bm46`); goditja e fundit e
  vrasësit mbi viktimën ia jep vendit të atij gjuajtësi, aty ku
  kalibri i topit përputhet. Lloji dhe kalibri i saj janë të skedarit të armës
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Kalibri** i të tjerave: ai i armës së vendit; për një grup automatikësh ai
  kalibri i vetëm i automatikut që mund ta ketë nënshkrimi i tij; përndryshe ai i
  topit kryesor të mjetit. Pa instalimin (`--game`) nuk ka lloj, emër ose
  kalibër përtej `explosive` / `kinetic`.

Nuk u gjet: ricochet. Disa mesazhe të tjera mbartin gjuajtësin dhe numrin e
goditjes (0xF0C2, ndoshta shtegu i kamerës së goditjes nëpër mjet; 0xF117,
0xF13C, 0xF13E); ruhen në skedarin anësor, nuk dekodohen. Një
mosdepërtim mbetet `nonpenetration`.

## Zjarret e mjeteve {#vehicle-fires}

Një mjet që digjet i shfaqet çdo klienti: serveri i dërgon mjetit një mesazh entiteti
(ngjarja `0a519c58`) që liston zjarret që digjen mbi të,
sa herë ndryshon lista. Për zjarr: dy ID 16-bitëshe (e dyta një nyje e
modelit të dëmit), lloji i tij, dhe -1 derisa zjarri kap. Një zjarr i ndezur nga
një goditje merr edhe një mesazh me pikën ku digjet, në kuadrin e mjetit
(x përpara, y lart, z majtas).

Rreshtat: `fire_on` kur një zjarr shfaqet në listë, `fire_off` kur ikën,
te mjeti, me `fireId` (`first:node`), `fireKind` dhe, për zjarret që ndezi një
goditje, `fireLocalX/Y/Z` (përpara, lart, djathtas). Pasi një mjet vdes lista e tij
shpesh nuk dërgohet më: zjarret e tij mbarojnë me mbetjet, përndryshe me
entitetin e tij, përndryshe me riluajtjen (`selfCheck.fires`).

Kontrolluar: sa herë ra numri i fikëseve të zjarrit të një tanku, një zjarr u largua nga
lista e tij brenda një pjese të sekondës; shumica e pikave të zjarrit shtrihen në të njëjtën anë të
mjetit si goditja që i ndezi. Llojet janë numra; çfarë emërtojnë
nuk dihet, as cila pjesë është një nyje. Aeroplanët nuk dërgojnë një listë të tillë: një
aeroplan që digjet nuk lexohet.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
