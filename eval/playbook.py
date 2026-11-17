"""Interactive play helper: send keys, watch state, grab frames."""
import sys, time, json
sys.path.insert(0, 'C:/Users/Administrator/repos/undertale-bench/env')
from undertale_bench.ipc import BridgeIPC
from undertale_bench.window import find_window, grab
from pathlib import Path

ipc = BridgeIPC()
SHOT = Path('C:/Users/Administrator/repos/undertale-bench/runs')
SHOT.mkdir(exist_ok=True)

def state():
    return ipc.read_state() or {}

def wait_state(timeout=10):
    return ipc.wait_state(timeout)

def new_state(timeout=10):
    return ipc.wait_new_state(timeout)

def tap(keys, hold=5, settle=4):
    if isinstance(keys, str):
        keys = [keys]
    seq = ipc.send_keys({k: True for k in keys})
    ipc.wait_ack(seq)
    for _ in range(hold):
        ipc.wait_new_state()
    seq = ipc.send_keys({k: False for k in keys})
    ipc.wait_ack(seq)
    for _ in range(settle):
        ipc.wait_new_state()
    return new_state()

def hold(keys, frames):
    if isinstance(keys, str):
        keys = [keys]
    seq = ipc.send_keys({k: True for k in keys})
    ipc.wait_ack(seq)
    st = None
    for _ in range(frames):
        st = ipc.wait_new_state()
    return st

def release_all():
    seq = ipc.send_keys({})
    ipc.wait_ack(seq)

def shot(name):
    w = find_window()
    if not w:
        print('no window'); return
    img = grab(w[1])
    p = SHOT / f'{name}.png'
    from PIL import Image
    Image.fromarray(img).save(p)
    print('saved', p)

_ev_seq = 0

def events():
    """Drain new bridge events since last call; prints and returns them."""
    global _ev_seq
    _ev_seq, evs = ipc.events_since(_ev_seq)
    for e in evs:
        print(e['frame'], e['type'], e['detail'])
    return evs

def brief(st=None):
    st = st or state()
    keep = {k: st.get(k) for k in ('frame','room','room_name','px','py','hp','plot','in_battle','dialogue','msg','battlegroup')}
    if keep.get('msg'):
        keep['msg'] = keep['msg'][:80]
    print(json.dumps(keep))
    return st
