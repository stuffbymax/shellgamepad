'''
created BY marinP/stuffbymax
description: a tool that allows user to use gamepad as keyboard
License MIT
'''
import evdev
import uinput
import sys

def find_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if evdev.ecodes.EV_KEY in device.capabilities():
            return device
    print("No controller found.")
    sys.exit(1)

try:
    device = find_controller()
    print(f"Using device: {device.path} ({device.name})")
except Exception as e:
    print(f"Error finding controller: {e}")
    sys.exit(1)

events = [
    uinput.KEY_ENTER, uinput.KEY_ESC, uinput.KEY_BACKSPACE, uinput.KEY_SPACE,
    uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT
]

try:
    ui = uinput.Device(events)
except Exception as e:
    print(f"Error creating uinput device: {e}")
    sys.exit(1)

BTN_MAP_COMMON = {
    304: uinput.KEY_ENTER,
    305: uinput.KEY_ESC,
    307: uinput.KEY_BACKSPACE,
    308: uinput.KEY_SPACE,
    544: uinput.KEY_UP,
    545: uinput.KEY_DOWN,
    546: uinput.KEY_LEFT,
    547: uinput.KEY_RIGHT
}

try:
    device.grab()
    print("Controller grabbed. Press Ctrl+C to stop.")
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key = BTN_MAP_COMMON.get(event.code)
            if key is not None:
                ui.emit(key, event.value)
        elif event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_HAT0Y:
                if event.value == -1:
                    ui.emit(uinput.KEY_UP, 1); ui.emit(uinput.KEY_UP, 0)
                elif event.value == 1:
                    ui.emit(uinput.KEY_DOWN, 1); ui.emit(uinput.KEY_DOWN, 0)
            elif event.code == evdev.ecodes.ABS_HAT0X:
                if event.value == -1:
                    ui.emit(uinput.KEY_LEFT, 1); ui.emit(uinput.KEY_LEFT, 0)
                elif event.value == 1:
                    ui.emit(uinput.KEY_RIGHT, 1); ui.emit(uinput.KEY_RIGHT, 0)
except KeyboardInterrupt:
    pass
finally:
    device.ungrab()
