with open("input.txt") as file:
   [grid, moves] = file.read().split("\n\n")
grid = [[c for c in line] for line in grid.split("\n")]
moves = [move for move in moves if not move.isspace()]
char_to_disp = {">": (1,0), "<": (-1,0), "v": (0,1), "^": (0,-1)}

pos = None
for i, row in enumerate(grid):
   if pos is not None:
      break
   for j, val in enumerate(row):
      if val == "@":
         pos = j, i
         break

def print_grid(grid):
   for row in grid:
      print("".join(c for c in row))
   print("\n")

for move in moves:
   direction = char_to_disp[move]
   probing_pos = (pos[0], pos[1])
   distance_to_push = None
   can_move = False
   probe_count = 0
   while True:
      probe_count += 1
      probing_pos = (probing_pos[0] + direction[0], probing_pos[1] + direction[1])
      x, y = probing_pos
      if grid[y][x] == ".":
         can_move = True
         distance_to_push = probe_count
         break
      elif grid[y][x] == "#":
         break
   if can_move:
      for dist in range(distance_to_push,0,-1):
         receiving_pos = (pos[0] + dist*direction[0], pos[1] + dist*direction[1])
         giving_pos = (receiving_pos[0] - direction[0], receiving_pos[1] - direction[1])
         grid[receiving_pos[1]][receiving_pos[0]] = grid[giving_pos[1]][giving_pos[0]]
      grid[pos[1]][pos[0]] = "."
      pos = (pos[0] + direction[0], pos[1] + direction[1])

total = 0
for i, row in enumerate(grid):
   for j, val in enumerate(row):
      if val == "O":
         total += j + (100*i)

print(total)