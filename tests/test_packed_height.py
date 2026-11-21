"""The packed ground heights' offset: from the level's heightmap, else from pairs that agree, else none."""
from types import SimpleNamespace

import numpy as np
import pytest

from heat3d_ext_warthunder import convert
from heat3d_ext_warthunder.convert import Sample


def replay(tracks):
    return SimpleNamespace(tracks=tracks, stream=SimpleNamespace(entities=[]))


def pairs(deltas):
    """One unit per delta: a float sample at height 100 and its packed one 2 s later at 100 - delta."""
    return {("ground", 100 + i): [Sample(0.0, 10.0 * i, 100.0, 0.0), Sample(2.0, 10.0 * i, 100.0 - d, 0.0, packed=True)]
            for i, d in enumerate(deltas)}


def flat(height):
    return lambda x, z: np.full(np.shape(x), height, np.float64)


@pytest.mark.parametrize("deltas, applied, method", [
    ([-9.9, -9.84, 0.38], 0.0, "none"),              # three pairs, 10 m apart: not taken
    ([-9.84, -9.8, -9.9, -9.85], 0.0, "none"),       # four that agree: still too few
    ([-9.84, -9.8, -9.9, -9.85, -9.82], -9.84, "pairs"),
    ([7.0, 7.0, 7.0, 7.0, 3.0, 11.0, 7.0, 7.0, 7.0, 7.0], 0.0, "none"),  # spread 4 m: not taken
    ([1.5, 1.5, 1.5, 1.5, 1.5], 0.0, "none"),        # agreeing, but within 5 m: none
])
def test_pairs_offset_only_from_five_that_agree_within_2_m(deltas, applied, method):
    r = replay(pairs(deltas))
    out = convert._packed_height(r)
    assert (out["applied"], out["method"], out["pairs"]) == (pytest.approx(applied), method, len(deltas))
    packed = [s for ss in r.tracks.values() for s in ss if s.packed]
    assert packed[0].y == pytest.approx(100.0 - deltas[0] + applied)


def ground_track(n, packed_y, float_y=None):
    """A unit driving on ground at height 50: n packed samples at packed_y, and as many float ones at float_y."""
    out = [Sample(float(i), float(i), packed_y + (0.3 if i % 7 == 0 else 0.0), 0.0, packed=True) for i in range(n)]
    if float_y is not None:
        out += [Sample(1000.0 + i, float(i), float_y, 5.0) for i in range(n)]
    return out


def test_heightmap_offset_wins_over_pairs():
    # Packed heights 1,493 m below the ground (a level whose packed heights count from its water level); three
    # pairs that disagree say -9.84.
    tracks = {("ground", 1): ground_track(200, 50.0 - 1493.0)} | pairs([-9.9, -9.84, 0.38])
    r = replay(tracks)
    out = convert._packed_height(r, flat(50.0))
    assert out["method"] == "heightmap" and out["applied"] == pytest.approx(1493.0, abs=0.01)
    assert out["heightmap"]["sure"] and out["heightmap"]["samples"] == 203
    assert r.tracks[("ground", 1)][1].y == pytest.approx(50.0, abs=0.01)


def test_heightmap_that_agrees_with_the_packed_heights_applies_none():
    r = replay({("ground", 1): ground_track(200, 50.1)} | pairs([-9.9, -9.84, -9.8, -9.85, -9.82]))
    out = convert._packed_height(r, flat(50.0))
    assert (out["method"], out["applied"]) == ("heightmap", 0.0)


def test_an_unsure_heightmap_falls_back_to_the_pairs_rule():
    # The packed samples scattered 0-40 m over the heightmap (bridges, roofs): half do not agree within 1 m.
    scattered = [Sample(float(i), float(i), 50.0 + (i % 40), 0.0, packed=True) for i in range(200)]
    r = replay({("ground", 1): scattered} | pairs([-9.9, -9.84, 0.38]))
    out = convert._packed_height(r, flat(50.0))
    assert out["heightmap"]["sure"] is False and (out["method"], out["applied"]) == ("none", 0.0)


def test_samples_outside_the_heightmap_do_not_count():
    def edge(x, z):
        return np.where(np.asarray(x) < 10, 50.0, np.nan)
    r = replay({("ground", 1): ground_track(200, 50.0 - 20.0)})
    out = convert._packed_height(r, edge)
    assert out["method"] == "none" and "heightmap" not in out  # 10 samples inside: too few


def test_level_heights_reads_only_the_heightmap_block(tmp_path, monkeypatch):
    from heat3d_ext_warthunder import dagorlevel

    hm = dagorlevel.Heightmap(np.array([[0.0, 10.0], [20.0, 30.0]], np.float32), 4.0, 100.0, 200.0, 0, False)
    monkeypatch.setattr(dagorlevel, "scan", lambda p: ({"HM2": [dagorlevel.Block("HM2", 0, 4)]}, {}))
    monkeypatch.setattr(dagorlevel, "read_heightmap", lambda data, block: hm)
    (tmp_path / "levels").mkdir()
    (tmp_path / "levels" / "x.bin").write_bytes(b"abcd")
    monkeypatch.setattr("heat3d_ext_warthunder.install.find_game", lambda game=None: tmp_path)
    h = convert.level_heights("levels/x.bin")
    assert h(np.array([102.0]), np.array([202.0]))[0] == pytest.approx(15.0)
    assert np.isnan(h(np.array([90.0]), np.array([202.0]))[0])
    assert convert.level_heights("levels/missing.bin") is None
