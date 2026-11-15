---
title: Convertir repeticiones
nav_order: 4
lang: "es"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Convertir repeticiones {#converting-replays}

Salida: un archivo `.3dheat` por batalla (por defecto), o archivos sueltos con
`--loose`.

## Paso a paso {#step-by-step}

1. **Activa las repeticiones.** War Thunder guarda las repeticiones de cliente en la
   carpeta `Replays` del juego cuando el guardado de repeticiones está activado en sus
   opciones, por ejemplo
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   También se puede convertir una repetición de servidor guardada desde la página de
   repeticiones del juego (un zip con `0000.wrpl`,
   `0001.wrpl`, ...).
2. **Abre una terminal** en una carpeta donde puedan ir los resultados
   ([Antes de empezar](before-you-start.md)).
3. **Convierte:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # archivos, carpetas, o ambos
   heat3d-wt-replay battle.zip -o out              # el zip de una repetición de servidor
   heat3d-wt-replay a.wrpl -o out --loose          # archivos separados en lugar de un .3dheat
   ```

   `out` se crea en la carpeta donde está tu terminal.
4. **Lee lo que dice.** Deberías ver una línea por batalla.
5. **Ábrelo:** carga `out/<mapa>/<partida>.3dheat` en el visor de 3DHeat
   ([Cargar uno](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Una ejecución con una repetición sintética: un .3dheat, --loose, un archivo roto, una carpeta vacía](../assets/img/convert.svg)

La imagen es una ejecución sobre una repetición que las pruebas construyen en código
(sin repetición real y sin instalación):

- `ok <archivo>`: una batalla convertida (con `--loose`: `ok <tabla> <documento de la partida>`);
- `failed <archivo>: <motivo>`: un archivo que no se pudo leer (estado de salida 1; las
  demás se siguen convirtiendo);
- `no .wrpl files given`: nada que convertir (estado de salida 2);
- `note: ...`: por ejemplo, que no se encontró ninguna instalación de War Thunder para
  dar nombre a los vehículos.

## Opciones {#options}

| Opción | Por defecto | Qué hace |
|---|---|---|
| `replays` (una o más) | - | archivos `.wrpl`, carpetas con ellos (la carpeta en sí, no sus subcarpetas), o zips de ellos (una repetición de servidor: sus partes `.wrpl` se descomprimen en una carpeta temporal) |
| `-o`, `--out` | obligatoria | dónde escribir: una carpeta por mapa dentro |
| `--game CARPETA` | encontrada | la carpeta de War Thunder cuyos textos dan nombre a vehículos, armas y munición, y cuyas tablas fijan los precios de la [economía](economy.md); también `HEAT3D_WT_GAME` |
| `--no-smoothing` | desactivada | conserva las muestras de estimación por navegación y las recibidas de otras unidades tal como están en la repetición ([Estimación por navegación](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | activada | empaqueta cada batalla en un archivo `.3dheat` |
| `--loose` | desactivada | guarda cada batalla como archivos separados (tabla, documento de la partida, archivos auxiliares) |
| `--version` | - | muestra `heat3d-wt-replay <versión>` y termina |
| `-h`, `--help` | - | muestra las opciones y termina |

Una batalla convertida otra vez se escribe de nuevo. Las opciones tal como las
muestra el programa: [Referencia de comandos](../cli-reference.md).

## Qué archivos son una batalla {#which-files-are-one-battle}

Cada batalla se convierte en un archivo
`out/<mapa>/<mapa>_<AB|RB|SB>_<modo>_<inicio, UTC>_<id de sesión>.3dheat`. AB, RB
y SB son las formas cortas que usa el juego para batallas arcade, realistas y de
simulador; `<modo>` es el modo de la misión tal como lo nombra el juego (`Conq4`
Conquista n.º 4, `Dom` Dominio, `Bttl` Batalla; véase
[Modo de batalla](ground.md#battle-mode)); cualquiera de las dos partes se omite
cuando la repetición no la indica. Las partes de una repetición de servidor
(`0000.wrpl`, `0001.wrpl`, ...) se leen juntas como una sola batalla; una
repetición de cliente y las partes del servidor de la misma batalla son dos
grabaciones y se quedan como dos.

## Estado de salida {#exit-status}

`0` cuando se convirtieron todas las batallas, `1` cuando alguna falló (las demás
se siguen convirtiendo), `2` cuando no se encontró ningún archivo de repetición entre
los argumentos.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
