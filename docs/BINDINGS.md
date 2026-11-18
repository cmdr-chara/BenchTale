# Undertale engine bindings — extracted from data.win (2026-11-18)

Full decompile dump: `runs/all_bindings.txt` (3,797 lines). This is the
calibration backbone for every region's milestones.

## global.plot — the story spine

| plot | object | beat |
|---|---|---|
| 0-30 | (see milestones.py header) | Ruins — already calibrated |
| 36 | obj_darksans1 | Sans intro (Snowdin walkway) |
| 37 | obj_papyrus1-5, obj_sansbyetrigger | Papyrus meets Sans scenes |
| 40 | obj_papyrus1_Step | first Papyrus puzzle intro |
| 41 | obj_movedoge_Destroy | Doggo resolved |
| 42 | obj_dogetrigger1 | Doggo post-scene |
| 43 | obj_papyrus2_Step | Invisible Electricity Maze done |
| 47 | obj_papyrus3_Step | word-search scene done |
| 49-51 | obj_forcedright, obj_mandog_Destroy, obj_readable_room1 | Dogi (Dogamy&Dogaressa) |
| 53,57,63 | obj_xoxocontroller1 | XOXO puzzle beats |
| 58 | obj_papyrus4_Step | XOXO / Sans scene |
| 60 | obj_greatdog_Destroy | Greater Dog resolved |
| 61,65 | obj_pofftrigger | Poff/junior jumble scene beats |
| 67 | obj_papyrus7_Step | multicolor tile puzzle scene done |
| **100** | obj_papyrusboss_Other_12 | **PAPYRUS FIGHT resolved** |
| 101 | obj_papyrus8_Step | post-fight → Snowdin Town |
| 104 | obj_monsterkidtrigger2 | Waterfall: Monster Kid |
| 106 | obj_undyne1 | Undyne first sighting |
| 107-108 | phonecall/fakedoor | Waterfall mid |
| 109 | obj_torchpuzzle | torch puzzle |
| 110 | obj_undyneencounter2 | Undyne spear chase |
| 111 | obj_shyrentrigger | Shyren |
| 112-113 | obj_monsterkidtrigger6 | Monster Kid bridge |
| 115 | obj_wakeupchara | garbage dump wake |
| 116-117 | obj_dummytrigger, obj_napstablookfriendtrigger | Mad Dummy / Napsta |
| 118 | obj_undyne_echoflower | echo flowers |
| 120-122 | mkid 7/8 + undynetrigger_boss + undyneboss | **Undyne boss ~122** |
| 126-127 | obj_alphystrigger1/2 | Hotland: Alphys lab |
| 130-146 | phonecall/triswitch/cookshow/boysnightout | Hotland events |
| 160 | obj_killerlab_event | lab back-area |
| 161 | obj_mettnewsevent | news report |
| 164-165 | chipdoor / spidertalkevent | Muffet zone |
| 167-168 | playmovement/multitileevent | MTT resort tile puzzle |
| 176-184 | precore/core_enemy/laserswitch/powerlaser | CORE |
| 193 | obj_mettdestroyed_event | post-Mettaton |
| 199 | obj_mettboss_event | **Mettaton EX/NEO resolved** |
| 201 | obj_lastsans_trigger, obj_lab_powerswitch | **Sans judgment** / True Lab power |
| 206-208 | asgoremeet / asgore_prebarrier | Asgore + barrier |
| 999 | obj_asriel_overworldanim, obj_friendc_event | True Pacifist finale |

## battlegroup ids (story encounters)

| id | fight | id | fight |
|---|---|---|---|
| 2 | Dummy | 20 | Napstablook |
| 22 | Toriel | 23 | Doggo |
| 25 | Dogi (Dogamy&Dogaressa) | 26 | Greater Dog |
| 27 | Papyrus | 44 | Shyren |
| 45/93 | Mad Dummy / Glad Dummy | 47 | Undyne (boss+chaser) |
| 56 | Muffet | 58 | Undyne hangout |
| 64/67/68 | warrior_event (RG01/02) | 69 | Mettaton news |
| 80/81/94 | Mettaton EX / NEO variants | 91/92 | Monster Kid |
| 95 | lastsans (Sans) | 100 | Asgore |
| 135 | Glyde (secret) | 140 | So Sorry (secret) |
| 255/256 | Asriel / ripoff friends | 19 | **"but nobody came"** (kill-exhausted area) |
| 82-86 | amalgams (True Lab) | 200 | undyne_echoflower |

## Route / outcome flags

| flag | meaning |
|---|---|
| flag[5] | **fun value** (gaster follower/event gating) |
| flag[45] | Toriel: 3 fled / 4 killed / 5 spared |
| flag[52] | Doggo outcome (1/2) |
| flag[53] | Dogi outcome (1/2) |
| flag[54] | Greater Dog (1/2/3) |
| flag[55] | Lesser Dog (1/2) |
| flag[57] | Snowdrake |
| flag[66]/[67]/[68] | Papyrus fight state/outcome |
| flag[27] | named-monster kills (bara/glad/greatdog) |
| flag[222]-[225] | area kill-counter markers: tundra/water/fire/core |
| flag[200] | kill-counter seeding (202/204/205) |
| flag[281] | So Sorry outcome |
| flag[282] | Glyde fought |
| flag[350] | Undyne outcome (0/1/2) |
| flag[389] | undyne date/napsta friend (3/4/5) |
| flag[390] | friendc variants |
| flag[497] | lastsans / judgment (1/2/3) |
| flag[500]/[501] | asriel battle / final panels |
| flag[509] | friendc event stages |
| flag[510] | asriel overworld anim |
| flag[512] | outsideworld (epilogue) |
| flag[475]/[476] | game completed / asgore last cutscene |
| flag[499] | castroll (True Pacifist credits) |
| flag[454]/[480]-[490] | True Lab: power switch, lab door, amalgams |
| flag[200]-series 251-285 | misc side-content (artclass 140, gladdummy 252, crossword 254, shops, dogshrine 293/295, onionsan 496, wrongnumbersong 277) |

## Regions → files

- Ruins: `eval/milestones.py` (calibrated)
- Snowdin: `eval/snowdin_milestones.py` (this doc's bindings)
- Waterfall/Hotland/NewHome/TrueLab: same pattern, plot+flag above.

## Live-verified mechanics (this session)

- **Savepoints**: touch → flavor text → auto-writes `file0` (continue point + respawn anchor). Verified: tundra_town @ (518,124). NOTE: the "File saved." box still has focus — press z once to dismiss before moving.
- **Death rollback**: death restores `file9` checkpoint state (kills/plot/hp/lv revert). Snowdin's file9 anchor predates Doggo → every death in early Snowdin returns to tundra4 @ LV1/plot40 until a forward savepoint is touched.
- **Papyrus (bg27, room_fogroom east end)**: never kills — hp→0 = capture → `room_tundra_garage` (shed, west exit only → tundra_town x2405). 3rd+ capture: "PERSISTENTEST" monologue, fight still re-triggers. Pass = survive full attack script then spare, or kill (680 HP).
- **Doggo**: attacks only moving targets — stand still in his phase = 0 dmg.
- **Dogi (bg25)**: trigger (447,402) in room_tundra_snowpuzz; plot→49 on start.
- **Menu cursor has memory**: stays on last column → blind z keeps re-picking (e.g. ACT→Check). Use `_nav_to_col(s,0)` before FIGHT.
- **myfight**: 0 = menu AND bullet phases; 1 = attack bar; 2 = text phase.
- **MERCY submenu is vertical** — down+z for Flee.
- **XOXO**: X→O on step; O→green△ on re-step (resets fvic). obj_xoxocontroller1 = LEVER (not ball): pull with all-O → plot advance; else full reset. flag[63] += solved attempts.
- **Kill counters (count UP)**: flag[202]=Ruins(genocide≥20), flag[203]=Snowdin(≥16), flag[204]=Waterfall(≥18), flag[205]=CORE/Hotland(≥40). flag[200]=active counter id (set by scr_steps arg3); flag[201]=global.kills snapshot; flag[222-225]=area kill markers. **Verified live**: `flag 203 16` → room_tundra8 loses Nice Cream vendor + snowball; flag[203]==0 repopulates them. Savepoint "Monsters left"/"But nobody came" text keys on flag[202]>=20 in-region (SCR_TEXT line ~9).
- **Encounters are progress-gated**: at plot 0, random encounters never fired in ~12k walked steps across Snowdin+Waterfall rooms — the encounter counter arms per actual game progress, not room visits. Kill-counter verification uses flags + object A/B, not grinding from plot 0.
- **Waterfall reachable**: `room_water_prewaterfall` loads (goto).
- **Papyrus re-fight softlock**: teleporting out of `room_tundra_garage` mid-capture then re-triggering the fight leaves the fight-#2 intro text unadvancable (no key works — z/x/enter all dead). Bail requires process restart or a non-battle goto.
- **Admin commands** (`bench_cmd.txt` lines, all logged as `admin` events): `heal 1`, `item <id>`, `gold <n>`, `flag <i> <v>`. Calibration-only — a scored run using them is marked assisted.
- **`keyboard_key_press` is OS-level**: IPC keys land in the *focused* window. With Chrome focused, z's type into its address bar. The UNDERTALE window must be foreground before any input-driven sequence.
- **`room_water10`, `room_fire_lab3-5`, `room_castle_hallway`, `room_castle_basement` do not exist** in this data.win (goto returns -1 → stays in current room).

## Coverage sweep (goto-verified, live)

| Region | Rooms OK / total | Notes |
|---|---|---|
| Ruins | full playthrough done | `runs/devin_first/` — 10/10 milestones |
| Snowdin | full spine + side rooms played | Papyrus fight mapped (capture loop, garage, softlock) |
| Waterfall | 35/36 | prewaterfall, waterfall1-20 (no 10), nicecream, piano, statue, trashzone1-2, blookyard, bridgepuzz1, preundyne, undynefinal1-3 |
| Hotland | 41/43 | fire1-10, prelab, lab1-2, elevators l/r 1-3, shootguy_1-5, preshootguy4, lasers1, walkandbranch1-2, restaurant, core1-5, core_bridge, core_warrior |
| New Home/Castle | 5/7 | castle_front, elevatorout, precastle, finalshoehorn, barrier |
| True Lab | 6/6 | hub, elevator, hall1, mirror, bedroom, power |
| Endgame | 3/3 | sanscorridor, asrielroom, asrieltest |

## Boot, freeze and death gotchas (live-verified 2026-11-18)

- **Fresh-boot intro never reaches `room_intromenu`**: `room_introstory` ↔ `room_introimage` cycle indefinitely (~5k frames per cycle) even with zero input — and pressing z during introimage restarts the cycle. `goto room_intromenu` lands on the Continue menu but z/enter do not trigger the load (focus/latency unclear). Working path: `goto` straight to a gameplay room instead of fighting the intro.
- **GOTO during intro leaves a stray `obj_writer`** (the story text crawl): it persists across rooms, holds `global.interact=1`, and freezes the player at the spawn point forever (px never moves, msg field keeps showing intro text). New `freeme` admin fixes it.
- **Admin `freeme`**: sets `global.interact=0`, destroys all `obj_writer`/`obj_dialoguer`/`obj_choicer`, and spawns `obj_mainchara` if absent. Send it once after every `goto` that lands while a cutscene/dialogue object is alive.
- **`room_gameover` crashes when file9 is missing**: `obj_gameover` Step calls `scr_tempload` → `ossafe_file_text_read_string` → "File is not opened for reading" error dialog that re-fires every frame (modal error loop; Ignore only advances to the next error). Root cause: death after a fresh boot that never created the file9 checkpoint. Fix: keep `%LOCALAPPDATA%/UNDERTALE/file9` present — copy of file0 works (same save format; the gameover reload then lands at the file0 savepoint).
- **f203 grind live-verified**: 6 real kills in room_tundra6/7 at plot 54 (bgs 24/30/32) incremented flag[203] 0→6 and global.kills 0→5; ~1 battle per 150-300 walked holds. Encounter rate visibly drops as the counter climbs; Snowdrake (bg30) flees at low hp — battle ends, counter still ticked once (end-battle counter behavior differs from kills). Flag-set `flag 203 16` reproduces exhausted state (vendor/snowball absent in tundra8, verified earlier).
- **`speed 60` during fights is lethal**: bullets move 2× while dodge reacts at wall-clock speed — instant death at LV1. Keep room_speed 30 for any real combat.

## Route-test recipe (fast path)

1. Boot → `goto <room>` (skip intro entirely) → `freeme` → `plot <n>` → `flag <ctr> <remaining>` for route state → play.
2. For gameover safety keep a file9 present before any death-risk work.
- **`freeme` must also nuke `obj_introimage`/`obj_unfader`/`obj_fader`/`obj_gameoverfake`/`obj_persistentfader`** — the boot-intro controller is *persistent* and survives `goto`; it keeps re-setting `global.interact=1` and re-creating the writer, re-freezing the player every frame. Found after water4/water5 freezes post-boot-goto.
- **goto can spawn inside collision** (water4 dropped the player at 495,279 wedged on all sides) — if px/py never change after freeme, re-goto or pick another room.
- **water5's east exit isn't a right-edge walk** — 200 right-holds never triggered a transition; the echo-flower room exits via a specific door/path (needs diagonal/route nav, or use goto).
- **room_water5 = water-boards puzzle**: `obj_waterboard`×4 + `obj_waterboardpuzzle1` controller; west door `obj_doorB`+`markerA` at (0,340); x=460 solidtall wall blocks east; the north path (y~280) is walled off from the water channel (y~340). Reach the channel via the west side (x<200) — from goto spawn it's blocked. water6/7/8 all load clean via goto+freeme.
- **Admin lines with NO argument were silently dropped**: the cmd parser gated on `string_pos(" ", line) > 0`, so a bare `freeme` never matched. Fixed in csx (k = whole line when no space); every prior "frozen despite freeme" episode was this bug, not a real freeze — the earlier water5 unfreeze was coincidence.
- **`with (obj_name)` inside the bridge crashes**: `obj_writer` resolved as a bridge instance variable → FATAL "not set before reading it" modal that silently froze the cmd reader while state kept updating (diagnose via: state frames advance but ack stalls). freeme now destroys by name-match over `with (all)`.
- **Substring matching killed obj_gameover**: matching `oname` inside a `|` list needs exact `|name|` boundaries both sides — `obj_gameover` is a substring of `obj_gameoverfake`; the loose match destroyed it and `obj_heartdefeated` alarm 4 FATALed on the missing object. After any crash: Abort the dialog, repatch, relaunch (Abort exits the game).
- **water8 encounters**: a battle fires ~halfway east (bg3, Aaron/Woshua at LV1 lethal in ~1 enemy turn; msg field shows `%%%` placeholders during battle intro). With flag[204]=18 encounters still fire — the exhausted flag only empties NPC/flavor content, not battlegroups. flag[200]=0 did not prevent it either.
- **Respawn loop**: z/enter taps on room_gameover reload file9 → lands at its savepoint room (tundra_town for the current file0 copy) with save stats. Works reliably now that file9 exists.
- **room_water8 has near-constant bg3 encounters** (Aaron/Woshua): a battle every few walk-holds east; flee via MERCY submenu doesn't reliably escape (flee chance + submenu vertical nav both fail often), so an LV1 walker ping-pongs at ~900-1140px forever. Admin `heal 1` mid-battle works but battles never end on flee alone — need real fight/dodge or a faster flee sequence. px resets to 0 on re-entry after some battles.
- **Never `freeme` during a battle or battle transition** — it breaks the encounter state machine into a perpetual `room→fastbattle→hp -4→room` loop that survives without any script attached; only a process kill clears it.

## freeme must NOT clear obj_mainchara.cutscene
`cutscene` is set by cutscene controllers (e.g. obj_undyneencounter1) to take over
`view_yview` animation. Clearing it makes obj_mainchara.Step_2 reset the view every
frame, permanently stalling controllers that wait for view_yview thresholds
(undyneencounter1 cn==1.2 → never cn==2 → interact stays 1 forever).
This was the real cause of the multi-minute "water8 freeze".

## Movement/input, verified
- `keyboard_check_direct` DOES observe `keyboard_key_press` simulation on this
  runtime; `keyboard_check` does NOT. Do not patch obj_time's direct reads.
- water8 spawn (140,159): wall lip at x~147 for y<=160 — dip to y>=162 before
  heading east. Same pattern probably applies elsewhere: always waypoint via
  the corridor midline, not the spawn y.

## Undyne chase sequence (water8 -> water9 -> spear minigame room 308+)
- Entering room_water8 spawns obj_undyneencounter1 unconditionally (flag[17]
  does not skip it); trigger at x>280. Sequence: cn 0.2 spear drop -> cn 4
  interact release + flag[17]=1 -> cn 8-10 chase with obj_uspeargen ->
  spear-dodge minigame room (~308) -> room_water9 chase2 -> knock into
  trashzone (obj_wakeupchara scene, intr=1).
- The minigame is LETHAL at LV1 for an agent without real dodging (hp 20 -> 0).
  For flag-level coverage hop past it: goto room_water9/10 still re-triggers
  chase controllers — goto room_water_savepoint1 (94) or later instead.

## Waterfall room census
61 rooms visited live (goto+scan), census in runs/water_sweep.json.
Path order after water9: room_water_savepoint1(94) -> water11 -> ... ->
undynefinal(134-136). Boss rooms: undynebridge(111)=encounter3,
undynebridgeend(112)=encounter4, undynefinal(134) boss triggers,
undynefinal3(136)=transheart intro. Interactions found: piano puzzle(102),
statue(104), onionsan event(100), carrybird(99), shyren(101), dogroom
rarependant(103), Mad Dummy trigger(115), napstablookdate(120),
temvillage(128), glowshroom/darkness puzzles(127,129).
room_water7_older(304) did not ack goto — likely dead/unused.
