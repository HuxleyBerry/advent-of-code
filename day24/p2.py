import numpy as np

def find_intersection(stone1, stone2, xyonly):
    velocity_matrix = [[stone1[1][i], -stone2[1][i]] for i in range(2)]
    positions_matrix = [[stone2[0][i] -stone1[0][i]] for i in range(2)]
    try:
        inverse = np.linalg.inv(velocity_matrix)
        times = np.matmul(inverse, positions_matrix)
        if times[0][0] < 0 or times[1][0] < 0:
            return False
        if not xyonly and stone1[0][2] + times[0][0]*stone1[1][2] != stone2[0][2] + times[1][0]*stone2[1][2]:
            return False
        intersection = [int(stone1[0][i]+times[0][0]*stone1[1][i]) for i in range(2 if xyonly else 3)]
        return intersection
    except:
        return "maybe"
    
def check_for_all_intersecting(stones, offset, xyonly):
    global_intersection = None
    i = 0
    required_iterations = 3
    while i < required_iterations:
        stone1 = (stones[i][0], tuple(stones[i][1][j] - offset[j] for j in range(3)))
        stone2 = (stones[i+1][0], tuple(stones[i+1][1][j] - offset[j] for j in range(3)))
        intersection = find_intersection(stone1, stone2, xyonly)
        if intersection == False:
            return False
        elif intersection == "maybe":
            required_iterations += 1
        else:
            if global_intersection == None or intersection == global_intersection:
                global_intersection = intersection
            elif intersection != global_intersection:
                return False
        i += 1
    return global_intersection

def search_for_small_offsets(stones, coord_min, coord_max):
    xy_intersections = []
    for i in range(coord_min,coord_max):
        for j in range(coord_min,coord_max):
            if check_for_all_intersecting(stones, (i,j,0), True):
                xy_intersections.append((i,j))
    for i,j in xy_intersections:
        for k in range(coord_min,coord_max):
            intersection = check_for_all_intersecting(stones, (i,j,k), False)
            if intersection:
                return sum(intersection)


with open("input.txt") as file:
    hailstones = []
    for line in file:
        pos, vel = line.strip().split(" @ ")
        hailstones.append((tuple(int(x) for x in pos.split(", ")), tuple(int(x) for x in vel.split(", "))))
    
    print(search_for_small_offsets(hailstones, -300,300))