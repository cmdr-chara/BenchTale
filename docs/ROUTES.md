# Route coverage — what distinguishes each route in engine state

All bindings below verified via data.win decompile + live flag probes.
Room-level coverage: every room in every region was entered live (see REGIONS.md).

## Shared state
- `global.kills` = total kills; flag[201] mirror.
- Kill counters per area: flag[202]=Ruins(20), flag[203]=Snowdin(16),
  flag[204]=Waterfall(18), flag[205]=CORE(40). flag[200] = active area's counter.
  Exhausting a counter empties NPCs/shops live (verified: f203=16 clears
  Snowdin vendor+ snowball).
- `global.plot` = main path spine (Ruins thresholds in milestones.py).
- flag[45] Toriel: 3 fled, 4 killed, 5 spared (verified live).
- flag[17]: Undyne water8 spear scene done.
- Battlegroups: bg22=Toriel, bg27=Papyrus, savepoint "monsters left" text
  exposes remaining kills for genocide runs.

## Neutral
Any mixed kill/spare profile ending at room_castle_barrier (237) → Asgore →
Flowey; ending scene = room_outsideworld (241, all friend actors present).

## Pacifist
kills==0 everywhere + all boss spare flags + no kill-counter progress.
Mechanically same rooms as neutral.

## True Pacifist
Neutral ending first (file flag), then friendship dates: Undyne
(room_water_undynehouse 118 — Papyrus cooking + Undyne date, verified intr=1
scene live), Papyrus date (room_water_blookhouse area), Alphys date
(room_fire_lab1/2) → letter → room_fire_labelevator (242) → True Lab
(243-263: levers, amalgams, power switch at 263) → barrier → Asriel finale
(rooms 330+ asrielappears/asrielmemory). room_undertale_end(239)=credits,
room_castle_trueexit(240) + room_outsideworld(241)=true ending.

## Genocide
Exhaust kill counters per area BEFORE bosses (savepoint shows "N left" →
"Determination." when exhausted). Route-unique content: room_water_redacted
(272, obj_redacted_a — verified loads), genocide Undyne = undynefinal chain
(134-136), Mettaton NEO (core_final 212?), Sans fight (sanscorridor 231 —
obj_lastsans_trigger), coffins/throne (233-237). Kill flag[45]=4 etc.

## Secret/easter-egg rooms (verified live)
- room_gaster (264): obj_gaster_room + OBJ_WRITER — fun-gated normally
- room_mysteryman (269): obj_mysteryman (grey door NPC)
- room_soundtest (270): obj_soundtest (fun 65 + pacifist spoiler tracks)
- room_water_fakehallway (268): empty — hallway variant
- room_icecave1 (265), room_ice_dog (266): ice-dog dev rooms
- room_overworld (274): obj_floweytrigger + obj_wanderparent
- room_water7_older (304): CRASHES the game on entry (modal FATAL) — blacklist

## Still open
- Papyrus bg27 legit pass at LV1 (dodge or grind) — task pending
- Real end-to-end route runs (genocide needs killable encounters or
  flag-assisted counters; flag-assisted verified: counters + NPC wipe live)
