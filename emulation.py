from config import ZONE_X, ZONE_Y, SPEED, DURATION
import pyautogui

def normalize_data(a):
    k = 1
    if a == 0:
        a = 1
    if a < 0:
        a = abs(a)
        k = -1
    return SPEED * k, DURATION / a

def move_mouse(x, y):
    if abs(x) > ZONE_X:
        speed, d = normalize_data(x)
        pyautogui.move(speed, None, d)
    if abs(y) > ZONE_Y:
        speed, d = normalize_data(x)
        pyautogui.move(None, speed, d)