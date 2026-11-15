---
title: Aviões
nav_order: 11
lang: "pt"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Aviões {#aircraft}

Para quem quer saber de onde vêm as colunas dos aviões e quanto confiar nelas. Cada
verificação abaixo compara um valor com algo que o replay diz de uma segunda forma,
independente; aqui se dão só o método e a concordância.

## Instrumentos de cabine {#cockpit-instruments}

A mensagem 0xD04A envia os medidores do jogador que grava como pares (número, valor):
quatro por segundo nas batalhas arcade, só os valores que mudaram nas batalhas de
simulador. Os números formam uma só lista para todas as cabines, e cada cabine envia os
medidores do seu modelo. O código do jogo define qual número é qual medidor, então cada
número foi nomeado pelo que faz e conferido com o replay (`convert.INSTRUMENTS` guarda o
resultado; nada é lido da instalação):

| Número | Nome | Conferido contra |
|---|---|---|
| 0 | velocidade indicada, m/s | a velocidade da trilha corrigida pela densidade do ar: correlação 0,99 |
| 39 | taxa de subida, m/s | a taxa de subida da trilha: correlação acima de 0,99 |
| 40, 41 | altitude, m; altitude módulo 1000 | a altura da trilha, a poucos metros de diferença |
| 52, 53 | rolamento e arfagem do horizonte artificial | menos o rolamento e a arfagem da tabela, a menos de 1 grau de diferença |
| 64 | bússola | o rumo da tabela, a menos de 0,1 grau de diferença |
| 15-20 | pedais do leme | a força lateral sobre o avião |
| 23, 31 | manche: profundor e ailerons (sinal como o do modelo da cabine) | o ângulo de ataque; a taxa de rolamento |
| 69, 71, 73 | relógio: horas (mostrador de 12 horas), minutos, segundos | a hora local do computador que gravou, até o minuto |
| 75 | pressão do coletor, atm | mais alta em potência de emergência de guerra do que em potência máxima |
| 81-86, 87-92, 93-98 | rotação por motor, rotação módulo 1000, indicador de rotação | iguais entre si; a rotação do motor: correlação acima de 0,97 |
| 195 | combustível | cai ao longo da surtida, cheio de novo ao renascer |
| 228-230 | pernas do trem de pouso, 1 abaixado | abaixado só perto da altura dos aeródromos e na velocidade de pouso |
| 240, 241 | aceleração por motor (1,1 potência de emergência de guerra ou pós-combustão) | a aceleração da entrada de voo |
| 330-332, 346-348 | contadores de munição (dois conjuntos iguais) | as munições do pacote de armas, caindo com as munições da entrada de voo |
| 135, 159 | temperatura do óleo e da cabeça dos cilindros | provável: sobem ao longo da surtida |
| 58, 61 | bola de derrapagem, agulha de curva | provável: seguem a força lateral e a taxa de curva |
| 223 | aerofreio | provável: acionado só na aproximação |
| 490-497, 500-505 | freios das rodas | provável: acionados só parado num aeródromo |

Outros números são enviados com um significado desconhecido; eles são guardados em
`authorInstruments.notNamed` do documento da partida.

As colunas `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` e `throttle` da tabela vêm daí, nas linhas do próprio jogador que
grava, pegando a última mensagem em no máximo 0,2 s depois da amostra.

## Entradas de voo {#flight-entries}

A entrada de voo de cada avião (tipo de pacote 2) traz, além da posição e da atitude:

- **Velocidade**: uma palavra de 32 bits depois da atitude. Os bits 31, 30 e 29 são os
  sinais de x, y e z; depois a velocidade em 11 bits de 500/2047 m/s (para em 500 m/s), e
  então |x| e |y| como frações da velocidade em 9 bits cada, e z é o que faz do vetor um
  vetor unitário. Conferido contra o passo entre amostras recebidas: a direção concorda
  com uma fração de grau para o jogador que grava e com cerca de 2 graus para todos os
  outros; a velocidade, com 0,2 %. `selfCheck.flightEntries`.
- **Munições por arma**: uma lista antes da posição, um item por arma, as munições
  restantes primeiro. A do jogador que grava é igual aos contadores da cabine um tique
  depois, em quase toda amostra.
- **Controles e aceleração**: 7 bytes depois da velocidade, lidos como 14 nibbles. Para o
  jogador que grava, a cada tique: 1 o profundor, 2 os ailerons, 3 o leme (8 em repouso),
  11 a aceleração em quinze avos (15 também para potência de emergência de guerra e
  pós-combustão), 4 os freios das rodas, 5 o aerofreio, 8 provavelmente o paraquedas de
  freagem. Os nibbles dos outros aviões mudam só algumas vezes numa batalha e não são os
  controles deles naquele momento.
- **Motores**: por motor, um byte de estado (0 desligado; 1-6 ligando; 7 funcionando; 8
  morto), um valor de 16 bits só com pós-combustão (32767 no máximo), e um byte só depois
  que o motor foi atingido. A maioria dos aviões cujo motor fica "morto" são abatidos ou
  terminam em minutos.

## Dados de reflexo {#reflection-data}

As mensagens 0xF02D e 0xF0AA replicam os objetos numerados do jogo: para cada objeto, o
seu id (os 5 bits do topo, o tipo; os 11 baixos, um índice) e uma tabela de campos. O tipo
14 são os slots de jogadores (campo 2 o id de usuário e o nome, 9 a equipe), e o tipo 15
são as equipes (índice 1 e 2):

- O campo 39 de um slot guarda as suas estatísticas em lugares fixos: abates (deslocamento
  0), abates de equipe (2), mortes (4), abates navais (10), abates de IA (12), abates
  terrestres de IA (14), assistências (20), zonas de captura (22), dano em zonas (24, 32
  bits), prêmio de dano (40, 32 bits), esquivas de mísseis (50). O campo 38 começa com a
  pontuação, o campo 42 é o esquadrão. No fim de uma batalha, cada valor é igual ao dos
  resultados, para cada jogador (`selfCheck.scoreboardVsResults`). Onde são guardados os
  abates terrestres não é conhecido.
- O campo 7 de uma equipe é a sua pontuação: no fim, é igual à soma das pontuações dos
  seus jogadores nos resultados. O campo 3 provavelmente são os seus tickets.
- Cada mensagem envia só os campos que mudaram, então o `scoreboard` do documento da
  partida lista as estatísticas de cada jogador e a pontuação de cada equipe a cada
  mudança.

## Estimativa por inércia, e o suavizador {#dead-reckoning-and-the-smoother}

Um replay de cliente grava cada avião quatro vezes por segundo, como o cliente o
desenhou. Entre as atualizações que recebe de um avião distante, o cliente o move
adiante pela sua última velocidade e o faz girar pelas suas últimas taxas, e na
atualização seguinte o encaixa ali de repente. Lido como está, um rastro corre em linha
reta e depois salta. Nada na entrada de voo marca quais amostras foram recebidas; uma
amostra estimada por inércia é reconhecida pelo que é: continua a reta das duas amostras
anteriores, no mesmo ritmo, com menos de 3 cm de diferença.

O quanto isso importa depende da batalha: nas batalhas arcade, cerca de metade das
amostras dos outros aviões pode ser estimada por inércia; nas de simulador, só alguns
por cento. O suavizador corta em cerca de cinco vezes os passos acima de 15 g
(`selfCheck.deadReckoning`). O próprio avião do jogador que grava não é extrapolado pelo
cliente e fica como está.

Por padrão (`--no-smoothing` desliga), as trilhas de todas as unidades menos as do próprio
jogador que grava são postas onde os estados recebidos dizem que estavam: uma amostra
estimada por inércia vai para uma curva que passa pelas amostras recebidas antes e depois
dela, cada uma com a sua própria velocidade; por mais de 3 s, a reta só se curva em direção
à próxima amostra recebida, então nenhuma amostra se move mais do que o encaixe próprio do
cliente. A sua atitude gira de modo uniforme de uma atitude recebida até a seguinte. As
amostras recebidas são suavizadas em no máximo 2 m ou 0,04 s do seu ritmo; uma curva
constante permanece como está. Os valores próprios do replay ficam nas colunas `Raw`.

## Atitude, conferida {#attitude-checked}

No próprio avião do jogador que grava, o rumo fica a um grau (mediana) da direção do
deslocamento, a arfagem a poucos graus do ângulo de subida, e nas curvas bem definidas o
rolamento tem o sinal da curva em quase toda amostra: o rolamento do modelo de voo é
positivo com a asa esquerda para baixo, e a tabela o converte para positivo com a asa
direita para baixo (`selfCheck.aircraftAttitude`). Os ângulos de 10 bits dão passos de
0,18 grau. A atitude das unidades terrestres é conferida contra os seus tiros
([Torres](ground.md#turrets)).

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
