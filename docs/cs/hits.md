---
title: "Zásahy, palba a požáry"
nav_order: 13
lang: cs
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Zásahy, palba a požáry {#hits-gunfire-and-fires}

Pro čtenáře, kteří chtějí vědět, odkud se berou sloupce zásahů, munice a požárů. Kontroly uvádějí jen metodu
a míru shody.

## Palba {#gunfire}

Každý projektil, který zasáhl jednotku, je v replayi (zpráva 0xF0E9): řádek `shot` na pozici střelce v okamžiku
zásahu, `targetX/Y/Z` místo zásahu (zasažená jednotka, posunutá o bod zásahu v jejím rámci a otočená jejím postojem),
směr k ní, `other` zasažená jednotka. Střely a kulky, které minuly, se neposílají: nejsou to entity a zprávy
o zbraních za letu obsahují jen rakety, řízené střely, bomby a torpéda. Zbývající náboje hráče, který nahrával
(jeho sloupec `ammo`), klesají, jak střílí, takže se dají rozpoznat jeho dávky, ale ne kam ty náboje letěly.
Těžká protiletadlová a dělostřelecká zbraň posílají každou jednotlivou ránu (`gun_shot`, bez směru), 40mm
protiletadlová děla své dávky (`fire_start`, `fire_stop`).

## Výsledky zásahů {#hit-outcomes}

U každého zásahu projektilem do pozemní jednotky posílá server zprávu 0xF144 (UnitOnHit) té jednotce: čtyři
jednobajtová pole, čtvrté jsou bity toho, co zásah udělal (`selfCheck.unitMessages.outcome_*`):

| Bit | Význam | Důkaz |
|---|---|---|
| 0x20 | vlastní zásah projektilu | skoro všechny přicházejí se zásahem 0xF0E9 na jednotku do 5 ms; bez něj s výbuchem (tříštivý) |
| 0x01 | prošel (průraz) | každá zpráva s 0x02, 0x04 nebo 0x08 ho má také |
| 0x02 | kritický zásah | většina záznamů kritických zásahů ho má, mnohem častěji, než by bylo náhodou |
| 0x04 | zničeno | většina přichází se záznamem zabití a smrtí jednotky do jedné vteřiny |
| 0x08 | těžké poškození | některé záznamy kritických zásahů ho mají; jinak zřídka |

`hitOutcome` bere nejhorší: `kill` (0x04), `critical` (0x02 nebo 0x08), `penetration` (0x01),
`nonpenetration` (samotné 0x20). Zásah se páruje s nejbližší nespárovanou zprávou 0xF144 s 0x20 na jeho jednotku
do 5 ms. Kamera zásahu ve hře rozliší odraz od neprůrazu, ale žádný bit ani pole nalezené zde to nedělá: první
tři bajty se od zásahu k zásahu mění a nejsou známy. Replaye klienta posílají 0xF144 jen pro vlastní letadlo hráče,
který nahrával, se všemi bity vynulovanými: zásahy letadel a lodí nemají výsledek.

## Munice {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Výbušná nebo ne.** Střela, která vybuchne, pošle 0xF133 (UnitOnExplosion) s uid střelce a číslem zásahu;
  zásah s ní je `explosive`, ostatní `kinetic`.
* **Kanón a jeho slot.** 0xF0BD (UnitBulletRearm) je další nabitý náboj: index zbraně v seznamu zbraní vozidla,
  slot munice a zbývající náboje. Nabíjení manuálním nabíječem přichází stálou dobou přebíjení po každém jeho
  zásahu, nabíjení automatického kanónu zlomek vteřiny po něm. Zásahy střelce se seskupují podle vozidla, podpisu
  a dávky; skupina patří zbrani, když ta zbraň nabije náboj do 20 s po polovině a více jejích zásahů se stálým
  zpožděním. `ammoSlot` je `weapon/slot`, slot nabitý před zásahem: pravděpodobně ten vystřelený, pokud hráč
  mezi tím munici nezměnil. Kulomety neposílají 0xF0BD.
* **Střela.** Zbraň, kterou zabil, je id střely (`125mm_3bm46`); poslední zásah zabijáka na oběť ho přiřadí slotu
  toho střelce, kde ráže děla sedí. Její typ a ráže jsou ze souboru zbraně (`bulletName`, `bulletType`, `caliber`;
  `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Ráže** zbytku: slotu zbraně; skupiny kulometů ta jediná ráže kulometu, kterou její podpis může mít; jinak hlavní
  dělo vozidla. Bez instalace (`--game`) není typ, název ani ráže nad `explosive` / `kinetic`.

Nenalezeno: odraz. Několik dalších zpráv nese střelce a číslo zásahu (0xF0C2, pravděpodobně dráha kamery zásahu
vozidlem; 0xF117, 0xF13C, 0xF13E); uchovávají se v doplňku, nedekódují se. Neprůraz zůstává `nonpenetration`.

## Požáry vozidel {#vehicle-fires}

Vozidlo v plamenech vidí každý klient: server posílá vozidlu zprávu entity (událost `0a519c58`) s výpisem požárů,
které na něm hoří, pokaždé, když se výpis změní. Na každý požár: dvě 16bitová id (druhé je uzel modelu poškození),
jeho druh, a -1, dokud se požár neuchytí. Požár zapálený zásahem dostane navíc zprávu s místem, kde hoří, v rámci
vozidla (x dopředu, y nahoru, z vlevo).

Řádky: `fire_on`, když se požár objeví ve výpisu, `fire_off`, když zmizí, u vozidla, s `fireId` (`first:node`),
`fireKind` a u požárů, které zapálil zásah, `fireLocalX/Y/Z` (dopředu, nahoru, vpravo). Jakmile je vozidlo mrtvé,
jeho výpis se často už neposílá: jeho požáry skončí s jeho vrakem, jinak s jeho entitou, jinak s replayem
(`selfCheck.fires`).

Ověřeno: pokaždé, když počet hasicích přístrojů tanku klesl, požár zmizel z jeho výpisu do zlomku vteřiny; většina
bodů požárů leží na stejné straně vozidla jako zásah, který je zapálil. Druhy jsou čísla; co pojmenovávají, není
známo, stejně jako to, která část je uzel. Letadla takový výpis neposílají: letadlo v plamenech se nečte.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
