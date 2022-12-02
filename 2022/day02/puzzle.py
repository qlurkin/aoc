import sys

result1 = {
    'A X': 1+3,
    'A Y': 2+6,
    'A Z': 3+0,
    'B X': 1+0,
    'B Y': 2+3,
    'B Z': 3+6,
    'C X': 1+6,
    'C Y': 2+0,
    'C Z': 3+3,
}
result2 = {
    'A X': 3+0,
    'A Y': 1+3,
    'A Z': 2+6,
    'B X': 1+0,
    'B Y': 2+3,
    'B Z': 3+6,
    'C X': 2+0,
    'C Y': 3+3,
    'C Z': 1+6,
}

def parse(filename, result):
    res = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                res.append(result[line])
    return res

def part1(filename):
    return sum(parse(filename, result1))

def part2(filename):
    return sum(parse(filename, result2))


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

