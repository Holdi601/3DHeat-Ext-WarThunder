---
title: Acertos, tiros e incêndios
nav_order: 13
lang: "pt"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Acertos, tiros e incêndios {#hits-gunfire-and-fires}

Para quem quer saber de onde vêm as colunas de acerto, munição e incêndio. As verificações
dão só o método e a concordância.

## Tiros {#gunfire}

Todo projétil que acertou uma unidade está no replay (mensagem 0xF0E9): uma linha `shot` na
posição do atirador no momento do acerto, `targetX/Y/Z` o ponto de impacto (a unidade
atingida, deslocada pelo ponto de impacto no seu referencial, girada pela sua atitude), a
direção até ele, `other` a unidade atingida. Projéteis e balas que erraram não são enviados:
não são entidades, e as mensagens de armas em voo trazem só foguetes, mísseis, bombas e
torpedos. As munições restantes do jogador que grava (a coluna `ammo`) caem à medida que ele
atira, então suas rajadas podem ser identificadas, mas não para onde essas munições foram. A
antiaérea pesada e a artilharia enviam cada tiro isolado (`gun_shot`, sem direção); os canhões
antiaéreos de 40 mm enviam as suas rajadas (`fire_start`, `fire_stop`).

## Resultados dos acertos {#hit-outcomes}

Em todo acerto de projétil numa unidade terrestre, o servidor envia à unidade a mensagem
0xF144 (UnitOnHit): quatro campos de um byte, o quarto com os bits do que o acerto causou
(`selfCheck.unitMessages.outcome_*`):

| Bit | Significado | Evidência |
|---|---|---|
| 0x20 | o próprio acerto de um projétil | quase todos vêm com um acerto 0xF0E9 na unidade em 5 ms; sem ele, com uma explosão (de estilhaços) |
| 0x01 | atravessou (penetração) | toda mensagem com 0x02, 0x04 ou 0x08 também o tem |
| 0x02 | acerto crítico | a maioria dos registros de acerto crítico o tem, bem mais do que por acaso |
| 0x04 | destruído | a maioria vem com um registro de abate e a morte da unidade em um segundo |
| 0x08 | dano pesado | alguns registros de acerto crítico o têm; raro fora disso |

`hitOutcome` fica com o pior: `kill` (0x04), `critical` (0x02 ou 0x08), `penetration` (0x01),
`nonpenetration` (só 0x20). Um acerto é pareado com a 0xF144 com 0x20 mais próxima da sua
unidade, em 5 ms. A câmera de acerto do jogo distingue um ricochete de uma não penetração,
mas nenhum bit ou campo encontrado aqui faz isso: os três primeiros bytes variam de acerto
para acerto e não são conhecidos. Replays de cliente enviam 0xF144 só para o próprio avião do
jogador que grava, com todos os bits zerados: acertos em aviões e navios não têm resultado.

## Munição {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosivo ou não.** Um projétil que explode envia 0xF133 (UnitOnExplosion) com o uid do
  atirador e o número do acerto; um acerto com ele é `explosive`, os demais `kinetic`.
* **O canhão e o seu compartimento.** 0xF0BD (UnitBulletRearm) é a próxima munição carregada:
  o índice da arma na lista de armas do veículo, o compartimento de munição e as munições
  restantes. O de um carregador manual vem um tempo de recarga constante depois de cada um
  dos seus acertos; o de um canhão automático, uma fração de segundo depois. Os acertos de um
  atirador são agrupados por veículo, assinatura e rajada; um grupo é de uma arma quando essa
  arma carrega uma munição em 20 s depois de metade ou mais dos seus acertos, com um atraso
  constante. `ammoSlot` é `weapon/slot`, o compartimento carregado antes do acerto: provavelmente
  o disparado, a menos que o jogador tenha trocado a munição no meio. Metralhadoras não enviam
  0xF0BD.
* **O projétil.** A arma de um abate é o id do projétil (`125mm_3bm46`); o último acerto do
  abatedor na vítima o atribui ao compartimento desse atirador, onde o calibre do canhão confere.
  O tipo e o calibre são os do arquivo da arma (`bulletName`, `bulletType`, `caliber`;
  `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **O calibre** dos demais: o da arma do compartimento; o de um grupo de metralhadora, o único
  calibre de metralhadora que a sua assinatura pode ter; senão o do canhão principal do veículo.
  Sem a instalação (`--game`), não há tipo, nome nem calibre além de `explosive` / `kinetic`.

Não encontrado: ricochete. Várias outras mensagens trazem o atirador e o número do acerto
(0xF0C2, provavelmente o caminho da câmera de acerto pelo veículo; 0xF117, 0xF13C, 0xF13E); elas
ficam no arquivo auxiliar, não decodificadas. Uma não penetração continua `nonpenetration`.

## Incêndios em veículos {#vehicle-fires}

Um veículo em chamas é mostrado a todo cliente: o servidor envia ao veículo uma mensagem de
entidade (evento `0a519c58`) listando os incêndios que queimam nele, sempre que a lista muda.
Para cada incêndio: dois ids de 16 bits (o segundo, um nó do modelo de dano), o seu tipo, e -1
enquanto o fogo não pegou. Um incêndio aceso por um acerto também recebe uma mensagem com o
ponto onde queima, no referencial do veículo (x para a frente, y para cima, z para a esquerda).

Linhas: `fire_on` quando um incêndio aparece na lista, `fire_off` quando sai, no veículo, com
`fireId` (`first:node`), `fireKind` e, para incêndios acesos por um acerto, `fireLocalX/Y/Z`
(frente, cima, direita). Depois que um veículo morre, a sua lista muitas vezes não é mais
enviada: os seus incêndios terminam com o destroço, senão com a entidade, senão com o replay
(`selfCheck.fires`).

Conferido: cada vez que a contagem de extintores de incêndio de um tanque caiu, um incêndio saiu
da lista em uma fração de segundo; a maioria dos pontos de incêndio fica do mesmo lado do
veículo que o acerto que o acendeu. Os tipos são números; o que nomeiam não é conhecido, nem
qual peça é cada nó. Aviões não enviam essa lista: um avião em chamas não é lido.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
