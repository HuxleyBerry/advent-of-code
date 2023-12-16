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

with open("input.txt") as file:
    grid = [line.strip() for line in file]
    beam_directions = [[[] for char in line] for line in grid]
    beam_directions[0][0].append((1,0))
    current_positions = [((0,0),(1,0))]
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
        #print(current_positions)
    total = 0
    for line in beam_directions:
        s = ""
        for cell in line:
            if len(cell) != 0:
                s += "#"
                total += 1
            else:
                s += "."
        #print(s)
    print(total)