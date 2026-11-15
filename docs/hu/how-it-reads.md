---
title: "Hogyan olvassa a visszajátszást"
nav_order: 10
lang: hu
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Hogyan olvassa a visszajátszást {#how-it-reads-a-replay}

Ez az oldal azoknak szól, akik tudni szeretnék, mit olvas a konvertáló, hogyan
ellenőriztük az olvasást, és ezért mennyire bízhatnak az egyes oszlopokban. A
konvertáláshoz nincs rá szükséged.

Az olvasást kliens-visszajátszásokon ellenőriztük légi arcade, légi szimulátor és
tengeri csatákon, szerver-visszajátszásokon földi csatákon, a 2025-ös elrendezéseknél pedig
a [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder) nyilvános
mintavisszajátszásain. Minden ellenőrzés egy értéket hasonlít össze valamivel, amit a
visszajátszás második, független módon mond el; itt csak a módszer és az egyezés van megadva.

## Mi van beolvasva, és az ellenőrzés {#what-is-read-and-the-check}

| Rész | Állapot és ellenőrzés |
|---|---|
| Fejléc, térkép, küldetés, kezdési idő, munkamenet; eredmények | minden fájl |
| Küldetésbeállítások (a fejléc utáni blk) | mód, időjárás, korlátok, `stars` (dátum, idő, hely) |
| Csomagfolyam (2025-ben zlib, 2026-ban zstd) | minden csomag keretezve |
| Repülőgép-helyzetek és állások (2026-os elrendezés) | másodpercenként 4 minta, egy csomag sem marad olvasatlanul; az irány egyezik a haladási iránnyal |
| Repülési csomagok az idejüknél előrébb | hálózati akadás után egy kliens-visszajátszás repülési csomagja néha minden más repülőgépet ott tart, ahol körülbelül 0,75 s-mal később lesz. Az előrehaladást csomagonként mérjük, és minden előrehaladó repülőgép megkapja az időt, amelyet a helyzete jelent (`selfCheck.flightPacketsRetimed`) |
| Holtpont-számított ugrások | a holtpont-számított sorozatból való ugrást az utolsó kapott állapotától mérjük, így a kliens korrekciói már nem vágják el a pályákat ([Holtpont-számítás](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportálások | egy pályát ott vágunk el, ahol az egysége messzebb mozdul, mint amennyit tudna: először a fajtájához mérve (repülőgép 750 m/s, föld és hajók 40 m/s, fegyverek 1800 m/s), majd a saját tempójához. Minden vágás szerepel a `trackBreaks` listában a valószínű okával (újraéledés, a játék mozgatja a játékost, egy távoli egység korrekciója). A vágások után egy pálya sorai között egyetlen lépés sem gyorsabb, mint amit a fajtája megenged (`selfCheck.stepSpeed`) |
| Föld- és hajóhelyzetek (0xF073 / 0xF074) | egy csomag sem marad olvasatlanul. Irány, billenés és dőlés a 16 bites állásból: az irány mediánban körülbelül 2 fokon belül egyezik a haladási iránnyal; a billenés 180/65536 fokonként lép; a dőlés előjelét megfordítva a törzs és a torony adta ágyúirány szinte minden tanklövésnél az eltalált egységre mutat. A hajók a vízszint szintjén vannak |
| Tornyok | a tankok torony-elfordulása és ágyúemelkedése: lásd [Tornyok](ground.md#turrets) |
| Tömörített föld-magasságok | 64 bitbe tömörített helyzetek magasságát a legtöbb pályán -100 m-től, egyeseken a vízszinttől számítjuk; az eltolást minden visszajátszáson mérjük azokból az egységekből, amelyek mindkét alakban láthatók (`selfCheck.packedGroundHeight`) |
| Entitásfolyam (létrehozás, megsemmisítés) | minden létrehozás olvasva. Az elrendezés a Dagor Engine közzétett forrásából származik; a War Thunder saját komponenstípusait úgy hagyjuk ki, hogy megkeressük, hol kezdődik a következő komponens. Minden egység jármű- és játékos-helye megegyezik azzal, amit az ölés- és találatrekordok neveznek meg, minden ellenőrzött rekordnál |
| Ki vezetett melyik egységet, MI-egységek, hajók, földi célpontok | az entitásfolyamból: minden egységnek megvan a járműve és a csapata, minden játékos egységének a játékosa |
| Ölések az eredményekhez képest | a játékosonkénti halálok egyeznek az eredményekével; az eredmények több ölést számolnak, mert a kliens nem kap minden ölést. A csata kezdete után induló visszajátszás csak az azutáni ölésekeket tartalmazza |
| Ölések, kritikus találatok, súlyos sérülés | minden fájl |
| Megsemmisült modulok (0xF118) | az egység és a rész száma; a rész neve a jármű sérülésmodelljét igényli, ami nincs a visszajátszásban |
| Kilőtt fegyverek (entitásfolyam) | a kilövési pont körülbelül 10-20 m-re van (medián) a legközelebbi egységtől, amelyet kilövőnek veszünk |
| Repülő fegyverek (0xF0DB) | rakéták, rakéták és bombák, mindegyik a saját entitásához kötve |
| Repülési rekord nélküli bombák | a repülési rekord nélküli bomba esését a kilövéstől a becsapódásig kiszámítjuk (gravitáció és légellenállás, 0,1 s-onként egy minta, `extrapolated` igaz). Tengeren ellenőrizve, ahol a becsapódási magasság ismert: a kiszámolt esések körülbelül 15 m-en belül érnek a vízbe. A meccsdokumentumban az ilyen fegyvernek `ballisticImpact` van; a `counts.bombsBallistic` megszámolja őket |
| Játékos-helyek, csevegés | minden fájl |
| Robbanások, légvédelmi robbanások, díjak, felderítések, időjárás, küldetésobjektumok | olvasva; a helyzeteket szemmel ellenőriztük a megjelenítőben |
| A felvevő játékos műszerei (0xD04A) | a tevékenységük szerint nevezve el: [Fedélzeti műszerek](aircraft.md#cockpit-instruments); a többi a `notNamed` alatt |
| A repülési bejegyzések többi mezője | sebesség, lőszer, vezérlők, motorok: [Repülési bejegyzések](aircraft.md#flight-entries) |
| Eseménysorok állása | minden eseménysor tartalmazza az egysége irányát, billenését, dőlését és nézési vektorát abban a pillanatban |
| Játékosstatisztikák és csapatpontszámok | a csata végén minden statisztika minden játékosnál egyezik az eredményekével: [Tükrözési adatok](aircraft.md#reflection-data) |
| Fegyver- és járműnevek | a telepítésed angol nyelvi fájljaiból; néhány hajó alapértelmezett övének és repülőtéri radarjának nincs neve a játékban |
| Játékosok és MI | az eredmények egyetlen játékosának sora sem MI, minden nem MI sor egy eredményjátékosé (`selfCheck.identity`) |
| Roncsok | egy egység mintái a halála után tovább érkeznek; egy föld- vagy hajóroncs `alive` értéke 0, amíg az entitását el nem távolítják, és egy pálya marad; a repülőgépek `alive` értéke legfeljebb 60 s-ig 0 (`selfCheck.wrecks`) |
| Járműváltások | ha egy játékos egysége még élt, amikor ugyanazon játékos következő egysége megjelent, ott véget ér (egy álló, otthagyott jármű). A `selfCheck.vehicleSwitch.twoLiveVehicles` értékének 0-nak kell lennie |
| Csatamód | [Csatamód](ground.md#battle-mode) |
| Repülőgépek 2026-os szerver-visszajátszásban | a 2026-os elrendezésben olvasva; az irány és a dőlés előjele egyezik a fordulatokkal; a helykitöltő repülőgépek és a felderítő drónok nem tartalmaznak adatot |
| Szerver-visszajátszás játékosai | a helyeken név szerint megtalálva; minden statisztika egyezik az eredményekével (`selfCheck.players`) |
| Repülőgépek 2025-ös szerver-visszajátszásokban és a 101286-os verzióban | nincs olvasva: a repülési csomagjaik más elrendezésűek |

## Üzenetek egységeknek {#messages-to-units}

Minden 4-es típusú csomag a Dagor Engine daNet mpi üzenete: a címzett objektum azonosítója,
majd (ha alacsony 11 bitje mind be van állítva) az objektum ext UID-ja, az üzenet azonosítója és
a tartalma. Az egységnek küldött üzenet ext UID-je az egység entitásazonosítója,
`index << 10 | generation`. Ellenőrizve: minden ilyen üzenet olyan entitást nevez meg, amely
abban a pillanatban élt.

A szakembereknek, az olvasott üzenetek:

| Üzenet | Mi, és az ellenőrzés |
|---|---|
| 0xF0E9 UnitHitEffects | egy lövedék találata: a lövő uid-je és a találati pont az egység koordinátarendszerében (x előre, y fel, z balra): centiméterek repülőgépeken és hajókon, földi egységeken 20/32768 m lépésekben (a tank tornyainak méretéhez illesztve). A `hitLocalX/Y/Z` méterben. Egy `shot` sorrá válik ([Lövések](hits.md#gunfire)). Szinte minden találati és ölés-rekord támadója ezen lövők között van; a találati pontok a lövő felé néző oldalon vannak |
| 0xF133 UnitOnExplosion | ugyanaz a lövő uid |
| 0xF04B OnUnitDead | `dead` sorok: minden ölés-rekord áldozatának van egy két másodpercen belül |
| 0xD047 FmwRpm | a motorok fordulatszáma (`rpm`); egyezik a fedélzeti fordulatszámmérővel |
| 0xF0B1, 0xF0A0 | `gun_shot` sorok: a nehéz légvédelem és a tüzérség egyes lövései |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` sorok: 40 mm-es légvédelmi ágyúk sorozatai (egy ágyú lövése; egy járművön lévő tűz `fire_on`, lásd [Járműtüzek](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` sorok |
| 0xD0FE ProjectileHitReplay | a felvevő játékos saját találatai és az ő találatai, fegyverrel és lőszerrel, a telepítésből nevezve (`projectileHitReplays`) |
| 0xF13E, 0xF031 | egy találat vizuális hatása és az egységen lejátszott effekt; ugyanarra az egységre érkező találattal együtt jönnek |
| 0xD041 | repülőgépenként egy védekező ágyúnként, másodpercenként kétszer; indexei egyeznek a repülési modell lövész-fegyvereivel |
| 0xD048, 0xF117 | az elrendezés olvasott, jelentése nem ismert |
| a többi (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | az üzenetek kísérőfájlában, az egységükkel és mezőikkel |

A neveket a közösség adja (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Még olvasva {#also-read}

- **Entitásfolyam-replikáció** (0x22, 0x23): entitásonként komponensértékek blokkja: hajók
  javítási időzítői, fogyóeszközök száma, tulajdonos- és csapatváltások, motortúlhevülés.
  A `counts.replicatedComponents` számolja; az értékek az üzenetek kísérőfájljában vannak.
- **Küldetés-szkript műveletek** (0xF028) és **tippek** (0xF0EC): `triggers`, `hints`.
  **Küldetés-előrehaladás** (0xF07A, 0xF07C): `missionProgress`.
- **A visszajátszás kamerája** (0xD043): lásd [A kamera](ground.md#the-camera).

## Nincs olvasva, és miért {#not-read-and-why}

- **Az entitásüzenetek nevei és törzsei** (0x20, 0x21): az osztályszám a játékba fordított lista
  egy helye, nincs elküldve, és nincs az adataiban. Kettő olvasott (egy jármű tüzei és tűzoltói);
  a többi az entitásával és az osztályszámával együtt, egészben marad meg.
- **Más replikált objektumok** (a játékos-helyektől és csapatoktól eltérő fajták): olvasva és
  megtartva, név nélkül; nincs az eredményekben, amivel ellenőrizni lehetne őket.
- **Más repülőgépek vezérlői, gázkarja és lőszere**: csak néha frissülnek; a repülési kísérőfájlban
  vannak, nem a táblázatban.
- **Repülőgép-tüzek**: egyetlen üzenetben sem találhatók; a tüzes repülőgépnek nincs `fire_on` sora.
- **Kilőtt fegyverek nevei**: egy bomba vagy rakéta entitása nem tartalmaz nevet; az ölés-rekordok
  nevezik meg egy ölés fegyverét.
- **Célt tévesztett lövések**: a visszajátszás csak a találatokat tartalmazza.

Minden meccsdokumentum `counts.messageIdsNotRead` és `selfCheck` mezője elmondja, mit tartalmaz egy
új visszajátszás, és milyen jól lett olvasva.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
