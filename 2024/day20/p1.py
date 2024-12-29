with open("input.txt") as file:
   grid = [l.strip() for l in file.readlines()]

width = len(grid[0])
height = len(grid)
save_requirement = 100

start, end = None, None
for i, row in enumerate(grid):
   for j, val in enumerate(row):
      if val == "S":
         start = j,i
      elif val == "E":
         end = j,i

def get_neighbours(pos, grid, width, height):
   x, y = pos
   return ((x1, y1) for (x1, y1) in ((x, y+1), (x, y-1), (x+1,y), (x-1,y)) if 0 <= x1 and x1 < width and 0 <= y1 and y1 < height and grid[y1][x1] != "#")

def is_cheat_neighbours(pos1, pos2):
   x1, y1 = pos1
   x2, y2 = pos2
   return abs(x1-x2) + abs(y1-y2) == 2

stack = [start]
parents = {start: None}
while len(stack) != 0:
   top = stack.pop()
   if top == end:
      break
   else:
      for neighbour in get_neighbours(top, grid, width, height):
         if neighbour not in parents:
            parents[neighbour] = top
            stack.append(neighbour)
path = [end]
current = end
while current != start:
   current = parents[current]
   path.append(current)

path = path[::-1]

total = 0
for (i, pos1) in enumerate(path):
   for j in range(i - 1 - save_requirement):
      pos2 = path[j]
      if is_cheat_neighbours(pos1, pos2):
         saved = i - j - 2 # i - 2 - save_requirement >= j
         if saved >= save_requirement:
            total += 1

print(total)