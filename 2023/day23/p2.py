def search(grid, start, end):
    path_lengths = []
    stack = [(start, 0, set())]
    network = make_network(grid)
    while len(stack) != 0:
        pos, current_length, visited = stack.pop()
        for neighbour, dist in network[(pos)]:
            if neighbour == end:
                path_lengths.append(current_length+dist)
            elif neighbour not in visited:
                visited_copy = visited.copy()
                visited_copy.add(neighbour)
                stack.append((neighbour, current_length+dist, visited_copy))
    return path_lengths

def get_neighbours(grid, x,y):
    unfiltered = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return [(x2, y2) for x2, y2 in unfiltered if 0 <= x2 and 0 <= y2 and x2 < len(grid[0]) and y2 < len(grid) and grid[y2][x2] != "#"]

def make_network(grid):
    network = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(grid):
            if grid[y][x] != "#":
                network[(x,y)] = [(n,1) for n in get_neighbours(grid, x, y)]
    del_list = []
    for (x,y), neighbour_list in network.items():
        if len(neighbour_list) == 2:
            half_distances = []
            new_neighbour_lists = [[],[]]
            for i, (n, dist) in enumerate(neighbour_list):
                for n2, dist2 in network[n]:
                    if n2 != (x,y):
                        new_neighbour_lists[i].append((n2, dist2))
                    else:
                        half_distances.append(dist2)
            full_distance = sum(half_distances)
            new_neighbour_lists[0].append((neighbour_list[1][0], full_distance))
            new_neighbour_lists[1].append((neighbour_list[0][0], full_distance))
            for i in range(2):
                network[neighbour_list[i][0]] = new_neighbour_lists[i]
            del_list.append((x,y))
    for key in del_list:
        del network[key]
    return network

with open("input.txt") as file:
    grid = [l.strip() for l in file]
    start = (grid[0].index("."),0)
    end = (grid[-1].index("."),len(grid)-1)
    print(max(search(grid, start, end)))