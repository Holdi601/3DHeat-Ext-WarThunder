---
title: Annexos i completesa
nav_order: 8
lang: ca
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Annexos i completesa {#sidecars-and-completeness}

Res d'una repetició no es descarta. Allò que llegeix el convertidor va a la taula i al
document de partida; tota la resta es guarda sencera en tres fitxers annexos al costat de
la taula (dins del fitxer `.3dheat`, o separats amb `--loose`). Aquesta és la regla que
comparteixen tots els convertidors de 3DHeat:
[Els convertidors ho guarden tot](https://holdi601.github.io/3DHeat/converters.html).

## Els annexos {#the-sidecars}

- `<partida>.messages.parquet`: cada missatge a una unitat (hora, identificador i nom del
  missatge, uid, eid, plantilla, vehicle, els seus camps d'identificació en hex, `decoded`
  (el que se n'ha llegit, com a JSON), la càrrega), cada valor de component replicat
  (`name` el component, `fields` el seu valor), cada missatge d'entitat (amb la seva
  entitat i el seu número de classe), cada objecte replicat (`ReflectionData
  <kind>/<index>`, els seus camps en hex) i cada paquet que cap lector d'aquí no agafa,
  sencer.
- `<partida>.objectives.parquet`: les zones de captura al llarg del temps, una fila per
  canvi que ha enviat el servidor: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (la seva lletra), `zoneId`, `object`, `owner` (0 cap, 1, 2),
  `progress` (-100..100, positiu cap a l'equip 2), les `x`, `y`, `z` de la zona i tots els
  `fields` de l'objecte en hex (vegeu [Objectius](objectives.md)).
- `<partida>.flight.parquet`: cada entrada del model de vol de cada avió sencera (els seus
  bits, i `phase`: el bit del seu primer byte on va començar), amb la seva velocitat, els
  14 quarts de comandament (`control1-3`, `throttle`), els seus motors amb el seu estat,
  postcombustor i condició, i les seves municions per arma (`ammo`; `numbers` és la llista
  sencera). Els valors dels altres avions són els de l'última actualització.

## Què garanteixen els recomptes {#what-the-counts-guarantee}

Els `counts` del document de partida diuen què contenia la repetició i què n'ha estat:

| Clau | Què és |
|---|---|
| `packets`, `unreadPackets` | cada tipus de paquet trobat, i els que cap lector no agafa (guardats sencers al fitxer annex de missatges) |
| `messageIds`, `messageIdsNotRead` | cada identificador de missatge trobat i quantes vegades, i els que només es guarden, sense llegir-se |
| `replicatedComponents`, `replicatedNotRead` | valors de component llegits, i els que només es guarden |
| `entities`, `entityTemplates`, `entityMessages` | el que ha creat i enviat el flux d'entitats |
| `droppedSamples` | mostres deixades fora a propòsit (la resta d'una unitat terrestre després que la seva entitat ha desaparegut), per motiu |

Res més no queda fora: un element de la repetició o bé es llegeix a la taula o al
document de partida, o bé es guarda sencer en un annex. Les comprovacions de
`selfCheck` del document de partida recullen el que s'ha llegit
([Com llegeix una repetició](how-it-reads.md)).

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
