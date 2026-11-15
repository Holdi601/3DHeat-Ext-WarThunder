---
title: Talous
nav_order: 14
lang: fi
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Talous {#economy}

Mitä taistelu maksoi ja tuotti, sarakkeina sen tapahtumariveillä, luettuna **asennuksestasi muunnoksen aikana**
(`char.vromfs.bin`: `config/wpcost.blk` ajoneuvoittain, `config/warpoints.blk` ja `config/rank.blk`; aseiden blk-tiedostot
`aces.vromfs.bin`-tiedostossa kertovat, mikä muokkaus kukin ammus on). Pelin yhtään lukua ei ole tässä tietovarastossa:
arvot menevät vain sinun omaan tulostukseesi. Ilman asennuksen `char.vromfs.bin`-tiedostoa talousdataa ei kirjoiteta
(`economy.available` epätosi). Hinnat ovat taistelun vaikeusasteen mukaiset (`repairCostHistorical` RB:lle,
`...Arcade` AB:lle, `...Simulation` SB:lle).

| Sarake | Rivit | Mitä se on |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (maayksikön laukaus, joka otetaan ammuksen jälkeen), `launch` (lentokoneet, helikopterit) | SL-hinta kierrokselle, raketille, ohjukselle tai pommille |
| `cost_lost_sl` | `death` pelaajan ajoneuvolle | ajoneuvon korjauskustannus (perusversio; täysin päivitetty blk:ssa) |
| `earn_sl`, `earn_rp` | `reward` (uusi tapahtuma, ansaitsijan paikassa ja ajassa) | ansaitut SL ja RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | jokainen rivi, jolla on `cost_*` tai `earn_sl` | `SL` (`earn_rp` ovat tutkimuspisteitä) |
| `econ_basis` | sama | `install` (asennuksesta luettu hinta) tai `inferred` (laskettu, alla) |

**Kuka voitti.** `won` (0/1) jokaisella joukkueen rivillä, kun replay sen kertoo: asiakasreplayn tuloksissa on
tekijän oma lopputulos (`status`: `success` tai `fail`), joten tekijän joukkue voitti tai hävisi ja toinen
joukkue päinvastoin; ottelun asiakirjan `result` kertoo, mikä (`winner`, `status`, `authorTeam`). Palvelinreplayt
ja replayt, jotka päättyvät ennen loppua, eivät kanna lopputulosta (palvelinreplayn `status` on aina `success` eikä
nimeä tekijää), eikä kummassakaan ole asennettuja muokkauksia: tulokset luettelevat jokaisen pelaajan ajoneuvot
vain nimellä ja tyypillä. Siellä `won` jää tyhjäksi.

Kustannusmallin lukee katselin sarakkeista `cost_*` (ja `earn_*`) `currency`-sarakkeen kanssa; `cost_fired_sl +
cost_lost_sl`-summa kertoo, missä Silver Lionsit kuluivat ja menetettiin, `earn_sl` missä ne ansaittiin (tappopalkkio
on sen `reward`-rivillä, ei `kill`-rivillä, joten mikään ei lasketa kahdesti).

- **Kierrokset** (`install`, kun lokeron ammus tunnetaan: tappo nimesi sen, katso [Osuman lopputulokset](hits.md#hit-outcomes);
  muuten `inferred`: sen aseen ammusten keskihinta, jonka kyseinen ajoneuvo voi ampua; vakioammus on ilmainen;
  konekiväärejä replay ei laske eivätkä ne maksa mitään).
- **Laukaisut** (`inferred`): peli hinnoittelee lentokoneen aseasetuksen lentoa kohden, ei kohdetta kohden; yksi kohde
  on hinnoiteltujen asetusten mediaani (hinta / kohteet, `sum_weapons`, vastatoimet ja pudotussäiliöt pois); 0, jos sen
  asetukset ovat ilmaisia.
- **Palkinnot** (kaikki `inferred`): replayssa ei ole palkintotietuetta: tulosten lohkossa on vain pisteet ja laskurit,
  mikään viesti ei kanna Silver Lionseja (tarkistettu asiakas- ja palvelinreplayistä). `kill` ansaitsee `aKill` x tappajan
  `rewardMul<mode>` x uhrin luokan paino (`units` warpoints.blk:ssa, sen `unitClass`-arvon mukaan; tekoälyyksiköt lajinsa
  mukaan) x `aiKillK` tekoälyuhrille x `groundKillMul`, kun lentokone tappaa maayksikön; RP samoin `expMul`:lla ja
  rank.blk:n painoilla. Jokainen muu askel pelaajan pisteissä replikoidussa tulostaulussa on palkinto, joka on arvoltaan
  pisteensä taistelun SL-per-piste-arvolla (tapon SL tapon askelten pisteiden mediaanin yli, lohkon `pointsPerKill`);
  sen tyyppi on laskuri, joka kasvoi sen mukana (avustukset, valloitetut alueet, alueen vahinko, vahinkopalkkio, ohjusten
  väistöt), muuten pelaajan kriittinen tai vakava osuma 3 s:n sisällä, muuten pelaajan yksikön havainto 2 s:n sisällä
  (`scouting`), muuten `other`. `battle_end` on `winK` (voitto) tai `defeatK` (tappio) pelaajan taistelun aikaisista
  ansioista, voittaja joukkueiden jäljellä olevien lippujen mukaan, sitten pistemäärä. Premium-aika, tehostajat, miehistö
  ja muokkaukset eivät ole tiedossa eikä niitä sovelleta; maataistelujen tappobudjetit (`def_ground_kill_wp_budget*`)
  eivät ole mallinnettuja.

Ottelun asiakirjan `economy` (ja `.3dheat`-säiliössä manifestin `extensions["heat3d/economy"]`) sisältää
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`),
`players` (samat pelaajittain, `netSl`:n kanssa), `vehicles` (pelaajan ajoneuvoa kohden: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`,
`battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`,
`wpMultiplier`), `winnerTeam`, `pointsPerKill` ja `check` (kuinka monta riviä kutakin tyyppiä hinnoiteltiin, arvioitiin
tai jäi hinnoittelematta).

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
