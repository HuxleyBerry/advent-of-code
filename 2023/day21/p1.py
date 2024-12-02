def step(grid, max_depth, start_x, start_y):
    visited_odd = set()
    visited_even = {(start_x, start_y)}
    queue = [(start_x, start_y, 0)]
    while len(queue) != 0:
        x, y, depth = queue.pop(0)
        if depth >= max_depth:
            break
        current_visitation_set = visited_odd if depth%2 == 0 else visited_even
        for x2, y2 in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if is_garden(x2, y2, grid) and (x2, y2) not in current_visitation_set:
                current_visitation_set.add((x2, y2))
                queue.append((x2, y2, depth+1))
    return len(visited_even)

def is_garden(x, y, grid):
    return 0 <= x and 0 <= y and x < len(grid[0]) and y < len(grid) and grid[y][x] == "."

with open("input.txt") as file:
    grid = [l.strip() for l in file]
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start_x, start_y = j, i
                break
    print(step(grid, 64, start_x, start_y))