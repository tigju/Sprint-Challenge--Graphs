from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# get the map adjecency list
map_traversal = {}

# get the rooms' ids player will go through
rooms_path = []

# helper method to reverse directions
def reverse_direction(direction):
    reverse_mapping = {"n": "s", "s": "n", "w": "e", "e": "w"}
    return reverse_mapping[direction]

# helper to add the room to map_traversal
def add_room(room):
    if room.id not in map_traversal:
        map_traversal[room.id] = {}
        for d in room.get_exits():
            map_traversal[room.id][d] = None

# add direct relationship between rooms
def add_exits(from_room, to_room, direction):
    add_room(from_room)
    add_room(to_room)
    map_traversal[from_room.id][direction] = to_room.id
    map_traversal[to_room.id][reverse_direction(direction)] = from_room.id

# get the random exit with unexplored room
def random_exit(current_room):
    available_exits = []
    for ex in current_room.get_exits():
        if map_traversal[current_room.id][ex] == None:
            available_exits.append(ex)

    if len(available_exits) < 1:
        result = None
    else:
        result = random.choice(available_exits)
    return result




# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
