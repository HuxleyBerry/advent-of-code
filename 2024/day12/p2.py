from collections import defaultdict

with open("input.txt") as file:
    grid = [line.strip() for line in file.readlines()]

width = len(grid[0])
height = len(grid)

def get_neighbours(loc):
    global width, height
    x, y = loc
    return ((x1, y1) for (x1, y1) in ((x,y+1), (x,y-1), (x+1,y), (x-1,y)) if 0 <= x1 and x1 < width and 0 <= y1 and y1 < height)

current_region_index = 0
regions_reversed = {}
regions = defaultdict(list)
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        found_region_index = -1
        for neighbour_x, neighbour_y in get_neighbours((j, i)):
            if grid[neighbour_y][neighbour_x] == val and (neighbour_x, neighbour_y) in regions_reversed:
                if found_region_index == -1:
                    neighbours_region = regions_reversed[(neighbour_x, neighbour_y)]
                    regions_reversed[(j, i)] = neighbours_region
                    regions[neighbours_region].append((j, i))
                    found_region_index = neighbours_region
                else:
                    # we have already found a matching neighbour
                    # any other matching neighbours must have their region index merged
                    region_to_merge = regions_reversed[(neighbour_x, neighbour_y)]
                    if region_to_merge != found_region_index:
                        for x,y in regions[region_to_merge]:
                            regions_reversed[(x,y)] = found_region_index
                        regions[found_region_index] += regions[region_to_merge]
                        regions.pop(region_to_merge)
        if found_region_index== -1:
            regions_reversed[(j,i)] = current_region_index
            regions[current_region_index].append((j, i))
            current_region_index += 1

def get_region_sides(region):
    sides = 0
    plots_as_set = set(region)
    for x,y in region:
        if (x,y-1) not in plots_as_set and ((x+1,y) not in plots_as_set or (x+1, y-1) in plots_as_set):
            sides += 1
        if (x,y+1) not in plots_as_set and ((x+1,y) not in plots_as_set or (x+1, y+1) in plots_as_set):
            sides += 1
        if (x-1,y) not in plots_as_set and ((x,y+1) not in plots_as_set or (x-1, y+1) in plots_as_set):
            sides += 1
        if (x+1,y) not in plots_as_set and ((x,y+1) not in plots_as_set or (x+1, y+1) in plots_as_set):
            sides += 1

    return sides

print(sum((get_region_sides(region)*len(region) for region in regions.values())))