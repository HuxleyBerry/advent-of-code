with open("input.txt") as f:
   data = [(line[:2], line[3:5]) for line in f]

edges = set(data)
computers = list(set((c1 for c1, c2 in data)).union(set((c2 for c1, c2 in data))))

def solve(already_picked, min_index):
   best = already_picked
   best_size = -1
   for i in range(min_index, len(computers)):
      if all(((computers[i], picked) in edges or (picked, computers[i]) in edges) for picked in already_picked):
         new_picked = already_picked + [computers[i]]
         res = solve(new_picked, i+1)
         if len(res) > best_size:
            best_size = len(res)
            best = res
   return best

result = solve([], 0)
print(",".join(sorted(result)))