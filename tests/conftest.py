import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os
import tempfile

# Unit tests never read an install's localisation; a test that wants names passes them (see names.Names).
os.environ.setdefault("HEAT3D_WT_NO_NAMES", "1")
# Nor keep or read copies of an install's archive (damage_parts.keep_archive) outside a temporary folder.
os.environ["HEAT3D_WT_ARCHIVES"] = tempfile.mkdtemp(prefix="heat3d-wt-archives-")
