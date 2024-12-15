from functools import reduce

with open("input.txt") as file:
   data = [line.strip().split() for line in file]
   data = [(tuple(int(x) for x in p[0][2:].split(",")), tuple(int(x) for x in p[1][2:].split(","))) for p in data]

width = 101
height = 103

def advance(pos, vel):
   global width, height
   x, y = pos
   dx, dy = vel
   return ((x+100*dx)%width, (y+100*dy)%height)

def get_quadrant(pos):
   global width, height
   x,y = pos
   if width%2 == 1 and x == width//2:
      return None
   elif height%2 == 1 and y == height//2:
      return None
   else:
    x_half = 0 if x < width//2 else 1
    y_half = 0 if y < height//2 else 1
    return x_half + 2*y_half
   
quadrants = [0 for i in range(4)]
for pos, vel in data:
    final_quadrant = get_quadrant(advance(pos, vel))
    if final_quadrant is not None:
        quadrants[final_quadrant] += 1

print(reduce(lambda x,y: x*y, quadrants))