---
title: "Högg, skothríð og eldar"
nav_order: 13
lang: "is"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Högg, skothríð og eldar {#hits-gunfire-and-fires}

Fyrir lesendur sem vilja vita hvaðan dálkar högga, skotfæra og elda koma.
Athuganir gefa aðeins aðferðina og samræmið.

## Skothríð {#gunfire}

Hvert skot sem hitti einingu er í upptökunni (skilaboð 0xF0E9): `shot` röð á
stöðu skyttunnar á þeirri stundu sem höggið varð, `targetX/Y/Z` höggpunkturinn
(einingin sem varð fyrir höggi, færð um höggpunktinn í ramma hennar, snúin með
afstöðu hennar), stefnan að honum, `other` einingin sem varð fyrir höggi. Skeljar
og kúlur sem geiguðu eru ekki sendar: þær eru ekki einingar, og skilaboð
vopna á flugi geyma aðeins eldflaugar, flugskeyti, sprengjur og tundurskeyti.
Skot upptökumannsins eftir (`ammo` dálkurinn) fækka þegar hann skýtur, svo
hrinur hans sjást, en ekki hvert þau skot fóru. Þung loftvarnabyssur og
stórskotalið senda hvert stakt skot (`gun_shot`, engin stefna), 40 mm
loftvarnabyssur hrinur sínar (`fire_start`, `fire_stop`).

## Útkoma högga {#hit-outcomes}

Með hverju skothöggi á landeiningu sendir þjónninn skilaboð 0xF144 (UnitOnHit)
til einingarinnar: fjóra eins bætis reiti, sá fjórði bitar þess sem höggið
gerði (`selfCheck.unitMessages.outcome_*`):

| Biti | Merking | Sönnun |
|---|---|---|
| 0x20 | eigið högg skots | nær öll koma með 0xF0E9 höggi á eininguna innan 5 ms; án þess, með sprengingu (splash) |
| 0x01 | það komst í gegn (penetration) | hver skilaboð með 0x02, 0x04 eða 0x08 hafa það líka |
| 0x02 | krítískt högg | flestar færslur um krítísk högg hafa það, miklu oftar en tilviljun |
| 0x04 | eyðilögð | flest koma með dráps færslu og dauða einingarinnar innan sekúndu |
| 0x08 | mikill skaði | sumar færslur um krítísk högg hafa það; sjaldgæft annars |

`hitOutcome` tekur það versta: `kill` (0x04), `critical` (0x02 eða 0x08),
`penetration` (0x01), `nonpenetration` (0x20 eitt). Högg er parað við næstu
óparaða 0xF144 með 0x20 til einingar þess innan 5 ms. Höggmyndavél leiksins
greinir ricochet frá non-penetration, en enginn biti eða reitur sem fannst hér
gerir það: fyrstu þrjú bætin breytast frá höggi til höggs og eru ekki þekkt.
Biðlaraupptökur senda 0xF144 aðeins fyrir eigin flugvél upptökumannsins, allir
bitar hreinir: högg á flugvélar og skip hafa enga útkomu.

## Skotfæri {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Sprengiskot eða ekki.** Skel sem springur sendir 0xF133 (UnitOnExplosion)
  með uid skyttunnar og númeri höggsins; högg með slíkt er `explosive`, hin
  `kinetic`.
* **Byssan og rauf hennar.** 0xF0BD (UnitBulletRearm) er næsta skot sem er
  hlaðið: vísir vopnsins í vopnalista farartækisins, skotfæraraufin og skotin
  eftir. Hjá handhleðslu kemur það stöðugum endurhleðslutíma eftir hvert högg
  hennar, hjá sjálfvirkri fallbyssu broti úr sekúndu eftir. Högg skyttu eru
  flokkuð eftir farartæki, undirskrift og hrinu; flokkur er vopns þegar það
  vopn hleður skot innan 20 s eftir helming högga hans eða fleiri með stöðugri
  töf. `ammoSlot` er `weapon/slot`, raufin sem var hlaðin fyrir höggið: líklega
  sú sem var skotið, nema spilarinn skipti um skotfæri þar á milli.
  Vélbyssur senda ekkert 0xF0BD.
* **Skelin.** Vopn drápsins er auðkenni skeljarinnar (`125mm_3bm46`); síðasta
  högg drápsmannsins á fórnarlambið gefur það raufinni hjá þeirri skyttu, þar
  sem kaliber byssunnar stemmir. Tegund hennar og kaliber eru úr vopnaskránni
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Kaliberið** hjá hinum: kaliber vopns raufarinnar; hjá vélbyssuflokki það
  eina vélbyssukaliber sem undirskriftin getur haft; annars kaliber
  aðalbyssu farartækisins. Án uppsetningarinnar (`--game`) er engin tegund, nafn
  eða kaliber umfram `explosive` / `kinetic`.

Ekki fundið: ricochet. Nokkur fleiri skilaboð bera skyttu og númer höggsins
(0xF0C2, líklega leið höggmyndavélarinnar um farartækið; 0xF117, 0xF13C,
0xF13E); þau eru geymd í hliðarskránni, ekki afkóðuð. Non-penetration helst
`nonpenetration`.

## Eldar í farartækjum {#vehicle-fires}

Farartæki í ljósum logum er sýnt öllum biðlurum: þjónninn sendir
einingarskilaboð til farartækisins (atburður `0a519c58`) sem telja upp eldana
sem brenna á því, í hvert sinn sem listinn breytist. Fyrir hvern eld: tvö 16
bita auðkenni (hið síðara hnútur í skaðamódeli), tegund hans, og -1 þar til
eldurinn nær sér. Eldur sem högg kveikti fær líka skilaboð með punktinum þar
sem hann brennur, í ramma farartækisins (x fram, y upp, z vinstri).

Raðir: `fire_on` þegar eldur birtist í listanum, `fire_off` þegar hann er
horfinn, við farartækið, með `fireId` (`first:node`), `fireKind` og, fyrir
elda sem högg kveikti, `fireLocalX/Y/Z` (fram, upp, hægri). Þegar farartæki er
dautt er listi þess oft ekki sendur aftur: eldar þess enda með flaki þess,
annars með einingu þess, annars með upptökunni (`selfCheck.fires`).

Athugað: í hvert sinn sem fjöldi slökkvitækja skriðdreka fækkaði fór eldur af
lista hans innan brots úr sekúndu; flestir eldpunktar liggja sömu megin á
farartækinu og höggið sem kveikti þá. Tegundirnar eru tölur; hvað þær nefna er
ekki vitað, né hvaða hluti hnútur er. Flugvélar senda engan slíkan lista:
flugvél í ljósum logum er ekki lesin.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
