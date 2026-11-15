---
title: Cum citește un replay
nav_order: 10
lang: "ro"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Cum citește un replay {#how-it-reads-a-replay}

Această pagină este pentru oamenii care vor să știe ce citește convertorul, cum a fost
verificat și cât de mult să se aibă încredere în fiecare coloană. Nu aveți nevoie de ea ca să convertiți replay-uri.

Citirea a fost verificată pe replay-uri de client din bătălii aeriene arcade, aeriene simulator și
navale, pe replay-uri de server din bătălii terestre și, pentru aranjamentele din 2025,
pe replay-urile publice de exemplu ale [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Fiecare verificare compară o valoare cu ceva ce spune replay-ul într-un al doilea mod,
independent; aici sunt date doar metoda și gradul de concordanță.

## Ce se citește, și verificarea {#what-is-read-and-the-check}

| Parte | Stare, și verificarea |
|---|---|
| Antetul, harta, misiunea, ora de start, sesiunea; rezultatele | fiecare fișier |
| Setările misiunii (blk-ul de după antet) | mod, vreme, limite, `stars` (data, ora, locul) |
| Fluxul de pachete (zlib în 2025, zstd în 2026) | fiecare pachet încadrat |
| Pozițiile și atitudinea avioanelor (aranjamentul din 2026) | 4 eșantioane pe secundă, niciun pachet necitit; cursul concordă cu direcția de deplasare |
| Pachete de zbor înaintea timpului lor | după o întrerupere de rețea, pachetul de zbor al unui replay de client ține uneori fiecare alt avion acolo unde va fi cu aproximativ 0,75 s mai târziu. Avansul se măsoară pe pachet, iar fiecare avion care avansează primește momentul pe care îl reprezintă (`selfCheck.flightPacketsRetimed`) |
| Salturile de navigare prin estimare (dead reckoning) | un pas dintr-o serie estimată este măsurat de la ultima stare primită, deci corecțiile clientului nu mai taie traseele ([Estimarea prin navigare](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportări | un traseu este tăiat unde unitatea sa se mută mai departe decât poate: mai întâi față de tipul ei (avion 750 m/s, teren și nave 40 m/s, arme 1800 m/s), apoi față de propriul ritm. Fiecare tăiere este listată în `trackBreaks` cu cauza ei probabilă (reapariție, jocul mutând jucătorul, o corecție a unei unități depărtate). După tăieri, niciun pas între rândurile unui traseu nu este mai rapid decât permite tipul său (`selfCheck.stepSpeed`) |
| Pozițiile terestre și ale navelor (0xF073 / 0xF074) | niciun pachet necitit. Cap, înclinare și rulare din atitudinea pe 16 biți: cursul concordă cu direcția de deplasare în limita a aproximativ 2 grade (mediană); înclinarea numără 180/65536 grade un pas; cu semnul rulării întors, direcția tunului din caroserie și turelă indică unitatea lovită pentru aproape fiecare lovitură de tanc. Navele stau la nivelul apei |
| Turele | rotirea turelei și înclinarea tunului tancurilor: vedeți [Turele](ground.md#turrets) |
| Înălțimile terestre împachetate | pozițiile împachetate în 64 de biți își numără înălțimea de la -100 m pe majoritatea nivelurilor și de la nivelul apei pe unele; decalajul se măsoară pe fiecare replay din unități văzute în ambele forme (`selfCheck.packedGroundHeight`) |
| Fluxul de entități (creare, distrugere) | fiecare creare citită. Aranjamentul vine din codul publicat al Dagor Engine; tipurile de componente proprii War Thunder sunt sărite prin găsirea locului unde începe următoarea componentă. Vehiculul și slotul de jucător al fiecărei unități sunt egale cu cele pe care le numesc înregistrările de ucidere și lovitură, pentru fiecare înregistrare verificată |
| Cine a condus ce unitate, unitățile IA, navele, țintele terestre | din fluxul de entități: fiecare unitate are vehiculul și echipa sa, unitatea fiecărui jucător are jucătorul său |
| Uciderile față de rezultate | morțile pe jucător sunt egale cu cele din rezultate; rezultatele numără mai multe ucideri, deoarece clientul nu primește fiecare ucidere. Un replay care pornește după ce bătălia a început ține doar uciderile de după acel moment |
| Uciderile, loviturile critice, avariile grave | fiecare fișier |
| Module distruse (0xF118) | unitatea și numărul piesei; numele piesei are nevoie de modelul de avariere al vehiculului, care nu este în replay |
| Arme eliberate (fluxul de entități) | punctul de eliberare este la aproximativ 10-20 m (mediană) de cea mai apropiată unitate, care se consideră lansatorul |
| Arme în zbor (0xF0DB) | rachete ghidate, rachete și bombe, fiecare legată de entitatea sa |
| Bombe fără înregistrări de zbor | o bombă fără ele își primește căderea calculată de la eliberare până la impact (gravitație și tracțiune, un eșantion la 0,1 s, `extrapolated` true). Verificat peste mare, unde înălțimea impactului este cunoscută: căderile calculate se termină în limita a aproximativ 15 m de apă. În documentul meciului o asemenea armă are `ballisticImpact`; `counts.bombsBallistic` le numără |
| Sloturile jucătorilor, chatul | fiecare fișier |
| Explozii, rafale de flak, premii, detectări, vreme, obiecte de misiune | citite; pozițiile verificate cu ochiul în vizualizator |
| Indicatoarele jucătorului care înregistrează (0xD04A) | numite după ce fac: [Instrumentele din cabină](aircraft.md#cockpit-instruments); restul sub `notNamed` |
| Celelalte câmpuri ale intrărilor de zbor | viteza, rundele, comenzile, motoarele: [Intrările de zbor](aircraft.md#flight-entries) |
| Atitudinea rândurilor de eveniment | fiecare rând de eveniment poartă cursul, înclinarea, rularea și vectorul de privire ale unității sale în acel moment |
| Statisticile jucătorilor și scorurile echipelor | la sfârșitul bătăliei fiecare statistică este egală cu cea din rezultate pentru fiecare jucător: [Date de reflecție](aircraft.md#reflection-data) |
| Numele armelor și vehiculelor | din localizarea în engleză a instalării dumneavoastră; câteva centuri implicite ale navelor și radarele aerodromurilor nu au nume în joc |
| Jucătorii și IA | niciun rând al unui jucător din rezultate nu este IA, fiecare rând care nu este IA este un jucător din rezultate (`selfCheck.identity`) |
| Epavele | eșantioanele unei unități după moartea sa continuă să vină; epava unei unități terestre sau a unei nave este `alive` 0 până când entitatea sa este scoasă și rămâne un singur traseu; avioanele păstrează `alive` 0 cel mult 60 s (`selfCheck.wrecks`) |
| Schimbările de vehicul | o unitate a unui jucător încă vie când apare următoarea unitate a aceluiași jucător este încheiată acolo (un vehicul lăsat în picioare). `selfCheck.vehicleSwitch.twoLiveVehicles` trebuie să fie 0 |
| Modul de bătălie | [Modul de bătălie](ground.md#battle-mode) |
| Avioane într-un replay de server din 2026 | citite în aranjamentul din 2026; cursul și semnul rulării concordă cu virajele; avioanele de substituție și dronele de recunoaștere nu poartă date |
| Jucătorii unui replay de server | găsiți după nume în sloturi; fiecare statistică este egală cu cea din rezultate (`selfCheck.players`) |
| Avioane în replay-urile de server din 2025 și versiunea 101286 | necitite: pachetele lor de zbor au alt aranjament |

## Mesaje către unități {#messages-to-units}

Fiecare pachet de tip 4 este un mesaj mpi al daNet al Dagor Engine: id-ul obiectului
destinatar, apoi (când biții săi de jos sunt toți 1) UID-ul extern al obiectului, id-ul mesajului
și conținutul. Un mesaj către o unitate poartă ca UID extern id-ul entității unității, `index << 10 | generation`. Verificat: fiecare
asemenea mesaj numește o entitate vie în acel moment.

Pentru specialiști, mesajele citite:

| Mesaj | Ce este, și verificarea |
|---|---|
| 0xF0E9 UnitHitEffects | lovitura unui proiectil: uid-ul trăgătorului și punctul de lovire în cadrul unității (x înainte, y sus, z stânga): centimetri la avioane și nave, 20/32768 m un pas la unitățile terestre (potrivit cu dimensiunea turelelor de tanc). `hitLocalX/Y/Z` în metri. Devine un rând `shot` ([Tragerea](hits.md#gunfire)). Atacatorul aproape fiecărei înregistrări de lovitură și ucidere este printre acești trăgători; punctele de lovire se află pe partea orientată spre trăgător |
| 0xF133 UnitOnExplosion | același uid al trăgătorului |
| 0xF04B OnUnitDead | rânduri `dead`: victima fiecărei înregistrări de ucidere are una în 2 s |
| 0xD047 FmwRpm | turațiile motoarelor (`rpm`); concordă cu indicatorul de turații al cabinei |
| 0xF0B1, 0xF0A0 | rânduri `gun_shot`: focuri unice ale antiaerienelor grele și ale artileriei |
| 0xF01B, 0xF01C | rânduri `fire_start`, `fire_stop`: rafale ale tunurilor antiaeriene de 40 mm (un tun care trage; un incendiu pe un vehicul este `fire_on`, vedeți [Incendiile vehiculelor](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | rânduri `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | loviturile proprii ale jucătorului care înregistrează și loviturile primite, cu arma și muniția, numite din instalare (`projectileHitReplays`) |
| 0xF13E, 0xF031 | efectul vizual al unei lovituri și un efect redat asupra unității; vin cu o lovitură asupra aceleiași unități |
| 0xD041 | unul pentru fiecare tun defensiv al unui avion, de două ori pe secundă; indicii săi corespund armelor de tunar din modelul de zbor |
| 0xD048, 0xF117 | aranjament citit, sens necunoscut |
| restul (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | în fișierul auxiliar al mesajelor, cu unitatea și câmpurile lor |

Numele sunt cele ale comunității (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Citite și ele {#also-read}

- **Replicarea fluxului de entități** (0x22, 0x23): pentru fiecare entitate un bloc de valori de componente: cronometrele de reparare ale navelor, numărătorile consumabilelor,
  schimbările de proprietar și de echipă, supraîncălzirea motorului. Numărate în `counts.replicatedComponents`; valorile în fișierul auxiliar al mesajelor.
- **Acțiunile scriptului misiunii** (0xF028) și **indiciile** (0xF0EC): `triggers`,
  `hints`. **Progresul misiunii** (0xF07A, 0xF07C): `missionProgress`.
- **Camera de replay** (0xD043): vedeți [Camera](ground.md#the-camera).

## Necitite, și de ce {#not-read-and-why}

- **Numele și conținutul mesajelor de entitate** (0x20, 0x21): numărul clasei este un loc
  într-o listă compilată în joc, nu este trimis și nu este în datele sale. Două
  sunt citite (incendiile unui vehicul și stingătoarele sale); restul sunt păstrate întregi
  cu entitatea și numărul clasei lor.
- **Alte obiecte replicate** (alte tipuri decât sloturile de jucători și echipele): citite și păstrate,
  nenumite; nimic în rezultate cu care să fie verificate.
- **Comenzile, accelerația și rundele altor avioane**: reîmprospătate doar din când în când; păstrate în fișierul auxiliar de zbor,
  nu în tabel.
- **Incendiile avioanelor**: nu s-au găsit în niciun mesaj; un avion în flăcări nu are rând `fire_on`.
- **Numele armelor eliberate**: entitatea unei bombe sau rachete nu are niciun nume; înregistrările de ucidere numesc arma unei uciderii.
- **Loviturile care au ratat**: un replay ține doar loviturile.

`counts.messageIdsNotRead` și `selfCheck` din fiecare document al meciului spun ce conține un replay nou
și cât de bine a fost citit.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
