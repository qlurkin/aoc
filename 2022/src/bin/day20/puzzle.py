import sys

def parse(filename):
    with open(filename) as file:
        numbers = [int(line.strip()) for line in file.readlines()]
    return numbers

def move(L: list, i, delta):
    item = L.pop(i)
    dest = (i+delta)%(len(L))
    if dest == 0:
        dest = len(L)
    L.insert(dest, item)

def find_index(numbers, i):
    for j, number in enumerate(numbers):
        if number[0] == i:
            return j
    raise ValueError("CACA")


def mixxx(numbers: list, n):
    numbers = list(enumerate(numbers))
    res = None
    for _ in range(n):
        for i in range(len(numbers)):
            j = find_index(numbers, i)
            move(numbers, j, numbers[j][1])
    return [number for _, number in numbers]


def part1(filename):
    numbers = parse(filename)
    numbers = mixxx(numbers, 1)
    zero = numbers.index(0)
    i1000 = (zero+1000)%len(numbers)
    i2000 = (zero+2000)%len(numbers)
    i3000 = (zero+3000)%len(numbers)
    return numbers[i1000] + numbers[i2000] + numbers[i3000]

def part2(filename):
    numbers = parse(filename)
    numbers = [x*811589153 for x in numbers]
    numbers = mixxx(numbers, 10)
    zero = numbers.index(0)
    i1000 = (zero+1000)%len(numbers)
    i2000 = (zero+2000)%len(numbers)
    i3000 = (zero+3000)%len(numbers)
    return numbers[i1000] + numbers[i2000] + numbers[i3000]

if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

