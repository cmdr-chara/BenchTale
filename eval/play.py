"""Interactive driver: send keys, wait N frames, dump state + screenshot.

Usage:
  python eval/play.py --keys z --frames 10          # hold z for 2f, release, wait 10
  python eval/play.py --keys right,down --frames 30 # hold right+down for all frames
  python eval/play.py --keys z --hold 5 --frames 10 # hold for 5 frames then release
  python eval/play.py --wait 30                     # just let the game run 30f
Prints the latest state and saves the current frame to runs/frame.png.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "env"))

from undertale_bench import UndertaleEnv  # noqa: E402
from undertale_bench.keys import NO_KEYS  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", default="")
    ap.add_argument("--hold", type=int, default=2)
    ap.add_argument("--frames", type=int, default=10)
    ap.add_argument("--wait", type=int, default=0)
    args = ap.parse_args()

    env = UndertaleEnv(mode="real-time", obs_screen=True)
    env._attach()

    held = {k: True for k in args.keys.split(",") if k}
    if held:
        env.ipc.send_keys(held)
        env.ipc.wait_frames(args.hold)
        env.ipc.send_keys(dict(NO_KEYS))
    if args.frames:
        st = env.ipc.wait_frames(args.frames)
    elif args.wait:
        st = env.ipc.wait_frames(args.wait)
    else:
        st = env.ipc.wait_state()

    out = Path("runs"); out.mkdir(exist_ok=True)
    screen = env._obs(st)["screen"]
    if screen is not None:
        import PIL.Image
        PIL.Image.fromarray(screen).save(out / "frame.png")

    slim = {k: v for k, v in st.items() if k != "flags_csv"}
    print(slim)


if __name__ == "__main__":
    main()
