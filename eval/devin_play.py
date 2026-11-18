"""Interactive driver for the first real run — Devin is the agent.

Each `python -c` call drives a slice of gameplay; this module keeps a
persistent run log in runs/devin_first/ identical in spirit to
run_eval output: steps.jsonl (state + events per decision) and,
at the end, result.json.
"""
import sys, json, time
from pathlib import Path
sys.path.insert(0, 'C:/Users/Administrator/repos/undertale-bench/env')
sys.path.insert(0, 'C:/Users/Administrator/repos/undertale-bench/eval')
from undertale_bench.ipc import BridgeIPC
from undertale_bench.window import find_window, grab
import os
from milestones import reached as _reached_ruins, reached_optional as _reached_ruins_opt

def _load_registries():
    regs = [_reached_ruins, _reached_ruins_opt]
    for mod_name in ('snowdin_milestones', 'waterfall_milestones', 'hotland_milestones', 'newhome_milestones'):
        try:
            mod = __import__(mod_name)
            regs.append(mod.reached)
            if hasattr(mod, 'reached_optional'):
                regs.append(mod.reached_optional)
        except ImportError:
            pass
    return regs

_REGS = _load_registries()

def reached(state):
    out = []
    for r in _REGS:
        out.extend(r(state))
    return out

RUN = Path(os.environ.get('BENCH_RUN_DIR', 'C:/Users/Administrator/repos/undertale-bench/runs/devin_first'))
RUN.mkdir(parents=True, exist_ok=True)
LOG = RUN / 'steps.jsonl'
SEQF = RUN / '.eseq'
HITF = RUN / '.hits'

ipc = BridgeIPC()
T0 = time.time()

def _load(name, default):
    try: return json.loads((RUN / name).read_text())
    except Exception: return default

def _eseq():
    try: return int(SEQF.read_text())
    except Exception: return 0

def st():
    return ipc.wait_state()

def shot(name):
    w = find_window()
    if not w: return None
    from PIL import Image
    p = RUN / f'{name}.png'
    Image.fromarray(grab(w[1])).save(p)
    return p

WHY = {'why': None}  # current justification, set via why() and read by _log

def why(text):
    """Attach a justification to every action logged until cleared (why(None))."""
    WHY['why'] = text

def _log(action, state):
    eseq = _eseq()
    eseq, evs = ipc.events_since(eseq)
    SEQF.write_text(str(eseq))
    hits = set(_load('.hits', []))
    new = [m for m in reached(state) if m not in hits]
    for m in new:
        hits.add(m)
        print(f"*** milestone {m} @frame {state.get('frame')}")
    (RUN / '.hits').write_text(json.dumps(sorted(hits)))
    LOG.open('a').write(json.dumps({
        'step_t': round(time.time() - T0, 2), 'action': {k: (sorted(v) if isinstance(v, (set, frozenset)) else v) for k, v in action.items()},
        'why': WHY['why'],
        'frame': state.get('frame'), 'room': state.get('room_name'),
        'px': state.get('px'), 'py': state.get('py'),
        'plot': state.get('plot'), 'hp': state.get('hp'),
        'in_battle': state.get('in_battle'), 'events': evs,
        'msg': (state.get('msg') or '')[:160],
        'milestones': new,
    }) + '\n')
    return new

def tap(keys, hold=4, settle=8, why=None):
    if isinstance(keys, str): keys = [keys]
    if why is not None: WHY['why'] = why
    s = ipc.send_keys({k: True for k in keys}); ipc.wait_ack(s)
    ipc.wait_frames(hold)
    s = ipc.send_keys({k: False for k in keys}); ipc.wait_ack(s)
    ipc.wait_frames(settle)
    state = st()
    _log({'tap': keys, 'hold': hold}, state)
    return state

def hold(keys, frames, tag=None, why=None):
    if isinstance(keys, str): keys = [keys]
    if why is not None: WHY['why'] = why
    s = ipc.send_keys({k: True for k in keys}); ipc.wait_ack(s)
    state = ipc.wait_frames(frames)
    _log({'hold': keys, 'frames': frames, 'tag': tag}, state)
    return state

def release():
    s = ipc.send_keys({}); ipc.wait_ack(s)
    return st()

def walk(direction, frames, tag=None, why=None):
    """Hold a direction, stop early if room changes."""
    if why is not None: WHY['why'] = why
    r0 = st().get('room_name')
    s = ipc.send_keys({direction: True}); ipc.wait_ack(s)
    last = st()
    for _ in range(frames):
        last = ipc.wait_new_state()
        if last.get('room_name') != r0:
            break
    s = ipc.send_keys({}); ipc.wait_ack(s)
    _log({'walk': direction, 'frames': frames, 'tag': tag}, last)
    return last

def brief():
    s_ = st()
    keep = {k: s_.get(k) for k in ('frame','room_name','px','py','hp','plot','in_battle','dialogue','choicer','battlegroup')}
    keep['msg'] = (s_.get('msg') or '')[:100]
    print(json.dumps(keep))
    return s_

def finish():
    from collections import Counter
    hits = set(_load('.hits', []))
    steps = LOG.read_text().splitlines() if LOG.exists() else []
    deaths = 0; counts = Counter(); unjust = 0
    for line in steps:
        rec = json.loads(line)
        if not rec.get('why'): unjust += 1
        for e in rec.get('events', []):
            counts[e['type']] += 1
            if e['type'] == 'death': deaths += 1
    result = {
        'agent': 'devin-interactive', 'mode': 'real-time',
        'wall_clock_s': round(time.time() - T0, 2),
        'milestones_hit': sorted(hits),
        'deaths': deaths, 'event_counts': dict(counts),
        'steps_unjustified': unjust,
        'score': len(hits) / len(MILESTONE_IDS),
    }
    (RUN / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
