from math import gcd
from functools import reduce

def lcm(arr):
    l=reduce(lambda x,y:(x*y)//gcd(x,y),arr)
    return l

with open("input.txt") as file:
    lines = file.readlines()
    instructions = lines[0].strip()
    instruction_length = len(instructions)
    _network = lines[2:]
    network = {}
    for line in _network:
        network[line[0:3]] =  (line[7:10], line[12:15])

    current_positions = [loc for loc in network if loc[2] == 'A']
    counts = [0 for x in current_positions]
    for i, pos in enumerate(current_positions):
        while current_positions[i][2] != "Z":
            index = 0 if instructions[counts[i]%instruction_length] == "L" else 1
            current_positions[i] = network[current_positions[i]][index]
            counts[i] += 1
    print(lcm(counts))