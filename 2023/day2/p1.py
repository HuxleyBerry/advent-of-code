colours = {"red": 12, "green": 13, "blue": 14}

def is_game_possible(game):
    [name, grabs] = game.split(": ")
    num = int(name.split(" ")[1])
    for grab in grabs.split("; "):
        if not is_grab_possible(grab):
            return 0
    return num

def is_grab_possible(grab):
    for colour in grab.split(", "):
        [count, col] = colour.split(" ")
        if int(count) > colours[col]:
            return False
    return True

with open("input.txt") as file:
    sum = 0
    for line in file:
        sum += is_game_possible(line.strip())
    print(sum)