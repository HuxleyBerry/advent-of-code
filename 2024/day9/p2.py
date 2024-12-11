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

pos = 0
file_starts = [pos]
gap_starts = []
for file_size, gap_size in zip(file_sizes[:-1], gap_sizes):
    pos += file_size
    gap_starts.append(pos)
    pos += gap_size
    file_starts.append(pos)

checksum = 0
gap_sizes_immutable = tuple(gap_sizes)
for file_index in range(len(file_sizes) - 1, -1, -1):
    file_size = file_sizes[file_index] 
    place_found = False
    for index in range(file_index):
        if file_size <= gap_sizes[index]:
            start = gap_starts[index] + gap_sizes_immutable[index] - gap_sizes[index]
            gap_sizes[index] -= file_size
            place_found = True     
            checksum += range_sum(start, start + file_size)*file_index
            break
    if not place_found:
        x = range_sum(file_starts[file_index], file_starts[file_index]+file_size)*file_index
        checksum += x

print(checksum)