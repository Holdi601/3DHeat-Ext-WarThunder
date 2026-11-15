---
title: "Földi egységek és kamera"
nav_order: 12
lang: hu
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Földi egységek és kamera {#ground-units-and-camera}

Azoknak, akik tudni szeretnék, honnan származnak a torony-, kamera- és csatamód-oszlopok,
és mennyire bízhatnak bennük. Az ellenőrzések csak a módszert és az egyezést adják meg.

## Tornyok {#turrets}

Egy tank földi állapota (16 bites állás) a helyzete után 141 nem olvasott bitet tartalmaz,
majd tornyonként 62 bitet: a torony elfordulását és az ágyú emelkedését (16-16 bit,
360/65536 fokonként lépve, előjeles), és 30 nem olvasott bitet; utána kitöltés, és egyes
állapotoknál további 200 bit. A tornyok száma az állapot előtt küldött bájt. Az olyan
állapot, amelynek a hossza nem illik, nem ad tornyot (a helyhez kötött egységek rövidebb
állapotot küldenek). Az elfordulás a törzshöz képest értendő, az óramutató járásával
megegyezően pozitív, 0 egyenesen előre; az emelkedés a törzshöz képest, felfelé pozitív.

Így ellenőriztük:

- **A lövésekkel:** minden tank általi találatnál az ágyújának világbeli iránya (a törzs
  állása elfordítva a torony elfordulásával és az ágyú emelkedésével) összevetve a lövő és
  az eltalált egység közötti egyenessel, legalább 30 m távolságnál: csatánként mediánban
  körülbelül 98 % 3 fokon belül iránynál és 99 % emelkedésnél (`selfCheck.turretsVsShots`).
  A többi főként géppuska-találat egy másik toronyból.
- **A felvevő játékos céljával:** a saját tankja elküldi a célzása világbeli szögét (keletről
  óramutató ellenében), emelkedését és távolságát. A törzs iránya plusz a torony elfordulása
  fél fokon belül (medián) egyezik a céllal.

**Szerver-visszajátszások** (0xF074) minden tank állapotát ugyanazzal az elrendezéssel küldik,
utána saját adataikkal, ezért minden olyan torony olvasódik, amelynek két szöge az állapoton
belül van (szinte minden tanksornál legalább a fő torony). Ez a torony, nem a kamera:

- **A lövésekkel**, az előbbiek szerint: csatánként 90 % felett 3 fokon belül iránynál és
  99 % emelkedésnél.
- **A nézettel:** a szerver-visszajátszás minden játékos célzását elküldi (`viewYaw`,
  `viewPitch`). A torony fél fokon belül követi a nézetet (medián), de sokkal lassabban fordul,
  mint ahogy a nézet mozog, ahogy egy toronyhajtás teszi (`selfCheck.turretVsView`).
- **De nem mindig a hajtás sebességével:** mintánként az elküldött érték néha ugrik a célzásra,
  ha a célzás az ágyú közelében van, gyorsabban, mint ahogy bármely hajtás fordul.

Ezért a táblázat a tornyot **a hajtásához kötve** tartja: a `turretYaw` / `gunPitch` legfeljebb
a fő ágyú fordulási sebességével mozog az elküldött érték felé, a telepítés járműfájljából
(szorozva 1,3-mal a legénység képzettségéhez és a módosításokhoz; ha a telepítés nem nevez
meg, 45 és 20 fok másodpercenként). A fő ágyú minden találatánál a torony pontosan a lövés
vonalára kerül, és egy visszafelé haladó menet időben odaér (`selfCheck.turretLimit`). A
`shot` sor is tartalmazza ezt a `turretYaw` / `gunPitch` értéket. Az elküldött érték a
`turretYawRaw` / `gunPitchRaw` oszlopokban marad meg. Az a tank, amelynek állapota nem
tartalmaz tornyot, üres toronyoszlopokat kap (a megjelenítő visszaeshet a `viewYaw` értékre).
A `gunPitch` távolságnál kissé a `viewPitch` fölött van: az ágyú emelkedése a lövedék
ejtéséhez.

A hajók állapota más elrendezésű; a tornyaikat nem olvassuk. A repülőgépek nem küldenek
fej- vagy nézeti irányt; a légvédelmi ágyúk 0xD020 üzenete olvasatlan marad.

## A kamera {#the-camera}

A 0xD043 üzenet, másodpercenként körülbelül 20, a felvevő játékos saját visszajátszás-kamerája:
az 1-es mező egy kvaterniót, amely a kamera előre nézését fordítja arra, amerre néz; a 2-es a
kamera helye a követett járműhöz képest (m); a 4-es ugyanez az eltolás a jármű saját
koordinátarendszerében (x előre, y fel, z balra); az 5-ös, hová céloz a játékos (egységvektor);
a 3-as a zoom (körülbelül 1,2 a tank harmadik személyű nézetében, körülbelül 1,0 repülőgépben,
magasabb egy lövész célkeresőjében vagy távcsőnél). Ellenőrizve: a 4-es mező a 2-es mező a jármű
koordinátarendszerébe fordítva, szinte minden üzenetnél 0,5 m-en belül; a kamera előre irányának
iránya egyezik a célzás irányával. A visszajátszás nem küld fokban megadott látómezőt, csak a zoomot.

A táblázatban a kamerának saját pályája van: fajtája `camera`, pályája `<player> camera #ca`,
legfeljebb 0,1 másodpercenként egy sor, a követett jármű helyén plusz a 2-es mező értékével,
a kvaterniót követve (`dirX/Y/Z`, `heading`, `pitch`, `roll`), a `zoom`, `aimHeading` és
`aimPitch` mezőkkel, és az `otherLife` mezővel, amely azt az életet adja, amelyet követ.
A `selfCheck.camera` számolja a sorokat és az ellenőrzést.

## Egy pálya vége {#end-of-a-track}

Egy pálya az első sorától az utolsójáig rajzolódik. Ha az egysége még a visszajátszás vége
előtt eltűnik, az utolsó sora egy `despawn` sor az utolsó helyén: abban az időben, amikor
a játék eltávolította az entitását (ha ez az utolsó mintájától 6 s-on belül volt), különben
az utolsó mintájánál. A sor nélküli pálya a visszajátszás végéig tart. Egy pálya sorai messze
lehetnek egymástól (egy távoli egységet vagy roncsot néhány másodpercenként frissítenek, a
roncsot néha percekig nem): az utolsó állapota addig marad érvényben, amíg nem jön a következő sora.

## Csatamód {#battle-mode}

A fejléc 688. bájtja az alacsony négy bitjében tartja a nehézségi szintet: 0 arcade (AB),
5 realisztikus (RB), 10 szimulátor (SB). Ellenőrizve azokkal a csatatípusokkal, amelyekről tudni
lehetett, mik voltak a visszajátszások. A játékmód `ground`, ha a küldetés tankok megjelenését
engedi, különben `naval`, ha hajókat, különben `air` (`allowedUnitTypes`); a küldetés saját
módja a kulcsából jön (`missions/_Dom`), a telepítésed `lang/missions_versus.csv` fájljából
nevezve meg. Ugyanez a kulcs adja a fájlnevek `<mode>` részét és a meccsazonosítót (`Conq4`,
`Dom`), és kimarad, ahol a fejlécben nincs.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
