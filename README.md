## README MADE BY AI
---

# Controller-to-Keyboard Mapper (evdev + uinput)

This Python script maps controller button inputs (PS3, PS4, Xbox, or generic gamepads) to keyboard key events on Linux systems using the **evdev** and **uinput** libraries.
It effectively lets you use your game controller as a virtual keyboard device.

---

## 🧩 Features

* Automatically detects a connected controller device.
* Supports multiple controller types:

  * PlayStation 3 (PS3)
  * PlayStation 4 (PS4)
  * Xbox 360 / Xbox One
  * Generic gamepads (including those using hat axes for D-pad)
* Maps controller buttons and D-pad directions to keyboard keys:

  * **A / X / Cross** → Enter
  * **B / Circle** → Esc
  * **X / Square** → Backspace
  * **Y / Triangle** → Space
  * **D-pad** → Arrow keys (Up, Down, Left, Right)

---

## ⚙️ Requirements

* Linux system (with `/dev/input` and `/dev/uinput` available)
* Python 3.x
* `evdev` and `uinput` libraries

Install dependencies with:

```bash
sudo apt install python3-evdev
pip install python-uinput
```

You may need to load the `uinput` kernel module if it’s not already active:

```bash
sudo modprobe uinput
```

---

## 🚀 Usage

1. Connect your controller via USB or Bluetooth.

2. Run the script with root privileges (required for input access):

   ```bash
   sudo python3 controller_mapper.py
   ```

3. The script will automatically detect your controller and print which device it’s using, e.g.:

   ```
   Using device: /dev/input/event4 (Sony Interactive Entertainment Wireless Controller)
   ```

4. Pressing controller buttons will now generate corresponding keyboard events in any active window.

---

## 🧭 How It Works

1. **Device Detection** – The script scans `/dev/input/` for any device with key event capabilities.
2. **Virtual Keyboard Creation** – A virtual keyboard device is created via `uinput`.
3. **Button Mapping** – Controller button codes are translated to keyboard key codes using predefined maps.
4. **Event Loop** – The script continuously reads input events and emits the matching keyboard events in real time.

---

## 🎮 Supported Button Maps

| Controller                 | Button                   | Mapped Key |
| -------------------------- | ------------------------ | ---------- |
| PS3 / PS4 / Xbox / Generic | X / Cross / A            | Enter      |
| PS3 / PS4 / Xbox / Generic | Circle / B               | Esc        |
| PS3 / PS4 / Xbox / Generic | Square / X               | Backspace  |
| PS3 / PS4 / Xbox / Generic | Triangle / Y             | Space      |
| D-pad                      | Up / Down / Left / Right | Arrow keys |

---

## ⚠️ Notes

* Root access is required to grab input devices and emit uinput events.
* This script will **grab** the controller device (it won’t be usable by other applications while running).
* The mappings can easily be customized by editing the `BTN_MAP_*` dictionaries in the script.

---

## 🧠 Example Customization

To map the **Circle** button to **Backspace** instead of **Esc**, simply edit:

```python
305: uinput.KEY_BACKSPACE
```

in the `BTN_MAP_PS4` or relevant dictionary.

---

## 🏁 License

This project is released under the MIT License.
Use freely and modify as needed for your system setup.

---

## to run the python script do
```bash
sudo chmod 777 $controller.py
```

> 777 will add read write execute permition to every one use ``chmod +x `` for security reasons
