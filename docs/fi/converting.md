---
title: Replayjen muuntaminen
nav_order: 4
lang: fi
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Replayjen muuntaminen {#converting-replays}

Tulos: yksi `.3dheat`-tiedosto taistelua kohden (oletus), tai erilliset
tiedostot valinnalla `--loose`.

## Vaihe vaiheelta {#step-by-step}

1. **Kytke replayt päälle.** War Thunder tallentaa asiakasohjelman replayt pelin
   `Replays`-kansioon, kun replayn tallennus on päällä sen asetuksissa, esimerkiksi
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Palvelimen replayn, joka on tallennettu pelin replay-sivulta (zip-tiedosto, jossa on
   `0000.wrpl`, `0001.wrpl`, ...), voi myös muuntaa.
2. **Avaa pääte** kansioon, johon tulokset saa kirjoittaa
   ([Ennen aloittamista](before-you-start.md)).
3. **Muunna:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # tiedostoja, kansioita tai molempia
   heat3d-wt-replay battle.zip -o out              # palvelimen replayn zip
   heat3d-wt-replay a.wrpl -o out --loose          # erilliset tiedostot yhden .3dheatin sijaan
   ```

   `out` luodaan kansioon, jossa pääte on.
4. **Lue, mitä se sanoo.** Näet yhden rivin taistelua kohden.
5. **Avaa se:** lataa `out/<map>/<match>.3dheat` 3DHeat-katselimeen
   ([Tiedoston lataaminen](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Ajo synteettisellä replaylla: yksi .3dheat, --loose, rikkinäinen tiedosto, tyhjä kansio](../assets/img/convert.svg)

Kuva on ajo replaylla, jonka testit rakentavat koodissa (ei oikeaa replayta,
ei asennusta):

- `ok <file>`: taistelu muunnettu (`--loose`-tilassa: `ok <table> <match document>`);
- `failed <file>: <why>`: tiedostoa ei voitu lukea (poistumiskoodi 1; muut
  muunnetaan silti);
- `no .wrpl files given`: ei muunnettavaa (poistumiskoodi 2);
- `note: ...`: esimerkiksi että War Thunderin asennusta ei löytynyt ajoneuvojen
  nimeämiseksi.

## Valinnat {#options}

| Valinta | Oletus | Tekee |
|---|---|---|
| `replays` (yksi tai useampi) | - | `.wrpl`-tiedostoja, niiden kansioita (kansio itse, ei sen alikansioita) tai niiden zip-arkistoja (palvelimen replay: sen `.wrpl`-osat puretaan väliaikaiseen kansioon) |
| `-o`, `--out` | pakollinen | minne kirjoitetaan: kansio kartaa kohden sen sisällä |
| `--game KANSIO` | löytyy | War Thunderin kansio, jonka tekstit nimeävät ajoneuvot, aseet ja ammukset, ja jonka hinnastot hinnoittelevat [talouden](economy.md); myös `HEAT3D_WT_GAME` |
| `--no-smoothing` | pois | säilytä muiden yksiköiden laskennalliset ja vastaanotetut näytteet sellaisina kuin replay ne antaa ([Laskennallinen liike](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | päällä | pakkaa jokainen taistelu yhteen `.3dheat`-tiedostoon |
| `--loose` | pois | säilytä jokainen taistelu erillisinä tiedostoina (taulukko, ottelun asiakirja, sivutiedostot) |
| `--version` | - | tulosta `heat3d-wt-replay <version>` ja lopeta |
| `-h`, `--help` | - | tulosta valinnat ja lopeta |

Taistelu, joka muunnetaan uudelleen, kirjoitetaan uudelleen. Valinnat sellaisina
kuin ohjelma ne tulostaa: [Komentoviite](../cli-reference.md).

## Mitkä tiedostot ovat yksi taistelu {#which-files-are-one-battle}

Jokainen taistelu tulee yhdeksi tiedostoksi,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB ja SB
ovat pelin lyhenteet arcade-, realistic- ja simulator-taisteluille; `<mode>` on
tehtävän tila pelin avaimen mukaan (`Conq4` Conquest #4, `Dom` Domination, `Bttl` Battle;
katso [Taistelutila](ground.md#battle-mode)); kumpi tahansa osa jää pois, jos replay ei
nimeä sitä. Palvelimen replayn osat (`0000.wrpl`, `0001.wrpl`, ...) luetaan yhdessä
yhtenä taisteluna; asiakasohjelman replay ja saman taistelun palvelimen osat ovat
kaksi tallennetta ja pysyvät kahtena.

## Poistumiskoodi {#exit-status}

`0`, kun jokainen taistelu muunnettiin; `1`, kun jokin epäonnistui (muut
muunnetaan silti); `2`, kun argumenteista ei löytynyt replay-tiedostoa.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
