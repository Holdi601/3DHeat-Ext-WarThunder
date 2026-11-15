---
title: "Markenheter och kamera"
nav_order: 12
lang: "sv"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Markenheter och kamera {#ground-units-and-camera}

För läsare som vill veta var torn-, kamera- och stridsläges-kolumnerna kommer ifrån och hur
mycket de kan lita på. Kontrollerna anger bara metoden och överensstämmelsen.

## Torn {#turrets}

En stridsvagns markstatus (16-bitars attityd) håller, efter sin position, 141 bitar som inte
läses, och sedan per torn 62 bitar: tornets gir och kanonens höjd (16 bitar vardera, 360/65536
grader per steg, med tecken) och 30 bitar som inte läses; sedan utfyllnad, och på vissa
tillstånd 200 bitar till. Antalet torn är den byte som skickas före tillståndet. Ett tillstånd vars
längd inte passar ger inga torn (statiska enheter skickar ett kortare tillstånd). Girningen är
relativ skrovet, medurs positiv, 0 rakt fram; höjden relativ skrovet, uppåt positiv.

Så kontrollerades det:

- **Mot skotten:** för varje träff av en stridsvagn, huvudkanonens världsriktning (skrovets attityd
  vriden med tornets gir och kanonens höjd) mot linjen från skytten till den träffade enheten, minst
  30 m bort: per strid en median på ungefär 98 % inom 3 grader i kurs och 99 % i höjd
  (`selfCheck.turretsVsShots`). Resten är mest träffar av en kulspruta i ett annat torn.
- **Mot den inspelande spelarens sikte:** dess egen stridsvagn skickar sitt siktes världsvinkel
  (moturs från öster), höjd och avstånd. Skrovets kurs plus tornets gir ligger inom en halv grad
  (median) från siktet.

**Serverrepriser** (0xF074) skickar varje stridsvagns tillstånd i samma layout, följt av data av
egen art, så varje torn vars två vinklar ligger inom tillståndet läses (minst det huvudsakliga för
nästan varje stridsvagnsrad). Det är tornet, inte kameran:

- **Mot skotten**, som ovan: per strid över 90 % inom 3 grader i kurs och 99 % i höjd.
- **Mot vyn:** en serverrepris skickar varje spelares sikte (`viewYaw`, `viewPitch`). Tornet följer
  vyn inom en halv grad (median), men vrider sig mycket långsammare än vyn svänger, som en tornmotor
  gör (`selfCheck.turretVsView`).
- **Men inte alltid i en motors hastighet:** mätpunkt för mätpunkt hoppar det värde som skickas ibland
  direkt till siktet när siktet ligger nära kanonen, snabbare än någon motor vrider.

Därför håller tabellen tornet **inom sin motors gräns**: `turretYaw` / `gunPitch` rör sig mot värdet
som skickas med högst huvudkanonens vridhastighet från installationens fordonsfil (gånger 1,3 för
besättningens färdigheter och modifieringar; 45 och 20 grader per sekund där installationen inte
anger någon). Vid varje träff med huvudkanonen sätts tornet exakt på skottets linje, och ett bakåtpass
hinner dit i tid (`selfCheck.turretLimit`). `shot`-raden bär också `turretYaw` / `gunPitch`. Värdet
som skickas finns kvar i `turretYawRaw` / `gunPitchRaw`. En stridsvagn vars tillstånd saknar torn har
tomma tornkolumner (visaren kan falla tillbaka på `viewYaw`).
`gunPitch` ligger något över `viewPitch` på långt håll: kanonens höjd för granatens fall.

Fartygens tillstånd har en annan layout; deras torn läses inte. Flygplan skickar ingen huvud- eller
sikteriktning; luftvärnskanonernas meddelande 0xD020 förblir oläst.

## Kameran {#the-camera}

Meddelande 0xD043, ungefär 20 per sekund, är den inspelande spelarens egen repriskamera: fält 1 en
kvaternion som vrider kamerans framåt till dit den tittar; 2 kamerans plats från fordonet den följer
(m); 4 samma förskjutning i fordonets egna system (x framåt, y upp, z vänster); 5 vart spelaren siktar
(en enhetsvektor); 3 zoomen (ungefär 1,2 i en stridsvagns tredjepersonsvy, ungefär 1,0 i ett
flygplan, högre i en skyttes sikte eller genom kikare). Kontrollerat: fält 4 är fält 2 vriden in i
fordonets system, inom 0,5 m för nästan varje meddelande; kamerans framåt har sikets kurs. Repriset
skickar inget synfält i grader, bara zoomen.

Tabellen har kameran som en egen bana: slag `camera`, bana `<player> camera #ca`, en rad högst var
0,1 s, på det följda fordonets plats plus fält 2, med blicken längs kvaternionen (`dirX/Y/Z`,
`heading`, `pitch`, `roll`), med `zoom`, `aimHeading` och `aimPitch`, och `otherLife` det liv den
följer. `selfCheck.camera` räknar raderna och kontrollen.

## Slutet på en bana {#end-of-a-track}

En bana ritas från sin första rad till sin sista. När dess enhet är borta innan repriset tar slut är
dess sista rad en `despawn`-rad på dess sista plats: vid den tid spelet tog bort dess entitet (när den
kom inom 6 s från dess sista mätpunkt), annars vid dess sista mätpunkt. En bana utan en varar till
repriset slut. Rader i en bana kan ligga långt isär (en avlägsen enhet eller ett vrak uppfriskas var
några sekund, ett vrak ibland inte på minuter): dess sista tillstånd gäller tills nästa rad.

## Stridsläge {#battle-mode}

Headerns byte vid förskjutning 688 håller svårighetsgraden i sina fyra lägsta bitar:
0 arkad (AB), 5 realistisk (RB), 10 simulator (SB). Kontrollerat mot de stridstyper som repriserna
kändes igen som. Spelläget är `ground` när uppdraget tillåter stridsvagnar att spawna, annars `naval`
när det tillåter fartyg, annars `air` (`allowedUnitTypes`); uppdragets eget läge kommer från dess nyckel
(`missions/_Dom`), namngivet ur din installations `lang/missions_versus.csv`. Samma nyckel är
`<mode>`-delen i filnamnen och match-id:t (`Conq4`, `Dom`), utelämnad där headern inte har någon.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
