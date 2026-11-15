---
title: "Repülőgépek"
nav_order: 11
lang: hu
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Repülőgépek {#aircraft}

Azoknak, akik tudni szeretnék, honnan származnak a repülőgép-oszlopok, és
mennyire bízhatnak bennük. Az alábbi minden ellenőrzés egy értéket hasonlít
össze valamivel, amit a visszajátszás második, független módon mond el;
csak a módszer és az egyezés van leírva.

## Fedélzeti műszerek {#cockpit-instruments}

A 0xD04A üzenet a felvevő játékos műszereit (szám, érték) párokban küldi:
arcade csatákban másodpercenként négyszer, szimulátor csatákban csak a
megváltozott értékeket. A számok az összes fedélzeti kijelzőre egy listát
alkotnak, és egy kijelző azokat a műszereket küldi, amelyek a modelljében
vannak. A játék kódja határozza meg, melyik szám melyik műszer, ezért minden
számot aszerint neveztünk el, mit csinál, és a visszajátszással ellenőriztük
(a `convert.INSTRUMENTS` tartalmazza az eredményt; semmi sincs a telepítésből
kiolvasva):

| Szám | Név | Ellenőrizve ezzel |
|---|---|---|
| 0 | jelzett légsebesség, m/s | a pálya sebessége a levegő sűrűségére javítva: korreláció 0,99 |
| 39 | emelkedési sebesség, m/s | a pálya emelkedési sebessége: korreláció 0,99 felett |
| 40, 41 | magasság, m; magasság modulo 1000 | a pálya magassága, néhány méteren belül |
| 52, 53 | mesterséges horizont dőlése és billenése | a táblázat (mínusz) dőlése és billenése, 1 foknál kisebb eltéréssel |
| 64 | iránytű | a táblázat iránya, 0,1 foknál kisebb eltéréssel |
| 15-20 | kormánypedálok | a repülőgépre ható oldalirányú erő |
| 23, 31 | botkormány: magassági és csűrőkormány (előjel a kijelző modelljéhez igazodik) | a támadási szög; a dőlési sebesség |
| 69, 71, 73 | óra: órák (12 órás számlap), percek, másodpercek | a rögzítő számítógép helyi ideje, percre pontosan |
| 75 | töltőnyomás, atm | háborús vészteljesítményen magasabb, mint teljes gázon |
| 81-86, 87-92, 93-98 | fordulatszám motoronként, fordulatszám modulo 1000, fordulatszámmérő | egymással pontosan; a motor fordulatszáma: korreláció 0,97 felett |
| 195 | üzemanyag | a bevetés során csökken, újraéledéskor újra tele |
| 228-230 | futómű-lábak, 1 = lent | csak a repülőterek magasságánál és leszálló sebességnél van lent |
| 240, 241 | gázkar motoronként (1,1 háborús vészteljesítmény vagy utánégető) | a repülési bejegyzés gázkarja |
| 330-332, 346-348 | lőszerszámlálók (két azonos készlet) | a fegyver előbeállításának lőszere, a repülési bejegyzés lőszerével együtt csökkenve |
| 135, 159 | olaj- és hengerfej-hőmérséklet | valószínű: a bevetés során emelkednek |
| 58, 61 | csúszógolyó, fordulatjelző mutató | valószínű: az oldalirányú erőt és a fordulási sebességet követik |
| 223 | légfék | valószínű: csak megközelítéskor van beállítva |
| 490-497, 500-505 | kerékfékek | valószínű: csak repülőtéren állva vannak beállítva |

Néhány további szám is érkezik, amelynek jelentése nem ismert; ezeket a
meccsdokumentum `authorInstruments.notNamed` mezőjében tároljuk.

A táblázat `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` és `throttle` mezői ezekből származnak, a
felvevő játékos saját sorain, a mintavétel után legfeljebb 0,2 s-mal érkező
utolsó üzenetet véve.

## Repülési bejegyzések {#flight-entries}

Minden repülőgép repülési bejegyzése (csomagtípus 2) a helyzete és
állása mellett a következőket hordozza:

- **Sebesség**: egy 32 bites szó az állás után. A 31., 30. és 29. bit az x, y
  és z előjele; utána a sebesség 11 biten, 500/2047 m/s egységekben (500 m/s-nél
  megáll), majd |x| és |y| a sebesség törtrészeként, 9-9 biten, a z pedig
  azt adja, hogy a vektor egységvektor legyen. A kapott mintavételek közötti
  lépéshez hasonlítva ellenőrizve: az irány a felvevő játékosnál egy fok
  töredékén belül, másoknál körülbelül 2 fokon belül egyezik; a sebesség 0,2
  %-on belül. `selfCheck.flightEntries`.
- **Lőszer fegyverenként**: egy lista a helyzet előtt, fegyverenként egy elem,
  először a hátralévő lőszer. A felvevő játékosé szinte minden mintánál egy
  órajellel később megegyezik a kijelző számlálóival.
- **Vezérlők és gáz**: 7 bájt a sebesség után, 14 nibble-ként olvasva. A
  felvevő játékosnál minden órajelben: 1 a magassági kormány, 2 a csűrők, 3
  a kormány (nyugalomban 8), 11 a gázkar tizenötödökben (15 a háborús
  vészteljesítményt és az utánégetőt is jelenti), 4 a kerékfék, 5 a légfék, 8
  valószínűleg a fékernyő. Más repülőgépek nibble-jei csatánként csak néhányszor
  változnak, és nem a pillanatnyi vezérlésük.
- **Motorok**: motoronként egy állapotbájt (0 ki; 1-6 indul; 7 jár; 8
  leállt), egy 16 bites érték csak utánégetőnél (32767 teljes), és egy bájt
  csak miután a motort eltalálták. Azok a repülőgépek, amelyeknek motorja
  „leállt” állapotba kerül, legtöbbször percen belül megsemmisülnek vagy
  véget érnek.

## Tükrözési adatok {#reflection-data}

A 0xF02D és 0xF0AA üzenetek a játék számozott objektumait tükrözik: objektumonként
az azonosítójukat (a felső 5 bit a fajta, az alsó 11 egy index) és egy mezőtáblát.
A 14-es fajta a játékos-helyek (2-es mező: felhasználói azonosító és név, 9-es: a
csapat), az 15-ös fajta a csapatok (1-es és 2-es index):

- Egy hely 39-es mezője a statisztikáit rögzített helyeken tartja: ölések
  (0. eltolás), csapattársak elleni ölések (2), halálok (4), tengeri ölések (10),
  MI-ölések (12), MI-földi ölések (14), asszisztok (20), elfoglalt zónák (22),
  zónasebzés (24, 32 bites), sebzési jutalom (40, 32 bites), rakétakitérések (50).
  A 38-as mező a pontszámmal kezdődik, a 42-es a rajjal. A csata végén minden
  érték minden játékosnál megegyezik az eredmények azonos értékeivel
  (`selfCheck.scoreboardVsResults`). Azt, hogy a földi ölések hol tárolódnak,
  nem tudjuk.
- Egy csapat 7-es mezője a pontszáma: a végén egyenlő a játékosai pontszámainak
  összegével az eredményekben. A 3-as mező valószínűleg a csapat jegyei.
  Minden üzenet csak a megváltozott mezőket küldi, ezért a meccsdokumentum
  `scoreboard` része minden játékos statisztikáit és minden csapat pontszámát
  listázza minden változásnál.

## Holtpont-számítás és a simító {#dead-reckoning-and-the-smoother}

A kliens-visszajátszás minden repülőgépet másodpercenként négyszer rögzít, úgy,
ahogy a kliens megrajzolta. Egy távoli repülőgép két frissítése között a kliens
az utolsó sebessége szerint tovább mozgatja, és az utolsó forgási sebességével
fordítja; a következő frissítésnél egyszerre odaugrik. Úgy olvasva a pálya egyenesen
fut, aztán ugrik. A repülési bejegyzésből nem derül ki, mely mintákat kaptuk meg;
a holtpont-számított mintát az jelzi, hogy az őt megelőző két minta egyenes vonalát
folytatja, azok tempójában, 3 cm-en belül.

Ez a csatától függ: arcade csatákban a többi repülőgép mintáinak mintegy fele lehet
holtpont-számított, szimulátor csatákban csak néhány százalék. A simító a 15 g-nél
nagyobb ugrásokat körülbelül ötöddel csökkenti (`selfCheck.deadReckoning`). A
felvevő játékos saját repülőgépét a kliens nem extrapolálja, ezért azt érintetlenül
hagyjuk.

Alapértelmezetten (a `--no-smoothing` kikapcsolja) az összes egység pályáját ott
helyezzük el, ahol a kapott állapotok szerint volt: egy holtpont-számított minta egy
görbén van, amely az előtte és utána lévő kapott mintákon megy át, mindegyiknek a saját
sebességével; 3 másodpercnél hosszabb szakaszon az egyenes vonal csak a következő
kapott minta felé hajlik, így egyetlen minta sem mozdul el a kliens saját ugrásánál
messzebbre. Az állása egyenletesen fordul egyik kapott állásról a következőre. A kapott
mintákat legfeljebb 2 m-rel vagy a sebességük 0,04 s-ával simítjuk; az állandó fordulat
változatlan marad. A visszajátszás saját értékei a `Raw` oszlopokban maradnak meg.

## Állás, ellenőrizve {#attitude-checked}

A felvevő játékos saját repülőgépén az irány (medián) egy fokon belül egyezik a
haladási iránnyal, a billenés néhány fokon belül az emelkedési szöggel, és éles
fordulatoknál a dőlés szinte minden mintánál a fordulás előjelét mutatja: a
repülésmodell dőlése a bal szárny lefelé mutatásakor pozitív, a táblázat a jobb szárny
lefelé mutatásakor pozitív. A 10 bites szögek 0,18 fokonként lépnek
(`selfCheck.aircraftAttitude`). A földi egységek állását a lövéseik alapján ellenőrizzük
([Tornyok](ground.md#turrets)).

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
