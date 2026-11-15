---
title: Converter replays
nav_order: 4
lang: "pt"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Converter replays {#converting-replays}

Saída: um arquivo `.3dheat` por batalha (o padrão), ou arquivos soltos com
`--loose`.

## Passo a passo {#step-by-step}

1. **Ative a gravação de replays.** O War Thunder salva replays de cliente na pasta
   `Replays` do jogo, quando o salvamento de replays está ligado nas opções, por
   exemplo `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Um replay de servidor salvo na página de replays do jogo (um zip com `0000.wrpl`,
   `0001.wrpl`, ...) também pode ser convertido.
2. **Abra um terminal** numa pasta onde os resultados possam ser gravados
   ([Antes de começar](before-you-start.md)).
3. **Converta:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # arquivos, pastas, ou ambos
   heat3d-wt-replay battle.zip -o out              # o zip de um replay de servidor
   heat3d-wt-replay a.wrpl -o out --loose          # arquivos separados em vez de um .3dheat
   ```

   `out` é criada na pasta em que o seu terminal está.
4. **Leia o que ele diz.** Você deve ver uma linha por batalha.
5. **Abra:** carregue `out/<map>/<match>.3dheat` no visualizador 3DHeat
   ([Carregando um arquivo](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Uma execução em um replay sintético: um .3dheat, --loose, um arquivo com defeito, uma pasta vazia](../assets/img/convert.svg)

A figura mostra uma execução em um replay que os testes criam em código (sem replay
real e sem instalação do jogo):

- `ok <arquivo>`: uma batalha convertida (com `--loose`: `ok <tabela> <documento da partida>`);
- `failed <arquivo>: <motivo>`: um arquivo que não pôde ser lido (status de saída 1;
  os demais são convertidos mesmo assim);
- `no .wrpl files given`: nada para converter (status de saída 2);
- `note: ...`: por exemplo, que nenhuma instalação do War Thunder foi encontrada
  para dar nome aos veículos.

## Opções {#options}

| Opção | Padrão | Faz |
|---|---|---|
| `replays` (uma ou mais) | - | arquivos `.wrpl`, pastas com eles (a própria pasta, não as subpastas), ou zips com eles (um replay de servidor: as partes `.wrpl` são descompactadas numa pasta temporária) |
| `-o`, `--out` | obrigatória | onde gravar: uma pasta por mapa dentro |
| `--game PASTA` | encontrada | a pasta do War Thunder cujos textos dão nome a veículos, armas e munições, e cujas tabelas precificam a [economia](economy.md); também `HEAT3D_WT_GAME` |
| `--no-smoothing` | desligada | mantém as amostras de outras unidades estimadas por inércia e recebidas como estão no replay ([Estimativa por inércia](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | ligada | junta cada batalha num único arquivo `.3dheat` |
| `--loose` | desligada | mantém cada batalha como arquivos separados (tabela, documento da partida, arquivos auxiliares) |
| `--version` | - | mostra `heat3d-wt-replay <versão>` e para |
| `-h`, `--help` | - | mostra as opções e para |

Uma batalha convertida de novo é gravada de novo. As opções como o programa as
mostra: [Referência de comandos](../cli-reference.md).

## Quais arquivos formam uma batalha {#which-files-are-one-battle}

Cada batalha vira um arquivo,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<início, UTC>_<id da sessão>.3dheat`. AB, RB
e SB são as siglas do jogo para batalhas arcade, realistas e de simulador;
`<mode>` é o modo da missão como o jogo o identifica (`Conq4` Conquista nº 4,
`Dom` Dominação, `Bttl` Batalha; veja [Modo de batalha](ground.md#battle-mode));
quando o replay não informa uma das partes, ela fica de fora. As partes de um replay
de servidor (`0000.wrpl`, `0001.wrpl`, ...) são lidas juntas como uma batalha; um
replay de cliente e as partes do servidor da mesma batalha são duas gravações e
continuam sendo duas.

## Status de saída {#exit-status}

`0` quando todas as batalhas foram convertidas, `1` quando alguma falhou (as demais
são convertidas mesmo assim), `2` quando nenhum arquivo de replay foi encontrado
entre os argumentos.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
