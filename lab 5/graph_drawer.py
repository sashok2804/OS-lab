import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox  # Добавляем импорт для messagebox

# Глобальная переменная для хранения текущего графика
current_canvas = None

def draw_graph(t1, t2, x1, x3, window):
    global current_canvas

    # Удаляем предыдущий график, если он есть
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    G = nx.DiGraph()

    # Добавляем зависимости транзакций и ресурсов
    if t1 and hasattr(t1, 'waiting_for') and t1.waiting_for:  # Добавляем проверку на наличие атрибута
        G.add_edge(t1.name, t1.waiting_for.name)
    if t2 and hasattr(t2, 'waiting_for') and t2.waiting_for:  # Добавляем проверку на наличие атрибута
        G.add_edge(t2.name, t2.waiting_for.name)
    
    # Если ресурсы заблокированы транзакциями, добавляем рёбра от ресурсов к транзакциям
    if x1 and hasattr(x1, 'locked_by') and x1.locked_by:  # Добавляем проверку на наличие атрибута
        G.add_edge(x1.name, x1.locked_by.name)
    if x3 and hasattr(x3, 'locked_by') and x3.locked_by:  # Добавляем проверку на наличие атрибута
        G.add_edge(x3.name, x3.locked_by.name)
    
    # Если ресурсы ожидаются транзакциями
    if t1 and hasattr(t1, 'resources') and t1.resources:  # Добавляем проверку на наличие атрибута
        for res in t1.resources:
            if res.locked_by == t1:
                G.add_edge(t1.name, res.name)
    if t2 and hasattr(t2, 'resources') and t2.resources:  # Добавляем проверку на наличие атрибута
        for res in t2.resources:
            if res.locked_by == t2:
                G.add_edge(t2.name, res.name)

    if not G.nodes:
        messagebox.showinfo("Граф пуст", "Нет активных зависимостей для отображения.")
        return

    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(4, 4))
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold')

    # Отображаем график в окне tkinter
    current_canvas = FigureCanvasTkAgg(fig, master=window)
    current_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    current_canvas.draw()

    plt.close(fig)  # Закрываем фигуру для предотвращения утечек памяти
