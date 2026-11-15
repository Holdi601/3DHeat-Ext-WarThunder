---
title: Arquivos auxiliares e completude
nav_order: 8
lang: "pt"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Arquivos auxiliares e completude {#sidecars-and-completeness}

Nada de um replay é descartado. O que o conversor lê vai para a tabela e para o
documento da partida; todo o resto é guardado inteiro em três arquivos auxiliares
ao lado da tabela (dentro do arquivo `.3dheat`, ou soltos com `--loose`). Esta é a
regra que todos os conversores do 3DHeat seguem:
[Conversores mantêm tudo](https://holdi601.github.io/3DHeat/converters.html).

## Os arquivos auxiliares {#the-sidecars}

- `<match>.messages.parquet`: cada mensagem para uma unidade (tempo, id e nome da
  mensagem, uid, eid, modelo, veículo, seus campos de id em hexadecimal, `decoded`
  (o que se lê dela, em JSON), a carga), cada valor de componente replicado (`name`
  o componente, `fields` o seu valor), cada mensagem de entidade (com o número de
  entidade e de classe), cada objeto replicado (`ReflectionData <kind>/<index>`, seus
  campos em hexadecimal) e cada pacote que nenhum leitor daqui lê, inteiro.
- `<match>.objectives.parquet`: as zonas de captura ao longo do tempo, uma linha por
  mudança enviada pelo servidor: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (a letra da zona), `zoneId`, `object`, `owner` (0 nenhum,
  1, 2), `progress` (-100..100, positivo para a equipe 2), os `x`, `y`, `z` da zona e
  todos os `fields` do objeto em hexadecimal (veja [Objetivos](objectives.md)).
- `<match>.flight.parquet`: cada entrada do modelo de voo de cada avião, inteira
  (seus bits e `phase`: o bit do primeiro byte em que começou), com sua velocidade,
  os 14 nibbles de controle (`control1-3`, `throttle`), seus motores com o estado,
  pós-combustão e condição, e suas munições por arma (`ammo`; `numbers` é a lista
  completa). Os valores dos outros aviões são os da última atualização.

## O que as contagens garantem {#what-the-counts-guarantee}

As `counts` do documento da partida dizem o que o replay continha e o que
aconteceu com cada coisa:

| Chave | O que é |
|---|---|
| `packets`, `unreadPackets` | cada tipo de pacote encontrado, e os que nenhum leitor lê (guardados inteiros no arquivo auxiliar de mensagens) |
| `messageIds`, `messageIdsNotRead` | cada id de mensagem encontrado e quantas vezes, e os que só foram guardados, não lidos |
| `replicatedComponents`, `replicatedNotRead` | valores de componentes lidos, e os que só foram guardados |
| `entities`, `entityTemplates`, `entityMessages` | o que o fluxo de entidades criou e enviou |
| `droppedSamples` | amostras deixadas de fora de propósito (os destroços de uma unidade terrestre depois que sua entidade some), por motivo |

Nada mais fica de fora: cada item do replay ou é lido para a tabela ou para o
documento da partida, ou é guardado inteiro num arquivo auxiliar. O `selfCheck` do
documento da partida reúne as verificações do que foi lido
([Como lê um replay](how-it-reads.md)).

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
