---
title: Kopnene jedinice i kamera
nav_order: 12
lang: "hr"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Kopnene jedinice i kamera {#ground-units-and-camera}

Za čitatelje koji žele znati odakle dolaze stupci tornja, kamere i načina bitke i koliko im vjerovati.
Provjere daju samo metodu i slaganje.

## Tornjevi {#turrets}

Stanje kopnene jedinice tenka (stav od 16 bitova) nakon položaja drži 141 bit koji se ne čita, zatim po
tornju 62 bita: kut zakreta tornja i nagib topa (po 16 bitova, 360/65536 stupnjeva po koraku, sa
predznakom) i 30 bitova koji se ne čitaju; zatim popuna, a u nekim stanjima još 200 bitova. Broj tornjeva je
bajt poslan prije stanja. Stanje čija duljina ne odgovara ne daje tornjeve (statične jedinice šalju kraće
stanje). Zakret je u odnosu na trup, pozitivan u smjeru kazaljke na satu, 0 ravno naprijed; nagib u odnosu
na trup, pozitivan prema gore.

Kako je provjereno:

- **Prema hicima:** za svaki pogodak tenka, svjetski smjer njegova glavnog topa (stav trupa zakrenut zakretom
  tornja i nagibom topa) prema pravcu od strijelca do pogođene jedinice, najmanje 30 m daleko: po bitci
  medijan oko 98 % unutar 3 stupnja u smjeru i 99 % u elevaciji (`selfCheck.turretsVsShots`). Ostali su
  uglavnom pogoci mitraljezom iz drugog tornja.
- **Prema nišanu igrača koji snima:** njegov vlastiti tenk šalje svjetski kut nišana (suprotno smjeru
  kazaljke od istoka), nagib i udaljenost. Smjer trupa plus zakret tornja leži unutar pola stupnja (medijan)
  od nišana.

**Poslužiteljske snimke** (0xF074) šalju stanje svakog tenka u istom rasporedu, iza čega slijede podaci
njihovih vlastitih, pa se čita svaki toranj čija se dva kuta nalaze unutar stanja (barem glavni za gotovo
svaki red tenka). Radi se o tornju, a ne o kameri:

- **Prema hicima**, kao gore: po bitci iznad 90 % unutar 3 stupnja u smjeru i 99 % u elevaciji.
- **Prema pogledu:** poslužiteljska snimka šalje nišan svakog igrača (`viewYaw`, `viewPitch`). Toranj prati
  pogled unutar pola stupnja (medijan), ali se okreće mnogo sporije nego što se pogled zamahuje, kao što to
  radi pogon tornja (`selfCheck.turretVsView`).
- **Ali ne uvijek brzinom pogona:** uzorak po uzorak, vrijednost kako je poslana ponekad skoči na nišan kad
  je nišan blizu topa, brže nego što se ijedan pogon okreće.

Tablica zato drži toranj **vezan za njegov pogon**: `turretYaw` / `gunPitch` se pomiču prema vrijednosti
kako je poslana, najviše brzinom okretanja glavnog topa iz vozne datoteke vozila iz instalacije (puta 1,3
za vještine posade i modifikacije; 45 i 20 stupnjeva u sekundi tamo gdje instalacija ne navodi ništa). Pri
svakom pogotku glavnog topa toranj se postavlja točno na pravac hica, a povratni prolaz ga dovede tamo na
vrijeme (`selfCheck.turretLimit`). Redak `shot` nosi i `turretYaw` / `gunPitch`. Vrijednost kako je poslana
ostaje u `turretYawRaw` / `gunPitchRaw`. Tenk čije stanje ne nosi toranj ima prazne stupce tornja (preglednik
može pasti na `viewYaw`). `gunPitch` je na daljini malo iznad `viewPitch`: to je elevacija topa za pad
granate.

Stanja brodova imaju drugi raspored; njihovi tornjevi se ne čitaju. Zrakoplovi ne šalju smjer glave ni
pogleda; poruka 0xD020 protuzračnih topova ostaje nepročitana.

## Kamera {#the-camera}

Poruka 0xD043, oko 20 u sekundi, je vlastita replay kamera igrača koji snima: polje 1 kvaternion koji
okreće naprijed kamere prema mjestu gdje gleda; 2 mjesto kamere od vozila koje prati (m); 4 isti pomak u
okviru vozila (x naprijed, y gore, z lijevo); 5 mjesto na koje igrač cilja (jedinični vektor); 3 zum (oko
1,2 u trećem licu tenka, oko 1,0 u zrakoplovu, više u strijelčevu nišanu ili kroz dalekozor). Provjereno:
polje 4 je polje 2 zakrenuto u okvir vozila, unutar 0,5 m za gotovo svaku poruku; naprijed kamere ima smjer
nišana. Snimka ne šalje vidno polje u stupnjevima, samo zum.

Tablica ima kameru kao svoju putanju: vrsta `camera`, putanja `<player> camera #ca`, redak najviše svakih
0,1 s, na mjestu praćenog vozila plus polje 2, gledajući duž kvaterniona (`dirX/Y/Z`, `heading`, `pitch`,
`roll`), sa `zoom`, `aimHeading` i `aimPitch`, te `otherLife` život koji prati. `selfCheck.camera` broji
retke i provjeru.

## Kraj putanje {#end-of-a-track}

Putanja se crta od prvog do zadnjeg retka. Kad je njezina jedinica nestala prije kraja snimke, njezin zadnji
redak je redak `despawn` na zadnjem mjestu: u trenutku kad ga je igra uklonila (ako je to bilo unutar 6 s
od njegova zadnjeg uzorka), inače na zadnjem uzorku. Putanja bez njega traje do kraja snimke. Reci jedne
putanje mogu biti daleko jedan od drugoga (udaljena jedinica ili olupina se osvježava svakih nekoliko
sekundi, a olupina ponekad ni nakon nekoliko minuta): njezino zadnje stanje vrijedi do sljedećeg retka.

## Način bitke {#battle-mode}

Bajt zaglavlja na pomaku 688 drži težinu u svoja niža četiri bita: 0 arkadna (AB), 5 realistična (RB), 10
simulacijska (SB). Provjereno prema vrstama bitaka za koje je poznato da su bile snimljene. Način igre je
`ground` kad misija dopušta tenkove, inače `naval` kad dopušta brodove, inače `air` (`allowedUnitTypes`);
vlastiti način misije dolazi iz njezina ključa (`missions/_Dom`), imenovan iz `lang/missions_versus.csv`
tvoje instalacije. Isti ključ je dio `<mode>` u nazivima datoteka i u identifikatoru meča (`Conq4`, `Dom`),
izostavljen tamo gdje zaglavlje nema ništa.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
