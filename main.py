import json
import networkx as nx
from PIL import Image, ImageDraw

with open('buildings_data.json', 'r') as f:
    data = json.load(f)

floor_maps = {
    "Floor_0": "0 FLOOR.png",
    "Floor_1": "1 FLOOR.png",

}

G = nx.Graph()

def add_rooms_and_connections(building, floor):
    for room, attributes in building[floor].items():
        coords = tuple(attributes['coords'])
        G.add_node(room, coords=coords, floor=floor)
        for conn in attributes['connections']:
            G.add_edge(room, conn, weight=1)


for building_name, building_data in data.items():
    for floor in building_data:
        add_rooms_and_connections(building_data, floor)


start_room = "Room_01"
end_room = "Room_21"
shortest_path = nx.shortest_path(G, source=start_room, target=end_room)


def draw_path_segment(draw, segment, color="red", width=5):
    for i in range(len(segment) - 1):
        room_start = segment[i]
        room_end = segment[i + 1]
        coords_start = G.nodes[room_start]['coords']
        coords_end = G.nodes[room_end]['coords']
        draw.line([coords_start, coords_end], fill=color, width=width)


segments = {}
for room in shortest_path:
    room_data = G.nodes[room]
    if 'floor' in room_data:
        floor = room_data['floor']
        if floor not in segments:
            segments[floor] = []
        segments[floor].append(room)
    else:
        print(f"Can't determine the floor for room: {room}")


for floor, segment in segments.items():
    map_file = floor_maps.get(floor)
    if map_file:
        img = Image.open(map_file)
        draw = ImageDraw.Draw(img)
        draw_path_segment(draw, segment)
        img.save(f"result_{floor}.png")
        img.show()
    else:
        print(f"No map for floor: {floor}")