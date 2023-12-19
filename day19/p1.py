def does_accept_part(part, workflows):
    return passes_tests(part, workflows, workflows["in"])

def passes_tests(part, workflows, tests):
    for test in tests:
        category, operation, num, target = test
        if operation == None:
            pass_test = True
        elif operation == ">":
            pass_test = part[category] > num
        elif operation == "<":
            pass_test = part[category] < num 
        if pass_test:
            if target == "A":
                return True
            elif target == "R":
                return False
            else:
                return passes_tests(part, workflows, workflows[target])


with open("input.txt") as file:
    workflows_unparsed, part_ratings_unparsed = file.read().split("\n\n")
    workflows_unparsed = workflows_unparsed.split("\n")
    part_ratings_unparsed = part_ratings_unparsed.split("\n")
    workflows = {}
    for uw in workflows_unparsed:
        name, rest = uw.split("{")
        rules = []
        for rulestring in rest[:-1].split(","):
            if ":" in rulestring:
                left, target = rulestring.split(":")
                rules.append((left[0], left[1], int(left[2:]), target))
            else:
                rules.append((None, None, None, rulestring))
        workflows[name] = rules
    total = 0
    for part_rating in part_ratings_unparsed:
        part_dict = {}
        for assignment in part_rating[1:-1].split(","):
            part_dict[assignment[0]] = int(assignment[2:])
        if does_accept_part(part_dict, workflows):
            part_sum = 0
            for k, v in part_dict.items():
                part_sum += v
            total += part_sum
    print(total)