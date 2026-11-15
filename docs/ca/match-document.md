---
title: El document de partida
nav_order: 7
lang: ca
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# El document de partida {#the-match-document}

![L'inici d'un document de partida sintètic, i les seves claus](../assets/img/match-document.svg)

`<partida>.match.json` guarda tot el que diu la repetició que no és una fila de la
taula. La pestanya Partida del visualitzador la llegeix.

## La batalla {#the-battle}

| Clau | Què és |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | l'identificador de la partida (com al nom del fitxer); l'identificador del mapa; el fitxer de nivell que fa servir |
| `mission`, `missionKey` | el nom de la missió i la seva clau als fitxers de text del joc |
| `battleClass`, `environment`, `weather` | tal com les dona la capçalera |
| `sessionId`, `server` | l'identificador de sessió de la batalla; el servidor |
| `replayVersion`, `flightLayout` | la versió del format de repetició; la disposició de paquets de vol llegida (`2025` o `2026`) |
| `files` | els fitxers de repetició llegits (un, o les parts d'una repetició de servidor) |
| `started`, `timePlayed`, `replayEnd` | hora d'inici (ISO, UTC); segons jugats, dels resultats; segons del darrer paquet de la repetició |
| `author`, `authorUserId` | el jugador que grava i el seu identificador Gaijin (repeticions de client) |
| `teams` | els equips de la batalla (`1`, `2`) |
| `result` | `winner`, `status` (`success` o `fail`, el resultat de qui grava), `authorTeam`, `teams` ([Economia](economy.md)) |
| `vehicleNames` | d'on han sortit els noms dels vehicles (la teva instal·lació) i el seu idioma |
| `conventions` | les unitats i els signes de la taula: eixos, temps, vida, trajectòria, alive, roll, i més |

## La resta {#everything-else}

| Clau | Què és |
|---|---|
| `battle`, `difficulty`, `gameMode` | el mode de batalla: `difficulty` `AB` / `RB` / `SB` (i el seu nom, i el byte de la capçalera), `gameMode` `ground` / `air` / `naval`, el mode de la missió (`Dom`, `Conq`, `Bttl`, `I2M`, ...) i el seu nom en anglès de la teva instal·lació (`Domination`, `Enduring Confrontation`), els tipus d'unitat permesos (vegeu [Mode de batalla](ground.md#battle-mode)) |
| `settings` | el bloc de la missió després de la capçalera: mode, entorn, temps, límits de puntuació i de temps, països, tipus d'unitat permesos, vent, i `stars` (latitud, longitud, data, hora local) |
| `sky` | el primer `CustomWeatherParams`: direcció del sol i de la lluna, vent, colors del cel, desplaçaments dels núvols |
| `players`, `slots` | la línia dels resultats per jugador (morts, baixes en terra, morts, assistències, puntuació, captures, esquadra, clan, país, alineació, els uids que van conduir); les ranures de jugador de la repetició (nom, identificador d'usuari, equip) |
| `units` | cada entitat d'unitat que ha creat la repetició: eid, uid, plantilla, vehicle, tipus, categoria, equip, jugador, nom a la missió, quan es va crear i eliminar, on es va crear, quins components no es van poder llegir |
| `objects` | els objectes amb nom de la missió: zones de captura i aeròdroms amb la seva posició i mida, els contorns dels aeròdroms com a punts, les àrees d'aparició |
| `objectives` | els objectius de la batalla, cadascun amb el seu `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (l'1 o el 2 de la repetició, buit per a tots dos), `name` (una zona de captura la seva lletra, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) amb `position`, `radius` / `height` / `size` i `heading`, `source` (`replay` o `mission`) i tot el que se'n sap (vegeu [Objectius](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | amb els noms i vehicles dels dos bàndols; les morts amb el nom en anglès de l'arma |
| `weapons` | cada coet, míssil, bomba, torpedo, dipòsit de caiguda i càrrega llançada: quan, on es va llançar (posició, actitud, velocitat), per quina unitat (la més propera dins 300 m i 1,5 s), quantes mostres de vol, on es va veure per últim cop, quan es va eliminar |
| `explosions`, `flak` | `PlayExplosionVisual` (posició, direcció, tipus) i `PlayFlakExplosionVisual` (posició) |
| `awards` | les distincions del jugador que grava (`TextStreak`: first_blood, ratxes, comptadors de reptes) |
| `detections`, `unitStates` | parells `UnitDetected` d'unitats; un missatge (0xF093) amb la posició, l'actitud i la velocitat d'una unitat, el significat del qual no es coneix |
| `authorInstruments` | els valors de cabina del jugador que grava (`ReplayCockpitParams`) per número d'instrument, com a molt un per segon; `known` nomena cada número que aquesta repetició ha enviat (nom, unitat, com es va comprovar), `notNamed` la resta |
| `scoreboard` | les estadístiques de cada jugador cada vegada que han canviat (morts, baixes en terra, assistències, puntuació, morts IA, morts navals, zones, dany, evasions de míssils, esquadra), i la puntuació de cada equip i els seus possibles tiquets al llarg del temps (vegeu [Dades de reflexió](aircraft.md#reflection-data)) |
| `economy` | els Lleons de plata i punts d'investigació de la batalla (vegeu [Economia](economy.md)): totals, per jugador, per vehicle, els multiplicadors, el guanyador, les comprovacions |
| `entityMessages` | els missatges d'entitat (0x20) per número de classe: recompte, plantilles d'objectiu, mides |
| `chat` | cada línia del xat |
| `triggers`, `hints`, `missionProgress` | les accions del guió de la missió (RunTriggerAction), les seves indicacions, els seus missatges de progrés |
| `camera` | els camps de la càmera de repetició del jugador que grava cada 0,25 s tal com s'han enviat (la taula la té com a trajectòria) |
| `projectileHitReplays` | els impactes del jugador que grava i els que ha rebut, amb l'arma i la munició i els seus noms en anglès |
| `results` | el bloc complet dels resultats tal com el va escriure el joc |
| `counts` | files, esdeveniments, vides, tipus, mostres, entitats per plantilla, armes, paquets llegits i no llegits, cada identificador de missatge vist i els que no s'han llegit, mostres descartades |
| `trackBreaks` | cada tall d'una trajectòria per un pas més ràpid del que pot anar la unitat: on, quant, quan de ràpid, i què és el més probable |
| `selfCheck` | les comprovacions de [Com llegeix una repetició](how-it-reads.md), calculades a cada conversió; `stepSpeed` dona per tipus la velocitat entre files consecutives d'una trajectòria tal com les uneix el visualitzador (mediana, percentil 99, la més alta, i els passos més ràpids del possible, que han de ser 0) |

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
