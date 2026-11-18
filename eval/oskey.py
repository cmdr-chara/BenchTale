"""Real OS-level key injection for UNDERTALE (registers on keyboard_check, unlike
keyboard_key_press sim which only reaches keyboard_check_direct on this runtime)."""
import time, ctypes
import win32gui, win32process
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
VK = {'z':0x5A,'x':0x58,'c':0x43,'enter':0x0D,'up':0x26,'down':0x28,'left':0x25,'right':0x27,'f4':0x73,'esc':0x1B}
def game_hwnd():
    hs=[]
    def cb(h,res):
        t=win32gui.GetWindowText(h)
        if 'UNDERTALE' in t.upper() and win32gui.IsWindowVisible(h): res.append(h)
    win32gui.EnumWindows(cb,hs)
    return hs[0] if hs else 0
def focus_game():
    h=game_hwnd()
    if not h: return False
    fg=user32.GetForegroundWindow(); cur=kernel32.GetCurrentThreadId()
    fgt=win32process.GetWindowThreadProcessId(fg)[0]; tgt=win32process.GetWindowThreadProcessId(h)[0]
    user32.AttachThreadInput(cur,fgt,True); user32.AttachThreadInput(cur,tgt,True)
    user32.BringWindowToTop(h); ok=user32.SetForegroundWindow(h)
    user32.AttachThreadInput(cur,tgt,False); user32.AttachThreadInput(cur,fgt,False)
    return ok!=0
def down(k): user32.keybd_event(VK[k],0,0,0)
def up(k):   user32.keybd_event(VK[k],0,2,0)
def tap(k,hold=0.08): down(k); time.sleep(hold); up(k)
class Hold:
    def __init__(self,*ks): self.ks=ks
    def __enter__(self):
        for k in self.ks: down(k)
        return self
    def __exit__(self,*a):
        for k in self.ks: up(k)
