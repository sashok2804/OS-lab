# graph_drawer.py
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Глобальная переменная для хранения текущего графика
current_canvas = None

def draw_graph(t1, t2, x1, x3, window):
    global current_canvas

    # Удаляем предыдущий график, если он есть
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    G = nx.DiGraph()

    # Добавляем зависимости транзакций и ресурсов
    if t1 and t1.waiting_for:  # Добавляем ребро, только если T1 существует и что-то ожидает
        G.add_edge(t1.name, t1.waiting_for.name)
    if t2 and t2.waiting_for:  # Добавляем ребро, если T2 ожидает что-то
        G.add_edge(t2.name, t2.waiting_for.name)
    
    # Если ресурсы заблокированы транзакциями, добавляем рёбра от ресурсов к транзакциям
    if x1.locked_by:
        G.add_edge(x1.name, x1.locked_by.name)
    if x3.locked_by:
        G.add_edge(x3.name, x3.locked_by.name)

    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(4, 4))
    nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold')

    # Отображаем график в окне tkinter
    current_canvas = FigureCanvasTkAgg(fig, master=window)
    current_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    current_canvas.draw()

