---
title: "Treffers, beschieting en branden"
nav_order: 13
lang: "nl"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Treffers, beschieting en branden {#hits-gunfire-and-fires}

Voor lezers die willen weten waar de kolommen van treffers, munitie en branden vandaan komen. Controles geven alleen de methode en de overeenstemming.

## Beschieting {#gunfire}

Elk projectiel dat een eenheid trof, staat in de replay (bericht 0xF0E9): een `shot`-rij op de positie van de schutter op het moment van de treffer, `targetX/Y/Z` het trefpunt (de getroffen eenheid, verschoven met het trefpunt in haar stelsel, gedraaid met haar houding), de richting ernaartoe, `other` de getroffen eenheid. Granaten en kogels die misten, worden niet gestuurd: het zijn geen entiteiten, en de berichten over wapens in de vlucht bevatten alleen raketten, missielen, raketten, bommen en torpedo's. De resterende rondes van de opnemende speler (zijn kolom `ammo`) dalen terwijl hij vuurt, dus zijn salvo's zijn te herkennen, maar niet waar die rondes terechtkwamen. Zware luchtafweer en artillerie sturen elk enkel schot (`gun_shot`, zonder richting), luchtafweergeschut van 40 mm hun salvo's (`fire_start`, `fire_stop`).

## Uitkomsten van treffers {#hit-outcomes}

Bij elke projectieltreffer op een grondeenheid stuurt de server bericht 0xF144 (UnitOnHit) naar de eenheid: vier velden van één byte, het vierde de bits van wat de treffer deed (`selfCheck.unitMessages.outcome_*`):

| Bit | Betekenis | Bewijs |
|---|---|---|
| 0x20 | de eigen treffer van een projectiel | bijna alle komen met een 0xF0E9-treffer op de eenheid binnen 5 ms; zonder die, met een explosie (splash) |
| 0x01 | het kwam erdoor (doordringing) | elk bericht met 0x02, 0x04 of 0x08 heeft het ook |
| 0x02 | kritieke treffer | de meeste records van een kritieke treffer hebben het, veel vaker dan toeval |
| 0x04 | vernietigd | de meeste komen met een killrecord en de dood van de eenheid binnen een seconde |
| 0x08 | zware schade | sommige records van een kritieke treffer hebben het; anders zeldzaam |

`hitOutcome` neemt het ergste: `kill` (0x04), `critical` (0x02 of 0x08), `penetration` (0x01), `nonpenetration` (0x20 alleen). Een treffer wordt gekoppeld aan de dichtstbijzijnde ongekoppelde 0xF144 met 0x20 bij zijn eenheid binnen 5 ms. De treffercamera van het spel onderscheidt een ricochet van een niet-doordringing, maar geen enkele bit of velden die hier gevonden zijn, doen dat: de eerste drie bytes variëren van treffer tot treffer en zijn niet bekend. Clientreplays sturen 0xF144 alleen voor het eigen vliegtuig van de opnemende speler, met alle bits uit: treffers op vliegtuigen en schepen hebben geen uitkomst.

## Munitie {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosief of niet.** Een granaat die openbarst, stuurt 0xF133 (UnitOnExplosion) met het uid van de schutter en het nummer van de treffer; een treffer met zo'n bericht is `explosive`, de rest `kinetic`.
* **Het kanon en zijn slot.** 0xF0BD (UnitBulletRearm) is de volgende ronde die geladen wordt: de index van het wapen in de wapenlijst van het voertuig, het munitieslot en de resterende rondes. Die van een handmatige lader komt een vaste laadtijd na elk van zijn treffers, die van een automatisch kanon een fractie van een seconde erna. De treffers van een schutter worden gegroepeerd per voertuig, signatuur en salvo; een groep is van een wapen wanneer dat wapen binnen 20 s na de helft of meer van haar treffers een ronde laadt, met een vaste vertraging. `ammoSlot` is `weapon/slot`, het slot dat vóór de treffer geladen was: waarschijnlijk het gebruikte, tenzij de speler er tussendoor de munitie veranderde. Machinegeweren sturen geen 0xF0BD.
* **De granaat.** De naam van een kill is het id van de granaat (`125mm_3bm46`); de laatste treffer van de killer op het slachtoffer geeft die aan het slot van die schutter, waar het kaliber van het kanon klopt. Het type en kaliber komen uit het wapenbestand (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Het kaliber** van de rest: dat van het wapen van een slot; dat van een groep machinegeweren het ene kaliber dat hun signatuur kan hebben; anders dat van het hoofdkanon van het voertuig. Zonder de installatie (`--game`) is er geen type, naam of kaliber buiten `explosive` / `kinetic`.

Niet gevonden: ricochet. Verschillende andere berichten dragen de schutter en het nummer van de treffer (0xF0C2, waarschijnlijk het pad van de trefferkamera door het voertuig; 0xF117, 0xF13C, 0xF13E); ze worden in de sidecar bewaard, niet gedecodeerd. Een niet-doordringing blijft `nonpenetration`.

## Branden van voertuigen {#vehicle-fires}

Een voertuig in brand wordt aan elke client getoond: de server stuurt een entiteitsbericht naar het voertuig (gebeurtenis `0a519c58`) met de branden die erop woeden, telkens als de lijst verandert. Per brand: twee id's van 16 bits (het tweede een knoop van het schademodel), zijn soort, en -1 tot de brand vat krijgt. Een brand die door een treffer ontstaat, krijgt ook een bericht met het punt waar hij brandt, in het stelsel van het voertuig (x vooruit, y omhoog, z links).

Rijen: `fire_on` wanneer een brand in de lijst verschijnt, `fire_off` wanneer hij weg is, bij het voertuig, met `fireId` (`first:node`), `fireKind` en, voor branden die een treffer aanstak, `fireLocalX/Y/Z` (vooruit, omhoog, rechts). Zodra een voertuig dood is, wordt zijn lijst vaak niet meer gestuurd: zijn branden eindigen met zijn wrak, anders met zijn entiteit, anders met de replay (`selfCheck.fires`).

Gecontroleerd: elke keer dat het aantal blusapparaten van een tank daalde, verdween binnen een fractie van een seconde een brand uit zijn lijst; de meeste brandpunten liggen aan dezelfde kant van het voertuig als de treffer die ze aanstak. De soorten zijn getallen; wat ze benoemen is niet bekend, en ook niet welk onderdeel een knoop is. Vliegtuigen sturen geen zo'n lijst: een vliegtuig in brand wordt niet gelezen.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
