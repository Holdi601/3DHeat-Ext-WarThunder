---
title: "Economie"
nav_order: 14
lang: nl
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economie {#economy}

Wat het gevecht kostte en opleverde, als kolommen op de gebeurtenisrijen, gelezen uit **je eigen installatie op het moment van omzetten**
(`char.vromfs.bin`: `config/wpcost.blk` per voertuig, `config/warpoints.blk` en `config/rank.blk`; de wapen-blks
van `aces.vromfs.bin` zeggen welke modificatie elke granaat is). Er staat geen enkel getal van het spel in deze repository: de
waarden komen alleen in je eigen uitvoer. Zonder het `char.vromfs.bin` van de installatie wordt geen economie geschreven
(`economy.available` false). De prijzen zijn die van de moeilijkheidsgraad van het gevecht (`repairCostHistorical` voor RB,
`...Arcade` voor AB, `...Simulation` voor SB).

| Kolom | Rijen | Wat |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (een ronde die na een schot wordt bijgeladen, grondvoertuigen), `launch` (vliegtuigen, helikopters) | SL, de kosten van de ronde, raket, missiel of bom |
| `cost_lost_sl` | `death` van het voertuig van een speler | de reparatiekosten van het voertuig (standaard; het volledig opgewaardeerde in het blok) |
| `earn_sl`, `earn_rp` | `reward` (nieuwe gebeurtenis, op de plek en het tijdstip van de verdiener) | verdiende SL en RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | elke rij met een `cost_*` of `earn_sl` | `SL` (`earn_rp` zijn onderzoekspunten) |
| `econ_basis` | hetzelfde | `install` (een prijs die uit de installatie gelezen is) of `inferred` (uitgerekend, hieronder) |

**Wie won.** `won` (0/1) op elke rij van een team, waar de replay het zegt: de resultaten van een client-
replay dragen de eigen uitkomst van de auteur (`status`: `success` of `fail`), dus won het team van de auteur of verloor het, en het andere team het omgekeerde;
`result` in het wedstrijddocument zegt welke (`winner`, `status`, `authorTeam`). Server-replays en replays die vóór
het einde zijn achtergelaten, hebben geen uitkomst (de `status` van een server-replay is altijd `success` en noemt geen auteur),
en geen van beide soorten bevat geïnstalleerde modificaties: de resultaten geven van elke speler de voertuigen alleen
op naam en type. Daar blijft `won` leeg.

Het kostenmodel van de viewer leest de kolommen `cost_*` (en `earn_*`) met `currency`; het optellen van `cost_fired_sl +
cost_lost_sl` geeft waar Zilveren Leeuwen uitgegeven en verloren werden, `earn_sl` waar ze verdiend werden (de beloning van een
kill staat op zijn `reward`-rij, niet op de `kill`-rij, dus niets telt twee keer).

- **Rondes** (`install` waar de munitie van de slot bekend is - een kill heeft haar genoemd, zie [Uitkomsten van treffers](hits.md#hit-outcomes) -
  anders `inferred`: de gemiddelde prijs van de granaten die dat kanon op dat voertuig kan afvuren; een standaardgranaat is gratis; machinegeweren
  worden door de replay niet geteld en kosten niets).
- **Lanceringen** (`inferred`): het spel prijst de wapenpreset van een vliegtuig per uitvlucht, niet per item; één item is de
  mediaan over de geprijsde presets van het voertuig van prijs / items (`sum_weapons`, tegenmaatregelen en afwerptanks buiten beschouwing gelaten);
  0 waar zijn presets gratis zijn.
- **Beloningen** (allemaal `inferred`): de replay bevat geen beloningsrecord - het resultaatblok heeft alleen scores en tellingen,
  geen bericht draagt Zilveren Leeuwen (gecontroleerd op client- en server-replays). Een `kill` levert `aKill` op x de `rewardMul<mode>`
  van de doder x het gewicht van de klasse van het slachtoffer (`units` in warpoints.blk, via zijn `unitClass`; AI-eenheden via hun
  soort) x `aiKillK` voor een AI-slachtoffer x `groundKillMul` voor een vliegtuig dat een grondeenheid doodt; RP hetzelfde met
  `expMul` en de gewichten van rank.blk. Elke andere stap van de score van een speler op het gerepliceerde scorebord is een beloning
  die zijn punten waard is tegen de SL per punt van het gevecht (de SL van een kill over de mediaan van de punten van de stappen van de kills,
  de `pointsPerKill` van het blok); zijn type is de teller die ermee steeg (assists, veroverde zones, zoneschade, schadebeloning,
  ontwijken van raketten), anders de kritieke / zware treffer van die speler binnen 3 s, anders een detectie van de eenheid
  van de speler binnen 2 s (`scouting`), anders `other`. `battle_end` is `winK` (gewonnen) of `defeatK` (verloren) van de
  verdiensten van de speler in het gevecht, de winnaar bepaald door de overgebleven tickets van de teams, daarna hun score. Premiumtijd, boosters,
  bemanning en modificaties zijn niet bekend en worden niet toegepast; de doodbudgetten van de grondgevechten
  (`def_ground_kill_wp_budget*`) zijn niet gemodelleerd.

Het `economy` van het wedstrijddocument (en, in een `.3dheat`-container, `extensions["heat3d/economy"]` van het manifest)
bevat `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (hetzelfde per speler, met `netSl`), `vehicles` (per voertuig van de speler: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` en `check` (hoeveel rijen van elke soort geprijsd,
geschat of niet geprijsd waren).

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
