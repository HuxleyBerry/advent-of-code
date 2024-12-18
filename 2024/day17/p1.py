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

out_string = ""
while True:
   instruction_pointer = state["ip"]
   if instruction_pointer >= len(instructions):
      print(out_string[:-1])
      break
   output = perform_operation(instructions[instruction_pointer], instructions[instruction_pointer+1], state)
   if output is not None:
      out_string += f"{output},"
