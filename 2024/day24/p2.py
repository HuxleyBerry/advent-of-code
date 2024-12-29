from copy import deepcopy
from itertools import combinations
from collections import defaultdict

with open("input.txt") as f:
   p1, p2 = f.read().split("\n\n")
   p1 = [(l[:3], int(l[5])) for l in p1.split("\n")]
   p2 = [l.strip().split() for l in p2.split("\n")]
   p2 = [(l[0], l[1], l[2], l[4]) for l in p2]

class Node:
   def __init__(self, value=None, parent1=None, parent2=None, operation=None):
      self.parent1 = parent1
      self.parent2 = parent2
      self.operation = operation
      self.value = value

   def __str__(self):
      if self.value is None:
         return f"Node with value derived from '{self.parent1} {self.operation} {self.parent2}'"
      else:
         return f"Node with value {self.value}"

name_to_node = {}
z_names = []
for w1, op, w2, target in p2:
   name_to_node[target] = Node(None, w1, w2, op)
   if target[0] == "z":
      z_names.append(target)

for name, _ in p1:
   name_to_node[name] = Node(None)
   
z_names.sort()

def calc(v1, v2, op):
   if op == "AND":
      return v1 & v2
   elif op == "OR":
      return v1 | v2
   else:
      return v1 ^ v2
   
def get_value(node_name, name_to_node):
   node = name_to_node[node_name]
   if node.value is not None:
      return node.value
   else:
      v1 = get_value(node.parent1, name_to_node)
      v2 = get_value(node.parent2, name_to_node)
      node.value = calc(v1, v2, node.operation)
      return node.value

def test(x_bits, y_bits, switches, count=False):
   name_to_node_map = deepcopy(name_to_node)
   for i, (x_bit, y_bit) in enumerate(zip(x_bits, y_bits)):
      name_to_node_map[f"x{'0' if i < 10 else ''}{i}"].value = x_bit
      name_to_node_map[f"y{'0' if i < 10 else ''}{i}"].value = y_bit

   for switch1, switch2 in switches:
      assert switch1 in name_to_node_map and switch2 in name_to_node_map
      temp = name_to_node_map[switch1]
      name_to_node_map[switch1] = name_to_node_map[switch2]
      name_to_node_map[switch2] = temp

   
   fake_sum = sum(get_value(z, name_to_node_map)*(2**i) for i, z in enumerate(z_names))

   x_num = sum(bit*(2**i) for i, bit in enumerate(x_bits))
   y_num = sum(bit*(2**i) for i, bit in enumerate(y_bits))
   xor = bin(fake_sum ^ (x_num + y_num))
   # print(bin(fake_sum), bin(x_num + y_num))
   # print('0b' + '0'*(len(bin(x_num + y_num)) - len(xor)) + bin(fake_sum ^ (x_num + y_num))[2:])
   if count:
      return xor.count('1')
   return xor
   
ancestors = defaultdict(set)
def set_ancestors(name):
   if name in ancestors:
      return ancestors[name]
   else:
      node = name_to_node[name]
      if node.parent1 is not None and node.parent2 is not None:
         unioned = set_ancestors(node.parent1).union(set_ancestors(node.parent2))
         unioned.add(node.parent1)
         unioned.add(node.parent2)
         ancestors[name] = unioned
         return unioned
      else:
         return set()
   
for i, z in enumerate(z_names):
   x = set_ancestors(z)

wrong_operations = []
should_be_z = []
for i, z in enumerate(z_names):
   node = name_to_node[z]
   if i < len(z_names) - 1:
      if node.operation != "XOR":
         print("wrong op:", z)
         wrong_operations.append(z)
      elif i >= 2 and {name_to_node[node.parent1].operation, name_to_node[node.parent2].operation} != {"XOR", "OR"}:
         print("wrong parents:", z, name_to_node[node.parent1].operation, name_to_node[node.parent2].operation)
      elif i >= 1 and (node.parent1[0] in ("x", "y") or node.parent2[0] in ("x", "y")):
         print("can't have xy parent:", z)
      
for name in name_to_node:
   node = name_to_node[name]
   if node.operation == "XOR":
      if name != "z00" and (node.parent1[0] in ("x", "y") or node.parent2[0] in ("x", "y")) and name[0] == "z":
         print("Shouldn't have descendant z:", name)
      elif node.parent1[0] not in ("x", "y") and node.parent2[0] not in ("x", "y") and name[0] != "z":
         print("Should be a z:", name)
         should_be_z.append(name)

should_be_z.sort(key=lambda s: len(ancestors[s]))
base = list(zip(wrong_operations, should_be_z))

swap_targets = set(z_names).union(*((n for n in ancestors[z] if n[0] not in ("x","y")) for z in z_names)).difference(set().union(*(set(tup) for tup in base)))
combs = list(combinations(swap_targets , 2))

x_bits = [1 for i in range(45)]
y_bits = [1 for i in range(45)]
candidates = []
for i, (a, b) in enumerate(combs):
   if i%1000 == 0:
      print(f"{(i*100)//len(combs)}% done.")
   if a not in ancestors[b] and b not in ancestors[a]:
      try:
         concat = base + [(a,b)]
         res = test(x_bits, y_bits, concat, True)
         if res == 0:
            # works for this number, will it work for all?
            candidates.append(concat)
      except RecursionError:
         pass #idk why happening
      except Exception as e:
         raise e

# now test for different sums
successful_candidates = []
x_bits_possibilities = ([1 for i in range(45)], [i%2 for i in range(45)], [1 if i%3 != 0 else 0 for i in range(45)])
y_bits_possibilities = ([0 for i in range(45)], [1 for i in range(45)], [1 for i in range(45)])
for candidate in candidates:
   if all(test(x_bits, y_bits, candidate, True) == 0 for x_bits, y_bits in zip(x_bits_possibilities, y_bits_possibilities)):
      successful_candidates.append(candidate)

assert len(successful_candidates) == 1
sol = successful_candidates[0]
sol = sorted([s[0] for s in sol] + [s[1] for s in sol])
print(",".join(sol))