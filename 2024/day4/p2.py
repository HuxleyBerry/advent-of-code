with open("input.txt", "r") as file:
    grid = [l.strip() for l in file.readlines()]

height = len(grid)
width = len(grid[0])
total = 0
# horizontal
for i in range(1, width-1):
    for j in range(1, height-1):
        if grid[j][i] != 'A':
            continue
        diagonals = [grid[j+k][i+l] for k in (-1,1) for l in (-1,1)]
        if any(d != 'M' and d != 'S' for d in diagonals):
            continue
        if diagonals[0] != diagonals[3] and diagonals[1] != diagonals[2]:
            total += 1

print(total)