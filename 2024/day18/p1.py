import heapq

with open("input.txt") as file:
   corrupted = [tuple(int(x) for x in line.split(",")) for line in file]

width = 71
height = 71
simulate_amount = 1024
unsafe = set(x for x in corrupted[:simulate_amount])

def in_bounds(pos):
   x, y = pos
   return 0 <= x and x < width and 0 <= y and y < height

def get_neighbours(pos):
   x, y = pos
   return ((x, y+1), (x, y-1), (x+1, y), (x-1, y))

pq = [(0, (0,0))]
visited = set((0,0))
while len(pq) != 0:
   cost, pos = heapq.heappop(pq)
   if pos == (width-1, height-1):
      print(cost)
      break
   for neighbour in get_neighbours(pos):
      if in_bounds(neighbour) and neighbour not in visited and neighbour not in unsafe:
         heapq.heappush(pq, (cost+1, neighbour))
         visited.add(neighbour)