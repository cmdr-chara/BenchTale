"""File-based IPC with the in-game bridge.

GameMaker file functions are sandboxed to %LOCALAPPDATA%\\UNDERTALE\\, which
doubles as the IPC directory:

  bench_state.json  game -> env   (rewritten every Step)
  bench_cmd.json    env  -> game  (desired held-key set + seq)
  bench_ack.txt     game -> env   ("<seq> <frame>" once applied)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path


def sandbox_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ["LOCALAPPDATA"]) / "UNDERTALE"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "UNDERTALE"


class BridgeIPC:
    def __init__(self, timeout: float = 30.0):
        d = sandbox_dir()
        self.state_path = d / "bench_state.json"
        self.cmd_path = d / "bench_cmd.json"
        self.ack_path = d / "bench_ack.txt"
        self.timeout = timeout
        self._seq = 0
        self._last_state_frame = -1

    def clear(self) -> None:
        for p in (self.state_path, self.cmd_path, self.ack_path):
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    # ----------------------------------------------------------- env -> game
    def send_keys(self, keys: dict[str, bool]) -> int:
        self._seq += 1
        payload = {"seq": self._seq, "keys": keys}
        tmp = self.cmd_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload))
        tmp.replace(self.cmd_path)
        return self._seq

    def wait_ack(self, seq: int, timeout: float | None = None) -> int:
        """Block until the bridge reports it applied `seq`; returns the game frame."""
        deadline = time.monotonic() + (timeout or self.timeout)
        while time.monotonic() < deadline:
            try:
                s, f = self.ack_path.read_text().split()
                if int(s) >= seq:
                    return int(f)
            except (FileNotFoundError, ValueError):
                pass
            time.sleep(0.005)
        raise TimeoutError(f"bridge did not ack cmd seq {seq}")

    # ----------------------------------------------------------- game -> env
    def read_state(self) -> dict | None:
        try:
            return json.loads(self.state_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def wait_state(self, timeout: float | None = None) -> dict:
        deadline = time.monotonic() + (timeout or self.timeout)
        while time.monotonic() < deadline:
            st = self.read_state()
            if st is not None:
                return st
            time.sleep(0.01)
        raise TimeoutError(f"no state at {self.state_path} — patched game not running?")

    def wait_new_state(self, timeout: float | None = None) -> dict:
        """Wait until frame number advances past the last seen one."""
        deadline = time.monotonic() + (timeout or self.timeout)
        while time.monotonic() < deadline:
            st = self.read_state()
            if st is not None and st.get("frame", -1) > self._last_state_frame:
                self._last_state_frame = st["frame"]
                return st
            time.sleep(0.005)
        raise TimeoutError("game frame counter not advancing")

    def wait_frames(self, n: int, timeout: float | None = None) -> dict:
        """Let the game run for at least `n` frames; returns the latest state."""
        first = self.wait_new_state(timeout)
        target = first["frame"] + n - 1
        deadline = time.monotonic() + (timeout or self.timeout * n)
        st = first
        while st["frame"] < target and time.monotonic() < deadline:
            st = self.wait_new_state(timeout)
        return st
