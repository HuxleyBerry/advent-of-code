from functools import reduce
from math import gcd

SPECIAL_MODULE_NAME = "rx"

def lcm_pair(a, b):
    return (a * b)//gcd(a,b)

def lcm(nums):
    return reduce(lcm_pair, nums)

def find_difference(nums):
    diff = nums[1] - nums[0]
    for i in range(1, len(nums)-1):
        new_diff = nums[i+1]-nums[i]
        if diff != new_diff:
            return -1
        diff = new_diff
    return diff

def count_presses_required(modules, end_predecessors):
    count = 0
    for i in range(20000):
        queue = [("broadcaster", False)]
        while len(queue) > 0:
            step(modules, queue, end_predecessors, count)
        count += 1
    differences = [find_difference(iterations) for name, iterations in end_predecessors.items()]
    if not any(d == -1 for d in differences):
        return lcm(differences)
    return -1

def step(modules, modules_queue, end_predecessors, count):
    module_name, pulse_type = modules_queue.pop(0)
    if module_name in end_predecessors and not pulse_type:
        end_predecessors[module_name].append(count)
    if module_name in modules:
        type, children, state = modules[module_name]
        if type == None: # broadcaster
            for child in children:
                add_to_queue(modules, modules_queue, module_name, child, pulse_type)
        elif type == "%":
            if not pulse_type:
                for child in children:
                    # off means high pulse
                    add_to_queue(modules, modules_queue, module_name, child, not state)
                modules[module_name] = (type, children, not state)
        elif type == "&":
            all_high = all(pt for parent, pt in state.items())
            for child in children:
                add_to_queue(modules, modules_queue, module_name, child, not all_high)

def add_to_queue(modules, queue, parent_name, child_name, pulse_type):
    # pulse_type is the type of the pulse sent from parent to child
    queue.append((child_name, pulse_type))
    if child_name in modules and modules[child_name][0] == "&":
        modules[child_name][2][parent_name] = pulse_type
    return queue


with open("input.txt") as file:
    modules = {}
    end_predecessors = {}
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
        if "mf" in outputs:
            end_predecessors[name] = []
    for module_name, (type, outputs, state) in modules.items():
        for output in outputs:
            if output in modules and modules[output][0] == "&":
                modules[output][2][module_name] = False
    print(count_presses_required(modules, end_predecessors))