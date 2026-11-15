---
title: Impactos, disparos e incendios
nav_order: 13
lang: es
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Impactos, disparos e incendios {#hits-gunfire-and-fires}

Para quien quiere saber de dónde vienen las columnas de impacto, munición e incendio. Las
comprobaciones dan solo el método y la coincidencia.

## Disparos {#gunfire}

Cada proyectil que alcanzó a una unidad está en la repetición (mensaje 0xF0E9): una fila `shot`
en la posición del tirador en el momento del impacto, `targetX/Y/Z` el punto de impacto (la unidad
alcanzada, desplazada por el punto de impacto en su sistema, girado por su actitud), la dirección
hacia ella, `other` la unidad alcanzada. Los obuses y balas que fallaron no se envían: no son
entidades, y los mensajes de armas en vuelo solo contienen cohetes, misiles, bombas y torpedos.
Los proyectiles que le quedan al jugador que graba (su columna `ammo`) bajan según dispara, así que
se pueden distinguir sus ráfagas, pero no adónde fueron esos proyectiles. La antiaérea pesada y la
artillería envían cada disparo suelto (`gun_shot`, sin dirección), los cañones antiaéreos de 40 mm
sus ráfagas (`fire_start`, `fire_stop`).

## Resultados de impacto {#hit-outcomes}

Con cada impacto de proyectil sobre una unidad terrestre, el servidor envía a la unidad el mensaje 0xF144
(UnitOnHit): cuatro campos de un byte, el cuarto son los bits de lo que hizo el impacto
(`selfCheck.unitMessages.outcome_*`):

| Bit | Significado | Prueba |
|---|---|---|
| 0x20 | el impacto propio de un proyectil | casi todos llegan con un impacto 0xF0E9 en la unidad a 5 ms; sin él, con una explosión (metralla) |
| 0x01 | atravesó (penetración) | todo mensaje con 0x02, 0x04 u 0x08 lo tiene también |
| 0x02 | impacto crítico | la mayoría de los registros de impacto crítico lo tienen, mucho más a menudo que por azar |
| 0x04 | destruido | la mayoría llega con un registro de baja y la muerte de la unidad en menos de un segundo |
| 0x08 | daño grave | algunos registros de impacto crítico lo tienen; raro en los demás |

`hitOutcome` toma el peor: `kill` (0x04), `critical` (0x02 u 0x08),
`penetration` (0x01), `nonpenetration` (solo 0x20). Un impacto se empareja con el 0xF144
con 0x20 sin pareja más cercano a su unidad a 5 ms. La cámara de impacto del juego distingue un rebote de
una no penetración, pero ningún bit ni campo encontrado aquí lo hace: los tres primeros bytes varían de
impacto a impacto y no se conocen. Las repeticiones de cliente envían 0xF144 solo para el propio avión del
jugador que graba, con todos los bits a cero: los impactos de aviones y barcos no tienen resultado.

## Munición {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosivo o no.** Un proyectil que estalla envía 0xF133 (UnitOnExplosion)
  con el uid del tirador y el número del impacto; un impacto con uno es
  `explosive`, los demás `kinetic`.
* **El cañón y su ranura.** 0xF0BD (UnitBulletRearm) es el siguiente proyectil cargado:
  el índice del arma en la lista de armas del vehículo, la ranura de munición y los
  proyectiles que quedan. El de un cargador manual llega a un tiempo de recarga constante tras
  cada uno de sus impactos, el de un cañón automático a una fracción de segundo. Los impactos de un
  tirador se agrupan por vehículo, firma y ráfaga; un grupo es de un arma cuando esa arma carga un
  proyectil en 20 s después de la mitad de sus impactos o más, con un retardo constante. `ammoSlot` es
  `arma/ranura`, la ranura cargada antes del impacto: probablemente la disparada, salvo que el
  jugador cambiara la munición en medio. Las ametralladoras no envían 0xF0BD.
* **El proyectil.** El arma de una baja es el id del proyectil (`125mm_3bm46`); el último
  impacto del asesino sobre la víctima se lo asigna a la ranura de ese tirador, donde
  coincide el calibre del cañón. Su tipo y calibre son los del archivo de armas
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **El calibre** del resto: el del arma de una ranura; el de un grupo de ametralladora, el
  único calibre de ametralladora que puede tener su firma; si no, el del cañón principal
  del vehículo. Sin la instalación (`--game`) no hay tipo, nombre ni calibre más allá de
  `explosive` / `kinetic`.

No se encuentra: el rebote. Varios mensajes más llevan el tirador y el número del impacto
(0xF0C2, probablemente el recorrido de la cámara de impacto por dentro del vehículo; 0xF117,
0xF13C, 0xF13E); se guardan en el archivo auxiliar, sin decodificar. Una
no penetración sigue siendo `nonpenetration`.

## Incendios de vehículos {#vehicle-fires}

Un vehículo en llamas se muestra a todos los clientes: el servidor envía un mensaje de entidad al
vehículo (evento `0a519c58`) con la lista de incendios que arden en él, cada vez que cambia la lista. Por
incendio: dos ids de 16 bits (el segundo, un nodo del modelo de daños), su tipo, y -1 hasta que el
fuego prende. Un incendio provocado por un impacto recibe además un mensaje con el punto donde arde, en el
sistema del vehículo (x adelante, y arriba, z izquierda).

Filas: `fire_on` cuando aparece un incendio en la lista, `fire_off` cuando ya no está, en el
vehículo, con `fireId` (`first:node`), `fireKind` y, para los incendios que provocó un
impacto, `fireLocalX/Y/Z` (adelante, arriba, derecha). Una vez muerto un vehículo, su
lista a menudo ya no se vuelve a enviar: sus incendios terminan con su resto, si no con su
entidad, si no con la repetición (`selfCheck.fires`).

Comprobado: cada vez que bajó el número de extintores de incendio de un tanque, un incendio salió
de su lista en una fracción de segundo; la mayoría de los puntos de incendio están en el mismo lado del
vehículo que el impacto que lo provocó. Los tipos son números; lo que nombran
no se conoce, ni tampoco qué parte es un nodo. Los aviones no envían ninguna lista así: un
avión en llamas no se lee.

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
