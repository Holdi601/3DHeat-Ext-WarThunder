---
title: "Konverzia replayov"
nav_order: 4
lang: "sk"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Konverzia replayov {#converting-replays}

Výstup je jeden súbor `.3dheat` na bitku (predvolene), alebo samostatné súbory
s `--loose`.

## Krok za krokom {#step-by-step}

1. **Zapnite ukladanie replayov.** War Thunder ukladá replaye klienta do priečinka
   `Replays` hry, ak je ukladanie replayov zapnuté v jej nastaveniach, napríklad
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Serverový replay uložený zo stránky replayov hry (zip so `0000.wrpl`,
   `0001.wrpl`, ...) sa dá konvertovať tiež.
2. **Otvorte terminál** v priečinku, kam sa môžu uložiť výsledky (
   [Než začnete](before-you-start.md)).
3. **Konvertujte:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # súbory, priečinky alebo oboje
   heat3d-wt-replay battle.zip -o out              # zip serverového replaye
   heat3d-wt-replay a.wrpl -o out --loose          # samostatné súbory namiesto jedného .3dheat
   ```

   `out` sa vytvorí v priečinku, v ktorom je váš terminál.
4. **Prečítajte si, čo program hlási.** Mali by ste vidieť jeden riadok na bitku.
5. **Otvorte ho:** načítajte `out/<map>/<match>.3dheat` do 3DHeat prehliadača
   ([Načítanie jedného](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Beh na syntetickom replaye: jeden .3dheat, --loose, pokazený súbor, prázdny priečinok](../assets/img/convert.svg)

Obrázok je beh na replaye, ktorý testy vytvoria v kóde (žiadny skutočný replay,
žiadna inštalácia):

- `ok <file>`: bitka je prekonvertovaná (s `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: súbor sa nedal prečítať (návratový stav 1; ostatné
  sa prekonvertujú);
- `no .wrpl files given`: nič na konverziu (návratový stav 2);
- `note: ...`: napríklad že sa nenašla inštalácia War Thunderu na pomenovanie
  vozidiel.

## Možnosti {#options}

| Možnosť | Predvolené | Čo robí |
|---|---|---|
| `replays` (jeden alebo viac) | - | súbory `.wrpl`, priečinky s nimi (samotný priečinok, nie jeho podpriečinky), alebo zipy s nimi (serverový replay: jeho `.wrpl` časti sa rozbalia do dočasného priečinka) |
| `-o`, `--out` | povinné | kam zapisovať: priečinok pre každú mapu vnútri |
| `--game FOLDER` | nájde sa | priečinok War Thunderu, z ktorého sa berú texty vozidiel, zbraní a munície a tabuľky, ktoré oceňujú [ekonomiku](economy.md); aj `HEAT3D_WT_GAME` |
| `--no-smoothing` | vypnuté | nechať vzorky iných jednotiek, dopočítané aj prijaté, tak, ako sú v replaye ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | zapnuté | zabaliť každú bitku do jedného súboru `.3dheat` |
| `--loose` | vypnuté | uchovať každú bitku ako samostatné súbory (tabuľka, dokument zápasu, sprievodné súbory) |
| `--version` | - | vypísať `heat3d-wt-replay <version>` a skončiť |
| `-h`, `--help` | - | vypísať možnosti a skončiť |

Bitka skonvertovaná znova sa zapíše znova. Možnosti tak, ako ich program vypisuje:
[Referencia príkazov](../cli-reference.md).

## Ktoré súbory sú jedna bitka {#which-files-are-one-battle}

Každá bitka sa stane jedným súborom
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
a SB sú skrátené tvary hry pre arkádové, realistické a simulátorové bitky;
`<mode>` je režim misie tak, ako ho hra označuje (`Conq4` Conquest #4, `Dom`
Domination, `Bttl` Battle; pozri [Režim bitky](ground.md#battle-mode)); ktorúkoľvek
časť vynecháme tam, kde replay žiadnu neuvádza. Časti serverového replaye
(`0000.wrpl`, `0001.wrpl`, ...) sa čítajú spolu ako jedna bitka; klientský replay
a serverové časti tej istej bitky sú dva záznamy a ostanú dva.

## Návratový stav {#exit-status}

`0`, keď sa prekonvertovali všetky bitky; `1`, keď zlyhala aspoň jedna (ostatné
sa aj tak prekonvertujú); `2`, keď medzi argumentmi nebol nájdený žiadny súbor replaye.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
