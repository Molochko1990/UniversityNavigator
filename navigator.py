import json
import networkx as nx
from PIL import Image, ImageDraw
import floor_maps as fm


def build_path(start_room, end_room):

    with open('buildings_data.json', 'r') as f:
        data = json.load(f)

    floor_maps = fm.floor_maps

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

    def convert_roomto_json_format(room):
        rus_to_lat = {
            'р': 'Room', 'Р': 'Room',
            'гук': 'GUK', 'ГУК': 'GUK',
            'и': 'I', 'И': 'I',
            'э': 'E', 'Э': 'E',
        }
        parts = room.split("-")

        if parts[0] in rus_to_lat:
            parts[0] = rus_to_lat[parts[0]]
        if parts[1][0] == '0':
            parts[1] = parts[1][1:]
        return "_".join(parts)

    start_room = convert_roomto_json_format(start_room)
    end_room = convert_roomto_json_format(end_room)

    def identify_the_building(room):
        university_buildings = {
            'Room': 'IRIT_RTF',
            'GUK': 'GUK',
            'I': 'GUK'
        }
        parts = room.split("_")
        if parts[0] in university_buildings:
            university_building = university_buildings[parts[0]]
            return university_building

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

    generated_paths = []

    for floor, segment in segments.items():
        map_file = floor_maps.get(identify_the_building(start_room), {}).get(floor)
        if map_file:
            img = Image.open(map_file)
            draw = ImageDraw.Draw(img)
            draw_path_segment(draw, segment)
            path_filename = f"result_{floor}.png"
            img.save(path_filename)
            img.show()
            generated_paths.append(path_filename)
        else:
            print(f"No map for floor: {floor}")
    return generated_paths
try:
    build_path('Р-123', 'р-135')
except:
    print('asqweqwe')
