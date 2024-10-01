import subprocess

# Функция для получения информации о видеокарте
def get_gpu_info():
    try:
        gpu_info = subprocess.check_output("lspci -v | grep -i vga", shell=True).decode('utf-8')
        return gpu_info
    except Exception as e:
        return f"Error retrieving GPU info: {str(e)}"

# Функция для получения информации о подключенных мониторах
def get_monitor_info():
    try:
        monitor_info = subprocess.check_output("xrandr", shell=True).decode('utf-8')
        return monitor_info
    except Exception as e:
        return f"Error retrieving monitor info: {str(e)}"
