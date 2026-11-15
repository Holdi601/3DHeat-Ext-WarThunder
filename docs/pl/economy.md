---
title: Ekonomia
nav_order: 14
lang: "pl"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomia {#economy}

Ile bitwa kosztowała i ile przyniosła, jako kolumny w jej wierszach zdarzeń, odczytane z **Twojej instalacji w czasie konwersji**
(`char.vromfs.bin`: `config/wpcost.blk` dla każdego pojazdu, `config/warpoints.blk` i `config/rank.blk`; bloki broni
z `aces.vromfs.bin` mówią, jaką modyfikacją jest każdy pocisk). Żadna liczba z gry nie znajduje się w tym repozytorium: wartości trafiają
tylko do Twojego własnego wyniku. Bez pliku `char.vromfs.bin` z instalacji nie zapisuje się żadna ekonomia
(`economy.available` ma wartość false). Ceny są te z trudności bitwy (`repairCostHistorical` dla RB,
`...Arcade` dla AB, `...Simulation` dla SB).

| Kolumna | Wiersze | Co to jest |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (nabój pobrany po strzale, pojazdy naziemne), `launch` (samoloty, helikoptery) | SL za nabój, rakietę, pocisk kierowany lub bombę |
| `cost_lost_sl` | `death` pojazdu gracza | koszt naprawy pojazdu (fabryczny; w bloku ten w pełni ulepszony) |
| `earn_sl`, `earn_rp` | `reward` (nowe zdarzenie, w miejscu i czasie tego, kto zarobił) | zarobione SL i RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | każdy wiersz z `cost_*` lub `earn_sl` | `SL` (`earn_rp` to punkty badań) |
| `econ_basis` | to samo | `install` (cena odczytana z instalacji) albo `inferred` (wyliczona, poniżej) |

**Kto wygrał.** `won` (0/1) w każdym wierszu drużyny, tam gdzie replay to podaje: wyniki replaya klienta niosą wynik autora
(`status`: `success` albo `fail`), więc drużyna autora wygrała lub przegrała, a druga drużyna odwrotnie; `result` w dokumencie meczu
mówi, która (`winner`, `status`, `authorTeam`). Replaye serwerowe i replaye zostawione przed
końcem nie mają wyniku (`status` replaya serwerowego to zawsze `success` i nie nazywa autora),
a żaden z tych rodzajów nie zawiera zainstalowanych modyfikacji: wyniki podają pojazdy każdego gracza
tylko z nazwy i typu. Tam `won` zostaje puste.

Model kosztów w przeglądarce czyta kolumny `cost_*` (i `earn_*`) wraz z `currency`; zsumowanie `cost_fired_sl +
cost_lost_sl` daje, gdzie wydano i straciło się Srebrne Lwy, a `earn_sl` gdzie je zarobiono (nagroda za zabójstwo
jest w jej wierszu `reward`, a nie w wierszu `kill`, więc nic nie liczy się dwa razy).

- **Naboje** (`install`, gdy znany jest pocisk slotu - nazwało go zabójstwo, zob. [Wyniki trafień](hits.md#hit-outcomes) -
  w przeciwnym razie `inferred`: średnia cena pocisków, które to działo może wystrzelić w tym pojeździe; pocisk fabryczny jest darmowy;
  karabiny maszynowe nie są liczone przez replay i nic nie kosztują).
- **Wystrzeliwania** (`inferred`): gra wycenia zestaw uzbrojenia samolotu za lot, a nie za sztukę; jedna sztuka to
  mediana po wycenionych zestawach pojazdu z cena / liczba sztuk (bez `sum_weapons`, środków zaradczych i zbiorników
  odrzutowych); 0 tam, gdzie jego zestawy są darmowe.
- **Nagrody** (wszystkie `inferred`): replay nie zawiera zapisu nagród - blok wyników ma tylko punkty i liczniki,
  żadna wiadomość nie niesie Srebrnych Lwów (sprawdzono na replayach klienta i serwerowych). `kill` zarabia `aKill` x
  `rewardMul<mode>` zabójcy x wagę klasy ofiary (`units` w warpoints.blk, wg jej `unitClass`; jednostki AI wg
  rodzaju) x `aiKillK` dla ofiary AI x `groundKillMul` dla samolotu zabijającego jednostkę naziemną; RP tak samo z
  `expMul` i wagami z rank.blk. Każdy inny krok wyniku gracza w odtworzonej tablicy wyników to nagroda warta swoich punktów
  po SL za punkt bitwy (SL zabójstwa przez medianę punktów kroków zabójstw, `pointsPerKill` z bloku); jej typ to licznik, który
  wzrósł razem z nim (asysty, zdobyte strefy, obrażenia strefy, nagroda za obrażenia, uniki pocisków), w przeciwnym razie
  krytyczne / poważne trafienie tego gracza w ciągu 3 s, w przeciwnym razie wykrycie jednostki gracza w ciągu 2 s (`scouting`), w przeciwnym razie `other`. `battle_end` to `winK` (wygrana) albo `defeatK` (przegrana) zarobków
  gracza w bitwie; zwycięzcę wskazują bilety drużyn, a potem ich wynik. Czas premium, wzmacniacze,
  załoga i modyfikacje nie są znane i nie są stosowane; budżety zabójstw w bitwach naziemnych
  (`def_ground_kill_wp_budget*`) nie są modelowane.

Blok `economy` w dokumencie meczu (a w kontenerze `.3dheat` także `extensions["heat3d/economy"]` w manifeście)
zawiera `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (to samo na gracza, z `netSl`), `vehicles` (na pojazd gracza: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` i `check` (ile wierszy każdego rodzaju
wyceniono, oszacowano lub nie wyceniono).

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
