# Design — undertale-bench

## Goal

Measure whether a foundation model can *play* a real PC game end-to-end: Undertale, starting with the Ruins. The agent sees the same pixels a player sees, plus structured state exported from inside the engine, and acts by holding keys. No in-game cheats: the injected bridge only observes and supplies input.

## Why not screenshots + OS input only

Undertale is a GameMaker: Studio (1.4) game — `data.win` is fully rewritable. Patching it in gives us:

- **Structured observation**: room name/id, `obj_mainchara` x/y, HP/LV/EXP/gold, `global.plot`, `global.flag[]`, battle fields (`battlegroup`, enemy HP, `mercymod`), dialogue text (`global.msg[]`). A VLM does not have to OCR its own HUD, and milestones can be scored on engine facts instead of pixel heuristics.
- **Deterministic input**: `keyboard_key_press`/`keyboard_key_release` driven by the bridge — no window-focus races, works headless-ish.
- **Frame-accurate stepping**: every state record carries a frame counter, so `step(actions, n_frames)` is verifiable.

## IPC design

GameMaker file functions are sandboxed to `%LOCALAPPDATA%\UNDERTALE\`, which doubles as the IPC directory:

| File | Direction | Contents |
|---|---|---|
| `bench_state.json` | game → env | one JSON object per step: frame, room, globals, flags, battle, msg |
| `bench_cmd.json` | env → game | `{"seq": n, "keys": {"left": true, "z": false, ...}}` — desired held-key set |
| `bench_ack.txt` | game → env | last applied `seq` + frame it was applied at |

The bridge (`obj_bench_bridge`, persistent, injected into the first room) runs in the Step event: poll command file, apply key diffs, write state. File-polling overhead is a few ms per frame — acceptable at 30 fps.

## Lite mode (process suspend)

A VLM with multi-second inference can never dodge bullet-hell patterns in real time. Rather than slowing `room_speed` (which would also stall the bridge and change gameplay physics), `lite` mode calls `NtSuspendProcess` between decisions: the whole game freezes deterministically, the agent thinks, the env writes the next key-state, then resumes. Physics and logic are untouched; runs are labeled `mode: lite` on the leaderboard.

## Observations and actions

- `obs["screen"]`: H×W×3 RGB capture of the game window (mss).
- `obs["state"]`: parsed `bench_state.json`.
- Action space (v0): a held-key map over `{up,down,left,right,z,x,c,enter,shift,ctrl}` plus `hold_frames`. Discrete `press(key)` helpers are derived on top.

## Scoring

Progress = fraction of Ruins milestones reached (engine-verified: room ids, `global.plot` thresholds, `global.flag` bits). Milestone constants live in `eval/milestones.py` and are explicitly marked `calibrated`/`needs_calibration` — early runs should dump raw `plot`/`flag` values at known story beats to pin the exact numbers down.

Metrics per run: furthest milestone, wall-clock and frame counts per milestone, deaths/resets, total LLM tokens, mode.

## Related work / positioning

VideoGameBench (raw pixel input on DOS/GB titles), BALROG (NetHack/Crafter RL envs), lmgame-Bench (Gym API on arcade titles), TextQuests (Infocom). undertale-bench's differentiators: a modern narrative RPG where progress is flag/plot-driven rather than score-driven, hybrid text+bullet-hell action, and an engine-injected bridge that makes the evaluation reproducible and cheatable-by-nobody (state comes from the game, not OCR).

## Repo boundaries

No game assets, no `data.win`, no extracted strings in the repo. The `.csx` patch adds code; it does not read or exfiltrate game content beyond the documented state fields.
