with open("input.txt") as f:
   data = [(line[:2], line[3:5]) for line in f]

connections = set(data)
t_computers = set((c1 for c1, c2 in data if c1[0] == 't')).union(set((c2 for c1, c2 in data if c2[0] == 't')))
total = 0
res = set()
for c1, c2 in connections:
   for t in t_computers:
      if t not in (c1, c2) and ((t, c1) in connections or (c1, t) in connections) and ((t, c2) in connections or (c2, t) in connections):
         res.add(tuple(sorted((t,c1,c2))))

print(len(res))