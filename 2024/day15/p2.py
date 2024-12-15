expand = {".": "..", "O": "[]", "@": "@.", "#": "##"}

with open("input.txt") as file:
   [grid, moves] = file.read().split("\n\n")
grid = ["".join(expand[c] for c in line) for line in grid.split("\n")]
grid = [[c for c in line] for line in grid]
moves = [move for move in moves if not move.isspace()]
char_to_disp = {">": (1,0), "<": (-1,0), "v": (0,1), "^": (0,-1)}
sort_function = {">": lambda pos: -pos[0], "<": lambda pos: pos[0], "v": lambda pos: -pos[1], "^": lambda pos: pos[1]}


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

def count_grid(grid):
    a,b,c = 0,0,0
    for row in grid:
        for cell in row:
            if cell == "#":
                a += 1
            elif cell == "[":
                b += 1
            elif cell == "]":
                c += 1
    return a,b,c

def is_push_possible(grid, pos, direction):
   push_target_loc = (pos[0] + direction[0], pos[1] + direction[1])
   push_target = grid[push_target_loc[1]][push_target_loc[0]]
   if push_target == "#":
      return False, None
   elif push_target == ".":
      return True, [push_target_loc]
   else:
      assert push_target in ("[","]")
      if direction[1] == 0: # horizontal
        possible, children = is_push_possible(grid, push_target_loc, direction)
        if possible:
           return True, children + [push_target_loc]
        else:
           return False, None
      else:
         children = [push_target_loc, (push_target_loc[0]+1, push_target_loc[1])] if push_target == "[" else [push_target_loc, (push_target_loc[0]-1, push_target_loc[1])]
         possible = True
         descendants = []
         for child_loc in children:
            result, childs_descendants = is_push_possible(grid, child_loc, direction)
            if result:
               descendants += childs_descendants
            else:
               possible = False
               break
         if possible:
            # remove duplicates... but lose order
            descendants = list(set(descendants))
            descendants += children
            return True, descendants
         else:
            return False, None
         

for move in moves:
    direction = char_to_disp[move]
    dx, dy = direction
    push_possible, affected_locations = is_push_possible(grid, pos, direction)
    if push_possible:
        affected_locations.sort(key=sort_function[move])
        for x,y in affected_locations:
            if (x - dx, y- dy) not in affected_locations:
                grid[y][x] = "."
            else:
                grid[y][x] = grid[y - dy][x - dx]
        grid[pos[1]][pos[0]] = "."
        pos = (pos[0] + dx, pos[1]+ dy)


total = 0
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        if val == "[":
            total += j + (100*i)

print(total)