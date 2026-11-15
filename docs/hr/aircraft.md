---
title: Zrakoplovi
nav_order: 11
lang: "hr"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Zrakoplovi {#aircraft}

Za čitatelje koji žele znati odakle dolaze stupci zrakoplova i koliko im vjerovati. Svaka provjera
ispod uspoređuje vrijednost s nečim što snimka kaže na drugi, neovisan način; daju se samo metoda i
slaganje.

## Instrumenti u kabini {#cockpit-instruments}

Poruka 0xD04A šalje instrumente igrača koji snima kao parove (broj, vrijednost): četiri u sekundi u
arkadnim bitkama, samo promijenjene vrijednosti u simulacijskim bitkama. Brojevi čine jedan popis za
sve kabine, a kabina šalje instrumente koje njezin model ima. Igrin kod određuje koji je broj koji
instrument, pa je svaki broj imenovan prema tome što radi i provjeren prema snimci
(`convert.INSTRUMENTS` sadrži rezultat; ništa se ne čita iz instalacije):

| Broj | Naziv | Provjereno prema |
|---|---|---|
| 0 | indicirana brzina, m/s | brzini putanje ispravljenoj za gustoću zraka: korelacija 0,99 |
| 39 | brzina penjanja, m/s | brzini penjanja putanje: korelacija iznad 0,99 |
| 40, 41 | visina, m; visina modulo 1000 | visini putanje, nekoliko metara razlike |
| 52, 53 | umjetni horizont, nagib u krilu i nagib | minus valjanje i nagib tablice, razlika manja od 1 stupnja |
| 64 | kompas | smjeru iz tablice, razlika manja od 0,1 stupnja |
| 15-20 | pedale kormila | bočnoj sili na zrakoplov |
| 23, 31 | palica: visina i krilca (predznak kao u modelu kabine) | napadnom kutu; brzini valjanja |
| 69, 71, 73 | sat: sati (brojčanik s 12 sati), minute, sekunde | lokalnom vremenu računala koje je snimalo, na minutu |
| 75 | tlak usisne grane, atm | višem pri ratnom pojačanju nego pri punom gasu |
| 81-86, 87-92, 93-98 | okretaji po motoru, okretaji modulo 1000, brojčanik okretaja | međusobno točno; okretajima motora: korelacija iznad 0,97 |
| 195 | gorivo | pada tijekom izlaska, ponovno puno pri ponovnom pojavljivanju |
| 228-230 | noge podvozja, 1 spušteno | spušteno samo blizu visine aerodroma i pri brzini slijetanja |
| 240, 241 | gas po motoru (1,1 ratno pojačanje ili naknadno izgaranje) | gasu iz unosa leta |
| 330-332, 346-348 | brojači streljiva (dva jednaka skupa) | broju metaka iz unaprijed postavljenog oružja, koji pada s mecima iz unosa leta |
| 135, 159 | temperatura ulja i glave cilindra | vjerojatno: rastu tijekom izlaska |
| 58, 61 | kuglica klizanja, igla zaokreta | vjerojatno: prate bočnu silu i brzinu zaokreta |
| 223 | zračna kočnica | vjerojatno: postavljena samo pri prilaženju |
| 490-497, 500-505 | kočnice kotača | vjerojatno: postavljene samo dok stoji na aerodromu |

Šalje se još nekoliko brojeva čije značenje nije poznato; čuvaju se u
`authorInstruments.notNamed` dokumenta meča.

Stupci tablice `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` i `throttle` dolaze iz ovih, na redcima samog igrača koji snima, uzimajući najviše
jednu poruku najviše 0,2 s nakon uzorka.

## Unosi leta {#flight-entries}

Unos leta svakog zrakoplova (vrsta paketa 2) nosi, osim položaja i stava:

- **Brzina**: 32-bitna riječ iza stava. Bitovi 31, 30 i 29 su predznaci x, y i z; zatim brzina u 11
  bitova po 500/2047 m/s (staje na 500 m/s), zatim |x| i |y| kao udjeli brzine u po 9 bitova, a z je
  ono što čini vektor jediničnim. Provjereno prema koraku između primljenih uzoraka: smjer se slaže unutar
  djelića stupnja za igrača koji snima i unutar oko 2 stupnja za sve ostale; brzina unutar 0,2 %.
  `selfCheck.flightEntries`.
- **Metaka po oružju**: popis prije položaja, jedna stavka po oružju, prvo broj preostalih metaka.
  Onaj igrača koji snima jednak je brojačima kabine jedan takt kasnije za gotovo svaki uzorak.
- **Upravljanje i gas**: 7 bajtova iza brzine, čitano kao 14 poluzalogaja. Za igrača koji snima, svaki
  takt: 1 visina, 2 krilca, 3 kormilo (8 u mirovanju), 11 gas u petnaestinama (15 i za ratno pojačanje i
  naknadno izgaranje), 4 kočnice kotača, 5 zračna kočnica, 8 vjerojatno padobran za kočenje. Poluzalogaji
  drugih zrakoplova mijenjaju se samo nekoliko puta u bitci i nisu njihovo upravljanje u tom trenutku.
- **Motori**: po motoru bajt stanja (0 isključen; 1-6 pokretanje; 7 radi; 8 mrtav), 16-bitna vrijednost
  samo uz naknadno izgaranje (32767 puno), i bajt samo nakon što je motor bio pogođen. Većina zrakoplova
  čiji motor pređe u "mrtav" bude uništena ili završi unutar nekoliko minuta.

## Podaci o refleksiji {#reflection-data}

Poruke 0xF02D i 0xF0AA repliciraju brojčane objekte igre: po objektu njegov id (gornjih 5 bitova vrsta,
donjih 11 indeks) i tablica polja. Vrsta 14 su slotovi igrača (polje 2 korisnički id i ime, 9 tim),
vrsta 15 timovi (indeks 1 i 2):

- Polje 39 slota drži njegovu statistiku na fiksnim mjestima: ubojstva (pomak 0), ubojstva saveznika (2),
  smrti (4), pomorska ubojstva (10), ubojstva AI-ja (12), ubojstva AI-ja na kopnu (14), asistencije (20),
  zone zauzimanja (22), šteta u zoni (24, 32-bitna), nagrada za štetu (40, 32-bitna), izbjegnute rakete
  (50). Polje 38 počinje s bodovima, polje 42 je odred. Na kraju bitke svaka vrijednost jednaka je
  onoj iz rezultata za svakog igrača (`selfCheck.scoreboardVsResults`). Nije poznato gdje se čuvaju
  ubojstva na kopnu.
- Polje 7 tima su njegovi bodovi: na kraju je jednako zbroju bodova njegovih igrača iz rezultata. Polje 3
  je vjerojatno njegova karta s brojem tiketa.
- Svaka poruka šalje samo polja koja su se promijenila, pa `scoreboard` u dokumentu meča navodi statistiku
  svakog igrača i bodove svakog tima pri svakoj promjeni.

## Mrtvi račun i izglađivač {#dead-reckoning-and-the-smoother}

Snimka klijenta bilježi svaki zrakoplov četiri puta u sekundi, onako kako ga je klijent nacrtao. Između
ažuriranja koja dobije za udaljeni zrakoplov, klijent ga pomakne dalje duž njegove zadnje brzine i
zakrene ga na zadnjim brzinama, a pri sljedećem ažuriranju ga prebaci na mjesto. Pročitana onakva kakva
jest, putanja ide ravno, pa skoči. Ništa u unosu leta ne označava koji su uzorci primljeni; uzorak mrtvog
računa prepoznaje se po tome što jest: nastavlja ravnu liniju dvaju uzoraka prije njega, njihovim tempom,
unutar 3 cm.

Koliko je to važno ovisi o bitci: u arkadnim bitkama oko polovice uzoraka drugih zrakoplova može biti
mrtvi račun, u simulacijskim bitkama samo nekoliko posto. Izglađivač smanjuje skokove preko 15 g oko pet
puta (`selfCheck.deadReckoning`). Zrakoplov igrača koji snima klijent ne ekstrapolira, pa ostaje kakav jest.

Prema zadanom (`--no-smoothing` to isključuje) putanje svih jedinica osim vlastitog zrakoplova igrača
koji snima postavljaju se tamo gdje ih primljena stanja kažu da su bila: uzorak mrtvog računa ide krivuljom
kroz primljene uzorke prije i poslije njega, svaki sa svojom brzinom; tijekom više od 3 s ravna linija se
samo savija prema sljedećem primljenom uzorku, pa se nijedan uzorak ne pomakne dalje od klijentova vlastitog
skoka. Njegov stav se ravnomjerno zakreće od jednog primljenog stava do sljedećeg. Primljeni uzorci se
izglađuju najviše 2 m ili 0,04 s njihove brzine; ustaljeni zaokret ostaje kakav jest. Izvorne vrijednosti
snimke ostaju u stupcima `Raw`.

## Stav, provjereno {#attitude-checked}

Na vlastitom zrakoplovu igrača koji snima smjer leži unutar jednog stupnja (medijan) od smjera kretanja,
nagib unutar nekoliko stupnjeva od kuta penjanja, a u jasnim zaokretima valjanje ima predznak zaokreta za
gotovo svaki uzorak: valjanje modela leta je lijevo krilo dolje pozitivno, a tablica ga pretvara u desno
krilo dolje pozitivno (`selfCheck.aircraftAttitude`). Kutovi od 10 bitova koračaju po 0,18 stupnja. Stav
kopnenih jedinica provjerava se prema njihovim hicima ([Tornjevi](ground.md#turrets)).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
