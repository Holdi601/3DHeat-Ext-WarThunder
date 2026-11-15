---
title: Aviones
nav_order: 11
lang: "es"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Aviones {#aircraft}

Para quien quiere saber de dónde vienen las columnas de aviones y cuánto confiar en ellas. Cada
comprobación de abajo compara un valor con algo que la repetición dice de una segunda
forma, independiente; aquí solo se dan el método y la coincidencia.

## Instrumentos de cabina {#cockpit-instruments}

El mensaje 0xD04A envía los indicadores del jugador que graba como pares (número, valor):
cuatro por segundo en batallas arcade, solo los valores que cambian en batallas de simulador. Los
números forman una sola lista para todas las cabinas, y cada cabina envía los
indicadores que tiene su modelo. El código del juego fija qué número es cada indicador,
así que cada número se nombró por lo que hace y se comprobó frente a la repetición
(`convert.INSTRUMENTS` contiene el resultado; no se lee nada de la instalación):

| Número | Nombre | Comprobado frente a |
|---|---|---|
| 0 | velocidad indicada, m/s | la velocidad de la trayectoria corregida por la densidad del aire: correlación 0,99 |
| 39 | velocidad de ascenso, m/s | la velocidad de ascenso de la trayectoria: correlación superior a 0,99 |
| 40, 41 | altitud, m; altitud módulo 1000 | la altura de la trayectoria, a pocos metros de diferencia |
| 52, 53 | balanceo y cabeceo del horizonte artificial | menos el balanceo y cabeceo de la tabla, a menos de 1 grado de diferencia |
| 64 | brújula | el rumbo de la tabla, a menos de 0,1 grados de diferencia |
| 15-20 | pedales del timón | la fuerza lateral sobre el avión |
| 23, 31 | palanca: elevador y alerones (signo como el del modelo de cabina) | el ángulo de ataque; la velocidad de balanceo |
| 69, 71, 73 | reloj: horas (esfera de 12 horas), minutos, segundos | la hora local del ordenador que graba, al minuto |
| 75 | presión del colector, atm | más alta en potencia de emergencia de guerra que a gas máximo |
| 81-86, 87-92, 93-98 | rpm por motor, rpm módulo 1000, indicador de rpm | entre sí, exactamente; las rpm del motor: correlación superior a 0,97 |
| 195 | combustible | baja durante una salida, vuelve a estar lleno al reaparecer |
| 228-230 | patas del tren de aterrizaje, 1 extendido | extendido solo cerca de la altura de los aeródromos y a velocidad de aterrizaje |
| 240, 241 | acelerador por motor (1,1 potencia de emergencia de guerra o postcombustión) | el acelerador de la entrada de vuelo |
| 330-332, 346-348 | contadores de munición (dos juegos iguales) | los proyectiles preestablecidos del arma, que bajan con los proyectiles de la entrada de vuelo |
| 135, 159 | temperatura del aceite y de la culata | probable: suben durante una salida |
| 58, 61 | bola de resbalamiento, aguja de viraje | probable: siguen la fuerza lateral y la velocidad de giro |
| 223 | aerofreno | probable: se activa solo en la aproximación |
| 490-497, 500-505 | frenos de rueda | probable: se activan solo parado en un aeródromo |

Se envían algunos números más cuyo significado no se conoce; se guardan en
`authorInstruments.notNamed` del documento de la partida.

Las columnas `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` y `throttle` de la tabla salen de estos, en las filas
propias del jugador que graba, tomando el último mensaje como mucho 0,2 s después de la
muestra.

## Entradas de vuelo {#flight-entries}

La entrada de vuelo de cada avión (tipo de paquete 2) contiene, además de su posición
y actitud:

- **Velocidad**: una palabra de 32 bits tras la actitud. Los bits 31, 30 y 29 son los
  signos de x, y y z; luego la velocidad en 11 bits de 500/2047 m/s (se para en
  500 m/s), luego |x| e |y| como fracciones de la velocidad en 9 bits cada uno, y z
  es lo que hace del vector un vector unitario. Comprobado frente al salto entre
  muestras recibidas: la dirección coincide en una fracción de grado para
  el jugador que graba y en unos 2 grados para los demás; la
  velocidad, a 0,2 %. `selfCheck.flightEntries`.
- **Proyectiles por arma**: una lista antes de la posición, un elemento por arma,
  primero los proyectiles que quedan. Los del jugador que graba son iguales a los
  contadores de la cabina un tick después, en casi todas las muestras.
- **Mandos y acelerador**: 7 bytes tras la velocidad, leídos como 14 nibbles.
  Para el jugador que graba, en cada tick: 1 el elevador, 2 los alerones, 3
  el timón (8 en reposo), 11 el acelerador en quinceavos (15 también para la potencia de
  emergencia de guerra y la postcombustión), 4 los frenos de rueda, 5 el aerofreno, 8
  probablemente el paracaídas de frenado. Los nibbles de los demás aviones cambian solo unas pocas veces
  por batalla y no son sus mandos en ese momento.
- **Motores**: por motor un byte de estado (0 apagado; 1-6 arrancando; 7 en marcha; 8
  muerto), un valor de 16 bits solo con postcombustión (32767 a fondo), y un byte solo
  tras haber sido alcanzado el motor. La mayoría de los aviones cuyo motor pasa a "muerto" son
  derribados o terminan en pocos minutos.

## Datos de reflexión {#reflection-data}

Los mensajes 0xF02D y 0xF0AA replican los objetos numerados del juego: por objeto,
su id (los 5 bits altos, el tipo; los 11 bajos, un índice) y una tabla de campos.
El tipo 14 son las ranuras de jugador (campo 2 el id de usuario y el nombre, 9 el equipo), el tipo 15
los equipos (índice 1 y 2):

- El campo 39 de una ranura contiene sus estadísticas en lugares fijos: bajas (desplazamiento 0),
  bajas de equipo (2), muertes (4), bajas navales (10), bajas de IA (12), bajas
  terrestres de IA (14), asistencias (20), zonas de captura (22), daño a zonas (24, 32 bits),
  premio por daño (40, 32 bits), evasiones de misiles (50). El campo 38 empieza con la
  puntuación, el campo 42 es la escuadra. Al final de una batalla, cada valor es igual
  al de los resultados para cada jugador (`selfCheck.scoreboardVsResults`). No se sabe
  dónde se guardan las bajas terrestres.
- El campo 7 de un equipo es su puntuación: al final es igual a la suma de las
  puntuaciones de sus jugadores en los resultados. El campo 3 es probablemente sus tickets.
- Cada mensaje envía solo los campos que cambiaron, así que `scoreboard` en el
  documento de la partida lista las estadísticas de cada jugador y la puntuación de cada
  equipo en cada cambio.

## Estimación por navegación y suavizador {#dead-reckoning-and-the-smoother}

Una repetición de cliente registra cada avión cuatro veces por segundo, tal como lo dibujó el cliente. Entre
las actualizaciones que recibe de un avión lejano, el cliente lo sigue moviendo a lo largo de su última
velocidad y lo gira a sus últimas velocidades de giro, y en la siguiente actualización lo
coloca de golpe allí. Leído tal cual, una trayectoria va recta y luego salta. Nada
en la entrada de vuelo marca qué muestras se recibieron; una muestra estimada por navegación
se reconoce por lo que es: continúa la línea recta de las dos muestras anteriores, a su
mismo ritmo, con un error de menos de 3 cm.

Cuánto importa depende de la batalla: en batallas arcade cerca de la mitad de las
muestras de los demás aviones pueden ser estimadas por navegación; en batallas de simulador,
solo unos pocos por ciento. El suavizador corta unos cinco veces los saltos de más de 15 g
(`selfCheck.deadReckoning`). El avión propio del jugador que graba no lo extrapola el cliente
y se deja como está.

Por defecto (`--no-smoothing` lo desactiva), las trayectorias de todas las unidades salvo las
del jugador que graba se colocan donde dicen los estados recibidos: una muestra estimada por
navegación va por una curva que une las muestras recibidas antes y después de ella, cada una con su
propia velocidad; más de 3 s, la línea recta solo se curva hacia la siguiente muestra recibida, así que
ninguna muestra se mueve más lejos que el propio salto del cliente. Su actitud se gira de forma
uniforme de una actitud recibida a la siguiente. Las muestras recibidas se suavizan como mucho 2 m
o 0,04 s de su velocidad; un giro constante se mantiene igual. Los valores propios de la repetición
se conservan en las columnas `Raw`.

## Actitud, comprobada {#attitude-checked}

En el avión propio del jugador que graba, el rumbo está a un grado
(mediana) de la dirección de avance, el cabeceo a unos pocos grados del ángulo de ascenso, y en los
giros claros el balanceo tiene el signo del giro en casi todas las muestras: el balanceo del modelo
de vuelo es positivo con el ala izquierda abajo, y la tabla lo invierte a positivo con el ala derecha
abajo (`selfCheck.aircraftAttitude`). Los ángulos de 10 bits avanzan en pasos de 0,18 grados.
La actitud de las unidades terrestres se comprueba frente a sus disparos ([Torretas](ground.md#turrets)).

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
