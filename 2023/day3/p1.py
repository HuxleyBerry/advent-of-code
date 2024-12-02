def check_if_location_not_symbol( lines, x, y, width, height):
    return x >= width or y >= height or x < 0 or y < 0 or lines[y][x] == "." or lines[y][x].isdigit()

def get_adjacent_locations(row, start_index, end_index):
    return [(x, row-1) for x in range(start_index-1, end_index+2)] + [(start_index-1, row), (end_index + 1, row)] + [(x, row+1) for x in range(start_index-1, end_index+2)]

with open("input.txt") as file:
    lines = file.readlines()
    height = len(lines)
    width = len(lines[0]) - 1
    sum = 0
    for i, line in enumerate(lines):
        current_num = ""
        for j, char in enumerate(line):
            if char.isdigit():
                current_num += char
            elif current_num != "":
                number_found = int(current_num)
                adjacent_locations = get_adjacent_locations(i, j - len(current_num), j - 1)
                #if True:
                if not all(check_if_location_not_symbol(lines, x, y, width, height) for (x,y) in adjacent_locations):
                    sum += int(current_num)
                current_num = ""
    print(sum)

