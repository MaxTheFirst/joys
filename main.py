from config import *
from vgamepad import VDS4Gamepad, XUSB_BUTTON
from serial import Serial, SerialException
from serial.tools.list_ports import comports 
from time import sleep

buttons = [XUSB_BUTTON.XUSB_GAMEPAD_A, XUSB_BUTTON.XUSB_GAMEPAD_B, XUSB_BUTTON.XUSB_GAMEPAD_X, XUSB_BUTTON.XUSB_GAMEPAD_Y, XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER]

gamepad = VDS4Gamepad()

def map_diapazone(x):
    return int((x - INPUT_MIN) * (OUTPUT_MAX - OUTPUT_MIN) / (INPUT_MAX - INPUT_MIN) + OUTPUT_MIN)

def get_data(serial: Serial):
    try:
        line = serial.readline().decode().strip()
        return list(map(int, line.split(',')))
    except (ValueError, SerialException):
        return None
    

def get_arduino():
    while True:
        try:
            serial = Serial(PORT, BAUDRATE, timeout=1, write_timeout=1, inter_byte_timeout=1)
        except SerialException:
            continue
        if get_data(serial):
            return serial
        sleep(1)
        
def update_buttons(data_buttons):
    for i, state in enumerate(data_buttons):
        if state:
            gamepad.press_button(buttons[i])
        else:
            gamepad.release_button(buttons[i])

def update_jostick(data):
    gamepad.left_joystick(*map(map_diapazone, data))

def main():
    serial = None
    last_data = None
    while True:
        if not serial:
            serial = get_arduino()
        data = get_data(serial)
        if not data:
            serial = None
            continue
        if data != last_data:
            last_data = data
            print(data)
            update_jostick(data[:2])
            update_buttons(data[2:])
            gamepad.update()

if __name__ == '__main__':
    main()