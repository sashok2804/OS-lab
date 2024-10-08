# graph_drawer.py
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Глобальная переменная для хранения текущего графика
current_canvas = None

def draw_graph(t1, t2, x1, x3, window):
    global current_canvas

    # Если есть предыдущий график, уничтожаем его
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

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
    current_canvas = FigureCanvasTkAgg(fig, master=window)
    current_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    current_canvas.draw()
