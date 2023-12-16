from itertools import combinations

with open("input.txt") as file:
    lines = [l.strip() for l in file.readlines()]
    blank_rows = [True for i in range(len(lines))]
    blank_columns = [True for i in range(len(lines[0]))]
    galaxy_locations = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != ".":
                blank_rows[i] = False
                blank_columns[j] = False
                galaxy_locations.append((j,i))
    sum = 0
    
    for (x1, y1), (x2, y2) in combinations(galaxy_locations, 2):
        if x1 >= x2:
            x_dist = (1000000-1)*blank_columns[x2:x1].count(True) - (x2 - x1)
        else:
            x_dist = (1000000-1)*blank_columns[x1:x2].count(True) - (x1 - x2)
        if y1 >= y2:
            y_dist = (1000000-1)*blank_rows[y2:y1].count(True) - (y2 - y1)
        else:
            y_dist = (1000000-1)*blank_rows[y1:y2].count(True) - (y1 - y2)
        sum += x_dist + y_dist
    print(sum)