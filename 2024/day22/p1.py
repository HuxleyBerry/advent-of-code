from functools import cache
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

@cache
def multi_step(num, steps):
   if steps == 1:
      return step(num)
   else:
      return step(multi_step(num, steps-1))

total = 0
for num in nums:
   total += multi_step(num,2000)

print(total)