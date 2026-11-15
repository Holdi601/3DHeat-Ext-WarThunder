---
title: "Ekonomika"
nav_order: 14
lang: cs
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomika {#economy}

Kolik bitva stála a co vynesla, jako sloupce na jejích řádcích událostí. Čte se z **vaší instalace v době převodu**
(`char.vromfs.bin`: `config/wpcost.blk` pro každé vozidlo, `config/warpoints.blk` a `config/rank.blk`; bloky zbraní
v `aces.vromfs.bin` říkají, jaká úprava patří ke každé střele). Žádné číslo hry není v tomto repozitáři: hodnoty
jdou jen do vašeho vlastního výstupu. Bez `char.vromfs.bin` z instalace se ekonomika nezapíše
(`economy.available` false). Ceny jsou ceny obtížnosti bitvy (`repairCostHistorical` pro RB,
`...Arcade` pro AB, `...Simulation` pro SB).

| Sloupec | Řádky | Co je v něm |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (náboj doplněný po výstřelu, pozemní vozidla), `launch` (letadla, vrtulníky) | SL, které stála náboj, raketa, střela nebo bomba |
| `cost_lost_sl` | `death` vozidla hráče | cena opravy vozidla (základní; u plně vylepšeného vozidla z bloku) |
| `earn_sl`, `earn_rp` | `reward` (nová událost, na místě a v čase toho, kdo získal) | získané SL a RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | každý řádek s `cost_*` nebo `earn_sl` | `SL` (`earn_rp` jsou výzkumné body) |
| `econ_basis` | totéž | `install` (cena načtená z instalace) nebo `inferred` (odvozená, níže) |

**Kdo vyhrál.** `won` (0/1) na každém řádku týmu, pokud to replay uvádí. Výsledky replaye klienta nesou
vlastní výsledek autora (`status`: `success` nebo `fail`), takže tým autora vyhrál nebo prohrál a
druhý tým naopak; to, který je který, říká `result` v dokumentu zápasu
(`winner`, `status`, `authorTeam`). Serverové replaye a replaye, které skončily dříve než bitva, žádný
výsledek nemají (`status` serverového replaye je vždy `success` a neuvádí autora),
a ani jedny nemají nainstalované úpravy: výsledky vypisují vozidla každého hráče jen
názvem a typem. U nich `won` zůstává prázdné.

Model nákladů prohlížeče čte sloupce `cost_*` (a `earn_*`) spolu s `currency`; součet `cost_fired_sl +
cost_lost_sl` dává, kde se Stříbrné lvy utratily a ztratily, `earn_sl` kde se získaly (odměna za zabití je
na svém řádku `reward`, ne na řádku `kill`, takže se nic nepočítá dvakrát).

- **Náboje** (`install`, kde je známa střela daného slotu - zabití ji pojmenovalo, viz [Výsledky zásahů](hits.md#hit-outcomes) -
  jinak `inferred`: průměrná cena střel, které ten kanón na tom vozidle může vystřelit; základní střela je zdarma;
  kulomety replay nepočítá a nic nestojí).
- **Vypuštění** (`inferred`): hra oceňuje výzbroj letadla za výlet, ne za kus; jeden kus je medián přes oceněné
  sestavy vozidla podle ceny / počtu kusů (`sum_weapons`, protiopatření a odhozené nádrže
  vynechány); 0 tam, kde jsou jeho sestavy zdarma.
- **Odměny** (všechny `inferred`): replay žádný záznam odměny neobsahuje - blok výsledků nese jen body a počty,
  žádná zpráva nenese Stříbrné lvy (ověřeno na replayích klienta i serveru). `kill` získá `aKill` x `rewardMul<mode>`
  zabijejícího x váhu třídy oběti (`units` v warpoints.blk, podle jejího `unitClass`; jednotky AI podle druhu) x
  `aiKillK` u oběti AI x `groundKillMul`, když letadlo zabije pozemní jednotku; RP totéž s `expMul` a váhami
  z rank.blk. Každý další krok skóre hráče v replikovaném žebříčku je odměna, která vyjde na své body v SL za bod
  bitvy (SL zabití přes median bodů kroků zabití, `pointsPerKill` bloku); jeho typ je čítač, který s ním vzrostl
  (asistence, zajaté zóny, poškození zón, odměna za poškození, uniknuté střely), jinak kritický nebo vážný zásah
  hráče do 3 s, jinak zjištění jednotky hráče do 2 s (`scouting`), jinak `other`. `battle_end` je `winK` (výhra) nebo
  `defeatK` (prohra) z vydělaného hráčem v bitvě, vítěz podle zbylých bodů týmů, potom podle skóre. Prémiový čas,
  posilovače, posádka a úpravy se neznají a nepočítají se; rozpočty zabití v pozemních bitvách
  (`def_ground_kill_wp_budget*`) se nemodelují.

`economy` v dokumentu zápasu (a v kontejneru `.3dheat` `extensions["heat3d/economy"]` v manifestu) obsahuje
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (totéž na hráče, s `netSl`), `vehicles` (na vozidlo hráče: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` a `check` (kolik řádků každého druhu bylo
oceněno, odhadnuto nebo neoceněno).

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
