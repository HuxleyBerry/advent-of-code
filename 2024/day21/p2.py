from itertools import chain

with open("input.txt") as file:
   codes = [l.strip() for l in file.readlines()]

numeric_keypad_to_positions = {str(i): ((i-1)%3, 2 - (i-1)//3) for i in range(1,10)}
numeric_keypad_to_positions["0"] = (1,3)
numeric_keypad_to_positions["A"] = (2,3)
numeric_keypad_to_positions["E"] = (0,3)
direction_keypad_to_positions = {"v": (1,1), "^": (1,0), "<": (0,1), ">": (2,1), "A": (2,0), "E": (0,0)}
# directions_to_symbol = {(0,1): "v", (0,-1): "^", (1,0): ">", (-1,0): "<"}

def get_possible_sequences(start, end, empty_pos):
   x_diff = end[0] - start[0]
   y_diff = end[1] - start[1]
   if x_diff == 0 and y_diff == 0:
      return [""]
   x_symbol = ">" if x_diff > 0 else "<"
   y_symbol = "v" if y_diff > 0 else "^"
   if x_diff != 0 and y_diff != 0:
      results = []
      if True:
      #if (start[0], end[1]) != empty_pos:
         results.append(y_symbol*abs(y_diff) + x_symbol*abs(x_diff))
      if True:
      #if (start[1], end[0]) != empty_pos:
         results.append(x_symbol*abs(x_diff) + y_symbol*abs(y_diff))
      return results
   else:
      return [x_symbol*abs(x_diff) + y_symbol*abs(y_diff)]

def get_button_sequences(numeric_string, positions_dict):
   current_pos = positions_dict["A"]
   empty_pos = positions_dict["E"]
   sequences = [""]
   for c in numeric_string:
      required_pos = positions_dict[c]
      possible_move_sequences = get_possible_sequences(current_pos, required_pos, empty_pos)
      sequences = [s + possible + "A" for s in sequences for possible in possible_move_sequences]
      current_pos = required_pos
   """if len(sequences[0]) == 44:
      print("oomg", numeric_string, len(numeric_string))
   else:
      print("nomg", numeric_string, len(numeric_string))"""
   return sequences

def get_numeric_part(code):
   s = ""
   leading_done = False
   for c in code:
      if c != "0":
         leading_done = True
      if leading_done and c.isdigit():
         s += c
   return int(s)

total = 0
for code in codes:
   sequences1 = get_button_sequences(code, numeric_keypad_to_positions)
   sequences2 = list(chain(*(get_button_sequences(sequence, direction_keypad_to_positions) for sequence in sequences1)))
   
   sequences3 = list(chain(*(get_button_sequences(sequence, direction_keypad_to_positions) for sequence in sequences2)))
   min_length = min((len(x) for x in sequences3))
   print(sequences1)
   #print([len(x) for x in sequences3])
   print(min_length)
   #print(min_length, get_numeric_part(code))
   #total += min_length*get_numeric_part(code)

print(total)