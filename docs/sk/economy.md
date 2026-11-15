---
title: "Ekonomika"
nav_order: 14
lang: sk
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomika {#economy}

Čo bitka stála a čo priniesla, ako stĺpce na jej riadkoch udalostí, čítané z **vašej inštalácie v čase konverzie**
(`char.vromfs.bin`: `config/wpcost.blk` pre každé vozidlo, `config/warpoints.blk` a `config/rank.blk`; blk súbory zbraní
v `aces.vromfs.bin` určujú, aký modifikát má každý náboj). Žiadne číslo hry nie je v tomto repozitári: hodnoty
idú len do vášho vlastného výstupu. Bez `char.vromfs.bin` z inštalácie sa ekonomika nezapíše (`economy.available` false).
Ceny sú ceny obtiažnosti bitky (`repairCostHistorical` pre RB, `...Arcade` pre AB, `...Simulation` pre SB).

| Stĺpec | Riadky | Čo |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (náboj doplnený po výstrele, pozemné vozidlá), `launch` (lietadlá, vrtuľníky) | SL, koľko stál náboj, raketa, strela alebo bomba |
| `cost_lost_sl` | `death` vozidla hráča | oprava vozidla (základná; v bloku plne vylepšeného) |
| `earn_sl`, `earn_rp` | `reward` (nová udalosť, na mieste a v čase toho, kto zarobil) | zarobené SL a RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | každý riadok s `cost_*` alebo `earn_sl` | `SL` (`earn_rp` sú výskumné body) |
| `econ_basis` | to isté | `install` (cena prečítaná z inštalácie) alebo `inferred` (vypočítaná, nižšie) |

**Kto vyhral.** `won` (0/1) na každom riadku tímu, kde to replay uvádza: výsledky klientského replaye nesú výsledok autora
(`status`: `success` alebo `fail`), takže tím autora vyhral alebo prehral a druhý tím naopak; `result` v dokumente zápasu
hovorí, ktorý (`winner`, `status`, `authorTeam`). Serverové replaye a replaye zanechané pred koncom výsledok nemajú
(`status` serverového replaye je vždy `success` a autora nemenuje), a ani jeden druh neobsahuje nainštalované modifikáty:
výsledky uvádzajú vozidlá každého hráča len podľa názvu a typu. Tam `won` zostáva prázdne.

Model nákladov v prehliadači číta stĺpce `cost_*` (a `earn_*`) spolu s `currency`; súčet `cost_fired_sl +
cost_lost_sl` ukazuje, kde sa Silver Lions minuli a stratili, `earn_sl` kde sa zarobili (odmena za zabitie je
na jeho riadku `reward`, nie na riadku `kill`, takže sa nič nepočíta dvakrát).

- **Náboje** (`install`, ak je známy náboj slotu – zabitie ho pomenovalo, pozri [Výsledky zásahov](hits.md#hit-outcomes) –
  inak `inferred`: priemerná cena nábojov, ktoré dané delo na tom vozidle môže vystreliť; štandardný náboj je zadarmo;
  guľomety replay nepočíta a nestoja nič).
- **Odpaly** (`inferred`): hra oceňuje prednastavenie zbraní lietadla za výlet, nie za kus; jeden kus je medián
  z oceneného prednastavenia vozidla: cena / počet kusov (`sum_weapons`, protiopatrenia a odhadzovacie nádrže vynechané);
  0 tam, kde sú prednastavenia zadarmo.
- **Odmeny** (všetko `inferred`): replay nemá záznam odmien – blok výsledkov má len skóre a počty, žiadna správa nenesie
  Silver Lions (overené na klientskych aj serverových replayoch). `kill` zarobí `aKill` × `rewardMul<mode>` vraha ×
  váhu triedy obete (`units` v warpoints.blk, podľa jej `unitClass`; jednotky AI podľa druhu) × `aiKillK` pri obeti AI ×
  `groundKillMul` keď lietadlo zabije pozemnú jednotku; RP rovnako s `expMul` a váhami z rank.blk. Každý ďalší krok
  skóre hráča v replikovanej tabuľke výsledkov je odmena v hodnote bodov pri SL za bod bitky (SL zabitia podelené
  mediánom bodov krokov zabití, `pointsPerKill` z bloku); jej typ je počítadlo, ktoré s ňou stúpla (asistencie, dobyté
  zóny, poškodenie zóny, odmena za poškodenie, úniky pred raketami), inak kritický alebo ťažký zásah hráča do 3 s, inak
  zistenie jednotky hráča do 2 s (`scouting`), inak `other`. `battle_end` je `winK` (výhra) alebo `defeatK` (prehra)
  z hráčovho zárobku v bitke, víťaz podľa zostávajúcich tiketov tímov, potom podľa skóre. Prémiový čas, zosilňovače,
  posádka a modifikáty nie sú známe ani nepoužité; limity zabití v pozemných bitkách (`def_ground_kill_wp_budget*`)
  nie sú modelované.

`economy` v dokumente zápasu (a v kontejneri `.3dheat` v `extensions["heat3d/economy"]` v manifeste)
obsahuje `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (to isté na hráča, s `netSl`), `vehicles` (na vozidlo hráča: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` a `check` (koľko riadkov každého druhu bolo
oceneno, odhadnuté alebo neocenené).

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
