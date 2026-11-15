---
title: Instalación
nav_order: 3
lang: es
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalación {#installing}

¿Es tu primera vez con la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).
Necesita Python 3.10 o posterior; pyarrow, numpy, zstandard y Pillow se instalan con él.

## Paso a paso {#step-by-step}

1. Consigue el código: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   o descarga un zip desde [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   y descomprímelo.
2. Abre una terminal en esa carpeta y escribe `pip install -e .`. Esto instala
   dos comandos: `heat3d-wt-replay` (repeticiones) y `heat3d-wt-level` (niveles).
3. Compruébalo: `heat3d-wt-replay --version`. Deberías ver
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` muestra las opciones:

![heat3d-wt-replay --help](../assets/img/help.svg)

Sin instalar: `python -m heat3d_ext_warthunder ...` y
`python -m heat3d_ext_warthunder.levelcli ...` en la carpeta de la herramienta.

## Nombres de tu instalación {#names-from-your-install}

Los vehículos, armas y munición reciben sus nombres en inglés de los archivos de
texto del propio juego, que se leen de tu instalación al convertir. La instalación
se busca a través de Steam o de las carpetas predeterminadas del lanzador;
`--game <carpeta>` o la variable de entorno `HEAT3D_WT_GAME` indican dónde está si no
la encuentra. El texto del juego no está en este repositorio; sin instalación, los
nombres son los identificadores de los vehículos (el convertidor lo indica con una
línea `note:`).

## Actualizaciones {#updates}

Cada inicio consulta antes las versiones publicadas del proyecto en GitHub (como
mucho una petición cada pocas horas; nunca detiene una conversión, con o sin
conexión). Cuando hay una versión nueva, el comando pregunta antes de instalarla:
un `git clone` se actualiza con `git pull --ff-only` (rechazado si tienes cambios
locales), y una copia descargada, desde el archivo de la versión. `HEAT3D_NO_UPDATE=1`
desactiva la consulta y la actualización.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
