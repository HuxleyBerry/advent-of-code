with open("input1.txt") as file:
    total = 0
    for line in file:
        filtered_line = "".join(c for c in line if c.isdigit())
        calibration = int(filtered_line[0] + filtered_line[-1])
        total += calibration
    print(total)