---
title: Sivutiedostot ja täydellisyys
nav_order: 8
lang: "fi"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sivutiedostot ja täydellisyys {#sidecars-and-completeness}

Replayssa ei heitetä mitään pois. Se, minkä muunnin lukee, menee taulukkoon ja
ottelun asiakirjaan; kaikki muu säilytetään kokonaisena kolmessa sivutiedostossa
taulukon vieressä (`.3dheat`-tiedoston sisällä tai erillisinä valinnalla `--loose`).
Tämä on sääntö, jonka kaikki 3DHeat-muuntimet jakavat:
[Muuntimet säilyttävät kaiken](https://holdi601.github.io/3DHeat/converters.html).

## Sivutiedostot {#the-sidecars}

- `<match>.messages.parquet`: jokainen viesti yksikölle (aika, viestitunnus ja nimi, uid, eid,
  malli, ajoneuvo, sen tunnuskentät heksadesimaalina, `decoded` (siitä luettu, JSON-muodossa),
  hyötykuorma), jokainen replikoitu komponentin arvo (`name` komponentti, `fields` sen arvo),
  jokainen kokonaisuusviesti (kokonaisuutensa ja luokkanumeronsa kanssa), jokainen replikoitu
  kohde (`ReflectionData <kind>/<index>`, sen kentät heksadesimaalina) ja jokainen paketti,
  jota mikään tämän työkalun lukija ei ota, kokonaisena.
- `<match>.objectives.parquet`: valloitusalueet ajan yli, yksi rivi jokaista palvelimen lähettämää
  muutosta kohti: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone`
  (sen kirjain), `zoneId`, `object`, `owner` (0 ei kukaan, 1, 2), `progress` (-100..100, positiivinen
  kohti joukkuetta 2), alueen `x`, `y`, `z` ja kohteen kaikki `fields` heksadesimaalina (katso
  [Tavoitteet](objectives.md)).
- `<match>.flight.parquet`: jokainen lentomallin merkintä jokaisesta lentokoneesta kokonaisena
  (sen bitit ja `phase`: ensimmäisen tavun bitti, josta se alkoi), sen nopeus, 14 ohjausnibbleä
  (`control1-3`, `throttle`), sen moottorit tiloineen, jälkipolttimineen ja kuntoineen, ja sen
  laukaukset aseittain (`ammo`; `numbers` on koko lista). Muiden lentokoneiden arvot ovat viimeksi
  päivitetyt.

## Mitä laskurit takaavat {#what-the-counts-guarantee}

Ottelun asiakirjan `counts` kertoo, mitä replayssa oli ja mitä sille tapahtui:

| Avain | Mitä se on |
|---|---|
| `packets`, `unreadPackets` | jokainen kohdattu pakettityyppi ja ne, joita mikään lukija ei ota (säilytetään kokonaisena viestisivutiedostossa) |
| `messageIds`, `messageIdsNotRead` | jokainen kohdattu viestitunnus ja kuinka usein, sekä ne, joita vain säilytetään eikä lueta |
| `replicatedComponents`, `replicatedNotRead` | luetut komponentin arvot, ja ne, joita vain säilytetään |
| `entities`, `entityTemplates`, `entityMessages` | mitä kokonaisuusvirta loi ja lähetti |
| `droppedSamples` | tarkoituksella jätetyt näytteet (maayksikön hylky sen kokonaisuuden jälkeen), syineen |

Mitään muuta ei jätetä pois: replayn kohde on joko luettu taulukkoon tai ottelun
asiakirjaan, tai säilytetty kokonaisena sivutiedostossa. Ottelun asiakirjan
`selfCheck` sisältää luetun tarkistukset ([Miten replay luetaan](how-it-reads.md)).

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
