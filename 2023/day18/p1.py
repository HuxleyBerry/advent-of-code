directions_dict = {"L": (-1,0), "U": (0,-1), "R": (1,0), "D": (0,1)}

with open("input.txt") as file:
    min_x, max_x, min_y, max_y = 100000, 0, 100000, 0
    current_x, current_y = 0, 0
    visited = {}
    for line in file:
        direction, distance, colour = line.split()
        distance = int(distance)
        colour = colour[1:-1]
        if direction in ("U", "D"):
            visited[(current_x, current_y)] = (direction, colour)
        for i in range(distance):
            current_x += directions_dict[direction][0]
            current_y += directions_dict[direction][1]
            visited[(current_x, current_y)] = (direction, colour)
                
        if current_x > max_x:
            max_x = current_x
        if current_x < min_x:
            min_x = current_x
        if current_y > max_y:
            max_y = current_y
        if current_y < min_y:
            min_y = current_y
    interior_count = 0
    for i in range(min_y, max_y+1):
        most_recent_direction = None
        for j in range(min_x, max_x+1):
            if (j,i) in visited:
                most_recent_direction = visited[(j,i)][0]
            else:
                if most_recent_direction == "U":
                    interior_count += 1
    print(interior_count + len(visited))