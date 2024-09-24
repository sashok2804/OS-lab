import tkinter as tk
from tkinter import ttk
from battery import charge_battery_process, discharge_battery_process
from command_line import CommandLineApp
from multiprocessing import Value
from multiprocessing import Process


class BatteryApp:
    def __init__(self, parent):
        self.parent = parent
        self.battery_level = Value('d', 100.0)

        # Метка для уровня заряда
        self.battery_label = ttk.Label(parent, text=f"Battery level: {self.battery_level.value:.1f}%")
        self.battery_label.pack(pady=10)

        # Кнопки для запуска разряда и заряда
        self.start_discharge_button = ttk.Button(parent, text="Start Discharging", command=self.start_discharge_process)
        self.start_discharge_button.pack(pady=5)

        self.start_charge_button = ttk.Button(parent, text="Start Charging", command=self.start_charge_process)
        self.start_charge_button.pack(pady=5)

        # Поле для ввода приоритета
        self.priority_label = ttk.Label(parent, text="Set Process Priority (-20 to 19):")
        self.priority_label.pack(pady=5)
        self.priority_entry = ttk.Entry(parent)
        self.priority_entry.pack(pady=5)
        self.priority_entry.insert(0, "0")

        # Обновление уровня заряда
        self.update_battery_label()

    def update_battery_label(self):
        self.battery_label.config(text=f"Battery level: {self.battery_level.value:.1f}%")
        self.parent.after(1000, self.update_battery_label)

    def start_discharge_process(self):
        priority = int(self.priority_entry.get())
        discharge_process = Process(target=discharge_battery_process, args=(self.battery_level, priority))
        discharge_process.start()

    def start_charge_process(self):
        priority = int(self.priority_entry.get())
        charge_process = Process(target=charge_battery_process, args=(self.battery_level, priority))
        charge_process.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battery Simulator")

    notebook = ttk.Notebook(root)
    battery_frame = ttk.Frame(notebook)
    command_frame = ttk.Frame(notebook)

    notebook.add(battery_frame, text="Battery Simulator")
    notebook.add(command_frame, text="Command Line")

    notebook.pack(expand=True, fill="both")

    # Инициализация приложения
    app = BatteryApp(battery_frame)
    cli = CommandLineApp(command_frame)

    root.mainloop()
