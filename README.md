# undertale-bench

A benchmark where an AI model must finish **Undertale** — or at least the **Ruins** — by playing the real game.

Unlike screenshot-and-keyboard harnesses, undertale-bench patches `data.win` with [UndertaleModTool CLI](https://github.com/UnderminersTeam/UndertaleModTool) to inject a bridge *inside* the game. Each frame the game writes structured state (room, position, HP, LV, EXP, plot, flags, dialogue text, battle info) to disk and reads the desired key state back — turning Undertale into a Gymnasium environment.

## Modes

- **real-time** — the game runs normally; the agent must act fast enough (hard mode, includes bullet-hell dodging).
- **lite** — between agent decisions the Windows process is suspended (`NtSuspendProcess`), so a slow VLM gets a true pause. The score records which mode was used.

## Layout

```
patches/    UndertaleModTool .csx script that injects obj_bench_bridge into data.win
env/        Python Gymnasium environment (screenshot + state obs, key-state actions)
eval/       Agent runner (scripted + VLM), milestone scoring for every region, step recording
leaderboard/ Result schema and submitted runs
scripts/    fetch_utmt.ps1 / patch_datawin.ps1 helpers
docs/       DESIGN.md — architecture, metrics, related work
```

## Setup (Windows)

1. Own a legal copy of Undertale (Steam). Nothing game-related is redistributed by this repo — the patch is applied to *your* `data.win`.
2. Install Python 3.11+ and `pip install -r requirements.txt`.
3. `scripts\fetch_utmt.ps1` — downloads UndertaleModTool CLI into `tools/`.
4. `scripts\patch_datawin.ps1 -GameDir "C:\...\Steam\steamapps\common\Undertale"` — produces `data_bench.win` next to `data.win` (original untouched).
5. Launch: `UNDERTALE.exe -game data_bench.win` (files land in `%LOCALAPPDATA%\UNDERTALE\bench_*`).

   Status: verified end-to-end on the real game — intro, naming, overworld movement, item pickup, choicer dialogues, a real random encounter (FIGHT timed hit + MERCY spare), and the Ruins exit door -> `room_tundra1`.

   Steam's `steam_api.dll` forces a restart through the Steam client when launched directly. Two options: rename `steam_api.dll` in the game dir (Undertale runs fine without it — this is what the eval scripts assume), or leave it and add `-game data_bench.win` in Steam → Properties → Launch Options and press Play (warns if your account is in use elsewhere).
6. `python eval/run_eval.py --agent scripted` for a smoke run. `python eval/play.py` is an interactive driver; `eval/playbook.py` (tap/hold/goto/shot helpers) is what real sessions use to drive the game. `ipc.goto_room("room_ruins7")` teleports for testing — scripted fights still need real progression.

## Scoring

`run_eval` scores every calibrated milestone across the whole game — Ruins (10+10), Snowdin (13+22), Waterfall (13+29), Hotland+CORE (13+25), New Home→endings (8+27), main-path plus optional/exploration ids — and classifies the route (neutral / pacifist / true pacifist / genocide) from flag state. Results land in `runs/<name>/result.json` with per-region breakdown and first-hit frames.

## VLM agent

`--agent vlm` drives the game with a vision-language model: each step sends the screenshot + pruned game state to a chat-completions endpoint and injects the returned keys. Every decision must carry a psychological `why` (human-style inner monologue), which is logged into `steps.jsonl`.

```
UBENCH_PROVIDER=openai   UBENCH_API_BASE=https://api.openai.com/v1
UBENCH_API_KEY=...       UBENCH_MODEL=gpt-4o
python eval/run_eval.py --agent vlm --mode lite --steps 2000 --out runs/gpt4o_run
```

`UBENCH_PROVIDER=anthropic` + `UBENCH_API_BASE=https://api.anthropic.com` works the same.

`--obs-mode` picks the difficulty tier, recorded in `result.json` for leaderboard comparability: `full` (screenshot + engine state, the default), `vision` (pixels only — VideoGameBench tier), `state` (textual state dump only — BALROG-text tier).

### First recorded run

`deepseek-v4.1-flash` (effort=low, `--obs-mode state`, 400 steps, ~1.7h): **score 0.0** — failed at the name-entry screen. It navigated the letter grid correctly and typed a name, but never toggled the confirm highlight, burning all 400 steps in `room_intromenu`. UI-navigation failures count as benchmark results, not bugs — the transcript is in `runs/ds41_run4/steps.jsonl`.

## Legal

Undertale is © Toby Fox. This repo contains only patch/instrumentation code; it neither ships nor downloads game assets. The patched `data_bench.win` never leaves your machine.
