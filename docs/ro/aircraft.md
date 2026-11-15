---
title: Avioane
nav_order: 11
lang: ro
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Avioane {#aircraft}

Pentru cititorii care vor să știe de unde vin coloanele despre avioane și cât de mult să se
aibă încredere în ele. Fiecare verificare de mai jos compară o valoare cu ceva ce spune replay-ul
într-un al doilea mod, independent; sunt date doar metoda și gradul de concordanță.

## Instrumentele din cabină {#cockpit-instruments}

Mesajul 0xD04A trimite indicatoarele jucătorului care înregistrează, ca perechi (număr, valoare):
patru pe secundă în bătăliile arcade, doar valorile schimbate în bătăliile simulator. Numerele
formează o singură listă pentru toate cabinele, iar o cabină trimite indicatoarele pe care le
are modelul ei. Codul jocului stabilește ce număr este ce indicator, deci fiecare număr a fost
numit după ce face și verificat în replay ( `convert.INSTRUMENTS` păstrează rezultatul; nimic nu
este citit din instalare):

| Număr | Nume | Verificat față de |
|---|---|---|
| 0 | viteza indicată, m/s | viteza traseului corectată pentru densitatea aerului: corelație 0,99 |
| 39 | viteza de urcare, m/s | viteza de urcare a traseului: corelație peste 0,99 |
| 40, 41 | altitudine, m; altitudine modulo 1000 | înălțimea traseului, la câțiva metri distanță |
| 52, 53 | rularea și tangajul orizontului artificial | minus rularea și tangajul din tabel, sub 1 grad diferență |
| 64 | busola | direcția din tabel, sub 0,1 grade diferență |
| 15-20 | pedalele de direcție | forța laterală asupra avionului |
| 23, 31 | manșa: profundor și eleroane (semnul ca al modelului de cabină) | unghiul de atac; viteza de rulare |
| 69, 71, 73 | ceasul: ore (cadran de 12 ore), minute, secunde | ora locală a calculatorului de înregistrare, la minut |
| 75 | presiunea din colector, atm | mai mare la putere de urgență de război decât la gaz maxim |
| 81-86, 87-92, 93-98 | turații pe motor, turații modulo 1000, indicatorul de turații | unul față de altul exact; turația motorului: corelație peste 0,97 |
| 195 | combustibil | scade în timpul unui zbor, se umple din nou la o reapariție |
| 228-230 | picioarele trenului de aterizare, 1 coborât | coborât doar aproape de înălțimea aerodromurilor și la viteza de aterizare |
| 240, 241 | accelerația pe motor (1.1 putere de urgență de război sau postardere) | accelerația din intrarea de zbor |
| 330-332, 346-348 | contoarele de muniție (două seturi egale) | rundele presetării armei, scăzând odată cu rundele din intrarea de zbor |
| 135, 159 | temperatura uleiului și a chiulasei | probabil: cresc pe parcursul unui zbor |
| 58, 61 | bila de derapaj, acul de viraj | probabil: urmează forța laterală și viteza de viraj |
| 223 | aerofrâna | probabil: activată doar la apropiere |
| 490-497, 500-505 | frânele roților | probabil: activate doar când stă pe un aerodrom |

Mai sunt trimise câteva numere ale căror sens nu este cunoscut; ele sunt păstrate în
`authorInstruments.notNamed` din documentul meciului.

Coloanele `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` și `throttle` din tabel provin din acestea, din
rândurile proprii ale jucătorului care înregistrează, luând cel mult ultimul mesaj cu 0,2 s înainte
de eșantion.

## Intrările de zbor {#flight-entries}

Intrarea de zbor a fiecărui avion (tipul de pachet 2) conține, pe lângă poziție și atitudine:

- **Viteza**: un cuvânt de 32 de biți după atitudine. Biții 31, 30 și 29 sunt semnele lui x, y și z; apoi
  viteza în 11 biți de 500/2047 m/s (se oprește la 500 m/s), apoi |x| și |y| ca fracții din
  viteză, în câte 9 biți fiecare, iar z este cel care face vectorul un vector unitar. Verificat
  față de pasul dintre eșantioanele primite: direcția concordă în limita unei fracțiuni de grad pentru
  jucătorul care înregistrează și în limita a aproximativ 2 grade pentru ceilalți; viteza, în limita a 0,2 %.
  `selfCheck.flightEntries`.
- **Runde pe armă**: o listă înaintea poziției, câte un element pentru fiecare armă, rundele rămase
  primele. Cea a jucătorului care înregistrează este egală cu contoarele cabinei cu un tic mai târziu pentru
  aproape fiecare eșantion.
- **Comenzi și accelerație**: 7 octeți după viteză, citiți ca 14 semiocteți. Pentru jucătorul care
  înregistrează, la fiecare tic: 1 profundorul, 2 eleroanele, 3 cârma (8 în repaus), 11 accelerația
  în cincisprezecimi (15 și pentru putere de urgență de război și postardere), 4 frânele roților, 5 aerofrâna,
  8 probabil parașuta de frânare. Semiocteții altor avioane se schimbă doar de câteva ori
  într-o bătălie și nu sunt comenzile lor în momentul respectiv.
- **Motoare**: pentru fiecare motor un octet de stare (0 oprit; 1-6 pornire; 7 în funcțiune; 8
  defect), o valoare pe 16 biți doar cu postardere (32767 plin), și un octet doar după ce motorul a fost lovit. Majoritatea
  avioanelor al căror motor ajunge „defect” sunt doborâte sau se termină în câteva minute.

## Date de reflecție {#reflection-data}

Mesajele 0xF02D și 0xF0AA replică obiectele numerotate ale jocului: pentru fiecare obiect
id-ul său (cei 5 biți de sus tipul, cei 11 de jos un index) și un tabel de câmpuri.
Tipul 14 sunt sloturile jucătorilor (câmpul 2 id-ul utilizatorului și numele, 9 echipa),
tipul 15 sunt echipele (indexul 1 și 2):

- Câmpul 39 al unui slot ține statisticile sale la locuri fixe: uciderile (decalaj 0), uciderile
  de echipă (2), morțile (4), uciderile navale (10), uciderile de IA (12), uciderile de IA la sol
  (14), asistențele (20), zonele capturate (22), daunele zonelor (24, pe 32 de biți), premiul pentru
  daune (40, pe 32 de biți), evitările de rachete (50). Câmpul 38 începe cu scorul, câmpul 42 este
  escadrila. La sfârșitul unei bătălii fiecare valoare este egală cu cea din rezultate pentru
  fiecare jucător (`selfCheck.scoreboardVsResults`). Unde sunt păstrate uciderile la sol nu este
  cunoscut.
- Câmpul 7 al unei echipe este scorul ei: la sfârșit este egal cu suma scorurilor jucătorilor ei
  din rezultate. Câmpul 3 este probabil biletele ei.
- Fiecare mesaj trimite doar câmpurile care s-au schimbat, deci `scoreboard` din documentul meciului
  listează statisticile fiecărui jucător și scorul fiecărei echipe la fiecare schimbare.

## Estimarea prin navigare și netezirea {#dead-reckoning-and-the-smoother}

Un replay de client înregistrează fiecare avion de patru ori pe secundă, așa cum l-a desenat clientul. Între
actualizările pe care le primește pentru un avion îndepărtat, clientul îl mută mai departe pe
ultima lui viteză și îl întoarce la ultimele lui viteze unghiulare, iar la următoarea actualizare
îl trage acolo. Citit așa cum este, un traseu merge drept, apoi sare. Nimic din intrarea de zbor
nu marchează ce eșantioane au fost primite; un eșantion estimat prin navigare se recunoaște după ce este:
continuă linia dreaptă a celor două eșantioane dinaintea lui, în ritmul lor, cu o abatere de cel mult 3 cm.

Cât contează asta depinde de bătălie: în bătăliile arcade aproximativ jumătate din
eșantioanele celorlalte avioane pot fi estimate prin navigare, în bătăliile simulator
doar câteva procente. Netezirea taie pașii peste 15 g de aproximativ cinci
ori (`selfCheck.deadReckoning`). Avionul jucătorului care înregistrează nu este extrapolat de client
și rămâne cum este.

Implicit (`--no-smoothing` îl oprește) traseele tuturor unităților, în afară de cele ale jucătorului
care înregistrează, sunt puse acolo unde le spun stările primite că au fost: un eșantion estimat prin navigare
merge pe o curbă prin eșantioanele primite dinainte și de după el, fiecare cu propria viteză; pe
mai mult de 3 s linia dreaptă este doar îndoită spre următorul eșantion primit, deci niciun eșantion nu
se mută mai departe decât trage clientul însuși. Atitudinea sa este întoarsă uniform de la o
atitudine primită la următoarea. Eșantioanele primite sunt netezite cu cel mult 2 m
sau 0,04 s din viteza lor; un viraj constant rămâne cum este. Valorile proprii ale replay-ului
rămân în coloanele `Raw`.

## Atitudinea, verificată {#attitude-checked}

La avionul jucătorului care înregistrează, cursul se află în limita unui grad (mediana) față de direcția
de deplasare, tangajul în limita a câtorva grade față de unghiul de urcare, iar în virajele clare
rularea are semnul virajului pentru aproape fiecare eșantion: modelul de zbor
dă rularea cu aripa stângă în jos pozitivă, iar tabelul o întoarce la aripa dreaptă în jos
pozitivă (`selfCheck.aircraftAttitude`). Unghiurile pe 10 biți au pași de 0,18 grade. Atitudinea
unităților terestre este verificată față de loviturile lor ([Turele](ground.md#turrets)).

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
