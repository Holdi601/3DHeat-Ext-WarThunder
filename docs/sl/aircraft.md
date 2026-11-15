---
title: Letala
nav_order: 11
lang: sl
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Letala {#aircraft}

Za bralce, ki želijo vedeti, od kod prihajajo stolpci letal in kako zaupanja vredni so. Vsako preverjanje
spodaj primerja vrednost z nečim, kar posnetek pove na drugi, neodvisen način; podana sta samo metoda in
skladnost.

## Instrumenti v kabini {#cockpit-instruments}

Sporočilo 0xD04A pošilja merilnike igralca, ki je posnetek snemal, kot pare (številka, vrednost): štirikrat na
sekundo v arkadnih bitkah, v simulatorskih bitkah samo spremenjene vrednosti. Številke tvorijo en seznam za vse
kabine, kabina pa pošilja merilnike, ki jih ima njen model. Igrina koda določi, katera številka je kateri merilnik,
zato je bila vsaka številka poimenovana po tem, kaj počne, in preverjena s posnetkom (`convert.INSTRUMENTS` hrani
rezultat; iz namestitve se nič ne bere):

| Številka | Ime | Preverjeno z |
|---|---|---|
| 0 | prikazana zračna hitrost, m/s | hitrostjo poti, popravljeno za gostoto zraka: korelacija 0,99 |
| 39 | hitrost vzpenjanja, m/s | hitrostjo vzpenjanja poti: korelacija nad 0,99 |
| 40, 41 | višina, m; višina modulo 1000 | višino poti, nekaj metrov narazen |
| 52, 53 | valj umetnega horizonta in naklon | minus valj in naklon tabele, manj kot 1 stopinja narazen |
| 64 | kompas | smer tabele, manj kot 0,1 stopinje narazen |
| 15-20 | pedali krmila smeri | stranska sila na letalo |
| 23, 31 | palica: višinsko krmilo in krilca (predznak kot pri modelu kabine) | kot napada; hitrost zvijanja |
| 69, 71, 73 | ura: ure (12-urna številčnica), minute, sekunde | lokalni čas računalnika, ki je snemal, na minuto natančno |
| 75 | tlak v sesalni cevi, atm | višji pri vojnem nujnem režimu kot pri polnem plinu |
| 81-86, 87-92, 93-98 | vrtljaji na motor, vrtljaji modulo 1000, merilnik vrtljajev | med seboj natanko; vrtljaji motorja: korelacija nad 0,97 |
| 195 | gorivo | pada skozi bojni let, ob ponovnem pojavu spet polno |
| 228-230 | nogi podvozja, 1 spuščeno | spuščeno samo blizu višine letališč in pri hitrosti pristanka |
| 240, 241 | plin na motor (1,1 vojni nujni režim ali post-zgorevanje) | plin vnosa letenja |
| 330-332, 346-348 | števci streliva (dva enaka niza) | naboji prednastavitve orožja, ki padajo z naboji vnosa letenja |
| 135, 159 | temperatura olja in glave valjev | verjetno: naraščata skozi bojni let |
| 58, 61 | kroglica zdrsa, igla zavoja | verjetno: sledita stranski sili in hitrosti zavijanja |
| 223 | zračna zavora | verjetno: nastavljena samo pri prilaganju |
| 490-497, 500-505 | zavore koles | verjetno: nastavljene samo, ko stoji na letališču |

Pošilja se še nekaj številk, katerih pomen ni znan; shranjene so v `authorInstruments.notNamed` dokumenta tekme.

Stolpci tabele `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` in
`throttle` izhajajo iz teh, na lastnih vrsticah igralca, ki je snemal, z zadnjim sporočilom največ 0,2 s po vzorcu.

## Vnosi letenja {#flight-entries}

Vnos letenja vsakega letala (vrsta paketa 2) poleg položaja in drže nosi:

- **Hitrost**: 32-bitna beseda za držo. Biti 31, 30 in 29 so predznaki x, y in z; nato hitrost v 11 bitih po
  500/2047 m/s (ustavi se pri 500 m/s), nato |x| in |y| kot deleža hitrosti v 9 bitih vsak, z pa iz tega naredi
  enotski vektor. Preverjeno s korakom med prejetimi vzorci: smer se ujema znotraj delčka stopinje za igralca,
  ki je snemal, in znotraj približno 2 stopinj za vse druge; hitrost znotraj 0,2 %. `selfCheck.flightEntries`.
- **Naboji po orožju**: seznam pred položajem, en element na orožje, najprej preostali naboji. Pri igralcu, ki je
  snemal, se pri skoraj vsakem vzorcu enakovredno ujema s števci v kabini eno takt kasneje.
- **Krmiljenje in plin**: 7 bajtov za hitrostjo, prebranih kot 14 nibblov. Za igralca, ki je snemal, vsak takt: 1
  višinsko krmilo, 2 krilca, 3 krmilo smeri (8 v mirovanju), 11 plin v petnajstinah (15 tudi za vojni nujni režim
  in post-zgorevanje), 4 zavore koles, 5 zračna zavora, 8 verjetno zavorni padalo. Nibbli drugih letal se spremenijo
  le nekajkrat v bitki in v tistem času niso njihovo krmiljenje.
- **Motorji**: za vsak motor bajt stanja (0 izklopljen; 1-6 se zaganja; 7 teče; 8 mrtev), 16-bitna vrednost samo pri
  post-zgorevanju (32767 polno) in bajt samo potem, ko je bil motor zadet. Večina letal, katerih motor preide v
  "mrtev", je uničenih ali konča v nekaj minutah.

## Podatki o refleksiji {#reflection-data}

Sporočili 0xF02D in 0xF0AA replicirata številčne predmete igre: za vsak predmet njegov identifikator (zgornjih 5
bitov vrsta, spodnjih 11 indeks) in tabelo polj. Vrsta 14 so reže igralcev (polje 2 uporabniški id in ime, 9 ekipa),
vrsta 15 ekipe (indeks 1 in 2):

- Polje 39 reže hrani njeno statistiko na stalnih mestih: ubijanja (zamik 0), ubijanja v ekipi (2), smrti (4),
  pomorska ubijanja (10), ubijanja AI (12), ubijanja kopenskih AI (14), pomoči (20), območja zajema (22), poškodbe
  območij (24, 32-bitno), nagrada za poškodbe (40, 32-bitno), izogibanja raketam (50). Polje 38 se začne z
  rezultatom, polje 42 je odred. Ob koncu bitke je vsaka vrednost enaka tisti iz rezultatov za vsakega igralca
  (`selfCheck.scoreboardVsResults`). Kje so shranjena kopenska ubijanja, ni znano.
- Polje 7 ekipe je njen rezultat: ob koncu je enako vsoti rezultatov njenih igralcev v rezultatih. Polje 3 so verjetno
  njene vstopnice.
- Vsako sporočilo pošlje samo polja, ki so se spremenila, zato `scoreboard` v dokumentu tekme navaja statistiko
  vsakega igralca in rezultat vsake ekipe ob vsaki spremembi.

## Mrtvo računanje in zglajevalnik {#dead-reckoning-and-the-smoother}

Posnetek odjemalca snema vsako letalo štirikrat na sekundo, tako kot ga je odjemalec narisal. Med posodobitvami, ki jih
prejme za oddaljeno letalo, ga odjemalec premika naprej vzdolž zadnje hitrosti in ga vrti z zadnjimi hitrostmi vrtenja,
ob naslednji posodobitvi pa ga skoči na pravo mesto. Prebran kot je, potek gre naravnost, nato skoči. Nič v vnosu
letenja ne označi, kateri vzorci so bili prejeti; vzorec, izračunan z mrtvim računanjem, se prepozna po tem, kakšen je:
nadaljuje ravno črto dveh vzorcev pred njim, v njunem tempu, na 3 cm natančno.

Koliko je to pomembno, je odvisno od bitke: v arkadnih bitkah je mogoče približno polovico vzorcev drugih letal
izračunati z mrtvim računanjem, v simulatorskih bitkah le nekaj odstotkov. Zglajevalnik zmanjša skoke nad 15 g približno
petkrat (`selfCheck.deadReckoning`). Lastnega letala igralca, ki je snemal, odjemalec ne ekstrapolira in ostane, kot je.

Privzeto (`--no-smoothing` to izklopi) so poti vseh enot razen lastnih enot igralca, ki je snemal, postavljene tja, kjer
jih prejeta stanja kažejo: vzorec, izračunan z mrtvim računanjem, gre po krivulji skozi prejete vzorce pred njim in za
njim, vsak s svojo hitrostjo; čez več kot 3 s se ravna črta samo upogne proti naslednjemu prejetemu vzorcu, tako da se
noben vzorec ne premakne dlje od lastnega poskoka odjemalca. Njegova drža se enakomerno obrne od enega prejetega
položaja do naslednjega. Prejeti vzorci se zgladijo največ za 2 m ali 0,04 s njihove hitrosti; enakomeren zavoj ostane
tak, kot je. Lastne vrednosti posnetka ostanejo v stolpcih `Raw`.

## Preverjena drža {#attitude-checked}

Na lastnem letalu igralca, ki je snemal, je smer znotraj stopinje (mediana) smeri leta, naklon znotraj nekaj stopinj
kota vzpenjanja, v jasnih zavojih pa ima zvitek predznak zavoja pri skoraj vsakem vzorcu: zvitek modela leta je pozitiven
pri levem krilu navzdol, tabela ga obrne v pozitiven pri desnem krilu navzdol (`selfCheck.aircraftAttitude`). 10-bitni
koti korakajo po 0,18 stopinje. Drža kopenskih enot se preveri z njihovimi streli ([Strelski stolpi](ground.md#turrets)).

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
