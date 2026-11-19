"""Agent interface + scripted smoke-test agent + VLM (model-API) agent.

A real agent implements `act(obs) -> action dict`. `obs["state"]` holds the
structured game state; `obs["screen"]` is the RGB frame (or None).

Action contract returned to the env:
    {"keys": {"z": true, "right": true}, "hold_frames": 15, "why": "..."}

The optional "why" is logged into steps.jsonl — per benchmark rules it must be
written like a human player's inner monologue (feelings, doubts, second
guessing), not a technical explanation.

VLM agent configuration (env vars):
    UBENCH_PROVIDER  openai | anthropic            (default openai)
    UBENCH_API_BASE  base URL                      (default https://api.openai.com/v1)
    UBENCH_API_KEY   API key
    UBENCH_MODEL     model id                      (default gpt-4o / claude-sonnet-4-5)
    UBENCH_MEMORY    recent turns kept in context  (default 8)
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import urllib.request
import urllib.error

VALID_KEYS = ("left", "right", "up", "down", "z", "x", "c", "enter", "shift", "ctrl", "f4")


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


# --------------------------------------------------------------------- VLM

_SYSTEM = """You are playing Undertale — the real GameMaker game — through a keyboard-only
interface. Each turn you receive the current screen and a JSON dump of the
game's internal state (room, position, hp, plot progress, flags, dialogue
text, battle info).

Reply with ONLY a JSON object, no prose outside it:
{"keys": {"<key>": true, ...}, "hold_frames": <int 1-60>, "why": "<string>"}

Valid keys: left, right, up, down, z, x, c, enter, shift, ctrl, f4.
  z/enter = confirm, interact, advance dialogue. x = cancel / menu. c = menu.
  arrows = overworld movement; in battle they steer the soul.
hold_frames = how many game frames (30fps) the keys stay held. Movement needs
roughly 30+ frames per tile; menu taps 2-4.

"why" is REQUIRED and must be written as a human player's inner monologue —
emotions, hesitation, overthinking, regrets ("okay that spiked me, i almost
died, careful now") — not technical notes. It is judged as part of the run.

Play only from what you see and what the state tells you: no walkthrough
knowledge, no wiki spoilers. Explore, read dialogue, figure it out.
"""


def _png_b64(screen, max_w=320) -> str | None:
    if screen is None:
        return None
    from PIL import Image
    img = Image.fromarray(screen)
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def _prune_state(st: dict) -> dict:
    keep = {}
    for k in ("room_name", "px", "py", "hp", "maxhp", "lv", "exp", "gold",
              "plot", "in_battle", "battlegroup", "dialogue", "choicer",
              "choice", "interact", "msg", "kills", "soul_x", "soul_y",
              "monsterhp", "at", "df"):
        v = st.get(k)
        if v is not None and v != "" and v != "None":
            keep[k] = v
    flags = st.get("flags_csv")
    if flags:
        nz = {i: v for i, v in enumerate(str(flags).split(",")) if v not in ("0", "")}
        if nz:
            keep["flags"] = nz
    items = st.get("items_csv")
    if items:
        keep["items"] = items
    return keep


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _sanitize_action(raw: dict | None) -> dict:
    if not isinstance(raw, dict):
        return {"keys": {}, "hold_frames": 10, "why": "(unparseable reply)"}
    keys = {k: True for k, v in (raw.get("keys") or {}).items()
            if k in VALID_KEYS and v}
    hold = raw.get("hold_frames", 10)
    try:
        hold = max(1, min(60, int(hold)))
    except (TypeError, ValueError):
        hold = 10
    return {"keys": keys, "hold_frames": hold,
            "why": str(raw.get("why") or "(no justification)")[:500]}


class VLMAgent(Agent):
    """Sends obs (screen + pruned state) to a chat-completions model and
    injects the returned keys. Works with OpenAI-compatible and Anthropic APIs."""

    def __init__(self):
        self.provider = os.environ.get("UBENCH_PROVIDER", "openai").lower()
        self.api_base = os.environ.get(
            "UBENCH_API_BASE",
            "https://api.openai.com/v1" if self.provider == "openai"
            else "https://api.anthropic.com").rstrip("/")
        self.api_key = os.environ.get("UBENCH_API_KEY", "")
        if not self.api_key:
            raise SystemExit("VLMAgent needs UBENCH_API_KEY")
        self.model = os.environ.get(
            "UBENCH_MODEL",
            "gpt-4o" if self.provider == "openai" else "claude-sonnet-4-5-20250929")
        self.memory: list[dict] = []
        self.memory_n = int(os.environ.get("UBENCH_MEMORY", "8"))
        self.name = f"vlm-{self.model}"

    # -------------------------------------------------------------- http
    def _post(self, url: str, headers: dict, payload: dict, timeout=120) -> dict:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read()[:500]
            raise RuntimeError(f"api {e.code}: {body}") from e

    def _call(self, user_content: list[dict]) -> str:
        if self.provider == "anthropic":
            resp = self._post(
                f"{self.api_base}/v1/messages",
                {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
                {"model": self.model, "max_tokens": 400,
                 "system": _SYSTEM,
                 "messages": [{"role": "user", "content": user_content}]})
            return "".join(b.get("text", "") for b in resp.get("content", []))
        # openai-compatible
        resp = self._post(
            f"{self.api_base}/chat/completions",
            {"Authorization": f"Bearer {self.api_key}"},
            {"model": self.model, "max_tokens": 400,
             "messages": [{"role": "system", "content": _SYSTEM},
                          {"role": "user", "content": user_content}]})
        return resp["choices"][0]["message"]["content"]

    # -------------------------------------------------------------- agent
    def act(self, obs: dict) -> dict:
        content: list[dict] = []
        b64 = _png_b64(obs.get("screen"))
        if b64 and self.provider == "openai":
            content.append({"type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64}"}})
        elif b64:
            content.append({"type": "image",
                            "source": {"type": "base64", "media_type": "image/png",
                                       "data": b64}})
        prompt = {"state": _prune_state(obs.get("state") or {}),
                  "recent": self.memory[-self.memory_n:]}
        content.append({"type": "text", "text": json.dumps(prompt)})

        try:
            raw = _extract_json(self._call(content))
        except Exception as e:  # API outage must not crash a scored run
            action = {"keys": {}, "hold_frames": 15,
                      "why": f"(api error: {e!r:.120} — freezing a beat)"}
            self.memory.append(action)
            return action

        action = _sanitize_action(raw)
        self.memory.append({"keys": sorted(action["keys"]),
                            "hold_frames": action["hold_frames"],
                            "why": action["why"]})
        return action


# ---------------------------------------------------------- Command Code CLI

class CmdCLiAgent(Agent):
    """Uses the Command Code `cmd` CLI (headless `cmd -p`) as the decision
    engine — e.g. deepseek-v4.1-flash through a Command Code subscription.
    Text-only input, so run with --obs-mode state.

    Env: COMMAND_CODE_API_KEY (user_... key), UBENCH_CC_MODEL (default
    deepseek/deepseek-v4.1-flash), UBENCH_MEMORY."""

    def __init__(self):
        if not os.environ.get("COMMAND_CODE_API_KEY"):
            raise SystemExit("CmdCLiAgent needs COMMAND_CODE_API_KEY")
        self.model = os.environ.get("UBENCH_CC_MODEL", "deepseek/deepseek-v4.1-flash")
        self.memory: list[dict] = []
        self.memory_n = int(os.environ.get("UBENCH_MEMORY", "8"))
        self.name = f"cmdcli-{self.model.split('/')[-1]}"
        import shutil
        self._node = shutil.which("node") or "node"
        # npm shim is `cmd.cmd`; calling it bare collides with cmd.exe —
        # invoke the real node entry point instead.
        pkg = os.environ.get(
            "UBENCH_CC_ENTRY",
            "C:/hostedtoolcache/node/24.22.2/x64/node_modules/"
            "command-code/dist/index.mjs")
        self._entry = pkg

    def act(self, obs: dict) -> dict:
        import subprocess
        prompt = {
            "state": _prune_state(obs.get("state") or {}),
            "recent": self.memory[-self.memory_n:],
        }
        q = (_SYSTEM + "\n\nCURRENT TURN\n" + json.dumps(prompt) +
             "\n\nRespond with ONLY the JSON action object.")
        argv = [self._node, self._entry, "-p", q, "-m", self.model,
                "--max-turns", "2", "--skip-onboarding", "--no-auto-update"]
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=180)
            text = r.stdout.strip()
            if r.returncode != 0:
                raise RuntimeError(f"cmd rc={r.returncode}: {r.stderr[:200]}")
        except Exception as e:
            action = {"keys": {}, "hold_frames": 15,
                      "why": f"(cli error: {e!r:.120} — holding still)"}
            self.memory.append(action)
            return action
        action = _sanitize_action(_extract_json(text))
        self.memory.append({"keys": sorted(action["keys"]),
                            "hold_frames": action["hold_frames"],
                            "why": action["why"]})
        return action


AGENTS = {"scripted": ScriptedConfirmAgent, "vlm": VLMAgent, "cmd": CmdCLiAgent}


def make_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise SystemExit(f"unknown agent {name!r}; available: {sorted(AGENTS)}")
    return AGENTS[name]()
