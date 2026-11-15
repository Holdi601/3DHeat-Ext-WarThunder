---
title: Economia
nav_order: 14
lang: pt
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economia {#economy}

Quanto a batalha custou e rendeu, como colunas nas linhas de evento, lidas da **sua instalação no momento da conversão**
(`char.vromfs.bin`: `config/wpcost.blk` por veículo, `config/warpoints.blk` e `config/rank.blk`; os blks de armas de
`aces.vromfs.bin` dizem qual modificação é cada projétil). Nenhum número do jogo está neste repositório: os valores vão
apenas para a sua própria saída. Sem o `char.vromfs.bin` da instalação, nenhuma economia é gravada (`economy.available`
falso). Os preços são os da dificuldade da batalha (`repairCostHistorical` para RB, `...Arcade` para AB, `...Simulation`
para SB).

| Coluna | Linhas | O que é |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (uma munição recarregada depois de um tiro, veículos terrestres), `launch` (aviões, helicópteros) | o custo em SL da munição, foguete, míssil ou bomba |
| `cost_lost_sl` | `death` de um veículo de jogador | o custo de reparo do veículo (de série; o totalmente melhorado no bloco) |
| `earn_sl`, `earn_rp` | `reward` (evento novo, no lugar e na hora de quem ganhou) | SL e RP ganhos |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | cada linha com um `cost_*` ou `earn_sl` | `SL` (`earn_rp` são pontos de pesquisa) |
| `econ_basis` | o mesmo | `install` (um preço lido da instalação) ou `inferred` (calculado, abaixo) |

**Quem venceu.** `won` (0/1) em cada linha de uma equipe, onde o replay informa: os resultados de um replay de cliente
trazem o próprio resultado do autor (`status`: `success` ou `fail`), então a equipe do autor venceu ou perdeu, e a outra
equipe o contrário; `result` no documento da partida diz qual (`winner`, `status`, `authorTeam`). Replays de servidor e
replays salvos antes do fim não trazem resultado (o `status` de um replay de servidor é sempre `success` e não nomeia o
autor), e nenhum dos dois tipos traz modificações instaladas: a lista de resultados mostra os veículos de cada jogador
apenas por nome e tipo. Nesses casos, `won` fica vazio.

O modelo de custos do visualizador lê as colunas `cost_*` (e `earn_*`) com `currency`; somar `cost_fired_sl +
cost_lost_sl` dá onde os Leões de Prata foram gastos e perdidos, `earn_sl` onde foram ganhos (a recompensa de um abate
está na sua linha `reward`, não na linha `kill`, então nada conta duas vezes).

- **Munições** (`install` quando a munição do compartimento é conhecida - um abate a nomeou, veja [Resultados dos
  acertos](hits.md#hit-outcomes) -, senão `inferred`: o preço médio das munições que aquele canhão pode disparar naquele
  veículo; uma munição de série é grátis; metralhadoras não são contadas pelo replay e não custam nada).
- **Lançamentos** (`inferred`): o jogo precifica o pacote de armas de um avião por surtida, não por item; um item é a
  mediana, entre os pacotes precificados do veículo, de preço / itens (`sum_weapons`, contramedidas e tanques
  descartáveis deixados de fora); 0 onde os pacotes são grátis.
- **Recompensas** (todas `inferred`): o replay não traz registro de recompensa - o bloco de resultados tem só
  pontuações e contagens, nenhuma mensagem leva Leões de Prata (verificado em replays de cliente e de servidor). Um
  `kill` rende `aKill` x o `rewardMul<mode>` do atacante x o peso da classe da vítima (`units` em warpoints.blk, pela sua
  `unitClass`; unidades de IA pelo tipo) x `aiKillK` para uma vítima de IA x `groundKillMul` quando um avião abate uma
  unidade terrestre; RP o mesmo com `expMul` e os pesos de rank.blk. Cada outro passo da pontuação de um jogador no
  placar replicado é uma recompensa valendo seus pontos em SL à taxa da batalha (o SL de um abate sobre a mediana de
  pontos dos passos de abates, o `pointsPerKill` do bloco); seu tipo é o contador que subiu junto (assistências, zonas
  capturadas, dano em zonas, prêmio de dano, esquivas de mísseis), senão o acerto crítico ou severo daquele jogador em
  3 s, senão uma detecção da unidade do jogador em 2 s (`scouting`), senão `other`. `battle_end` é `winK` (venceu) ou
  `defeatK` (perdeu) dos ganhos na batalha do jogador, sendo vencedora a equipe com mais tickets restantes, depois a
  pontuação. Tempo premium, impulsionadores, tripulação e modificações não são conhecidos nem aplicados; os orçamentos de
  abates das batalhas terrestres (`def_ground_kill_wp_budget*`) não são modelados.

A `economy` do documento da partida (e, num contêiner `.3dheat`, o `extensions["heat3d/economy"]` do manifesto) traz
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`),
`players` (o mesmo por jogador, com `netSl`), `vehicles` (por veículo de jogador: `repairSl`, `repairFullUpgradedSl`,
`purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`,
`economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`,
`pointsPerKill` e `check` (quantas linhas de cada tipo foram precificadas, estimadas ou não precificadas).

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
