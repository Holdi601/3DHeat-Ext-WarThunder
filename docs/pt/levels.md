---
title: Níveis
nav_order: 9
lang: pt
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Níveis (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` transforma os níveis da sua própria instalação do War Thunder em
níveis `.glb` para o visualizador, no mesmo referencial das tabelas dos replays.

## Passo a passo {#step-by-step}

1. Liste os níveis da sua instalação: `heat3d-wt-level list`. Ele mostra uma linha
   por nível: o nome, o terreno e os mapas, depois a contagem. Por exemplo (um nível
   inventado):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Extraia um, vários (curingas são aceitos) ou todos:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Carregue `levels/<level>/<level>.glb` no painel Fundo / nível do visualizador, sob as
   batalhas daquele mapa.

Os níveis que você gera ficam na sua máquina: nunca os publique (veja
[Termos e licença](terms.md)).

## Opções {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Comando / opção | Faz |
|---|---|
| `list [--game PASTA]` | cada nível da instalação |
| `extract <levels...>` / `--all` | os níveis indicados (como `list` os mostra; curingas são aceitos), ou todos |
| `-o`, `--out` | pasta de saída; cada nível vai para `<out>/<level>/` |
| `--game PASTA` | a pasta do War Thunder (padrão: encontrada pelo Steam ou pelo launcher; também `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | amostragem do terreno, cor do chão e orçamento de objetos sobre o mapa de tanques (padrão `medium`) |
| `--max-object-triangles N` | o orçamento de objetos (padrão: o do nível de detalhe) |
| `--max-grid N` | amostras do mapa de altura por lado, por parte (padrão 1024) |
| `--no-objects` | deixa de fora construções, árvores e outros objetos colocados |
| `--no-generated` | deixa de fora os objetos que as classes de terreno geram (florestas, cidades) |
| `--no-terrain-colour` | texturiza o chão com o mapa tático, não com as classes de terreno |
| `--no-texture` | deixa o chão sem textura |
| `--skip-existing` | deixa de lado os níveis cujo `.glb` já existe |

## O que é gravado {#what-is-written}

Cada nível vira `<out>/<level>/<level>.glb`, `<level>.json` (o que foi lido, o nível
da água, os retângulos dos mapas, contagens de triângulos, tempos) e os mapas táticos
do nível como `<level>_map.png` (o mapa aéreo) e `<level>_tankmap.png`; os mapas
terrestres também recebem `<level>_terrain.png`, as cores do próprio chão sobre o
mapa de tanques. O glb é gravado em `<level>.glb.part` e renomeado quando fica
completo; enquanto um nível é gravado, `<out>/<level>/.<level>.lock` fica travado,
para que duas extrações nunca gravem o mesmo nível (a segunda mostra `busy <level>`).
A instalação é encontrada pelo Steam ou pelas pastas padrão do launcher;
`--game <pasta>` ou `HEAT3D_WT_GAME` dizem onde ela está, caso não esteja.

| Parte | O que é |
|---|---|
| `ground:<level>` | o mapa de altura do terreno (`HM2`) como uma grade; nos mapas terrestres, o centro do mapa de tanques (metade da largura) no passo do `--detail`, colorido com as classes de terreno, decalques do chão e estradas (`<level>_terrain.png`; o mapa tático onde isso não é possível); nos mapas sem mapa de tanques (mapas aéreos), o mapa de altura inteiro num só passo (2048 amostras por lado em `high`, 1024 nos demais), colorido com as classes de terreno sobre a área do mapa aéreo (4096 pixels por lado, cerca de 32 m por pixel sobre 131 km; o mapa tático onde isso não é possível); nos níveis sem mapa de altura, a malha do terreno |
| `ground:<level> tank map` | o resto do mapa de tanques, um passo mais grosso |
| `ground:<level> heightmap surroundings` | o resto do mapa de altura, ainda mais grosso |
| `ground:<level> land mesh` | os triângulos de colisão da malha do terreno onde o mapa de altura não chega (os arredores de um mapa de tanques, até dezenas de quilômetros); nos níveis sem mapa de altura, é o chão, colorido como acima |
| `ground:<level> outside the map` | chão que a imagem não cobre, sem textura |
| `water:<level>` | um retângulo plano na `water_level` do nível sobre todo o terreno: o jogo desenha a água como um plano só, e o terreno baixo sob ele é mar, lago ou leito de rio |
| `water:<level> rivers` | nos níveis com mapa de altura da água (`WHM`), a superfície inclinada da água sobre as células que ela cobre |
| `structure:<level> buildings` | cada objeto colocado que não é planta: casas, ruínas, muros, cercas, pontes, trilhos, rochas, adereços. Os fixos (`RIGz`) e, sobre o mapa de tanques, os que as classes de terreno geram (quarteirões, pedras). Cada um é desenhado pela sua malha de renderização (paredes, telhados, aberturas de janelas, vigas), no LOD que o orçamento de triângulos permite, colorido por material com a média da sua textura difusa |
| `structure:<level> trees` | árvores e arbustos, fixos e gerados (florestas, cercas vivas): a malha de renderização onde o orçamento permite, senão um tronco e uma copa (um cone para coníferas) na cor da própria folhagem da árvore, no tamanho real |

Objetos sem malha de renderização usam a forma de colisão; árvores sem ela usam a
copa. As cores de vértice (`COLOR_0`) guardam valores codificados em sRGB, que é como
o visualizador 3DHeat os lê.

**Coordenadas** são os metros do jogo com z espelhado: glb (x, y, z) = jogo (x, y, -z).
O mundo do jogo é de sistema esquerdo (x para leste, y para cima, z para norte); o
glTF é de sistema direito. `heat3d-wt-replay` mantém o z do jogo e diz ao visualizador
para espelhá-lo, então um replay e o nível do seu mapa se sobrepõem sem nenhum passo
de posicionamento. O JSON dá o retângulo de cada mapa tático em metros do jogo e seus
cantos no espaço do glb, para carregar o PNG como imagem de mapa.

**Detalhe.** `--detail low|medium|high` (padrão medium) define, sobre o mapa de tanques:

| | centro do mapa de tanques | resto do mapa de tanques | cor do chão | orçamento de objetos | mais triângulos por objeto | plantas geradas mantidas |
|---|---|---|---|---|---|---|
| low | a cada 4ª amostra | a cada 8ª | 4 m por pixel | 1,2 M | 1.500 | árvores 35 %, arbustos 20 % |
| medium | a cada 2ª | a cada 4ª | 2 m | 3,5 M | 4.000 | árvores 70 %, arbustos 50 % |
| high | cada amostra (2 m na maioria dos mapas terrestres) | a cada 2ª | 1 m (no máximo 4096 pixels por lado) | 4,5 M | 12.000 | todas |

Os dois anéis do mapa de tanques são limitados a 0,3 M (low), 1 M (medium) e 3,7 M
(high) triângulos: nos mapas cujo mapa de altura é mais fino que 2 m, os passos
dobram (o anel externo primeiro) até caber, então esses saem com cerca de 2 m também.

Um mapa terrestre em `high` sai com cerca de 8 milhões de triângulos (3,5 M de
terreno, 4,5 M de objetos) e 250 MB; em `medium`, cerca de 4,5 M. Os LODs dos objetos
são os que o próprio jogo desenharia a partir de uma distância de visão, o mais curto
cujo total cabe no orçamento: adereços pequenos caem primeiro para LODs grosseiros e
construções grandes por último, pelas faixas de distância que os autores deram a cada
LOD (`lodDistance` no JSON); o que esse passo economiza além do orçamento volta para
os maiores objetos. A cor grosseira do chão (mapas aéreos) primeiro faz a média das
texturas em mosaico de cada classe de terreno até o tamanho do pixel, para que os
mosaicos não criem padrão de interferência (moiré). Se nem os LODs mais grosseiros
couberem, as árvores que mais economizam viram copas, e então os tipos menores são
deixados de fora (`leftOut`); nenhum objeto é desenhado como caixa (uma forma de
colisão, se houver, é a do próprio objeto).
Objetos gerados são rarefeitos de modo determinístico por tipo (`density`), sempre os
mesmos a cada execução. `--max-object-triangles` troca o orçamento, `--max-grid`
(padrão 1024) limita as partes mais grosseiras do mapa de altura, `--no-objects` deixa
os objetos de fora, `--no-generated` os gerados, `--no-terrain-colour` texturiza o
chão com o mapa tático, `--no-texture` deixa o chão sem textura.

O `parts.objects` do JSON lista as instâncias (fixas e geradas, por tipo e classe de
terreno), quantas foram desenhadas em qual LOD (`drawnAs`), os triângulos, a distância
do LOD e os segundos; `parts.heightmap.rings` o passo e os triângulos de cada anel do
terreno; `parts.terrainColour` as classes de terreno e suas cores, estradas e
decalques do chão; `trianglesTotal`, `glbBytes` e `secondsBy` os totais.

## O que é lido, e com que qualidade {#what-is-read-and-how-well}

| Parte | Situação |
|---|---|
| Binário do nível (`levels/<level>.bin`, `DBLD` 3x64): tabela de blocos | cada nível verificado |
| Mapa de altura (`HM2`, versões 0-2; a versão 2 são valores de 8 bits em blocos, em pedaços Oodle ou zstd) | cada nível cujo mapa de altura é a versão 2 com pedaços Oodle; conferido a olho contra os mapas táticos (rios, vales, costas e cidades coincidem) |
| Colisão da malha do terreno (`lmap`, seu traçador de raios `LTdump`) | lida onde o nível tem uma (empacotada em Oodle). É a superfície de colisão do jogo, não a malha desenhada, então é mais grosseira onde o terreno é plano |
| Cor do chão (classes de terreno e mapa de pesos de `lmap`, mapa de física `LMp2`, splines `hspl`) | os mapas de cor das classes de terreno e as texturas de detalhe (suas cores médias) ponderados pelo mapa de pesos, o índice de bioma de 1 m das classes de terreno indexadas, as formas de estradas e decalques do chão do mapa de física na cor da textura da sua spline ou material, penhascos em encostas íngremes. Conferido contra os mapas de tanques: estradas, cidades, lagos, faixas de floresta e afloramentos rochosos coincidem. A fórmula de cor do shader de terreno do próprio War Thunder não está no código-fonte público; usa-se a publicada pelo motor (daNetGame), que sai mais saturada que o mapa tático |
| Nível da água | `water_level` do BLK do nível em `aces.vromfs.bin` (0 onde não há) |
| Mapa de altura da água (`WHM`: uma grade de células planas e páginas de 130x130 com alturas de 16 bits) | lido onde o nível tem um; seus rios inclinam com o terreno |
| Mapas táticos | de `content/base/res/locations_maps.dxp.bin`, posicionados por `mapCoord0/1` e `tankMapCoord0/1` do BLK; o topo da imagem é o norte |
| Objetos colocados (`RIGz`: as instâncias fixas do gerador de instâncias de render) | cada instância, como uma matriz 3x4 de valores de 16 bits ou, em alguns níveis, de 32 bits (o número de bytes da célula decide); cada byte de cada célula contabilizado nos níveis verificados |
| Objetos gerados (máscaras de classe de terreno do `RIGz` e recursos `LandClass`) | o gerador do jogo, portado: os mesmos pontos tentados na mesma ordem com os mesmos números aleatórios, as máscaras de classe de terreno e de exclusão, o objeto escolhido em cada ponto, sua rotação, escala e deslocamento de altura; entidades em mosaico (quarteirões de cidade) e plantadas (florestas, arbustos, campos). Gerados só sobre o mapa de tanques. Aproximados: a altura e a normal do chão (do mapa de altura; o jogo traça um raio), as caixas de exclusão que o jogo registra em tempo de execução, e o giro das árvores (o jogo o alinha à paleta de rotações do impostor). |
| Malhas de renderização (recursos `RendInst` em `content/*/res/*.grp`, materiais em `riDesc.bin`) | os vértices e triângulos de cada LOD (posições em float; índices de 16 ou 32 bits, simples ou empacotados por meshoptimizer), o material de cada elemento. Elementos de decalque e de billboard de impostor ficam de fora; os transparentes (vidro) são mantidos |
| Cores dos objetos | por material, a média do pequeno mip da sua textura difusa (ponderada pelo alfa nas folhas), dos pacotes de texturas da instalação: t0 para a maioria dos shaders, a primeira difusa de detalhe onde t0 é uma sobreposição ou uma máscara. Uma cor por material: sem textura nos objetos |
| Formas de colisão (`<object>_collision`) | recursos de colisão de versão de fluxo 3, usados onde um objeto não tem malha de renderização. Só se desenha o que os raios do jogo atingem (nós `TRACEABLE`), e caixas, esferas e cápsulas só quando o recurso não tem malha: o resto são aproximações físicas grosseiras que apareceriam como cubos em volta do objeto |
| Malha de navegação (`Lnav`), a malha de terreno renderizada, grama, `spgz`, `stbl`, `d2co` | não lidos |

Os níveis são comprimidos com Oodle, que é proprietário. O jogo traz uma cópia,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (uma compilação x64 comum), e é ela
que é carregada; `HEAT3D_OODLE=<dll ou pasta>` aponta para outra. Nada do Oodle está
incluído aqui.

## Formatos, e onde são documentados {#formats-and-where-they-are-documented}

A Gaijin publicou o código-fonte do Dagor Engine sob a licença BSD 3-Clause
(github.com/GaijinEntertainment/DagorEngine). Os leitores daqui foram escritos a
partir dele; nenhum código do jogo foi descompilado. Cada módulo cita os arquivos de
origem que segue:

- `vromfs.py`: `*.vromfs.bin` (cabeçalho `VRFs`/`VRFx`, um corpo zstd cujos primeiros
  e últimos 16 bytes são combinados por XOR com uma chave fixa, uma tabela de nomes e
  uma tabela de deslocamentos: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) e BLK binário (formas 1-5, com o mapa de nomes
  compartilhado do arquivo `\xff?nm` e o dicionário zstd: `ioSys/dataBlock/blk_serialize.cpp`,
  `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: pacotes de texturas `DxP2` (`lib3d/texPackMgr2.cpp`) e cabeçalhos DDSx
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 são decodificados pelo Pillow.
- `dagorlevel.py`: o binário do nível (`scene/loadLevel.cpp`), o mapa de altura
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), o
  traçador de raios do terreno (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) e o mapa de altura da água (`fftWater/fftWater.cpp`).
- `rigen.py`: os objetos colocados (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: os objetos gerados (`rendInst/rendInstGenLand.cpp`,
  `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`,
  `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`,
  `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`,
  `gameRes/grpData.h`).
- `rendinst.py`: instâncias de renderização (`shaders/rendInstRes.cpp`,
  `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`,
  `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) e o codec de índices do
  meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: a cor do chão (`landMesh/lmeshManager.cpp`,
  `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`,
  `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: pacotes de recursos (`gameRes/grpData.h`) e recursos de colisão
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  cujos triângulos são guardados como uma BVH de quads (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) lê os mesmos arquivos; não é necessário e não é usado.

---

Parte do [3DHeat](https://github.com/Holdi601/3DHeat) ([documentação](https://holdi601.github.io/3DHeat/)). Código: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
