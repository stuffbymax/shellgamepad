'''
created BY marinP/stuffbymax
description: Gamepad to keyboard mapper - supports PS3, PS4, PS5, Xbox 360, Xbox One, Xbox Series X/S
License: MIT
version: 0.0.4
'''

import evdev
import uinput
import sys
import time

KNOWN_CONTROLLERS = [
    "sony", "playstation", "dualshock", "dualsense", "sixaxis",
    "ps3", "ps4", "ps5", "wireless controller",
    "xbox", "microsoft", "x-box", "xinput", "360 pad",
    "xbox 360", "xbox one", "xbox series",
    "gamepad", "joystick",
]

EXCLUDE_NAMES = [
    "touchpad", "motion", "accelerometer", "gyro",
    "sensor", "rumble", "battery",
]

BTN_MAP_PS3 = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    544: uinput.KEY_UP, 545: uinput.KEY_DOWN, 546: uinput.KEY_LEFT, 547: uinput.KEY_RIGHT,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1, 312: uinput.KEY_F2, 313: uinput.KEY_F3,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7, 318: uinput.KEY_F8,
}

BTN_MAP_PS4 = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1, 312: uinput.KEY_F2, 313: uinput.KEY_F3,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7,
    318: uinput.KEY_F8, 319: uinput.KEY_F9,
}

BTN_MAP_PS5 = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1, 312: uinput.KEY_F2, 313: uinput.KEY_F3,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7,
    318: uinput.KEY_F8, 319: uinput.KEY_F9, 320: uinput.KEY_F10,
}

BTN_MAP_XBOX360 = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7, 318: uinput.KEY_F8,
}

BTN_MAP_XBOXONE = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7,
    318: uinput.KEY_F8, 706: uinput.KEY_F9,
}

BTN_MAP_XBOXSERIES = {
    304: uinput.KEY_ENTER, 305: uinput.KEY_ESC, 307: uinput.KEY_SPACE, 308: uinput.KEY_BACKSPACE,
    310: uinput.KEY_TAB, 311: uinput.KEY_F1,
    314: uinput.KEY_F4, 315: uinput.KEY_F5, 316: uinput.KEY_F6, 317: uinput.KEY_F7,
    318: uinput.KEY_F8, 706: uinput.KEY_F9, 167: uinput.KEY_F10,
}

def find_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        name_lower = device.name.lower()
        if any(k in name_lower for k in KNOWN_CONTROLLERS):
            if any(ex in name_lower for ex in EXCLUDE_NAMES):
                print(f"[SGBU] Skipping sub-device: {device.name}")
                continue
            caps = device.capabilities()
            if evdev.ecodes.EV_KEY in caps:
                return device
    for device in devices:
        name_lower = device.name.lower()
        if any(ex in name_lower for ex in EXCLUDE_NAMES):
            continue
        caps = device.capabilities()
        if evdev.ecodes.EV_KEY in caps and evdev.ecodes.EV_ABS in caps:
            keys = caps[evdev.ecodes.EV_KEY]
            if len(keys) >= 8:
                return device
    return None

def detect_controller_type(device):
    name_lower = device.name.lower()
    if "dualsense" in name_lower or "ps5" in name_lower:
        print("[SGBU] Detected: PS5 DualSense")
        return "ps5", BTN_MAP_PS5
    elif "dualshock 4" in name_lower or "ps4" in name_lower or "wireless controller" in name_lower:
        print("[SGBU] Detected: PS4 DualShock 4")
        return "ps4", BTN_MAP_PS4
    elif "ps3" in name_lower or "dualshock 3" in name_lower or "sixaxis" in name_lower:
        print("[SGBU] Detected: PS3 DualShock 3 / Sixaxis")
        return "ps3", BTN_MAP_PS3
    elif "series" in name_lower or "xbox series" in name_lower:
        print("[SGBU] Detected: Xbox Series X/S")
        return "xboxseries", BTN_MAP_XBOXSERIES
    elif "xbox one" in name_lower or "xbone" in name_lower:
        print("[SGBU] Detected: Xbox One")
        return "xboxone", BTN_MAP_XBOXONE
    elif "xbox 360" in name_lower or "360 pad" in name_lower or "xinput" in name_lower:
        print("[SGBU] Detected: Xbox 360")
        return "xbox360", BTN_MAP_XBOX360
    elif "xbox" in name_lower or "microsoft" in name_lower or "x-box" in name_lower:
        print(f"[SGBU] Detected: Xbox (generic) — using Xbox One map")
        return "xboxone", BTN_MAP_XBOXONE
    else:
        print(f"[SGBU] Unknown controller '{device.name}', using PS4 button map")
        return "ps4", BTN_MAP_PS4

AXIS_THRESHOLD = 16000
stick_state = {"left_x": 0, "left_y": 0}

def handle_analog(ui, code, value):
    if code == evdev.ecodes.ABS_X:
        stick_state["left_x"] = value
    elif code == evdev.ecodes.ABS_Y:
        stick_state["left_y"] = value
    else:
        return
    lx = stick_state["left_x"]
    ly = stick_state["left_y"]
    if lx < -AXIS_THRESHOLD:
        ui.emit(uinput.KEY_LEFT, 1); ui.emit(uinput.KEY_LEFT, 0)
    elif lx > AXIS_THRESHOLD:
        ui.emit(uinput.KEY_RIGHT, 1); ui.emit(uinput.KEY_RIGHT, 0)
    if ly < -AXIS_THRESHOLD:
        ui.emit(uinput.KEY_UP, 1); ui.emit(uinput.KEY_UP, 0)
    elif ly > AXIS_THRESHOLD:
        ui.emit(uinput.KEY_DOWN, 1); ui.emit(uinput.KEY_DOWN, 0)

def handle_hat(ui, code, value):
    if code == evdev.ecodes.ABS_HAT0Y:
        if value == -1:
            ui.emit(uinput.KEY_UP, 1); ui.emit(uinput.KEY_UP, 0)
        elif value == 1:
            ui.emit(uinput.KEY_DOWN, 1); ui.emit(uinput.KEY_DOWN, 0)
    elif code == evdev.ecodes.ABS_HAT0X:
        if value == -1:
            ui.emit(uinput.KEY_LEFT, 1); ui.emit(uinput.KEY_LEFT, 0)
        elif value == 1:
            ui.emit(uinput.KEY_RIGHT, 1); ui.emit(uinput.KEY_RIGHT, 0)

def main():
    print("[SGBU] Controller mapper v0.0.4 starting...")
    print("[SGBU] Supports: PS3 / PS4 / PS5 / Xbox 360 / Xbox One / Xbox Series X|S")
    device = None
    for attempt in range(10):
        device = find_controller()
        if device:
            break
        print(f"[SGBU] No controller found, retrying ({attempt+1}/10)...")
        time.sleep(2)
    if not device:
        print("[SGBU] No controller found after retries. Exiting.")
        sys.exit(1)
    print(f"[SGBU] Using: {device.path} — {device.name}")
    ctrl_type, btn_map = detect_controller_type(device)
    events = [
        uinput.KEY_ENTER, uinput.KEY_ESC, uinput.KEY_BACKSPACE, uinput.KEY_SPACE,
        uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT,
        uinput.KEY_TAB,
        uinput.KEY_F1, uinput.KEY_F2, uinput.KEY_F3, uinput.KEY_F4,
        uinput.KEY_F5, uinput.KEY_F6, uinput.KEY_F7, uinput.KEY_F8,
        uinput.KEY_F9, uinput.KEY_F10,
    ]
    try:
        ui = uinput.Device(events)
    except Exception as e:
        print(f"[SGBU] Failed to create uinput device: {e}")
        print("[SGBU] Make sure uinput module is loaded: sudo modprobe uinput")
        sys.exit(1)
    try:
        device.grab()
        print(f"[SGBU] Controller grabbed ({ctrl_type} mode). Press Ctrl+C to stop.")
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = btn_map.get(event.code)
                if key is not None:
                    ui.emit(key, event.value)
            elif event.type == evdev.ecodes.EV_ABS:
                if event.code in (evdev.ecodes.ABS_HAT0X, evdev.ecodes.ABS_HAT0Y):
                    handle_hat(ui, event.code, event.value)
                elif event.code in (evdev.ecodes.ABS_X, evdev.ecodes.ABS_Y):
                    handle_analog(ui, event.code, event.value)
    except KeyboardInterrupt:
        print("\n[SGBU] Mapper stopped.")
    except Exception as e:
        print(f"[SGBU] Error: {e}")
    finally:
        try:
            device.ungrab()
        except Exception:
            pass

if __name__ == "__main__":
    main()
