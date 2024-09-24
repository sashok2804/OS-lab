import sys
import psutil
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel

class MemoryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        # Основные элементы интерфейса
        layout = QVBoxLayout()

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Введите адрес памяти (hex)")
        layout.addWidget(QLabel("Адрес памяти:"))
        layout.addWidget(self.address_input)

        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Введите значение для записи")
        layout.addWidget(QLabel("Значение:"))
        layout.addWidget(self.value_input)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Вывод:"))
        layout.addWidget(self.output)

        # Кнопки для взаимодействия
        read_btn = QPushButton("Читать", self)
        read_btn.clicked.connect(self.read_memory)
        layout.addWidget(read_btn)

        write_btn = QPushButton("Записать", self)
        write_btn.clicked.connect(self.write_memory)
        layout.addWidget(write_btn)

        # Кнопка для информации о процессах
        process_info_btn = QPushButton("Информация о процессах", self)
        process_info_btn.clicked.connect(self.show_process_info)
        layout.addWidget(process_info_btn)

        # Терминал
        terminal_btn = QPushButton("Запустить терминал", self)
        terminal_btn.clicked.connect(self.run_terminal)
        layout.addWidget(terminal_btn)

        # Установка основного лэйаута
        self.setLayout(layout)
        self.setWindowTitle('Memory Reader/Writer')

    def read_memory(self):
        address = self.address_input.text()
        if not address:
            self.output.append("Ошибка: адрес не введён.")
            return

        try:
            # Выполняем команду чтения памяти через scanmem
            result = subprocess.run(['scanmem', '-p', 'game_pid', '-r', address], capture_output=True, text=True)
            self.output.append(f"Чтение данных по адресу {address}: {result.stdout}")
        except Exception as e:
            self.output.append(f"Ошибка при чтении данных: {str(e)}")

    def write_memory(self):
        address = self.address_input.text()
        value = self.value_input.text()
        if not address or not value:
            self.output.append("Ошибка: адрес или значение не введены.")
            return

        try:
            # Выполняем команду записи в память через scanmem
            subprocess.run(['scanmem', '-p', 'game_pid', '-w', address, value], check=True)
            self.output.append(f"Запись значения {value} по адресу {address} выполнена успешно.")
        except Exception as e:
            self.output.append(f"Ошибка при записи данных: {str(e)}")

    def show_process_info(self):
        # Используем библиотеку psutil для получения информации о процессах
        try:
            processes = psutil.process_iter(['pid', 'name', 'memory_info'])
            for proc in processes:
                self.output.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_info']}")
        except Exception as e:
            self.output.append(f"Ошибка при получении информации о процессах: {str(e)}")

    def run_terminal(self):
        # Встроенный терминал для выполнения команд
        try:
            os.system("gnome-terminal")  # Открывает терминал GNOME (можно заменить на другой терминал)
        except Exception as e:
            self.output.append(f"Ошибка при запуске терминала: {str(e)}")


def main():
    app = QApplication(sys.argv)
    memory_app = MemoryApp()
    memory_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
