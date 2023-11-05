import json
import networkx as nx
from PIL import Image, ImageDraw

with open('path_to_your_file.json', 'r') as f:
    data = json.load(f)

G = nx.Graph()

# все ключевые точки
key_points = ["P-113", "P-114", "P-115", "P-1-1"]  # в формате P-113 будут написаны кабинеты, в формате P_1_1 точки в коридорах
for key_point in key_points:
    G.add_node(key_point)
# связь между всеми точками
#
connections = [("P-113", "P-1-1"), ("P-1-1", "P-1-2"), ("P-1-2", "P-115"), ("P-1-2", "P-114")]
for connection in connections:
    G.add_edge(connection[0], connection[1], weight=1)
#Поиск пути
start_room = "P-114"
end_room = "P-115"
shortest_path = nx.shortest_path(G, source=start_room, target=end_room, weight="weight")
# визуализация пути на карте
img = Image.open("0 FLOOR.png")
draw = ImageDraw.Draw(img)
# Координаты каждого кабинета, коридора, лестницы и тд
coordinates_rtf_1 = {
    "P-113": (210, 160),
    "P-114": (150, 150),
    "P-115": (250, 250),
    "P-1-1": (230, 160),
    "P-1-2": (230, 180)
}
# рисуем линию
for i in range(len(shortest_path) - 1):
    draw.line([coordinates_rtf_1[shortest_path[i]], coordinates_rtf_1[shortest_path[i+1]]], fill="red", width=5)

img.show()
img.save("result.png")
