import evdev
import uinput
import sys

# Supported gamepad names (extendable)
SUPPORTED_CONTROLLERS = {
    "PLAYSTATION": "ps3",
    "PS3": "ps3",
    "XBOX": "xbox",
    "GENERIC": "generic"
}

# Button maps for known controllers (can be customized)
BUTTON_MAPS = {
    "ps3": {
        304: uinput.KEY_ENTER,      # X
        305: uinput.KEY_ESC,        # Circle
        307: uinput.KEY_BACKSPACE,  # Square
        308: uinput.KEY_SPACE,      # Triangle
        544: uinput.KEY_UP,         # D-pad Up
        545: uinput.KEY_DOWN,       # D-pad Down
        546: uinput.KEY_LEFT,       # D-pad Left
        547: uinput.KEY_RIGHT       # D-pad Right
    },
    "xbox": {
        304: uinput.KEY_ENTER,      # A
        305: uinput.KEY_ESC,        # B
        307: uinput.KEY_BACKSPACE,  # X
        308: uinput.KEY_SPACE,      # Y
        544: uinput.KEY_UP,         # D-pad Up
        545: uinput.KEY_DOWN,       # D-pad Down
        546: uinput.KEY_LEFT,       # D-pad Left
        547: uinput.KEY_RIGHT       # D-pad Right
    },
    "generic": {
        304: uinput.KEY_ENTER,      # Button 0
        305: uinput.KEY_ESC,        # Button 1
        307: uinput.KEY_BACKSPACE,  # Button 2
        308: uinput.KEY_SPACE,      # Button 3
        544: uinput.KEY_UP,
        545: uinput.KEY_DOWN,
        546: uinput.KEY_LEFT,
        547: uinput.KEY_RIGHT
    }
}

def find_gamepad():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    gamepads = []

    for device in devices:
        if device.capabilities().get(evdev.ecodes.EV_KEY):
            gamepads.append(device)

    if not gamepads:
        print("No input devices with keys found.")
        sys.exit(1)

    # If multiple gamepads, show list and let user pick
    print("Available Gamepads:")
    for i, dev in enumerate(gamepads):
        print(f"[{i}] {dev.name} - {dev.path}")

    try:
        choice = int(input("Select device number (default 0): ") or "0")
        return gamepads[choice]
    except (IndexError, ValueError):
        print("Invalid selection.")
        sys.exit(1)

def detect_controller_type(device):
    name = device.name.upper()
    for keyword, controller_type in SUPPORTED_CONTROLLERS.items():
        if keyword in name:
            return controller_type
    return "generic"

# Main
device = find_gamepad()
controller_type = detect_controller_type(device)

print(f"Using device: {device.path} ({device.name}) as type '{controller_type}'")

BTN_MAP = BUTTON_MAPS.get(controller_type, BUTTON_MAPS["generic"])

# Setup uinput
events = set(BTN_MAP.values())
ui = uinput.Device(events)

# Read loop
device.grab()
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key = BTN_MAP.get(event.code)
        if key is not None:
            ui.emit(key, event.value)
