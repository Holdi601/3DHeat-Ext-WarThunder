"""
A battle packed into one `.3dheat` file: the loose files come back byte for
byte, Parquet stored (a byte range the viewer reads in place), JSON deflated.
"""

import json
import zipfile

import pyarrow as pa
import pyarrow.parquet as pq

from heat3d_ext_warthunder.container import members_of, pack


def test_a_battle_packs_into_one_file_and_comes_back_whole(tmp_path):
    pq.write_table(pa.table({"x": list(range(1000))}), tmp_path / "b.parquet")
    pq.write_table(pa.table({"type": ["a"]}), tmp_path / "b.flight.parquet")
    pq.write_table(pa.table({"type": ["a"]}), tmp_path / "b.objectives.parquet")
    (tmp_path / "b.match.json").write_text(json.dumps({"match": "b"}), encoding="utf-8")
    (tmp_path / "b2.parquet").write_bytes(b"another battle")
    loose = {p.name: p.read_bytes() for p in tmp_path.iterdir() if p.name.startswith("b.")}
    assert [r for r, _ in members_of(tmp_path / "b.parquet")] == ["table", "match", "flight", "objectives"]
    out = pack(tmp_path / "b.parquet", {"game": "warthunder", "match": "b"})
    assert sorted(p.name for p in tmp_path.iterdir()) == ["b.3dheat", "b2.parquet"]
    with zipfile.ZipFile(out) as z:
        infos = z.infolist()
        assert infos[0].filename == "manifest.json"
        manifest = json.loads(z.read("manifest.json"))
        assert manifest["roles"] == {"table": "b.parquet", "match": "b.match.json", "flight": "b.flight.parquet",
                                     "objectives": "b.objectives.parquet"}
        for i in infos[1:]:
            assert i.compress_type == (zipfile.ZIP_DEFLATED if i.filename.endswith(".json") else zipfile.ZIP_STORED)
            assert z.read(i) == loose[i.filename]
