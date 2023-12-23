from collections import defaultdict

def get_brick_height(brick):
    return 1 + abs(brick[0][2] - brick[1][2])

def get_cube_xy_positions(brick):
    mins = [min(brick[0][i], brick[1][i]) for i in range(2)]
    maxes = [max(brick[0][i], brick[1][i]) for i in range(2)]
    return {(x,y) for x in range(mins[0], maxes[0]+1) for y in range(mins[1], maxes[1]+1)}

def find_supporting(bricks):
    supported_by = [set() for brick in bricks]
    heights = defaultdict(int)
    peak_owner = defaultdict(int)
    for i, brick in enumerate(bricks):
        cube_positions = get_cube_xy_positions(brick)
        max_height_below_brick = max(heights[(x,y)] for (x,y) in cube_positions)
        for pos in cube_positions:
            if heights[pos] == max_height_below_brick and max_height_below_brick != 0: # there must be a supporting block below
                supported_by[i].add(peak_owner[pos])
            heights[pos] = max_height_below_brick+get_brick_height(brick)
            peak_owner[pos] = i
    return supported_by

def find_fall_count(bricks):
    supported_by = find_supporting(bricks)
    total = 0
    for i in range(len(bricks)):
        fallen = {i}
        for j in range(i+1, len(bricks)):
            j_supporters = supported_by[j].difference(fallen)
            if len(j_supporters) == 0 and len(supported_by[j]) != 0:
                fallen.add(j)
        total += len(fallen) - 1
    return total

with open("input.txt") as file:
    bricks = [tuple(tuple(int(s) for s in h.split(",")) for h in line.strip().split("~")) for line in file]
    bricks.sort(key=lambda x: min(x[0][2], x[1][2]))
    print(find_fall_count(bricks))