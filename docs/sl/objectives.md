---
title: Cilji
nav_order: 15
lang: "sl"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Cilji {#objectives}

`objectives` v dokumentu tekme navaja, za kaj se bitka bije, iz dveh virov (`source`):

- **Posnetek** (`replay`): predmeti misije, ki jih navaja 0xD039 (območja zajema `cz_circle_NN`,
  letališča, helikopterski ploščadi, baze), postavljeni tja, kjer jih replicirani predmeti vrste 3
  (0xF02D) zdaj postavljajo – območje zajema se na začetku premakne iz mesta svoje predloge na
  območje tega načina (`moved`). Številke vrste 3 sledijo redu iz 0xD039; vsak predmet, ki ni
  premaknjen, leži natanko tam, kjer ga ima 0xD039, s čimer se red preveri. Območje zajema dobi
  obliko in polmer območja misije na svojem mestu (`area`, v 2 m) in svojo črko iz svojega
  lastnega indeksa (polje 69 vrste 5: 0 = A); vrstni red črk je iz posnetka, ni preverjen proti
  zemljevidu igre.
- **Misija** (`mission`): datoteka misije `<mission>.blk` v `mis.vromfs.bin` vaše namestitve in
  predloge, ki jih uvaža (samo za branje, ob pretvorbi): njena območja, razvrščena po imenu –
  pojavi (številčne točke pojava `..._spawnareaNN` kot en pojav `points`), bojna območja,
  bombne tarče (`bomb_zone`), točke pojava konvojev (`road_NN_spawn`), območja izhoda in uničenja.
  Območja drugega načina istega zemljevida (`conq_`, `dom_`, `bttl_`, ...) so izpuščena, pri
  različicah `_arcade` / `_realistic` / `_hardcore` pa se vzame bitkina (RB vzame `_realistic`, sicer
  `_hardcore`, kot to delajo skripte misij); izpuščeni so tudi oznake v brifingu, točke topov proti
  letalom in območja, širša od 5 km (območja, po katerih so razpršeni pojavi). Vsak pojav pove, koliko
  potez igralcev se je začelo v njem (`used`, `usedByTeam`). Misija lahko naključno zamenja strani
  (`randomSpawnTeams`): če pojavi pokažejo ekipi posnetka obratno, se vsaka `team` zamenja, stran
  imena pa se ohrani kot `missionTeam`. Poti konvojev niso v prebranih točkah poti misij; podano je
  samo tam, kjer se konvoji pojavijo.

Območja zajema skozi čas so spremljevalna datoteka `<match>.objectives.parquet`: replicirani
predmeti vrste 5, eden na območje – polje 2 njegov lastnik (0, 1, 2), polje 67 njegov napredek
zajema, predznačen bajt od -100 do 100 (pozitivno proti ekipi 2), polje 69 njegov indeks. Preverjeno
(`selfCheck.objectives`) na strežniških posnetkih tal bitk Conquest in Domination: vsaka sprememba
lastnika pride skupaj z igralcem zajemajoče ekipe, ki v lestvici v istem trenutku pridobi
`captureZone` (v 1,5 s), in z živo enoto tal te ekipe znotraj območja; pojavi vsake bitke
kažejo ekipi posnetka le v eno smer (pogosto obratno glede na `t1_` / `t2_` misije).

## Scenske enote: tramvaji in železniški vagoni {#scene-units-trams-and-rail-wagons}

Stopnja lahko postavi lastne enote: entitete `unit_loader+rail_wagon` strežniškega posnetka so
tramvaji scenske datoteke stopnje (`gamedata/scenes/<level>_objects.blk` v `aces.vromfs.bin`:
`setting__unit_class`, njihova preobrazba in `setting__isDead`). Njihove entitete nimajo berljivega
uid-ja, zato je pot na tleh brez entitete enote, katere prvi vzorec leži znotraj 2 m od scenske
enote, ta enota: njen razred `Vehicle`, vrsta `train`, tip `tram`, `locomotive` ali `wagon`, brez
ekipe; enota, ki jo scena postavi kot mrtvo (na primer izgoreli tramvaji), je od prve vrstice naprej
olupina (`alive` 0). Igra zanje nima angleškega imena; `VehicleName` je identifikator, prebran kot
besede ("Railway tram A"). Njihovi položaji ne nihajo: skoraj nikoli se ne premaknejo (vsak vzorec je
isti do bita). Posnetek jih pošilja približno desetkrat na sekundo ne glede na to, zato se obdržijo
samo tisti vzorci, ki jih premaknejo (0,05 m ali 0,1 stopinje), in po en vsakih 10 s
(`selfCheck.sceneUnits` šteje izpuščene vzorce). Prej so bile to poti z imenom `uid 8` brez vozila.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
