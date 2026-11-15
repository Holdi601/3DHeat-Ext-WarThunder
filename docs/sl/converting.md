---
title: Pretvorba posnetkov
nav_order: 4
lang: "sl"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Pretvorba posnetkov {#converting-replays}

Izhod: ena datoteka `.3dheat` na bitko (privzeto) ali ločene datoteke z
`--loose`.

## Korak za korakom {#step-by-step}

1. **Vklopite shranjevanje posnetkov.** War Thunder shranjuje posnetke odjemalca v mapo
   `Replays` v igri, kadar je shranjevanje posnetkov vklopljeno v njenih nastavitvah, na
   primer `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Strežniški posnetek, shranjen s strani posnetkov v igri (zip z `0000.wrpl`,
   `0001.wrpl`, ...), je mogoče pretvoriti prav tako.
2. **Odprite ukazno vrstico** v mapi, kamor smejo iti rezultati
   ([Preden začnete](before-you-start.md)).
3. **Pretvorite:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # datoteke, mape ali oboje
   heat3d-wt-replay battle.zip -o out              # zip strežniškega posnetka
   heat3d-wt-replay a.wrpl -o out --loose          # ločene datoteke namesto enega .3dheat
   ```

   `out` se ustvari v mapi, v kateri je vaša ukazna vrstica.
4. **Preberite, kaj piše.** Videti bi morali eno vrstico za vsako bitko.
5. **Odprite jo:** naložite `out/<map>/<match>.3dheat` v 3DHeat pregledovalnik
   ([Nalaganje ene datoteke](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Zagon na sintetičnem posnetku: en .3dheat, --loose, pokvarjena datoteka, prazna mapa](../assets/img/convert.svg)

Slika prikazuje zagon na posnetku, ki ga teste sestavijo v kodi (brez pravega posnetka,
brez namestitve igre):

- `ok <datoteka>`: bitka pretvorjena (z `--loose`: `ok <tabela> <dokument tekme>`);
- `failed <datoteka>: <zakaj>`: datoteke ni bilo mogoče prebrati (končno stanje 1; ostale
  se vseeno pretvorijo);
- `no .wrpl files given`: nič za pretvorbo (končno stanje 2);
- `note: ...`: na primer, da namestitev War Thunder za poimenovanje vozil ni bila najdena.

## Možnosti {#options}

| Možnost | Privzeto | Kaj počne |
|---|---|---|
| `replays` (ena ali več) | - | datoteke `.wrpl`, mape z njimi (sama mapa, ne njene podmape) ali zipi z njimi (strežniški posnetek: njegovi deli `.wrpl` se razpakirajo v začasno mapo) |
| `-o`, `--out` | obvezno | kam pisati: mapa za vsak zemljevid znotraj |
| `--game FOLDER` | najdeno | mapa War Thunder, katere besedilo poimenuje vozila, orožja in strelivo ter katere tabele ovrednotijo [gospodarstvo](economy.md); tudi `HEAT3D_WT_GAME` |
| `--no-smoothing` | izklopljeno | ohrani vzorce drugih enot, izračunane z mrtvim računanjem, in prejete vzorce, kot jih ima posnetek ([Mrtvo računanje](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | vklopljeno | vsako bitko zapakira v eno datoteko `.3dheat` |
| `--loose` | izklopljeno | vsako bitko ohrani kot ločene datoteke (tabela, dokument tekme, spremljevalne datoteke) |
| `--version` | - | izpiše `heat3d-wt-replay <version>` in se ustavi |
| `-h`, `--help` | - | izpiše možnosti in se ustavi |

Bitka, pretvorjena znova, se zapiše znova. Možnosti, kot jih izpiše program:
[Referenca ukazov](../cli-reference.md).

## Katere datoteke so ena bitka {#which-files-are-one-battle}

Vsaka bitka postane ena datoteka
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB in SB so
igrine kratke oblike za arkadne, realistične in simulatorske bitke; `<mode>` je način misije,
kot ga igra zapiše (`Conq4` Conquest #4, `Dom` Domination, `Bttl` Battle; glejte
[Način bitke](ground.md#battle-mode)); vsak del lahko izpustimo, kjer posnetek nobenega ne
navaja. Deli strežniškega posnetka (`0000.wrpl`, `0001.wrpl`, ...) se berejo skupaj kot ena
bitka; posnetek odjemalca in deli strežnika iste bitke sta dva posnetka in ostaneta dva.

## Končno stanje {#exit-status}

`0`, ko so bile vse bitke pretvorjene, `1`, ko je katera spodletela (ostale se vseeno
pretvorijo), `2`, ko med argumenti ni bilo najdene nobene datoteke posnetka.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
