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
