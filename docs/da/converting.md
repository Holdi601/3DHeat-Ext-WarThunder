---
title: Konvertering af replays
nav_order: 4
lang: "da"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konvertering af replays {#converting-replays}

Resultat: én `.3dheat`-fil pr. kamp (standard), eller separate filer med
`--loose`.

## Trin for trin {#step-by-step}

1. **Slå replays til.** War Thunder gemmer klientreplays i spillets mappe `Replays`,
   når replay-gemning er slået til i dets indstillinger, for eksempel
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   En serverreplay, gemt fra spillets replay-side (en zip med `0000.wrpl`,
   `0001.wrpl`, ...), kan også konverteres.
2. **Åbn en terminal** i en mappe, hvor resultaterne må ligge
   ([Før du går i gang](before-you-start.md)).
3. **Konvertér:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # filer, mapper eller begge
   heat3d-wt-replay battle.zip -o out              # en serverreplays zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate filer i stedet for én .3dheat
   ```

   `out` oprettes i den mappe, din terminal står i.
4. **Læs hvad der står.** Du bør se én linje pr. kamp.
5. **Åbn den:** indlæs `out/<map>/<match>.3dheat` i 3DHeat-vieweren
   ([Indlæs én](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![En kørsel på en syntetisk replay: én .3dheat, --loose, en ødelagt fil, en tom mappe](../assets/img/convert.svg)

Billedet viser en kørsel på en replay, som testene bygger i kode (ingen rigtig
replay, ingen installation):

- `ok <file>`: en kamp konverteret (med `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: en fil, der ikke kunne læses (afslutningsstatus 1; de
  andre konverteres stadig);
- `no .wrpl files given`: intet at konvertere (afslutningsstatus 2);
- `note: ...`: for eksempel at ingen War Thunder-installation blev fundet til at
  navngive køretøjerne.

## Valgmuligheder {#options}

| Valg | Standard | Gør |
|---|---|---|
| `replays` (en eller flere) | - | `.wrpl`-filer, mapper med dem (selve mappen, ikke undermapper), eller zips med dem (en serverreplay: dens `.wrpl`-dele pakkes ud i en midlertidig mappe) |
| `-o`, `--out` | påkrævet | hvor der skrives: en mappe pr. kort indeni |
| `--game FOLDER` | fundet | War Thunder-mappen, hvis tekst navngiver køretøjer, våben og ammunition, og hvis tabeller prisfastsætter [økonomien](economy.md); også `HEAT3D_WT_GAME` |
| `--no-smoothing` | fra | behold andre enheders dead-reckoned og modtagne samples, som replayet har dem ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | til | pak hver kamp i én `.3dheat`-fil |
| `--loose` | fra | behold hver kamp som separate filer (tabel, kampdokument, sidecars) |
| `--version` | - | skriv `heat3d-wt-replay <version>` og stop |
| `-h`, `--help` | - | skriv valgmulighederne og stop |

En kamp, der konverteres igen, skrives igen. Valgmulighederne, som programmet
viser dem: [Kommandoreference](../cli-reference.md).

## Hvilke filer er én kamp {#which-files-are-one-battle}

Hver kamp bliver til én fil,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
og SB er spillets korte former for arkade-, realistiske og simulatorkampe;
`<mode>` er missionens tilstand, som spillet angiver den (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; se
[Kamptilstand](ground.md#battle-mode)); enhver del udelades, hvor replayet ikke
nævner den. En serverreplays dele (`0000.wrpl`, `0001.wrpl`, ...) læses sammen
som én kamp; en klientreplay og serverens dele af samme kamp er to optagelser og
forbliver to.

## Afslutningsstatus {#exit-status}

`0`, når hver kamp blev konverteret, `1`, når en af dem fejlede (de øvrige
konverteres stadig), `2`, når ingen replay-fil blev fundet blandt argumenterne.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
