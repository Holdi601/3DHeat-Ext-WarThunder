---
title: "Ekonomija"
nav_order: 14
lang: "mt"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomija {#economy}

X'kellfet u x'qalgħet il-battalja, bħala kolonni fuq ir-ringieli tal-avvenimenti tagħha, moqrija mill-**installazzjoni tiegħek fil-ħin tal-konverżjoni**
(`char.vromfs.bin`: `config/wpcost.blk` għal kull vettura, `config/warpoints.blk` u `config/rank.blk`; il-blks tal-armi
ta' `aces.vromfs.bin` jgħidu liema modifika hija kull qoxra). Ebda numru tal-logħba m'huwa f'dan ir-repożitorju: il-
valuri jmorru fil-ħruġ tiegħek biss. Mingħajr `char.vromfs.bin` tal-installazzjoni ma tinkiteb ebda ekonomija
(`economy.available` falz). Il-prezzijiet huma dawk tad-difficulty tal-battalja (`repairCostHistorical` għal RB,
`...Arcade` AB, `...Simulation` SB).

| Kolonna | Ringieli | X'inhi |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (rawnd meħud wara sparatura, vetturi tal-art), `launch` (ajruplani, helikopters) | SL li kellef ir-rawnd, ir-rokit, il-missila jew il-bomba |
| `cost_lost_sl` | `death` ta' vettura ta' plejer | l-ispiża tat-tiswija tal-vettura (stock; dik imtejba għall-aħħar fil-blokk) |
| `earn_sl`, `earn_rp` | `reward` (avveniment ġdid, fil-post u l-ħin ta' min qalgħu) | SL u RP imqalgħa |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | kull ringiela b'`cost_*` jew `earn_sl` | `SL` (`earn_rp` huma punti tar-riċerka) |
| `econ_basis` | l-istess | `install` (prezz moqri mill-installazzjoni) jew `inferred` (ikkalkulat, hawn taħt) |

**Min rebaħ.** `won` (0/1) fuq kull ringiela ta' tim, fejn tgħid ir-ripetizzjoni: ir-riżultati ta' ripetizzjoni
tal-klijent iġorru r-riżultat proprju tal-awtur (`status`: `success` jew `fail`), għalhekk it-tim tal-awtur rebaħ
jew tilef u t-tim l-ieħor l-oppost; `result` fid-dokument tal-partita jgħid liema (`winner`, `status`, `authorTeam`).
Ripetizzjonijiet tas-server u ripetizzjonijiet li ħarġu minnhom qabel it-tmiem ma jġorru ebda riżultat (l-`status` ta'
ripetizzjoni tas-server huwa dejjem `success` u ma jsemmi ebda awtur), u l-ebda waħda miż-żewġ tipi ma żżomm modifiki installati: ir-riżultati
jelenkaw il-vetturi ta' kull plejer bl-isem u bit-tip biss. Hemmhekk `won` jibqa' vojt.

Il-mudell tal-ispiża tal-viewer jaqra l-kolonni `cost_*` (u `earn_*`) b'`currency`; billi tgħodd `cost_fired_sl +
cost_lost_sl` ikollok fejn intefqu u tilfu Silver Lions, `earn_sl` fejn inqalgħu (ir-premju ta' qtil jinsab fuq
ir-ringiela `reward` tiegħu, mhux fuq ir-ringiela `kill`, biex xejn ma jingħadd darbtejn).

- **Rawnds** (`install` fejn il-qoxra tas-slot hija magħrufa - qtil semmiha, ara [Hit outcomes](hits.md#hit-outcomes) -
  inkella `inferred`: il-prezz medju tal-qxur li dak il-kanun jista' jispara fuq dik il-vettura; qoxra stock hija b'xejn; magna guns
  ma jingħaddux mir-ripetizzjoni u ma jiswew xejn).
- **Launches** (`inferred`): il-logħba tipprezza preset tal-armi ta' ajruplan għal kull sortie, mhux għal kull oġġett; oġġett
  wieħed huwa l-medjan fuq il-presets ipprezzati tal-vettura tal-prezz / oġġetti (`sum_weapons`, countermeasures u drop tanks
  imħallija barra); 0 fejn il-presets tagħha huma b'xejn.
- **Premjijiet** (kollha `inferred`): ir-ripetizzjoni ma żżomm ebda record ta' premju - il-blokk tar-riżultati għandu biss punti u għadd,
  ebda messaġġ ma jġorr Silver Lions (ikkontrollat fuq ripetizzjonijiet tal-klijent u tas-server). `kill` jaqla' `aKill` x
  `rewardMul<mode>` tal-qattiel x il-piż tal-klassi tal-vittma (`units` f'warpoints.blk, mill-`unitClass` tagħha; unitajiet AI skont it-tip
  tagħhom) x `aiKillK` għal vittma AI x `groundKillMul` għal ajruplan li joqtol unità tal-art; RP l-istess b'`expMul` u l-piżijiet
  ta' rank.blk. Kull pass ieħor tal-punti ta' plejer fl-scoreboard replikat huwa premju li jiswa l-punti tiegħu bl-SL tal-battalja
  għal kull punt (l-SL ta' qtil fuq il-medjan tal-punti tal-passi tal-qtil, il-`pointsPerKill` tal-blokk); it-tip tiegħu huwa l-kontatur
  li tela' miegħu (assists, żoni maqbuda, ħsara taż-żona, premju tal-ħsara, missili evaded), inkella daqqa kritika / severa ta' dak il-plejer
  fi ħdan 3 s, inkella detezzjoni tal-unità tal-plejer fi ħdan 2 s (`scouting`), inkella `other`. `battle_end` huwa `winK` (rebaħ) jew
  `defeatK` (tilef) tal-qligħ fil-battalja tal-plejer, ir-rebbieħ skont it-tickets li fadal tat-timijiet, imbagħad il-punti tagħhom.
  Ħin premium, boosters, ekwipaġġ u modifiki mhumiex magħrufa u mhumiex applikati; il-baġits tal-qtil tal-battaljiet tal-art
  (`def_ground_kill_wp_budget*`) mhumiex immudellati.

L-`economy` tad-dokument tal-partita (u, f'kontenitur `.3dheat`, l-`extensions["heat3d/economy"]` tal-manifest)
iżomm `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (l-istess għal kull plejer, b'`netSl`), `vehicles` (għal kull vettura ta' plejer: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` u `check` (kemm ringieli ta' kull tip ġew
ipprezzati, stmati jew mhux ipprezzati).

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
