def tilt(grid, direction, width, height):
    if direction == "N" or direction == "S":
        increment = 1 if direction == "N" else -1
        for col in range(width):
            current_blockage = -1 if direction == "N" else height
            iter = range(height) if direction == "N" else range(height-1,-1,-1)
            for row in iter:
                if grid[row][col] == "O":
                    grid[row][col] = "."
                    grid[current_blockage+increment][col] = "O"
                    current_blockage += increment
                elif grid[row][col] == "#":
                    current_blockage = row
    elif direction == "W" or direction == "E":
        increment = 1 if direction == "W" else -1
        for row in range(height):
            current_blockage = -1 if direction == "W" else width
            iter = range(width) if direction == "W" else range(width-1,-1,-1)
            for col in iter:
                if grid[row][col] == "O":
                    grid[row][col] = "."
                    grid[row][current_blockage+increment] = "O"
                    current_blockage += increment
                elif grid[row][col] == "#":
                    current_blockage = col
    return grid

def spin(grid, width, height):
    grid = tilt(grid, "N", width, height)
    grid = tilt(grid, "W", width, height)
    grid = tilt(grid, "S", width, height)
    grid = tilt(grid, "E", width, height)
    return grid

def score(grid_string, width, height):
    total = 0
    for i, char in enumerate(grid_string):
        row = i//width
        if char == "O":
            total += (height-row)
    return total

def make_grid_hashable(grid):
    return "".join(["".join(row) for row in grid])

SPINS = 10**9
with open("input.txt") as file:
    grid = [list(l.strip()) for l in file]
    sum = 0
    height = len(grid)
    width = len(grid[0])
    storage = {}
    grid_strings = []
    equivalent_index = -1
    for i in range(SPINS):
        grid = spin(grid, width, height)
        grid_string = make_grid_hashable(grid)
        grid_strings.append(grid_string)
        if grid_string in storage:
            prev_index = storage[grid_string]
            period = i - prev_index
            equivalent_index = ((SPINS-1)-prev_index)%period + prev_index
            break
        else:
            storage[grid_string] = i
    if equivalent_index == -1:
        print(score(grid_strings[-1], width, height))
    else:
        print(score(grid_strings[equivalent_index], width, height))