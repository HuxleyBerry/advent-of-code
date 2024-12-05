with open("input.txt", "r") as file:
    text = file.read()

between = text.split("mul")[1:]
total = 0
enabled = True
for section in between:
    if section[0] == "(":
        location = section.find(")")
        if location != -1:
            split_section = section[1:location].split(",")
            if len(split_section) == 2:
                left, right = split_section
                if left.isdigit() and right.isdigit() and enabled:
                    total += int(left)*int(right)
    index = 0
    while index < len(section):
        if enabled:
            loc = section.find("don't()", index)
        else:
            loc = section.find("do()", index)
        index = loc+1
        if loc == -1:
            break
        else:
            enabled = not enabled

print(total)