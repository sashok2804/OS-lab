import tkinter as tk
from input_devices import get_mouse_position, listen_keyboard
from system_info import get_gpu_info, get_monitor_info

class DeviceInfoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PC Device Info and Input Listener")
        self.geometry("600x400")

        # Метка для отображения позиции мыши
        self.mouse_position_label = tk.Label(self, text="Mouse Position: ", font=("Helvetica", 12))
        self.mouse_position_label.pack(pady=10)

        # Метка для отображения последней нажатой клавиши
        self.key_label = tk.Label(self, text="Last Key Pressed: ", font=("Helvetica", 12))
        self.key_label.pack(pady=10)

        # Кнопка для начала отслеживания мыши и клавиатуры
        btn_start_listeners = tk.Button(self, text="Start Listening to Mouse and Keyboard", command=self.start_listeners)
        btn_start_listeners.pack(pady=10)

        # Метка для отображения информации о видеокарте
        self.gpu_info_label = tk.Label(self, text="GPU Info: ", font=("Helvetica", 12), justify=tk.LEFT)
        self.gpu_info_label.pack(pady=10)

        # Кнопка для получения информации о видеокарте
        btn_get_gpu_info = tk.Button(self, text="Get GPU Info", command=self.display_gpu_info)
        btn_get_gpu_info.pack(pady=10)

        # Метка для отображения информации о мониторах
        self.monitor_info_label = tk.Label(self, text="Monitor Info: ", font=("Helvetica", 12), justify=tk.LEFT)
        self.monitor_info_label.pack(pady=10)

        # Кнопка для получения информации о мониторах
        btn_get_monitor_info = tk.Button(self, text="Get Monitor Info", command=self.display_monitor_info)
        btn_get_monitor_info.pack(pady=10)

    # Запуск отслеживания мыши и клавиатуры
    def start_listeners(self):
        get_mouse_position(self.update_mouse_position)
        listen_keyboard(self.update_key_press)

    # Обновление позиции мыши
    def update_mouse_position(self, position):
        self.mouse_position_label.config(text=f"Mouse Position: {position}")

    # Обновление информации о последней нажатой клавише
    def update_key_press(self, key):
        self.key_label.config(text=f"Last Key Pressed: {key}")

    # Отображение информации о видеокарте
    def display_gpu_info(self):
        gpu_info = get_gpu_info()
        self.gpu_info_label.config(text=f"GPU Info:\n{gpu_info}")

    # Отображение информации о мониторах
    def display_monitor_info(self):
        monitor_info = get_monitor_info()
        self.monitor_info_label.config(text=f"Monitor Info:\n{monitor_info}")
