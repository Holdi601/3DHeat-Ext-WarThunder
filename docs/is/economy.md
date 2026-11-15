---
title: "Hagkerfi"
nav_order: 14
lang: "is"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Hagkerfi {#economy}

Það sem bardaginn kostaði og gaf af sér, sem dálkar á atburðaröðum hans, lesið úr **þinni uppsetningu við breytingu**
(`char.vromfs.bin`: `config/wpcost.blk` fyrir hvert farartæki, `config/warpoints.blk` og `config/rank.blk`; vopna-blk
í `aces.vromfs.bin` segja hvaða breyting hver skel er). Engin tala leiksins er í þessari geymslu: gildin fara
aðeins í þitt eigið úttak. Án `char.vromfs.bin` uppsetningarinnar er ekkert hagkerfi skrifað
(`economy.available` ósatt). Verðin eru þau sem gilda um erfiðleikastig bardagans (`repairCostHistorical` fyrir RB,
`...Arcade` AB, `...Simulation` SB).

| Dálkur | Raðir | Hvað |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (skot tekið eftir skot, landfarartæki), `launch` (flugvélar, þyrlur) | SL sem skotið, eldflaugin, flugskeytið eða sprengjan kostaði |
| `cost_lost_sl` | `death` farartækis spilara | viðgerðarkostnaður farartækisins (stock; fullbætta farartækið í blokkinni) |
| `earn_sl`, `earn_rp` | `reward` (nýr atburður, á stað og stund þess sem vann sér inn) | SL og RP unnin |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | hver röð með `cost_*` eða `earn_sl` | `SL` (`earn_rp` eru rannsóknarstig) |
| `econ_basis` | sama | `install` (verð lesið úr uppsetningunni) eða `inferred` (reiknað út, hér að neðan) |

**Hver vann.** `won` (0/1) á hverri röð liðs, þar sem upptakan segir til um það: niðurstöður
biðlaraupptöku bera eigin útkomu upptökumannsins (`status`: `success` eða `fail`), svo lið
upptökumannsins vann eða tapaði og hitt liðið öfugt; `result` í leikjaskjalinu
segir hvort (`winner`, `status`, `authorTeam`). Þjónsupptökur og upptökur sem var yfirgefið fyrir
lokin bera enga útkomu (`status` þjónsupptöku er alltaf `success` og nefnir engan upptökumann),
og hvorug tegundin geymir uppsettar breytingar: niðurstöðurnar telja farartæki hvers spilara upp
aðeins eftir nafni og gerð. Þar helst `won` tómt.

Kostnaðarlíkan skoðarans les dálkana `cost_*` (og `earn_*`) með `currency`; summa `cost_fired_sl +
cost_lost_sl` sýnir hvar Silver Lions voru eytt og töpuð, `earn_sl` hvar þau unnust (laun dráps eru
á `reward` röð þess, ekki á `kill` röðinni, svo ekkert telst tvisvar).

- **Skot** (`install` þar sem skel raufarinnar er þekkt - dráp nefndi hana, sjá [Útkoma högga](hits.md#hit-outcomes) -
  annars `inferred`: meðalverð skeljanna sem sú byssa getur skotið á því farartæki; stock skel er ókeypis; vélbyssur
  eru ekki taldar af upptökunni og kosta ekkert).
- **Losanir** (`inferred`): leikurinn verðleggur vopnaforstillingu flugvélar á leiðangur, ekki á hlut; einn hlutur er
  miðgildi verðlagðra forstillinga farartækisins af verð / fjöldi hluta (`sum_weapons`, mótvægisaðgerðir og aukageymar
  undanskilin); 0 þar sem forstillingar þess eru ókeypis.
- **Laun** (öll `inferred`): upptakan geymir enga launafærslu - niðurstöðublokkin hefur aðeins stig og talningar,
  engin skilaboð bera Silver Lions (athugað á biðlara- og þjónsupptökum). `kill` vinnur sér inn `aKill` x `rewardMul<mode>`
  drápsmannsins x vægi flokks fórnarlambsins (`units` í warpoints.blk, eftir `unitClass`; AI-einingar eftir
  tegund) x `aiKillK` fyrir AI-fórnarlamb x `groundKillMul` fyrir flugvél sem drepur landeiningu; RP eins
  með `expMul` og vægi rank.blk. Hvert annað skref í stigum spilara á afrituðu stigatöflunni er laun
  sem eru virði stiga sinna á SL á stig bardagans (SL dráps yfir miðgildi stiga skrefa drápanna, `pointsPerKill`
  blokkarinnar); tegund þess er teljarinn sem hækkaði með því (aðstoðir, handtekin svæði, skaði á svæði,
  skaðaverðlaun, flugskeytum forðað), annars krítískt / alvarlegt högg þess spilara innan 3 s, annars greining á
  einingu spilarans innan 2 s (`scouting`), annars `other`. `battle_end` er `winK` (sigur) eða `defeatK` (tap) af
  tekjum spilarans í bardaganum, sigurvegarinn eftir miðum (tickets) liðanna sem eftir eru, svo stigum þeirra. Premium tími, boosters,
  áhöfn og breytingar eru ekki þekkt og ekki beitt; dráps-kvótar landbardaga
  (`def_ground_kill_wp_budget*`) eru ekki líkaðir.

`economy` í leikjaskjalinu (og, í `.3dheat` gámi, `extensions["heat3d/economy"]` í manifest)
geymir `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (hið sama á spilara, með `netSl`), `vehicles` (á farartæki spilara: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` og `check` (hversu margar raðir af hverri tegund voru
verðlagðar, áætlaðar eða ekki verðlagðar).

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
