---
title: Tavoitteet
nav_order: 15
lang: fi
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Tavoitteet {#objectives}

`objectives` ottelun asiakirjassa luettelee ne, joista taistelu käydään, kahdesta lähteestä (`source`):

- **Replay** (`replay`): tehtäväkohteet, jotka 0xD039 nimeää (valloitusalueet `cz_circle_NN`, lentokentät, helikopterikentät,
  tukikohdat), sijoitettuina sinne, minne lajin 3 (0xF02D) replikoidut kohteet asettavat ne nyt: valloitusalue alkaa
  mallinsa paikasta ja siirretään tämän tilan alueelle alussa (`moved`). Lajin 3 numerot seuraavat 0xD039:n järjestystä;
  jokainen siirtämätön kohde on täsmälleen siellä, missä 0xD039 sen pitää, mikä tarkistaa järjestyksen. Valloitusalue
  saa muodon ja säteen alueesta sen paikalla (`area`, 2 m:n sisällä) ja kirjaimensa omasta indeksistään (lajin 5 kenttä 69:
  0 = A); kirjainjärjestys on replayn, eikä sitä ole tarkistettu pelin kartasta.
- **Tehtävä** (`mission`): tehtävätiedosto `<mission>.blk` asennuksesi `mis.vromfs.bin`-tiedostossa ja sen tuomat mallit
  (vain luku, muunnoksen aikana): sen alueet, nimen mukaan luokiteltuina: lähtöalueet (lähtöalueen numeroidut pisteet
  `..._spawnareaNN` yhtenä `points`-lähtöalueena), taistelualueet, pommituskohteet (`bomb_zone`), saattueen lähtöpisteet
  (`road_NN_spawn`), poistumis- ja tappoalueet. Saman kartan muiden tilojen alueet (`conq_`, `dom_`, `bttl_`, ...) jätetään
  pois, ja `_arcade` / `_realistic` / `_hardcore`-muunnelmista otetaan taistelun oma (RB ottaa `_realistic`, muuten
  `_hardcore`, kuten tehtävän käsikirjoitukset tekevät); myös briefing-merkit, ilmatorjuntatykkien pisteet ja yli 5 km:n
  leveät alueet (joiden yli lähtöalueet on hajautettu) jätetään pois. Jokainen lähtöalue kertoo, kuinka monen pelaajan
  radat alkoivat siellä (`used`, `usedByTeam`). Tehtävä voi vaihtaa puolia satunnaisesti (`randomSpawnTeams`): kun lähtöalueet
  näyttävät replayn joukkueet toisinpäin, jokainen `team` vaihdetaan ja nimen puoli säilytetään kohdassa `missionTeam`.
  Saattuereittejä ei ole tehtävän lukemissa välipisteissä; vain se, missä saattueita ilmestyy, annetaan.

Valloitusalueet ajan yli ovat sivutiedosto `<match>.objectives.parquet`: lajin 5 replikoidut kohteet, yksi per alue:
kenttä 2 sen omistaja (0, 1, 2), kenttä 67 sen valloituksen edistyminen, etumerkillinen tavu -100:sta 100:aan (positiivinen
kohti joukkuetta 2), kenttä 69 sen indeksi. Tarkistettu (`selfCheck.objectives`) maapalvelinreplayistä, joissa on
Conquest- ja Domination-taisteluja: jokainen omistajan vaihto tulee samalla hetkellä (1,5 s:n sisällä) pelaajan kanssa, joka
valloittavan joukkueen pelaaja saa `captureZone`-pisteen tulostaulussa, ja elossa olevan maayksikön kanssa, joka on tuon
joukkueen ja alueen sisällä; jokaisen taistelun lähtöalueet näyttävät replayn joukkueet vain yhdellä tavalla (usein
vaihdettuna tehtävän `t1_` / `t2_` suhteen).

## Kohtauksen yksiköt: raitiovaunut ja junanvaunut {#scene-units-trams-and-rail-wagons}

Kenttä voi sijoittaa omia yksiköitään: palvelinreplayn `unit_loader+rail_wagon`-kokonaisuudet ovat kentän kohtaustiedoston
raitiovaunuja (`gamedata/scenes/<level>_objects.blk` tiedostossa `aces.vromfs.bin`: `setting__unit_class`, sen muunnos ja
`setting__isDead`). Niiden kokonaisuuksissa ei ole luettavaa tunnusta, joten maarata ilman yksikköä, jonka ensimmäinen
näyte on 2 m:n sisällä kohtausyksiköstä, on tuo yksikkö: sen luokka `Vehicle`-kenttänä, tyyppi `train`, tyyppi `tram`,
`locomotive` tai `wagon`, ei joukkuetta; yksikkö, jonka kohtaus sijoittaa kuolleena (kuten palaneet raitiovaunut), on hylky
(`alive` 0) ensimmäisestä rivistä alkaen. Peli ei anna niille englanninkielistä nimeä; `VehicleName` on tunnus luettuna sanoina
("Railway tram A"). Niiden sijainnit eivät heilu: lähes kaikki eivät liiku koskaan (jokainen näyte on sama bitti
bitiltä). Replay lähettää niitä noin kymmenen kertaa sekunnissa riippumatta siitä, joten näytteistä säilytetään vain ne, jotka
liikuttavat niitä (0,05 m tai 0,1 astetta), ja yksi 10 sekunnin välein (`selfCheck.sceneUnits` laskee pudotetut näytteet).
Aiemmin ne olivat ratoja nimeltä `uid 8` ilman ajoneuvoa.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
