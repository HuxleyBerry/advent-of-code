from functools import cache

with open("input.txt") as file:
   towels = file.readline().strip().split(", ")
   file.readline()
   patterns = [l.strip() for l in file.readlines()]

towels_set = set(towels)
longest_pattern = len(max(towels, key=lambda x:len(x)))

@cache
def is_possible(pattern):
   if len(pattern) == 0:
      return True
   for i in range(1, min(longest_pattern+1, len(pattern)+1)):
      if pattern[:i] in towels_set and is_possible(pattern[i:]):
         return True
   return False

print(sum(1 if is_possible(pattern) else 0 for pattern in patterns))