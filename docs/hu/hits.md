---
title: "Találatok, lövések és tüzek"
nav_order: 13
lang: hu
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Találatok, lövések és tüzek {#hits-gunfire-and-fires}

Azoknak, akik tudni szeretnék, honnan származnak a találat-, lőszer- és tűz-oszlopok.
Az ellenőrzések csak a módszert és az egyezést adják meg.

## Lövések {#gunfire}

Minden lövedék, amely egy egységet eltalált, benne van a visszajátszásban (0xF0E9 üzenet): a
`shot` sor a lövő helyén a találat pillanatában, a `targetX/Y/Z` a találati pont (az
eltalált egység, a találati ponttal eltolva a saját koordinátarendszerében, elforgatva az
állásával), az arra mutató irány, és az `other` az eltalált egység. A célt tévesztett
lövedékek és lövések nem kerülnek elküldésre: nem entitások, és a repülő fegyverek üzenetei
csak rakétákat, bombákat és torpedókat tartalmaznak. A felvevő játékos kilőtt
lövedékei (az `ammo` oszlop) lövés közben csökkennek, így a sorozatai megkülönböztethetők,
de az nem, hová mentek ezek a lövedékek. A nehéz légvédelem és a tüzérség minden egyes lövést
külön küld (`gun_shot`, irány nélkül), a 40 mm-es légvédelmi ágyúk a sorozataikat
(`fire_start`, `fire_stop`).

## Találatok kimenetele {#hit-outcomes}

Minden lövedéktalálatnál a szerver a 0xF144 üzenetet (UnitOnHit) küldi az egységnek: négy
egybájtos mező, a negyedik azoknak a biteknek a halmaza, amit a találat tett
(`selfCheck.unitMessages.outcome_*`):

| Bit | Jelentés | Bizonyíték |
|---|---|---|
| 0x20 | a lövedék saját találata | szinte mindegyik öt ms-on belül egy 0xF0E9 találattal jár az egységen; ha nincs, robbanással jár (szilánk) |
| 0x01 | átütött (áthatolás) | minden olyan üzenet, amelyen 0x02, 0x04 vagy 0x08 van, ezt is tartalmazza |
| 0x02 | kritikus találat | a legtöbb kritikus-találat-rekordon megvan, sokkal gyakrabban, mint a véletlen szerint |
| 0x04 | megsemmisült | a legtöbb egy ölés-rekorddal és az egység halálával jár egy másodpercen belül |
| 0x08 | súlyos sérülés | néhány kritikus-találat-rekordon van; egyébként ritka |

A `hitOutcome` a legrosszabbat veszi: `kill` (0x04), `critical` (0x02 vagy 0x08),
`penetration` (0x01), `nonpenetration` (csak 0x20). Egy találatot a hozzá legközelebbi,
párosítatlan, 0x20-as 0xF144 üzenettel párosítjuk, amely öt ms-on belül ugyanarra az
egységre érkezett. A játék találati kamerája megkülönbözteti a ricochet-et (pattanás) az
át nem ütéstől, de az itt talált egyetlen bit vagy mező sem: az első három bájt találatról
találatra változik, és nem ismert. A kliens-visszajátszások a 0xF144 üzenetet csak a felvevő
játékos saját repülőgépére küldik, minden bit nulla: a repülőgép- és hajótalálatoknak nincs kimenetele.

## Lőszer {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Robbanó-e.** Az a lövedék, amely felrobban, a 0xF133 (UnitOnExplosion) üzenetet küldi a
  lövő uid-jével és a találat számával; a vele járó találat `explosive`, a többi `kinetic`.
* **Az ágyú és a rekesz.** A 0xF0BD (UnitBulletRearm) a következőként betöltött lövedék: a
  fegyver indexe a jármű fegyverlistájában, a lőszerrekesz és a hátralévő lövedékek.
  Egy kézi töltőé minden találata után egy állandó újratöltési idővel érkezik, egy
  automata ágyúé a másodperc egy töredékével később. A lövő találatait jármű, jel és sorozat
  szerint csoportosítjuk; egy csoport akkor egy fegyveré, ha az a fegyver a találatok
  legalább felének után 20 s-on belül állandó késéssel tölt be egy lövedéket. Az `ammoSlot`
  a `fegyver/rekesz`, a találat előtt betöltött rekesz: valószínűleg az, amelyet kilőttek,
  kivéve, ha a játékos közben változtatott a lőszeren. A géppuskák nem küldenek 0xF0BD üzenetet.
* **A lövedék.** Egy ölés fegyvere a lövedék azonosítója (`125mm_3bm46`); a gyilkos utolsó
  találata az áldozaton ezt a lövő rekeszéhez rendeli, ahol az ágyú kalibere egyezik. Típusa
  és kalibere a fegyverfájlból való (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS,
  `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **A többi kaliber:** a rekesz fegyveréé; a géppuska-csoporté az egyetlen géppuska-kaliber,
  amely a jelének lehet; különben a jármű főágyúé. A telepítés (`--game`) nélkül a
  `explosive` / `kinetic` értéken túl nincs típus, név vagy kaliber.

Nem található: a ricochet. Több további üzenet is tartalmazza a találat lövőjét és számát
(0xF0C2, valószínűleg a találati kamera útja a járművön keresztül; 0xF117, 0xF13C, 0xF13E);
ezek a kísérőfájlban maradnak, nincsenek dekódolva. Az át nem ütés `nonpenetration` marad.

## Járműtüzek {#vehicle-fires}

Egy égő járművet minden kliens lát: a szerver a járműnek egy entitásüzenetet küld (esemény
`0a519c58`), amely felsorolja a rajta égő tüzeket, minden alkalommal, amikor a lista változik.
Tüzenként: két 16 bites azonosító (a második egy sérülésmodell-csomópont), a fajtája, és -1,
amíg a tűz meg nem fogott. Egy találat által meggyújtott tűz kap egy üzenetet is arról a pontról,
ahol ég, a jármű koordinátarendszerében (x előre, y fel, z balra).

Sorok: `fire_on`, amikor egy tűz megjelenik a listán; `fire_off`, amikor eltűnik, a járművön,
a `fireId`-vel (`first:node`), a `fireKind`-del, és egy találat által meggyújtott tűz esetén a
`fireLocalX/Y/Z` (előre, fel, jobbra) értékkel. Miután a jármű megsemmisült, a listáját gyakran
nem küldik el újra: a tüzei a roncsával érnek véget, különben az entitásával, különben a
visszajátszással (`selfCheck.fires`).

Ellenőrizve: valahányszor egy tank tűzoltójainak száma csökkent, egy tűz egy másodperc töredéke
alatt kikerült a listájáról; a legtöbb tűzpont ugyanazon az oldalon van a járműnek, mint az a
találat, amely meggyújtotta. A fajták számok; hogy mit neveznek meg, nem ismert, és azt sem,
melyik csomópont melyik részt jelöli. A repülőgépek nem küldenek ilyen listát: a tüzes
repülőgép nem olvasható.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
