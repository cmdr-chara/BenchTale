"""Hotland + CORE milestones — calibrated from data.win decompile.

plot spine: 122 post-Undyne -> 126 lab entry -> 127 Mettaton intro ->
130-143 lab phone calls -> 133/164 chip door -> 134-135 cooking show ->
140 tri-switch -> 146 resort scene -> 161 news report -> 165 Muffet ->
167-168 multitile -> 176 pre-CORE -> 179 CORE enemies -> 180-181 laser
switches -> 182-185 elevator calls -> 193 elevator sabotage ->
199 Mettaton EX/NEO resolved -> New Home.

battlegroups: 48 Mettaton quiz, 49 musical/standoff, 50-52/77-78/19 hotland
encounters, 56 Muffet, 57 multitile, 59-60 CORE scripted, 64-68 CORE
encounters + RG01/02, 69+bombtype news bombs, 80-81 Mettaton EX,
94 Mettaton NEO, 58 Undyne hangout (non-battle flag path).

flags: 281 So Sorry (1/2), 374 lab/shootguy switch, 397 Muffet killed,
402 Royal Guards fought, 425 Mettaton killed (EX or NEO),
88 Papyrus hangout (1-4), 493 TP chain (8 letter, 9 undyne date,
10 alphys date, 11+, 12 true lab unlocked), 8 Undyne friendship.
"""
from __future__ import annotations

from milestones import _room, _room_in, _plot_ge, _flag, _flag_ge, _has_item, _kills_ge
from snowdin_milestones import _battlegroup


HOTLAND_MILESTONES = [
    ("lab_entered",      "Entered Alphys's lab",                         lambda s: _room_in(s, "room_fire_lab1", "room_fire_lab2") or _plot_ge(s, 126), "calibrated"),
    ("quiz_show",        "Mettaton quiz show (bg48)",                    lambda s: _battlegroup(s, 48) or _plot_ge(s, 127), "calibrated"),
    ("cooking_show",     "Mettaton cooking show done",                   lambda s: _plot_ge(s, 135),  "calibrated"),
    ("triswitch",        "Tri-switch puzzle (conveyor lasers)",          lambda s: _plot_ge(s, 140),  "calibrated"),
    ("resort_reached",   "MTT Resort reached",                           lambda s: _plot_ge(s, 146) or _room_in(s, "room_fire_hotellobby", "room_fire_hotelfront_1", "room_fire_hotelfront_2"), "calibrated"),
    ("news_report",      "Mettaton news report / bomb defusal",          lambda s: _plot_ge(s, 161),  "calibrated"),
    ("muffet_fight",     "Muffet boss fight (bg56)",                     lambda s: _battlegroup(s, 56) or _plot_ge(s, 165), "calibrated"),
    ("multitile_done",   "Hotland multitile gauntlet cleared",           lambda s: _plot_ge(s, 168),  "calibrated"),
    ("core_entered",     "Entered the CORE",                             lambda s: _plot_ge(s, 176) or _room_in(s, "room_fire_core1", "room_fire_coreview2"), "calibrated"),
    ("core_lasers",      "CORE laser switch sequence done",              lambda s: _plot_ge(s, 181),  "calibrated"),
    ("elevator_sabotage","Mettaton's elevator trap sprung",              lambda s: _plot_ge(s, 193),  "calibrated"),
    ("mettaton_boss",    "Mettaton EX / NEO fight resolved",             lambda s: _plot_ge(s, 199) or _flag(s, 425, 1), "calibrated"),
    ("newhome_entry",    "Reached New Home / castle elevator",           lambda s: _room_in(s, "room_castle_elevatorout", "room_castle_front", "room_castle_precastle"), "calibrated"),
]

HOTLAND_IDS = [m[0] for m in HOTLAND_MILESTONES]

HOTLAND_OPTIONAL = [
    # Boss outcomes
    ("muffet_killed",    "Muffet killed (flag[397]=1)",                  lambda s: _flag(s, 397, 1),  "calibrated"),
    ("mettaton_killed",  "Mettaton destroyed (flag[425]=1)",             lambda s: _flag(s, 425, 1),  "calibrated"),
    ("mettaton_neo",     "Faced Mettaton NEO (genocide, bg94)",          lambda s: _battlegroup(s, 94), "calibrated"),
    ("royal_guards",     "Royal Guard 01/02 fight (flag[402]=1)",        lambda s: _flag(s, 402, 1) or _battlegroup(s, 64) or _battlegroup(s, 67) or _battlegroup(s, 68), "calibrated"),
    ("hotland_exhausted","Hotland+CORE kill counter exhausted (flag[205]>=40)", lambda s: _flag_ge(s, 205, 40), "calibrated"),
    # Exploration — census-verified side rooms
    ("sans_hotdog",      "Sans's hotdog stand",                          lambda s: _room(s, "room_fire_hotdog"), "calibrated"),
    ("sans_restaurant",  "Sans's MTT restaurant date",                   lambda s: _room(s, "room_fire_restaurant") or _room(s, "room_fire_boysnightout"), "calibrated"),
    ("art_club",         "So Sorry secret boss room (flag[281])",        lambda s: _room(s, "room_fire_sorry") or _flag(s, 281, 1) or _flag(s, 281, 2), "calibrated"),
    ("mewmew_room",      "Mew Mew Kissy Cutie 2 room",                   lambda s: _room(s, "room_fire_mewmew2"), "calibrated"),
    ("shootguy_done",    "Shootguy minigame cleared (flag[374])",        lambda s: _flag(s, 374, 1),  "calibrated"),
    ("spider_bakesale",  "Muffet's bake sale corridor",                  lambda s: _room(s, "room_fire_spidershop"), "calibrated"),
    ("opera_stage",      "Opera/musical stage room",                     lambda s: _room(s, "room_fire_operatest"), "calibrated"),
    ("core_warrior",     "CORE warrior event (bg64/67/68)",              lambda s: _room(s, "room_fire_core_warrior"), "calibrated"),
    ("hotel_bed",        "MTT hotel bed / room-service knock room",      lambda s: _room(s, "room_fire_hotelbed"), "calibrated"),
    ("stained_apron",    "Stained Apron found",                          lambda s: _has_item(s, 46),  "needs_calibration"),
    ("burnt_pan",        "Burnt Pan found",                              lambda s: _has_item(s, 45),  "needs_calibration"),
    ("glamburger",       "Bought a Glamburger at the resort",            lambda s: _has_item(s, 27),  "needs_calibration"),
    ("mettaton_face_steak","Mettaton-shaped steak",                      lambda s: _has_item(s, 32),  "needs_calibration"),
]

HOTLAND_OPTIONAL_IDS = [m[0] for m in HOTLAND_OPTIONAL]


def reached(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in HOTLAND_MILESTONES if p(state)]


def reached_optional(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in HOTLAND_OPTIONAL if p(state)]
