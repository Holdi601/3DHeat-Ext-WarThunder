---
title: Pirms sākat
nav_order: 2
lang: lv
source: before-you-start.md
source_hash: "99034fb56b0d"
nav_exclude: true
search_exclude: true
---
# Pirms sākat {#before-you-start}

Jauns komandrindā? Šī lappuse ved no nulles līdz tam, ka `heat3d-wt-replay`
darbojas, apmēram desmit minūtēs. Ja jau lietojat Python, dodieties tieši uz
[Uzstādīšana](installing.md).

## 1. Uzstādiet Python {#install-python}

1. Lejupielādējiet Python **3.10 vai jaunāku** no
   [python.org/downloads](https://www.python.org/downloads/).
2. Windows sistēmā atzīmējiet **Add python.exe to PATH** instalētāja pirmajā logā un
   tad noklikšķiniet **Install Now**.
3. macOS un Linux sistēmā Python 3 bieži jau ir. Kur šajās lappusēs ir rakstīts `python`,
   rakstiet `python3`, un `pip` vietā rakstiet `pip3`.

## 2. Atveriet termināli {#open-a-terminal}

Termināls ir logs, kurā rakstāt komandas.

- **Windows:** atveriet mapi File Explorer, noklikšķiniet adreses joslā, ierakstiet
  `cmd` un nospiediet Enter. Atveras logs, kas jau ir šajā mapē.
- **macOS:** atveriet lietotni **Terminal**. **Linux:** ar peles labo pogu noklikšķiniet
  mapē un izvēlieties **Open in Terminal**.

Lai pārietu uz citu mapi, ierakstiet `cd` un mapes nosaukumu:

```bash
cd "C:\Users\you\Downloads\3DHeat-Ext-WarThunder-main"
```

## 3. Pārbaudiet, vai Python darbojas {#check-that-python-works}

```bash
python --version
```

Jābūt redzamam `Python 3.` un skaitlim 10 vai lielākam, piemēram
`Python 3.12.4`.

## 4. Iegūstiet rīku un uzstādiet to {#get-the-tool-and-install-it}

1. Rīka GitHub lapā ([rīka GitHub lapa](https://github.com/Holdi601/3DHeat-Ext-WarThunder))
   noklikšķiniet zaļo pogu **Code**, tad **Download ZIP**, un izpakojiet zip failu.
2. Atveriet termināli izpakotajā mapē (tajā, kurā ir `README.md`).
3. Ierakstiet:

   ```bash
   pip install -e .
   ```

   Beigās vajadzētu redzēt: `Successfully installed heat3d-ext-warthunder-0.2.0`
   (varbūt ar vēl dažiem nosaukumiem).
4. Pārbaudiet:

   ```bash
   heat3d-wt-replay --version
   ```

   Vajadzētu redzēt: `heat3d-wt-replay 0.2.0`

## Kā lasīt šajās lappusēs esošās komandas {#how-to-read-the-commands-on-these-pages}

- Vārdi leņķa iekavās, piemēram `<replays>`, ir vietturi: ierakstiet savu failu vai
  mapi tur, bez iekavām.
- Ceļš ar atstarpēm prasa pēdiņas: `"C:\Program Files (x86)\Steam"`.
- Teksts aiz `#` ir komentārs: to neraksti.
- `-o out` raksta mapē `out`, kas atrodas mapē, kurā ir jūsu termināls. Ja tās nav,
  tā tiek izveidota.

## Kā izskatās veiksme {#what-success-looks-like}

Komanda izdrukā vienu rindu katram atkārtojumam, piemēram:

```text
ok out/<map>/<match>.3dheat
```

un beidzas ar izejas statusu `0`. Jaunie faili ir mapē `out`.

## Biežākās kļūdas {#common-errors}

| Ko redzat | Ko darīt |
|---|---|
| `'python' is not recognized ...` vai `command not found` | Python nav PATH: uzstādiet to vēlreiz, atzīmējot **Add python.exe to PATH**, vai rakstiet `py` `python` vietā (Windows) |
| `'pip' is not recognized ...` | rakstiet `python -m pip install -e .` |
| `'heat3d-wt-replay' is not recognized ...` | rakstiet `python -m heat3d_ext_warthunder` `heat3d-wt-replay` vietā; tas dara to pašu |
| `No module named heat3d_ext_warthunder` | jūs neesat rīka mapē vai tas nav uzstādīts: dodieties uz to un palaidiet `pip install -e .` |
| `the following arguments are required: -o/--out` | pievienojiet komandai `-o out` |

Tālāk: [Atkārtojumu pārvēršana](converting.md).
