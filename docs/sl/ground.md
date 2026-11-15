---
title: Kopenske enote in kamera
nav_order: 12
lang: "sl"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Kopenske enote in kamera {#ground-units-and-camera}

Za bralce, ki želijo vedeti, od kod prihajajo stolpci za strelske stolpe, kamero in način bitke ter kako
zaupanja vredni so. Preverjanja podajajo samo metodo in skladnost.

## Strelski stolpi {#turrets}

Stanje tal tanka (16-bitna drža) po položaju hrani 141 neprebranih bitov, nato za vsak stolp 62 bitov: vodoravni
kot stolpa in naklon topa (vsak po 16 bitov, 360/65536 stopinje na korak, predznačen) ter 30 neprebranih bitov;
nato polnilo, pri nekaterih stanjih pa še 200 bitov. Število stolpov je bajt, poslan pred stanjem. Stanje, katerega
dolžina se ne ujema, ne da nobenega stolpa (statične enote pošiljajo krajše stanje). Vodoravni kot je glede na trup,
v smeri urnega kazalca pozitiven, 0 naravnost naprej; naklon glede na trup, navzgor pozitiven.

Kako je bilo preverjeno:

- **Proti strelom:** pri vsakem zadetku tanka smer glavnega topa v svetu (drža trupa, obrnjena za vodoravni kot
  stolpa in naklon topa) proti črti od strelca do zadete enote, vsaj 30 m daleč: na bitko mediana približno 98 %
  znotraj 3 stopinj v smeri in 99 % v elevaciji (`selfCheck.turretsVsShots`). Preostali so večinoma zadetki strojnice
  v drugem stolpu.
- **Proti cilju igralca, ki je snemal:** njegov lasten tank pošilja kot svojega cilja kot v svetu (v nasprotni smeri
  urnega kazalca od vzhoda), naklon in razdaljo. Smer trupa plus vodoravni kot stolpa je znotraj pol stopinje
  (mediana) cilja.

**Strežniški posnetki** (0xF074) pošiljajo stanje vsakega tanka v isti postavitvi, za njim pa svoje podatke, zato se
prebere vsak stolp, katerega dva kota ležita znotraj stanja (pri skoraj vsaki vrstici tanka vsaj glavni). Gre za stolp,
ne za kamero:

- **Proti strelom**, kot zgoraj: na bitko nad 90 % znotraj 3 stopinj v smeri in 99 % v elevaciji.
- **Proti pogledu:** strežniški posnetek pošilja cilj vsakega igralca (`viewYaw`, `viewPitch`). Stolp sledi pogledu znotraj
  pol stopinje (mediana), vendar se obrača veliko počasneje, kot se pogled zamahuje, kot to dela pogon stolpa
  (`selfCheck.turretVsView`).
- **Vendar ne vedno s hitrostjo pogona:** vzorec za vzorcem vrednost, kot je poslana, včasih skoči na cilj, kadar je cilj
  blizu topa, hitreje, kot se katerikoli pogon obrača.

Zato tabela hrani stolp **omejen na njegov pogon**: `turretYaw` / `gunPitch` se premikata proti vrednosti, kot je poslana,
največ s hitrostjo vrtenja glavnega topa iz vozilne datoteke namestitve (pomnoženo s 1,3 za veščine posadke in
modifikacije; 45 in 20 stopinj na sekundo, kjer namestitev nobene ne navaja). Ob vsakem zadetku glavnega topa se stolp
natanko nastavi na črto strela, povratni prehod pa ga tja pripelje pravočasno (`selfCheck.turretLimit`). Vrstica `shot`
nosi tudi ta `turretYaw` / `gunPitch`. Vrednost, kot je poslana, ostane v `turretYawRaw` / `gunPitchRaw`. Tank, katerega
stanje ne nosi stolpa, ima prazne stolpce stolpa (pregledovalnik lahko preide na `viewYaw`). `gunPitch` je na razdalji
malo nad `viewPitch`: to je elevacija topa za padec izstrelka.

Stanja ladij imajo drugačno postavitev; njihovi stolpi se ne berejo. Letala ne pošiljajo smeri glave ali pogleda; sporočilo
0xD020 protiletalskih topov ostane neprebrano.

## Kamera {#the-camera}

Sporočilo 0xD043, približno 20-krat na sekundo, je lastna nadomestna kamera igralca, ki je snemal: polje 1 kvaternion, ki
obrne sprednjo stran kamere v smer, kamor gleda; 2 mesto kamere glede na vozilo, ki mu sledi (m); 4 isti zamik v okviru
vozila (x naprej, y gor, z levo); 5 kam igralec cilja (enotski vektor); 3 zoom (približno 1,2 v pogledu tretje osebe v
tanku, približno 1,0 v letalu, več pri strelskem daljnogledu ali skozi daljnogled). Preverjeno: polje 4 je polje 2,
obrnjeno v okvir vozila, znotraj 0,5 m pri skoraj vsakem sporočilu; sprednja stran kamere ima smer glave cilja. Posnetek ne
pošlje vidnega polja v stopinjah, samo zoom.

Tabela ima kamero kot svojo pot: vrsta `camera`, pot `<player> camera #ca`, vrstica največ vsakih 0,1 s, na mestu
vozila, ki mu sledi, plus polje 2, gledano vzdolž kvaterniona (`dirX/Y/Z`, `heading`, `pitch`, `roll`), z `zoom`,
`aimHeading` in `aimPitch` ter `otherLife`, življenje, ki mu sledi. `selfCheck.camera` šteje vrstice in preverjanje.

## Konec poti {#end-of-a-track}

Pot se riše od svoje prve do zadnje vrstice. Ko njena enota izgine, preden se posnetek konča, je njena zadnja vrstica
vrstica `despawn` na njenem zadnjem mestu: ob času, ko je igra odstranila njeno entiteto (če je to bilo v 6 s od njenega
zadnjega vzorca), sicer ob njenem zadnjem vzorcu. Pot brez te vrstice traja do konca posnetka. Vrstice ene poti so lahko
zelo narazen (oddaljena enota ali olupina se osvežuje na nekaj sekund, olupina včasih tudi čez minute): njeno zadnje
stanje velja do naslednje vrstice.

## Način bitke {#battle-mode}

Bajt glave na zamiku 688 hrani težavnost v svojih nižjih štirih bitih: 0 arkada (AB), 5 realistična (RB), 10 simulator
(SB). Preverjeno z vrstami bitk, za katere je bilo znano, da so jih posnetki vsebovali. Način igre je `ground`, kadar
misija dovoli pojavljanje tankov, sicer `naval`, kadar dovoli ladje, sicer `air` (`allowedUnitTypes`); lasten način misije
izhaja iz njenega ključa (`missions/_Dom`), poimenovan iz `lang/missions_versus.csv` vaše namestitve. Isti ključ je del
`<mode>` v imenih datotek in v identifikatorju tekme (`Conq4`, `Dom`), izpuščen tam, kjer ga glava nima.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
