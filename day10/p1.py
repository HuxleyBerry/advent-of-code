E, W, N, S = (1, 0), (-1,0), (0,-1), (0,1)
directions_dict = {"|": [N, S], "-": [E, W], "L": [N, E], "J": [N, W], "7": [S, W], "F": [S, E], ".": [], "S": [N,S,E,W]}

def get_pipe_neighbours(lines, x, y, width, height):
    pipe_type = lines[y][x]
    directions = directions_dict[pipe_type]
    return ((x+i, y+j) for i,j in directions if x+i >= 0 and x+i < width and y+j >= 0 and y+j < height)

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
    count = 0
    while not started or current_loc != start_loc:
        started = True
        for x, y in get_pipe_neighbours(lines, current_loc[0], current_loc[1], width, height):
            if (x, y) != previous: # prevent backtracking
                if not (current_loc == start_loc) or current_loc in get_pipe_neighbours(lines, x, y, width, height):
                    previous = current_loc
                    current_loc = x, y
                    break
        count += 1
    print(count//2)