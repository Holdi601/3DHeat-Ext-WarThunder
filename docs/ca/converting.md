---
title: Conversió de repeticions
nav_order: 4
lang: "ca"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Conversió de repeticions {#converting-replays}

Sortida: un fitxer `.3dheat` per batalla (per defecte), o fitxers separats amb
`--loose`.

## Pas a pas {#step-by-step}

1. **Activa les repeticions.** War Thunder desa les repeticions de client a la
   carpeta `Replays` del joc quan el desament de repeticions és actiu a les seves
   opcions, per exemple
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Una repetició de servidor desada des de la pàgina de repeticions del joc (un zip
   amb `0000.wrpl`, `0001.wrpl`, ...) també es pot convertir.
2. **Obre un terminal** en una carpeta on puguin anar els resultats
   ([Abans de començar](before-you-start.md)).
3. **Converteix:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # fitxers, carpetes, o tots dos
   heat3d-wt-replay battle.zip -o out              # el zip d'una repetició de servidor
   heat3d-wt-replay a.wrpl -o out --loose          # fitxers separats en lloc d'un .3dheat
   ```

   `out` es crea a la carpeta on és el teu terminal.
4. **Llegeix què diu.** Hauries de veure una línia per batalla.
5. **Obre-la:** carrega `out/<mapa>/<partida>.3dheat` al visualitzador de 3DHeat
   ([Carregar-ne un](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Una execució sobre una repetició sintètica: un .3dheat, --loose, un fitxer trencat, una carpeta buida](../assets/img/convert.svg)

La imatge és una execució sobre una repetició que les proves construeixen en codi
(cap repetició real, cap instal·lació):

- `ok <fitxer>`: una batalla convertida (amb `--loose`: `ok <taula> <document de partida>`);
- `failed <fitxer>: <motiu>`: un fitxer que no s'ha pogut llegir (estat de sortida 1;
  les altres es converteixen igualment);
- `no .wrpl files given`: res a convertir (estat de sortida 2);
- `note: ...`: per exemple, que no s'ha trobat cap instal·lació de War Thunder per
  posar noms als vehicles.

## Opcions {#options}

| Opció | Per defecte | Fa |
|---|---|---|
| `replays` (una o més) | - | fitxers `.wrpl`, carpetes d'ells (la carpeta mateixa, no les subcarpetes), o zips d'ells (una repetició de servidor: les seves parts `.wrpl` es descomprimeixen en una carpeta temporal) |
| `-o`, `--out` | obligatòria | on escriure: una carpeta per mapa a dins |
| `--game CARPETA` | trobada | la carpeta de War Thunder amb el text que dona noms a vehicles, armes i munició, i les taules que valoren l'[economia](economy.md); també `HEAT3D_WT_GAME` |
| `--no-smoothing` | desactivada | mantén les mostres estimades i rebudes de les altres unitats tal com les té la repetició ([Estimació per navegació](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | activada | empaqueta cada batalla en un fitxer `.3dheat` |
| `--loose` | desactivada | mantén cada batalla com a fitxers separats (taula, document de partida, annexos) |
| `--version` | - | escriu `heat3d-wt-replay <versió>` i s'atura |
| `-h`, `--help` | - | escriu les opcions i s'atura |

Una batalla convertida de nou s'escriu de nou. Les opcions tal com les escriu el
programa: [Referència d'ordres](../cli-reference.md).

## Quins fitxers són una batalla {#which-files-are-one-battle}

Cada batalla esdevé un fitxer,
`out/<mapa>/<mapa>_<AB|RB|SB>_<mode>_<inici, UTC>_<id de sessió>.3dheat`. AB, RB
i SB són les formes curtes que fa servir el joc per a les batalles arcade, realistes
i de simulador; `<mode>` és el mode de la missió tal com el marca el joc (`Conq4`
Conquesta #4, `Dom` Dominació, `Bttl` Batalla; mira
[Mode de batalla](ground.md#battle-mode)); qualsevol de les dues parts es deixa fora
quan la repetició no en diu cap. Les parts d'una repetició de servidor (`0000.wrpl`,
`0001.wrpl`, ...) es llegeixen juntes com una sola batalla; una repetició de client i
les parts del servidor de la mateixa batalla són dues gravacions i es queden en dues.

## Estat de sortida {#exit-status}

`0` quan totes les batalles s'han convertit, `1` quan n'ha fallat alguna (les altres
es converteixen igualment), `2` quan no s'ha trobat cap fitxer de repetició entre
els arguments.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
