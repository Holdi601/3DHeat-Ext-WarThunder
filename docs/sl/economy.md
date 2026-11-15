---
title: Gospodarstvo
nav_order: 14
lang: "sl"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Gospodarstvo {#economy}

Koliko je bitka stala in koliko prinesla, kot stolpci v njenih vrsticah dogodkov, prebrano iz **vaše
namestitve ob pretvorbi** (`char.vromfs.bin`: `config/wpcost.blk` za vsako vozilo, `config/warpoints.blk`
in `config/rank.blk`; blk-ji orožij v `aces.vromfs.bin` povedo, katera modifikacija je vsak strel). Nobena
igrina številka ni v tem repozitoriju: vrednosti gredo samo v vaš lasten izhod. Brez `char.vromfs.bin`
namestitve gospodarstvo ni zapisano (`economy.available` false). Cene so tiste za težavnost bitke
(`repairCostHistorical` za RB, `...Arcade` za AB, `...Simulation` za SB).

| Stolpec | Vrstice | Kaj |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (naboj, vzet po strelu, kopenska vozila), `launch` (letala, helikopterji) | SL, ki ga stane naboj, raketa, izstrelek ali bomba |
| `cost_lost_sl` | `death` vozila igralca | stroški popravila vozila (standardno; v bloku tisto, polno nadgrajeno) |
| `earn_sl`, `earn_rp` | `reward` (nov dogodek, na mestu in ob času prejemnika) | zasluženi SL in RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | vsaka vrstica s `cost_*` ali `earn_sl` | `SL` (`earn_rp` so točke raziskav) |
| `econ_basis` | enako | `install` (cena prebrana iz namestitve) ali `inferred` (izračunana, spodaj) |

**Kdo je zmagal.** `won` (0/1) na vsaki vrstici ekipe, kjer to posnetek pove: rezultati posnetka
odjemalca nosijo lasten izid avtorja (`status`: `success` ali `fail`), zato je avtorjeva ekipa
zmagala ali izgubila, druga ekipa pa obratno; `result` v dokumentu tekme pove, kako je (`winner`,
`status`, `authorTeam`). Strežniški posnetki in posnetki, shranjeni pred koncem, ne nosijo izida
(`status` strežniškega posnetka je vedno `success` in ne imenuje avtorja), obe vrsti pa ne vsebujeta
nameščenih modifikacij: rezultati navajajo vozila vsakega igralca samo po imenu in tipu. Tam `won`
ostane prazen.

Model stroškov v pregledovalniku bere stolpce `cost_*` (in `earn_*`) s `currency`; seštevek
`cost_fired_sl + cost_lost_sl` pove, kje so bili Silver Lions porabljeni in izgubljeni, `earn_sl` pa,
kje so bili zaslužen (nagrada za kill je na svoji vrstici `reward`, ne na vrstici `kill`, zato se nič
ne šteje dvakrat).

- **Streli** (`install`, kjer je znan izstrelek reže – poimenoval ga je kill, glejte
  [Izidi zadetkov](hits.md#hit-outcomes) – sicer `inferred`: povprečna cena izstrelkov, ki jih ta
  top lahko izstreli na tem vozilu; standardni izstrelek je brezplačen; strojnice posnetek ne šteje
  in stanejo nič).
- **Izstrelitve** (`inferred`): igra ceni prednastavitev orožij letala na bojni let, ne na kos; en kos
  je mediana prednastavitev vozila z ceno po ceni / kosih (`sum_weapons`, protiukrepi in odvržene
  rezervoarje izpustimo); 0 tam, kjer so njegove prednastavitve brezplačne.
- **Nagrade** (vse `inferred`): posnetek ne vsebuje zapisa nagrad – rezultati imajo samo točke in
  števila, nobeno sporočilo ne nosi Silver Lions (preverjeno na posnetkih odjemalca in strežnika).
  `kill` zasluži `aKill` x `rewardMul<mode>` morilca x težo razreda žrtve (`units` v warpoints.blk po
  njenem `unitClass`; enote AI po svoji vrsti) x `aiKillK` za žrtev AI x `groundKillMul`, kadar letalo
  ubije kopensko enoto; RP enako z `expMul` in utežmi iz rank.blk. Vsak drug korak točk igralca v
  replicirani lestvici je nagrada, vredna svojih točk po SL na točko bitke (SL kill-a nad mediano točk
  korakov kill-ov, `pointsPerKill` bloka); njegova vrsta je števec, ki je zrasel skupaj z njim
  (pomoči, zajeta območja, poškodbe območij, nagrada za poškodbe, izogibanja raketam), sicer kritičen /
  hud zadetek tega igralca v 3 s, sicer zaznavanje enote igralca v 2 s (`scouting`), sicer `other`.
  `battle_end` je `winK` (zmaga) ali `defeatK` (poraz) zaslužka igralca v bitki, zmagovalec po ostalih
  vstopnicah ekip, nato po njihovem rezultatu. Čas s premijo, ojačevalci, posadka in modifikacije niso
  znani in niso upoštevani; proračuni ubojev v kopenskih bitkah (`def_ground_kill_wp_budget*`) niso
  modelirani.

Element `economy` v dokumentu tekme (in v vsebniku `.3dheat` `extensions["heat3d/economy"]` v manifestu)
vsebuje `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (enako za vsakega igralca, z `netSl`), `vehicles` (za vozilo vsakega igralca:
`repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`,
`expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers`
(`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` in `check` (koliko
vrstic vsake vrste je bilo ocenjenih, ocenjenih ali neocenjenih).

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
