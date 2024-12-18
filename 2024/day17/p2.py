from copy import deepcopy
from functools import cache

with open("input.txt") as file:
    reg_A = int(file.readline()[12:])
    reg_B = int(file.readline()[12:])
    reg_C = int(file.readline()[12:])
    file.readline()
    instructions = [int(x) for x in file.readline()[9:].split(",")]

state = {"A": reg_A, "B": reg_B, "C": reg_B, "ip": 0}

def get_combo_operand(operand, state):
    if operand <= 3:
        return operand
    elif operand < 7:
        # relies on insertion order preserved
        return list(state.values())[operand-4]
    else:
        raise Exception("Invalid program")

def perform_operation(opcode, operand, state):
    out = None
    dont_jump = False
    match opcode: # type: ignore
        case 0:
            state["A"]//=(2**get_combo_operand(operand, state))
        case 1:
            state["B"]^= operand
        case 2:
            state["B"] = get_combo_operand(operand, state)%8
        case 3:
            if state["A"] != 0:
                state["ip"] = operand
                dont_jump = True
        case 4:
            state["B"]^=state["C"]
        case 5:
            out = get_combo_operand(operand, state)%8
        case 6:
            state["B"] = state["A"]//(2**get_combo_operand(operand, state))
        case 7:
            state["C"] = state["A"]//(2**get_combo_operand(operand, state))
    if not dont_jump:
        state["ip"] += 2
    return out

def find_how_to_get_output(desired_output, state, required):
    res = []
    for a_val in (8*required + i for i in range(8)):
        state_copy = deepcopy(state)
        state_copy["A"] = a_val
        while True:
            instruction_pointer = state_copy["ip"]
            output = perform_operation(instructions[instruction_pointer], instructions[instruction_pointer+1], state_copy)
            if output is not None:
                if output == desired_output:
                    res.append(a_val)
                break
    return res
    
def solve(current, pos, instructions, state):
    if pos == -1:
        return current
    else:
        possibilities = find_how_to_get_output(instructions[pos], state, current)
        for possibility in possibilities:
            attempt = solve(possibility, pos-1, instructions, state) 
            if attempt is not None:
                return attempt
        return None

print(solve(0, len(instructions)-1, instructions, state))