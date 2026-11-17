"""Ruins milestones, scored on engine facts from the bridge.

Each entry: (id, description, predicate(state) -> bool, calibration status).
`needs_calibration` marks thresholds inferred but not yet verified against a
real run — use eval/dump_globals.py at known story beats to pin them down.
"""
from __future__ import annotations


def _room(st, name):
    return st.get("room_name") == name


def _plot_ge(st, v):
    return st.get("plot", 0) is not None and st["plot"] >= v


def _flag(st, i, v):
    csv = st.get("flags_csv") or ""
    parts = csv.rstrip(",").split(",")
    if len(parts) <= i or not parts[i]:
        return False
    try:
        return float(parts[i]) == v
    except ValueError:
        return parts[i] == v


MILESTONES = [
    ("intro_done",      "Intro cinematics passed, in the Ruins",        lambda s: _room(s, "room_ruins1"),        "calibrated"),
    ("dummy_encounter", "First encounter (the Dummy) resolved",         lambda s: _plot_ge(s, 10.5),              "needs_calibration"),
    ("first_puzzle",    "First switch/lever puzzle solved",             lambda s: _room(s, "room_ruins7") or _plot_ge(s, 11), "needs_calibration"),
    ("napstablook",     "Napstablook encounter resolved",               lambda s: _plot_ge(s, 13),                "needs_calibration"),
    ("spike_puzzle",    "Spike-room puzzle solved",                     lambda s: _plot_ge(s, 15),                "needs_calibration"),
    ("toriel_house",    "Reached Toriel's home",                        lambda s: _room(s, "room_torielhouse1"),  "needs_calibration"),
    ("toriel_fight",    "Toriel fight resolved (spare or kill)",        lambda s: _plot_ge(s, 17),                "needs_calibration"),
    ("exited_ruins",    "Exited to Snowdin — Ruins complete",           lambda s: _room(s, "room_tundra1"),       "calibrated"),
]

MILESTONE_IDS = [m[0] for m in MILESTONES]


def reached(state: dict) -> list[str]:
    return [mid for mid, _desc, pred, _cal in MILESTONES if pred(state)]
