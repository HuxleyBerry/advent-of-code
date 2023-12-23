ddict = {"^": (0,-1), ">": (1,0), "<": (-1,0), "v": (0,1)}
def search(grid, start, end):
    path_lengths = []
    stack = [(start, set())]
    while len(stack) != 0:
        pos, visited = stack.pop()
        neighbours = get_neighbours(grid, pos[0], pos[1])
        for neighbour in neighbours:
            if neighbour == end:
                path_lengths.append(len(visited)+1)
            elif neighbour not in visited:
                visited_copy = visited.copy()
                visited_copy.add(neighbour)
                stack.append((neighbour, visited_copy))
    return path_lengths

def get_neighbours(grid, x,y):
    if grid[y][x] in ["^", ">", "<", "v"]:
        dx, dy = ddict[grid[y][x]]
        return [(x+dx,y+dy)]
    else:
        unfiltered = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        return [(x2, y2) for x2, y2 in unfiltered if 0 <= x2 and 0 <= y2 and x2 < len(grid[0]) and y2 < len(grid) and grid[y2][x2] != "#"]

with open("input.txt") as file:
    grid = [l.strip() for l in file]
    start = (grid[0].index("."),0)
    end = (grid[-1].index("."),len(grid)-1)
    path_lengths = search(grid, start, end)
    print(max(path_lengths))