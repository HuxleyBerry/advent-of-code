def parse(s):
    return tuple(int(q[2:]) for q in s.split(", "))

with open("input.txt") as file:
    machines = file.read().split("\n\n")
    machines = [machine.split("\n") for machine in machines]
    machines = [(parse(a[10:]),parse(b[10:]),parse(prize[7:])) for [a,b,prize] in machines]

def solve_when_paralell(v, w, target):
    if v > w*3:
        a, b = v, w
        switch = False
    else:
        a, b = w, v
        switch = True
    x = min(target//a, 100)
    y = 0
    while True:
        if x < 0:
            return "impossible"
        calc = x*a + y*b
        if calc == target:
            return (x, y) if not switch else (y,x)
        elif calc < target:
            y += 1
        else:
            x -= 1

total = 0
for a, b, prize in machines:
    determinant = (a[0]*b[1] - a[1]*b[0])
    if (determinant == 0):
        # linear combination of each other
        if all(v == 0 for v in (*a, *b)):
            continue
        if a[0]*prize[1] != a[1]*prize[0]:
            continue
        res = solve_when_paralell(a[0], b[0], prize[0])
        if res == "impossible":
            continue
        x, y = res
        if x > 100 or y > 100:
            continue
        total += x*3 + y
    else:
        _x = (b[1]*prize[0] - b[0]*prize[1])
        _y = (-a[1]*prize[0] + a[0]*prize[1])
        x, x_remainder = divmod(_x, determinant)
        y, y_remainder = divmod(_y, determinant)
        if not (x < 0 or y < 0 or x_remainder != 0 or y_remainder != 0 or x > 100 or y > 100):
            # print(x, y)
            total += x*3 + y

print(total)