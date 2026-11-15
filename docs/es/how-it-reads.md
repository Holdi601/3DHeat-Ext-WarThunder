---
title: Cómo lee una repetición
nav_order: 10
lang: es
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Cómo lee una repetición {#how-it-reads-a-replay}

Esta página es para quien quiere saber qué lee el convertidor, cómo se comprobó,
y así cuánto confiar en cada columna. No hace falta para convertir repeticiones.

La lectura se comprobó con repeticiones de cliente de batallas arcade aéreas, de simulador
aéreo y navales, con repeticiones de servidor de batallas terrestres y, para
las disposiciones de 2025, con las repeticiones de muestra públicas de
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Cada comprobación compara un valor con algo que la repetición dice de una segunda
forma, independiente; aquí solo se dan el método y la coincidencia.

## Qué se lee, y la comprobación {#what-is-read-and-the-check}

| Parte | Estado, y la comprobación |
|---|---|
| Cabecera, mapa, misión, hora de inicio, sesión; resultados | cada archivo |
| Ajustes de la misión (el blk tras la cabecera) | modo, clima, límites, `stars` (fecha, hora, lugar) |
| Flujo de paquetes (zlib en 2025, zstd en 2026) | cada paquete enmarcado |
| Posiciones y actitud de los aviones (disposición de 2026) | 4 muestras por segundo, ningún paquete sin leer; el rumbo coincide con la dirección de avance |
| Paquetes de vuelo adelantados respecto a su momento | tras un tirón de red, el paquete de vuelo de una repetición de cliente a veces sitúa a todos los demás aviones donde estarán unos 0,75 s después. El adelanto se mide por paquete, y a cada avión que va delante se le asigna el instante que representa (`selfCheck.flightPacketsRetimed`) |
| Saltos de estimación por navegación | un salto dentro de un tramo estimado por navegación se mide desde el último estado recibido, así que las correcciones del cliente ya no cortan las trayectorias ([Estimación por navegación](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teletransportes | una trayectoria se corta donde su unidad se mueve más lejos de lo que puede: primero según su tipo (avión 750 m/s, terrestre y barcos 40 m/s, armas 1800 m/s), luego según su propio ritmo. Cada corte aparece en `trackBreaks` con su causa probable (reaparición, el juego moviendo al jugador, una corrección de una unidad lejana). Tras los cortes, ningún paso entre filas de una trayectoria es más rápido de lo que permite su tipo (`selfCheck.stepSpeed`) |
| Posiciones de unidades terrestres y barcos (0xF073 / 0xF074) | ningún paquete sin leer. Rumbo, cabeceo y balanceo a partir de la actitud de 16 bits: el rumbo coincide con la dirección de avance a unos 2 grados (mediana); el cabeceo cuenta 180/65536 grados por paso; con el signo del balanceo invertido, la dirección del cañón desde el casco y la torreta apunta a la unidad alcanzada en casi todos los disparos de tanque. Los barcos se sitúan al nivel del agua |
| Torretas | giro de la torreta y elevación del cañón de los tanques: véase [Torretas](ground.md#turrets) |
| Alturas del suelo empaquetadas | las posiciones empaquetadas en 64 bits cuentan su altura desde -100 m en la mayoría de los niveles y desde el nivel del agua en algunos; el desplazamiento se mide en cada repetición con unidades vistas en ambas formas (`selfCheck.packedGroundHeight`) |
| Flujo de entidades (creación, destrucción) | cada creación leída. La disposición viene del código fuente publicado del Dagor Engine; los tipos de componente propios de War Thunder se saltan encontrando dónde empieza el siguiente componente. La ranura de vehículo y de jugador de cada unidad coincide con las que nombran los registros de bajas e impactos, en cada registro comprobado |
| Quién condujo qué unidad, unidades de IA, barcos, objetivos terrestres | del flujo de entidades: cada unidad tiene su vehículo y equipo, y la unidad de cada jugador su jugador |
| Bajas frente a los resultados | las muertes por jugador son iguales a las de los resultados; los resultados cuentan más bajas, porque al cliente no se le envía cada baja. Una repetición que empieza tras el inicio de la batalla solo contiene las bajas posteriores |
| Bajas, impactos críticos, daño grave | cada archivo |
| Módulos destruidos (0xF118) | la unidad y el número de la parte; el nombre de la parte necesita el modelo de daño del vehículo, que no está en la repetición |
| Armas soltadas (flujo de entidades) | el punto de suelta está a unos 10-20 m (mediana) de la unidad más cercana, que se toma como lanzador |
| Armas en vuelo (0xF0DB) | misiles, cohetes y bombas, cada uno ligado a su entidad |
| Bombas sin registros de vuelo | una bomba sin ellos recibe su caída calculada desde la suelta hasta el impacto (gravedad y arrastre, una muestra cada 0,1 s, `extrapolated` verdadero). Comprobado sobre el mar, donde se conoce la altura del impacto: las caídas calculadas terminan a unos 15 m del agua. En el documento de la partida, esa arma tiene `ballisticImpact`; `counts.bombsBallistic` las cuenta |
| Ranuras de jugador, chat | cada archivo |
| Explosiones, estallidos antiaéreos, condecoraciones, detecciones, clima, objetos de misión | leídos; posiciones comprobadas a ojo en el visor |
| Instrumentos del jugador que graba (0xD04A) | nombrados por lo que hacen: [Instrumentos de cabina](aircraft.md#cockpit-instruments); el resto en `notNamed` |
| Otros campos de las entradas de vuelo | velocidad, proyectiles, mandos, motores: [Entradas de vuelo](aircraft.md#flight-entries) |
| Actitud de las filas de evento | cada fila de evento lleva el rumbo, cabeceo, balanceo y vector de mirada de su unidad en ese momento |
| Estadísticas de jugador y puntuaciones de equipo | al final de la batalla, cada estadística es igual a la de los resultados para cada jugador: [Datos de reflexión](aircraft.md#reflection-data) |
| Nombres de armas y vehículos | de la localización en inglés de tu instalación; algunos cinturones por defecto de barcos y radares de aeródromos no tienen nombre en el juego |
| Jugadores y IA | ninguna fila de un jugador de los resultados es IA, cada fila que no es IA es de un jugador de los resultados (`selfCheck.identity`) |
| Restos | las muestras de una unidad tras su muerte siguen llegando; el resto de una unidad terrestre o barco es `alive` 0 hasta que se quita su entidad, y sigue siendo una sola trayectoria; los aviones mantienen `alive` 0 durante 60 s como máximo (`selfCheck.wrecks`) |
| Cambios de vehículo | una unidad del jugador aún viva cuando aparece la siguiente unidad del mismo jugador termina ahí (un vehículo abandonado en pie). `selfCheck.vehicleSwitch.twoLiveVehicles` debe ser 0 |
| Modo de batalla | [Modo de batalla](ground.md#battle-mode) |
| Aviones en una repetición de servidor de 2026 | leídos en la disposición de 2026; el rumbo y el signo del balanceo coinciden con los giros; los aviones de marcador y los drones de reconocimiento no llevan datos |
| Jugadores de una repetición de servidor | encontrados por nombre en las ranuras; cada estadística es igual a la de los resultados (`selfCheck.players`) |
| Aviones en repeticiones de servidor de 2025 y versión 101286 | no leídos: sus paquetes de vuelo tienen otra disposición |

## Mensajes a las unidades {#messages-to-units}

Cada paquete de tipo 4 es un mensaje mpi del daNet del Dagor Engine: el id del objeto
destinatario, luego (cuando sus 11 bits bajos son todos 1) el UID extendido del objeto, el id
del mensaje y la carga. Un mensaje a una unidad lleva como UID extendido el id de
entidad de la unidad, `index << 10 | generation`. Comprobado: cada uno de esos mensajes nombra
una entidad viva en ese momento.

Para los especialistas, los mensajes que se leen:

| Mensaje | Qué es, y la comprobación |
|---|---|
| 0xF0E9 UnitHitEffects | el impacto de un proyectil: el uid del tirador y el punto de impacto en el sistema de la unidad (x adelante, y arriba, z izquierda): centímetros en aviones y barcos, 20/32768 m por paso en unidades terrestres (ajustado al tamaño de las torretas de tanque). `hitLocalX/Y/Z` en metros. Se convierte en una fila `shot` ([Disparos](hits.md#gunfire)). El atacante de casi todos los registros de impacto y baja está entre estos tiradores; los puntos de impacto caen en el lado que mira al tirador |
| 0xF133 UnitOnExplosion | el mismo uid de tirador |
| 0xF04B OnUnitDead | filas `dead`: cada víctima de un registro de baja tiene una dentro de 2 s |
| 0xD047 FmwRpm | las revoluciones de los motores (`rpm`); coinciden con el indicador de revoluciones de la cabina |
| 0xF0B1, 0xF0A0 | filas `gun_shot`: disparos sueltos de antiaérea pesada y artillería |
| 0xF01B, 0xF01C | filas `fire_start`, `fire_stop`: ráfagas de cañones antiaéreos de 40 mm (un cañón disparando; un fuego en un vehículo es `fire_on`, véase [Incendios de vehículos](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | filas `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | los impactos propios del jugador que graba y los que recibió, con arma y munición, nombrados desde la instalación (`projectileHitReplays`) |
| 0xF13E, 0xF031 | el efecto visual de un impacto y un efecto reproducido en la unidad; llegan junto a un impacto en la misma unidad |
| 0xD041 | uno por cada cañón defensivo de un avión, dos veces por segundo; sus índices coinciden con los artilleros del modelo de vuelo |
| 0xD048, 0xF117 | disposición leída, significado no conocido |
| el resto (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | en el archivo auxiliar de mensajes, con su unidad y campos |

Los nombres son los de la comunidad (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## También se lee {#also-read}

- **Replicación del flujo de entidades** (0x22, 0x23): por entidad, un bloque de
  valores de componente: temporizadores de reparación de barcos, recuentos de consumibles,
  cambios de propietario y equipo, sobrecalentamiento de motor. Se cuenta en
  `counts.replicatedComponents`; los valores, en el archivo auxiliar de mensajes.
- **Acciones del guion de la misión** (0xF028) y **pistas** (0xF0EC): `triggers`,
  `hints`. **Progreso de la misión** (0xF07A, 0xF07C): `missionProgress`.
- **La cámara de repetición** (0xD043): véase [La cámara](ground.md#the-camera).

## No se lee, y por qué {#not-read-and-why}

- **Nombres y cuerpos de los mensajes de entidad** (0x20, 0x21): el número de clase es un
  lugar en una lista compilada en el juego, no se envía y no está en sus datos. Se leen dos
  (los incendios de un vehículo y sus extintores); el resto se guarda completo con su entidad
  y número de clase.
- **Otros objetos replicados** (tipos distintos de las ranuras de jugador y equipos): leídos y
  guardados, sin nombrar; no hay nada en los resultados con qué comprobarlos.
- **Mandos, acelerador y proyectiles de otros aviones**: solo se actualizan de vez en cuando; se guardan
  en el archivo auxiliar de vuelo, no en la tabla.
- **Incendios de aviones**: no se encuentran en ningún mensaje; un avión en llamas no tiene
  fila `fire_on`.
- **Nombres de armas soltadas**: la entidad de una bomba o cohete no tiene nombre; los
  registros de baja nombran el arma de una baja.
- **Disparos que fallaron**: una repetición contiene solo los impactos.

El `counts.messageIdsNotRead` y el `selfCheck` de cada documento de la partida indican qué
contiene una repetición nueva y con qué fiabilidad se leyó.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
