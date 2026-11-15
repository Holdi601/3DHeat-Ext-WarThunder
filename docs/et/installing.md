---
title: Paigaldamine
nav_order: 3
lang: "et"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Paigaldamine {#installing}

Uus käsurea kasutamisel? Loe esmalt [Enne alustamist](before-you-start.md).
Vajab Pythonit 3.10 või uuemat; pyarrow, numpy, zstandard ja Pillow paigaldatakse
koos sellega.

## Samm-sammult {#step-by-step}

1. Hangi kood: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`
   või laadi zip alla lehelt [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   ja paki lahti.
2. Ava terminal selles kaustas ja kirjuta `pip install -e .`. See paigaldab kaks
   käsku: `heat3d-wt-replay` (kordused) ja `heat3d-wt-level` (tasemed).
3. Kontrolli: `heat3d-wt-replay --version`. Peaksid nägema
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` loetleb valikud:

![heat3d-wt-replay --help](../assets/img/help.svg)

Ilma paigaldamata: `python -m heat3d_ext_warthunder ...` ja
`python -m heat3d_ext_warthunder.levelcli ...` tööriista kaustas.

## Nimed sinu installatsioonist {#names-from-your-install}

Sõidukid, relvad ja laskemoon saavad oma inglisekeelsed nimed mängu enda
tekstifailidest, mis loetakse konverteerimisel sinu installatsioonist. Installatsioon
leitakse Steami või käivitaja vaikekaustadest; `--game <kaust>` või
keskkonnamuutuja `HEAT3D_WT_GAME` ütlevad, kus see muidu on. Mängu teksti ei ole
selles hoidlas; ilma installatsioonita on nimed sõidukite ID-d (konverter ütleb
seda reaga `note:`).

## Uuendused {#updates}

Iga käivitamine kontrollib kõigepealt projekti GitHubi väljalaske (kõige rohkem
üks päring iga paari tunni tagant; see ei peata kunagi konverteerimist, ka siis, kui võrku ei ole). Kui on ilmunud uuem väljalase, küsib käsk enne paigaldamist: `git clone`
uuendatakse käsuga `git pull --ff-only` (keeldub, kui sul on lokaalseid muudatusi); allalaaditud koopia uuendatakse väljalaske arhiivist. `HEAT3D_NO_UPDATE=1` lülitab kontrolli ja
uuendamise välja.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
