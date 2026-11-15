---
title: Objetivos
nav_order: 15
lang: pt
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objetivos {#objectives}

`objectives` no documento da partida lista o que a batalha disputa, a partir de duas fontes (`source`):

- **O replay** (`replay`): os objetos da missão que 0xD039 nomeia (zonas de captura `cz_circle_NN`, aeródromos, heliportos,
  bases), colocados onde os objetos replicados de tipo 3 (0xF02D) os põem agora - uma zona de captura começa no lugar do
  seu modelo e é movida para a zona deste modo no início (`moved`). Os números do tipo 3 seguem a ordem de 0xD039; cada
  objeto que não é movido fica exatamente onde 0xD039 o põe, o que confere a ordem. Uma zona de captura recebe a forma e
  o raio da área da missão no seu lugar (`area`, dentro de 2 m) e sua letra pelo próprio índice (campo 69 do tipo 5: 0 =
  A); a ordem das letras é a do replay, não conferida com o mapa do jogo.
- **A missão** (`mission`): o arquivo de missão `<mission>.blk` no `mis.vromfs.bin` da sua instalação e os modelos que
  ele importa (só leitura, no momento da conversão): suas áreas, classificadas pelo nome - pontos de surgimento (os pontos
  numerados `..._spawnareaNN` de um surgimento como um só `points`), áreas de batalha, alvos de bombardeio (`bomb_zone`),
  pontos de surgimento de comboios (`road_NN_spawn`), áreas de saída e de abate. Áreas de outro modo do mesmo mapa
  (`conq_`, `dom_`, `bttl_`, ...) ficam de fora, e das variantes `_arcade` / `_realistic` / `_hardcore` fica a da própria
  batalha (RB pega `_realistic`, senão `_hardcore`, como os scripts de missão fazem); marcadores de briefing, pontos de
  canhões antiaéreos e áreas com mais de 5 km (aquelas por onde os surgimentos se espalham) também ficam de fora. Cada
  surgimento informa quantos rastros de jogadores começaram nele (`used`, `usedByTeam`). Uma missão pode trocar os lados
  ao acaso (`randomSpawnTeams`): quando os surgimentos mostram as equipes do replay invertidas, cada `team` é trocada e o
  lado do nome é mantido como `missionTeam`. As rotas de comboio não estão nos pontos de passagem das missões como são
  lidos; só se informa onde os comboios aparecem.

As zonas de captura ao longo do tempo são o arquivo auxiliar `<match>.objectives.parquet`: os objetos replicados de tipo 5,
um por zona - campo 2 o seu dono (0, 1, 2), campo 67 o seu progresso de captura, um byte com sinal de -100 a 100 (positivo
para a equipe 2), campo 69 o seu índice. Conferido (`selfCheck.objectives`) em replays de servidor terrestres de batalhas
de Conquista e Dominação: cada mudança de dono vem com um jogador da equipe que captura ganhando um `captureZone` no
placar no mesmo instante (em 1,5 s) e com uma unidade terrestre viva dessa equipe dentro da zona; os surgimentos de cada
batalha mostram as equipes do replay num só sentido (muitas vezes trocadas em relação aos `t1_` / `t2_` da missão).

## Unidades de cena: bondes e vagões {#scene-units-trams-and-rail-wagons}

Um nível pode colocar unidades próprias: as entidades `unit_loader+rail_wagon` de um replay de servidor são os bondes do
arquivo de cena do nível (`gamedata/scenes/<level>_objects.blk` em `aces.vromfs.bin`: `setting__unit_class`, sua
transformação e `setting__isDead`). Suas entidades não trazem uid legível, então uma trilha terrestre sem entidade de
unidade cuja primeira amostra cai a menos de 2 m de uma unidade de cena é essa unidade: a sua classe como `Vehicle`, tipo
`train`, subtipo `tram`, `locomotive` ou `wagon`, sem equipe; uma unidade que a cena coloca morta (como bondes queimados)
é um destroço (`alive` 0) desde a sua primeira linha. O jogo não tem nome em inglês para elas; `VehicleName` é o id lido
como palavras ("Railway tram A"). Suas posições não oscilam: quase todas nunca se movem (cada amostra igual até o bit).
O replay as envia cerca de dez vezes por segundo de qualquer forma, então das suas amostras só ficam as que de fato as
movem (0,05 m ou 0,1 grau), e uma a cada 10 s (`selfCheck.sceneUnits` conta as amostras descartadas). Antes, elas eram
trilhas chamadas `uid 8` sem veículo.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
