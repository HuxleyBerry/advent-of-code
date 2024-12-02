with open("input.txt") as file:
    lines = file.readlines()
    instructions = lines[0].strip()
    instruction_length = len(instructions)
    _network = lines[2:]
    network = {}
    for line in _network:
        network[line[0:3]] =  (line[7:10], line[12:15])

    current_positions = "AAA"
    count = 0
    while current_pos != "ZZZ":
        index = 0 if instructions[count%instruction_length] == "L" else 1
        current_pos = network[current_pos][index]
        count += 1
    print(count)