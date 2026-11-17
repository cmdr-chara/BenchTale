"""Agent interface + a scripted smoke-test agent.

A real agent implements `act(obs) -> action dict`. `obs["state"]` holds the
structured game state; `obs["screen"]` is the RGB frame (or None).
"""
from __future__ import annotations


class Agent:
    name = "base"

    def act(self, obs: dict) -> dict:
        raise NotImplementedError


class ScriptedConfirmAgent(Agent):
    """Mash confirm/walk — smoke test for IPC, not a real player."""

    name = "scripted-confirm"

    def __init__(self):
        self._i = 0

    def act(self, obs: dict) -> dict:
        self._i += 1
        pattern = self._i % 6
        if pattern in (0, 1):
            return {"keys": {"z": True}, "hold_frames": 3}
        if pattern == 2:
            return {"keys": {"right": True}, "hold_frames": 20}
        if pattern == 3:
            return {"keys": {"down": True}, "hold_frames": 20}
        if pattern == 4:
            return {"keys": {"enter": True}, "hold_frames": 3}
        return {"keys": {}, "hold_frames": 10}


AGENTS = {"scripted": ScriptedConfirmAgent}


def make_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise SystemExit(f"unknown agent {name!r}; available: {sorted(AGENTS)}")
    return AGENTS[name]()
