"""Key names shared with the GML bridge. Order/name must match patches/bench_bridge.csx."""

KEY_NAMES = ["left", "right", "up", "down", "z", "x", "c", "enter", "shift", "ctrl"]

# Windows virtual-key codes (for reference / OS-level fallback input)
VK = {
    "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
    "z": 0x5A, "x": 0x58, "c": 0x43,
    "enter": 0x0D, "shift": 0x10, "ctrl": 0x11,
}

NO_KEYS = {k: False for k in KEY_NAMES}
