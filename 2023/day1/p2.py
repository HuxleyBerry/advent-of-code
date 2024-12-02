numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def is_num(line, index):
    if line[index].isdigit():
        return line[index]
    for j, number in enumerate(numbers):
        success = True
        for i, char in enumerate(number):
            if index+i >= len(line) or char != line[index+i]:
                success = False
        if success:
            return str(j+1)
    return False
    

with open("input1.txt") as file:
    total = 0
    for line in file:
        filtered_line = ""
        for i in range(len(line)):
            result = is_num(line, i)
            if result != False:
                filtered_line += result
        calibration = int(filtered_line[0] + filtered_line[-1])
        total += calibration
    print(total)