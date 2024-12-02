from functools import lru_cache

def count_possibilities(records, contiguous):
    contiguous_int = [int(x) for x in contiguous]
    memo = {}
    return count_possibilities_recursive(memo, records, contiguous_int, 0, 0, 0)

def count_possibilities_recursive(memo, records, contiguous, current_block_size, blocks_completed, current_index):
    if (current_block_size, blocks_completed, current_index) in memo:
        return memo[(current_block_size, blocks_completed, current_index)]
    else:
        if current_index == len(records):
            result = 1 if blocks_completed == len(contiguous) else 0
        else:
            char = records[current_index]
            if current_block_size == 0:
                sum = 0
                if char == "." or char == "?":
                    sum += count_possibilities_recursive(memo, records, contiguous, 0, blocks_completed, current_index+1)
                if char == "#" or char == "?":
                    if blocks_completed < len(contiguous):
                        if current_index == len(records) - 1 and 1 == contiguous[blocks_completed]:
                            sum += count_possibilities_recursive(memo, records, contiguous, 1, blocks_completed+1, current_index+1)
                        else:
                            sum += count_possibilities_recursive(memo, records, contiguous, 1, blocks_completed, current_index+1)
                result = sum
            else: # working on a block
                sum = 0
                if char == "." or char == "?":
                    if current_block_size == contiguous[blocks_completed]:
                        # able to complete a block with a "."
                        sum += count_possibilities_recursive(memo, records, contiguous, 0, blocks_completed+1, current_index+1)
                if char == "#" or char == "?": 
                    # able to continue a block with "#"
                    if current_index == len(records) - 1 and current_block_size+1 == contiguous[blocks_completed]:
                        sum += count_possibilities_recursive(memo, records, contiguous, current_block_size+1, blocks_completed+1, current_index+1)
                    elif current_block_size < contiguous[blocks_completed]: # block needs to be continued
                        sum += count_possibilities_recursive(memo, records, contiguous, current_block_size+1, blocks_completed, current_index+1)
                result = sum
        memo[(current_block_size, blocks_completed, current_index)] = result
        return result
   

with open("input.txt") as file:
    sum = 0
    for i, line in enumerate(file):
        left, right = line.split()
        unfolded_left = ((left + "?")*5)[:-1]
        #sum += count_possibilities(left, right.split(","))
        sum += count_possibilities(unfolded_left, right.split(",")*5)
    print(sum)