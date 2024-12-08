from collections import defaultdict
from itertools import permutations

height = 0
width = None
locations = defaultdict(set)
with open("input.txt") as file:
    for i, line in enumerate(file.readlines()):
        height += 1
        if i == 0:
            width = len(line.strip())
        for j, val in enumerate(line.strip()):
            if val != ".":
                locations[val].add((i,j))

def in_bounds(loc):
    global width, height
    x, y = loc
    return 0 <= x and x < width and 0 <= y and y < height

antinode_locations = set()
for freq in locations:
    for (x1, y1), (x2, y2) in permutations(locations[freq],2):
        candidate = (2*x2 - x1, 2*y2 - y1)
        if in_bounds(candidate):
            antinode_locations.add(candidate)

print(len(antinode_locations))