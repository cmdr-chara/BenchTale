"""Ruins milestones, scored on engine facts from the bridge.

Each entry: (id, description, predicate(state) -> bool, calibration status).

Fully calibrated from the game's own code (data.win CodeEntries, 2026-11-17):
every story beat writes global.plot at a known trigger —

    1   obj_floweytrigger        Flowey encounter
    2   ruins1 savepoint/toroverworld collisions
    3-5.5 torieltrigger1-3 + plotswitch1-2   Toriel escort & switch tutorial
    6   obj_dummy1               Dummy battle starts (interact -> obj_battler)
    7   torieltrigger3           Dummy battle resolved
    7.5-8.5 torhandhold1/toroverworld7       hand-holding corridor
    9   torieltrigger4                       end of escort
    9.2-9.8 torielcall1-4                    first phone calls
    10.4 obj_napstablook1        Napstablook encounter begins
    11  napstablook resolved (also: Toriel KILLED sets plot=11 —
        spare instead sets global.flag[45]=5, fight ends mnfight=99)
    12  torielcall5
    13  plotswitch3
    14-16 ruins15B/C/D switch reads          three-switch / spike corridor
    17-19 torieltrigger5-7                   approach to Toriel's house
    19.1-19.9 in-house SCR_TEXT dialogues (pie etc.)
    20-21 obj_chairiel           sitting at the table
    22-25 torieltrigger9-12      basement walk toward the door
    28  obj_floweytrigger2       Flowey at the exit
    30  obj_demodoorA            Ruins exit door -> room_tundra1

Save points (obj_savepoint): room_ruins1, room_ruins7, room_ruins12A,
room_ruins19 — all also set plot>=2 on use.
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
    ("game_start",      "Named the fallen human, first playable room",  lambda s: _room(s, "room_area1"),           "calibrated"),
    ("flowey_done",     "Flowey encounter resolved",                    lambda s: _plot_ge(s, 1),                   "calibrated"),
    ("ruins_entry",     "Toriel led you into the Ruins",                lambda s: _room(s, "room_ruins1"),          "calibrated"),
    ("dummy_encounter", "The Dummy (Toriel's demo fight) resolved",     lambda s: _plot_ge(s, 7),                   "calibrated"),
    ("escort_done",     "Hand-holding done, free-roam Ruins",           lambda s: _plot_ge(s, 9),                   "calibrated"),
    ("napstablook",     "Napstablook encounter resolved",               lambda s: _plot_ge(s, 11) or _flag(s, 45, 5), "calibrated"),
    ("spike_corridor",  "Three-switch spike corridor (ruins15) done",   lambda s: _plot_ge(s, 16),                  "calibrated"),
    ("toriel_house",    "Reached Toriel's home",                        lambda s: _room_in(s, "room_torhouse1", "room_torhouse2", "room_torhouse3"), "calibrated"),
    ("toriel_fight",    "Toriel fight resolved (spare: flag45=5, kill: plot=11 from >=25)", lambda s: _flag(s, 45, 5) or _room(s, "room_ruinsexit"), "calibrated"),
    ("exited_ruins",    "Exited to Snowdin — Ruins complete",           lambda s: _room(s, "room_tundra1") or _plot_ge(s, 30), "calibrated"),
]

MILESTONE_IDS = [m[0] for m in MILESTONES]


def reached(state: dict) -> list[str]:
    return [mid for mid, _desc, pred, _cal in MILESTONES if pred(state)]
