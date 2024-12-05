from collections import defaultdict

with open("input.txt") as file:
    contents = file.read()

[orderings, updates] = contents.split("\n\n")
orderings = [tuple(int(x) for x in order.split("|")) for order in orderings.split("\n")]
updates = [tuple(int(x) for x in update.split(",")) for update in updates.split("\n")]

adjacency_list = defaultdict(set)
adjacency_list_reversed = defaultdict(set)
for before, after in orderings:
    adjacency_list[before].add(after)
    adjacency_list_reversed[after].add(before)

pairs = set(orderings)

def get_update_num(update, pairs, adjacency_list, adjacency_list_reversed):
    valid = True
    for i, page1 in enumerate(update):
        if not valid:
            break
        for page2 in update[i+1:]:
            if (page2, page1) in pairs:
                valid = False
                break
    if valid:
        return 0

    update_set = set(update)          
    al = defaultdict(set)
    alr = defaultdict(set)
    for page in update:
        al[page] = adjacency_list[page].intersection(update_set)
        alr[page] = adjacency_list_reversed[page].intersection(update_set)

    S = set(vertex for vertex in al if len(alr[vertex]) == 0)
    toplogically_sorted = []
    while len(S) > 0:
        vertex = S.pop()
        toplogically_sorted.append(vertex)
        outneighbours = al[vertex].copy()
        for neighbour in outneighbours:
            al[vertex].remove(neighbour)
            alr[neighbour].remove(vertex)
            if len(alr[neighbour]) == 0:
                S.add(neighbour)
    assert not any(len(neighbours) > 0 for neighbours in al.values())
    return toplogically_sorted[len(update)//2]

total = 0
for update in updates:
    assert len(update)%2 == 1
    total += get_update_num(update, pairs, adjacency_list, adjacency_list_reversed)

print(total)