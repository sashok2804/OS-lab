# main.py
import tkinter as tk
from tkinter import messagebox
from resource import Resource
from transaction import Transaction
from graph_drawer import draw_graph

# Функция для захвата ресурсов транзакциями
def acquire_resource(transaction, resource, window):
    if resource.locked_by is None:
        resource.locked_by = transaction
    else:
        transaction.waiting_for = resource.locked_by
        messagebox.showinfo("Внимание!", f"{transaction.name} ожидает {resource.name}, занятого {resource.locked_by.name}")
    draw_graph(t1, t2, x1, x3, window)

# Функция моделирования взаимоблокировки
def simulate_deadlock(window):
    # Сброс ресурсов
    for r in [x1, x3]:
        r.locked_by = None

    t1.waiting_for = None
    t2.waiting_for = None

    # T1 захватывает X1
    acquire_resource(t1, x1, window)
    # T2 захватывает X3
    acquire_resource(t2, x3, window)
    # T1 пытается захватить X3
    acquire_resource(t1, x3, window)
    # T2 пытается захватить X1
    acquire_resource(t2, x1, window)

    # Проверка на взаимоблокировку
    if t1.waiting_for == t2 and t2.waiting_for == t1:
        messagebox.showwarning("Взаимоблокировка!", "Произошла взаимоблокировка! T1 и T2 ждут друг друга.")

# Функция выхода из взаимоблокировки
def resolve_deadlock(window):
    # Прерывание T1 для выхода из взаимоблокировки
    t1.waiting_for = None
    x1.locked_by = None
    x3.locked_by = None
    messagebox.showinfo("Решение", "T1 была прервана для выхода из взаимоблокировки.")
    draw_graph(t1, t2, x1, x3, window)

# Создание интерфейса
window = tk.Tk()
window.title("Моделирование взаимоблокировки")

# Ресурсы
x1 = Resource("X1")
x3 = Resource("X3")

# Транзакции
t1 = Transaction("T1", [x1, x3])
t2 = Transaction("T2", [x3, x1])

# Кнопки
simulate_button = tk.Button(window, text="Смоделировать взаимоблокировку", command=lambda: simulate_deadlock(window))
simulate_button.pack(pady=10)

resolve_button = tk.Button(window, text="Решить взаимоблокировку", command=lambda: resolve_deadlock(window))
resolve_button.pack(pady=10)

exit_button = tk.Button(window, text="Выход", command=window.quit)
exit_button.pack(pady=10)

# Запуск приложения
window.mainloop()
