import os
import psutil
import shutil
import socket
import pwd
import grp
from getpass import getuser

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
            "14. ps — показывает процессы.\n"
            "15. who — показывает текущего пользователя.\n"
            "16. df — показывает использование диска.\n"
            "17. du — показывает размер директорий.\n"
            "18. top — показывает системные процессы.\n"
            "19. kill <pid> — завершает процесс по ID.\n"
            "20. ip a — показывает информацию об IP-адресах.\n"
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

    # Команды безопасности через Python API
    elif cmd == 'ps':
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                processes.append(f"{proc.info['pid']} {proc.info['username']} {proc.info['name']}")
            return "\n".join(processes)
        except Exception as e:
            return f"Ошибка при получении списка процессов: {e}"

    elif cmd == 'who':
        return f"Текущий пользователь: {getuser()}"

    elif cmd == 'df':
        try:
            partitions = psutil.disk_partitions()
            usage = []
            for partition in partitions:
                part_usage = psutil.disk_usage(partition.mountpoint)
                usage.append(
                    f"{partition.device} {part_usage.total // (2**30)}G {part_usage.used // (2**30)}G {part_usage.free // (2**30)}G"
                )
            return "\n".join(usage)
        except Exception as e:
            return f"Ошибка при получении информации о диске: {e}"

    elif cmd == 'du':
        if len(command_parts) < 2:
            path = '.'
        else:
            path = command_parts[1]
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return f"Размер директории {path}: {total_size // (1024 * 1024)} MB"
        except Exception as e:
            return f"Ошибка при получении размера директории: {e}"

    elif cmd == 'top':
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(f"{proc.info['pid']} {proc.info['name']} CPU: {proc.info['cpu_percent']}% MEM: {proc.info['memory_percent']}%")
            return "\n".join(processes)
        except Exception as e:
            return f"Ошибка при получении списка процессов: {e}"

    elif cmd == 'kill':
        if len(command_parts) < 2:
            return "Пожалуйста, укажите PID процесса."
        pid = int(command_parts[1])
        try:
            psutil.Process(pid).kill()
            return f"Процесс с PID {pid} завершен."
        except Exception as e:
            return f"Ошибка при завершении процесса: {e}"

    elif cmd == 'ip' and command_parts[1] == 'a':
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return f"Hostname: {hostname}\nIP Address: {ip_address}"
        except Exception as e:
            return f"Ошибка при получении информации об IP: {e}"
        
    elif cmd == 'chmod':
        if len(command_parts) < 3:
            return "Пожалуйста, укажите режим доступа и файл."
        mode = int(command_parts[1], 8)
        filename = command_parts[2]
        try:
            os.chmod(filename, mode)
            return f"Права доступа для {filename} изменены на {oct(mode)}."
        except OSError as e:
            return f"Ошибка при изменении прав доступа: {e}"

    elif cmd == 'chown':
        if len(command_parts) < 3:
            return "Пожалуйста, укажите пользователя, группу и файл."
        user_group = command_parts[1].split(':')
        user = user_group[0]
        group = user_group[1] if len(user_group) > 1 else None
        filename = command_parts[2]

        try:
            uid = pwd.getpwnam(user).pw_uid
            gid = grp.getgrnam(group).gr_gid if group else -1
            os.chown(filename, uid, gid)
            return f"Владелец файла {filename} изменен на {user}:{group}."
        except KeyError:
            return "Пользователь или группа не найдены."
        except OSError as e:
            return f"Ошибка при изменении владельца файла: {e}"

    else:
        return f"Неизвестная команда: {command}"
