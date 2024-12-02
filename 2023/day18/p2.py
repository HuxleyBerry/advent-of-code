directions_dict = {"L": (-1,0), "U": (0,-1), "R": (1,0), "D": (0,1)}
hex_to_dec = {"f": 15, "e": 14, "d": 13, "c": 12, "b": 11, "a": 10}
hex_to_dig = {"0": "R", "1": "D", "2": "L", "3": "U"}

def to_hexa(s):
    length = len(s)
    total = 0
    for i, c in enumerate(s):
        num = int(c) if c.isnumeric() else hex_to_dec[c] 
        total += (16**(length-i-1))*num
    return total

with open("input.txt") as file:
    current_x, current_y = 0, 0
    total = 0
    RD_count = 1
    for line in file:
        direction, distance, colour = line.split()
        colour = colour[2:-1]
        direction = hex_to_dig[colour[-1]]
        distance = to_hexa(colour[:-1])
        new_x = current_x + distance*directions_dict[direction][0]
        new_y = current_y + distance*directions_dict[direction][1]
        if direction in ("R","D"):
            RD_count += distance
        total += (new_y*current_x - new_x*current_y)
        current_x, current_y = new_x, new_y
    print(total//2 + RD_count)