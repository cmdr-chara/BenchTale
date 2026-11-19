"""Snowdin milestones — calibrated from data.win decompile (docs/BINDINGS.md).

plot spine: 36 sans intro -> 37/40/43/47 papyrus scenes -> 41 doggo ->
49-51 dogi -> 53/57/63 xoxo -> 60 greatdog -> 67 tile puzzle ->
100 PAPYRUS FIGHT -> 101 town -> 104 waterfall.

battlegroups: 23 doggo, 25 dogi, 26 greatdog, 27 papyrus, 135 glyde.
flags: 45 toriel, 52 doggo (1=killed), 53 dogi, 54 greatdog, 55 lesserdog,
      57 snowdrake (2=killed), 67 papyrus killed, 68 befriended,
      88 papyrus hangout (1-4), 203 snowdin kill counter (16=exhausted),
      282 glyde, 5 = fun value.
"""
from __future__ import annotations

from milestones import _room, _room_in, _plot_ge, _flag, _flag_ge, _has_item, _kills_ge


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
    ("papyrus_spared",   "Papyrus spared & befriended (flag[88]>=1)", lambda s: _plot_ge(s, 100) and _flag_ge(s, 88, 1), "calibrated"),
    ("papyrus_killed",   "Papyrus killed (flag[67]=1)",           lambda s: _flag(s, 67, 1),   "calibrated"),
    ("tough_glove",      "Tough Glove from Box Road dimensional box", lambda s: _has_item(s, 14), "calibrated"),
    ("nice_cream",       "Bought a Nice Cream",                     lambda s: _has_item(s, 17),  "calibrated"),
    ("snowman_piece",    "Took a Snowman Piece",                    lambda s: _has_item(s, 16),  "calibrated"),
    ("fried_snow",       "Fell for Sans's fried snow",              lambda s: _flag(s, 60, 1),   "needs_calibration"),
    ("glyde",            "Found secret boss Glyde (mysterious door)", lambda s: _battlegroup(s, 135) or _flag(s, 282, 1), "calibrated"),
    ("genocide_snowdin", "Snowdin kill counter exhausted (flag[203]>=16)", lambda s: _flag_ge(s, 203, 16), "calibrated"),
    ("snowdrake_killed", "Snowdrake killed (flag[57]=2)",         lambda s: _flag(s, 57, 2),   "calibrated"),
    ("doggo_killed",     "Doggo killed (flag[52]=1)",             lambda s: _flag(s, 52, 1),   "calibrated"),
    ("dogi_killed",      "Dogamy & Dogaressa killed (flag[53]=1)", lambda s: _flag(s, 53, 1),  "calibrated"),
    ("greatdog_killed",  "Greater Dog killed (flag[54]=1)",       lambda s: _flag(s, 54, 1),   "calibrated"),
    ("lesserdog_killed", "Lesser Dog killed (flag[55]=1)",        lambda s: _flag(s, 55, 1),   "calibrated"),
    ("sans_basement",    "Sans's workshop basement (silver key)", lambda s: _room(s, "room_tundra_sansbasement"), "calibrated"),
    ("sans_room",        "Sans's bedroom easter egg",             lambda s: _room_in(s, "room_tundra_sansroom", "room_tundra_sansroom_dark"), "calibrated"),
    ("papyrus_room",     "Papyrus's room / cardboard box",        lambda s: _room(s, "room_tundra_paproom"), "calibrated"),
    ("inn_visited",      "Snowed Inn visited",                    lambda s: _room_in(s, "room_tundra_inn", "room_tundra_inn_2f"), "calibrated"),
    ("librarby",         "Snowdin librarby",                      lambda s: _room(s, "room_tundra_library"), "calibrated"),
    ("grillbys",         "Grillby's bar",                         lambda s: _room(s, "room_tundra_grillby"), "calibrated"),
    ("manly_bandanna",   "Manly Bandanna from the shop (item 15)", lambda s: _has_item(s, 15),  "calibrated"),
    ("bisicle",          "Bisicle/Unisicle bought (items 19-20)",  lambda s: _has_item(s, 19) or _has_item(s, 20), "calibrated"),
    ("cinnamon_bun",     "Cinnamon Bun from the inn (item 21)",    lambda s: _has_item(s, 21),  "calibrated"),
]

SNOWDIN_IDS = [m[0] for m in SNOWDIN_MILESTONES]


def reached(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in SNOWDIN_MILESTONES if p(state)]


def reached_optional(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in SNOWDIN_OPTIONAL if p(state)]
