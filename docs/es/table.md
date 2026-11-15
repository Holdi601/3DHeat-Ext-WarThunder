---
title: La tabla
nav_order: 6
lang: es
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# La tabla {#the-table}

![La tabla de una repetición sintética, resumida](../assets/img/table.svg)

Una fila por muestra o evento, 105 columnas ([Lista de columnas](../columns.md), generada a partir del código); en el pie, bajo `heat3d`, las
instrucciones de lectura del visor, así que el visor no necesita que se rellene ningún formulario.

| Columna | Qué es |
|---|---|
| `time` | segundos según el reloj propio de la repetición |
| `event` | `position`; las filas de evento están sobre la trayectoria en su momento (entre dos muestras, sobre la línea que las une); `kill` (en el asesino), `death` (en la víctima), `hit_critical` / `hit_severe` (en la unidad alcanzada), `module_destroyed` (en la unidad), `launch` (en la unidad que soltó un arma), `impact` (la última muestra de un arma cuando se retiró justo después); `explosion` y `flak` (0xD08E, 0xD01F) en su posición, tipo `effect`, sin trayectoria, con la dirección de la explosión cuando la tiene; `shot` (un proyectil que alcanzó, en el tirador), `gun_shot`, `fire_start`, `fire_stop` (una ráfaga de cañón, no un vehículo en llamas), `fire_on`, `fire_off` (un vehículo en llamas, véase [Incendios de vehículos](hits.md#vehicle-fires)), `reward` (Leones de Plata y puntos de investigación ganados, véase [Economía](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (véase [Mensajes a las unidades](how-it-reads.md#messages-to-units)); `despawn`: la última fila de una trayectoria cuya unidad desaparece antes de que acabe la repetición (véase [Final de una trayectoria](ground.md#end-of-a-track)) |
| `track` | lo que el visor dibuja como una sola cosa: una vida de una unidad, o el vuelo de un arma - `<jugador o vehículo> #<hex>` (el visor muestra el nombre sin la parte `#`) |
| `x`, `y`, `z` | metros del juego: x hacia el este, y hacia arriba, z hacia el norte (las pistas invierten z, así que el norte no se dibuja hacia el sur) |
| `player` | el nombre del jugador; una unidad de IA `<NombreVehículo> #<uid>` (por ejemplo `F-15A #204`); `uid <n>` cuando nada la nombra; para un arma, quién la soltó |
| `userId`, `team` | el id de Gaijin del jugador y el equipo (`1`, `2`) |
| `ai`, `isPlayer` | `ai` es verdadero para cada unidad que no conduce ninguna cuenta de jugador (unidades de misión, aviones de IA, objetivos terrestres, cañones antiaéreos, barcos sin jugador, marcadores), `isPlayer` es lo contrario: un jugador es una unidad cuya entidad nombra una ranura de jugador con un id de Gaijin. Un arma tiene el de quien la lanzó; vacío cuando no se sabe |
| `match` | el id de la partida (el `match` del documento de la partida), en cada fila; las pistas lo asocian como sesión, así que dos repeticiones cargadas nunca unen trayectorias |
| `life` | `uid#n`: la trayectoria de una unidad, cortada donde el uid pasa a otra unidad, la unidad se mueve más rápido de lo que puede (una reaparición, un rearme, el juego que la mueve, el cliente que corrige una unidad lejana; véase Teletransportes en [Cómo lee una repetición](how-it-reads.md#what-is-read-and-the-check)) o lleva mucho sin verse; `w<hex>` el vuelo de un arma (`w<hex>#n` tras un corte) |
| `uid` | el id de la unidad en la repetición |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (un tranvía o vagón de tren que coloca el nivel, véase [Unidades de escena](objectives.md#scene-units-trams-and-rail-wagons)); armas `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` la cámara de repetición del jugador que graba (véase [La cámara](ground.md#the-camera)) |
| `type` | el tipo propio del juego cuando los resultados lo indican (`fighter`, `assault`, `destroyer`, `gun_boat`), si no, como `kind` |
| `Vehicle` | el id de vehículo del juego (`f_15a`, `germ_flakpz_I_Gepard`), con el que coinciden las figuras del visor |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | el nombre en inglés del vehículo según la localización de tu instalación (`Pz.Kpfw. III Ausf. J1`, corto `Pz.III J1`) y su clave (`germ_pzkpfw_III_ausf_J_0`); se omiten las marcas de país de la fuente del juego. Cuando el juego no lo nombra, o no se encuentra ninguna instalación, el nombre es el id y la clave queda vacía |
| `mission` | el nombre de la unidad en la misión (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | hacia dónde apunta la unidad (el vector de mirada): los aviones desde la actitud del modelo de vuelo, las unidades terrestres y los barcos desde la suya, las armas a lo largo de su vuelo |
| `heading`, `pitch`, `roll` | lo mismo en grados; el rumbo es la brújula, en sentido horario desde el norte, el cabeceo positivo con la nariz arriba, el balanceo positivo con el ala derecha abajo (el modelo de vuelo envía el signo contrario, véase [Actitud, comprobada](aircraft.md#attitude-checked); en una unidad terrestre, el lado derecho abajo). Las pistas lo indican bajo `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | la torreta principal de un tanque - hacia dónde apunta el cañón, no hacia donde mira su jugador; el valor de la repetición limitado a la velocidad del motor de la torreta y ajustado a la línea de cada disparo del cañón principal (véase [Torretas](ground.md#turrets)): su giro respecto al casco (grados, positivo en sentido horario visto desde arriba, 0 hacia delante) y la elevación de su cañón respecto al casco (grados, positivo hacia arriba); `turrets` cada torreta del vehículo como `giro elevación;giro elevación;...` en su propio orden (una ranura no usada muestra `0.00 0.00`). Tanques, SPAA, APC y camiones, en repeticiones de cliente y de servidor; no barcos (véase [Torretas](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | la torreta principal tal como la envía la repetición; `turretYaw` / `gunPitch` son esos valores limitados a la velocidad del motor de la torreta y ajustados a la línea de cada disparo del cañón principal (véase [Torretas](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | hacia dónde mira el jugador (apunta con la cámara) en el mundo: grados de brújula (0 norte, sentido horario) y grados hacia arriba, la misma convención que `aimHeading` / `aimPitch` (a diferencia de `turretYaw` / `gunPitch`, que siguen siendo relativos al casco). El tanque de cada jugador en una repetición de servidor, el del jugador que graba en una repetición de cliente; vacío cuando el jugador no apunta a ningún sitio (los cuatro flotantes de apuntado valen 0). La torreta lo sigue a su propia velocidad de giro, así que los dos difieren mientras gira (véase [Torretas](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | el tanque propio del jugador que graba: hacia dónde apunta (grados de brújula, grados hacia arriba, la distancia en m; 2000 cuando no hay nada en la mira); filas de cámara: hacia dónde apunta el jugador (rumbo, cabeceo) |
| `zoom` | filas de cámara: el aumento de la cámara (véase [La cámara](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` o `SB` de la batalla, y `ground`, `air` o `naval`, en cada fila (véase [Modo de batalla](ground.md#battle-mode)) |
| `extrapolated` | una muestra de avión que es la estimación por navegación del cliente, no un estado recibido (véase [Estimación por navegación](aircraft.md#dead-reckoning-and-the-smoother)); una muestra de bomba calculada a partir de su suelta (véase Bombas sin registros de vuelo en [Cómo lee una repetición](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | cuánto movió el suavizador la muestra (m), y la posición y actitud propias de la repetición (balanceo con el signo de la tabla) |
| `targetX`, `targetY`, `targetZ` | el punto de impacto de un `shot` |
| `hitOutcome`, `hitFlags` | el resultado de un `shot` sobre una unidad terrestre: `kill`, `critical`, `penetration` o `nonpenetration` (rebotado o detenido: la repetición no distingue un rebote), a partir de los bits que el servidor envía con el impacto (`hitFlags`, en bruto); vacío cuando no se envía ninguno (aviones, barcos). Véase [Resultados de impacto](hits.md#hit-outcomes) |
| `hitShell` | la firma de proyectil de un `shot`: cuatro bytes del mensaje de impacto (hex en bruto); una misma firma puede corresponder a distintos proyectiles (los APFSDS de 120 y 125 mm comparten una), por eso se guarda en bruto y no se interpreta como calibre |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | la munición de un `shot`: su tipo (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) y su id (`125mm_3bm46`) cuando una baja nombra la ranura del tirador; si no, `explosive` (la explosión del impacto) o `kinetic`; el `weapon/slot` del cañón según sus recargas; el calibre en mm según los archivos de armas de la instalación. Véase [Resultados de impacto](hits.md#hit-outcomes) |
| `rpm` | las revoluciones del motor de un avión (la media de sus motores) tal como se enviaron por última vez, con un margen de 2 s |
| `vx`, `vy`, `vz` | la velocidad de un avión tal como la envía su entrada de vuelo (m/s, los ejes del juego; las velocidades por encima de 500 m/s se leen como 500) |
| `engine`, `afterburner`, `engineCondition` | los motores de un avión según su entrada de vuelo: `off`, `starting`, `running`, `dead` (separados por `/` cuando sus motores difieren); la postcombustión de 0 a 1; un byte que se envía solo después de que el motor fuera alcanzado |
| `weaponName` | bajas y muertes: el arma o munición en inglés según tu instalación (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | solo el avión del jugador que graba: el acelerador de 0 a 1.1 desde su cabina (1.1 potencia de emergencia o postcombustión; si no, las quinceavas partes de su entrada de vuelo), los mandos de -1 a 1 según su entrada de vuelo (elevador positivo tirando hacia arriba, alerón positivo girando a la derecha), los proyectiles que quedan por arma (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | solo el avión del jugador que graba, desde su cabina: velocidad indicada y velocidad de ascenso (m/s), combustible, presión del colector (atm), tren (0-1, 1 extendido), temperatura del aceite y de la culata, cuando la cabina tiene ese indicador |
| `speed` | m/s sobre unos dos segundos de la trayectoria (calculado aquí; la repetición no envía velocidad de las demás unidades) |
| `alive` | 0 para las muestras de una unidad tras su muerte (sus restos): las de una unidad terrestre o barco hasta que el juego la quita o acaban sus muestras, las de un avión durante 60 s como máximo |
| `otherVehicle`, `otherLife` | la víctima de un `shot`: su vehículo y su `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | el punto de impacto de un `shot` en el propio sistema de la víctima (m; x adelante, y arriba, z izquierda; véase [Mensajes a las unidades](how-it-reads.md#messages-to-units)) y la dirección de llegada del disparo, convertida a ese sistema según la actitud de la víctima en ese momento |
| `hitPart`, `hitFlag` | el mensaje de impacto de un `shot`: su palabra de parte tal como se envió, y su byte alto |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | lo que costó y ganó la batalla, y quién ganó: véase [Economía](economy.md) |
| `other`, `weapon` | bajas: el otro bando y el arma; impactos: quién alcanzó (del uid del registro, o si no de la ranura del jugador), su vehículo; lanzamientos: el arma; módulos destruidos: quién alcanzó por última vez a la unidad en los 5 s anteriores, y `part <n>` |

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
