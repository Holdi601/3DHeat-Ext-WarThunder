---
title: "Upptökum breytt"
nav_order: 4
lang: "is"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Upptökum breytt {#converting-replays}

Úttak: ein `.3dheat` skrá fyrir hvern bardaga (sjálfgefið), eða lausar skrár
með `--loose`.

## Skref fyrir skref {#step-by-step}

1. **Kveiktu á upptökum.** War Thunder vistar biðlaraupptökur í möppunni
   `Replays` í leiknum þegar kveikt er á vistun upptaka í stillingum hans, til
   dæmis `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Þjónsupptöku sem vistuð er af upptökusíðu leiksins (zip með `0000.wrpl`,
   `0001.wrpl`, ...) er líka hægt að breyta.
2. **Opnaðu skipanalínu** í möppu þar sem niðurstöðurnar mega fara
   ([Áður en þú byrjar](before-you-start.md)).
3. **Breyttu:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` er búin til í möppunni sem skipanalínan þín er í.
4. **Lestu það sem hún segir.** Þú ættir að sjá eina línu fyrir hvern bardaga.
5. **Opnaðu það:** hladdu `out/<map>/<match>.3dheat` í 3DHeat-skoðaranum
   ([Að hlaða einni](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Keyrsla á tilbúinni upptöku: ein .3dheat, --loose, skemmd skrá, tóm mappa](../assets/img/convert.svg)

Myndin er keyrsla á upptöku sem prófanirnar smíða í kóða (engin raunveruleg
upptaka, engin uppsetning):

- `ok <file>`: bardagi breyttur (með `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: skrá sem ekki var hægt að lesa (útgöngustaða 1; hinar
  eru samt sem áður breyttar);
- `no .wrpl files given`: ekkert til að breyta (útgöngustaða 2);
- `note: ...`: til dæmis að engin War Thunder uppsetning fannst til að nefna
  farartækin.

## Valkostir {#options}

| Valkostur | Sjálfgefið | Gerir |
|---|---|---|
| `replays` (ein eða fleiri) | - | `.wrpl` skrár, möppur með þeim (sjálf mappan, ekki undirmöppur hennar), eða zip með þeim (þjónsupptaka: `.wrpl` hlutar hennar eru pakkaðir upp í tímabundna möppu) |
| `-o`, `--out` | nauðsynlegt | hvert á að skrifa: mappa fyrir hvert kort inni í henni |
| `--game FOLDER` | fundið | War Thunder mappan sem textinn nefnir farartæki, vopn og skotfæri úr og sem töflur verðleggja [hagkerfið](economy.md) með; einnig `HEAT3D_WT_GAME` |
| `--no-smoothing` | slökkt | halda reiknuðum og mótteknum sýnum annarra eininga eins og upptakan hefur þau ([Ágiskun á stöðu](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | kveikt | pakka hverjum bardaga í eina `.3dheat` skrá |
| `--loose` | slökkt | halda hverjum bardaga sem aðskildum skrám (tafla, leikjaskjal, hliðarskrár) |
| `--version` | - | prenta `heat3d-wt-replay <version>` og stoppa |
| `-h`, `--help` | - | prenta valkostina og stoppa |

Bardagi sem er breytt aftur er skrifaður aftur. Valkostirnir eins og forritið
prentar þá: [Skipanayfirlit](../cli-reference.md).

## Hvaða skrár eru einn bardagi {#which-files-are-one-battle}

Hver bardagi verður ein skrá,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
og SB eru stuttar myndir leiksins af arcade-, realistic- og simulator-bardögum;
`<mode>` er hamur verkefnisins eins og leikurinn lykilar hann (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; sjá
[Bardagahamur](ground.md#battle-mode)); hvor hluti er felldur niður þar sem
upptakan nefnir engan. Hlutar þjónsupptöku (`0000.wrpl`, `0001.wrpl`, ...) eru
lesnir saman sem einn bardagi; biðlaraupptaka og þjónshlutar sama bardaga eru
tvær upptökur og haldast tvær.

## Útgöngustaða {#exit-status}

`0` þegar allir bardagar voru breyttir, `1` þegar einhver mistókst (hinir eru
samt breyttir), `2` þegar engin upptökuskrá fannst meðal röksemdanna.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
