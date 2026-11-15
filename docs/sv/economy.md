---
title: "Ekonomi"
nav_order: 14
lang: "sv"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomi {#economy}

Vad striden kostade och gav, som kolumner på dess händelserader, lästa ur **din
installation vid konverteringstillfället** (`char.vromfs.bin`: `config/wpcost.blk` per
fordon, `config/warpoints.blk` och `config/rank.blk`; vapen-blk:erna i
`aces.vromfs.bin` säger vilken modifiering varje granat är). Inget av spelets tal
finns i det här arkivet: värdena går bara in i din egen utdata. Utan installationens
`char.vromfs.bin` skrivs ingen ekonomi (`economy.available` falskt). Priserna är de för
stridens svårighetsgrad (`repairCostHistorical` för RB, `...Arcade` för AB,
`...Simulation` för SB).

| Kolumn | Rader | Vad |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (en runda som tas efter ett skott, markfordon), `launch` (flygplan, helikoptrar) | SL för rundan, raketen, roboten eller bomben |
| `cost_lost_sl` | `death` för en spelares fordon | fordonets reparationskostnad (standard; det fullt uppgraderade i blocket) |
| `earn_sl`, `earn_rp` | `reward` (ny händelse, vid den som tjänade och tiden) | SL och RP som tjänats |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | varje rad med en `cost_*` eller `earn_sl` | `SL` (`earn_rp` är forskningspoäng) |
| `econ_basis` | samma | `install` (ett pris lästa ur installationen) eller `inferred` (uträknat, nedan) |

**Vem som vann.** `won` (0/1) på varje rad för ett lag, där repriserna anger det: en
klientrepris resultat bär författarens eget utfall (`status`: `success` eller `fail`), så
författarens lag vann eller förlorade och det andra laget tvärtom; `result` i
matchdokumentet säger vilket (`winner`, `status`, `authorTeam`). Serverrepriser och
repriser som lämnats före slutet bär inget utfall (en serverrepris `status` är alltid
`success` och anger ingen författare), och ingendera slaget har installerade
modifieringar: resultaten listar varje spelares fordon bara med namn och typ. Där
förblir `won` tomt.

Visarens kostnadsmodell läser kolumnerna `cost_*` (och `earn_*`) med `currency`; att summera
`cost_fired_sl + cost_lost_sl` ger var Silver Lions gick åt och förlorades, `earn_sl` var de
tjänades (en dödsbelöning ligger på sin `reward`-rad, inte på `kill`-raden, så ingenting räknas
två gånger).

- **Skott** (`install` där skyttens granat är känd - en död namngav den, se
  [Träffutfall](hits.md#hit-outcomes) - annars `inferred`: medelpriset för de granater
  den kanonen kan skjuta på det fordonet; en standardgranat är gratis; kulsprutor räknas
  inte av repriserna och kostar ingenting).
- **Avfyranden** (`inferred`): spelet prissätter ett flygplans vapenförinställning per
  flygpass, inte per artikel; en artikel är medianen över fordonets prissatta
  förinställningar av pris / artiklar (`sum_weapons`, motmedel och släppbara tankar
  utelämnas); 0 där förinställningarna är gratis.
- **Belöningar** (alla `inferred`): repriserna innehåller ingen belöningspost - resultatblocket
  har bara poäng och antal, inget meddelande bär Silver Lions (kontrollerat på klient- och
  serverrepriser). En `kill` tjänar `aKill` x dödarens `rewardMul<mode>` x offerklassens vikt
  (`units` i warpoints.blk, efter dess `unitClass`; AI-enheter efter sitt slag) x `aiKillK`
  för ett AI-offer x `groundKillMul` när ett flygplan dödar en markenhet; RP på samma sätt
  med `expMul` och rank.blks vikter. Varje annat steg i en spelares poäng i den replikerade
  resultattavlan är en belöning värd sina poäng till stridens SL per poäng (en dödsbelönings
  SL över medianpoängen för dödsstegen, blockets `pointsPerKill`); dess typ är räknaren som
  steg upp med den (assists, erövrade zoner, zonskada, skadeutmärkelse, undvikna robotar),
  annars den spelarens kritiska / svåra träff inom 3 s, annars en upptäckt av spelarens enhet
  inom 2 s (`scouting`), annars `other`. `battle_end` är `winK` (vinst) eller `defeatK`
  (förlust) av spelarens intjänade belöningar under striden, vinnaren efter lagens kvarvarande
  biljetter, sedan poängen. Premiumtid, boosters, besättning och modifieringar är inte kända
  och tillämpas inte; markstridernas dödsbudgetar (`def_ground_kill_wp_budget*`) är inte
  modellerade.

Matchdokumentets `economy` (och, i en `.3dheat`-behållare, manifestets
`extensions["heat3d/economy"]`) innehåller `currency` `SL`, `researchCurrency` `RP`, `difficulty`,
`totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`), `players` (samma per spelare, med `netSl`),
`vehicles` (per spelares fordon: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`,
`crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`,
`economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`),
`winnerTeam`, `pointsPerKill` och `check` (hur många rader av varje slag som prissattes, uppskattades
eller inte prissattes).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
