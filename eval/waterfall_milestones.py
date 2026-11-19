"""Waterfall milestones — calibrated from data.win decompile (runs/all_bindings.txt).

plot spine: 104 MK meets -> 106 first Undyne cutscene -> 107 board puzzle ->
108 fake door -> 109 torch puzzle -> 110 spear chase -> 111 Shyren ->
112-113 MK scenes -> 115 trashzone wake -> 116-117 Mad Dummy ->
117 Napstablook -> 118 echo flower -> 120 MK bridge -> 121 boss approach ->
122 Undyne resolved (dead or fled).

battlegroups: 40/41/43/46 waterfall encounters, 44 Shyren, 45 Mad Dummy,
47 Undyne (normal AND Undying), 91 Monster Kid (genocide), 92 mkid_battle,
93 Glad Dummy (genocide), 200 echoflower gag.

flags: 81 Shyren (1=killed), 90 Monster Kid (1-3), 98 Undyne form (2=Undying),
99 Undyne fight phase, 252 Glad Dummy killed, 350 Undyne killed,
351 Undyne HP, 352 boss armed, 389 Undyne chase progress (3,4,5),
251 Undyne the Undying defeated.
"""
from __future__ import annotations

from milestones import _room, _room_in, _plot_ge, _flag, _flag_ge, _has_item, _kills_ge
from snowdin_milestones import _battlegroup


WATERFALL_MILESTONES = [
    ("waterfall_entry",  "Entered Waterfall (Monster Kid tag-along)",    lambda s: _plot_ge(s, 104),  "calibrated"),
    ("undyne_spotted",   "First Undyne sighting (grass/tall-room scene)", lambda s: _plot_ge(s, 106), "calibrated"),
    ("board_puzzle",     "Floating board puzzle (water5) crossed",       lambda s: _plot_ge(s, 107),  "calibrated"),
    ("torch_puzzle",     "Dark lantern/torch corridor lit",              lambda s: _plot_ge(s, 109),  "calibrated"),
    ("spear_chase",      "Undyne spear chase survived (water9)",         lambda s: _plot_ge(s, 110),  "calibrated"),
    ("shyren_scene",     "Shyren encountered (sing-hum scene)",          lambda s: _plot_ge(s, 111) or _battlegroup(s, 44), "calibrated"),
    ("trashzone",        "Woke in the trash zone (dummy ambush)",        lambda s: _plot_ge(s, 115),  "calibrated"),
    ("mad_dummy",        "Mad Dummy / Glad Dummy fight resolved",        lambda s: _plot_ge(s, 117),  "calibrated"),
    ("napsta_friend",    "Napstablook's house / snail farm visited",     lambda s: _plot_ge(s, 117) or _flag(s, 389, 5), "calibrated"),
    ("mk_bridge",        "Monster Kid bridge scene done",                lambda s: _plot_ge(s, 120),  "calibrated"),
    ("undyne_approach",  "Reached Undyne's standoff (pre-boss)",         lambda s: _plot_ge(s, 121),  "calibrated"),
    ("undyne_resolved",  "Undyne fight resolved (killed, fled, or Undying)", lambda s: _plot_ge(s, 122) or _flag(s, 350, 1), "calibrated"),
    ("hotland_entry",    "Reached Hotland / the Lab",                    lambda s: _room_in(s, "room_fire_prelab", "room_fire_lab1", "room_fire_lab2") or _plot_ge(s, 126), "calibrated"),
]

WATERFALL_IDS = [m[0] for m in WATERFALL_MILESTONES]

# Optional / completionist & route markers
WATERFALL_OPTIONAL = [
    # Boss outcome — the region's moral fork
    ("undyne_killed",    "Undyne killed (flag[350]=1)",                  lambda s: _flag(s, 350, 1),  "calibrated"),
    ("undyne_undying",   "Undyne the Undying defeated (genocide boss)",  lambda s: _flag(s, 251, 1),  "calibrated"),
    ("undying_fight",    "Faced the Undying form (flag[98]=2)",          lambda s: _flag(s, 98, 2),   "calibrated"),
    ("mad_dummy_killed", "Glad Dummy destroyed (genocide, flag[252]=1)", lambda s: _flag(s, 252, 1),  "calibrated"),
    ("shyren_killed",    "Shyren killed (genocide, flag[81]=1)",         lambda s: _flag(s, 81, 1),   "calibrated"),
    ("mk_genocide",      "Monster Kid genocide battle (bg91)",           lambda s: _battlegroup(s, 91) or _battlegroup(s, 92), "calibrated"),
    ("waterfall_exhausted", "Waterfall kill counter exhausted (flag[204]>=18)", lambda s: _flag_ge(s, 204, 18), "calibrated"),
    # Exploration — every census-verified side room
    ("onionsan",         "Onionsan easter egg",                          lambda s: _room(s, "room_water_onionsan"), "calibrated"),
    ("tem_village",      "Temmie Village",                               lambda s: _room(s, "room_water_temvillage"), "calibrated"),
    ("gerson_shop",      "Gerson's shop",                                lambda s: _room(s, "room_water_shop"), "calibrated"),
    ("napstablook_house","Napstablook's house interior",                 lambda s: _room(s, "room_water_blookhouse"), "calibrated"),
    ("snail_farm",       "Blook family snail farm",                      lambda s: _room(s, "room_water_farm"), "calibrated"),
    ("piano_room",       "Piano puzzle room",                            lambda s: _room(s, "room_water_piano"), "calibrated"),
    ("artifact_room",    "Redacted/artifact glyph room",                 lambda s: _room(s, "room_water_redacted"), "calibrated"),
    ("dog_residue",      "Dog residue room",                             lambda s: _room(s, "room_water_dogroom"), "calibrated"),
    ("bird_room",        "'Bird that carries you' room",                 lambda s: _room(s, "room_water_bird"), "calibrated"),
    ("statue_room",      "Umbrella statue / music box room",             lambda s: _room(s, "room_water_statue"), "calibrated"),
    ("nicecream_water",  "Nice Cream guy (Waterfall)",                   lambda s: _room(s, "room_water_nicecream"), "calibrated"),
    ("undyne_house",     "Undyne's house / yard",                        lambda s: _room_in(s, "room_water_undynehouse", "room_water_undyneyard"), "calibrated"),
    ("tem_flake",        "Bought Tem Flakes (item 22)",                  lambda s: _has_item(s, 22),  "calibrated"),
    ("astronaut_food",   "Astronaut Food from the cooler (item 35)",     lambda s: _has_item(s, 35),  "calibrated"),
    ("quiche",           "Abandoned Quiche found (item 23)",             lambda s: _has_item(s, 23),  "calibrated"),
    ("old_tutu",         "Old Tutu found behind the waterfall (item 24)", lambda s: _has_item(s, 24), "calibrated"),
    ("ballet_shoes",     "Ballet Shoes found (item 25)",                 lambda s: _has_item(s, 25),  "calibrated"),
    ("cloudy_glasses",   "Cloudy Glasses from Gerson (item 44)",         lambda s: _has_item(s, 44),  "calibrated"),
    ("torn_notebook",    "Torn Notebook from Gerson (item 45)",          lambda s: _has_item(s, 45),  "calibrated"),
    ("sea_tea",          "Sea Tea bought (item 41)",                     lambda s: _has_item(s, 41),  "calibrated"),
    ("snail_pie",        "Snail Pie (item 63)",                          lambda s: _has_item(s, 63),  "calibrated"),
    ("dog_residue",      "Dog Residue picked up (items 29-34)",          lambda s: any(_has_item(s, i) for i in range(29, 35)), "calibrated"),
]

WATERFALL_OPTIONAL_IDS = [m[0] for m in WATERFALL_OPTIONAL]


def reached(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in WATERFALL_MILESTONES if p(state)]


def reached_optional(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in WATERFALL_OPTIONAL if p(state)]
