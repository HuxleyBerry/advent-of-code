def get_score_of_card(card_string):
    nums = card_string.split(":")[1]
    [winning, yours] = nums.split(" | ")
    winning = winning.split()
    yours = yours.split()
    count = 0
    for num in yours:
        if num in winning:
            count += 1
    if count > 0:
        return 2**(count-1)
    return 0

with open("input.txt") as file:
    sum = 0
    for line in file:
        sum += get_score_of_card(line)
    print(sum)