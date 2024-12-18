import heapq

with open("input.txt") as file:
   corrupted = [tuple(int(x) for x in line.split(",")) for line in file]

width = 71
height = 71

def in_bounds(pos):
   x, y = pos
   return 0 <= x and x < width and 0 <= y and y < height

def get_neighbours(pos):
   x, y = pos
   return ((x, y+1), (x, y-1), (x+1, y), (x-1, y))

def test_if_possible(simulate_amount):
    pq = [(0, (0,0))]
    visited = set((0,0))
    unsafe = set(x for x in corrupted[:simulate_amount])
    while len(pq) != 0:
        cost, pos = heapq.heappop(pq)
        if pos == (width-1, height-1):
            return True
        for neighbour in get_neighbours(pos):
            if in_bounds(neighbour) and neighbour not in visited and neighbour not in unsafe:
                heapq.heappush(pq, (cost+1, neighbour))
                visited.add(neighbour)
    return False

lower = 0
upper = len(corrupted) - 1
while lower < upper:
    print(lower, upper)
    average = (lower + upper)//2
    if test_if_possible(average):
        lower = average + 1
    else:
        upper = average

print(f"{corrupted[lower-1][0]},{corrupted[lower-1][1]}")