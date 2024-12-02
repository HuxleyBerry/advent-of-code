def get_hash(string):
    cv = 0
    for char in string:
        cv = ((cv + ord(char))*17)%256
        
    return cv

def perform_step(boxes, step):
    label = step[:-1] if step[-1] == "-" else step[:-2]
    box_num = get_hash(label)
    if step[-1] == "-":
        for i, lens in enumerate(boxes[box_num]):
            if lens[0] == label:
                boxes[box_num].pop(i)
                break
    else:
        focal_length = int(step[-1])
        matching_label_found = False
        for i, lens in enumerate(boxes[box_num]):
            if lens[0] == label:
                boxes[box_num][i] = (label, focal_length)
                matching_label_found = True
                break
        if not matching_label_found:
            boxes[box_num].append((label, focal_length))

def get_focus_power(box_num, slot_num, focus):
    return (box_num+1)*(slot_num+1)*focus

with open("input.txt") as file:
    strings = file.read().strip().split(",")
    boxes = [[] for i in range(256)]
    total = 0
    for step in strings:
        perform_step(boxes, step)
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            total += get_focus_power(i, j, lens[1])
    print(total)
