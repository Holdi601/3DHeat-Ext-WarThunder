---
title: Unidades terrestres e câmera
nav_order: 12
lang: pt
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unidades terrestres e câmera {#ground-units-and-camera}

Para quem quer saber de onde vêm as colunas de torre, câmera e modo de batalha, e quanto
confiar nelas. As verificações dão só o método e a concordância.

## Torres {#turrets}

O estado terrestre de um tanque (atitude de 16 bits) traz, depois da posição, 141 bits não
lidos, e então, por torre, 62 bits: a rotação da torre e a elevação do canhão (16 bits cada,
360/65536 graus por passo, com sinal) e 30 bits não lidos; depois o preenchimento, e em
alguns estados mais 200 bits. A quantidade de torres é o byte enviado antes do estado. Um
estado cujo tamanho não cabe não dá torres (unidades estáticas enviam um estado menor). A
rotação é relativa ao casco, positiva no sentido horário, 0 em frente; a elevação é relativa
ao casco, positiva para cima.

Como foi conferido:

- **Contra os tiros:** para cada acerto de um tanque, a direção no mundo do seu canhão
  principal (a atitude do casco girada pela rotação da torre e pela elevação do canhão)
  contra a linha do atirador até a unidade atingida, a pelo menos 30 m: por batalha, uma
  mediana de cerca de 98 % dentro de 3 graus em rumo e 99 % em elevação
  (`selfCheck.turretsVsShots`). Os restantes são, na maioria, acertos de uma metralhadora em
  outra torre.
- **Contra a mira do jogador que grava:** o próprio tanque envia o ângulo no mundo da sua
  mira (anti-horário a partir do leste), a arfagem e a distância. O rumo do casco somado à
  rotação da torre fica a meio grau (mediana) da mira.

**Replays de servidor** (0xF074) enviam o estado de cada tanque no mesmo layout, seguido de
dados próprios; então cada torre cujos dois ângulos caem dentro do estado é lida (pelo menos
a principal, em quase toda linha de tanque). É a torre, não a câmera:

- **Contra os tiros**, como acima: por batalha, acima de 90 % dentro de 3 graus em rumo e 99 %
  em elevação.
- **Contra a visão:** um replay de servidor envia a mira de cada jogador (`viewYaw`,
  `viewPitch`). A torre segue a visão dentro de meio grau (mediana), mas gira bem mais devagar
  do que a visão oscila, como um mecanismo de torre (`selfCheck.turretVsView`).
- **Mas nem sempre na velocidade de um mecanismo:** amostra a amostra, o valor como enviado às
  vezes pula para a mira quando ela está perto do canhão, mais rápido do que qualquer
  mecanismo gira.

Assim, a tabela guarda a torre **limitada ao seu mecanismo**: `turretYaw` / `gunPitch` se
movem na direção do valor enviado, sem passar da velocidade de giro do canhão principal no
arquivo de veículo da instalação (vezes 1,3 para habilidades da tripulação e modificações;
45 e 20 graus por segundo onde a instalação não informa nenhuma). A cada acerto do canhão
principal, a torre é posta exatamente na linha do tiro, e uma passagem para trás a leva até
lá a tempo (`selfCheck.turretLimit`). A linha `shot` também traz esses `turretYaw` /
`gunPitch`. O valor como enviado fica em `turretYawRaw` / `gunPitchRaw`. Um tanque cujo
estado não traz torre tem as colunas de torre vazias (o visualizador pode recorrer a
`viewYaw`).
`gunPitch` fica um pouco acima de `viewPitch` à distância: é a elevação do canhão para a
queda do projétil.

Os estados de navios têm outro layout; as suas torres não são lidas. Aviões não enviam
direção de cabeça nem de visão; a mensagem 0xD020 dos canhões antiaéreos fica não lida.

## A câmera {#the-camera}

A mensagem 0xD043, cerca de 20 por segundo, é a câmera de replay do próprio jogador que
grava: o campo 1 é um quatérnio que gira a frente da câmera para onde ela olha; o 2, o lugar
da câmera a partir do veículo que segue (m); o 4, o mesmo deslocamento no referencial do
veículo (x para a frente, y para cima, z para a esquerda); o 5, para onde o jogador mira (um
vetor unitário); o 3, o zoom (cerca de 1,2 na visão de terceira pessoa de um tanque, cerca de
1,0 num avião, mais alto na mira de artilheiro ou com binóculo). Conferido: o campo 4 é o
campo 2 girado para o referencial do veículo, a menos de 0,5 m em quase toda mensagem; a
frente da câmera tem o rumo da mira. O replay não envia campo de visão em graus, só o zoom.

A tabela tem a câmera como uma trilha própria: tipo `camera`, trilha `<player> camera #ca`,
uma linha no máximo a cada 0,1 s, no lugar do veículo seguido mais o campo 2, olhando ao
longo do quatérnio (`dirX/Y/Z`, `heading`, `pitch`, `roll`), com `zoom`, `aimHeading` e
`aimPitch`, e `otherLife` a vida que ela segue. `selfCheck.camera` conta as linhas e a
verificação.

## Fim de uma trilha {#end-of-a-track}

Uma trilha é desenhada da sua primeira linha até a última. Quando a sua unidade some antes
do fim do replay, a última linha é uma linha `despawn` no seu último lugar: no momento em
que o jogo removeu a sua entidade (quando isso ocorreu dentro de 6 s da sua última amostra),
senão na sua última amostra. Uma trilha sem uma dessas linhas dura até o fim do replay. As
linhas de uma mesma trilha podem estar bem afastadas (uma unidade distante ou um destroço é
atualizado a cada poucos segundos, e um destroço às vezes não é atualizado por minutos): o
seu último estado vale até a próxima linha.

## Modo de batalha {#battle-mode}

O byte do cabeçalho no deslocamento 688 guarda a dificuldade nos seus quatro bits baixos:
0 arcade (AB), 5 realista (RB), 10 simulador (SB). Conferido contra os tipos de batalha que
se sabia terem sido os dos replays. O modo de jogo é `ground` quando a missão permite que
tanques surjam, senão `naval` quando permite navios, senão `air` (`allowedUnitTypes`); o
modo da própria missão vem da sua chave (`missions/_Dom`), com nome tirado de
`lang/missions_versus.csv` da sua instalação. A mesma chave é a parte `<mode>` dos nomes de
arquivo e o id da partida (`Conq4`, `Dom`), omitida onde o cabeçalho não traz nenhuma.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
