with open("input.txt","r") as file:
    levels = file.readlines()
    levels = [[int(x) for x in level.split()] for level in levels]

total = 0
for level in levels:
    if len(level) <= 1:
        total += 1
        continue
    first_diff = level[1] - level[0]
    if first_diff not in (-3,-2,-1,1,2,3):
        continue
    normalised_diff = first_diff//abs(first_diff)
    success = True
    for i in range(1,len(level)-1):
        diff = level[i+1] - level[i]
        if diff not in (normalised_diff, normalised_diff*2, normalised_diff*3):
            success = False
            break
    if success:
        total += 1

print(total)