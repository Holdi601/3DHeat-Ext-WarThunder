---
title: Instalação
nav_order: 3
lang: pt
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalação {#installing}

Nunca usou a linha de comando? Leia primeiro [Antes de começar](before-you-start.md).
Precisa de Python 3.10 ou mais recente; pyarrow, numpy, zstandard e Pillow são
instalados junto.

## Passo a passo {#step-by-step}

1. Obtenha o código: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ou baixe um zip em [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   e descompacte.
2. Abra um terminal nessa pasta e digite `pip install -e .`. Isso instala
   dois comandos: `heat3d-wt-replay` (replays) e `heat3d-wt-level` (níveis).
3. Confira: `heat3d-wt-replay --version`. Você deve ver
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` lista as opções:

![heat3d-wt-replay --help](../assets/img/help.svg)

Sem instalar: `python -m heat3d_ext_warthunder ...` e
`python -m heat3d_ext_warthunder.levelcli ...` na pasta da ferramenta.

## Nomes da sua instalação {#names-from-your-install}

Veículos, armas e munições recebem seus nomes em inglês a partir dos arquivos de
texto do próprio jogo, lidos da sua instalação durante a conversão. A instalação é
encontrada pelo Steam ou pelas pastas padrão do launcher; `--game <pasta>` ou a
variável de ambiente `HEAT3D_WT_GAME` dizem onde ela está, caso não esteja. Nenhum
texto do jogo está neste repositório; sem uma instalação, os nomes são os
identificadores dos veículos (o conversor avisa isso numa linha `note:`).

## Atualizações {#updates}

A cada início, o comando verifica primeiro as releases do projeto no GitHub (no
máximo um pedido a cada poucas horas; nunca interrompe uma conversão, com ou sem
internet). Quando há uma versão nova, o comando pergunta antes de instalá-la: um
`git clone` é atualizado com `git pull --ff-only` (recusado se você tiver mudanças
locais), uma cópia baixada pelo arquivo da release. `HEAT3D_NO_UPDATE=1` desliga a
verificação e a atualização.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
