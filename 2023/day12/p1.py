def count_possibilities(records, contiguous):
    unknown_positions = [i for i, char in enumerate(records) if char == "?"]
    contiguous_int = [int(x) for x in contiguous]
    return count_possibilities_recursive(records, contiguous_int, unknown_positions)

def count_possibilities_recursive(records, contiguous, unknown_positions):
    if len(unknown_positions) == 0:
        return 1 if does_info_match(records, contiguous) else 0
    else:
        index = unknown_positions[0]
        operational = records[:index] + "." + records[index+1:]
        damaged = records[:index] + "#" + records[index+1:]
        new_unknown = unknown_positions[1:]
        return count_possibilities_recursive(operational, contiguous, new_unknown) + count_possibilities_recursive(damaged, contiguous, new_unknown)

def does_info_match(records, contiguous):
    blocks = []
    current_block_size = 0
    for char in records:
        if char == "#":
            current_block_size += 1
        else:
            if current_block_size != 0:
                blocks.append(current_block_size)
                current_block_size = 0
    if current_block_size != 0:
        blocks.append(current_block_size)
    return blocks == contiguous

with open("input.txt") as file:
    sum = 0
    for i, line in enumerate(file):
        print(i)
        left, right = line.split()
        sum += count_possibilities(left, right.split(","))
    print(sum)