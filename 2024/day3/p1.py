with open("input.txt", "r") as file:
    text = file.read()

between = text.split("mul")[1:]
total = 0
for section in between:
    if section[0] != "(":
        continue
    location = section.find(")")
    if location == -1:
        continue
    split_section = section[1:location].split(",")
    if len(split_section) != 2:
        continue
    left, right = split_section
    if not (left.isdigit() and right.isdigit()):
        continue
    total += int(left)*int(right)

print(total)