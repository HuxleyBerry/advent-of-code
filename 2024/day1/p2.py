from collections import defaultdict

with open("input1.txt","r") as file:
    data = [tuple(int(x) for x in l.split()) for l in file.readlines()]

left = [d[0] for d in data]
right = [d[1] for d in data]
occurences = defaultdict(int)
for num in right:
    occurences[num] += 1

print(sum([num*occurences[num] for num in left]))