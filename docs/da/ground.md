---
title: Landenheder og kamera
nav_order: 12
lang: da
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Landenheder og kamera {#ground-units-and-camera}

For dem, der vil vide, hvor tårn-, kamera- og kampstilstandskolonnerne kommer fra, og hvor meget
man kan stole på dem. Kontroller giver kun metoden og overensstemmelsen.

## Tårne {#turrets}

En tanks landtilstand (16-bit holdning) indeholder, efter dens position, 141 bit, der ikke læses,
og derefter pr. tårn 62 bit: tårnets drejning og kanonens hævning (16 bit hver, 360/65536 grader
pr. trin, med fortegn) og 30 bit, der ikke læses; derefter udfyldning, og i nogle tilstande 200 bit
mere. Antallet af tårne er den byte, der sendes før tilstanden. En tilstand, hvis længde ikke passer,
giver ingen tårne (statiske enheder sender en kortere tilstand). Drejningen er i forhold til skroget,
med uret positiv, 0 lige frem; hævningen i forhold til skroget, op positiv.

Sådan blev det kontrolleret:

- **Mod skuddene:** for hvert træf af en tank, kanonens verdensretning (skrogets holdning drejet med
  tårnets drejning og kanonens hævning) mod linjen fra skytten til den ramte enhed, mindst 30 m væk:
  pr. kamp en median på ca. 98 % inden for 3 grader i heading og 99 % i elevation
  (`selfCheck.turretsVsShots`). Resten er for det meste træf fra en maskinpistol i et andet tårn.
- **Mod den optagende spillers sigte:** dens egen tank sender sin sigtevinkel i verden (mod uret fra
  øst), pitch og afstand. Skrogets heading plus tårnets drejning ligger inden for en halv grad
  (median) af sigtet.

**Serverreplays** (0xF074) sender hver tanks tilstand i samme layout, efterfulgt af deres egne data,
så hvert tårn, hvis to vinkler ligger inden for tilstanden, læses (mindst hovedtårnet for næsten
hver tankrække). Det er tårnet, ikke kameraet:

- **Mod skuddene**, som ovenfor: pr. kamp over 90 % inden for 3 grader i heading og 99 % i elevation.
- **Mod udsynet:** en serverreplay sender hver spillers sigte (`viewYaw`, `viewPitch`). Tårnet følger
  udsynet inden for en halv grad (median), men drejer langt langsommere, end udsynet svinger, som et
  tårndrev gør (`selfCheck.turretVsView`).
- **Men ikke altid i et drevs hastighed:** prøve for prøve springer den værdi, der sendes, nogle gange
  op på sigtet, når sigtet er tæt på kanonen, hurtigere end noget drev kan dreje.

Så tabellen holder tårnet **holdt til sit drev**: `turretYaw` / `gunPitch` bevæger sig mod den værdi,
der sendes, med højst hovedkanonens drejehastighed fra installationens køretøjsfil (gange 1,3 for
mandskabets færdigheder og modifikationer; 45 og 20 grader i sekundet, hvor installationen ikke navngiver
nogen). Ved hvert træf fra hovedkanonen sættes tårnet nøjagtigt på skudlinjen, og et baglæns pas bringer
det derhen i tide (`selfCheck.turretLimit`). `shot`-rækken bærer også `turretYaw` / `gunPitch`. Den værdi,
der sendes, bliver i `turretYawRaw` / `gunPitchRaw`. En tank, hvis tilstand ikke bærer et tårn, har tomme
tårnkolonner (vieweren kan falde tilbage til `viewYaw`).
`gunPitch` ligger lidt over `viewPitch` på afstand: kanonens hævning for granatens fald.

Skibes tilstande har et andet layout; deres tårne læses ikke. Fly sender ingen hoved- eller sigteretning;
luftværnskanonernes meddelelse 0xD020 forbliver ulæst.

## Kameraet {#the-camera}

Meddelelse 0xD043, ca. 20 i sekundet, er den optagende spillers eget replay-kamera: felt 1 en kvaternion,
der drejer kameraets forside hen til, hvor det kigger; 2 kameraets placering i forhold til det køretøj, det
følger (m); 4 den samme forskydning i køretøjets egen ramme (x fremad, y op, z venstre); 5 hvor spilleren
sigter (en enhedsvektor); 3 zoomen (ca. 1,2 i en tanks tredjepersonsvisning, ca. 1,0 i et fly, højere i en
skytteskærm eller gennem kikkert). Kontrolleret: felt 4 er felt 2 drejet ind i køretøjets ramme, inden for
0,5 m for næsten hver meddelelse; kameraets forside har sigtets heading. Replayet sender intet synsfelt i
grader, kun zoomen.

Tabellen har kameraet som et spor for sig selv: art `camera`, spor `<player> camera #ca`, en række højst
hver 0,1 s, ved det fulgte køretøjs placering plus felt 2, kigget langs kvaternionen (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), med `zoom`, `aimHeading` og `aimPitch`, og `otherLife` det liv, det følger.
`selfCheck.camera` tæller rækkerne og kontrollen.

## Slutningen af et spor {#end-of-a-track}

Et spor tegnes fra sin første række til sin sidste. Når dets enhed er væk, før replayet slutter,
er dets sidste række en `despawn`-række ved dens sidste plads: på det tidspunkt, spillet fjernede
dens entitet (når det lå inden for 6 s af dens sidste sample), ellers ved dens sidste sample. Et spor
uden en varer til replayets slutning. Rækker i et spor kan ligge langt fra hinanden (en fjern enhed
eller et vrag opdateres hvert par sekund, et vrag nogle gange ikke i flere minutter): dens sidste
tilstand holder, indtil dens næste række kommer.

## Kampens tilstand {#battle-mode}

Headerens byte ved offset 688 holder sværhedsgraden i sine nederste fire bit:
0 arkade (AB), 5 realistisk (RB), 10 simulator (SB). Kontrolleret mod de kamptyper, replayene kendtes
for at være. Spilletilstanden er `ground`, når missionen lader stridsvogne spawne, ellers `naval`, når
den lader skibe spawne, ellers `air` (`allowedUnitTypes`); missionens egen tilstand kommer fra dens
nøgle (`missions/_Dom`), navngivet ud fra din installations `lang/missions_versus.csv`. Samme nøgle er
`<mode>`-delen af filnavnene og kamp-id'et (`Conq4`, `Dom`), udeladt, hvor headeren ingen har.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
