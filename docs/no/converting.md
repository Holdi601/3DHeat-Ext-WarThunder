---
title: "Konvertere replayer"
nav_order: 4
lang: no
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konvertere replayer {#converting-replays}

Resultat: én `.3dheat`-fil per slag (standard), eller separate filer med
`--loose`.

## Steg for steg {#step-by-step}

1. **Slå på replayer.** War Thunder lagrer klientreplayer i mappen `Replays` i
   spillet når lagring av replay er på i innstillingene, for eksempel
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   En serverreplay lagret fra spillets replay-side (en zip med `0000.wrpl`,
   `0001.wrpl`, ...) kan også konverteres.
2. **Åpne en terminal** i en mappe der resultatene kan havne
   ([Før du starter](before-you-start.md)).
3. **Konverter:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # filer, mapper, eller begge
   heat3d-wt-replay battle.zip -o out              # en serverreplays zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate filer i stedet for én .3dheat
   ```

   `out` lages i mappen terminalen står i.
4. **Les hva den sier.** Du bør se én linje per slag.
5. **Åpne den:** last `out/<kart>/<kamp>.3dheat` i 3DHeat-visningsprogrammet
   ([Laste én](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![En kjøring på en syntetisk replay: én .3dheat, --loose, en ødelagt fil, en tom mappe](../assets/img/convert.svg)

Bildet viser en kjøring på en replay som testene lager i kode (ingen ekte replay,
ingen installasjon):

- `ok <fil>`: et slag konvertert (med `--loose`: `ok <tabell> <kampdokument>`);
- `failed <fil>: <årsak>`: en fil som ikke kunne leses (exit-status 1; de andre
  konverteres likevel);
- `no .wrpl files given`: ingenting å konvertere (exit-status 2);
- `note: ...`: for eksempel at ingen War Thunder-installasjon ble funnet for å
  navngi kjøretøyene.

## Valg {#options}

| Valg | Standard | Gjør |
|---|---|---|
| `replays` (én eller flere) | - | `.wrpl`-filer, mapper med dem (selve mappen, ikke undermappene), eller zip-filer med dem (en serverreplay: delene `.wrpl` pakkes ut til en midlertidig mappe) |
| `-o`, `--out` | påkrevd | hvor det skrives: en mappe per kart inni |
| `--game MAPPE` | funnet | War Thunder-mappen som har teksten som navngir kjøretøy, våpen og ammunisjon, og hvis tabeller prisetter [økonomien](economy.md); også `HEAT3D_WT_GAME` |
| `--no-smoothing` | av | behold andre enheters dead reckoning- og mottatte samples slik replayen har dem ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | på | pakk hvert slag i én `.3dheat`-fil |
| `--loose` | av | behold hvert slag som separate filer (tabell, kampdokument, sidefiler) |
| `--version` | - | skriv `heat3d-wt-replay <versjon>` og stopp |
| `-h`, `--help` | - | skriv ut valgene og stopp |

Et slag som konverteres på nytt, skrives på nytt. Valgene slik programmet skriver
dem ut: [Kommandoreferanse](../cli-reference.md).

## Hvilke filer er ett slag {#which-files-are-one-battle}

Hvert slag blir én fil,
`out/<kart>/<kart>_<AB|RB|SB>_<modus>_<start, UTC>_<økt-id>.3dheat`. AB, RB
og SB er spillets korte former for arkade-, realistiske og simulatorslag;
`<modus>` er oppdragets modus slik spillet nøkler den (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; se
[Kampmodus](ground.md#battle-mode)); enhver av delene utelates der replayen ikke
oppgir noen. Delene av en serverreplay (`0000.wrpl`, `0001.wrpl`, ...) leses
sammen som ett slag; en klientreplay og serverens deler av samme slag er to
opptak og forblir to.

## Exit-status {#exit-status}

`0` når alle slag ble konvertert, `1` når noen mislyktes (de andre konverteres
likevel), `2` når ingen replayfil ble funnet blant argumentene.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
