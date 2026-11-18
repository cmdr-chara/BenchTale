"""File-based IPC with the in-game bridge.

GameMaker file functions are sandboxed to %LOCALAPPDATA%\\UNDERTALE\\, which
doubles as the IPC directory:

  bench_state.json  game -> env   (rewritten every Step)
  bench_cmd.txt     env  -> game  (flat text: "seq N" then "key 0|1" per line)
  bench_ack.txt     game -> env   ("<seq> <frame>" once applied)
  bench_events.txt  game -> env   (append-only "<eseq> <frame> <type> <detail>")
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
        self.cmd_path = d / "bench_cmd.txt"
        self.ack_path = d / "bench_ack.txt"
        self.events_path = d / "bench_events.txt"
        self.timeout = timeout
        self._seq = self._recover_seq()
        self._last_state_frame = -1

    def _recover_seq(self) -> int:
        """bench_seq persists in-game across processes — continue from last ack."""
        try:
            return int(self.ack_path.read_text().split()[0])
        except Exception:
            return 0

    def clear(self) -> None:
        for p in (self.state_path, self.cmd_path, self.ack_path, self.events_path):
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    # ----------------------------------------------------------- env -> game
    def send_keys(self, keys: dict[str, bool], goto: str | None = None) -> int:
        self._seq += 1
        from .keys import KEY_NAMES
        lines = [f"seq {self._seq}"]
        if goto is not None:
            lines.append(f"goto {goto}")
        lines += [f"{k} {1 if keys.get(k) else 0}" for k in KEY_NAMES]
        tmp = self.cmd_path.with_suffix(".tmp")
        body = "\n".join(lines) + "\n"
        for _ in range(200):
            try:
                tmp.write_text(body)
                tmp.replace(self.cmd_path)
                break
            except (PermissionError, FileNotFoundError):
                time.sleep(0.01)
        else:
            raise TimeoutError("bench_cmd.txt locked by game")
        return self._seq

    def goto_room(self, room_name: str) -> int:
        """Debug/testing helper: jump the game to a room (bench-only command)."""
        seq = self.send_keys({}, goto=room_name)
        return self.wait_ack(seq)

    def send_cmd(self, *cmd_lines: str) -> int:
        """Send raw calibration commands (e.g. "heal 1", "item 11", "flag 45 5").

        Each use is logged as an `admin` event in bench_events.txt, so any run
        that used them is marked as assisted — they exist for calibration,
        not for scored benchmark runs.
        """
        self._seq += 1
        from .keys import KEY_NAMES
        lines = [f"seq {self._seq}", *cmd_lines]
        lines += [f"{k} 0" for k in KEY_NAMES]
        tmp = self.cmd_path.with_suffix(".tmp")
        body = "\n".join(lines) + "\n"
        for _ in range(200):
            try:
                tmp.write_text(body)
                tmp.replace(self.cmd_path)
                break
            except (PermissionError, FileNotFoundError):
                time.sleep(0.01)
        else:
            raise TimeoutError("bench_cmd.txt locked by game")
        return self.wait_ack(self._seq)

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

    # ------------------------------------------------------------ events
    def events_since(self, last_eseq: int) -> tuple[int, list[dict]]:
        """Return (new_last_eseq, events) for every line with eseq > last_eseq.

        Line format: "<eseq> <frame> <type> <detail...>".
        """
        out: list[dict] = []
        try:
            text = self.events_path.read_text()
        except FileNotFoundError:
            return last_eseq, out
        for line in text.splitlines():
            parts = line.strip().split(" ", 3)
            if len(parts) < 3:
                continue
            try:
                eseq, frame = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            if eseq <= last_eseq:
                continue
            out.append({"eseq": eseq, "frame": frame, "type": parts[2],
                        "detail": parts[3] if len(parts) > 3 else ""})
            last_eseq = max(last_eseq, eseq)
        return last_eseq, out
