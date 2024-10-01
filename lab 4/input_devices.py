import pyautogui
import keyboard
from threading import Thread

# Функция для получения координат мыши
def get_mouse_position(callback):
    def track_mouse():
        while True:
            pos = pyautogui.position()
            callback(pos)  # Передача позиции через callback

    thread = Thread(target=track_mouse)
    thread.daemon = True
    thread.start()

# Функция для отслеживания нажатий клавиш
def listen_keyboard(callback):
    def on_key_event(e):
        callback(e.name)  # Передача нажатой клавиши через callback

    thread = Thread(target=lambda: keyboard.hook(on_key_event))
    thread.daemon = True
    thread.start()
