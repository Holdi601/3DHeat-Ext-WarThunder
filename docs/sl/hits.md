---
title: Zadetki, streljanje in požari
nav_order: 13
lang: "sl"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Zadetki, streljanje in požari {#hits-gunfire-and-fires}

Za bralce, ki želijo vedeti, od kod prihajajo stolpci za zadetke, strelivo in požare. Preverjanja podajajo samo
metodo in skladnost.

## Streljanje {#gunfire}

Vsak izstrelek, ki je zadel enoto, je v posnetku (sporočilo 0xF0E9): vrstica `shot` na položaju strelca v trenutku
zadetka, `targetX/Y/Z` točka zadetka (zadeta enota, premaknjena za točko zadetka v njenem okviru, obrnjena z njeno držo),
smer proti njej, `other` zadeta enota. Naboji in krogle, ki so zgrešili, niso poslani: niso entitete, sporočila o orožjih
v letu pa hranijo samo rakete, izstrelke vodenega orožja, bombe in torpede. Preostali naboji igralca, ki je snemal
(njegov stolpec `ammo`), padajo, ko strelja, zato se njegove rafale dajo razločiti, ne pa, kam so ti naboji šli. Težki
protiletalski in artilerijski topovi pošljejo vsak posamezen strel (`gun_shot`, brez smeri), 40 mm protiletalski topovi
pa svoje rafale (`fire_start`, `fire_stop`).

## Izidi zadetkov {#hit-outcomes}

Pri vsakem zadetku izstrelka na kopensko enoto strežnik enoti pošlje sporočilo 0xF144 (UnitOnHit): štiri enobajtna
polja, četrto je biti, kaj je zadetek naredil (`selfCheck.unitMessages.outcome_*`):

| Bit | Pomen | Dokaz |
|---|---|---|
| 0x20 | lastni zadetek izstrelka | skoraj vsi pridejo z zadetkom 0xF0E9 na enoto v 5 ms; brez njega, z eksplozijo (razcep) |
| 0x01 | prodrl je (prebojnost) | vsako sporočilo z 0x02, 0x04 ali 0x08 ga ima tudi |
| 0x02 | kritičen zadetek | večina zapisov kritičnih zadetkov ga ima, veliko pogosteje, kot bi bilo naključno |
| 0x04 | uničen | večina pride z zapisom ubijanja in smrtjo enote v eni sekundi |
| 0x08 | huda poškodba | nekateri zapisi kritičnih zadetkov ga imajo; sicer redko |

`hitOutcome` vzame najhujše: `kill` (0x04), `critical` (0x02 ali 0x08), `penetration` (0x01),
`nonpenetration` (samo 0x20). Zadetek se poveže z najbližjim neparjenim 0xF144 z 0x20 na njegovo enoto v 5 ms. Igrina
kamera zadetka razlikuje odboj od neprodora, vendar tega ne pove noben bit ali polje, ki je tukaj najdeno: prvi trije
bajti se od zadetka do zadetka spreminjajo in njihov pomen ni znan. Posnetki odjemalca pošljejo 0xF144 samo za lastno
letalo igralca, ki je snemal, z vsemi biti pobrisanimi: zadetki letal in ladij nimajo izida.

## Strelivo {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Eksploziven ali ne.** Izstrelek, ki eksplodira, pošlje 0xF133 (UnitOnExplosion) z uid-jem strelca in številko
  zadetka; zadetek s tem je `explosive`, ostali `kinetic`.
* **Top in njegova reža.** 0xF0BD (UnitBulletRearm) je naslednji nabit naboj: indeks orožja na seznamu orožij vozila,
  reža streliva in preostali naboji. Ročno nabijanje nabijalca pride stalen čas nabijanja po vsakem njegovem zadetku,
  avtomatski top pa delček sekunde po. Zadetki strelca so razvrščeni po vozilu, podpisu in rafali; skupina pripada
  orožju, kadar to orožje nabije naboj v 20 s po polovici ali več njenih zadetkov pri stalnem zamiku. `ammoSlot` je
  `weapon/slot`, reža, nabita pred zadetkom: verjetno tista, ki je streljala, razen če je igralec vmes zamenjal strelivo.
  Strojnice ne pošiljajo 0xF0BD.
* **Izstrelek.** Orožje ubijanja je identifikator izstrelka (`125mm_3bm46`); zadnji zadetek ubijalca na žrtev ga da
  reži tega strelca, kjer se kalibra topa ujema. Njegov tip in kalibra sta iz datoteke orožja (`bulletName`, `bulletType`,
  `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kalibra ostalega:** reže orožja; skupine strojnic ena kalibra strojnice, ki ga njihov podpis lahko ima; sicer glavni
  top vozila. Brez namestitve (`--game`) ni tipa, imena ali kalibra razen `explosive` / `kinetic`.

Ni najdeno: odboj. Več drugih sporočil nosi strelca in številko zadetka (0xF0C2, verjetno pot kamere zadetka skozi
vozilo; 0xF117, 0xF13C, 0xF13E); shranjena so v spremljevalni datoteki, niso dekodirana. Neprodor ostane
`nonpenetration`.

## Požari vozil {#vehicle-fires}

Vozilo v ognju je prikazano vsakemu odjemalcu: strežnik vozilu pošlje sporočilo entitete (dogodek `0a519c58`), ki
navaja požare, ki gorijo na njem, vsakič, ko se seznam spremeni. Za vsak požar: dva 16-bitna identifikatorja (drugi je
vozlišče modela poškodb), njegova vrsta in -1, dokler požar ne zajame. Požar, ki ga je prižgal zadetek, dobi tudi
sporočilo s točko, kjer gori, v okviru vozila (x naprej, y gor, z levo).

Vrstice: `fire_on`, ko se požar pojavi na seznamu, `fire_off`, ko ga ni več, na vozilu, z `fireId` (`first:node`),
`fireKind` in za požare, ki jih je prižgal zadetek, `fireLocalX/Y/Z` (naprej, gor, desno). Ko je vozilo mrtvo, seznam
pogosto ni več poslan: njegovi požari se končajo z njegovo olupino, sicer z njegovo entiteto, sicer s posnetkom
(`selfCheck.fires`).

Preverjeno: vsakič, ko je število gasilnikov tanka padlo, je požar zapustil seznam v delčku sekunde; večina točk požara
leži na isti strani vozila kot zadetek, ki ga je prižgal. Vrste so številke; kaj pomenijo, ni znano, prav tako ni znano,
kateri del je vozlišče. Letala takega seznama ne pošiljajo: letalo v ognju ni prebrano.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
