---
title: "Ekonomia"
nav_order: 14
lang: sq
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomia {#economy}

Sa kushtoi dhe sa fitoi beteja, si kolona në rreshtat e ngjarjeve të saj, të lexuara nga **instalimi yt në kohën e konvertimit**
(`char.vromfs.bin`: `config/wpcost.blk` për mjet, `config/warpoints.blk` dhe `config/rank.blk`; blk-të e armëve
të `aces.vromfs.bin` thonë cila modifikim është çdo predhë). Asnjë numër i lojës nuk është në këtë depo: vlerat
shkojnë vetëm në daljen tënde. Pa `char.vromfs.bin` të instalimit nuk shkruhet ekonomi
(`economy.available` false). Çmimet janë ato të vështirësisë së betejës (`repairCostHistorical` për RB,
`...Arcade` AB, `...Simulation` SB).

| Kolona | Rreshtat | Çfarë |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (një predhë e marrë pas një të shtëne, mjete tokësore), `launch` (aeroplanë, helikopterë) | SL që kushtoi predha, rakata, raketa ose bomba |
| `cost_lost_sl` | `death` i mjetit të një lojtari | kostoja e riparimit të mjetit (stock; ai i përmirësuar plotësisht në bllok) |
| `earn_sl`, `earn_rp` | `reward` (ngjarje e re, në vendin dhe kohën e fituesit) | SL dhe RP të fituara |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | çdo rresht me `cost_*` ose `earn_sl` | `SL` (`earn_rp` janë pikë kërkimi) |
| `econ_basis` | e njëjta | `install` (një çmim i lexuar nga instalimi) ose `inferred` (i llogaritur, më poshtë) |

**Kush fitoi.** `won` (0/1) në çdo rresht të një skuadre, aty ku e thotë riluajtja: rezultatet e një
riluajtjeje klienti mbajnë rezultatin e vetë autorit (`status`: `success` ose `fail`), kështu që skuadra e
autorit fitoi ose humbi dhe skuadra tjetër e kundërta; `result` në dokumentin e ndeshjes
thotë cila (`winner`, `status`, `authorTeam`). Riluajtjet e serverit dhe riluajtjet e lëna para
fundit nuk mbajnë rezultat (`status` i një riluajtjeje serveri është gjithmonë `success` dhe nuk emërton autor),
dhe asnjëra nuk mban modifikime të instaluara: rezultatet listojnë mjetet e çdo lojtari vetëm
me emër dhe lloj. Aty `won` mbetet bosh.

Modeli i kostos i shikuesit lexon kolonat `cost_*` (dhe `earn_*`) me `currency`; mbledhja e `cost_fired_sl +
cost_lost_sl` jep ku u shpenzuan dhe u humbën Silver Lions, `earn_sl` ku u fituan (shpërblimi i një vrasjeje është
te rreshti i tij `reward`, jo te rreshti `kill`, kështu që asgjë nuk numërohet dy herë).

- **Predhat** (`install` aty ku predha e vendit dihet - një vrasje e emërtoi, shih [Rezultatet e goditjeve](hits.md#hit-outcomes) -
  përndryshe `inferred`: çmimi mesatar i predhave që ai top mund të gjuajë në atë mjet; një predhë stock është falas; automatikët
  nuk numërohen nga riluajtja dhe nuk kushtojnë asgjë).
- **Lëshimet** (`inferred`): loja ia vendos çmimin presetit të armëve të një aeroplani për mision, jo për copë; një copë është
  mediana mbi presetet e çmuara të mjetit e çmimit / copë (`sum_weapons`, kundërmasat dhe depozitat e hedhshme lihen
  jashtë); 0 aty ku presetet e tij janë falas.
- **Shpërblimet** (të gjitha `inferred`): riluajtja nuk mban regjistër shpërblimi - blloku i rezultateve ka vetëm pikë dhe numra,
  asnjë mesazh nuk mban Silver Lions (kontrolluar në riluajtje klienti dhe serveri). Një `kill` fiton `aKill` x
  `rewardMul<mode>` i vrasësit x pesha e klasës së viktimës (`units` në warpoints.blk, sipas `unitClass` të saj; njësitë AI sipas llojit të tyre) x `aiKillK` për një viktimë AI x `groundKillMul` për një aeroplan që vret një njësi tokësore; RP e njëjtë me
  `expMul` dhe peshat e rank.blk. Çdo hap tjetër i pikëve të një lojtari në tabelën e replikuar të rezultateve është një shpërblim
  me vlerë pikët e tij me SL-në e betejës për pikë (SL e një vrasjeje mbi medianën e pikëve të hapave të vrasjeve, `pointsPerKill` i bllokut); lloji i tij është numëruesi që u ngrit me të (ndihma, zona të kapura, dëm zone,
  çmim dëmi, shmangie raketash), përndryshe goditja kritike / e rëndë e atij lojtari brenda 3 s, përndryshe një zbulim i
  njësisë së lojtarit brenda 2 s (`scouting`), përndryshe `other`. `battle_end` është `winK` (fitim) ose `defeatK` (humbje) e
  fitimeve të lojtarit gjatë betejës, fituesi sipas biletave të mbetura të skuadrave, pastaj pikëve të tyre. Koha premium, boosterët,
  ekuipazhi dhe modifikimet nuk dihen dhe nuk zbatohen; buxhetet e vrasjeve të betejave tokësore
  (`def_ground_kill_wp_budget*`) nuk modelohen.

`economy` i dokumentit të ndeshjes (dhe, në një kontejner `.3dheat`, `extensions["heat3d/economy"]` i manifestit)
mban `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (e njëjta për lojtar, me `netSl`), `vehicles` (për mjet lojtari: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` dhe `check` (sa rreshta të çdo lloji u
çmuan, u vlerësuan ose nuk u çmuan).

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
