import heapq

with open("input.txt") as file:
   grid = [line.strip() for line in file]

start = None
end = None
for i, row in enumerate(grid):
   for j, val in enumerate(row):
      if val == "E":
         end = (j,i)
      elif val == "S":
         start = (j,i)

assert start is not None and end is not None

def heuristic(pos, direction, end):
    manhattan_dist = abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    differences = (end[0] - pos[0], end[1] - pos[1])
    directions_required = [((diff//abs(diff),0) if i == 0 else (0, diff//abs(diff))) for i, diff in enumerate(differences) if diff != 0]
    if len(directions_required) == 1:
        if directions_required[0] == direction:
            return manhattan_dist
        elif directions_required[0] == (-direction[0], -direction[1]):
            return manhattan_dist + 2000
        else:
            return manhattan_dist + 1000
    elif len(directions_required) == 2:
        if direction in directions_required:
            return manhattan_dist + 1000
        else:
            return manhattan_dist + 2000
    else:
        return 0
   

def find_shortest_path(grid, start, initial_direction, end):
   visited = set((start, initial_direction))
   priority_queue = []
   heapq.heappush(priority_queue, (heuristic(start, initial_direction, end), start, initial_direction, 0))
   while len(priority_queue) != 0:
      priority, pos, direction, cost_so_far = heapq.heappop(priority_queue)
      if pos == end:
         return cost_so_far
      children = [(pos, (direction[1], direction[0]), cost_so_far + 1000), (pos, (-direction[1], -direction[0]), cost_so_far + 1000)]
      if grid[pos[1] + direction[1]][pos[0] + direction[0]] != "#":
         children.append(((pos[0] + direction[0], pos[1] + direction[1]), direction, cost_so_far + 1))
      for child in children:
         child_pos, child_direction, child_cost = child
         if (child_pos, child_direction) in visited:
            continue
         heapq.heappush(priority_queue, (child_cost + heuristic(child_pos, child_direction, end), *child))
         visited.add((child_pos, child_direction))

print(find_shortest_path(grid, start, (1,0), end))