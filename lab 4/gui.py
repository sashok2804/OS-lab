import tkinter as tk
from input_devices import get_mouse_position, listen_keyboard, stop_mouse_tracking
from system_info import get_gpu_info, get_monitor_info

class DeviceInfoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Информация о ПК и вводе данных")
        self.geometry("600x400")

        # Метка для отображения позиции мыши
        self.mouse_position_label = tk.Label(self, text="Позиция мыши: ", font=("Helvetica", 12))
        self.mouse_position_label.pack(pady=10)

        # Метка для отображения последней нажатой клавиши
        self.key_label = tk.Label(self, text="Последняя нажатая клавиша: ", font=("Helvetica", 12))
        self.key_label.pack(pady=10)

        # Кнопка для начала отслеживания мыши и клавиатуры
        btn_start_listeners = tk.Button(self, text="Начать отслеживание мыши и клавиатуры", command=self.start_listeners)
        btn_start_listeners.pack(pady=10)

        # Кнопка для остановки отслеживания мыши
        btn_stop_mouse_tracking = tk.Button(self, text="Остановить отслеживание мыши", command=self.stop_mouse_tracking)
        btn_stop_mouse_tracking.pack(pady=10)

        # Метка для отображения информации о видеокарте
        self.gpu_info_label = tk.Label(self, text="Информация о видеокарте: ", font=("Helvetica", 12), justify=tk.LEFT)
        self.gpu_info_label.pack(pady=10)

        # Кнопка для получения информации о видеокарте
        btn_get_gpu_info = tk.Button(self, text="Получить информацию о видеокарте", command=self.display_gpu_info)
        btn_get_gpu_info.pack(pady=10)

        # Метка для отображения информации о мониторах
        self.monitor_info_label = tk.Label(self, text="Информация о мониторах: ", font=("Helvetica", 12), justify=tk.LEFT)
        self.monitor_info_label.pack(pady=10)

        # Кнопка для получения информации о мониторах
        btn_get_monitor_info = tk.Button(self, text="Получить информацию о мониторах", command=self.display_monitor_info)
        btn_get_monitor_info.pack(pady=10)

    # Запуск отслеживания мыши и клавиатуры
    def start_listeners(self):
        get_mouse_position(self.update_mouse_position)
        listen_keyboard(self.update_key_press)

    # Остановка отслеживания мыши
    def stop_mouse_tracking(self):
        stop_mouse_tracking()

    # Обновление позиции мыши
    def update_mouse_position(self, position):
        self.mouse_position_label.config(text=f"Позиция мыши: {position}")

    # Обновление информации о последней нажатой клавише
    def update_key_press(self, key):
        self.key_label.config(text=f"Последняя нажатая клавиша: {key}")

    # Отображение информации о видеокарте
    def display_gpu_info(self):
        gpu_info = get_gpu_info()
        self.gpu_info_label.config(text=f"Информация о видеокарте:\n{gpu_info}")

    # Отображение информации о мониторах
    def display_monitor_info(self):
        monitor_info = get_monitor_info()
        self.monitor_info_label.config(text=f"Информация о мониторах:\n{monitor_info}")
