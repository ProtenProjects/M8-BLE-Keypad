import board
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
import keypad
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

KEY_PINS = [
    board.D1,
    board.D2,
    board.D3,
    board.D4,
    board.D5,
    board.D6,
    board.D7,
    board.D8,
]

KEYCODES = [
    Keycode.X,
    Keycode.Z,
    Keycode.UP_ARROW,
    Keycode.RIGHT_ARROW,
    Keycode.DOWN_ARROW,
    Keycode.LEFT_ARROW,
    Keycode.SPACE,
    Keycode.SHIFT,
]

hid = HIDService()
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
kbd = Keyboard(hid.devices)

device_info = DeviceInfoService(
    software_revision=adafruit_ble.__version__, manufacturer="Adafruit Industries"
)
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "M8_PAD"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)


while True:
    event = keys.events.get()
    if event:
        key_number = event.key_number
        # A key transition occurred.
        if event.pressed:
            print(KEYCODES[key_number])
            kbd.press(KEYCODES[key_number])

        if event.released:
            kbd.release(KEYCODES[key_number])
