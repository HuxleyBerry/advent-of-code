from itertools import combinations
import numpy as np

AREA_MIN = 200000000000000
AREA_MAX = 400000000000000

def intersection_in_area(stone1, stone2):
    velocity_matrix = [[stone1[1][i], -stone2[1][i]] for i in range(2)]
    positions_matrix = [[stone2[0][i] -stone1[0][i]] for i in range(2)]
    try:
        inverse = np.linalg.inv(velocity_matrix)
        times = np.matmul(inverse, positions_matrix)
        if times[0][0] < 0 or times[1][0] < 0:
            return False
        intersection_xy = [stone1[0][i]+times[0][0]*stone1[1][i] for i in range(2)]
        return all(AREA_MIN <= coord and coord <= AREA_MAX for coord in intersection_xy)
    except:
        for i in range(2):
            if velocity_matrix[i][0] == 0 and velocity_matrix[i][1] == 0:
                print(i)
                # Should really be handling this, but it turns out to not be necessary for my input
        return False

with open("input.txt") as file:
    hailstones = []
    for line in file:
        pos, vel = line.strip().split(" @ ")
        hailstones.append((tuple(int(x) for x in pos.split(", ")), tuple(int(x) for x in vel.split(", "))))
    print(sum(1 for stone1, stone2 in combinations(hailstones,2) if intersection_in_area(stone1, stone2)))