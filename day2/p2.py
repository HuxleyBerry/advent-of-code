def find_power(game):
    grabs = game.split(": ")[1]
    maxes = {"red": 0, "green": 0, "blue": 0}
    for grab in grabs.split("; "):
        update_maxes_from_grab(grab, maxes)
    product = 1
    for colour in maxes:
        product *= maxes[colour]
    return product

def update_maxes_from_grab(grab, maxes):
    for colour_num_pair in grab.split(", "):
        [count, col] = colour_num_pair.split(" ")
        if int(count) > maxes[col]:
            maxes[col] = int(count)
    return maxes

with open("input.txt") as file:
    sum = 0
    for line in file:
        sum += find_power(line.strip())
    print(sum)