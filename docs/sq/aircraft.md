---
title: "Aeroplanët"
nav_order: 11
lang: "sq"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Aeroplanët {#aircraft}

Për lexuesit që duan të dinë nga vijnë kolonat e aeroplanëve dhe sa
mund t'u besohet. Çdo kontroll më poshtë e krahason një vlerë me diçka që
riluajtja e thotë në një mënyrë të dytë, të pavarur; jepen vetëm metoda dhe përputhja.

## Instrumentet e kabinës {#cockpit-instruments}

Mesazhi 0xD04A dërgon matësit e lojtarit që regjistron si çifte (numër, vlerë):
katër në sekondë në betejat arcade, vetëm vlerat e ndryshuara në betejat simulator.
Numrat formojnë një listë për të gjitha kabinat, dhe një kabinë dërgon
matësit që ka modeli i saj. Kodi i lojës përcakton cili numër është cili matës,
kështu që çdo numër u emërtua sipas asaj që bën dhe u kontrollua ndaj riluajtjes
(`convert.INSTRUMENTS` mban rezultatin; asgjë nuk lexohet nga instalimi):

| Numri | Emri | Kontrolluar ndaj |
|---|---|---|
| 0 | shpejtësia e treguar, m/s | shpejtësia e gjurmës e korrigjuar për densitetin e ajrit: korrelacion 0.99 |
| 39 | shpejtësia e ngjitjes, m/s | shpejtësia e ngjitjes e gjurmës: korrelacion mbi 0.99 |
| 40, 41 | lartësia, m; lartësia modul 1000 | lartësia e gjurmës, disa metra larg |
| 52, 53 | roll dhe pitch i horizontit artificial | minus roll dhe pitch i tabelës, nën 1 gradë larg |
| 64 | busulla | heading i tabelës, nën 0.1 gradë larg |
| 15-20 | pedalet e timonit | forca anësore mbi aeroplanin |
| 23, 31 | stick: elevator dhe ailerons (shenja si e modelit të kabinës) | këndi i sulmit; shpejtësia e rrotullimit |
| 69, 71, 73 | ora: orët (cifërblat 12-orësh), minutat, sekondat | ora lokale e kompjuterit që regjistron, deri në minutë |
| 75 | presioni i manifoldit, atm | më i lartë në fuqi emergjente lufte se në gaz të plotë |
| 81-86, 87-92, 93-98 | rpm për motor, rpm modul 1000, matësi i rpm | njëri me tjetrin saktësisht; rpm i motorit: korrelacion mbi 0.97 |
| 195 | karburanti | bie gjatë një misioni, plot përsëri në një ripërtëritje |
| 228-230 | këmbët e trapit të uljes, 1 poshtë | poshtë vetëm pranë lartësisë së fushave ajrore dhe në shpejtësi ulje |
| 240, 241 | gazi për motor (1.1 fuqi emergjente lufte ose afterburner) | gazi i hyrjes së fluturimit |
| 330-332, 346-348 | numëruesit e municionit (dy bashkësi të barabarta) | predhat e presetit të armëve, që bien me predhat e hyrjes së fluturimit |
| 135, 159 | temperatura e vajit dhe e kokës së cilindrave | ndoshta: ngrihen gjatë një misioni |
| 58, 61 | topi i rrëshqitjes, gjilpëra e kthesës | ndoshta: ndjekin forcën anësore dhe shpejtësinë e kthesës |
| 223 | airbrake | ndoshta: vendoset vetëm në afrim |
| 490-497, 500-505 | frenat e rrotave | ndoshta: vendosen vetëm kur qëndron në një fushë ajrore |

Dërgohen edhe disa numra të tjerë kuptimi i të cilëve nuk dihet; ruhen te
`authorInstruments.notNamed` i dokumentit të ndeshjes.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` dhe `throttle` të tabelës vijnë nga këto, në
rreshtat e vetë lojtarit që regjistron, duke marrë mesazhin e fundit më së shumti 0.2 s pas
mostrës.

## Hyrjet e fluturimit {#flight-entries}

Hyrja e fluturimit e çdo aeroplani (lloji i paketës 2) mbart, përveç pozicionit
dhe qëndrimit të tij:

- **Shpejtësia**: një fjalë 32-bitëshe pas qëndrimit. Bitët 31, 30 dhe 29 janë
  shenjat e x, y dhe z; pastaj shpejtësia në 11 bit prej 500/2047 m/s (ndalet te
  500 m/s), pastaj |x| dhe |y| si pjesë të shpejtësisë me nga 9 bit, dhe z
  është ajo që e bën vektorin vektor njësi. Kontrolluar ndaj hapit midis
  mostrave të marra: drejtimi përputhet brenda një pjese të gradës për
  lojtarin që regjistron dhe brenda rreth 2 gradësh për të gjithë të tjerët; shpejtësia
  brenda 0.2 %. `selfCheck.flightEntries`.
- **Predhat për armë**: një listë para pozicionit, një element për armë,
  me predhat e mbetura të parat. Ajo e lojtarit që regjistron është e barabartë me numëruesit
  e kabinës një tik më vonë për pothuajse çdo mostër.
- **Kontrollet dhe gazi**: 7 bajtë pas shpejtësisë, të lexuar si 14 nibble.
  Për lojtarin që regjistron, çdo tik: 1 elevator, 2 ailerons, 3
  timoni (8 në prehje), 11 gazi në të pesëmbëdhjetat (15 edhe për fuqi
  emergjente lufte dhe afterburner), 4 frenat e rrotave, 5 airbrake, 8
  ndoshta parashuta frenuese. Nibble-t e aeroplanëve të tjerë ndryshojnë vetëm disa herë në një
  betejë dhe nuk janë kontrollet e tyre në atë kohë.
- **Motorët**: për motor një bajt gjendjeje (0 off; 1-6 starting; 7 running; 8
  dead), një vlerë 16-bitëshe vetëm me afterburner (32767 plot), dhe një bajt vetëm
  pasi motori u godit. Shumica e aeroplanëve, motori i të cilëve bëhet "dead",
  vriten ose mbarojnë brenda minutash.

## Të dhënat e reflektimit {#reflection-data}

Mesazhet 0xF02D dhe 0xF0AA replikojnë objektet e numërtuara të lojës: për objekt
ID e tij (5 bitët e sipërm lloji, 11 të poshtmit një indeks) dhe një tabelë fushash.
Lloji 14 janë vendet e lojtarëve (fusha 2 ID e përdoruesit dhe emri, 9 skuadra), lloji 15
skuadrat (indeksi 1 dhe 2):

- Fusha 39 e një vendi mban statistikat e tij në vende fikse: vrasje (offset 0),
  vrasje të skuadrës (2), vdekje (4), vrasje detare (10), vrasje AI (12), vrasje
  tokësore AI (14), ndihma (20), zona kapjeje (22), dëm zone (24, 32-bit),
  çmim dëmi (40, 32-bit), shmangie raketash (50). Fusha 38 fillon me
  pikët, fusha 42 është skuadra. Në fund të betejës çdo vlerë është e barabartë me
  atë të rezultateve për çdo lojtar (`selfCheck.scoreboardVsResults`). Ku
  mbahen vrasjet tokësore nuk dihet.
- Fusha 7 e një skuadre është pikët e saj: në fund është e barabartë me shumën e
  pikëve të lojtarëve të saj në rezultate. Fusha 3 është ndoshta biletat e saj.
- Çdo mesazh dërgon vetëm fushat që ndryshuan, kështu që `scoreboard` në
  dokumentin e ndeshjes liston statistikat e çdo lojtari dhe pikët e çdo skuadre në
  çdo ndryshim.

## Dead reckoning dhe zbutësi {#dead-reckoning-and-the-smoother}

Një riluajtje klienti regjistron çdo aeroplan katër herë në sekondë, siç e vizatoi
klienti. Midis përditësimeve që merr për një aeroplan të largët, klienti
e lëviz përgjatë shpejtësisë së tij të fundit dhe e kthen me shpejtësitë e tij të fundit të kthimit, dhe
në përditësimin tjetër e kap atje. Siç lexohet, një gjurmë shkon drejt,
pastaj kërcen. Asgjë në hyrjen e fluturimit nuk shënon cilat mostra u morën;
një mostër me dead reckoning gjendet nga ajo që është: vazhdon vijën e drejtë
të dy mostrave para saj, me ritmin e tyre, brenda 3 cm.

Sa ka rëndësi kjo varet nga beteja: në betejat arcade rreth gjysma
e mostrave të aeroplanëve të tjerë mund të jenë me dead reckoning, në betejat simulator
vetëm disa përqind. Zbutësi i pret hapat mbi 15 g afërsisht pesë
herë (`selfCheck.deadReckoning`). Aeroplani i vetë lojtarit që regjistron
nuk ekstrapolohet nga klienti dhe lihet siç është.

Si parazgjedhje (`--no-smoothing` e çaktivizon) gjurmët e të gjitha njësive përveç atyre të
lojtarit që regjistron vendosen aty ku thonë gjendjet e marra se ishin: një
mostër me dead reckoning shkon në një kurbë përmes mostrave të marra para
dhe pas saj, secila me shpejtësinë e vet; mbi më shumë se 3 s vija e
drejtë përkulet vetëm drejt mostrës së marrë të radhës, kështu që asnjë mostër nuk lëviz
më larg se kapja e vetë klientit. Qëndrimi i saj kthehet njëtrajtësisht nga një
qëndrim i marrë te tjetri. Mostrat e marra zbuten më së shumti me 2 m
ose 0.04 s të shpejtësisë së tyre; një kthesë e qëndrueshme mbetet siç është. Vlerat e vetë riluajtjes
mbeten në kolonat `Raw`.

## Qëndrimi, i kontrolluar {#attitude-checked}

Në aeroplanin e vetë lojtarit që regjistron, heading shtrihet brenda një grade
(mediana) të drejtimit të udhëtimit, pitch brenda disa gradësh të
këndit të ngjitjes, dhe në kthesa të qarta roll ka shenjën e kthesës për pothuajse
çdo mostër: roll i modelit të fluturimit është krahu i majtë poshtë pozitiv, dhe
tabela e kthen në krahu i djathtë poshtë pozitiv (`selfCheck.aircraftAttitude`).
Këndet 10-bitëshe hapen 0.18 gradë. Qëndrimi i njësive tokësore kontrollohet
ndaj të shtënave të tyre ([Kupolat](ground.md#turrets)).

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
