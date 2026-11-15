---
title: A tabela
nav_order: 6
lang: pt
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# A tabela {#the-table}

![A tabela de um replay sintético, resumida](../assets/img/table.svg)

Uma linha por amostra ou evento, 105 colunas ([Lista de colunas](../columns.md), gerada a partir do código); no rodapé, sob `heat3d`, as instruções de leitura do visualizador, então o visualizador não precisa de nenhum formulário preenchido.

| Coluna | O que é |
|---|---|
| `time` | segundos no relógio do próprio replay |
| `event` | `position`; as linhas de evento ficam sobre a trilha no seu momento (entre duas amostras, na linha entre elas); `kill` (no abatedor), `death` (na vítima), `hit_critical` / `hit_severe` (na unidade atingida), `module_destroyed` (na unidade), `launch` (na unidade que liberou uma arma), `impact` (a última amostra de uma arma quando foi removida logo depois); `explosion` e `flak` (0xD08E, 0xD01F) na sua posição, tipo `effect`, sem trilha, com a direção da explosão onde há uma; `shot` (um projétil que acertou, no atirador), `gun_shot`, `fire_start`, `fire_stop` (a rajada de um canhão, não um veículo em chamas), `fire_on`, `fire_off` (um veículo em chamas, veja [Incêndios em veículos](hits.md#vehicle-fires)), `reward` (Leões de Prata e pontos de pesquisa ganhos, veja [Economia](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (veja [Mensagens para unidades](how-it-reads.md#messages-to-units)); `despawn`: a última linha de uma trilha cuja unidade some antes do fim do replay (veja [Fim de uma trilha](ground.md#end-of-a-track)) |
| `track` | o que o visualizador desenha como uma coisa só: uma vida de uma unidade, ou o voo de uma arma - `<player or vehicle> #<hex>` (o visualizador mostra o nome sem a parte `#`) |
| `x`, `y`, `z` | os metros do jogo: x para leste, y para cima, z para norte (as dicas espelham z, então o norte não é desenhado para o sul) |
| `player` | o nome do jogador; uma unidade de IA `<VehicleName> #<uid>` (por exemplo `F-15A #204`); `uid <n>` quando nada a nomeia; para uma arma, quem a liberou |
| `userId`, `team` | o id Gaijin do jogador e a equipe (`1`, `2`) |
| `ai`, `isPlayer` | `ai` verdadeiro para toda unidade que nenhuma conta de jogador dirige (unidades de missão, aviões de IA, alvos terrestres, canhões antiaéreos, navios sem jogador, substitutos), `isPlayer` o oposto: um jogador é uma unidade cuja entidade nomeia um slot de jogador com um id Gaijin. Uma arma tem o do seu lançador; vazio quando não se sabe |
| `match` | o id da partida (o `match` do documento da partida), em toda linha; as dicas o mapeiam como a sessão, então dois replays carregados nunca juntam trilhas |
| `life` | `uid#n`: a trilha de uma unidade, cortada quando o uid passa para outra unidade, a unidade se move mais rápido do que pode (um renascimento, um rearmamento, o jogo movendo-a, o cliente corrigindo uma unidade distante; veja Teletransportes em [Como ele lê um replay](how-it-reads.md#what-is-read-and-the-check)) ou fica muito tempo sem ser vista; `w<hex>` o voo de uma arma (`w<hex>#n` depois de um corte) |
| `uid` | o id da unidade no replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (um bonde ou vagão de trilho que o nível coloca, veja [Unidades de cena](objectives.md#scene-units-trams-and-rail-wagons)); armas `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` a câmera de replay do jogador que grava (veja [A câmera](ground.md#the-camera)) |
| `type` | o tipo próprio do jogo onde os resultados o informam (`fighter`, `assault`, `destroyer`, `gun_boat`), senão igual a `kind` |
| `Vehicle` | o id do veículo no jogo (`f_15a`, `germ_flakpz_I_Gepard`), que as figuras do visualizador usam |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | o nome em inglês do veículo, da localização da sua instalação (`Pz.Kpfw. III Ausf. J1`, curto `Pz.III J1`) e a sua chave (`germ_pzkpfw_III_ausf_J_0`); as marcas de país da fonte do jogo ficam de fora. Onde o jogo não nomeia nada, ou não se acha instalação, o nome é o id e a chave fica vazia |
| `mission` | o nome da unidade na missão (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | para onde a unidade aponta (o vetor de visão): aviões a partir da atitude do modelo de voo, unidades terrestres e navios a partir da sua própria, armas ao longo do seu voo |
| `heading`, `pitch`, `roll` | o mesmo em graus; o rumo é a bússola, no sentido horário a partir do norte, arfagem com o nariz para cima positiva, rolamento com a asa direita para baixo positivo (o modelo de voo envia o sinal oposto, veja [Atitude, conferida](aircraft.md#attitude-checked); o lado direito de uma unidade terrestre para baixo). As dicas dizem isso em `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | a torre principal de um tanque - para onde o canhão aponta, não para onde o seu jogador olha; o valor do replay limitado à velocidade do mecanismo da torre e posto na linha de cada tiro do canhão principal (veja [Torres](ground.md#turrets)): a sua rotação em relação ao casco (graus, positiva no sentido horário visto de cima, 0 em frente) e a elevação do canhão em relação ao casco (graus, positiva para cima); `turrets` cada torre do veículo como `yaw pitch;yaw pitch;...` na sua própria ordem (um slot não usado lê `0.00 0.00`). Tanques, SPAA, APCs e caminhões, em replays de cliente e de servidor; não navios (veja [Torres](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | a torre principal como o replay a envia; `turretYaw` / `gunPitch` são ela limitada à velocidade do mecanismo e posta na linha de cada tiro do canhão principal (veja [Torres](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | para onde o jogador olha (mira com a câmera) no mundo: graus de bússola (0 norte, sentido horário) e graus para cima, a mesma convenção de `aimHeading` / `aimPitch` (ao contrário de `turretYaw` / `gunPitch`, que continuam relativos ao casco). O tanque de cada jogador num replay de servidor, o do próprio jogador que grava num replay de cliente; vazio onde o jogador não mira em lugar nenhum (os quatro floats de mira em 0). A torre segue isso na sua própria velocidade de rotação, então os dois diferem enquanto ela gira (veja [Torres](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | o próprio tanque do jogador que grava: para onde mira (graus de bússola, graus para cima, a distância em m; 2000 quando nada está na mira); linhas de câmera: para onde o jogador mira (rumo, arfagem) |
| `zoom` | linhas de câmera: a ampliação da câmera (veja [A câmera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | o `AB`, `RB` ou `SB` da batalha, e `ground`, `air` ou `naval`, em toda linha (veja [Modo de batalha](ground.md#battle-mode)) |
| `extrapolated` | uma amostra de avião que é a estimativa por inércia do cliente, não um estado recebido (veja [Estimativa por inércia](aircraft.md#dead-reckoning-and-the-smoother)); uma amostra de bomba calculada a partir da sua liberação (veja Bombas sem registros de voo em [Como ele lê um replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | o quanto o suavizador moveu a amostra (m), e a posição e a atitude próprias do replay (o rolamento no sinal da tabela) |
| `targetX`, `targetY`, `targetZ` | o ponto de impacto de um `shot` |
| `hitOutcome`, `hitFlags` | o resultado de um `shot` numa unidade terrestre: `kill`, `critical`, `penetration` ou `nonpenetration` (ricocheteou ou foi parado: o replay não distingue um ricochete), a partir dos bits que o servidor envia com o acerto (`hitFlags`, bruto); vazio onde nenhum é enviado (aviões, navios). Veja [Resultados dos acertos](hits.md#hit-outcomes) |
| `hitShell` | a assinatura do projétil de um `shot`: quatro bytes da mensagem de acerto (hex bruto); uma assinatura pode representar projéteis diferentes (120 e 125 mm APFSDS compartilham uma), então é guardada bruta, não lida como calibre |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | a munição de um `shot`: o seu tipo (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) e o seu id (`125mm_3bm46`) onde um abate nomeia o compartimento do atirador, senão `explosive` (a rajada do acerto) ou `kinetic`; o `weapon/slot` do canhão a partir das suas recargas; o calibre em mm dos arquivos de arma da instalação. Veja [Resultados dos acertos](hits.md#hit-outcomes) |
| `rpm` | a rotação do motor de um avião (a média dos seus motores) como enviada por último, em 2 s |
| `vx`, `vy`, `vz` | a velocidade de um avião como a sua entrada de voo a envia (m/s, os eixos do jogo; velocidades acima de 500 m/s leem 500) |
| `engine`, `afterburner`, `engineCondition` | os motores de um avião pela sua entrada de voo: `off`, `starting`, `running`, `dead` (unidos por `/` quando os seus motores diferem); a pós-combustão de 0 a 1; um byte enviado só depois que o motor foi atingido |
| `weaponName` | abates e mortes: a arma ou munição no inglês da sua instalação (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | só o avião do jogador que grava: a aceleração de 0 a 1,1 da sua cabine (1,1 potência de emergência de guerra ou pós-combustão; senão os quinze avos da sua entrada de voo), os controles de -1 a 1 da sua entrada de voo (profundor positivo puxando, aileron positivo rolando para a direita), as munições restantes por arma (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | só o avião do jogador que grava, da sua cabine: velocidade indicada e taxa de subida (m/s), combustível, pressão do coletor (atm), trem de pouso (0 a 1, 1 abaixado), temperatura do óleo e da cabeça dos cilindros, onde a sua cabine tem o medidor |
| `speed` | m/s em cerca de dois segundos da trilha (calculado aqui; o replay não envia velocidade para as outras unidades) |
| `alive` | 0 para as amostras de uma unidade depois da sua morte (o seu destroço): de uma unidade terrestre ou de um navio até o jogo a remover ou as suas amostras terminarem, de um avião por no máximo 60 s |
| `otherVehicle`, `otherLife` | a vítima de um `shot`: o seu veículo e a sua `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | o ponto de impacto de um `shot` no próprio referencial da vítima (m; x para a frente, y para cima, z para a esquerda; veja [Mensagens para unidades](how-it-reads.md#messages-to-units)) e o sentido do tiro, transformado nesse referencial pela atitude da vítima naquele momento |
| `hitPart`, `hitFlag` | a mensagem de acerto de um `shot`: a sua palavra de peça como enviada, e o seu byte alto |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | quanto a batalha custou e rendeu, e quem venceu: veja [Economia](economy.md) |
| `other`, `weapon` | abates: o outro lado e a arma; acertos: quem acertou (a partir do uid do registro, senão do slot do jogador), o veículo deles; lançamentos: a arma; módulos destruídos: quem atingiu a unidade por último nos 5 s antes, e `part <n>` |

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
