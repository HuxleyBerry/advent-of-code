with open("input.txt") as file:
    data = [[int(x) for x in line.strip()] for line in file.readlines()]

width = len(data[0])
height = len(data)
def in_bounds(loc):
    global width, height
    x, y = loc
    return 0 <= x and  x < width and 0 <= y and y < height

def traverse(x, y, grid, current_height, achieved):
    neighbours = [loc for loc in ((x,y+1), (x, y-1), (x+1,y), (x-1,y)) if in_bounds(loc)]
    for x1, y1 in neighbours:
        if grid[y1][x1] == current_height + 1:
            if current_height + 1 == 9:
                achieved.add((x1,y1))
            else:
                traverse(x1,y1, grid, current_height+1, achieved)

total = 0
for i, row in enumerate(data):
    for j, val in enumerate(row):
        if val == 0:
            achieved = set()
            traverse(j,i,data, 0,achieved)
            total += len(achieved)
            
print(total)