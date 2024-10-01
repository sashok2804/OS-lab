import pyautogui
import keyboard
from threading import Thread

# Глобальная переменная для управления отслеживанием мыши
tracking_mouse = False

# Функция для получения координат мыши
def get_mouse_position(callback):
    global tracking_mouse
    tracking_mouse = True

    def track_mouse():
        while tracking_mouse:
            pos = pyautogui.position()
            callback(pos)

    thread = Thread(target=track_mouse)
    thread.daemon = True
    thread.start()

# Функция для остановки отслеживания мыши
def stop_mouse_tracking():
    global tracking_mouse
    tracking_mouse = False

# Функция для отслеживания нажатий клавиш
def listen_keyboard(callback):
    def on_key_event(e):
        callback(e.name)

    thread = Thread(target=lambda: keyboard.hook(on_key_event))
    thread.daemon = True
    thread.start()
