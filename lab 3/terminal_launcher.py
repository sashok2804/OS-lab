import subprocess
import os
import platform
from tkinter import messagebox

def run_terminal_command(command):
    command_parts = command.strip().split()

    if not command_parts:
        return "Пожалуйста, введите команду."

    cmd = command_parts[0]

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
        )

    elif cmd == 'clear':
        return ""  

    elif cmd == 'ls':
        try:
            output = subprocess.check_output(['ls'], universal_newlines=True)
            return output
        except Exception as e:
            return f"Ошибка при выполнении команды ls: {e}"

    elif cmd == 'pwd':
        try:
            output = subprocess.check_output(['pwd'], universal_newlines=True)
            return output
        except Exception as e:
            return f"Ошибка при выполнении команды pwd: {e}"

    elif cmd == 'mkdir' and len(command_parts) > 1:
        dirname = command_parts[1]
        try:
            os.mkdir(dirname)
            return f"Директория '{dirname}' создана."
        except Exception as e:
            return f"Ошибка при создании директории '{dirname}': {e}"

    elif cmd == 'rmdir' and len(command_parts) > 1:
        dirname = command_parts[1]
        try:
            os.rmdir(dirname)
            return f"Директория '{dirname}' удалена."
        except Exception as e:
            return f"Ошибка при удалении директории '{dirname}': {e}"

    elif cmd == 'touch' and len(command_parts) > 1:
        filename = command_parts[1]
        try:
            open(filename, 'a').close()
            return f"Файл '{filename}' создан."
        except Exception as e:
            return f"Ошибка при создании файла '{filename}': {e}"

    elif cmd == 'rm' and len(command_parts) > 1:
        filename = command_parts[1]
        try:
            os.remove(filename)
            return f"Файл '{filename}' удален."
        except Exception as e:
            return f"Ошибка при удалении файла '{filename}': {e}"

    elif cmd == 'mv' and len(command_parts) > 2:
        src = command_parts[1]
        dst = command_parts[2]
        try:
            os.rename(src, dst)
            return f"'{src}' перемещен или переименован в '{dst}'."
        except Exception as e:
            return f"Ошибка при перемещении или переименовании '{src}': {e}"

    elif cmd == 'cp' and len(command_parts) > 2:
        src = command_parts[1]
        dst = command_parts[2]
        try:
            subprocess.check_output(['cp', src, dst], universal_newlines=True)
            return f"'{src}' скопирован в '{dst}'."
        except Exception as e:
            return f"Ошибка при копировании '{src}': {e}"

    elif cmd == 'cat' and len(command_parts) > 1:
        filename = command_parts[1]
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Ошибка при чтении файла '{filename}': {e}"

    elif cmd == 'chmod' and len(command_parts) > 2:
        mode = command_parts[1]
        filename = command_parts[2]
        try:
            os.chmod(filename, int(mode, 8))
            return f"Права доступа файла '{filename}' изменены на {mode}."
        except Exception as e:
            return f"Ошибка при изменении прав доступа к файлу '{filename}': {e}"

    elif cmd == 'chown' and len(command_parts) > 2:
        user_group = command_parts[1]
        filename = command_parts[2]
        try:
            subprocess.check_output(['chown', user_group, filename], universal_newlines=True)
            return f"Владелец файла '{filename}' изменен на {user_group}."
        except Exception as e:
            return f"Ошибка при изменении владельца файла '{filename}': {e}"

    else:
        return f"Неизвестная команда: {command}. Введите 'help' для списка доступных команд."
