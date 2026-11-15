---
title: Osumat, tulitus ja palot
nav_order: 13
lang: fi
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Osumat, tulitus ja palot {#hits-gunfire-and-fires}

Tarkoitettu lukijoille, jotka haluavat tietää, mistä osuma-, ammus- ja palosarakkeet tulevat.
Tarkistukset antavat menetelmän ja yhteneväisyyden vain.

## Tulitus {#gunfire}

Jokainen ammus, joka osui yksikköön, on replayssa (viesti 0xF0E9): `shot`-rivi ampujan sijainnissa
osumahetkellä, `targetX/Y/Z` osumapiste (osuttu yksikkö, siirrettynä osumapisteellä sen koordinaatistossa,
käännettynä sen asennolla), suunta siihen, `other` osunut yksikkö. Ohi menneitä kuoria ja luoteja ei lähetetä:
ne eivät ole kokonaisuuksia, ja lennossa olevien aseiden viestit kattavat vain raketit, ohjukset, pommit ja
torpedot. Tallentavan pelaajan jäljellä olevat laukaukset (sen `ammo`-sarake) vähenevät sen ampuessa, joten
sen purskeet voidaan erottaa, mutta ei sitä, minne nuo laukaukset menivät. Raskas ilmatorjunta ja tykistö
lähettävät jokaisen yksittäisen laukauksen (`gun_shot`, ei suuntaa), 40 mm:n ilmatorjuntatykit niiden
purskeet (`fire_start`, `fire_stop`).

## Osuman lopputulokset {#hit-outcomes}

Jokaisesta osumasta maayksikköön palvelin lähettää viestin 0xF144 (UnitOnHit) yksikölle: neljä yhden tavun
kenttää, neljäs on bitit siitä, mitä osuma teki (`selfCheck.unitMessages.outcome_*`):

| Bitti | Merkitys | Todiste |
|---|---|---|
| 0x20 | ammuksen oma osuma | lähes kaikki tulevat 0xF0E9-osuman kanssa yksikköön 5 ms:n sisällä; ilman sitä räjähdyksen kanssa (roiske) |
| 0x01 | se läpäisi (läpäisy) | jokaisella viestillä, jossa on 0x02, 0x04 tai 0x08, on sekin |
| 0x02 | kriittinen osuma | useimmilla kriittisen osuman tietueilla on se, paljon useammin kuin sattumalta |
| 0x04 | tuhoutui | useimmat tulevat tappotietueen ja yksikön kuoleman kanssa sekunnin sisällä |
| 0x08 | raskas vaurio | joillakin kriittisen osuman tietueilla; muuten harvoin |

`hitOutcome` ottaa pahimman: `kill` (0x04), `critical` (0x02 tai 0x08), `penetration` (0x01),
`nonpenetration` (0x20 yksin). Osuma paritetaan lähimmän parittoman 0xF144-viestin kanssa, jossa on 0x20 ja
joka on sen yksikön 5 ms:n sisällä. Pelin osuman kamera erottaa kimpoamisen läpäisemättömästä osumasta, mutta
mikään täällä löydetty bitti tai kenttä ei tee sitä: kolme ensimmäistä tavua vaihtelevat osumasta toiseen,
eikä niiden merkitystä tiedetä. Asiakasreplayt lähettävät 0xF144:n vain tallentavan pelaajan omalle
lentokoneelle, kaikki bitit pois: lentokoneiden ja laivojen osumilla ei ole lopputulosta.

## Ammukset {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Räjähtävä tai ei.** Ammus, joka purkautuu, lähettää 0xF133 (UnitOnExplosion) ampujan uid:n ja osuman
  numeron kanssa; osuma, jolla on se, on `explosive`, muut `kinetic`.
* **Tykki ja sen paikka.** 0xF0BD (UnitBulletRearm) on seuraava ladattu laukaus: aseen indeksi ajoneuvon
  aselistassa, ammuspaikka ja jäljellä olevat laukaukset. Manuaalisen latauksen tulee tasaisen latausajan
  päästä jokaisesta osumastaan, automaattitykin sekunnin murto-osan päästä. Ampujan osumat ryhmitellään
  ajoneuvon, tunnuksen ja purskeen mukaan; ryhmä on aseen, kun ase lataa laukauksen 20 s:n sisällä vähintään
  puolesta sen osumista tasaisella viiveellä. `ammoSlot` on `weapon/slot`, paikka, joka oli ladattu ennen
  osumaa: todennäköisesti se, joka ammuttiin, ellei pelaaja vaihtanut ammusta välissä. Konekiväärit eivät
  lähetä 0xF0BD:tä.
* **Ammus.** Tappoaseen tunnus on ammuksen tunnus (`125mm_3bm46`); ampujan viimeinen osuma uhriin antaa sen
  ampujan paikalle, jossa tykin kaliiperi täsmää. Sen tyyppi ja kaliiperi ovat aseen tiedoston
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Muiden kaliiperi:** paikan aseen; konekivääriryhmän se yksi konekiväärikaliiperi, jonka sen tunnus voi
  olla; muuten ajoneuvon pääaseen. Ilman asennusta (`--game`) ei ole tyyppiä, nimeä tai kaliiperia
  muuta kuin `explosive` / `kinetic`.

Ei löydetty: kimpoaminen. Useat muut viestit kantavat osuman ampujan ja numeron (0xF0C2, todennäköisesti
osuman kameran polku ajoneuvon läpi; 0xF117, 0xF13C, 0xF13E); ne säilytetään sivutiedostossa, eikä niitä
dekoodata. Läpäisemätön osuma pysyy `nonpenetration`-tuloksena.

## Ajoneuvojen palot {#vehicle-fires}

Palava ajoneuvo näkyy jokaiselle asiakkaalle: palvelin lähettää ajoneuvolle kokonaisuusviestin (tapahtuma
`0a519c58`), joka luettelee sillä palavat palot aina, kun luettelo muuttuu. Jokaisesta palosta: kaksi 16-bittistä
tunnusta (toinen vaurio-mallin solmu), sen tyyppi, ja -1, kunnes palo syttyy. Osuman sytyttämälle palolle tulee
myös viesti pisteestä, josta se palaa, ajoneuvon koordinaatistossa (x eteen, y ylös, z vasemmalle).

Rivit: `fire_on`, kun palo ilmestyy luetteloon, `fire_off`, kun se on poissa, ajoneuvolle, kentillä `fireId`
(`first:node`), `fireKind` ja osuman sytyttämille paloille `fireLocalX/Y/Z` (eteen, ylös, oikealle). Kun
ajoneuvo on kuollut, sen luetteloa ei usein lähetetä uudelleen: sen palot päättyvät hylkyyn, muuten sen
kokonaisuuteen, muuten replayn loppuun (`selfCheck.fires`).

Tarkistettu: aina kun säiliön sammuttimien määrä laski, palo poistui sen luettelosta murto-sekunnin sisällä;
useimmat palopisteet ovat samalla puolella ajoneuvoa kuin osuma, joka sen sytytti. Tyypit ovat numeroita;
niiden merkitystä ei tiedetä, eikä sitäkään, mikä osa solmu on. Lentokoneet eivät lähetä tällaista luetteloa:
palava lentokone ei ole luettavissa.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
