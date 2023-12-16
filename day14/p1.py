with open("input.txt") as file:
    grid = [l.strip() for l in file]
    sum = 0
    height = len(grid)
    for col in range(len(grid[0])):
        current_blockage = -1
        for row in range(len(grid)):
            if grid[row][col] == "O":
                sum += height - (current_blockage+1)
                current_blockage += 1
            elif grid[row][col] == "#":
                current_blockage = row
    print(sum)