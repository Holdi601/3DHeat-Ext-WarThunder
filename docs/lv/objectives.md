---
title: Mērķi
nav_order: 15
lang: "lv"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Mērķi {#objectives}

`objectives` mača dokumentā uzskaita to, par ko kauja notiek, no diviem avotiem (`source`):

- **Atkārtojums** (`replay`): misijas objektus, ko 0xD039 nosauc (kapitāla zonas `cz_circle_NN`, aerodromi, helikopteru laukumi, bāzes),
  novietotus tur, kur replicētie kind 3 objekti (0xF02D) tos attēlo tagad — kapitāla zona sākas savā šablona vietā un tiek pārvietota
  uz šī režīma zonu sākumā (`moved`). Kind 3 numuri seko 0xD039 secībai; katrs objekts, kas nav pārvietots, atrodas tieši tur, kur to
  attēlo 0xD039, un tas pārbauda secību. Kapitāla zona iegūst savas vietas misijas laukuma formu un rādiusu (`area`, 2 m robežās) un savu
  burtu no sava indeksa (kind 5 lauks 69: 0 = A); burtu secība ir atkārtojuma, nav pārbaudīta pret spēles karti.
- **Misija** (`mission`): misijas fails `<mission>.blk` jūsu instalācijas `mis.vromfs.bin` un šablonus, ko tas importē (tikai lasīšana,
  konvertēšanas laikā): tās laukumus, klasificētus pēc nosaukuma — dzimšanas zonas (dzimšanas zonas numurētie punkti `..._spawnareaNN` kā
  viena `points` dzimšanas zona), kaujas laukumi, bombardēšanas mērķi (`bomb_zone`), konvoju dzimšanas punkti (`road_NN_spawn`), izejas un
  nogalināšanas zonas. Citu tā paša kartes režīmu laukumi (`conq_`, `dom_`, `bttl_`, ...) ir ārpusē, un no `_arcade` / `_realistic` /
  `_hardcore` variantiem paliek kaujas paša (RB ņem `_realistic`, citādi `_hardcore`, kā to dara misijas skripti); arī briefinga marķieri,
  pretgaisa lielgabalu punkti un laukumi, kas platāki par 5 km (tajos dzimšanas zonas ir izkaisītas). Katra dzimšanas zona saka, cik spēlētāju
  celiņi sākās tajā (`used`, `usedByTeam`). Misija var nejauši samainīt puses (`randomSpawnTeams`): kad dzimšanas zonas rāda atkārtojuma
  komandas otrādi, katrs `team` tiek samainīts, un vārda puse paturēta kā `missionTeam`. Konvoju maršruti nav misijas waypoint lasījumā;
  ir dots tikai tur, kur konvoji parādās.

Kapitāla zonas laika gaitā ir papildfails `<match>.objectives.parquet`: kind 5 replicētie objekti, viens katrai zonai — 2. lauks tās īpašnieks
(0, 1, 2), 67. lauks tās iekarošanas progress, parakstīts baits no -100 līdz 100 (pozitīvs uz komandu 2), 69. lauks tās indekss. Pārbaudīts
(`selfCheck.objectives`) uz sauszemes servera atkārtojumiem Conquest un Domination kaujās: katra īpašnieka maiņa ir kopā ar spēlētāju no
iekarojošās komandas, kam punktu tabulā tajā pašā brīdī (1,5 s robežās) pieaug `captureZone`, un ar dzīvu sauszemes vienību tās komandas
zonā; katras kaujas dzimšanas zonas rāda atkārtojuma komandas tikai vienā virzienā (bieži otrādi nekā misijas `t1_` / `t2_`).

## Skatuves vienības: tramvaji un sliežu vagoni {#scene-units-trams-and-rail-wagons}

Līmenis var novietot pats savas vienības: sauszemes servera atkārtojuma `unit_loader+rail_wagon` entītijas ir līmeņa skatuves faila tramvaji
(`gamedata/scenes/<level>_objects.blk` `aces.vromfs.bin`: `setting__unit_class`, tā transformācija un `setting__isDead`). To entītijām nav
nolasāma uid, tāpēc sauszemes celiņš bez vienības entītijas, kura pirmais paraugs atrodas 2 m robežās no skatuves vienības, ir šī vienība:
tās klase kā `Vehicle`, veids `train`, tips `tram`, `locomotive` vai `wagon`, bez komandas; vienība, ko skatuve novieto mirušu (piemēram,
nodedzināti tramvaji), ir vraks (`alive` 0) no pirmās rindas. Spēle tiem nav angļu nosaukuma; `VehicleName` ir ID, lasīts kā vārdi
("Railway tram A"). To pozīcijas nesvārstās: gandrīz visas nekad nekustas (katrs paraugs ir tieši tāds pats līdz bitam). Atkārtojums tos sūta
ap desmit reizes sekundē neatkarīgi no tā, tāpēc no to paraugiem tiek paturēti tikai tie, kas tos pārvieto (0,05 m vai 0,1 grāds), un viens ik
10 s (`selfCheck.sceneUnits` skaita izmestos paraugus). Agrāk tie bija celiņi ar nosaukumu `uid 8` bez transportlīdzekļa.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
