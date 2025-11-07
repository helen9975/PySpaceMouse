import pyspacemouse
import time
import sys

RIGHT_PATH = "/dev/hidraw4"
LEFT_PATH  = "/dev/hidraw9"

def make_button_any_cb(tag):
    def _cb(state, buttons):
        print(f"[{tag}] Button change: {buttons}")
    return _cb

def make_dof_cb(tag):
    def _cb(state):
        print(f"[{tag}] DOF: {state}")
    return _cb

def make_button_arr_cbs(tag):
    def b0(state, buttons, pressed):  print(f"[{tag}] Button 0 -> {pressed}")
    def b1(state, buttons, pressed):  print(f"[{tag}] Button 1 -> {pressed}")
    def b01(state, buttons, pressed): print(f"[{tag}] Buttons 0+1 -> {pressed}")
    return [
        pyspacemouse.ButtonCallback(0, b0),
        pyspacemouse.ButtonCallback([1], b1),
        pyspacemouse.ButtonCallback([0, 1], b01),
    ]

def open_by_path(tag, path):
    dev = pyspacemouse.open(
        dof_callback=make_dof_cb(tag),
        button_callback=make_button_any_cb(tag),
        button_callback_arr=make_button_arr_cbs(tag),
        set_nonblocking_loop=True,
        path=path,        # <- bind to this exact hidraw device
    )
    if dev is None:
        print(f"Failed to open SpaceMouse [{tag}] at {path}", file=sys.stderr)
    else:
        print(f"Opened SpaceMouse [{tag}] at {path}")
    return dev

def main():
    dev_right = open_by_path("RIGHT", RIGHT_PATH)
    dev_left  = open_by_path("LEFT",  LEFT_PATH)

    if not (dev_right or dev_left):
        return  # neither opened

    try:
        while True:
            if dev_right: dev_right.read()
            if dev_left:  dev_left.read()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        if dev_right: dev_right.close()
        if dev_left:  dev_left.close()

if __name__ == "__main__":
    main()
