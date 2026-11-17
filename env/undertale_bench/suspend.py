"""Suspend/resume the game process for `lite` mode (Windows).

Freezing the whole process is a true pause: physics, timers and the bridge all
stop together, so a slow-thinking VLM gets fair turns even in bullet-hell
segments. Requires nothing game-side.
"""
from __future__ import annotations

import ctypes

_ntdll = ctypes.windll.ntdll if hasattr(ctypes, "windll") else None
_PROCESS_ALL_ACCESS = 0x1F0FFF


def _open(pid: int) -> int:
    kernel32 = ctypes.windll.kernel32
    h = kernel32.OpenProcess(_PROCESS_ALL_ACCESS, False, pid)
    if not h:
        raise OSError(f"OpenProcess({pid}) failed")
    return h


def suspend(pid: int) -> None:
    h = _open(pid)
    try:
        status = _ntdll.NtSuspendProcess(h)
        if status != 0:
            raise OSError(f"NtSuspendProcess failed: {status:#x}")
    finally:
        ctypes.windll.kernel32.CloseHandle(h)


def resume(pid: int) -> None:
    h = _open(pid)
    try:
        status = _ntdll.NtResumeProcess(h)
        if status != 0:
            raise OSError(f"NtResumeProcess failed: {status:#x}")
    finally:
        ctypes.windll.kernel32.CloseHandle(h)
