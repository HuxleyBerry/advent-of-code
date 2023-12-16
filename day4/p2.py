def get_score_of_card(card_string):
    nums = card_string.split(":")[1]
    [winning, yours] = nums.split(" | ")
    winning = winning.split()
    yours = yours.split()
    count = 0
    for num in yours:
        if num in winning:
            count += 1
    return count

with open("input.txt") as file:
    card_copies = [1 for i in range(186)]
    for i, line in enumerate(file):
        score = get_score_of_card(line)
        for j in range(i+1, i+1+score):
            card_copies[j] += card_copies[i]
    print(card_copies)
    print(sum(card_copies))