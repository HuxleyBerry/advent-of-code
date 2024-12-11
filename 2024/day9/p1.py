with open("input.txt") as file:
    data = file.readline().strip()

file_sizes = []
gap_sizes = []
for i, char in enumerate(data):
    if i%2 == 0:
        file_sizes.append(int(char))
    else:
        gap_sizes.append(int(char))

def range_sum(start, end):
    return (end*(end-1) - start*(start-1))//2

checksum = 0
current_gap = 0
pos = file_sizes[0]
gap_sizes_immutable = tuple(gap_sizes)
complete = False
for file_index in range(len(file_sizes) - 1, -1, -1):
    if complete:
        break
    file_size = file_sizes[file_index]
    while file_size > 0:
        if current_gap == file_index - 1:
            complete = True
        if gap_sizes[current_gap] > 0:
            amount = min(gap_sizes[current_gap], file_size) if not complete else file_size
            file_size -= amount
            checksum += range_sum(pos, pos+amount)*file_index
            pos += amount
            gap_sizes[current_gap] -= amount
        elif not complete: # move to next gap
            pos += file_sizes[current_gap+1]
            current_gap += 1
        if complete:
            break

pos = 0
for index in range(file_index+1):
    checksum += range_sum(pos, pos+file_sizes[index])*index
    pos += file_sizes[index] + gap_sizes_immutable[index]

print(checksum)