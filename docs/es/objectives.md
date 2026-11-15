---
title: Objetivos
nav_order: 15
lang: es
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objetivos {#objectives}

`objectives` en el documento de la partida lista lo que se disputa en la batalla, desde dos fuentes (`source`):

- **La repetición** (`replay`): los objetos de misión que nombra 0xD039 (zonas de captura `cz_circle_NN`, aeródromos, helipuertos,
  bases), colocados donde los objetos replicados de tipo 3 (0xF02D) los sitúan ahora - una zona de captura empieza en el lugar
  de su plantilla y se mueve a la zona de este modo al inicio (`moved`). Los números del tipo 3 siguen el orden de 0xD039;
  cada objeto que no se mueve está exactamente donde lo tiene 0xD039, lo que comprueba el orden. Una zona de captura recibe
  la forma y el radio del área de la misión en su lugar (`area`, a 2 m) y su letra según su propio índice (tipo
  5 campo 69: 0 = A); el orden de las letras es el de la repetición, no se comprobó con el mapa del juego.
- **La misión** (`mission`): el archivo de misión `<misión>.blk` en el `mis.vromfs.bin` de tu instalación y las
  plantillas que importa (solo lectura, al convertir): sus áreas, clasificadas por nombre - apariciones (los puntos
  numerados de una aparición `..._spawnareaNN` como una sola aparición `points`), áreas de batalla, objetivos de bombardeo
  (`bomb_zone`), puntos de aparición de convoyes (`road_NN_spawn`), áreas de salida y de baja. Las áreas de otro modo del mismo mapa (`conq_`, `dom_`, `bttl_`,
  ...) se dejan fuera, y de las variantes `_arcade` / `_realistic` / `_hardcore` se toma la de la batalla (RB toma
  `_realistic`, si no `_hardcore`, como lo hacen los guiones de la misión); también los marcadores de información, los puntos de cañones antiaéreos y las áreas de más
  de 5 km (aquellas sobre las que se dispersan las apariciones). Cada aparición indica cuántas trayectorias de jugadores empezaron en ella (`used`,
  `usedByTeam`). Una misión puede intercambiar sus bandos al azar (`randomSpawnTeams`): cuando las apariciones muestran los equipos
  de la repetición al revés, cada `team` se intercambia y el bando del nombre se conserva como `missionTeam`. Las rutas de convoyes no
  están en los puntos de ruta de las misiones tal como se leen; solo se indica dónde aparecen los convoyes.

Las zonas de captura a lo largo del tiempo están en el archivo auxiliar `<partida>.objectives.parquet`: los objetos replicados de tipo 5, uno
por zona - campo 2 su propietario (0, 1, 2), campo 67 su progreso de captura, un byte con signo de -100 a 100 (positivo
hacia el equipo 2), campo 69 su índice. Comprobado (`selfCheck.objectives`) en repeticiones de servidor terrestres de batallas de Conquista y Dominio: cada cambio de
propietario llega con un jugador del equipo que captura ganando una `captureZone` en el marcador en el mismo momento (en 1,5 s)
y con una unidad terrestre viva de ese equipo dentro de la zona; las apariciones de cada batalla muestran los equipos de la
repetición en un solo sentido (a menudo al revés que los `t1_` / `t2_` de la misión).

## Unidades de escena: tranvías y vagones {#scene-units-trams-and-rail-wagons}

Un nivel puede colocar unidades propias: las entidades `unit_loader+rail_wagon` de una repetición de servidor son los tranvías del
archivo de escena del nivel (`gamedata/scenes/<nivel>_objects.blk` en `aces.vromfs.bin`: `setting__unit_class`, su
transformación e `setting__isDead`). Sus entidades no llevan un uid legible, así que una trayectoria terrestre sin entidad de unidad
cuya primera muestra cae a 2 m de una unidad de escena es esa unidad: su clase como `Vehicle`, tipo `train`, tipo
`tram`, `locomotive` o `wagon`, sin equipo; una unidad que la escena coloca muerta (como tranvías quemados) es un vehículo destruido (`alive` 0) desde su primera fila. El juego no tiene un nombre en inglés para ellas; `VehicleName` es el id
leído como palabras ("Railway tram A"). Sus posiciones no oscilan: casi todas nunca se mueven (cada
muestra igual bit a bit). La repetición las envía unas diez veces por segundo
de todos modos, así que de sus muestras solo se guardan las que las mueven (0,05 m o 0,1 grados), y una cada 10 s
(`selfCheck.sceneUnits` cuenta las muestras descartadas). Antes eran trayectorias llamadas `uid 8`
sin vehículo.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
