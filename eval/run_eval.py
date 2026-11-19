"""Run an agent against the patched game and score all region milestones.

Usage:  python eval/run_eval.py --agent vlm --mode lite --steps 2000 --out runs/gpt4o_ruins
        python eval/run_eval.py --agent scripted --mode lite --steps 500 --out runs/smoke
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "env"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from undertale_bench import UndertaleEnv  # noqa: E402
from agents import make_agent  # noqa: E402

# (module, score-bucket) — main-path ids go to 'main', optional ids to 'optional'
REGIONS = [
    ("milestones", "ruins"),
    ("snowdin_milestones", "snowdin"),
    ("waterfall_milestones", "waterfall"),
    ("hotland_milestones", "hotland"),
    ("endgame_milestones", "endgame"),
]


def _load_registries():
    """Return {region: {main: [fn], optional: [fn], main_ids: int, opt_ids: int}}."""
    regs = {}
    for mod_name, region in REGIONS:
        try:
            mod = importlib.import_module(mod_name)
        except ImportError:
            continue
        ms = getattr(mod, "MILESTONES", None) or getattr(mod, f"{region.upper()}_MILESTONES", [])
        opt = getattr(mod, "OPTIONAL_MILESTONES",
                      getattr(mod, f"{region.upper()}_OPTIONAL", []))
        regs[region] = {
            "main": mod.reached,
            "optional": getattr(mod, "reached_optional", lambda s: []),
            "main_ids": len(ms),
            "opt_ids": len(opt),
            "classify": getattr(mod, "classify_route", None),
        }
    return regs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="scripted")
    ap.add_argument("--mode", default="lite", choices=["lite", "real-time"])
    ap.add_argument("--steps", type=int, default=500)
    ap.add_argument("--out", default="runs/latest")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "steps.jsonl"

    env = UndertaleEnv(mode=args.mode, obs_screen=True)
    agent = make_agent(args.agent)
    regs = _load_registries()

    hit: dict[str, set[str]] = {r: {"main": set(), "opt": set()} for r in regs}
    first_hit: dict[str, dict] = {}
    ev_seq = 0
    deaths = 0
    event_counts: dict[str, int] = {}
    route = "early"
    obs, _ = env.reset()
    t0 = time.time()

    with log_path.open("w") as log:
        for i in range(args.steps):
            action = agent.act(obs)
            obs, _r, term, _trunc, info = env.step(action)
            st = info["state"]

            new_ms = []
            for region, reg in regs.items():
                for m in reg["main"](st):
                    if m not in hit[region]["main"]:
                        hit[region]["main"].add(m)
                        first_hit[f"{region}:{m}"] = {
                            "frame": st.get("frame", -1),
                            "s": round(time.time() - t0, 2),
                            "kind": "main"}
                        new_ms.append(m)
                        print(f"[{st.get('frame')}] {region}: {m}")
                for m in reg["optional"](st):
                    if m not in hit[region]["opt"]:
                        hit[region]["opt"].add(m)
                        first_hit[f"{region}:{m}"] = {
                            "frame": st.get("frame", -1),
                            "s": round(time.time() - t0, 2),
                            "kind": "optional"}
                        new_ms.append(m)
                        print(f"[{st.get('frame')}] {region} (opt): {m}")
                if reg["classify"]:
                    route = reg["classify"](st)

            ev_seq, evs = env.ipc.events_since(ev_seq)
            for e in evs:
                event_counts[e["type"]] = event_counts.get(e["type"], 0) + 1
                if e["type"] == "death":
                    deaths += 1

            log.write(json.dumps({
                "step": i, "action": action,
                "why": action.get("why"),
                "frame": st.get("frame"), "room": st.get("room_name"),
                "plot": st.get("plot"), "hp": st.get("hp"),
                "in_battle": st.get("in_battle"), "msg": (st.get("msg") or "")[:200],
                "events": evs, "milestones": new_ms,
            }) + "\n")

    env.close()

    per_region = {}
    main_hits = main_total = opt_hits = opt_total = 0
    for region, reg in regs.items():
        h = hit[region]
        main_hits += len(h["main"]); main_total += reg["main_ids"]
        opt_hits += len(h["opt"]); opt_total += reg["opt_ids"]
        per_region[region] = {
            "main": sorted(h["main"]), "optional": sorted(h["opt"]),
            "main_score": len(h["main"]) / reg["main_ids"] if reg["main_ids"] else None,
            "opt_score": len(h["opt"]) / reg["opt_ids"] if reg["opt_ids"] else None,
        }

    result = {
        "agent": agent.name, "mode": args.mode, "steps": args.steps,
        "wall_clock_s": round(time.time() - t0, 2),
        "route": route,
        "milestones": per_region,
        "milestone_first_hit": first_hit,
        "deaths": deaths,
        "event_counts": event_counts,
        "score": main_hits / main_total if main_total else 0.0,
        "optional_score": opt_hits / opt_total if opt_total else 0.0,
    }
    (out / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
