---
title: "Il-konverżjoni tar-ripetizzjonijiet"
nav_order: 4
lang: mt
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Il-konverżjoni tar-ripetizzjonijiet {#converting-replays}

Ħruġ: fajl `.3dheat` wieħed għal kull battalja (id-default), jew fajls separati
b'`--loose`.

## Pass pass {#step-by-step}

1. **Ixgħel ir-ripetizzjonijiet.** War Thunder isejvja ripetizzjonijiet tal-klijent fil-folder
   `Replays` tal-logħba meta s-saving tar-ripetizzjonijiet ikun mixgħul fl-għażliet tagħha,
   pereżempju `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Ripetizzjoni tas-server misjuva mill-paġna tar-ripetizzjonijiet tal-logħba (zip b'`0000.wrpl`,
   `0001.wrpl`, ...) tista' tiġi kkonvertita wkoll.
2. **Iftaħ terminal** f'folder fejn ir-riżultati jistgħu jmorru
   ([Qabel ma tibda](before-you-start.md)).
3. **Ikkonverti:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` jinħoloq fil-folder fejn ikun it-terminal tiegħek.
4. **Aqra dak li jgħid.** Għandek tara linja waħda għal kull battalja.
5. **Iftaħha:** ikkarga `out/<map>/<match>.3dheat` fid-3DHeat viewer
   ([Loading one](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Tħaddim fuq ripetizzjoni sintetika: .3dheat wieħed, --loose, fajl miksur, folder vojt](../assets/img/convert.svg)

L-istampa hija tħaddim fuq ripetizzjoni li t-testijiet jibnu fil-kodiċi (mhux ripetizzjoni vera,
mhux installazzjoni):

- `ok <file>`: battalja kkonvertita (b'`--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: fajl li ma setax jinqara (status tal-ħruġ 1; l-oħrajn jiġu
  kkonvertiti xorta);
- `no .wrpl files given`: xejn x'tikkonverti (status tal-ħruġ 2);
- `note: ...`: pereżempju li ma nstabet ebda installazzjoni ta' War Thunder biex tingħata isem il-vetturi.

## Għażliet {#options}

| Għażla | Default | Tagħmel |
|---|---|---|
| `replays` (waħda jew aktar) | - | fajls `.wrpl`, folders tagħhom (il-folder nnifsu, mhux is-subfolders), jew zips tagħhom (ripetizzjoni tas-server: il-partijiet `.wrpl` tagħha jinfetħu f'folder temporanju) |
| `-o`, `--out` | meħtieġa | fejn jinkiteb: folder għal kull mappa ġewwa |
| `--game FOLDER` | misjub | il-folder ta' War Thunder li t-test tiegħu jagħti ismijiet lill-vetturi, lill-armi u lill-munizzjon, u li t-tabelli tiegħu jipprezzaw l-[ekonomija](economy.md); ukoll `HEAT3D_WT_GAME` |
| `--no-smoothing` | mitfi | iżomm il-kampjuni dead-reckoned u riċevuti ta' unitajiet oħra kif għandha r-ripetizzjoni ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | mixgħul | ippakkja kull battalja f'fajl `.3dheat` wieħed |
| `--loose` | mitfi | żomm kull battalja bħala fajls separati (tabella, dokument tal-partita, sidecars) |
| `--version` | - | jistampa `heat3d-wt-replay <version>` u jieqaf |
| `-h`, `--help` | - | jistampa l-għażliet u jieqaf |

Battalja kkonvertita mill-ġdid tinkiteb mill-ġdid. L-għażliet kif jistampahom il-programm:
[Referenza tal-kmandi](../cli-reference.md).

## Liema fajls huma battalja waħda {#which-files-are-one-battle}

Kull battalja ssir fajl wieħed,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
u SB huma l-forom qosra tal-logħba għall-battaljiet arcade, realistic u simulator;
`<mode>` hija l-modalità tal-missjoni kif jikkjaviha l-logħba (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; ara
[Battle mode](ground.md#battle-mode)); kull parti titħalla barra fejn ir-ripetizzjoni
ma ssemmi ebda waħda. Il-partijiet ta' ripetizzjoni tas-server (`0000.wrpl`, `0001.wrpl`, ...)
jinqraw flimkien bħala battalja waħda; ripetizzjoni tal-klijent u l-partijiet tas-server
tal-istess battalja huma żewġ reġistrazzjonijiet u jibqgħu tnejn.

## Status tal-ħruġ {#exit-status}

`0` meta kull battalja ġiet ikkonvertita, `1` meta xi waħda falliet (l-oħrajn jiġu
kkonvertiti xorta), `2` meta ma nstab ebda fajl ta' ripetizzjoni fost l-argumenti.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
