import os
import psutil
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel

class MemoryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Введите адрес памяти (hex)")
        layout.addWidget(QLabel("Адрес памяти:"))
        layout.addWidget(self.address_input)

        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Введите значение для записи")
        layout.addWidget(QLabel("Значение:"))
        layout.addWidget(self.value_input)

        self.pid_input = QLineEdit(self)
        self.pid_input.setPlaceholderText("Введите PID процесса")
        layout.addWidget(QLabel("PID процесса:"))
        layout.addWidget(self.pid_input)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Вывод:"))
        layout.addWidget(self.output)

        read_btn = QPushButton("Читать", self)
        read_btn.clicked.connect(self.read_memory)
        layout.addWidget(read_btn)

        write_btn = QPushButton("Записать", self)
        write_btn.clicked.connect(self.write_memory)
        layout.addWidget(write_btn)

        process_info_btn = QPushButton("Информация о процессах", self)
        process_info_btn.clicked.connect(self.show_process_info)
        layout.addWidget(process_info_btn)

        self.setLayout(layout)

    def read_memory(self):
        address = self.address_input.text()
        pid = self.pid_input.text()

        if not address or not pid:
            self.output.append("Ошибка: адрес или PID не введены.")
            return

        try:
            addr = int(address, 16)
            pid = int(pid)

            mem_file = f"/proc/{pid}/mem"
            with open(mem_file, 'rb') as mem:
                mem.seek(addr)
                value = mem.read(4)  # Чтение 4 байт
                value_hex = value.hex()
                self.output.append(f"Чтение данных по адресу {address} (PID {pid}): значение {value_hex}")
        except Exception as e:
            self.output.append(f"Ошибка при чтении данных: {str(e)}")

    def write_memory(self):
        address = self.address_input.text()
        value = self.value_input.text()
        pid = self.pid_input.text()

        if not address or not value or not pid:
            self.output.append("Ошибка: адрес, значение или PID не введены.")
            return

        try:
            addr = int(address, 16)
            pid = int(pid)
            value_bytes = bytes.fromhex(value)

            mem_file = f"/proc/{pid}/mem"
            with open(mem_file, 'r+b') as mem:
                mem.seek(addr)
                mem.write(value_bytes)
                self.output.append(f"Запись значения {value} по адресу {address} (PID {pid}) выполнена успешно.")
        except Exception as e:
            self.output.append(f"Ошибка при записи данных: {str(e)}")

    def show_process_info(self):
        try:
            processes = psutil.process_iter(['pid', 'name', 'memory_info'])
            for proc in processes:
                self.output.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_info']}")
        except Exception as e:
            self.output.append(f"Ошибка при получении информации о процессах: {str(e)}")
