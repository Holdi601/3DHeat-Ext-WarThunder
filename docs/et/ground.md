---
title: Maapealsed üksused ja kaamera
nav_order: 12
lang: et
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Maapealsed üksused ja kaamera {#ground-units-and-camera}

Lugejatele, kes tahavad teada, kust pööretornide, kaamera ja lahingurežiimi veerud pärinevad ja
kui palju neid usaldada. Kontrollid annavad ainult meetodi ja kokkulangevuse.

## Tornid {#turrets}

Tanki maapealne olek (16-bitine asend) hoiab pärast asukohta 141 bitti, mida ei loeta, ja iga torni
kohta 62 bitti: torni pööre ja püssi tõus (16 bitti kumbki, 360/65536 kraadi samm, märgiga) ning 30
bitti, mida ei loeta; siis täidis, ja mõnel olekul veel 200 bitti. Tornide arv on bait, mis saadetakse
enne olekut. Olek, mille pikkus ei sobi, ei anna torne (staatilised üksused saadavad lühema oleku).
Pööre on korpuse suhtes, päripäeva positiivne, 0 otse ees; tõus on korpuse suhtes, üles positiivne.

Kuidas kontrolliti:

- **Laskude vastu:** iga tanki tabamuse kohta vaadeldakse tema peamise relva maailmasuunda (korpuse
  asend pööratud torni pöörde ja püssi tõusuga) vastu joont laskjast tabatud üksuseni, vähemalt 30 m
  kaugusel: lahingu kohta mediaanina umbes 98% 3 kraadi piires suunas ja 99% kõrguses
  (`selfCheck.turretsVsShots`). Ülejäänud on enamasti teise torni kuulipildujaga tabamused.
- **Salvestajamängija sihi vastu:** tema enda tank saadab oma sihi maailmanurga (vastupäeva idast),
  tõusu ja kauguse. Korpuse suund pluss torni pööre jääb poole kraadi piiresse (mediaan) sihist.

**Serveri kordused** (0xF074) saadavad iga tanki oleku samas paigutuses, millele järgnevad nende
enda andmed, nii et loetakse iga torni, mille kaks nurka jäävad oleku sisse (peaaegu iga tankirea
puhul vähemalt peamine). See on torn, mitte kaamera:

- **Laskude vastu**, nagu ülal: lahingu kohta üle 90% 3 kraadi piires suunas ja 99% kõrguses.
- **Vaate vastu:** serveri kordus saadab iga mängija sihi (`viewYaw`, `viewPitch`). Torn järgib vaadet
  poole kraadi täpsusega (mediaan), kuid pöördub palju aeglasemalt kui vaade kõigub, nagu teeb torni
  ajam (`selfCheck.turretVsView`).
- **Aga mitte alati ajami kiirusel:** näidis näidise haaval hüppab saadetud väärtus mõnikord sihile,
  kui siht on püssi lähedal, kiiremini kui ükski ajam pöördub.

Seega hoiab tabel torni **ajami piires kinni**: `turretYaw` / `gunPitch` liiguvad saadetud väärtuse
poole mitte kiiremini kui installatsiooni sõiduki failist loetud peamise püssi pöördekiirus (korrutatud
1,3-ga meeskonnaoskuste ja modifikatsioonide jaoks; kus installatsioon ühtegi ei nimeta, siis 45 ja 20
kraadi sekundis). Iga peamise püssi tabamuse juures seatakse torn täpselt laskejoonele ja tagurpidi
läbimine viib ta sinna õigeaegselt (`selfCheck.turretLimit`). Rida `shot` kannab samuti
`turretYaw` / `gunPitch` väärtusi. Saadetud väärtus jääb veergudesse `turretYawRaw` / `gunPitchRaw`.
Tank, mille olek ei kanna torni, jätab torni veerud tühjaks (vaaturi võib langeda tagasi `viewYaw`-ile).
`gunPitch` on kaugusel veidi `viewPitch`-ist kõrgemal: püssi tõus kuuli langemise jaoks.

Laevade olekutel on teine paigutus; nende torne ei loeta. Lennukid ei saada pea- ega vaatesuunda;
õhutõrjerelvade sõnum 0xD020 jääb loetamata.

## Kaamera {#the-camera}

Sõnum 0xD043, umbes 20 korda sekundis, on salvestajamängija enda kordusekaamera: väli 1 on kvaternion, mis
pöörab kaamera esiosa sinna, kuhu ta vaatab; 2 kaamera asukoht jälgitava sõiduki suhtes (m); 4 sama nihe
sõiduki enda raamistikus (x ees, y üles, z vasakule); 5 kuhu mängija sihib (ühikvektor); 3 suumimine
(umbes 1,2 tanki kolmanda isiku vaates, umbes 1,0 lennukis, kõrgem relvaneni või binoklist). Kontrollitud:
väli 4 on väli 2 pööratud sõiduki raamistikku, 0,5 m täpsusega peaaegu iga sõnumi puhul; kaamera esiosa
suund on sihi suund. Kordus ei saada vaatevälja kraadides, ainult suumi.

Tabelis on kaamera omaette rajana: liik `camera`, rada `<player> camera #ca`, rida vähemalt iga 0,1 s
tagant, jälgitava sõiduki asukohas pluss väli 2, vaadates mööda kvaterniooni (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), koos `zoom`, `aimHeading` ja `aimPitch`, ning `otherLife` eluga, mida ta jälgib.
`selfCheck.camera` loeb ridu ja kontrolli.

## Raja lõpp {#end-of-a-track}

Rada joonistatakse esimesest reast viimaseni. Kui selle üksus on kadunud enne korduse lõppu, on tema
viimane rida `despawn`-rida viimasel asukohal: sel ajal, kui mäng eemaldas tema olemi (kui see tuli
6 s jooksul tema viimasest näidisest), muidu viimasel näidisel. Rada ilma selleta kestab korduse lõpuni.
Ühe raja read võivad olla üksteisest kaugel (kaugem üksus või vrakk värskendatakse iga paari sekundi
tagant, vrakk mõnikord minuteid mitte): tema viimane olek kehtib kuni järgmise reani.

## Lahingurežiim {#battle-mode}

Päise bait nihkel 688 hoiab raskusastet oma madalates neljas bitis: 0 arcade (AB), 5 realistic (RB),
10 simulator (SB). Kontrollitud vastu lahingutüüpe, mille kohta kordused olid teada. Mängurežiim on
`ground`, kui missioon lubab tankide tekitamist, muidu `naval`, kui see lubab laevu, muidu `air`
(`allowedUnitTypes`); missiooni enda režiim tuleb tema võtmest (`missions/_Dom`), nimetatuna sinu
installatsiooni failist `lang/missions_versus.csv`. Sama võti on failinimede `<mode>` osa ja lahingu ID
(`Conq4`, `Dom`), jäetud välja, kui päises seda ei ole.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
