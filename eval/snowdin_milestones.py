"""Snowdin milestones — calibrated from data.win decompile (docs/BINDINGS.md).

plot spine: 36 sans intro -> 37/40/43/47 papyrus scenes -> 41 doggo ->
49-51 dogi -> 53/57/63 xoxo -> 60 greatdog -> 67 tile puzzle ->
100 PAPYRUS FIGHT -> 101 town -> 104 waterfall.

battlegroups: 23 doggo, 25 dogi, 26 greatdog, 27 papyrus, 135 glyde.
flags: 45 toriel, 52 doggo, 53 dogi, 54 greatdog, 55 lesserdog,
      57 snowdrake, 66-68 papyrus, 222-225 area kill markers,
      5 = fun value.
"""
from __future__ import annotations

from milestones import _room, _room_in, _plot_ge, _flag, _has_item, _kills_ge


def _battlegroup(st, v):
    return st.get("battlegroup") == v


SNOWDIN_MILESTONES = [
    ("snowdin_entry",    "Exited Ruins into Snowdin forest",        lambda s: _room_in(s, "room_tundra1", "room_tundra2", "room_tundra3"), "calibrated"),
    ("sans_intro",       "Sans introduced himself (lamp scene)",    lambda s: _plot_ge(s, 36),   "calibrated"),
    ("papyrus_meet",     "Met Papyrus",                             lambda s: _plot_ge(s, 37),   "calibrated"),
    ("doggo_done",       "Doggo sentry fight resolved",             lambda s: _plot_ge(s, 41) or _flag(s, 52, 1) or _flag(s, 52, 2), "calibrated"),
    ("maze_done",        "Invisible Electricity Maze cleared",      lambda s: _plot_ge(s, 43),   "calibrated"),
    ("word_search",      "Monster Kidz Word Search scene",          lambda s: _plot_ge(s, 47),   "calibrated"),
    ("dogi_done",        "Dogamy & Dogaressa resolved",             lambda s: _plot_ge(s, 51) or _flag(s, 53, 1) or _flag(s, 53, 2), "calibrated"),
    ("xoxo_done",        "XOXO puzzles cleared",                    lambda s: _plot_ge(s, 63),   "calibrated"),
    ("greatdog_done",    "Greater Dog resolved",                    lambda s: _plot_ge(s, 60) or _flag(s, 54, 1) or _flag(s, 54, 2), "calibrated"),
    ("tile_puzzle",      "Multicolor tile puzzle scene",            lambda s: _plot_ge(s, 67),   "calibrated"),
    ("papyrus_fight",    "Papyrus boss fight resolved",             lambda s: _plot_ge(s, 100),  "calibrated"),
    ("snowdin_town",     "Reached Snowdin Town",                    lambda s: _plot_ge(s, 101),  "calibrated"),
    ("waterfall_entry",  "Left Snowdin for Waterfall",              lambda s: _plot_ge(s, 104),  "calibrated"),
]

SNOWDIN_OPTIONAL = [
    ("papyrus_spared",   "Papyrus spared (fight won, no kill)",     lambda s: _plot_ge(s, 100) and _flag(s, 68, 1), "needs_calibration"),
    ("papyrus_killed",   "Papyrus killed",                          lambda s: _flag(s, 67, 1),   "needs_calibration"),
    ("tough_glove",      "Tough Glove from Box Road dimensional box", lambda s: _has_item(s, 14), "calibrated"),
    ("nice_cream",       "Bought a Nice Cream",                     lambda s: _has_item(s, 17),  "calibrated"),
    ("snowman_piece",    "Took a Snowman Piece",                    lambda s: _has_item(s, 16),  "calibrated"),
    ("fried_snow",       "Fell for Sans's fried snow",              lambda s: _flag(s, 60, 1),   "needs_calibration"),
    ("glyde",            "Found secret boss Glyde (mysterious door)", lambda s: _battlegroup(s, 135) or _flag(s, 282, 1), "calibrated"),
    ("genocide_snowdin", "Snowdin kill counter exhausted",          lambda s: _flag(s, 222, 1),  "needs_calibration"),
]

SNOWDIN_IDS = [m[0] for m in SNOWDIN_MILESTONES]


def reached(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in SNOWDIN_MILESTONES if p(state)]


def reached_optional(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in SNOWDIN_OPTIONAL if p(state)]
