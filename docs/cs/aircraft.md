---
title: "Letadla"
nav_order: 11
lang: cs
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Letadla {#aircraft}

Pro čtenáře, kteří chtějí vědět, odkud se berou sloupce letadel a jak moc jim věřit. Každá kontrola níže porovnává
hodnotu s něčím, co replay říká jiným, nezávislým způsobem; uvádí se jen metoda a míra shody.

## Palubní přístroje {#cockpit-instruments}

Zpráva 0xD04A posílá ručičky přístrojů hráče, který nahrával, jako dvojice (číslo, hodnota): čtyřikrát za vteřinu
v arkadových bitvách, v simulátoru jen měněné hodnoty. Čísla tvoří jeden seznam přes všechny kokpity a kokpit posílá
ty ručičky, které jeho model má. Kód hry určuje, které číslo je která ručička, takže každé číslo bylo pojmenováno podle
toho, co dělá, a ověřeno proti replayi (`convert.INSTRUMENTS` výsledek drží; nic se nečte z instalace):

| Číslo | Název | Ověřeno proti |
|---|---|---|
| 0 | indikovaná vzdušná rychlost, m/s | rychlost trati opravená o hustotu vzduchu: korelace 0,99 |
| 39 | rychlost stoupání, m/s | rychlost stoupání trati: korelace nad 0,99 |
| 40, 41 | výška, m; výška modulo 1000 | výška trati, o několik metrů |
| 52, 53 | náklon a sklon umělého horizontu | mínus náklon a sklon z tabulky, o méně než 1 stupeň |
| 64 | kompas | kurz z tabulky, o méně než 0,1 stupně |
| 15-20 | pedály kormidla | boční síla na letadlo |
| 23, 31 | páka: výškovka a křidélka (znaménko jako u modelu kokpitu) | úhel náběhu; rychlost náklonu |
| 69, 71, 73 | hodiny: hodiny na 12hodinovém číselníku, minuty, vteřiny | místní čas počítače, který nahrával, na minutu přesně |
| 75 | tlak v sání, atm | vyšší na válečném nouzovém výkonu než na plném plynu |
| 81-86, 87-92, 93-98 | otáčky na motor, otáčky modulo 1000, ručička otáček | navzájem přesně; otáčky motoru: korelace nad 0,97 |
| 195 | palivo | klesá během výletu, po respawnu opět plné |
| 228-230 | nohy podvozku, 1 = vysunuto | vysunuto jen blízko výšky letiště a při rychlosti přistání |
| 240, 241 | plyn na motor (1,1 válečný nouzový výkon nebo přídavné spalování) | plyn ze záznamu letu |
| 330-332, 346-348 | počítadla munice (dvě stejné sady) | náboje sestavy zbraní, klesající s náboji ze záznamu letu |
| 135, 159 | teplota oleje a hlavy válců | pravděpodobně: rostou během výletu |
| 58, 61 | kulička skluzu, ručička zatáčky | pravděpodobně: sledují boční sílu a rychlost zatáčení |
| 223 | vzduchové brzdy | pravděpodobně: nastaveny jen při přiblížení |
| 490-497, 500-505 | kola brzd | pravděpodobně: nastaveny jen na stojícím letadle na letišti |

Posílá se ještě několik čísel, jejichž význam není znám; uchovávají se v `authorInstruments.notNamed` dokumentu
zápasu.

Sloupce tabulky `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` a `throttle`
pocházejí odsud, z řádků samotného hráče, který nahrával; bere se poslední zpráva nejvýš 0,2 s před vzorkem.

## Záznamy letu {#flight-entries}

Záznam letu každého letadla (typ paketu 2) nese kromě polohy a postoje:

- **Rychlost**: 32bitové slovo za postojem. Bity 31, 30 a 29 jsou znaménka x, y a z; pak rychlost v 11 bitech
  po 500/2047 m/s (zastaví se na 500 m/s), potom |x| a |y| jako zlomky rychlosti po 9 bitech, a z je to, co dělá
  vektor jednotkovým. Ověřeno proti kroku mezi přijatými vzorky: směr souhlasí do zlomku stupně pro hráče, který
  nahrával, a do asi 2 stupňů pro ostatní; rychlost do 0,2 %. `selfCheck.flightEntries`.
- **Náboje na zbraň**: seznam před polohou, jedna položka na zbraň, nejdřív zbývající náboje. U hráče, který
  nahrával, se téměř u každého vzorku rovná počítadlům v kokpitu o jeden tik později.
- **Ovládání a plyn**: 7 bajtů za rychlostí, čteno jako 14 půlbajtů. U hráče, který nahrával, v každém tiku:
  1 výškovka, 2 křidélka, 3 kormidlo (8 v klidu), 11 plyn v patnáctinách (15 také pro válečný nouzový výkon
  a přídavné spalování), 4 kola brzd, 5 vzduchové brzdy, 8 pravděpodobně brzdicí padák. Půlbajty ostatních letadel
  se mění jen několikrát za bitvu a nejsou jejich ovládáním v daném okamžiku.
- **Motory**: pro každý motor stavový bajt (0 vypnutý; 1-6 startuje; 7 běží; 8 mrtvý), 16bitová hodnota jen
  s přídavným spalováním (32767 plně) a bajt jen poté, co byl motor zasažen. Většina letadel, jejichž motor přejde
  do stavu „mrtvý“, je sestřelena nebo skončí během minut.

## Data odrazu {#reflection-data}

Zprávy 0xF02D a 0xF0AA replikují očíslované objekty hry: u každého objektu jeho id (horních 5 bitů druh, spodních
11 index) a tabulku polí. Druh 14 jsou sloty hráčů (pole 2 uživatelské id a jméno, 9 tým), druh 15 týmy (index 1 a 2):

- Pole 39 slotu hráče drží jeho statistiky na pevných místech: zabití (posun 0), zabití spojenců (2), smrti (4),
  námořní zabití (10), zabití AI (12), zabití pozemní AI (14), asistence (20), zóny dobytí (22), poškození zón
  (24, 32bitové), odměna za poškození (40, 32bitové), uniknuté střely (50). Pole 38 začíná skóre, pole 42 je
  squad. Na konci bitvy se každá hodnota rovná hodnotě z výsledků pro každého hráče
  (`selfCheck.scoreboardVsResults`). Kde se drží zabití pozemních jednotek, není známo.
- Pole 7 týmu je jeho skóre: na konci se rovná součtu skóre jeho hráčů ve výsledcích. Pole 3 jsou pravděpodobně
  jeho body (tickets).
- Každá zpráva posílá jen pole, která se změnila, takže `scoreboard` v dokumentu zápasu vypisuje statistiky každého
  hráče a skóre každého týmu při každé změně.

## Odhad polohy (dead reckoning) a vyhlazování {#dead-reckoning-and-the-smoother}

Replay klienta zaznamenává každé letadlo čtyřikrát za vteřinu tak, jak ho klient vykreslil. Mezi aktualizacemi,
které klient pro vzdálené letadlo dostane, klient letadlo posune dál podle jeho poslední rychlosti a otočí ho podle
posledních úhlových rychlostí, a při další aktualizaci ho přeskočí na místo. Čte-li se to tak, jak je, trať jde
rovně a pak skočí. Nic v záznamu letu neoznačuje, které vzorky byly přijaty; vzorek odhadnutý z polohy se pozná podle
toho, jaký je: pokračuje v přímce dvou předchozích vzorků, jejich tempem, na 3 cm přesně.

Záleží na bitvě: v arkadových bitvách může být odhadnuta asi polovina vzorků ostatních letadel, v simulátoru jen
několik procent. Vyhlazovač zkracuje skoky nad 15 g asi pětkrát (`selfCheck.deadReckoning`). Vlastní letadlo hráče,
který nahrával, klient neextrapoluje, a zůstává tak, jak je.

Ve výchozím nastavení (`--no-smoothing` to vypne) jsou tratě všech jednotek kromě vlastní jednotky hráče, který
nahrával, umístěny tam, kde podle přijatých stavů byly: odhadnutý vzorek jde po křivce mezi přijatými vzorky před
ním a za ním, každý se svou rychlostí; přes více než 3 s se přímka jen ohne směrem k dalšímu přijatému vzorku, takže
žádný vzorek se neposune dál než vlastní skok klienta. Jeho postoj se rovnoměrně otáčí od jednoho přijatého postoje
k dalšímu. Přijaté vzorky se vyhlazují nejvýš o 2 m nebo 0,04 s jejich rychlosti; ustálená zatáčka zůstane, jaká je.
Hodnoty samotného replaye zůstávají ve sloupcích `Raw`.

## Postoj, ověřený {#attitude-checked}

U vlastního letadla hráče, který nahrával, leží kurz do jednoho stupně (medián) od směru letu, sklon do několika stupňů
od úhlu stoupání a v jasných zatáčkách má náklon u téměř každého vzorku znaménko zatáčky: náklon modelu letu je
kladný, když levé křídlo je dole, a tabulka ho převádí na kladný, když pravé křídlo je dole
(`selfCheck.aircraftAttitude`). 10bitové úhly se mění po 0,18 stupně. Postoj pozemních jednotek se ověřuje proti
jejich výstřelům ([Věže](ground.md#turrets)).

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
