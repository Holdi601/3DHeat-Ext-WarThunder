---
title: "Avioni"
nav_order: 11
lang: bs
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Avioni {#aircraft}

Za čitaoce koji žele znati odakle dolaze kolone aviona i koliko im
vjerovati. Svaka provjera ispod upoređuje vrijednost s nečim što
replay kaže na drugi, nezavisan način; daju se samo metoda i slaganje.

## Instrumenti kokpita {#cockpit-instruments}

Poruka 0xD04A šalje mjerače igrača koji snima kao parove (broj, vrijednost):
četiri u sekundi u arkadnim bitkama, samo promijenjene vrijednosti u simulatorskim
bitkama. Brojevi čine jednu listu preko svih kokpita, a kokpit šalje
mjerače koje njegov model ima. Kod igre određuje koji je broj koji mjerač,
pa je svaki broj imenovan prema onome što radi i provjeren prema replayu
(`convert.INSTRUMENTS` drži rezultat; ništa se ne čita iz instalacije):

| Broj | Ime | Provjereno prema |
|---|---|---|
| 0 | indicirana brzina, m/s | brzina staze ispravljena za gustoću zraka: korelacija 0,99 |
| 39 | brzina penjanja, m/s | brzina penjanja staze: korelacija iznad 0,99 |
| 40, 41 | visina, m; visina modulo 1000 | visina staze, razlika nekoliko metara |
| 52, 53 | vještački horizont roll i pitch | minus roll i pitch tabele, razlika manja od 1 stepena |
| 64 | kompas | heading tabele, razlika manja od 0,1 stepena |
| 15-20 | papučice kormila | bočna sila na avion |
| 23, 31 | palica: elevator i aileroni (predznak kao u modelu kokpita) | napadni ugao; brzina valjanja |
| 69, 71, 73 | sat: sati (12-satni brojčanik), minute, sekunde | lokalno vrijeme računara koji snima, na minutu tačno |
| 75 | pritisak u usisnoj grani, atm | veći pri ratnoj nužnoj snazi nego pri punom gasu |
| 81-86, 87-92, 93-98 | okretaji po motoru, okretaji modulo 1000, mjerač okretaja | međusobno tačno; okretaji motora: korelacija iznad 0,97 |
| 195 | gorivo | pada tokom izlaska, ponovo puno pri respawnu |
| 228-230 | noge stajnog trapa, 1 je izvučen | izvučen samo blizu visine aerodroma i pri brzini slijetanja |
| 240, 241 | gas po motoru (1,1 ratna nužna snaga ili naknadno sagorijevanje) | gas unosa leta |
| 330-332, 346-348 | brojači municije (dva jednaka skupa) | meci zadane konfiguracije oružja, padaju s mecima unosa leta |
| 135, 159 | temperatura ulja i glave cilindra | vjerovatno: rastu tokom izlaska |
| 58, 61 | kuglica klizanja, igla zavoja | vjerovatno: prate bočnu silu i brzinu zavoja |
| 223 | zračna kočnica | vjerovatno: postavljena samo pri prilazu |
| 490-497, 500-505 | kočnice točkova | vjerovatno: postavljene samo dok stoji na aerodromu |

Šalje se još nekoliko brojeva čije značenje nije poznato; čuvaju se u
`authorInstruments.notNamed` dokumenta meča.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` i `throttle` tabele dolaze odavde, na
vlastitim redovima igrača koji snima, uzimajući zadnju poruku najviše 0,2 s poslije
uzorka.

## Unosi leta {#flight-entries}

Unos leta svakog aviona (paket tipa 2) nosi, osim pozicije
i stava:

- **Brzina**: 32-bitna riječ poslije stava. Bitovi 31, 30 i 29 su
  predznaci x, y i z; zatim brzina u 11 bitova od 500/2047 m/s (staje na
  500 m/s), zatim |x| i |y| kao razlomci brzine u po 9 bitova, a z
  je ono što vektor čini jediničnim. Provjereno prema koraku između
  primljenih uzoraka: smjer se slaže unutar djelića stepena za
  igrača koji snima i unutar oko 2 stepena za sve ostale; brzina
  unutar 0,2 %. `selfCheck.flightEntries`.
- **Meci po oružju**: lista prije pozicije, jedna stavka po oružju,
  preostali meci prvi. Lista igrača koji snima jednaka je brojačima kokpita
  jedan otkucaj kasnije za gotovo svaki uzorak.
- **Komande i gas**: 7 bajtova poslije brzine, čitaju se kao 14 nibble-ova.
  Za igrača koji snima, svaki otkucaj: 1 elevator, 2 aileroni, 3
  kormilo (8 u mirovanju), 11 gas u petnaestinama (15 i za ratnu
  nužnu snagu i naknadno sagorijevanje), 4 kočnice točkova, 5 zračna kočnica, 8
  vjerovatno padobran za kočenje. Nibble-ovi drugih aviona mijenjaju se samo nekoliko puta
  tokom bitke i nisu njihove komande u tom trenutku.
- **Motori**: po motoru bajt stanja (0 isključen; 1-6 pokreće se; 7 radi; 8
  mrtav), 16-bitna vrijednost samo s naknadnim sagorijevanjem (32767 puno), i bajt samo
  nakon što je motor pogođen. Većina aviona čiji motor postane „mrtav“
  biva ubijena ili završi unutar nekoliko minuta.

## Podaci refleksije {#reflection-data}

Poruke 0xF02D i 0xF0AA repliciraju numerirane objekte igre: po objektu
njegov id (gornjih 5 bitova vrsta, donjih 11 indeks) i tabelu polja.
Vrsta 14 su igrački slotovi (polje 2 id korisnika i ime, 9 tim), vrsta 15
timovi (indeks 1 i 2):

- Polje 39 slota drži njegove statistike na fiksnim mjestima: ubistva (pomak 0),
  ubistva u timu (2), smrti (4), pomorska ubistva (10), AI ubistva (12), AI kopnena
  ubistva (14), asistencije (20), zone zauzimanja (22), šteta zonama (24, 32-bitno),
  nagrada za štetu (40, 32-bitno), izbjegnute rakete (50). Polje 38 počinje
  bodovima, polje 42 je odred. Na kraju bitke svaka vrijednost jednaka je
  onoj iz rezultata za svakog igrača (`selfCheck.scoreboardVsResults`). Gdje
  se čuvaju kopnena ubistva nije poznato.
- Polje 7 tima je njegov rezultat: na kraju jednako je zbiru
  rezultata njegovih igrača u rezultatima. Polje 3 su vjerovatno njegovi tiketi.
- Svaka poruka šalje samo polja koja su se promijenila, pa `scoreboard` u
  dokumentu meča navodi statistike svakog igrača i rezultat svakog tima pri
  svakoj promjeni.

## Dead reckoning i glatkač {#dead-reckoning-and-the-smoother}

Klijentski replay snima svaki avion četiri puta u sekundi, onako kako ga je
klijent crtao. Između ažuriranja koja prima za udaljeni avion, klijent ga
pomjera dalje duž njegove zadnje brzine i okreće ga zadnjim brzinama okretanja, a
pri sljedećem ažuriranju ga trzajem postavlja tamo. Pročitana takva kakva jeste, staza ide ravno,
pa skoči. Ništa u unosu leta ne označava koji su uzorci primljeni;
dead-reckoned uzorak prepoznaje se po tome šta jeste: nastavlja ravnu
liniju dva uzorka prije sebe, njihovim tempom, na 3 cm tačno.

Koliko je to važno zavisi od bitke: u arkadnim bitkama oko polovina
uzoraka drugih aviona može biti dead-reckoned, u simulatorskim bitkama
samo nekoliko procenata. Glatkač smanjuje korake preko 15 g otprilike pet
puta (`selfCheck.deadReckoning`). Klijent ne ekstrapolira vlastiti avion igrača koji snima
pa on ostaje kakav jeste.

Zadano (`--no-smoothing` to isključuje) staze svih jedinica osim vlastite
jedinice igrača koji snima postavljaju se tamo gdje kažu primljena stanja da su bile: dead-reckoned
uzorak ide na krivulju kroz primljene uzorke prije i poslije njega,
svaki sa svojom brzinom; preko više od 3 s ravna linija se samo savija prema sljedećem primljenom uzorku, pa se nijedan uzorak ne pomjera
dalje od vlastitog trzaja klijenta. Njegov stav se ravnomjerno okreće od jednog
primljenog stava do sljedećeg. Primljeni uzorci se glade najviše za 2 m
ili 0,04 s njihove brzine; stalni zavoj ostaje kakav jeste. Vlastite
vrijednosti replaya ostaju u kolonama `Raw`.

## Stav, provjeren {#attitude-checked}

Na vlastitom avionu igrača koji snima heading leži unutar stepena
(medijan) smjera kretanja, pitch unutar nekoliko stepena ugla
penjanja, a u jasnim zavojima roll ima predznak zavoja za gotovo svaki uzorak:
roll modela leta je pozitivan kad je lijevo krilo dolje, a tabela ga okreće u
pozitivan kad je desno krilo dolje (`selfCheck.aircraftAttitude`).
10-bitni uglovi se mijenjaju korakom od 0,18 stepeni. Stav kopnenih jedinica provjerava se
prema njihovim hicima ([Kupole](ground.md#turrets)).

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
