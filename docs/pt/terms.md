---
title: Termos e licença
nav_order: 16
lang: "pt"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Termos e licença {#terms-and-licence}

## Os termos {#the-terms}

Termos de Serviço da Gaijin (atualizados em 2026-08-17), EULA (Anexo 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Ler os arquivos de nível da sua própria cópia para uma visão 3D
local é decisão do usuário, tomada sabendo disso. Os níveis gerados ficam na sua
máquina: **nunca os publique**, e nada aqui distribui dados do jogo.

## Fontes {#sources}

Todo o código aqui foi escrito para este projeto; nenhum código foi copiado de outro
analisador. O que ele sabe sobre o formato vem de:

- O código-fonte do Dagor Engine da Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` e `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` para o fluxo de entidades (`ecs.py`), e `net/message.cpp`
  (`MessageClass::initImpl`) para como as mensagens de entidade numeram suas classes.
  Os nomes de componentes e tipos são comparados por seus hashes FNV-1a com palavras dos
  próprios arquivos do jogo; `ecs.py` lista os nomes encontrados.
- Do mesmo código: `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` e
  `daNet/bitStream.h`: como uma mensagem nomeia o objeto a que se destina
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, e o seu próprio analisador
  `web/wrpl-parse.js`, lidos para os layouts de bits do modelo de voo, sincronia de
  terrestres, armas em voo, mensagens com campos de id, slots de jogadores, os valores
  de cabine e o blk binário. O WTACRP cita como próprias referências maxsupermanhd/wrpl-inspector,
  wt_blk e wrpl-acmi (AGPL-3.0); o código deles não foi lido aqui.
- Os replays do próprio autor, lidos como arquivos: as diferenças de 2025 (o layout mais antigo
  do modelo de voo, chat sem byte de sinalização, zlib), a atitude em terra, o deslocamento de
  altura empacotado, os pontos de liberação das armas e os instrumentos de cabine foram
  descobertos aqui sobre eles.

## Testes {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<pasta com os replays de amostra> python -m pytest -q   # também confere os replays públicos de amostra de 2025
HEAT3D_WT_REPLAYS=<pasta dos seus replays> python -m pytest -q            # passos, identidades, sinais de IA, sinal do rolamento, o suavizador, nomes
```

Os testes unitários nunca leem uma instalação (`HEAT3D_WT_NO_NAMES` fica definido); o
teste com os seus replays lê os nomes da sua instalação.

Os testes criam replays em código (`tests/synth.py`: cabeçalho, pacotes, resultados,
o fluxo de entidades, armas em voo) no layout que os leitores documentam; nenhum replay
está no repositório.

## Licença {#licence}

MIT - veja [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Usa pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) e Pillow (MIT-CMU). Os leitores de nível foram escritos a partir
do código-fonte do Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licença BSD
3-Clause; nenhum código dele é copiado aqui, e as constantes de formato usadas (a chave XOR
do vromfs, os deslocamentos da grade de faixas de altura) são citadas onde aparecem.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
