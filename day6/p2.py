from math import floor, ceil, sqrt
from functools import reduce

def count_ways_of_winning(time, distance):
    sqrt_disc = sqrt(time*time - 4*distance)
    lower = floor((time - sqrt_disc)/2) + 1
    upper  = ceil((time + sqrt_disc)/2) - 1
    return upper - lower + 1

with open("input.txt") as file:
    [times, distances] = file.readlines()
    times = times.split()[1:]
    distances = distances.split()[1:]
    time = int(reduce(lambda x,y : x + y, times))
    distance = int(reduce(lambda x,y : x + y, distances))
    print(count_ways_of_winning(time, distance))