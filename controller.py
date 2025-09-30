import evdev, uinput, sys

def find_ps3_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "PLAYSTATION" in device.name.upper() or "PS3" in device.name.upper():
            return device
    print("PS3 controller not found.")
    sys.exit(1)

device = find_ps3_controller()
print(f"Using device: {device.path} ({device.name})")

events = (uinput.KEY_ENTER, uinput.KEY_ESC, uinput.KEY_SPACE, uinput.KEY_BACKSPACE,
          uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT)
ui = uinput.Device(events)

BTN_MAP = {
    304: uinput.KEY_ENTER,  # X
    305: uinput.KEY_ESC,    # Circle
    307: uinput.KEY_BACKSPACE, # Square
    308: uinput.KEY_SPACE,      # Triangle
    544: uinput.KEY_UP,         # D-pad Up
    545: uinput.KEY_DOWN,       # D-pad Down
    546: uinput.KEY_LEFT,       # D-pad Left
    547: uinput.KEY_RIGHT       # D-pad Right
}

device.grab()
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key = BTN_MAP.get(event.code)
        if key is not None:
            ui.emit(key, event.value)
