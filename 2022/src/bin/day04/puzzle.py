import sys

def parse(filename):
    with open(filename) as file:
        res = []
        for line in file:
            line = line.strip()
            if len(line) > 0:
                elve1, elve2 = map(lambda interval: tuple(int(x) for x in interval.split('-')), line.split(','))
                res.append((elve1, elve2))
        return res

def part1(filename):
    count = 0
    for elve1, elve2 in parse(filename):
        # print(elve1, elve2, end=' -> ')
        if elve1[0] <= elve2[0]:
            if elve2[1] <= elve1[1]:
                count += 1
                # print('+1')
                continue
        if elve2[0] <= elve1[0]:
            if elve1[1] <= elve2[1]:
                count += 1
                # print('+1')
                continue
        # print()
    return count

def part2(filename):
    count = 0
    for elve1, elve2 in parse(filename):
        # print(elve1, elve2, end=' -> ')
        if not (elve1[1] < elve2[0] or elve1[0] > elve2[1]):
            count += 1
            # print('+1')
            continue
        # print()
    return count


if __name__ == "__main__":
    part = int(sys.argv[1])
    filename = sys.argv[2]
    if part == 1:
        print(part1(filename))
    if part == 2:
        print(part2(filename))

