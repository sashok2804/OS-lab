import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Класс для ресурсов и транзакций
class Resource:
    def __init__(self, name):
        self.name = name
        self.locked_by = None

class Transaction:
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources
        self.waiting_for = None

# Функция для захвата ресурсов транзакциями
def acquire_resource(transaction, resource):
    if resource.locked_by is None:
        resource.locked_by = transaction
    else:
        transaction.waiting_for = resource.locked_by
        messagebox.showinfo("Внимание!", f"{transaction.name} ожидает {resource.name}, занятого {resource.locked_by.name}")

# Функция моделирования взаимоблокировки
def simulate_deadlock():
    # Сброс ресурсов
    for r in [x1, x3]:
        r.locked_by = None

    t1.waiting_for = None
    t2.waiting_for = None

    # T1 захватывает X1
    acquire_resource(t1, x1)
    # T2 захватывает X3
    acquire_resource(t2, x3)
    # T1 пытается захватить X3
    acquire_resource(t1, x3)
    # T2 пытается захватить X1
    acquire_resource(t2, x1)

    draw_graph()

    # Проверка на взаимоблокировку
    if t1.waiting_for == t2 and t2.waiting_for == t1:
        messagebox.showwarning("Взаимоблокировка!", "Произошла взаимоблокировка! T1 и T2 ждут друг друга.")

# Функция выхода из взаимоблокировки
def resolve_deadlock():
    # Прерывание T1 для выхода из взаимоблокировки
    t1.waiting_for = None
    x1.locked_by = None
    x3.locked_by = None
    messagebox.showinfo("Решение", "T1 была прервана для выхода из взаимоблокировки.")
    draw_graph()

# Функция отрисовки графа
def draw_graph():
    G = nx.DiGraph()

    if t1.waiting_for:
        G.add_edge(t1.name, t1.waiting_for.name)
    if t2.waiting_for:
        G.add_edge(t2.name, t2.waiting_for.name)
    
    if x1.locked_by:
        G.add_edge(x1.name, x1.locked_by.name)
    if x3.locked_by:
        G.add_edge(x3.name, x3.locked_by.name)

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(4, 4))
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold')
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

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
simulate_button = tk.Button(window, text="Смоделировать взаимоблокировку", command=simulate_deadlock)
simulate_button.pack(pady=10)

resolve_button = tk.Button(window, text="Решить взаимоблокировку", command=resolve_deadlock)
resolve_button.pack(pady=10)

exit_button = tk.Button(window, text="Выход", command=window.quit)
exit_button.pack(pady=10)

# Запуск приложения
window.mainloop()
