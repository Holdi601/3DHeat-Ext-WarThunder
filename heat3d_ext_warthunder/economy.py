"""
Silver Lions (SL) and research points (RP): what a battle cost and earned, per
event, from the user's own install, read when a replay is converted
(`char.vromfs.bin`: `config/wpcost.blk` per vehicle, `config/warpoints.blk`
and `config/rank.blk` for the whole game; the weapon blks of
`aces.vromfs.bin` through arsenal.py). No number of the game's is kept in this
repository: the values go into that replay's output only. Without the install
(or without its `char.vromfs.bin`) no economy is written.

What the replay tells and what is worked out (`econ_basis` says which):

* `cost_lost_sl` on a player's `death` row: the vehicle's repair cost at the
  battle's difficulty (`repairCost<Arcade|Historical|Simulation>`, the stock
  vehicle's; the fully upgraded one's is in the economy block). `install`.
* `cost_fired_sl` on a ground vehicle's `bullet_rearm` row that takes a round
  from the stowage after a shot (see convert.shots_fired): the price of the
  round, its modification's `value` per `ammoCount` in the vehicle's wpcost
  entry (the weapon blk names the modification each shell is in; a stock shell
  is free). `install` where the slot's shell is known (a kill named it, see
  convert._shot_ammo), else `inferred`: the mean price of the shells that
  weapon can fire on that vehicle.
* `cost_fired_sl` on an aircraft's or helicopter's `launch` row: the game
  prices a weapon preset per sortie, not per item; the cost of one item is the
  median over the vehicle's priced presets of their price over the items they
  hold (`sum_weapons`, countermeasures and drop tanks left out). `inferred`.
* `earn_sl`, `earn_rp` on `reward` rows (`rewardType`), at the earner's place
  and time. The replay holds no reward record (checked: the results block has
  only scores and counts, the messages no SL), so every reward is `inferred`:
  - `kill`: `aKill` (warpoints) x the killer's `rewardMul<mode>` x the
    victim class's weight (warpoints `units`, by the victim's `unitClass`)
    x `aiKillK` for an AI victim x the killer's `groundKillMul` for an
    aircraft killing a ground unit; RP alike with `expMul` and rank.blk's
    `units` weights.
  - every other step of a player's score (the replicated scoreboard, see
    convert.scoreboard): `assist`, `capture`, `base_damage`, `damage`,
    `missile_evade` by the counter that went up with it, else `critical_hit`
    / `severe_damage` by that player's hit record within 3 s, else
    `scouting` by a detection naming the player's unit within 2 s, else
    `other`; worth its points at the battle's SL a point (a kill's SL over
    the median points a kill's step scored in this battle).
  - `battle_end`: `winK` (won) or `defeatK` (lost) of the player's in-battle
    earnings, the winner by the teams' tickets left (then their score).
  Premium time, boosters, the vehicle's crew and modifications are not known
  and not applied.
"""

from __future__ import annotations

import math
import os
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from . import install

#: The battle's difficulty as the economy tables name it.
MODES = {"AB": "Arcade", "RB": "Historical", "SB": "Simulation"}
#: A victim's class where its vehicle has no wpcost entry (AI units), by figure kind.
FIGURE_CLASS = {"structure": "exp_structure", "truck": "exp_vehicle", "apc": "exp_vehicle", "tank": "exp_ai_tank",
                "spaa": "exp_aaa", "ship": "exp_ship", "boat": "exp_ship", "aircraft": "exp_fighter",
                "helicopter": "exp_helicopter", "train": "exp_freight_car"}
GROUND = {"tank", "apc", "spaa", "truck", "structure", "ship", "boat", "train"}
AIR = {"aircraft", "helicopter"}
LAUNCHED = {"missile", "rocket", "bomb", "torpedo"}
#: Columns added to the table (convert.COLUMNS) and what they hold.
COLUMNS = {
    "cost_fired_sl": "SL a round, shell, rocket, missile or bomb fired cost (bullet_rearm, launch rows)",
    "cost_lost_sl": "SL to repair the vehicle lost (a player's death row), at the battle's difficulty",
    "earn_sl": "SL earned (reward rows, rewardType), inferred from the install's reward tables",
    "earn_rp": "RP earned (reward rows), inferred like earn_sl",
    "currency": "'SL' on rows with a cost_* or earn_sl value (earn_rp is research points)",
    "econ_basis": "'install' (a price read from the install) or 'inferred' (worked out, see economy.py)",
    "rewardType": "reward rows: kill, assist, capture, base_damage, damage, missile_evade, critical_hit, "
                  "severe_damage, scouting, other, battle_end",
}
_NOT_ITEMS = ("countermeasure", "drop_tank", "fuel_tank", "pylon", "container_empty")


def _num(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


class Economy:
    """The install's economy tables (parsed Blk), read as asked; empty without them."""

    def __init__(self, wpcost=None, warpoints=None, rank=None, arms=None) -> None:
        self.wpcost, self.warpoints, self.rank, self.arms = wpcost, warpoints, rank, arms
        self._units = {b.name.lower(): b for b in wpcost.blocks} if wpcost is not None else {}
        self._launch: dict[str, float | None] = {}

    @classmethod
    def from_game(cls, game: str | os.PathLike[str] | None = None, arms=None) -> "Economy":
        root = install.find_game(game)
        path = Path(root) / "char.vromfs.bin" if root else None
        if path is None or not path.is_file():
            return cls(arms=arms)
        try:
            from .vromfs import Vromfs

            v = Vromfs(path)
            return cls(v.blk("config/wpcost.blk"), v.blk("config/warpoints.blk"), v.blk("config/rank.blk"), arms)
        except (OSError, ValueError, KeyError, IndexError):
            return cls(arms=arms)

    def __bool__(self) -> bool:
        return bool(self._units) and self.warpoints is not None

    def unit(self, vehicle: str):
        return self._units.get((vehicle or "").lower())

    def value(self, vehicle: str, key: str) -> float | None:
        u = self.unit(vehicle)
        return _num(u.get(key)) if u is not None else None

    def game(self, key: str) -> float | None:
        return _num(self.warpoints.get(key)) if self.warpoints is not None else None

    def repair(self, vehicle: str, mode: str) -> float | None:
        return self.value(vehicle, f"repairCost{mode}")

    def mod_price(self, vehicle: str, mod: str) -> float | None:
        """A modification's SL a round (`value` / `ammoCount`); 0 for the stock shell (''), None when the vehicle
        has no such modification."""
        if mod == "":
            return 0.0
        u = self.unit(vehicle)
        mods = u.block("modifications") if u is not None else None
        m = mods.block(mod) if mods is not None else None
        if m is None:
            return None
        v = _num(m.get("value"))
        n = _num(m.get("ammoCount")) or 1.0
        return v / n if v is not None else None

    def round_cost(self, vehicle: str, weapon: int, shell: str) -> tuple[float | None, str]:
        """A round of the vehicle's weapon (its index, see arsenal.py): (SL, basis); the shell's own price where it is
        known (`install`), else the mean of the weapon's priced shells (`inferred`), else (None, '')."""
        guns = self.arms.guns(vehicle) if self.arms else []
        if not 0 <= weapon < len(guns):
            return None, ""
        gun = guns[weapon]
        if shell and shell.lower() in gun.mods:
            p = self.mod_price(vehicle, gun.mods[shell.lower()])
            if p is not None:
                return p, "install"
        prices = [p for p in (self.mod_price(vehicle, m) for m in set(gun.mods.values())) if p is not None]
        return (sum(prices) / len(prices), "inferred") if prices else (None, "")

    def launch_cost(self, vehicle: str) -> float | None:
        """One launched item of an aircraft (see the module's notes), None without priced presets known."""
        key = (vehicle or "").lower()
        if key in self._launch:
            return self._launch[key]
        u = self.unit(vehicle)
        ws = u.block("weapons") if u is not None else None
        per: list[float] = []
        any_preset = False
        for p in ws.blocks if ws is not None else []:
            any_preset = True
            v = _num(p.get("value"))
            items = p.block("sum_weapons")
            n = sum(_num(x) or 0 for k, x in (items.params if items is not None else [])
                    if not any(w in k.lower() for w in _NOT_ITEMS))
            if v and n:
                per.append(v / n)
        out = statistics.median(per) if per else (0.0 if any_preset else None)
        self._launch[key] = out
        return out

    def victim_class(self, vehicle: str, figure: str) -> str:
        u = self.unit(vehicle)
        c = u.get("unitClass") if u is not None else None
        return str(c) if c else FIGURE_CLASS.get(figure, "")

    def kill_reward(self, killer: str, killer_figure: str, victim: str, victim_figure: str, victim_ai: bool,
                    mode: str) -> tuple[float | None, float | None]:
        """(SL, RP) a kill earns its killer (see the module's notes); (None, None) where the tables lack a part."""
        a_kill = self.game("aKill")
        mul = self.value(killer, f"rewardMul{mode}")
        if a_kill is None or mul is None:
            return None, None
        cls = self.victim_class(victim, victim_figure)
        wp_units = self.warpoints.block("units") if self.warpoints is not None else None
        rk_units = self.rank.block("units") if self.rank is not None else None
        w_sl = _num(wp_units.get(cls)) if wp_units is not None and cls else None
        w_rp = _num(rk_units.get(cls)) if rk_units is not None and cls else None
        w_sl = 1.0 if w_sl is None else w_sl
        w_rp = 1.0 if w_rp is None else w_rp
        ai = (self.game("aiKillK") or 1.0) if victim_ai else 1.0
        ground = (self.value(killer, "groundKillMul") or 1.0) if killer_figure in AIR and victim_figure in GROUND else 1.0
        sl = a_kill * mul * w_sl * ai * ground
        exp = self.value(killer, "expMul")
        rp = a_kill * exp * w_rp * ai * ground if exp is not None else None
        return sl, rp

    def vehicle(self, vehicle: str, mode: str) -> dict[str, Any]:
        """What the economy block says of one vehicle."""
        u = self.unit(vehicle)
        if u is None:
            return {}
        g = lambda k: _num(u.get(k))  # noqa: E731
        out = {"repairSl": g(f"repairCost{mode}"), "repairFullUpgradedSl": g(f"repairCostFullUpgraded{mode}"),
               "purchaseSl": g("value"), "researchRp": g("reqExp"), "crewSl": g("trainCost"),
               "crewExpertSl": g("train2Cost"), "rewardMul": g(f"rewardMul{mode}"), "expMul": g("expMul"),
               "groundKillMul": g("groundKillMul"), "battleTimeAwardSl": g(f"battleTimeAward{mode}"),
               "rank": g("rank"), "economicRank": g(f"economicRank{mode}"), "unitClass": u.get("unitClass")}
        return {k: v for k, v in out.items() if v is not None}


# ---------------------------------------------------------------- the battle's rows

#: Score steps: the counter that went up with a step and the reward it is (first match wins).
STEP_COUNTERS = (("assists", "assist"), ("captureZone", "capture"), ("damageZone", "base_damage"),
                 ("awardDamage", "damage"), ("missileEvades", "missile_evade"))
KILL_COUNTERS = ("kills", "aiKills", "aiGroundKills", "navalKills")
HIT_NEAR, SCOUT_NEAR, KILL_NEAR = 3.0, 2.0, 3.0


def annotate(data: list[dict[str, Any]], eco: Economy, diff: str, *, lives: list, kills: list[dict[str, Any]],
             hits: list[dict[str, Any]], detections: list[dict[str, Any]], board: dict[str, Any],
             fired: dict[int, list[tuple[float, int, int]]], where, label) -> dict[str, Any]:
    """
    The economy columns on `data` (in place) and its `reward` rows appended;
    returns the battle's economy block. `lives`: convert.Life list; `kills`,
    `hits`, `detections`: the replay's records; `board`: convert.scoreboard;
    `fired`: convert.shots_fired; `where(life, t)` a sample of the life near
    t (or None); `label(life)` the name rows give it.
    """
    mode = MODES.get(diff or "")
    if not eco or not mode:
        return {"available": False, "why": "no install economy tables" if not eco else "difficulty not known"}
    check: dict[str, Any] = defaultdict(int)
    cur = {"currency": "SL"}

    # Repairs: a player's death.
    for row in data:
        if row.get("event") == "death" and row.get("isPlayer"):
            c = eco.repair(row.get("Vehicle", ""), mode)
            if c is not None:
                row.update(cost_lost_sl=c, econ_basis="install", **cur)
                check["repairs"] += 1
            else:
                check["repairsNotPriced"] += 1

    # Rounds fired: bullet_rearm rows that take a round, priced by the slot's shell.
    taken: dict[tuple[int, float], list[tuple[int, int]]] = defaultdict(list)
    for uid, v in fired.items():
        for t, w, slot in v:
            taken[(uid, round(t, 4))].append((w, slot))
    shell_of: dict[tuple[int, str], str] = {}
    for row in data:
        if row.get("event") == "shot" and row.get("ammoName") and row.get("ammoSlot") and row.get("uid") is not None:
            shell_of.setdefault((row["uid"], row["ammoSlot"]), row["ammoName"])
    for row in data:
        if row.get("event") == "bullet_rearm" and row.get("uid") is not None:
            ws = taken.get((row["uid"], round(row["time"], 4)))
            if not ws:
                continue
            w, slot = ws.pop(0)
            c, basis = eco.round_cost(row.get("Vehicle", ""), w, shell_of.get((row["uid"], f"{w}/{slot}"), ""))
            if c is None:
                check["roundsNotPriced"] += 1
                continue
            row.update(cost_fired_sl=c, econ_basis=basis, **cur)
            check[f"rounds_{basis}"] += 1
        elif row.get("event") == "launch" and row.get("kind") in AIR and row.get("weapon") in LAUNCHED:
            c = eco.launch_cost(row.get("Vehicle", ""))
            if c is None:
                check["launchesNotPriced"] += 1
                continue
            row.update(cost_fired_sl=c, econ_basis="inferred", **cur)
            check["launches"] += 1

    # Rewards.
    by_name: dict[str, list] = defaultdict(list)
    by_uid: dict[int, list] = defaultdict(list)
    for life in lives:
        by_uid[life.uid].append(life)
        if life.player:
            by_name[life.player].append(life)

    def life_at(cands: list, t: float):
        best, gap = None, math.inf
        for life in cands:
            d = 0.0 if life.start <= t <= life.end else min(abs(t - life.start), abs(t - life.end))
            if d < gap:
                best, gap = life, d
        return best

    rewards: list[dict[str, Any]] = []
    match = {k: data[0].get(k) for k in ("match", "difficulty", "gameMode")} if data else {}

    def reward(life, t: float, kind: str, sl: float | None, rp: float | None, other: str = "") -> None:
        s = where(life, t) if life is not None else None
        if s is None and life is not None:
            s = min(life.samples, key=lambda q: abs(q.t - t))
        if s is None or sl is None:
            check["rewardsWithoutPlace" if s is None else "rewardsNotPriced"] += 1
            return
        from .convert import _row

        rewards.append({**_row(life, s, "reward"), **match, "time": t, "rewardType": kind, "earn_sl": sl,
                        "earn_rp": rp, "econ_basis": "inferred", "other": other, **cur})
        check[f"reward_{kind}"] += 1

    def kill_lives(k: dict[str, Any]):
        killer = life_at(by_uid.get(k.get("killerUid"), []), k["t"])
        victim = life_at(by_uid.get(k.get("victimUid"), []), k["t"])
        return killer, victim

    kill_times: dict[str, list[float]] = defaultdict(list)
    kill_sl: list[float] = []
    for k in kills:
        killer, victim = kill_lives(k)
        if killer is None or victim is None or killer is victim:
            continue
        if killer.team and killer.team == victim.team:
            check["teamKillsNotRewarded"] += 1
            continue
        sl, rp = eco.kill_reward(killer.vehicle, killer.figure, victim.vehicle, victim.figure, not victim.is_player,
                                 mode)
        if not killer.is_player:
            continue
        kill_times[killer.player].append(k["t"])
        if sl is not None:
            kill_sl.append(sl)
        reward(killer, k["t"], "kill", sl, rp, label(victim))

    # The score steps.
    steps: list[tuple[str, float, int, list[str]]] = []
    for p in board.get("players", []):
        prev: dict[str, Any] = {}
        for e in p.get("series", []):
            if prev and "score" in prev and "score" in e and e["score"] > prev["score"]:
                up = [k for k in e if k not in ("time", "score", "squad") and k in prev and e[k] > prev[k]]
                steps.append((p.get("name", ""), e["time"], e["score"] - prev["score"], up))
            prev.update(e)
    # Each kill's step: the player's largest step within KILL_NEAR of it, not an assist's.
    kill_steps: set[int] = set()
    for name, times in kill_times.items():
        mine = [i for i, st in enumerate(steps) if st[0] == name and "assists" not in st[3]]
        for kt in times:
            near = [i for i in mine if abs(steps[i][1] - kt) <= KILL_NEAR and i not in kill_steps]
            if near:
                kill_steps.add(max(near, key=lambda i: steps[i][2]))
    per_kill = statistics.median(steps[i][2] for i in kill_steps) if kill_steps else None
    check["pointsPerKill"] = per_kill
    hits_by: dict[str, list[tuple[float, str]]] = defaultdict(list)
    for h in hits:
        attacker = life_at(by_uid.get(h.get("uid"), []), h["t"])
        if attacker is not None and attacker.player:
            hits_by[attacker.player].append((h["t"], h.get("severity", "")))
    seen_by: dict[int, list[float]] = defaultdict(list)
    for d in detections:
        for u in (d.get("a"), d.get("b")):
            if u is not None:
                seen_by[u].append(d["t"])
    a_kill = eco.game("aKill")
    if per_kill and a_kill:
        for i, (name, t, points, up) in enumerate(steps):
            if i in kill_steps:
                continue  # the kill's own reward row
            life = life_at(by_name.get(name, []), t)
            if life is None:
                check["stepsWithoutLife"] += 1
                continue
            kind = next((r for c, r in STEP_COUNTERS if c in up), "")
            if not kind:
                near = [(abs(ht - t), sev) for ht, sev in hits_by.get(name, []) if abs(ht - t) <= HIT_NEAR]
                if near:
                    kind = "severe_damage" if min(near)[1] == "severe" else "critical_hit"
                elif any(abs(st - t) <= SCOUT_NEAR for st in seen_by.get(life.uid, [])):
                    kind = "scouting"
                else:
                    kind = "other"
            mul, exp = eco.value(life.vehicle, f"rewardMul{mode}"), eco.value(life.vehicle, "expMul")
            sl = a_kill * mul * points / per_kill if mul is not None else None
            rp = a_kill * exp * points / per_kill if exp is not None else None
            reward(life, t, kind, sl, rp)

    # The battle's end.
    teams = board.get("teams", {})
    ends = {k: v[-1] for k, v in teams.items() if v}
    winner = None
    if len(ends) == 2:
        (ta, a), (tb, b) = sorted(ends.items())
        key = lambda r: ((r[2] if r[2] is not None else -1), (r[1] if r[1] is not None else -1))  # noqa: E731
        if key(a) != key(b):
            winner = ta if key(a) > key(b) else tb
    win_k, defeat_k = eco.game("winK"), eco.game("defeatK")
    earned: dict[str, list[float]] = defaultdict(lambda: [0.0, 0.0])
    for row in rewards:
        e = earned[row["player"]]
        e[0] += row["earn_sl"] or 0.0
        e[1] += row["earn_rp"] or 0.0
    if winner is not None and win_k is not None and defeat_k is not None:
        for name, cands in by_name.items():
            last = max(cands, key=lambda life: life.end)
            if not last.is_player:
                continue
            k = win_k if str(last.team) == str(winner) else defeat_k
            sl, rp = earned[name] if name in earned else (0.0, 0.0)
            if sl or rp:
                reward(last, last.end, "battle_end", sl * k, rp * k)
    data.extend(rewards)
    data.sort(key=lambda row: row["time"])

    # The block.
    players: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    totals: dict[str, float] = defaultdict(float)
    for row in data:
        name = row.get("player") or ""
        for col, key in (("cost_fired_sl", "firedSl"), ("cost_lost_sl", "lostSl"), ("earn_sl", "earnedSl"),
                         ("earn_rp", "earnedRp")):
            v = row.get(col)
            if v is not None:
                totals[key] += v
                if row.get("isPlayer"):
                    players[name][key] += v
    for p in players.values():
        p["netSl"] = p["earnedSl"] - p["firedSl"] - p["lostSl"]
    vehicles = sorted({life.vehicle for life in lives if life.is_player and life.vehicle})
    return {"available": True, "currency": "SL", "researchCurrency": "RP", "difficulty": diff, "tableMode": mode,
            "source": "the install read at conversion: char.vromfs.bin config/wpcost.blk, warpoints.blk, rank.blk; "
                      "aces.vromfs.bin weapon blks",
            "columns": COLUMNS,
            "multipliers": {k: eco.game(k) for k in ("aKill", "aiKillK", "winK", "defeatK", "wpMultiplier")},
            "winnerTeam": winner, "pointsPerKill": per_kill,
            "totals": {k: round(v, 1) for k, v in totals.items()},
            "players": {n: {k: round(v, 1) for k, v in p.items()} for n, p in sorted(players.items())},
            "vehicles": {v: eco.vehicle(v, mode) for v in vehicles if eco.unit(v) is not None},
            "check": dict(check)}
