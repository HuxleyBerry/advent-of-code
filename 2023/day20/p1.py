def count_pulses(modules):
    low_count, high_count = 0, 0
    for i in range(1000):
        low_count += 1 # pressing button
        queue = [("broadcaster", False)]
        while len(queue) > 0:
            low_count, high_count = step(modules, queue, low_count, high_count)
    return low_count*high_count

def increment(amount, low_count, high_count, pulse_type):
    if pulse_type:
        return low_count, high_count+amount
    else:
        return low_count+amount, high_count

def step(modules, modules_queue, low_count, high_count):
    module_name, pulse_type = modules_queue.pop(0)
    if module_name in modules:
        type, children, state = modules[module_name]
        if type == None: # broadcaster
            for child in children:
                add_to_queue(modules, modules_queue, module_name, child, pulse_type)
            low_count, high_count = increment(len(children), low_count, high_count, pulse_type)
        elif type == "%":
            if not pulse_type:
                for child in children:
                    # off means high pulse
                    add_to_queue(modules, modules_queue, module_name, child, not state)
                modules[module_name] = (type, children, not state)
                low_count, high_count = increment(len(children), low_count, high_count, not state)
        elif type == "&":
            all_high = all(pt for parent, pt in state.items())
            for child in children:
                add_to_queue(modules, modules_queue, module_name, child, not all_high)
            low_count, high_count = increment(len(children), low_count, high_count, not all_high)
    return low_count, high_count


def add_to_queue(modules, queue, parent_name, child_name, pulse_type):
    # pulse_type is the type of the pulse sent from parent to child
    queue.append((child_name, pulse_type))
    if child_name in modules and modules[child_name][0] == "&":
        modules[child_name][2][parent_name] = pulse_type
    return queue


with open("input.txt") as file:
    modules = {}
    for line in file:
        left, right = line.split(" -> ")
        if left == "broadcaster":
            name, type = "broadcaster", None
            state = None
        else:
            name, type = left[1:], left[0]
            if type == "%":
                state = False
            elif type == "&":
                state = {}
        outputs = right.strip().split(", ")
        modules[name] = (type, outputs, state)
    for module_name, (type, outputs, state) in modules.items():
        for output in outputs:
            if output in modules and modules[output][0] == "&":
                modules[output][2][module_name] = False
    print(count_pulses(modules))