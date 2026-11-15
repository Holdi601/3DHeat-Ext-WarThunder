---
title: "Cíle"
nav_order: 15
lang: cs
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Cíle {#objectives}

`objectives` v dokumentu zápasu vypisuje, o co se v bitvě bojuje, ze dvou zdrojů (`source`):

- **Replay** (`replay`): objekty mise, které pojmenovává 0xD039 (zóny dobytí `cz_circle_NN`, letiště, heliporty,
  základny), umístěné tam, kde je nyní postavily replikované objekty druhu 3 (0xF02D): zóna dobytí začíná na místě
  své šablony a na začátku se přesune na zónu tohoto režimu (`moved`). Čísla druhu 3 následují pořadí z 0xD039;
  každý objekt, který se nepřesunul, leží přesně tam, kde ho má 0xD039, což pořadí ověřuje. Zóna dobytí dostane
  tvar a poloměr oblasti mise na svém místě (`area`, do 2 m) a své písmeno z vlastního indexu (druh 5, pole 69:
  0 = A); pořadí písmen je z replaye, neověřuje se proti mapě hry.
- **Mise** (`mission`): soubor mise `<mission>.blk` v `mis.vromfs.bin` vaší instalace a šablony, které importuje
  (jen čtení, v době převodu): její oblasti, roztříděné podle názvu: spawny (číslované body spawnu
  `..._spawnareaNN` jako jeden spawn `points`), bitevní oblasti, cíle bombardování (`bomb_zone`), body spawnu
  konvojů (`road_NN_spawn`), oblasti výjezdu a zabití. Oblasti jiného režimu téže mapy (`conq_`, `dom_`, `bttl_`,
  ...) se vynechají a z variant `_arcade` / `_realistic` / `_hardcore` se vezme ta pro danou bitvu (RB bere
  `_realistic`, jinak `_hardcore`, jak to dělají skripty misí); vynechají se také značky v briefingu, body
  protiletadlových děl a oblasti širší než 5 km (oblasti, po kterých jsou spawny rozptýleny). Každý spawn říká, kolik
  tratí hráčů v něm začalo (`used`, `usedByTeam`). Mise může náhodně prohodit strany (`randomSpawnTeams`): když spawny
  ukazují týmy replaye obráceně, každý `team` se prohodí a strana podle jména se zachová jako `missionTeam`.
  Trasy konvojů nejsou v čtených waypointech misí; uvádí se jen to, kde se konvoje objevují.

Zóny dobytí v čase jsou doplněk `<match>.objectives.parquet`: replikované objekty druhu 5, jeden na zónu - pole 2 její
vlastník (0, 1, 2), pole 67 její postup dobytí, bajt se znaménkem od -100 do 100 (kladný směrem k týmu 2), pole 69
její index. Ověřeno (`selfCheck.objectives`) na pozemních serverových replayích bitev Conquest a Domination: každá
změna vlastníka přichází spolu s hráčem dobývajícího týmu, který v tabulce skóre získá `captureZone`, ve stejném
okamžiku (do 1,5 s) a se živou pozemní jednotkou toho týmu uvnitř zóny; spawny každé bitvy ukazují týmy replaye jen
jedním směrem (často obráceně oproti `t1_` / `t2_` mise).

## Jednotky scény: tramvaje a vozy na kolejích {#scene-units-trams-and-rail-wagons}

Úroveň může umístit vlastní jednotky: entity `unit_loader+rail_wagon` na serverovém replayi jsou tramvaje ze scénového
souboru úrovně (`gamedata/scenes/<level>_objects.blk` v `aces.vromfs.bin`: `setting__unit_class`, její transformace
a `setting__isDead`). Jejich entity nenesou čitelné uid, takže pozemní trať bez entity jednotky, jejíž první vzorek
leží do 2 m od jednotky scény, je ta jednotka: její třída jako `Vehicle`, druh `train`, typ `tram`, `locomotive`
nebo `wagon`, bez týmu; jednotka, kterou scéna umístí jako mrtvou (například vyhořelé tramvaje), je vrak (`alive` 0)
od svého prvního řádku. Hra pro ně nemá anglický název; `VehicleName` je id přečtené jako slova („Railway tram A“).
Jejich polohy se nekolísají: téměř nikdy se nehýbou (každý vzorek stejný až na bit). Replay je posílá asi desetkrát
za vteřinu bez ohledu na to, takže z jejich vzorků se nechávají jen ty, které je pohnou (0,05 m nebo 0,1 stupně),
a jeden každých 10 s (`selfCheck.sceneUnits` počítá zahozené vzorky). Dříve to byly tratě pojmenované `uid 8`
bez vozidla.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
