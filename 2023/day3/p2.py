def check_if_location_not_asterisk( lines, x, y, width, height):
    return x >= width or y >= height or x < 0 or y < 0 or lines[y][x] != "*"

def get_adjacent_locations(row, start_index, end_index):
    return [(x, row-1) for x in range(start_index-1, end_index+2)] + [(start_index-1, row), (end_index + 1, row)] + [(x, row+1) for x in range(start_index-1, end_index+2)]

with open("input.txt") as file:
    lines = file.readlines()
    height = len(lines)
    width = len(lines[0]) - 1
    gear_adjancies = [[[] for i in range(width)] for j in range(height)]
    sum = 0
    for i, line in enumerate(lines):
        current_num = ""
        for j, char in enumerate(line):
            if char.isdigit():
                current_num += char
            elif current_num != "":
                adjacent_locations = get_adjacent_locations(i, j - len(current_num), j - 1)
                for (x,y) in adjacent_locations:
                    if not check_if_location_not_asterisk(lines, x, y, width, height):
                        gear_adjancies[y][x].append(int(current_num))
                current_num = ""
    for row in gear_adjancies:
        for loc in row:
            if len(loc) == 2:
                sum += loc[0]*loc[1]
    print(sum)

