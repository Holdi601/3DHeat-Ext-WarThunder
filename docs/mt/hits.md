---
title: "Daqqiet, sparar u nirien"
nav_order: 13
lang: "mt"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Daqqiet, sparar u nirien {#hits-gunfire-and-fires}

Għal min irid jaf minn fejn jiġu l-kolonni tad-daqqiet, tal-munizzjon u tan-nirien. Il-kontrolli
jagħtu biss il-metodu u l-qbil.

## Sparar {#gunfire}

Kull projettil li laqat unità jinsab fir-ripetizzjoni (messaġġ 0xF0E9): ringiela `shot` fil-pożizzjoni
tax-xutter fil-mument tad-daqqa, `targetX/Y/Z` il-punt tad-daqqa (l-unità li nħabtet, imċaqalqa mill-punt
tad-daqqa fil-qafas tagħha, imdawra bl-attitudni tagħha), id-direzzjoni lejha, `other` l-unità li nħabtet.
Qxur u balal li tilfu mhumiex mibgħuta: mhumiex entitajiet, u l-messaġġi tal-armi fit-titjira jżommu
biss rokits, missili, bombi u torpidnijiet. Ir-rawnds li fadal tal-plejer li rreġistra (il-kolonna `ammo`
tiegħu) jaqgħu waqt li jispara, għalhekk is-sensiliet tiegħu jistgħu jinġiebu, imma mhux fejn marru dawk
ir-rawnds. L-AA tqila u l-artillerija jibagħtu kull sparatura waħda (`gun_shot`, bla direzzjoni), kanuni
AA ta' 40 mm is-sensiliet tagħhom (`fire_start`, `fire_stop`).

## Riżultati tad-daqqiet {#hit-outcomes}

Ma' kull daqqa ta' projettil fuq unità tal-art is-server jibgħat il-messaġġ 0xF144 (UnitOnHit) lill-unità:
erba' kampi ta' byte wieħed, ir-raba' l-bits ta' dak li għamlet id-daqqa
(`selfCheck.unitMessages.outcome_*`):

| Bit | Tifsira | Evidenza |
|---|---|---|
| 0x20 | daqqa proprja ta' projettil | kważi kollha jiġu b'daqqa 0xF0E9 fuq l-unità fi ħdan 5 ms; mingħajrha, b'isplużjoni (splash) |
| 0x01 | għadda minn ġewwa (penetrazzjoni) | kull messaġġ b'0x02, 0x04 jew 0x08 għandu wkoll dan |
| 0x02 | daqqa kritika | il-biċċa l-kbira tar-records ta' daqqa kritika għandhom dan, ħafna aktar spiss milli b'xorti |
| 0x04 | meqruda | il-biċċa l-kbira jiġu b'record ta' qtil u l-mewt tal-unità fi ħdan sekonda |
| 0x08 | ħsara kbira | xi records ta' daqqa kritika għandhom dan; rari inkella |

`hitOutcome` jieħu l-agħar: `kill` (0x04), `critical` (0x02 jew 0x08), `penetration` (0x01),
`nonpenetration` (0x20 waħdu). Daqqa tiġi mqabbla mal-eqreb 0xF144 mhux imqabbel b'0x20 lill-unità
tagħha fi ħdan 5 ms. Il-kamera tad-daqqiet tal-logħba tiddistingwi ricochet minn non-penetrazzjoni, imma
ebda bit jew kamp misjub hawn ma jagħmel hekk: l-ewwel tliet bytes ivarjaw minn daqqa għal oħra u
mhumiex magħrufa. Ripetizzjonijiet tal-klijent jibagħtu 0xF144 biss għall-ajruplan proprju tal-plejer
li rreġistra, bil-bits kollha ċari: daqqiet fuq ajruplani u vapuri m'għandhomx riżultat.

## Munizzjon {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Esplussiv jew le.** Qoxra li tinfaqa' tibgħat 0xF133 (UnitOnExplosion) bl-uid tax-xutter u
  n-numru tad-daqqa; daqqa b'wieħed hija `explosive`, il-bqija `kinetic`.
* **Il-kanun u s-slot tiegħu.** 0xF0BD (UnitBulletRearm) huwa r-rawnd li jmiss mgħobbi: l-indiċi tal-arma
  fil-lista tal-armi tal-vettura, is-slot tal-munizzjon u r-rawnds li fadal. Dak ta' loader manwali
  jiġi ħin kostanti ta' reload wara kull waħda mid-daqqiet tiegħu, dak ta' autocannon frazzjoni ta' sekonda
  wara. Id-daqqiet ta' xutter jiġu miġbura skont vettura, firma u sensiela; grupp huwa ta' arma meta
  dik l-arma tgħabbi rawnd fi ħdan 20 s wara nofs id-daqqiet tiegħu jew aktar b'dewmien kostanti.
  `ammoSlot` huwa `weapon/slot`, is-slot imgħobbi qabel id-daqqa: probabbilment dak sparat, ħlief
  jekk il-plejer biddel il-munizzjon bejn żmien u ieħor. Magna guns ma jibagħtu l-ebda 0xF0BD.
* **Il-qoxra.** L-arma ta' qtil hija l-id tal-qoxra (`125mm_3bm46`); l-aħħar daqqa tal-qattiel fuq
  il-vittma tagħtiha lis-slot ta' dak ix-xutter, fejn il-kalibru tal-kanun jaqbel. It-tip u l-kalibru
  tagħha huma tal-fajl tal-arma (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Il-kalibru** tal-bqija: dak tal-arma ta' slot; ta' grupp ta' magna guns dak l-uniku kalibru ta'
  magna gun li l-firma tiegħu jista' jkollha; inkella dak tal-kanun ewlieni tal-vettura. Mingħajr
  l-installazzjoni (`--game`) ma jkun hemm ebda tip, isem jew kalibru lil hinn minn `explosive` /
  `kinetic`.

Mhux misjub: ricochet. Diversi messaġġi oħra jġorru x-xutter u n-numru tad-daqqa (0xF0C2, probabbilment
il-mogħdija tal-kamera tad-daqqiet fil-vettura; 0xF117, 0xF13C, 0xF13E); jinżammu fis-sidecar, mhux
deċifrati. Non-penetrazzjoni tibqa' `nonpenetration`.

## Nirien tal-vetturi {#vehicle-fires}

Vettura li tinxtegħel tintwera lil kull klijent: is-server jibgħat messaġġ ta' entità lill-vettura
(avveniment `0a519c58`) li jelenka n-nirien li qed jaqbdu fuqha, kull darba li l-lista tinbidel. Għal
kull nar: żewġ ids ta' 16-il bit (it-tieni node tal-mudell tal-ħsara), it-tip tiegħu, u -1 sakemm in-nar
jaqbad. Nar mixgħul minn daqqa jirċievi wkoll messaġġ bil-punt fejn qed jaqbad, fil-qafas tal-vettura
(x 'il quddiem, y 'il fuq, z lejn ix-xellug).

Ringieli: `fire_on` meta nar jidher fil-lista, `fire_off` meta jkun marr, fuq il-vettura, bi `fireId`
(`first:node`), `fireKind` u, għal nirien li daqqa xegħlet, `fireLocalX/Y/Z` ('il quddiem, 'il fuq,
lejn il-lemin). Ladarba vettura tmut il-lista tagħha spiss ma terġax tintbagħat: in-nirien tagħha jispiċċaw
mal-wreck tagħha, inkella mal-entità tagħha, inkella mar-ripetizzjoni (`selfCheck.fires`).

Ikkontrollat: kull darba li l-għadd tal-estinguituri ta' tank niżel, nar ħareġ mil-lista tiegħu fi ħdan
frazzjoni ta' sekonda; il-biċċa l-kbira tal-punti tan-nirien jinsabu fl-istess naħa tal-vettura bħad-daqqa
li xegħlithom. It-tipi huma numri; dak li jsemmu mhux magħruf, u lanqas liema parti hija node. L-ajruplani
ma jibagħtu ebda lista bħal din: ajruplan jaqbad mhux moqri.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
