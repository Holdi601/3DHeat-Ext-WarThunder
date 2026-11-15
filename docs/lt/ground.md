---
title: Sausumos technika ir kamera
nav_order: 12
lang: lt
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Sausumos technika ir kamera {#ground-units-and-camera}

Skirta skaitytojams, norintiems žinoti, iš kur ateina bokštelio, kameros ir mūšio režimo stulpeliai
ir kiek jiems pasitikėti. Patikrinimai nurodo tik metodą ir sutapimą.

## Bokšteliai {#turrets}

Tanko sausumos būsena (16 bitų orientacija) po pozicijos turi 141 bitą, kurie neskaitomi, o kiekvienam
bokšteliui - 62 bitus: bokštelio posūkį ir patrankos kampą (po 16 bitų, 360/65536 laipsnio žingsniu,
su ženklu), ir 30 bitų, kurie neskaitomi; tada užpildą, o kai kuriose būsenose dar 200 bitų. Bokštelių
skaičius yra baitas, siunčiamas prieš būseną. Būsena, kurios ilgis netinka, nieko nedavo bokštelių
(statiniai vienetai siunčia trumpesnę būseną). Posūkis yra santykinis su korpusu, pagal laikrodžio
rodyklę teigiamas, 0 - tiesiai į priekį; kampas santykinis su korpusu, aukštyn teigiamas.

Kaip tai patikrinta:

- **Pagal šūvius:** kiekvienam tanko pataikymui pagrindinės patrankos pasaulio kryptis (korpuso
  orientacija, pasukta bokštelio posūkiu ir patrankos kampu) lyginama su linija nuo šaulio iki
  pataikyto vieneto, ne trumpesne nei 30 m: vidutiniškai per mūšį apie 98 % patenka į 3 laipsnius
  horizontalėje ir 99 % kėlime (`selfCheck.turretsVsShots`). Likusieji daugiausia yra kulkosvaidžio
  pataikymai iš kito bokštelio.
- **Pagal žaidėjo taikymą:** jo paties tankas siunčia savo taikymo pasaulio kampą (prieš laikrodžio
  rodyklę nuo rytų), kampą aukštyn ir atstumą. Korpuso kryptis pliusas bokštelio posūkis skiriasi nuo
  taikymo ne daugiau kaip pusę laipsnio (mediana).

**Serverio įrašai** (0xF074) siunčia kiekvieno tanko būseną tuo pačiu išdėstymu, po jos - savo
duomenis, todėl skaitomas kiekvienas bokštelis, kurio abu kampai telpa būsenoje (bent pagrindinis
beveik kiekvienam tankui). Tai bokštelis, o ne kamera:

- **Pagal šūvius**, kaip aukščiau: vienam mūšiui daugiau nei 90 % patenka į 3 laipsnius horizontalėje ir
  99 % kėlime.
- **Pagal vaizdą:** serverio įrašas siunčia kiekvieno žaidėjo taikymą (`viewYaw`, `viewPitch`). Bokštelis
  seka vaizdą ne toliau nei per pusę laipsnio (mediana), bet sukasi daug lėčiau nei vaizdas
  pasisuka, kaip tai daro bokštelio pavara (`selfCheck.turretVsView`).
- **Bet ne visada pavaros greičiu:** pavyzdys po pavyzdžio, perduota reikšmė kartais staiga peršoka į
  taikymą, kai taikymas yra arti patrankos, greičiau nei bet kuri pavara gali sukti.

Todėl lentelėje yra bokštelis, **sulaikytas pagal savo pavarą**: `turretYaw` / `gunPitch` juda link
perduotos reikšmės ne greičiau, nei sukasi pagrindinė patranka pagal techniką iš diegimo transporto
failo (padauginta iš 1,3 dėl įgulos įgūdžių ir modifikacijų; kur diegime nieko nenurodyta, - 45 ir 20
laipsnių per sekundę). Kiekvieno pagrindinės patrankos pataikymo metu bokštelis nustatomas tiksliai į
šūvio liniją, o atgalinis praėjimas nuveda jį ten laiku (`selfCheck.turretLimit`). Eilutė `shot` taip
pat turi tuos `turretYaw` / `gunPitch`. Perduota reikšmė išlieka `turretYawRaw` / `gunPitchRaw`.
Tanko, kurio būsenoje nėra bokštelio, bokštelio stulpeliai tušti (žiūryklė gali grįžti prie
`viewYaw`).
`gunPitch` nedaug viršija `viewPitch` tolimame nuotolyje: patrankos pakilimas kompensuoja sviedinio
nukritimą.

Laivų būsenos turi kitokį išdėstymą; jų bokšteliai neskaitomi. Orlaiviai nesiunčia galvos ar žvilgsnio
krypties; priešlėktuvinių patrankų pranešimas 0xD020 lieka neskaitytas.

## Kamera {#the-camera}

Pranešimas 0xD043, maždaug 20 per sekundę, yra paties žaidėjo replėjaus kamera: laukas 1 - kvaternionas,
pasukantis kameros priekį į tai, kur ji žiūri; 2 - kameros vieta nuo transporto priemonės, kurią ji seka
(m); 4 - tas pats poslinkis transporto priemonės rėmelyje (x - pirmyn, y - aukštyn, z - kairėn); 5 - kur
žaidėjas taikosi (vienetinis vektorius); 3 - artinimas (apie 1,2 tanko trečio asmens vaizde, apie 1,0
orlaivyje, daugiau vado taikiklyje ar per žiūronus). Patikrinta: laukas 4 yra laukas 2, pasuktas į
transporto priemonės rėmelį, ne daugiau kaip per 0,5 m beveik kiekvienam pranešimui; kameros priekis
turi taikymo kryptį. Įrašas neduoda matymo lauko laipsniais, tik artinimą.

Lentelėje kamera turi savo trajektoriją: `kind` - `camera`, `track` - `<player> camera #ca`, eilutė ne
dažniau kaip kas 0,1 s, stebimos transporto priemonės vietoje plius laukas 2, žiūrint išilgai
kvaterniono (`dirX/Y/Z`, `heading`, `pitch`, `roll`), su `zoom`, `aimHeading` ir `aimPitch`, o
`otherLife` - gyvybė, kurią ji seka. `selfCheck.camera` suskaičiuoja eilutes ir patikrinimą.

## Trajektorijos pabaiga {#end-of-a-track}

Trajektorija nubrėžiama nuo savo pirmos iki paskutinės eilutės. Kai jos vienetas dingsta prieš įrašui
pasibaigiant, jo paskutinė eilutė yra `despawn` eilutė paskutinėje vietoje: tą akimirką, kai žaidimas
pašalino jo esybę (jei tai įvyko per 6 s nuo paskutinio pavyzdžio), kitu atveju - paskutiniame pavyzdyje.
Trajektorija be jos tęsiasi iki įrašo pabaigos. Vienos trajektorijos eilutės gali būti labai toli viena
nuo kitos (tolimas vienetas ar griuvėsiai atnaujinami kas kelias sekundes, griuvėsiai kartais - kelias
minutes): paskutinė būsena galioja iki kitos eilutės.

## Mūšio režimas {#battle-mode}

Antraštės baitas 688 pozicijoje laiko sunkumą mažuosiuose keturiuose bituose: 0 - arkadinis (AB),
5 - realistinis (RB), 10 - simuliatorius (SB). Patikrinta pagal mūšių tipus, apie kuriuos žinota, kad
įrašai yra iš jų. Žaidimo režimas yra `ground`, kai misija leidžia spawninti tankus, kitu atveju `naval`,
kai leidžia laivus, kitu atveju `air` (`allowedUnitTypes`); paties misijos režimas gaunamas iš jos rakto
(`missions/_Dom`), pavadintas pagal diegimo `lang/missions_versus.csv`. Tas pats raktas yra failų
vardų `<mode>` dalis ir mūšio id (`Conq4`, `Dom`), praleistas tuose atvejuose, kai antraštėje jo nėra.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
