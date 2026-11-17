"""Gymnasium environment wrapping the patched Undertale process.

Observation: {"screen": HxWx3 uint8, "state": dict from the in-game bridge}
Action:      {"keys": {name: bool}, "hold_frames": int}

Modes:
  real-time — game runs freely; step() waits `hold_frames` game frames.
  lite      — process suspended between steps so a slow agent can think.
"""
from __future__ import annotations

import time

import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # allow use without gymnasium installed
    class _Fallback:
        class Env: ...
        spaces = None
    gym = _Fallback()
    spaces = None

from .ipc import BridgeIPC
from .keys import KEY_NAMES, NO_KEYS
from . import suspend as _suspend
from . import window as _window


class UndertaleEnv(gym.Env):
    metadata = {"name": "undertale-bench", "fps": 30}

    def __init__(self, mode: str = "lite", obs_screen: bool = True):
        assert mode in ("lite", "real-time")
        self.mode = mode
        self.obs_screen = obs_screen
        self.ipc = BridgeIPC()
        self._hwnd = None
        self._pid = None
        self._paused = False

        if spaces is not None:
            self.action_space = spaces.Dict({
                "keys": spaces.Dict({k: spaces.Discrete(2) for k in KEY_NAMES}),
                "hold_frames": spaces.Discrete(600),
            })
            self.observation_space = spaces.Dict({
                "screen": spaces.Box(0, 255, (480, 640, 3), np.uint8),
                "state": spaces.Dict({}),
            })

    # ------------------------------------------------------------- plumbing
    def _attach(self) -> None:
        found = _window.find_window()
        if found is None:
            raise RuntimeError("UNDERTALE window not found — start the patched game first")
        self._hwnd, self._rect = found
        self._pid = _window.window_pid(self._hwnd)

    def pause(self) -> None:
        if self.mode == "lite" and self._pid and not self._paused:
            _suspend.suspend(self._pid)
            self._paused = True

    def resume(self) -> None:
        if self._pid and self._paused:
            _suspend.resume(self._pid)
            self._paused = False

    # --------------------------------------------------------------- gym API
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self._attach()
        self.ipc.clear()
        self.resume()
        state = self.ipc.wait_state()
        self.pause()
        return self._obs(state), {"state": state}

    def step(self, action):
        keys = dict(NO_KEYS)
        keys.update({k: bool(v) for k, v in action.get("keys", {}).items() if k in keys})
        hold = int(action.get("hold_frames", 1))

        seq = self.ipc.send_keys(keys)
        self.resume()
        self.ipc.wait_ack(seq)
        state = self.ipc.wait_frames(hold)
        self.pause()

        obs = self._obs(state)
        reward = 0.0          # scoring is milestone-based, see eval/milestones.py
        terminated = False    # decided by the evaluator, not the env
        return obs, reward, terminated, False, {"state": state}

    def press(self, key: str, frames: int = 3) -> dict:
        """Convenience: tap a single key, release, wait `frames` game frames."""
        obs, *_ = self.step({"keys": {key: True}, "hold_frames": 2})
        obs, *_ = self.step({"keys": NO_KEYS, "hold_frames": frames})
        return obs

    # ----------------------------------------------------------------- misc
    def _obs(self, state: dict):
        screen = None
        if self.obs_screen and self._hwnd:
            was_paused = self._paused
            self.resume()
            time.sleep(0.05)  # let the renderer present one frame
            screen = _window.grab(self._rect)
            if was_paused:
                self.pause()
        return {"screen": screen, "state": state}

    def close(self):
        self.resume()
        self.ipc.send_keys(dict(NO_KEYS))
