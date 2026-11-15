---
title: "Grondeenheden en camera"
nav_order: 12
lang: "nl"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Grondeenheden en camera {#ground-units-and-camera}

Voor lezers die willen weten waar de kolommen van toren, camera en gevechtsmodus vandaan komen en hoe ver je ze kunt vertrouwen. Controles geven alleen de methode en de overeenstemming.

## Torens {#turrets}

De grondtoestand van een tank (houding van 16 bits) bevat, na zijn positie, 141 bits die niet gelezen worden, en daarna per toren 62 bits: de gier van de toren en de hoogte van het kanon (elk 16 bits, 360/65536 graden per stap, met teken), en 30 bits die niet gelezen worden; dan opvulling, en bij sommige toestanden nog 200 bits. Het aantal torens is de byte die vóór de toestand gestuurd wordt. Een toestand waarvan de lengte niet past, geeft geen torens (statische eenheden sturen een kortere toestand). De gier is ten opzichte van de romp, met de klok mee positief, 0 recht vooruit; de hoogte ten opzichte van de romp, omhoog positief.

Hoe het gecontroleerd is:

- **Tegen de schoten:** voor elke treffer van een tank wordt de wereldrichting van zijn hoofdkanon (de houding van de romp gedraaid door de gier van de toren en de hoogte van het kanon) vergeleken met de lijn van de schutter naar de getroffen eenheid, minstens 30 m weg: per gevecht een mediaan van ongeveer 98 % binnen 3 graden in heading en 99 % in hoogte (`selfCheck.turretsVsShots`). De rest zijn meestal treffers van een machinegeweer in een andere toren.
- **Tegen de richting van de opnemende speler:** diens eigen tank stuurt de wereldhoek van zijn richting (tegen de klok in vanaf oost), hoogte en afstand. De heading van de romp plus de gier van de toren ligt binnen een halve graad (mediaan) van de richting.

**Serverreplays** (0xF074) sturen de toestand van elke tank in dezelfde indeling, gevolgd door eigen gegevens, dus elke toren waarvan de twee hoeken binnen de toestand liggen, wordt gelezen (minstens de hoofdtoren bij bijna elke tankrij). Het is de toren, niet de camera:

- **Tegen de schoten**, zoals hierboven: per gevecht boven 90 % binnen 3 graden in heading en 99 % in hoogte.
- **Tegen het beeld:** een serverreplay stuurt de richting van elke speler (`viewYaw`, `viewPitch`). De toren volgt het beeld binnen een halve graad (mediaan), maar draait veel trager dan het beeld zwaait, zoals een torenaandrijving doet (`selfCheck.turretVsView`).
- **Maar niet altijd met de snelheid van een aandrijving:** sample voor sample springt de waarde zoals gestuurd soms op het doel als het doel dicht bij het kanon ligt, sneller dan welke aandrijving ook draait.

De tabel bevat dus de toren **gehouden aan zijn aandrijving**: `turretYaw` / `gunPitch` bewegen naar de waarde zoals gestuurd met hoogstens de draaisnelheid van het hoofdkanon uit het voertuigbestand van de installatie (maal 1,3 voor bemanningsvaardigheden en modificaties; 45 en 20 graden per seconde waar de installatie geen waarde noemt). Bij elke treffer van het hoofdkanon wordt de toren precies op de lijn van het schot gezet, en een terugwaartse doorloop brengt hem daar op tijd (`selfCheck.turretLimit`). Het `shot`-rij draagt die `turretYaw` / `gunPitch` ook. De waarde zoals gestuurd blijft in `turretYawRaw` / `gunPitchRaw`. Een tank waarvan de toestand geen toren bevat, heeft lege torenkolommen (de viewer kan terugvallen op `viewYaw`). `gunPitch` ligt op afstand iets boven `viewPitch`: de hoogte van het kanon voor de val van het projectiel.

De toestanden van schepen hebben een andere indeling; hun torens worden niet gelezen. Vliegtuigen sturen geen kop- of kijkrichting; het bericht 0xD020 van de luchtafweergeschutten blijft ongelezen.

## De camera {#the-camera}

Bericht 0xD043, ongeveer 20 per seconde, is de eigen replaycamera van de opnemende speler: veld 1 een quaternion dat de voorkant van de camera draait naar waar hij kijkt; 2 de plaats van de camera ten opzichte van het voertuig dat hij volgt (m); 4 dezelfde verschuiving in het eigen assenstelsel van het voertuig (x vooruit, y omhoog, z links); 5 waar de speler richt (een eenheidsvector); 3 de zoom (ongeveer 1,2 in de derdepersoonsweergave van een tank, ongeveer 1,0 in een vliegtuig, hoger in het vizier van een schutter of door een verrekijker). Gecontroleerd: veld 4 is veld 2 omgezet naar het assenstelsel van het voertuig, binnen 0,5 m bij bijna elk bericht; de voorkant van de camera heeft de heading van het beeld. De replay stuurt geen gezichtsveld in graden, alleen de zoom.

De tabel heeft de camera als eigen spoor: soort `camera`, spoor `<speler> camera #ca`, een rij hoogstens elke 0,1 s, op de plaats van het gevolgde voertuig plus veld 2, kijkend langs het quaternion (`dirX/Y/Z`, `heading`, `pitch`, `roll`), met `zoom`, `aimHeading` en `aimPitch`, en `otherLife` het leven dat hij volgt. `selfCheck.camera` telt de rijen en de controle.

## Einde van een spoor {#end-of-a-track}

Een spoor wordt getekend van zijn eerste tot zijn laatste rij. Wanneer zijn eenheid weg is voordat de replay eindigt, is zijn laatste rij een `despawn`-rij op zijn laatste plaats: op het moment dat het spel zijn entiteit verwijderde (als dat binnen 6 s na zijn laatste sample kwam), anders op zijn laatste sample. Een spoor zonder zo'n rij loopt tot het eind van de replay. Rijen van één spoor kunnen ver uit elkaar liggen (een verre eenheid of een wrak wordt elke paar seconden ververst, een wrak soms pas na minuten): de laatste toestand blijft gelden tot de volgende rij.

## Gevechtsmodus {#battle-mode}

De byte van de kop op offset 688 bevat de moeilijkheidsgraad in zijn laagste vier bits: 0 arcade (AB), 5 realistisch (RB), 10 simulator (SB). Gecontroleerd tegen de gevechtstypen waarvan bekend was welke de replays waren. De spelmodus is `ground` als de missie tanks laat spawnen, anders `naval` als ze schepen laat, anders `air` (`allowedUnitTypes`); de eigen modus van de missie komt uit haar sleutel (`missions/_Dom`), benoemd uit `lang/missions_versus.csv` van je installatie. Dezelfde sleutel is het deel `<mode>` van de bestandsnamen en het wedstrijd-id (`Conq4`, `Dom`), weggelaten waar de kop er geen heeft.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
