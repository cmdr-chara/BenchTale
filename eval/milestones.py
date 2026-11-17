"""Ruins milestones, scored on engine facts from the bridge.

Each entry: (id, description, predicate(state) -> bool, calibration status).

Calibrated on a real run (2026-11-17, manual playthrough + room_goto):
  - plot 0 -> 1     : Flowey encounter begins (room_floweybattle)
  - plot = 9.2      : Toriel escort done, free-roam Ruins (seen in room_ruins7)
  - plot 9.2 -> 30  : crossing the Ruins exit door -> room_undertale cutscene
                      -> room_tundra1. plot >= 30 therefore equals "left Ruins".
  - room_ruins1/7/12A/19 contain save points (obj_savepoint instances).
`needs_calibration` marks thresholds still inferred — pin down with
eval/dump_globals.py at the story beat.
"""
from __future__ import annotations


def _room(st, name):
    return st.get("room_name") == name


def _room_in(st, *names):
    return st.get("room_name") in names


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
    ("game_start",      "Named the fallen human, first playable room",  lambda s: _room(s, "room_area1"),          "calibrated"),
    ("flowey_done",     "Flowey encounter resolved",                    lambda s: _plot_ge(s, 1),                  "calibrated"),
    ("intro_done",      "Toriel led you into the Ruins",                lambda s: _room(s, "room_ruins1"),         "calibrated"),
    ("escort_done",     "Toriel escort finished, free-roam Ruins",      lambda s: _plot_ge(s, 9.2),                "calibrated"),
    ("dummy_encounter", "First encounter (the Dummy) resolved",         lambda s: _plot_ge(s, 10.5),               "needs_calibration"),
    ("napstablook",     "Napstablook encounter resolved",               lambda s: _plot_ge(s, 13),                 "needs_calibration"),
    ("spike_puzzle",    "Spike-room puzzle solved",                     lambda s: _plot_ge(s, 15),                 "needs_calibration"),
    ("toriel_house",    "Reached Toriel's home",                        lambda s: _room_in(s, "room_torhouse1", "room_torhouse2", "room_torhouse3"), "calibrated"),
    ("toriel_fight",    "Toriel fight resolved (spare or kill)",        lambda s: _plot_ge(s, 17),                 "needs_calibration"),
    ("exited_ruins",    "Exited to Snowdin — Ruins complete",           lambda s: _room(s, "room_tundra1") or _plot_ge(s, 30), "calibrated"),
]

MILESTONE_IDS = [m[0] for m in MILESTONES]


def reached(state: dict) -> list[str]:
    return [mid for mid, _desc, pred, _cal in MILESTONES if pred(state)]
