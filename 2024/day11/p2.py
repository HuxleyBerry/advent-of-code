with open("input.txt") as file:
    stones = [int(x) for x in file.readline().split()]

def get_descendants(num):
    if num == 0:
        return [1]
    else:
        num_str = str(num)
        if len(num_str)%2 == 0:
            left = int(num_str[:len(num_str)//2])
            right = int(num_str[len(num_str)//2:])
            return [left, right]
        else:
            return [2024*num]
        
def count_descendants_internal(num, iters, memo):
    if iters == 75:
        return 1
    else:
        return sum((count_descendants(desc, iters+1, memo) for desc in get_descendants(num)))
    
def count_descendants(num, iters, memo):
    if (num, iters) in memo:
        return memo[(num, iters)]
    else:
        res = count_descendants_internal(num, iters, memo)
        memo[(num, iters)] = res
        return res
    
memo = {}
    
print(sum((count_descendants(num, 0, memo)) for num in stones))
