"""File-based IPC with the in-game bridge.

GameMaker file functions are sandboxed to %LOCALAPPDATA%\\UNDERTALE\\, which
doubles as the IPC directory:

  bench_state.json  game -> env   (rewritten every Step)
  bench_cmd.txt     env  -> game  (flat text: "seq N" then "key 0|1" per line)
  bench_ack.txt     game -> env   ("<seq> <frame>" once applied)
  bench_events.txt  game -> env   (append-only "<eseq> <frame> <type> <detail>")
"""
from __future__ import annotations

import ctypes
import json
import os
import time
from pathlib import Path


def sandbox_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ["LOCALAPPDATA"]) / "UNDERTALE"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "UNDERTALE"


_OS_VK = {"z": 0x5A, "x": 0x58, "c": 0x43, "enter": 0x0D, "up": 0x26,
          "down": 0x28, "left": 0x25, "right": 0x27, "f4": 0x73,
          "shift": 0x10, "ctrl": 0x11}


def _game_foreground() -> bool:
    try:
        user32 = ctypes.windll.user32
        buf = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(user32.GetForegroundWindow(), buf, 256)
        return "UNDERTALE" in buf.value.upper()
    except Exception:
        return False


def _os_tap(key: str, hold: float = 0.05) -> None:
    """Real OS-level key event — registers on keyboard_check/pressed (the
    buffered channel every menu reads), which the bridge's keyboard_key_press
    sim never reaches on this runtime."""
    vk = _OS_VK.get(key)
    if vk is None:
        return
    try:
        user32 = ctypes.windll.user32
        user32.keybd_event(vk, 0, 0, 0)
        time.sleep(hold)
        user32.keybd_event(vk, 0, 2, 0)
    except Exception:
        pass


_WNDENUM = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)


def _game_hwnd() -> int:
    user32 = ctypes.windll.user32
    found: list[int] = []

    def cb(h, _lp):
        buf = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(h, buf, 256)
        if "UNDERTALE" in buf.value.upper() and user32.IsWindowVisible(h):
            found.append(h)
        return True

    user32.EnumWindows(_WNDENUM(cb), 0)
    return found[0] if found else 0


def _focus_game() -> bool:
    """Steal foreground for the UNDERTALE window (AttachThreadInput trick)."""
    try:
        user32 = ctypes.windll.user32
        k32 = ctypes.windll.kernel32
        h = _game_hwnd()
        if not h:
            return False
        fg = user32.GetForegroundWindow()
        cur = k32.GetCurrentThreadId()
        pid = ctypes.c_ulong()
        fgt = user32.GetWindowThreadProcessId(fg, ctypes.byref(pid)) if fg else 0
        tgt = user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
        if fgt:
            user32.AttachThreadInput(cur, fgt, True)
        user32.AttachThreadInput(cur, tgt, True)
        user32.BringWindowToTop(h)
        ok = user32.SetForegroundWindow(h)
        user32.AttachThreadInput(cur, tgt, False)
        if fgt:
            user32.AttachThreadInput(cur, fgt, False)
        time.sleep(0.25)
        return bool(ok) or _game_foreground()
    except Exception:
        return False


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
        self._down_keys: set[str] = set()

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
        # Menus/naming/choicer/dialogue read keyboard_check_pressed, which
        # ignores the bridge's simulated presses. Fire one real OS tap per
        # newly-pressed key so every menu callsite works like human input.
        new_presses = {k for k, v in keys.items() if v} - self._down_keys
        self._down_keys = {k for k, v in keys.items() if v}
        if new_presses:
            if not _game_foreground():
                _focus_game()
            if _game_foreground():
                for k in sorted(new_presses):
                    _os_tap(k)
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
