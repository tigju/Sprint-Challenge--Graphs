from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

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

# breadth first traversal gets the backtrack path, when there is no more depth in graph to explore
def breadth_first(curr_room):
    queue = deque()
    player.current_room = curr_room
    queue.append([player.current_room])
    visited = set()
    while len(queue) > 0:
        path = queue.popleft()
        # print([r.id for r in path])
        room = path[-1]
        # print(path)
        if room not in visited:
            if list(map_traversal[room.id].values()).count(None) != 0:
                # get_rooms = [p.id for p in path[1:]]
                # rooms_path.append(get_rooms)

                # get the rooms path
                [rooms_path.append(p.id) for p in path[1:]]

                return path[1:]
            # add to visited
            visited.add(room)

            # go through the remaining exits and append to queue
            for n in room.get_exits():
                queue.append(path + [room.get_room_in_direction(n)])


# depth first traversal visits all exits with unexplored rooms until reaches dead end
def depth_first(player_in_current_room):

    stack = deque()
    stack.append(player_in_current_room)

    while len(stack) > 0:
        # pop the current room from stack
        curRoom = stack.pop()
        # add the room id in rooms_path
        rooms_path.append(curRoom.id)

        # if curRoom is not None:
        # check if current room not in map_traversal, if not we add room
        if curRoom.id not in map_traversal:
            add_room(curRoom)

        # get random exit from unvisited in current room
        random_ex = random_exit(curRoom)
        # # print(random_ex)
        # random_exit method returns none if there are no unvisited rooms
        # so we check if there are some unvisited we add it to map_traversal
        if random_ex != None:
            if map_traversal[curRoom.id][random_ex] == None:
                # add rooms with exits to map_traversal. add_exits makes directed connection between the rooms
                add_exits(curRoom, curRoom.get_room_in_direction(
                    random_ex), random_ex)
                # add the next room to stack
                stack.append(curRoom.get_room_in_direction(random_ex))
        # if there are no unvisited rooms:
        else:
            # do the breadth first traversal if there is no unexplored exit in current room
            path = breadth_first(curRoom)
            # when done breadth first traversal and path is not none, return the room we are back
            if path is not None:
                # get the room we are back from breadth traversal
                curRoom = path[-1]
                # print(curRoom.id)
                # get the random exit from unvisited
                ran = random_exit(curRoom)
                # if there are some unexplored exits, add them to map_traversal
                if ran != None:
                    if map_traversal[curRoom.id][ran] == None:
                        # add rooms with exits to map_traversal. add_exits makes directed connection between the rooms
                        add_exits(
                            curRoom, curRoom.get_room_in_direction(ran), ran)
                        # add the next room to stack
                        stack.append(curRoom.get_room_in_direction(ran))



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
