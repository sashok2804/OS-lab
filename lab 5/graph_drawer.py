import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_graph(t1, t2, x1, x3, window):
    # Очищаем все виджеты перед отрисовкой нового графика
    for widget in window.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    G = nx.DiGraph()

    # Добавляем рёбра графа: зависимости транзакций и ресурсов
    if t1.waiting_for:
        G.add_edge(t1.name, t1.waiting_for.name)
    if t2.waiting_for:
        G.add_edge(t2.name, t2.waiting_for.name)
    
    if x1.locked_by:
        G.add_edge(x1.name, x1.locked_by.name)
    if x3.locked_by:
        G.add_edge(x3.name, x3.locked_by.name)

    pos = nx.circular_layout(G)  # Используем circular layout для компактности

    fig, ax = plt.subplots(figsize=(4, 4))
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold')

    # Встраиваем график в окно tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    canvas.draw()
