def map_num(source, num_range_start, num_range_end, all_maps):
    source_maps = all_maps[source]
    current_range_start = num_range_start
    mapped_ranges = []
    for _map in source_maps["maps"]:
        if current_range_start < _map[1]:
            if num_range_end <= _map[1]:
                mapped_ranges.append((current_range_start, num_range_end))
                current_range_start = num_range_end
                break
            else:
                mapped_ranges.append((current_range_start, _map[1]))
                current_range_start = _map[1]
                if num_range_end <= _map[1] + _map[2]:
                    mapped_ranges.append((_map[0], _map[0] + num_range_end - _map[1]))
                    current_range_start = num_range_end
                    break
                else:
                    mapped_ranges.append((_map[0], _map[0] + _map[2]))
                    current_range_start = _map[1] + _map[2]
        else:
            if current_range_start >= _map[1] + _map[2]:
                continue
            else:
                if num_range_end <= _map[1] + _map[2]:
                    mapped_ranges.append((_map[0] + current_range_start - _map[1], _map[0] + num_range_end - _map[1]))
                    current_range_start = num_range_end
                    break
                else:
                    mapped_ranges.append((_map[0] + current_range_start - _map[1], _map[0] + _map[2]))
                    current_range_start = _map[1] + _map[2]
    if current_range_start != num_range_end:
        mapped_ranges.append((current_range_start, num_range_end))
    return source_maps["dest"], mapped_ranges

with open("input.txt") as file:
    blocks = file.read().split("\n\n")
    seed_ranges = blocks[0].split()[1:]
    seed_ranges = [int(s) for s in seed_ranges]
    seeds = zip(seed_ranges[::2], seed_ranges[1::2])
    all_maps = {}
    for block in blocks[1:]:
        split_block = block.split("\n")
        title = split_block[0][:-5].split("-")
        maps = [[int(n) for n in line.split()] for line in split_block[1:]]
        all_maps[title[0]] = {"dest": title[2], "maps": sorted(maps, key=lambda x: x[1])}
    source = "seed"
    ranges = [(a, a + b) for a, b in seeds]
    while source != "location":
        print(source)
        new_ranges = []
        for range_start, range_end in ranges:
            new_source, result_ranges = map_num(source, range_start, range_end, all_maps)
            new_ranges = new_ranges + result_ranges
        ranges = new_ranges
        source = new_source
    minimum = 1000000000000
    for range_start, range_end in ranges:
        if range_start < minimum:
            minimum = range_start
    print(minimum)