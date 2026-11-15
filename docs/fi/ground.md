---
title: Maayksiköt ja kamera
nav_order: 12
lang: fi
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Maayksiköt ja kamera {#ground-units-and-camera}

Tämä sivu on tarkoitettu lukijoille, jotka haluavat tietää, mistä tornien, kameran ja taistelutilan
sarakkeet tulevat ja kuinka paljon niihin voi luottaa. Tarkistukset antavat menetelmän ja
yhteneväisyyden vain.

## Tornit {#turrets}

Säiliön maatila (16-bittinen asento) sisältää sijainnin jälkeen 141 bittiä, joita ei lueta, ja sitten
jokaiselle tornille 62 bittiä: tornin kääntö ja tykin kallistus (16 bittiä kumpikin, 360/65536 astetta
askeleelta, etumerkillinen) ja 30 bittiä, joita ei lueta; sitten täytettä, ja joissain tiloissa 200 bittiä
lisää. Tornien määrä on tila-tavu, joka lähetetään ennen tilaa. Tila, jonka pituus ei sovi, ei anna
torneja (staattiset yksiköt lähettävät lyhyemmän tilan). Kääntö on suhteessa runkoon, myötäpäivään
positiivinen, 0 suoraan edessä; kallistus suhteessa runkoon, ylös positiivinen.

Miten tämä tarkistettiin:

- **Laukauksia vasten:** jokaiselle säiliön osumalle sen pääaseen maailmansuunta (rungon asento käännettynä
  tornin kääntöllä ja tykin kallistuksella) verrattuna ampujan ja osumakohdan väliseen linjaan, vähintään
  30 m päässä: per taistelu mediaani noin 98 % 3 asteen sisällä suunnassa ja 99 % kulmassa
  (`selfCheck.turretsVsShots`). Loput ovat enimmäkseen toisen tornin konekiväärin osumia.
- **Tallentavan pelaajan tähtäystä vasten:** hänen oma säiliönsä lähettää tähtäyksensä maailmakulman
  (vastapäivään idästä), kallistuksen ja etäisyyden. Rungon heading plus tornin kääntö on puolen asteen
  sisällä (mediaani) tähtäyksestä.

**Palvelinreplayt** (0xF074) lähettävät jokaisen säiliön tilan samassa asettelussa, minkä perässä on niiden
omaa dataa, joten jokainen torni, jonka kaksi kulmaa ovat tilan sisällä, luetaan (ainakin pääasetorni
lähes jokaisella säiliörivillä). Kyse on tornista, ei kamerasta:

- **Laukauksia vasten**, kuten yllä: taistelua kohden yli 90 % 3 asteen sisällä suunnassa ja 99 % kulmassa.
- **Näkymää vasten:** palvelinreplay lähettää jokaisen pelaajan tähtäyksen (`viewYaw`, `viewPitch`). Torni
  seuraa näkymää puolen asteen sisällä (mediaani), mutta kääntyy paljon hitaammin kuin näkymä heiluu, kuten
  tornin käyttömoottori tekee (`selfCheck.turretVsView`).
- **Ei aina käyttömoottorin nopeudella:** näyte näytteeltä lähetetty arvo hyppää joskus tähtäykseen, kun
  tähtäys on lähellä tykkiä, nopeammin kuin mikään käyttömoottori kääntyy.

Taulukko sisältää siis tornin **pidettynä sen käyttömoottorissa**: `turretYaw` / `gunPitch` liikkuvat
kohti lähetettyä arvoa enintään pääaseen kääntönopeudella asennuksen ajoneuvotiedostosta (kerrottuna
1,3:lla miehistön taidoille ja muokkauksille; 45 ja 20 astetta sekunnissa, jos asennus ei nimeä mitään).
Jokaisessa pääaseen osumassa torni asetetaan täsmälleen laukauksen linjalle, ja taaksepäin kulkeva
läpikäynti tuo sen ajoissa sinne (`selfCheck.turretLimit`). `shot`-rivi kantaa myös `turretYaw` /
`gunPitch`-arvot. Lähetetty arvo säilyy kohdissa `turretYawRaw` / `gunPitchRaw`. Säiliöllä, jonka tila ei
kanna tornia, on tyhjät tornisarakkeet (katselin voi käyttää `viewYaw`-arvoa varana).
`gunPitch` on hieman `viewPitch`-arvon yläpuolella kantaman päässä: tykin kohoaminen laukauksen pudotusta varten.

Laivojen tilat ovat toisenlaisia; niiden tornit eivät ole luettavissa. Lentokoneet eivät lähetä pään tai
näkymän suuntaa; ilmatorjuntatykkien viesti 0xD020 pysyy lukematta.

## Kamera {#the-camera}

Viesti 0xD043, noin 20 sekunnissa, on tallentavan pelaajan oma replay-kamera: kenttä 1 kvaternio, joka
kääntää kameran eteenpäin siihen, mihin se katsoo; 2 kameran paikka suhteessa seurattavaan ajoneuvoon (m);
4 sama siirtymä ajoneuvon omassa koordinaatistossa (x eteen, y ylös, z vasemmalle); 5 minne pelaaja
tähtää (yksikkövektori); 3 zoom (noin 1,2 säiliön kolmannen persoonan näkymässä, noin 1,0 lentokoneessa,
korkeampi tykkimiehen tähtäimessä tai kiikareilla). Tarkistettu: kenttä 4 on kenttä 2 käännettynä
ajoneuvon koordinaatistoon, 0,5 m:n sisällä lähes jokaisella viestillä; kameran eteenpäin osoittava suunta
on tähtäyksen heading. Replay ei lähetä näkökenttää asteina, vain zoomin.

Taulukossa kamera on oma rata: tyyppi `camera`, rata `<player> camera #ca`, rivi enintään 0,1 s välein,
seurattavan ajoneuvon paikassa plus kenttä 2, katsoen kvaternion suuntaan (`dirX/Y/Z`, `heading`, `pitch`,
`roll`), sekä `zoom`, `aimHeading` ja `aimPitch`, ja `otherLife` on elämä, jota se seuraa. `selfCheck.camera`
laskee rivit ja tarkistuksen.

## Radan loppu {#end-of-a-track}

Rata piirretään ensimmäiseltä riviltään viimeiseen. Kun sen yksikkö on poistunut ennen replayn loppua,
sen viimeinen rivi on `despawn`-rivi viimeisessä paikassaan: silloin kun peli poisti sen kokonaisuuden
(kun se tapahtui 6 s:n sisällä viimeisestä näytteestä), muuten viimeisessä näytteessä. Rata ilman sitä
kestää replayn loppuun. Saman radan rivit voivat olla kaukana toisistaan (kaukainen yksikkö tai hylky
päivittyy muutaman sekunnin välein, hylky joskus vasta minuuttien päästä): sen viimeinen tila pysyy
voimassa, kunnes seuraava rivi tulee.

## Taistelutila {#battle-mode}

Otsikon tavussa 688 on vaikeusaste sen neljässä alimmaisessa bitissä: 0 arcade (AB), 5 realistic (RB),
10 simulator (SB). Tarkistettu replayjen tunnettuja taistelutyyppejä vasten. Pelitila on `ground`, kun
tehtävä sallii säiliöiden ilmestymisen, muuten `naval`, kun se sallii laivat, muuten `air`
(`allowedUnitTypes`); tehtävän oma tila tulee sen avaimesta (`missions/_Dom`), nimettynä asennuksesi
tiedostosta `lang/missions_versus.csv`. Sama avain on tiedostonimien `<mode>`-osa ja ottelun tunnus
(`Conq4`, `Dom`), jätettynä pois, kun otsikossa sitä ei ole.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
