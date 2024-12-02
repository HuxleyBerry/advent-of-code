with open("input.txt","r") as file:
    levels = file.readlines()
    levels = [[int(x) for x in level.split()] for level in levels]

total = 0

def safe(level):
    assert len(level) > 3
    first_diff = level[1] - level[0]
    if first_diff not in (-3,-2,-1,1,2,3):
        return False
    normalised_diff = first_diff//abs(first_diff)
    success = True
    removed_already = False
    i = 1
    while i < len(level)-1:
        diff = level[i+1] - level[i]
        if diff not in (normalised_diff, normalised_diff*2, normalised_diff*3):
            if removed_already:
                success = False
                break
            else:
                if i+2 >= len(level):
                    return True
                removed_already = True
                bonus_diff = level[i+2] - level[i]
                if bonus_diff not in (normalised_diff, normalised_diff*2, normalised_diff*3):
                    success = False
                    break
                else:
                    i += 2
                    continue
        i += 1
    if success:
        return True
    else:
        return False

print(sum([1 if safe(level) or safe(level[::-1]) else 0 for level in levels]))