---
title: O documento da partida
nav_order: 7
lang: pt
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# O documento da partida {#the-match-document}

![O início de um documento da partida sintético, e as suas chaves](../assets/img/match-document.svg)

`<match>.match.json` guarda tudo o que o replay diz e que não é uma linha da tabela. A aba
Partida do visualizador lê esse arquivo.

## A batalha {#the-battle}

| Chave | O que é |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | o id da partida (como no nome do arquivo); o id do mapa; o arquivo de nível que ele usa |
| `mission`, `missionKey` | o nome da missão e a sua chave nos arquivos de texto do jogo |
| `battleClass`, `environment`, `weather` | como o cabeçalho os informa |
| `sessionId`, `server` | o id de sessão da batalha; o servidor |
| `replayVersion`, `flightLayout` | a versão do formato do replay; o layout lido dos pacotes de voo (`2025` ou `2026`) |
| `files` | os arquivos de replay lidos (um, ou as partes de um replay de servidor) |
| `started`, `timePlayed`, `replayEnd` | hora de início (ISO, UTC); segundos jogados, dos resultados; segundos do último pacote do replay |
| `author`, `authorUserId` | o jogador que grava e o seu id Gaijin (replays de cliente) |
| `teams` | as equipes da batalha (`1`, `2`) |
| `result` | `winner`, `status` (`success` ou `fail`, o resultado do autor), `authorTeam`, `teams` ([Economia](economy.md)) |
| `vehicleNames` | de onde vieram os nomes dos veículos (a sua instalação) e o seu idioma |
| `conventions` | as unidades e os sinais da tabela: eixos, tempo, vida, trilha, alive, rolamento, e mais |

## Todo o resto {#everything-else}

| Chave | O que é |
|---|---|
| `battle`, `difficulty`, `gameMode` | o modo de batalha: `difficulty` `AB` / `RB` / `SB` (com o seu nome e o byte do cabeçalho), `gameMode` `ground` / `air` / `naval`, o modo da missão (`Dom`, `Conq`, `Bttl`, `I2M`, ...) e o seu nome em inglês da sua instalação (`Domination`, `Enduring Confrontation`), os tipos de unidade permitidos (veja [Modo de batalha](ground.md#battle-mode)) |
| `settings` | o blk da missão depois do cabeçalho: modo, ambiente, clima, pontuação e limites de tempo, países, tipos de unidade permitidos, vento, e `stars` (latitude, longitude, data, hora local) |
| `sky` | o primeiro `CustomWeatherParams`: direção do sol e da lua, vento, cores do céu, deslocamentos das nuvens |
| `players`, `slots` | a linha dos resultados por jogador (abates, abates terrestres, mortes, assistências, pontuação, capturas, esquadrão, clã, país, formação, os uids que dirigiram); os slots de jogadores do replay (nome, id de usuário, equipe) |
| `units` | cada entidade de unidade que o replay criou: eid, uid, modelo, veículo, tipo, subtipo, equipe, jogador, nome na missão, quando foi criada e removida, onde foi criada, quais componentes não puderam ser lidos |
| `objects` | os objetos nomeados da missão: zonas de captura e aeródromos com a sua posição e tamanho, contornos dos aeródromos como pontos, áreas de surgimento |
| `objectives` | os objetivos da batalha, cada um com `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (o 1 ou 2 do replay, vazio para ambos), `name` (uma zona de captura com a sua letra, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) com `position`, `radius` / `height` / `size` e `heading`, `source` (`replay` ou `mission`) e o que mais se sabe (veja [Objetivos](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | com os nomes e os veículos dos dois lados; abates com o nome em inglês da arma |
| `weapons` | cada foguete, míssil, bomba, torpedo, tanque descartável e carga lançada: quando, onde foi liberada (posição, atitude, velocidade), por qual unidade (a mais próxima em 300 m e 1,5 s), quantas amostras de voo, onde foi vista pela última vez, quando foi removida |
| `explosions`, `flak` | `PlayExplosionVisual` (posição, direção, tipo) e `PlayFlakExplosionVisual` (posição) |
| `awards` | as premiações do jogador que grava (`TextStreak`: first_blood, sequências, contadores de desafio) |
| `detections`, `unitStates` | pares `UnitDetected` de unidades; uma mensagem (0xF093) com a posição, a atitude e a velocidade de uma unidade, cujo significado não é conhecido |
| `authorInstruments` | os valores da cabine do jogador que grava (`ReplayCockpitParams`) por número de instrumento, no máximo um por segundo; `known` nomeia cada número que este replay enviou (nome, unidade, como foi conferido), `notNamed` os demais |
| `scoreboard` | as estatísticas de cada jogador cada vez que mudaram (abates, mortes, assistências, pontuação, abates de IA, abates navais, zonas, dano, esquivas de mísseis, esquadrão), e a pontuação e os tickets prováveis de cada equipe ao longo do tempo (veja [Dados de reflexo](aircraft.md#reflection-data)) |
| `economy` | os Leões de Prata e os pontos de pesquisa da batalha (veja [Economia](economy.md)): totais, por jogador, por veículo, os multiplicadores, o vencedor, as verificações |
| `entityMessages` | as mensagens de entidade (0x20) por número de classe: contagem, modelos alvo, tamanhos |
| `chat` | cada linha do chat |
| `triggers`, `hints`, `missionProgress` | as ações do script da missão (RunTriggerAction), suas dicas, suas mensagens de progresso |
| `camera` | os campos da câmera de replay do jogador que grava a cada 0,25 s, como enviados (a tabela a tem como trilha) |
| `projectileHitReplays` | os próprios acertos do jogador que grava e os que ele recebe, com arma, munição e os seus nomes em inglês |
| `results` | o blk de resultados inteiro, como o jogo o escreveu |
| `counts` | linhas, eventos, vidas, tipos, amostras, entidades por modelo, armas, pacotes lidos e não lidos, cada id de mensagem visto e os não lidos, amostras descartadas |
| `trackBreaks` | cada corte de uma trilha por um passo mais rápido do que a unidade pode ir: onde, quanto, quão rápido, e o que é mais provavelmente |
| `selfCheck` | as verificações listadas em [Como ele lê um replay](how-it-reads.md), calculadas em cada conversão; `stepSpeed` dá, por tipo, a velocidade entre linhas consecutivas de uma trilha como o visualizador as une (mediana, percentil 99, maior, e passos mais rápidos do que o possível, que devem ser 0) |

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
