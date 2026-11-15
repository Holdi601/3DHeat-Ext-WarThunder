---
title: "Økonomi"
nav_order: 14
lang: no
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Økonomi {#economy}

Hva slaget kostet og tjente, som kolonner på dets hendelsesrader, lest fra **din installasjon når
konverteringen kjøres** (`char.vromfs.bin`: `config/wpcost.blk` per kjøretøy, `config/warpoints.blk` og `config/rank.blk`; våpen-blk-ene i
`aces.vromfs.bin` sier hvilken modifikasjon hver granat er). Ingen av spillets tall ligger i dette depotet: verdiene
går bare inn i din egen utdata. Uten installasjonens `char.vromfs.bin` skrives ingen økonomi (`economy.available` false). Prisene er
de for slagets vanskelighetsgrad (`repairCostHistorical` for RB, `...Arcade` for AB, `...Simulation` for SB).

| Kolonne | Rader | Hva |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (en runde tatt etter et skudd, bakkekjøretøy), `launch` (fly, helikoptre) | SL-prisen for runden, raketten, missilet eller bomben |
| `cost_lost_sl` | `death` for et spillers kjøretøy | kjøretøyets reparasjonskostnad (standard; det fullt oppgraderte i blokken) |
| `earn_sl`, `earn_rp` | `reward` (ny hendelse, på tjenerens plass og tid) | SL og RP tjent |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | hver rad med en `cost_*` eller `earn_sl` | `SL` (`earn_rp` er forskningspoeng) |
| `econ_basis` | det samme | `install` (en pris lest fra installasjonen) eller `inferred` (regnet ut, se under) |

**Hvem vant.** `won` (0/1) på hver rad for et lag, der replayen sier det. En klientreplays resultater bærer
forfatterens eget utfall (`status`: `success` eller `fail`), så forfatterens lag vant eller tapte, og det andre laget det motsatte;
`result` i kampdokumentet sier hvilket (`winner`, `status`, `authorTeam`). Serverreplayer og replayer avsluttet før slutten
bærer ikke noe utfall (en serverreplays `status` er alltid `success` og nevner ingen forfatter), og ingen av de to typene
holder installerte modifikasjoner: resultatene lister hver spillers kjøretøy bare med navn og type. Der blir `won` tom.

Visningsprogrammets kostnadsmodell leser kolonnene `cost_*` (og `earn_*`) med `currency`; summen av `cost_fired_sl +
cost_lost_sl` gir hvor Silver Lions ble brukt og tapt, `earn_sl` der de ble tjent (en drapspremie står på sin `reward`-rad,
ikke på `kill`-raden, så ingenting telles to ganger).

- **Runder** (`install` der plassens granat er kjent - et drap navnga den, se [Utfall av treff](hits.md#hit-outcomes) -
  ellers `inferred`: gjennomsnittsprisen for granatene den kanonen kan skyte på det kjøretøyet; en standardgranat er gratis;
  maskingevær telles ikke av replayen og koster ingenting).
- **Oppskytinger** (`inferred`): spillet priser et flys våpenforvalg per utflyging, ikke per enhet; én enhet er medianen over
  forvalgene med pris for kjøretøyet av pris / enheter (`sum_weapons`; motmidler og hjelpetanker holdes utenfor); 0 der forvalgene er gratis.
- **Premier** (alle `inferred`): replayen har ingen premipost - resultatblokken har bare poengsummer og tellinger, og ingen melding
  bærer Silver Lions (kontrollert på klient- og serverreplayer). Et `kill` gir `aKill` x drapperens `rewardMul<modus>` x offerklassens
  vekt (`units` i warpoints.blk, etter dens `unitClass`; KI-enheter etter sin type) x `aiKillK` for et KI-offer x `groundKillMul`
  for et fly som dreper en bakkeenhet; RP det samme med `expMul` og rank.blk sine vekter. Hvert annet steg i en spillers poengsum i
  den replikerte resultattavlen er en premie verdt sine poeng ved slagets SL per poeng (et drap sin SL over medianen av poeng i
  drapenes steg, `pointsPerKill` i blokken); dens type er telleren som steg med det (assists, erobrede soner, sonskade, skadepremie,
  unndratte missiler), ellers den spillerens kritiske / alvorlige treff innen 3 s, ellers et oppdagelse av spillerens enhet innen 2 s
  (`scouting`), ellers `other`. `battle_end` er `winK` (vunnet) eller `defeatK` (tapt) av spillerens inntjening i slaget, vinneren
  etter lagenes gjenværende billetter, deretter poengsummen. Premietid, forsterkere, mannskap og modifikasjoner er ikke kjent og
  ikke brukt; bakkeslagenes drapsbudsjetter (`def_ground_kill_wp_budget*`) er ikke modellert.

Kampdokumentets `economy` (og, i en `.3dheat`-container, manifestets `extensions["heat3d/economy"]`) holder `currency` `SL`,
`researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`), `players` (det samme per spiller, med
`netSl`), `vehicles` (per spillers kjøretøy: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`,
`rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` og `check` (hvor mange rader av hver type som ble prisatt, anslått
eller ikke prisatt).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
