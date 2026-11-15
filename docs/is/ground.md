---
title: "Landfarartæki og myndavél"
nav_order: 12
lang: "is"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Landfarartæki og myndavél {#ground-units-and-camera}

Fyrir lesendur sem vilja vita hvaðan dálkar turna, myndavélar og bardagahams
koma og hversu mikið má treysta þeim. Athuganir gefa aðeins aðferðina og
samræmið.

## Turnar {#turrets}

Landástand skriðdreka (16 bita afstaða) geymir, á eftir stöðunni, 141 bita sem
eru ekki lesnir, svo fyrir hvern turn 62 bita: snúning turnsins og halla
byssunnar (16 bitar hvort, 360/65536 gráður á skref, með formerki) og 30 bita
sem eru ekki lesnir; svo fyllingu, og á sumum ástöndum 200 bita til viðbótar.
Fjöldi turna er bætið sem sent er á undan ástandinu. Ástand sem lengdin passar
ekki fyrir gefur enga turna (kyrrstæðar einingar senda styttra ástand).
Snúningurinn (yaw) er miðað við skrokkinn, réttsælis jákvætt, 0 beint áfram;
hallinn (pitch) miðað við skrokkinn, upp jákvætt.

Hvernig það var athugað:

- **Gegn skotunum:** fyrir hvert högg skriðdreka, heimsstefna aðalbyssu hans
  (afstaða skrokks snúin með snúningi turns og halla byssu) gegn línunni frá
  skyttunni að einingunni sem varð fyrir höggi, í að minnsta kosti 30 m fjarlægð:
  fyrir hvern bardaga miðgildi um 98 % innan 3 gráða í stefnu og 99 % í hæð
  (`selfCheck.turretsVsShots`). Hin eru aðallega högg vélbyssu í öðrum turni.
- **Gegn miðun upptökumannsins:** hans eigin skriðdreki sendir heimshorn
  miðunar sinnar (rangsælis frá austri), halla og fjarlægð. Stefna skrokksins
  plús snúningur turnsins liggur innan hálfrar gráðu (miðgildi) frá miðuninni.

**Þjónsupptökur** (0xF074) senda ástand hvers skriðdreka í sama sniði, á eftir
fylgja eigin gögn þeirra, svo hver turn sem bæði hornin liggja inni í ástandinu
er lesinn (að minnsta kosti aðalturninn fyrir nær hverja skriðdrekaröð). Þetta
er turninn, ekki myndavélin:

- **Gegn skotunum**, eins og að ofan: fyrir hvern bardaga yfir 90 % innan
  3 gráða í stefnu og 99 % í hæð.
- **Gegn sjónstefnunni:** þjónsupptaka sendir miðun hvers spilara
  (`viewYaw`, `viewPitch`). Turninn fylgir sjónstefnunni innan hálfrar gráðu
  (miðgildi), en snýst mun hægar en sjónstefnan sveiflast, eins og turndrif
  gerir (`selfCheck.turretVsView`).
- **En ekki alltaf á hraða drifsins:** sýni fyrir sýni stekkur gildið eins og
  það var sent stundum á miðunina þegar miðunin er nálægt byssunni, hraðar en
  nokkurt drif snýst.

Taflan geymir því turninn **haldinn við drifið sitt**: `turretYaw` /
`gunPitch` færast í átt að gildinu eins og það var sent á ekki meiri hraða en
snúningshraða aðalbyssunnar úr farartækisskrá uppsetningarinnar (sinnum 1,3
fyrir hæfni áhafnar og breytingar; 45 og 20 gráður á sekúndu þar sem
uppsetningin nefnir engan). Við hvert högg aðalbyssunnar er turninn stilltur
nákvæmlega á línu skotsins og afturábak umferð kemur honum þangað í tæka tíð
(`selfCheck.turretLimit`). `shot` röðin ber líka þetta `turretYaw` /
`gunPitch`. Gildið eins og það var sent helst í `turretYawRaw` /
`gunPitchRaw`. Skriðdreki þar sem ástandið ber engan turn hefur tóma turndálka
(skoðarinn getur gripið til `viewYaw`). `gunPitch` liggur örlítið yfir
`viewPitch` á færi: hæð byssunnar vegna fallsins á skelinni.

Ástand skipa hefur annað snið; turnar þeirra eru ekki lesnir. Flugvélar senda
enga höfuð- eða sjónstefnu; skilaboð 0xD020 loftvarnabyssanna haldast ólesin.

## Myndavélin {#the-camera}

Skilaboð 0xD043, um 20 á sekúndu, eru eigin upptökumyndavél upptökumannsins:
reitur 1 kvaternjón sem snýr framstefnu myndavélarinnar þangað sem hún lítur;
2 staða myndavélarinnar frá farartækinu sem hún fylgir (m); 4 sama færsla í
eigin ramma farartækisins (x fram, y upp, z vinstri); 5 hvert spilarinn miðar
(einingarvigur); 3 aðdrátturinn (um 1,2 í þriðju persónu sýn skriðdreka, um
1,0 í flugvél, hærri í sjónauka skyttu eða gegnum handsjónauka). Athugað:
reitur 4 er reitur 2 snúinn í ramma farartækisins, innan 0,5 m fyrir nær hver
skilaboð; framstefna myndavélarinnar hefur stefnu miðunarinnar. Upptakan
sendir ekkert sjónsvið í gráðum, aðeins aðdráttinn.

Taflan hefur myndavélina sem eigin feril: kind `camera`, track
`<player> camera #ca`, röð í mesta lagi á 0,1 s fresti, á stað farartækisins
sem er fylgt plús reit 2, horfir eftir kvaternjóninu (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), með `zoom`, `aimHeading` og `aimPitch`, og `otherLife` lífið
sem hún fylgir. `selfCheck.camera` telur raðirnar og athugunina.

## Endir ferils {#end-of-a-track}

Ferill er teiknaður frá fyrstu röð sinni til hinnar síðustu. Þegar eining
hans er horfin áður en upptakan endar er síðasta röð hans `despawn` röð á
síðasta stað hans: á þeim tíma sem leikurinn fjarlægði einingu hans (þegar það
kom innan 6 s frá síðasta sýni hans), annars á síðasta sýni hans. Ferill án
slíkrar varir til loka upptökunnar. Raðir eins ferils geta verið langt hver frá
annarri (fjarlæg eining eða flak er endurnýjað á nokkurra sekúndna fresti,
flak stundum ekki í mínútur): síðasta ástand þess gildir þar til næsta röð
þess kemur.

## Bardagahamur {#battle-mode}

Bæti hausins á offset 688 geymir erfiðleikastigið í fjórum lægstu bitunum:
0 arcade (AB), 5 realistic (RB), 10 simulator (SB). Athugað gegn
bardagategundum sem vitað var að upptökurnar voru. Leikjahamurinn (game mode)
er `ground` þegar verkefnið leyfir skriðdrekum að koma fram, annars `naval`
þegar það leyfir skipum, annars `air` (`allowedUnitTypes`); eigin hamur
verkefnisins kemur úr lykli þess (`missions/_Dom`), nefndur úr
`lang/missions_versus.csv` í þinni uppsetningu. Sami lykill er `<mode>` hluti
skráarnafnanna og auðkennis leiksins (`Conq4`, `Dom`), felldur niður þar sem
hausinn hefur engan.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
