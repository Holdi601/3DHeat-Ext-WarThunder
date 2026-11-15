---
title: "Převod replayů"
nav_order: 4
lang: "cs"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Převod replayů {#converting-replays}

Výstup: jeden soubor `.3dheat` na bitvu (výchozí), nebo samostatné soubory s
`--loose`.

## Krok za krokem {#step-by-step}

1. **Zapněte ukládání replayů.** War Thunder ukládá replaye klienta do složky
   `Replays` ve hře, když je v jeho nastavení zapnuté ukládání replayů, například
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Serverový replay uložený ze stránky replayů ve hře (zip s `0000.wrpl`,
   `0001.wrpl`, ...) lze také převést.
2. **Otevřete terminál** ve složce, kam se mohou výsledky uložit
   ([Než začnete](before-you-start.md)).
3. **Převeďte:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # soubory, složky, nebo obojí
   heat3d-wt-replay battle.zip -o out              # zip serverového replaye
   heat3d-wt-replay a.wrpl -o out --loose          # samostatné soubory místo jednoho .3dheat
   ```

   `out` se vytvoří ve složce, ve které je váš terminál.
4. **Přečtěte si, co nástroj hlásí.** Uvidíte jeden řádek na bitvu.
5. **Otevřete výsledek:** načtěte `out/<map>/<match>.3dheat` v prohlížeči 3DHeat
   ([Načtení jednoho souboru](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Běh nad syntetickým replayem: jeden .3dheat, --loose, poškozený soubor, prázdná složka](../assets/img/convert.svg)

Obrázek ukazuje běh nad replayem, který testy vytvářejí v kódu (žádný skutečný
replay, žádná instalace):

- `ok <file>`: bitva převedena (s `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: soubor nešel přečíst (stav ukončení 1; ostatní se
  převedou dál);
- `no .wrpl files given`: nic k převodu (stav ukončení 2);
- `note: ...`: například že nebyla nalezena instalace War Thunder, podle které
  by se pojmenovala vozidla.

## Volby {#options}

| Volba | Výchozí | Co dělá |
|---|---|---|
| `replays` (jedna nebo více) | - | soubory `.wrpl`, složky s nimi (složka sama, ne její podsložky), nebo zipy s nimi (serverový replay: jeho části `.wrpl` se rozbalí do dočasné složky) |
| `-o`, `--out` | povinné | kam zapisovat: složka pro každou mapu uvnitř |
| `--game FOLDER` | najde se | složka War Thunder, jejíž texty pojmenovávají vozidla, zbraně a munici a jejíž tabulky oceňují [ekonomiku](economy.md); také `HEAT3D_WT_GAME` |
| `--no-smoothing` | vypnuto | ponechat vzorky jiných jednotek, dopočítané odhadem (dead reckoning) i přijaté, tak, jak je replay obsahuje ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | zapnuto | zabalit každou bitvu do jednoho souboru `.3dheat` |
| `--loose` | vypnuto | ponechat každou bitvu jako samostatné soubory (tabulka, dokument zápasu, doplňky) |
| `--version` | - | vypsat `heat3d-wt-replay <version>` a skončit |
| `-h`, `--help` | - | vypsat volby a skončit |

Bitva převedená znovu se zapíše znovu. Volby tak, jak je program vypisuje:
[Přehled příkazů](../cli-reference.md).

## Které soubory tvoří jednu bitvu {#which-files-are-one-battle}

Každá bitva se stane jedním souborem
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
a SB jsou zkratky hry pro arkadové, realistické a simulátorové bitvy;
`<mode>` je režim mise tak, jak ho hra označuje (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; viz
[Režim bitvy](ground.md#battle-mode)); kterákoli část se vynechá, pokud replay
žádnou neuvádí. Části serverového replaye (`0000.wrpl`, `0001.wrpl`, ...) se
čtou společně jako jedna bitva; nahrávka klienta a části serveru ze stejné
bitvy jsou dvě nahrávky a zůstanou dvěma.

## Stav ukončení {#exit-status}

`0`, když byla převedena každá bitva; `1`, když kterákoli selhala (ostatní se
převedou dál); `2`, když mezi argumenty nebyl nalezen žádný soubor replaye.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
