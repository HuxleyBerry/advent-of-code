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
        current = (x1, y1)
        vector = (x2 - x1, y2 - y1)
        while in_bounds(current):
            antinode_locations.add(current)
            current = (current[0] + vector[0], current[1] + vector[1])

print(len(antinode_locations))
"""for i in range(height):
    s = ""
    for j in range(width):
        s += ("#" if (i,j) in antinode_locations else ".")
    print(s)"""