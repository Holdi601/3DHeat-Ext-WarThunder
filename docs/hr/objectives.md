---
title: Ciljevi
nav_order: 15
lang: "hr"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Ciljevi {#objectives}

`objectives` u dokumentu meča navodi za što se bitka vodi, iz dva izvora (`source`):

- **Snimka** (`replay`): objekti misije koje imenuje 0xD039 (zone zauzimanja `cz_circle_NN`, aerodromi, helidromi,
  baze), postavljeni tamo gdje ih sada stavljaju replicirani objekti vrste 3 (0xF02D) - zona zauzimanja počinje na
  mjestu svog predloška i na početku se premješta na zonu ovog načina (`moved`). Brojevi vrste 3 slijede redoslijed
  iz 0xD039; svaki objekt koji nije premješten leži točno tamo gdje ga 0xD039 ima, što provjerava redoslijed. Zona
  zauzimanja dobiva oblik i polumjer područja misije na svom mjestu (`area`, unutar 2 m) i svoje slovo iz vlastitog
  indeksa (vrsta 5 polje 69: 0 = A); redoslijed slova je snimkin, nije provjeren prema karti igre.
- **Misija** (`mission`): datoteka misije `<mission>.blk` u `mis.vromfs.bin` tvoje instalacije i predlošci koje
  uvozi (samo čitanje, u trenutku pretvaranja): njezina područja, razvrstana po nazivu - pojavljivanja (točke
  numerirane `..._spawnareaNN` pojavljivanja kao jedno `points` pojavljivanje), bojna područja, mete bombardiranja
  (`bomb_zone`), točke pojavljivanja konvoja (`road_NN_spawn`), područja izlaska i ubojstva. Područja drugog načina
  iste karte (`conq_`, `dom_`, `bttl_`, ...) su izostavljena, a od varijanti `_arcade` / `_realistic` / `_hardcore`
  uzima se bitkina (RB uzima `_realistic`, inače `_hardcore`, kako to čine skripte misija); izostavljaju se i oznake
  brifinga, točke protuzračnih topova i područja šira od 5 km (područja na koja su pojavljivanja raspršena). Svako
  pojavljivanje kaže koliko je putanja igrača počelo u njemu (`used`, `usedByTeam`). Misija može nasumično zamijeniti
  strane (`randomSpawnTeams`): kad pojavljivanja pokažu timove snimke obrnuto, svaki `team` se zamijeni, a strana iz
  naziva zadržava se kao `missionTeam`. Rute konvoja nisu u putnim točkama misija kako su pročitane; navodi se samo
  gdje se konvoji pojavljuju.

Zone zauzimanja kroz vrijeme su pomoćna datoteka `<match>.objectives.parquet`: replicirani objekti vrste 5, po jedan
po zoni - polje 2 njezin vlasnik (0, 1, 2), polje 67 njezin napredak zauzimanja, predznačni bajt od -100 do 100
(pozitivno prema timu 2), polje 69 njezin indeks. Provjereno (`selfCheck.objectives`) na poslužiteljskim snimkama
kopnenih bitaka Conquest i Domination: svaka promjena vlasnika dolazi uz igrača tima koji zauzima koji dobije
`captureZone` u tablici rezultata u isti trenutak (unutar 1,5 s) i uz živu kopnenu jedinicu tog tima unutar zone;
pojavljivanja svake bitke pokazuju timove snimke samo na jedan način (često zamijenjeno u odnosu na `t1_` / `t2_`
misije).

## Scenske jedinice: tramvaji i željeznički vagoni {#scene-units-trams-and-rail-wagons}

Razina može postaviti vlastite jedinice: entiteti `unit_loader+rail_wagon` poslužiteljske snimke su tramvaji iz
scenske datoteke razine (`gamedata/scenes/<level>_objects.blk` u `aces.vromfs.bin`: `setting__unit_class`, njihova
transformacija i `setting__isDead`). Njihovi entiteti ne nose čitljiv uid, pa je putanja kopnene jedinice bez
entiteta jedinice čiji prvi uzorak leži unutar 2 m od scenske jedinice upravo ta jedinica: njezina klasa kao
`Vehicle`, vrsta `train`, tip `tram`, `locomotive` ili `wagon`, bez tima; jedinica koju scena postavlja mrtvom (kao
izgorjeli tramvaji) je olupina (`alive` 0) od svog prvog retka. Igra za njih nema engleski naziv; `VehicleName` je id
pročitan kao riječi ("Railway tram A"). Njihovi položaji ne titraju: gotovo nikad se ne pomiču (svaki uzorak isti do
bita). Snimka ih ipak šalje oko deset puta u sekundi, pa se od njihovih uzoraka čuvaju samo oni koji ih pomiču (0,05 m
ili 0,1 stupanj), i jedan svakih 10 s (`selfCheck.sceneUnits` broji odbačene uzorke). Prije su bili putanje s nazivom
`uid 8` bez vozila.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
