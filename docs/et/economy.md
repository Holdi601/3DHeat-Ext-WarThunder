---
title: Majandus
nav_order: 14
lang: et
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Majandus {#economy}

Mis lahing maksis ja mida tõi, veergudena selle sündmuste ridadel, loetuna **sinu installatsioonist konverteerimise ajal**
(`char.vromfs.bin`: `config/wpcost.blk` iga sõiduki kohta, `config/warpoints.blk` ja `config/rank.blk`; `aces.vromfs.bin`
relvade blk-failid ütlevad, millise modifikatsiooniga iga kest on). Mängu ühtegi numbrit ei ole selles hoidlas: hinnad
lähevad ainult sinu enda väljundisse. Ilma installatsiooni `char.vromfs.bin`-ita majandust ei kirjutata
(`economy.available` false). Hinnad on lahingu raskusastme omad (RB puhul `repairCostHistorical`, AB puhul
`...Arcade`, SB puhul `...Simulation`).

| Veerg | Read | Mis see on |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (laskmise järel võetud kuul, maismaasõidukid), `launch` (lennukid, helikopterid) | SL-is kuuli, raketi, rakett- või pommi maksumus |
| `cost_lost_sl` | `death` mängija sõidukil | sõiduki remondi maksumus (laos; täielikult uuendatud sõiduki oma blokis) |
| `earn_sl`, `earn_rp` | `reward` (uus sündmus, teeniva mängija kohas ja ajal) | teenitud SL ja RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | iga rida, millel on `cost_*` või `earn_sl` | `SL` (`earn_rp` on uurimispunktid) |
| `econ_basis` | sama | `install` (installatsioonist loetud hind) või `inferred` (arvutatud, allpool) |

**Kes võitis.** `won` (0/1) meeskonna iga rea juures, kui kordus seda ütleb: kliendi kordus tulemused
kannavad autori enda tulemust (`status`: `success` või `fail`), seega autori meeskond võitis või kaotas
ja teine meeskond vastupidi; `result` mängu dokumendis ütleb, milline (`winner`, `status`, `authorTeam`).
Serveri kordused ja enne lõppu lahkunud kordused ei kanna tulemust (serveri kordus `status` on alati
`success` ega nimeta autorit), ja kumbki liik ei hoia paigaldatud modifikatsioone: tulemused loetlevad
iga mängija sõidukid ainult nime ja tüübi järgi. Seal jääb `won` tühjaks.

Vaaturi kulumudel loeb veerge `cost_*` (ja `earn_*`) koos `currency`-ga; `cost_fired_sl +
cost_lost_sl` summa annab, kus Silver Lions kulutati ja kaotati, `earn_sl` aga, kus need teeniti
(tapmise tasu on oma `reward` real, mitte `kill` real, nii et midagi ei arvestata kaks korda).

- **Laskemoon** (`install`, kui relva kest on teada - tapmine nimetas selle, vt [Tabamuste tulemused](hits.md#hit-outcomes) -,
  muidu `inferred`: selle relva lastavate kestade keskmine hind sellel sõidukil; standardkest on tasuta;
  kuulipildujaid kordus ei loe ja need ei maksa midagi).
- **Õhkutõusud** (`inferred`): mäng hindab lennuki relvakomplekti lennu kohta, mitte üksuse kohta; üks üksus on
  sõiduki hinnatud komplektide mediaan hind / üksused (`sum_weapons`, vastumeetmed ja kukutatavad paagid
  välja arvatud); 0, kui tema komplektid on tasuta.
- **Tasud** (kõik `inferred`): kordus ei hoia tasu kirjet - tulemuste plokk sisaldab ainult skoori ja arvusid,
  ükski sõnum ei kanna Silver Lionsi (kontrollitud kliendi ja serveri kordustel). `kill` teenib `aKill` x tapja
  `rewardMul<mode>` x ohvri klassi kaal (`units` warpoints.blk-s, tema `unitClass` järgi; AI üksused oma liigi järgi)
  x `aiKillK` AI ohvri puhul x `groundKillMul`, kui lennuk tapab maapealse üksuse; RP sama, `expMul` ja rank.blk
  kaaludega. Iga teine mängija skoori samm replitseeritud tulemustabelis on tasu, mis vaatab oma punkte lahingu
  SL-ides punkti kohta (tapmise SL kaupa tapmiste sammude mediaanpunktid, ploki `pointsPerKill`); tema tüüp on
  loendur, mis selle koos tõusis (abistamised, vallutatud soonad, soonekahju, kahjupreemia, rakettidest
  kõrvalehoidmised), muidu selle mängija kriitiline või raske tabamus 3 s jooksul, muidu tuvastamine
  mängija üksuse poolt 2 s jooksul (`scouting`), muidu `other`. `battle_end` on mängija lahingusisese teenistuse
  `winK` (võit) või `defeatK` (kaotus), võitja otsustatakse meeskondade alles jäänud piletite järgi, siis skoori
  järgi. Preemiaaega, võimendajaid, meeskonda ja modifikatsioone ei teata ega rakendata; maapealsete lahingute
  tapmiseelarveid (`def_ground_kill_wp_budget*`) ei modelleerita.

Mängu dokumendi `economy` (ja `.3dheat` konteineris laadija `extensions["heat3d/economy"]`) sisaldab
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`),
`players` (sama mängija kohta, koos `netSl`-ga), `vehicles` (mängija sõiduki kohta: `repairSl`, `repairFullUpgradedSl`,
`purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`,
`rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`),
`winnerTeam`, `pointsPerKill` ja `check` (kui palju iga liigi ridu hinnati, hinnati hinnanguliselt või ei hinnatud).

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
