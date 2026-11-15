---
title: Lovituri, tragere și incendii
nav_order: 13
lang: ro
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Lovituri, tragere și incendii {#hits-gunfire-and-fires}

Pentru cititorii care vor să știe de unde vin coloanele despre lovituri, muniție și incendii.
Verificările dau doar metoda și gradul de concordanță.

## Tragerea {#gunfire}

Fiecare proiectil care a lovit o unitate se află în replay (mesajul 0xF0E9): un rând `shot`
la poziția trăgătorului în momentul loviturii, `targetX/Y/Z` punctul lovit (unitatea lovită, mutată cu punctul de lovire în cadrul ei, întoarsă după atitudinea ei), direcția spre ea, `other` unitatea lovită. Obuzele și
gloanțele care au ratat nu sunt trimise: nu sunt entități, iar
mesajele pentru lucrurile în zbor cuprind doar rachete, rachete ghidate, bombe și torpile.
Rundele rămase ale jucătorului care înregistrează (coloana sa `ammo`) scad pe măsură ce trage, deci
rafalele sale pot fi deosebite, dar nu unde au ajuns acele runde. Antiaerienele grele și artileria trimit fiecare
foc unic (`gun_shot`, fără direcție), tunurile antiaeriene de 40 mm rafalele lor (`fire_start`, `fire_stop`).

## Rezultatele loviturilor {#hit-outcomes}

La fiecare lovitură de proiectil asupra unei unități terestre, serverul trimite mesajul 0xF144
(UnitOnHit) către unitate: patru câmpuri de un octet, al patrulea sunt biții a ceea ce a făcut lovitura
(`selfCheck.unitMessages.outcome_*`):

| Bit | Înseamnă | Dovadă |
|---|---|---|
| 0x20 | lovitura proprie a unui proiectil | aproape toate vin cu o lovitură 0xF0E9 asupra unității în 5 ms; fără ea, cu o explozie (stropire) |
| 0x01 | a trecut (penetrare) | fiecare mesaj cu 0x02, 0x04 sau 0x08 îl are și el |
| 0x02 | lovitură critică | majoritatea înregistrărilor de lovitură critică îl au, mult mai des decât la întâmplare |
| 0x04 | distrus | majoritatea vin cu o înregistrare de ucidere și moartea unității în o secundă |
| 0x08 | avarie grea | unele înregistrări de lovitură critică îl au; rar în rest |

`hitOutcome` ia cel mai grav: `kill` (0x04), `critical` (0x02 sau 0x08),
`penetration` (0x01), `nonpenetration` (0x20 singur). O lovitură este asociată cu cel mai apropiat 0xF144
nepereche cu 0x20 către unitatea sa, în 5 ms. Camera de lovitură a jocului deosebește un ricoșeu de o
neperforare, dar niciun bit sau câmp găsit aici nu o face: primii trei octeți variază de la lovitură la lovitură și
nu se cunosc. Replay-urile de client trimit 0xF144 doar pentru avionul propriu al jucătorului care înregistrează, cu toți biții
goi: loviturile asupra avioanelor și navelor nu au rezultat.

## Muniția {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explozivă sau nu.** Un obuz care explodează trimite 0xF133 (UnitOnExplosion)
  cu id-ul utilizatorului trăgătorului și numărul loviturii; o lovitură cu unul este
  `explosive`, restul `kinetic`.
* **Tunul și slotul său.** 0xF0BD (UnitBulletRearm) este următoarea rundă încărcată:
  indexul armei în lista de arme a vehiculului, slotul de muniție și rundele rămase. Cel al unui
  încărcător manual vine un timp de reîncărcare constant după fiecare dintre loviturile sale, cel al unui tun automat
  o fracțiune de secundă după. Loviturile unui trăgător sunt grupate după vehicul, semnătură și rafală; un grup este al unei
  arme când arma aceea încarcă o rundă în 20 s după jumătate sau mai mult din loviturile sale
  la o întârziere constantă. `ammoSlot` este `weapon/slot`, slotul încărcat
  înainte de lovitură: probabil cel tras, cu excepția cazului în care jucătorul a schimbat muniția între timp.
  Mitralierele nu trimit 0xF0BD.
* **Proiectilul.** Arma unei uciderii este id-ul proiectilului (`125mm_3bm46`); ultima lovitură a
  ucigașului asupra victimei o dă slotului acelui trăgător, unde calibrul tunului este de acord.
  Tipul și calibrul său sunt ale fișierului armei (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS,
  `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Calibrul** celorlalte: al armei slotului; al unui grup de mitralieră, singurul calibru de mitralieră pe care îl poate avea semnătura sa; altfel cel al tunului principal
  al vehiculului. Fără instalare (`--game`) nu există tip, nume sau calibru în afară de `explosive` / `kinetic`.

Nu s-a găsit: ricoșeul. Mai multe mesaje poartă trăgătorul și numărul loviturii (0xF0C2, probabil traseul camerei de lovitură
prin vehicul; 0xF117, 0xF13C, 0xF13E); sunt păstrate în fișierul auxiliar, nu decodate. O
neperforare rămâne `nonpenetration`.

## Incendiile vehiculelor {#vehicle-fires}

Un vehicul în flăcări este arătat fiecărui client: serverul trimite un mesaj de entitate către vehicul (eveniment `0a519c58`) care listează incendiile care ard pe el,
de fiecare dată când lista se schimbă. Pentru fiecare incendiu: doi id-uri pe 16 biți (al doilea un nod al modelului de avariere), tipul său și -1 până când incendiul prinde. Un incendiu aprins de o
lovitură primește și un mesaj cu punctul unde arde, în cadrul vehiculului (x înainte, y sus, z stânga).

Rânduri: `fire_on` când apare un incendiu în listă, `fire_off` când nu mai este, la vehicul, cu `fireId` (`first:node`), `fireKind` și, pentru incendiile
aprinse de o lovitură, `fireLocalX/Y/Z` (înainte, sus, dreapta). Odată ce un vehicul este distrus, lista sa
adesea nu mai este trimisă: incendiile sale se termină odată cu epava sa, altfel cu entitatea sa, altfel cu replay-ul (`selfCheck.fires`).

Verificat: de fiecare dată când numărul de stingătoare al unui tanc a scăzut, un incendiu a ieșit din
listă într-o fracțiune de secundă; majoritatea punctelor de incendiu se află pe aceeași parte a
vehiculului ca lovitura care l-a aprins. Tipurile sunt numere; ce numesc nu se știe, nici ce parte este un nod. Avioanele nu trimit o astfel de listă: un
avion în flăcări nu este citit.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
