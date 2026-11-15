---
title: Unidades terrestres y cámara
nav_order: 12
lang: es
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unidades terrestres y cámara {#ground-units-and-camera}

Para quien quiere saber de dónde vienen las columnas de torreta, cámara y modo de batalla, y
cuánto confiar en ellas. Las comprobaciones dan solo el método y la coincidencia.

## Torretas {#turrets}

El estado terrestre de un tanque (actitud de 16 bits) contiene, tras su posición, 141 bits
sin leer, y luego por torreta 62 bits: el giro de la torreta y la elevación del cañón
(16 bits cada uno, 360/65536 grados por paso, con signo), y 30 bits sin leer; después,
relleno, y en algunos estados 200 bits más. El número de torretas es el byte que se envía
antes del estado. Un estado cuya longitud no encaja no da torretas (las unidades estáticas
envían un estado más corto). El giro es relativo al casco, positivo en sentido horario,
0 hacia delante; la elevación, relativa al casco, positiva hacia arriba.

Cómo se comprobó:

- **Frente a los disparos:** para cada impacto de un tanque, la dirección en el mundo de su
  cañón principal (la actitud del casco girada por el giro de la torreta y la elevación del
  cañón) frente a la línea desde el tirador hasta la unidad alcanzada, a al menos 30 m: por
  batalla, una mediana de cerca del 98 % dentro de 3 grados en rumbo y del 99 % en elevación
  (`selfCheck.turretsVsShots`). Los demás son sobre todo impactos de una ametralladora en
  otra torreta.
- **Frente a la mira del jugador que graba:** su propio tanque envía el ángulo en el mundo de
  su mira (en sentido antihorario desde el este), el cabeceo y la distancia. El rumbo del casco
  más el giro de la torreta está a medio grado (mediana) de la mira.

**Repeticiones de servidor** (0xF074) envían el estado de cada tanque con la misma disposición,
seguido de datos propios, así que se lee cada torreta cuyos dos ángulos caen dentro del
estado (al menos la principal, en casi todas las filas de tanque). Es la torreta, no la cámara:

- **Frente a los disparos**, como arriba: por batalla, más del 90 % dentro de 3 grados en rumbo y el
  99 % en elevación.
- **Frente a la vista:** una repetición de servidor envía la mira de cada jugador
  (`viewYaw`, `viewPitch`). La torreta sigue a la vista a medio grado (mediana),
  pero gira mucho más despacio que la vista oscila, como lo hace un mecanismo de torreta
  (`selfCheck.turretVsView`).
- **Pero no siempre a la velocidad de un mecanismo:** muestra a muestra, el valor tal como se envía
  a veces salta sobre la mira cuando la mira está cerca del cañón, más deprisa de lo que gira
  cualquier mecanismo.

Por eso la tabla guarda la torreta **limitada a su mecanismo**: `turretYaw` /
`gunPitch` se mueven hacia el valor enviado a una velocidad no mayor que la de giro del cañón
principal según el archivo de vehículo de la instalación (por 1,3 para las habilidades de la tripulación
y las modificaciones; 45 y 20 grados por segundo donde la instalación no lo indica). En cada impacto
del cañón principal, la torreta se fija exactamente en la línea del disparo, y una pasada hacia atrás
la lleva allí a tiempo (`selfCheck.turretLimit`).
La fila `shot` lleva también ese `turretYaw` / `gunPitch`. El valor tal como se envía
se mantiene en `turretYawRaw` / `gunPitchRaw`. Un tanque cuyo estado no lleva
torreta tiene vacías las columnas de torreta (el visor puede recurrir a `viewYaw`).
`gunPitch` queda un poco por encima de `viewPitch` a distancia: es la elevación del cañón
para la caída del proyectil.

Los estados de los barcos tienen otra disposición; sus torretas no se leen. Los aviones
no envían dirección de cabeza ni de vista; el mensaje 0xD020 de los cañones antiaéreos
sigue sin leerse.

## La cámara {#the-camera}

El mensaje 0xD043, unos 20 por segundo, es la cámara de repetición propia del jugador que graba: el campo 1 un cuaternión que gira el
frente de la cámara hacia donde mira; el 2, el lugar de la cámara respecto al vehículo que sigue (m); el 4, el mismo
desplazamiento en el propio sistema del vehículo (x adelante, y arriba, z izquierda); el 5, hacia dónde apunta
el jugador (un vector unitario); el 3, el zoom (unas 1,2 en la vista de tercera persona de un tanque, unas
1,0 en un avión, más alto en la mira de artillero o con prismáticos).
Comprobado: el campo 4 es el campo 2 llevado al sistema del vehículo, a menos de 0,5 m en
casi todos los mensajes; el frente de la cámara tiene el rumbo de la mira. La
repetición no envía el campo de visión en grados, solo el zoom.

La tabla tiene la cámara como trayectoria propia: tipo `camera`, trayectoria
`<jugador> camera #ca`, una fila como mucho cada 0,1 s, en el lugar del vehículo seguido más el campo 2,
mirando a lo largo del cuaternión (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), con `zoom`, `aimHeading` y `aimPitch`, y `otherLife`
la vida que sigue. `selfCheck.camera` cuenta las filas y la comprobación.

## Final de una trayectoria {#end-of-a-track}

Una trayectoria se dibuja desde su primera fila hasta su última. Cuando su unidad desaparece
antes de que acabe la repetición, su última fila es una fila `despawn` en su último lugar:
en el momento en que el juego quitó su entidad (cuando ocurrió a menos de 6 s de su
última muestra), si no, en su última muestra. Una trayectoria sin ella dura hasta el final
de la repetición. Las filas de una misma trayectoria pueden estar muy separadas (una unidad lejana o un
resto se actualiza cada pocos segundos, y un resto a veces no durante minutos): su último
estado se mantiene hasta su siguiente fila.

## Modo de batalla {#battle-mode}

El byte de la cabecera en el desplazamiento 688 contiene la dificultad en sus cuatro bits bajos:
0 arcade (AB), 5 realista (RB), 10 simulador (SB). Comprobado frente a los
tipos de batalla que se sabía que tenían las repeticiones. El modo de juego es `ground` cuando
la misión permite aparecer tanques, si no `naval` cuando permite barcos, si no `air`
(`allowedUnitTypes`); el modo propio de la misión sale de su clave
(`missions/_Dom`), con nombre según `lang/missions_versus.csv` de tu instalación. La misma
clave es la parte `<modo>` de los nombres de archivo y el id de la partida (`Conq4`,
`Dom`), omitida donde la cabecera no tiene ninguna.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
