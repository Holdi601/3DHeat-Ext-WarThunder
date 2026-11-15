---
title: Ekonomika
nav_order: 14
lang: lt
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomika {#economy}

Ką mūšis kainavo ir ką uždirbo - stulpeliai jo įvykių eilutėse, nuskaityti iš **jūsų diegimo konvertavimo metu**
(`char.vromfs.bin`: `config/wpcost.blk` kiekvienai technikai, `config/warpoints.blk` ir `config/rank.blk`; ginklų
blk failai `aces.vromfs.bin` nurodo, kuri modifikacija yra kiekvienas sviedinys). Žaidimo skaičių šioje saugykloje
nėra: reikšmės patenka tik į jūsų paties išvestį. Be `char.vromfs.bin` iš diegimo ekonomika neįrašoma
(`economy.available` yra false). Kainos yra tos, kurias nustato mūšio sunkumas (RB - `repairCostHistorical`,
AB - `...Arcade`, SB - `...Simulation`).

| Stulpelis | Eilutės | Ką reiškia |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (sviedinys, paimtas po šūvio, sausumos technikai), `launch` (orlaiviai, sraigtasparniai) | SL kaina už sviedinį, raketą, raketą su valdymu ar bombą |
| `cost_lost_sl` | `death` žaidėjo technikos | technikos remonto kaina (standartinė; pilnai patobulinta - iš bloko) |
| `earn_sl`, `earn_rp` | `reward` (nauji įvykiai, uždirbėjo vietoje ir laiku) | uždirbti SL ir RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | kiekviena eilutė su `cost_*` arba `earn_sl` | `SL` (`earn_rp` yra tyrimų taškai) |
| `econ_basis` | tas pats | `install` (kaina nuskaityta iš diegimo) arba `inferred` (apskaičiuota, žemiau) |

**Kas laimėjo.** `won` (0/1) kiekvienoje komandos eilutėje, kai įraše tai nurodyta: kliento įrašo
rezultatuose yra autoriaus paties baigtis (`status`: `success` arba `fail`), todėl autoriaus komanda
laimėjo arba pralaimėjo, o kita komanda - atvirkščiai; rungtynių dokumente `result` nurodo, kas tai
(`winner`, `status`, `authorTeam`). Serverio įrašuose ir įrašuose, išsaugotuose prieš pabaigą, baigties
nėra (serverio įrašo `status` visada `success` ir autoriaus nenurodo), ir nei vienas, nei kitas nerodo
įdiegtų modifikacijų: rezultatuose kiekvieno žaidėjo technika nurodoma tik pagal vardą ir tipą. Ten
`won` lieka tuščias.

Žiūryklės kainų modelis skaito stulpelius `cost_*` (ir `earn_*`) su `currency`; sudėjus `cost_fired_sl +
cost_lost_sl` gaunama, kur Sidabro liūtai buvo išleisti ir prarasti, `earn_sl` - kur jie buvo uždirbti
(žudymo atlygis yra jo `reward` eilutėje, o ne `kill` eilutėje, todėl niekas neskaičiuojama dukart).

- **Šaudmenys** (`install`, kai žinoma to lizdo sviedinio kaina - žudymas jį pavadino, žr.
  [Pataikymo rezultatai](hits.md#hit-outcomes) - kitu atveju `inferred`: tos patrankos galimų sviedinių
  vidutinė kaina toje technikoje; standartinis sviedinys nemokamas; kulkosvaidžių įrašas nesuskaičiuojamas
  ir jie nieko nekainuoja).
- **Paleidimai** (`inferred`): žaidimas orlaivio ginklų rinkinį kainuoja vienam skrydžiui, o ne už vieną
  vienetą; vienas vienetas yra mediana iš technikos kainuojamų rinkinių kainos / vienetų skaičiaus
  (`sum_weapons`, priešpriemonės ir papildomi bakai neįskaičiuojami); 0, kai jos rinkiniai nemokami.
- **Atlygiai** (visi `inferred`): įraše nėra atlygio įrašo - rezultatų blokas turi tik taškus ir
  skaičius, jokia žinutė neneša Sidabro liūtų (patikrinta kliento ir serverio įrašuose). `kill` uždirba
  `aKill` x žudiko `rewardMul<mode>` x aukos klasės svoris (`units` warpoints.blk, pagal jos `unitClass`;
  DI vienetai pagal rūšį) x `aiKillK` DI aukai x `groundKillMul`, kai orlaivis naikina sausumos vienetą;
  RP - tas pats su `expMul` ir rank.blk svoriais. Kiekvienas kitas žaidėjo rezultato žingsnis
  replikuotoje suvestinėje yra atlygis, lygus jo taškams mūšio SL už tašką (kill SL virš žudymo žingsnių
  medianos taškų, `pointsPerKill` bloke); jo tipas yra skaitiklis, kuris padidėjo kartu (assists, užimtos
  zonos, zonos žala, žalos apdovanojimas, vengimas raketoms), kitu atveju žaidėjo kritinis / sunkus
  pataikymas per 3 s, kitu atveju žaidėjo vieneto aptikimas per 2 s (`scouting`), kitu atveju `other`.
  `battle_end` yra `winK` (laimėta) arba `defeatK` (pralaimėta) žaidėjo mūšio uždarbio, laimėtoją
  nustatant pagal likusius komandų bilietus, tada pagal jų rezultatą. Premium laikas, stiprinimai, įgula ir
  modifikacijos nežinomi ir netaikomi; sausumos mūšių žudymo biudžetai (`def_ground_kill_wp_budget*`)
  nemodeliuojami.

Rungtynių dokumento `economy` (o `.3dheat` konteineryje - manifesto `extensions["heat3d/economy"]`)
laiko `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (tas pats kiekvienam žaidėjui, su `netSl`), `vehicles` (kiekvienos žaidėjo technikos:
`repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` ir `check` (kiek kiekvienos rūšies eilučių
buvo įkainuota, įvertinta ar neįkainuota).

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
