from functools import cache
from collections import defaultdict
import sys
sys.setrecursionlimit(2500)

prune_num = 2**24

with open("input.txt") as f:
   nums = [int(x) for x in f]

def step(num):
   num ^= (num*64)
   num %= prune_num
   num ^= (num//32)
   num %= prune_num
   num ^= (num*2048)
   num %= prune_num
   return num

prices = []
for num in nums:
   current = num
   p = [num]
   for i in range(1999):
      current = step(current)
      p.append(current)
   prices.append([x%10 for x in p])

outer_results = []
for num, prices_list in zip(nums, prices):
   results = {}
   for i in range(4,2000):
      differences = (prices_list[i-3] - prices_list[i-4], prices_list[i-2] - prices_list[i-3], prices_list[i-1] - prices_list[i-2], prices_list[i] - prices_list[i-1])
      if differences not in results:
         results[differences] = prices_list[i]
   outer_results.append(results)

totals = defaultdict(int)
for results in outer_results:
   for differences, price in results.items():
      totals[differences] += price

print(max(totals.values()))