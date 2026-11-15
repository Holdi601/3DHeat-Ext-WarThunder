---
title: Unități terestre și cameră
nav_order: 12
lang: ro
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unități terestre și cameră {#ground-units-and-camera}

Pentru cititorii care vor să știe de unde vin coloanele despre turelă, cameră și modul de bătălie
și cât de mult să se aibă încredere în ele. Verificările dau doar metoda și gradul de concordanță.

## Turele {#turrets}

Starea terestră a unui tanc (atitudine pe 16 biți) conține, după poziție, 141 de biți
necitiți, apoi pentru fiecare turelă 62 de biți: rotirea turelei și înclinarea tunului
(câte 16 biți fiecare, 360/65536 grade un pas, cu semn) și 30 de biți necitiți; apoi umplutură,
iar la unele stări încă 200 de biți. Numărul de turele este octetul trimis
înaintea stării. O stare a cărei lungime nu se potrivește nu dă turele (unitățile statice trimit
o stare mai scurtă). Rotirea este relativă la caroserie, pozitivă în sensul acelor de ceas,
0 înainte; înclinarea relativă la caroserie, pozitivă în sus.

Cum a fost verificat:

- **Față de lovituri:** pentru fiecare lovitură dată de un tanc, direcția în lume a tunului său principal (atitudinea caroseriei
  rotită de rotirea turelei și înclinarea tunului) față de linia de la trăgător la unitatea lovită, la cel puțin 30 m
  distanță: pe bătălie o mediană de aproximativ 98 % în 3 grade la cap și 99 % la elevație
  (`selfCheck.turretsVsShots`). Restul sunt în mare parte lovituri de mitralieră dintr-o altă turelă.
- **Față de țintirea jucătorului care înregistrează:** propriul său tanc trimite unghiul în lume al țintei sale (în sens antiorar de la est), înclinarea
  și distanța. Cursul caroseriei plus rotirea turelei se află în limita unei jumătăți de grad (mediană) de țintă.

**Replay-urile de server** (0xF074) trimit starea fiecărui tanc în același aranjament,
urmată de date proprii, deci fiecare turelă ale cărei două unghiuri se află în stare este citită (cel puțin cea principală pentru
aproape fiecare rând de tanc). Este vorba de turelă, nu de cameră:

- **Față de lovituri**, ca mai sus: pe bătălie peste 90 % în 3 grade la cap și 99 % la elevație.
- **Față de vizualizare:** un replay de server trimite țintirea fiecărui jucător (`viewYaw`, `viewPitch`). Turela urmează
  vizualizarea în limita unei jumătăți de grad (mediană), dar se întoarce mult mai lent decât oscilează vizualizarea,
  cum face o acționare de turelă (`selfCheck.turretVsView`).
- **Dar nu întotdeauna cu viteza unei acționări:** eșantion cu eșantion, valoarea așa cum este trimisă
  sare uneori pe țintă când ținta este aproape de tun, mai repede decât se întoarce orice acționare.

Așadar tabelul ține turela **ținută la acționarea ei**: `turretYaw` /
`gunPitch` se mută spre valoarea trimisă cu cel mult viteza de întoarcere a tunului principal din fișierul
vehiculului din instalare (înmulțită cu 1,3 pentru abilitățile echipajului și modificări; 45 și 20 de grade pe secundă unde instalarea nu
numește niciuna). La fiecare lovitură a tunului principal turela este pusă exact pe linia loviturii, iar o
trecere înapoi o aduce acolo la timp (`selfCheck.turretLimit`). Rândul `shot` poartă și el
`turretYaw` / `gunPitch`. Valoarea trimisă rămâne în `turretYawRaw` / `gunPitchRaw`. Un tanc a cărui stare
nu are turelă are coloanele de turelă goale (vizualizatorul poate reveni la `viewYaw`).
`gunPitch` stă puțin deasupra lui `viewPitch` la distanță: înălțimea tunului pentru
căderea proiectilului.

Stările navelor au alt aranjament; turelele lor nu sunt citite. Avioanele nu trimit direcția capului sau a vizualizării; mesajul 0xD020 al
tunurilor antiaeriene rămâne necitit.

## Camera {#the-camera}

Mesajul 0xD043, aproximativ 20 pe secundă, este camera de replay proprie a jucătorului care înregistrează: câmpul 1 un cuaternion care
întoarce partea din față a camerei spre unde privește; 2 locul camerei față de vehiculul pe care îl urmărește (m); 4 aceeași deplasare în
cadrul propriu al vehiculului (x înainte, y sus, z stânga); 5 unde ține jucătorul ținta (un vector unitar); 3 zoomul (aproximativ 1,2 în vederea a treia persoană a unui tanc,
aproximativ 1,0 într-un avion, mai mare în luneta unui tunar sau prin binoclu).
Verificat: câmpul 4 este câmpul 2 întors în cadrul vehiculului, în limita a 0,5 m pentru
aproape fiecare mesaj; partea din față a camerei are cursul țintirii. Replay-ul nu trimite câmp vizual în grade,
doar zoomul.

Tabelul are camera ca un traseu al său: tipul `camera`, traseul
`<player> camera #ca`, un rând cel mult la fiecare 0,1 s, la locul vehiculului urmărit plus câmpul 2, privind de-a lungul cuaternionului (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), cu `zoom`, `aimHeading` și `aimPitch`, și `otherLife`
viața pe care o urmărește. `selfCheck.camera` numără rândurile și verificarea.

## Sfârșitul unui traseu {#end-of-a-track}

Un traseu este desenat de la primul rând la ultimul. Când unitatea sa dispare
înainte de sfârșitul replay-ului, ultimul său rând este un rând `despawn` la ultimul său loc:
în momentul în care jocul a scos entitatea (când acesta a venit la 6 s de ultimul său eșantion), altfel la ultimul său eșantion. Un traseu fără unul durează până la sfârșitul
replay-ului. Rândurile unui traseu pot fi departe unul de altul (o unitate depărtată sau o epavă se reîmprospătează
la câteva secunde, o epavă uneori nu în minute): ultima sa stare ține până la următorul său rând.

## Modul de bătălie {#battle-mode}

Octetul din antet de la decalajul 688 ține dificultatea în cei patru biți de jos:
0 arcade (AB), 5 realist (RB), 10 simulator (SB). Verificat față de tipurile de bătălie despre care se știa că sunt replay-urile.
Modul de joc este `ground` când misiunea lasă tancurile să apară, altfel `naval` când lasă navele, altfel `air`
(`allowedUnitTypes`); modul propriu al misiunii vine din cheia sa (`missions/_Dom`), numit din `lang/missions_versus.csv`
din instalarea dumneavoastră. Aceeași cheie este partea `<mode>` din numele fișierelor și din id-ul meciului (`Conq4`,
`Dom`), lăsată afară unde antetul nu are niciuna.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
