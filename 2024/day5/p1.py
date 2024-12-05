with open("input.txt") as file:
    contents = file.read()

[orderings, updates] = contents.split("\n\n")
orderings = [tuple(int(x) for x in order.split("|")) for order in orderings.split("\n")]
updates = [tuple(int(x) for x in update.split(",")) for update in updates.split("\n")]

pairs = set(orderings)

def check_update_valid(update, pairs):
    for i, page1 in enumerate(update):
        for page2 in update[i+1:]:
            if (page2, page1) in pairs:
                return False
    return True

total = 0
for update in updates:
    assert len(update)%2 == 1
    if check_update_valid(update, pairs):
        total += update[len(update)//2]

print(total)