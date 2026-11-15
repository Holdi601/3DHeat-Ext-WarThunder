---
title: "Qabel ma tibda"
nav_order: 2
lang: mt
source: before-you-start.md
source_hash: "99034fb56b0d"
nav_exclude: true
search_exclude: true
---
# Qabel ma tibda {#before-you-start}

Ġdid mal-linja tal-kmandi? Din il-paġna tieħdok minn xejn sa `heat3d-wt-replay`
li jaħdem f'madwar għaxar minuti. Jekk diġà tuża Python, mur direttament għal
[Installazzjoni](installing.md).

## 1. Installa Python {#install-python}

1. Niżżel Python **3.10 jew aktar ġdid** minn
   [python.org/downloads](https://www.python.org/downloads/).
2. Fuq Windows, immarka **Add python.exe to PATH** fl-ewwel tieqa tal-installer,
   imbagħad ikklikkja **Install Now**.
3. Fuq macOS u Linux, Python 3 ħafna drabi jkun diġà hemm. Ikteb `python3`
   kull fejn dawn il-paġni jgħidu `python`, u `pip3` minflok `pip`.

## 2. Iftaħ terminal {#open-a-terminal}

Terminal huwa tieqa fejn tikteb kmandi.

- **Windows:** iftaħ il-folder fil-File Explorer, ikklikkja fuq il-bar tal-indirizz,
  ikteb `cmd` u agħfas Enter. Tiftaħ tieqa li diġà tkun f'dak il-folder.
- **macOS:** iftaħ l-app **Terminal**. **Linux:** ikklikkja bil-lemin fil-folder
  u agħżel **Open in Terminal**.

Biex tmur f'folder ieħor, ikteb `cd` u l-folder:

```bash
cd "C:\Users\you\Downloads\3DHeat-Ext-WarThunder-main"
```

## 3. Iċċekkja li Python jaħdem {#check-that-python-works}

```bash
python --version
```

Għandek tara `Python 3.` u numru ta' 10 jew aktar, pereżempju
`Python 3.12.4`.

## 4. Ġib l-għodda u installaha {#get-the-tool-and-install-it}

1. Fuq [il-paġna tal-għodda fuq GitHub](https://github.com/Holdi601/3DHeat-Ext-WarThunder), ikklikkja
   l-buttuna ħadra **Code**, imbagħad **Download ZIP**, u ħoll iz-zip.
2. Iftaħ terminal fil-folder maħlul (dak li fih `README.md`).
3. Ikteb:

   ```bash
   pip install -e .
   ```

   Fl-aħħar għandek tara: `Successfully installed heat3d-ext-warthunder-0.2.0`
   (jista' jkun b'aktar ismijiet).
4. Iċċekkjah:

   ```bash
   heat3d-wt-replay --version
   ```

   Għandek tara: `heat3d-wt-replay 0.2.0`

## Kif taqra l-kmandi f'dawn il-paġni {#how-to-read-the-commands-on-these-pages}

- Kliem bejn parentesi angolari, bħal `<replays>`, huma placeholders: ikteb
  hemm il-fajl jew il-folder tiegħek, mingħajr il-parentesi.
- Triq b'spazji teħtieġ il-kwotazzjoni: `"C:\Program Files (x86)\Steam"`.
- It-test wara `#` huwa kumment: ma tikteb.
- `-o out` jikteb f'folder jismu `out` ġewwa l-folder fejn ikun it-terminal tiegħek.
  Jinħoloq jekk ma jkunx hemm.

## Kif tkun taf li ħadem {#what-success-looks-like}

Il-kmand jistampa linja waħda għal kull ripetizzjoni, pereżempju:

```text
ok out/<map>/<match>.3dheat
```

u jispiċċa bi status tal-ħruġ `0`. Il-fajls il-ġodda jkunu fil-folder `out`.

## Żbalji komuni {#common-errors}

| Tara | X'tagħmel |
|---|---|
| `'python' is not recognized ...` jew `command not found` | Python mhuwiex fil-PATH: installah mill-ġdid bil-**Add python.exe to PATH** immarkat, jew ikteb `py` minflok `python` (Windows) |
| `'pip' is not recognized ...` | ikteb `python -m pip install -e .` minflok |
| `'heat3d-wt-replay' is not recognized ...` | ikteb `python -m heat3d_ext_warthunder` minflok `heat3d-wt-replay`; jagħmel l-istess |
| `No module named heat3d_ext_warthunder` | m'intix fil-folder tal-għodda, jew mhix installata: mur hemm b'`cd` u aħdem `pip install -e .` |
| `the following arguments are required: -o/--out` | żid `-o out` mal-kmand |

Li jmiss: [Il-konverżjoni tar-ripetizzjonijiet](converting.md).
