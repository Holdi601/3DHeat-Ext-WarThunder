---
title: "Ciele"
nav_order: 15
lang: "sk"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Ciele {#objectives}

`objectives` v dokumente zápasu vypisuje, o čo sa v bitke bojuje, z dvoch zdrojov (`source`):

- **Replay** (`replay`): objekty misie, ktoré pomenúva 0xD039 (zóny dobytia `cz_circle_NN`, letiská, pristávacie plochy,
  základne), umiestnené tam, kde ich teraz dávajú replikované objekty druhu 3 (0xF02D) – zóna dobytia začína na mieste
  svojej šablóny a na začiatku sa presunie na zónu tohto režimu (`moved`). Čísla druhu 3 nasledujú poradie 0xD039;
  každý objekt, ktorý sa nepresunul, leží presne tam, kde ho má 0xD039, čo overuje poradie. Zóna dobytia dostane tvar
  a polomer oblasti misie na svojom mieste (`area`, do 2 m) a svoje písmeno z vlastného indexu (druh 5, pole 69: 0 = A);
  poradie písmen je z replaye, neoverené oproti mapě hry.
- **Misia** (`mission`): súbor misie `<mission>.blk` v `mis.vromfs.bin` vo vašej inštalácii a šablóny, ktoré importuje
  (len čítanie, pri konverzii): jej oblasti, zaradené podľa názvu – spawny (očíslované body spawnu `..._spawnareaNN` ako
  jeden spawn `points`), bojové oblasti, bombardovacie ciele (`bomb_zone`), body spawnu konvojov (`road_NN_spawn`),
  výstupné a zabíjacie oblasti. Oblasti inšieho režimu tej istej mapy (`conq_`, `dom_`, `bttl_`, ...) sa vynechávajú
  a z variant `_arcade` / `_realistic` / `_hardcore` sa berie tá bitky (RB berie `_realistic`, inak `_hardcore`, ako to
  robia skripty misií); tiež značky brífingu, body protilietadlových zbraní a oblasti širšie než 5 km (tie, po ktorých
  sú spawny rozptýlené). Každý spawn hovorí, koľko stôp hráčov v ňom začalo (`used`, `usedByTeam`). Misia môže náhodne
  vymieňať strany (`randomSpawnTeams`): keď spawny ukazujú tímy replaye naopak, každý `team` sa vymení a strana z názvu
  sa zachová ako `missionTeam`. Trasy konvojov nie sú v waypointoch misií tak, ako sa čítajú; uvádza sa len, kde sa konvoje objavujú.

Zóny dobytia v čase sú sprievodný súbor `<match>.objectives.parquet`: replikované objekty druhu 5, jeden na zónu – pole 2
jej vlastník (0, 1, 2), pole 67 jej postup dobytia, znamienkový bajt od -100 do 100 (kladný smerom k tímu 2), pole 69
jej index. Overené (`selfCheck.objectives`) na pozemných serverových replayoch bitiek Conquest a Domination: každá zmena
vlastníka sa zhoduje s hráčom dobývajúceho tímu, ktorý v tabuľke výsledkov získa `captureZone` v tom istom okamihu (do 1,5 s),
a so živou pozemnou jednotkou toho tímu v zóne; spawny každej bitky ukazujú tímy replaye len jedným smerom (často
vymenené oproti `t1_` / `t2_` misie).

## Scénické jednotky: električky a vagóny {#scene-units-trams-and-rail-wagons}

Level môže umiestniť vlastné jednotky: entity `unit_loader+rail_wagon` zo serverového replaye sú električky zo scénového
súboru levelu (`gamedata/scenes/<level>_objects.blk` v `aces.vromfs.bin`: `setting__unit_class`, jej transformácia a
`setting__isDead`). Ich entity nenesú čitateľné uid, takže pozemná stopa bez entity jednotky, ktorej prvá vzorka leží do
2 m od scénovej jednotky, je táto jednotka: jej trieda ako `Vehicle`, druh `train`, typ `tram`, `locomotive` alebo `wagon`,
bez tímu; jednotka, ktorú scéna umiestni mŕtvu (ako vyhorené električky), je vrak (`alive` 0) od svojho prvého riadku.
Hra pre ne nemá anglický názov; `VehicleName` je id čítané ako slová („Railway tram A“). Ich polohy necukajú: takmer
nikdy sa nehýbu (každá vzorka rovnaká až na bit). Replay ich posiela asi desaťkrát za sekundu bez ohľadu na to, takže
z ich vzoriek sa ponechajú len tie, ktoré ich pohnú (0,05 m alebo 0,1 stupňa), a jedna každých 10 s
(`selfCheck.sceneUnits` počíta zahodené vzorky). Predtým boli stopy pomenované `uid 8` bez vozidla.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
