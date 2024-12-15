with open("input.txt") as file:
   data = [line.strip().split() for line in file]
   data = [(tuple(int(x) for x in p[0][2:].split(",")), tuple(int(x) for x in p[1][2:].split(","))) for p in data]

width = 101
height = 103

bot_count = len(data)

def advance(pos, vel,i):
   global width, height
   x, y = pos
   dx, dy = vel
   return ((x+i*dx)%width, (y+i*dy)%height)

def is_inner(pos):
   global width, height
   x,y = pos
   return x >= width//4 and x <= (3*width)//4 and y >= height//4 and x <= (3*height)//4 

def get_large_blob(locations):
    central = next((pos for pos in locations if is_inner(pos)))
    blob = {central}
    locations.remove(central)
    while True:
        success = False
        for x, y in locations:
            neighbours = ((x+1,y),(x-1,y),(x,y-1),(x,y+1))
            if any(neighbour in blob for neighbour in neighbours):
                blob.add((x,y))
                locations.remove((x,y))
                success = True
                break
        if not success:
            break
    return blob

def print_tree(locations):
    global width, height
    s = ""
    for i in range(height):
        for j in range(width):
            s += "1" if (j,i) in locations else "."
        s += "\n"

    with open("output.txt","w") as file:
        file.write(s)

for i in range(1,10000):    
    locations = set()
    for pos, vel in data:
        locations.add(advance(pos, vel,i))
    blob = get_large_blob(locations)
    if len(blob) >= 50:
        print_tree(locations)
