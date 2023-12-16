E, W, N, S = (1, 0), (-1,0), (0,-1), (0,1)
directions_dict = {"|": [N, S], "-": [E, W], "L": [N, E], "J": [N, W], "7": [S, W], "F": [S, E], ".": [], "S": [N,S,E,W]}

def get_pipe_neighbours(lines, x, y, width, height):
    pipe_type = lines[y][x]
    directions = directions_dict[pipe_type]
    return ((x+i, y+j) for i,j in directions if x+i >= 0 and x+i < width and y+j >= 0 and y+j < height)

def find_and_return_index(list, item):
    for i, it in enumerate(list):
        if it == item:
            return i
    return -1

with open("input.txt") as file:
    lines = file.readlines()
    start_found = False
    width = len(lines[0]) - 1
    height = len(lines)
    for i, line in enumerate(lines):
        if start_found:
            break
        for j, char in enumerate(line):
            if char == "S":
                start_loc = (j, i)
                start_found = True
    previous = -1, -1
    started = False
    current_loc = start_loc
    loop = []
    while not started or current_loc != start_loc:
        started = True
        for x, y in get_pipe_neighbours(lines, current_loc[0], current_loc[1], width, height):
            if (x, y) != previous: # prevent backtracking
                if not (current_loc == start_loc) or current_loc in get_pipe_neighbours(lines, x, y, width, height):
                    previous = current_loc
                    current_loc = x, y
                    break
        loop.append((current_loc))
    interior_count = 0
    for i, line in enumerate(lines):
        current_pipe = -1, -1
        current_direction = -1
        for j, char in enumerate(line.strip()):
            index = find_and_return_index(loop, (j, i))
            if index != -1: # examining a tile in the loop 
                current_pipe = (j, i)
                successor = loop[(index+1)%len(loop)]
                predecessor = loop[(index-1)%len(loop)]
                if predecessor[1] < current_pipe[1] or current_pipe[1] < successor[1]:
                    current_direction = "down"
                elif predecessor[1] > current_pipe[1] or current_pipe[1] > successor[1]:
                    current_direction = "up"
            else:
                if current_direction == "up":
                    interior_count += 1
    print(interior_count)