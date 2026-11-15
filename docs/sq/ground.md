---
title: "Njësitë tokësore dhe kamera"
nav_order: 12
lang: "sq"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Njësitë tokësore dhe kamera {#ground-units-and-camera}

Për lexuesit që duan të dinë nga vijnë kolonat e kupolës, kamerës dhe mënyrës së betejës
dhe sa mund t'u besohet. Kontrollet japin vetëm metodën dhe
përputhjen.

## Kupolat {#turrets}

Gjendja tokësore e një tanku (qëndrim 16-bitësh) mban, pas pozicionit të tij, 141 bit
të palexuar, pastaj për çdo kupolë 62 bit: kthimi i kupolës dhe pitch i topit
(16 bit secili, 360/65536 gradë një hap, me shenjë) dhe 30 bit të palexuar; pastaj
mbushje, dhe në disa gjendje edhe 200 bit të tjerë. Numri i kupolave është bajti i dërguar
para gjendjes. Një gjendje, gjatësia e së cilës nuk përshtatet, nuk jep kupola (njësitë
statike dërgojnë një gjendje më të shkurtër). Kthimi është relativ ndaj trupit, pozitiv në drejtim të
akrepave të orës, 0 drejt përpara; pitch relativ ndaj trupit, pozitiv lart.

Si u kontrollua:

- **Ndaj të shtënave:** për çdo goditje nga një tank, drejtimi botëror i topit të tij kryesor
  (qëndrimi i trupit i kthyer nga kthimi i kupolës dhe pitch i topit) ndaj
  vijës nga gjuajtësi te njësia e goditur, të paktën 30 m larg: për betejë një
  mediane prej rreth 98 % brenda 3 gradësh në heading dhe 99 % në lartësi
  (`selfCheck.turretsVsShots`). Të tjerat janë kryesisht goditje nga një automatik në
  një kupolë tjetër.
- **Ndaj synimit të lojtarit që regjistron:** tanku i tij dërgon këndin botëror të synimit të tij
  (në kundërkahun e akrepave nga lindja), pitch dhe distancën. Heading i trupit
  plus kthimi i kupolës shtrihet brenda gjysmë gradë (mediana) të synimit.

**Riluajtjet e serverit** (0xF074) dërgojnë gjendjen e çdo tanku në të njëjtën strukturë,
të ndjekur nga të dhëna të veta, kështu që çdo kupolë, dy këndet e së cilës shtrihen brenda
gjendjes, lexohet (të paktën kryesorja për pothuajse çdo rresht tanku). Është
kupola, jo kamera:

- **Ndaj të shtënave**, si më sipër: për betejë mbi 90 % brenda 3 gradësh në
  heading dhe 99 % në lartësi.
- **Ndaj pamjes:** një riluajtje serveri dërgon synimin e çdo lojtari
  (`viewYaw`, `viewPitch`). Kupola e ndjek pamjen brenda gjysmë gradë
  (mediana), por kthehet shumë më ngadalë se sa lëkundet pamja, siç bën një motor kupole
  (`selfCheck.turretVsView`).
- **Por jo gjithmonë me shpejtësinë e një motori:** mostër pas mostre, vlera siç dërgohet
  ndonjëherë kërcen mbi synimin kur synimi është afër topit, më shpejt se çdo motor që kthehet.

Pra tabela mban kupolën **të mbajtur në motorin e saj**: `turretYaw` /
`gunPitch` lëvizin drejt vlerës siç dërgohet jo më shpejt se shpejtësia e rrotullimit
të topit kryesor nga skedari i mjetit i instalimit (herë 1.3 për aftësitë e ekuipazhit
dhe modifikimet; 45 dhe 20 gradë në sekondë aty ku instalimi nuk emërton asnjë).
Në çdo goditje të topit kryesor kupola vendoset saktësisht në vijën e të shtënës,
dhe një kalim prapa e sjell atje në kohë (`selfCheck.turretLimit`).
Rreshti `shot` mbart edhe ato `turretYaw` / `gunPitch`. Vlera siç dërgohet
mbetet te `turretYawRaw` / `gunPitchRaw`. Një tank, gjendja e të cilit nuk mbart
kupolë, ka kolonat e kupolës bosh (shikuesi mund të kthehet te `viewYaw`).
`gunPitch` shtrihet pak mbi `viewPitch` në largësi: ngritja e topit për
rënien e predhës.

Gjendjet e anijeve kanë strukturë tjetër; kupolat e tyre nuk lexohen. Aeroplanët
nuk dërgojnë drejtim koke ose pamjeje; mesazhi i armëve kundërajrore 0xD020 mbetet i palexuar.

## Kamera {#the-camera}

Mesazhi 0xD043, rreth 20 në sekondë, është kamera e vetë riluajtjes e lojtarit që regjistron:
fusha 1 një kuaternion që e kthen përpara-n e kamerës drejt ku shikon;
2 vendi i kamerës nga mjeti që ndjek (m); 4 e njëjta zhvendosje në kuadrin
e vetë mjetit (x përpara, y lart, z majtas); 5 ku synon lojtari
(një vektor njësi); 3 zmadhimi (rreth 1.2 në pamjen e personit të tretë të një tanku, rreth
1.0 në një aeroplan, më i lartë në shënjestrën e një gjuajtësi ose përmes dylbive).
Kontrolluar: fusha 4 është fusha 2 e kthyer në kuadrin e mjetit, brenda 0.5 m
për pothuajse çdo mesazh; përpara-ja e kamerës ka heading-un e synimit. Riluajtja
nuk dërgon fushë shikimi në gradë, vetëm zmadhimin.

Tabela e ka kamerën si gjurmë më vete: kind `camera`, track
`<player> camera #ca`, një rresht më së shumti çdo 0.1 s, në vendin e mjetit të ndjekur
plus fusha 2, duke shikuar përgjatë kuaternionit (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), me `zoom`, `aimHeading` dhe `aimPitch`, dhe `otherLife`
jeta që ndjek. `selfCheck.camera` numëron rreshtat dhe kontrollin.

## Fundi i një gjurme {#end-of-a-track}

Një gjurmë vizatohet nga rreshti i saj i parë deri te i fundit. Kur njësia e saj ikën
para fundit të riluajtjes, rreshti i saj i fundit është një rresht `despawn` në vendin e saj të fundit:
në kohën kur loja hoqi entitetin e saj (kur kjo ndodhi brenda 6 s nga mostra e saj e
fundit), përndryshe te mostra e saj e fundit. Një gjurmë pa të zgjat deri në fund
të riluajtjes. Rreshtat e një gjurme mund të jenë shumë larg njëri-tjetrit (një njësi e largët
ose një mbetje rifreskohet çdo disa sekonda, një mbetje ndonjëherë jo për minuta): gjendja e saj e fundit
mbahet derisa vjen rreshti tjetër.

## Mënyra e betejës {#battle-mode}

Bajti i header-it në offset 688 mban vështirësinë në katër bitët e ulët:
0 arcade (AB), 5 realistic (RB), 10 simulator (SB). Kontrolluar ndaj llojeve të betejave
që dihej se ishin riluajtjet. Mënyra e lojës është `ground` kur misioni lejon të ripërtërihen tanke, përndryshe `naval` kur lejon anije, përndryshe `air`
(`allowedUnitTypes`); mënyra e vetë misionit vjen nga çelësi i tij
(`missions/_Dom`), e emërtuar nga `lang/missions_versus.csv` i instalimit tënd. I njëjti
çelës është pjesa `<mode>` e emrave të skedarëve dhe e ID-së së ndeshjes (`Conq4`,
`Dom`), e lënë jashtë aty ku header-i nuk ka.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
