ELF_STEPS = 26501365

def step(grid, start_x, start_y, dimension):
    visited = {}
    queue = [(start_x, start_y, 0)]
    new_location_reached = True
    while len(queue) != 0 and new_location_reached:
        x, y, depth = queue.pop(0)
        for x2, y2 in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if is_garden(x2, y2, grid, dimension) and (x2, y2) not in visited:
                visited[(x2, y2)] = depth+1
                queue.append((x2, y2, depth+1))
    return visited

def is_garden(x, y, grid, dimension):
    return abs(x//dimension) <= 1 and abs(y//dimension) <= 1 and grid[y%dimension][x%dimension] in (".", "S")

def maps_at_distance(d):
    return d if d > 0 else 1

def maps_at_or_below_distance(d):
    odd_rings, even_rings = 1+ (d-1)//2, 1 + d//2
    return (2*odd_rings)**2, (2*even_rings - 1)**2

def count_achievable_cells_in_maps_of_distance(d, distance_0, distance_1, distance_2, steps, dimension):
    if d >= 2:
        achieved = 0
        steps_to_diagonal_inner_maps = dimension*(d-2)
        achieved += sum(1 for k,v in distance_2.items() if v <= (steps-steps_to_diagonal_inner_maps) and (k[0]+k[1]+d)%2 == steps%2)*(d-1)
        steps_to_adjacent_inner_maps = dimension*(d-1)
        achieved += sum(1 for k,v in distance_1.items() if v <= (steps-steps_to_adjacent_inner_maps) and (k[0]+k[1]+d)%2 == (steps+1)%2)
        return achieved
    elif d == 1:
        return sum(1 for k,v in distance_1.items() if v <= steps and (k[0]+k[1])%2 == steps%2)
    elif d == 0:
        return sum(1 for k,v in distance_0.items() if v <= steps and (k[0]+k[1])%2 == steps%2)
    

with open("input.txt") as file:
    grid = [l.strip() for l in file]
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start_x, start_y = j, i
                break
    dimension = len(grid)
    # the following will hold the distance to all the cells (with correct parity) that reside in the 
    # 3x3 of maps centered at the start
    distances = step(grid, start_x, start_y, dimension)
    distance_0, distance_1, distance_2 = {}, {}, {}
    for (x,y), d in distances.items():
        map_dist = abs(x//dimension) + abs(y//dimension)
        if map_dist == 2:
            distance_2[(x,y)] = d
        elif map_dist == 1:
            distance_1[(x,y)] = d
        else:
            distance_0[(x,y)] = d
    max_dist = max(max(v for k, v in distance_2.items()), max(v for k, v in distance_1.items()))
    quot, surplus = divmod(ELF_STEPS, dimension)
    total = 0
    map_dist = quot+1
    while map_dist >= 0:
        if surplus >= max_dist:
            # This means that there are enough moves to reach every reachable cell of the maps of the current distance (map_dist)
            # So we don't need to loop through distances and see which cells are sufficiently close, since we know they all are
            # Furthermore, this will also apply for all map distances lower than this
            odd_maps_count, even_maps_count = maps_at_or_below_distance(map_dist)
            cells_of_even_parity_count = sum(1 for k in distance_0 if (k[0]+k[1])%2 == 0)
            cells_of_odd_parity_count = sum(1 for k in distance_0 if (k[0]+k[1])%2 == 1)
            if ELF_STEPS%2 == 0:
                total += even_maps_count*cells_of_even_parity_count + odd_maps_count*cells_of_odd_parity_count
            else:
                total += odd_maps_count*cells_of_even_parity_count + even_maps_count*cells_of_odd_parity_count
            break
        else:
            total += count_achievable_cells_in_maps_of_distance(map_dist, distance_0, distance_1, distance_2, ELF_STEPS, dimension)
            map_dist -= 1
            surplus += dimension
    print(total)