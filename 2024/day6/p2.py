with open("input.txt") as file:
    grid = [l.strip() for l in file.readlines()]

width = len(grid[0])
height = len(grid)
obstacle_locations = set()
guard_pos = None
guard_orientation = (0,-1)
for i, row in enumerate(grid):
    for j, cell in enumerate(row):
        if cell == "#":
            obstacle_locations.add((j,i))
        elif cell == "^":
            guard_pos = (j,i)
assert guard_pos is not None
possible_new_obstacle_locations = set()

def loc_in_bounds(loc):
    global width, height
    x, y = loc
    return 0 <= x and x < width and 0 <= y and y < height

pos = (guard_pos[0], guard_pos[1])
while True:
    ahead_pos = (pos[0] + guard_orientation[0], pos[1] + guard_orientation[1])
    if not loc_in_bounds(ahead_pos):
        break
    elif ahead_pos in obstacle_locations:
        guard_orientation = (-guard_orientation[1], guard_orientation[0])
    else:
        pos = ahead_pos
        possible_new_obstacle_locations.add(ahead_pos)

total = 0
for i, possible_location in enumerate(possible_new_obstacle_locations):
    print(f"{(i+1)*100//len(possible_new_obstacle_locations)}% done")
    pos = (guard_pos[0], guard_pos[1])
    guard_orientation = (0,-1)
    visited = {(guard_pos, guard_orientation)}
    while True:
        ahead_pos = (pos[0] + guard_orientation[0], pos[1] + guard_orientation[1])
        if (ahead_pos, guard_orientation) in visited:
            total += 1
            break
        if not loc_in_bounds(ahead_pos):
            break
        elif ahead_pos in obstacle_locations or ahead_pos == possible_location:
            guard_orientation = (-guard_orientation[1], guard_orientation[0])
        else:
            pos = ahead_pos
            visited.add((ahead_pos, guard_orientation))

print(total)