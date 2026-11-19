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

## Live bullet export (blt) + dialogue edges
- state JSON now has `blt`: [[x,y],...] of up to 24 live projectiles, matched by
  object name prefix `blt_*` or a fixed obj_* list (undynespear, sans bones,
  mettaton, spider, etc). Verified live in water9 chase — dodging off blt
  took 0 damage across the spear phase.
- **writer/dialogue needs press EDGES**: holding z does nothing once latched;
  alternate `z 0` / `z 1` taps. Held-key re-press only re-fires when the key
  is unheld, so a held z produces a single edge total.
- **bridge now spawns in every early room** (room_start..room_ruins1): the boot
  path varies when save data exists (introstory is skipped -> bridge never
  spawned and the intro froze on "Hi."). Self-dedup keeps the first spawn.

## water9 chase (obj_undyneencounter2, verified live end-to-end)
cn0 spawn uspeargen -> x>460 speeds spears -> x>510 locks interact, Undyne
walks on (cn3-23 scripted ~30s) -> cn24 waits for player in x(200-220)/(780-790)
-> cn25-33 Monster Kid runs over, dialogue (needs z edges) -> cn38:
plot=110, interact=0, flag[15/16/17]=0, sl1/sl2 solids removed, music resumes.
Flag[17] is RESET by cn23 — it's "scene in progress", not "scene done"; use
plot>=110 as the done predicate.

## Waterfall tail (live sweep, plot 115->117)
- trashzone entry auto-sets plot=115; friendlyhub plays the Monster Kid
  "my house is up here" scene (needs z edges) -> plot=117.
- Verified loading: undyneyard(117), undynehouse(118), hapstablook(121),
  farm(122), prebird(123), shop(124), dock(125), temvillage(128),
  water15-21(126-133). bird room(99) east exit is walled - needs the
  carrybird ride, goto around it.
- intr=1 lingering in several waterfall rooms post-scene does not block goto.
- undynefinal 136-138: boss rooms (not yet entered).

## Input fix (repatch): movement chain + release latch
- obj_time latches try_* off keyboard_check, which NEVER observes
  keyboard_key_press sim on this runtime; pin try_up/down/left/right to
  keyboard_check_direct each frame from the bridge (verified live: movement
  returned immediately).
- release must be unconditional: `if (keyboard_check(vk)) release` never ran
  because check never sees sim -> latched keys held forever.
- New admin `warp x y`: moves obj_mainchara directly (verified live).

## Undyne boss (bg47, room_water_undynefinal -> room_battle), live
- Room expects global.plot==121 at entry (obj_undynetrigger_boss2 Create);
  door spawn is bottom-left markerA (20,640); wide solid at y=624 -> route
  east to x~150 corridor, then north. Trigger_boss2 fires ~y=540: monologue
  -> room_battle, battlegroup=47.
- Green mode: spears tracked via blt (blt_whitespear/blt_bluespear/obj_rotspear
  all match). Soul sits ~(320,240); block = press the direction of the
  NEAREST incoming spear relative to center. Single-direction hold blocked
  a full wave phase at LV1 losing only 5hp (loop latency ~0.3s is the leak).
- Fight math at LV1: Undyne 1500hp; landed hits do ~6-15hp each and require
  the attack-bar z on myfight==1; a legit kill needs dozens of clean phases.
  Green-mode blocking is the workable mechanic; attack-bar timing is the
  bottleneck for a real LV1 clear.

## Hotland live walk (post-Undyne)
- After the Undyne kill: plot=122, kills=1, LV1->8, flag[350]=flag[352]=1;
  undynefinal2/3 are exit corridors (east walk), Papyrus phonecall room
  trigger at x~683 in undynefinal3, then room_fire1 (Hotland).
- fire1: rock formation blocks straight east; slip north of solidwide(160,84)
  via y~95-103 lane, then east to doorA(500,120) -> fire2 -> prelab.
- fire_dock is a DETOUR room (riverman + dogboat): its north door returns
  to fire2. The lab is room_fire_lab1 (141), reached via goto; the prelab
  north door_t(215,-15) is blocked from the south side (solidexwide lip).
- lab1: long dark hall ~1100px wide, walk east y~140; alphystrigger1 ~x663
  -> lights + Alphys/Mettaton intro -> bg48 Mettaton quiz show battle.
- QUIZ (bg48): questions use obj_answernodule (2x2 grid, arrow+z); wrong
  answers zap hp but Mettaton cannot kill (floored at hp1). Observed through
  the Alphys-help monologue.
- GOTCHA: freeme inside a battle-side script DESTROYS the writers the battle
  controller waits on -> permanent stall (intr latch cleared but controller
  never resumes). Same class as the water8 view starvation. Rule: never
  freeme inside room_battle — kill the process instead.

## Input model — REAL fix (verified live, fire3)
`keyboard_key_press` sim registers ONLY on `keyboard_check_direct` on this runtime;
`keyboard_check`/`keyboard_check_pressed` never see it (dbg_zcheck=0 vs zdirect=1 held).
Everything that "advanced" before via sim-z was writer auto-advance.
**Fix: real OS input.** `eval/oskey.py`: keybd_event via user32 + AttachThreadInput
focus workaround (SetForegroundWindow works after AttachThreadInput+BringWindowToTop).
Real keys register on BOTH check and direct -> menu edges, dialogue, movement all work.
Game must be foreground (windowed is fine). First real z tap cleared the stuck
Alphys status notification that survived ~200 sim taps.

## Lab2 gate
lab2's intro conveyor (obj_sideconveyorl 120,160 pushes west) + unfinished quiz scene
lock control; z-sim couldn't advance it. Mettaton quiz (bg48) stalls at hp=1 in our
hands — writer dependency issue; skipping via goto. Quiz is NOT plot-gating (122 persists).

## Elevator hub (verified live)
room_fire_elevator (214) interior: obj_elevatorpanel at (140,80) — interact needs
FACE-UP + z. Flow: "Click..." -> "Please select a location." -> floor grid
(text choicer: Left/Right Floor N + Cancel; cursor defaults to Cancel).
Ride = select floor, then WALK SOUTH out to the destination spoke.
Spokes: r1<->l1<->r2 (r2 has obj_heatsflamesman NPC at 240,120; his line ends
"...n go home."). door_s (160,115)/(162,75) are the spoke entrances; door_t in
elevator_l1 (220,230) exits SOUTH into prelab's north door -> elevator hub is a
BACKTRACK shortcut, not forward progress.
prelab exits: doorB west (fire2 side), doorC east -> lab1, doorA south (220,232),
door_t north (elevator_l1), savepoint at (200,120).

## Savepoint interact
Star needs a z PRESS while overlapping (not just touch). Choicer -> z = writes
file9 anchored to that room. file9 now = room_fire_savepoint1 @ plot 122.
Savepoints also auto-set plot floor: save event bumped plot 54->137?? (verify:
plot jumped to 137 on save in savepoint1 — the save writes current globals).

## Hotland encounters
obj_encount_fire1 arms random battles (bg51 = 3-monster group) in fire5's upper
zone. LV1 dodge dies to them (~2 deaths); heal-assisted fight + flee worked.
kills counter increments on real kills (seen 1->2).

## Mettaton EX (bg80) — verified live, played
Trigger: room_fire_core_metttest, obj_mettboss_event at (150,780) fires when
mainchara.y<840. Chain (decompiled): con 0..7 scrolls view to y620, reads
undertale.ini Mettaton.BossMet (already>=1 -> skip variant), then the 28-line
monologue writer -> "OH NO!" scrollaway -> mettafly -> battler bg80.
- The monologue is ~10+ writer pages: keep tapping z; each page needs a press.
  dlg field may read None while text renders (screenshot-verify instead).
- murder=1 (scr_murderlv>=12) swaps in the Mettaton NEO variant path
  (con 30-52: bg94 instead of bg80) and sets global.plot=199 after.
- Post-fight: mettdestroyed_event -> plot 199.
- Fight mechanics: FIGHT attack bar works; attack phases ~13hp lost at LV1
  (heal-assisted for calibration). Yellow soul shoots with z during attacks.
- myfight=1 = player turn; menu cursor persists on FIGHT between turns —
  single `right` may drop (~50% taps), so ACT nav needs verify-and-retry.
- Win is ratings-based (not kill): monsterhp exports 9999,50,50.
- core_final room: obj_alphysfollow_event (Alphys walks with you after con 7,
  sets flag[430]) -> finalelevatorpanel -> New Home.

## New Home / Asgore's house — route spine (verified live)
- Route: castle_elevatorout -> castle_precastle (grey street, door_s_musfade at
  ~1996,136 -> lastruins_corridor at its EAST end) -> castle_hook -> castle_front.
- castle_front is a DEAD END: doorA (160,160)->asghouse1, doorBmusicfade
  (160,520)->castle_hook (back). Forward path is THROUGH the house.
- asghouse1 (foyer): center staircase splits lower/upper; upper landing
  reachable via up-left diagonal around ~(49,59)->(36,59), then east along
  y~120-123 lane. `obj_doorXmusicfade` (144,109) -> **room_basement1_final**
  guarded by the chain.
- Lock/keys: `obj_latchkey` sets flag[452]=1 (kitchen key, room_kitchen_final
  at (122,126)) and flag[453]=1 (hallway key, room_asghouse3 at (540,117)).
  `obj_lock_and_key` (226,104 in asghouse1) sets flag[454]=1 when both flags
  are 1 -> chain sprite dies, interact fires con->3. Key pickup = touch
  radius ~14px facing the object.
- Kitchen: reached via asghouse2 north door (door_ruins13 54,220 spawn side /
  the top-left stair door). obj_npc_room (146,188) story monster.
- asghouse3 (hallway): east-west corridor; doorC (151,124)->room_asgoreroom,
  doorA (570,123)->room_asgoreroom as well (two doors one room), doorD
  (0,183)->asghouse1 west floor (lands 25,164). obj_earlystorybattle (465,142)
  fires storybattle. obj_mirrorreflection (120,87) — non-interactive z.
- room_asrielroom_final (kids' room): entered via asghouse3 doorC area
  (warp (226,110) triggered it / north door), 5 readables, exits doorD
  south -> asghouse3 (151,175).
- GOTCHA: doorXmusicfade's basement trigger is the STAIRS mouth — standing
  (144,119) capped; the verified entry was `goto` (couldn't find the exact
  walk-in lane; the door obj anchor 144,109 sits in a solid band y~105-119).
- Basement chain: basement1_final (doorX west back, doorA east 480,140,
  story_engager 360,120) -> basement2_final -> basement3_final (doorA north
  180,0) -> basement4_final (story_engager 220,160, doorA east 300,180)
  -> room_lastruins_corridor. Each room interleaves storybattle scenes.
- lastruins_corridor: ~2048px east-west, 9 obj_story_engager at y=160 x
  180-1700 (each = one storybattle segment). East end: obj_elevatordoor
  (1980,112) sealed/unresponsive + door_s_musfade (1996,136) -> back to
  castle_precastle. REAL forward exit: doorA (1900,220) south ->
  room_sanscorridor (spawn 150,172).
- sanscorridor (Judgement Hall): obj_lastsans_trigger (820,120) at x~800
  fires the full judgement scene (long monologue, ~45 z-taps) -> plot=201.
  doorA north (1240,90) -> room_castle_finalshoehorn.
- finalshoehorn: savepoint (460,110), doorAmusicfade (680,520), doorB
  (180,520), doorXmusicfade (400,90).
- Route flags: flag[452]/[453] = the two keys; flag[454]=1 = chain unlocked.
  flag[7] must be 0 for the musicfade doors (checked in their Alarm_2).

## Post-judgement chain (verified live, kill-route)
- finalshoehorn: savepoint (460,110). South-east doorAmusicfade (680,520) ->
  room_castle_coffins1 (its two doors both return to shoehorn markers;
  coffins1 is a side wing). doorXmusicfade (400,90) -> throneroom.
- throneroom: savepoint (160,110), toriel/asgore thrones, obj_asgoremeet_event
  (140,500). Triggering it latches control and runs the full "Howdy" scene;
  ~40 z advances -> plot=206, battlegroup=100, Asgore exits north.
  GOTCHA: the north doorA (120,95) does NOT transition by walking into it
  after the scene (gate while scene resolves?) - warp into it fired the
  room change to room_castle_prebarrier.
- prebarrier: east-west corridor; asgore_prebarrier_event arms a second
  dialogue at x~480 -> plot=207 then 208. savepoint (520,142). East exit
  doorAmusicfade (610,138) needs deep overlap (walk at y~141 capped at 643;
  warp 615,138 fired it).
- room_castle_barrier: obj_barrierevent + obj_finalbarrier armed; the walk-up
  scene runs Asgore's last monologue -> room_battle bg100.
- Asgore fight: monsterhp ~3500. MERCY button is SHATTERED (his intro).
  Menu stays up while soul_x==40 (parked soul, NOT -400; menu must be
  detected via the visible UI, not soul sentinel). ATK boost via `set at <v>`
  barely scales (heavily DF-capped ~45-90/hit); fight is long at any LV.
  At ~588 hp he kneels: the choice UI = obj_asgore_lastcutscene +
  obj_fakeheart — the soul moves FREELY with arrows; the choice fires on
  OVERLAP of the button box then z. Confirm: land the heart on FIGHT/MERCY
  box then z (heart speed ~45game-px/s; overshoot is easy).
- Choosing FIGHT kills him -> scripted dust scene -> room_castle_exit.
  kills counter did NOT increment (Asgore's scripted kill isn't a normal
  kill) — check flag side-effects for the ending split instead.
- Admin: new `set <global> <v>` (variable_global_set) + `get <global>`
  (guarded by variable_global_exists — a missing name threw and killed the
  cmd reader on the previous build).
