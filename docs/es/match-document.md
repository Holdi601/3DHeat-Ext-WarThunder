---
title: "El documento de la partida"
nav_order: 7
lang: "es"
source: match-document.md
source_hash: "3bd1f4245ad0"
nav_exclude: true
search_exclude: true
---
# El documento de la partida {#the-match-document}

![El inicio de un documento de la partida sintético, y sus claves](../assets/img/match-document.svg)

`<partida>.match.json` contiene todo lo que dice la repetición y que no es una fila de
la tabla. La pestaña Partida del visor lo lee.

## La batalla {#the-battle}

| Clave | Qué es |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | el id de la partida (como en el nombre del archivo); el id del mapa; el archivo de nivel que usa |
| `mission`, `missionKey` | el nombre de la misión y su clave en los archivos de texto del juego |
| `battleClass`, `environment`, `weather` | tal como los da el encabezado |
| `sessionId`, `server` | el id de sesión de la batalla; el servidor |
| `replayVersion`, `flightLayout` | la versión del formato de repetición; la disposición de los paquetes de vuelo leída (`2025` o `2026`) |
| `files` | los archivos de repetición leídos (uno, o las partes de una repetición de servidor) |
| `started`, `timePlayed`, `replayEnd` | hora de inicio (ISO, UTC); segundos jugados, según los resultados; segundos del último paquete de la repetición |
| `author`, `authorUserId` | el jugador que graba y su id de Gaijin (repeticiones de cliente) |
| `teams` | los equipos de la batalla (`1`, `2`) |
| `result` | `winner`, `source` (`results.status` o `tickets`), `status` (`success` o `fail`, el resultado del autor), `authorTeam`, `teams`, `endReason` (`destruction`, `capture`, `tickets`, `time`) ([Economía](economy.md)) |
| `vehicleNames` | de dónde salieron los nombres de los vehículos (tu instalación) y su idioma |
| `conventions` | las unidades y signos de la tabla: ejes, tiempo, vida, trayectoria, vivo, balanceo, y más |

## Todo lo demás {#everything-else}

| Clave | Qué es |
|---|---|
| `battle`, `difficulty`, `gameMode` | el modo de batalla: `difficulty` `AB` / `RB` / `SB` (y su nombre, y el byte del encabezado), `gameMode` `ground` / `air` / `naval`, el modo de la misión (`Dom`, `Conq`, `Bttl`, `I2M`, ...) y su nombre en inglés según tu instalación (`Domination`, `Enduring Confrontation`), los tipos de unidad permitidos (véase [Modo de batalla](ground.md#battle-mode)) |
| `settings` | el bloque de la misión tras el encabezado: modo, entorno, clima, límites de puntuación y de tiempo, países, tipos de unidad permitidos, viento, y `stars` (latitud, longitud, fecha, hora local) |
| `sky` | el primer `CustomWeatherParams`: dirección del sol y la luna, viento, colores del cielo, desplazamientos de las nubes |
| `players`, `slots` | la línea de los resultados por jugador (bajas, bajas terrestres, muertes, asistencias, puntuación, capturas, escuadra, clan, país, alineación, los uid que condujeron); las ranuras de jugador de la repetición (nombre, id de usuario, equipo) |
| `units` | cada entidad de unidad que creó la repetición: eid, uid, plantilla, vehículo, tipo, equipo, jugador, nombre en la misión, cuándo se creó y se quitó, dónde se creó, qué componentes no se pudieron leer |
| `objects` | los objetos con nombre de la misión: zonas de captura y aeródromos con su posición y tamaño, los contornos de los aeródromos como puntos, zonas de aparición |
| `objectives` | los objetivos de la batalla, cada uno con su `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (el 1 o 2 de la repetición, vacío para ambos), `name` (en una zona de captura su letra, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) con `position`, `radius` / `height` / `size` y `heading`, `source` (`replay` o `mission`) y lo demás que se sabe (véase [Objetivos](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | con nombres y vehículos de ambos bandos; las bajas con el nombre en inglés del arma |
| `weapons` | cada cohete, misil, bomba, torpedo, depósito auxiliar y carga soltada: cuándo, dónde se soltó (posición, actitud, velocidad), por qué unidad (la más cercana en 300 m y 1,5 s), cuántas muestras de vuelo, dónde se vio por última vez, cuándo se quitó |
| `explosions`, `flak` | `PlayExplosionVisual` (posición, dirección, tipo) y `PlayFlakExplosionVisual` (posición) |
| `awards` | las condecoraciones del jugador que graba (`TextStreak`: first_blood, rachas, contadores de desafíos) |
| `detections`, `unitStates` | parejas `UnitDetected` de unidades; un mensaje (0xF093) con la posición, actitud y velocidad de una unidad cuyo significado no se conoce |
| `authorInstruments` | los valores de cabina del jugador que graba (`ReplayCockpitParams`) por número de instrumento, como máximo uno por segundo; `known` nombra cada número que envió esta repetición (nombre, unidad, cómo se comprobó), `notNamed` el resto |
| `scoreboard` | las estadísticas de cada jugador cada vez que cambiaron (bajas, muertes, asistencias, puntuación, bajas de IA, bajas navales, zonas, daño, evasiones de misiles, escuadra), y la puntuación y los tickets probables de cada equipo a lo largo del tiempo (véase [Datos de reflexión](aircraft.md#reflection-data)) |
| `economy` | los Leones de Plata y puntos de investigación de la batalla (véase [Economía](economy.md)): totales, por jugador, por vehículo, los multiplicadores, el ganador, las comprobaciones |
| `entityMessages` | los mensajes de entidad (0x20) por número de clase: recuento, plantillas de destino, tamaños |
| `chat` | cada línea del chat |
| `triggers`, `hints`, `missionProgress` | las acciones del guion de la misión (RunTriggerAction), sus pistas, sus mensajes de progreso |
| `camera` | los campos de la cámara de repetición del jugador que graba cada 0,25 s tal como se enviaron (la tabla los tiene como trayectoria) |
| `projectileHitReplays` | los impactos propios del jugador que graba y los que recibió, con arma y munición y sus nombres en inglés |
| `results` | el bloque completo de resultados tal como lo escribió el juego |
| `counts` | filas, eventos, vidas, tipos, muestras, entidades por plantilla, armas, paquetes leídos y no leídos, cada id de mensaje visto y los no leídos, muestras descartadas |
| `trackBreaks` | cada corte de una trayectoria por un paso más rápido de lo que puede ir la unidad: dónde, cuánto, a qué velocidad, y lo que es más probable |
| `selfCheck` | las comprobaciones listadas en [Cómo lee una repetición](how-it-reads.md), calculadas en cada conversión; `stepSpeed` da por tipo la velocidad entre filas consecutivas de una trayectoria tal como las une el visor (mediana, percentil 99, máxima, y los pasos más rápidos de lo posible, que deben ser 0) |

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
