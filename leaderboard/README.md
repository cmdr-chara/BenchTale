# Leaderboard

One JSON file per submitted run, matching `schema.json`. A run is valid only if produced by `eval/run_eval.py` against the patched game; the `steps.jsonl` transcript must be kept in `runs/` for audit.

Fields to fill before submitting: `model` (exact model + version), `mode`, `milestones_hit`, `score`, `steps`, `wall_clock_s`, `notes`.
