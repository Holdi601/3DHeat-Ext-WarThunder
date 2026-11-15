---
title: "Pozemní jednotky a kamera"
nav_order: 12
lang: "cs"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Pozemní jednotky a kamera {#ground-units-and-camera}

Pro čtenáře, kteří chtějí vědět, odkud se berou sloupce věží, kamery a režimu bitvy, a jak moc jim věřit. Kontroly
uvádějí jen metodu a míru shody.

## Věže {#turrets}

Pozemní stav tanku (16bitový postoj) drží za svou polohou 141 nečtených bitů, potom pro každou věž 62 bitů: natočení
věže a sklon děla (každé 16 bitů, 360/65536 stupně na krok, se znaménkem) a 30 nečtených bitů; pak výplň, a u některých
stavů ještě 200 bitů navíc. Počet věží je bajt poslaný před stavem. Stav, jehož délka nesedí, nedá žádné věže (statické
jednotky posílají kratší stav). Natočení je vzhledem k trupu, kladné po směru hodinových ručiček, 0 rovně vpřed;
sklon vzhledem k trupu, kladný nahoru.

Jak to bylo ověřeno:

- **Proti výstřelům:** u každého zásahu tankem směr hlavního děla ve světě (postoj trupu otočený natočením věže
  a sklonem děla) proti přímce od střelce k zasažené jednotce, nejméně 30 m daleko: na bitvu medián asi 98 % do
  3 stupňů ve směru a 99 % ve výšce (`selfCheck.turretsVsShots`). Zbytek jsou většinou zásahy kulometem z jiné věže.
- **Proti míření hráče, který nahrával:** jeho vlastní tank posílá úhel svého míření ve světě (proti směru hodinových
  ručiček od východu), sklon a vzdálenost. Kurz trupu plus natočení věže leží do poloviny stupně (medián) od míření.

**Serverové replaye** (0xF074) posílají stav každého tanku ve stejném uspořádání, za ním data vlastní, takže se čte
každá věž, jejíž dva úhly leží uvnitř stavu (u téměř každého řádku tanku aspoň ta hlavní). Je to věž, ne kamera:

- **Proti výstřelům**, jak výše: na bitvu nad 90 % do 3 stupňů ve směru a 99 % ve výšce.
- **Proti pohledu:** serverový replay posílá míření každého hráče (`viewYaw`, `viewPitch`). Věž sleduje pohled do
  poloviny stupně (medián), ale otáčí se mnohem pomaleji, než se pohled kývá, jako to dělá pohon věže
  (`selfCheck.turretVsView`).
- **Ne vždy rychlostí pohonu:** vzorek po vzorku se poslaná hodnota někdy přiskočí na míření, je-li míření blízko
  děla, rychleji, než se jakýkoli pohon otočí.

Tabulka tedy drží věž **omezenou jejím pohonem**: `turretYaw` / `gunPitch` se přibližují k poslané hodnotě nejvýš
rychlostí otáčení hlavního děla z souboru vozidla v instalaci (krát 1,3 kvůli dovednostem posádky a úpravám; 45 a 20
stupňů za vteřinu tam, kde instalace žádné neuvádí). Při každém zásahu hlavním dělem se věž nastaví přesně na přímku
výstřelu a zpětný průchod ji tam dovede včas (`selfCheck.turretLimit`). Řádek `shot` nese také `turretYaw` /
`gunPitch`. Poslaná hodnota zůstává v `turretYawRaw` / `gunPitchRaw`. Tank, jehož stav nenese věž, má sloupce věže
prázdné (prohlížeč může přejít na `viewYaw`).
`gunPitch` leží na dálku o něco výš než `viewPitch`: je to sklon děla kvůli pádu střely.

Stavy lodí mají jiné uspořádání; jejich věže se nečtou. Letadla neposílají směr hlavy ani pohledu; zpráva 0xD020
pro protiletadlová děla zůstává nečtená.

## Kamera {#the-camera}

Zpráva 0xD043, asi 20 za vteřinu, je kamera replaye hráče, který nahrával: pole 1 je kvaternion, který otáčí dopředný
směr kamery tam, kam se dívá; 2 je místo kamery vzhledem k vozidlu, které sleduje (m); 4 stejný posun v rámci vozidla
(x dopředu, y nahoru, z vlevo); 5 kam hráč míří (jednotkový vektor); 3 přiblížení (asi 1,2 v pohledu zvenku na tanku,
asi 1,0 v letadle, vyšší v zaměřovači střelce nebo v dalekohledu).
Ověřeno: pole 4 je pole 2 otočené do rámce vozidla, do 0,5 m téměř u každé zprávy; dopředný směr kamery má kurz míření.
Replay neposílá zorné pole ve stupních, jen přiblížení.

Tabulka má kameru jako vlastní trať: druh `camera`, trať `<player> camera #ca`, řádek nejvýš každých 0,1 s, na místě
sledovaného vozidla plus pole 2, dívající se podle kvaternionu (`dirX/Y/Z`, `heading`, `pitch`, `roll`), s `zoom`,
`aimHeading` a `aimPitch` a `otherLife`, životem, který sleduje. `selfCheck.camera` počítá řádky a kontrolu.

## Konec tratě {#end-of-a-track}

Trať se kreslí od svého prvního řádku k poslednímu. Když je jednotka pryč dřív, než replay skončí, jeho posledním
řádkem je řádek `despawn` na jeho posledním místě: v čase, kdy hra odstranila jeho entitu (pokud to přišlo do 6 s
od jeho posledního vzorku), jinak v jeho posledním vzorku. Trať bez něj trvá až do konce replaye. Řádky jedné tratě
mohou být daleko od sebe (vzdálená jednotka nebo vrak se obnovuje každých několik vteřin, vrak někdy až po minuty):
jeho poslední stav platí, dokud nepřijde další řádek.

## Režim bitvy {#battle-mode}

Bajt hlavičky na posunu 688 drží obtížnost ve svých nižších čtyřech bitech: 0 arkáda (AB), 5 realistická (RB), 10
simulátor (SB). Ověřeno proti typům bitev, o kterých je známo, jaké replaye byly. Herní režim je `ground`, když mise
dovoluje spawn tanků, jinak `naval`, když dovoluje lodě, jinak `air` (`allowedUnitTypes`); vlastní režim mise je
z jejího klíče (`missions/_Dom`), pojmenovaný podle `lang/missions_versus.csv` vaší instalace. Týž klíč je částí
`<mode>` názvů souborů a id zápasu (`Conq4`, `Dom`), vynechaný tam, kde ho hlavička nemá.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
