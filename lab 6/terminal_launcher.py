import os
import platform
import shutil
from datetime import datetime

def run_terminal_command(command):
    command_parts = command.strip().split()

    if not command_parts:
        return "Пожалуйста, введите команду."

    cmd = command_parts[0]

    # Базовые команды
    if cmd == 'help':
        return (
            "Доступные команды:\n"
            "1. help — показывает доступные команды.\n"
            "2. clear — очищает терминал.\n"
            "Работа с файлами:\n"
            "3. ls — показывает список файлов в текущей директории.\n"
            "4. pwd — показывает текущую директорию.\n"
            "5. mkdir <dirname> — создает новую директорию.\n"
            "6. rmdir <dirname> — удаляет пустую директорию.\n"
            "7. touch <filename> — создает новый файл.\n"
            "8. rm <filename> — удаляет файл.\n"
            "9. mv <src> <dst> — перемещает или переименовывает файл или папку.\n"
            "10. cp <src> <dst> — копирует файл или папку.\n"
            "11. cat <filename> — показывает содержимое файла.\n"
            "12. chmod <mode> <filename> — изменяет права доступа к файлу.\n"
            "13. chown <user>:<group> <filename> — изменяет владельца файла.\n"
            "Команды безопасности:\n"
            "14. netstat — показывает сетевые подключения.\n"
            "15. ps — показывает процессы.\n"
            "16. ufw status — проверка статуса файрвола (Linux).\n"
            "17. who — показывает список текущих пользователей системы.\n"
            "18. last — показывает историю входов пользователей.\n"
            "19. df — показывает использование диска.\n"
            "20. du — показывает размер директорий.\n"
            "21. top — показывает системные процессы в реальном времени.\n"
            "22. kill <pid> — завершает процесс по ID.\n"
            "23. ip a — показывает информацию об IP-адресах.\n"
        )
    elif cmd == 'clear':
        return ""

    # Работа с файлами
    elif cmd == 'ls':
        try:
            files = os.listdir()
            output = "\n".join(files)
            return output if output else "Директория пуста."
        except Exception as e:
            return f"Ошибка при выполнении команды ls: {e}"

    elif cmd == 'pwd':
        return os.getcwd()

    elif cmd == 'mkdir':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя директории."
        dirname = command_parts[1]
        try:
            os.mkdir(dirname)
            return f"Директория {dirname} создана."
        except OSError as e:
            return f"Ошибка при создании директории: {e}"

    elif cmd == 'rmdir':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя директории."
        dirname = command_parts[1]
        try:
            os.rmdir(dirname)
            return f"Директория {dirname} удалена."
        except OSError as e:
            return f"Ошибка при удалении директории: {e}"

    elif cmd == 'touch':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя файла."
        filename = command_parts[1]
        try:
            with open(filename, 'w'):
                pass
            return f"Файл {filename} создан."
        except OSError as e:
            return f"Ошибка при создании файла: {e}"

    elif cmd == 'rm':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя файла."
        filename = command_parts[1]
        try:
            os.remove(filename)
            return f"Файл {filename} удален."
        except OSError as e:
            return f"Ошибка при удалении файла: {e}"

    elif cmd == 'mv':
        if len(command_parts) < 3:
            return "Пожалуйста, укажите исходный и целевой файл."
        src = command_parts[1]
        dst = command_parts[2]
        try:
            shutil.move(src, dst)
            return f"{src} перемещен в {dst}."
        except OSError as e:
            return f"Ошибка при перемещении: {e}"

    elif cmd == 'cp':
        if len(command_parts) < 3:
            return "Пожалуйста, укажите исходный и целевой файл."
        src = command_parts[1]
        dst = command_parts[2]
        try:
            shutil.copy(src, dst)
            return f"{src} скопирован в {dst}."
        except OSError as e:
            return f"Ошибка при копировании: {e}"

    elif cmd == 'cat':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите имя файла."
        filename = command_parts[1]
        try:
            with open(filename, 'r') as f:
                return f.read()
        except OSError as e:
            return f"Ошибка при чтении файла: {e}"

    # Команды безопасности
    elif cmd == 'ps':
        try:
            processes = os.popen('ps aux').read()
            return processes
        except Exception as e:
            return f"Ошибка при получении списка процессов: {e}"

    elif cmd == 'who':
        try:
            users = os.popen('who').read()
            return users
        except Exception as e:
            return f"Ошибка при получении списка пользователей: {e}"

    elif cmd == 'df':
        try:
            usage = os.popen('df -h').read()
            return usage
        except Exception as e:
            return f"Ошибка при получении информации о диске: {e}"

    elif cmd == 'du':
        try:
            size = os.popen('du -sh').read()
            return size
        except Exception as e:
            return f"Ошибка при получении размера директорий: {e}"

    elif cmd == 'top':
        try:
            top_output = os.popen('top -bn1').read()
            return top_output
        except Exception as e:
            return f"Ошибка при запуске top: {e}"

    elif cmd == 'kill':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите PID процесса."
        pid = command_parts[1]
        try:
            os.kill(int(pid), 9)
            return f"Процесс с PID {pid} завершен."
        except OSError as e:
            return f"Ошибка при завершении процесса: {e}"

    elif cmd == 'ip' and command_parts[1] == 'a':
        try:
            ip_info = os.popen('ip a').read()
            return ip_info
        except Exception as e:
            return f"Ошибка при получении информации об IP: {e}"

    else:
        return f"Неизвестная команда: {command}"
