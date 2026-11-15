---
title: "Konvertimi i riluajtjeve"
nav_order: 4
lang: sq
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konvertimi i riluajtjeve {#converting-replays}

Rezultati: një skedar `.3dheat` për çdo betejë (parazgjedhja), ose skedarë të
shkëputur me `--loose`.

## Hap pas hapi {#step-by-step}

1. **Ndiz riluajtjet.** War Thunder i ruan riluajtjet e klientit në dosjen `Replays`
   të lojës kur ruajtja e riluajtjeve është e ndezur te opsionet e saj, për shembull
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Mund të konvertohet edhe një riluajtje e serverit e ruajtur nga faqja e riluajtjeve të lojës
   (një zip me `0000.wrpl`, `0001.wrpl`, ...).
2. **Hap një terminal** në një dosje ku mund të shkojnë rezultatet
   ([Para se të fillosh](before-you-start.md)).
3. **Konverto:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` krijohet në dosjen ku është terminali yt.
4. **Lexo çfarë thotë.** Duhet të shohësh një rresht për çdo betejë.
5. **Hape:** ngarko `out/<map>/<match>.3dheat` në shikuesin 3DHeat
   ([Ngarkimi i njërit](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Një ekzekutim mbi një riluajtje sintetike: një .3dheat, --loose, një skedar i prishur, një dosje bosh](../assets/img/convert.svg)

Pamja është një ekzekutim mbi një riluajtje që testet e ndërtojnë në kod (nuk është
riluajtje e vërtetë, nuk ka instalim):

- `ok <file>`: një betejë u konvertua (me `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: një skedar që nuk u lexua dot (statusi i daljes 1; të
  tjerët konvertohen prapë);
- `no .wrpl files given`: nuk ka asgjë për të konvertuar (statusi i daljes 2);
- `note: ...`: për shembull që nuk u gjet instalim i War Thunder për t'i emërtuar
  mjetet.

## Opsionet {#options}

| Opsioni | Parazgjedhja | Çfarë bën |
|---|---|---|
| `replays` (një ose më shumë) | - | skedarë `.wrpl`, dosje me ta (vetë dosja, jo nëndosjet e saj), ose zip me ta (një riluajtje e serverit: pjesët e saj `.wrpl` shpaketohen në një dosje të përkohshme) |
| `-o`, `--out` | i detyrueshëm | ku të shkruhet: brenda tij një dosje për çdo hartë |
| `--game FOLDER` | gjendet | dosja e War Thunder, teksti i së cilës emërton mjetet, armët dhe municionet, dhe tabelat e së cilës vlerësojnë [ekonominë](economy.md); edhe `HEAT3D_WT_GAME` |
| `--no-smoothing` | joaktiv | mban mostrat e njësive të tjera të llogaritura me dead reckoning dhe të marra siç i ka riluajtja ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | aktiv | paketon çdo betejë në një skedar `.3dheat` |
| `--loose` | joaktiv | e mban çdo betejë si skedarë të veçantë (tabelë, dokument ndeshjeje, skedarë anësorë) |
| `--version` | - | printon `heat3d-wt-replay <version>` dhe ndalon |
| `-h`, `--help` | - | printon opsionet dhe ndalon |

Një betejë e konvertuar sërish shkruhet sërish. Opsionet siç i printon programi:
[Referenca e komandave](../cli-reference.md).

## Cilët skedarë janë një betejë {#which-files-are-one-battle}

Çdo betejë bëhet një skedar,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
dhe SB janë format e shkurtra të lojës për betejat arcade, realistic dhe simulator;
`<mode>` është mënyra e misionit siç e kodon loja (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; shih
[Mënyra e betejës](ground.md#battle-mode)); secila pjesë lihet jashtë kur
riluajtja nuk e emërton. Pjesët e një riluajtjeje të serverit (`0000.wrpl`, `0001.wrpl`, ...)
lexohen së bashku si një betejë; një riluajtje e klientit dhe pjesët e serverit për
të njëjtën betejë janë dy regjistrime dhe mbeten dy.

## Statusi i daljes {#exit-status}

`0` kur çdo betejë u konvertua, `1` kur ndonjëra dështoi (të tjerat konvertohen
prapë), `2` kur nuk u gjet asnjë skedar riluajtjeje midis argumenteve.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
