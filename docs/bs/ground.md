---
title: "Kopnene jedinice i kamera"
nav_order: 12
lang: bs
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Kopnene jedinice i kamera {#ground-units-and-camera}

Za čitaoce koji žele znati odakle dolaze kolone kupole, kamere i načina
bitke i koliko im vjerovati. Provjere daju samo metodu i slaganje.

## Kupole {#turrets}

Kopneno stanje tenka (16-bitni stav) drži, poslije svoje pozicije, 141 bit
koji se ne čita, zatim po kupoli 62 bita: yaw kupole i pitch topa
(po 16 bita, 360/65536 stepeni po koraku, s predznakom) i 30 bitova koji se ne čitaju; zatim
popuna, a na nekim stanjima još 200 bitova. Broj kupola je bajt poslan
prije stanja. Stanje čija dužina ne odgovara ne daje kupole (statične
jedinice šalju kraće stanje). Yaw je relativan prema trupu, pozitivan u smjeru kazaljke na satu,
0 ravno naprijed; pitch relativan prema trupu, pozitivan prema gore.

Kako je provjereno:

- **Prema hicima:** za svaki pogodak tenka, svjetski smjer njegovog glavnog topa
  (stav trupa okrenut yawom kupole i pitchom topa) prema liniji od
  strijelca do pogođene jedinice, udaljene najmanje 30 m: po bitci medijan od oko 98 % unutar 3 stepena po
  smjeru i 99 % po elevaciji
  (`selfCheck.turretsVsShots`). Ostatak su uglavnom pogoci mitraljeza u
  drugoj kupoli.
- **Prema nišanjenju igrača koji snima:** njegov vlastiti tenk šalje svjetski
  ugao svog nišanjenja (suprotno od kazaljke na satu od istoka), pitch i udaljenost. Heading trupa
  plus yaw kupole leži unutar pola stepena (medijan) od nišanjenja.

**Serverski replayevi** (0xF074) šalju stanje svakog tenka u istom rasporedu,
praćeno vlastitim podacima, pa se čita svaka kupola čija se dva ugla nalaze unutar
stanja (barem glavna za gotovo svaki red tenka). To je
kupola, a ne kamera:

- **Prema hicima**, kao gore: po bitci iznad 90 % unutar 3 stepena po
  smjeru i 99 % po elevaciji.
- **Prema pogledu:** serverski replay šalje nišanjenje svakog igrača
  (`viewYaw`, `viewPitch`). Kupola prati pogled unutar pola stepena
  (medijan), ali se okreće mnogo sporije nego što se pogled zamahuje, kao što to radi
  pogon kupole (`selfCheck.turretVsView`).
- **Ali ne uvijek brzinom pogona:** uzorak po uzorak, vrijednost kako je poslana
  ponekad skoči na nišanjenje kad je nišanjenje blizu topa, brže nego što
  se ijedan pogon okreće.

Zato tabela drži kupolu **držanu na njen pogon**: `turretYaw` /
`gunPitch` kreću se prema vrijednosti kako je poslana ne brže od brzine
okretanja glavnog topa iz datoteke vozila u instalaciji (puta 1,3 za vještine posade
i modifikacije; 45 i 20 stepeni u sekundi gdje instalacija ne navodi
nijednu). Pri svakom pogotku glavnog topa kupola se postavlja tačno na liniju
hica, a prolaz unazad je dovodi tamo na vrijeme (`selfCheck.turretLimit`).
Red `shot` nosi i te `turretYaw` / `gunPitch`. Vrijednost kako je poslana
ostaje u `turretYawRaw` / `gunPitchRaw`. Tenk čije stanje ne nosi
kupolu ima prazne kolone kupole (preglednik se može vratiti na `viewYaw`).
`gunPitch` leži malo iznad `viewPitch` na daljini: elevacija topa
za pad granate.

Stanja brodova imaju drugačiji raspored; njihove kupole se ne čitaju. Avioni
ne šalju smjer glave ni pogleda; poruka 0xD020 protivavionskih topova ostaje nepročitana.

## Kamera {#the-camera}

Poruka 0xD043, oko 20 u sekundi, je vlastita replay kamera igrača koji snima:
polje 1 kvaternion koji okreće smjer naprijed kamere prema onome kamo gleda;
2 mjesto kamere u odnosu na vozilo koje prati (m); 4 isti pomak
u vlastitom okviru vozila (x naprijed, y gore, z lijevo); 5 kamo igrač cilja
(jedinični vektor); 3 zum (oko 1,2 u pogledu iz trećeg lica tenka, oko
1,0 u avionu, više u nišanu nišandžije ili kroz dvogled).
Provjereno: polje 4 je polje 2 okrenuto u okvir vozila, unutar 0,5 m
za gotovo svaku poruku; smjer naprijed kamere ima heading nišanjenja. Replay
ne šalje vidno polje u stepenima, samo zum.

Tabela ima kameru kao vlastitu stazu: kind `camera`, track
`<player> camera #ca`, red najviše svakih 0,1 s, na mjestu praćenog vozila
plus polje 2, gleda duž kvaterniona (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), sa `zoom`, `aimHeading` i `aimPitch`, a `otherLife`
je život koji prati. `selfCheck.camera` broji redove i provjeru.

## Kraj staze {#end-of-a-track}

Staza se crta od svog prvog do zadnjeg reda. Kad njena jedinica nestane
prije kraja replaya, njen zadnji red je red `despawn` na njenom zadnjem mjestu:
u vrijeme kad je igra uklonila njen entitet (kad je to došlo unutar 6 s od njenog
zadnjeg uzorka), inače na njenom zadnjem uzorku. Staza bez njega traje do kraja
replaya. Redovi jedne staze mogu biti daleko jedan od drugog (udaljena jedinica ili olupina
osvježava se svakih nekoliko sekundi, olupina ponekad ni minutima): njeno zadnje
stanje vrijedi do njenog sljedećeg reda.

## Način bitke {#battle-mode}

Bajt zaglavlja na pomaku 688 drži težinu u svoja niža četiri bita:
0 arkadna (AB), 5 realistična (RB), 10 simulatorska (SB). Provjereno prema
tipovima bitaka za koje se znalo da su replayevi. Način igre je `ground` kad
misija dozvoljava pojavljivanje tenkova, inače `naval` kad dozvoljava brodove, inače `air`
(`allowedUnitTypes`); vlastiti način misije dolazi iz njenog ključa
(`missions/_Dom`), imenovan iz `lang/missions_versus.csv` vaše instalacije. Isti
ključ je dio `<mode>` imena datoteka i id-a meča (`Conq4`,
`Dom`), izostavljen gdje ga zaglavlje nema.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
