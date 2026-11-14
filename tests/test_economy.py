"""Silver Lions and research points on a battle's rows, from made-up economy tables (no number of the game's)."""

from __future__ import annotations

import pytest

from heat3d_ext_warthunder import arsenal, convert, economy
from heat3d_ext_warthunder.vromfs import Blk


def blk(name: str = "", *items) -> Blk:
    b = Blk(name)
    for it in items:
        (b.blocks if isinstance(it, Blk) else b.params).append(it)
    return b


WPCOST = blk(
    "",
    blk("tank_a", ("repairCostHistorical", 1000), ("repairCostFullUpgradedHistorical", 1500), ("value", 50000),
        ("reqExp", 20000), ("trainCost", 9000), ("rewardMulHistorical", 2.0), ("expMul", 1.5),
        ("unitClass", "exp_tank"),
        blk("modifications", blk("gun_ap", ("value", 30), ("ammoCount", 1)), blk("gun_heat", ("value", 90), ("ammoCount", 2)))),
    blk("tank_b", ("repairCostHistorical", 2000), ("rewardMulHistorical", 1.0), ("expMul", 1.0),
        ("unitClass", "exp_heavy_tank")),
    blk("jet_a", ("repairCostHistorical", 3000), ("rewardMulHistorical", 3.0), ("expMul", 2.0), ("groundKillMul", 1.5),
        ("unitClass", "exp_fighter"),
        blk("weapons", blk("jet_a_default"),
            blk("jet_a_bombs", ("value", 120), blk("sum_weapons", ("bomb_x", 4), ("countermeasure_y", 60))),
            blk("jet_a_rockets", ("value", 100), blk("sum_weapons", ("rocket_z", 20))))),
)
WARPOINTS = blk("", ("aKill", 100.0), ("aiKillK", 0.5), ("winK", 0.4), ("defeatK", 0.1),
                blk("units", ("exp_tank", 0.5), ("exp_heavy_tank", 1.0), ("exp_fighter", 1.0)))
RANK = blk("", blk("units", ("exp_tank", 1.0), ("exp_heavy_tank", 1.0), ("exp_fighter", 1.0)))


class Arms:
    """A tank_a with one gun: a stock shell, an AP and a HEAT modification."""

    def guns(self, vehicle: str):
        if vehicle != "tank_a":
            return []
        return [arsenal.Gun("gun.blk", 75.0, mods={"stock": "", "ap_1": "gun_ap", "heat_1": "gun_heat"})]

    def __bool__(self) -> bool:
        return True


def eco() -> economy.Economy:
    return economy.Economy(WPCOST, WARPOINTS, RANK, Arms())


def life(uid: int, vehicle: str, player: str, team: str, figure: str, start: float = 0.0, end: float = 100.0):
    ss = [convert.Sample(float(t), float(uid * 10), 0.0, float(t)) for t in range(int(start), int(end) + 1)]
    return convert.Life(uid, "air" if figure == "aircraft" else "ground", 1, ss, vehicle=vehicle, player=player,
                        user_id=str(uid) if player else "", team=team, figure=figure)


def test_prices():
    e = eco()
    assert e.repair("TANK_A", "Historical") == 1000
    assert e.round_cost("tank_a", 0, "ap_1") == (30, "install")
    assert e.round_cost("tank_a", 0, "heat_1") == (45, "install")  # 90 for two rounds
    assert e.round_cost("tank_a", 0, "stock") == (0, "install")
    assert e.round_cost("tank_a", 0, "") == (25, "inferred")  # the mean of 0, 30, 45
    assert e.round_cost("tank_a", 3, "ap_1") == (None, "")
    assert e.launch_cost("jet_a") == pytest.approx(17.5)  # median of 120/4 and 100/20, countermeasures not items
    assert e.launch_cost("tank_b") is None
    # A kill: aKill x the killer's rewardMul x the victim class x (AI) x (aircraft on ground).
    assert e.kill_reward("tank_a", "tank", "tank_b", "tank", False, "Historical") == (200.0, 150.0)
    assert e.kill_reward("jet_a", "aircraft", "tank_a", "tank", True, "Historical") == (112.5, 150.0)
    assert e.vehicle("tank_a", "Historical")["crewSl"] == 9000
    assert not economy.Economy()


def test_annotate():
    a, b, j = life(1, "tank_a", "Alice", "1", "tank"), life(2, "tank_b", "Bob", "2", "tank"), life(3, "jet_a", "Jet", "1", "aircraft")
    rows = []
    for l in (a, b, j):
        rows.append({**convert._row(l, l.samples[0], "position"), "match": "m", "difficulty": "RB", "gameMode": "ground"})
    rows.append({**convert._row(a, a.samples[5], "shot"), "ammoSlot": "0/1", "ammoName": "ap_1"})
    rows.append({**convert._row(a, a.samples[6], "bullet_rearm"), "time": 6.0})
    rows.append({**convert._row(a, a.samples[8], "bullet_rearm"), "time": 8.0})
    rows.append({**convert._row(a, a.samples[9], "bullet_rearm"), "time": 9.0})  # a resupply: not a shot
    rows.append({**convert._row(j, j.samples[7], "launch"), "weapon": "bomb"})
    rows.append({**convert._row(b, b.samples[20], "death")})
    fired = {1: [(6.0, 0, 1), (8.0, 0, 2)]}
    kills = [{"t": 20.0, "killerUid": 1, "victimUid": 2}]
    board = {"players": [
        {"name": "Alice", "series": [{"time": 0.0, "score": 0, "assists": 0, "captureZone": 0},
                                     {"time": 20.2, "score": 200, "assists": 0, "captureZone": 0},
                                     {"time": 30.0, "score": 300, "assists": 0, "captureZone": 1},
                                     {"time": 40.0, "score": 320, "assists": 0, "captureZone": 1}]},
        {"name": "Bob", "series": [{"time": 0.0, "score": 0, "assists": 0}, {"time": 15.0, "score": 100, "assists": 1}]}],
        "teams": {"1": [[90.0, 500.0, 10, 0]], "2": [[90.0, 100.0, 0, 0]]}}
    block = economy.annotate(rows, eco(), "RB", lives=[a, b, j], kills=kills, hits=[{"t": 40.5, "uid": 1, "severity": "severe"}],
                             detections=[], board=board, fired=fired, where=convert._at_time, label=convert._label)
    assert block["available"] and block["winnerTeam"] == "1" and block["pointsPerKill"] == 200
    by = lambda ev: [r for r in rows if r["event"] == ev]  # noqa: E731
    assert [(r.get("cost_fired_sl"), r.get("econ_basis")) for r in by("bullet_rearm")] == [
        (30, "install"), (25, "inferred"), (None, None)]
    assert by("launch")[0]["cost_fired_sl"] == pytest.approx(17.5)
    assert by("death")[0]["cost_lost_sl"] == 2000 and by("death")[0]["currency"] == "SL"
    rw = {(r["player"], r["rewardType"]): r for r in by("reward")}
    assert set(rw) == {("Alice", "kill"), ("Alice", "capture"), ("Alice", "severe_damage"), ("Bob", "assist"),
                       ("Alice", "battle_end"), ("Bob", "battle_end")}
    assert rw[("Alice", "kill")]["earn_sl"] == 200 and rw[("Alice", "kill")]["other"] == "Bob"
    assert rw[("Alice", "capture")]["earn_sl"] == pytest.approx(100)  # 100 points at 200 SL a 200-point kill
    assert rw[("Bob", "assist")]["earn_sl"] == pytest.approx(50)  # Bob's rewardMul is half Alice's
    assert rw[("Alice", "battle_end")]["earn_sl"] == pytest.approx(0.4 * (200 + 100 + 20))
    assert rw[("Bob", "battle_end")]["earn_sl"] == pytest.approx(0.1 * 50)
    assert all(r["econ_basis"] == "inferred" and r["x"] is not None for r in by("reward"))
    assert block["players"]["Alice"]["firedSl"] == 55
    assert [r["time"] for r in rows] == sorted(r["time"] for r in rows)


def test_without_tables():
    rows = [{"time": 0.0, "event": "death", "isPlayer": True, "Vehicle": "tank_a"}]
    assert economy.annotate(rows, economy.Economy(), "RB", lives=[], kills=[], hits=[], detections=[], board={},
                            fired={}, where=convert._at_time, label=convert._label)["available"] is False
    assert "cost_lost_sl" not in rows[0]
