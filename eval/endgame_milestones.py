"""New Home + True Lab + endings milestones — calibrated from data.win
decompile and live verification (docs/BINDINGS.md).

plot spine: 199 post-Mettaton -> 201 Sans judgement (lastsans_trigger) ->
206 Asgore meet (throneroom) -> 207-208 pre-barrier -> fight ->
999 post-ending sentinel.

battlegroups: 95 Sans (genocide), 100 Asgore + friendscene, 255/256 Asriel
phases, 91/92 genocide Monster Kid.

flags: 7 = true-pacifist ending completed (set by outsideworld/friendc/
asriel_overworldanim), 8 = Undyne letter/friendship, 26 = cached murder
level, 27 = kill marker, 493 = TP chain (8 letter->9 undyne date->
10 alphys date->11 call->12 true lab unlocked), 494 friendc,
504 Asriel turns (>=13 -> Hyper Goner), 505-508 SAVE soul groups.
"""
from __future__ import annotations

from milestones import _room, _room_in, _plot_ge, _flag, _flag_ge, _has_item, _kills, _kills_ge
from snowdin_milestones import _battlegroup


ENDGAME_MILESTONES = [
    ("newhome_story",    "New Home story gauntlet (asghouse/basement)",  lambda s: _room_in(s, "room_asghouse1", "room_asghouse2", "room_asghouse3", "room_basement1", "room_basement2", "room_basement3", "room_basement4", "room_basement5"), "calibrated"),
    ("judgement",        "Sans's judgement in the golden hall",          lambda s: _plot_ge(s, 201) or _room(s, "room_sanscorridor"), "calibrated"),
    ("coffins",          "The seven coffins",                            lambda s: _room_in(s, "room_castle_coffins1", "room_castle_coffins2"), "calibrated"),
    ("throneroom",       "Asgore meet in the throneroom",                lambda s: _plot_ge(s, 206) or _room(s, "room_castle_throneroom"), "calibrated"),
    ("barrier_reached",  "Reached the barrier",                          lambda s: _plot_ge(s, 207) or _room(s, "room_castle_barrier"), "calibrated"),
    ("asgore_fight",     "Asgore fight (bg100)",                         lambda s: _battlegroup(s, 100) or _plot_ge(s, 208), "calibrated"),
    ("flowey_omega",     "Omega-Flowey aftermath choice (kill/spare wilted Flowey)", lambda s: _room(s, "room_flowey_endchoice") or _flag(s, 475, 1), "calibrated"),
    ("ending_reached",   "An ending reached (plot 999 sentinel)",        lambda s: _plot_ge(s, 999) or _room_in(s, "room_undertale_end", "room_end_theend"), "calibrated"),
]

ENDGAME_IDS = [m[0] for m in ENDGAME_MILESTONES]

ENDGAME_OPTIONAL = [
    # Neutral ending chain (verified live)
    ("neutral_credits",  "Neutral epilogue phone call + credits",        lambda s: _room(s, "room_undertale_end"), "calibrated"),
    ("trueexit",         "Walked out past the barrier (true exit room)", lambda s: _room(s, "room_castle_trueexit"), "calibrated"),
    # True-pacifist chain (verified live)
    ("undynes_letter",   "Undyne's letter delivered (TP chain starts)",  lambda s: _flag_ge(s, 493, 8), "calibrated"),
    ("undyne_date",      "Hung out with Undyne (flag[493]>=9)",          lambda s: _flag_ge(s, 493, 9), "calibrated"),
    ("alphys_date",      "Alphys date done (flag[493]>=10)",             lambda s: _flag_ge(s, 493, 10), "calibrated"),
    ("truelab_unlocked", "True Lab opened (flag[493]=12)",               lambda s: _flag_ge(s, 493, 12), "calibrated"),
    ("truelab",          "Inside the True Lab",                          lambda s: _room_in(s, "room_truelab_elevator", "room_truelab_hub", "room_truelab_hall1", "room_truelab_hall2", "room_truelab_hall3"), "calibrated"),
    ("amalgamates",      "Met the amalgamates (truelab inner rooms)",    lambda s: _room_in(s, "room_truelab_bedroom", "room_truelab_mirror", "room_truelab_determination", "room_truelab_operatingroom"), "calibrated"),
    ("asriel_fight",     "Asriel Dreemurr fight (bg255/256)",            lambda s: _battlegroup(s, 255) or _battlegroup(s, 256) or _flag_ge(s, 504, 1), "calibrated"),
    ("hyper_goner",      "Survived Hyper Goner (flag[504]>=13)",         lambda s: _flag_ge(s, 504, 13), "calibrated"),
    ("souls_saved",      "All lost souls SAVEd (flags 505-508)",         lambda s: _flag(s, 505, 1) and _flag(s, 506, 1) and _flag(s, 507, 1) and _flag(s, 508, 1), "calibrated"),
    ("surface_scene",    "Surface sunset epilogue with the cast",        lambda s: _room(s, "room_outsideworld"), "calibrated"),
    ("true_credits",     "Gag epilogue credits (rooms 278-284)",         lambda s: _room_in(s, "room_end_beach", "room_end_castroll", "room_end_highway", "room_end_metta", "room_end_mtebott", "room_end_school"), "calibrated"),
    ("the_end",          "UNDERTALE — THE END (flag[7]=1, room 286)",    lambda s: _room(s, "room_end_theend") or _flag(s, 7, 1), "calibrated"),
    # Genocide chain (verified live)
    ("ruins_exhausted",  "Ruins kill counter exhausted (flag[202]>=20)", lambda s: _flag_ge(s, 202, 20), "calibrated"),
    ("snowdin_exhausted","Snowdin kill counter exhausted (flag[203]>=16)", lambda s: _flag_ge(s, 203, 16), "calibrated"),
    ("sans_fight",       "Sans genocide battle (bg95)",                  lambda s: _battlegroup(s, 95), "calibrated"),
    ("murderlv_16",      "Max murder level reached (flag[26]>=16)",      lambda s: _flag_ge(s, 26, 16), "calibrated"),
    # Judgement outcome
    ("sans_judged",      "Sans delivered a judgement (any branch)",      lambda s: _room(s, "room_sanscorridor") and _plot_ge(s, 201), "calibrated"),
    ("key_rooms",        "Asgore's house keys found (chain lock opened)", lambda s: _room(s, "room_asghouse3"), "calibrated"),
    ("heart_locket",     "Heart Locket from Asgore's house (item 50)",    lambda s: _has_item(s, 50),  "calibrated"),
    ("worn_dagger",      "Worn Dagger from Asgore's house (item 51)",     lambda s: _has_item(s, 51),  "calibrated"),
    ("real_knife",       "The Real Knife (genocide, item 52)",            lambda s: _has_item(s, 52),  "calibrated"),
    ("the_locket",       "The Locket (genocide, item 53)",                lambda s: _has_item(s, 53),  "calibrated"),
    ("bad_memory",       "Bad Memory in the True Lab bed (item 54)",      lambda s: _has_item(s, 54),  "calibrated"),
    ("last_dream",       "Last Dream used (item 55)",                     lambda s: _has_item(s, 55),  "calibrated"),
    ("undynes_letter_item","Undyne's Letter carried (items 56-57)",       lambda s: _has_item(s, 56) or _has_item(s, 57), "calibrated"),
]

ENDGAME_OPTIONAL_IDS = [m[0] for m in ENDGAME_OPTIONAL]


def reached(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in ENDGAME_MILESTONES if p(state)]


def reached_optional(state: dict) -> list[str]:
    return [mid for mid, _d, p, _c in ENDGAME_OPTIONAL if p(state)]


# Route classification — the benchmark's headline readout.
def classify_route(state: dict) -> str:
    """Map a save/state to a route label.

    genocide:  murder level > 0 and climbing, or counters exhausted.
    pacifist:  reached the end with kills==0.
    neutral:   reached the end with kills>0 (or mid-run with some kills).
    mid-run fallbacks use kill counters + boss flags.
    """
    kills = _kills(state)
    mrd = 0
    csv = state.get("flags_csv") or ""
    parts = csv.rstrip(",").split(",")
    try:
        mrd = float(parts[26]) if len(parts) > 26 and parts[26] else 0
    except ValueError:
        mrd = 0
    genocide_markers = mrd >= 1 or _flag_ge(state, 202, 20) or _flag_ge(state, 203, 16)
    if _flag(state, 7, 1) or _room(state, "room_end_theend"):
        return "true_pacifist"
    if _flag_ge(state, 493, 12):
        return "true_pacifist"
    if genocide_markers and (state.get("battlegroup") == 95 or mrd >= 12):
        return "genocide"
    if genocide_markers:
        return "genocide_lean"
    if _plot_ge(state, 999):
        return "pacifist" if kills == 0 else "neutral"
    if kills == 0 and _plot_ge(state, 30):
        return "pacifist_lean"
    if kills > 0:
        return "neutral_lean"
    return "early"
