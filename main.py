import json
import networkx as nx
from PIL import Image, ImageDraw
import floor_maps

with open('buildings_data.json', 'r') as f:
    data = json.load(f)

floor_maps = floor_maps.floor_maps

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


start_room = "Room_145"
end_room = "Stairs_1_2"
shortest_path = nx.shortest_path(G, source=start_room, target=end_room)


def draw_path_segment(draw, segment, color="green", width=5):
    for i in range(len(segment) - 1):
        room_start = segment[i]
        room_end = segment[i + 1]
        coords_start = G.nodes[room_start]['coords']
        coords_end = G.nodes[room_end]['coords']
        draw.line([coords_start, coords_end], fill=color, width=width)


segments = {}
for key_point in shortest_path:
    room_data = G.nodes[key_point]
    if 'floor' in room_data:
        floor = room_data['floor']
        if floor not in segments:
            segments[floor] = []
        segments[floor].append(key_point)
    else:
        print(f"Can't determine the floor for room: {key_point}")


for floor, segment in segments.items():
    map_file = floor_maps.get('IRIT_RTF', {}).get(floor)
    # map_file = floor_maps.get(floor)
    print(floor_maps)
    if map_file:
        img = Image.open(map_file)
        draw = ImageDraw.Draw(img)
        draw_path_segment(draw, segment)
        img.save(f"result_{floor}.png")
        img.show()
    else:
        print(f"No map for floor: {floor}")