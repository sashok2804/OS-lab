import os
import time
import random
from multiprocessing import Process, Value
from threading import Thread, Event

def discharge_battery_thread(battery_level, stop_flag):
    """Функция разряда батареи в одном потоке"""
    while not stop_flag.is_set() and battery_level.value > 0:
        time.sleep(random.uniform(0.1, 0.5))
        with battery_level.get_lock():
            battery_level.value = max(0, battery_level.value - 0.1)
        print(f"Discharging... Battery level: {battery_level.value:.1f}%")

def discharge_battery_process(battery_level, priority):
    """Процесс с двумя потоками для разряда батареи"""
    os.nice(priority)  # Установка приоритета процесса
    stop_flag = Event()

    # Два потока для разряда батареи
    thread1 = Thread(target=discharge_battery_thread, args=(battery_level, stop_flag))
    thread2 = Thread(target=discharge_battery_thread, args=(battery_level, stop_flag))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

def charge_battery_thread(battery_level, stop_flag):
    """Функция зарядки батареи в одном потоке"""
    while not stop_flag.is_set() and battery_level.value < 100:
        time.sleep(random.uniform(0.1, 0.5))
        with battery_level.get_lock():
            battery_level.value = min(100, battery_level.value + 0.1)
        print(f"Charging... Battery level: {battery_level.value:.1f}%")

def charge_battery_process(battery_level, priority):
    """Процесс с одним потоком для зарядки батареи"""
    os.nice(priority)  # Установка приоритета процесса
    stop_flag = Event()

    # Один поток для зарядки
    thread = Thread(target=charge_battery_thread, args=(battery_level, stop_flag))
    thread.start()

    thread.join()
