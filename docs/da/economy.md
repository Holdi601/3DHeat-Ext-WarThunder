---
title: Økonomi
nav_order: 14
lang: "da"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Økonomi {#economy}

Hvad kampen kostede og indbragte, som kolonner på dens begivenhedsrækker, læst fra **din installation
på konverteringstidspunktet** (`char.vromfs.bin`: `config/wpcost.blk` pr. køretøj, `config/warpoints.blk`
og `config/rank.blk`; våbenblk'ene i `aces.vromfs.bin` siger, hvilken modifikation hver granat er). Intet
tal fra spillet ligger i dette repository: værdierne går kun ind i dit eget output. Uden installationens
`char.vromfs.bin` skrives ingen økonomi (`economy.available` falsk). Priserne er dem for kampens sværhedsgrad
(`repairCostHistorical` for RB, `...Arcade` for AB, `...Simulation` for SB).

| Kolonne | Rækker | Hvad |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (en patron taget efter et skud, landkøretøjer), `launch` (fly, helikoptere) | SL for patronen, raketten, missilet eller bomben |
| `cost_lost_sl` | `death` for en spillers køretøj | køretøjets reparationsomkostning (standard; det fuldt opgraderede i blokken) |
| `earn_sl`, `earn_rp` | `reward` (ny begivenhed, på den der tjente, og ved dens tid) | optjent SL og RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | hver række med en `cost_*` eller `earn_sl` | `SL` (`earn_rp` er forskningspoint) |
| `econ_basis` | det samme | `install` (en pris læst fra installationen) eller `inferred` (udregnet, nedenfor) |

**Hvem der vandt.** `won` (0/1) på hver række for et hold, hvor replayet siger det: et klientreplays
resultater bærer optagerens eget udfald (`status`: `success` eller `fail`), så optagerens hold vandt eller
tabte, og det andet hold det omvendte; `result` i kampdokumentet siger hvilket (`winner`, `status`,
`authorTeam`). Serverreplays og replays, der stoppes før slutningen, bærer intet udfald (et serverreplays
`status` er altid `success` og nævner ingen optager), og ingen af de to slags rummer installerede
modifikationer: resultaterne lister hver spillers køretøjer kun med navn og type. Der forbliver `won` tom.

Viewerens omkostningsmodel læser kolonnerne `cost_*` (og `earn_*`) sammen med `currency`; at lægge
`cost_fired_sl + cost_lost_sl` sammen giver, hvor Silver Lions blev brugt og tabt, `earn_sl` hvor de blev
tjent (et drabs belønning står på dets `reward`-række, ikke på `kill`-rækken, så intet tælles to gange).

- **Patroner** (`install`, hvor skudets granat for pladsen er kendt - et drab navngav den, se [Udfald af træf](hits.md#hit-outcomes) -
  ellers `inferred`: gennemsnitsprisen for de granater, den kanon kan skyde på det køretøj; en standardgranat
  er gratis; maskinpistoler tælles ikke af replayet og koster intet).
- **Affyringer** (`inferred`): spillet prissætter et flys våbenforvalg pr. udflyvning, ikke pr. stykke; et stykke
  er medianen over køretøjets prissatte forvalg af pris / stykker (`sum_weapons`, modforanstaltninger og
  udsmidsbare tanke udeladt); 0, hvor dets forvalg er gratis.
- **Belønninger** (alle `inferred`): replayet indeholder ingen belønningspost - resultatblokken har kun score og
  tællere, ingen meddelelse bærer Silver Lions (kontrolleret på klient- og serverreplays). Et `kill` giver
  `aKill` x dræberens `rewardMul<mode>` x offerklassens vægt (`units` i warpoints.blk, efter dens `unitClass`;
  AI-enheder efter deres art) x `aiKillK` for et AI-offer x `groundKillMul` for et fly, der dræber en landenhed;
  RP det samme med `expMul` og rank.blks vægte. Hvert andet trin i en spillers score i den replikerede
  scoreboard er en belønning, der er værd sine point i kampens SL pr. point (et drabs SL over medianpointene
  for drabenes trin, blokkens `pointsPerKill`); dets type er den tæller, der steg med det (assists, erobrede
  zoner, zoneskade, skadepræmie, missilundvigelser), ellers den spillers kritiske / alvorlige træf inden for
  3 s, ellers en detektion af spillerens enhed inden for 2 s (`scouting`), ellers `other`. `battle_end` er
  `winK` (vundet) eller `defeatK` (tabt) af spillerens indtjening i kampen, idet vinderen afgøres af holdenes
  resterende billetter, derefter deres score. Præmietid, boostere, mandskab og modifikationer er ikke kendt
  og ikke anvendt; landkampenes drabsbudgetter (`def_ground_kill_wp_budget*`) er ikke modelleret.

Kampdokumentets `economy` (og, i en `.3dheat`-container, manifestets `extensions["heat3d/economy"]`) indeholder
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`),
`players` (det samme pr. spiller, med `netSl`), `vehicles` (pr. spillers køretøj: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` og `check` (hvor mange rækker af hver slags
der blev prissat, estimeret eller ikke prissat).

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
