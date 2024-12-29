from functools import cache

with open("input.txt") as file:
   towels = file.readline().strip().split(", ")
   file.readline()
   patterns = [l.strip() for l in file.readlines()]

towels_set = set(towels)
longest_pattern = len(max(towels, key=lambda x:len(x)))

@cache
def count_ways(pattern):
    if len(pattern) == 0:
        return 1
    total = 0
    for i in range(1, min(longest_pattern+1, len(pattern)+1)):
        if pattern[:i] in towels_set:
            x = count_ways(pattern[i:])
            total += x
    return total

print(sum(count_ways(pattern) for pattern in patterns))