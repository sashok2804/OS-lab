import sys
import psutil
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QTabWidget


class CustomTerminal(QWidget):
    def __init__(self):
        super().__init__()

        self.attached_process = None  # Процесс, к которому мы "присоединяемся"
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Введите команду")
        self.command_input.returnPressed.connect(self.process_command)
        layout.addWidget(QLabel("Терминал:"))
        layout.addWidget(self.command_input)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Вывод:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def append_output(self, text):
        """Функция для добавления текста в окно вывода"""
        self.output.append(text)

    def process_command(self):
        """Обработка введенной команды"""
        command = self.command_input.text().strip()
        if command:
            self.append_output(f"Выполнение команды: {command}")
            self.command_input.clear()

            # Разделяем команду на аргументы
            args = command.split()
            cmd = args[0].lower()

            # Обработка каждой команды
            if cmd == "meminfo":
                self.meminfo()
            elif cmd == "readmem" and len(args) == 2:
                self.readmem(args[1])
            elif cmd == "writemem" and len(args) == 3:
                self.writemem(args[1], args[2])
            elif cmd == "processlist":
                self.processlist()
            elif cmd == "killprocess" and len(args) == 2:
                self.killprocess(args[1])
            elif cmd == "memusage":
                self.memusage()
            elif cmd == "findprocess" and len(args) == 2:
                self.findprocess(args[1])
            elif cmd == "attach" and len(args) == 2:
                self.attach(args[1])
            elif cmd == "detach":
                self.detach()
            elif cmd == "help":
                self.show_help()
            else:
                self.append_output("Ошибка: неизвестная команда или неверное количество аргументов.")

    def meminfo(self):
        """Вывод информации о памяти"""
        mem = psutil.virtual_memory()
        self.append_output(f"Общая память: {mem.total}, Свободная память: {mem.available}, Используется: {mem.used}")

    def readmem(self, address):
        """Чтение данных по адресу"""
        try:
            addr = int(address, 16)
            self.append_output(f"Чтение данных по адресу {address}: значение 0xDEADBEEF (эмуляция)")
        except ValueError:
            self.append_output(f"Ошибка: неверный адрес {address}")

    def writemem(self, address, value):
        """Запись данных по адресу"""
        try:
            addr = int(address, 16)
            self.append_output(f"Запись значения {value} по адресу {address} (эмуляция)")
        except ValueError:
            self.append_output(f"Ошибка: неверный адрес {address}")

    def processlist(self):
        """Вывод списка процессов"""
        processes = psutil.process_iter(['pid', 'name'])
        for proc in processes:
            self.append_output(f"PID: {proc.info['pid']}, Имя: {proc.info['name']}")

    def killprocess(self, pid):
        """Завершение процесса по ID"""
        try:
            p = psutil.Process(int(pid))
            p.terminate()
            self.append_output(f"Процесс {pid} завершен.")
        except Exception as e:
            self.append_output(f"Ошибка при завершении процесса {pid}: {str(e)}")

    def memusage(self):
        """Использование памяти текущим приложением"""
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        self.append_output(f"Использование памяти приложением: {mem_info.rss} байт")

    def findprocess(self, name):
        """Поиск процесса по имени"""
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                self.append_output(f"Найден процесс: PID {proc.info['pid']}, Имя {proc.info['name']}")
                found = True
        if not found:
            self.append_output(f"Процесс с именем {name} не найден.")

    def attach(self, pid):
        """Присоединение к процессу"""
        try:
            self.attached_process = psutil.Process(int(pid))
            self.append_output(f"Присоединение к процессу {pid} (эмуляция)")
        except Exception as e:
            self.append_output(f"Ошибка при присоединении к процессу: {str(e)}")

    def detach(self):
        """Отключение от процесса"""
        if self.attached_process:
            self.append_output(f"Отключение от процесса {self.attached_process.pid} (эмуляция)")
            self.attached_process = None
        else:
            self.append_output("Нет присоединенного процесса для отключения.")

    def show_help(self):
        """Показ справки по командам"""
        help_text = """
Доступные команды:
  meminfo               - Показать информацию о памяти
  readmem <address>     - Чтение данных по указанному адресу
  writemem <address> <value> - Запись значения по указанному адресу
  processlist           - Показать список процессов
  killprocess <pid>     - Завершить процесс по ID
  memusage              - Показать использование памяти текущим приложением
  findprocess <name>    - Найти процесс по имени
  attach <pid>          - Присоединиться к процессу
  detach                - Отключиться от процесса
  help                  - Показать эту справку
"""
        self.append_output(help_text)


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
        if not address:
            self.output.append("Ошибка: адрес не введён.")
            return

        try:
            self.output.append(f"Чтение данных по адресу {address}: значение 0xDEADBEEF (эмуляция)")
        except Exception as e:
            self.output.append(f"Ошибка при чтении данных: {str(e)}")

    def write_memory(self):
        address = self.address_input.text()
        value = self.value_input.text()
        if not address or not value:
            self.output.append("Ошибка: адрес или значение не введены.")
            return

        try:
            self.output.append(f"Запись значения {value} по адресу {address} выполнена успешно (эмуляция).")
        except Exception as e:
            self.output.append(f"Ошибка при записи данных: {str(e)}")

    def show_process_info(self):
        try:
            processes = psutil.process_iter(['pid', 'name', 'memory_info'])
            for proc in processes:
                self.output.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Memory: {proc.info['memory_info']}")
        except Exception as e:
            self.output.append(f"Ошибка при получении информации о процессах: {str(e)}")


class CombinedApp(QTabWidget):
    def __init__(self):
        super().__init__()

        self.memory_tab = MemoryApp()
        self.terminal_tab = CustomTerminal()

        self.addTab(self.memory_tab, "Чтение/Запись памяти")
        self.addTab(self.terminal_tab, "Терминал")

        self.setWindowTitle('Memory & Terminal App')


def main():
    app = QApplication(sys.argv)
    combined_app = CombinedApp()
    combined_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
