---
title: Como ele lê um replay
nav_order: 10
lang: "pt"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Como ele lê um replay {#how-it-reads-a-replay}

Esta página é para quem quer saber o que o conversor lê, como foi verificado e, com
isso, quanto confiar em cada coluna. Você não precisa dela para converter replays.

A leitura foi verificada em replays de cliente de batalhas aéreas arcade, aéreas de
simulador e navais, em replays de servidor de batalhas terrestres e, para os layouts de
2025, nos replays públicos de amostra de
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Cada verificação compara um valor com algo que o replay diz de uma segunda forma,
independente; aqui se dão só o método e a concordância.

## O que é lido, e a verificação {#what-is-read-and-the-check}

| Parte | Situação, e a verificação |
|---|---|
| Cabeçalho, mapa, missão, hora de início, sessão; resultados | todos os arquivos |
| Configurações da missão (o blk depois do cabeçalho) | modo, clima, limites, `stars` (data, hora, lugar) |
| Fluxo de pacotes (zlib em 2025, zstd em 2026) | cada pacote enquadrado |
| Posições e atitude dos aviões (layout de 2026) | 4 amostras por segundo, nenhum pacote deixado sem leitura; o rumo concorda com a direção do deslocamento |
| Pacotes de voo adiantados | depois de uma falha de rede, o pacote de voo de um replay de cliente às vezes põe todos os outros aviões onde estarão cerca de 0,75 s depois. O adiantamento é medido por pacote, e cada avião que se adianta recebe o tempo que representa (`selfCheck.flightPacketsRetimed`) |
| Saltos da estimativa por inércia | um salto de uma sequência estimada por inércia é medido a partir do último estado recebido, então as correções do cliente não cortam mais as trilhas ([Estimativa por inércia](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teletransportes | uma trilha é cortada onde a sua unidade se move mais do que pode: primeiro pelo seu tipo (avião 750 m/s, terrestres e navios 40 m/s, armas 1800 m/s), depois pelo seu próprio ritmo. Cada corte é listado em `trackBreaks` com a sua causa provável (renascimento, o jogo movendo o jogador, uma correção de uma unidade distante). Depois dos cortes, nenhum passo entre linhas de uma trilha é mais rápido do que o seu tipo permite (`selfCheck.stepSpeed`) |
| Posições de terrestres e navios (0xF073 / 0xF074) | nenhum pacote deixado sem leitura. Rumo, arfagem e rolamento a partir da atitude de 16 bits: o rumo concorda com a direção do deslocamento em cerca de 2 graus (mediana); a arfagem conta 180/65536 graus por passo; com o sinal do rolamento invertido, a direção do canhão a partir do casco e da torre aponta para a unidade atingida em quase todo tiro de tanque. Navios ficam no nível da água |
| Torres | rotação da torre e elevação do canhão dos tanques: veja [Torres](ground.md#turrets) |
| Alturas de terrestres empacotadas | posições empacotadas em 64 bits contam a altura a partir de -100 m na maioria dos níveis e a partir do nível da água em alguns; o deslocamento é medido em cada replay a partir de unidades vistas nas duas formas (`selfCheck.packedGroundHeight`) |
| Fluxo de entidades (criação, destruição) | cada criação lida. O layout vem do código-fonte publicado do Dagor Engine; os tipos de componente próprios do War Thunder são pulados encontrando onde começa o próximo componente. O veículo e o slot de jogador de cada unidade são iguais aos que os registros de abate e de acerto nomeiam, em todo registro conferido |
| Quem dirigiu qual unidade, unidades de IA, navios, alvos terrestres | do fluxo de entidades: cada unidade tem seu veículo e equipe, a unidade de cada jogador tem seu jogador |
| Abates contra os resultados | as mortes por jogador são iguais às dos resultados; os resultados contam mais abates, pois o cliente não recebe todos os abates. Um replay que começa depois que a batalha já começou traz só os abates posteriores a esse ponto |
| Abates, acertos críticos, dano severo | todos os arquivos |
| Módulos destruídos (0xF118) | a unidade e o número da peça; o nome da peça precisa do modelo de dano do veículo, que não está no replay |
| Armas liberadas (fluxo de entidades) | o ponto de liberação fica a uns 10-20 m (mediana) da unidade mais próxima, que é tomada como o lançador |
| Armas em voo (0xF0DB) | mísseis, foguetes e bombas, cada um ligado à sua entidade |
| Bombas sem registros de voo | uma bomba sem eles tem sua queda calculada desde a liberação até o impacto (gravidade e arrasto, uma amostra a cada 0,1 s, `extrapolated` verdadeiro). Conferido sobre o mar, onde a altura do impacto é conhecida: as quedas calculadas terminam a cerca de 15 m da água. No documento da partida, essa arma tem `ballisticImpact`; `counts.bombsBallistic` as conta |
| Slots de jogadores, chat | todos os arquivos |
| Explosões, rajadas antiaéreas, prêmios, detecções, clima, objetos de missão | lidos; posições conferidas a olho no visualizador |
| Instrumentos do jogador que grava (0xD04A) | nomeados pelo que fazem: [Instrumentos de cabine](aircraft.md#cockpit-instruments); os demais em `notNamed` |
| Outros campos das entradas de voo | velocidade, munições, controles, motores: [Entradas de voo](aircraft.md#flight-entries) |
| Atitude nas linhas de evento | cada linha de evento traz o rumo, a arfagem, o rolamento e o vetor de visão da sua unidade naquele momento |
| Estatísticas de jogadores e pontuações de equipe | no fim da batalha, cada estatística é igual à dos resultados, para cada jogador: [Dados de reflexo](aircraft.md#reflection-data) |
| Nomes de armas e veículos | da localização em inglês da sua instalação; alguns cintos padrão de navios e radares de aeródromos não têm nome no jogo |
| Jogadores e IA | nenhuma linha de jogador dos resultados é IA, toda linha que não é IA é de um jogador dos resultados (`selfCheck.identity`) |
| Destroços | as amostras de uma unidade depois da sua morte continuam chegando; o destroço de uma unidade terrestre ou de um navio é `alive` 0 até a sua entidade ser removida, e continua sendo uma trilha só; aviões mantêm `alive` 0 por no máximo 60 s (`selfCheck.wrecks`) |
| Trocas de veículo | uma unidade de jogador ainda viva quando a próxima unidade do mesmo jogador aparece é encerrada ali (um veículo deixado de pé). `selfCheck.vehicleSwitch.twoLiveVehicles` deve ser 0 |
| Modo de batalha | [Modo de batalha](ground.md#battle-mode) |
| Aviões em um replay de servidor de 2026 | lidos no layout de 2026; o rumo e o sinal do rolamento concordam com as curvas; aviões de substituição e drones de reconhecimento não trazem dados |
| Jogadores de um replay de servidor | encontrados pelo nome nos slots; cada estatística é igual à dos resultados (`selfCheck.players`) |
| Aviões em replays de servidor de 2025 e na versão 101286 | não lidos: seus pacotes de voo têm outro layout |

## Mensagens para unidades {#messages-to-units}

Cada pacote do tipo 4 é uma mensagem mpi do daNet do Dagor Engine: o id do objeto
destinatário, depois (quando os seus 11 bits baixos estão todos em 1) o UID ext do objeto,
o id da mensagem e a carga. Uma mensagem para uma unidade leva como UID ext o id de entidade
da unidade, `index << 10 | generation`. Conferido: toda mensagem assim nomeia uma entidade
viva naquele momento.

Para especialistas, as mensagens lidas são:

| Mensagem | O que é, e a verificação |
|---|---|
| 0xF0E9 UnitHitEffects | o acerto de um projétil: o uid do atirador e o ponto de impacto no referencial da unidade (x para a frente, y para cima, z para a esquerda): centímetros em aviões e navios, 20/32768 m por passo em unidades terrestres (ajustado ao tamanho das torres de tanques). `hitLocalX/Y/Z` em metros. Vira uma linha `shot` ([Tiros](hits.md#gunfire)). O atirador de quase todo registro de acerto e de abate está entre esses atiradores; os pontos de impacto ficam do lado voltado para o atirador |
| 0xF133 UnitOnExplosion | o mesmo uid de atirador |
| 0xF04B OnUnitDead | linhas `dead`: cada vítima de registro de abate tem uma em 2 s |
| 0xD047 FmwRpm | as rotações dos motores (`rpm`); concorda com o indicador de rotação da cabine |
| 0xF0B1, 0xF0A0 | linhas `gun_shot`: tiros isolados de antiaérea pesada e artilharia |
| 0xF01B, 0xF01C | linhas `fire_start`, `fire_stop`: rajadas de canhões antiaéreos de 40 mm (um canhão disparando; um incêndio num veículo é `fire_on`, veja [Incêndios em veículos](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | linhas `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | os próprios acertos do jogador que grava e os que ele recebe, com arma e munição, nomeados pela instalação (`projectileHitReplays`) |
| 0xF13E, 0xF031 | o efeito visual de um acerto e um efeito tocado na unidade; vêm com um acerto na mesma unidade |
| 0xD041 | uma por canhão defensivo de um avião, duas vezes por segundo; seus índices batem com os armamentos de metralhador do modelo de voo |
| 0xD048, 0xF117 | layout lido, significado desconhecido |
| o resto (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | no arquivo auxiliar de mensagens, com a sua unidade e campos |

Os nomes são da comunidade (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Também lido {#also-read}

- **Replicação do fluxo de entidades** (0x22, 0x23): por entidade, um bloco de valores de
  componentes: temporizadores de reparo de navios, contagens de consumíveis, mudanças de dono e
  de equipe, superaquecimento de motor. Contado em `counts.replicatedComponents`; os valores no
  arquivo auxiliar de mensagens.
- **Ações do script da missão** (0xF028) e **dicas** (0xF0EC): `triggers`, `hints`.
  **Progresso da missão** (0xF07A, 0xF07C): `missionProgress`.
- **A câmera do replay** (0xD043): veja [A câmera](ground.md#the-camera).

## Não lido, e por quê {#not-read-and-why}

- **Nomes e corpos das mensagens de entidade** (0x20, 0x21): o número da classe é um lugar
  numa lista compilada dentro do jogo, não enviada e não está nos seus dados. Duas são lidas
  (os incêndios de um veículo e os seus extintores); o resto é guardado inteiro com a sua
  entidade e o número da classe.
- **Outros objetos replicados** (tipos diferentes de slots de jogadores e equipes): lidos e
  guardados, sem nome; não há nos resultados nada para conferi-los.
- **Controles, aceleração e munições de outros aviões**: atualizados só de vez em quando;
  guardados no arquivo auxiliar de voo, não na tabela.
- **Incêndios em aviões**: não encontrados em nenhuma mensagem; um avião em chamas não tem
  linha `fire_on`.
- **Nomes de armas liberadas**: a entidade de uma bomba ou foguete não tem nome; os registros
  de abate nomeiam a arma de um abate.
- **Tiros que erraram**: um replay traz só os acertos.

O `counts.messageIdsNotRead` e o `selfCheck` de cada documento da partida dizem o que um replay
novo contém e quão bem foi lido.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
