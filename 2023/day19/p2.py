import copy

def get_ranges_size(ranges):
    product = 1
    for k, v in ranges.items():
        product *= (v[1] - v[0] + 1)
    return product
            
def count_passing_ranges(ranges, workflows, tests, test_index):
    category, operation, num, target = tests[test_index]
    if category != None:
        range_start, range_end = ranges[category]
    if operation == None:
        if target == "A":
            return get_ranges_size(ranges)
        elif target == "R":
            return 0
        else:
            return count_passing_ranges(ranges, workflows, workflows[target], 0)
    elif operation == ">":
        if range_end <= num:
            return count_passing_ranges(ranges, workflows, tests, test_index+1)
        elif range_start > num:
            if target == "A":
                return get_ranges_size(ranges)
            elif target == "R":
                return 0
            else:
                return count_passing_ranges(ranges, workflows, workflows[target], 0)
        else:
            # upper passes and moves on to next workflow
            # lower fails and moves on to next test in current workflow
            lower = copy.deepcopy(ranges)
            upper = copy.deepcopy(ranges)
            lower[category] = (range_start, num)
            upper[category] = (num+1, range_end)
            if target == "A":
                upper_count = get_ranges_size(upper)
            elif target == "R":
                upper_count =  0
            else:
                upper_count = count_passing_ranges(upper, workflows, workflows[target], 0)
            return upper_count + count_passing_ranges(lower, workflows, tests, test_index+1)
    elif operation == "<":
        if range_start >= num:
            return count_passing_ranges(ranges, workflows, tests, test_index+1)
        elif range_end < num:
            if target == "A":
                return get_ranges_size(ranges)
            elif target == "R":
                return 0
            else:
                return count_passing_ranges(ranges, workflows, workflows[target], 0)
        else:
            # lower passes and moves on to next workflow
            # upper fails and moves on to next test in current workflow
            lower = copy.deepcopy(ranges)
            upper = copy.deepcopy(ranges)
            lower[category] = (range_start, num-1)
            upper[category] = (num, range_end)
            if target == "A":
                lower_count = get_ranges_size(lower)
            elif target == "R":
                lower_count =  0
            else:
                lower_count = count_passing_ranges(lower, workflows, workflows[target], 0)
            return lower_count + count_passing_ranges(upper, workflows, tests, test_index+1)



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
    rating_ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    print(count_passing_ranges(rating_ranges, workflows, workflows["in"], 0))