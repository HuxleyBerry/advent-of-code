splitter_outs = {"|": [(0,1),(0,-1)], "-": [(1,0),(-1,0)]}

def in_bounds(grid, x, y):
    return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)

def step_beam(grid, x, y, direction):
    if grid[y][x] == ".":
        out_directions = [direction]
    elif grid[y][x] == "/":
        out_directions = [(-direction[1], -direction[0])]
    elif grid[y][x] == "\\":
        out_directions = [(direction[1], direction[0])]
    elif grid[y][x] in ("-", "|"):
        if direction in splitter_outs[grid[y][x]]:
            out_directions = [direction]
        else:
            out_directions = splitter_outs[grid[y][x]]
    results = [((x+out[0], y+out[1]), out) for out in out_directions if in_bounds(grid, x+out[0], y+out[1])]
    return results

def find_energised_count(grid, start_x, start_y, start_direction):
    beam_directions = [[[] for char in line] for line in grid]
    beam_directions[start_y][start_x].append((start_direction))
    current_positions = [((start_x, start_y), start_direction)]
    while len(current_positions) != 0:
        stepped_positions = []
        new_positions = []
        for (x, y), direction in current_positions:
            stepped_positions += step_beam(grid, x, y, direction)
        for (x, y), direction in stepped_positions:
            if direction not in beam_directions[y][x]:
                beam_directions[y][x].append(direction)
                new_positions.append(((x, y), direction))
        current_positions = new_positions
    total = 0
    for line in beam_directions:
        for cell in line:
            if len(cell) != 0:
                total += 1
    return total


with open("input.txt") as file:
    grid = [line.strip() for line in file]
    width = len(grid[0])
    height = len(grid)
    max = 0
    for x in (0, width-1):
        for y in range(height):
            energised = find_energised_count(grid, x, y, (1,0) if x == 0 else (-1,0))
            if energised > max:
                max = energised
    for y in (0, height-1):
        for x in range(width):
            energised = find_energised_count(grid, x, y, (0,1) if y == 0 else (0,-1))
            if energised > max:
                max = energised
    print(max)