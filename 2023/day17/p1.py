from queue import PriorityQueue

def get_neighbours(x,y,direction, multiplicity, width, height):
    if direction == None:
        out_directions = [(1,0),(0,1)]
    else:
        out_directions = [(direction[1], direction[0]), (-direction[1], -direction[0])]
        if multiplicity < 3:
            out_directions.append(direction)
    return [(x+dx,y+dy) for (dx, dy) in out_directions if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < height]

with open("input.txt") as file:
    grid = [l.strip() for l in file]
    width = len(grid[0])
    height = len(grid)
    visited = [[set() for char in line] for line in grid]
    queue = PriorityQueue()
    queue.put((0,(0,0),None,0))
    while not queue.empty():
        distance, (x,y), direction, multiplicity = queue.get()
        if x == width-1 and y == height-1:
            print(distance)
            break
        for x2, y2 in get_neighbours(x,y,direction, multiplicity, width, height):
            new_direction = (x2-x,y2-y)
            new_distance = distance + int(grid[y2][x2])
            new_multiplicity = 1 if new_direction != direction else multiplicity + 1
            if (new_direction, new_multiplicity) not in visited[y2][x2]:
                visited[y2][x2].add((new_direction, new_multiplicity))
                queue.put((new_distance, (x2,y2), new_direction, new_multiplicity))
            