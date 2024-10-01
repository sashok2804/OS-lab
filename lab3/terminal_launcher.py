import subprocess

def open_terminal():
    try:
        subprocess.Popen("start cmd", shell=True)  # Для Windows
        print("Терминал запущен.")
    except Exception as e:
        print(f"Ошибка при запуске терминала: {e}")
