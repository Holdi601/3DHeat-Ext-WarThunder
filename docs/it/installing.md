---
title: "Installazione"
nav_order: 3
lang: "it"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installazione {#installing}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).
Serve Python 3.10 o successivo; pyarrow, numpy, zstandard e Pillow vengono
installati con esso.

## Passo dopo passo {#step-by-step}

1. Scarica il codice: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   oppure scarica uno zip da [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   e decomprimilo.
2. Apri un terminale in quella cartella e scrivi `pip install -e .`. Questo installa
   due comandi: `heat3d-wt-replay` (replay) e `heat3d-wt-level` (livelli).
3. Verifica: `heat3d-wt-replay --version`. Dovresti vedere
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` elenca le opzioni:

![heat3d-wt-replay --help](../assets/img/help.svg)

Senza installare: `python -m heat3d_ext_warthunder ...` e
`python -m heat3d_ext_warthunder.levelcli ...` nella cartella dello strumento.

## Nomi dalla tua installazione {#names-from-your-install}

Veicoli, armi e munizioni ricevono i nomi in inglese dai file di testo del
gioco, letti dalla tua installazione durante la conversione. L'installazione viene
trovata tramite Steam o le cartelle predefinite del launcher; `--game <cartella>` o la
variabile d'ambiente `HEAT3D_WT_GAME` indicano dove trovarla. Nel
repository non c'è nessun testo del gioco; senza installazione i nomi sono gli
ID dei veicoli (il convertitore lo segnala con una riga `note:`).

## Aggiornamenti {#updates}

Ogni avvio controlla prima le release GitHub del progetto (al massimo una richiesta
ogni poche ore; non blocca mai una conversione, che sia online o no). Quando è
uscita una release più recente, il comando chiede prima di installarla: un clone `git`
viene aggiornato con `git pull --ff-only` (rifiutato se hai modifiche locali),
una copia scaricata dall'archivio della release. `HEAT3D_NO_UPDATE=1` disattiva
il controllo e l'aggiornamento.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
