def get_hash(string):
    cv = 0
    for char in string:
        cv = ((cv + ord(char))*17)%256
        
    return cv

with open("input.txt") as file:
    strings = file.read().strip().split(",")
    total = 0
    for string in strings:
        total += get_hash(string)
    print(total)