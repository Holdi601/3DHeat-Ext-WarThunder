---
title: "Εγκατάσταση"
nav_order: 3
lang: el
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Εγκατάσταση {#installing}

Χρειάζεται Python 3.10 ή νεότερη· τα pyarrow, numpy, zstandard και Pillow
εγκαθίστανται μαζί της.

Αν είστε νέος στη γραμμή εντολών, διαβάστε πρώτα το [Πριν ξεκινήσετε](before-you-start.md).

## Βήμα προς βήμα {#step-by-step}

1. Πάρτε τον κώδικα: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ή κατεβάστε ένα zip από τις [Κυκλοφορίες](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   και αποσυμπιέστε το.
2. Ανοίξτε ένα τερματικό σε αυτόν τον φάκελο και γράψτε `pip install -e .`. Εγκαθιστά
   δύο εντολές: `heat3d-wt-replay` (replays) και `heat3d-wt-level` (επίπεδα).
3. Ελέγξτε το: `heat3d-wt-replay --version`. Πρέπει να δείτε
   `heat3d-wt-replay 0.2.0`. Το `heat3d-wt-replay --help` δείχνει τις επιλογές:

![heat3d-wt-replay --help](../assets/img/help.svg)

Χωρίς εγκατάσταση: `python -m heat3d_ext_warthunder ...` και
`python -m heat3d_ext_warthunder.levelcli ...` μέσα στον φάκελο του εργαλείου.

## Ονόματα από την εγκατάστασή σας {#names-from-your-install}

Τα οχήματα, τα όπλα και τα πυρομαχικά παίρνουν τα αγγλικά ονόματά τους από τα
δικά του αρχεία κειμένου του παιχνιδιού, διαβασμένα από την εγκατάστασή σας κατά
τη μετατροπή. Η εγκατάσταση βρίσκεται μέσω του Steam ή των προεπιλεγμένων φακέλων
του launcher· το `--game <φάκελος>` ή η μεταβλητή περιβάλλοντος `HEAT3D_WT_GAME`
δείχνουν πού αλλιώς. Κανένα κείμενο του παιχνιδιού δεν υπάρχει σε αυτό το αποθετήριο·
χωρίς εγκατάσταση, τα ονόματα είναι τα αναγνωριστικά των οχημάτων (ο μετατροπέας
το λέει σε μια γραμμή `note:`).

## Ενημερώσεις {#updates}

Κάθε εκκίνηση ελέγχει πρώτα τις κυκλοφορίες του έργου στο GitHub (το πολύ ένα αίτημα
κάθε μερικές ώρες· ποτέ δεν σταματά μια μετατροπή, online ή offline). Όταν βγει νεότερη
κυκλοφορία, η εντολή ρωτά πριν την εγκαταστήσει: ένα `git clone` ενημερώνεται με
`git pull --ff-only` (αρνείται όσο έχετε τοπικές αλλαγές), ένα κατεβασμένο αντίγραφο
από το αρχείο της κυκλοφορίας. Το `HEAT3D_NO_UPDATE=1` απενεργοποιεί τον έλεγχο και
την ενημέρωση.

---

Μέρος του [3DHeat](https://github.com/Holdi601/3DHeat) ([τεκμηρίωση](https://holdi601.github.io/3DHeat/)). Πηγή: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
