with open("input.txt", "r") as file:
    grid = [l.strip() for l in file.readlines()]

height = len(grid)
width = len(grid[0])
total = 0
target = ('XMAS', 'SAMX')
# horizontal
for i in range(width-3):
    for j in range(height):
        if grid[j][i:i+4] in target:
            total += 1

# vertical
for i in range(width):
    for j in range(height-3):
        if "".join(grid[j+k][i] for k in range(4)) in target:
            total += 1

# forward diagonal
for i in range(width-3):
    for j in range(height-3):
        if "".join(grid[j+k][i+k] for k in range(4)) in target:
            total += 1
# backward diagonal
for i in range(3, width):
    for j in range(height-3):
        if "".join(grid[j+k][i-k] for k in range(4)) in target:
            total += 1

print(total)