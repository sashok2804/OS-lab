import time
from threading import Thread, Event
from multiprocessing import Process

# Пример функции для запуска и остановки потоков и процессов.
def start_thread(name, stop_flag, target_func):
    thread = Thread(target=target_func, args=(name, stop_flag))
    thread.start()
    return thread

def stop_thread(name, threads, thread_stop_flags):
    if name in threads:
        thread_stop_flags[name].set()
        threads[name].join()
        del threads[name]
        del thread_stop_flags[name]

# Аналогичные функции для процессов
def start_process(name, target_func):
    process = Process(target=target_func, args=(name,))
    process.start()
    return process

def stop_process(pid, processes):
    if pid in processes:
        processes[pid].terminate()
        del processes[pid]
