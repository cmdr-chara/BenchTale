"""Locate the UNDERTALE window, find its PID, and capture frames."""
from __future__ import annotations

import numpy as np

WINDOW_TITLE = "UNDERTALE"


def find_window() -> tuple[int, dict] | None:
    """Return (hwnd, rect{left,top,width,height}) of the Undertale window."""
    import win32gui

    found: list[int] = []

    def cb(hwnd: int, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == WINDOW_TITLE:
            found.append(hwnd)

    win32gui.EnumWindows(cb, None)
    if not found:
        return None
    hwnd = found[0]
    l, t, r, b = win32gui.GetClientRect(hwnd)
    cl, ct = win32gui.ClientToScreen(hwnd, (l, t))
    return hwnd, {"left": cl, "top": ct, "width": r - l, "height": b - t}


def window_pid(hwnd: int) -> int:
    import win32process

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def grab(rect: dict) -> np.ndarray:
    """Screenshot the client area -> HxWx3 uint8."""
    import mss

    with mss.mss() as sct:
        shot = sct.grab({"left": rect["left"], "top": rect["top"],
                         "width": rect["width"], "height": rect["height"]})
        return np.asarray(shot)[:, :, :3]
