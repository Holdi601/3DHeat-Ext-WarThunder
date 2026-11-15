---
title: "Replays omzetten"
nav_order: 4
lang: nl
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Replays omzetten {#converting-replays}

Uitvoer: één `.3dheat`-bestand per gevecht (de standaard), of losse bestanden met
`--loose`.

## Stap voor stap {#step-by-step}

1. **Zet replays aan.** War Thunder slaat client-replays op in de map `Replays`
   van het spel, als het opslaan van replays aan staat in de opties, bijvoorbeeld
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Een server-replay die je via de replaypagina van het spel opslaat (een zip met `0000.wrpl`,
   `0001.wrpl`, ...) kun je ook omzetten.
2. **Open een terminal** in een map waarin de resultaten mogen komen
   ([Voordat je begint](before-you-start.md)).
3. **Zet om:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # bestanden, mappen, of beide
   heat3d-wt-replay battle.zip -o out              # de zip van een server-replay
   heat3d-wt-replay a.wrpl -o out --loose          # losse bestanden in plaats van één .3dheat
   ```

   `out` wordt aangemaakt in de map waarin je terminal staat.
4. **Lees wat er staat.** Je ziet één regel per gevecht.
5. **Open het:** laad `out/<map>/<match>.3dheat` in de 3DHeat-viewer
   ([Een bestand laden](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Een run op een synthetische replay: één .3dheat, --loose, een kapot bestand, een lege map](../assets/img/convert.svg)

De afbeelding is een run op een replay die de tests in code opbouwen (geen echte replay,
geen installatie):

- `ok <bestand>`: een gevecht is omgezet (met `--loose`: `ok <tabel> <wedstrijddocument>`);
- `failed <bestand>: <waarom>`: een bestand dat niet gelezen kon worden (afsluitstatus 1; de
  rest wordt wel omgezet);
- `no .wrpl files given`: niets om om te zetten (afsluitstatus 2);
- `note: ...`: bijvoorbeeld dat er geen installatie van War Thunder gevonden is om de
  voertuigen een naam te geven.

## Opties {#options}

| Optie | Standaard | Doet |
|---|---|---|
| `replays` (één of meer) | - | `.wrpl`-bestanden, mappen daarvan (de map zelf, niet de submappen), of zips daarvan (een server-replay: de `.wrpl`-delen worden uitgepakt naar een tijdelijke map) |
| `-o`, `--out` | verplicht | waarheen schrijven: een map per kaart erin |
| `--game MAP` | gevonden | de map van War Thunder waarvan de tekst voertuigen, wapens en munitie benoemt, en waarvan de tabellen de [economie](economy.md) prijzen; ook `HEAT3D_WT_GAME` |
| `--no-smoothing` | uit | houd de dead-reckoned en ontvangen samples van andere eenheden zoals de replay ze heeft ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | aan | pak elk gevecht in één `.3dheat`-bestand |
| `--loose` | uit | bewaar elk gevecht als losse bestanden (tabel, wedstrijddocument, sidecars) |
| `--version` | - | toon `heat3d-wt-replay <versie>` en stop |
| `-h`, `--help` | - | toon de opties en stop |

Een gevecht dat opnieuw wordt omgezet, wordt opnieuw geschreven. De opties zoals het
programma ze toont: [Opdrachtreferentie](../cli-reference.md).

## Welke bestanden horen bij één gevecht {#which-files-are-one-battle}

Elk gevecht wordt één bestand,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<sessie-id>.3dheat`. AB, RB
en SB zijn de korte vormen die het spel gebruikt voor arcade-, realistische en
simulatorgevechten; `<mode>` is de modus van de missie zoals het spel die aanduidt (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; zie [Gevechtsmodus](ground.md#battle-mode));
een van beide delen wordt weggelaten waar de replay er geen noemt. De delen van een server-replay
(`0000.wrpl`, `0001.wrpl`, ...) worden samen gelezen als één gevecht; een client-replay en de
delen van de server van hetzelfde gevecht zijn twee opnamen en blijven twee.

## Afsluitstatus {#exit-status}

`0` als elk gevecht is omgezet, `1` als er één is mislukt (de rest wordt wel
omgezet), `2` als er tussen de argumenten geen replaybestand is gevonden.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
