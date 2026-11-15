---
title: "Ciljevi"
nav_order: 15
lang: "bs"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Ciljevi {#objectives}

`objectives` u dokumentu meča navodi oko čega se bitka vodi, iz dva izvora (`source`):

- **Replay** (`replay`): objekti misije koje imenuje 0xD039 (zone zauzimanja `cz_circle_NN`, aerodromi, heliodromi,
  baze), postavljeni tamo gdje ih sada stavljaju replicirani objekti vrste 3 (0xF02D) - zona zauzimanja počinje na
  mjestu svog šablona i na početku se pomjera na zonu ovog načina (`moved`). Brojevi vrste 3 slijede redoslijed 0xD039;
  svaki objekt koji nije pomjeren leži tačno gdje ga ima 0xD039, što provjerava redoslijed. Zona zauzimanja dobiva
  oblik i radijus područja misije na svom mjestu (`area`, unutar 2 m) i svoje slovo iz vlastitog indeksa (vrsta
  5 polje 69: 0 = A); redoslijed slova je redoslijed replaya, nije provjeren prema mapi igre.
- **Misija** (`mission`): datoteka misije `<mission>.blk` u `mis.vromfs.bin` vaše instalacije i
  šabloni koje uvozi (samo čitanje, u vrijeme pretvaranja): njena područja, razvrstana po imenu - zone pojavljivanja (numerirane
  tačke zone `..._spawnareaNN` kao jedna zona `points`), područja bitke, mete bombardiranja (`bomb_zone`), tačke pojavljivanja
  konvoja (`road_NN_spawn`), područja izlaza i ubijanja. Područja drugog načina iste mape (`conq_`, `dom_`, `bttl_`,
  ...) izostavljaju se, a od varijanti `_arcade` / `_realistic` / `_hardcore` uzima se vlastita varijanta bitke (RB uzima
  `_realistic`, inače `_hardcore`, kao što rade skripte misija); izostavljaju se i oznake brifinga, tačke protivavionskih topova i područja šira od
  5 km (područja po kojima su zone pojavljivanja raspršene). Svaka zona pojavljivanja kaže koliko je igračkih staza u njoj počelo (`used`,
  `usedByTeam`). Misija može nasumično zamijeniti svoje strane (`randomSpawnTeams`): kad zone pojavljivanja pokazuju timove replaya
  obrnuto, svaki `team` se zamijeni, a strana iz imena zadrži kao `missionTeam`. Rute konvoja
  nisu u putnim tačkama misija kako se čitaju; daje se samo gdje se konvoji pojavljuju.

Zone zauzimanja kroz vrijeme su sidecar `<match>.objectives.parquet`: replicirani objekti vrste 5, jedan
po zoni - polje 2 njen vlasnik (0, 1, 2), polje 67 njen napredak zauzimanja, bajt s predznakom od -100 do 100 (pozitivno
prema timu 2), polje 69 njen indeks. Provjereno (`selfCheck.objectives`) na kopnenim serverskim replayevima bitaka Conquest i Domination: svaka promjena vlasnika
dolazi s igračem tima koji zauzima koji dobija `captureZone` u tabeli rezultata u istom trenutku (unutar
1,5 s) i sa živom kopnenom jedinicom tog tima unutar zone; zone pojavljivanja svake bitke pokazuju timove replaya
samo na jedan način (često zamijenjene u odnosu na `t1_` / `t2_` misije).

## Scenske jedinice: tramvaji i željeznički vagoni {#scene-units-trams-and-rail-wagons}

Nivo može postaviti vlastite jedinice: entiteti `unit_loader+rail_wagon` serverskog replaya su tramvaji
iz scenske datoteke nivoa (`gamedata/scenes/<level>_objects.blk` u `aces.vromfs.bin`: `setting__unit_class`, njena
transformacija i `setting__isDead`). Njihovi entiteti ne nose čitljiv uid, pa je kopnena staza bez entiteta jedinice
čiji prvi uzorak leži unutar 2 m od scenske jedinice ta jedinica: njena klasa kao `Vehicle`, kind `train`, type
`tram`, `locomotive` ili `wagon`, bez tima; jedinica koju scena postavlja mrtvu (poput izgorjelih tramvaja) je olupina (`alive` 0) od svog prvog reda. Igra za njih nema englesko ime; `VehicleName` je id
pročitan kao riječi ("Railway tram A"). Njihove pozicije ne podrhtavaju: gotovo svi se nikad ne pomjeraju (svaki
uzorak isti do na bit). Replay ih šalje oko deset puta u sekundi
bez obzira na to, pa se od njihovih uzoraka zadržavaju samo oni koji ih pomjeraju (0,05 m ili 0,1 stepen), i jedan svakih 10 s
(`selfCheck.sceneUnits` broji odbačene uzorke). Prije su bile staze imenovane `uid 8`
bez vozila.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
