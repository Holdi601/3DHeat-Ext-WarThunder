---
title: Obiective
nav_order: 15
lang: "ro"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Obiective {#objectives}

`objectives` din documentul meciului listează pentru ce se luptă bătălia, din două surse (`source`):

- **Replay-ul** (`replay`): obiectele misiunii pe care le numește 0xD039 (zonele de capturare `cz_circle_NN`, aerodromurile, helipadurile,
  bazele), plasate acolo unde obiectele replicate de tipul 3 (0xF02D) le pun acum - o zonă de capturare începe la locul șablonului său și este mutată la zona acestui mod la început (`moved`). Numerele tipului 3 urmează ordinea lui 0xD039;
  fiecare obiect care nu este mutat stă exact unde îl are 0xD039, ceea ce verifică ordinea. O zonă de capturare primește
  forma și raza zonei de misiune la locul său (`area`, în 2 m) și litera sa după propriul index (tipul
  5 câmpul 69: 0 = A); ordinea literelor este cea a replay-ului, nefiind verificată față de harta jocului.
- **Misiunea** (`mission`): fișierul misiunii `<mission>.blk` din `mis.vromfs.bin` al instalării dumneavoastră și șabloanele
  pe care le importă (doar citire, la conversie): zonele sale, clasificate după nume - punctele de apariție (punctele numerotate ale unei apariții `..._spawnareaNN` ca o singură apariție `points`), zonele de luptă, ținte de bombardament (`bomb_zone`), puncte de apariție ale convoaielor (`road_NN_spawn`), zone de ieșire și de ucidere. Zonele altui mod al aceleiași hărți (`conq_`, `dom_`, `bttl_`,
  ...) sunt lăsate afară, iar dintre variantele `_arcade` / `_realistic` / `_hardcore` cea proprie bătăliei (RB ia `_realistic`, altfel `_hardcore`, cum fac scripturile misiunii); markerii de briefing, punctele tunurilor antiaeriene și zonele mai late de 5 km (cele peste care sunt împrăștiate aparițiile) la fel. Fiecare apariție spune câte trasee ale jucătorilor au început în ea (`used`,
  `usedByTeam`). O misiune își poate schimba aleatoriu părțile (`randomSpawnTeams`): când aparițiile arată echipele replay-ului invers, fiecare `team` este schimbat și partea numelui este păstrată ca `missionTeam`. Rutele convoaielor nu sunt în punctele de drum ale misiunilor așa cum sunt citite; se dă doar acolo unde apar convoaie.

Zonele de capturare în timp sunt fișierul auxiliar `<match>.objectives.parquet`: obiectele replicate de tipul 5, câte unul per zonă - câmpul 2 proprietarul său (0, 1, 2), câmpul 67 progresul capturării, un octet cu semn de la -100 la 100 (pozitiv spre echipa 2), câmpul 69 indexul său. Verificat (`selfCheck.objectives`) pe replay-uri de server terestre ale bătăliilor Conquest și Domination: fiecare schimbare de proprietar vine cu un jucător al echipei care capturează câștigând un `captureZone` în tabela de scor în același moment (în 1,5 s) și cu o unitate terestră vie a acelei echipe în zonă; aparițiile fiecărei bătălii arată echipele replay-ului într-un singur fel (adesea invers față de `t1_` / `t2_` ale misiunii).

## Unități de scenă: tramvaie și vagoane de cale ferată {#scene-units-trams-and-rail-wagons}

Un nivel poate plasa unități proprii: entitățile `unit_loader+rail_wagon` ale unui replay de server sunt tramvaiele fișierului de scenă al nivelului (`gamedata/scenes/<level>_objects.blk` din `aces.vromfs.bin`: `setting__unit_class`, transformarea sa și `setting__isDead`). Entitățile lor nu poartă un uid citibil, deci un traseu terestru fără entitate de unitate al cărui prim eșantion se află în 2 m de o unitate de scenă este acea unitate: clasa sa ca `Vehicle`, tipul `train`, felul `tram`, `locomotive` sau `wagon`, fără echipă; o unitate pe care scena o plasează moartă (cum sunt tramvaiele arse) este o epavă (`alive` 0) de la primul său rând. Jocul nu are un nume în engleză pentru ele; `VehicleName` este id-ul citit ca cuvinte („Railway tram A”). Pozițiile lor nu oscilează: aproape niciuna nu se mișcă vreodată (fiecare eșantion identic până la bit). Replay-ul le trimite de aproximativ zece ori pe secundă oricum, deci din eșantioanele lor sunt păstrate doar cele care le mută (0,05 m sau 0,1 grade), și unul la 10 s (`selfCheck.sceneUnits` numără eșantioanele lăsate). Înainte, erau trasee numite `uid 8` fără vehicul.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
