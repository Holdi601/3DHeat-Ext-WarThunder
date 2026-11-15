---
title: Archivos auxiliares y completitud
nav_order: 8
lang: "es"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Archivos auxiliares y completitud {#sidecars-and-completeness}

Nada de una repetición se descarta. Lo que lee el convertidor va a la tabla y al
documento de la partida; todo lo demás se guarda completo en tres archivos auxiliares
junto a la tabla (dentro del archivo `.3dheat`, o sueltos con `--loose`). Es la regla que
comparten todos los convertidores de 3DHeat:
[Los convertidores lo conservan todo](https://holdi601.github.io/3DHeat/converters.html).

## Los archivos auxiliares {#the-sidecars}

- `<partida>.messages.parquet`: cada mensaje a una unidad (tiempo, id y nombre del mensaje, uid, eid, plantilla, vehículo, sus campos de id en hex, `decoded` (lo que se lee de él, como JSON), la carga), cada valor de componente replicado (`name` el componente, `fields` su valor), cada mensaje de entidad (con su entidad y número de clase), cada objeto replicado (`ReflectionData
  <kind>/<index>`, sus campos en hex) y cada paquete que ningún lector de aquí toma, completo.
- `<partida>.objectives.parquet`: las zonas de captura a lo largo del tiempo, una fila por
  cambio que envió el servidor: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (su letra), `zoneId`, `object`, `owner` (0 ninguno,
  1, 2), `progress` (-100..100, positivo hacia el equipo 2), los `x`,
  `y`, `z` de la zona, y todos los `fields` del objeto en hex (véase
  [Objetivos](objectives.md)).
- `<partida>.flight.parquet`: cada entrada del modelo de vuelo de cada avión, completa
  (sus bits, y `phase`: el bit del primer byte en el que empezó), con su
  velocidad, los 14 nibbles de control (`control1-3`, `throttle`), sus motores
  con su estado, postcombustión y condición, y sus proyectiles por arma
  (`ammo`; `numbers` es la lista completa). Los valores de los demás aviones son los
  de la última actualización.

## Lo que garantizan los recuentos {#what-the-counts-guarantee}

Los `counts` del documento de la partida dicen qué contenía la repetición y qué pasó
con ello:

| Clave | Qué es |
|---|---|
| `packets`, `unreadPackets` | cada tipo de paquete encontrado, y los que ningún lector toma (guardados completos en el archivo auxiliar de mensajes) |
| `messageIds`, `messageIdsNotRead` | cada id de mensaje encontrado y cuántas veces, y los que solo se guardan, no se leen |
| `replicatedComponents`, `replicatedNotRead` | valores de componente leídos, y los que solo se guardan |
| `entities`, `entityTemplates`, `entityMessages` | lo que creó y envió el flujo de entidades |
| `droppedSamples` | muestras dejadas fuera a propósito (los restos de una unidad terrestre tras desaparecer su entidad), por motivo |

No se deja nada fuera: cada elemento de la repetición o se lee a la tabla o al
documento de la partida, o se guarda completo en un archivo auxiliar. El `selfCheck`
del documento de la partida contiene las comprobaciones de lo que se leyó
([Cómo lee una repetición](how-it-reads.md)).

---

Parte de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentación](https://holdi601.github.io/3DHeat/)). Código fuente: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
