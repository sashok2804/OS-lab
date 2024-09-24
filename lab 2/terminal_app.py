import psutil
import os
import struct
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel

def read_from_memory(pid, address, size=4):
    """Функция для чтения памяти процесса"""
    try:
        with open(f"/proc/{pid}/mem", 'rb', 0) as mem_file:
            mem_file.seek(address)
            return mem_file.read(size)
    except Exception as e:
        return str(e)

def write_to_memory(pid, address, value):
    """Функция для записи в память процесса"""
    try:
        with open(f"/proc/{pid}/mem", 'wb', 0) as mem_file:
            mem_file.seek(address)
            mem_file.write(value)
        return "Запись успешно завершена."
    except Exception as e:
        return str(e)

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

            args = command.split()
            cmd = args[0].lower()

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
            if not self.attached_process:
                self.append_output("Ошибка: необходимо присоединиться к процессу.")
                return
            
            addr = int(address, 16)
            pid = self.attached_process.pid
            data = read_from_memory(pid, addr)
            if isinstance(data, bytes):
                value = struct.unpack('I', data)[0]  # Читаем 4 байта как целое число
                self.append_output(f"Чтение данных по адресу {address}: значение {value}")
            else:
                self.append_output(f"Ошибка при чтении: {data}")
        except ValueError:
            self.append_output(f"Ошибка: неверный адрес {address}")

    def writemem(self, address, value):
        """Запись данных по адресу"""
        try:
            if not self.attached_process:
                self.append_output("Ошибка: необходимо присоединиться к процессу.")
                return

            addr = int(address, 16)
            pid = self.attached_process.pid
            value_to_write = struct.pack('I', int(value))  # Записываем 4-байтовое целое число
            result = write_to_memory(pid, addr, value_to_write)
            self.append_output(f"Запись значения {value} по адресу {address}: {result}")
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
        try:
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            self.append_output(f"Использование памяти приложением: {mem_info.rss} байт")
        except Exception as e:
            self.append_output(f"Ошибка при получении использования памяти: {str(e)}")

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
        """Присоединение к процессу с использованием gdb"""
        try:
            os.system(f"sudo gdb -p {pid}")  # Используем gdb для присоединения к процессу
            self.attached_process = psutil.Process(int(pid))
            self.append_output(f"Присоединение к процессу {pid}")
        except Exception as e:
            self.append_output(f"Ошибка при присоединении к процессу: {str(e)}")

    def detach(self):
        """Отключение от процесса"""
        if self.attached_process:
            try:
                os.system(f"sudo gdb -p {self.attached_process.pid} -batch -ex detach")  # Отключение через gdb
                self.append_output(f"Отключение от процесса {self.attached_process.pid}")
                self.attached_process = None
            except Exception as e:
                self.append_output(f"Ошибка при отключении: {str(e)}")
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
