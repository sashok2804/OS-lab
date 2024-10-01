import subprocess

def open_terminal():
    try:
        # Запуск gnome-terminal в Linux
        subprocess.Popen(['gnome-terminal'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Терминал запущен.")
    except Exception as e:
        print(f"Ошибка при запуске терминала: {e}")
