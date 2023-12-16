from functools import cmp_to_key

def count_distinct_cards_in_hand(hand):
    occur = set()
    occur_twice = set()
    for h in hand:
        if h != "J":
            if h in occur:
                occur_twice.add(h)
            occur.add(h)
    return len(occur), len(occur_twice)

def get_hand_type(hand):
    occuring, double_occuring = count_distinct_cards_in_hand(hand)
    if occuring <= 1:
        return 6 # five of a kind
    elif occuring == 2:
        if double_occuring != 2:
            return 5 # four of a kind
        else:
            return 4 # full house
    elif occuring == 3:
        if double_occuring != 2:
            return 3 # three of a kind
        else:
            return 2 # two pair
    elif occuring == 4:
        return 1 # one pair
    else:
        return 0

def card_to_num(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "T":
        return 10
    elif card == "J":
        return 1
    else:
        return int(card)

def compare_bids(bid1, bid2):
    hand1, hand2 = bid1[0], bid2[0]
    type1, type2 = get_hand_type(hand1), get_hand_type(hand2)
    if type1 > type2:
        return 1
    elif type1 < type2:
        return -1
    else:
        for card1, card2 in zip(hand1, hand2):
            num1, num2 = card_to_num(card1), card_to_num(card2)
            if num1 > num2:
                return 1
            elif num1 < num2:
                return -1
        return 0

with open("input.txt") as file:
    card_bids = [l.split() for l in file.readlines()]
    card_bids.sort(key=cmp_to_key(compare_bids))
    print(get_hand_type("AJQKA"))
    sum = 0
    for index, bid in enumerate(card_bids):
        sum += (index+1)*int(bid[1])
    print(sum)