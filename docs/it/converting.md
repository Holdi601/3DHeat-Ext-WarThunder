---
title: "Conversione dei replay"
nav_order: 4
lang: "it"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Conversione dei replay {#converting-replays}

Output: un file `.3dheat` per battaglia (predefinito), oppure file separati con
`--loose`.

## Passo dopo passo {#step-by-step}

1. **Attiva il salvataggio dei replay.** War Thunder salva i replay del client nella cartella
   `Replays` del gioco quando il salvataggio dei replay è attivo nelle sue opzioni, per esempio
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Si può convertire anche un replay del server salvato dalla pagina dei replay del gioco (uno zip con `0000.wrpl`,
   `0001.wrpl`, ...).
2. **Apri un terminale** in una cartella dove possono finire i risultati
   ([Prima di iniziare](before-you-start.md)).
3. **Converti:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # file, cartelle, o entrambi
   heat3d-wt-replay battle.zip -o out              # lo zip di un replay del server
   heat3d-wt-replay a.wrpl -o out --loose          # file separati invece di un .3dheat
   ```

   `out` viene creata nella cartella in cui si trova il terminale.
4. **Leggi cosa dice.** Dovresti vedere una riga per battaglia.
5. **Aprila:** carica `out/<map>/<match>.3dheat` nel visualizzatore 3DHeat
   ([Caricarne uno](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Un'esecuzione su un replay sintetico: un .3dheat, --loose, un file rotto, una cartella vuota](../assets/img/convert.svg)

L'immagine mostra un'esecuzione su un replay che i test creano nel codice (nessun replay reale,
nessuna installazione):

- `ok <file>`: una battaglia convertita (con `--loose`: `ok <tabella> <documento della partita>`);
- `failed <file>: <motivo>`: un file che non si può leggere (stato di uscita 1; gli
  altri vengono comunque convertiti);
- `no .wrpl files given`: nulla da convertire (stato di uscita 2);
- `note: ...`: per esempio che non è stata trovata nessuna installazione di War Thunder per dare i nomi ai
  veicoli.

## Opzioni {#options}

| Opzione | Predefinito | Cosa fa |
|---|---|---|
| `replays` (uno o più) | - | file `.wrpl`, cartelle di file `.wrpl` (la cartella stessa, non le sue sottocartelle), o zip di questi (un replay del server: le sue parti `.wrpl` vengono decompresse in una cartella temporanea) |
| `-o`, `--out` | obbligatoria | dove scrivere: una cartella per mappa al suo interno |
| `--game CARTELLA` | trovata | la cartella di War Thunder il cui testo dà i nomi a veicoli, armi e munizioni, e le cui tabelle danno il prezzo all'[economia](economy.md); anche `HEAT3D_WT_GAME` |
| `--no-smoothing` | disattivata | mantieni i campioni stimati e ricevuti delle altre unità come sono nel replay ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | attiva | raccoglie ogni battaglia in un file `.3dheat` |
| `--loose` | disattivata | mantieni ogni battaglia come file separati (tabella, documento della partita, file accessori) |
| `--version` | - | stampa `heat3d-wt-replay <versione>` e si ferma |
| `-h`, `--help` | - | stampa le opzioni e si ferma |

Una battaglia convertita di nuovo viene riscritta. Le opzioni come le stampa il programma:
[Riferimento dei comandi](../cli-reference.md).

## Quali file sono una battaglia {#which-files-are-one-battle}

Ogni battaglia diventa un file,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
e SB sono le sigle del gioco per le battaglie arcade, realistiche e simulatore;
`<mode>` è la modalità della missione come la indica il gioco (`Conq4`
Conquista #4, `Dom` Dominio, `Bttl` Battaglia; vedi
[Modalità di battaglia](ground.md#battle-mode)); ciascuna delle due parti viene omessa se il replay non ne indica nessuna.
Le parti di un replay del server (`0000.wrpl`, `0001.wrpl`, ...)
vengono lette insieme come una battaglia; un replay del client e le parti del server
della stessa battaglia sono due registrazioni e restano due.

## Codice di uscita {#exit-status}

`0` quando ogni battaglia è stata convertita, `1` quando una è fallita (le altre vengono
comunque convertite), `2` quando tra gli argomenti non è stato trovato nessun file di replay.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
