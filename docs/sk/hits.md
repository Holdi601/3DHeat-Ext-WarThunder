---
title: "Zásahy, streľba a požiare"
nav_order: 13
lang: "sk"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Zásahy, streľba a požiare {#hits-gunfire-and-fires}

Pre čitateľov, ktorí chcú vedieť, odkiaľ pochádzajú stĺpce zásahov, munície a požiarov. Kontroly uvádzajú len metódu a zhodu.

## Streľba {#gunfire}

Každý projektil, ktorý zasiahol jednotku, je v replaye (správa 0xF0E9): riadok `shot` na pozícii strelca v okamihu zásahu,
`targetX/Y/Z` bod zásahu (zasiahnutá jednotka, posunutá o bod zásahu v jej súradniciach, otočená jej postojom), smer k nej,
`other` zasiahnutá jednotka. Strely a guľky, ktoré minuli, sa neposielajú: nie sú entitami a správy o letiacich zbraniach
obsahujú len rakety, strely, bomby a torpéda. Náboje, ktoré hráč, ktorý replay nahral, ešte mal (jeho stĺpec `ammo`), klesajú,
ako strieľa, takže sa dajú rozoznať jeho dávky, ale nie kam tie náboje išli. Ťažké protilietadlové zbrane a delostrelectvo
posielajú každý jednotlivý výstrel (`gun_shot`, bez smeru), 40 mm protilietadlové zbrane svoje dávky (`fire_start`, `fire_stop`).

## Výsledky zásahov {#hit-outcomes}

Pri každom zásahu pozemnej jednotky projektilom posiela server správu 0xF144 (UnitOnHit) tej jednotke: štyri jednobajtové
polia, štvrté sú bity toho, čo zásah urobil (`selfCheck.unitMessages.outcome_*`):

| Bit | Význam | Dôkaz |
|---|---|---|
| 0x20 | vlastný zásah projektilu | takmer všetky prídu so zásahom 0xF0E9 na jednotku do 5 ms; bez neho s výbuchom (tlaková vlna) |
| 0x01 | prešiel (prienik) | každá správa s 0x02, 0x04 alebo 0x08 ho má tiež |
| 0x02 | kritický zásah | väčšina záznamov kritického zásahu ho má, oveľa častejšie, než by bola náhoda |
| 0x04 | zničenie | väčšina prichádza so záznamom o zabití a smrťou jednotky do sekundy |
| 0x08 | ťažké poškodenie | niektoré záznamy kritického zásahu ho majú; inak zriedka |

`hitOutcome` berie najhorší: `kill` (0x04), `critical` (0x02 alebo 0x08), `penetration` (0x01), `nonpenetration`
(0x20 samostatne). Zásah sa páruje s najbližšou nespárovanou správou 0xF144 s 0x20 na jeho jednotke do 5 ms. Kamera
zásahu hry rozozná odraz od neprieniku, ale žiadny bit ani pole tu nájdené to nerozlíšia: prvé tri bajty sa menia od zásahu
k zásahu a ich význam nie je známy. Klientské replaye posielajú 0xF144 len pre lietadlo hráča, ktorý replay nahral,
všetky bity vypnuté: zásahy lietadiel a lodí nemajú výsledok.

## Munícia {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Výbušná alebo nie.** Strela, ktorá vybuchne, pošle 0xF133 (UnitOnExplosion) s uid strelca a číslom zásahu;
  zásah s ním je `explosive`, ostatné `kinetic`.
* **Delo a jeho slot.** 0xF0BD (UnitBulletRearm) je ďalší nabitý náboj: index zbrane v zozname zbraní vozidla,
  slot munície a zostávajúce náboje. Nabíjačovo ručné doplnenie príde ustálený čas nabitia po každom svojom zásahu,
  automatického kanóna zlomok sekundy po ňom. Zásahy strelca sa zoskupujú podľa vozidla, podpisu a dávky; skupina patrí
  zbrani, keď táto zbraň nabije náboj do 20 s po polovici alebo viac jej zásahov pri ustálenom oneskorení. `ammoSlot` je
  `weapon/slot`, slot nabitý pred zásahom: pravdepodobne ten vystrelený, pokiaľ hráč medzitým munície nezmenil.
  Guľomety neposielajú 0xF0BD.
* **Strela.** Zbraň zabitia je id strely (`125mm_3bm46`); posledný zásah vraha na obeť ho dá slotu toho strelca,
  kde sa kalibre dela zhodujú. Jej typ a kalibrom je z súboru zbrane (`bulletName`, `bulletType`, `caliber`;
  `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kalibrom** ostatných: slotu zbrane; skupiny guľometov jediný kalibrom guľometu, aký jej podpis môže mať; inak hlavného
  dela vozidla. Bez inštalácie (`--game`) nie je typ, názov ani kalibrom nad `explosive` / `kinetic`.

Nenájdené: odraz. Niekoľko ďalších správ nesie strelca a číslo zásahu (0xF0C2, pravdepodobne dráha kamery zásahu
vozidlom; 0xF117, 0xF13C, 0xF13E); sú uchované v sprievodnom súbore, nedekódované. Neprieniku zostáva `nonpenetration`.

## Požiare vozidiel {#vehicle-fires}

Vozidlo v plameňoch vidí každý klient: server posiela vozidlu správu entity (udalosť `0a519c58`) so zoznamom požiarov, ktoré
na ňom horia, pri každej zmene zoznamu. Pri každom požiari dve 16-bitové id (druhé je uzol poškodeného modelu), jeho druh
a -1, kým sa požiar neuchytí. Požiar zapálený zásahom dostane aj správu s bodom, kde horí, v súradniciach vozidla
(x dopredu, y nahor, z vľavo).

Riadky: `fire_on`, keď sa požiar objaví v zozname, `fire_off`, keď zmizne, pri vozidle, s `fireId` (`first:node`),
`fireKind` a pri požiaroch zapálených zásahom `fireLocalX/Y/Z` (dopredu, nahor, doprava). Keď je vozidlo mŕtve, jeho zoznam
sa často už neposiela: jeho požiare skončia s jeho vrakom, inak s jeho entitou, inak s replayom (`selfCheck.fires`).

Overené: pri každom poklese počtu hasiacich prístrojov tanku požiar zmizol zo svojho zoznamu do zlomku sekundy; väčšina bodov
požiaru leží na tej istej strane vozidla ako zásah, ktorý ho zapálil. Druhy sú čísla; nie je známe, čo označujú, ani ktorá časť
je uzol. Lietadlá takýto zoznam neposielajú: lietadlo v plameňoch sa nečíta.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
