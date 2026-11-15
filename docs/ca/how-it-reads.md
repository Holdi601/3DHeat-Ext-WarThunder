---
title: Com llegeix una repetició
nav_order: 10
lang: ca
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Com llegeix una repetició {#how-it-reads-a-replay}

Aquesta pàgina és per a qui vol saber què llegeix el convertidor, com es va comprovar, i
per tant com de fiable és cada columna. No cal per convertir repeticions.

La lectura es va comprovar amb repeticions de client de batalles arcade aèries, de
simulador aeri i navals, amb repeticions de servidor de batalles terrestres, i, per als
dissenys de 2025, amb les repeticions de mostra públiques de
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Cada comprovació
compara un valor amb una altra cosa que la repetició diu d'una segona manera independent;
aquí només es donen el mètode i l'acord.

## Què es llegeix, i la comprovació {#what-is-read-and-the-check}

| Part | Estat i comprovació |
|---|---|
| Capçalera, mapa, missió, hora d'inici, sessió; resultats | cada fitxer |
| Configuració de la missió (el blk després de la capçalera) | mode, temps, límits, `stars` (data, hora, lloc) |
| Flux de paquets (zlib el 2025, zstd el 2026) | cada paquet emmarcat |
| Posicions i actitud dels avions (disposició de 2026) | 4 mostres per segon, cap paquet sense llegir; el heading coincideix amb la direcció del moviment |
| Paquets de vol adelantats | després d'un petit bloqueig de xarxa, un paquet de vol d'una repetició de client a vegades conté cada altre avió allà on serà uns 0,75 s més tard. L'avantatge es mesura per paquet, i a cada avió que va per davant se li dona l'hora que representa (`selfCheck.flightPacketsRetimed`) |
| Salts de l'estimació per navegació | un salt fora d'un recorregut estimat es mesura des de l'últim estat rebut, de manera que les correccions del client ja no tallen les trajectòries ([Estimació per navegació](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teletransports | una trajectòria es talla on la seva unitat es mou més lluny del que pot: primer contra el seu tipus (avió 750 m/s, terrestre i vaixells 40 m/s, armes 1800 m/s), després contra el seu propi ritme. Cada tall es llista a `trackBreaks` amb la seva causa probable (reaparició, el joc movent el jugador, una correcció d'una unitat llunyana). Després dels talls, cap pas entre files d'una trajectòria no és més ràpid del que permet el seu tipus (`selfCheck.stepSpeed`) |
| Posicions terrestres i de vaixells (0xF073 / 0xF074) | cap paquet sense llegir. Heading, pitch i roll de l'actitud de 16 bits: el heading coincideix amb la direcció del moviment a uns 2 graus (mediana); el pitch compta 180/65536 graus per pas; amb el signe del roll girat, la direcció del canó des del casc i la torreta apunta a la unitat impactada en gairebé cada tret de tanc. Els vaixells estan al nivell de l'aigua |
| Torretes | el guinyol de torreta dels tancs i l'elevació del canó: vegeu [Torretes](ground.md#turrets) |
| Alçades del terreny empaquetades | les posicions empaquetades en 64 bits compten la seva alçada des de -100 m a la majoria de nivells, i des del nivell de l'aigua en alguns; el desplaçament es mesura a cada repetició a partir d'unitats vistes en les dues formes (`selfCheck.packedGroundHeight`) |
| Flux d'entitats (creació, destrucció) | cada creació llegida. La disposició ve del codi font publicat del Dagor Engine; els tipus de component propis de War Thunder se salten trobant on comença el component següent. La ranura de vehicle i de jugador de cada unitat són les mateixes que nomenen els registres de mort i d'impacte, per a cada registre comprovat |
| Qui manejava quina unitat, unitats IA, vaixells, objectius terrestres | del flux d'entitats: cada unitat té el seu vehicle i equip, i la unitat de cada jugador té el seu jugador |
| Morts contra els resultats | les morts per jugador són les dels resultats; els resultats compten més morts, perquè el client no rep totes les morts. Una repetició que comença després que la batalla hagi començat només té les morts posteriors a aquest moment |
| Morts, impactes crítics, danys greus | cada fitxer |
| Mòduls destruïts (0xF118) | la unitat i el número de la part; el nom de la part necessita el model de danys del vehicle, que no és a la repetició |
| Armes llançades (flux d'entitats) | el punt de llançament és a uns 10-20 m (mediana) de la unitat més propera, que es pren com el llançador |
| Armes en vol (0xF0DB) | míssils, coets i bombes, cadascun lligat a la seva entitat |
| Bombes sense registres de vol | una bomba sense ells té la seva caiguda calculada des del llançament fins a l'impacte (gravetat i resistència, una mostra cada 0,1 s, `extrapolated` a cert). Comprovat sobre el mar, on l'alçada d'impacte és coneguda: les caigudes calculades acaben a uns 15 m de l'aigua. Al document de partida, aquesta arma té `ballisticImpact`; `counts.bombsBallistic` les compta |
| Ranures de jugador, xat | cada fitxer |
| Explosions, explosions de flak, distincions, deteccions, clima, objectes de missió | llegits; posicions comprovades a ull al visualitzador |
| Els instruments del jugador que grava (0xD04A) | nomenats per allò que fan: [Instruments de cabina](aircraft.md#cockpit-instruments); la resta a `notNamed` |
| Altres camps de les entrades de vol | velocitat, munició, comandaments, motors: [Entrades de vol](aircraft.md#flight-entries) |
| Actitud de les files d'esdeveniment | cada fila d'esdeveniment porta el heading, pitch, roll i vector de mirada de la seva unitat en aquell moment |
| Estadístiques de jugadors i puntuacions d'equip | al final de la batalla, cada estadística és igual a la dels resultats per a cada jugador: [Dades de reflexió](aircraft.md#reflection-data) |
| Noms d'armes i de vehicles | de la localització en anglès de la teva instal·lació; alguns cinturons per defecte de vaixells i radars d'aeròdrom no tenen nom al joc |
| Jugadors i IA | cap fila de jugador dels resultats no és IA, i cada fila que no és IA és d'un jugador dels resultats (`selfCheck.identity`) |
| Restes | les mostres d'una unitat després de la seva mort continuen arribant; la resta d'una unitat terrestre o d'un vaixell és `alive` 0 fins que la seva entitat s'elimina, i segueix sent una mateixa trajectòria; els avions mantenen `alive` 0 com a molt 60 s (`selfCheck.wrecks`) |
| Canvis de vehicle | un vehicle encara viu d'un jugador quan apareix el següent vehicle del mateix jugador es dona per acabat allà (un vehicle deixat dret). `selfCheck.vehicleSwitch.twoLiveVehicles` ha de ser 0 |
| Mode de batalla | [Mode de batalla](ground.md#battle-mode) |
| Avions en una repetició de servidor de 2026 | llegits en la disposició de 2026; el heading i el signe del roll coincideixen amb els girs; els avions de marcador de posició i els drons de reconeixement no porten dades |
| Jugadors d'una repetició de servidor | trobats pel nom a les ranures; cada estadística és igual a la dels resultats (`selfCheck.players`) |
| Avions en repeticions de servidor de 2025 i versió 101286 | no llegits: els seus paquets de vol tenen una altra disposició |

## Missatges a les unitats {#messages-to-units}

Cada paquet de tipus 4 és un missatge mpi del daNet del Dagor Engine: l'identificador de
l'objecte destinatari, després (quan els seus 11 bits baixos són tots 1) l'UID extern de
l'objecte, l'identificador del missatge i la càrrega. Un missatge a una unitat porta com a
UID extern l'identificador d'entitat de la unitat, `index << 10 | generation`. Comprovat:
cada missatge d'aquest tipus nomena una entitat viva en aquell moment.

Per als especialistes, els missatges que es llegeixen:

| Missatge | Què, i la comprovació |
|---|---|
| 0xF0E9 UnitHitEffects | l'impacte d'un projectil: l'uid del tirador i el punt d'impacte al marc de la unitat (x endavant, y amunt, z esquerra): centímetres als avions i vaixells, 20/32768 m per pas a les unitats terrestres (ajustat a la mida de les torretes de tanc). `hitLocalX/Y/Z` en metres. Esdevé una fila `shot` ([Trets](hits.md#gunfire)). El tirador de gairebé cada registre d'impacte i de mort és entre aquests tiradors; els punts d'impacte són a la cara que mira al tirador |
| 0xF133 UnitOnExplosion | el mateix uid del tirador |
| 0xF04B OnUnitDead | files `dead`: cada víctima d'un registre de mort en té una dins 2 s |
| 0xD047 FmwRpm | les rpm dels motors (`rpm`); coincideix amb l'indicador de rpm de la cabina |
| 0xF0B1, 0xF0A0 | files `gun_shot`: trets individuals d'antiaeri pesant i d'artilleria |
| 0xF01B, 0xF01C | files `fire_start`, `fire_stop`: ràfegues de canons antiaeris de 40 mm (un canó que dispara; un foc en un vehicle és `fire_on`, vegeu [Focs als vehicles](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | files `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | els impactes propis del jugador que grava i els que rep, amb arma i munició, nomenats des de la instal·lació (`projectileHitReplays`) |
| 0xF13E, 0xF031 | l'efecte visual d'un impacte i un efecte reproduït sobre la unitat; vénen amb un impacte a la mateixa unitat |
| 0xD041 | un per cada canó defensiu d'un avió, dos cops per segon; els seus índexs coincideixen amb les armes de tirador del model de vol |
| 0xD048, 0xF117 | disposició llegida, significat no conegut |
| la resta (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | a l'annex de missatges amb la seva unitat i camps |

Els noms són els de la comunitat (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## També llegit {#also-read}

- **Replicació del flux d'entitats** (0x22, 0x23): per entitat, un bloc de valors de component:
  temporitzadors de reparació de vaixells, comptadors de consumibles, canvis de propietari i
  equip, sobreescalfament del motor. Comptat a `counts.replicatedComponents`; els valors a
  l'annex de missatges.
- **Accions del guió de la missió** (0xF028) i **indicacions** (0xF0EC): `triggers`, `hints`.
  **Progrés de la missió** (0xF07A, 0xF07C): `missionProgress`.
- **La càmera de repetició** (0xD043): vegeu [La càmera](ground.md#the-camera).

## No llegit, i per què {#not-read-and-why}

- **Noms i cossos dels missatges d'entitat** (0x20, 0x21): el número de classe és un lloc en una
  llista compilada dins del joc, no s'envia i no és a les seves dades. Dos es llegeixen (els focs
  d'un vehicle i els seus extintors); la resta es guarda sencera amb la seva entitat i número de
  classe.
- **Altres objectes replicats** (tipus diferents de les ranures de jugador i els equips): llegits i
  guardats, no nomenats; no hi ha a les dades dels resultats amb què comprovar-los.
- **Els comandaments, l'accelerador i la munició d'altres avions**: només s'actualitzen de tant en
  tant; es guarden a l'annex de vol, no a la taula.
- **Focs als avions**: no es troben a cap missatge; un avió en flames no té cap fila `fire_on`.
- **Noms de les armes llançades**: l'entitat d'una bomba o d'un coet no té cap nom; els registres de
  mort nomenen l'arma d'una mort.
- **Trets que han fallat**: una repetició només conté els impactes.

Els `counts.messageIdsNotRead` i el `selfCheck` de cada document de partida diuen què conté una
repetició nova i com de bé s'ha llegit.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
