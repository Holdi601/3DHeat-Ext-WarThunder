---
title: "Όροι και άδεια"
nav_order: 16
lang: "el"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Όροι και άδεια {#terms-and-licence}

## Τι διαβάζεται {#what-it-reads}

Ο μετατροπέας διαβάζει τα replays που αποθηκεύει το War Thunder στον υπολογιστή σας (ή replays των μαχών σας που κατεβάσατε εσείς από το warthunder.com) και τα αρχεία επιπέδων της δικής σας εγκατάστασης του War Thunder. Τίποτα από το παιχνίδι δεν περιλαμβάνεται ούτε αναδιανέμεται εδώ: κανένα asset του παιχνιδιού, κανένας κώδικας του παιχνιδιού, κανένα DLL· το Oodle φορτώνεται από τη δική σας εγκατάσταση. Ό,τι γράφει μένει στον υπολογιστή σας: **μην δημοσιεύετε ποτέ τα επίπεδα**.

Το 3DHeat δεν συνδέεται με την Gaijin Entertainment ούτε έχει την έγκρισή της. Το War Thunder και τα σχετικά ονόματα και εμπορικά σήματα ανήκουν στους κατόχους τους.

Δικαιούχοι: ανοίξτε ένα issue στο <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - απαντάμε γρήγορα και αφαιρούμε οτιδήποτε κατόπιν αιτήματος.

## Πηγές {#sources}

Όλος ο κώδικας εδώ γράφτηκε για αυτό το έργο· κανένας κώδικας δεν αντιγράφηκε από άλλον
αναλυτή. Όσα ξέρει για τη μορφή προέρχονται από:

- Τον πηγαίο κώδικα της Dagor Engine της Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` και `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` για τη ροή οντοτήτων (`ecs.py`), και `net/message.cpp`
  (`MessageClass::initImpl`) για το πώς τα μηνύματα οντοτήτων αριθμούν τις κλάσεις τους.
  Τα ονόματα στοιχείων και τύπων ταιριάζονται με τα hash FNV-1a τους απέναντι σε λέξεις
  από τα αρχεία του ίδιου του παιχνιδιού· το `ecs.py` απαριθμεί τα ονόματα που βρέθηκαν.
- Τα `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` και
  `daNet/bitStream.h` του ίδιου κώδικα: πώς ένα μήνυμα ονομάζει το αντικείμενο για το
  οποίο προορίζεται (`wrpl.read_mpi`).
- Το ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, και τον δικό του αναλυτή
  `web/wrpl-parse.js`, διαβασμένα για τις διατάξεις bits του μοντέλου πτήσης, του
  συγχρονισμού εδάφους, των όπλων σε πτήση, των μηνυμάτων με πεδία αναγνωριστικού, των
  θέσεων παικτών, των τιμών της κάμπινας και του δυαδικού blk. Το WTACRP ονομάζει ως δικές
  του αναφορές τα maxsupermanhd/wrpl-inspector, wt_blk και wrpl-acmi (AGPL-3.0)· ο κώδικας
  τους δεν διαβάστηκε εδώ.
- Τα δικά του replays του συντάκτη, διαβασμένα ως αρχεία: οι διαφορές του 2025 (η παλαιότερη
  διάταξη του μοντέλου πτήσης, η συνομιλία χωρίς byte σημαιών, το zlib), η στάση του εδάφους,
  η απόκλιση του συμπιεσμένου ύψους, τα σημεία απελευθέρωσης των όπλων και τα όργανα της
  κάμπινας βρέθηκαν πάνω σε αυτά εδώ.

## Δοκιμές {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # ελέγχει επίσης τα δημόσια δείγματα replays του 2025
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # βήματα, ταυτότητες, σημαίες AI, πρόσημο roll, ο εξομαλυντής, τα ονόματα
```

Οι μονάδες δοκιμών δεν διαβάζουν ποτέ εγκατάσταση (το `HEAT3D_WT_NO_NAMES` είναι
ορισμένο)· η δοκιμή με τα δικά σας replays διαβάζει τα ονόματα από την εγκατάστασή σας.

Οι δοκιμές φτιάχνουν replays μέσα στον κώδικα (`tests/synth.py`: κεφαλίδα, πακέτα,
αποτελέσματα, η ροή οντοτήτων, τα όπλα σε πτήση) στη διάταξη που τεκμηριώνουν οι αναγνώστες·
κανένα replay δεν υπάρχει στο αποθετήριο.

## Άδεια {#licence}

MIT· βλ. το [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE).
Χρησιμοποιεί το pyarrow (Apache-2.0), το numpy (BSD-3-Clause), το zstandard (BSD-3-Clause)
και το Pillow (MIT-CMU). Οι αναγνώστες επιπέδων γράφτηκαν από τον πηγαίο κώδικα της Dagor
Engine, Copyright (c) 2023 Gaijin Entertainment, άδεια BSD 3-Clause· κανένας κώδικας της
δεν αντιγράφεται εδώ, και οι σταθερές της μορφής που χρησιμοποιούνται (το κλειδί XOR των
vromfs, οι μετατοπίσεις του πλέγματος των εύρων ύψους) αναφέρονται εκεί που εμφανίζονται.

---

Μέρος του [3DHeat](https://github.com/Holdi601/3DHeat) ([τεκμηρίωση](https://holdi601.github.io/3DHeat/)). Πηγή: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
