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
      
for wire, val in p1:
   if wire in name_to_node:
      name_to_node[wire].value = val
   else:
      node = Node(val)
      name_to_node[wire] = node

z_names.sort()

def calc(v1, v2, op):
   if op == "AND":
      return v1 & v2
   elif op == "OR":
      return v1 | v2
   else:
      return v1 ^ v2
   
def get_value(node_name):
   node = name_to_node[node_name]
   if node.value is not None:
      return node.value
   else:
      v1 = get_value(node.parent1)
      v2 = get_value(node.parent2)
      node.value = calc(v1, v2, node.operation)
      return node.value

num = 0
for i, z in enumerate(z_names):
   num += get_value(z)*(2**i)

print(num)