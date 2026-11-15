---
title: "Célok"
nav_order: 15
lang: "hu"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Célok {#objectives}

A meccsdokumentum `objectives` mezője felsorolja, miért folyik a csata, két forrásból (`source`):

- **A visszajátszás** (`replay`): a küldetésobjektumok, amelyeket a 0xD039 nevez meg (elfoglalható
  zónák `cz_circle_NN`, repülőterek, helikopter-leszállók, bázisok), oda helyezve, ahol a 3-as fajtájú
  replikált objektumok (0xF02D) most vannak – egy elfoglalható zóna a sablonja helyén indul, és a
  csatamód zónájába kerül a kezdetkor (`moved`). A 3-as fajta számai a 0xD039 sorrendjét követik;
  minden objektum, amelyet nem mozgattak, pontosan ott van, ahol a 0xD039 szerint, ez ellenőrzi a
  sorrendet. Egy elfoglalható zóna megkapja a küldetésterület alakját és sugarát az helyén
  (`area`, 2 m-en belül), és a betűjelét a saját indexéből (5-ös fajta, 69-es mező: 0 = A); a
  betűsorrend a visszajátszásé, nem ellenőriztük a játék térképével.
- **A küldetés** (`mission`): a `<mission>.blk` küldetésfájl a telepítésed `mis.vromfs.bin`
  fájljában és az általa importált sablonok (csak olvasva, konvertáláskor): a területei, nevük
  szerint osztályozva – a kezdőpontok (egy kezdőpont számozott pontjai, `..._spawnareaNN`, egyetlen
  `points` kezdőpontként), csatatérületek, bombázási célpontok (`bomb_zone`), konvoj-kezdőpontok
  (`road_NN_spawn`), kilépési és ölési területek. Az ugyanazon térkép más módjainak területei
  (`conq_`, `dom_`, `bttl_`, ...) kimaradnak, és az `_arcade` / `_realistic` / `_hardcore`
  változatok közül a csata saját változata marad meg (az RB a `_realistic`-et, különben a
  `_hardcore`-t veszi, ahogy a küldetésszkriptek is); a kiosztó jelölők, a légvédelmi ágyú pontjai
  és az 5 km-nél szélesebb területek (amelyekre a kezdőpontok szét vannak szórva) szintén kimaradnak.
  Minden kezdőpont megmondja, hány játékos pályája kezdődött benne (`used`, `usedByTeam`). Egy
  küldetés véletlenszerűen felcserélheti az oldalakat (`randomSpawnTeams`): ha a kezdőpontok
  fordítva mutatják a visszajátszás csapatait, minden `team` felcserélődik, és a név szerinti oldal
  `missionTeam` néven megmarad. A konvojok útvonalai nincsenek a küldetések beolvasott
  útpontjai között; csak az van megadva, hogy hol jelennek meg konvojok.

Az elfoglalható zónák időbeli alakulása a `<match>.objectives.parquet` kísérőfájl: az 5-ös fajta
replikált objektumai, zónánként egy – a 2-es mező a tulajdonosa (0, 1, 2), a 67-es mező az
elfoglalás állása, előjeles bájt -100 és 100 között (pozitív a 2. csapat felé), a 69-es mező az
indexe. Ellenőrizve (`selfCheck.objectives`) földi szerver-visszajátszásokon, Hódítás- és
Dominancia-csatákon: minden tulajdonos-változást egy olyan játékos jelez az eredménytáblában, aki
az elfoglaló csapatból ugyanabban a pillanatban (1,5 s-on belül) `captureZone` pontot szerez, és az
adott csapat egy élő földi egysége is a zónában van; minden csata kezdőpontjai a visszajátszás
csapatait csak egy irányba mutatják (gyakran felcserélve a küldetés `t1_` / `t2_` jelöléséhez képest).

## Jelenetegységek: villamosok és sínkocsik {#scene-units-trams-and-rail-wagons}

Egy pálya saját egységeket is elhelyezhet: a szerver-visszajátszás `unit_loader+rail_wagon` entitásai
a pálya jelenetfájljának villamosai (`gamedata/scenes/<level>_objects.blk` az `aces.vromfs.bin`-ben:
`setting__unit_class`, az átalakításuk és a `setting__isDead`). Az entitásaik nem tartalmaznak
olvasható uid-et, ezért az a földi pálya, amelynek nincs egységentitása, de az első mintája 2 m-en
belül van egy jelenetegységtől, az az egység: az osztálya `Vehicle`, fajtája `train`, típusa `tram`,
`locomotive` vagy `wagon`, csapat nélkül; a jelenet halottnak helyezett egység (például kiégett
villamosok) az első sorától roncs (`alive` 0). A játéknak nincs angol nevük; a `VehicleName` az
azonosító szavakként olvasva ("Railway tram A"). A helyzetük nem ingadozik: szinte soha nem mozdulnak
(minden minta bitről bitre ugyanaz). A visszajátszás ettől függetlenül körülbelül tízszer másodpercenként
küldi őket, ezért a mintáik közül csak azokat tartjuk meg, amelyek mozgatják őket (0,05 m vagy 0,1 fok),
és 10 másodpercenként egyet (`selfCheck.sceneUnits` a kidobott mintákat számolja). Korábban
`uid 8` nevű pályák voltak, jármű nélkül.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
