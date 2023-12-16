def map_num(source, num, all_maps):
    source_maps = all_maps[source]
    for _map in source_maps["maps"]:
        if num >= _map[1] and num < _map[1] + _map[2]:
            return source_maps["dest"], num - _map[1] + _map[0]
    return source_maps["dest"], num

with open("input.txt") as file:
    blocks = file.read().split("\n\n")
    seeds = blocks[0].split()[1:]
    seeds = [int(s) for s in seeds]
    all_maps = {}
    for block in blocks[1:]:
        split_block = block.split("\n")
        title = split_block[0][:-5].split("-")
        maps = [[int(n) for n in line.split()] for line in split_block[1:]]
        all_maps[title[0]] = {"dest": title[2], "maps": maps}
    minimum = 1000000000000
    for seed in seeds:
        source, num = "seed", seed
        while source != "location":
            source, num = map_num(source, num, all_maps)
        if num < minimum:
            minimum = num
    print(minimum)