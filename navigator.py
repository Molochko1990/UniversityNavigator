import json
import networkx as nx
from PIL import Image, ImageDraw
import floor_maps as fm


def build_path(start_room, end_room):
    try:
        with open('buildings_data.json', 'r') as f:
            data = json.load(f)

        floor_maps = fm.floor_maps

        G = nx.Graph()

        # Creating a graph from coordinates obtained from a JSON file.
        def add_rooms_and_connections(floors_data, floor):
            for room, attributes in floors_data[floor].items():
                coords = tuple(attributes['coords'])
                G.add_node(room, coords=coords, floor=floor)
                for conn in attributes['connections']:
                    G.add_edge(room, conn, weight=1)

        for building_name, floors_data in data.items():
            for floor in floors_data:
                add_rooms_and_connections(floors_data, floor)

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

        # ['Room_01', 'C_01', ... 'C_0_1_stairs', 'Stairs_0_1', 'Stairs_1_1', 'C_1_1_stairs', 'C_127', 'Room_127']
        if start_room not in G.nodes:
            return f"Начальный кабинет {start_room} указан неверно."
        elif end_room not in G.nodes:
            return f"Конечный кабинет {end_room} указан неверно."
        else:
            shortest_path = nx.shortest_path(G, source=start_room, target=end_room)

        # Drawing the route line on the image. 'draw' is an object from the Pillow library used for drawing the route.
        # 'segment' is a list of points in the corridor.
        # coords_start This variable stores the coordinates of the points through which the line will pass.
        def draw_path_segment(draw, segment, color="green", width=5):
            for i in range(len(segment) - 1):
                room_start = segment[i]
                room_end = segment[i + 1]
                coords_start = G.nodes[room_start]['coords']
                coords_end = G.nodes[room_end]['coords']
                draw.line([coords_start, coords_end], fill=color, width=width)

        # {'Floor_0': ['Room_01', 'C_01', 'C_02', 'C_03', 'C_23', 'C_27', 'C_0_1_stairs', 'Stairs_0_1'], 'Floor_1': ....
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

        # paths to .png images
        generated_paths = []

        for floor, segment in segments.items():
            # This variable stores the path to the image of the floor plan
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
    except nx.exception.NodeNotFound:
        return 'Кажется одного из этих кабинетов нет, проверьте правильность'
# build_path('Room-322', 'Room-125')