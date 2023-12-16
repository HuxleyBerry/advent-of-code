from math import floor, ceil, sqrt

def count_ways_of_winning(time, distance):
    sqrt_disc = sqrt(time*time - 4*distance)
    lower = floor((time - sqrt_disc)/2) + 1
    upper  = ceil((time + sqrt_disc)/2) - 1
    return upper - lower + 1

with open("input.txt") as file:
    [times, distances] = file.readlines()
    times = [int(x) for x in times.split()[1:]]
    distances = [int(x) for x in distances.split()[1:]]
    product = 1
    for time, distance in zip(times, distances):
        product *= count_ways_of_winning(time, distance)
    print(product)