"""Run an agent against the patched game and score Ruins milestones.

Usage:  python eval/run_eval.py --agent scripted --mode lite --steps 500 --out runs/smoke
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "env"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from undertale_bench import UndertaleEnv  # noqa: E402
from agents import make_agent  # noqa: E402
from milestones import reached, MILESTONE_IDS  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="scripted")
    ap.add_argument("--mode", default="lite", choices=["lite", "real-time"])
    ap.add_argument("--steps", type=int, default=500)
    ap.add_argument("--out", default="runs/latest")
    ap.add_argument("--no-screen", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "steps.jsonl"

    env = UndertaleEnv(mode=args.mode, obs_screen=not args.no_screen)
    agent = make_agent(args.agent)

    hit: set[str] = set()
    first_hit_frame: dict[str, int] = {}
    first_hit_s: dict[str, float] = {}
    ev_seq = 0
    deaths = 0
    event_counts: dict[str, int] = {}
    obs, _ = env.reset()
    t0 = time.time()

    with log_path.open("w") as log:
        for i in range(args.steps):
            action = agent.act(obs)
            obs, _r, term, _trunc, info = env.step(action)
            st = info["state"]

            for m in reached(st):
                if m not in hit:
                    hit.add(m)
                    first_hit_frame[m] = st.get("frame", -1)
                    first_hit_s[m] = round(time.time() - t0, 2)
                    print(f"[{st.get('frame')}] milestone: {m}")

            ev_seq, evs = env.ipc.events_since(ev_seq)
            for e in evs:
                event_counts[e["type"]] = event_counts.get(e["type"], 0) + 1
                if e["type"] == "death":
                    deaths += 1

            log.write(json.dumps({
                "step": i, "action": action,
                "frame": st.get("frame"), "room": st.get("room_name"),
                "plot": st.get("plot"), "hp": st.get("hp"),
                "in_battle": st.get("in_battle"), "msg": (st.get("msg") or "")[:200],
                "events": evs,
            }) + "\n")

    env.close()
    result = {
        "agent": agent.name, "mode": args.mode, "steps": args.steps,
        "wall_clock_s": round(time.time() - t0, 2),
        "milestones_hit": sorted(hit),
        "milestone_frames": first_hit_frame,
        "milestone_seconds": first_hit_s,
        "deaths": deaths,
        "event_counts": event_counts,
        "score": len(hit) / len(MILESTONE_IDS),
    }
    (out / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
