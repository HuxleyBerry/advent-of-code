with open("input1.txt","r") as file:
    data = [tuple(int(x) for x in l.split()) for l in file.readlines()]

left = sorted([d[0] for d in data])
right = sorted([d[1] for d in data])
print(sum([abs(a-b) for a,b in zip(left, right)]))