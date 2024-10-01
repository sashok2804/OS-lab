import subprocess

# Функция для получения информации о видеокарте
def get_gpu_info():
    try:
        gpu_info = subprocess.check_output("lspci -v | grep -i vga", shell=True).decode('utf-8')
        return gpu_info
    except Exception as e:
        return f"Ошибка получения информации о видеокарте: {str(e)}"

# Функция для получения информации о подключённых мониторах
def get_monitor_info():
    try:
        # Используем xrandr для получения информации о мониторах
        monitor_info = subprocess.check_output("xrandr --listmonitors", shell=True).decode('utf-8')
        return monitor_info
    except Exception as e:
        return f"Ошибка получения информации о мониторах: {str(e)}"
