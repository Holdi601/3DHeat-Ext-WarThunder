---
title: "Konvertera repriser"
nav_order: 4
lang: sv
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konvertera repriser {#converting-replays}

Resultatet är en `.3dheat`-fil per strid (standard), eller lösa filer med
`--loose`.

## Steg för steg {#step-by-step}

1. **Slå på repriser.** War Thunder sparar klientrepriser i spelets mapp `Replays`
   när repriser-sparande är påslaget i dess inställningar, till exempel
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   En serverrepris sparad från spelets repriser-sida (en zip med `0000.wrpl`,
   `0001.wrpl`, ...) kan också konverteras.
2. **Öppna en terminal** i en mapp dit resultaten får skrivas
   ([Innan du börjar](before-you-start.md)).
3. **Konvertera:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # filer, mappar, eller både och
   heat3d-wt-replay battle.zip -o out              # en serverrepris zip
   heat3d-wt-replay a.wrpl -o out --loose          # separata filer i stället för en .3dheat
   ```

   `out` skapas i mappen din terminal står i.
4. **Läs vad den skriver.** Du bör se en rad per strid.
5. **Öppna den:** ladda `out/<map>/<match>.3dheat` i 3DHeat-visaren
   ([Ladda en fil](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![En körning på en syntetisk repris: en .3dheat, --loose, en trasig fil, en tom mapp](../assets/img/convert.svg)

Bilden är en körning på en repris som testerna bygger i kod (ingen riktig repris,
ingen installation):

- `ok <file>`: en strid konverterad (med `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: en fil som inte kunde läsas (exitstatus 1; de andra
  konverteras ändå);
- `no .wrpl files given`: inget att konvertera (exitstatus 2);
- `note: ...`: till exempel att ingen War Thunder-installation hittades för att
  namnge fordonen.

## Alternativ {#options}

| Alternativ | Standard | Gör |
|---|---|---|
| `replays` (en eller flera) | - | `.wrpl`-filer, mappar med sådana (mappen själv, inte dess undermappar), eller zip-filer med dem (en serverrepris: dess `.wrpl`-delar packas upp till en tillfällig mapp) |
| `-o`, `--out` | krävs | var det skrivs: en mapp per karta inuti |
| `--game MAPP` | hittas | War Thunder-mappen vars text namnger fordon, vapen och ammunition, och vars tabeller prissätter [ekonomin](economy.md); även `HEAT3D_WT_GAME` |
| `--no-smoothing` | av | behåll andra enheters dead reckoning och mottagna mätpunkter som repriserna har dem ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | på | packa varje strid i en `.3dheat`-fil |
| `--loose` | av | behåll varje strid som separata filer (tabell, matchdokument, sidofiler) |
| `--version` | - | skriv `heat3d-wt-replay <version>` och stanna |
| `-h`, `--help` | - | skriv alternativen och stanna |

En strid som konverteras igen skrivs om. Alternativen så som programmet skriver
dem: [Kommandoreferens](../cli-reference.md).

## Vilka filer som är en strid {#which-files-are-one-battle}

Varje strid blir en fil,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
och SB är spelets korta former för arkad-, realistiska och simulatorstrider;
`<mode>` är uppdragets läge så som spelet nycklar det (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; se
[Stridsläge](ground.md#battle-mode)); någon del utelämnas där repriser inte anger
den. En serverrepris delar (`0000.wrpl`, `0001.wrpl`, ...) läses ihop som en strid;
en klientrepris och serverdelarna av samma strid är två inspelningar och förblir två.

## Exitstatus {#exit-status}

`0` när varje strid konverterades, `1` när någon misslyckades (de övriga konverteras
ändå), `2` när ingen repris-fil hittades bland argumenten.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
