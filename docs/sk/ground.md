---
title: "Pozemné jednotky a kamera"
nav_order: 12
lang: sk
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Pozemné jednotky a kamera {#ground-units-and-camera}

Pre čitateľov, ktorí chcú vedieť, odkiaľ pochádzajú stĺpce veže, kamery a režimu bitky a nakoľko im dôverovať.
Kontroly uvádzajú len metódu a zhodu.

## Veže {#turrets}

Pozemný stav tanku (16-bitový postoj) obsahuje po jeho polohe 141 nečítaných bitov, potom na každú vežu 62 bitov:
uhol otočenia veže a sklon diela (každý 16 bitov, 360/65536 stupňa na krok, so znamienkom) a 30 nečítaných bitov;
potom výplň, a na niektorých stavoch ešte 200 bitov. Počet veží je bajt poslaný pred stavom. Stav, ktorého dĺžka sa
nezhoduje, nedá žiadne veže (statické jednotky posielajú kratší stav). Uhol otočenia je vzhľadom na trup, kladný v smere
hodinových ručičiek, 0 rovno vpred; sklon vzhľadom na trup, kladný nahor.

Ako to bolo overené:

- **Proti výstrelom:** pri každom zásahu tankom sa smer hlavného diela vo svete (postoj trupu otočený uhlom veže a
  sklonom diela) porovnal s priamkou od strelca k zasiahnutej jednotke, aspoň 30 m ďaleko: na bitku medián asi 98 %
  do 3 stupňov v smere a 99 % vo výške (`selfCheck.turretsVsShots`). Zvyšok sú väčšinou zásahy guľometom v inej veži.
- **Proti pohľadu hráča, ktorý replay nahral:** jeho vlastný tank posiela uhol svojho pohľadu vo svete (proti smeru
  hodinových ručičiek od východu), sklon a vzdialenosť. Smer trupu plus uhol veže leží do pol stupňa (medián) od pohľadu.

**Serverové replaye** (0xF074) posielajú stav každého tanku v tom istom rozložení, nasledovaný vlastnými údajmi, takže
sa načíta každá veža, ktorej dva uhly ležia v stave (aspoň hlavná veža takmer pri každom riadku tanku). Je to veža, nie kamera:

- **Proti výstrelom**, ako vyššie: na bitku nad 90 % do 3 stupňov v smere a 99 % vo výške.
- **Proti pohľadu:** serverový replay posiela pohľad každého hráča (`viewYaw`, `viewPitch`). Veža sleduje pohľad do pol
  stupňa (medián), ale otáča sa oveľa pomalšie, než sa pohľad hýbe, ako to robí pohon veže (`selfCheck.turretVsView`).
- **Ale nie vždy rýchlosťou pohonu:** vzorka po vzorke sa hodnota tak, ako je poslaná, niekedy skočí na pohľad, keď je
  pohľad blízko dela, rýchlejšie, než sa otočí akýkoľvek pohon.

Tabuľka teda drží vežu **pridŕžanú jej pohonom**: `turretYaw` / `gunPitch` sa posúvajú k hodnote, ako je poslaná, najviac
rýchlosťou otáčania hlavného dela z inštalačného súboru vozidla (krát 1,3 pre zručnosti posádky a modifikáty; 45 a 20
stupňov za sekundu, kde inštalácia žiadne neuvádza). Pri každom zásahu hlavným delom sa veža nastaví presne na priamku
výstrelu a spätný prechod ju tam dostane včas (`selfCheck.turretLimit`). Riadok `shot` nesie tiež `turretYaw` /
`gunPitch`. Hodnota tak, ako je poslaná, zostáva v `turretYawRaw` / `gunPitchRaw`. Tank, ktorého stav neobsahuje
žiadnu vežu, má stĺpce veže prázdne (prehliadač môže použiť `viewYaw`).
`gunPitch` je na diaľku o niečo vyššie než `viewPitch`: je to výška dela pre pokles strely.

Stavy lodí majú iné rozloženie; ich veže sa nečítajú. Lietadlá neposielajú smer hlavy ani pohľadu; správa streleckých
zbraní proti lietadlám 0xD020 zostáva nečítaná.

## Kamera {#the-camera}

Správa 0xD043, asi dvadsaťkrát za sekundu, je replay kamera samotného hráča, ktorý replay nahral: pole 1 je kvaternión,
ktorý otáča predný smer kamery tam, kam sa pozerá; 2 je miesto kamery od vozidla, ktoré sleduje (m); 4 ten istý posun
v súradniciach vozidla (x dopredu, y nahor, z vľavo); 5 kam hráč mieri (jednotkový vektor); 3 priblíženie (asi 1,2
v pohľade z tretej osoby v tanku, asi 1,0 v lietadle, vyššie v strelcovom zameriavači alebo cezďalekohľad).
Overené: pole 4 je pole 2 otočené do súradníc vozidla, do 0,5 m takmer pri každej správe; predný smer kamery má
smer hlavy pohľadu. Replay neposiela zorné pole v stupňoch, len priblíženie.

Tabuľka má kameru ako vlastnú stopu: druh `camera`, stopa `<player> camera #ca`, riadok najviac každých 0,1 s, na mieste
sledovaného vozidla plus pole 2, pozerajúc pozdĺž kvaterniónu (`dirX/Y/Z`, `heading`, `pitch`, `roll`), so `zoom`,
`aimHeading` a `aimPitch` a `otherLife`, životom, ktorý sleduje. `selfCheck.camera` počíta riadky a kontrolu.

## Koniec stopy {#end-of-a-track}

Stopa sa kreslí od svojho prvého riadku po posledný. Keď jej jednotka zanikne skôr, než replay skončí, jej posledný riadok
je riadok `despawn` na jej poslednom mieste: v čase, keď hra odstránila jej entitu (ak to nastalo do 6 s od jej poslednej
vzorky), inak pri jej poslednej vzorke. Stopa bez toho trvá do konca replaye. Riadky jednej stopy môžu byť veľmi ďaleko
od seba (vzdialená jednotka alebo vrak sa obnovuje každých pár sekúnd, vrak niekedy minúty vôbec): jej posledný stav platí,
kým príde ďalší riadok.

## Režim bitky {#battle-mode}

Bajt v hlavičke na pozícii 688 nesie obtiažnosť v svojich nižších štyroch bitoch:
0 arkádová (AB), 5 realistická (RB), 10 simulátorová (SB). Overené oproti typom bitiek, o ktorých sa vedelo, že ich replaye
obsahovali. Herný režim je `ground`, keď misia dovoľuje spawn tankov, inak `naval`, keď dovoľuje lode, inak `air`
(`allowedUnitTypes`); vlastný režim misie je z jej kľúča (`missions/_Dom`), pomenovaný podľa `lang/missions_versus.csv`
vo vašej inštalácii. Ten istý kľúč je časťou `<mode>` názvov súborov a id zápasu (`Conq4`, `Dom`), vynechaný tam,
kde hlavička žiadny nemá.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
