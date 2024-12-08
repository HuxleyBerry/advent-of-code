with open("input.txt") as file:
    data = [l.strip().split(": ") for l in file.readlines()]
    data = [(int(r[0]), [int(x) for x in r[1].split()]) for r in data]


def try_everything(target, current, nums_left):
    if len(nums_left) == 0:
        return current == target
    else:
        return try_everything(target, current+nums_left[0], nums_left[1:]) or try_everything(target, current*nums_left[0], nums_left[1:]) or try_everything(target, int(str(current) + str(nums_left[0])), nums_left[1:])
     
total = 0  
for target, nums in data:
    if try_everything(target, nums[0], nums[1:]):
        total += target

print(total)